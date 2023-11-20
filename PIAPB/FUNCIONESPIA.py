import os
import re
import matplotlib.pyplot as plt
from statistics import mean

#FUNCIONES

def limppantalla(): # FUNCION PARA LIMPIAR PANTALLA. ELIUD
    nomsis = os.name
    if nomsis == 'nt': #Esto es para windows
        os.system('cls')
    else: #MACOS y LINUX
        os.system('clear')

def excepVaENT(men, limite): #FUNCION REGINA
    while True:
        try:
            ent = input(men)
            if re.match(r'^-?\d+$', ent):
                num = int(ent)
                if 0 < num <= limite:
                    return num
                else:
                    raise ValueError(f"Por favor, ingresa un número válido.")
            else:
                raise ValueError("Por favor, ingresa un número entero válido.")
        except ValueError as e:
            print(e)


def validar_numero(numero): #FUNCION USO DE RE PARA VALIDACION DEL MENÚ. ELIUD
    return re.match('^[1-5]$', str(numero))


def excepcionesEnt(numeroEntero): #FUNCION DE EXCEPCIONES PARA VALIDAR MENÚ. ELIUD
    while True:
        try:
            numero = int(input(numeroEntero))
            if validar_numero(numero):
                return numero
            else:
                print("\n*** FAVOR DE INGRESAR UNA DE LAS OPCIONES ***\n")
        except ValueError:
            print("\n*** FAVOR DE INGRESAR UN NÚMERO ENTERO ***\n")


def excepVa_RANG_Y_ENT(variable, y): #FUNCION DE ERICK
        while True:
            try:
                num = int(input(variable))
                if num > 0 and num <=y:
                    return num
                else:
                    print("\nIngresa un número dentro de las opciones dadas:\n")
            except ValueError:
                print("\nIngresa un número correcto:\n")
            

def preg_peli_vista():
    resp_visuali = input("¿Deseas guardar la película en el historial de visualizaciones? \n'Si' \n' No'\n").lower()
    while resp_visuali not in ["si", "no"]:
        print("Favor de responder con un '1)Si' o '2)No'")
        resp_visuali = input("¿Deseas guardar la película en el historial de visualizaciones? \n'Si' \n' No'\n").lower()
    return resp_visuali

def obtener_generos_vistos(archivo_peliculas_vistas): #FUNCIÓN DE JUAN CARLOS
    # Función para obtener la cantidad de películas por género en el historial
    generos_vistos = {}
    with open(archivo_peliculas_vistas, 'r') as archivo:
        for linea in archivo:
            if 'Géneros' in linea:
                generos_linea = linea.split(':')[1].strip().split(', ')
                for genero in generos_linea:
                    if genero in generos_vistos:
                        generos_vistos[genero] += 1
                    else:
                        generos_vistos[genero] = 1
    return generos_vistos

def obtener_proporcion_generos_historial(archivo_peliculas_vistas): #FUNCIÓN DE JUAN CARLOS
    # Función para obtener la proporción de géneros en el historial
    generos_vistos = obtener_generos_vistos(archivo_peliculas_vistas)
    total_peliculas = sum(generos_vistos.values())
    proporcion_generos = {genero: (conteo / total_peliculas) for genero, conteo in generos_vistos.items()}
    return proporcion_generos

def grafico_pastel_generos_historial(archivo_peliculas_vistas): #FUNCIÓN DE JUAN CARLOS
    # Función para graficar el pastel de géneros en el historial
    proporcion_generos = obtener_proporcion_generos_historial(archivo_peliculas_vistas)

    labels = list(proporcion_generos.keys())
    sizes = list(proporcion_generos.values())

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Proporción de Géneros', fontdict={'fontname': 'IMPACT', 'fontsize': 20, 'color': '#7C0CB8'})
    plt.savefig('graficaPIEHis.png')
    plt.show()

def grafico_barras_puntuacion_historial(archivo_historial): #FUNCIÓN DE JUAN CARLOS
    # Función para graficar la puntuación promedio de las películas en el historial
    with open(archivo_historial, 'r') as archivo:
        data = archivo.read()
        peliculas = re.findall(r'Título: (.+?)\n.*?Puntuación promedio: (.+?)\n', data, re.DOTALL)

    if not peliculas:
        print("No hay películas en el historial.")
        return

    titulosg = [p[0] for p in peliculas]
    puntuaciones = [float(p[1]) for p in peliculas]
    media_puntuaciones = mean(puntuaciones)
    plt.figure(figsize=(10, 6))
    plt.bar(titulosg, puntuaciones, color='#DCCA15')
    plt.xlabel('Títulos de Películas',fontdict={'fontname': 'IMPACT', 'fontsize': 15, 'color': '#F2DC5D'})
    plt.ylabel('Puntuación promedio', fontdict={'fontname': 'IMPACT', 'fontsize': 15, 'color': '#F2DC5D'})
    plt.title('POPULARIDAD DE LAS PELICULAS EN EL HISTORIAL', fontdict={'fontname': 'IMPACT', 'fontsize': 20, 'color': '#F2DC5D'})
    plt.xticks(rotation=45, ha='right')
    plt.axhline(media_puntuaciones, color='black', linestyle='--', linewidth=2, label=f'Media: {media_puntuaciones}')
    plt.legend()  # Muestra la leyenda
    plt.tight_layout()
    plt.savefig('graficaBHis.png')
    plt.show()
