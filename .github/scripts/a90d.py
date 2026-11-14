import os, subprocess
from PIL import Image

PACKS = [
    dict(name="Chibi Neko by cosmix", slug="chibi-neko", author="zodiepupper", lic="CC0",
         page="https://opengameart.org/content/chibi-neko-by-cosmix", fname="chibineko.zip",
         prev="https://opengameart.org/sites/default/files/screenshot_20261029_155124.png"),
    dict(name="Bald Man - Rigged", slug="bald-man-rigged", author="EmoPreben", lic="CC0",
         page="https://opengameart.org/content/bald-man-rigged", fname="baldman_painted_rigged.zip",
         prev="https://opengameart.org/sites/default/files/skaermbillede_2026-10-11_152122.png"),
]
OLD = [
    dict(name="Low Poly Stalls", slug="low-poly-stalls", prev="https://opengameart.org/sites/default/files/preview_384.jpg"),
    dict(name="low_poly_swords", slug="low-poly-swords", prev="https://opengameart.org/sites/default/files/screenshot_20261102_195000.png"),
    dict(name="3D Character Pack", slug="3d-character-pack", prev="https://opengameart.org/sites/default/files/new2.jpg"),
    dict(name="3D Human Parts Pack", slug="3d-human-parts-pack", prev="https://opengameart.org/sites/default/files/3d_human_parts_pack.jpg"),
]
UA = "Mozilla/5.0 (X11; Linux x86_64)"


def sh(cmd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def dl(url, dest):
    sh(["curl", "-fsSL", "-A", UA, "-o", dest, url])
    print("size", os.path.getsize(dest), flush=True)


def make_preview(src, slug):
    os.makedirs("previews", exist_ok=True)
    im = Image.open(src)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")
    im.thumbnail((480, 480))
    p = "previews/" + slug + ".png"
    im.save(p, "PNG", optimize=True)
    if os.path.getsize(p) > 200 * 1024:
        rgb = im.convert("RGB")
        q = "previews/" + slug + ".jpg"
        rgb.save(q, "JPEG", quality=85, optimize=True)
        os.remove(p)
        return q
    return p


for p in PACKS:
    s = p["slug"]
    if os.path.isdir(s):
        print("skip existing", s, flush=True)
        continue
    os.makedirs(s)
    dst = os.path.join(s, p["fname"])
    dl("https://opengameart.org/sites/default/files/" + p["fname"], dst)
    subprocess.run(["unzip", "-qo", dst, "-d", s], check=False)
    with open(os.path.join(s, "LICENSE-SOURCE.txt"), "w") as f:
        f.write("Source: %s\nAuthor: %s\nLicense: %s\nFile: %s\nDownloaded via OpenGameArt 2026-11-14 (A90 round). Files unmodified.\n" % (p["page"], p["author"], p["lic"], p["fname"]))
    prev = ""
    try:
        dl(p["prev"], "/tmp/p.png")
        prev = make_preview("/tmp/p.png", s)
    except Exception as e:
        print("preview fail", s, e, flush=True)
    sh(["git", "add", s])
    sh(["git", "commit", "-m", "에셋: " + p["name"] + " 추가"])
    if prev:
        sh(["git", "add", prev])
        sh(["git", "commit", "-m", "썸네일: " + p["name"] + " 추가"])
    print("done", s, prev, flush=True)

for o in OLD:
    if os.path.exists("previews/" + o["slug"] + ".png") or os.path.exists("previews/" + o["slug"] + ".jpg"):
        print("preview exists", o["slug"], flush=True)
        continue
    try:
        dl(o["prev"], "/tmp/o.png")
        prev = make_preview("/tmp/o.png", o["slug"])
        sh(["git", "add", prev])
        sh(["git", "commit", "-m", "썸네일: " + o["name"] + " 추가"])
        print("old preview", o["slug"], prev, flush=True)
    except Exception as e:
        print("old fail", o["slug"], e, flush=True)

sh(["git", "push", "origin", "HEAD:main"])
print("PUSHED", flush=True)
