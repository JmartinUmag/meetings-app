import { defineStore } from 'pinia'
import { getStorageItem } from './utils'
import { User } from '@/interfaces'

interface TokenState {
  user: User | null
  token: string | null
  tokenType: string | null
}

export const useTokenStore = defineStore({
  id: 'token',
  state: (): TokenState => ({
    user: getStorageItem('user', null, true),
    token: getStorageItem('token', ''),
    tokenType: getStorageItem('tokenType', ''),
  }),
  getters: {
    isAuthenticated: (state: TokenState) => state.token !== null,
  },
  actions: {
    setToken(token: string, tokenType: string) {
      this.token = token
      this.tokenType = tokenType
    },
    setUser(user: User) {
      this.user = user
    },
    clearData() {
      this.user = null
      this.token = null
      this.tokenType = null
    },
  },
})
