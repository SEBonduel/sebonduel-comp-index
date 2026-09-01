#!/usr/bin/env python3
"""Récupère les chars tier X depuis l'API WG et écrit data/tanks.json.

Sortie : liste [{id, name, nation, type, tier, premium, icon, slug}] triée par
nation puis nom. `icon` en https (pour un site GitHub Pages). `slug` sert de clé
stable pour les builds et pour le lien viewer d'armure.

Usage : python3 fetch_tanks.py
"""
import json
import re
import urllib.request
from pathlib import Path

APP_ID = "00eed50e0468215e87ec936f17c52d8f"
OUT = Path(__file__).parent / "data" / "tanks.json"

TYPE_FR = {
    "lightTank": "Léger", "mediumTank": "Moyen", "heavyTank": "Lourd",
    "AT-SPG": "Chasseur", "SPG": "Artillerie",
}
NATION_FR = {
    "ussr": "URSS", "germany": "Allemagne", "usa": "USA", "france": "France",
    "uk": "R.-U.", "china": "Chine", "japan": "Japon",
    "czech": "Tchécosl.", "poland": "Pologne", "sweden": "Suède", "italy": "Italie",
}


def slugify(name):
    s = name.lower()
    s = s.replace("ö", "o").replace("ä", "a").replace("ü", "u").replace("é", "e")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def main():
    url = (f"https://api.worldoftanks.eu/wot/encyclopedia/vehicles/"
           f"?application_id={APP_ID}&tier=10"
           f"&fields=tank_id,name,short_name,nation,type,tier,is_premium,images.big_icon")
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)["data"]

    tanks = []
    for v in data.values():
        icon = (v.get("images") or {}).get("big_icon") or ""
        icon = icon.replace("http://", "https://")
        name = v.get("short_name") or v.get("name")
        tanks.append({
            "id": v["tank_id"],
            "name": name,
            "nation": v["nation"],
            "nation_fr": NATION_FR.get(v["nation"], v["nation"]),
            "type": v["type"],
            "type_fr": TYPE_FR.get(v["type"], v["type"]),
            "tier": v["tier"],
            "premium": bool(v.get("is_premium")),
            "icon": icon,
            "slug": slugify(name),
        })

    tanks.sort(key=lambda t: (t["nation_fr"], t["name"]))
    OUT.write_text(json.dumps(tanks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(tanks)} chars tier X -> {OUT.relative_to(OUT.parent.parent)}")


if __name__ == "__main__":
    main()
