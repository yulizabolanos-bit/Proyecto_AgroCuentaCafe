
from movimiento_financiero import MovimientoFinanciero

# Clase hija 2
class Ingreso(MovimientoFinanciero):

    def __init__(self, fecha, descripcion, cantidad, unidad_medida, valor_unidad, comprador):
        super().__init__(fecha, descripcion, cantidad, unidad_medida,valor_unidad)
        self.comprador = comprador


    def datos(self):
        return (f"{super().datos()} | Comprador: {self.comprador} | Total del ingreso: ${self.calcular_total():,.0f}")

    def validar_venta(self):
        if self.cantidad > 0 and self.valor_unidad > 0:
            return True
        else:
            return False


# #
# ingreso1 = Ingreso("12/Agosto/2026", "Venta de café",100,"Kg",18000,"Cooperativa cafetera")
#
# print(ingreso1.datos())
# print(ingreso1.validar_venta())
