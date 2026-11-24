"""Génère les voix demandées dans voix/demandes/*.json avec OmniVoice (k2-fsa, Apache 2.0).
Tourne sur GitHub Actions (CPU). Format d'une demande :
{"instruct": "male, young adult, moderate pitch", "language": "fr", "speed": 1.0,
 "lignes": [{"id": "01", "texte": "..."}]}
Sortie : voix/sorties/<demande>/<id>.wav (24 kHz). Une demande déjà générée n'est pas refaite.
"""
import json, os, sys, glob, time
import soundfile as sf, torch
from omnivoice import OmniVoice

torch.set_num_threads(os.cpu_count() or 4)
todo = []
for p in sorted(glob.glob('voix/demandes/*.json')):
    name = os.path.basename(p)[:-5]
    out = f'voix/sorties/{name}'
    if os.path.exists(f'{out}/FINI'): continue
    todo.append((p, name, out))
if not todo: print('rien à faire'); sys.exit(0)

model = OmniVoice.from_pretrained('k2-fsa/OmniVoice', device_map='cpu', dtype=torch.float32)
for p, name, out in todo:
    d = json.load(open(p)); os.makedirs(out, exist_ok=True)
    for l in d['lignes']:
        t0 = time.time()
        kw = dict(text=l['texte'])
        for k in ('instruct', 'language', 'speed'):
            v = l.get(k, d.get(k))
            if v is not None: kw[k] = v
        if d.get('ref_audio'): kw['ref_audio'] = d['ref_audio']; kw['ref_text'] = d.get('ref_text')
        audio = model.generate(**kw)[0]
        sf.write(f"{out}/{l['id']}.wav", audio, 24000)
        print(name, l['id'], f'{len(audio)/24000:.1f}s audio en {time.time()-t0:.0f}s', flush=True)
    open(f'{out}/FINI', 'w').write('ok\n')
