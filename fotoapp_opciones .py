# Código para ejecutar en el Notebook de pruebas
import os
import fotoapp as fa

imagen_actual = None
ruta_actual = None

while True:
  print("\n--- MENÚ FOTOAPP ---")
  print("1. Cargar y redimensionar imagen para Redes Sociales")
  print("2. Ajustar contraste (Histograma)")
  print("3. Aplicar filtro de Pillow (1 al 9)")
  print("4. Generar boceto / Detección de bordes (2 técnicas)")
  print("5. Salir")

  opcion = input("Seleccione una opción (1-5): ")

  try:
    if opcion == "1":
      ruta_actual = input("Ingrese la ruta de la imagen o URL: ")
      red = input(
          "Ingrese la red social (Youtube, Instagram, Twitter, Facebook): "
      )
      imagen_actual = fa.cargar_y_redimensionar(ruta_actual, red)
      print("¡Imagen cargada y redimensionada con éxito!")
      # Guardar temporalmente para OpenCV en la opción 4 si es ruta local
      imagen_actual.save("temp_img.jpg")

    elif opcion == "2":
      if imagen_actual is None:
        raise fa.ImageNotLoadedException()
      fa.ajustar_contraste(imagen_actual)

    elif opcion == "3":
      if imagen_actual is None:
        raise fa.ImageNotLoadedException()
      print(
          "Filtros: 1.Blur, 2.Contour, 3.Detail, 4.Edge Enhance, 5.Edge Enhance"
          " More, 6.Emboss, 7.Find Edges, 8.Sharpen, 9.Smooth"
      )
      num = int(input("Ingrese el número del filtro (1-9): "))
      fa.aplicar_filtro_pillow(imagen_actual, num)

    elif opcion == "4":
      if ruta_actual is None or not os.path.exists("temp_img.jpg"):
        raise fa.ImageNotLoadedException(
            "Debe cargar una imagen local válida para procesar los bordes."
        )
      fa.generar_boceto("temp_img.jpg")

    elif opcion == "5":
      print("Saliendo de la aplicación. ¡Hasta luego!")
      break
    else:
      print("Opción no válida. Intente del 1 al 5.")

  except Exception as e:
    print(f"[ERROR]: {e}")