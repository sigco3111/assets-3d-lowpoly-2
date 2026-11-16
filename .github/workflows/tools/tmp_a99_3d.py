import json, os, re, subprocess, urllib.request, zipfile, datetime

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
INDEX = "https://raw.githubusercontent.com/sigco3111/game-asset-catalog/main/assets-index.min.json"

PACKS = [
    {
        "slug": "3d-vehicles-pack",
        "name": "3D Vehicles Pack",
        "url": "https://opengameart.org/content/3d-vehicles-pack",
        "author": "mehrasaur",
        "date": "2018-04-05",
        "tags": "vehicles,3d,lowpoly,clay,props",
    },
    {
        "slug": "lowpoly-house-interior-pack",
        "name": "LowPoly House Interior Pack",
        "url": "https://opengameart.org/content/lowpoly-house-interior-pack",
        "author": "quaternius",
        "date": "2021-06-18",
        "tags": "interior,furniture,3d,lowpoly,house",
    },
    {
        "slug": "low-poly-food-pack",
        "name": "Low Poly Food Pack",
        "url": "https://opengameart.org/content/low-poly-food-pack",
        "author": "quaternius",
        "date": "2020-06-01",
        "tags": "food,3d,lowpoly,props",
    },
]


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_names():
    data = json.loads(get(INDEX))
    names = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "name" and isinstance(v, str):
                    names.add(norm(v))
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    return names


def sh(cmd):
    print("$ " + cmd, flush=True)
    subprocess.run(cmd, shell=True, check=True)


def commit(msg, paths):
    sh("git add -A " + " ".join(paths))
    sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "' + msg + '"')


def main():
    names = load_names()
    print("index names:", len(names), flush=True)
    added = []
    for p in PACKS:
        if len(added) >= 2:
            break
        if norm(p["name"]) in names:
            print("skip duplicate:", p["name"], flush=True)
            continue
        if os.path.isdir(p["slug"]):
            print("skip existing dir:", p["slug"], flush=True)
            continue
        try:
            html = get(p["url"])
            zips = re.findall(r'https://opengameart\.org/sites/default/files/[^"\'<> ]+\.zip', html)
            if not zips:
                print("no zip link on", p["url"], flush=True)
                continue
            zip_url = zips[0]
            zip_name = urllib.parse.unquote(zip_url.rsplit("/", 1)[-1])
            data = get(zip_url, binary=True)
            os.makedirs(p["slug"], exist_ok=True)
            with open(os.path.join(p["slug"], zip_name), "wb") as f:
                f.write(data)
            nfiles = 0
            with zipfile.ZipFile(os.path.join(p["slug"], zip_name)) as z:
                nfiles = len([i for i in z.namelist() if not i.endswith("/")])
            imgs = re.findall(r'https://opengameart\.org/sites/default/files/[^"\'<> ]+\.(?:png|jpg|jpeg)', html)
            thumb = ""
            for u in imgs:
                if "preview" in u.lower() or "/styles/" not in u:
                    thumb = u
                    break
            if thumb:
                ext = thumb.rsplit(".", 1)[-1].lower()
                with open(os.path.join(p["slug"], "preview." + ext), "wb") as f:
                    f.write(get(thumb, binary=True))
            size_mb = round(len(data) / 1048576.0, 1)
            with open(os.path.join(p["slug"], "pack.md"), "w", encoding="utf-8") as f:
                f.write("# " + p["name"] + "\n\n")
                f.write("- 출처 URL: " + p["url"] + "\n")
                f.write("- 받은 파일: " + zip_name + " (" + str(size_mb) + "MB)\n")
                f.write("- 라이선스: CC0\n")
                f.write("- 제작자: " + p["author"] + "\n")
                f.write("- 공개일: " + p["date"] + "\n")
                f.write("- 파일 수: " + str(nfiles) + "\n")
                f.write("- 파일 크기(바이트): " + str(len(data)) + "\n")
                f.write("- 태그: " + p["tags"] + "\n")
                f.write("- 표기 요구: 없음 (CC0)\n")
                f.write("- AI 생성 여부: 출처 페이지에 언급 없음\n")
            with open(os.path.join(p["slug"], "LICENSE-SOURCE.txt"), "w", encoding="utf-8") as f:
                f.write("팩: " + p["name"] + "\n")
                f.write("출처: " + p["url"] + "\n")
                f.write("라이선스: CC0 1.0 (출처 페이지 표기)\n")
                f.write("제작자: " + p["author"] + "\n")
                f.write("공개일: " + p["date"] + "\n")
                f.write("다운로드: " + zip_url + "\n")
                f.write("확인: " + datetime.date.today().isoformat() + " OpenGameArt 팩 페이지에 CC0 표기 확인\n")
            commit("에셋: " + p["name"] + " 추가", [p["slug"]])
            sh("git push origin HEAD:main")
            added.append({"slug": p["slug"], "name": p["name"], "zip": zip_name, "mb": size_mb, "files": nfiles, "author": p["author"]})
            print("added:", p["name"], flush=True)
        except Exception as e:
            print("ERROR", p["name"], repr(e), flush=True)
    print("SUMMARY " + json.dumps(added), flush=True)


main()
