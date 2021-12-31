import camelcaseKeys from 'camelcase-keys'
import { useTokenStore } from '@/stores/token'
import { Token } from '@/interfaces'

const BASE_URL = 'http://localhost:8000'

async function api<T>(
  url: string,
  method = 'GET',
  body: BodyInit | null | undefined = undefined,
  headers: HeadersInit | Record<string, never> = {}
): Promise<T> {
  const token = useTokenStore()

  if (token.isAuthenticated) {
    headers = {
      Authorization: `${token.tokenType} ${token.token}`,
      ...headers,
    }
  }

  return fetch(url, { method, body, headers }).then(async (response) => {
    if (!response.ok) {
      const text = await response.text()
      let detail: string

      try {
        const json = JSON.parse(text)
        detail = json.detail
      } catch (error) {
        detail = await response.text()
      }

      throw { status: response.status, message: detail }
    }
    return camelcaseKeys(await response.json())
  })
}

/*
 * Endpoints
 */
async function login(username: string, password: string): Promise<Token> {
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)
  params.append('grant_type', 'password')

  return api(`${BASE_URL}/auth/token`, 'POST', params, {
    'Content-Type': 'application/x-www-form-urlencoded',
  })
}

export { login }
