# Sous la Surface : fabrication et publication quotidienne

Compte Instagram @souslasurface1mn et TikTok « Sous La Surface ».
Promesse : ce que personne ne t'explique, en 1 minute. Deux piliers qui alternent :
- **Maths et argent** (probabilités, finance perso, lois cachées du quotidien)
- **Mer et monde** (commerce maritime, géopolitique des routes, navires)

Le propriétaire valide la vidéo du jour s'il le souhaite. **Sans réponse de sa part, la vidéo est publiée quand même à 18 h.**

## Règles du propriétaire (non négociables)

- Pas de voix off.
- Pas d'emojis, ni dans les vidéos ni dans les légendes.
- Ne jamais terminer par « Demain : … ». La chute se termine par « Abonne-toi. » seul.
- Garder la direction artistique : fond bleu nuit, doré, typo Inter Display + chiffres en mono (constantes dans `pipeline/lib.py`).
- Garder la musique et la structure du pilote (`pipeline/music.py`, épisodes 001 et 002).
- Français, tutoiement, phrases courtes et directes.
- Chiffres vérifiés uniquement. Jamais de chiffre inventé. Sujet finance : contenu éducatif, jamais de conseil personnalisé.

## Structure d'un épisode (60 à 70 s)

1. **Accroche, 0–4 s** : affirmation choc qui surgit mot par mot, et quelque chose bouge dès la première image.
2. **Enjeu, 4–12 s** : pourquoi c'est surprenant, ce que l'intuition dirait.
3. **La question** : posée en gros, puis gardée en bandeau en haut tant qu'on n'a pas la réponse.
4. **La preuve, ~13–30 s** : une démonstration visuelle animée (compteurs, remplissage, carte, calendrier…). Jamais d'écran figé plus de 3 s.
5. **La réponse, ~30–36 s** : le chiffre clé en très gros.
6. **Le retournement, ~36–48 s** : « Pourquoi ? » / « Le secret ? » puis le mécanisme caché, en visuel. La batterie de la musique s'arrête sur ce passage (mesures 14–15), c'est voulu.
7. **L'escalade, ~48–56 s** : l'idée appliquée à plus grande échelle.
8. **La chute, 56 s → fin** : phrase à retenir (2 lignes, la 2e en doré), puis encart « Abonne-toi. ».

Repères de mise en page (1080×1920) : texte entre y≈230 et y≈1550 (le bas est caché par les boutons des applis), largeur de texte ≤ 940 px, bandeau-question à y≈296.

## Procédure du jour (tâche planifiée de 12 h)

1. `cd pipeline && bash setup.sh`
2. Ouvrir `SUJETS.md`, prendre le premier sujet « à faire » en alternant les piliers par rapport à la dernière ligne de `PUBLICATIONS.md`.
3. Vérifier chaque chiffre avec une recherche web et garder les sources. Si un chiffre n'est pas vérifiable, le retirer ou formuler une fourchette prudente.
4. Écrire `pipeline/episodes/epNNN_slug.py` en partant de `ep001` ou `ep002` (mêmes helpers `words`, `bump`, `big_center` depuis `kinetic.py`, même `sfx_events()`).
5. Contrôle visuel : `python3 build.py episodes/epNNN_slug.py --stills 2 8 14 22 31 40 46 53 62`, assembler une planche et la regarder. Corriger les chevauchements une fois.
6. Rendu : `python3 build.py episodes/epNNN_slug.py ../videos/AAAA-MM-JJ-slug.mp4`. Vérifier durée vidéo = audio et volume entre -17 et -15 LUFS (`ffmpeg -i f.mp4 -af ebur128 -f null -`).
7. Commit de la vidéo et du script, push sur `main`.
8. Vérifier que `https://raw.githubusercontent.com/icaresolaire-alt/souslasurface/main/videos/AAAA-MM-JJ-slug.mp4` répond 200 avec la bonne taille.
9. Programmer dans Metricool (`createScheduledPost`) :
   - `blogId` : `7503487`, date du jour à **18:00** Europe/Paris
   - `providers` : instagram et tiktok
   - `media` : le lien raw GitHub ci-dessus
   - `instagramData` : `{"type": "REEL", "showReelOnFeed": true}`
   - `tiktokData` : **`title` obligatoire** (court), `privacyOption` `PUBLIC_TO_EVERYONE`
   - `autoPublish` true, `draft` false
   - Légende : 2 à 3 phrases sans emoji, puis une ligne de 4 à 6 hashtags.
10. Envoyer au propriétaire la vidéo (fichier) + la légende + le lien Metricool, en disant : « Publication automatique à 18 h. Réponds "annule" avant 18 h pour l'arrêter. » Si on reçoit « annule », passer le post en brouillon avec `updateScheduledPost` (draft true).
11. Mettre à jour `SUJETS.md` (statut) et `PUBLICATIONS.md` (date, sujet, fichier, sources), commit et push.

En cas d'échec d'une étape : ne pas publier une vidéo non vérifiée, et prévenir le propriétaire de ce qui a bloqué.
