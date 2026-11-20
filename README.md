# boosterstop.com — structure du site

Site statique hébergé sur GitHub Pages, assemblé par **Jekyll** (intégré à GitHub Pages, rien à installer).
Le header, le footer, la nav mobile et la bannière cookies sont écrits **une seule fois** dans `_includes/` et injectés dans les 12 pages au moment du déploiement.

```
_config.yml              configuration Jekyll (ne pas supprimer)
_includes/
  head.html              <head> commun : GA4 + consentement, viewport, favicon, polices, site.css
  nav.html               header (menu + switch EN/FR)
  footer.html            footer + nav mobile + bannière cookies + site.js
assets/
  site.css               CSS de l'habillage commun
  site.js                JS commun (bannière cookies, consentement GA4)
index.html, stock.html, licences-geneve.html, expansion.html, newsletter.html, privacy.html   → versions EN
fr/…                     mêmes pages en FR
```

## Modifier le menu, le footer, la bannière cookies

Éditer **uniquement** le fichier concerné dans `_includes/`, commit, et les 12 pages sont à jour après le déploiement (1 à 2 min, onglet Actions du dépôt).

- Ajouter un lien dans le menu → `_includes/nav.html` (une ligne `<li>` ; les textes EN/FR sont côte à côte avec `{% if fr %}…{% else %}…{% endif %}`)
- Couleurs, tailles, espacement du header/footer → `assets/site.css`
- Texte de la bannière cookies → `_includes/footer.html`

## Anatomie d'une page

```html
---
lang: en          ← en ou fr
page: stock       ← index | stock | licences-geneve | expansion | newsletter | privacy
---
<!DOCTYPE html>
<html lang="en">
<head>
{% include head.html %}
<title>…</title>            ← SEO propre à la page : title, description, canonical, hreflang, OG, JSON-LD
<style> … CSS propre à la page … </style>
</head>
<body>
{% include nav.html %}
… contenu de la page …
{% include footer.html %}
… scripts propres à la page …
</body>
</html>
```

Les 4 premières lignes (`---` … `---`) sont **obligatoires** et doivent rester tout en haut du fichier : c'est ce qui dit à Jekyll de traiter la page. `lang` et `page` pilotent les liens du menu (racine ou `/fr/`), l'entrée active et le switch EN/FR.

## Créer une nouvelle page

1. Copier `privacy.html` (la plus simple), changer `page:` dans le front matter, le `<title>`, les metas, le contenu.
2. Copier dans `fr/` avec `lang: fr`.
3. Ajouter le lien dans `_includes/nav.html` si elle doit apparaître au menu, et l'URL dans `sitemap.xml`.

## Ajouter / connecter une machine

Tout part du tableau `MACHINES` en haut du `<script>` de `stock.html` (et `fr/stock.html`) :

```js
{ name: 'La Poste de Carouge', addr: '…', lat: 46.1835, lng: 6.1375, worker: null }
```

`worker` est l'index appelé sur le Cloudflare Worker :

- `worker: 0` à `7` → la machine est connectée, le stock live s'affiche
- `worker: null` → la machine est installée mais pas encore branchée : le site affiche « Stock live bientôt » à la place des étages, et l'onglet porte un liseré jaune

Index actuels du Worker : `0` Rive (4017), `1` Charmilles (3996), `2` Petit-Lancy (3995), `3` King Jouet Carouge (4260), `4` La Poste de Carouge (4259), `5` Plainpalais (4261), `6` King Jouet Ecublens (4262, l'ancienne machine de Meyrin), `7` Thônex (4258) — ordre de `MACHINE_IDS` dans le Worker : toujours ajouter à la fin, ne jamais réordonner.

Les huit machines suisses sont branchées (sept à Genève, une à Ecublens). **Pour en brancher une nouvelle** : ajouter son id zhongdacloud à la fin de `MACHINE_IDS` dans le Worker, puis remplacer `null` par ce nouvel index dans `stock.html`, `fr/stock.html` et ses pages distributeur (`WORKER_INDEX`). Passer aussi `live: true` dans `_data/machines.yml`.

Ajouter une machine = une ligne dans `MACHINES` + un `<button class="machine-tab">` dans le panneau `#panel-ch`, + un bloc `Store` dans le JSON-LD de `index.html` pour le SEO local.

## Déplacement temporaire d'une machine (travaux, fermeture)

Exemple en cours : en novembre 2026, la machine de La Poste de Thônex est installée à La Poste des Eaux-Vives pendant les travaux de Thônex.

- Tout se règle dans `_data/machines.yml`, bloc `temporaire` de la machine : `actif: true`, puis le nom, l'adresse, les coordonnées et les horaires de l'emplacement provisoire, et `retour` (le texte affiché après « Retour à Thônex prévu »).
- **Retour à la normale : passer `actif: false`** (ou supprimer le bloc). Rien d'autre à retoucher, toutes les pages reprennent l'adresse habituelle au déploiement suivant.
- `_includes/machine.html` lit ce bloc et fournit les variables `mx_…` (nom, adresse, horaires, phrase d'information). Il est appelé avec `id="thonex"` par Stock Live, la carte de l'accueil, la page de la machine, la page Distributeurs, les listes des pages licences, la presse, le pied de page, l'encart du blog et `llms.txt`.
- L'adresse de la page ne change pas (`distributeur-thonex.html`), ni son titre : seul un bandeau jaune « Emplacement provisoire » s'ajoute. Le Worker non plus : c'est la même machine (index 7).
- Les distances par quartier (Chêne-Bourg, Chêne-Bougeries, Les Eaux-Vives, Champel) de `cartes-pokemon-geneve.html` et `distributeurs-geneve.html` sont écrites en dur pour l'emplacement « Eaux-Vives » : pour un autre emplacement provisoire, elles gardent les valeurs de Thônex et sont à recalculer.
- Les phrases générales qui citent les six filiales La Poste (accueil, expansion, FAQ des pages licences) et la liste de la newsletter ne changent pas.

## Pièges à connaître

- Jekyll interprète `{{ … }}` et `{% … %}` dans les pages. Si un jour du JavaScript en contient, entourer le `<script>` de `{% raw %}` … `{% endraw %}`.
- Les dossiers et fichiers commençant par `_` ne sont pas publiés (c'est voulu pour `_includes`).
- Les scripts Python (`*.py`) et ce README sont exclus de la publication via `_config.yml`.

## Migration (à faire une seule fois dans le dépôt GitHub)

1. **Supprimer le fichier `.nojekyll`** à la racine du dépôt (il désactive Jekyll).
2. Uploader le contenu de cette archive : les 6 pages racine, le dossier `fr/`, les dossiers `_includes/` et `assets/`, et `_config.yml`. Les fichiers du même nom remplacent les anciens.
3. Vérifier dans Settings → Pages que la source est **« Deploy from a branch »** (c'est ce mode qui lance Jekyll).
4. Attendre la fin du déploiement (onglet Actions, 1 à 2 min), puis contrôler : menu, switch EN/FR, bannière cookies, nav mobile sur une page EN et une page FR.
5. Ne pas toucher à `CNAME`, `robots.txt`, `sitemap.xml`, `llms.txt`, `404.html`, images : ils sont copiés tels quels.

## Langues

- `_data/langues.yml` : les langues du site. `complet: true` = EN, FR, NL (menu et pied de page traduits). AR (arabe, de droite à gauche) a les pages principales, générées depuis l'anglais par /i18n/make_ar.py ; DE, ES, IT, PT, SV, NO, DA, FI n'ont que la page Partenaire local ; sur les autres pages, le menu de langue les propose dans un groupe « Page partenaire local ».
- `_data/i18n.yml` : tous les textes du menu, du pied de page, de la barre mobile et de la bannière cookies, par langue.
- Menu de langue (`_includes/nav.html`) : pour chaque langue, il cherche la même page dans le dossier de la langue (`/nl/stock.html`…). Si elle n'existe pas, il renvoie vers l'accueil de cette langue.
- `{% include hreflang.html %}` dans le `<head>` de chaque page écrit le canonical et tous les hreflang tout seul : traduire une page = créer le fichier au même nom dans le dossier de la langue, rien d'autre à retoucher (penser au `sitemap.xml`).
- Liens du menu et du pied de page : `{% include lien.html f="stock.html" %}` donne la page dans la langue du menu, ou la version anglaise si elle n'est pas encore traduite.
- Pages NL : accueil, stock, expansion, accueillir une machine, newsletter, confidentialité, rachat, presse, partenaire local. Les pages propres à Genève renvoient vers l'anglais.
- Page Partenaire local : un seul gabarit (`_layouts/partenaire.html`), textes et pays dans `_data/partenaire.yml`. Ajouter un pays = une entrée dans `pays`.

## Belgique

- Les 5 machines (Carrefour) sont dans `_data/machines.yml` (`pays: be`) : adresse FR/NL, coordonnées, textes propres à chaque lieu.
- Pages générées par `_layouts/belgique.html` (textes : `_data/belgique.yml`) en FR, NL et EN : une page par machine (`distributeur-….html`) et `distributeurs-belgique.html`.
- L'accueil (onglet Belgique de la carte), Stock Live, Expansion, le pied de page et l'encart « où acheter » du blog lisent les mêmes données : ajouter une machine belge = une entrée dans `machines.yml` + ses 3 petits fichiers de page.
- Le menu « Locaties » de la version NL mène à la page Belgique (`nav_emplacements_f` dans `_data/i18n.yml`).
- **Stock en direct.** Les machines belges sont sur un autre compte zhongdacloud que la Suisse ; le même Worker lit les deux (secrets `ZHONGDA_USER_BE` et `ZHONGDA_PASS_BE`). Index du Worker : `8` Korbeek-Lo (4236), `9` Mechelen/Zemst (4237), `10` Tomberg (4255), `11` Gosselies (4256), `12` La Louvière (4257). Le champ `worker` de `machines.yml` suffit : la page de la machine (`_layouts/belgique.html`), l'onglet Belgique de Stock Live (`_includes/stock-be.html` et `stock-be-script.html`) et le relevé du matin le lisent. Sans `worker`, la machine affiche « Stock live bientôt ». Prix en euros.
- **Horaires.** Le champ `ouverture` de `machines.yml` (lundi à dimanche, horaires habituels du magasin) remplit le tableau des pages machines et colore les pastilles de la carte de l'accueil (vert = ouvert, heure de Bruxelles). Les jours fériés légaux belges ne sont jamais affichés « ouvert ». Logique : `_includes/be-ouverture.html`.
- L'onglet Belgique de Stock Live a sa carte (`#beMap`), créée quand l'onglet s'affiche.
- Lien direct vers une machine belge sur Stock Live : `stock.html?pays=be&machine=be-gosselies` (id de `machines.yml`).
- Novembre 2026 : la machine de Zandhoven est passée au Carrefour Gosselies. `distributeur-zandhoven.html` (EN, FR, NL) redirige vers `distributeur-gosselies.html`.

## Newsletter (une par pays)

- Gabarit unique `_layouts/newsletter.html`, textes et pays dans `_data/newsletter.yml`. `newsletter.html`, `fr/`, `nl/` et `ar/newsletter.html` ne contiennent que leur front matter (`layout: newsletter`). Ne plus les régénérer avec make_ar.py : l'arabe est dans `_data/newsletter.yml`.
- Le visiteur choisit **un seul pays** (Suisse, Belgique, Émirats « bientôt »). La page affiche l'offre de ce pays et envoie l'inscription avec `pays` (CH, BE, AE), `liste` (newsletter-ch, newsletter-be, newsletter-ae), le texte exact du consentement et un sujet « [BoosterStop BE] … ».
- Chaque pays a son `endpoint` Formspree : un formulaire par pays = une liste Brevo par pays = un email de bienvenue (et donc un code) par pays. Le code n'est jamais écrit sur la page.
- Lien direct vers un pays : `/newsletter.html#be` (ou `?pays=be`). Sans lien, la page présélectionne selon le fuseau horaire (Zurich, Bruxelles, Dubaï), puis la langue (NL → Belgique, AR → Émirats).
- Après l'inscription, un bloc **facultatif** « Personnalisez votre newsletter » demande prénom, distributeur habituel (liste lue dans `_data/machines.yml` selon le pays, masquée s'il n'y en a pas) et anniversaire (jour et mois, jamais l'année). Il part au même endpoint avec `type: profil`, la même adresse email, `distributeur` (id de machines.yml), `distributeur_nom` et `anniversaire` au format JJ-MM. L'inscription elle-même ne demande toujours que pays, jeux, email et consentement.
- Dans Brevo : attributs PRENOM, DISTRIBUTEUR et ANNIVERSAIRE (texte JJ-MM) à mettre à jour sur le contact existant (même email).
- Ajouter un pays = une entrée dans `pays:` de `_data/newsletter.yml`, avec sa couleur dans le gabarit (`[data-pays="xx"]`).

## Relevé du stock (SEO)

- `.github/workflows/stock-releve.yml` lance chaque matin `.github/scripts/stock_releve.py`, qui interroge le Worker pour chaque machine ayant un `worker` dans `machines.yml` et écrit `_data/stock.json`.
- Les pages machines (`{% include stock-releve.html %}`) et Stock Live (`{% include stock-liste.html %}`) affichent ce relevé en texte, lisible par Google. Le navigateur le remplace par le stock en direct ; si la machine ne répond pas, le relevé reste affiché.
- Lancer un relevé à la main : onglet Actions > « Relevé du stock » > Run workflow.
- Brancher une machine belge sur le stock en direct : l'ajouter à la fin du tableau `MACHINES` du Worker (compte `be`), puis lui donner cet index dans le champ `worker` de `machines.yml`.
