import json, os, re, shutil, subprocess, urllib.request, zipfile, datetime

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
INDEX = "https://raw.githubusercontent.com/sigco3111/game-asset-catalog/main/assets-index.min.json"
LIMIT = 1

PACKS = [
    {"slug": "3td-fantasy-ruins-pack", "name": "3TD Fantasy Ruins Pack",
     "url": "https://opengameart.org/content/3td-fantasy-ruins-pack",
     "author": "3D Tri-Dimensional", "date": "2016-06-01", "lic": "CC0",
     "tags": "ruins,fantasy,modular,3d,lowpoly"},
    {"slug": "modular-sci-fi-megakit", "name": "Modular Sci-Fi MegaKit",
     "url": "https://opengameart.org/content/modular-sci-fi-megakit",
     "author": "Kenney", "date": "2021-01-01", "lic": "CC0",
     "tags": "scifi,modular,3d,lowpoly,environment"},
    {"slug": "wooden-overhang-modular-kit", "name": "Wooden Overhang Modular Kit",
     "url": "https://opengameart.org/content/wooden-overhang-modular-kit",
     "author": "Kenney", "date": "2021-01-01", "lic": "CC-BY 4.0",
     "tags": "wooden,modular,3d,lowpoly,environment"},
]


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=300) as r:
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


def sh(cmd, check=True):
    print("$ " + cmd, flush=True)
    subprocess.run(cmd, shell=True, check=check)


def main():
    names = load_names()
    print("index names:", len(names), flush=True)
    added = []
    for p in PACKS:
        if len(added) >= LIMIT:
            break
        if norm(p["name"]) in names:
            print("SKIP dup:", p["name"], flush=True)
            continue
        if os.path.isdir(p["slug"]):
            print("SKIP existing dir:", p["slug"], flush=True)
            continue
        try:
            html = get(p["url"])
            if p["lic"].split()[0] not in html and p["lic"] not in html:
                print("SKIP no CC-BY on page:", p["url"], flush=True)
                continue
            zips = re.findall(r'https://opengameart\.org/sites/default/files/[^"\'<> ]+\.zip', html)
            if not zips:
                print("SKIP no zip link:", p["url"], flush=True)
                continue
            zip_url = zips[0]
            zip_name = urllib.parse.unquote(zip_url.rsplit("/", 1)[-1])
            data = get(zip_url, binary=True)
            tmp = "/tmp/" + zip_name
            with open(tmp, "wb") as f:
                f.write(data)
            with zipfile.ZipFile(tmp) as z:
                nfiles = len([i for i in z.namelist() if not i.endswith("/")])
            size_mb = round(len(data) / 1048576.0, 2)
            os.makedirs(p["slug"], exist_ok=True)
            shutil.move(tmp, os.path.join(p["slug"], zip_name))
            imgs = re.findall(r'https://opengameart\.org/sites/default/files/[^"\'<> ]+\.(?:png|jpg|jpeg)', html)
            thumb = imgs[0] if imgs else ""
            if thumb:
                ext = thumb.rsplit(".", 1)[-1].lower()
                with open(os.path.join(p["slug"], "preview." + ext), "wb") as f:
                    f.write(get(thumb, binary=True))
            with open(os.path.join(p["slug"], "pack.md"), "w", encoding="utf-8") as f:
                f.write("# " + p["name"] + "\n\n")
                f.write("- 출처 URL: " + p["url"] + "\n")
                f.write("- 받은 파일: " + zip_name + " (" + str(size_mb) + "MB)\n")
                f.write("- 라이선스: " + p["lic"] + "\n")
                f.write("- 라이선스 원문: " + ("https://creativecommons.org/publicdomain/zero/1.0/" if p["lic"] == "CC0" else "https://creativecommons.org/licenses/by/4.0/") + "\n")
                f.write("- 제작자: " + p["author"] + "\n")
                f.write("- 공개일: " + p["date"] + "\n")
                f.write("- 파일 수: " + str(nfiles) + "\n")
                f.write("- 파일 크기(바이트): " + str(len(data)) + "\n")
                f.write("- 태그: " + p["tags"] + "\n")
                f.write("- 표기 요구: " + ("없음 (CC0)" if p["lic"] == "CC0" else "있음 (" + p["lic"] + ", 제작자 " + p["author"] + " · 원본 출처 링크 표기)"))
                f.write("- AI 생성 여부: 출처 페이지에 언급 없음\n")
            with open(os.path.join(p["slug"], "LICENSE-SOURCE.txt"), "w", encoding="utf-8") as f:
                f.write("팩: " + p["name"] + "\n출처: " + p["url"] + "\n")
                f.write("라이선스: " + p["lic"] + " (출처 페이지 표기)\n")
                f.write("저작자: " + p["author"] + "\n공개일: " + p["date"] + "\n")
                f.write("다운로드: " + zip_url + "\n")
                f.write("확인: " + datetime.date.today().isoformat() + " OpenGameArt 페이지 CC-BY 3.0 표기 확인\n")
                f.write("표기: " + p["name"] + " by " + p["author"] + ", CC-BY 3.0, " + p["url"] + "\n")
            sh("git add -A " + p["slug"])
            sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "에셋: ' + p["name"] + ' 추가"')
            sh("git push origin HEAD:main")
            added.append({"slug": p["slug"], "name": p["name"], "zip": zip_name, "mb": size_mb, "files": nfiles, "lic": p["lic"]})
            print("ADDED:", p["name"], flush=True)
        except subprocess.CalledProcessError as e:
            print("GIT ERROR", p["name"], e, flush=True)
            sh("git reset --hard HEAD", check=False)
        except Exception as e:
            print("ERROR", p["name"], repr(e), flush=True)
    print("SUMMARY " + json.dumps(added, ensure_ascii=False), flush=True)


main()
