#!/usr/bin/env bash
set -e
python3 - <<'PY'
import os, urllib.request
packs = [
 dict(slug='low-poly-stalls', name='Low Poly Stalls',
      f='lightdreamerlabs-3d-stalls.zip',
      page='https://opengameart.org/content/low-poly-stalls',
      url='https://opengameart.org/sites/default/files/lightdreamerlabs-3d-stalls.zip',
      author='lightdreamerlabs', date='2026', size='703.1KB',
      tags='stall,shop,food,prop,3d', lic='CC0'),
]
for p in packs:
    d = p['slug']
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, p['f'])
    urllib.request.urlretrieve(p['url'], f)
    sz = os.path.getsize(f)
    assert sz > 5000, (d, sz)
    lines = ['# ' + p['name'], '',
             '- 출처 URL: ' + p['page'],
             '- 받은 파일: ' + p['f'] + ' (' + p['size'] + ')',
             '- 라이선스: ' + p['lic'],
             '- 제작자: ' + p['author'],
             '- 공개 연도: ' + p['date'],
             '- 파일 크기(바이트): ' + str(sz),
             '- 태그: ' + p['tags'],
             '- 표기 요구: 없음 (CC0)',
             '- AI 생성 여부: 출처 페이지에 언급 없음',
             '- 수집 라운드: A88', '']
    open(os.path.join(d, 'pack.md'), 'w', encoding='utf-8').write('\n'.join(lines))
    lic = ['# ' + p['name'], '',
           '출처 URL: ' + p['page'],
           '표기 라이선스: ' + p['lic'],
           '제작자: ' + p['author'], '',
           '이 파일은 수집자가 출처 페이지의 라이선스 표기를 기록한 것입니다.',
           '원본 배포물에 라이선스 파일이 포함되어 있지 않으면 이 파일이 그 역할을 합니다.', '']
    open(os.path.join(d, 'LICENSE-SOURCE.txt'), 'w', encoding='utf-8').write('\n'.join(lic))
    print(d, sz)
PY
