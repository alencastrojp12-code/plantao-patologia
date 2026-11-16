"""Gera ../prova-patologia.html (arquivo único, com imagens e áudios embutidos).
Uso: python build.py img [pasta_do_site]   (precisa de edge-tts; áudios ficam em cache/; site padrão: a pasta acima de fonte/ (raiz do repositório))"""
import asyncio, base64, hashlib, json, re, sys
from pathlib import Path
import edge_tts
from perguntas import Q, TEMAS, COLA, FINAIS, GLOSSARIO

AQUI = Path(__file__).parent
IMGS = Path(sys.argv[1])
CACHE = AQUI / "cache"; CACHE.mkdir(exist_ok=True)
VOZ = "pt-BR-FranciscaNeural"
CERTO = ["Acertou!", "Isso aí!", "Mandou bem!", "Exato!", "Boa!", "É essa mesmo!"]
ERRADO = ["Não foi dessa vez.", "Essa não.", "Quase!", "Hum, essa não é.", "Cuidado com essa!", "Essa é a pegadinha."]
# siglas que a voz leria errado
FALA = {"HBsAg": "agá bê ésse á gê", "NADH": "ene á dê agá", "VLDL": "vê éle dê éle", "LDL": "éle dê éle",
        "CD8": "cê dê oito", "PAS": "pê á ésse", "PK": "pê cá", "PDN": "pê dê ene", "N, H e F": "ene, agá e éfe",
        "1-B": "um bê", "1-A": "um á", "Th1": "tê agá um", "Th2": "tê agá dois", "CD4": "cê dê quatro",
        "TNF": "tê ene éfe", "PiZZ": "pi zê zê", "HIV": "agá i vê", "IgE": "i gê é", "PP": "pê pê", "DPOC": "dê pê ó cê"}

def falar(t):
    for k, v in FALA.items():
        t = re.sub(rf"(?<!\w){re.escape(k)}(?!\w)", v, t)
    assert not re.search(r"[→+×]", t), t
    return t

clips = {}
for n, q in enumerate(Q):
    assert len(q["ops"]) == 4, q["id"]
    for i, (_, why) in enumerate(q["ops"]):
        pre = (CERTO if i == 0 else ERRADO)[(n + i) % 6]
        clips[f'{q["id"]}.{i}'] = f"{pre} {why}"
    clips[f'{q["id"]}.e'] = f'{q["exp"]} Pra não esquecer: {q["tip"]}'
    clips[f'{q["id"]}.t'] = q.get("filme") or q["key"]  # modo discursivo: o filminho, ou a própria resposta quando ela já é explicada
for t, c in COLA.items():
    clips[f"cola.{t}"] = c["frase"]
for k, v in FINAIS.items():
    clips[f"fim.{k}"] = v

async def gerar():
    sem = asyncio.Semaphore(5)
    async def um(k, txt):
        txt = falar(txt)
        f = CACHE / (hashlib.sha1(f"{VOZ}|{txt}".encode()).hexdigest()[:16] + ".mp3")
        if not f.exists() or f.stat().st_size == 0:
            async with sem:
                await edge_tts.Communicate(txt, VOZ).save(str(f))
        assert f.stat().st_size > 2000, k
        return k, f
    return dict(await asyncio.gather(*(um(k, t) for k, t in clips.items())))

arquivos = asyncio.run(gerar())
b64 = lambda f, mime: f"data:{mime};base64," + base64.b64encode(Path(f).read_bytes()).decode()
audio = {k: b64(f, "audio/mpeg") for k, f in arquivos.items()}

usadas = {i for q in Q for i in q["img"]} | {i for q in Q for i, _ in q.get("apoio", [])}
for i in usadas:
    assert (IMGS / f"{i}.jpg").exists(), i
img = {i: b64(IMGS / f"{i}.jpg", "image/jpeg") for i in sorted(usadas)}  # ordem fixa: sem diff à toa no git

ids = [q["id"] for q in Q]
assert len(ids) == len(set(ids))
def montar(audio):
    dados = {"qs": Q, "temas": TEMAS, "cola": COLA, "audio": audio, "img": img, "glos": GLOSSARIO}
    js = json.dumps(dados, ensure_ascii=False).replace("</", r"<\/")
    return (AQUI / "template.html").read_text(encoding="utf-8").replace("/*DADOS*/", f"window.D={js};")

saida = AQUI.parent / "prova-patologia.html"
saida.write_text(montar(audio), encoding="utf-8")

# versão web: a página tem limite de 16 MiB, então os áudios viram arquivos que baixam só ao tocar
web = Path(sys.argv[2]) if len(sys.argv) > 2 else AQUI.parent; (web / "a").mkdir(parents=True, exist_ok=True)
for velho in (web / "a").glob("*.mp3"): velho.unlink()  # questão removida não deixa áudio sobrando
for k, f in arquivos.items():
    (web / "a" / f"{k}.mp3").write_bytes(Path(f).read_bytes())
(web / "index.html").write_text(montar({k: f"a/{k}.mp3" for k in arquivos}), encoding="utf-8")
assert len(list((web / "a").iterdir())) == len(arquivos) and (web / "index.html").stat().st_size < 16 * 2**20

longa = sum(len(q["ops"][0][0]) == max(len(o[0]) for o in q["ops"]) for q in Q)
print(f"{len(Q)} questões, {len(clips)} áudios, {len(img)} imagens, {saida.stat().st_size/1e6:.1f} MB")
print(f"alternativa certa é a mais longa em {longa}/{len(Q)}:",
      [q["id"] for q in Q if len(q["ops"][0][0]) == max(len(o[0]) for o in q["ops"])])
