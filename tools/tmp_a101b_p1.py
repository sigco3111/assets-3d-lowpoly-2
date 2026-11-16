import re,subprocess as S,urllib.request as U
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Chrome/124"}
O=[]
def lg(s):
 print(s,flush=True);O.append(str(s))
def g(u):
 try:
  return U.urlopen(U.Request(u,headers=UA),timeout=60).read().decode("utf-8","replace")
 except Exception as e:
  return "ERR "+repr(e)
for u in ["https://kenney.nl/assets/castle-kit","https://poly.pizza/bundle/Toon-Shooter-Game-Kit-qraiSXoAru","https://kaylousberg.itch.io/kaykit-platformer"]:
 h=g(u)
 lg("== "+u+" len "+str(len(h)))
 if h.startswith("ERR"):
  lg(h);continue
 hs=[x for x in re.findall(r'href="([^"]+)"',h) if ".zip" in x.lower() or "download" in x.lower()]
 lg("hrefs "+str(hs[:8]))
 ds=re.findall(r'[a-zA-Z0-9_\-/:.]+\.zip',h)
 lg("zipish "+str(ds[:8]))
open("tools/a101b_probe.txt","w",encoding="utf-8").write("\n".join(O)+"\n")
S.run('git add tools/a101b_probe.txt && git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "진단: A101b 다운로드 URL 확인" && git push origin HEAD:main',shell=True)
