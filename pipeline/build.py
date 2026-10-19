"""Rendu complet d'un épisode, couverture comprise.
Usage (depuis pipeline/) : python3 build.py episodes/epXXX_nom.py ../videos/AAAA-MM-JJ-nom.mp4
Images fixes de contrôle (temps de l'épisode, sans la couverture) :
    python3 build.py episodes/epXXX_nom.py --stills 2 10 30 50
Couverture seule (image de la grille du profil) :
    python3 build.py episodes/epXXX_nom.py --cover
"""
import sys, os, subprocess, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'episodes'))
from lib import render, still, Frame
from make_audio import build_audio
import cover as cov

# Rythme : 1,3 = la vidéo dure 30 % de plus que le script (retour des spectateurs : trop rapide).
PACE = 1.3

def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

if __name__ == '__main__':
    mod = load(sys.argv[1])
    d = os.environ.get('STILLS_DIR', '/tmp'); os.makedirs(d, exist_ok=True)
    if sys.argv[2] == '--stills':
        for x in sys.argv[3:]: still(f'{d}/still_{x}.png', float(x), mod.draw)
        print(f'images dans {d}/still_*.png')
    elif sys.argv[2] == '--cover':
        draw, _ = cov.wrap_draw(mod)
        still(f'{d}/cover.png', 0.0, draw)
        print(f'couverture : {d}/cover.png')
    else:
        out = os.path.abspath(sys.argv[2]); wav = out[:-4] + '.wav'; wav2 = out[:-4] + '-decale.wav'
        pace = float(getattr(mod, 'PACE', PACE))
        build_audio(mod, wav, pace)
        ms = int(cov.OFFSET * 1000)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', f'adelay={ms}|{ms}', wav2], check=True)
        draw, total = cov.wrap_draw(mod, pace)
        render(out, total, draw, audio=wav2)
        for p in (wav, wav2, wav.replace('.wav', '-musique.wav'), wav.replace('.wav', '-musique.mid')):
            if os.path.exists(p): os.remove(p)
        print('ok', out)
