import flet as ft

def UserView(page, auth_controller):
    user = getattr(page, "user_data", None)

    return ft.View(
        route="/perfil",
        bgcolor="#57689E",
        controls=[
            ft.AppBar(
                title=ft.Text("Mi Perfil", color=ft.Colors.WHITE),
                bgcolor="#57689E",
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/dashboard"), icon_color=ft.Colors.WHITE),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"), icon_color=ft.Colors.WHITE)
                ],
            ),
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Nombre: {user.get('nombre', '')} {user.get('apellido', '')}", size=18),
                            ft.Text(f"Email: {user.get('email', '')}", size=18),
                            ft.Text(f"Registro: {user.get('fecha_registro', '')}"),
                            ft.Text(f"Último acceso: {user.get('ultimo_acceso', '')}"),
                        ], spacing=15),
                        padding=30,
                    )
                ),
                alignment=ft.alignment.center,
                expand=True,
            ),
        ]
    )