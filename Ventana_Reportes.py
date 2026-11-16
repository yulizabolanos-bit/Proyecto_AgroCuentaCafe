import tkinter as tk
from tkinter import ttk, messagebox


class VentanaReportes:
    def __init__(self, ventana_padre, mi_cosecha, registro_trabajadores, gestor_excel):
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Balance Financiero y Liquidación de Trabajadores - AgroCuenta Café")
        self.ventana.geometry("760x620")
        self.ventana.resizable(False, False)

        self.mi_cosecha = mi_cosecha
        self.registro_trabajadores = registro_trabajadores
        self.gestor_excel = gestor_excel

        self.crear_elementos_pantalla()
        self.consultar_balance_total()

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

        tk.Button(marco_fechas, text="Consultar Fechas", bg="#1565c0", fg="white", command=self.consultar_por_fechas).pack(side="left", padx=8)
        tk.Button(marco_fechas, text="Ver Toda la Cosecha", command=self.consultar_balance_total).pack(side="left", padx=4)

        # --- SECCIÓN 2: Resultado Financiero (Inversión, Ventas, Ganancia o Pérdida) ---
        marco_resultado = tk.LabelFrame(self.ventana, text="Resultado Financiero de la Finca", padx=12, pady=10)
        marco_resultado.pack(fill="x", padx=15, pady=5)

        self.texto_diagnostico = tk.Text(marco_resultado, height=7, font=("Arial", 10), bg="#f9fbe7", relief="flat", wrap="word")
        self.texto_diagnostico.pack(fill="x")
        self.texto_diagnostico.config(state="disabled")

        # --- SECCIÓN 3: Buscador y Liquidación de Trabajadores ---
        marco_busqueda = tk.LabelFrame(self.ventana, text="Liquidación de Trabajadores (Kilos, Jornales y Pago Total)", padx=10, pady=8)
        marco_busqueda.pack(fill="both", expand=True, padx=15, pady=5)

        fila_buscar = tk.Frame(marco_busqueda)
        fila_buscar.pack(fill="x", pady=5)

        tk.Label(fila_buscar, text="Nombre del trabajador:").pack(side="left", padx=5)
        self.caja_buscar = tk.Entry(fila_buscar, width=25)
        self.caja_buscar.pack(side="left", padx=5)
        self.caja_buscar.bind("<Return>", lambda evento: self.buscar_trabajador())

        tk.Button(fila_buscar, text="Buscar y Liquidar", bg="#2e7d32", fg="white", command=self.buscar_trabajador).pack(side="left", padx=5)
        tk.Button(fila_buscar, text="Ver Todos los Registros", command=self.cargar_todos_trabajos).pack(side="left", padx=5)

        columnas = ("fecha", "detalle", "cantidad", "unidad", "valor_unit", "total_pagar")
        self.tabla_pesajes = ttk.Treeview(marco_busqueda, columns=columnas, show="headings", height=6)
        self.tabla_pesajes.heading("fecha", text="Fecha")
        self.tabla_pesajes.heading("detalle", text="Labor / Trabajador")
        self.tabla_pesajes.heading("cantidad", text="Cantidad")
        self.tabla_pesajes.heading("unidad", text="Unidad")
        self.tabla_pesajes.heading("valor_unit", text="Valor Unit. ($)")
        self.tabla_pesajes.heading("total_pagar", text="Subtotal ($)")

        self.tabla_pesajes.column("fecha", width=95, anchor="center")
        self.tabla_pesajes.column("detalle", width=210)
        self.tabla_pesajes.column("cantidad", width=80, anchor="center")
        self.tabla_pesajes.column("unidad", width=70, anchor="center")
        self.tabla_pesajes.column("valor_unit", width=105, anchor="center")
        self.tabla_pesajes.column("total_pagar", width=110, anchor="center")
        self.tabla_pesajes.pack(fill="both", expand=True, pady=5)

        self.lbl_resumen_trabajador = tk.Label(
            marco_busqueda,
            text="Total kilos recolectados: 0 kg   |   Total a pagar: $0",
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
        kilos = datos["kilos_vendidos"]
        balance = datos["balance"]
        por_categoria = datos["por_categoria"]

        desglose = ""
        if por_categoria:
            partes = [f"  • {cat}: ${monto:,.0f}" for cat, monto in por_categoria.items()]
            desglose = "\nDetalle de lo que invertiste en tu finca:\n" + "\n".join(partes) + "\n"

        if balance > 0:
            veredicto = f"RESULTADO: ¡Tuviste una GANANCIA de ${balance:,.0f}!"
        elif balance < 0:
            veredicto = f"RESULTADO: Tuviste una PÉRDIDA de ${abs(balance):,.0f}."
        else:
            veredicto = "RESULTADO: Estás en punto de equilibrio ($0 ganancia / $0 pérdida)."

        mensaje = (
            f"Periodo consultado: {titulo_periodo}\n"
            f"• Café vendido: {kilos:,.1f} kg  |  Total ingresos por ventas: ${vendido:,.0f}\n"
            f"• Total invertido / gastado en la finca: ${invertido:,.0f}\n"
            f"{desglose}\n"
            f"{veredicto}"
        )

        self.texto_diagnostico.config(state="normal")
        self.texto_diagnostico.delete("1.0", tk.END)
        self.texto_diagnostico.insert("1.0", mensaje)
        self.texto_diagnostico.config(state="disabled")

    def consultar_balance_total(self):
        datos = self.mi_cosecha.generar_resumen_financiero()
        self.mostrar_diagnostico(datos, f"Toda la cosecha ({self.mi_cosecha.descripcion})")

    def consultar_por_fechas(self):
        inicio = self.caja_fecha_inicio.get().strip()
        fin = self.caja_fecha_fin.get().strip()
        if not inicio or not fin:
            messagebox.showwarning("Fechas requeridas", "Escribe ambas fechas en formato AAAA-MM-DD.", parent=self.ventana)
            return
        datos = self.mi_cosecha.generar_resumen_financiero(inicio, fin)
        self.mostrar_diagnostico(datos, f"Desde {inicio} hasta {fin}")

    def cargar_todos_trabajos(self):
        for item in self.tabla_pesajes.get_children():
            self.tabla_pesajes.delete(item)

        total_kilos = 0
        total_pago = 0

        for g in self.mi_cosecha.lista_gasto:
            if g.categoria == "Mano de obra":
                subtotal = g.calcular_total()
                self.tabla_pesajes.insert("", "end", values=(
                    g.fecha,
                    g.descripcion,
                    g.cantidad,
                    g.unidad_medida,
                    f"${g.valor_unidad:,.0f}",
                    f"${subtotal:,.0f}"
                ))
                if str(g.unidad_medida).lower() == "kg":
                    total_kilos += float(g.cantidad)
                total_pago += subtotal

        self.lbl_resumen_trabajador.config(
            text=f"Todos los trabajadores -> Kilos recolectados: {total_kilos:,.1f} kg   |   Total Mano de Obra: ${total_pago:,.0f}"
        )

    def buscar_trabajador(self):
        nombre = self.caja_buscar.get().strip()
        if not nombre:
            messagebox.showwarning("Campo vacío", "Escribe el nombre de un trabajador para buscar.", parent=self.ventana)
            return

        for item in self.tabla_pesajes.get_children():
            self.tabla_pesajes.delete(item)

        total_kilos = 0
        total_dias = 0
        total_pago = 0
        encontrado = False

        for g in self.mi_cosecha.lista_gasto:
            if g.categoria == "Mano de obra" and " - " in str(g.descripcion):
                trabajador_fila = str(g.descripcion).split(" - ")[1].split(" (")[0].strip().lower()
                if trabajador_fila == nombre.lower():
                    encontrado = True
                    subtotal = g.calcular_total()
                    self.tabla_pesajes.insert("", "end", values=(
                        g.fecha,
                        g.descripcion,
                        g.cantidad,
                        g.unidad_medida,
                        f"${g.valor_unidad:,.0f}",
                        f"${subtotal:,.0f}"
                    ))
                    if str(g.unidad_medida).lower() == "kg":
                        total_kilos += float(g.cantidad)
                    else:
                        total_dias += float(g.cantidad)
                    total_pago += subtotal

        if not encontrado:
            self.lbl_resumen_trabajador.config(text="Total kilos recolectados: 0 kg   |   Total a pagar: $0")
            messagebox.showinfo("Sin resultados", f"No se encontraron registros para el trabajador '{nombre}'.", parent=self.ventana)
            return

        detalle_dias = f"  |  Jornales: {total_dias:,.1f} días" if total_dias > 0 else ""
        self.lbl_resumen_trabajador.config(
            text=f"Trabajador: {nombre.title()} -> Recolectó: {total_kilos:,.1f} kg{detalle_dias}   |   TOTAL A PAGAR: ${total_pago:,.0f}"
        )
