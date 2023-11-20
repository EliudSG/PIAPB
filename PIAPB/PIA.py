from statistics import mode,mean
from EXCELPIA import Excel
import matplotlib.pyplot as plt
import FUNCIONESPIA as fu
import requests
import os
import json
import re
import time
import sys

def excepcionesArch(nomarch): #FUNCION DE EXPECIONES PARA ARCHIVOS. ELIUD   
    if os.path.exists(nomarch):
        with open(nomarch, 'a') as archivo:
            pass
    else:
        with open(nomarch, 'w') as archivo:
            pass      
    if os.path.exists(peliculasvistas):
        with open(peliculasvistas, 'a') as archivo:
            pass
    else:
        with open(peliculasvistas, 'w') as archivo:
            pass

#APERTURA DE LA API 
api_key = "e25ee42fc20bdb2cb85163cd2998b7a1"

url_generos = "https://api.themoviedb.org/3/genre/movie/list"
params_generos = {
    "api_key": api_key
}

'''url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwOTA2Mzk0OWI3YzVlYjE5ZGNlNGNiOGRiNjA2NzhlNiIsInN1YiI6IjY1MzFjMTRiOWFjNTM1MDg3NTJlZWRkMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.LLAwL5d_RGQ92-qyV3cl5zYjW8xxXM401290hooJz9o"
}

response = requests.get(url, headers=headers)
data = json.loads(response.text)'''

response_generos = requests.get(url_generos, params=params_generos)



#MENU Y CODIGO DEL PROGRAMA
if __name__ == "__main__":
    archH = "Historial.txt"
    peliculasvistas = "películasvistas.txt"
    excepcionesArch(archH)   

    menu = '''1) BÚSQUEDA
2) HISTORIAL
3) VER PELICULAS TRENDING
4) SALIR'''

    menu2 = '''1) POR NOMBRE
2) POR GÉNERO
3) REGRESAR AL MENU PRINCIPAL'''

    menu3 = '''1) VER HISTORIAL
2) BORRAR HISTORIAL
3) PELICULAS VISTAS
4) BORRAR PELICULAS VISTAS
5) REGRESAR AL MENU PRINCIPAL'''

    while True:
        
        print("-----------------------MENÚ-----------------------\n", menu, "\n")
        numE = fu.excepcionesEnt("INGRESE LA OPCIÓN QUE DESEA: ")

        if numE == 1:
            while True:
                
                print("-----------------------BÚSQUEDA-----------------------\n", menu2, "\n")
                numE2 = fu.excepcionesEnt("INGRESE LA OPCIÓN QUE DESEA: ")

                if numE2 == 1:  # BUSQUEDA POR NOMBRE
                    nom_apikey = "e25ee42fc20bdb2cb85163cd2998b7a1"
                    nombre_peli = input("Escribe el nombre de la película que deseas buscar: ")
                    url_ini = "https://api.themoviedb.org/3/"
                    finurl = "search/movie"
                    params = {
                        "api_key": nom_apikey,
                        "query": nombre_peli
                    }
                    response = requests.get(url_ini + finurl, params=params)

                    if response.status_code == 200:
                        data = response.json()
                        #pprint.pprint(data)
                        longi_de_result = data["total_results"]
                        if longi_de_result !=0:    
                            titulos = data['results']
                            result_titu = list()
                            lista_de_id = list()
                            for title in titulos:
                                result_titu.append(title["title"])
                                lista_de_id.append(title["id"])
                            i = 0
                            for i in range(len(result_titu)):
                                pelicula = data['results'][i]
                                titulo = pelicula['title']
                                año = pelicula['release_date'].split('-')[0]
                                print(f'{i + 1}. {titulo} ({año})')
                            elección_correc = fu.excepVa_RANG_Y_ENT("Ingresa la opción que estás buscando: ", len(result_titu))
                            tit_Ele_Co = result_titu[elección_correc - 1]
                            titulos_coid = lista_de_id[elección_correc -1]
                            titulos_coid = str(titulos_coid)
                            url_ini = "https://api.themoviedb.org/3/movie/"
                            params = {
                                "api_key": nom_apikey,
                                "query": titulos_coid
                    }
                            url_fin = "https://api.themoviedb.org/3/movie/" + titulos_coid
                            response = requests.get(url_fin, params=params)
                            data = json.loads(response.text)
                            print(f'Título: {data["title"]}')
                            generos_de_peli = list()
                            for genero in data['genres']:
                                generos_de_peli.append(genero["name"])
                            print("Géneros: ")
                            for x in generos_de_peli:
                                print("-", x)
                            print(f'ID de la película: {data["id"]}')
                            print(f'Fecha de lanzamiento: {data["release_date"]}')
                            print(f'Puntuación promedio: {data["vote_average"]}')
                            print(f'Resumen: {data["overview"]}')

                            infope = {
                                "Título": data["title"],
                                "ID de la película": data["id"],
                                "Fecha de lanzamiento": data["release_date"],
                                "Puntuación promedio": data["vote_average"],
                            }
                            Excel(infope["Título"],
                                    infope["ID de la película"],
                                    infope["Fecha de lanzamiento"],
                                    infope["Puntuación promedio"])
                        
                            respuestaa_vistaa = fu.preg_peli_vista()

                            #Guardar en el historial de búsqueda.

                            

                            with open("historial.txt", "a") as archivo:
                                archivo.write(f"Información de la película seleccionada:\n")
                                archivo.write(f'Título: {data["title"]}\n')
                                archivo.write(f'ID de la película: {data["id"]}\n')
                                archivo.write(f'Fecha de lanzamiento: {data["release_date"]}\n')
                                archivo.write(f'Puntuación promedio: {data["vote_average"]}\n')
                                archivo.write(f'Resumen: {data["overview"]}\n')
                                archivo.write('-' * 50 + '\n')
                            #Mandar película vista a un archivo
                            if respuestaa_vistaa == "si":
                                with open("películasvistas.txt", "a") as vistas:
                                    vistas.write(f"Información de la película seleccionada:\n")
                                    vistas.write(f'Título: {data["title"]}\n')
                                    generos_str = ', '.join(generos_de_peli)
                                    vistas.write(f'Géneros: {generos_str}\n')    
                                    vistas.write(f'ID de la película: {data["id"]}\n')
                                    vistas.write(f'Fecha de lanzamiento: {data["release_date"]}\n')
                                    vistas.write(f'Puntuación promedio: {data["vote_average"]}\n')
                                    vistas.write(f'Resumen: {data["overview"]}\n')
                                    vistas.write('-' * 50 + '\n') 
                            else:
                                print("No se guardó en el historial.")
                                
                        else:
                            print("No hay coincidencias")
                            pass
                elif numE2 == 2:  # BUSQUEDA POR GÉNERO
                    if response_generos.status_code == 200:
                        data_generos = response_generos.json()
                        genres = data_generos['genres']

                        # Muestra lista de géneros
                        print("Lista de géneros:")
                        for i, genre in enumerate(genres, start=1):
                            print(f"{i}. {genre['name']}")

                        eleccion_genero = fu.excepVaENT("Selecciona el número del género que deseas buscar: ", 19)
                        genre_elegido = genres[eleccion_genero - 1]['id']

                        url_ini = "https://api.themoviedb.org/3/discover/movie"
                        params = {
                            "api_key": api_key,
                            "with_genres": genre_elegido
                        }

                        response = requests.get(url_ini, params=params)
                        if response.status_code == 200:
                            data = response.json()
                            movies = data['results']

                            # Muestra lista de películas
                            print("\nLista de películas:")
                            for i, movie in enumerate(movies, start=1):
                                print(f"{i}. {movie['title']}")

                            eleccion_pelicula = fu.excepVaENT("\nSelecciona el número de la película que deseas ver: ", 20)
                            
                            if 0 < eleccion_pelicula <= len(movies):
                                pelicula_elegida = movies[eleccion_pelicula - 1]
                                print('---------------------------------------------------')
                                print("\nInformación de la película seleccionada:")
                                print(f'Título: {pelicula_elegida["title"]}')
                                print(f'ID de la película: {pelicula_elegida["id"]}')
                                print(f'Fecha de lanzamiento: {pelicula_elegida["release_date"]}')
                                print(f'Puntuación promedio: {pelicula_elegida["vote_average"]}')
                                print(f'Resumen: {pelicula_elegida["overview"]}')
                                print('\n---------------------------------------------------')
                            # Guardar las impresiones en el archivo "historial"
                            infope = {
                                "Título": pelicula_elegida["title"],
                                "ID de la película": pelicula_elegida["id"],
                                "Fecha de lanzamiento": pelicula_elegida["release_date"],
                                "Puntuación promedio": pelicula_elegida["vote_average"],
                            }
                            Excel(infope["Título"],
                              infope["ID de la película"],
                              infope["Fecha de lanzamiento"],
                              infope["Puntuación promedio"])
                                  
                            with open("historial.txt", "a") as archivo:
                                archivo.write(f"Información de la película seleccionada:\n")
                                archivo.write(f'Título: {pelicula_elegida["title"]}\n')
                                archivo.write(f'ID de la película: {pelicula_elegida["id"]}\n')
                                archivo.write(f'Fecha de lanzamiento: {pelicula_elegida["release_date"]}\n')
                                archivo.write(f'Puntuación promedio: {pelicula_elegida["vote_average"]}\n')
                                archivo.write(f'Resumen: {pelicula_elegida["overview"]}\n')
                                archivo.write('-' * 50 + '\n')
                        else:
                            print("El número de película seleccionado no es válido.\n")
                    pass
                elif numE2 == 3:
                    break
                else:
                    print("NUMERO NO VALIDO, VUELVA A INGRESAR...\n")
        elif numE == 2:

            while True:
                
                print("-----------------------HISTORIAL-----------------------\n", menu3, "\n")
                numE2 = fu.excepcionesEnt("INGRESE LA OPCIÓN QUE DESEA: ")

                if numE2 == 1:  # VISTA DEL HISTORIAL
                    with open("historial.txt", 'r') as archivo :
                        print (archivo.read())
                        # Llamamos a la función para generar el gráfico de pastel
                        #archivo_peliculas_vistas = "películasvistas.txt"  
                        #fu.grafico_pastel_generos_historial(archivo_peliculas_vistas)

                        archivo_historial = "historial.txt"  
                        fu.grafico_barras_puntuacion_historial(archivo_historial)
                elif numE2 == 2:  # ELIMINAR HISTORIAL

                    borrarhisto=fu.excepcionesEnt("¿Seguro que desea Eliminar el Historial? 1)SI 2):NO: ")
                    
                    if borrarhisto==1:
                        fu.limppantalla()
                        print("Borrando...")
                        with open(archH, 'w') as archivo:
                            pass
                        time.sleep(2)
                        fu.limppantalla()
                        print("¡¡Se borro con exito!!\n")
                        time.sleep(2)

                    elif borrarhisto==2:
                        print("No se borro el historial.")
                    
                    else:
                        print ("\n**Numero no valido**\n")
                elif numE2 == 3:
                    with open("películasvistas.txt", 'r') as visualizaciones :
                        print (visualizaciones.read())  
                        # Llamamos a la función para generar el gráfico de pastel
                        archivo_peliculas_vistas = "películasvistas.txt"  
                        fu.grafico_pastel_generos_historial(archivo_peliculas_vistas)
                elif numE2 == 4:
                    borrarhisto=fu.excepcionesEnt("¿Seguro que desea Eliminar el Historial de Peliculas Vistas? 1)SI 2):NO: ") 
                    if borrarhisto==1:
                        fu.limppantalla()
                        print("Borrando...")
                        with open("películasvistas.txt", 'w') as archivo:
                            pass
                        time.sleep(2)
                        fu.limppantalla()
                        print("¡¡Se borro con exito!!\n")
                        time.sleep(2)
                    elif borrarhisto==2:
                        print("No se borro el historial.")       
                    else:
                        print ("\n**Numero no valido**\n")

                elif numE2 == 5:
                    break
        
        elif numE == 3:
            #if 'results' in data:
                url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

                headers = {
                            "accept": "application/json",
                            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwOTA2Mzk0OWI3YzVlYjE5ZGNlNGNiOGRiNjA2NzhlNiIsInN1YiI6IjY1MzFjMTRiOWFjNTM1MDg3NTJlZWRkMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.LLAwL5d_RGQ92-qyV3cl5zYjW8xxXM401290hooJz9o"
                            }
                response = requests.get(url, headers=headers)
                data = json.loads(response.text)
                
                titulos = list()
                popular = list()

                for pelicula in data['results']:
                    titulos.append(pelicula["title"])
                    popular.append(pelicula['vote_average'])
                    print('Título:', pelicula["title"])
                    print('Fecha de Esteno', pelicula['release_date'])
                    print('Sinopsis:', pelicula['overview'])
                    print('Popularidad:', pelicula['vote_average'])
                    print('-'*30)
                
                moda_popular= (mode(popular))
                plt.figure(figsize=(10, 6))  # Ajustar el tamaño de la figura
                plt.bar(titulos, popular, color='#33E9FF')
                plt.xlabel('Títulos de Películas', fontdict={'fontname': 'Lucida Sans Unicode', 'fontsize': 20, 'color': '#744AB2'})
                plt.ylabel('Popularidad', fontdict={'fontname': 'Lucida Sans Unicode', 'fontsize': 20, 'color': '#744AB2'})
                plt.title('Popularidad de Películas', fontdict={'fontname': 'IMPACT', 'fontsize': 20, 'color': '#3D90DA'})
                plt.xticks(rotation=45, ha='right')  # Rotar las etiquetas del eje x para mejor visibilidad
                plt.tight_layout()  # Ajustar el diseño de la figura para evitar cortes
                plt.axhline(moda_popular, color='black', linestyle='--', linewidth=2, label=f'Moda: {moda_popular}')
                plt.legend()  # Muestra la leyenda
                plt.tight_layout()
                plt.savefig('graficaBPoP.png')
                plt.show()
            #else:
               # print("No se encontraron resultados en la respuesta de la API.")

        elif numE == 4:
            fu.limppantalla()
            print("Vuelva Pronto!!!!")
            break
