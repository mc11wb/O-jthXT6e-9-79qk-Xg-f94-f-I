# BoosterStop — pages distributeurs + SEO local

Décompresse et dépose le contenu à la racine du dépôt en conservant
l'arborescence. Les chemins correspondent exactement à ceux du dépôt.

## Fichiers NOUVEAUX (16)

Hub, un par langue :

    distributeurs-geneve.html
    fr/distributeurs-geneve.html

Sept emplacements, un fichier par langue :

    distributeur-geneve-rive.html          fr/distributeur-geneve-rive.html
    distributeur-geneve-charmilles.html    fr/distributeur-geneve-charmilles.html
    distributeur-petit-lancy.html          fr/distributeur-petit-lancy.html
    distributeur-geneve-plainpalais.html   fr/distributeur-geneve-plainpalais.html
    distributeur-meyrin.html               fr/distributeur-meyrin.html
    distributeur-thonex.html               fr/distributeur-thonex.html
    distributeur-carouge.html              fr/distributeur-carouge.html

Les noms de fichiers sont identiques en FR et EN : c'est ce que la
logique de `nav.html` attend pour construire le sélecteur de langue.

## Fichiers MODIFIÉS (6) — ils écrasent les tiens

    _includes/nav.html
    _includes/footer.html
    assets/site.css
    index.html
    fr/index.html
    sitemap.xml

### _includes/nav.html
Le lien « Emplacements / Locations » pointait sur l'ancre `#where` de
l'accueil. Il pointe maintenant sur la page hub, qui est une vraie page
indexable. Aucun autre lien du menu n'a bougé.

### _includes/footer.html
Ajout d'un bloc « Nos distributeurs à Genève » avec les 7 liens, juste
avant la nav mobile. C'est le maillage interne qui fait remonter les
pages emplacement.

### assets/site.css
Ajout à la fin du fichier des règles `.footer-locs`, `.fl-title`,
`.fl-links`, `.fl-all`. Rien de supprimé, rien de modifié au-dessus.

### index.html et fr/index.html
Les 7 blocs `Store` empilés dans le JSON-LD de l'accueil sont retirés :
chaque établissement vit désormais sur sa propre page. À la place, un
`ItemList` pointe vers les 7 pages. `Organization`, `WebSite` et
`FAQPage` sont conservés tels quels. Le HTML visible n'est pas touché.

### sitemap.xml
Passe de 12 à 28 URL, avec les alternates hreflang pour chaque paire.

## Jours fériés genevois

Les pages connaissent les 9 jours fériés du canton (loi J 1 45) :
Nouvel An, Vendredi-Saint, lundi de Pâques, Ascension, lundi de
Pentecôte, 1er août, Jeûne genevois, Noël, 31 décembre. Le 1er mai
n'est pas férié à Genève et n'y figure donc pas.

Cinq de ces dates se déplacent chaque année. Elles sont **calculées**
en JavaScript, pas listées : le badge « Fermé — jour férié » restera
juste sans que tu aies à toucher au code. Le calcul a été contrôlé
contre les dates publiées par ge.ch pour 2026.

Le JSON-LD contient en plus 27 fermetures exceptionnelles
(`specialOpeningHoursSpecification`), de 2026 à 2028. À regénérer vers
2028 si tu veux garder trois ans d'avance — le badge, lui, n'expire
jamais.

**Un cas à vérifier** : le 1er août 2027 tombe un dimanche. La loi
genevoise reporte le férié au lendemain pour les entreprises non
soumises à la loi fédérale sur le travail. Si La Poste ferme le lundi
2 août 2027, il faudra l'ajouter à la main — c'est le seul cas des
trois prochaines années.

## Coordonnées corrigées

Trois emplacements étaient mal géolocalisés dans le dépôt. Les pages
utilisent maintenant les coordonnées Google :

    Rive           46.2008, 6.1520    →  46.201946, 6.1504446   (~170 m)
    Charmilles     46.2112, 6.1268    →  46.2080238, 6.1230909  (~450 m)
    Petit-Lancy    46.1872, 6.1214    →  46.1889447, 6.1104449  (~850 m)

Les quatre autres étaient justes.

**À faire de ton côté** : reporter ces trois corrections dans le tableau
`MACHINES` de `stock.html` et `fr/stock.html` (ligne ~432), sinon la
carte de la page Stock reste décalée. Je n'ai pas touché à ces deux
fichiers pour ne pas interférer avec ton code live.

## À faire après l'upload

1. Repointer les 7 fiches Google vers leur page respective, en FR,
   avec une UTM par fiche pour pouvoir mesurer.
2. Saisir les jours fériés en « horaires exceptionnels » sur les 7
   fiches Google. Sans ça Google affiche « ouvert » ces jours-là et
   quelqu'un se déplace pour rien.
3. Soumettre le nouveau sitemap dans Search Console.
