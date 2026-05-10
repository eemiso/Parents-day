import { reactive } from 'vue'

export const rouletteStore = reactive({
  momGift: localStorage.getItem('momGift') || '',
  dadGift: localStorage.getItem('dadGift') || '',
  result: localStorage.getItem('roulette_result') || '',
  hasSpun: !!localStorage.getItem('roulette_result'),
  attempts: Number(localStorage.getItem('roulette_attempts') || 0),
  
  setGifts(mom: string, dad: string) {
    this.momGift = mom
    this.dadGift = dad
    localStorage.setItem('momGift', mom)
    localStorage.setItem('dadGift', dad)
  },
  
  setResult(res: string) {
    this.result = res
    this.hasSpun = true
    localStorage.setItem('roulette_result', res)
  },
  
  reset() {
    this.result = ''
    this.hasSpun = false
    this.attempts = 0
    localStorage.removeItem('roulette_result')
    localStorage.removeItem('roulette_attempts')
  },
  
  incrementAttempts() {
    this.attempts++
    localStorage.setItem('roulette_attempts', this.attempts.toString())
  }
})
