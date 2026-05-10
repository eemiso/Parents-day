<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Heart } from 'lucide-vue-next'

const router = useRouter()

const coupons = [
  { title: '어깨 안마 쿠폰', desc: '시원하게 안마해 드립니다.', time: '15분' },
  { title: '무한 심부름 쿠폰', desc: '무엇이든 시켜만 주세요!', time: '주1회' },
  { title: '설거지 해결 쿠폰', desc: '산더미 같은 설거지 대신 해드립니다.', time: '주1회' },
  { title: '커피/간식 쿠폰', desc: '원하시는 가장 맛있는 간식을 사드립니다.', time: '한달에 1번' },
  { title: '자유이용권', desc: '원하실 때 언제든 소원을 들어드립니다.', time: '무제한' },
  { title: '같이 시간 보내기', desc: '원하실 때 언제든 들어드립니다.', time: '무제한' }
]

const goBack = () => {
  router.push('/coupons')
}
</script>

<template>
  <div class="coupon-list-container">
    <!-- Top Nav -->
    <nav class="list-nav">
      <button @click="goBack" class="btn-back-prev">
        <span>← 이전으로 (쿠폰 안내)</span>
      </button>
    </nav>

    <div class="list-header fade-in">
      <Heart class="header-heart" />
      <h3>사용하고 싶으실 때 '쿠폰!'을 외쳐주세요</h3>
    </div>

    <div class="coupon-grid-wide fade-in">
      <div v-for="(coupon, idx) in coupons" :key="idx" class="coupon-ticket shadow-premium">
        <div class="ticket-body">
          <div class="ticket-tag">FAMILY COUPON</div>
          <div class="ticket-title">{{ coupon.title }}</div>
          <div class="ticket-desc">{{ coupon.desc }}</div>
          <div class="ticket-footer">VALID: {{ coupon.time }}</div>
        </div>
        <div class="ticket-stub">
          <div class="stub-line"></div>
          <div class="stub-text">USE</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.coupon-list-container {
  height: 100%; width: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
  padding: 2vh 4vw;
  background-color: #FAF9F6;
  overflow: hidden;
}

.list-nav { width: 100%; max-width: 1300px; display: flex; margin-bottom: 2vh; }
.btn-back-prev {
  background: white; border: 1px solid #eee; padding: 0.8vh 1.5rem;
  border-radius: 50px; font-weight: 700; cursor: pointer; transition: 0.2s;
  color: #666; font-size: 1.6vh;
}
.btn-back-prev:hover { border-color: #FF6B81; color: #FF6B81; }

.list-header { text-align: center; margin-bottom: 4vh; }
.header-heart { color: #FF6B81; width: 4vh; height: 4vh; margin-bottom: 1vh; }
.list-header h3 { font-size: 2.5vh; color: #333; font-weight: 800; }

.coupon-grid-wide {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 3vh;
  width: 100%;
  max-width: 1400px;
  flex: 1;
  align-items: flex-start;
  overflow-y: auto;
  padding: 1vh;
}

.coupon-ticket {
  display: flex;
  background: white;
  height: 16vh;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.coupon-ticket:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(255,107,129,0.15); }

.ticket-body { flex: 3; padding: 2vh 1.5rem; position: relative; text-align: left; }
.ticket-tag { font-size: 1.2vh; color: #FF6B81; font-weight: 800; margin-bottom: 0.5vh; letter-spacing: 1px; }
.ticket-title { font-size: 2.4vh; font-weight: 900; color: #1A1A1A; margin-bottom: 0.5vh; }
.ticket-desc { font-size: 1.6vh; color: #666; line-height: 1.4; }
.ticket-footer { position: absolute; bottom: 1.5vh; right: 1.5rem; font-size: 1.2vh; color: #999; font-weight: 700; }

.ticket-stub {
  flex: 0.8;
  background: linear-gradient(135deg, #FF6B81, #FF8E9E);
  display: flex; align-items: center; justify-content: center;
  position: relative; color: white;
}
.stub-line {
  position: absolute; left: 0; top: 0; bottom: 0; width: 1px;
  border-left: 2px dashed rgba(255,255,255,0.4);
}
.stub-text { font-weight: 900; font-size: 2vh; letter-spacing: 4px; transform: rotate(-90deg); }

.fade-in { animation: fadeIn 0.8s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
