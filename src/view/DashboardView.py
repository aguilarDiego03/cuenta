import flet as ft
from datetime import datetime

def DashboardView(page, tarea_controller):
    user = getattr(page, "user_data", None)
    
    COLOR_PRINCIPAL = "#57689E"
    COLOR_FONDO = "#F5F5F5"
    
    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=10)
    
    fecha_limite = ft.DatePicker(
        first_date=datetime(2000, 1, 1),
        last_date=datetime(2030, 12, 31)
    )
    
    hora_limite = ft.TimePicker()
    
    page.overlay.append(fecha_limite)
    page.overlay.append(hora_limite)

    def abrir_calendario(e):
        fecha_limite.open = True
        page.update()

    def abrir_reloj(e):
        hora_limite.open = True
        page.update()
    
    btn_fecha = ft.ElevatedButton(
        "📅 Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=abrir_calendario,
        bgcolor=COLOR_FONDO,
        color=COLOR_PRINCIPAL,
    )
    
    btn_hora = ft.ElevatedButton(
        "⏰ Hora",
        icon=ft.Icons.ACCESS_TIME,
        on_click=abrir_reloj,
        bgcolor=COLOR_FONDO,
        color=COLOR_PRINCIPAL,
    )
    
    txt_fecha_seleccionada = ft.Text("📅 No seleccionada", size=12, color="#666")
    txt_hora_seleccionada = ft.Text("⏰ No seleccionada", size=12, color="#666")
    
    def actualizar_fecha(e):
        if fecha_limite.value:
            txt_fecha_seleccionada.value = f"📅 {fecha_limite.value.strftime('%d/%m/%Y')}"
        else:
            txt_fecha_seleccionada.value = "📅 No seleccionada"
        page.update()
    
    def actualizar_hora(e):
        if hora_limite.value:
            txt_hora_seleccionada.value = f"⏰ {hora_limite.value.strftime('%H:%M')}"
        else:
            txt_hora_seleccionada.value = "⏰ No seleccionada"
        page.update()
    
    fecha_limite.on_change = actualizar_fecha
    hora_limite.on_change = actualizar_hora
    
    def eliminar_tarea(id_tarea):
        success, msg = tarea_controller.eliminar_tarea(id_tarea)
        if success:
            cargar_tareas()
            mostrar_mensaje("✅ Tarea eliminada", "green")
        else:
            mostrar_mensaje(f"❌ {msg}", "red")
    
    def mostrar_mensaje(texto, color):
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=color)
        page.snack_bar.open = True
        page.update()
    
    def formatear_fecha(fecha):
        if not fecha:
            return "No disponible"
        if isinstance(fecha, datetime):
            return fecha.strftime('%d/%m/%Y')
        if isinstance(fecha, str):
            try:
                año, mes, dia = fecha.split('-')[0:3]
                return f"{dia}/{mes}/{año}"
            except:
                return fecha
        return str(fecha)
    
    def obtener_color_prioridad(prioridad):
        colores = {
            "alta": "#FF6B6B",
            "media": "#FFD93D", 
            "baja": "#6BCB77"
        }
        return colores.get(prioridad, COLOR_PRINCIPAL)
    
    def cargar_tareas():
        if user and 'id_usuario' in user:
            lista_tareas.controls.clear()
            tareas = tarea_controller.obtener_lista(user['id_usuario'])
            
            if not tareas:
                lista_tareas.controls.append(
                    ft.Container(
                        content=ft.Text("✨ ¡No hay tareas! Crea una nueva", 
                                      size=14, color="#666", italic=True),
                        alignment=ft.alignment.center,
                        padding=30
                    )
                )
            else:
                for t in tareas:
                    info_fecha = ""
                    if t.get('fecha_limite'):
                        info_fecha += f"📅 {formatear_fecha(t['fecha_limite'])}"
                    if t.get('hora_limite'):
                        hora = str(t['hora_limite'])[:5]
                        info_fecha += f" ⏰ {hora}"
                    
                    lista_tareas.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Row([
                                    ft.Container(
                                        width=5,
                                        height=60,
                                        bgcolor=obtener_color_prioridad(t.get('prioridad', 'media')),
                                        border_radius=3,
                                    ),
                                    ft.Column([
                                        ft.Text(t['titulo'], weight="bold", size=15),
                                        ft.Text(t.get('descripcion', 'Sin descripción')[:50], 
                                               size=12, color="#666"),
                                        ft.Row([
                                            ft.Text(f"🎯 {t.get('prioridad', 'media')}", size=11),
                                            ft.Text(f"📂 {t.get('clasificacion', 'personal')}", size=11),
                                            ft.Text(f"📌 {t.get('estado', 'pendiente')}", size=11),
                                        ], spacing=10),
                                        ft.Text(info_fecha, size=10, color="#999"),
                                    ], spacing=3, expand=True),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color="#FF6B6B",
                                        icon_size=20,
                                        on_click=lambda e, id_t=t['id_tarea']: eliminar_tarea(id_t)
                                    ),
                                ]),
                                padding=8,
                            ),
                            elevation=2,
                        )
                    )
            page.update()
    
    txt_titulo = ft.TextField(
        label="Título", 
        expand=True, 
        bgcolor=COLOR_FONDO, 
        border_radius=10,
        border_color=COLOR_PRINCIPAL
    )
    
    txt_descripcion = ft.TextField(
        label="Descripción", 
        expand=True, 
        multiline=True, 
        max_lines=2,
        bgcolor=COLOR_FONDO, 
        border_radius=10,
        border_color=COLOR_PRINCIPAL
    )
    
    prioridad_dropdown = ft.Dropdown(
        label="Prioridad",
        value="media",
        width=140,
        bgcolor=COLOR_FONDO,
        border_radius=10,
        options=[
            ft.dropdown.Option("alta", "🔴 Alta"),
            ft.dropdown.Option("media", "🟡 Media"),
            ft.dropdown.Option("baja", "🟢 Baja"),
        ]
    )
    
    clasificacion_dropdown = ft.Dropdown(
        label="Categoría",
        value="personal",
        width=140,
        bgcolor=COLOR_FONDO,
        border_radius=10,
        options=[
            ft.dropdown.Option("personal", "👤 Personal"),
            ft.dropdown.Option("trabajo", "💼 Trabajo"),
            ft.dropdown.Option("estudio", "📚 Estudio"),
            ft.dropdown.Option("hogar", "🏠 Hogar"),
            ft.dropdown.Option("salud", "🏥 Salud"),
            ft.dropdown.Option("otro", "📌 Otro"),
        ]
    )
    
    estado_dropdown = ft.Dropdown(
        label="Estado",
        value="pendiente",
        width=140,
        bgcolor=COLOR_FONDO,
        border_radius=10,
        options=[
            ft.dropdown.Option("pendiente", "🟡 Pendiente"),
            ft.dropdown.Option("en_progreso", "🔄 Progreso"),
            ft.dropdown.Option("completada", "✅ Completada"),
            ft.dropdown.Option("cancelada", "❌ Cancelada"),
        ]
    )
    
    def agregar_tarea(e):
        if not txt_titulo.value:
            mostrar_mensaje("⚠️ El título es obligatorio", "red")
            return
        
        val_fecha = fecha_limite.value.strftime('%Y-%m-%d') if fecha_limite.value else None
        val_hora = hora_limite.value.strftime('%H:%M:%S') if hora_limite.value else None

        success, msg = tarea_controller.guardar_nueva(
            user['id_usuario'],
            txt_titulo.value,
            txt_descripcion.value,
            prioridad_dropdown.value,
            clasificacion_dropdown.value,
            estado_dropdown.value,
            val_fecha,  
            val_hora   
        )
        
        if success:
            txt_titulo.value = ""
            txt_descripcion.value = ""
            prioridad_dropdown.value = "media"
            clasificacion_dropdown.value = "personal"
            estado_dropdown.value = "pendiente"
            fecha_limite.value = None
            hora_limite.value = None
            txt_fecha_seleccionada.value = "📅 No seleccionada"
            txt_hora_seleccionada.value = "⏰ No seleccionada"
            cargar_tareas()
            mostrar_mensaje("✅ Tarea guardada", "green")
        else:
            mostrar_mensaje(f"❌ {msg}", "red")
    
    def mostrar_perfil(e):
        dialogo = ft.AlertDialog(
            title=ft.Text("👤 Mi Perfil"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"📛 {user.get('nombre', '')} {user.get('apellido', '')}", size=16),
                    ft.Text(f"📧 {user.get('email', '')}", size=14),
                    ft.Text(f"📅 Registro: {formatear_fecha(user.get('fecha_registro'))}", size=12),
                ], spacing=10),
                width=280,
                padding=20
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: setattr(dialogo, 'open', False) or page.update())
            ],
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()
    
    nombre_usuario = user.get('nombre', 'Usuario') if user else 'Usuario'
    
    cargar_tareas()
    
    return ft.View(
        route="/dashboard",
        bgcolor=COLOR_PRINCIPAL,
        controls=[
            ft.AppBar(
                title=ft.Text(f"📋 SIGE - {nombre_usuario}", color="white", size=18),
                bgcolor=COLOR_PRINCIPAL,
                center_title=False,
                actions=[
                    ft.IconButton(ft.Icons.PERSON, on_click=mostrar_perfil, icon_color="white"),
                    ft.IconButton(ft.Icons.LOGOUT, on_click=lambda _: page.go("/"), icon_color="white"),
                ],
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("➕ Nueva Tarea", size=18, weight="bold"),
                                ft.Divider(),
                                ft.Row([txt_titulo, txt_descripcion], spacing=10),
                                ft.Row([prioridad_dropdown, clasificacion_dropdown, estado_dropdown], spacing=10),
                                ft.Row([btn_fecha, btn_hora, txt_fecha_seleccionada, txt_hora_seleccionada], spacing=10),
                                ft.ElevatedButton(
                                    "💾 Guardar Tarea", 
                                    on_click=agregar_tarea,
                                    bgcolor=COLOR_PRINCIPAL,
                                    color="white",
                                ),
                            ], spacing=12),
                            padding=20,
                        ),
                        elevation=3,
                    ),
                    
                    ft.Text("📋 Mis Tareas", size=16, weight="bold", color="white"),
                    ft.Container(height=5),
                    lista_tareas,
                    
                ], expand=True),
                padding=20,
                expand=True,
            ),
        ]
    )