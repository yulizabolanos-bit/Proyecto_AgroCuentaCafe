
class Trabajador:
    def __init__(self, nombre):
        self.nombre = nombre
        self._registros = [] #atributo protejido

    def registrar_pesaje(self, fecha, kilos):
        if kilos <= 0:
            raise ValueError("Los kilos deben ser mayores que cero")

        self._registros.append({"fecha": fecha,"kilos": kilos })

    def calcular_total_dia(self, fecha):
        total = 0

        for registro in self._registros:
            if registro["fecha"] == fecha:
                total += registro["kilos"]

        return total

    def  mostrar_resumen(self, fecha):
        total = self.calcular_total_dia(fecha)

        return f"El / la trabajador(a) {self.nombre} recogió un total de {total} kg de café en la fecha {fecha}."
#
#
# trabajador1 = Trabajador("Mabel")
# trabajador1.registrar_pesaje("12/agosto/2026",12)
# trabajador1.registrar_pesaje("12/agosto/2026",34)
# print(trabajador1.calcular_total_dia("12/agosto/2026"))
# print(trabajador1.mostrar_resumen("12/agosto/2026"))
#
#
# trabajador1= Trabajador("Mabel")
# trabajador1.registrar_pesaje("13/agosto/2025",13)
# trabajador1.registrar_pesaje("13/agosto/2025",45)
# print(trabajador1.calcular_total_dia("13/agosto/2025"))
# print(trabajador1.mostrar_resumen("13/agosto/2025"))
