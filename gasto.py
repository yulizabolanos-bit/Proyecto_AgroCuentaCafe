
from movimiento_financiero import MovimientoFinanciero
#clase hija 1

class Gasto(MovimientoFinanciero):
    categoria_gastos = [
        "Mano de obra",
        "Insumos Agrícolas",
        "Alimentación",
        "Transporte",
        "Otros gastos"
    ]

    def __init__( self, fecha,descripcion,cantidad,unidad_medida,valor_unidad, categoria):
        super(). __init__(fecha,descripcion,cantidad,unidad_medida,valor_unidad)
        self.categoria = categoria


    def validar_categoria(self):
        if self.categoria in self.categoria_gastos:
            return True
        else:
            return False

    def datos(self):
        if self.validar_categoria():
            return f"{super().datos()} | Categoria: {self.categoria} | Total Invertido : ${self.calcular_total(): ,.0f}"
        else:
            return "La categoría del gasto no es válida."

# compra3 = Gasto("febrero 4", "urea",3,"bultos",130000, "Insumos Agrícolas" )
#
# print(compra3.datos())



