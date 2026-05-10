<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

const canvasRef = ref<HTMLCanvasElement | null>(null)
let ctx: CanvasRenderingContext2D | null = null
let animationId: number

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  alpha: number
  color: string
}

let particles: Particle[] = []
const colors = ['#D14D72', '#FF8E9E', '#FCC8D1', '#FFD700', '#FF7F50', '#00CED1']

const createFirework = (x: number, y: number) => {
  const color = colors[Math.floor(Math.random() * colors.length)]
  for (let i = 0; i < 60; i++) {
    particles.push({
      x,
      y,
      vx: (Math.random() - 0.5) * 12,
      vy: (Math.random() - 0.5) * 12,
      alpha: 1,
      color
    })
  }
}

const update = () => {
  if (!ctx || !canvasRef.value) return
  ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)

  particles = particles.filter(p => p.alpha > 0)
  particles.forEach(p => {
    p.x += p.vx
    p.y += p.vy
    p.vy += 0.12 // gravity
    p.alpha -= 0.008

    ctx!.globalAlpha = p.alpha
    ctx!.fillStyle = p.color
    ctx!.beginPath()
    ctx!.arc(p.x, p.y, 2.5, 0, Math.PI * 2)
    ctx!.fill()
  })

  // 빈도수 증가
  if (Math.random() < 0.08) {
    createFirework(
      Math.random() * canvasRef.value.width,
      Math.random() * canvasRef.value.height * 0.7
    )
  }

  animationId = requestAnimationFrame(update)
}

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  const resize = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  
  window.addEventListener('resize', resize)
  resize()
  
  ctx = canvas.getContext('2d')
  
  // 시작하자마자 몇 개 터뜨리기
  for(let i=0; i<3; i++) {
    createFirework(Math.random() * window.innerWidth, Math.random() * window.innerHeight * 0.5)
  }
  
  update()
})

onUnmounted(() => {
  cancelAnimationFrame(animationId)
})
</script>

<template>
  <canvas ref="canvasRef" class="fireworks-canvas"></canvas>
</template>

<style scoped>
.fireworks-canvas {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999; /* 더 높게 설정 */
}
</style>
