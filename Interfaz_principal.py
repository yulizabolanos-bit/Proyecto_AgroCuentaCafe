import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gasto import Gasto
from ingreso import Ingreso
from trabajador import Trabajador
from Ventana_Reportes import VentanaReportes


class InterfazPrincipal:
    def __init__(self, ventana_base, usuario_autorizado, mi_cosecha, registro_trabajadores, gestor_excel):
        self.ventana_base = ventana_base
        self.ventana_base.title(f"AgroCuenta Café - {mi_cosecha.descripcion}")
        self.ventana_base.geometry("940x650")
        self.ventana_base.resizable(True, True)

        self.usuario_autorizado = usuario_autorizado
        self.mi_cosecha = mi_cosecha
        self.registro_trabajadores = registro_trabajadores
        self.gestor_excel = gestor_excel

        self.tipo_labor_var = tk.StringVar(value="recoleccion")
        self.fila_gasto_seleccionada = None

        self.crear_barra_menu()
        self.crear_elementos_pantalla()
        self.cargar_datos_desde_excel()

    def formatear_numero(self, valor):
        numero = float(valor)
        return int(numero) if numero.is_integer() else numero

    def crear_barra_menu(self):
        barra_menu = tk.Menu(self.ventana_base)
        self.ventana_base.config(menu=barra_menu)

        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Guardar archivo Excel nuevo en mi computador...", command=self.guardar_excel_como)
        menu_archivo.add_command(label="Abrir mi archivo Excel existente...", command=self.abrir_archivo_excel)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana_base.quit)

        menu_registrar = tk.Menu(barra_menu, tearoff=0)
        menu_registrar.add_command(label="Gastos y Mano de Obra", command=lambda: self.cuaderno_pestanas.select(0))
        menu_registrar.add_command(label="Ventas de Café (Ingresos)",
                                   command=lambda: self.cuaderno_pestanas.select(1))

        menu_ver = tk.Menu(barra_menu, tearoff=0)
        menu_ver.add_command(label="Ver Balance y Ganancias / Pérdidas", command=self.abrir_ventana_reportes)

        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        barra_menu.add_cascade(label="Registrar", menu=menu_registrar)
        barra_menu.add_cascade(label="Ver Reportes", menu=menu_ver)

    def abrir_archivo_excel(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar mi archivo Excel de AgroCuenta Café",
            filetypes=[("Archivos de Excel", "*.xlsx")]
        )
        if ruta:
            try:
                self.gestor_excel.archivo = ruta
                self.gestor_excel.verificar_excel_cerrado()
                self.recargar_memoria_y_tablas()
                self.lbl_ruta_excel.config(text=f"Archivo activo: {self.gestor_excel.archivo}")
                messagebox.showinfo("Archivo cargado", f"Conectado correctamente a:\n{ruta}")
            except PermissionError as aviso:
                self.lbl_ruta_excel.config(text=f"Archivo activo: {self.gestor_excel.archivo}")
                messagebox.showwarning("Excel abierto", str(aviso))
            except Exception as error:
                messagebox.showerror("Error al abrir", str(error))

    def guardar_excel_como(self):
        ruta = filedialog.asksaveasfilename(
            title="Guardar archivo Excel en mi computador",
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")]
        )
        if ruta:
            try:
                self.gestor_excel.exportar_copia(ruta)
                self.gestor_excel.archivo = ruta
                self.lbl_ruta_excel.config(text=f"Archivo activo: {self.gestor_excel.archivo}")
                messagebox.showinfo("Archivo vinculado",
                                    f"Guardado y vinculado en:\n{ruta}\n\nAhora todos tus cambios se guardarán directamente aquí.")
            except Exception as error:
                messagebox.showerror("Error al guardar", str(error))

    def abrir_ventana_reportes(self):
        VentanaReportes(self.ventana_base, self.mi_cosecha, self.registro_trabajadores, self.gestor_excel)

    def crear_elementos_pantalla(self):
        encabezado = tk.Frame(self.ventana_base, bg="#2e7d32", pady=10, padx=15)
        encabezado.pack(fill="x")

        tk.Label(
            encabezado,
            text=f"AGROCUENTA CAFÉ  |  Cosecha: {self.mi_cosecha.descripcion}",
            font=("Arial", 13, "bold"),
            bg="#2e7d32",
            fg="white"
        ).pack(side="left")

        tk.Label(
            encabezado,
            text=f"Administrador: {self.usuario_autorizado.nombre}",
            font=("Arial", 10),
            bg="#2e7d32",
            fg="white"
        ).pack(side="right")

        barra_estado = tk.Frame(self.ventana_base, bg="#e8f5e9", pady=4, padx=15)
        barra_estado.pack(fill="x")

        self.lbl_ruta_excel = tk.Label(
            barra_estado,
            text=f"Archivo activo: {self.gestor_excel.archivo}",
            font=("Arial", 9, "italic"),
            bg="#e8f5e9",
            fg="#1b5e20"
        )
        self.lbl_ruta_excel.pack(side="left")

        self.cuaderno_pestanas = ttk.Notebook(self.ventana_base)
        self.cuaderno_pestanas.pack(fill="both", expand=True, padx=12, pady=10)

        self.pestana_gastos = tk.Frame(self.cuaderno_pestanas, padx=10, pady=10)
        self.pestana_ingresos = tk.Frame(self.cuaderno_pestanas, padx=10, pady=10)

        self.cuaderno_pestanas.add(self.pestana_gastos, text="  1. Registro de Gastos y Mano de Obra  ")
        self.cuaderno_pestanas.add(self.pestana_ingresos, text="  2. Registro de Ingresos (Ventas de Café)  ")

        self.construir_pestana_gastos()
        self.construir_pestana_ingresos()

    def construir_pestana_gastos(self):
        marco_general = tk.LabelFrame(self.pestana_gastos, text="1. Tipo de Gasto y Fecha", padx=10, pady=8)
        marco_general.pack(fill="x", pady=(0, 8))

        tk.Label(marco_general, text="Categoría:").grid(row=0, column=0, sticky="w", padx=5)
        self.combo_categoria = ttk.Combobox(marco_general, values=Gasto.categoria_gastos, state="readonly", width=24)
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=0, column=1, padx=5)
        self.combo_categoria.bind("<<ComboboxSelected>>", lambda evento: self.actualizar_campos_segun_categoria())

        tk.Label(marco_general, text="Fecha (AAAA-MM-DD):").grid(row=0, column=2, sticky="w", padx=15)
        self.caja_fecha_gasto = tk.Entry(marco_general, width=18)
        self.caja_fecha_gasto.insert(0, "2026-11-15")
        self.caja_fecha_gasto.grid(row=0, column=3, padx=5)

        self.marco_trabajador = tk.LabelFrame(self.pestana_gastos, text="2. Datos del Trabajador (Solo Mano de Obra)", padx=10, pady=8)
        self.marco_trabajador.pack(fill="x", pady=(0, 8))

        tk.Label(self.marco_trabajador, text="Nombre del trabajador:").pack(side="left", padx=5)
        self.caja_trabajador = tk.Entry(self.marco_trabajador, width=25)
        self.caja_trabajador.pack(side="left", padx=5)

        tk.Radiobutton(
            self.marco_trabajador,
            text="Recolección de café (Kilos)",
            variable=self.tipo_labor_var,
            value="recoleccion",
            command=self.actualizar_etiquetas_labor
        ).pack(side="left", padx=12)

        tk.Radiobutton(
            self.marco_trabajador,
            text="Otra labor (Jornales/Días)",
            variable=self.tipo_labor_var,
            value="otra_labor",
            command=self.actualizar_etiquetas_labor
        ).pack(side="left", padx=5)

        marco_detalle = tk.LabelFrame(self.pestana_gastos, text="3. Detalle y Valores del Gasto", padx=10, pady=8)
        marco_detalle.pack(fill="x", pady=(0, 8))

        self.lbl_desc_gasto = tk.Label(marco_detalle, text="Observación:")
        self.lbl_desc_gasto.grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.caja_desc_gasto = tk.Entry(marco_detalle, width=26)
        self.caja_desc_gasto.grid(row=0, column=1, padx=5, pady=4)

        self.lbl_cant_gasto = tk.Label(marco_detalle, text="Kilos recolectados:")
        self.lbl_cant_gasto.grid(row=0, column=2, sticky="w", padx=15, pady=4)
        self.caja_cant_gasto = tk.Entry(marco_detalle, width=18)
        self.caja_cant_gasto.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(marco_detalle, text="Unidad de medida:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.caja_unidad_gasto = tk.Entry(marco_detalle, width=26)
        self.caja_unidad_gasto.insert(0, "kg")
        self.caja_unidad_gasto.grid(row=1, column=1, padx=5, pady=4)

        self.lbl_valor_gasto = tk.Label(marco_detalle, text="Precio por kilo ($):")
        self.lbl_valor_gasto.grid(row=1, column=2, sticky="w", padx=15, pady=4)
        self.caja_valor_gasto = tk.Entry(marco_detalle, width=18)
        self.caja_valor_gasto.grid(row=1, column=3, padx=5, pady=4)

        marco_botones = tk.Frame(self.pestana_gastos)
        marco_botones.pack(pady=6)

        tk.Button(marco_botones, text="Registrar Gasto", bg="#2e7d32", fg="white", width=16, command=self.registrar_gasto).pack(side="left", padx=5)
        tk.Button(marco_botones, text="Actualizar Seleccionado", bg="#1565c0", fg="white", width=20, command=self.actualizar_gasto).pack(side="left", padx=5)
        tk.Button(marco_botones, text="Eliminar Seleccionado", bg="#c62828", fg="white", width=20, command=self.eliminar_gasto).pack(side="left", padx=5)
        tk.Button(marco_botones, text="Limpiar / Deseleccionar", width=20, command=self.limpiar_formulario_gasto).pack(side="left", padx=5)

        columnas_gastos = ("fecha", "descripcion", "cantidad", "unidad", "valor", "categoria", "total")
        self.tabla_gastos = ttk.Treeview(self.pestana_gastos, columns=columnas_gastos, show="headings", height=8)
        encabezados = ["Fecha", "Descripción", "Cantidad", "Unidad", "Valor Unit.", "Categoría", "Total ($)"]
        for col, texto in zip(columnas_gastos, encabezados):
            self.tabla_gastos.heading(col, text=texto)
            self.tabla_gastos.column(col, width=115, anchor="center")

        self.tabla_gastos.pack(fill="both", expand=True)
        self.tabla_gastos.bind("<Double-1>", lambda evento: self.seleccionar_fila_gasto())

        self.actualizar_campos_segun_categoria()

    def actualizar_campos_segun_categoria(self):
        categoria = self.combo_categoria.get()
        if categoria == "Mano de obra":
            self.marco_trabajador.pack(fill="x", pady=(0, 8), after=self.pestana_gastos.winfo_children()[0])
            self.actualizar_etiquetas_labor()
        else:
            self.marco_trabajador.pack_forget()
            self.lbl_desc_gasto.config(text="Descripción del gasto:")
            self.lbl_cant_gasto.config(text="Cantidad:")
            self.lbl_valor_gasto.config(text="Valor unitario ($):")
            self.caja_unidad_gasto.delete(0, tk.END)

    def actualizar_etiquetas_labor(self):
        if self.tipo_labor_var.get() == "recoleccion":
            self.lbl_desc_gasto.config(text="Observación (opcional):")
            self.lbl_cant_gasto.config(text="Kilos recolectados:")
            self.lbl_valor_gasto.config(text="Precio por kilo ($):")
            self.caja_unidad_gasto.delete(0, tk.END)
            self.caja_unidad_gasto.insert(0, "kg")
        else:
            self.lbl_desc_gasto.config(text="Nombre de la labor:")
            self.lbl_cant_gasto.config(text="Días trabajados:")
            self.lbl_valor_gasto.config(text="Precio del jornal ($):")
            self.caja_unidad_gasto.delete(0, tk.END)
            self.caja_unidad_gasto.insert(0, "días")

    def validar_solo_letras(self, texto):
        return bool(texto) and texto.replace(" ", "").isalpha()

    def registrar_gasto(self):
        categoria = self.combo_categoria.get()
        fecha = self.caja_fecha_gasto.get().strip()
        cant_texto = self.caja_cant_gasto.get().strip()
        valor_texto = self.caja_valor_gasto.get().strip()
        unidad_medida = self.caja_unidad_gasto.get().strip()

        if not fecha or not cant_texto or not valor_texto or not unidad_medida:
            messagebox.showwarning("Campos incompletos", "Por favor completa la fecha, cantidad, unidad y valor antes de registrar.")
            return

        try:
            cantidad = float(cant_texto)
            valor_unidad = float(valor_texto)
            if cantidad <= 0 or valor_unidad <= 0:
                messagebox.showwarning("Valores inválidos", "La cantidad y el valor unitario deben ser mayores a cero.")
                return
        except ValueError:
            messagebox.showerror("Error de formato", "La cantidad y el valor unitario deben ser valores numéricos.")
            return

        try:
            if categoria == "Mano de obra":
                nombre_trabajador = self.caja_trabajador.get().strip()
                if not nombre_trabajador:
                    messagebox.showwarning("Falta trabajador", "Por favor escribe el nombre del trabajador.")
                    return

                if not self.validar_solo_letras(nombre_trabajador):
                    messagebox.showerror("Nombre inválido", "El nombre del trabajador solo debe contener letras (no se permiten números).")
                    return

                trabajador_actual = self.registro_trabajadores.buscar_trabajador(nombre_trabajador)
                if trabajador_actual is None:
                    trabajador_actual = Trabajador(nombre_trabajador)
                    self.registro_trabajadores.agregar_trabajador(trabajador_actual)
                    self.gestor_excel.guardar_fila("Trabajadores", [trabajador_actual.nombre])

                observacion = self.caja_desc_gasto.get().strip()
                if observacion and not self.validar_solo_letras(observacion):
                    messagebox.showerror("Labor inválida",
                                     "El nombre de la labor u observación solo debe contener letras (no se permiten números).")
                    return

                if self.tipo_labor_var.get() == "recoleccion":
                    trabajador_actual.registrar_pesaje(fecha, cantidad)
                    self.gestor_excel.guardar_fila("Pesaje",
                                               [trabajador_actual.nombre, fecha, self.formatear_numero(cantidad)])
                    descripcion = f"Recolección café - {trabajador_actual.nombre}" + (
                    f" ({observacion})" if observacion else "")
                else:
                    labor = observacion or "Jornal general"
                    descripcion = f"{labor} - {trabajador_actual.nombre}"
            else:
                descripcion = self.caja_desc_gasto.get().strip()
                if not descripcion:
                    messagebox.showwarning("Falta descripción", "Por favor escribe la descripción del gasto.")
                    return

            nuevo_gasto = Gasto(fecha, descripcion, cantidad, unidad_medida, valor_unidad, categoria)
            self.mi_cosecha.agregar_gasto(nuevo_gasto)

            fila_excel = [
                fecha,
                descripcion,
                self.formatear_numero(cantidad),
                unidad_medida,
                self.formatear_numero(valor_unidad),
                categoria,
                self.formatear_numero(nuevo_gasto.calcular_total())
            ]
            self.gestor_excel.guardar_fila("Gastos", fila_excel)
            self.tabla_gastos.insert("", "end", values=fila_excel)

            messagebox.showinfo("Éxito", "Gasto registrado correctamente.")
            self.limpiar_formulario_gasto()

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def seleccionar_fila_gasto(self):
        seleccion = self.tabla_gastos.selection()
        if not seleccion:
            return
        item = seleccion[0]
        self.fila_gasto_seleccionada = self.tabla_gastos.index(item)
        valores = self.tabla_gastos.item(item, "values")

        self.combo_categoria.set(valores[5])
        self.actualizar_campos_segun_categoria()

        self.caja_fecha_gasto.delete(0, tk.END)
        self.caja_fecha_gasto.insert(0, valores[0])
        self.caja_desc_gasto.delete(0, tk.END)
        self.caja_desc_gasto.insert(0, valores[1])
        self.caja_cant_gasto.delete(0, tk.END)
        self.caja_cant_gasto.insert(0, self.formatear_numero(valores[2]))
        self.caja_unidad_gasto.delete(0, tk.END)
        self.caja_unidad_gasto.insert(0, valores[3])
        self.caja_valor_gasto.delete(0, tk.END)
        self.caja_valor_gasto.insert(0, self.formatear_numero(valores[4]))

        if valores[5] == "Mano de obra" and " - " in str(valores[1]):
            nombre_extraido = str(valores[1]).split(" - ")[1].split(" (")[0]
            self.caja_trabajador.delete(0, tk.END)
            self.caja_trabajador.insert(0, nombre_extraido)

    def actualizar_gasto(self):
        if self.fila_gasto_seleccionada is None:
            messagebox.showwarning("Sin selección", "Haz doble clic sobre una fila de la tabla para editarla.")
            return
        try:
            fecha = self.caja_fecha_gasto.get().strip()
            descripcion = self.caja_desc_gasto.get().strip()
            cantidad = float(self.caja_cant_gasto.get())
            unidad = self.caja_unidad_gasto.get().strip()
            valor = float(self.caja_valor_gasto.get())
            categoria = self.combo_categoria.get()

            if categoria == "Mano de obra":
                nombre_trab = self.caja_trabajador.get().strip()
                if nombre_trab and not self.validar_solo_letras(nombre_trab):
                    messagebox.showerror("Nombre inválido", "El nombre del trabajador solo debe contener letras.")
                    return

            total = cantidad * valor
            nuevos_datos = [
                fecha,
                descripcion,
                self.formatear_numero(cantidad),
                unidad,
                self.formatear_numero(valor),
                categoria,
                self.formatear_numero(total)
            ]
            self.gestor_excel.actualizar_fila_por_indice("Gastos", self.fila_gasto_seleccionada + 2, nuevos_datos)
            self.recargar_memoria_y_tablas()
            self.limpiar_formulario_gasto()
            messagebox.showinfo("Actualizado", "El gasto se actualizó correctamente en Excel.")
        except Exception as error:
            messagebox.showerror("Error al actualizar", str(error))

    def eliminar_gasto(self):
        seleccion = self.tabla_gastos.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona una fila de la tabla para eliminar.")
            return
        valores = self.tabla_gastos.item(seleccion[0], "values")
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este gasto permanentemente?"):
            try:
                self.gestor_excel.eliminar_gasto_y_pesaje_exacto(
                    valores[0], valores[1], valores[2], valores[5]
                )
                self.recargar_memoria_y_tablas()
                self.limpiar_formulario_gasto()
            except Exception as error:
                messagebox.showerror("Error al eliminar", str(error))
    def limpiar_formulario_gasto(self):
        self.fila_gasto_seleccionada = None
        for item in self.tabla_gastos.selection():
            self.tabla_gastos.selection_remove(item)

        self.caja_trabajador.delete(0, tk.END)
        self.caja_desc_gasto.delete(0, tk.END)
        self.caja_cant_gasto.delete(0, tk.END)
        self.caja_valor_gasto.delete(0, tk.END)

    # ==========================================================
    # 4. PESTAÑA 2: INGRESOS (VENTAS DE CAFÉ)
    # ==========================================================
    def construir_pestana_ingresos(self):
        marco_ingreso = tk.LabelFrame(self.pestana_ingresos, text="Registrar Venta de Café o Pasilla", padx=10, pady=10)
        marco_ingreso.pack(fill="x", pady=(0, 10))

        tk.Label(marco_ingreso, text="Fecha (AAAA-MM-DD):").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.caja_fecha_ingreso = tk.Entry(marco_ingreso, width=20)
        self.caja_fecha_ingreso.insert(0, "2026-11-15")
        self.caja_fecha_ingreso.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(marco_ingreso, text="Tipo (Café / Pasilla):").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.caja_desc_ingreso = tk.Entry(marco_ingreso, width=22)
        self.caja_desc_ingreso.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(marco_ingreso, text="Kilos vendidos:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.caja_kilos_ingreso = tk.Entry(marco_ingreso, width=20)
        self.caja_kilos_ingreso.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(marco_ingreso, text="Precio por kilo ($):").grid(row=1, column=2, sticky="w", padx=5, pady=4)
        self.caja_precio_ingreso = tk.Entry(marco_ingreso, width=22)
        self.caja_precio_ingreso.grid(row=1, column=3, padx=5, pady=4)

        tk.Label(marco_ingreso, text="Comprador / Cooperativa:").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.caja_comprador = tk.Entry(marco_ingreso, width=20)
        self.caja_comprador.grid(row=2, column=1, padx=5, pady=4)

        marco_btn_ing = tk.Frame(marco_ingreso)
        marco_btn_ing.grid(row=3, column=0, columnspan=4, pady=8)

        tk.Button(marco_btn_ing, text="Registrar Venta", bg="#2e7d32", fg="white", width=18, command=self.registrar_ingreso).pack(side="left", padx=5)
        tk.Button(marco_btn_ing, text="Eliminar Seleccionada", bg="#c62828", fg="white", width=20, command=self.eliminar_ingreso).pack(side="left", padx=5)
        tk.Button(marco_btn_ing, text="Limpiar / Deseleccionar", width=20, command=self.limpiar_formulario_ingreso).pack(side="left", padx=5)

        columnas_ing = ("fecha", "descripcion", "cantidad", "unidad", "valor", "comprador", "total")
        self.tabla_ingresos = ttk.Treeview(self.pestana_ingresos, columns=columnas_ing, show="headings", height=10)
        encabezados_ing = ["Fecha", "Tipo Café", "Kilos", "Unidad", "Precio/Kg ($)", "Comprador", "Total ($)"]
        for col, texto in zip(columnas_ing, encabezados_ing):
            self.tabla_ingresos.heading(col, text=texto)
            self.tabla_ingresos.column(col, width=115, anchor="center")

        self.tabla_ingresos.pack(fill="both", expand=True)

    def registrar_ingreso(self):
        fecha = self.caja_fecha_ingreso.get().strip()
        descripcion = self.caja_desc_ingreso.get().strip()
        kilos_texto = self.caja_kilos_ingreso.get().strip()
        precio_texto = self.caja_precio_ingreso.get().strip()
        comprador = self.caja_comprador.get().strip()

        if not fecha or not descripcion or not kilos_texto or not precio_texto or not comprador:
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos de la venta.")
            return

        try:
            kilos = float(kilos_texto)
            precio = float(precio_texto)
        except ValueError:
            messagebox.showerror("Error de formato", "Los kilos y el precio deben ser valores numéricos.")
            return

        nuevo_ingreso = Ingreso(fecha, descripcion, kilos, "kg", precio, comprador)
        if not nuevo_ingreso.validar_venta():
            messagebox.showwarning("Venta inválida", "Los kilos y el precio deben ser mayores a cero.")
            return

        self.mi_cosecha.agregar_ingreso(nuevo_ingreso)
        fila_excel = [
            fecha,
            descripcion,
            self.formatear_numero(kilos),
            "kg",
            self.formatear_numero(precio),
            comprador,
            self.formatear_numero(nuevo_ingreso.calcular_total())
        ]
        self.gestor_excel.guardar_fila("Ingreso", fila_excel)
        self.tabla_ingresos.insert("", "end", values=fila_excel)

        messagebox.showinfo("Venta registrada", f"Venta registrada por ${nuevo_ingreso.calcular_total():,.0f}")
        self.limpiar_formulario_ingreso()

    def eliminar_ingreso(self):
        seleccion = self.tabla_ingresos.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona una venta de la tabla para eliminar.")
            return
        indice = self.tabla_ingresos.index(seleccion[0])
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar esta venta permanentemente?"):
            try:
                self.gestor_excel.eliminar_fila_por_indice("Ingreso", indice + 2)
                self.recargar_memoria_y_tablas()
            except Exception as error:
                messagebox.showerror("Error", str(error))

    def limpiar_formulario_ingreso(self):
        for item in self.tabla_ingresos.selection():
            self.tabla_ingresos.selection_remove(item)
        self.caja_desc_ingreso.delete(0, tk.END)
        self.caja_kilos_ingreso.delete(0, tk.END)
        self.caja_precio_ingreso.delete(0, tk.END)
        self.caja_comprador.delete(0, tk.END)

    # ==========================================================
    # 5. SINCRONIZACIÓN CON EXCEL
    # ==========================================================
    def cargar_datos_desde_excel(self):
        for fila in self.gestor_excel.leer_filas("Trabajadores"):
            if fila and fila[0]:
                if self.registro_trabajadores.buscar_trabajador(str(fila[0])) is None:
                    self.registro_trabajadores.agregar_trabajador(Trabajador(str(fila[0])))

        for fila in self.gestor_excel.leer_filas("Pesaje"):
            if fila and len(fila) >= 3:
                trab = self.registro_trabajadores.buscar_trabajador(str(fila[0]))
                if trab:
                    trab.registrar_pesaje(str(fila[1]), float(fila[2]))

        for fila in self.gestor_excel.leer_filas("Gastos"):
            if fila and len(fila) >= 7:
                gasto = Gasto(str(fila[0]), str(fila[1]), float(fila[2]), str(fila[3]), float(fila[4]), str(fila[5]))
                self.mi_cosecha.agregar_gasto(gasto)
                fila_limpia = [
                    fila[0],
                    fila[1],
                    self.formatear_numero(fila[2]),
                    fila[3],
                    self.formatear_numero(fila[4]),
                    fila[5],
                    self.formatear_numero(fila[6])
                ]
                self.tabla_gastos.insert("", "end", values=fila_limpia)

        for fila in self.gestor_excel.leer_filas("Ingreso"):
            if fila and len(fila) >= 7:
                ingreso = Ingreso(str(fila[0]), str(fila[1]), float(fila[2]), str(fila[3]), float(fila[4]), str(fila[5]))
                self.mi_cosecha.agregar_ingreso(ingreso)
                fila_limpia = [
                    fila[0],
                    fila[1],
                    self.formatear_numero(fila[2]),
                    fila[3],
                    self.formatear_numero(fila[4]),
                    fila[5],
                    self.formatear_numero(fila[6])
                ]
                self.tabla_ingresos.insert("", "end", values=fila_limpia)

    def recargar_memoria_y_tablas(self):
        self.mi_cosecha.lista_gasto.clear()
        self.mi_cosecha.lista_ingreso.clear()
        for item in self.tabla_gastos.get_children():
            self.tabla_gastos.delete(item)
        for item in self.tabla_ingresos.get_children():
            self.tabla_ingresos.delete(item)
        self.cargar_datos_desde_excel()