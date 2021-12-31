import { defineStore } from 'pinia'
import { getStorageItem } from './utils'
import jwtDecode, { JwtPayload } from 'jwt-decode'

interface TokenState {
  user: string | null
  token: string | null
  tokenType: string | null
}

export const useTokenStore = defineStore({
  id: 'token',
  state: (): TokenState => ({
    user: getStorageItem('user'),
    token: getStorageItem('token'),
    tokenType: getStorageItem('tokenType'),
  }),
  getters: {
    isAuthenticated: (state: TokenState) => state.token !== null,
  },
  actions: {
    setToken(token: string, tokenType: string) {
      const { sub } = jwtDecode<JwtPayload>(token)

      this.user = String(sub)
      this.token = token
      this.tokenType = tokenType
    },
    clearToken() {
      this.user = null
      this.token = null
      this.tokenType = null
    },
  },
})
