from cosecha import Cosecha
from gasto import Gasto
from ingreso import Ingreso
from registro_trabajo import RegistroTrabajador
from trabajador import Trabajador
from usuario import Usuario

usuario_autorizado = Usuario("Mabel Bolaños", "123",1090 )
registro_trabajadores = RegistroTrabajador()

print("\n~~~~~~~~~~Agrocuenta Cafe~~~~~~~~~~\n")

while True:
  nombre = input("Nombre: ")
  clave_ingreso = input("Clave ingresado: ")

  if usuario_autorizado.verificar_credenciales(nombre, clave_ingreso):
    print(
        f"Bienvenido/a {usuario_autorizado.nombre}!.\n\n Acceso concedido :)"
        " \n"
    )
    break
  else:
    print(
        " El nombre o la clave es incorrecto! ..\n Acceso denegado :("
        " intentelo de nuevo \n"
    )

print("=========Registro cosecha========\n")
descripcion_cosecha = input("Ingrese fecha o periodo de la cosecha : ")
mi_cosecha = Cosecha(descripcion_cosecha)

while True:
  print(f"\nAGROCUENTA CAFE -- cosecha: {mi_cosecha.descripcion}\n")
  print("1.Registrar gasto")
  print("2.Registrar ingreso (venta)")
  print("3.Consultar balance de la cosecha")
  print("4.salir")

  opcion_principal = int(
      input("Ingrese una de las opciones que desea (1-4): ")
  )

  if opcion_principal <= 0 or opcion_principal > 4:
    print("ERROR--La opcion elegida no se encuentra en ese rango")
    continue

  else:

    if opcion_principal == 1:
      print("categoria selecionada [Registro de gastos]\n")

      for num, cat in enumerate(Gasto.categoria_gastos, start=1):
        print(f"{num}. {cat}")

      opcion_categoria = int(input("\nIngrese una opcion (1-5): "))

      if opcion_categoria <= 0 or opcion_categoria > len(Gasto.categoria_gastos):
        print("ERROR--La opcion selecionada no es valida")
        continue
      else:
        categoria_elegida = Gasto.categoria_gastos[opcion_categoria - 1]

        if categoria_elegida == "Mano de obra":
          print(f"\n--- {categoria_elegida} ---")
          nombre_trabajador = input("\nIngrese nombre del trabajador: ").strip()

          trabajador_actual = registro_trabajadores.buscar_trabajador(
              nombre_trabajador
          )

          if trabajador_actual is None:
            print(
                f"El trabajador/a {nombre_trabajador} es nuevo/a ..."
                " Registrandolo \n"
            )
            trabajador_actual = Trabajador(nombre_trabajador)
            registro_trabajadores.agregar_trabajador(trabajador_actual)
          else:
            print(f"Trabajador encontrado: {trabajador_actual.nombre}")

          print(f"¿Que labor realizo {trabajador_actual.nombre}?")
          print("1.Recoleccion de cafe")
          print("2.otra labor (Abono, guadaño, fumigo, deshiervo. etc)\n")

          tipo_labor = int(input("seleccione una de las dos opciones (1 o 2) : "))
          if tipo_labor <= 0 or tipo_labor > 2:
            print("ERROR--La opcion selecionada no es valida")
            continue

          fecha = input("Ingrese la fecha de el dia de hoy: ").strip()

          if tipo_labor == 1:
            while True:
              kilos = int(input("cuantos kilos recolecto: "))
              if kilos > 0:
                break
              print("ERROR: Los kilos deben ser mayores a cero.")

            while True:
              precio_kilo = int(input("Precio de pago por kilo: $ "))
              if precio_kilo > 0:
                break
              print("ERROR: El precio por kilo no puede ser negativo ni cero.")

            trabajador_actual.registrar_pesaje(fecha, kilos)

            descripcion = f"Recolección café - {trabajador_actual.nombre}"
            cantidad = kilos
            unidad_medida = "kg"
            valor_unidad = precio_kilo

            print(trabajador_actual.mostrar_resumen(fecha))

          else:
            nombre_labor = input("Escriba la labor: ").strip()

            while True:
              dias = int(input("Dias trabajados: "))
              if dias > 0:
                break
              print("ERROR: Los días trabajados deben ser mayores a cero.")

            while True:
              valor_dia = int(input("Precio del jornal: $ "))
              if valor_dia > 0:
                break
              print("ERROR: El precio del jornal no puede ser negativo ni cero.")

            descripcion = f"{nombre_labor} - {trabajador_actual.nombre}"
            cantidad = dias
            unidad_medida = "días"
            valor_unidad = valor_dia

          nuevo_gasto = Gasto(
              fecha,
              descripcion,
              cantidad,
              unidad_medida,
              valor_unidad,
              categoria_elegida,
          )

          mi_cosecha.agregar_gasto(nuevo_gasto)
          print("\nGasto registrado exitosamente:")
          print(nuevo_gasto.datos())

        else:
          print(f"\n--- {categoria_elegida} ---")
          fecha = input("Fecha : ").strip()
          descripcion = input(
              f"Descripción del gasto ({categoria_elegida}): "
          ).strip()

          while True:
            cantidad = int(input("Cantidad: "))
            if cantidad > 0:
              break
            print("ERROR: La cantidad debe ser mayor a cero.")

          unidad_medida = input(
              "Unidad de medida (bultos, litros, viaje, comida etc): "
          ).strip()

          while True:
            valor_unidad = int(input("Valor unitario ($): "))
            if valor_unidad > 0:
              break
            print("ERROR: El valor unitario no puede ser negativo ni cero.")

          nuevo_gasto = Gasto(
              fecha,
              descripcion,
              cantidad,
              unidad_medida,
              valor_unidad,
              categoria_elegida,
          )
          mi_cosecha.agregar_gasto(nuevo_gasto)

          print("\n✔ Gasto registrado exitosamente:")
          print(nuevo_gasto.datos())

    elif opcion_principal == 2:
      print("\n--- Registro de Ingreso (Venta de Café) ---")
      fecha = input("Fecha de la venta: ").strip()
      descripcion = input("Tipo de ingreso (cafe, pasilla): ").strip()

      while True:
        cantidad = int(input("Kilos vendidos: "))
        if cantidad > 0:
          break
        print("ERROR: La cantidad vendida debe ser mayor a cero.")

      while True:
        valor_unidad = int(input("Precio por kilo ($): "))
        if valor_unidad > 0:
          break
        print("ERROR: El precio de venta debe ser mayor a cero.")

      comprador = input("Nombre de vendedor o cooperativa: ").strip()

      nuevo_ingreso = Ingreso(
          fecha, descripcion, cantidad, "kg", valor_unidad, comprador
      )

      if nuevo_ingreso.validar_venta():
        mi_cosecha.agregar_ingreso(nuevo_ingreso)
        print("\nVenta registrada exitosamente:")
        print(nuevo_ingreso.datos())

    elif opcion_principal == 3:
      mi_cosecha.consultar_inventario()

    elif opcion_principal == 4:
      print(
          f"Saliendo del programa... ¡Hasta pronto, {usuario_autorizado.nombre}!"
      )
      break