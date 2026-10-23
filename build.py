#!/usr/bin/env python3
"""Gera o index.html a partir de src/posts.json, src/plan.json e src/template.html.
Uso: python3 build.py
"""
import json, pathlib

raiz = pathlib.Path(__file__).resolve().parent
src = raiz / "src"
posts = json.loads((src / "posts.json").read_text(encoding="utf-8"))
plan = json.loads((src / "plan.json").read_text(encoding="utf-8"))
tpl = (src / "template.html").read_text(encoding="utf-8")

# confere se os arquivos de cada post existem
for p in posts["posts"]:
    for caminho in (f"vid/web/{p['video']}.mp4", f"vid/full/{p['video']}.mp4",
                    f"img/web/{p['video']}.webp", f"img/full/{p['video']}.png"):
        if not (raiz / caminho).exists():
            print("AVISO: arquivo não encontrado:", caminho)
    n = len("\n\n".join([p["legenda"], " ".join(p["hashtags"])]))
    if len(p["hashtags"]) > 5:
        print("AVISO: mais de 5 hashtags em", p["id"])
    if n > 2200:
        print("AVISO: legenda acima de 2.200 caracteres em", p["id"])

dados = json.dumps({"marca": posts["marca"], "posts": posts["posts"], "plan": plan},
                   ensure_ascii=False).replace("</", "<\\/")
html = tpl.replace("__DATA__", dados).replace("__MARCA__", posts["marca"]["nome"])
(raiz / "index.html").write_text(html, encoding="utf-8")
print("index.html gerado com", len(posts["posts"]), "posts")


# ---- versão para publicar como artefato (opcional): python3 build.py --artifact
import sys, re
if "--artifact" in sys.argv:
    h = html
    css = re.search(r"<style>(.*?)</style>", h, re.S).group(1)
    corpo = re.search(r"<body>(.*)</body>", h, re.S).group(1)
    css = css.replace("--fb:", "color-scheme:dark;--fb:", 1)
    css = css.replace(".wrap{max-width:760px;margin:0 auto;padding:0 16px}",
        ".wrap{max-width:760px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}")
    css = css.replace("header.top{position:sticky;top:0;", "header.top{position:sticky;top:env(safe-area-inset-top,0px);")
    css += "body::before{content:'';position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:30;background:var(--bk)}"
    css += ".toast{bottom:calc(20px + env(safe-area-inset-bottom,0px))}"
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@800;900&family=Inter:wght@500;600&display=swap">'
    art = ('<title>Central de posts Jardineiro</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
           + fonts + "\n<style>" + css + "</style>\n" + corpo)
    (raiz / "artifact.html").write_text(art, encoding="utf-8")
    print("artifact.html gerado")


# ---- pacotes .zip por post (video + capa + legenda.txt): python3 build.py --zips [--small]
if "--zips" in sys.argv:
    import zipfile, shutil
    pasta = raiz / ("zip_art" if "--small" in sys.argv else "zip")
    if pasta.exists():
        shutil.rmtree(pasta)
    pasta.mkdir()
    for p in posts["posts"]:
        nome = f"post{p['ordem']}-{p['id']}.zip"
        video = raiz / "vid/full" / f"{p['video']}.mp4"
        if "--small" in sys.argv and (raiz / "vid/art" / f"{p['video']}.mp4").exists():
            video = raiz / "vid/art" / f"{p['video']}.mp4"
        texto = p["legenda"].rstrip() + "\n\n" + " ".join(p["hashtags"]) + "\n\n---\nTexto alternativo:\n" + p["alt"] + "\n"
        with zipfile.ZipFile(pasta / nome, "w", zipfile.ZIP_STORED) as z:
            z.write(video, f"{p['ordem']}-{p['id']}.mp4")
            z.write(raiz / "img/full" / f"{p['video']}.png", f"{p['ordem']}-{p['id']}-capa.png")
            z.writestr(f"{p['ordem']}-{p['id']}-legenda.txt", texto)
    print("zips gerados em", pasta.name)
