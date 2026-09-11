const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'

async function procesarRespuesta(response, mensajeError) {
  if (!response.ok) {
    let mensaje = mensajeError
    try {
      const error = await response.json()
      mensaje = error.message || error.detail || mensajeError
    } catch {
      mensaje = mensajeError
    }
    throw new Error(mensaje)
  }

  if (response.status === 204) return null
  const contenido = await response.text()
  if (!contenido) return null
  return JSON.parse(contenido)
}

export async function listarTiposCambio(lang = 'es') {
  const response = await fetch(`${API_URL}/tipos-cambio?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(response, 'No se pudieron cargar los tipos de cambio.')
}

export async function obtenerTipoCambio(id, lang = 'es') {
  const response = await fetch(`${API_URL}/tipos-cambio/${id}?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(response, 'No se pudo obtener el tipo de cambio.')
}

export async function crearTipoCambio(datos, lang = 'es') {
  const response = await fetch(`${API_URL}/tipos-cambio?lang=${encodeURIComponent(lang)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
  return await procesarRespuesta(response, 'No se pudo crear el tipo de cambio.')
}

export async function actualizarTipoCambio(id, datos, lang = 'es') {
  const response = await fetch(`${API_URL}/tipos-cambio/${id}?lang=${encodeURIComponent(lang)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
  return await procesarRespuesta(response, 'No se pudo actualizar el tipo de cambio.')
}

export async function cambiarEstadoTipoCambio(id) {
  const response = await fetch(`${API_URL}/tipos-cambio/${id}/estado`, { method: 'PATCH' })
  return await procesarRespuesta(response, 'No se pudo cambiar el estado del tipo de cambio.')
}

export const tipoCambioService = {
  listarTiposCambio,
  obtenerTipoCambio,
  crearTipoCambio,
  actualizarTipoCambio,
  cambiarEstadoTipoCambio,
}
