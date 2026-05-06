import flet as ft

def LoginView(page: ft.Page, auth_controller):
    
    correo = ft.TextField(
        label="Correo electrónico",
        width=350,
        bgcolor="#F0F0F0", 
        border_radius=10,
    )

    contraseña = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        bgcolor="#F0F0F0",  
        border_radius=10,
    )
    
    mensaje = ft.Text("", color="red")

    def login_click(e):
        if not correo.value or not contraseña.value:
            mensaje.value = "Por favor, llene todos los campos"
            page.update()
            return
        
        user, msg = auth_controller.login(correo.value, contraseña.value)
        if user:
            page.user_data = user
            page.go("/dashboard")
        else:
            mensaje.value = msg
            page.update()

    iniciar_sesion = ft.ElevatedButton(
        "Iniciar sesión",
        width=200,
        on_click=login_click,
        bgcolor="#57689E",
        color=ft.Colors.WHITE,
    )
    
    btn_registro = ft.TextButton(
        "¿No tienes cuenta? Regístrate",
        on_click=lambda _: page.go("/register"),
        style=ft.ButtonStyle(color=ft.Colors.BLACK),  
    )
    
    contraseña.on_submit = login_click

    return ft.View(
        route="/",
        bgcolor="#57689E",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Column(
                [
                    ft.Text("Inicio de Sesión", size=30, weight="bold", color=ft.Colors.WHITE),
                    ft.Container(height=30),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                correo,
                                contraseña,
                                mensaje,
                                iniciar_sesion,
                                btn_registro,
                            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=30,
                            bgcolor=ft.Colors.WHITE, 
                        ),
                        elevation=5,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]
    )