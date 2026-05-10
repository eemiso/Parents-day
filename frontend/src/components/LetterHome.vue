<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const children = [
  { name: 'miso', label: '미소', role: '첫째 딸' },
  { name: 'minji', label: '민지', role: '둘째 딸' },
  { name: 'minjun', label: '민준', role: '막내 아들' }
]

const goToLetter = (childName: string) => {
  router.push(`/letters/${childName}`)
}
</script>

<template>
  <div class="letter-home-component fade-in">
    <div class="header-section">
      <div class="gift-icon">💌</div>
      <h1 class="main-title">미소·민지·민준이의 편지 보관함</h1>
      <p class="sub-title">누구의 편지를 먼저 읽어볼까요?</p>
    </div>
    
    <div class="child-grid">
      <div 
        v-for="child in children" 
        :key="child.name" 
        class="child-card"
        @click="goToLetter(child.name)"
      >
        <div class="avatar-wrapper">
          <img :src="`/images/${child.name}.png`" :alt="child.label" class="child-image" />
        </div>
        <div class="info-group">
          <div class="child-name">{{ child.label }}</div>
          <div class="child-role">{{ child.role }}</div>
        </div>
        <div class="hover-hint">편지 읽어보기 →</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.letter-home-component {
  width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center;
  padding: 50px 40px;
}

.header-section { text-align: center; margin-bottom: 40px; }
.gift-icon { font-size: 4rem; margin-bottom: 10px; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1)); }
.main-title { font-size: 2.5rem; font-weight: 950; color: #2D3436; margin-bottom: 10px; letter-spacing: -1px; }
.sub-title { font-size: 1.2rem; color: #636E72; font-weight: 600; opacity: 0.8; }

.child-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  width: 100%;
  max-width: 1000px;
  flex: 1;
  align-items: center;
}

.child-card {
  background: white; border-radius: 40px; padding: 40px 20px;
  display: flex; flex-direction: column; align-items: center; gap: 20px;
  cursor: pointer; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid #f8f9fa;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03);
  position: relative;
}

.child-card:hover {
  transform: translateY(-15px);
  box-shadow: 0 30px 60px rgba(255, 107, 129, 0.15);
  border-color: #FF6B81;
}

.avatar-wrapper {
  width: 160px; height: 160px; border-radius: 50%;
  background: #FFF5F6; padding: 12px;
  display: flex; align-items: center; justify-content: center;
  transition: 0.4s;
}
.child-card:hover .avatar-wrapper { background: #FFD1DC; scale: 1.05; }

.child-image {
  width: 100%; height: 100%; object-fit: contain; border-radius: 50%;
  filter: drop-shadow(0 5px 15px rgba(0,0,0,0.1));
}

.info-group { text-align: center; }
.child-name { font-size: 1.8rem; font-weight: 900; color: #2D3436; margin-bottom: 5px; }
.child-role { font-size: 1.1rem; color: #FF6B81; font-weight: 700; opacity: 0.8; }

.hover-hint {
  font-size: 0.9rem; font-weight: 700; color: #FF6B81;
  opacity: 0; transform: translateY(10px); transition: 0.3s;
}
.child-card:hover .hover-hint { opacity: 1; transform: translateY(0); }

.fade-in { animation: fadeIn 0.8s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

@media (max-height: 850px) {
  .avatar-wrapper { width: 130px; height: 130px; }
  .main-title { font-size: 2rem; }
  .child-card { padding: 30px 20px; }
}
</style>
