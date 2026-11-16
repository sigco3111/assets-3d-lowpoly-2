import glob, os, subprocess


def sh(c):
    print(c, flush=True)
    subprocess.run(c, shell=True, check=True)


readme = open("README.md", encoding="utf-8").read()
new = readme.replace("(low-poly-rpg-pack/preview.png)", "(low-poly-rpg-pack/preview.jpg)")
new = new.replace("(lowpoly-survival-pack/preview.png)", "(lowpoly-survival-pack/preview.jpg)")
if new != readme:
    open("README.md", "w", encoding="utf-8").write(new)
    print("readme preview links fixed", flush=True)
for slug in ["low-poly-rpg-pack", "lowpoly-survival-pack"]:
    p = os.path.join(slug, "pack.md")
    t = open(p, encoding="utf-8").read()
    f = t.replace("첨부)- 라이선스", "첨부)\n- 라이선스")
    if f != t:
        open(p, "w", encoding="utf-8").write(f)
        print("pack.md fixed", slug, flush=True)

targets = []
for pat in ["tools/tmp_a99_*.py", ".github/workflows/tmp-a99-*.yml", ".github/workflows/tmp_a99_*.py"]:
    targets += glob.glob(pat)
for t in targets:
    sh("git rm -q " + t)
sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" add -A README.md low-poly-rpg-pack lowpoly-survival-pack')
sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "정리: A99 임시 파일 삭제 및 README 링크 정리"')
sh("git push origin HEAD:main")
print("cleaned", targets, flush=True)
