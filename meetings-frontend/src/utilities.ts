import { apiError, Role } from '@/interfaces'
import { format } from 'date-fns'
import { useTokenStore } from '@/stores/token'
import router from '@/router'

function isApiError(error: unknown): error is apiError {
  // @ts-ignore
  return 'status' in error && 'message' in error
}

function formatDateTime(datetime: Date | string): string {
  if (typeof datetime === 'string') {
    datetime = new Date(datetime)
  }
  return format(datetime, 'dd/MM/yyyy HH:mm')
}

function getFileUrl(filename: string): string {
  const baseUrl = import.meta.env.VITE_STORAGE_BASE_URL
  return `${baseUrl}/${filename}`
}

function checkRoutePermission(
  routeName: string,
  routeParams: Record<string, string | never> = {}
): boolean {
  const tokenStore = useTokenStore()
  const user = tokenStore.user
  const route = router.resolve({ name: routeName, params: routeParams })

  if (user !== null && user.roles) {
    if (route.meta.allowedRoles) {
      return user.roles.some((role: Role) =>
        (route.meta.allowedRoles as string[]).includes(role.name)
      )
    } else {
      return true
    }
  }

  return false
}

export { isApiError, formatDateTime, getFileUrl, checkRoutePermission }
