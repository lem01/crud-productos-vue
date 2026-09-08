import api from './api'

export const IDIOMAS = {
  es: { id: 1, codigo: 'es' },
  en: { id: 2, codigo: 'en' },
}

export async function listarCategorias(lang) {
  const { data } = await api.get('/categorias', { params: { lang } })
  return data
}

export async function obtenerCategoria(id, lang) {
  const { data } = await api.get(`/categorias/${id}`, { params: { lang } })
  return data
}

export async function crearCategoria(datos, lang) {
  const { data } = await api.post('/categorias', datos, { params: { lang } })
  return data
}

export async function actualizarCategoria(id, datos, lang) {
  const { data } = await api.put(`/categorias/${id}`, datos, { params: { lang } })
  return data
}

export async function cambiarEstadoCategoria(id) {
  await api.patch(`/categorias/${id}/estado`)
}

export const categoriaService = {
  listarCategorias,
  obtenerCategoria,
  crearCategoria,
  actualizarCategoria,
  cambiarEstadoCategoria,
  // Compatibilidad con el selector de categorías del módulo de productos.
  async getAll(lang = 'es') {
    const categorias = await listarCategorias(lang)
    return categorias.map((categoria) => ({
      ...categoria,
      traducciones: {
        [lang]: {
          nombre: categoria.nombre,
          descripcion: categoria.descripcion,
        },
      },
    }))
  },
}
