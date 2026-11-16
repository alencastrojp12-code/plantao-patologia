# Plantão de Patologia

Site: https://alencastrojp12-code.github.io/plantao-patologia/

## Como editar (passo a passo)

### 1. Uma vez só: preparar o computador (Windows)

1. Aceite o convite de colaborador que chegou no seu e-mail (ou em github.com/notifications).
2. Instale o **Git**: https://git-scm.com/download/win (pode ir clicando em "Next").
3. Instale o **Python**: https://www.python.org/downloads/. Na primeira tela, **marque "Add python.exe to PATH"**.
4. Abra o **PowerShell** e rode, uma linha por vez:

```
cd $HOME\Documents
git clone https://github.com/alencastrojp12-code/plantao-patologia.git
cd plantao-patologia
python -m pip install edge-tts
```

Na primeira vez que você enviar algo, abre uma janela pedindo login no GitHub: entre com a sua conta.

### 2. Toda vez que for mexer

No PowerShell, dentro da pasta `plantao-patologia`:

```
git pull
```

(isso baixa o que a outra pessoa mudou; sempre faça antes de editar)

### 3. Editar as questões

Tudo fica em **`fonte/perguntas.py`** (abra no Bloco de Notas ou no VS Code). Cada questão é um bloco `dict(...)`:

| Campo | O que é |
|---|---|
| `id` | código único (ex.: `r7`). Não repita. |
| `tema` | a caixinha: `fig`, `pul`, `car`, `tb`, `rim`, `neo` |
| `ref` | de onde veio (ex.: "Provas antigas · Pielonefrite a") |
| `img` | fotos do enunciado: nomes dos arquivos de `fonte/img/` sem o `.jpg` |
| `q` | o enunciado |
| `ops` | 4 alternativas, cada uma `("texto", "por que está certa/errada")`. **A primeira é sempre a certa** (o site embaralha). |
| `key` | **"Escreva na prova"**: a resposta curta que se escreve na prova |
| `filme` | 🎬 o filminho (vira o áudio do final) |
| `tip` | o macete |
| `exp` | explicação completa |
| `aviso` | (opcional) erro de gabarito ou o que o professor descontou |
| `apoio` | (opcional) fotos extras depois de responder: `[("nome_da_foto", "legenda")]` |

Outras partes do mesmo arquivo: `TEMAS` (as caixinhas), `COLA` (as colas por tema) e `GLOSSARIO` (palavras difíceis).

Fotos novas: salve em `fonte/img/` como `.jpg` e use o nome sem `.jpg` em `img` ou `apoio`.

⚠️ **Não mude o `key` das questões que já existem sem combinar antes**: são as respostas que já foram decoradas.

### 4. Gerar o site de novo

```
python fonte/build.py fonte/img .
```

- Na primeira vez ele grava todos os áudios de novo (precisa de internet, leva alguns minutos). Depois só grava os que mudaram.
- Se der erro, ele mostra a linha. O mais comum é vírgula ou aspas faltando no `perguntas.py`.
- Para conferir antes de enviar, abra o arquivo `prova-patologia.html` que aparece na pasta (dois cliques).

### 5. Enviar para o site

```
git add -A
git commit -m "o que eu mudei"
git push
```

Em 1 ou 2 minutos o site atualiza sozinho (se não aparecer, aperte Ctrl+F5).

## Dúvidas comuns

- **`git push` recusado ("rejected")**: a outra pessoa enviou algo antes. Rode `git pull` e depois `git push` de novo.
- **`python` não é reconhecido**: o Python foi instalado sem "Add to PATH". Reinstale marcando essa opção.
- **Não editar `index.html` nem a pasta `a/` na mão**: elas são geradas pelo passo 4 e qualquer mudança feita nelas é apagada na próxima geração.
