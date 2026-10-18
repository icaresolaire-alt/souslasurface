"""Story Instagram teaser : les premières secondes de l'épisode + un écran « Nouvelle vidéo sur le profil ».
Usage (depuis pipeline/) : python3 story.py ../videos/AAAA-MM-JJ-slug.mp4 "Titre court du sujet"
Sortie : ../videos/AAAA-MM-JJ-slug-story.mp4 (environ 8 s, 1080x1920, avec la musique de l'épisode)
"""
import sys, os, subprocess, tempfile
from lib import *

HOOK = 5.0      # secondes reprises de l'accroche
CARD = 3.0      # durée de l'écran final

def card(title):
    def draw(f, t):
        a = ease(seg(t, 0.0, 0.35))
        f.text('SOUS LA SURFACE', W/2, 640, 34, MUTED, a, MONO, True)
        f.text('Nouvelle vidéo', W/2, 820, 96, INK, a)
        f.text('sur le profil', W/2, 930, 96, SPARK, ease(seg(t, 0.2, 0.55)))
        f.rect(140, 1040, 800, 6, LINE, a, 3)
        f.wrap(title, W/2, 1140, 54, 860, INK, ease(seg(t, 0.4, 0.8)))
    return draw

def main(src, title):
    out = src[:-4] + '-story.mp4'
    tmp = tempfile.mkdtemp()
    card_mp4 = os.path.join(tmp, 'card.mp4')
    render(card_mp4, CARD, card(title))   # vidéo + piste silencieuse
    run = lambda *a: subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
    hook = os.path.join(tmp, 'hook.mp4')
    run('-i', src, '-t', str(HOOK), '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-an', hook)
    vid = os.path.join(tmp, 'vid.mp4')
    run('-i', hook, '-i', card_mp4, '-filter_complex', '[0:v][1:v]concat=n=2:v=1:a=0[v]', '-map', '[v]',
        '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', vid)
    total = HOOK + CARD
    run('-i', vid, '-i', src, '-map', '0:v', '-map', '1:a', '-t', str(total),
        '-af', f'afade=t=out:st={total-1.5}:d=1.5', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
        '-movflags', '+faststart', out)
    print('ok', out)

if __name__ == '__main__':
    main(os.path.abspath(sys.argv[1]), sys.argv[2])
