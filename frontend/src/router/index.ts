import { createMemoryHistory, createRouter } from 'vue-router'
import Home from '@/views/Home.vue'
import HolidayMember from '@/views/HolidayMember.vue'
import PartyWorldMember from '@/views/PartyWorldMember.vue'

const routes = [
  { path: '/', component: Home},
  { path: '/HolidayMember', component: HolidayMember },
  { path: '/PartyWorldMember', component: PartyWorldMember },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router