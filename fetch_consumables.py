#!/usr/bin/env python3
"""Génère data/consumables.json : catalogue des consommables WoT (icônes WG + alias).

Même principe que fetch_provisions.py : on associe à chaque consommable son nom
court FR et des alias, pour que les builds affichent la bonne icône.

Usage : python3 fetch_consumables.py
"""
import json
import urllib.request
from pathlib import Path

APP_ID = "00eed50e0468215e87ec936f17c52d8f"
OUT = Path(__file__).parent / "data" / "consumables.json"

# tag exact -> (nom affiché, alias de recherche)
CURATION = [
    ("largeMedkit", "Grande trousse de premiers secours",
     ["trousse de secours", "grande trousse", "trousse", "medkit", "premiers secours"]),
    ("smallMedkit", "Petite trousse de premiers secours", ["petite trousse"]),
    ("largeRepairkit", "Grand kit de réparation",
     ["kit de reparation", "kit de réparation", "grand kit", "repairkit", "reparation"]),
    ("smallRepairkit", "Petit kit de réparation", ["petit kit"]),
    ("autoExtinguishers", "Extincteur automatique",
     ["extincteur automatique", "extincteur auto"]),
    ("handExtinguishers", "Extincteur manuel", ["extincteur manuel", "extincteur"]),
    ("ration", "Rations de combat supplémentaires",
     ["ration de combat", "rations de combat", "ration", "rations", "vivres"]),
    ("chocolate", "Chocolat", ["chocolat"]),
    ("cocacola", "Caisse de Cola", ["cola"]),
    ("hotCoffee", "Café fort", ["cafe fort", "café fort"]),
    ("ration_uk", "Pudding et thé", ["pudding"]),
    ("ration_japan", "Onigiri", ["onigiri"]),
    ("ration_china", "Rations de combat améliorées", ["rations ameliorees"]),
    ("ration_italy", "Spaghetti bolognaise", ["spaghetti"]),
    ("ration_poland", "Tartines de Smalec", ["smalec", "tartines"]),
    ("ration_czech", "Buchty", ["buchty"]),
    ("ration_sweden", "Café avec brioches à la cannelle", ["brioches", "cannelle"]),
    ("regenerationKit", "Récupération", ["recuperation", "récupération"]),
]


def main():
    url = (f"https://api.worldoftanks.eu/wot/encyclopedia/provisions/"
           f"?application_id={APP_ID}&language=fr")
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)["data"]

    by_tag = {v.get("tag"): v for v in data.values() if v.get("tag")}
    out = []
    for tag, name, aliases in CURATION:
        v = by_tag.get(tag)
        icon = (v or {}).get("image") or ""
        if not icon:
            print(f"  warn: icône introuvable pour {tag}")
            continue
        out.append({"name": name, "aliases": aliases,
                    "icon": icon.replace("http://", "https://")})

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(out)} consommables -> {OUT.relative_to(OUT.parent.parent)}")


if __name__ == "__main__":
    main()
