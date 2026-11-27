# Timberfall 환경 PBR 텍스처·잎사귀 카드·하늘 HDR (CC0)

1인칭 철거 게임 Timberfall(https://patch.gg/games/blendi/timberfall)이 쓴 환경 소재 모음입니다.
목재·지붕기와·암석·콘크리트·금속·잔디·자갈·나무껍질 PBR 텍스처 10종(diffuse/normal/ARM WebP 3맵씩),
나뭇잎·풀잎 컷아웃 카드 2종, 조명용 하늘 HDR 1종(Qwantani Late Afternoon 1K).

**라이선스: CC0 1.0.** 귀속 표기 없이 쓸 수 있습니다(CREDITS.txt의 파일별 원저작자 참조).

## 내용 (zip)

- `textures/` Poly Haven PBR 10종 ×3맵(WebP 1K): rough_wood, fine_grained_wood, clay_roof_tiles_02,
  rock_surface, rough_concrete, rusty_metal_sheet, green_metal_rust, leafy_grass, sparse_grass,
  gravel_floor, bark_brown_02 (각 `_diff`/`_nor`/`_arm`)
- `foliage/` ambientCG 컷아웃을 게임이 카드로 합성한 leaf_cluster.webp, grass_tuft.webp (알파 포함)
- `hdri/` qwantani_late_afternoon_puresky_1k.hdr (Poly Haven, equirect 1K)

## 활용 메모

- three.js 등에서 그대로 쓰는 표준 PBR 맵 구성(diffuse/normalGL/ARM=AO·Roughness·Metallic 채널 합성).
- 출처: https://patch.gg/games/blendi/timberfall · 소스 https://git.patch.gg/blendi/timberfall.git · 수집일: 2026-11-27
