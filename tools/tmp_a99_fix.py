import json, os, re, subprocess, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
RELEASE = "v1.0"
BT = chr(96)
PACKS = [
    ("3d-vehicles-pack", "3D Vehicles Pack", "https://opengameart.org/content/3d-vehicles-pack", "mehrasaur"),
    ("low-poly-rpg-pack", "Low Poly RPG Pack", "https://opengameart.org/content/low-poly-rpg-pack", "quaternius"),
    ("lowpoly-survival-pack", "LowPoly Survival Pack", "https://opengameart.org/content/lowpoly-survival-pack", "quaternius"),
]


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=300) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def sh(cmd, check=True):
    print("$ " + cmd, flush=True)
    subprocess.run(cmd, shell=True, check=check)


def main():
    readme = open("README.md", encoding="utf-8").read()
    changed = False
    for slug, name, url, author in PACKS:
        if not os.path.isdir(slug):
            print("missing dir", slug, flush=True)
            continue
        pth = os.path.join(slug, "pack.md")
        txt = open(pth, encoding="utf-8").read()
        fixed = txt.replace("첨부)- 라이선스", "첨부)\n- 라이선스")
        if fixed != txt:
            open(pth, "w", encoding="utf-8").write(fixed)
            txt = fixed
            changed = True
            print("fixed pack.md", slug, flush=True)
        if not any(f.startswith("preview.") for f in os.listdir(slug)):
            try:
                html = get(url)
                cands = re.findall(r'https://opengameart\.org/sites/default/files/[^"\'<> ]+\.(?:png|jpg|jpeg)', html)
                cands = [c for c in cands if "/styles/" not in c and "audio_preview" not in c]
                if cands:
                    with open(os.path.join(slug, "preview." + cands[0].rsplit(".", 1)[-1].lower()), "wb") as f:
                        f.write(get(cands[0], binary=True))
                    changed = True
                    print("added preview", slug, cands[0], flush=True)
                else:
                    print("no preview candidate", slug, flush=True)
            except Exception as e:
                print("preview error", slug, repr(e), flush=True)
        m = re.search(r"- 받은 파일: (\S+) \(([0-9.]+)MB(, 릴리스 v1\.0 첨부)?\)", txt)
        if not m:
            print("cannot parse zip line", slug, flush=True)
            continue
        zipname, size, rel = m.group(1), m.group(2), m.group(3)
        if "### " + name not in readme:
            readme = readme.rstrip() + "\n### " + name + " ![" + name + " 미리보기](" + slug + "/preview.png)\n"
            if rel:
                readme += "- 파일: [릴리스 " + RELEASE + " 첨부 다운로드](https://github.com/sigco3111/assets-3d-lowpoly-2/releases/download/" + RELEASE + "/" + zipname + ") (" + size + "MB) — 릴리스 첨부\n"
            else:
                readme += "- 파일: " + BT + zipname + BT + " (" + size + "MB) — 저장소 내 포함\n"
            readme += "- 제작: " + author + " / 라이선스: CC0 / 원본: " + url + "\n"
            changed = True
            print("readme entry added", name, flush=True)
    dirs = [d for d in os.listdir(".") if os.path.isdir(d) and os.path.isfile(os.path.join(d, "pack.md"))]
    m = re.search(r"수록 팩: (\d+)팩", readme)
    if m:
        readme = readme[:m.start(1)] + str(len(dirs)) + readme[m.end(1):]
        changed = True
        print("pack count ->", len(dirs), flush=True)
    if changed:
        open("README.md", "w", encoding="utf-8").write(readme)
        sh("git add -A README.md 3d-vehicles-pack low-poly-rpg-pack lowpoly-survival-pack")
        sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "정리: A99 3D README 미리보기"')
        sh("git push origin HEAD:main")
        print("pushed", flush=True)
    else:
        print("nothing to change", flush=True)


main()
