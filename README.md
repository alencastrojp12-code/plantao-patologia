# Plantão de Patologia

Site: https://alencastrojp12-code.github.io/plantao-patologia/

Cada pessoa edita pelo próprio Claude. O que um muda vai para o GitHub, e o Claude do outro puxa de lá antes de mexer.
As regras que o Claude segue estão em [`CLAUDE.md`](CLAUDE.md).

## Passo a passo (uma vez só)

1. **Aceite o convite** de colaborador que chegou no seu e-mail do GitHub (ou em https://github.com/notifications).
2. **Instale o app do Claude** (https://claude.ai/download) e entre na sua conta. Precisa de um plano que tenha o Claude Code (aba **Code**).
3. **Instale o Git** (https://git-scm.com/download/win) e o **Python** (https://www.python.org/downloads/). No Python, **marque "Add python.exe to PATH"** na primeira tela.
4. No app do Claude, abra a aba **Code**, escolha a pasta **Documentos** e mande:

   > Clona o repositório https://github.com/alencastrojp12-code/plantao-patologia aqui e instala o edge-tts no Python. Depois me diz se deu tudo certo.

5. Comece uma conversa nova na aba Code, agora escolhendo a pasta **Documentos\plantao-patologia**. É sempre nessa pasta que você vai trabalhar.

Na primeira vez que o Claude enviar algo, abre uma janela pedindo login no GitHub: entre com a sua conta.

## No dia a dia

Abra o Claude na pasta `plantao-patologia` e peça o que quiser, por exemplo:

- "Acrescenta essa questão da prova antiga: …" (pode mandar o PDF ou a foto)
- "Corrige a explicação da questão de pielonefrite aguda"
- "Tira o tema X, não vai cair"

O Claude puxa o que o outro mudou, edita, gera o site, confere e envia para o GitHub. Em 1 ou 2 minutos o site atualiza (se não aparecer, aperte Ctrl+F5).

⚠️ O "Escreva na prova" das questões que já existem não muda sem combinar: são as respostas que já foram decoradas.

## Como as questões ficam guardadas (se quiser mexer na mão)

Tudo fica em `fonte/perguntas.py`. Cada questão é um bloco `dict(...)`:

| Campo | O que é |
|---|---|
| `id` | código único (ex.: `r7`) |
| `tema` | a caixinha: `fig`, `pul`, `car`, `tb`, `rim`, `neo` |
| `ref` | de onde veio (ex.: "Provas antigas · Pielonefrite a") |
| `img` | fotos do enunciado: nomes em `fonte/img/` sem o `.jpg` |
| `q` | o enunciado |
| `ops` | 4 alternativas `("texto", "por que está certa/errada")`; **a primeira é a certa** (o site embaralha) |
| `key` | **"Escreva na prova"** |
| `filme` | 🎬 o filminho (vira o áudio do final) |
| `tip` | o macete |
| `exp` | explicação completa |
| `aviso` | (opcional) erro de gabarito ou o que o professor descontou |
| `apoio` | (opcional) fotos extras depois de responder: `[("foto", "legenda")]` |

Comandos, no PowerShell, dentro da pasta `plantao-patologia`:

```
git pull
python fonte/build.py fonte/img
git add -A
git commit -m "o que eu mudei"
git push
```

Não edite `index.html` nem a pasta `a/` na mão: eles são gerados pelo `build.py`.
