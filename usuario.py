
class Usuario:
    #atributo
    def __init__(self, nombre, clave, cedula = None):
        self.nombre = nombre
        self._cedula = cedula #atributo protejido
        self.__clave = clave # atributo privado, no puede ser cambiada desde afuera

#metodo
    def verificar_credenciales(self, nombre_ingresado, clave_ingresada):

        nombre_valido = (self.nombre.strip().lower() == nombre_ingresado.strip().lower())
        clave_valida = self.__clave.strip() == clave_ingresada.strip()

        return nombre_valido and clave_valida

    def cambiar_clave(self, cedula_ingresada,clave_actual,clave_nueva):

        if cedula_ingresada != self._cedula:
            return False,"ERROR de identidad...La cedula ingresada no corresponde con el numero de cedula correcto"

        if not self.verificar_credenciales(self.nombre,clave_actual):
            return False, " ERROR...La clave ingresada no corresponde con la correcta"

        self.__clave = clave_nueva # Actualiza el valor de la clave
        return True ,"Tu cambio de clave fue un ¡Exito! :)"
#
# # objeto
#
# usuario_autorizado = Usuario("Mabel",1080,1290)
# print(usuario_autorizado.comprobar_clave(1290))
# mensaje= usuario_autorizado.cambiar_clave("123",1290, 234)
# print("\n",mensaje)
#
# mensaje = usuario_autorizado.cambiar_clave(1080,1290, 234)
# print("\n",mensaje)
# print(usuario_autorizado.comprobar_clave(1290))
# print(usuario_autorizado.comprobar_clave(234))


