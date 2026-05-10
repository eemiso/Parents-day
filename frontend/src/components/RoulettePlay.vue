<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Heart, RefreshCw, ChevronLeft, 
  Sparkles, Gift, PartyPopper, Star, Clover, RotateCcw
} from 'lucide-vue-next'
import { rouletteStore } from '../store/roulette'

const router = useRouter()
const route = useRoute()

const canvasRef = ref<HTMLCanvasElement | null>(null)
const isSpinning = ref(false)
const showResult = ref(false)
const resultGift = ref<any>(null)
const rotation = ref(0)

// 재도전 모드 확인
const isRetry = computed(() => route.query.retry === 'true')

// 룰렛 아이템
const gifts = computed(() => {
  return [
    { text: '현금 15만원 💰', color: '#FFB5C5', textColor: '#8E5A5A' },
    { text: '커피 한잔 ☕', color: '#E0F2F1', textColor: '#4F7A7A' },
    { text: '특급 안마 💆 15분', color: '#F3E5F5', textColor: '#7A5A7A' },
    { text: '맛있는 저녁 쏜다🍽️', color: '#FFF9C4', textColor: '#8E7A5A' },
    { text: rouletteStore.momGift || '엄마 소원 💖', color: '#FFEBEE', textColor: '#A64452' },
    { text: rouletteStore.dadGift || '아빠 소원 💙', color: '#E3F2FD', textColor: '#446A8E' },
    { text: '효도 쿠폰 3장 🎫', color: '#F1F8E9', textColor: '#5A7A5A' },
    { text: '다음 기회에...😅', color: '#ECEFF1', textColor: '#546E7A' }
  ]
})

// 초기화
const resetRoulette = () => {
  if (confirm('처음부터 다시 시작할까요?')) {
    router.push('/roulette/play')
    rotation.value = 0
    showResult.value = false
    setTimeout(() => drawRoulette(0), 100)
  }
}

// 원래 디자인의 룰렛 그리기 로직 (복구됨)
const drawRoulette = (angle = 0) => {
  if (!canvasRef.value) return
  const canvas = canvasRef.value
  const context = canvas.getContext('2d')
  if (!context) return
  
  const width = canvas.width
  const height = canvas.height
  const centerX = width / 2
  const centerY = height / 2
  const radius = width / 2 - 35
  
  context.clearRect(0, 0, width, height)
  
  // 1. 외곽 골드 링 (원래 디자인)
  context.save()
  context.beginPath()
  context.arc(centerX, centerY, radius + 20, 0, Math.PI * 2)
  const outerGradient = context.createRadialGradient(centerX, centerY, radius + 5, centerX, centerY, radius + 25)
  outerGradient.addColorStop(0, '#D4AF37')
  outerGradient.addColorStop(0.5, '#F9E29C')
  outerGradient.addColorStop(1, '#C5A028')
  context.fillStyle = outerGradient
  context.shadowBlur = 15
  context.shadowColor = 'rgba(0,0,0,0.1)'
  context.fill()
  context.restore()

  // 2. 외곽 전구 효과 (원래 디자인)
  const numBulbs = 24
  for (let i = 0; i < numBulbs; i++) {
    const bulbAngle = (i * Math.PI * 2) / numBulbs
    const bulbX = centerX + Math.cos(bulbAngle) * (radius + 13)
    const bulbY = centerY + Math.sin(bulbAngle) * (radius + 13)
    
    context.beginPath()
    context.arc(bulbX, bulbY, 4, 0, Math.PI * 2)
    const isLit = isSpinning.value ? Math.random() > 0.5 : true
    context.fillStyle = isLit ? '#FFF9C4' : '#E0E0E0'
    if (isLit) {
      context.shadowBlur = 10
      context.shadowColor = '#FFF9C4'
    }
    context.fill()
    context.shadowBlur = 0
  }

  // 3. 룰렛 조각
  const numGifts = gifts.value.length
  const arcSize = (Math.PI * 2) / numGifts
  
  gifts.value.forEach((gift, i) => {
    const startAngle = angle + i * arcSize
    const endAngle = startAngle + arcSize
    
    context.beginPath()
    context.moveTo(centerX, centerY)
    context.arc(centerX, centerY, radius, startAngle, endAngle)
    context.fillStyle = gift.color
    context.fill()
    
    // 텍스트
    context.save()
    context.translate(centerX, centerY)
    context.rotate(startAngle + arcSize / 2)
    context.textAlign = 'right'
    context.fillStyle = gift.textColor
    context.font = 'bold 16px "Pretendard", sans-serif'
    context.fillText(gift.text, radius - 30, 6)
    context.restore()
    
    // 구분선
    context.beginPath()
    context.moveTo(centerX, centerY)
    context.lineTo(centerX + Math.cos(startAngle) * radius, centerY + Math.sin(startAngle) * radius)
    context.strokeStyle = 'rgba(255,255,255,0.4)'
    context.lineWidth = 2
    context.stroke()
  })

  // 4. 화이트 이너 보더
  context.beginPath()
  context.arc(centerX, centerY, radius, 0, Math.PI * 2)
  context.strokeStyle = 'rgba(255,255,255,0.5)'
  context.lineWidth = 5
  context.stroke()
}

// 스핀 로직 (조작된 로직 유지)
const spin = () => {
  if (isSpinning.value) return
  isSpinning.value = true
  showResult.value = false
  
  const numGifts = gifts.value.length
  const arcSize = 360 / numGifts
  
  let targetIndex: number
  if (!isRetry.value) {
    targetIndex = 7 // 첫 번째는 무조건 꽝
  } else {
    targetIndex = Math.floor(Math.random() * (numGifts - 1)) // 재도전은 랜덤 당첨
  }
  
  const spinRounds = 10 + Math.floor(Math.random() * 5)
  // 멈출 각도 계산 (상단 270도 지점 기준, 캔버스 드로잉 각도와 맞춤)
  // drawRoulette에서 angle + i * arcSize 로 그리므로, 
  // 포인터(상단 270도)에 오게 하려면 (270 - (index * arcSize + arcSize/2))
  const targetAngle = 270 - (targetIndex * arcSize + arcSize / 2)
  const totalRotation = (spinRounds * 360) + targetAngle
  
  const duration = 5000
  const startTime = performance.now()
  const startRotation = (rotation.value * 180 / Math.PI) % 360
  
  const animate = (timestamp: number) => {
    const elapsed = timestamp - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easedProgress = 1 - Math.pow(1 - progress, 4)
    const currentAngle = startRotation + (totalRotation - startRotation) * easedProgress
    
    rotation.value = (currentAngle * Math.PI) / 180
    drawRoulette(rotation.value)

    if (progress < 1) {
      requestAnimationFrame(animate)
    } else {
      isSpinning.value = false
      resultGift.value = gifts.value[targetIndex]
      setTimeout(() => {
        showResult.value = true
      }, 300)
    }
  }
  requestAnimationFrame(animate)
}

onMounted(() => {
  setTimeout(() => drawRoulette(0), 100)
})
</script>

<template>
  <div class="roulette-component fade-in">
    <!-- 감성 배경 장식 (원래 디자인 유지) -->
    <div class="decorative-items">
      <div class="bg-item petal-1">🌸</div>
      <div class="bg-item heart-1">💖</div>
      <div class="bg-item star-1">✨</div>
      <div class="bg-item ribbon-1">🎀</div>
      <div class="bg-item flower-1">🌺</div>
      <div class="bg-item gift-1">🎁</div>
    </div>

    <div class="roulette-container">
      <header class="header-section">
        <button @click="router.push('/')" class="btn-back-minimal">
          <ChevronLeft :size="18" />
          <span>처음으로</span>
        </button>
        
        <div class="title-group">
          <Clover class="clover-icon" :size="32" color="#6AB04C" />
          <h1 class="main-title">행운의 선물 룰렛</h1>
        </div>
      </header>

      <div class="roulette-center-area">
        <div class="roulette-visual-wrapper">
          <div class="outer-glow" :class="{ 'is-spinning': isSpinning }"></div>
          <div class="pointer-3d">
            <div class="pointer-arrow"></div>
          </div>
          <canvas ref="canvasRef" width="560" height="560" class="roulette-canvas"></canvas>
          <button @click="spin" class="spin-button-glossy" :disabled="isSpinning">
            <div class="spin-inner">
              <span v-if="!isSpinning">SPIN!</span>
              <RefreshCw v-else class="rotating" />
            </div>
          </button>

          <!-- 초기화 버튼 추가 (우측 작게) -->
          <button @click="resetRoulette" class="btn-reset-small" title="초기화">
            <RotateCcw :size="14" />
            <span>초기화</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 결과 모달 -->
    <Transition name="pop">
      <div v-if="showResult" class="modal-overlay">
        <div class="modal-card">
          <PartyPopper :size="48" color="#FF6B81" class="modal-icon" />
          <h2>축하합니다!</h2>
          <div class="winner-box">
            <div class="winner-label">당첨된 선물</div>
            <div class="winner-text">{{ resultGift?.text }}</div>
          </div>
          <p class="modal-desc">부모님께 최고의 선물이 될 거예요! 💝</p>
          <div class="modal-btns">
            <button @click="showResult = false" class="btn-close">확인</button>
            <button v-if="resultGift?.text.includes('😅')" @click="router.push('/minigame')" class="btn-retry-action">
              한 번 더 도전하기
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
/* 원래 스타일 유지 */
.roulette-component {
  width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center;
  position: relative; padding: 40px;
}

.decorative-items { position: absolute; inset: 0; pointer-events: none; }
.bg-item { position: absolute; font-size: 2.5rem; opacity: 0.1; animation: float 10s infinite alternate; }
.petal-1 { top: 10%; left: 10%; }
.heart-1 { top: 20%; right: 15%; animation-delay: -2s; }
.star-1 { bottom: 20%; left: 15%; animation-delay: -5s; }
.ribbon-1 { bottom: 10%; right: 10%; animation-delay: -7s; }
.flower-1 { top: 50%; left: 5%; }
.gift-1 { top: 40%; right: 5%; }

@keyframes float {
  from { transform: translateY(0) rotate(0deg); }
  to { transform: translateY(-30px) rotate(15deg); }
}

.roulette-container {
  width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center;
  position: relative; z-index: 10;
}

.header-section { width: 100%; text-align: center; margin-bottom: 25px; position: relative; }
.btn-back-minimal {
  position: absolute; left: 0; top: 0;
  background: white; border: 1px solid #f0f0f0; padding: 10px 22px;
  border-radius: 50px; display: flex; align-items: center; gap: 8px;
  font-weight: 700; color: #777; cursor: pointer; transition: 0.3s;
}
.btn-back-minimal:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.06); }

.title-group { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.main-title { font-size: 2.8rem; font-weight: 950; color: #2D3436; letter-spacing: -1px; }

.roulette-center-area { flex: 1; display: flex; align-items: center; justify-content: center; min-height: 0; }

.roulette-visual-wrapper {
  position: relative; width: 540px; height: 540px;
  display: flex; align-items: center; justify-content: center;
  scale: 0.9;
}

.outer-glow {
  position: absolute; width: 530px; height: 530px;
  background: radial-gradient(circle, rgba(255, 107, 129, 0.25) 0%, transparent 70%);
  border-radius: 50%; opacity: 0.6; transition: 0.5s;
}
.is-spinning { animation: pulse-glow 1s infinite alternate; }
@keyframes pulse-glow { from { scale: 1; opacity: 0.4; } to { scale: 1.05; opacity: 0.8; } }

.roulette-canvas { position: relative; z-index: 2; filter: drop-shadow(0 20px 60px rgba(0,0,0,0.08)); }

.pointer-3d { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); z-index: 15; }
.pointer-arrow {
  width: 0; height: 0;
  border-left: 20px solid transparent; border-right: 20px solid transparent;
  border-top: 45px solid #FF4D6D;
  filter: drop-shadow(0 5px 10px rgba(255, 77, 109, 0.4));
}

.spin-button-glossy {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  z-index: 20; width: 100px; height: 100px;
  background: white; border: none; border-radius: 50%;
  padding: 10px; cursor: pointer; transition: 0.3s;
}
.spin-button-glossy:hover:not(:disabled) { scale: 1.08; box-shadow: 0 15px 40px rgba(255, 107, 129, 0.3); }

.spin-inner {
  width: 100%; height: 100%; border-radius: 50%;
  background: linear-gradient(135deg, #FF6B81 0%, #FF4D6D 100%);
  display: flex; align-items: center; justify-content: center;
  color: white; font-weight: 950; font-size: 1.2rem;
}
.rotating { animation: spin-anim 1s infinite linear; }
@keyframes spin-anim { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* 초기화 버튼 스타일 */
.btn-reset-small {
  position: absolute; bottom: 20px; right: -50px;
  background: rgba(0,0,0,0.03); border: none; padding: 6px 12px;
  border-radius: 20px; color: #aaa; font-size: 0.7rem; font-weight: 700;
  display: flex; align-items: center; gap: 4px; cursor: pointer; transition: 0.2s;
  z-index: 30;
}
.btn-reset-small:hover { background: rgba(0,0,0,0.08); color: #888; }

/* 결과 모달 */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(45, 52, 54, 0.7);
  backdrop-filter: blur(10px); z-index: 1000;
  display: flex; align-items: center; justify-content: center;
}
.modal-card {
  background: white; width: 90%; max-width: 480px;
  border-radius: 45px; padding: 50px; text-align: center;
  box-shadow: 0 50px 100px rgba(0,0,0,0.4);
}
.modal-icon { margin-bottom: 20px; }
.winner-box {
  margin: 30px 0; padding: 35px; background: #FFF5F6;
  border-radius: 35px; border: 3px dashed #FF6B81;
}
.winner-label { font-size: 1.1rem; color: #FF6B81; font-weight: 700; margin-bottom: 12px; }
.winner-text { font-size: 2.2rem; font-weight: 950; color: #2D3436; }
.modal-desc { color: #636E72; font-weight: 600; margin-bottom: 35px; }
.modal-btns { display: flex; flex-direction: column; gap: 12px; }

.btn-close, .btn-retry-action {
  width: 100%; padding: 18px; border-radius: 50px; border: none;
  font-size: 1.15rem; font-weight: 800; cursor: pointer; transition: 0.3s;
}
.btn-close { background: #2D3436; color: white; }
.btn-retry-action { background: #FF6B81; color: white; }

.pop-enter-active { animation: pop-in 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
@keyframes pop-in { from { scale: 0.8; opacity: 0; } to { scale: 1; opacity: 1; } }
</style>
