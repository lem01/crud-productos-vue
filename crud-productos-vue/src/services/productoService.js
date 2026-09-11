import api from './api'

export const IDIOMAS = Object.freeze({
  es: Object.freeze({ id: 1, codigo: 'es' }),
  en: Object.freeze({ id: 2, codigo: 'en' }),
})

export async function listarProductos(lang = 'es') {
  const respuesta = await api.get('/productos', { params: { lang } })
  return respuesta.data
}

export async function obtenerProducto(id, lang = 'es') {
  const respuesta = await api.get(`/productos/${id}`, { params: { lang } })
  return respuesta.data
}

export async function crearProducto(datos, lang = 'es') {
  const respuesta = await api.post('/productos', datos, { params: { lang } })
  return respuesta.data
}

export async function actualizarProducto(id, datos, lang = 'es') {
  const respuesta = await api.put(`/productos/${id}`, datos, { params: { lang } })
  return respuesta.data
}

export async function cambiarEstadoProducto(id) {
  const respuesta = await api.patch(`/productos/${id}/estado`)
  return respuesta.data
}

export async function listarCategoriasProducto(lang = 'es') {
  const respuesta = await api.get('/categorias', { params: { lang } })
  return respuesta.data
}

export async function listarMarcasProducto(lang = 'es') {
  const respuesta = await api.get('/marcas', { params: { lang } })
  return respuesta.data
}

export const productoService = {
  listarProductos,
  obtenerProducto,
  crearProducto,
  actualizarProducto,
  cambiarEstadoProducto,
  async getAll(lang = 'es') {
    const productos = await listarProductos(lang)
    const resultado = []
    productos.forEach((producto) => {
      resultado.push({
        ...producto,
        traducciones: {
          [lang]: {
            nombre: producto.nombre,
            descripcion: producto.descripcion,
          },
        },
      })
    })
    return resultado
  },
}
