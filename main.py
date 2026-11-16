import tkinter as tk
from usuario import Usuario
from registro_trabajo import RegistroTrabajador
from cosecha import Cosecha
from Gestor_Excel import GestorExcel
from Ventana_login import VentanaLogin

ventana_base = tk.Tk()

gestor_excel = GestorExcel()
usuario_autorizado = Usuario("Mabel Bolaños")
registro_trabajadores = RegistroTrabajador()
mi_cosecha = Cosecha("Cosecha Principal 2026")

app = VentanaLogin(
    ventana_base,
    usuario_autorizado,
    mi_cosecha,
    registro_trabajadores,
    gestor_excel
)

ventana_base.mainloop()