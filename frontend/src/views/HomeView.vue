<script setup lang="ts">
import { useRouter } from 'vue-router'
import { PenTool, Image as ImageIcon, Ticket, RotateCw, ChevronRight, Heart } from 'lucide-vue-next'

const router = useRouter()

const features = [
  { 
    id: 'letters', 
    title: '자녀들의 편지', 
    desc: '진심을 담은 따뜻한 메시지', 
    icon: PenTool,
    color: '#FF6B81',
    bg: '#FFF0F3'
  },
  { 
    id: 'photo', 
    title: '추억 사진첩', 
    desc: '함께 웃던 소중한 순간들', 
    icon: ImageIcon,
    color: '#4834D4',
    bg: '#EDEBFF'
  },
  { 
    id: 'coupons', 
    title: '효도 쿠폰', 
    desc: '아이들의 약속이 담긴 쿠폰', 
    icon: Ticket,
    color: '#6AB04C',
    bg: '#F0FFF0'
  },
  { 
    id: 'four-cut', 
    title: '우리 가족 네컷', 
    desc: '함께 찍은 소중한 인생네컷', 
    icon: ImageIcon,
    color: '#FF9F43',
    bg: '#FFF5EB'
  },
  { 
    id: 'carnation', 
    title: '디지털 카네이션', 
    desc: '사랑을 담아 꽃을 피워보세요', 
    icon: Heart,
    color: '#FF4757',
    bg: '#FFF0F0'
  },
  { 
    id: 'roulette', 
    title: '선물 룰렛', 
    desc: '오늘의 깜짝 행운을 뽑아보세요', 
    icon: RotateCw,
    color: '#F0932B',
    bg: '#FFF9F0'
  }
]

const navigateTo = (id: string) => {
  router.push(`/${id}`)
}
</script>

<template>
  <section class="home-view fade-in">
    <div class="hero-card">
      <!-- 둥둥 떠다니는 데코 이미지 추가 -->
      <!-- 세 남매 데코 이미지 (둥둥 떠다니는 효과) -->
      <div class="hero-deco-group">
        <img src="/images/miso.png" class="floating-img deco-miso" alt="miso" />
        <img src="/images/minji.png" class="floating-img deco-minji" alt="minji" />
        <img src="/images/minjun.png" class="floating-img deco-minjun" alt="minjun" />
      </div>
      
      <div class="hero-image">🌸</div>
      <p class="hero-label">2026. 05. 08</p>
      <h1 class="hero-title">엄마 아빠,<br>항상 <span class="highlight">사랑하고 감사합니다</span></h1>
      <p class="hero-subtitle">미소, 민지, 민준이가 준비한 선물함입니다.</p>
    </div>

    <div class="menu-grid">
      <div 
        v-for="feat in features" 
        :key="feat.id" 
        class="menu-card modern-card"
        @click="navigateTo(feat.id)"
      >
        <div class="menu-icon-box" :style="{ backgroundColor: feat.bg }">
          <component :is="feat.icon" :size="32" :color="feat.color" />
        </div>
        <div class="menu-text">
          <h3>{{ feat.title }}</h3>
          <p>{{ feat.desc }}</p>
        </div>
        <ChevronRight class="menu-arrow" :color="feat.color" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.home-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: visible; /* 잘림 방지 */
  position: relative;
  padding-top: 20px;
}

.hero-card {
  background: white;
  padding: 4vh 2rem;
  border-radius: 40px;
  text-align: center;
  margin-bottom: 2vh;
  box-shadow: 0 15px 40px rgba(0,0,0,0.03);
  border: 1px solid rgba(255, 107, 129, 0.1);
  position: relative;
  overflow: visible;
}

/* 플로팅 이미지 그룹 스타일 */
.hero-deco-group {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 5;
}

.floating-img {
  position: absolute;
  width: 140px;
  height: auto;
  filter: drop-shadow(0 12px 25px rgba(0,0,0,0.12));
  animation: float-ani 4s infinite ease-in-out;
  border-radius: 25px;
  z-index: 5;
}

/* 위치 및 크기 개별 조정 */
.deco-miso {
  width: 220px !important;
  top: 50%;
  left: 10px;
  opacity: 1;
  z-index: 5 !important;
  animation: float-left-ani 4s infinite ease-in-out !important;
}

.deco-minji {
  width: 180px !important;
  top: -40px;
  right: 20px;
  animation-delay: -1.5s;
}

.deco-minjun {
  width: 140px;
  bottom: -20px;
  right: 30px;
  animation-delay: -3s;
}

@keyframes float-ani {
  0%, 100% { transform: translateY(0) rotate(-2deg); }
  50% { transform: translateY(-15px) rotate(3deg); }
}

@keyframes float-left-ani {
  0%, 100% { transform: translateY(-50%) rotate(-1deg); }
  50% { transform: translateY(calc(-50% - 20px)) rotate(1deg); }
}

.hero-image { font-size: 6vh; margin-bottom: 1vh; position: relative; z-index: 2; }
.hero-label { font-weight: 700; color: #FF6B81; margin-bottom: 0.5vh; font-size: 1.8vh; position: relative; z-index: 2; }
.hero-title { font-size: min(2.5rem, 5vh); line-height: 1.3; margin-bottom: 1vh; color: #2D3436; position: relative; z-index: 2; }
.highlight { color: #FF6B81; }
.hero-subtitle { color: #636E72; font-size: 2vh; position: relative; z-index: 2; }

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2vh;
  flex: 1;
}

.menu-card {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  padding: 2vh !important;
  cursor: pointer;
  background: white;
  border-radius: 20px;
  transition: 0.3s;
}
.menu-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(255, 107, 129, 0.1); }

.menu-icon-box {
  width: 8vh; height: 8vh;
  border-radius: 15px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.menu-text h3 { font-size: 2.5vh; margin-bottom: 0.3vh; color: #2D3436; }
.menu-text p { color: #636E72; font-size: 1.8vh; }
.menu-arrow { margin-left: auto; opacity: 0.3; transition: all 0.2s; width: 2.5vh; }
.menu-card:hover .menu-arrow { opacity: 1; transform: translateX(5px); }

.fade-in { animation: fadeIn 1s cubic-bezier(0.165, 0.84, 0.44, 1); }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
