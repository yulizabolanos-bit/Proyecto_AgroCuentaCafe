from openpyxl import Workbook
from openpyxl import load_workbook


class GestorExcel:
    def __init__(self, nombre_archivo="Datos agrocuentacafe.xlsx"):
        self.archivo = nombre_archivo
        self.inicializar_excel()

    def inicializar_excel(self):
        try:
            libro = load_workbook(self.archivo)
            hojas_requeridas = {
                "Trabajadores": ["Nombre"],
                "Pesaje": ["Nombre trabajador", "Fecha", "Kilos"],
                "Gastos": ["Fecha", "Descripcion", "Cantidad", "Unidad_medida", "Valor_unidad", "Categoria", "Total"],
                "Ingreso": ["Fecha", "Descripcion", "Cantidad", "Unidad_medida", "Valor_unidad", "Comprador", "Total"],
                "Balance": ["Periodo", "Kilos Vendidos", "Total Ingresos", "Total Inversion", "Balance Neto", "Resultado"]
            }
            hubo_cambios = False
            for nombre_hoja, encabezados in hojas_requeridas.items():
                if nombre_hoja not in libro.sheetnames:
                    nueva_hoja = libro.create_sheet(title=nombre_hoja)
                    nueva_hoja.append(encabezados)
                    hubo_cambios = True
            if hubo_cambios:
                libro.save(self.archivo)
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

            hoja_balance = libro.create_sheet(title="Balance")
            hoja_balance.append(["Periodo", "Kilos Vendidos", "Total Ingresos", "Total Inversion", "Balance Neto", "Resultado"])

            libro.save(self.archivo)
            libro.close()

    def guardar_fila(self, nombre_hoja, datos_fila):
        try:
            libro = load_workbook(self.archivo)
            if nombre_hoja not in libro.sheetnames:
                libro.close()
                raise ValueError(f"La hoja '{nombre_hoja}' no existe en el archivo Excel.")
            hoja = libro[nombre_hoja]

            # Buscar la verdadera última fila con datos para evitar saltos o sobrescrituras
            ultima_fila_real = 1
            for fila_idx in range(hoja.max_row, 1, -1):
                if any(hoja.cell(row=fila_idx, column=col).value is not None for col in range(1, hoja.max_column + 1)):
                    ultima_fila_real = fila_idx
                    break

            nueva_fila = ultima_fila_real + 1
            for col_idx, valor in enumerate(datos_fila, start=1):
                hoja.cell(row=nueva_fila, column=col_idx, value=valor)

            libro.save(self.archivo)
            libro.close()
        except PermissionError:
            raise PermissionError("El archivo Excel está abierto. Ciérralo antes de guardar datos.")

    def leer_filas(self, nombre_hoja):
        try:
            libro = load_workbook(self.archivo)
            if nombre_hoja not in libro.sheetnames:
                libro.close()
                return []
            hoja = libro[nombre_hoja]
            filas = []
            for fila in hoja.iter_rows(min_row=2, values_only=True):
                # Ignorar filas completamente vacías para no desfasar índices
                if fila and any(celda is not None for celda in fila):
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
            libro.close()
        except PermissionError:
            raise PermissionError("El archivo Excel está abierto. Ciérralo antes de modificar datos.")

    def eliminar_fila_por_indice(self, nombre_hoja, num_fila_excel):
        try:
            libro = load_workbook(self.archivo)
            hoja = libro[nombre_hoja]
            hoja.delete_rows(num_fila_excel, 1)
            libro.save(self.archivo)
            libro.close()
        except PermissionError:
            raise PermissionError("El archivo Excel está abierto. Ciérralo antes de eliminar datos.")

    def actualizar_hoja_balance(self, fila_balance):
        """Mantiene siempre actualizado el resumen general en la fila 2 de la hoja Balance."""
        try:
            libro = load_workbook(self.archivo)
            if "Balance" not in libro.sheetnames:
                hoja = libro.create_sheet(title="Balance")
                hoja.append(["Periodo", "Kilos Vendidos", "Total Ingresos", "Total Inversion", "Balance Neto", "Resultado"])
            else:
                hoja = libro["Balance"]

            for col_idx, valor in enumerate(fila_balance, start=1):
                hoja.cell(row=2, column=col_idx, value=valor)

            libro.save(self.archivo)
            libro.close()
        except PermissionError:
            pass

    def exportar_copia(self, ruta_destino):
        try:
            libro = load_workbook(self.archivo)
            libro.save(ruta_destino)
            libro.close()
        except Exception as e:
            raise RuntimeError(f"No se pudo exportar el archivo: {e}")




