import json,os,re,shutil,subprocess as S,urllib.request as U,urllib.parse as P,zipfile as Z,datetime as D
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Chrome/124"}
IX="https://raw.githubusercontent.com/sigco3111/game-asset-catalog/main/assets-index.min.json"
CC="https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt"
LOG="tools/a101b_log.txt"
O=[]
PACKS=[
 {"slug":"low-poly-nature-pack","name":"Low Poly Nature Pack","url":"https://opengameart.org/content/low-poly-nature-pack-1","author":"quaternius","tags":"nature,environment,3d,lowpoly"},
 {"slug":"low-poly-medieval-models-163","name":"Low Poly Medieval Models - 163","url":"https://opengameart.org/content/low-poly-medieval-models-163-cc0-village-castle-interiors-props-weapons-food-dungeon-nature","author":"Avraman","tags":"medieval,village,castle,dungeon,3d,lowpoly"},
]
def lg(s):
 print(s,flush=True);O.append(str(s))
def g(u,b=0):
 r=U.urlopen(U.Request(u,headers=UA),timeout=900).read()
 return r if b else r.decode("utf-8","replace")
def n(s):
 return re.sub(r"[^a-z0-9]","",s.lower())
def nm():
 o=set()
 def w(x):
  if isinstance(x,dict):
   for k,v in x.items():
    if k=="name" and isinstance(v,str):
     o.add(n(v));o.add(re.sub(r"[0-9]+$","",n(v)))
    else:
     w(v)
  elif isinstance(x,list):
   for v in x:
    w(v)
 w(json.loads(g(IX)))
 return o
def sh(c,ck=1):
 lg("$ "+c);S.run(c,shell=True,check=ck)
def go(p):
 h=g(p["url"])
 lg("page %d cc0 %s"%(len(h),"CC0" in h))
 if "CC0" not in h:
  return
 zs=re.findall(r'https://opengameart\.org/sites/default/files/[^"\'<> ]+\.zip',h)
 lg("zips "+json.dumps(zs[:4]))
 zs=[z for z in zs if "preview" not in z.lower()]
 if not zs:
  return
 zu=zs[0];zn=P.unquote(zu.rsplit("/",1)[-1]);dt=g(zu,1)
 t="/tmp/x.zip";open(t,"wb").write(dt)
 zf=Z.ZipFile(t);nf=len([i for i in zf.namelist() if not i.endswith("/")])
 mb=round(len(dt)/1048576.0,2)
 m=re.search(r'article:published_time" content="(\d{4}-\d{2}-\d{2})',h)
 dd=m.group(1) if m else "출처 페이지 표기 미확인"
 os.makedirs(p["slug"]);rel=""
 if len(dt)>5*1024*1024:
  tg=p["slug"]+"-v1.0"
  sh("gh release create "+tg+" --title '"+p["name"]+"' --notes zip || true",0)
  sh("gh release upload "+tg+' "'+t+'" --clobber')
  os.remove(t);rel=", 릴리스 "+tg+" 첨부"
 else:
  shutil.move(t,os.path.join(p["slug"],zn))
 im=re.findall(r"https://opengameart\.org/sites/default/files/[^\"' )]+\.(?:png|jpg|jpeg)",h)
 pr=[i for i in im if "audio_preview" not in i and "styles/large" in i]
 th=pr[0] if pr else (im[0] if im else "")
 lg("thumb "+th)
 if th:
  try:
   open(p["slug"]+"/preview."+th.rsplit(".",1)[-1].lower(),"wb").write(g(th,1))
  except Exception as e:
   lg("th "+repr(e))
 L=["# "+p["name"],"","- 출처 URL: "+p["url"],
  "- 받은 파일: "+zn+" ("+str(mb)+"MB"+rel+")","- 라이선스: CC0",
  "- 라이선스 원문: https://creativecommons.org/publicdomain/zero/1.0/",
  "- 제작자: "+p["author"],"- 공개일: "+dd,"- 파일 수: "+str(nf),
  "- 파일 크기(바이트): "+str(len(dt)),"- 태그: "+p["tags"],
  "- 표기 요구: 없음 (CC0)","- AI 생성 여부: 출처 페이지에 언급 없음"]
 open(p["slug"]+"/pack.md","w",encoding="utf-8").write("\n".join(L)+"\n")
 C=["팩: "+p["name"],"출처: "+p["url"],"라이선스: CC0 1.0 (출처 페이지 표기)",
  "저작자: "+p["author"],"공개일: "+dd,"다운로드: "+zu,
  "확인: "+D.date.today().isoformat()+" OpenGameArt 페이지 CC0 표기와 .zip 링크 확인","표기: 없음"]
 open(p["slug"]+"/LICENSE-SOURCE.txt","w",encoding="utf-8").write("\n".join(C)+"\n")
 open(p["slug"]+"/CREDITS.txt","w",encoding="utf-8").write("\n".join([p["name"],"제작: "+p["author"],"출처: "+p["url"],"라이선스: CC0 1.0","수집: sigco3111 game-asset-catalog"])+"\n")
 try:
  open(p["slug"]+"/LICENSE.txt","w",encoding="utf-8").write(g(CC))
 except Exception as e:
  lg("lic "+repr(e))
 sh("git add -A "+p["slug"])
 sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "에셋: '+p["name"]+' 추가"')
 sh("git push origin HEAD:main")
 lg("ADDED "+p["name"]+" "+zn+" "+str(mb)+"MB "+str(nf))
def main():
 try:
  s=nm();lg("names %d"%len(s))
  c=0
  for p in PACKS:
   if c>=2:break
   try:
    if os.path.isdir(p["slug"]):lg("DIR "+p["slug"]);continue
    if n(p["name"]) in s:lg("DUP "+p["name"]);continue
    go(p);c+=1
   except Exception as e:
    lg("ERR "+p["name"]+" "+repr(e));sh("git reset --hard HEAD",0)
 except Exception as e:
  lg("FATAL "+repr(e))
 open(LOG,"w",encoding="utf-8").write("\n".join(O)+"\n")
 S.run('git add '+LOG+' && git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "진단: A101b 로그" && git push origin HEAD:main',shell=True)
main()
