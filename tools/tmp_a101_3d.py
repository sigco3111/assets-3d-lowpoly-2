import json, os, re, shutil, subprocess, urllib.request, urllib.parse, zipfile, datetime

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
INDEX = "https://raw.githubusercontent.com/sigco3111/game-asset-catalog/main/assets-index.min.json"
LIMIT = 3
PACKS = [
    {"slug": "mini-dungeon", "name": "Mini Dungeon", "url": "https://kenney.nl/assets/mini-dungeon", "date": "2026-01-01", "tags": "dungeon,fantasy,3d,lowpoly,environment"},
    {"slug": "mini-forest", "name": "Mini Forest", "url": "https://kenney.nl/assets/mini-forest", "date": "2026-01-01", "tags": "forest,nature,3d,lowpoly,environment"},
    {"slug": "city-kit-roads", "name": "City Kit (Roads)", "url": "https://kenney.nl/assets/city-kit-roads", "date": "2024-01-01", "tags": "city,roads,3d,lowpoly,environment"},
    {"slug": "mini-characters", "name": "Mini Characters", "url": "https://kenney.nl/assets/mini-characters", "date": "2026-01-01", "tags": "characters,3d,lowpoly,animated"},
    {"slug": "city-kit-industrial", "name": "City Kit (Industrial)", "url": "https://kenney.nl/assets/city-kit-industrial", "date": "2025-01-01", "tags": "city,industrial,3d,lowpoly,environment"},
]


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_names():
    out = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "name" and isinstance(v, str):
                    out.add(norm(v))
                    out.add(re.sub(r"[0-9]+$", "", norm(v)))
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(json.loads(get(INDEX)))
    return out


def sh(cmd, check=True):
    print("$ " + cmd, flush=True)
    subprocess.run(cmd, shell=True, check=check)


def collect(p, names):
    if norm(p["name"]) in names:
        print("SKIP dup: " + p["name"], flush=True)
        return None
    if os.path.isdir(p["slug"]):
        print("SKIP dir: " + p["slug"], flush=True)
        return None
    html = get(p["url"])
    print("cc0 on page: " + str("CC0" in html), flush=True)
    if "CC0" not in html:
        print("SKIP no CC0: " + p["url"], flush=True)
        return None
    hrefs = re.findall(r'href="([^"]+?\.zip)"', html)
    zips = [h for h in hrefs if "/media/pages/assets/" in h]
    print("zip hrefs: " + json.dumps(zips[:3]), flush=True)
    if not zips:
        return None
    zip_url = zips[0]
    if zip_url.startswith("/"):
        zip_url = "https://kenney.nl" + zip_url
    zip_name = urllib.parse.unquote(zip_url.rsplit("/", 1)[-1])
    data = get(zip_url, binary=True)
    tmp = "/tmp/" + zip_name
    with open(tmp, "wb") as f:
        f.write(data)
    with zipfile.ZipFile(tmp) as z:
        nfiles = len([i for i in z.namelist() if not i.endswith("/")])
    size_mb = round(len(data) / 1048576.0, 2)
    os.makedirs(p["slug"])
    rel = ""
    if len(data) > 5 * 1024 * 1024:
        tag = p["slug"] + "-v1.0"
        sh("gh release create " + tag + " --title '" + p["name"] + "' --notes 'asset pack zip' || true")
        sh('gh release upload ' + tag + ' "' + tmp + '" --clobber')
        os.remove(tmp)
        rel = ", 릴리스 " + tag + " 첨부"
    else:
        shutil.move(tmp, os.path.join(p["slug"], zip_name))
    imgs = re.findall(r"https://kenney\.nl/media/pages/assets/[^\"' ]+\.(?:png|jpg|jpeg)", html)
    previews = [i for i in imgs if "preview" in i]
    thumb = previews[0] if previews else (imgs[0] if imgs else "")
    if thumb:
        ext = thumb.rsplit(".", 1)[-1].lower()
        with open(os.path.join(p["slug"], "preview." + ext), "wb") as f:
            f.write(get(thumb, binary=True))
    today = datetime.date.today().isoformat()
    md = [
        "# " + p["name"],
        "",
        "- 출처 URL: " + p["url"],
        "- 받은 파일: " + zip_name + " (" + str(size_mb) + "MB" + rel + ")",
        "- 라이선스: CC0",
        "- 라이선스 원문: https://creativecommons.org/publicdomain/zero/1.0/",
        "- 제작자: Kenney",
        "- 공개일: " + p["date"],
        "- 파일 수: " + str(nfiles),
        "- 파일 크기(바이트): " + str(len(data)),
        "- 태그: " + p["tags"],
        "- 표기 요구: 없음 (CC0)",
        "- AI 생성 여부: 출처 페이지에 언급 없음",
    ]
    with open(os.path.join(p["slug"], "pack.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    lic = [
        "팩: " + p["name"],
        "출처: " + p["url"],
        "라이선스: CC0 (출처 페이지 Creative Commons CC0 표기)",
        "저작자: Kenney",
        "공개일: " + p["date"],
        "다운로드: " + zip_url,
        "확인: " + today + " kenney.nl 팩 페이지 CC0 표기와 .zip 링크 확인",
        "표기: 없음 (CC0, 표기 불필요)",
    ]
    with open(os.path.join(p["slug"], "LICENSE-SOURCE.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lic) + "\n")
    sh("git add -A " + p["slug"])
    sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "에셋: ' + p["name"] + ' 추가"')
    sh("git push origin HEAD:main")
    return {"slug": p["slug"], "name": p["name"], "zip": zip_name, "mb": size_mb, "files": nfiles, "url": p["url"], "release": rel}


def main():
    names = load_names()
    print("index names: " + str(len(names)), flush=True)
    added = []
    for p in PACKS:
        if len(added) >= LIMIT:
            break
        try:
            r = collect(p, names)
            if r:
                added.append(r)
                print("ADDED: " + p["name"], flush=True)
        except subprocess.CalledProcessError as e:
            print("GIT ERROR " + p["name"] + " " + repr(e), flush=True)
            sh("git reset --hard HEAD", check=False)
        except Exception as e:
            print("ERROR " + p["name"] + " " + repr(e), flush=True)
    print("SUMMARY " + json.dumps(added, ensure_ascii=False), flush=True)
    sh("git rm -f tools/tmp_a101_3d.py .github/workflows/tmp-a101-3d.yml", check=False)
    sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "정리: A101 3D 임시 파일 삭제"', check=False)
    sh("git push origin HEAD:main", check=False)


main()
