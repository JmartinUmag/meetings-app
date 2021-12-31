import { apiError } from '@/interfaces'

function isApiError(error: unknown): error is apiError {
  // @ts-ignore
  return 'status' in error && 'message' in error
}

export { isApiError }
