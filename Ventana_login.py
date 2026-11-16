import tkinter as tk
from tkinter import messagebox
from Interfaz_principal import InterfazPrincipal


class VentanaLogin:
    def __init__(self, ventana_base, usuario_autorizado, mi_cosecha, registro_trabajadores, gestor_excel):
        self.ventana_base = ventana_base
        self.ventana_base.title("Inicio de Sesión - AgroCuenta Café")
        self.ventana_base.geometry("420x320")
        self.ventana_base.resizable(False, False)

        self.usuario_autorizado = usuario_autorizado
        self.mi_cosecha = mi_cosecha
        self.registro_trabajadores = registro_trabajadores
        self.gestor_excel = gestor_excel

        self.mostrar_clave_var = tk.BooleanVar(value=False)

        self.crear_elementos_pantalla()

    def crear_elementos_pantalla(self):
        encabezado = tk.Frame(self.ventana_base, bg="#2e7d32", pady=14)
        encabezado.pack(fill="x")

        tk.Label(
            encabezado,
            text="AGROCUENTA CAFÉ",
            font=("Arial", 15, "bold"),
            bg="#2e7d32",
            fg="white"
        ).pack()

        tk.Label(
            encabezado,
            text="Control Financiero de Finca Cafetera",
            font=("Arial", 9),
            bg="#2e7d32",
            fg="#e8f5e9"
        ).pack()

        marco_form = tk.Frame(self.ventana_base, padx=30, pady=20)
        marco_form.pack(fill="both", expand=True)

        tk.Label(marco_form, text="Usuario:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.caja_usuario = tk.Entry(marco_form, font=("Arial", 10), width=35)
        self.caja_usuario.pack(pady=(2, 10), fill="x")
        self.caja_usuario.focus()

        tk.Label(marco_form, text="Contraseña:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.caja_clave = tk.Entry(marco_form, font=("Arial", 10), width=35, show="*")
        self.caja_clave.pack(pady=(2, 4), fill="x")
        self.caja_clave.bind("<Return>", lambda evento: self.iniciar_sesion())

        tk.Checkbutton(
            marco_form,
            text="Mostrar contraseña",
            variable=self.mostrar_clave_var,
            command=self.alternar_visibilidad_clave,
            font=("Arial", 9)
        ).pack(anchor="w", pady=(0, 12))

        tk.Button(
            marco_form,
            text="Ingresar al Sistema",
            bg="#2e7d32",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=6,
            command=self.iniciar_sesion
        ).pack(fill="x")

    def alternar_visibilidad_clave(self):
        if self.mostrar_clave_var.get():
            self.caja_clave.config(show="")
        else:
            self.caja_clave.config(show="*")

    def iniciar_sesion(self):
        nombre = self.caja_usuario.get().strip()
        clave = self.caja_clave.get().strip()

        if not nombre or not clave:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa tu usuario y contraseña.")
            return

        if self.usuario_autorizado.verificar_credenciales(nombre, clave):
            for widget in self.ventana_base.winfo_children():
                widget.destroy()
            InterfazPrincipal(
                self.ventana_base,
                self.usuario_autorizado,
                self.mi_cosecha,
                self.registro_trabajadores,
                self.gestor_excel
            )
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos. Marca 'Mostrar contraseña' para verificar.")
            self.caja_clave.delete(0, tk.END)