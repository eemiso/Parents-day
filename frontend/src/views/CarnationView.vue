<script setup lang="ts">
import { ref } from 'vue'
import { ChevronLeft, Heart, Sparkles, Droplets } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import CelebrationEffect from '../components/CelebrationEffect.vue'

const router = useRouter()
const bloomState = ref<'seed' | 'growing' | 'bloomed'>('seed')
const showFireworks = ref(false)

const startBlooming = () => {
  if (bloomState.value !== 'seed') return
  
  bloomState.value = 'growing'
  
  // 3초 후 완개
  setTimeout(() => {
    bloomState.value = 'bloomed'
    showFireworks.value = true
  }, 3000)
}

const goBack = () => {
  router.push('/')
}
</script>

<template>
  <div class="carnation-view">
    <CelebrationEffect v-if="showFireworks" />
    
    <div class="top-nav">
      <button @click="goBack" class="back-btn">
        <ChevronLeft :size="24" />
        메인으로
      </button>
    </div>

    <div class="main-stage">
      <!-- 아이들 누끼 이미지 그룹 (물을 주는 순간 등장) -->
      <div v-if="bloomState !== 'seed'" class="kids-global-group" :class="bloomState">
        <img v-for="n in [10, 11, 12, 13, 14, 15, 16]" :key="n" :src="`/images/${n}.png`" :class="['kid-img', `kid-${n}`]" alt="kid" />
      </div>

      <div class="message-area" :class="{ visible: bloomState !== 'seed' }">
        <h1 v-if="bloomState === 'bloomed'" class="final-msg">
          엄마, 아빠 사랑해요! <br>
          <span class="sub">항상 건강하고 행복하세요</span>
        </h1>
        <h1 v-else class="guide-msg">부모님을 향한 마음을 <br>꽃으로 피워보세요</h1>
      </div>

      <div class="flower-container">
        <!-- 화분 -->
        <div class="pot"></div>
        
        <!-- 줄기 -->
        <div class="stem" :class="bloomState"></div>
        
        <!-- 잎사귀 -->
        <div class="leaf leaf-1" :class="bloomState"></div>
        <div class="leaf leaf-2" :class="bloomState"></div>

        <!-- 꽃머리 -->
        <div class="flower-head" :class="bloomState">
          <div class="petal p1"></div>
          <div class="petal p2"></div>
          <div class="petal p3"></div>
          <div class="petal p4"></div>
          <div class="petal p5"></div>
          <div class="petal p6"></div>
        </div>
      </div>

      <div class="action-area">
        <button 
          v-if="bloomState === 'seed'" 
          @click="startBlooming" 
          class="bloom-btn"
        >
          <Droplets :size="20" /> 사랑의 물 주기
        </button>
        <button 
          v-else-if="bloomState === 'bloomed'" 
          @click="bloomState = 'seed'; showFireworks = false" 
          class="retry-btn"
        >
          다시 피우기
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.carnation-view {
  width: 100%; height: 100%;
  display: flex; flex-direction: column;
  padding: 2rem;
  background: radial-gradient(circle at center, #FFF5F7 0%, #FFF0F3 100%);
  position: relative;
  overflow: hidden;
}

.top-nav { position: relative; z-index: 100; }
.back-btn {
  display: flex; align-items: center; gap: 0.5rem;
  background: white; border: none; padding: 0.8rem 1.2rem;
  border-radius: 15px; font-weight: 700; color: #636E72;
  cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.main-stage {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 3rem;
}

.message-area { text-align: center; min-height: 120px; transition: 0.5s; }
.guide-msg { font-size: 2rem; font-weight: 900; color: #2D3436; line-height: 1.4; }
.final-msg { font-size: 2.5rem; font-weight: 900; color: #FF4757; line-height: 1.3; animation: bounceIn 1s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.final-msg .sub { font-size: 1.2rem; color: #636E72; font-weight: 600; display: block; margin-top: 1rem; }

@keyframes bounceIn {
  from { opacity: 0; transform: scale(0.5); }
  to { opacity: 1; transform: scale(1); }
}

/* 꽃 애니메이션 핵심 */
.flower-container {
  position: relative; width: 200px; height: 350px;
  display: flex; flex-direction: column; align-items: center;
}

/* 아이들 누끼 이미지 전체 화면 배치 및 새로운 효과 */
.kids-global-group {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

.kid-img {
  position: absolute;
  width: 320px; /* 12~16번 대상 크기 대폭 상향 */
  max-height: 35vh;
  object-fit: contain;
  filter: drop-shadow(0 12px 25px rgba(0,0,0,0.18));
  opacity: 0;
  animation: 
    kid-pop-in 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards,
    kid-cheer 3.5s infinite ease-in-out 0.8s;
}

/* 10, 11번 개별 설정 (상대적 크기 유지) */
.kid-10, .kid-11 {
  width: 160px !important;
}

/* 10번 위치: 버튼 아래 */
.kid-10 {
  top: 11% !important;
  left: 1% !important;
}

/* 겹침 방지를 위한 정밀 배치 (사이드에서 살짝 중앙으로 이동) */
/* 이미지들을 화면 가장자리로 배치하여 중앙 카네이션을 가리지 않도록 함 */
.kid-10 { /* 왼쪽 상단 */
  top: 5%;
  left: 0%;
  transform: none;
  animation-delay: 0s, 0.8s;
}
.kid-11 { /* 왼쪽 하단 */
  bottom: 5%;
  left: 0%;
  transform: none;
  animation-delay: 0.2s, 1s;
}
.kid-12 { /* 오른쪽 상단 */
  top: 5%;
  right: 0%;
  transform: none;
  animation-delay: 0.4s, 1.2s;
}
.kid-13 { /* 오른쪽 하단 */
  bottom: 5%;
  right: 0%;
  transform: none;
  animation-delay: 0.6s, 1.4s;
}
.kid-14 { /* 왼쪽 중간 (중앙보다 위쪽) */
  top: 30%;
  left: 0%;
  transform: none;
  animation-delay: 0.8s, 1.6s;
}
.kid-15 { /* 오른쪽 중간 (중앙보다 위쪽) */
  top: 30%;
  right: 0%;
  transform: none;
  animation-delay: 1s, 1.8s;
}
.kid-16 { /* 하단 중간 왼쪽으로 살짝 이동 */
  bottom: 20%;
  left: 20%;
  transform: none;
  animation-delay: 1.2s, 2s;
}

/* 꽃이 피었을 때 강조 효과 */
.kids-global-group.bloomed .kid-img {
  filter: drop-shadow(0 0 30px rgba(255, 71, 87, 0.6));
}

@keyframes kid-pop-in {
  from { opacity: 0; transform: scale(0.5) translateY(50px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes kid-cheer {
  0%, 100% { transform: rotate(-3deg); }
  50% { transform: rotate(3deg); }
}

.pot {
  position: absolute; bottom: 0;
  width: 100px; height: 80px;
  background: #D4A373;
  clip-path: polygon(0 0, 100% 0, 85% 100%, 15% 100%);
  z-index: 10;
}

.stem {
  position: absolute; bottom: 70px;
  width: 8px; height: 0;
  background: #4CAF50;
  transition: height 2s ease-in-out;
  border-radius: 4px;
}
.stem.growing, .stem.bloomed { height: 180px; }

.leaf {
  position: absolute; width: 40px; height: 20px;
  background: #81C784; border-radius: 50% 0 50% 0;
  opacity: 0; transition: 1s 1s;
}
.leaf.growing, .leaf.bloomed { opacity: 1; }
.leaf-1 { bottom: 120px; left: 60px; transform: rotate(-30deg); }
.leaf-2 { bottom: 160px; right: 60px; transform: rotate(40deg) scaleX(-1); }

.flower-head {
  position: absolute; bottom: 240px;
  width: 0; height: 0;
  display: flex; align-items: center; justify-content: center;
  transition: all 1s 2s;
}
.flower-head.bloomed { width: 120px; height: 120px; }

.petal {
  position: absolute; width: 60px; height: 80px;
  background: #FF4757; border-radius: 50% 50% 10% 10%;
  opacity: 0; transform-origin: bottom center;
  transition: 1s;
  box-shadow: inset 0 0 20px rgba(0,0,0,0.1);
}
.flower-head.bloomed .petal { opacity: 1; }

.p1 { transform: rotate(0deg); }
.p2 { transform: rotate(60deg); }
.p3 { transform: rotate(120deg); }
.p4 { transform: rotate(180deg); }
.p5 { transform: rotate(240deg); }
.p6 { transform: rotate(300deg); }

.bloom-btn, .retry-btn {
  padding: 1rem 2.5rem; border-radius: 50px; border: none;
  font-size: 1.2rem; font-weight: 800; cursor: pointer;
  display: flex; align-items: center; gap: 0.8rem;
  transition: 0.3s;
}
.bloom-btn { background: #FF4757; color: white; box-shadow: 0 10px 25px rgba(255, 71, 87, 0.3); }
.bloom-btn:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(255, 71, 87, 0.4); }

.retry-btn { background: white; color: #636E72; border: 1px solid #EEE; }
</style>
