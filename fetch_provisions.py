#!/usr/bin/env python3
"""Génère data/equipment.json : catalogue des équipements compétitifs (icônes WG
officielles + alias), pour que les builds affichent l'icône du bon équipement.

L'icône d'une famille est la même quel que soit le niveau/classe (ex. rammer.png).
On associe à chaque famille un nom court FR + des alias (ce que tu peux écrire dans
les builds : « rammer », « stab », « turbo »…). Le site fait le matching.

Usage : python3 fetch_provisions.py
"""
import json
import urllib.request
from pathlib import Path

APP_ID = "00eed50e0468215e87ec936f17c52d8f"
OUT = Path(__file__).parent / "data" / "equipment.json"

# famille (fragment de tag) -> (nom court affiché, alias de recherche)
CURATION = [
    ("aimingStabilizer", "Stabilisateur vertical",
     ["stab", "vstab", "stabilisateur", "stab vertical", "stab. vertical", "stabilisateur vertical"]),
    ("rammer", "Fouloir de canon",
     ["rammer", "fouloir", "fouloir de canon", "chargement", "rassembleur"]),
    ("improvedVentilation", "Ventilation améliorée",
     ["vents", "ventilation", "ventilo", "ventilation améliorée"]),
    ("coatedOptics", "Optiques traitées",
     ["optique", "optiques", "optics", "optique améliorée", "optiques traitées"]),
    ("enhancedAimDrives", "Système de visée",
     ["aiming", "visée", "systeme de visee", "système de visée", "aim drives", "drives"]),
    ("turbocharger", "Turbocompresseur",
     ["turbo", "turbocompresseur", "compresseur"]),
    ("improvedRotationMechanism", "Mécanisme de rotation",
     ["irm", "rotation", "mécanisme de rotation", "mecanisme de rotation"]),
    ("extraHealthReserve", "Durcissant amélioré",
     ["durcissant", "durcissement", "hardening", "extra health", "résistance", "resistance", "pv"]),
    ("antifragmentationLining", "Revêtement anti-éclats",
     ["revetement", "revêtement", "spall", "spall liner", "anti-éclats", "anti eclats", "revêtement anti-éclats"]),
    ("commandersView", "Vision du chef de char",
     ["cvs", "vision", "chef de char", "commander", "vision du chef"]),
    ("additionalInvisibilityDevice", "Silencieux d'échappement",
     ["lnes", "silencieux", "échappement", "echappement", "exhaust", "invisibilité"]),
    ("stereoscope", "Télescope binoculaire",
     ["binoculaire", "binocs", "télescope", "telescope", "stereoscope", "jumelles"]),
    ("grousers", "Crampons de chenilles",
     ["crampons", "grousers", "chenilles"]),
    ("improvedConfiguration", "Configuration modifiée",
     ["config", "configuration", "wet ammo", "munitions", "configuration modifiée"]),
    ("improvedSights", "Visée améliorée",
     ["visée améliorée", "visee amelioree", "sights", "viseur"]),
    ("improvedRadioCommunication", "Équipement radio",
     ["radio", "équipement radio", "equipement radio"]),
]


def main():
    url = (f"https://api.worldoftanks.eu/wot/encyclopedia/provisions/"
           f"?application_id={APP_ID}&language=fr")
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)["data"]

    # icône par fragment de tag (première correspondance ; même image par famille)
    icon_by_frag = {}
    for v in data.values():
        tag = v.get("tag", "")
        img = (v.get("image") or "").replace("http://", "https://")
        for frag, _, _ in CURATION:
            if tag.startswith(frag) and frag not in icon_by_frag and img:
                icon_by_frag[frag] = img

    out = []
    for frag, name, aliases in CURATION:
        icon = icon_by_frag.get(frag)
        if not icon:
            print(f"  warn: icône introuvable pour {frag}")
            continue
        out.append({"name": name, "aliases": aliases, "icon": icon})

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(out)} équipements -> {OUT.relative_to(OUT.parent.parent)}")


if __name__ == "__main__":
    main()
