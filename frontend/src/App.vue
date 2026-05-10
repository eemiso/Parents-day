<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Heart } from 'lucide-vue-next'
import CelebrationEffect from './components/CelebrationEffect.vue'
import CursorTrail from './components/CursorTrail.vue'

const route = useRoute()
const router = useRouter()
const showSplash = ref(true)
const showFireworks = ref(false)

const isHome = computed(() => route.path === '/')

onMounted(() => {
  showFireworks.value = true
  setTimeout(() => { 
    showSplash.value = false 
    setTimeout(() => { showFireworks.value = false }, 8000)
  }, 3000)
})

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="app-container">
    <!-- 전역 배경 및 데코레이션 -->
    <div class="global-bg">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="petals-container">
        <div class="petal" v-for="n in 8" :key="n"></div>
      </div>
    </div>

    <!-- 스플래시 화면 -->
    <transition name="fade">
      <div v-if="showSplash" class="splash-screen">
        <div class="splash-logo">🌸</div>
        <h2 class="splash-text">사랑하는 엄마, 아빠를 위한</h2>
        <h1 class="splash-main-text">어버이날 깜짝 선물</h1>
      </div>
    </transition>

    <CelebrationEffect v-if="showFireworks" />
    <CursorTrail />

    <!-- 헤더 (Thanks To.) -->
    <header class="main-header">
      <div class="header-inner container" @click="goHome">
        <Heart class="logo-icon" :size="24" />
        <span class="logo-text">Thanks To.</span>
      </div>
    </header>

    <!-- 메인 콘텐츠 영역 -->
    <main class="main-content-wrapper">
      <!-- 홈 화면일 때: 레이아웃 자유롭게 -->
      <div v-if="isHome" class="home-layout container">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
        <footer class="main-footer">
          <p>언제나 우리 곁에 있어주셔서 감사합니다.</p>
          <p class="footer-copy">© 2026 Miso, Minji, Minjun. All rights reserved.</p>
        </footer>
      </div>

      <!-- 상세 기능 페이지일 때: 공통 화이트 카드 컨테이너 적용 -->
      <div v-else class="feature-container container">
        <div class="main-feature-card fade-in">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </div>
    </main>
  </div>
</template>

<style>
:root {
  --primary: #FF6B81;
  --bg-gradient: linear-gradient(135deg, #FFF0F3 0%, #FFF9F0 100%);
}

body {
  margin: 0; padding: 0;
  font-family: 'Pretendard', sans-serif;
  overflow: hidden;
  background: #FFF0F3;
}

.container { width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
</style>

<style scoped>
.app-container {
  width: 100vw; height: 100vh;
  display: flex; flex-direction: column;
  background: var(--bg-gradient);
  position: relative; overflow: hidden;
}

/* 전역 배경 장식 */
.global-bg { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.blob { position: absolute; filter: blur(100px); border-radius: 50%; opacity: 0.2; }
.blob-1 { width: 60vh; height: 60vh; background: #FFD1DC; top: -10vh; left: -10vw; }
.blob-2 { width: 50vh; height: 50vh; background: #FFF9C4; bottom: -5vh; right: -5vw; }

.petals-container { position: absolute; inset: 0; overflow: hidden; }
.petal { 
  position: absolute; background: #FFD1DC; border-radius: 150% 0 150% 0; opacity: 0.3; 
  animation: fall 10s infinite linear; top: -10%;
}
.petal:nth-child(1) { left: 10%; width: 15px; height: 15px; animation-duration: 7s; }
.petal:nth-child(2) { left: 30%; width: 10px; height: 10px; animation-duration: 9s; animation-delay: 2s; }
.petal:nth-child(3) { left: 55%; width: 18px; height: 18px; animation-duration: 11s; animation-delay: 1s; }
.petal:nth-child(4) { left: 75%; width: 12px; height: 12px; animation-duration: 8s; animation-delay: 3s; }
.petal:nth-child(5) { left: 90%; width: 16px; height: 16px; animation-duration: 10s; animation-delay: 0.5s; }
.petal:nth-child(6) { left: 20%; width: 14px; height: 14px; animation-duration: 12s; animation-delay: 4s; }
.petal:nth-child(7) { left: 45%; width: 11px; height: 11px; animation-duration: 8.5s; animation-delay: 1.5s; }
.petal:nth-child(8) { left: 80%; width: 13px; height: 13px; animation-duration: 9.5s; animation-delay: 2.5s; }

@keyframes fall {
  0% { transform: translateY(0vh) rotate(0deg); opacity: 0; }
  10% { opacity: 0.5; }
  90% { opacity: 0.5; }
  100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}

/* 헤더 */
.main-header {
  height: 80px; display: flex; align-items: center;
  position: relative; z-index: 100; flex-shrink: 0;
}
.header-inner { display: flex; align-items: center; gap: 10px; cursor: pointer; width: fit-content; }
.logo-icon { color: var(--primary); fill: var(--primary); }
.logo-text { font-size: 1.6rem; font-weight: 900; color: #2D3436; letter-spacing: -0.5px; }

/* 메인 레이아웃 */
.main-content-wrapper { flex: 1; position: relative; z-index: 10; display: flex; flex-direction: column; min-height: 0; }

.home-layout { flex: 1; display: flex; flex-direction: column; padding-bottom: 20px; }

.feature-container { 
  flex: 1; display: flex; align-items: center; justify-content: center; 
  padding-bottom: 40px; 
  min-height: 0; /* 내부 스크롤 보장 */
}

/* 핵심: 상세 페이지용 공통 화이트 카드 */
.main-feature-card {
  background: rgba(255, 255, 255, 0.95);
  width: 100%; height: 100%;
  border-radius: 50px;
  box-shadow: 0 40px 100px rgba(255, 107, 129, 0.1);
  display: flex; flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* 푸터 */
.main-footer { margin-top: auto; text-align: center; color: #636E72; opacity: 0.4; font-size: 0.9rem; padding: 10px 0; }
.footer-copy { font-size: 0.8rem; margin-top: 4px; }

/* 스플래시 */
.splash-screen {
  position: fixed; inset: 0; background: white; z-index: 2000;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center;
}
.splash-logo { font-size: 5rem; margin-bottom: 2rem; animation: heartbeat 1.5s infinite; }
.splash-text { font-weight: 500; color: #636E72; margin-bottom: 0.5rem; }
.splash-main-text { font-size: 2.8rem; color: #2D3436; font-weight: 900; }

@keyframes heartbeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.4s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.fade-in { animation: fadeIn 0.8s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
