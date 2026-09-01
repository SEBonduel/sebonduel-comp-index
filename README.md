# SEBonduel - Index Compétitif Tier X

Un site façon skill4ltu, mais pour le **jeu en équipe / compétitif** et **uniquement
les chars tier X** de World of Tanks : équipements (jusqu'à 2 compos), directives de
terrain, ordre des compétences d'équipage, consommables, obus et une note de rôle.
Design sombre, image du char en fond de chaque carte, filtres et recherche.

## Structure

```
index.html          le site (statique, hébergeable sur GitHub Pages)
fetch_tanks.py      récupère les chars tier X depuis l'API WG -> data/tanks.json
data/tanks.json     119 chars tier X (id, nom, nation, type, icône, slug)
data/builds.json    les builds compétitifs, clé = slug (rempli à la main)
```

## Remplir un build

Dans `data/builds.json`, ajoute une entrée par char (clé = `slug` de `tanks.json`) :

```json
"is-7": {
  "equipment": [
    { "label": "Standard", "slots": ["Équip. 1", "Équip. 2", "Équip. 3"] },
    { "label": "Alternatif", "slots": ["Équip. 1", "Équip. 2", "Équip. 3"] }
  ],
  "fieldMods": ["Directive 1", "Directive 2"],
  "crew": ["Compétence 1", "Compétence 2", "..."],
  "consumables": ["Conso 1", "Conso 2", "Conso 3"],
  "ammo": "25 APCR · 5 HE",
  "note": "Rôle et stratégie en compétitif."
}
```

- `equipment` : 1 ou 2 compos. Chaque compo a un `label` et 3 `slots`.
- Tout champ vide/absent est simplement masqué. Un char sans build affiche
  « Build à venir » et n'a pas de point vert.

## Regénérer la liste des chars

```bash
python3 fetch_tanks.py
```

## Notes

- Données chars et icônes : **API Wargaming**. Les builds sont du contenu **SEBonduel**.
- Le bouton « blindage 3D » pointe vers **tanks.gg** (best-effort selon le nom du char).
- Site non affilié à Wargaming.net.
