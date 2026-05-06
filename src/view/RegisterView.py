import flet as ft
import re
from models.schemasModel import UsuarioSchema  

def RegisterView(page: ft.Page, auth_controller):
    
    nombre = ft.TextField(label="Nombre(s)", width=350, bgcolor="#F0F0F0", border_radius=10)
    apellido = ft.TextField(label="Apellidos", width=350, bgcolor="#F0F0F0", border_radius=10)
    email = ft.TextField(label="Correo electrónico", width=350, bgcolor="#F0F0F0", border_radius=10)
    password = ft.TextField(label="Contraseña", password=True, width=350, bgcolor="#F0F0F0", border_radius=10)
    confirm_password = ft.TextField(label="Confirmar contraseña", password=True, width=350, bgcolor="#F0F0F0", border_radius=10)
    
    mensaje = ft.Text("", color="red")
    
    def registrar_click(e):
        if not all([nombre.value, apellido.value, email.value, password.value, confirm_password.value]):
            mensaje.value = "Todos los campos son obligatorios"
            page.update()
            return
        
        if password.value != confirm_password.value:
            mensaje.value = "Las contraseñas no coinciden"
            page.update()
            return
        
        if len(password.value) < 6:
            mensaje.value = "La contraseña debe tener al menos 6 caracteres"
            page.update()
            return
        
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.value):
            mensaje.value = "Correo electrónico inválido"
            page.update()
            return
        
        usuario_data = UsuarioSchema(
            nombre=nombre.value,
            apellido=apellido.value,
            email=email.value,
            password=password.value
        )
        
        exito, msg = auth_controller.registrar(usuario_data)
        
        if exito:
            page.go("/")
        else:
            mensaje.value = msg
            page.update()
    
    def ir_login(e):
        page.go("/")
    
    btn_registrar = ft.ElevatedButton(
        "Registrarse",
        width=200,
        on_click=registrar_click,
        bgcolor="#57689E",
        color=ft.Colors.WHITE,
    )
    
    btn_login = ft.TextButton(
        "¿Ya tienes cuenta? Inicia sesión",
        on_click=ir_login,
        style=ft.ButtonStyle(color=ft.Colors.BLACK),  # Texto negro
    )

    return ft.View(
        route="/register",
        bgcolor="#57689E",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Column(
                [
                    ft.Text("Crear Cuenta", size=30, weight="bold", color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                nombre,
                                apellido,
                                email,
                                password,
                                confirm_password,
                                mensaje,
                                btn_registrar,
                                btn_login,
                            ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=30,
                            bgcolor=ft.Colors.WHITE,  # Fondo blanco de la tarjeta
                        ),
                        elevation=5,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]
    )