import api from './api'

export const IDIOMAS = Object.freeze({
  es: Object.freeze({ id: 1, codigo: 'es' }),
  en: Object.freeze({ id: 2, codigo: 'en' }),
})

export async function listarMarcas(lang = 'es') {
  const { data } = await api.get('/marcas', { params: { lang } })
  return data
}

export async function obtenerMarca(id, lang = 'es') {
  const { data } = await api.get(`/marcas/${id}`, { params: { lang } })
  return data
}

export async function crearMarca(datos, lang = 'es') {
  const { data } = await api.post('/marcas', datos, { params: { lang } })
  return data
}

export async function actualizarMarca(id, datos, lang = 'es') {
  const { data } = await api.put(`/marcas/${id}`, datos, { params: { lang } })
  return data
}

export async function cambiarEstadoMarca(id) {
  const { data } = await api.patch(`/marcas/${id}/estado`)
  return data
}

export const marcaService = {
  listarMarcas,
  obtenerMarca,
  crearMarca,
  actualizarMarca,
  cambiarEstadoMarca,
}
