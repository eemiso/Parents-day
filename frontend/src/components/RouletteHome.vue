<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { rouletteStore } from '../store/roulette'

const router = useRouter()
const momGift = ref(rouletteStore.momGift)
const dadGift = ref(rouletteStore.dadGift)

const createWheel = () => {
  rouletteStore.setGifts(momGift.value, dadGift.value)
  router.push('/roulette/play')
}
</script>

<template>
  <div class="roulette-home-container">
    <!-- Top Nav -->
    <nav class="top-nav">
      <button @click="router.push('/')" class="btn-back-home">
        <span>← 처음으로</span>
      </button>
    </nav>

    <!-- Visual Decorations -->
    <div class="bg-deco deco-heart-1">❤️</div>
    <div class="bg-deco deco-gift-1">🎁</div>
    <div class="bg-deco deco-star-1">✨</div>
    <div class="bg-deco deco-ribbon-1">🎀</div>

    <div class="setup-card fade-in">
      <div class="header-section">
        <h2 class="main-title">부모님 소원 룰렛</h2>
        <p class="description">평소에 갖고 싶으셨던 선물을 입력해주세요!</p>
      </div>

      <!-- Decorative Divider -->
      <div class="event-divider">
        <div class="divider-line"></div>
        <div class="divider-badge">💝 부모님 이벤트</div>
        <div class="divider-line"></div>
      </div>

      <div class="input-form shadow-premium">
        <div class="input-group">
          <label class="input-label">엄마 소원 💖</label>
          <input v-model="momGift" type="text" placeholder="엄마의 마음속 소원은 무엇인가요?" class="custom-input" />
        </div>

        <div class="input-group">
          <label class="input-label">아빠 소원 💙</label>
          <input v-model="dadGift" type="text" placeholder="아빠의 마음속 소원은 무엇인가요?" class="custom-input" />
        </div>

        <div class="action-area">
          <button @click="createWheel" class="btn-create-wheel-premium">
            <span>🎁 룰렛판 만들기</span>
          </button>
        </div>
      </div>

      <p class="bottom-hint">입력하신 소원이 룰렛판의 한 조각이 됩니다!</p>
    </div>
  </div>
</template>

<style scoped>
.roulette-home-container {
  height: 100%; width: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 0;
  background: radial-gradient(circle at top, #FFF5F6 0%, #FFFDF8 100%);
  position: relative; overflow: hidden;
}

.top-nav { position: absolute; top: 2vh; left: 3vw; z-index: 100; }
.btn-back-home {
  background: white; border: 1px solid #FFD1DC; padding: 1vh 1.8rem;
  border-radius: 50px; font-weight: 700; cursor: pointer; transition: 0.2s;
  color: #FF6B81; font-size: 1.6vh; box-shadow: 0 4px 10px rgba(255,107,129,0.1);
}
.btn-back-home:hover { background: #FFF5F6; transform: translateX(-3px); }

/* Decorations */
.bg-deco { position: absolute; font-size: 5vh; opacity: 0.15; pointer-events: none; animation: float 5s infinite ease-in-out; }
.deco-heart-1 { top: 15%; left: 15%; color: #FF6B81; }
.deco-gift-1 { top: 25%; right: 15%; color: #F0932B; animation-delay: 1s; }
.deco-star-1 { bottom: 20%; left: 20%; color: #F1C40F; animation-delay: 2s; }
.deco-ribbon-1 { bottom: 15%; right: 20%; color: #BE2EDD; animation-delay: 1.5s; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); }
  50% { transform: translateY(-20px) rotate(10deg) scale(1.1); }
}

.setup-card { text-align: center; max-width: 620px; width: 92%; z-index: 10; }

.main-title { 
  font-size: min(2.8rem, 4.8vh); font-weight: 950; color: #2D3436; 
  margin-bottom: 0.8vh; letter-spacing: -1px;
}
.description { 
  font-size: 1.8vh; color: #636E72; line-height: 1.4; 
  margin-bottom: 3vh; font-weight: 500;
}

/* Divider Styles */
.event-divider {
  display: flex; align-items: center; justify-content: center;
  gap: 1.5rem; margin-bottom: 3.5vh; width: 100%;
}
.divider-line {
  flex: 1; height: 1px; background: #FFD1DC; opacity: 0.6;
}
.divider-badge {
  background: white; border: 1px solid #FFD1DC; padding: 0.6vh 1.5rem;
  border-radius: 50px; font-weight: 800; font-size: 1.5vh; color: #FF6B81;
  box-shadow: 0 4px 10px rgba(255,107,129,0.08); white-space: nowrap;
}

.input-form {
  background: white; padding: 3vh 3.5rem; border-radius: 40px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.03), 0 10px 20px rgba(255,107,129,0.05);
  border: 1px solid rgba(255,107,129,0.05); text-align: left;
}

.input-group { margin-bottom: 2vh; }
.input-label { display: block; font-weight: 800; color: #444; margin-bottom: 0.5vh; font-size: 1.7vh; }

.custom-input {
  width: 100%; padding: 1.4vh 1.5rem; border-radius: 15px;
  border: 2px solid #F1F5F9; font-size: 1.8vh; outline: none;
  transition: all 0.3s; background: #FAFBFC;
}
.custom-input:focus { border-color: #FF6B81; background: white; box-shadow: 0 0 20px rgba(255,107,129,0.1); }

.action-area { margin-top: 3.5vh; }
.btn-create-wheel-premium {
  width: 100%; padding: 1.8vh; border-radius: 18px; border: none;
  background: linear-gradient(135deg, #FF6B81, #FF8E9E);
  color: white; font-weight: 900; font-size: 2.3vh; cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 25px rgba(255, 107, 129, 0.2);
}
.btn-create-wheel-premium:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 15px 35px rgba(255, 107, 129, 0.3);
}

.bottom-hint { margin-top: 2.5vh; font-size: 1.5vh; color: #BBB; font-weight: 600; }

.fade-in { animation: fadeIn 0.8s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
