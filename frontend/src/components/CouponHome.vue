<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Ticket } from 'lucide-vue-next'

const router = useRouter()

const startCoupons = () => {
  router.push('/coupons/list')
}
</script>

<template>
  <div class="coupon-container">
    <!-- Decorative Background Elements -->
    <div class="bg-deco deco-1">❤️</div>
    <div class="bg-deco deco-2">🎫</div>
    <div class="bg-deco deco-3">✨</div>
    <div class="bg-deco deco-4">🌸</div>

    <div class="coupon-intro-card fade-in">
      <div class="gift-icon-box animate-float">🎫</div>
      <h2 class="intro-title">사랑하는 부모님을 위한<br>효도 쿠폰 세트</h2>
      <p class="intro-desc">
        미소, 민지, 민준이가 준비한 작은 약속들입니다.<br>
        필요하실 때 언제든 꺼내서 보여주세요!
      </p>
      
      <div class="btn-container">
        <button @click="startCoupons" class="btn-coupon-premium">
          <Ticket :size="28" />
          <span>쿠폰 보따리 열어보기</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.coupon-container {
  height: 100%; width: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
  padding-top: 10vh; 
  background: linear-gradient(135deg, #FFF5F6 0%, #FFFDFB 100%);
  position: relative; overflow: hidden;
}

/* Background Decorations */
.bg-deco { position: absolute; font-size: 4vh; opacity: 0.15; pointer-events: none; }
.deco-1 { top: 10%; left: 10%; animation: float 4s infinite ease-in-out; }
.deco-2 { top: 20%; right: 15%; animation: float 5s infinite ease-in-out 1s; }
.deco-3 { bottom: 20%; left: 15%; animation: float 6s infinite ease-in-out 2s; }
.deco-4 { bottom: 15%; right: 10%; animation: float 4.5s infinite ease-in-out 0.5s; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
}

.coupon-intro-card {
  text-align: center;
  max-width: 650px;
  width: 95%;
  z-index: 10;
}

.gift-icon-box { 
  font-size: 9vh; margin-bottom: 2vh; 
  filter: drop-shadow(0 10px 20px rgba(255, 107, 129, 0.2));
}

.intro-title { 
  font-size: min(2.8rem, 5vh); font-weight: 900; color: #2D3436; 
  line-height: 1.4; margin-bottom: 2.5vh; 
}

.intro-desc { 
  font-size: 2.2vh; color: #636E72; line-height: 1.8; 
  margin-bottom: 6vh; font-weight: 500;
}

.btn-container { display: flex; justify-content: center; width: 100%; margin-bottom: 4vh; }

.btn-coupon-premium {
  display: inline-flex; align-items: center; justify-content: center; gap: 1rem;
  padding: 2vh 4.5rem; border-radius: 80px; border: none;
  background: linear-gradient(135deg, #FF6B81, #FF8E9E);
  color: white; font-weight: 900; font-size: 2.4vh;
  cursor: pointer; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 30px rgba(255, 107, 129, 0.3), 0 0 0 0 rgba(255, 107, 129, 0);
}

.btn-coupon-premium:hover {
  transform: translateY(-8px) scale(1.05);
  box-shadow: 0 20px 40px rgba(255, 107, 129, 0.4), 0 0 20px 5px rgba(255, 107, 129, 0.2);
}

.intro-note { font-size: 1.7vh; color: #999; font-weight: 600; opacity: 0.7; }

.animate-float { animation: float 3s infinite ease-in-out; }

.fade-in { animation: fadeIn 1s cubic-bezier(0.165, 0.84, 0.44, 1); }
@keyframes fadeIn { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
</style>
