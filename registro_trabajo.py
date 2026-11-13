

class RegistroTrabajador:
    def __init__(self):
        self.trabajadores = []

    def agregar_trabajador(self, trabajador):
        self.trabajadores.append(trabajador)

    def buscar_trabajador(self, nombre):
        for trabajador in self.trabajadores:
            if trabajador.nombre.lower() == nombre.lower(): # lower, permite el ingreso de mayusculas y minusculas
                return trabajador

        return None

    def lista_trabajadores(self):
                #los corchetes indican la lista de trabajadores donde
                #t.nombre---> de cada objeto t extrae solo el nombre
        return [t.nombre for t in self.trabajadores]

    def eliminar_trabajador(self, nombre):
        trabajador_encontrado = self.buscar_trabajador(nombre)
        if trabajador_encontrado:
            self.trabajadores.remove(trabajador_encontrado)
            return True, f"El trabajador {nombre} fue eliminado."
        return False, "No se encontró al trabajador."



