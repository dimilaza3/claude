"""Builds two extra copies of index.html:
   dist/pontikoulis-offline.html  - one self-contained file (images embedded) to copy onto school computers
   dist/artifact.html             - body-only version used for the claude.ai preview"""
import base64, json, os, re
root = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(root, "index.html"), encoding="utf-8").read()
os.makedirs(os.path.join(root, "dist"), exist_ok=True)
emb = {}
for n in sorted(os.listdir(os.path.join(root, "images"))):
    mime = "image/png" if n.endswith(".png") else "image/jpeg"
    emb[n] = f"data:{mime};base64," + base64.b64encode(open(os.path.join(root, "images", n), "rb").read()).decode()
off = src.replace('<script>\n"use strict";', "<script>window.EMBED=" + json.dumps(emb) + ";</script>\n<script>\n\"use strict\";", 1)
open(os.path.join(root, "dist", "pontikoulis-offline.html"), "w", encoding="utf-8").write(off)
art = "\n".join(l for l in src.split("\n") if "<!--WRAP-->" not in l)
open(os.path.join(root, "dist", "artifact.html"), "w", encoding="utf-8").write(art)
print("ok", len(off) // 1024, "KB offline")
