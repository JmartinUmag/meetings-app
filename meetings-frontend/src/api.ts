import router from '@/router'
import camelcaseKeys from 'camelcase-keys'
import { useTokenStore } from '@/stores/token'
import { Meeting, MeetingCreate, Token, User } from '@/interfaces'
import snakecaseKeys from 'snakecase-keys'

const BASE_URL = import.meta.env.VITE_API_BASE_URL

async function api<T>(
  url: string,
  method = 'GET',
  body: BodyInit | null | undefined = undefined,
  headers: HeadersInit | Record<string, never> = {}
): Promise<T> {
  const tokenStore = useTokenStore()

  if (tokenStore.isAuthenticated) {
    headers = {
      Authorization: `${tokenStore.tokenType} ${tokenStore.token}`,
      ...headers,
    }
  }

  return fetch(url, { method, body, headers }).then(async (response) => {
    if (!response.ok) {
      const text = await response.text()
      let detail: string

      // if the user is authenticated and the response is a 401,
      // logout the user and don't throw the error
      if (response.status === 401 && tokenStore.isAuthenticated) {
        tokenStore.clearData()
        await router.push({ name: 'Login' })
        return Promise.resolve()
      }

      // get error detail from response body
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

async function getUsers(): Promise<User[]> {
  return api(`${BASE_URL}/auth/users/`)
}

async function getMyUser(): Promise<User> {
  return api(`${BASE_URL}/auth/users/me`)
}

async function createMeeting(meeting: MeetingCreate): Promise<Meeting> {
  return api(
    `${BASE_URL}/meetings/meetings/`,
    'POST',
    JSON.stringify(snakecaseKeys(meeting)),
    {
      'Content-Type': 'application/json',
    }
  )
}

async function getMeetingById(id: number | string): Promise<Meeting> {
  return api(`${BASE_URL}/meetings/meetings/${id}`)
}

async function createFile(
  file: File,
  meetingId: number | string
): Promise<File> {
  const formData = new FormData()
  formData.append('file', file)

  return api(
    `${BASE_URL}/meetings/meetings/${meetingId}/add-file`,
    'POST',
    formData
  )
}

export { login, getMyUser, getUsers, createMeeting, getMeetingById, createFile }
