import { procesarRespuesta, procesarRespuestaOperacion } from '@/utils/apiResponse'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'

async function ejecutarOperacion(url, options) {
  const respuesta = await fetch(url, options)
  return procesarRespuestaOperacion(respuesta, { url, method: options.method })
}

export async function listarPrecios(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/precios?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudieron cargar los precios.')
}

export async function obtenerPrecio(id, lang = 'es') {
  const respuesta = await fetch(`${API_URL}/precios/${id}?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudo obtener el precio.')
}

export async function crearPrecio(datos, lang = 'es') {
  return ejecutarOperacion(`${API_URL}/precios?lang=${encodeURIComponent(lang)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
}

export async function actualizarPrecio(id, datos, lang = 'es') {
  return ejecutarOperacion(`${API_URL}/precios/${id}?lang=${encodeURIComponent(lang)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
}

export async function cambiarEstadoPrecio(id) {
  return ejecutarOperacion(`${API_URL}/precios/${id}/estado`, { method: 'PATCH' })
}

export async function listarProductosPrecio(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/productos?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudieron cargar los productos.')
}

export async function listarCentrosPrecio(lang = 'es') {
  const respuesta = await fetch(`${API_URL}/centros-distribucion?lang=${encodeURIComponent(lang)}`)
  return await procesarRespuesta(respuesta, 'No se pudieron cargar los centros.')
}

export const precioService = {
  listarPrecios,
  obtenerPrecio,
  crearPrecio,
  actualizarPrecio,
  cambiarEstadoPrecio,
}
