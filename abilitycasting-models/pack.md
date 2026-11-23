# AbilityCasting 결투장·생물·소품 3D 모델 6종 (GLB)

AbilityCastingThreeJS(Elemental Sandbox)에서 원작자가 Blender로 제작한 것이 확인되는 모델과 텍스처만 모은 팩입니다. GLB 메타데이터(Blender I/O), 전용 애니메이션 클립, 설정 주석("built in Blender"), 원본 저장소의 art/*.blend 소스로 자작을 확인했습니다.

**라이선스: MIT.** 저작권 표기와 MIT 전문을 유지하면 사용할 수 있습니다(동봉 LICENSE.txt, Copyright (c) 2026 mohamedachrefelouafi). 환경 HDRI만 Poly Haven CC0(귀속 불필요)입니다.

## 내용 (zip)

- `models/duel_hall.glb` — 결투장 환경 (텍스처 미내장, 머티리얼은 원본 src/world 참고)
- `models/wolf.glb` — 늑대, 리그 + 클립 6종 (01_Run·02_walk·03_creep·04_Idle·05_site·Gallop)
- `models/shark.glb` — 백상어, 전용 클립 Breach·Swim
- `models/arcane_tome.glb` — 마법서
- `models/wildroot_reliquary.glb` — 뿌리 아치와 룬스톤
- `models/amethyst_stones.glb` — 자수정 결정 5종
- `textures/` — 결투장 천 텍스처 (cloth color·ORM·emissive + 원본 T_DuelCloth 3종)
- `env/spruit_sunrise.hdr` — Poly Haven Spruit Sunrise 2K (Greg Zaal, CC0)
- `LICENSE.txt` `CREDITS.txt` `README.txt`

## 제외 항목 (권리상 수록 불가)

- `dragon.glb`, `magical_gyroscope.glb` — Sketchfab 서드파티 모델, 원라이선스 확인 불가
- Mixamo 캐릭터 FBX 4종과 `diffuse.png` — Mixamo 에셋은 재배포 금지
- cathedral PBR·배너·스테인드글라스·`rune_glow` 텍스처 — 출처 확인 불가

## 활용 메모

- Blender 원본(.blend)은 원본 저장소 `art/`에 있습니다(duel_hall, duel_hall_day 변형, wolf).
- 이 모델을 쓰는 시네마틱 주문 코드는 코드 팩(assets-code abilitycasting-spell-vfx)에 있습니다.
- 출처: https://github.com/achrefelouafi/AbilityCastingThreeJS
- 수집일: 2026-11-23 · 파일: abilitycasting-models.zip
