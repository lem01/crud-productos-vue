const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'

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

export async function listarInventario(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/inventario?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudo cargar el inventario.')
}

export async function obtenerInventario(id, lang = 'es') {
  const respuesta = await fetch(`${API_URL}/inventario/${id}?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudo obtener el inventario.')
}

export async function crearInventario(datos, lang = 'es') {
  const respuesta = await fetch(`${API_URL}/inventario?lang=${encodeURIComponent(lang)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
  return await procesarRespuesta(respuesta, 'No se pudo crear el inventario.')
}

export async function actualizarInventario(id, datos, lang = 'es') {
  const respuesta = await fetch(`${API_URL}/inventario/${id}?lang=${encodeURIComponent(lang)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
  return await procesarRespuesta(respuesta, 'No se pudo actualizar el inventario.')
}

export async function eliminarInventario(id) {
  const respuesta = await fetch(`${API_URL}/inventario/${id}`, { method: 'DELETE' })
  return await procesarRespuesta(respuesta, 'No se pudo eliminar el inventario.')
}

export async function listarProductosInventario(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/productos?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudieron cargar los productos.')
}

export async function listarCentrosInventario(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/centros-distribucion?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudieron cargar los centros.')
}

export const inventarioService = {
  listarInventario,
  obtenerInventario,
  crearInventario,
  actualizarInventario,
  eliminarInventario,
}
