import os, subprocess
from PIL import Image

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


for o in OLD:
    if os.path.exists("previews/" + o["slug"] + ".png") or os.path.exists("previews/" + o["slug"] + ".jpg"):
        print("preview exists", o["slug"], flush=True)
        continue
    try:
        dl(o["prev"], "/tmp/op.png")
        prev = make_preview("/tmp/op.png", o["slug"])
        sh(["git", "add", prev])
        sh(["git", "commit", "-m", "썸네일: " + o["name"] + " 추가"])
        print("old preview", o["slug"], prev, flush=True)
    except Exception as e:
        print("old fail", o["slug"], e, flush=True)

sh(["git", "push", "origin", "HEAD:main"])
print("PUSHED", flush=True)
