# AbilityCasting 결투장·생물·소품 3D 모델 5종 (GLB)

AbilityCastingThreeJS(Elemental Sandbox)에서 원작자가 Blender로 제작한 것이 확인되는 모델·텍스처·Blender 원본을 모은 팩입니다.

**라이선스: MIT.** 저작권 표기와 MIT 전문을 유지하면 사용할 수 있습니다(동봉 LICENSE.txt, Copyright (c) 2026 mohamedachrefelouafi). 환경 HDRI만 Poly Haven CC0(귀속 불필요)입니다.

## 내용 (zip)

- `models/duel_hall.glb` — 결투장 환경 (텍스처 미내장, 머티리얼은 원본 src/world 참고)
- `models/wolf.glb` — 늑대, 리그 + 클립 6종 (01_Run·02_walk·03_creep·04_Idle·05_site·Gallop)
- `models/arcane_tome.glb` — 마법서
- `models/wildroot_reliquary.glb` — 뿌리 아치와 룬스톤
- `models/amethyst_stones.glb` — 자수정 결정 5종
- `textures/` — 결투장 천 텍스처 (cloth color·ORM·emissive + 원본 T_DuelCloth 3종)
- `env/spruit_sunrise.hdr` — Poly Haven Spruit Sunrise 2K (Greg Zaal, CC0)
- `blender/` — duel_hall·duel_hall_day·wolf의 Blender 원본
- `LICENSE.txt` `CREDITS.txt` `README.txt`

## 자작 판정 근거

- duel_hall·wolf: 원본 README 프로젝트 구조 절이 art/의 두 항목을 프로젝트 Blender 소스로 명시, .blend 원본 동봉
- arcane_tome·wildroot_reliquary·amethyst_stones: 원본 설정 주석이 "built in Blender"/"cut in Blender"라고 기술
- 전 모델 GLB 메타데이터가 Blender I/O 내보내기 (Sketchfab 등 서드파티 표기 없음)

shark.glb는 Blender 내보내기 메타와 전용 클립뿐이라 자작 명시 근거가 부족해 MIT 판정에서 제외하고 권리 미확인 팩(abilitycasting-unverified)으로 옮겼습니다.

## 제외 항목

- `dragon.glb`·`magical_gyroscope.glb`, cathedral·배너·스테인드글라스·룬 텍스처 — 권리 미확인, 별도 팩(abilitycasting-unverified)에 수록
- Mixamo 캐릭터 FBX 4종과 `diffuse.png` — Mixamo 에셋은 재배포 금지라 수집하지 않음

## 활용 메모

- 이 모델을 쓰는 시네마틱 주문 코드는 코드 팩(assets-code abilitycasting-spell-vfx)에 있습니다.
- 출처: https://github.com/achrefelouafi/AbilityCastingThreeJS
- 수집일: 2026-11-23 · 파일: abilitycasting-models.zip (53MB, Releases 첨부)
