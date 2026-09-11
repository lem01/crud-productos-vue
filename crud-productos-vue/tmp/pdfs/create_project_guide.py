from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    KeepTogether,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "guia_basica_crud_productos_vue.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#17233C")
BLUE = colors.HexColor("#3157D5")
LIGHT_BLUE = colors.HexColor("#EEF2FF")
CYAN = colors.HexColor("#DFF7F5")
TEAL = colors.HexColor("#137C77")
TEXT = colors.HexColor("#2A3447")
MUTED = colors.HexColor("#667085")
LINE = colors.HexColor("#DCE1E9")
PAPER = colors.HexColor("#F7F9FC")
WHITE = colors.white
AMBER = colors.HexColor("#FFF3D6")
RED_BG = colors.HexColor("#FFF0F0")


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverKicker", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=colors.HexColor("#91A6FF"), spaceAfter=12, uppercase=True))
styles.add(ParagraphStyle(name="CoverTitle", fontName="Helvetica-Bold", fontSize=29, leading=34, textColor=WHITE, spaceAfter=14))
styles.add(ParagraphStyle(name="CoverSub", fontName="Helvetica", fontSize=12, leading=18, textColor=colors.HexColor("#DCE3FF"), spaceAfter=16))
styles.add(ParagraphStyle(name="H1x", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=12, spaceBefore=3))
styles.add(ParagraphStyle(name="H2x", fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=BLUE, spaceBefore=10, spaceAfter=7))
styles.add(ParagraphStyle(name="H3x", fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=NAVY, spaceBefore=7, spaceAfter=4))
styles.add(ParagraphStyle(name="Bodyx", fontName="Helvetica", fontSize=9.3, leading=14, textColor=TEXT, spaceAfter=7))
styles.add(ParagraphStyle(name="Smallx", fontName="Helvetica", fontSize=7.7, leading=11, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="Bulletx", fontName="Helvetica", fontSize=9, leading=13.5, textColor=TEXT, leftIndent=12, firstLineIndent=-7, bulletIndent=1, spaceAfter=4))
styles.add(ParagraphStyle(name="Codex", fontName="Courier", fontSize=7.5, leading=10.8, textColor=colors.HexColor("#E7ECFF"), backColor=NAVY, borderPadding=8, spaceBefore=4, spaceAfter=8))
styles.add(ParagraphStyle(name="CodeLight", fontName="Courier", fontSize=7.4, leading=10.5, textColor=NAVY, backColor=colors.HexColor("#F0F3F9"), borderColor=LINE, borderWidth=.5, borderPadding=7, spaceBefore=3, spaceAfter=7))
styles.add(ParagraphStyle(name="Callout", fontName="Helvetica", fontSize=8.8, leading=13, textColor=TEXT, leftIndent=8, rightIndent=8, borderPadding=8, borderColor=colors.HexColor("#C8D3FF"), borderWidth=.7, backColor=LIGHT_BLUE, spaceBefore=5, spaceAfter=8))
styles.add(ParagraphStyle(name="Question", fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=3))
styles.add(ParagraphStyle(name="Answer", fontName="Helvetica", fontSize=8.6, leading=13, textColor=TEXT, leftIndent=8, spaceAfter=5))
styles.add(ParagraphStyle(name="TableHead", fontName="Helvetica-Bold", fontSize=7.6, leading=9.5, textColor=WHITE, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="TableCell", fontName="Helvetica", fontSize=7.4, leading=10, textColor=TEXT))


def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def bullet(text):
    return Paragraph("• " + text, styles["Bulletx"])


def table(rows, widths, header=True, font_size=7.4):
    data = []
    for ri, row in enumerate(rows):
        style = "TableHead" if header and ri == 0 else "TableCell"
        data.append([Paragraph(str(cell), styles[style]) for cell in row])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), .45, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), NAVY)]
        if len(rows) > 1:
            cmds += [("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PAPER])]
    t.setStyle(TableStyle(cmds))
    return t


def flow_box(text, bg=LIGHT_BLUE, fg=NAVY):
    t = Table([[P(text, "TableCell")]], colWidths=[39 * mm], rowHeights=[17 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), .8, fg),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(.5)
    canvas.line(18 * mm, PAGE_H - 14 * mm, PAGE_W - 18 * mm, PAGE_H - 14 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, PAGE_H - 10.5 * mm, "Guía de estudio - CRUD de Productos Vue")
    canvas.drawRightString(PAGE_W - 18 * mm, 10 * mm, f"Página {doc.page}")
    canvas.restoreState()


def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.circle(PAGE_W - 18 * mm, PAGE_H - 25 * mm, 38 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#203661"))
    canvas.circle(10 * mm, 18 * mm, 42 * mm, fill=1, stroke=0)
    canvas.restoreState()


def all_pages(canvas, doc):
    if doc.page == 1:
        cover(canvas, doc)
    else:
        header_footer(canvas, doc)


doc = BaseDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=18 * mm,
    rightMargin=18 * mm,
    topMargin=20 * mm,
    bottomMargin=17 * mm,
    title="Guía básica del proyecto CRUD de Productos Vue",
    author="Guía de estudio generada a partir del código del proyecto",
    subject="Arquitectura, Vue 3, comunicación con API y preparación para prueba técnica",
)
cover_frame = Frame(23 * mm, 30 * mm, PAGE_W - 46 * mm, PAGE_H - 60 * mm, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
body_frame = Frame(18 * mm, 16 * mm, PAGE_W - 36 * mm, PAGE_H - 41 * mm, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="All", frames=[body_frame], onPage=all_pages)])

story = []
story += [Spacer(1, 43 * mm), P("GUÍA BÁSICA PARA PRUEBA TÉCNICA", "CoverKicker"), P("CRUD de Productos<br/>con Vue 3 y Vite", "CoverTitle")]
story += [P("Cómo está estructurado, cómo circulan los datos y cómo se comunica con una API REST.", "CoverSub")]
cover_info = Table([
    [P("ENFOQUE", "TableHead"), P("CASO PRINCIPAL", "TableHead")],
    [P("Comprensión práctica del código", "TableCell"), P("Módulo de productos y BaseModal.vue", "TableCell")],
], colWidths=[58 * mm, 82 * mm])
cover_info.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), BLUE), ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#E9EDFF")),
    ("BOX", (0,0), (-1,-1), .7, colors.HexColor("#91A6FF")), ("INNERGRID", (0,0), (-1,-1), .5, colors.HexColor("#91A6FF")),
    ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
]))
story += [cover_info, Spacer(1, 18 * mm), P("Proyecto analizado localmente • Vue 3.5 • Vite 8 • Bootstrap 5 • Vue Router • Vue I18n", "CoverSub"), PageBreak()]

story += [P("1. El proyecto en 90 segundos", "H1x")]
story += [P("Es una SPA (Single Page Application) administrativa. El navegador carga una sola aplicación Vue; Vue Router cambia la vista visible sin recargar toda la página. Cada módulo presenta una lista, filtros, formularios en modales y operaciones CRUD contra un backend REST.")]
story += [P("Mapa mental", "H2x")]
flow = Table([[flow_box("Usuario<br/><b>interactúa</b>"), P("→", "H2x"), flow_box("Vista Vue<br/><b>coordina estado</b>"), P("→", "H2x"), flow_box("Servicio<br/><b>define endpoint</b>"), P("→", "H2x"), flow_box("API REST<br/><b>procesa datos</b>", CYAN, TEAL)]], colWidths=[39*mm, 8*mm, 39*mm, 8*mm, 39*mm, 8*mm, 39*mm])
flow.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("ALIGN", (1,0), (5,0), "CENTER")]))
story += [flow, Spacer(1, 7 * mm)]
story += [P("Tecnologías y responsabilidad", "H2x"), table([
    ["Tecnología", "Qué hace aquí"],
    ["Vue 3 + Composition API", "Componentes reactivos con <font name='Courier'>ref</font>, <font name='Courier'>reactive</font>, <font name='Courier'>computed</font>, <font name='Courier'>watch</font> y ciclo de vida."],
    ["Vite", "Servidor de desarrollo, variables <font name='Courier'>VITE_*</font>, alias <font name='Courier'>@</font> y compilación de producción."],
    ["Vue Router", "Relaciona URL con una vista y la muestra dentro de <font name='Courier'>&lt;RouterView /&gt;</font>."],
    ["Vue I18n", "Textos de interfaz en español/inglés; el idioma también viaja a la API mediante <font name='Courier'>?lang=</font>."],
    ["Bootstrap + Icons", "Diseño, rejilla, tablas, formularios, botones, modales e iconos."],
    ["Fetch API", "Solicitudes HTTP al backend; no se usa Axios."],
], [40*mm, 130*mm])]
story += [P("Idea clave", "H2x"), P("La vista no debería conocer detalles repetidos de HTTP. Por eso importa la capa <font name='Courier'>services/</font>: traduce acciones del negocio como “listar productos” a una URL y un método HTTP.", "Callout")]
story += [PageBreak()]

story += [P("2. Cómo está organizado", "H1x")]
tree = """src/
|-- main.js                 arranque y plugins
|-- App.vue                 componente raíz
|-- router/index.js         mapa URL -> vista
|-- views/                  pantallas por dominio
|   |-- productos/          ProductosView + ProductoForm
|   |-- categorias/         lista + formulario
|   |-- marcas/             lista + formulario
|   |-- inventario/         lista + formulario
|   `-- ...                 precios, descuentos, etc.
|-- components/
|   |-- layout/             shell, navbar y sidebar
|   `-- common/             piezas reutilizables
|-- services/               acceso a endpoints REST
|-- utils/apiResponse.js    tratamiento de respuestas/errores
|-- i18n/                   mensajes es/en
|-- constants/              catálogos fijos del frontend
`-- assets/css/app.css      estilos globales"""
story += [P(tree.replace("&", "&amp;").replace("<", "&lt;").replace("\n", "<br/>"), "CodeLight")]
story += [P("Recorrido de arranque", "H2x")]
story += [table([
    ["Paso", "Archivo", "Qué ocurre"],
    ["1", "index.html", "Aporta el elemento DOM <font name='Courier'>#app</font>."],
    ["2", "src/main.js", "Crea Vue, carga Bootstrap/CSS, registra router e i18n y monta la aplicación."],
    ["3", "src/App.vue", "Renderiza <font name='Courier'>AppLayout</font>."],
    ["4", "AppLayout.vue", "Muestra sidebar, navbar y el contenido dinámico con <font name='Courier'>RouterView</font>."],
    ["5", "router/index.js", "Elige la vista según la URL, por ejemplo <font name='Courier'>/productos</font>."],
], [14*mm, 42*mm, 114*mm])]
story += [P("Patrón de cada módulo", "H2x")]
story += [bullet("<b>*View.vue</b>: conserva el estado de la pantalla, carga datos, filtra, abre modales y llama servicios."), bullet("<b>*Form.vue</b>: recibe datos por props, valida campos, construye el payload y emite <font name='Courier'>submit</font>."), bullet("<b>*Service.js</b>: define endpoints y devuelve datos del backend."), bullet("<b>Componentes common</b>: resuelven UI repetida sin conocer el negocio.")]
story += [P("Regla para ubicar código", "Callout"), P("Si cambia la apariencia reutilizable, busca en <font name='Courier'>components/common</font>. Si cambia el flujo de una pantalla, busca en <font name='Courier'>views</font>. Si cambia la URL o el contrato HTTP, busca en <font name='Courier'>services</font>.", "Bodyx")]
story += [PageBreak()]

story += [P("3. La comunicación con la API", "H1x")]
story += [P("La URL base viene de <font name='Courier'>import.meta.env.VITE_API_URL</font>. El README propone este archivo en la raíz:")]
story += [P("VITE_API_URL=http://localhost:8080/api", "Codex")]
story += [P("Ejemplo real: listar productos", "H2x")]
story += [table([
    ["Capa", "Código / resultado"],
    ["Vista", "<font name='Courier'>listarProductos(locale.value)</font>"],
    ["Servicio", "<font name='Courier'>api.get('/productos', { params: { lang } })</font>"],
    ["Cliente HTTP", "Construye <font name='Courier'>GET {baseURL}/productos?lang=es</font>."],
    ["Backend", "Responde JSON con la lista."],
    ["Vista", "Asigna el resultado a <font name='Courier'>productos.value</font>; Vue actualiza la tabla."],
], [37*mm, 133*mm])]
story += [P("Qué hace src/services/api.js", "H2x")]
story += [bullet("Agrega la URL base y serializa parámetros con <font name='Courier'>URLSearchParams</font>."), bullet("Serializa el body como JSON y agrega <font name='Courier'>Content-Type: application/json</font> cuando hay datos."), bullet("Cancela después de 10 segundos con <font name='Courier'>AbortController</font>."), bullet("Intenta leer JSON; ante estado no exitoso crea un <font name='Courier'>Error</font> con <font name='Courier'>error.response</font>."), bullet("Expone <font name='Courier'>get</font>, <font name='Courier'>post</font>, <font name='Courier'>put</font> y <font name='Courier'>patch</font>. No expone <font name='Courier'>delete</font>.")]
story += [P("Métodos HTTP usados", "H2x"), table([
    ["Método", "Intención", "Ejemplo"],
    ["GET", "Consultar", "/productos?lang=es"],
    ["POST", "Crear", "/productos"],
    ["PUT", "Reemplazar/actualizar", "/productos/{id}"],
    ["PATCH", "Cambio parcial", "/productos/{id}/estado"],
    ["DELETE", "Eliminar", "/inventario/{id} (fetch directo)"],
], [25*mm, 59*mm, 86*mm])]
story += [P("Detalle importante", "H2x"), P("El frontend espera que <font name='Courier'>VITE_API_URL</font> exista para los módulos que usan <font name='Courier'>api.js</font>. Otros servicios incluyen un fallback a <font name='Courier'>http://localhost:8080/api</font>. Esa diferencia puede producir comportamientos distintos si falta el archivo <font name='Courier'>.env</font>.", "Callout")]
story += [PageBreak()]

story += [P("4. Caso completo: pantalla de productos", "H1x")]
story += [P("ProductosView.vue funciona como componente coordinador (o container). Mantiene el estado y conecta UI, formulario y servicios.")]
story += [P("Al entrar a /productos", "H2x")]
story += [table([
    ["Momento", "Acción"],
    ["onMounted(load)", "Ejecuta la carga inicial."],
    ["load()", "Activa <font name='Courier'>cargando</font> y limpia el error."],
    ["Promise.all", "Solicita productos, categorías y marcas en paralelo."],
    ["Éxito", "Actualiza tres refs; el template renderiza la tabla y los selects."],
    ["Error", "Guarda un mensaje en <font name='Courier'>serviceError</font>."],
    ["finally", "Desactiva el indicador de carga."],
], [38*mm, 132*mm])]
story += [P("Estado reactivo esencial", "H2x")]
story += [table([
    ["Estado", "Propósito"],
    ["productos, categorias, marcas", "Datos obtenidos del backend."],
    ["cargando / guardando", "Evitan UI inconsistente y operaciones duplicadas."],
    ["search, status, category", "Criterios locales de filtrado."],
    ["formOpen / confirmOpen", "Controlan los dos modales."],
    ["editing / selected", "Producto editado o pendiente de cambio de estado."],
    ["notice / serviceError", "Feedback de éxito y error."],
], [49*mm, 121*mm])]
story += [P("Filtrado", "H2x"), P("<font name='Courier'>filtered</font> es un <font name='Courier'>computed</font>: deriva una lista a partir de productos y filtros. No modifica el arreglo original ni consulta nuevamente el backend. Al cambiar una dependencia, Vue recalcula el resultado.")]
story += [P("Cambio de idioma", "H2x"), P("<font name='Courier'>watch(locale, load)</font> vuelve a consultar la API cuando cambia el idioma. Esto es distinto de traducir la interfaz: Vue I18n traduce botones y etiquetas; el parámetro <font name='Courier'>lang</font> pide al backend nombres y descripciones localizados.")]
story += [P("Modelo mental", "Callout"), P("<b>ref/reactive</b> guarda estado; <b>computed</b> deriva estado; <b>watch</b> ejecuta un efecto cuando algo cambia; <b>onMounted</b> ejecuta un efecto al entrar la vista.")]
story += [PageBreak()]

story += [P("5. Crear y editar un producto", "H1x")]
story += [P("Flujo de creación", "H2x")]
steps = [
    ["1", "Clic en Nuevo", "<font name='Courier'>create()</font> limpia <font name='Courier'>editing</font> y abre el modal."],
    ["2", "Formulario", "ProductoForm recibe catálogos y listas de valores existentes."],
    ["3", "Validación", "Normaliza código/SKU, valida obligatorios y duplicados."],
    ["4", "Evento", "Emite <font name='Courier'>submit</font> con un payload listo para la API."],
    ["5", "Vista", "<font name='Courier'>save(data)</font> llama <font name='Courier'>crearProducto</font>."],
    ["6", "Después", "Cierra el modal, recarga datos y muestra aviso de éxito."],
]
story += [table([["Paso", "Lugar", "Qué sucede"]] + steps, [14*mm, 40*mm, 116*mm])]
story += [P("Payload aproximado", "H2x")]
payload = """{
  codigo: "PROD-001",
  sku: "SKU-001",
  codigoBarras: null,
  categoriaId: 3,
  marcaId: 2,
  activo: true,
  traducciones: [
    { idiomaId: 1, nombre: "Café", descripcion: "..." },
    { idiomaId: 2, nombre: "Coffee", descripcion: "..." }
  ]
}"""
story += [P(payload.replace("\n", "<br/>").replace(" ", "&nbsp;"), "CodeLight")]
story += [P("Flujo de edición", "H2x")]
story += [bullet("La lista muestra una traducción a la vez, así que <font name='Courier'>edit(item)</font> consulta el producto en español y en inglés en paralelo."), bullet("La vista reconstruye un objeto <font name='Courier'>editing</font> con <font name='Courier'>traducciones.es</font> y <font name='Courier'>traducciones.en</font>."), bullet("ProductoForm observa el prop con <font name='Courier'>watch</font> y copia los datos a su estado interno."), bullet("Al guardar, la vista detecta <font name='Courier'>Boolean(editing.value)</font> y usa PUT en lugar de POST.")]
story += [P("Props hacia abajo, eventos hacia arriba", "H2x"), P("La vista entrega datos al formulario mediante <b>props</b>. El formulario no llama directamente a la API: comunica el resultado con <font name='Courier'>emit('submit', payload)</font>. Este flujo unidireccional hace más fácil reutilizar, probar y razonar sobre el componente.", "Callout")]
story += [PageBreak()]

story += [P("6. BaseModal.vue, explicado", "H1x")]
story += [P("BaseModal es infraestructura visual reutilizable. No sabe qué es un producto ni cómo guardar: solo muestra contenido, título, pie y comunica el cierre.")]
story += [P("Contrato del componente", "H2x"), table([
    ["Entrada / salida", "Significado"],
    ["prop show", "Booleano que decide si el modal existe en el DOM."],
    ["prop title", "Texto del encabezado."],
    ["prop size", "Genera una clase Bootstrap como <font name='Courier'>modal-lg</font>."],
    ["prop closeOnBackdrop", "Permite o impide cerrar al hacer clic fuera del contenido."],
    ["evento close", "Solicita al padre cerrar; el padre cambia su propio estado."],
    ["slot default", "Contenido principal, por ejemplo ProductoForm."],
    ["slot footer", "Botones opcionales del pie."],
], [48*mm, 122*mm])]
story += [P("Las piezas Vue importantes", "H2x")]
story += [bullet("<font name='Courier'>&lt;Teleport to='body'&gt;</font> mueve el modal al <font name='Courier'>body</font>, evitando problemas de capas, overflow y stacking context del componente padre."), bullet("<font name='Courier'>v-if='show'</font> crea y destruye el modal según el estado."), bullet("<font name='Courier'>@mousedown.self</font> solo reacciona cuando el clic ocurre exactamente en el fondo, no dentro de <font name='Courier'>modal-content</font>."), bullet("<font name='Courier'>$slots.footer</font> evita dibujar un pie vacío."), bullet("El <font name='Courier'>watch</font> agrega/quita <font name='Courier'>modal-open</font> en el body; <font name='Courier'>onBeforeUnmount</font> garantiza limpieza.")]
story += [P("Quién controla a quién", "H2x")]
modal_flow = Table([
    [flow_box("ProductosView<br/><b>formOpen</b>"), P("prop show →", "TableCell"), flow_box("BaseModal<br/><b>presenta UI</b>", CYAN, TEAL)],
    [P("", "Smallx"), P("← evento close", "TableCell"), P("", "Smallx")],
], colWidths=[55*mm, 38*mm, 55*mm], hAlign="CENTER")
modal_flow.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("ALIGN", (1,0), (1,-1), "CENTER")]))
story += [modal_flow, Spacer(1, 4 * mm)]
story += [P("Ejemplo de uso", "H2x"), P("&lt;BaseModal :show='formOpen' :title='editing ? editTitle : newTitle'<br/>&nbsp;&nbsp;@close='formOpen = false'&gt;<br/>&nbsp;&nbsp;&lt;ProductoForm @submit='save' /&gt;<br/>&nbsp;&nbsp;&lt;template #footer&gt;...botones...&lt;/template&gt;<br/>&lt;/BaseModal&gt;", "CodeLight")]
story += [PageBreak()]

story += [P("7. Manejo de errores y estados", "H1x")]
story += [P("La vista envuelve operaciones asíncronas con <font name='Courier'>try/catch/finally</font>. Este patrón mantiene sincronizados datos, mensajes y spinners.")]
story += [table([
    ["Bloque", "Responsabilidad"],
    ["try", "Ejecuta la solicitud y aplica el resultado."],
    ["catch", "Convierte el fallo en un mensaje visible para el usuario."],
    ["finally", "Restablece <font name='Courier'>cargando</font> o <font name='Courier'>guardando</font>, tanto si hubo éxito como error."],
], [28*mm, 142*mm])]
story += [P("Capas actuales de error", "H2x")]
story += [bullet("<font name='Courier'>api.js</font> produce un error con mensaje HTTP y adjunta <font name='Courier'>error.response</font>."), bullet("<font name='Courier'>apiResponse.js</font> ofrece funciones para extraer datos, tratar 204 y registrar <font name='Courier'>messageLog</font>."), bullet("Algunos servicios duplican su propia función <font name='Courier'>procesarRespuesta</font>."), bullet("Productos usa principalmente <font name='Courier'>error.message</font> para presentar el error.")]
story += [P("Riesgos técnicos que puedes mencionar", "H2x")]
story += [table([
    ["Hallazgo", "Impacto", "Mejora razonable"],
    ["Dos estilos HTTP", "Código duplicado y manejo de errores desigual.", "Migrar todos los servicios a un único cliente."],
    ["Fallback desigual de URL", "Un módulo puede funcionar sin .env y otro no.", "Validar la variable al iniciar y usar una política única."],
    ["api.js sin DELETE", "Inventario no puede usar el cliente común.", "Agregar <font name='Courier'>delete(path, config)</font>."],
    ["Sin autenticación", "No hay token ni manejo de 401/403.", "Agregar headers/interceptor equivalente si la prueba lo exige."],
    ["Sin paginación real", "La UI muestra controles, pero filtra la lista completa localmente.", "Definir parámetros page/size y metadatos del backend."],
], [42*mm, 60*mm, 68*mm])]
story += [P("Cómo explicarlo sin criticar de más", "Callout"), P("“La separación por servicios es correcta. Veo una migración parcial hacia un cliente HTTP compartido; como siguiente paso unificaría los servicios para centralizar timeout, errores, headers y autenticación.”")]
story += [PageBreak()]

story += [P("8. Cómo ejecutar y depurar", "H1x")]
story += [P("Preparación", "H2x")]
story += [P("npm install<br/># crear .env con VITE_API_URL=http://localhost:8080/api<br/>npm run dev", "Codex")]
story += [P("El backend debe estar activo. Vite suele mostrar una URL local como <font name='Courier'>http://localhost:5173</font>.")]
story += [P("Checklist si la tabla no carga", "H2x")]
story += [bullet("Revisar la consola del navegador y la pestaña Network."), bullet("Confirmar que <font name='Courier'>VITE_API_URL</font> tiene <font name='Courier'>/api</font> y reiniciar Vite después de editar <font name='Courier'>.env</font>."), bullet("Abrir la solicitud: URL, método, query <font name='Courier'>lang</font>, status y respuesta JSON."), bullet("Comprobar CORS en el backend si el navegador bloquea la solicitud."), bullet("Comprobar que los nombres del JSON coinciden con los usados en la vista: <font name='Courier'>id</font>, <font name='Courier'>codigo</font>, <font name='Courier'>nombre</font>, <font name='Courier'>activo</font>, etc."), bullet("Distinguir timeout (10 s en api.js), error HTTP y error de red.")]
story += [P("Cómo seguir una operación en el código", "H2x")]
story += [table([
    ["Pregunta", "Dónde mirar"],
    ["¿Qué dispara la acción?", "Evento <font name='Courier'>@click</font> o <font name='Courier'>@submit</font> en la vista/formulario."],
    ["¿Qué función corre?", "Función del <font name='Courier'>&lt;script setup&gt;</font>, por ejemplo <font name='Courier'>save</font>."],
    ["¿Qué endpoint llama?", "Import correspondiente en <font name='Courier'>src/services</font>."],
    ["¿Qué se envía?", "Payload construido justo antes de <font name='Courier'>emit('submit')</font>."],
    ["¿Qué cambia en pantalla?", "Asignaciones a refs/reactive y condiciones <font name='Courier'>v-if</font>/<font name='Courier'>v-for</font>."],
], [48*mm, 122*mm])]
story += [P("Prueba rápida de producción", "H2x"), P("Ejecuta <font name='Courier'>npm run build</font>. Si compila, valida sintaxis e integración del bundle; no sustituye pruebas funcionales contra el backend.", "Callout")]
story += [PageBreak()]

story += [P("9. Preguntas típicas de prueba técnica", "H1x")]
qa = [
    ("¿Por qué separar View y Form?", "La vista coordina datos/API; el formulario gestiona entrada, validación y payload. Reduce responsabilidades y permite reutilizar el formulario para crear y editar."),
    ("¿Qué diferencia hay entre ref y reactive?", "ref envuelve un valor y se accede con .value en JavaScript; reactive crea un proxy para un objeto. En el template Vue los desenvuelve automáticamente."),
    ("¿Por qué filtered es computed?", "Es información derivada. Vue la recalcula cuando cambian productos o filtros y puede reutilizar el valor mientras no cambien dependencias."),
    ("¿Por qué Promise.all?", "Productos, categorías y marcas son solicitudes independientes. Ejecutarlas en paralelo reduce el tiempo total de carga; si una falla, el conjunto rechaza."),
    ("¿Para qué sirve Teleport?", "Renderiza el modal bajo body aunque su declaración esté dentro de la vista, evitando límites y conflictos visuales del árbol padre."),
    ("¿Cómo viaja el formulario al backend?", "ProductoForm emite un payload; ProductosView recibe el evento; productoService elige POST o PUT; api.js serializa JSON y usa fetch."),
    ("¿Qué ocurre al cambiar el idioma?", "Vue I18n cambia textos locales y el watch de la vista recarga datos del backend con el nuevo parámetro lang."),
    ("¿Cómo evitar doble envío?", "La vista comprueba guardando, lo activa antes del await y deshabilita controles hasta finally."),
    ("¿Qué mejorarías primero?", "Unificar todos los servicios en api.js, agregar DELETE, validar VITE_API_URL y estandarizar errores. Después añadir tests y paginación real."),
]
for q, a in qa:
    story += [P(q, "Question"), P(a, "Answer")]
story += [PageBreak()]

story += [P("10. Guion corto para presentar el proyecto", "H1x")]
story += [P("Puedes explicarlo así en 60-90 segundos:", "H2x")]
pitch = """“Es una SPA administrativa hecha con Vue 3 y Vite. main.js registra Router e i18n; AppLayout mantiene la navegación y RouterView muestra cada módulo. Los módulos están separados por dominio: una View coordina el estado y las llamadas, y un Form recibe props, valida y emite el payload. La comunicación REST vive en services: para productos se usa un cliente común basado en fetch que toma VITE_API_URL, agrega query params, serializa JSON, aplica timeout y normaliza errores. En productos, la carga obtiene lista, categorías y marcas con Promise.all; crear usa POST, editar usa PUT y el estado usa PATCH. BaseModal es un componente reutilizable controlado por props y eventos, con Teleport y slots. Como mejora, unificaría los servicios que aún usan fetch directo y agregaría DELETE, autenticación y paginación.”"""
story += [P(pitch, "Callout")]
story += [P("Ruta de estudio recomendada", "H2x"), table([
    ["Orden", "Lee", "Objetivo"],
    ["1", "main.js → App.vue → AppLayout.vue", "Comprender el arranque."],
    ["2", "router/index.js", "Relacionar URLs con pantallas."],
    ["3", "ProductosView.vue", "Entender estado y coordinación."],
    ["4", "ProductoForm.vue", "Seguir props, validación y emit."],
    ["5", "productoService.js → api.js", "Seguir la solicitud HTTP completa."],
    ["6", "BaseModal.vue", "Comprender reutilización, slots y Teleport."],
    ["7", "Otro módulo", "Comparar patrones e inconsistencias."],
], [17*mm, 67*mm, 86*mm])]
story += [P("Ejercicio práctico", "H2x")]
story += [bullet("Abre /productos y, con Network visible, crea un registro de prueba."), bullet("Antes de enviar, predice método, URL, query y body."), bullet("Compara tu predicción con la solicitud real."), bullet("Edita el registro y explica por qué se hacen dos GET antes del PUT."), bullet("Cambia el idioma y observa qué llamadas se repiten."), bullet("Provoca un error controlado (backend apagado o dato inválido) y sigue el mensaje hasta la UI.")]
story += [P("Si puedes narrar esos seis pasos señalando los archivos involucrados, ya entiendes el núcleo del proyecto y puedes defenderlo con seguridad en una prueba técnica.", "Callout")]
story += [Spacer(1, 5 * mm), P("Documento elaborado a partir del código actual del repositorio. No describe el backend interno; infiere su contrato desde los endpoints y payloads consumidos por el frontend.", "Smallx")]

doc.build(story)
print(OUT)
