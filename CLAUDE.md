# Plantão de Patologia — instruções para o Claude

Site de estudo para a prova de patologia (questões discursivas com foto, "Escreva na prova", filminho, macete, glossário e áudio).
Este repositório é compartilhado por mais de uma pessoa, cada uma com o seu Claude. O GitHub é a fonte da verdade:
o que uma pessoa muda chega na outra pelo `git pull`.

- Site publicado (GitHub Pages, branch main, raiz): https://alencastrojp12-code.github.io/plantao-patologia/
- Repositório: https://github.com/alencastrojp12-code/plantao-patologia

## Fluxo obrigatório a cada pedido de mudança

1. **Antes de editar:** `git pull --rebase` (a outra pessoa pode ter mudado algo).
2. **Editar** só a fonte:
   - `fonte/perguntas.py`: `TEMAS`, `Q` (questões), `COLA` (colas por tema), `FINAIS`, `GLOSSARIO`. Campos de cada questão no README.
   - `fonte/template.html`: visual e comportamento.
   - `fonte/build.py`: geração e o mapa `FALA` (pronúncia de siglas no áudio).
   - Fotos novas: `fonte/img/<nome>.jpg`.
   - Nunca edite à mão `index.html` nem `a/`: são gerados.
3. **Gerar:** `python fonte/build.py fonte/img` (precisa de `python -m pip install edge-tts` e internet para áudios novos).
   Ele imprime "N questões, N áudios, N imagens"; qualquer `AssertionError` (id repetido, foto faltando) tem que ser resolvido.
4. **Conferir:** abra `prova-patologia.html` (versão de arquivo único, ignorada pelo git) ou leia a saída do build.
5. **Enviar:**
   ```
   git add -A
   git commit -m "<o que mudou, em português>"
   git pull --rebase
   git push
   ```
   Em 1–2 minutos o site atualiza. Diga à pessoa o que entrou e o link.

### Conflitos
- Em `fonte/perguntas.py`: junte os dois lados à mão, mantendo as questões das duas pessoas.
- Em `index.html` ou `a/*.mp3`: são gerados. Resolva o `perguntas.py` primeiro, depois rode o build de novo e use o resultado.
- Na primeira vez num computador o build regrava todos os áudios (sem cache); o conteúdo é o mesmo, pode enviar.

## Regras de conteúdo (pedidas por quem criou o projeto)

- **Nunca mude o `key` ("Escreva na prova") de uma questão que já existe sem perguntar**: as pessoas decoram essas respostas. Avise que a outra pessoa também pode ter decorado.
- `key` = só o essencial que o professor aceita, curto e simples, mas completo. O entendimento vai no `filme`.
- Prioridade: questões das provas antigas e das listas (a prova costuma repetir).
- Confira cada resposta com o livro de referência (Robbins). Erro de gabarito/resumo vai no `aviso`.
- `ops`: 4 alternativas, a primeira é a certa (o site embaralha). A certa não pode ser sempre a mais longa: o build lista onde isso acontece.
- Foto do enunciado sem rótulo que entregue a resposta.
- Se disserem que um assunto não cai, tire a caixinha inteira (tema, questões, cola, glossário e fotos que só ele usa).

## Link do claude.ai (só a conta de quem criou o projeto)

Existe também uma versão privada no claude.ai em que o Claude da página corrige a resposta escrita:
https://claude.ai/artifact/4N5Gjm4Y1cGoaoFFjALSkc (capabilities `sample` e `tts`).
Ela **não** atualiza pelo GitHub. Só o Claude da conta do claude.ai que criou esse link consegue republicar: depois do push, publique `index.html`
no mesmo URL com os `a/*.mp3` novos ou alterados em `files` (e `null` para os removidos).
Se você não estiver nessa conta, pule isso e avise que o link do claude.ai só muda quando essa conta pedir ao próprio Claude.
