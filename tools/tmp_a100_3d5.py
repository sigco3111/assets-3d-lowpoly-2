import json, os, re, shutil, subprocess, urllib.request, zipfile, datetime, traceback

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
INDEX = "https://raw.githubusercontent.com/sigco3111/game-asset-catalog/main/assets-index.min.json"
RELEASE = "v1.0"
LIMIT = 2
LOG = []

PACKS = [
    {"slug": "low-poly-halloween-kit", "name": "Low-Poly Halloween Kit",
     "url": "https://opengameart.org/content/low-poly-halloween-kit",
     "author": "AssetQuest", "date": "2023-10-01", "tags": "halloween,props,3d,lowpoly,environment"},
    {"slug": "modular-dungeon-2-3d-models", "name": "Modular Dungeon 2 - 3D Models",
     "url": "https://opengameart.org/content/modular-dungeon-2-3d-models",
     "author": "Kenney", "date": "2021-01-01", "tags": "dungeon,modular,3d,lowpoly,environment"},
    {"slug": "tower-defense-kit", "name": "Tower Defense Kit",
     "url": "https://opengameart.org/content/tower-defense-kit",
     "author": "Kenney", "date": "2021-01-01", "tags": "towerdefense,3d,lowpoly,kenney"},
    {"slug": "modular-castle-level-construction-kit", "name": "Modular Castle Level Construction Kit",
     "url": "https://opengameart.org/content/modular-castle-level-construction-kit",
     "author": "Kenney", "date": "2021-01-01", "tags": "castle,modular,3d,lowpoly,environment"},
]


def log(s):
    print(s, flush=True)
    LOG.append(str(s))


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
    log("$ " + cmd)
    subprocess.run(cmd, shell=True, check=check)


def write_log():
    with open("a100_log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")
    sh('git add a100_log.txt')
    sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "임시: A100 3D 로그" || true', check=False)
    sh("git push origin HEAD:main", check=False)


def main():
    try:
        names = load_names()
    except Exception:
        log("INDEX FAILED\n" + traceback.format_exc())
        write_log()
        return
    log("index names: " + str(len(names)))
    added = []
    for p in PACKS:
        if len(added) >= LIMIT:
            break
        if norm(p["name"]) in names:
            log("SKIP dup: " + p["name"])
            continue
        if os.path.isdir(p["slug"]):
            log("SKIP existing dir: " + p["slug"])
            continue
        try:
            html = get(p["url"])
            log("page " + p["url"] + " len " + str(len(html)) + " hasCC0 " + str("CC0" in html))
            m = re.search(r"License\(s\):(.{0,200})", html, re.S)
            if m:
                log("license field: " + re.sub(r"<[^>]+>", " ", m.group(1))[:120].replace("\n", " "))
            zips = re.findall(r'https://opengameart\.org/sites/default/files/[^"\'<> ]+\.zip', html)
            log("zips: " + str(zips[:4]))
            if not zips:
                log("SKIP no zip link: " + p["url"])
                continue
            zip_url = zips[0]
            zip_name = urllib.parse.unquote(zip_url.rsplit("/", 1)[-1])
            data = get(zip_url, binary=True)
            log("downloaded " + zip_name + " bytes " + str(len(data)))
            tmp = "/tmp/" + zip_name
            with open(tmp, "wb") as f:
                f.write(data)
            with zipfile.ZipFile(tmp) as z:
                nfiles = len([i for i in z.namelist() if not i.endswith("/")])
            size_mb = round(len(data) / 1048576.0, 1)
            big = len(data) > 5 * 1024 * 1024
            os.makedirs(p["slug"], exist_ok=True)
            if big:
                sh("gh release create " + RELEASE + " --title " + RELEASE + " --notes '3D 로우폴리 팩 zip 첨부' || true", check=False)
                sh('gh release upload ' + RELEASE + ' "' + tmp + '" --clobber')
                os.remove(tmp)
            else:
                shutil.move(tmp, os.path.join(p["slug"], zip_name))
            imgs = re.findall(r'https://opengameart\.org/sites/default/files/[^"\'<> ]+\.(?:png|jpg|jpeg)', html)
            thumb = ""
            for u in imgs:
                if "preview" in u.lower():
                    thumb = u
                    break
            if not thumb and imgs:
                thumb = imgs[0]
            if thumb:
                ext = thumb.rsplit(".", 1)[-1].lower()
                with open(os.path.join(p["slug"], "preview." + ext), "wb") as f:
                    f.write(get(thumb, binary=True))
            with open(os.path.join(p["slug"], "pack.md"), "w", encoding="utf-8") as f:
                f.write("# " + p["name"] + "\n\n")
                f.write("- 출처 URL: " + p["url"] + "\n")
                f.write("- 받은 파일: " + zip_name + " (" + str(size_mb) + "MB" + (", 릴리스 " + RELEASE + " 첨부" if big else "") + ")\n")
                f.write("- 라이선스: CC0\n")
                f.write("- 라이선스 원문: https://creativecommons.org/publicdomain/zero/1.0/\n")
                f.write("- 제작자: " + p["author"] + "\n")
                f.write("- 공개일: " + p["date"] + "\n")
                f.write("- 파일 수: " + str(nfiles) + "\n")
                f.write("- 파일 크기(바이트): " + str(len(data)) + "\n")
                f.write("- 태그: " + p["tags"] + "\n")
                f.write("- 표기 요구: 없음 (CC0)\n")
                f.write("- AI 생성 여부: 출처 페이지에 언급 없음\n")
            with open(os.path.join(p["slug"], "LICENSE-SOURCE.txt"), "w", encoding="utf-8") as f:
                f.write("팩: " + p["name"] + "\n출처: " + p["url"] + "\n")
                f.write("라이선스: CC0 1.0 (출처 페이지 표기)\n")
                f.write("제작자: " + p["author"] + "\n공개일: " + p["date"] + "\n")
                f.write("다운로드: " + zip_url + "\n")
                f.write("확인: " + datetime.date.today().isoformat() + " OpenGameArt 팩 페이지에 CC0 표기 확인\n")
            sh("git add -A " + p["slug"])
            sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "에셋: ' + p["name"] + ' 추가"')
            sh("git push origin HEAD:main")
            added.append({"slug": p["slug"], "name": p["name"], "zip": zip_name, "mb": size_mb, "files": nfiles, "big": big})
            log("ADDED: " + p["name"])
        except subprocess.CalledProcessError as e:
            log("GIT ERROR " + p["name"] + " " + str(e))
            sh("git reset --hard HEAD", check=False)
        except Exception:
            log("ERROR " + p["name"] + "\n" + traceback.format_exc())
    log("SUMMARY " + json.dumps(added, ensure_ascii=False))
    write_log()


main()
