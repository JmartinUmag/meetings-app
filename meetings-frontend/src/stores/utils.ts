function getStorageItem(key: string, defaultValue: string | null = null) {
  if (!['', null].includes(localStorage.getItem(key))) {
    return localStorage.getItem(key)
  } else {
    return defaultValue
  }
}

export { getStorageItem }
