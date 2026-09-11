const baseURL = import.meta.env.VITE_API_URL
const timeout = 10000

  async function request(method, path, data, config = {}) {
  const query = config.params ? `?${new URLSearchParams(config.params).toString()}` : ''
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)

  try {
    const response = await fetch(`${baseURL}${path}${query}`, {
      method,
      headers: data === undefined ? undefined : { 'Content-Type': 'application/json' },
      body: data === undefined ? undefined : JSON.stringify(data),
      signal: controller.signal,
    })

    const responseData = await response.json().catch(() => null)

    if (!response.ok) {
      const error = new Error(responseData?.message || `Error HTTP ${response.status}`)
      error.response = { data: responseData, status: response.status }
      throw error
    }

    return { data: responseData, status: response.status }
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error(`La solicitud superó el tiempo límite de ${timeout / 1000} segundos`)
    }

    throw error
  } finally {
    clearTimeout(timeoutId)
  }
}

const api = {
  get(path, config) {
    return request('GET', path, undefined, config)
  },
  post(path, data, config) {
    return request('POST', path, data, config)
  },
  put(path, data, config) {
    return request('PUT', path, data, config)
  },
  patch(path, data, config) {
    return request('PATCH', path, data, config)
  },
}

export default api
