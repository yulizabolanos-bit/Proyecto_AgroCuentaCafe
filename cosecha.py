class Cosecha:
    def __init__(self, descripcion="Cosecha Actual"):
        self.descripcion = descripcion
        self.lista_gasto = []
        self.lista_ingreso = []

    def agregar_gasto(self, gasto):
        self.lista_gasto.append(gasto)

    def agregar_ingreso(self, ingreso):
        self.lista_ingreso.append(ingreso)

    def total_gasto(self):
        total = 0
        for g in self.lista_gasto:
            total += g.calcular_total()
        return total

    def total_ingreso(self):
        total = 0
        for i in self.lista_ingreso:
            total += i.calcular_total()
        return total

    def consultar_inventario(self):
        gasto = self.total_gasto()
        ingreso = self.total_ingreso()
        balance = ingreso - gasto

        print("\n", f"REGISTRO DE MI COSECHA [ {self.descripcion} ]", "\n")
        print(f"El gasto total hasta el momento es de: {gasto} ")
        print(f"Su ingreso total hasta el momento es de: {ingreso} ")
        print(f"Su balance actual es de: {balance} ")

    def generar_resumen_financiero(self, fecha_inicio=None, fecha_fin=None):
        total_invertido = 0
        total_vendido = 0
        kilos_vendidos = 0
        inversion_por_categoria = {}

        for g in self.lista_gasto:
            if fecha_inicio and fecha_fin:
                if not (fecha_inicio <= str(g.fecha) <= fecha_fin):
                    continue
            valor = g.calcular_total()
            total_invertido += valor
            inversion_por_categoria[g.categoria] = inversion_por_categoria.get(g.categoria, 0) + valor

        for i in self.lista_ingreso:
            if fecha_inicio and fecha_fin:
                if not (fecha_inicio <= str(i.fecha) <= fecha_fin):
                    continue
            total_vendido += i.calcular_total()
            kilos_vendidos += float(i.cantidad)

        balance = total_vendido - total_invertido
        return {
            "invertido": total_invertido,
            "vendido": total_vendido,
            "kilos_vendidos": kilos_vendidos,
            "balance": balance,
            "por_categoria": inversion_por_categoria
        }

# mi_consulta = Cosecha("12 / octubre /2026")
# mi_consulta.consultar_inventario()