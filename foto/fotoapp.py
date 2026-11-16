import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import cv2


class ImageNotLoadedException(Exception):
  """Excepción personalizada para validar que la imagen fue cargada."""

  def __init__(
      self, message="Debe cargar una imagen primero utilizando la opción 1."
  ):
    super().__init__(message)


def cargar_y_redimensionar(ruta_o_url, red_social):
  """1. Lee/abre la foto y la redimensiona al tamaño adecuado para la red social,

  manteniendo la escala.
  """
  # Dimensiones recomendadas para redes sociales (ancho, alto)
  dimensiones = {
      "Youtube": (1280, 720),
      "Instagram": (1080, 1080),
      "Twitter": (1200, 675),
      "Facebook": (1200, 630),
  }

  if red_social not in dimensiones:
    raise ValueError(
        "Red social no válida. Elija entre: Youtube, Instagram, Twitter,"
        " Facebook."
    )

  try:
    # Si es URL o ruta local
    if ruta_o_url.startswith("http://") or ruta_o_url.startswith("https://"):
      import requests
      from io import BytesIO

      response = requests.get(ruta_o_url)
      img = Image.open(BytesIO(response.content))
    else:
      img = Image.open(ruta_o_url)

    # Redimensionar manteniendo la escala (thumbnail modifica la imagen in-place manteniendo proporción)
    target_size = dimensiones[red_social]
    img_redimensionada = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS)
    return img_redimensionada
  except Exception as e:
    raise Exception(f"Error al abrir o procesar la imagen: {e}")


def ajustar_contraste(img):
  """2. Ajusta el contraste de la foto utilizando ecualización/histograma."""
  # Convertir a escala de grises para ecualización de histograma estándar o trabajar por canales
  if img.mode != "L":
    img_gray = img.convert("L")
  else:
    img_gray = img

  # Ecualizar histograma usando Pillow (ImageOps)
  img_ecualizada = ImageOps.equalize(img_gray)

  # Mostrar y guardar figura comparativa
  fig, axes = plt.subplots(1, 2, figsize=(10, 5))
  axes[0].imshow(img, cmap="gray" if img.mode == "L" else None)
  axes[0].set_title("Imagen Original")
  axes[0].axis("off")

  axes[1].imshow(img_ecualizada, cmap="gray")
  axes[1].set_title("Imagen Ecualizada (Contraste Ajustado)")
  axes[1].axis("off")

  plt.tight_layout()
  plt.savefig("resultado_contraste.png")
  plt.show()

  return img_ecualizada


def aplicar_filtro_pillow(img, numero_filtro):
  """3. Aplica uno de los 9 filtros de Pillow según el número elegido."""
  filtros_dict = {
      1: ("Blur", ImageFilter.BLUR),
      2: ("Contour", ImageFilter.CONTOUR),
      3: ("Detail", ImageFilter.DETAIL),
      4: ("Edge Enhance", ImageFilter.EDGE_ENHANCE),
      5: ("Edge Enhance More", ImageFilter.EDGE_ENHANCE_MORE),
      6: ("Emboss", ImageFilter.EMBOSS),
      7: ("Find Edges", ImageFilter.FIND_EDGES),
      8: ("Sharpen", ImageFilter.SHARPEN),
      9: ("Smooth", ImageFilter.SMOOTH),
  }

  if numero_filtro not in filtros_dict:
    raise ValueError("Número de filtro inválido. Debe ser un entero entre 1 y 9.")

  nombre_filtro, filtro_obj = filtros_dict[numero_filtro]
  img_filtrada = img.filter(filtro_obj)

  # Mostrar original y filtrada lado a lado
  fig, axes = plt.subplots(1, 2, figsize=(10, 5))
  axes[0].imshow(img)
  axes[0].set_title("Imagen Original")
  axes[0].axis("off")

  axes[1].imshow(img_filtrada)
  axes[1].set_title(f"Filtro: {nombre_filtro}")
  axes[1].axis("off")

  plt.tight_layout()
  plt.savefig(f"resultado_filtro_{nombre_filtro.lower().replace(' ', '_')}.png")
  plt.show()

  return img_filtrada


def generar_boceto(img_path):
  """4. Aplica dos técnicas diferentes para generar un efecto boceto/bordes."""
  # Cargar imagen con OpenCV
  img_cv = cv2.imread(img_path)
  gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

  # Técnica 1: Detección de bordes Canny
  blur = cv2.GaussianBlur(gray, (5, 5), 0)
  canny_edges = cv2.Canny(blur, 50, 150)

  # Técnica 2: Operador Laplaciano + Binarización
  laplacian = cv2.Laplacian(gray, cv2.CV_64F)
  laplacian = np.uint8(np.absolute(laplacian))
  _, thresh = cv2.threshold(laplacian, 30, 255, cv2.THRESH_BINARY_INV)

  # Mostrar resultados lado a lado
  fig, axes = plt.subplots(1, 2, figsize=(10, 5))
  axes[0].imshow(canny_edges, cmap="gray")
  axes[0].set_title("Técnica 1: Canny Edge Detection")
  axes[0].axis("off")

  axes[1].imshow(thresh, cmap="gray")
  axes[1].set_title("Técnica 2: Laplaciano + Umbralización")
  axes[1].axis("off")

  plt.tight_layout()
  plt.savefig("resultado_bocetos.png")
  plt.show()

  return canny_edges, thresh
