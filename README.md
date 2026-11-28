# Branche — maquette

Site vitrine : les modèles, les pièces déjà cousues, et un configurateur de
coloris zone par zone.

**Ouvrir `index.html` dans un navigateur.** Pas de serveur, pas d'installation.

## Les fichiers

```
index.html        la page ; les dessins sont regroupés en bas
assets/
  tissus.js       les tissus et les zones de chaque modèle
  tokens.css      les couleurs, la typo, les espacements
  styles.css      les composants
  app.js          le configurateur et les boîtes de dialogue
  favicon.svg
svg/              les dessins, à ouvrir dans Inkscape (modèles et logo)
tools/
  build-svg.py    réinjecte svg/ dans index.html
```

## Modifier quelque chose

| Pour… | Éditer | Puis |
|---|---|---|
| un texte, un prix, une date | `index.html` | recharger |
| une couleur de la charte | `assets/tokens.css` | recharger |
| ajouter ou corriger un tissu | `assets/tissus.js` | recharger |
| le coloris par défaut d'un modèle | `assets/tissus.js` | recharger |
| un dessin ou le logo | `svg/*.svg` dans Inkscape | `python3 tools/build-svg.py` |

Seul le dernier cas demande une commande.

### Ajouter un tissu

Une ligne dans la bonne famille de `assets/tissus.js` :

```js
{ nom: "X-Pak Sunset", hex: "#e8703a" },
```

Il apparaît aussitôt dans toutes les zones qui acceptent cette famille — les
pastilles sont construites à partir de ce fichier, il n'y a rien à ajouter dans
le HTML.

Les familles : `exterieur`, `interieur`, `mixte`, `accessoire`. Une zone
extérieure propose les tissus extérieurs **et** mixtes ; même principe pour
l'intérieur.

### Changer un dessin

Les fichiers de `svg/` sont les originaux Inkscape — les trois modèles et le
logo. Après modification :

```sh
python3 tools/build-svg.py
```

Le script nettoie le SVG, le recadre sur le dessin et l'injecte dans
`index.html`. Il n'a besoin d'aucune dépendance.

Les dessins sont injectés en bas de `index.html`, sous forme de `<symbol>`
que la page référence par `<use>`. C'est ce qui garde le haut du fichier
lisible malgré leur volume.

**Les noms de calques comptent.** Un calque dont le nom figure dans `ZONES`
(en haut de `tools/build-svg.py`) devient une zone colorable : son remplissage
est remplacé par une variable CSS que la page pilote. Renommer un calque sans
mettre `ZONES` à jour fait échouer le script, avec le nom manquant en clair.

Pour rendre un nouveau calque personnalisable : l'ajouter à `ZONES`, puis à la
liste des zones du modèle dans `assets/tissus.js`.

## Pourquoi les dessins sont dans le HTML

Un SVG chargé depuis un fichier séparé (`<img>`, `<object>`) n'hérite pas des
variables CSS de la page : ses zones ne seraient pas colorables. Les `<symbol>`
vivent donc dans `index.html`, regroupés en bas, et `svg/` garde les sources
éditables.

C'est aussi pourquoi `assets/tissus.js` déclare une constante plutôt que d'être
un `.json` : un `fetch()` échoue en `file://`, un `<script src>` non.

## À faire

- les photos du showcase (six emplacements, `Photo à venir` dans `index.html`)
- les textes marqués « provisoire » ou « à préciser »
- les vrais avis clients
