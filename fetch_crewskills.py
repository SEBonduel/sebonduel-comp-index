#!/usr/bin/env python3
"""Génère data/crewskills.json : catalogue des compétences d'équipage WoT
(nom FR + clé + icône officielle), pour afficher le logo de chaque compétence.

Usage : python3 fetch_crewskills.py
"""
import json
import urllib.request
from pathlib import Path

APP_ID = "00eed50e0468215e87ec936f17c52d8f"
OUT = Path(__file__).parent / "data" / "crewskills.json"

# Alias courants (raccourcis) -> clé de compétence, pour le matching côté site.
ALIASES = {
    "commander_sixthSense": ["6e sens", "sixieme sens", "sixième sens", "6ème sens"],
    "brotherhood": ["bia", "freres d'armes", "frères d'armes", "fraternite"],
    "repair": ["reparation", "réparation", "reparations"],
    "camouflage": ["camo", "camouflage"],
    "commander_eagleEye": ["oeil de lynx", "eagle eye"],
    "radioman_finder": ["détection", "detection", "traqueur"],
    "driver_smoothDriving": ["conduite souple"],
    "gunner_smoothTurret": ["rotation souple"],
}


def main():
    url = (f"https://api.worldoftanks.eu/wot/encyclopedia/crewskills/"
           f"?application_id={APP_ID}&language=fr")
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)["data"]

    out = []
    for key, v in data.items():
        img = ((v.get("image_url") or {}).get("big_icon") or "").replace("http://", "https://")
        if not img:
            continue
        out.append({
            "name": v.get("name") or key,
            "skill": v.get("skill") or key,
            "aliases": ALIASES.get(v.get("skill"), []),
            "icon": img,
        })
    out.sort(key=lambda x: x["name"])
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(out)} compétences -> {OUT.relative_to(OUT.parent.parent)}")


if __name__ == "__main__":
    main()
