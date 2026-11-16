from openpyxl import Workbook  # Para crear un libro
from openpyxl import load_workbook  # Abrir un libro que ya existe


class GestorExcel:
    def __init__(self, nombre_archivo="Datos agrocuentacafe.xlsx"):
        self.archivo = nombre_archivo
        self.inicializar_excel()  # Asegura que el excel exista antes de intentar leer o guardar algo

    def inicializar_excel(self):
        try:
            libro = load_workbook(self.archivo)
            libro.close()
        except FileNotFoundError:
            libro = Workbook()

            hoja_trabajadores = libro.active
            hoja_trabajadores.title = "Trabajadores"
            hoja_trabajadores.append(["Nombre"])

            hoja_pesajes = libro.create_sheet(title="Pesaje")
            hoja_pesajes.append(["Nombre trabajador", "Fecha", "Kilos"])

            hoja_gastos = libro.create_sheet(title="Gastos")
            hoja_gastos.append(["Fecha", "Descripcion", "Cantidad", "Unidad_medida", "Valor_unidad", "Categoria", "Total"])

            hoja_ingreso = libro.create_sheet(title="Ingreso")
            hoja_ingreso.append(["Fecha", "Descripcion", "Cantidad", "Unidad_medida", "Valor_unidad", "Comprador", "Total"])

            libro.save(self.archivo)

    def guardar_fila(self, nombre_hoja, datos_fila):
        try:
            libro = load_workbook(self.archivo)
            if nombre_hoja not in libro.sheetnames:
                raise ValueError(f"La hoja '{nombre_hoja}' no existe.")
            hoja = libro[nombre_hoja]
            hoja.append(datos_fila)
            libro.save(self.archivo)
        except PermissionError:
            raise PermissionError("Cierra el archivo Excel antes de guardar datos.")

    def leer_filas(self, nombre_hoja):
        try:
            libro = load_workbook(self.archivo)
            if nombre_hoja not in libro.sheetnames:
                return []
            hoja = libro[nombre_hoja]
            filas = []
            for fila in hoja.iter_rows(min_row=2, values_only=True):
                filas.append(list(fila))
            libro.close()
            return filas
        except Exception as e:
            raise RuntimeError(f"Error al leer Excel: {e}")

    def actualizar_fila_por_indice(self, nombre_hoja, numero_fila_excel, nuevos_datos):
        try:
            libro = load_workbook(self.archivo)
            hoja = libro[nombre_hoja]
            for numero_columna, dato in enumerate(nuevos_datos, start=1):
                hoja.cell(row=numero_fila_excel, column=numero_columna, value=dato)
            libro.save(self.archivo)
        except PermissionError:
            raise PermissionError("Cierra el archivo Excel antes de modificar datos.")

    def eliminar_fila_por_indice(self, nombre_hoja, num_fila_excel):
        try:
            libro = load_workbook(self.archivo)
            hoja = libro[nombre_hoja]
            hoja.delete_rows(num_fila_excel, 1)
            libro.save(self.archivo)
        except PermissionError:
            raise PermissionError("Cierra el archivo Excel antes de eliminar datos.")

    def exportar_copia(self, ruta_destino):
        try:
            libro = load_workbook(self.archivo)
            libro.save(ruta_destino)
            libro.close()
        except Exception as e:
            raise RuntimeError(f"No se pudo exportar el archivo: {e}")





