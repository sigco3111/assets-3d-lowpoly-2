import os, re, glob, subprocess, urllib.request
from PIL import Image

PACKS = [
    dict(name="Bird Bath", slug="bird-bath", author="JeremyWoods", lic="CC0",
         page="https://opengameart.org/content/bird-bath", fname="birdbath.zip"),
    dict(name="low poly iron ore", slug="low-poly-iron-ore", author="musher3004", lic="CC0",
         page="https://opengameart.org/content/low-poly-iron-ore", fname="stone.zip"),
    dict(name="Chibi Neko by cosmix", slug="chibi-neko", author="zodiepupper", lic="CC0",
         page="https://opengameart.org/content/chibi-neko-by-cosmix", fname="chibineko.zip"),
]
OLD = [
    dict(name="Low Poly Stalls", slug="low-poly-stalls", page="https://opengameart.org/content/low-poly-stalls"),
    dict(name="low_poly_swords", slug="low-poly-swords", page="https://opengameart.org/content/lowpolyswords"),
    dict(name="3D Character Pack", slug="3d-character-pack", page="https://opengameart.org/content/3d-character-pack"),
    dict(name="3D Human Parts Pack", slug="3d-human-parts-pack", page="https://opengameart.org/content/3d-human-parts-pack"),
]

UA = "Mozilla/5.0 (X11; Linux x86_64)"


def sh(cmd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def dl(url, dest):
    print("download", url, flush=True)
    sh(["curl", "-fsSL", "-A", UA, "-o", dest, url])
    print("size", os.path.getsize(dest), flush=True)


def og_image(page):
    try:
        out = subprocess.run(["curl", "-fsSL", "-A", UA, page], capture_output=True, check=True).stdout.decode("utf-8", "ignore")
    except Exception as e:
        print("og fetch fail", e, flush=True)
        return None
    m = re.search(r'og:image"[^>]*content="([^"]+)"', out) or re.search(r'content="([^"]+)"[^>]*property="og:image"', out)
    return m.group(1) if m else None


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
    imgs = [x for x in glob.glob(s + "/**/*", recursive=True) if x.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"))]
    src = max(imgs, key=os.path.getsize) if imgs else None
    if not src:
        og = og_image(p["page"])
        if og:
            dl(og, "/tmp/og.png")
            src = "/tmp/og.png"
    prev = ""
    if src:
        try:
            prev = make_preview(src, s)
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
    og = og_image(o["page"])
    if not og:
        print("no og", o["slug"], flush=True)
        continue
    try:
        dl(og, "/tmp/o.png")
        prev = make_preview("/tmp/o.png", o["slug"])
        sh(["git", "add", prev])
        sh(["git", "commit", "-m", "썸네일: " + o["name"] + " 추가"])
        print("old preview", o["slug"], prev, flush=True)
    except Exception as e:
        print("old fail", o["slug"], e, flush=True)

sh(["git", "push", "origin", "HEAD:main"])
print("PUSHED", flush=True)
