
#clase padre

class MovimientoFinanciero:
    def __init__(self, fecha,descripcion,cantidad ,unidad_medida, valor_unidad):

        self.fecha = fecha
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.unidad_medida = unidad_medida
        self.valor_unidad = valor_unidad
        self._total = self.cantidad * self.valor_unidad


    #metodos

    def calcular_total(self):

        return self._total

    def datos(self):
        return f"fecha:{self.fecha} | descripcion: {self.descripcion} | cantidad: { self.cantidad} {self.unidad_medida} | valor unitario:${self.valor_unidad:,.0f} "


# #objeto
# compra=MovimientoFinanciero("12/julio/2026","urea",3,"bultos",120000)
# print(compra.datos())
# print("Total: $",compra.calcular_total())
#
# compra2= MovimientoFinanciero("12/julio/2026","urea",5,"bulto",95000)
# print(compra2.datos())
# print("total: $",compra2.calcular_total())