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
