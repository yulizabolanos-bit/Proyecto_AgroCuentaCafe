
class Cosecha:
    def __init__(self, descripcion):
        self.descripcion = descripcion
        self.lista_gasto = []
        self.lista_ingreso=[]


    def agregar_gasto(self, gasto):

        self.lista_gasto.append(gasto)

    def agregar_ingreso(self,ingreso):

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

        print("\n",f"REGISTRO DE MI COSECHA [ {self.descripcion} ]","\n")
        print(f"El gasto total hasta el momento es de: {gasto} ")
        print(f"Su ingreso total hasta el momento es de: {ingreso} ")
        print(f"Su balance actual es de: {balance} ")


# mi_consulta = Cosecha("12 / octubre /2026")
# mi_consulta.consultar_inventario()