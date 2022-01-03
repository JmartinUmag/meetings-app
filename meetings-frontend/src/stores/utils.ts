function getStorageItem(
  key: string,
  defaultValue: string | null = null,
  json = false
) {
  if (!['', null].includes(localStorage.getItem(key))) {
    if (json) {
      try {
        return JSON.parse(String(localStorage.getItem(key)))
      } catch (e) {
        return defaultValue
      }
    }
    return localStorage.getItem(key)
  } else {
    return defaultValue
  }
}

export { getStorageItem }
