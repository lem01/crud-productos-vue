import api from './api'
import { procesarRespuesta } from '@/utils/apiResponse'

export const IDIOMAS = Object.freeze({
  es: Object.freeze({ id: 1, codigo: 'es' }),
  en: Object.freeze({ id: 2, codigo: 'en' }),
})

export async function listarCentros(lang = 'es') {
  const respuesta = await api.get('/centros-distribucion', { params: { lang } })
  return await procesarRespuesta(respuesta, 'No se pudo obtener la lista')
}

export async function obtenerCentro(id, lang = 'es') {
  const respuesta = await api.get(`/centros-distribucion/${id}`, { params: { lang } })
  return await procesarRespuesta(respuesta, 'No se pudo obtener el centro de distribución')
}

export async function crearCentro(datos, lang = 'es') {
  const respuesta = await api.post('/centros-distribucion', datos, { params: { lang } })
  return await procesarRespuesta(respuesta, 'No se pudo crear el centro de distribución')
}

export async function actualizarCentro(id, datos, lang = 'es') {
  const respuesta = await api.put(`/centros-distribucion/${id}`, datos, { params: { lang } })
  return await procesarRespuesta(respuesta, 'No se pudo actualizar el centro de distribución')
}

export async function cambiarEstadoCentro(id) {
  const respuesta = await api.patch(`/centros-distribucion/${id}/estado`)
  return await procesarRespuesta(
    respuesta,
    'No se pudo cambiar el estado del centro de distribución',
  )
}

export const centroDistribucionService = {
  listarCentros,
  obtenerCentro,
  crearCentro,
  actualizarCentro,
  cambiarEstadoCentro,
}
