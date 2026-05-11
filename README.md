# 🌸 ParentSurprise (Thanks To)

> "부모님께 드리는 특별한 디지털 감사제"
>
> ParentSurprise는 어버이날을 맞아 부모님께 감동과 재미를 동시에 선사하기 위해 기획된 프리미엄 디지털 이벤트 플랫폼입니다. 단순한 메시지 전달을 넘어, 인터랙티브 요소와 감각적인 디자인을 통해 잊지 못할 경험을 제공합니다.

---

## 📺 프로젝트 소개 (Introduction)
이 프로젝트는 기술적인 복잡함보다는 사용자 경험(UX)과 감성적인 인터랙션에 집중한 프로젝트입니다. 부모님 세대가 사용하시기에 불편함이 없도록 직관적인 UI를 구성하였으며, 다양한 애니메이션 효과를 통해 보는 즐거움을 더했습니다.

---

## 🖼️ 화면 구성 (Screen Configuration)

| 화면 명 | 설명 |
| :--- | :--- |
| 메인 홈 (Home) | 서비스의 시작점으로, 전체적인 컨셉과 메뉴를 한눈에 볼 수 있는 게이트웨이입니다. |
| 황금 룰렛 (Roulette) | 긴장감을 유도하기 위해 설계된 선물 추첨 시스템으로, 리액티브한 캔버스 애니메이션이 포함되어 있습니다. |
| 디지털 카네이션 (Carnation) | '물 주기' 인터랙션을 통해 꽃이 피어나며 자녀들의 응원 메시지가 나타나는 핵심 페이지입니다. |
| 인생네컷 (Four-Cut) | 가족과의 소중한 사진들을 감각적인 프레임에 담아 감상하고 저장할 수 있는 공간입니다. |
| 효도 쿠폰 & 편지 (Coupons/Letters) | 자녀들의 정성이 담긴 텍스트 기반의 선물과 메시지를 프리미엄 카드 형태로 제공합니다. |

---

## ⚙️ 기술 스택 (Tech Stack)

### Front-end
![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![TypeScript](https://img.shields.io/badge/typescript-%23007acc.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

### Back-end
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

### Tools
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

---

 🤔 기술적 이슈와 해결 과정 (Technical Issues)

### 1. CORS 이슈 및 백엔드 통신 최적화
- **이슈**: 프론트엔드(Vite)와 백엔드(FastAPI) 포트가 달라 API 호출 시 `Network Error (CORS)` 발생.
- **해결**: FastAPI의 `CORSMiddleware`를 사용하여 허용된 오리진(`allow_origins=["*"]`)을 설정하고, 공통 헤더 작업을 간소화하기 위해 Axios 인스턴스 및 인터셉터를 적용하여 에러 핸들링을 중앙화했습니다.

### 2. 확률 제어 룰렛 시스템 (Rigged Logic)
- **이슈**: 단순 랜덤 룰렛은 극적인 재미가 떨어짐.
- **해결**: 1회차 실행 시 무조건 '꽝'이나 '재도전'이 나오도록 유도하고, 2회차 실행 시 설정된 선물이 당첨되도록 `rouletteStore`의 `attempts` 상태를 활용해 로직을 제어했습니다.

### 3. 복합 CSS 애니메이션 동기화
- **이슈**: '디지털 카네이션' 피어남 효과 시 줄기, 잎, 꽃잎 애니메이션이 순차적으로 작동해야 함.
- **해결**: Vue의 `ref` 기반 상태(`seed` -> `growing` -> `bloomed`)를 정의하고, 각 요소의 `transition-delay`를 다르게 설정하여 상태 변경 시 자연스러운 연쇄 반응(Cascading Animation)을 구현했습니다.

### 4. 로컬 상태 유지 및 영속성 (Persistence)
- **이슈**: 페이지 새로고침 시 룰렛 당첨 결과나 편지 읽음 상태가 초기화됨.
- **해결**: `localStorage`와 Vue의 `reactive` 객체를 결합한 커스텀 스토어를 구축하여, 데이터 변경 시 브라우저 저장소에 자동으로 동기화되도록 설계했습니다.

---
