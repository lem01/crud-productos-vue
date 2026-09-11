export const obtenerMensajeRespuesta = (response) => {
  return response?.data?.message || ''
}

export const manejarErrorApi = (error) => {
  const respuesta = error?.response?.data
  const mensajeUsuario = respuesta?.message || 'Ocurrió un error al procesar la solicitud'
  const messageLog = respuesta?.messageLog

  if (typeof messageLog === 'string' ? messageLog.trim() : Boolean(messageLog)) {
    console.error('[ERROR TÉCNICO DEL SERVIDOR]', {
      status: respuesta?.status,
      messageLog,
      endpoint: error?.config?.url,
      method: error?.config?.method,
    })
  }

  return mensajeUsuario
}

export const procesarRespuesta = async (respuesta, mensajeError) => {
  // El cliente compartido `api` ya entrega el contenido JSON dentro de `data`.
  if (respuesta && Object.prototype.hasOwnProperty.call(respuesta, 'data')) {
    return respuesta.status === 204 ? null : respuesta.data
  }

  // Compatibilidad con servicios que todavía utilizan `fetch` directamente.
  if (!respuesta.ok) {
    let mensaje = mensajeError

    try {
      const error = await respuesta.json()
      mensaje = error.message || error.detail || mensajeError
    } catch {
      mensaje = mensajeError
    }

    throw new Error(mensaje)
  }

  if (respuesta.status === 204) return null

  const contenido = await respuesta.text()
  return contenido ? JSON.parse(contenido) : null
}

export const procesarRespuestaOperacion = async (respuesta, config) => {
  let data = null
  const contenido = await respuesta.text()

  if (contenido) {
    try {
      data = JSON.parse(contenido)
    } catch {
      data = null
    }
  }

  if (!respuesta.ok) {
    const error = new Error(data?.message || 'Ocurrió un error al procesar la solicitud')
    error.response = { data, status: respuesta.status }
    error.config = config
    throw error
  }

  return { data, status: respuesta.status }
}
