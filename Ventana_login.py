import tkinter as tk
from tkinter import messagebox
from interfaz_principal import InterfazPrincipal


class VentanaLogin:
    def __init__(self, ventana_base, usuario_autorizado, mi_cosecha, registro_trabajadores, gestor_excel):
        self.ventana_base = ventana_base
        self.ventana_base.title("Inicio de Sesión - AgroCuenta Café")
        self.ventana_base.geometry("400x330")
        self.ventana_base.resizable(False, False)

        self.usuario_autorizado = usuario_autorizado
        self.mi_cosecha = mi_cosecha
        self.registro_trabajadores = registro_trabajadores
        self.gestor_excel = gestor_excel

        self.crear_elementos_pantalla()

    def crear_elementos_pantalla(self):
        contenedor_principal = tk.Frame(self.ventana_base, padx=25, pady=20)
        contenedor_principal.pack(fill="both", expand=True)

        tk.Label(contenedor_principal, text="AGROCUENTA CAFÉ", font=("Arial", 15, "bold"), fg="#2e7d32").pack(pady=(0, 5))
        tk.Label(contenedor_principal, text="Control de Cosecha, Trabajadores y Finanzas", font=("Arial", 9)).pack(pady=(0, 15))

        # Campo Usuario
        tk.Label(contenedor_principal, text="Nombre de usuario:").pack(anchor="w")
        self.caja_usuario = tk.Entry(contenedor_principal, width=35)
        self.caja_usuario.pack(pady=(2, 10))
        self.caja_usuario.focus()

        # Campo Clave
        tk.Label(contenedor_principal, text="Clave de acceso:").pack(anchor="w")
        self.caja_clave = tk.Entry(contenedor_principal, width=35, show="*")
        self.caja_clave.pack(pady=(2, 10))

        # Campo Periodo de Cosecha
        tk.Label(contenedor_principal, text="Periodo o nombre de la cosecha:").pack(anchor="w")
        self.caja_cosecha = tk.Entry(contenedor_principal, width=35)
        self.caja_cosecha.insert(0, "Cosecha Principal 2026")
        self.caja_cosecha.pack(pady=(2, 15))

        # Permitir iniciar sesión presionando Enter
        self.caja_clave.bind("<Return>", lambda evento: self.validar_ingreso())
        self.caja_cosecha.bind("<Return>", lambda evento: self.validar_ingreso())

        boton_ingresar = tk.Button(
            contenedor_principal,
            text="Ingresar al Sistema",
            bg="#2e7d32",
            fg="white",
            font=("Arial", 10, "bold"),
            width=22,
            command=self.validar_ingreso
        )
        boton_ingresar.pack(pady=5)

    def validar_ingreso(self):
        nombre = self.caja_usuario.get().strip()
        clave = self.caja_clave.get().strip()
        periodo = self.caja_cosecha.get().strip()

        if not nombre or not clave or not periodo:
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos para ingresar.")
            return

        if self.usuario_autorizado.verificar_credenciales(nombre, clave):
            self.mi_cosecha.descripcion = periodo
            messagebox.showinfo("Acceso concedido", f"¡Bienvenido/a {self.usuario_autorizado.nombre}!")

            # Limpia los elementos del login y carga la interfaz principal en la misma ventana
            for elemento in self.ventana_base.winfo_children():
                elemento.destroy()

            InterfazPrincipal(
                self.ventana_base,
                self.usuario_autorizado,
                self.mi_cosecha,
                self.registro_trabajadores,
                self.gestor_excel
            )
        else:
            messagebox.showerror("Acceso denegado", "El nombre de usuario o la clave son incorrectos.")
            self.caja_clave.delete(0, tk.END)