#!/usr/bin/env bash
set -e
python3 - <<'PY'
import os, urllib.request
packs = [
 dict(d='low-poly-swords', name='low_poly_swords', f='swords_obj.zip',
      page='https://opengameart.org/content/lowpolyswords',
      url='https://opengameart.org/sites/default/files/swords_obj.zip',
      author='Q2DENJINDREW', date='2026', lic='CC0', tags='sword,weapon,lowpoly,obj'),
 dict(d='3d-character-pack', name='3D Character Pack', f='bravos_game_br_2024.zip',
      page='https://opengameart.org/content/3d-character-pack',
      url='https://opengameart.org/sites/default/files/bravos_game_br_2024.zip',
      author='byzmod3d', date='2026', lic='CC0', tags='character,humanoid,lowpoly,3d'),
 dict(d='3d-human-parts-pack', name='3D Human Parts Pack', f='3d_human_parts_pack.zip',
      page='https://opengameart.org/content/3d-human-parts-pack',
      url='https://opengameart.org/sites/default/files/3d_human_parts_pack.zip',
      author='byzmod3d', date='2026', lic='CC0', tags='human,body,parts,lowpoly,3d'),
]
for p in packs:
    os.makedirs(p['d'], exist_ok=True)
    f = os.path.join(p['d'], p['f'])
    urllib.request.urlretrieve(p['url'], f)
    sz = os.path.getsize(f)
    assert sz > 5000, (p['d'], sz)
    md = ['# ' + p['name'], '', '- 출처 URL: ' + p['page'],
          '- 받은 파일: ' + p['f'] + ' (' + str(sz) + ' bytes)',
          '- 라이선스: ' + p['lic'], '- 제작자: ' + p['author'],
          '- 공개 연도: ' + p['date'], '- 태그: ' + p['tags'],
          '- AI 생성 여부: 출처 페이지에 언급 없음', '- 수집 라운드: A89', '']
    open(os.path.join(p['d'], 'pack.md'), 'w', encoding='utf-8').write('\n'.join(md))
    lic = ['# ' + p['name'], '', '출처 URL: ' + p['page'],
           '표기 라이선스: ' + p['lic'], '제작자: ' + p['author'], '',
           '이 파일은 수집자가 출처 페이지의 라이선스 표기를 기록한 것입니다.', '']
    open(os.path.join(p['d'], 'LICENSE-SOURCE.txt'), 'w', encoding='utf-8').write('\n'.join(lic))
    print(p['d'], sz)
PY
