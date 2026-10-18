# Sous la Surface : fabrication et publication quotidienne

Compte Instagram @souslasurface1mn et TikTok « Sous La Surface ».
Promesse : ce que personne ne t'explique, en 1 minute. **Le compte doit être varié** : la mer et les lois cachées ne sont que deux rubriques parmi d'autres.

Rubriques (tourner entre elles, jamais la même deux jours de suite, et pas plus de 2 fois par semaine pour une même rubrique) :
- **Actualité expliquée** : 2 fois par semaine, le mardi et le vendredi (voir la règle plus bas)
- **Maths et probabilités**
- **Argent et économie**
- **Mer et commerce mondial**
- **Science, nature et corps humain**
- **Histoire et inventions**
- **Psychologie et biais du cerveau**
- **Tech et internet**

### Règle « Actualité expliquée » (mardi et vendredi)
- Chercher sur le web les sujets des 7 derniers jours (WebSearch en mode extended) et choisir un sujet qui cache un **mécanisme** à expliquer (pourquoi les prix montent, comment marche telle technologie, ce que change telle décision…), pas une simple info.
- Au moins **deux sources sérieuses** concordantes pour chaque fait, avec la date affichée à l'écran (« au 21 octobre 2026 »).
- Ton neutre et factuel : sur un sujet politique disputé, expliquer les mécanismes et les positions sans donner d'avis.
- Pas de drame humain exploité (morts, catastrophes, faits divers) comme accroche.
- Si un fait évolue d'heure en heure (conflit en cours, crise), ne pas l'affirmer comme acquis : le dater ou choisir un autre sujet.
- Mettre le sujet dans `SUJETS.md` avec la mention « actualité » avant de le traiter.

Le propriétaire valide la vidéo du jour s'il le souhaite. **Sans réponse de sa part, la vidéo est publiée quand même à 18 h.**

## Règles du propriétaire (non négociables)

- Pas de voix off.
- Pas d'emojis, ni dans les vidéos ni dans les légendes.
- Ne jamais terminer par « Demain : … ». La chute se termine par « Abonne-toi. » seul.
- Garder la direction artistique : fond bleu nuit, doré, typo Inter Display + chiffres en mono (constantes dans `pipeline/lib.py`).
- Garder la structure du pilote (épisodes 001 et 002). **La musique doit varier** : `pipeline/music.py` propose 5 ambiances (chill, piano, electro, guitare, cinema) choisies automatiquement d'après le numéro d'épisode. Ne pas forcer deux fois de suite la même (variable `MUSIC_STYLE` dans l'épisode seulement si besoin).
- Français, tutoiement, phrases courtes et directes.
- **Sujet géographique (routes, ports, détroits, pays) : toujours une vraie carte du monde**, avec `pipeline/worldmap.py` (contours Natural Earth, routes maritimes réalistes, ports). Exemple dans `ep002`.
- Chiffres vérifiés uniquement. Jamais de chiffre inventé. Sujet finance : contenu éducatif, jamais de conseil personnalisé.

## Structure d'un épisode (60 à 70 s)

1. **Accroche, 0–4 s** : affirmation choc qui surgit mot par mot, et quelque chose bouge dès la première image.
2. **Enjeu, 4–12 s** : pourquoi c'est surprenant, ce que l'intuition dirait.
3. **La question** : posée en gros, puis gardée en bandeau en haut tant qu'on n'a pas la réponse.
4. **La preuve, ~13–30 s** : une démonstration visuelle animée (compteurs, remplissage, carte, calendrier…). Jamais d'écran figé plus de 3 s.
5. **La réponse, ~30–36 s** : le chiffre clé en très gros.
6. **Le retournement, ~36–48 s** : « Pourquoi ? » / « Le secret ? » puis le mécanisme caché, en visuel. La batterie de la musique s'arrête sur ce passage (≈ 35–40 s), c'est voulu.
7. **L'escalade, ~48–56 s** : l'idée appliquée à plus grande échelle.
8. **La chute, 56 s → fin** : phrase à retenir (2 lignes, la 2e en doré), puis encart « Abonne-toi. ».

Repères de mise en page (1080×1920) : texte entre y≈230 et y≈1550 (le bas est caché par les boutons des applis), largeur de texte ≤ 940 px, bandeau-question à y≈296.

## Procédure du jour (tâche planifiée de 12 h)

1. `cd pipeline && bash setup.sh`
2. Choisir le sujet : le mardi et le vendredi, un sujet d'actualité (règle ci-dessus). Les autres jours, le premier sujet « à faire » de `SUJETS.md` dont la rubrique est différente de celle de la veille (dernière ligne de `PUBLICATIONS.md`). Quand il reste moins de 10 sujets « à faire », en ajouter 10 nouveaux, variés, dans plusieurs rubriques.
3. Vérifier chaque chiffre avec une recherche web et garder les sources. Si un chiffre n'est pas vérifiable, le retirer ou formuler une fourchette prudente.
4. Écrire `pipeline/episodes/epNNN_slug.py` en partant de `ep001` ou `ep002` (mêmes helpers `words`, `bump`, `big_center` depuis `kinetic.py`, même `sfx_events()`).
5. Contrôle visuel : `python3 build.py episodes/epNNN_slug.py --stills 2 8 14 22 31 40 46 53 62`, assembler une planche et la regarder. Corriger les chevauchements une fois.
6. Rendu : `python3 build.py episodes/epNNN_slug.py ../videos/AAAA-MM-JJ-slug.mp4`. Vérifier durée vidéo = audio et volume entre -17 et -15 LUFS (`ffmpeg -i f.mp4 -af ebur128 -f null -`).
   Puis la story teaser : `python3 story.py ../videos/AAAA-MM-JJ-slug.mp4 "Titre court du sujet"` (crée `AAAA-MM-JJ-slug-story.mp4`, 8 s).
7. Commit de la vidéo, de la story et du script, push sur `main`.
8. Vérifier que `https://raw.githubusercontent.com/icaresolaire-alt/souslasurface/main/videos/AAAA-MM-JJ-slug.mp4` et `...-story.mp4` répondent 200 avec la bonne taille.
9. Programmer dans Metricool (`createScheduledPost`) :
   - `blogId` : `7503487`, date du jour à **18:00** Europe/Paris
   - `providers` : instagram et tiktok
   - `media` : le lien raw GitHub ci-dessus
   - `instagramData` : `{"type": "REEL", "showReelOnFeed": true}`
   - `tiktokData` : **`title` obligatoire** (court), `privacyOption` `PUBLIC_TO_EVERYONE`
   - `autoPublish` true, `draft` false
   - Légende : 2 à 3 phrases sans emoji, puis une ligne de 4 à 6 hashtags.
   Puis la story, dans un second `createScheduledPost` :
   - date du jour à **18:15** Europe/Paris, `providers` : instagram **seul** (TikTok ne prend pas les stories via Metricool)
   - `media` : le lien raw de `...-story.mp4`, `instagramData` : `{"type": "STORY"}`
   - **pas de champ `text`** (une story publiée seule n'a pas de légende)
   - La story n'est pas cliquable (limite d'Instagram pour les publications automatiques), c'est normal.
10. Envoyer au propriétaire la vidéo (fichier) + la légende + le lien Metricool (et signaler que la story part à 18 h 15), en disant : « Publication automatique à 18 h. Réponds "annule" avant 18 h pour l'arrêter. » Si on reçoit « annule », passer le post et la story en brouillon avec `updateScheduledPost` (draft true).
11. Mettre à jour `SUJETS.md` (statut) et `PUBLICATIONS.md` (date, sujet, fichier, sources), commit et push.

En cas d'échec d'une étape : ne pas publier une vidéo non vérifiée, et prévenir le propriétaire de ce qui a bloqué.

## Données

- `pipeline/data/ne_50m_land.geojson` : contours des terres, Natural Earth (domaine public).
