import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RouletteHome from '../components/RouletteHome.vue'
import RoulettePlay from '../components/RoulettePlay.vue'
import MiniGame from '../components/MiniGame.vue'
import PhotoGen from '../components/PhotoGen.vue'
import FourCutView from '../views/FourCutView.vue'
import CarnationView from '../views/CarnationView.vue'
import CouponHome from '../components/CouponHome.vue'
import CouponList from '../components/CouponList.vue'
import LetterHome from '../components/LetterHome.vue'
import LetterDetail from '../components/LetterDetail.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/roulette', name: 'roulette', component: RouletteHome },
  { path: '/roulette/play', name: 'roulette-play', component: RoulettePlay },
  { path: '/minigame', name: 'minigame', component: MiniGame },
  { path: '/photo', name: 'photo', component: PhotoGen },
  { path: '/four-cut', name: 'four-cut', component: FourCutView },
  { path: '/carnation', name: 'carnation', component: CarnationView },
  { path: '/coupons', name: 'coupons', component: CouponHome },
  { path: '/coupons/list', name: 'coupon-list', component: CouponList },
  { path: '/letters', name: 'letters', component: LetterHome },
  { path: '/letters/:child', name: 'letter-detail', component: LetterDetail, props: true }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
