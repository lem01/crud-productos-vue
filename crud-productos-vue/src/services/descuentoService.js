const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'

export const IDIOMAS = Object.freeze({
  es: Object.freeze({ id: 1, codigo: 'es' }),
  en: Object.freeze({ id: 2, codigo: 'en' }),
})

async function procesarRespuesta(respuesta, mensajeError) {
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
  if (!contenido) return null
  return JSON.parse(contenido)
}

export async function listarDescuentos(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/descuentos?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudieron cargar los descuentos.')
}

export async function obtenerDescuento(id, lang = 'es') {
  const respuesta = await fetch(`${API_URL}/descuentos/${id}?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudo obtener el descuento.')
}

export async function crearDescuento(datos, lang = 'es') {
  const respuesta = await fetch(`${API_URL}/descuentos?lang=${encodeURIComponent(lang)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
  return await procesarRespuesta(respuesta, 'No se pudo crear el descuento.')
}

export async function actualizarDescuento(id, datos, lang = 'es') {
  const respuesta = await fetch(`${API_URL}/descuentos/${id}?lang=${encodeURIComponent(lang)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
  return await procesarRespuesta(respuesta, 'No se pudo actualizar el descuento.')
}

export async function cambiarEstadoDescuento(id) {
  const respuesta = await fetch(`${API_URL}/descuentos/${id}/estado`, { method: 'PATCH' })
  return await procesarRespuesta(respuesta, 'No se pudo cambiar el estado del descuento.')
}

export async function listarCentrosDescuento(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/centros-distribucion?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudieron cargar los centros.')
}

export async function listarTiposDescuento(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/tipos-descuento?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudieron cargar los tipos de descuento.')
}

export async function listarProductosDescuento(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/productos?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudieron cargar los productos.')
}

export const descuentoService = {
  listarDescuentos,
  obtenerDescuento,
  crearDescuento,
  actualizarDescuento,
  cambiarEstadoDescuento,
}
