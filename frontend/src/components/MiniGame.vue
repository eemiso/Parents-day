<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Heart, Sparkles, Trophy, Timer, Gift, 
  ArrowRight, RefreshCw, X, ChevronRight, CheckCircle2, 
  Star, Mail, Ghost, Camera, Smile, AlertTriangle, ImageIcon
} from 'lucide-vue-next'
import { rouletteStore } from '../store/roulette'

const router = useRouter()

// --- [이미지 설정] 미션별로 다른 이미지를 사용합니다 ---
const m1PngImgs = [
  '/images/minjun.png',
  '/images/minji.png',
  '/images/miso.png'
]
const m3PngImgs = [
  '/images/1.png',
  '/images/2.png',
  '/images/3.png',
  '/images/4.png'
]

// --- 게임 상태 관리 ---
const currentMission = ref(1) 
const gameState = ref<'intro' | 'playing' | 'mission_success' | 'penalty' | 'all_success'>('intro')
const timeLeft = ref(15)
const isShaking = ref(false)
let timerInterval: number

const penalties = [
  "오늘 야식 엄마아빠가 쏘기 ❤️",
]
const currentPenalty = ref("")

// --- Mission 1: 하트 6개 잡기 (가족사진은 방해물) ---
const m1Items = ref<{ id: number, x: number, y: number, content: string, isEmoji: boolean, isTarget: boolean, size: number, speedX: number, speedY: number, rotation: number, rotSpeed: number }[]>([])
const m1TargetCaught = ref(0)
const m1TargetTotal = 6
let m1Animation: number

const startM1 = () => {
  m1Items.value = []
  m1TargetCaught.value = 0
  timeLeft.value = 15
  
  // 각 가족사진당 4개씩 고정으로 생성 (총 12개 방해물)
  m1PngImgs.forEach(src => {
    for (let i = 0; i < 4; i++) {
      spawnM1Item(false, src)
    }
  })
  
  // 하트(타겟) 1개 생성
  spawnM1Item(true)
  startTimer(() => failMission())
  animateM1()
}

const spawnM1Item = (isTarget: boolean, forcedContent?: string) => {
  const content = isTarget ? '❤️' : (forcedContent || m1PngImgs[Math.floor(Math.random() * m1PngImgs.length)])
  const isEmoji = isTarget
  
  // 전체적인 이미지 크기를 대폭 키움 (110px ~ 140px)
  let size = isTarget ? 70 : 110 + Math.random() * 30

  m1Items.value.push({
    id: Math.random(),
    x: 10 + Math.random() * 80,
    y: 10 + Math.random() * 80,
    content,
    isEmoji,
    isTarget,
    size,
    speedX: (Math.random() - 0.5) * 1.5,
    speedY: (Math.random() - 0.5) * 1.5,
    rotation: Math.random() * 20 - 10,
    rotSpeed: (Math.random() - 0.5) * 1.2
  })
}

const animateM1 = () => {
  if (gameState.value !== 'playing') return
  m1Items.value.forEach(item => {
    item.x += item.speedX
    item.y += item.speedY
    item.rotation += item.rotSpeed
    if (item.x < 5 || item.x > 95) item.speedX *= -1
    if (item.y < 5 || item.y > 95) item.speedY *= -1
  })
  // 타겟(하트) 보충
  if (m1Items.value.filter(i => i.isTarget).length < 2 && m1TargetCaught.value < m1TargetTotal) {
    if (Math.random() > 0.98) spawnM1Item(true)
  }
  m1Animation = requestAnimationFrame(animateM1)
}

const clickM1Item = (item: any) => {
  if (item.isTarget) {
    m1TargetCaught.value++
    m1Items.value = m1Items.value.filter(i => i.id !== item.id)
    if (m1TargetCaught.value >= m1TargetTotal) completeMission()
    else spawnM1Item(true)
  } else {
    timeLeft.value = Math.max(0, timeLeft.value - 2)
    isShaking.value = true
    setTimeout(() => isShaking.value = false, 300)
  }
}

// --- Mission 2: 다른 그림 찾기 (PNG 이미지 버전) ---
const m2GridItems = ref<{ src: string, isDifferent: boolean }[]>([])

const startM2 = () => {
  timeLeft.value = 12
  const availableImgs = m1PngImgs.filter(img => img && img.length > 0)
  const shuffled = [...availableImgs].sort(() => Math.random() - 0.5)
  const baseSrc = shuffled[0]
  const diffSrc = shuffled[1] || shuffled[0]
  
  const total = 10 // 5x2 가로형 그리드
  const targetIdx = Math.floor(Math.random() * total)
  m2GridItems.value = Array.from({ length: total }, (_, i) => ({
    src: i === targetIdx ? diffSrc : baseSrc,
    isDifferent: i === targetIdx
  }))
  startTimer(() => failMission())
}

const pickM2Item = (item: any) => {
  if (gameState.value !== 'playing') return
  if (item.isDifferent) completeMission()
  else failMission()
}

// --- Mission 3: 사랑의 순서 기억하기 (가족사진 버전) ---
const m3Sequence = ref<string[]>([])
const m3UserIdx = ref(0)
const m3ShowSeq = ref(true)

const startM3 = () => {
  // 4개의 전용 사진 순서 랜덤 생성
  m3Sequence.value = [...m3PngImgs].sort(() => Math.random() - 0.5).slice(0, 4)
  // 사진이 4개 미만이면 중복 허용해서라도 4개 맞춤
  while (m3Sequence.value.length < 4) {
    m3Sequence.value.push(m3PngImgs[Math.floor(Math.random() * m3PngImgs.length)])
  }
  
  m3UserIdx.value = 0
  m3ShowSeq.value = true
  timeLeft.value = 20
  setTimeout(() => {
    m3ShowSeq.value = false
    startTimer(() => failMission())
  }, 2500)
}

const pickM3Icon = (src: string) => {
  if (m3ShowSeq.value || gameState.value !== 'playing') return
  if (src === m3Sequence.value[m3UserIdx.value]) {
    m3UserIdx.value++
    if (m3UserIdx.value === m3Sequence.value.length) completeMission()
  } else {
    failMission()
  }
}

// --- 공통 로직 ---
const startTimer = (onEnd: () => void) => {
  clearInterval(timerInterval)
  timerInterval = window.setInterval(() => {
    if (timeLeft.value > 0) timeLeft.value--
    else {
      clearInterval(timerInterval)
      onEnd()
    }
  }, 1000)
}

const startGame = () => {
  gameState.value = 'playing'
  if (currentMission.value === 1) startM1()
  else if (currentMission.value === 2) startM2()
  else if (currentMission.value === 3) startM3()
}

const completeMission = () => {
  clearInterval(timerInterval)
  cancelAnimationFrame(m1Animation)
  gameState.value = 'mission_success'
}

const nextMission = () => {
  if (currentMission.value < 3) {
    currentMission.value++
    gameState.value = 'intro'
  } else {
    gameState.value = 'all_success'
    setTimeout(() => router.push('/roulette/play?retry=true'), 3000)
  }
}

const failMission = () => {
  clearInterval(timerInterval)
  cancelAnimationFrame(m1Animation)
  isShaking.value = true
  currentPenalty.value = penalties[Math.floor(Math.random() * penalties.length)]
  gameState.value = 'penalty'
  setTimeout(() => isShaking.value = false, 500)
}

const restartFromOne = () => {
  currentMission.value = 1
  gameState.value = 'intro'
}

onUnmounted(() => {
  clearInterval(timerInterval)
  cancelAnimationFrame(m1Animation)
})
</script>

<template>
  <div class="mg-main-layout" :class="{ 'shake-active': isShaking }">
    <div class="mg-container fade-in">
      
      <header class="mg-header">
        <div class="pill mission-pill">미션 {{ currentMission }} / 3</div>
        <div class="pill timer-pill" :class="{ 'warning': timeLeft < 5 }">
          <Timer :size="18" />
          <span>{{ timeLeft }}초</span>
        </div>
      </header>

      <main class="mg-game-box">
        <div class="mg-card">
          
          <!-- Mission 1: 하트 클릭 (가족사진 방해물) -->
          <div v-if="currentMission === 1" class="stage-view">
            <template v-if="gameState === 'playing'">
              <div class="m1-canvas">
                <div 
                  v-for="item in m1Items" :key="item.id" 
                  class="m1-obj-wrap"
                  :style="{ 
                    left: item.x + '%', 
                    top: item.y + '%', 
                    width: item.size + 'px',
                    transform: `translate(-50%, -50%) rotate(${item.rotation}deg)`
                  }"
                  @mousedown="clickM1Item(item)"
                >
                  <span v-if="item.isEmoji" class="m1-emoji">{{ item.content }}</span>
                  <img v-else :src="item.content" class="m1-png" />
                </div>
              </div>
              <div class="mg-footer-hint">❤️ 사랑의 하트 {{ m1TargetCaught }} / {{ m1TargetTotal }} 개 찾기!</div>
            </template>
            <div v-if="gameState === 'intro'" class="intro-screen">
              <div class="intro-icon">❤️</div>
              <h2>Mission 1: 하트 잡기 미션</h2>
              <p>떠다니는 가족 사진들 사이에서<br><strong>사랑의 하트 ❤️ 6개</strong>를 빠르게 클릭하세요!</p>
              <button @click="startGame" class="btn-primary">미션 시작!</button>
            </div>
          </div>

          <!-- Mission 2: 다른 그림 찾기 (PNG 이미지 버전) -->
          <div v-if="currentMission === 2" class="stage-view">
            <template v-if="gameState === 'playing'">
              <div class="m2-png-grid">
                <div v-for="(item, idx) in m2GridItems" :key="idx" class="m2-png-box" @click="pickM2Item(item)">
                  <img :src="item.src" class="m2-png-img" />
                </div>
              </div>
              <div class="mg-footer-hint">단 한 명만 다른 가족 사진을 찾아보세요!</div>
            </template>
            <div v-if="gameState === 'intro'" class="intro-screen">
              <div class="intro-icon">🔍</div>
              <h2>Mission 2: 다른 사진 찾기</h2>
              <p>똑같은 가족 사진들 중에서<br>단 하나만 다른 사람을 골라보세요!</p>
              <button @click="startGame" class="btn-primary">미션 시작</button>
            </div>
          </div>

          <!-- Mission 3: 사랑의 순서 기억하기 -->
          <div v-if="currentMission === 3" class="stage-view">
            <template v-if="gameState === 'playing'">
              <div class="m3-memory">
                <div v-if="m3ShowSeq" class="m3-show">
                  <div class="m3-hint">가족들의 순서를 꼭 기억하세요!</div>
                  <div class="m3-seq-list">
                    <div v-for="(src, idx) in m3Sequence" :key="idx" class="m3-seq-unit-png">
                      <img :src="src" class="m3-seq-img" />
                    </div>
                  </div>
                </div>
                <div v-else class="m3-input">
                  <p class="m3-input-hint">보았던 순서대로 눌러주세요!</p>
                  <div class="m3-btns-png">
                    <button v-for="src in m3PngImgs" :key="src" @click="pickM3Icon(src)" class="m3-btn-png-box">
                      <img :src="src" class="m3-btn-img" />
                    </button>
                  </div>
                  <div class="m3-progress">
                    <CheckCircle2 v-for="i in m3UserIdx" :key="i" color="#4CAF50" :size="24" />
                  </div>
                </div>
              </div>
            </template>
            <div v-if="gameState === 'intro'" class="intro-screen">
              <div class="intro-icon">🧠</div>
              <h2>Mission 3: 사랑의 순서 기억하기</h2>
              <p>나타나는 4개 아이콘의 순서를 잘 기억했다가<br>그대로 따라 눌러 미션을 완료하세요!</p>
              <button @click="startGame" class="btn-primary">최종 미션 도전</button>
            </div>
          </div>

          <!-- Overlays -->
          <div v-if="gameState === 'mission_success'" class="overlay mission-success">
            <div class="overlay-card">
              <CheckCircle2 :size="70" color="#4CAF50" />
              <h3>미션 성공!</h3>
              <p>{{ currentMission }}단계를 클리어했습니다.</p>
              <button @click="nextMission" class="btn-action">
                <span>{{ currentMission === 3 ? '마지막 선물 확인' : '다음 단계로' }}</span>
                <ChevronRight :size="18" />
              </button>
            </div>
          </div>

          <div v-if="gameState === 'penalty'" class="overlay penalty">
            <div class="overlay-card penalty-card">
              <AlertTriangle :size="50" color="#FF6B81" />
              <h3>실패! 부모님 벌칙 타임</h3>
              <div class="penalty-msg">“ {{ currentPenalty }} ”</div>
              <p>벌칙을 수행하고 다시 1단계부터 도전하세요!</p>
              <button @click="restartFromOne" class="btn-restart">처음부터 재도전하기</button>
            </div>
          </div>

          <div v-if="gameState === 'all_success'" class="overlay all-clear">
            <div class="overlay-card">
              <Trophy :size="90" color="#FFD700" class="trophy-anim" />
              <h2>미션 퍼펙트 클리어! 🎉</h2>
              <p>자랑스러운 우리 부모님!<br>이제 행운의 룰렛을 돌리러 가요.</p>
              <Sparkles color="#FFD700" :size="40" />
            </div>
          </div>

        </div>
      </main>

      <footer v-if="gameState === 'intro' && currentMission === 1">
        <button @click="router.push('/roulette/play')" class="btn-exit">나중에 하기</button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.mg-main-layout {
  height: 100vh; width: 100%; display: flex;
  background: #fdfcfb; overflow: hidden; position: relative;
}

.mg-container {
  flex: 1; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; /* 상단 정렬로 변경 */
  padding: 6vh 2rem 2vh; /* 상단 여백 최적화 */
}

.mg-header { display: flex; gap: 1rem; margin-bottom: 1.5vh; }
.pill {
  background: white; padding: 0.6rem 1.5rem; border-radius: 50px;
  font-weight: 800; color: #2D3436; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  display: flex; align-items: center; gap: 0.6rem;
}
.mission-pill { color: #FF6B81; }
.timer-pill.warning { color: #FF6B81; animation: blink 0.5s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.mg-game-box { width: 100%; max-width: 1050px; height: 70vh; }
.mg-card {
  width: 100%; height: 100%; background: white; border-radius: 40px;
  box-shadow: 0 40px 100px rgba(255, 107, 129, 0.12);
  position: relative; overflow: hidden; border: 1px solid rgba(255, 107, 129, 0.05);
}

.stage-view { height: 100%; display: flex; flex-direction: column; }

/* Mission 1 */
.m1-canvas { flex: 1; position: relative; overflow: hidden; background: #fdfcfb; }
.m1-obj-wrap { position: absolute; cursor: pointer; user-select: none; display: flex; align-items: center; justify-content: center; }
.m1-emoji { font-size: 3.5rem; }
.m1-png { width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 5px 10px rgba(0,0,0,0.1)); }

/* Mission 2 PNG Grid */
.m2-png-grid { 
  display: grid; 
  grid-template-columns: repeat(5, 1fr); /* 가로로 더 넓게 배치 */
  gap: 1rem; 
  padding: 1.5rem 3rem; 
  flex: 1; 
  min-height: 0;
  align-content: center;
}
.m2-png-box {
  width: 100%; height: 100%; 
  background: #fdfcfb; border-radius: 20px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: 0.3s; border: 1px solid #f1f5f9; padding: 8px;
  overflow: hidden;
}
.m2-png-box:hover { transform: scale(1.05); border-color: #FFD1DC; background: white; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
.m2-png-img { max-width: 100%; max-height: 100%; object-fit: contain; }

/* Mission 3 Sequence PNG */
.m3-memory { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 1rem; }
.m3-show { text-align: center; }
.m3-hint { font-weight: 800; color: #FF6B81; font-size: 1.5rem; margin-bottom: 1rem; }
.m3-seq-list { display: flex; gap: 2rem; justify-content: center; }
.m3-seq-unit-png { 
  width: 130px; height: 130px; 
  display: flex; align-items: center; justify-content: center;
  animation: pop-in 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) both; 
}
.m3-seq-img { 
  width: 100%; height: 100%; object-fit: contain; 
  filter: drop-shadow(0 10px 15px rgba(0,0,0,0.12));
}

.m3-input-hint { font-weight: 800; color: #666; margin-bottom: 1rem; font-size: 1.1rem; }
.m3-btns-png { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-bottom: 1rem; }
.m3-btn-png-box { 
  width: 120px; height: 120px; background: none; border: none;
  cursor: pointer; transition: 0.3s; padding: 0;
  display: flex; align-items: center; justify-content: center;
}
.m3-btn-png-box:hover { transform: translateY(-8px) scale(1.05); }
.m3-btn-img { 
  width: 100%; height: 100%; object-fit: contain; 
  filter: drop-shadow(0 8px 12px rgba(0,0,0,0.1));
}
.m3-progress { display: flex; gap: 0.8rem; justify-content: center; }

/* Intro / Overlays */
.intro-screen { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; text-align: center; }
.intro-icon { font-size: 4rem; margin-bottom: 1rem; }
.intro-screen h2 { font-size: 2rem; font-weight: 950; color: #2D3436; margin-bottom: 0.5rem; }
.intro-screen p { color: #636E72; font-weight: 600; line-height: 1.4; margin-bottom: 1.5rem; }

.btn-primary, .btn-action, .btn-restart { padding: 1.2rem 3.5rem; border-radius: 50px; border: none; font-weight: 900; font-size: 1.2rem; cursor: pointer; transition: 0.3s; }
.btn-primary { background: #2D3436; color: white; }
.btn-action { background: #4CAF50; color: white; display: flex; align-items: center; gap: 0.8rem; }
.btn-restart { background: #FF6B81; color: white; margin-top: 1rem; }

.overlay { position: absolute; inset: 0; background: rgba(255,255,255,0.98); display: flex; align-items: center; justify-content: center; z-index: 100; text-align: center; }
.overlay-card { padding: 2rem; display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.penalty-card { background: #FFF5F6; border: 4px dashed #FF6B81; border-radius: 40px; padding: 3rem; width: 90%; max-width: 500px; }
.penalty-msg { font-size: 1.8rem; font-weight: 950; color: #FF6B81; margin: 1.5rem 0; line-height: 1.4; }

.mg-footer-hint { padding: 1.2rem; text-align: center; font-weight: 800; color: #999; border-top: 1px solid #f1f5f9; background: #fff; }
.btn-exit { background: none; border: none; color: #ccc; font-weight: 700; text-decoration: underline; cursor: pointer; margin-top: 2rem; }

@keyframes pop-in { from { transform: scale(0); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.fade-in { animation: fadeIn 0.8s ease-out; }

.trophy-anim { animation: bounce 1s infinite alternate; }
@keyframes bounce { from { transform: translateY(0); } to { transform: translateY(-30px); } }

.shake-active { animation: shake-ani 0.5s cubic-bezier(.36,.07,.19,.97) both; }
@keyframes shake-ani { 10%, 90% { transform: translate3d(-1px, 0, 0); } 20%, 80% { transform: translate3d(2px, 0, 0); } 30%, 50%, 70% { transform: translate3d(-4px, 0, 0); } 40%, 60% { transform: translate3d(4px, 0, 0); } }
</style>
