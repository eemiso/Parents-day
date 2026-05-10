<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { 
  Heart, Play, SkipForward, Maximize2, RefreshCw, 
  ChevronLeft, ChevronRight, X, Calendar, MessageSquare 
} from 'lucide-vue-next'

const totalPhotos = 58
const album = ref(Array.from({ length: totalPhotos }, (_, i) => {
  const num = i + 1
  return {
    url: `/assets/family/${num}.jpg`,
    date: `2024. 05. 0${(i % 9) + 1}`,
    caption: [
      "기억나시나요? 우리 가족의 행복했던 순간 💖",
      "함께라서 더욱 소중했던 그날의 공기 ✨",
      "부모님의 미소는 우리에게 가장 큰 선물입니다 🥰",
      "오래도록 간직하고 싶은 우리만의 이야기 📖",
      "사랑한다는 말보다 더 깊은 진심을 담아 💌"
    ][i % 5],
    num: num
  }
}))

const currentIndex = ref(0)
const isFinished = ref(false)
const playbackSpeed = ref(1)
const isAutoPlay = ref(true)
let timer: any = null

const selectedPhotoIndex = ref<number | null>(null)

const next = () => {
  if (currentIndex.value < totalPhotos - 1) {
    currentIndex.value++
  } else {
    finishSlideshow()
  }
}

const prev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const skip = () => {
  finishSlideshow()
}

// 📍 이미지 에러 핸들링
const handleImageError = (e: Event, photoNum: number) => {
  const img = e.target as HTMLImageElement
  if (img.src.includes('.JPG')) return 
  if (img.src.includes('.jpg')) {
    img.src = `/assets/family/${photoNum}.JPG`
  }
}

const finishSlideshow = () => {
  stopTimer()
  isFinished.value = true
}

const startTimer = () => {
  stopTimer()
  if (!isAutoPlay.value) return
  const interval = 3000 / playbackSpeed.value 
  timer = setInterval(next, interval)
}

const stopTimer = () => {
  if (timer) clearInterval(timer)
}

const replay = () => {
  currentIndex.value = 0
  isFinished.value = false
  isAutoPlay.value = true
  startTimer()
}

const openModal = (index: number) => {
  selectedPhotoIndex.value = index
  document.body.style.overflow = 'hidden' // Lock background scroll
}

const closeModal = () => {
  selectedPhotoIndex.value = null
  document.body.style.overflow = '' // Restore scroll
}

const modalNext = () => {
  if (selectedPhotoIndex.value !== null && selectedPhotoIndex.value < totalPhotos - 1) {
    selectedPhotoIndex.value++
  }
}

const modalPrev = () => {
  if (selectedPhotoIndex.value !== null && selectedPhotoIndex.value > 0) {
    selectedPhotoIndex.value--
  }
}

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  stopTimer()
  document.body.style.overflow = ''
})
</script>

<template>
  <div class="photo-experience-container" :class="{ 'is-gallery': isFinished }">
    
    <!-- Cinema View (Slideshow) -->
    <div v-if="!isFinished" class="cinema-stage fade-in">
      <div class="cinema-header">
        <div class="header-left">
          <span class="badge">CINEMATIC</span>
          <h3 class="cinema-title">우리의 기록, 소중한 순간들</h3>
        </div>
        <div class="cinema-controls">
          <button @click="playbackSpeed = (playbackSpeed === 1 ? 2 : 1)" class="btn-icon-text">
            {{ playbackSpeed }}x 속도
          </button>
          <button @click="skip" class="btn-icon-text outline">
            전체 보기 <SkipForward :size="14" />
          </button>
        </div>
      </div>

      <div class="viewport-wrapper">
        <div class="photo-viewport-16-9">
          <transition name="fade">
            <img :key="currentIndex + 'bg'" :src="album[currentIndex].url" class="photo-bg-blur" @error="handleImageError($event, album[currentIndex].num)" />
          </transition>

          <transition name="cinema-fade" mode="out-in">
            <div class="slide-container" :key="currentIndex">
              <img 
                :src="album[currentIndex].url" 
                class="cinema-photo ken-burns"
                @error="handleImageError($event, album[currentIndex].num)"
              />
              <div class="caption-overlay">
                <p class="photo-caption">{{ album[currentIndex].caption }}</p>
              </div>
            </div>
          </transition>

          <button @click="prev" class="nav-btn prev" :disabled="currentIndex === 0"><ChevronLeft /></button>
          <button @click="next" class="nav-btn next"><ChevronRight /></button>
        </div>
      </div>

      <div class="cinema-footer">
        <div class="progress-info">
          <span class="current">{{ currentIndex + 1 }}</span>
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: `${((currentIndex + 1) / totalPhotos) * 100}%` }"></div>
          </div>
          <span class="total">{{ totalPhotos }}</span>
        </div>
      </div>
    </div>

    <!-- Art Gallery View -->
    <div v-else class="gallery-stage fade-in">
      <div class="gallery-header-premium">
        <div class="title-group">
          <h2>우리의 모든 순간들 <span class="heart-pulse">💖</span></h2>
          <p>어버이날을 맞아 꺼내보는 소중한 보물 상자 (총 {{ totalPhotos }}장)</p>
        </div>
        <button @click="replay" class="btn-replay">
          <RefreshCw :size="18" /> 슬라이드 쇼 다시보기
        </button>
      </div>
      
      <div class="photo-grid">
        <div 
          v-for="(photo, idx) in album" 
          :key="photo.num" 
          class="gallery-card"
          @click="openModal(idx)"
        >
          <div class="card-inner">
            <img 
              :src="photo.url" 
              class="card-img" 
              @error="handleImageError($event, photo.num)" 
              loading="lazy"
            />
            <div class="card-overlay">
              <div class="zoom-circle">
                <Maximize2 :size="24" color="white" />
              </div>
            </div>
          </div>
          <div class="card-footer">
            <span class="card-date">{{ photo.date }}</span>
            <span class="card-num">No. {{ photo.num }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Lightbox Modal -->
    <transition name="modal-fade">
      <div v-if="selectedPhotoIndex !== null" class="modal-overlay" @click.self="closeModal">
        <button class="modal-close" @click="closeModal">
          <X :size="32" />
        </button>

        <div class="modal-container">
          <button class="modal-nav-btn prev" @click="modalPrev" :disabled="selectedPhotoIndex === 0">
            <ChevronLeft :size="40" />
          </button>

          <div class="modal-content-wrapper">
            <div class="modal-image-box">
              <transition name="photo-swap" mode="out-in">
                <img 
                  :key="selectedPhotoIndex"
                  :src="album[selectedPhotoIndex].url" 
                  class="modal-img" 
                  @error="handleImageError($event, album[selectedPhotoIndex].num)"
                />
              </transition>
            </div>
            
            <div class="modal-info">
              <div class="info-top">
                <div class="info-date">
                  <Calendar :size="16" />
                  <span>{{ album[selectedPhotoIndex].date }}</span>
                </div>
                <div class="info-tag">Memory #{{ album[selectedPhotoIndex].num }}</div>
              </div>
              <p class="info-caption">
                <MessageSquare :size="18" class="quote-icon" />
                {{ album[selectedPhotoIndex].caption }}
              </p>
              <div class="info-footer">
                <Heart class="info-heart" :size="20" fill="#FF6B81" color="#FF6B81" />
                <span>우리는 부모님을 항상 사랑합니다</span>
              </div>
            </div>
          </div>

          <button class="modal-nav-btn next" @click="modalNext" :disabled="selectedPhotoIndex === totalPhotos - 1">
            <ChevronRight :size="40" />
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.photo-experience-container { 
  width: 100%; 
  height: 100%; /* Fill the main-content area */
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  overflow-y: auto; /* Enable internal scrolling */
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
}

.photo-experience-container.is-gallery {
  overflow-y: auto;
  padding-bottom: 5rem;
}

/* Cinema Stage (Slideshow) */
.cinema-stage { 
  width: 100%; 
  max-width: 1200px; 
  height: 100%; 
  display: flex; 
  flex-direction: column; 
  justify-content: center; 
  padding: 2rem;
}

.cinema-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2vh; flex-shrink: 0; }
.badge { font-weight: 800; font-size: 1.5vh; color: #FF6B81; background: #FFF0F2; padding: 0.3vh 0.8rem; border-radius: 50px; letter-spacing: 1px; }
.cinema-title { font-size: 3vh; font-weight: 900; margin-top: 0.5vh; color: #2D3436; }

.viewport-wrapper {
  position: relative;
  background: #000;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 40px 80px rgba(0,0,0,0.25);
  border: 8px solid white;
  flex: 1;
  max-height: 60vh;
}

.photo-viewport-16-9 {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.photo-bg-blur {
  position: absolute;
  inset: -20px;
  width: calc(100% + 40px);
  height: calc(100% + 40px);
  object-fit: cover;
  filter: blur(40px) brightness(0.5);
  z-index: 1;
}

.slide-container {
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cinema-photo {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.ken-burns { animation: kenBurnsAnimation 10s infinite alternate ease-in-out; }
@keyframes kenBurnsAnimation { from { transform: scale(1.0); } to { transform: scale(1.1); } }

.caption-overlay {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 5vh 2rem 3vh;
  background: linear-gradient(transparent, rgba(0,0,0,0.9));
  text-align: center;
  z-index: 10;
}
.photo-caption { 
  color: white; 
  font-size: 2.8vh; 
  font-weight: 700; 
  font-family: 'Nanum Myeongjo', serif; 
  text-shadow: 0 2px 10px rgba(0,0,0,0.8); 
  letter-spacing: -0.5px;
}

.btn-icon-text { padding: 0.6rem 1.2rem; border-radius: 12px; border: 2px solid #1A1A1A; background: white; color: #1A1A1A; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: 0.2s; }
.btn-icon-text.outline { border-color: #EEE; color: #999; }

.nav-btn { position: absolute; top: 50%; transform: translateY(-50%); width: 60px; height: 60px; background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3); border-radius: 50%; color: white; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 20; transition: all 0.3s; }
.nav-btn:hover:not(:disabled) { background: rgba(255,255,255,0.3); transform: translateY(-50%) scale(1.1); }
.nav-btn:disabled { opacity: 0.2; cursor: not-allowed; }
.nav-btn.prev { left: 30px; }
.nav-btn.next { right: 30px; }

.progress-info { display: flex; align-items: center; gap: 1.5rem; color: #636E72; font-weight: 800; margin-top: 3vh; flex-shrink: 0; width: 100%; max-width: 1200px; }
.progress-track { flex: 1; height: 6px; background: #EEE; border-radius: 10px; overflow: hidden; }
.progress-fill { height: 100%; background: #FF6B81; transition: width 0.5s; box-shadow: 0 0 10px rgba(255,107,129,0.3); }

/* Gallery Stage */
.gallery-stage { 
  width: 100%; 
  max-width: 1400px; 
  min-height: 100%; /* Ensure background covers full height */
  padding: 4rem 3rem 10rem 3rem; /* Extra padding at bottom for scrolling */
  display: flex; 
  flex-direction: column; 
  background-color: #fdfcfb; /* Warm paper color */
  border-radius: 40px;
  margin-top: 2rem;
  box-shadow: inset 0 0 40px rgba(0,0,0,0.02);
}

.gallery-header-premium { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 4rem; 
  border-bottom: 2px solid #f0e6e6;
  padding-bottom: 2rem;
}

.title-group h2 { font-size: 2.8rem; font-weight: 900; color: #2D3436; margin-bottom: 0.5rem; font-family: 'Nanum Myeongjo', serif; }
.title-group p { color: #8e7f7f; font-size: 1.2rem; }

.heart-pulse { display: inline-block; animation: heartBeat 1.5s infinite; color: #FF6B81; }

@keyframes heartBeat {
  0% { transform: scale(1); }
  14% { transform: scale(1.3); }
  28% { transform: scale(1); }
  42% { transform: scale(1.3); }
  70% { transform: scale(1); }
}

.btn-replay { 
  padding: 0.8rem 1.8rem; 
  background: white; 
  border: 1px solid #eee; 
  border-radius: 50px; 
  font-weight: 700; 
  color: #636E72; 
  display: flex; 
  align-items: center; 
  gap: 0.8rem; 
  cursor: pointer; 
  transition: all 0.3s;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.btn-replay:hover { background: #fff; border-color: #FF6B81; color: #FF6B81; transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255,107,129,0.15); }

.photo-grid { 
  display: grid; 
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); 
  gap: 3.5rem; 
  padding: 1rem;
}

.gallery-card { 
  cursor: pointer; 
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  background: white;
  padding: 15px 15px 60px 15px; 
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  border: 1px solid #f0e6e6;
  position: relative;
  transform: rotate(var(--rotation, 0deg));
}

/* Give each card a slightly different rotation for an 'organic' feel */
.gallery-card:nth-child(even) { --rotation: -1deg; }
.gallery-card:nth-child(3n) { --rotation: 1.5deg; }
.gallery-card:nth-child(5n) { --rotation: -0.5deg; }

.gallery-card:hover { 
  transform: translateY(-20px) rotate(0deg) scale(1.02); 
  box-shadow: 0 40px 80px rgba(0,0,0,0.15);
  z-index: 10;
}

.card-inner { 
  position: relative; 
  width: 100%; 
  aspect-ratio: 1 / 1;
  overflow: hidden; 
  background: #f9f9f9;
  border: 1px solid #eee;
}

.card-img { 
  width: 100%; 
  height: 100%; 
  object-fit: cover; 
  transition: transform 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.gallery-card:hover .card-img { transform: scale(1.08); }

.card-overlay { 
  position: absolute; 
  inset: 0; 
  background: rgba(255,107,129,0.1); 
  opacity: 0; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  transition: 0.3s;
}

.gallery-card:hover .card-overlay { opacity: 1; }

.zoom-circle {
  width: 60px; height: 60px;
  background: rgba(255,255,255,0.9);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  transform: scale(0.5);
  transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.gallery-card:hover .zoom-circle { transform: scale(1); color: #FF6B81; }

.card-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1.2rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-date { font-size: 1rem; color: #9a8c8c; font-weight: 700; font-family: 'Nanum Myeongjo', serif; }
.card-num { font-size: 0.8rem; color: #FF6B81; font-weight: 800; opacity: 0.6; }

/* Modal Design */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 15, 15, 0.85);
  backdrop-filter: blur(20px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.modal-close {
  position: absolute;
  top: 2rem;
  right: 2rem;
  background: white;
  border: none;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10001;
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
  transition: 0.3s;
}
.modal-close:hover { transform: rotate(90deg) scale(1.1); color: #FF6B81; }

.modal-container {
  display: flex;
  align-items: center;
  gap: 3rem;
  width: 100%;
  max-width: 1400px;
}

.modal-nav-btn {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  color: white;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  flex-shrink: 0;
}
.modal-nav-btn:hover:not(:disabled) { background: white; color: #1A1A1A; }
.modal-nav-btn:disabled { opacity: 0.1; cursor: not-allowed; }

.modal-content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.modal-image-box {
  width: 100%;
  max-height: 70vh;
  display: flex;
  justify-content: center;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 50px 100px rgba(0,0,0,0.5);
  background: #000;
  border: 4px solid rgba(255,255,255,0.1);
}

.modal-img {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
}

.modal-info {
  background: white;
  padding: 2.5rem;
  border-radius: 30px;
  width: 100%;
  max-width: 800px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.3);
  text-align: center;
}

.info-top {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.info-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #636E72;
  font-weight: 700;
}

.info-tag {
  background: #f1f2f6;
  padding: 4px 12px;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 800;
  color: #2f3542;
}

.info-caption {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2D3436;
  line-height: 1.5;
  margin-bottom: 2rem;
  font-family: 'Nanum Myeongjo', serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.quote-icon { color: #FF6B81; opacity: 0.4; }

.info-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f0f0f0;
  color: #B2BEC3;
  font-weight: 600;
}

.info-heart { animation: heartBeat 2s infinite; }

/* Transitions */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.4s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.photo-swap-enter-active, .photo-swap-leave-active { transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
.photo-swap-enter-from { opacity: 0; transform: translateX(30px) scale(0.95); }
.photo-swap-leave-to { opacity: 0; transform: translateX(-30px) scale(0.95); }

/* Mobile Responsive */
@media (max-width: 1024px) {
  .modal-container { gap: 1rem; }
  .modal-nav-btn { width: 50px; height: 50px; }
  .photo-grid { grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
}

@media (max-width: 768px) {
  .gallery-header-premium { flex-direction: column; align-items: flex-start; gap: 1.5rem; }
  .modal-container { position: relative; }
  .modal-nav-btn { position: absolute; top: 35%; transform: translateY(-50%); z-index: 10; background: rgba(0,0,0,0.5); }
  .modal-nav-btn.prev { left: -1rem; }
  .modal-nav-btn.next { right: -1rem; }
  .info-caption { font-size: 1.2rem; }
  .gallery-stage { padding: 1rem; }
}
</style>
