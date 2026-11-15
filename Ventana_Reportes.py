import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class VentanaReportes:
    def __init__(self, ventana_padre, mi_cosecha, registro_trabajadores, gestor_excel):
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Balance y Reportes - AgroCuenta Café")
        self.ventana.geometry("680x500")
        self.ventana.resizable(False, False)

        self.mi_cosecha = mi_cosecha
        self.registro_trabajadores = registro_trabajadores
        self.gestor_excel = gestor_excel

        self.crear_widgets()
        self.actualizar_balance()

    def crear_widgets(self):
        # --- SECCIÓN 1: Balance General de la Cosecha ---
        frame_balance = tk.LabelFrame(self.ventana, text=f"Resumen de Cosecha: {self.mi_cosecha.descripcion}", padx=10, pady=10)
        frame_balance.pack(fill="x", padx=15, pady=10)

        self.lbl_ingresos = tk.Label(frame_balance, text="Total Ingresos: $0", font=("Arial", 10, "bold"), fg="green")
        self.lbl_ingresos.pack(side="left", padx=15)

        self.lbl_gastos = tk.Label(frame_balance, text="Total Gastos: $0", font=("Arial", 10, "bold"), fg="red")
        self.lbl_gastos.pack(side="left", padx=15)

        self.lbl_balance = tk.Label(frame_balance, text="Balance Actual: $0", font=("Arial", 11, "bold"))
        self.lbl_balance.pack(side="right", padx=15)

        # --- SECCIÓN 2: Buscador de Trabajador y Pesajes ---
        frame_busqueda = tk.LabelFrame(self.ventana, text="Consultar Pesajes por Trabajador", padx=10, pady=10)
        frame_busqueda.pack(fill="both", expand=True, padx=15, pady=5)

        fila_buscar = tk.Frame(frame_busqueda)
        fila_buscar.pack(fill="x", pady=5)

        tk.Label(fila_buscar, text="Nombre del trabajador:").pack(side="left", padx=5)
        self.entry_buscar = tk.Entry(fila_buscar, width=25)
        self.entry_buscar.pack(side="left", padx=5)
        self.entry_buscar.bind("<Return>", lambda event: self.buscar_trabajador())

        btn_buscar = tk.Button(fila_buscar, text="Buscar", command=self.buscar_trabajador)
        btn_buscar.pack(side="left", padx=5)

        btn_todos = tk.Button(fila_buscar, text="Ver Todos los Pesajes", command=self.cargar_todos_pesajes)
        btn_todos.pack(side="left", padx=5)

        # Tabla Treeview para mostrar pesajes
        columnas = ("trabajador", "fecha", "kilos")
        self.tabla_pesajes = ttk.Treeview(frame_busqueda, columns=columnas, show="headings", height=8)
        self.tabla_pesajes.heading("trabajador", text="Trabajador")
        self.tabla_pesajes.heading("fecha", text="Fecha")
        self.tabla_pesajes.heading("kilos", text="Kilos Recolectados")

        self.tabla_pesajes.column("trabajador", width=220)
        self.tabla_pesajes.column("fecha", width=150, anchor="center")
        self.tabla_pesajes.column("kilos", width=150, anchor="center")
        self.tabla_pesajes.pack(fill="both", expand=True, pady=5)

        self.lbl_total_kilos = tk.Label(frame_busqueda, text="Total kilos mostrados: 0 kg", font=("Arial", 9, "bold"))
        self.lbl_total_kilos.pack(anchor="e")

        # --- SECCIÓN 3: Botón Exportar con filedialog ---
        frame_acciones = tk.Frame(self.ventana, pady=10)
        frame_acciones.pack(fill="x", padx=15)

        btn_exportar = tk.Button(frame_acciones, text="Exportar Copia a Excel", bg="#2e7d32", fg="white", command=self.exportar_excel)
        btn_exportar.pack(side="right", padx=5)

        btn_cerrar = tk.Button(frame_acciones, text="Cerrar Ventana", command=self.ventana.destroy)
        btn_cerrar.pack(side="left", padx=5)

        self.cargar_todos_pesajes()

    def actualizar_balance(self):
        ingresos = self.mi_cosecha.total_ingreso()
        gastos = self.mi_cosecha.total_gasto()
        balance = ingresos - gastos

        self.lbl_ingresos.config(text=f"Total Ingresos: ${ingresos:,.0f}")
        self.lbl_gastos.config(text=f"Total Gastos: ${gastos:,.0f}")
        self.lbl_balance.config(text=f"Balance Actual: ${balance:,.0f}")

    def cargar_todos_pesajes(self):
        for item in self.tabla_pesajes.get_children():
            self.tabla_pesajes.delete(item)

        filas = self.gestor_excel.leer_filas("Pesajes")
        total_kilos = 0
        for fila in filas:
            self.tabla_pesajes.insert("", "end", values=fila)
            total_kilos += float(fila[2])

        self.lbl_total_kilos.config(text=f"Total kilos mostrados: {total_kilos} kg")

    def buscar_trabajador(self):
        nombre = self.entry_buscar.get().strip()
        if not nombre:
            messagebox.showwarning("Campo vacío", "Escribe el nombre del trabajador a buscar.", parent=self.ventana)
            return

        trabajador = self.registro_trabajadores.buscar_trabajador(nombre)
        if trabajador is None:
            messagebox.showinfo("Sin resultados", f"No se encontró al trabajador '{nombre}'.", parent=self.ventana)
            return

        for item in self.tabla_pesajes.get_children():
            self.tabla_pesajes.delete(item)

        filas = self.gestor_excel.leer_filas("Pesajes")
        total_kilos = 0
        for fila in filas:
            if str(fila[0]).lower() == trabajador.nombre.lower():
                self.tabla_pesajes.insert("", "end", values=fila)
                total_kilos += float(fila[2])

        self.lbl_total_kilos.config(text=f"Total kilos de {trabajador.nombre}: {total_kilos} kg")

    def exportar_excel(self):
        ruta = filedialog.asksaveasfilename(
            parent=self.ventana,
            title="Guardar reporte de AgroCuenta Café",
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")]
        )
        if ruta:
            try:
                self.gestor_excel.exportar_copia(ruta)
                messagebox.showinfo("Éxito", "Copia del archivo Excel exportada correctamente.", parent=self.ventana)
            except Exception as e:
                messagebox.showerror("Error al exportar", str(e), parent=self.ventana)