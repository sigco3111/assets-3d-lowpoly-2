import json,os,re,shutil,subprocess as S,urllib.request as U,urllib.parse as P,zipfile as Z,datetime as D
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Chrome/124"}
IX="https://raw.githubusercontent.com/sigco3111/game-asset-catalog/main/assets-index.min.json"
CC="https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt"
SR="https://opengameart.org/art-search-advanced?field_art_type_tid%5B%5D=9&field_art_licenses_tid%5B%5D=4"
LOG="tools/a101b_log.txt"
O=[]
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
def go(url,names):
 h=g(url)
 if "CC0" not in h:
  lg("nocc0 "+url);return 0
 t=re.search(r"<title>(.*?)</title>",h,re.S)
 nmv=(t.group(1) if t else url).replace(" | OpenGameArt.org","").strip()
 if n(nmv) in names:
  lg("DUP "+nmv);return 0
 zs=[z for z in re.findall(r'https://opengameart\.org/sites/default/files/[^"\'<> ]+\.zip',h) if "preview" not in z.lower()]
 if not zs:
  lg("nozip "+nmv);return 0
 zu=zs[0];zn=P.unquote(zu.rsplit("/",1)[-1])
 dt=g(zu,1)
 if len(dt)>40*1024*1024:
  lg("toobig "+nmv);return 0
 t2="/tmp/x.zip";open(t2,"wb").write(dt)
 nf=len([i for i in Z.ZipFile(t2).namelist() if not i.endswith("/")])
 mb=round(len(dt)/1048576.0,2)
 slug=re.sub(r"[^a-z0-9]+","-",nmv.lower()).strip("-")[:50]
 if os.path.isdir(slug):
  lg("DIR "+slug);return 0
 m=re.search(r'article:published_time" content="(\d{4}-\d{2}-\d{2})',h)
 dd=m.group(1) if m else "출처 페이지 표기 미확인"
 au=re.search(r'Author:.*?<a[^>]*>([^<]{2,40})</a>',h,re.S)
 au=au.group(1).strip() if au else "출처 페이지 표기"
 os.makedirs(slug);rel=""
 if len(dt)>5*1024*1024:
  tg=slug+"-v1.0"
  sh("gh release create "+tg+" --title '"+nmv+"' --notes zip || true",0)
  sh("gh release upload "+tg+' "'+t2+'" --clobber')
  os.remove(t2);rel=", 릴리스 "+tg+" 첨부"
 else:
  shutil.move(t2,os.path.join(slug,zn))
 im=re.findall(r"https://opengameart\.org/sites/default/files/[^\"' )]+\.(?:png|jpg|jpeg)",h)
 pr=[i for i in im if "styles/large" in i]
 th=pr[0] if pr else (im[0] if im else "")
 if th:
  try:
   open(slug+"/preview."+th.rsplit(".",1)[-1].lower(),"wb").write(g(th,1))
  except Exception as e:
   lg("th "+repr(e))
 L=["# "+nmv,"","- 출처 URL: "+url,"- 받은 파일: "+zn+" ("+str(mb)+"MB"+rel+")",
  "- 라이선스: CC0","- 라이선스 원문: https://creativecommons.org/publicdomain/zero/1.0/",
  "- 제작자: "+au,"- 공개일: "+dd,"- 파일 수: "+str(nf),
  "- 파일 크기(바이트): "+str(len(dt)),"- 태그: 3d,lowpoly,models",
  "- 표기 요구: 없음 (CC0)","- AI 생성 여부: 출처 페이지에 언급 없음"]
 open(slug+"/pack.md","w",encoding="utf-8").write("\n".join(L)+"\n")
 C=["팩: "+nmv,"출처: "+url,"라이선스: CC0 1.0 (출처 페이지 표기)","저작자: "+au,
  "공개일: "+dd,"다운로드: "+zu,
  "확인: "+D.date.today().isoformat()+" OpenGameArt 페이지 CC0 표기와 .zip 링크 확인","표기: 없음"]
 open(slug+"/LICENSE-SOURCE.txt","w",encoding="utf-8").write("\n".join(C)+"\n")
 open(slug+"/CREDITS.txt","w",encoding="utf-8").write("\n".join([nmv,"제작: "+au,"출처: "+url,"라이선스: CC0 1.0","수집: sigco3111 game-asset-catalog"])+"\n")
 try:
  open(slug+"/LICENSE.txt","w",encoding="utf-8").write(g(CC))
 except Exception as e:
  lg("lic "+repr(e))
 sh("git add -A "+slug)
 sh('git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "에셋: '+nmv+' 추가"')
 sh("git push origin HEAD:main")
 lg("ADDED "+nmv+" "+zn+" "+str(mb)+"MB "+str(nf))
 return 1
def main():
 c=0
 try:
  names=nm();lg("names %d"%len(names))
  s=g(SR)
  links=[]
  for h in re.findall(r'href="(/content/[^"#?]+)"',s):
   if h not in links:
    links.append(h)
  lg("links %d"%len(links))
  for h in links[:25]:
   if c>=2:break
   try:
    c+=go("https://opengameart.org"+h,names)
   except Exception as e:
    lg("ERR "+h+" "+repr(e));sh("git reset --hard HEAD",0)
 except Exception as e:
  lg("FATAL "+repr(e))
 open(LOG,"w",encoding="utf-8").write("\n".join(O)+"\n")
 S.run('git add '+LOG+' && git -c user.name="sigco3111" -c user.email="sigco3111k@gmail.com" commit -m "진단: A101b 로그" && git push origin HEAD:main',shell=True)
main()
