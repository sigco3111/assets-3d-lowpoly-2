# Procedural Animals 베이크 샘플 6종 (.animal)

MIT 라이선스 절차적 동물 생성기(threejs-procedural-animals)의 베이크 도구로 만든 개체 6종 샘플입니다. 리그·스킨·애니메이션 데이터가 포함된 전용 `.animal` 포맷으로, 같은 라이브러리로 약 20ms에 로드됩니다(GLB가 아니며 로드에 동일 라이브러리 필요). 생성기 없이 즉시 게임에 넣을 때 씁니다.

**라이선스: MIT** (Copyright (c) 2026 Majid Manzarpour and procedural-animals contributors). 생성기 코드와 동일 조건: 재배포 시 저작권 표기와 MIT 전문 유지.

- 생성기: https://github.com/majidmanzarpour/threejs-procedural-animals · 코드 팩: assets-code procedural-animals-threejs
- 수집일: 2026-11-23 · 파일: procedural-animal-samples.zip (25MB, .animal 6개 + LICENSE + README.txt)
- 개체(버텍스 수): wolf 74,617 · horse 75,503 · eagle 64,814 · shark 72,175 · snake 67,856 · spider 72,115
- 생성 파라미터: seed 3, quality high (procedural-animals-bake <종> --seed 3 --quality high)
- 로드: createAnimal('wolf', { baked: await (await fetch('wolf.animal')).arrayBuffer() })
- 검증: 베이크 도구 자체 검증(배열 라운드트립 동일·로드 후 본 행렬 NaN 없음·버텍스 수 일치) 6종 전량 통과, 2026-11-23
- 미리보기: 6종 실제 렌더(헤드리스 크롬 WebGL)
