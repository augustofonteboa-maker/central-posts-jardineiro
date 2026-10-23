# Central de posts · Jardineiro

Abra `index.html` no navegador (funciona direto do disco ou hospedado).

## Como usar
1. Toque em **Salvar vídeo**.
2. Toque em **Copiar legenda**.
3. Abra o Instagram, escolha o vídeo, cole a legenda.

## Editar uma legenda
- Pelo site: edite no campo da legenda (fica salvo neste navegador).
- Definitivo: abra `src/posts.json`, mude o campo `legenda` do post e rode `python3 build.py`.

## Trocar nome da marca
Em `src/posts.json`, campo `marca.nome`. Hashtag de marca provisória: `#seujardineiro` (troque em cada post).

## Gerar o site de novo
`python3 build.py` (precisa só do Python 3). Ele lê `src/posts.json`, `src/plan.json` e `src/template.html` e escreve `index.html`.

## Pastas
- `vid/full`: vídeos originais (download). `vid/web`: versões leves para prévia.
- `img/full`: capas em PNG. `img/web`: capas WebP 900 px.
- `assets`: logo (`logo.png`, `logo-claro.png`, `logo-escuro.png`), ícones e fontes.
- `src`: dados e template.
