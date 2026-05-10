<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const childNameMap: Record<string, string> = {
  'miso': '미소',
  'minji': '민지',
  'minjun': '민준'
}

const letterContent = ref('편지를 불러오는 중입니다... 🌸')
const childLabel = computed(() => childNameMap[route.params.child as string] || '자녀')

const fetchLetter = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/letter/generate', {
      user_name: childLabel.value
    })
    letterContent.value = response.data.letter
  } catch (error) {
    console.error('편지 로딩 실패:', error)
    letterContent.value = '편지를 불러오는 데 실패했습니다. 다시 시도해 주세요.'
  }
}

onMounted(() => {
  fetchLetter()
})

const goBack = () => {
  router.push('/letters')
}
</script>

<template>
  <div class="letter-detail-component fade-in">
    <div class="paper-wrapper">
      <div class="letter-paper-realistic shadow-deep">
        
        <div class="paper-decoration top">
          <div class="carnation-seal">🌸</div>
          <div class="letter-meta-info">
            <span class="date-text">2026. 05. 08</span>
            <div class="top-line"></div>
          </div>
        </div>

        <div class="paper-content-area">
          <pre class="letter-text-stationery">{{ letterContent }}</pre>
        </div>

        <div class="paper-decoration bottom">
          <div class="floral-accent">🌺</div>
          <div class="signature-stationery">
            <span class="sig-from">사랑하는 아들/딸</span>
            <span class="sig-name">{{ childLabel }} 올림</span>
          </div>
        </div>

      </div>
    </div>

    <div class="action-footer">
      <button @click="goBack" class="btn-return">편지 보관함으로</button>
    </div>
  </div>
</template>

<style scoped>
.letter-detail-component {
  width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 40px;
}

.paper-wrapper {
  flex: 1; width: 100%; display: flex; align-items: center; justify-content: center;
  min-height: 0;
}

.letter-paper-realistic {
  background: #FFF;
  width: 100%; max-width: 1000px;
  height: 70vh;
  padding: 3rem 4rem;
  border-radius: 8px;
  position: relative;
  box-shadow: 0 30px 60px rgba(0,0,0,0.05);
  display: flex; flex-direction: column;
  background-image: url('https://www.transparenttextures.com/patterns/natural-paper.png');
}

.paper-decoration.top { 
  margin-bottom: 1.5rem; border-bottom: 2px solid #FDEFF0; padding-bottom: 1rem; 
  display: flex; justify-content: space-between; align-items: center; flex-shrink: 0;
}
.carnation-seal { font-size: 2.2rem; filter: drop-shadow(0 4px 8px rgba(255,107,129,0.2)); }
.date-text { font-family: 'Nanum Myeongjo', serif; font-weight: 700; color: #FF6B81; font-size: 1.1rem; }

.paper-content-area { 
  flex: 1; width: 100%; overflow-y: hidden;
  background-image: linear-gradient(transparent 37px, #FDEFF0 37px, #FDEFF0 38px);
  background-size: 100% 38px;
  background-position-y: 30px;
  background-attachment: local;
}

.letter-text-stationery { 
  white-space: pre-wrap; font-family: 'Nanum Myeongjo', serif; 
  font-size: 20px; color: #333; 
  line-height: 38px; 
  text-align: left; 
  margin: 0; padding: 0;
}

.paper-decoration.bottom { 
  display: flex; justify-content: space-between; align-items: flex-end; 
  margin-top: 1.5rem; padding-bottom: 0.5rem; flex-shrink: 0; 
}
.floral-accent { font-size: 3rem; opacity: 0.4; }
.signature-stationery { display: flex; flex-direction: column; align-items: flex-end; gap: 0.3rem; }
.sig-from { font-size: 1.1rem; color: #FF6B81; font-weight: 700; font-family: 'Nanum Myeongjo', serif; }
.sig-name { font-size: 1.6rem; font-weight: 900; font-family: 'Nanum Myeongjo', serif; color: #2D3436; }

.action-footer { margin-top: 25px; flex-shrink: 0; }
.btn-return { 
  padding: 0.8rem 3rem; border-radius: 50px; border: none; 
  background: #2D3436; color: white; font-weight: 800; cursor: pointer; 
  transition: 0.3s; font-size: 1rem;
}
.btn-return:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }

.fade-in { animation: fadeIn 0.8s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
