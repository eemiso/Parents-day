<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Heart, RefreshCw, ChevronLeft, Download, Star } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import html2canvas from 'html2canvas'

const router = useRouter()
const frames = [
  { name: 'Classic White', color: '#FFFFFF', text: '#2D3436' },
  { name: 'Sweet Pink', color: '#FFF0F3', text: '#FF6B81' },
  { name: 'Modern Black', color: '#1A1A1A', text: '#FFFFFF' },
  { name: 'Vintage Cream', color: '#FDFCF0', text: '#8E7F7F' }
]

const selectedFrame = ref(frames[0])
const photoCount = 58
const selectedPhotos = ref<number[]>([])
const uploadedPhotos = ref<(string | null)[]>([null, null, null, null])
const newPhotosPool = ref<string[]>([]) // 새로 추가된 사진들을 담는 바구니
const frameRef = ref<HTMLElement | null>(null)
const isDownloading = ref(false)

const shufflePhotos = () => {
  // 만약 새로 업로드한 사진 풀(Pool)이 있다면 거기서 뽑기
  if (newPhotosPool.value.length >= 1) {
    const pool = [...newPhotosPool.value]
    const shuffled = pool.sort(() => Math.random() - 0.5)
    
    // 4장을 채움 (사진이 4장보다 적으면 반복해서 채움)
    for (let i = 0; i < 4; i++) {
      uploadedPhotos.value[i] = shuffled[i % shuffled.length]
    }
  } else {
    // 풀이 비어있으면 기존 앨범에서 랜덤 추출
    const nums = Array.from({ length: photoCount }, (_, i) => i + 1)
    selectedPhotos.value = nums.sort(() => Math.random() - 0.5).slice(0, 4)
    uploadedPhotos.value = [null, null, null, null]
  }
}

const handleBulkUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    const files = Array.from(target.files)
    newPhotosPool.value = [] // 기존 풀 초기화
    
    files.forEach(file => {
      const reader = new FileReader()
      reader.onload = (e) => {
        newPhotosPool.value.push(e.target?.result as string)
        // 사진이 다 읽히면 자동으로 한 번 섞어줌
        if (newPhotosPool.value.length === files.length) {
          shufflePhotos()
        }
      }
      reader.readAsDataURL(file)
    })
  }
}

onMounted(() => {
  shufflePhotos()
})

const goBack = () => {
  router.push('/')
}

const downloadImage = async () => {
  if (!frameRef.value) return
  
  isDownloading.value = true
  try {
    const canvas = await html2canvas(frameRef.value, {
      useCORS: true,
      scale: 3, // 화질 대폭 상향 (3배)
      backgroundColor: selectedFrame.value.color,
      logging: false,
      onclone: (clonedDoc) => {
        // 클론된 문서에서 애니메이션이나 불필요한 효과 제거하여 선명도 확보
        const el = clonedDoc.querySelector('.four-cut-frame') as HTMLElement
        if (el) {
          el.style.animation = 'none'
          el.style.transform = 'none'
          el.style.boxShadow = 'none'
        }
      }
    })
    
    const link = document.createElement('a')
    link.download = `우리집인생네컷_${new Date().toISOString().slice(0, 10)}.png`
    link.href = canvas.toDataURL('image/png')
    link.click()
  } catch (err) {
    console.error('이미지 저장 실패:', err)
    alert('이미지 저장에 실패했습니다. 다시 시도해 주세요.')
  } finally {
    isDownloading.value = false
  }
}

const handleImageError = (e: Event, photoNum: number) => {
  const img = e.target as HTMLImageElement
  if (img.src.includes('.JPG')) return 
  img.src = `/assets/family/${photoNum}.JPG`
}
</script>

<template>
  <div class="four-cut-view">
    <div class="top-nav">
      <button @click="goBack" class="back-btn">
        <ChevronLeft :size="24" />
        메인으로
      </button>
      <h2 class="page-title">우리 가족 인생네컷 📸</h2>
    </div>

    <div class="content-layout">
      <!-- 왼쪽: 프레임 컨트롤 -->
      <div class="controls-panel">
        <div class="control-section">
          <h3>프레임 색상</h3>
          <div class="frame-options">
            <button 
              v-for="frame in frames" 
              :key="frame.name"
              class="frame-btn"
              :style="{ backgroundColor: frame.color }"
              :class="{ active: selectedFrame.name === frame.name }"
              @click="selectedFrame = frame"
            >
              <span class="sr-only">{{ frame.name }}</span>
            </button>
          </div>
        </div>

        <div class="control-section">
          <h3>사진 관리</h3>
          <div class="bulk-upload-wrapper">
            <input 
              id="bulk-upload"
              type="file" 
              multiple 
              accept="image/*" 
              class="hidden-input" 
              @change="handleBulkUpload"
            />
          
          </div>
          
          <button @click="shufflePhotos" class="action-btn shuffle">
            <RefreshCw :size="18" /> {{ newPhotosPool.length > 0 ? '내 사진들로 섞기' : '랜덤 사진으로 채우기' }}
          </button>
          
          <p v-if="newPhotosPool.length > 0" class="pool-status">
            현재 <strong>{{ newPhotosPool.length }}장</strong>의 내 사진이 등록되었습니다.
          </p>
          <p v-else class="control-tip">여러 장의 사진을 한꺼번에 올리고 랜덤하게 섞어보세요.</p>
        </div>

        <div class="control-section">
          <h3>결과 저장</h3>
          <button 
            @click="downloadImage" 
            class="action-btn save" 
            :disabled="isDownloading"
          >
            <Download :size="18" /> 
            {{ isDownloading ? '저장 중...' : '이미지로 저장하기' }}
          </button>
        </div>
      </div>

      <!-- 오른쪽: 인생네컷 실물 디자인 -->
      <div class="preview-panel">
        <div 
          ref="frameRef"
          class="four-cut-frame shadow-xl"
          :style="{ backgroundColor: selectedFrame.color, color: selectedFrame.text }"
        >
          <div class="frame-header">
            <span class="frame-date">2026. 05. 08</span>
            <div class="frame-logo">
              <Heart :size="16" fill="currentColor" />
              <span>Happy Family</span>
            </div>
          </div>

          <div class="photos-container">
            <div 
              v-for="(photoNum, index) in selectedPhotos" 
              :key="photoNum + '-' + index"
              class="photo-box"
            >
              <img 
                v-if="uploadedPhotos[index]"
                :src="uploadedPhotos[index]!" 
                class="photo-img uploaded"
              />
              <img 
                v-else
                :src="`/assets/family/${photoNum}.jpg`" 
                class="photo-img"
                @error="handleImageError($event, photoNum)"
              />

              <!-- 장식 스티커들 -->
              <div v-if="index === 0" class="sticker s1">💖</div>
              <div v-if="index === 1" class="sticker s2">LOVE</div>
              <div v-if="index === 3" class="sticker s3">꽃길만 걸어요</div>
            </div>
          </div>

          <div class="frame-footer">
            <p class="footer-msg">언제나 사랑합니다, 엄마 아빠!</p>
            <div class="footer-bottom">
              <span class="author">Miso, Minji, Minjun</span>
              <div class="qr-placeholder">
                <div class="qr-box"></div>
                <span>Memory QR</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.four-cut-view {
  width: 100%;
  height: 100%;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.top-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  border: none;
  padding: 0.8rem 1.2rem;
  border-radius: 15px;
  font-weight: 700;
  color: #636E72;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: 0.3s;
}
.back-btn:hover { transform: translateX(-5px); color: #FF6B81; }

.page-title {
  font-size: 1.8rem;
  font-weight: 900;
  color: #2D3436;
}

.content-layout {
  flex: 1;
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 3rem;
  min-height: 0;
}

.controls-panel {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.control-section {
  background: rgba(255, 255, 255, 0.6);
  padding: 1.5rem;
  border-radius: 24px;
  border: 1px solid rgba(255, 107, 129, 0.1);
}

.control-section h3 {
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 1.2rem;
  color: #2D3436;
}

.frame-options {
  display: flex;
  gap: 1rem;
}

.frame-btn {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  border: 3px solid transparent;
  cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.frame-btn.active {
  border-color: #FF6B81;
  transform: scale(1.1);
}

.action-btn {
  width: 100%;
  padding: 1rem;
  border-radius: 15px;
  border: none;
  background: white;
  color: #2D3436;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  transition: 0.3s;
}
.action-btn:hover {
  background: #FF6B81;
  color: white;
  transform: translateY(-3px);
}

.action-btn.save {
  background: #2D3436;
  color: white;
}
.action-btn.save:hover {
  background: #000;
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.deco-info {
  background: #FFF0F3;
  color: #FF6B81;
}
.tip {
  font-size: 0.95rem;
  line-height: 1.6;
  font-weight: 600;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

/* 프리미엄 인생네컷 프레임 디자인 */
.preview-panel {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  overflow-y: auto;
  padding-bottom: 2rem;
}

.four-cut-frame {
  width: 320px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  animation: slideInDown 1s ease-out;
}

@keyframes slideInDown {
  from { transform: translateY(-100px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.frame-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 5px;
  font-size: 0.8rem;
  font-weight: 800;
  opacity: 0.8;
}

.frame-logo {
  display: flex;
  align-items: center;
  gap: 4px;
}

.photos-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.photo-box {
  width: 100%;
  aspect-ratio: 4 / 3;
  background: #EEE;
  overflow: hidden;
  position: relative;
}

.photo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}
.photo-box:hover .photo-img { transform: scale(1.05); }

.photo-img.uploaded {
  object-fit: cover;
}

.hidden-input {
  display: none;
}

.control-tip {
  font-size: 0.8rem;
  color: #636E72;
  margin-top: 10px;
  line-height: 1.4;
}

.bulk-upload-wrapper {
  margin-bottom: 0.8rem;
}

.action-btn.upload-pool {
  background: #FFF0F3;
  color: #FF6B81;
  border: 1px dashed #FF6B81;
}

.pool-status {
  margin-top: 10px;
  font-size: 0.85rem;
  color: #FF6B81;
  background: white;
  padding: 8px;
  border-radius: 10px;
  text-align: center;
}

/* 스티커 스타일 */
.sticker {
  position: absolute;
  z-index: 10;
  font-weight: 900;
  pointer-events: none;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}
.s1 { top: 10px; right: 10px; font-size: 1.5rem; }
.s2 { bottom: 10px; left: 10px; background: rgba(255,107,129,0.9); color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.7rem; }
.s3 { top: 10px; left: 10px; font-family: 'Nanum Myeongjo', serif; font-size: 0.8rem; background: white; color: #1A1A1A; padding: 2px 6px; border-radius: 3px; }

.frame-footer {
  margin-top: 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 10px 5px;
}

.footer-msg {
  font-family: 'Nanum Myeongjo', serif;
  font-size: 1.1rem;
  font-weight: 900;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.author {
  font-size: 0.7rem;
  font-weight: 700;
  opacity: 0.6;
}

.qr-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.qr-box {
  width: 35px;
  height: 35px;
  background: currentColor;
  opacity: 0.8;
  border-radius: 4px;
}

.qr-placeholder span {
  font-size: 0.6rem;
  font-weight: 800;
}

.sr-only { display: none; }

@media (max-width: 900px) {
  .content-layout { grid-template-columns: 1fr; }
  .preview-panel { order: -1; }
}
</style>
