import flet as ft
from datetime import datetime

def DashboardView(page, tarea_controller):
    user = getattr(page, "user_data", None)
    
    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=10)
    
    fecha_limite = ft.DatePicker()
    hora_limite = ft.TimePicker()
    
    page.overlay.append(fecha_limite)
    page.overlay.append(hora_limite)

    def abrir_calendario(e):
        fecha_limite.open = True
        page.update()

    def abrir_reloj(e):
        hora_limite.open = True
        page.update()
    
    txt_fecha = ft.Text("Fecha: No seleccionada", size=12)
    txt_hora = ft.Text("Hora: No seleccionada", size=12)
    
    def eliminar_tarea(id_tarea):
        tarea_controller.eliminar_tarea(id_tarea)
        cargar_tareas()
    
    def cargar_tareas():
        if user and 'id_usuario' in user:
            lista_tareas.controls.clear()
            tareas = tarea_controller.obtener_lista(user['id_usuario'])
            
            for t in tareas:
                fecha_info = ""
                if t.get('fecha_limite'):
                    fecha_info += f"\nFecha: {t['fecha_limite']}"
                if t.get('hora_limite'):
                    fecha_info += f" Hora: {t['hora_limite']}"
                
                # Color según prioridad
                color_prioridad = {
                    "alta": "#FF6B6B",
                    "media": "#FFD93D",
                    "baja": "#6BCB77"
                }.get(t.get('prioridad', 'media'), "#57689E")
                
                lista_tareas.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    width=5,
                                    height=60,
                                    bgcolor=color_prioridad,
                                    border_radius=5,
                                ),
                                ft.Column([
                                    ft.Text(t['titulo'], weight="bold", size=16),
                                    ft.Text(t.get('descripcion', 'Sin descripción'), size=12, color="#666666"),
                                    ft.Text(f"Estado: {t.get('estado', 'pendiente')}{fecha_info}", size=11, color="#888888"),
                                ], spacing=5, expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color="#FF6B6B",
                                    on_click=lambda e, id_t=t['id_tarea']: eliminar_tarea(id_t)
                                ),
                            ]),
                            padding=10,
                        ),
                        elevation=2,
                    )
                )
            page.update()
    
    txt_titulo = ft.TextField(label="Título", expand=True, bgcolor="#F0F0F0", border_radius=10)
    txt_descripcion = ft.TextField(label="Descripción", expand=True, multiline=True, bgcolor="#F0F0F0", border_radius=10)
    
    prioridad = ft.Dropdown(
        label="Prioridad", value="media", width=120, bgcolor="#F0F0F0",
        options=[
            ft.dropdown.Option("alta", "Alta"),
            ft.dropdown.Option("media", "Media"),
            ft.dropdown.Option("baja", "Baja")
        ]
    )
    
    clasificacion = ft.Dropdown(
        label="Clasificación", value="personal", width=130, bgcolor="#F0F0F0",
        options=[
            ft.dropdown.Option("personal", "Personal"),
            ft.dropdown.Option("trabajo", "Trabajo"),
            ft.dropdown.Option("estudio", "Estudio")
        ]
    )
    
    estado = ft.Dropdown(
        label="Estado", value="pendiente", width=130, bgcolor="#F0F0F0",
        options=[
            ft.dropdown.Option("pendiente", "Pendiente"),
            ft.dropdown.Option("en_progreso", "▶En progreso"),
            ft.dropdown.Option("completada", "Completada"),
            ft.dropdown.Option("cancelada", "Cancelada")
        ]
    )
    
    def agregar_tarea(e):
        if user and txt_titulo.value:
            fecha_val = fecha_limite.value.strftime('%Y-%m-%d') if fecha_limite.value else None
            hora_val = hora_limite.value.strftime('%H:%M:%S') if hora_limite.value else None
            
            tarea_controller.guardar_nueva(
                user['id_usuario'], txt_titulo.value, txt_descripcion.value,
                prioridad.value, clasificacion.value, estado.value, fecha_val, hora_val
            )
            txt_titulo.value = ""
            txt_descripcion.value = ""
            fecha_limite.value = None
            hora_limite.value = None
            txt_fecha.value = "Fecha: No seleccionada"
            txt_hora.value = "Hora: No seleccionada"
            cargar_tareas()
            page.update()
    
    def actualizar_fecha(e):
        if fecha_limite.value:
            txt_fecha.value = f"Fecha: {fecha_limite.value.strftime('%d/%m/%Y')}"
        else:
            txt_fecha.value = "Fecha: No seleccionada"
        page.update()
    
    def actualizar_hora(e):
        if hora_limite.value:
            txt_hora.value = f" Hora: {hora_limite.value.strftime('%H:%M')}"
        else:
            txt_hora.value = "Hora: No seleccionada"
        page.update()
    
    fecha_limite.on_change = actualizar_fecha
    hora_limite.on_change = actualizar_hora
    
    def mostrar_perfil(e):
        if user:
            dlg = ft.AlertDialog(
                title=ft.Text("Perfil"),
                content=ft.Text(f"{user.get('nombre', '')} {user.get('apellido', '')}\n{user.get('email', '')}")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
    
    cargar_tareas()
    
    return ft.View(
        route="/dashboard",
        bgcolor="#57689E",
        controls=[
            ft.AppBar(
                title=ft.Text(f"SIGE - {user.get('nombre', 'Usuario') if user else 'Usuario'}", color=ft.Colors.WHITE),
                bgcolor="#57689E",
                actions=[
                    ft.IconButton(ft.Icons.PERSON, on_click=mostrar_perfil, icon_color=ft.Colors.WHITE),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"), icon_color=ft.Colors.WHITE)
                ],
            ),
            ft.Container(
                content=ft.Column([
                    # Tarjeta para crear tarea - fondo blanco
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("Nueva Tarea", size=18, weight="bold"),
                                ft.Row([txt_titulo, txt_descripcion], spacing=10, wrap=True),
                                ft.Row([prioridad, clasificacion, estado], spacing=10, wrap=True),
                                ft.Row([
                                    ft.ElevatedButton("Fecha", on_click=abrir_calendario, bgcolor="#F0F0F0", color="#333333"),
                                    ft.ElevatedButton("Hora", on_click=abrir_reloj, bgcolor="#F0F0F0", color="#333333"),
                                    txt_fecha,
                                    txt_hora,
                                ], spacing=10, wrap=True),
                                ft.ElevatedButton("Guardar Tarea", on_click=agregar_tarea, bgcolor="#57689E", color=ft.Colors.WHITE),
                            ], spacing=15),
                            padding=20,
                            bgcolor=ft.Colors.WHITE,
                        ),
                        elevation=3,
                    ),
                    
                    ft.Container(height=10),
                    
                    ft.Text(" Mis Tareas", size=18, weight="bold", color=ft.Colors.WHITE),
                    ft.Container(height=10),
                    
                    ft.Container(
                        content=lista_tareas,
                        expand=True,
                    ),
                ], expand=True),
                padding=20,
                expand=True,
            ),
        ]
    )