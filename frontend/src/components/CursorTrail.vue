<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

const dots = ref<{x: number, y: number, id: number, emoji: string}[]>([])
let counter = 0
const emojis = ['💐']
let lastPos = { x: 0, y: 0 }

const handleMouseMove = (e: MouseEvent) => {
  // 마우스가 일정 거리 이상 움직였을 때만 생성 (정신없음 방지)
  const dist = Math.hypot(e.clientX - lastPos.x, e.clientY - lastPos.y)
  if (dist < 40) return 

  lastPos = { x: e.clientX, y: e.clientY }
  
  const id = counter++
  const emoji = emojis[Math.floor(Math.random() * emojis.length)]
  dots.value.push({ x: e.clientX, y: e.clientY, id, emoji })
  
  // 1초 뒤 제거
  setTimeout(() => {
    dots.value = dots.value.filter(d => d.id !== id)
  }, 1000)
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
})
</script>

<template>
  <div class="trail-container">
    <div 
      v-for="dot in dots" 
      :key="dot.id" 
      class="trail-dot fade-out"
      :style="{ left: dot.x + 'px', top: dot.y + 'px' }"
    >
      {{ dot.emoji }}
    </div>
  </div>
</template>

<style scoped>
.trail-container {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 10000;
}

.trail-dot {
  position: absolute;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  pointer-events: none;
}

@keyframes fadeOut {
  from { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  to { opacity: 0; transform: translate(-50%, -50%) scale(2) translateY(-20px); }
}

.fade-out {
  animation: fadeOut 1s ease-out forwards;
}
</style>
