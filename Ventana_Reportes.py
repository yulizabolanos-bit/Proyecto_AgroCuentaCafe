import tkinter as tk
from tkinter import ttk, messagebox


class VentanaReportes:
    def __init__(self, ventana_padre, mi_cosecha, registro_trabajadores, gestor_excel):
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Balance Financiero y Liquidación de Trabajadores - AgroCuenta Café")
        self.ventana.geometry("820x690")
        self.ventana.resizable(True, True)

        self.mi_cosecha = mi_cosecha
        self.registro_trabajadores = registro_trabajadores
        self.gestor_excel = gestor_excel

        self.crear_elementos_pantalla()
        self.consultar_balance_total()

    def formatear_numero(self, valor):
        numero = float(valor)
        return int(numero) if numero.is_integer() else numero

    def crear_elementos_pantalla(self):
        # --- SECCIÓN 1: Filtro por Rango de Fechas ---
        marco_fechas = tk.LabelFrame(self.ventana, text=f"Consultar Balance de: {self.mi_cosecha.descripcion}", padx=10, pady=8)
        marco_fechas.pack(fill="x", padx=15, pady=(10, 5))

        tk.Label(marco_fechas, text="Desde (AAAA-MM-DD):").pack(side="left", padx=5)
        self.caja_fecha_inicio = tk.Entry(marco_fechas, width=13)
        self.caja_fecha_inicio.insert(0, "2026-01-01")
        self.caja_fecha_inicio.pack(side="left", padx=5)

        tk.Label(marco_fechas, text="Hasta (AAAA-MM-DD):").pack(side="left", padx=5)
        self.caja_fecha_fin = tk.Entry(marco_fechas, width=13)
        self.caja_fecha_fin.insert(0, "2026-12-31")
        self.caja_fecha_fin.pack(side="left", padx=5)

        tk.Button(marco_fechas, text="Consultar Fechas", bg="#1565c0", fg="white", command=self.consultar_por_fechas).pack(side="left", padx=6)
        tk.Button(marco_fechas, text="Balance Total del Año", bg="#2e7d32", fg="white", command=self.consultar_balance_total).pack(side="left", padx=4)

        # --- SECCIÓN 2: Resultado Financiero (Inversión, Ventas, Ganancia o Pérdida) ---
        marco_resultado = tk.LabelFrame(self.ventana, text="Resultado Financiero General de la Finca", padx=12, pady=8)
        marco_resultado.pack(fill="x", padx=15, pady=5)

        self.texto_diagnostico = tk.Text(marco_resultado, height=6, font=("Arial", 10), bg="#f9fbe7", relief="flat", wrap="word")
        self.texto_diagnostico.pack(fill="x")
        self.texto_diagnostico.config(state="disabled")

        self.lbl_veredicto_final = tk.Label(
            marco_resultado,
            text="RESULTADO: $0",
            font=("Arial", 11, "bold"),
            pady=6,
            relief="groove"
        )
        self.lbl_veredicto_final.pack(fill="x", pady=(6, 0))

        # --- SECCIÓN 3: Buscador y Liquidación de Trabajadores ---
        marco_busqueda = tk.LabelFrame(self.ventana, text="Control de Pagos y Liquidación de Trabajadores", padx=10, pady=8)
        marco_busqueda.pack(fill="both", expand=True, padx=15, pady=5)

        fila_buscar = tk.Frame(marco_busqueda)
        fila_buscar.pack(fill="x", pady=5)

        tk.Label(fila_buscar, text="Nombre del trabajador:").pack(side="left", padx=5)
        self.caja_buscar = tk.Entry(fila_buscar, width=22)
        self.caja_buscar.pack(side="left", padx=5)
        self.caja_buscar.bind("<Return>", lambda evento: self.buscar_trabajador())

        tk.Button(fila_buscar, text="Consultar Pendiente", bg="#1565c0", fg="white", command=self.buscar_trabajador).pack(side="left", padx=4)
        tk.Button(fila_buscar, text="Liquidar / Pagar Pendiente", bg="#2e7d32", fg="white", font=("Arial", 9, "bold"), command=self.liquidar_trabajador).pack(side="left", padx=4)
        tk.Button(fila_buscar, text="Ver Todos", command=self.cargar_todos_trabajos).pack(side="left", padx=4)

        columnas = ("fecha", "detalle", "cantidad", "unidad", "valor_unit", "total_pagar", "estado")
        self.tabla_pesajes = ttk.Treeview(marco_busqueda, columns=columnas, show="headings", height=6)
        self.tabla_pesajes.heading("fecha", text="Fecha")
        self.tabla_pesajes.heading("detalle", text="Labor / Trabajador")
        self.tabla_pesajes.heading("cantidad", text="Cant.")
        self.tabla_pesajes.heading("unidad", text="Unidad")
        self.tabla_pesajes.heading("valor_unit", text="Valor Unit.")
        self.tabla_pesajes.heading("total_pagar", text="Subtotal")
        self.tabla_pesajes.heading("estado", text="Estado de Pago")

        self.tabla_pesajes.column("fecha", width=85, anchor="center")
        self.tabla_pesajes.column("detalle", width=210)
        self.tabla_pesajes.column("cantidad", width=60, anchor="center")
        self.tabla_pesajes.column("unidad", width=60, anchor="center")
        self.tabla_pesajes.column("valor_unit", width=90, anchor="center")
        self.tabla_pesajes.column("total_pagar", width=95, anchor="center")
        self.tabla_pesajes.column("estado", width=155, anchor="center")
        self.tabla_pesajes.pack(fill="both", expand=True, pady=5)

        self.lbl_resumen_trabajador = tk.Label(
            marco_busqueda,
            text="Pendiente por pagar: $0",
            font=("Arial", 10, "bold"),
            fg="#1b5e20"
        )
        self.lbl_resumen_trabajador.pack(anchor="e", pady=2)

        # --- SECCIÓN 4: Cerrar ---
        marco_acciones = tk.Frame(self.ventana, pady=6)
        marco_acciones.pack(fill="x", padx=15)

        tk.Button(marco_acciones, text="Cerrar Ventana", command=self.ventana.destroy).pack(side="right", padx=5)

        self.cargar_todos_trabajos()

    def mostrar_diagnostico(self, datos, titulo_periodo):
        invertido = datos["invertido"]
        vendido = datos["vendido"]
        kilos = self.formatear_numero(datos["kilos_vendidos"])
        balance = datos["balance"]
        por_categoria = datos["por_categoria"]

        if por_categoria:
            partes = [f"   • {cat}: ${monto:,.0f}" for cat, monto in por_categoria.items()]
            desglose = "Desglose de lo que invertiste en tu finca:\n" + "\n".join(partes)
        else:
            desglose = "Aún no hay gastos registrados en este periodo."

        mensaje = (
            f"Periodo consultado: {titulo_periodo}\n"
            f"• Total café vendido: {kilos:,} kg   |   Total ingresos por ventas: ${vendido:,.0f}\n"
            f"• Total invertido / gastado en la finca: ${invertido:,.0f}\n"
            f"{desglose}"
        )

        self.texto_diagnostico.config(state="normal")
        self.texto_diagnostico.delete("1.0", tk.END)
        self.texto_diagnostico.insert("1.0", mensaje)
        self.texto_diagnostico.config(state="disabled")

        if balance > 0:
            estado_texto = "GANANCIA"
            self.lbl_veredicto_final.config(
                text=f"¡TUVISTE UNA GANANCIA DE ${balance:,.0f}! (Ingresos ${vendido:,.0f} - Inversión ${invertido:,.0f})",
                bg="#c8e6c9",
                fg="#1b5e20"
            )
        elif balance < 0:
            estado_texto = "PÉRDIDA"
            self.lbl_veredicto_final.config(
                text=f"TUVISTE UNA PÉRDIDA DE ${abs(balance):,.0f} (Ingresos ${vendido:,.0f} - Inversión ${invertido:,.0f})",
                bg="#ffcdd2",
                fg="#b71c1c"
            )
        else:
            estado_texto = "EQUILIBRIO"
            self.lbl_veredicto_final.config(
                text=f"PUNTO DE EQUILIBRIO: $0 ganancia / $0 pérdida (Ingresos ${vendido:,.0f} = Inversión ${invertido:,.0f})",
                bg="#fff9c4",
                fg="#f57f17"
            )

        # Se guarda automáticamente en la hoja 'Balance' de Excel sin botones extra
        fila_balance = [
            titulo_periodo,
            kilos,
            self.formatear_numero(vendido),
            self.formatear_numero(invertido),
            self.formatear_numero(balance),
            estado_texto
        ]
        self.gestor_excel.actualizar_hoja_balance(fila_balance)

    def consultar_balance_total(self):
        datos = self.mi_cosecha.generar_resumen_financiero()
        self.mostrar_diagnostico(datos, f"Todo el año ({self.mi_cosecha.descripcion})")

    def consultar_por_fechas(self):
        inicio = self.caja_fecha_inicio.get().strip()
        fin = self.caja_fecha_fin.get().strip()
        if not inicio or not fin:
            messagebox.showwarning("Fechas requeridas", "Escribe ambas fechas en formato AAAA-MM-DD.", parent=self.ventana)
            return
        datos = self.mi_cosecha.generar_resumen_financiero(inicio, fin)
        self.mostrar_diagnostico(datos, f"Desde {inicio} hasta {fin}")

    def extraer_nombre_y_estado(self, descripcion):
        desc = str(descripcion)
        esta_pagado = "[PAGADO" in desc
        estado_texto = "PAGADO" if esta_pagado else "Pendiente de pago"
        if esta_pagado:
            inicio_tag = desc.find("[PAGADO")
            fin_tag = desc.find("]", inicio_tag)
            if fin_tag != -1:
                estado_texto = desc[inicio_tag + 1:fin_tag]

        desc_limpia = desc.split("[PAGADO")[0].strip()
        nombre = ""
        if " - " in desc_limpia:
            nombre = desc_limpia.split(" - ")[1].split(" (")[0].strip()
        return nombre, desc_limpia, esta_pagado, estado_texto

    def cargar_todos_trabajos(self):
        for item in self.tabla_pesajes.get_children():
            self.tabla_pesajes.delete(item)

        total_pendiente = 0
        total_pagado = 0

        for g in self.mi_cosecha.lista_gasto:
            if g.categoria == "Mano de obra":
                _, desc_limpia, esta_pagado, estado_texto = self.extraer_nombre_y_estado(g.descripcion)
                subtotal = g.calcular_total()
                self.tabla_pesajes.insert("", "end", values=(
                    g.fecha,
                    desc_limpia,
                    self.formatear_numero(g.cantidad),
                    g.unidad_medida,
                    f"${g.valor_unidad:,.0f}",
                    f"${subtotal:,.0f}",
                    estado_texto
                ))
                if esta_pagado:
                    total_pagado += subtotal
                else:
                    total_pendiente += subtotal

        self.lbl_resumen_trabajador.config(
            text=f"Total ya pagado: ${total_pagado:,.0f}   |   Total pendiente por pagar: ${total_pendiente:,.0f}",
            fg="#b71c1c" if total_pendiente > 0 else "#1b5e20"
        )

    def buscar_trabajador(self):
        nombre = self.caja_buscar.get().strip()
        if not nombre:
            messagebox.showwarning("Campo vacío", "Escribe el nombre de un trabajador para consultar.", parent=self.ventana)
            return

        if not nombre.replace(" ", "").isalpha():
            messagebox.showerror("Error", "No se permiten ingresar números en el nombre del trabajador.", parent=self.ventana)
            return

        for item in self.tabla_pesajes.get_children():
            self.tabla_pesajes.delete(item)

        kilos_pendientes = 0
        dias_pendientes = 0
        pago_pendiente = 0
        pago_ya_realizado = 0
        encontrado = False

        for g in self.mi_cosecha.lista_gasto:
            if g.categoria == "Mano de obra":
                trab_fila, desc_limpia, esta_pagado, estado_texto = self.extraer_nombre_y_estado(g.descripcion)
                if trab_fila.lower() == nombre.lower():
                    encontrado = True
                    subtotal = g.calcular_total()
                    self.tabla_pesajes.insert("", "end", values=(
                        g.fecha,
                        desc_limpia,
                        self.formatear_numero(g.cantidad),
                        g.unidad_medida,
                        f"${g.valor_unidad:,.0f}",
                        f"${subtotal:,.0f}",
                        estado_texto
                    ))
                    if esta_pagado:
                        pago_ya_realizado += subtotal
                    else:
                        pago_pendiente += subtotal
                        if str(g.unidad_medida).lower() == "kg":
                            kilos_pendientes += float(g.cantidad)
                        else:
                            dias_pendientes += float(g.cantidad)

        if not encontrado:
            self.lbl_resumen_trabajador.config(text="Sin registros para este trabajador.", fg="black")
            messagebox.showinfo("Sin resultados", f"No se encontraron registros para '{nombre}'.", parent=self.ventana)
            return

        if pago_pendiente == 0:
            self.lbl_resumen_trabajador.config(
                text=f"Trabajador: {nombre.title()} -> ¡AL DÍA! Sin deuda pendiente (Ya liquidado: ${pago_ya_realizado:,.0f})",
                fg="#1b5e20"
            )
        else:
            kilos_txt = self.formatear_numero(kilos_pendientes)
            dias_txt = self.formatear_numero(dias_pendientes)
            detalle_dias = f" + {dias_txt} días" if dias_pendientes > 0 else ""
            self.lbl_resumen_trabajador.config(
                text=f"Trabajador: {nombre.title()} -> Sin pago: {kilos_txt} kg{detalle_dias} | TOTAL A PAGAR: ${pago_pendiente:,.0f}",
                fg="#b71c1c"
            )

    def liquidar_trabajador(self):
        nombre = self.caja_buscar.get().strip()
        if not nombre:
            messagebox.showwarning("Falta nombre", "Escribe el nombre del trabajador y dale a 'Consultar Pendiente' antes de liquidar.", parent=self.ventana)
            return

        if not nombre.replace(" ", "").isalpha():
            messagebox.showerror("Error", "No se permiten ingresar números en el nombre del trabajador.", parent=self.ventana)
            return

        indices_pendientes = []
        monto_a_liquidar = 0
        ultima_fecha_trabajo = ""

        for idx, g in enumerate(self.mi_cosecha.lista_gasto):
            if g.categoria == "Mano de obra":
                trab_fila, _, esta_pagado, _ = self.extraer_nombre_y_estado(g.descripcion)
                if trab_fila.lower() == nombre.lower() and not esta_pagado:
                    indices_pendientes.append(idx)
                    monto_a_liquidar += g.calcular_total()
                    ultima_fecha_trabajo = str(g.fecha)

        if not indices_pendientes:
            messagebox.showinfo("Trabajador al día", f"El trabajador '{nombre.title()}' no tiene pagos pendientes por liquidar.", parent=self.ventana)
            return

        fecha_corte = ultima_fecha_trabajo or self.caja_fecha_fin.get().strip()
        confirmar = messagebox.askyesno(
            "Confirmar Liquidación",
            f"¿Confirmas que ya pagaste ${monto_a_liquidar:,.0f} a {nombre.title()}?\n\n"
            f"Sus registros quedarán marcados como liquidados hasta {fecha_corte} y su saldo quedará en $0.",
            parent=self.ventana
        )
        if not confirmar:
            return

        try:
            for idx in indices_pendientes:
                g = self.mi_cosecha.lista_gasto[idx]
                g.descripcion = f"{g.descripcion} [PAGADO {fecha_corte}]"
                fila_excel = [
                    g.fecha,
                    g.descripcion,
                    self.formatear_numero(g.cantidad),
                    g.unidad_medida,
                    self.formatear_numero(g.valor_unidad),
                    g.categoria,
                    self.formatear_numero(g.calcular_total())
                ]
                self.gestor_excel.actualizar_fila_por_indice("Gastos", idx + 2, fila_excel)

            messagebox.showinfo("Liquidación exitosa", f"¡Listo! {nombre.title()} ha sido liquidado hasta {fecha_corte} por ${monto_a_liquidar:,.0f}.", parent=self.ventana)
            self.buscar_trabajador()
        except Exception as error:
            messagebox.showerror("Error al guardar en Excel", str(error), parent=self.ventana)