# Se importa módulo "FastAPI"
from fastapi import FastAPI
# Se importa pandas
import pandas as pd
# Se importa módulo "warnings" para que no aparezcan dichos mensaje
import warnings
warnings.filterwarnings("ignore")

# Se importa el csv "Movies" con sus correspondientes transformaciones
movies_funciones = pd.read_csv("Movies_Transformaciones.csv")



# Se eliminan valores nulos y se convierte a datetime 
movies_funciones = movies_funciones.dropna(subset= ['release_date']).reset_index(drop = True)
movies_funciones['release_date'] = pd.to_datetime(movies_funciones['release_date'], format='%Y-%m-%d', errors='coerce')

# Se instancia "FastAPI"
app = FastAPI()

# Dirección: http://127.0.0.1:8000/


#                                               ----> 1) SE CREA LA FUNCIÓN "cantidad_filmaciones_mes(Mes)" <----
@app.get('/cantidad_filmaciones_mes/{Mes}')
def cantidad_filmaciones_mes(Mes):
    
    # Creamos diccionario con los meses en español 
    meses_a_numero = {'enero' : 1, 
                    'febrero' : 2,
                    'marzo' : 3,
                    'abril' : 4,
                    'mayo' : 5,
                    'junio' : 6,
                    'julio' : 7,
                    'agosto' : 8,
                    'septiembre' : 9,
                    'octubre' : 10,
                    'noviembre' : 11,
                    'diciembre': 12}
    
    # El valor de entrada se pasa a minúscula para mejor manejo
    Mes = Mes.lower()
    
    # Se crea la variable "dias_semana" la cual toma el diccionario de dias y constata que dicho dia ingresado se 
    # encuentre en el diccionario, caso contrario devuelve None
    mes_numero = meses_a_numero.get(Mes, None)
    if mes_numero is None:  # En caso de ser None, retorna "Día no válido"
        return {'Error' : 'Mes no válido'}
    
    # Se realiza un filtro con la columna "release_date", y con el módulo dayofweek, se constata el día de la semana ingresado
    peliculas_mes = movies_funciones[movies_funciones['release_date'].dt.month == mes_numero]
    
    # Retorna la cantidad de películas estrenadas en un día determinado de la semana
    return {'cantidad' : len(peliculas_mes)}





#                                               ----> 2) SE CREA LA FUNCIÓN  "cantidad_filmaciones_dia(Dia)" <----

@app.get('/cantidad_filmaciones_dia/{Dia}')
def cantidad_filmaciones_dia(Dia):
    
    dias_semana_diccionario = {'lunes':0,   # Se crea un diccionario para mappear los días de la semana y sus variaciones con y sin tilde
                     'martes':1, 
                     'miercoles':2,
                     'miércoles':2, 
                     'jueves':3, 
                     'viernes':4, 
                     'sabado':5,
                     'sábado': 5, 
                     'domingo':6}
    Dia = Dia.lower()   # El valor de entrada se pasa a minúscula para mejor manejo
    
    dias_semana = dias_semana_diccionario.get(Dia, None)    # Se crea la variable "dias_semana" la cual toma el diccionario de dias y constata que dicho dia ingresado se encuentre en el diccionario, caso contrario devuelve None
    if dias_semana is None: # En caso de ser None, retorna "Día no válido"
        return {'Error' : 'Día no válido'}
    
    
    peliculas_dia = movies_funciones[movies_funciones['release_date'].dt.dayofweek == dias_semana]  # Se realiza un filtro con la columna "release_date", y con el módulo dayofweek, se constata el día de la semana ingresado
    
    return {'cantidad' : len(peliculas_dia)} # Retorna la cantidad de películas estrenadas en un día determinado de la semana



#                                               ----> 3) SE CREA LA FUNCIÓN  "score_titulo(titulo)" <----

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo):

    titulo = titulo.lower() # El valor de entrada se pasa a minúscula para mejor manejo
    
    peliculas_filtradas = movies_funciones.loc[movies_funciones['title'].str.lower() == titulo] # Se realiza el filtro de el título ingresado por el usuario con los titulos del DataFrame
    
    
    # Se utilizan condicionales
    if peliculas_filtradas.empty: # Si "peliculas_filtras" se encuentra vacío, devuelve "Título No Encontrado"
        return {'Error' : 'Titulo No Encontrado'}
    else:  # Si se encuentra el título se itera en un bucle for para el caso de los títulos que repiten su nombre pero distintas películas y se agregan a una lista 
        resultados = []
        
        # Se realiza un bucle "for" ya que hay titulos que repiten su nombre
        for _, fila in peliculas_filtradas.iterrows():
            resultados.append({
                'Titulo': fila['title'],
                'Año de Estreno': fila['release_year'],
                'Popularidad': fila['popularity']
            })
        
        return resultados # Retorna la lista "resultados"
    


#                                               ----> 4) SE CREA LA FUNCIÓN  "votos_titulo(titulo_filmacion)" <----


@app.get('/votos_titulo/{titulo_filmacion}')
def votos_titulo(titulo_filmacion):
    
    titulo_filmacion = titulo_filmacion.lower() # El valor de entrada se pasa a minúscula para mejor manejo
    
    peliculas_filtradas = movies_funciones.loc[movies_funciones['title'].str.lower() == titulo_filmacion] # Se realiza el filtro de el título ingresado por el usuario con los titulos del DataFrame

    
    # Se utilizan condicionales
    if peliculas_filtradas.empty: # Si "peliculas_filtras" se encuentra vacío, devuelve "Título No Encontrado"
        return {'Error' : 'Titulo No Encontrado'}
    else: 
        peliculas_cantidad_votos = peliculas_filtradas[peliculas_filtradas['vote_count'] >= 2000] # Se realiza un filtro para dar con las películas que cuentan con más de 2000 valoraciones
        if peliculas_cantidad_votos.empty: # Si la variable "peliculas_cantidad_votos" se encuentra encuentra vacía, tiene menos de 2000 valoraciones y devuelve mensaje de error 
            return {'Error' : 'La película cuenta con menos de 2000 valoraciones. Ingrese un título que cumpla dicha condición'}
        else: # En el caso de cumplir con el filtro devuelve "Título", "Año Estreno (con motivo de especificar que hay titulos repetidos pero son distintas películas)", "Cantidad Votos", "Valor Promedio Votaciones"
        
            resultados = []
            
            for _, fila in peliculas_cantidad_votos.iterrows(): # Se realiza un bucle for sobre la variable "peliculas_cantidad_votos" ya que es donde se aplicó el filtro de valoraciones
                resultados.append({
                    'Titulo': fila['title'],
                    'Año Estreno' : fila['release_year'],
                    'Cantidad Votos': fila['vote_count'],
                    'Valor Promedio de Votaciones': fila['vote_average']
                })
                        
            return resultados
        
        
        

#                                               ----> 5) SE CREA LA FUNCIÓN  "get_actor(nombre_actor)" <----


# Ya que las siguientes 2 funciones requieren datos del csv "credits", se procede a importar el mismo
credits_funciones = pd.read_csv("Credits_Transformaciones.csv")

import numpy as np

# Se reemplazan valores  "-inf" y "Nan" de la columna "return (porcent)" del dataframe "Movies_Funciones"
movies_funciones['return (porcent)'].fillna(0, inplace = True)
movies_funciones['return (porcent)'].replace(-np.inf, 0, inplace = True)



# SE CREA LA FUNCIÓN 

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor): 
    
    # Se establece el mismo tipo de dato para las columnas "id_ORIGINAL" de ambos dataframe
    credits_funciones['id_ORIGINAL'] = credits_funciones['id_ORIGINAL'].astype(str)
    movies_funciones['id_ORIGINAL'] = movies_funciones['id_ORIGINAL'].astype(str)
    
    # El valor de entrada se pasa a minúscula para mejor manejo
    nombre_actor = nombre_actor.lower()
    
    # Se realiza el filtro de el título ingresado por el usuario con los titulos del DataFrame
    actor_filtrado = credits_funciones.loc[credits_funciones['Actores'].str.lower().str.contains(nombre_actor)] # Se realiza el filtro de el título ingresado por el usuario con los titulos del DataFrame

    
    if actor_filtrado.empty: # Si "actor_filtrado" se encuentra vacío, devuelve "Actor No Encontrado"
        return {'Error' : 'Actor No Encontrado'}
    else: # Caso contrario:
        
        # Une ambos dataframe por la columna "id_ORIGINAL"
        peliculas_actor = pd.merge(actor_filtrado, movies_funciones, on = 'id_ORIGINAL')
        
        # Calcula la cantidad total de películas en las que trabajó el actor
        cantidad_peliculas = len(peliculas_actor)
        
        # Calcula el promedio del retorno de las películas 
        promedio_retorno = (peliculas_actor['return (porcent)'].sum()) / cantidad_peliculas
        
        # Calcula el éxito del actor sumando el retorno de las películas
        exito_actor = peliculas_actor['return (porcent)'].sum()
        
        
        # Retorna el diccionario con dichos datos
        return {'Actor' : nombre_actor, 'Cantidad Peliculas' : cantidad_peliculas, 'Éxito Actor' : exito_actor, 'Promedio Retorno de Películas' : promedio_retorno}





#                                               ----> 6) SE CREA LA FUNCIÓN  "get_director(nombre_director)" <----



@app.get('/get_director/{nombre_director}')
def get_director(nombre_director):
    
    # Se establece el mismo tipo de dato para las columnas "id_ORIGINAL" de ambos dataframe
    credits_funciones['id_ORIGINAL'] = credits_funciones['id_ORIGINAL'].astype(str)
    movies_funciones['id_ORIGINAL'] = movies_funciones['id_ORIGINAL'].astype(str)
    
    
    # El valor de entrada se pasa a minúscula para mejor manejo
    nombre_director = nombre_director.lower()
    
    # Se realiza el filtro de el director ingresado por el usuario con los directores del DataFrame
    director_filtrado = credits_funciones.loc[credits_funciones['Director'].str.lower().str.contains(nombre_director)] 

    if director_filtrado.empty: # Si "director_filtrado" se encuentra vacío, devuelve Director No Encontrado"
        return {'Error' : 'Director No Encontrado'}
    
    else: # Caso contrario:
                
        # Une ambos dataframe por la columna "id_ORIGINAL"
        peliculas_director = pd.merge(director_filtrado, movies_funciones, on = 'id_ORIGINAL')
        
        # Calcula el éxito del director sumando el retorno de las películas
        exito_director = peliculas_director['return (porcent)'].sum()

        # Se extraen los títulos de las películas
        nombre_peliculas = peliculas_director['title'].tolist() # El método ".tolist()" convierte los valores en listas
        
        # Se extrae la fecha de lanzamiento
        fecha_lanzamiento = peliculas_director['release_date'].astype(str).tolist()
        
        # Se extrae el retorno individual 
        retorno_individual = peliculas_director['return (porcent)'].tolist()
        
        # Se extrae el costo
        costo = peliculas_director['budget'].tolist()
        
        # Se extrae la ganancia
        ganancia = peliculas_director['revenue'].tolist()
        
        
        # Se crea una lista donde se guardarán la información de cada película en formato "diccionario"
        peliculas_info = []
    for i in range(len(nombre_peliculas)): # El bucle "for" itera desde "0" hasta el útlimo índice de "nombre_peliculas"
        peliculas_info.append({ 
            'Título': nombre_peliculas[i],
            'Fecha Lanzamiento': fecha_lanzamiento[i],
            'Retorno Individual': retorno_individual[i],
            'Costo': costo[i],
            'Ganancia': ganancia[i]})
    
    # Retorna los valores detallados 
    return {'Director': nombre_director,
        'Éxito Director': exito_director,
        'Películas': peliculas_info}
<<<<<<< HEAD
    
    
    
    
#                                               ----> 7) SE CREA LA FUNCIÓN  "recomendacion(titulo, n_recomendaciones=5)" <----



import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Leer el DataFrame
movies_ml = pd.read_csv('Dataframe_movies_ml')

# Definir las columnas de características
feature_columns = ['runtime', 'vote_average', 'vote_count', 'release_year', 'original_language1', 'popularity1']

# Definir las características para el entrenamiento del modelo
train_features = movies_ml[feature_columns]
titles = movies_ml['title']  # Almacenar los títulos para el uso posterior

# Instanciar y entrenar el modelo KNN
knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
knn_model.fit(train_features)

@app.get('/recomendacion/{titulo}')
def recomendacion(titulo):
    # Obtener las características de la película
    if titulo not in titles.values:
        return {'Error': 'Película No Encontrada'}

    movie_features = movies_ml[movies_ml['title'] == titulo][feature_columns]
    
    if movie_features.empty:
        return {'Error': 'Película No Encontrada'}

    # Obtener la similitud
    distances, indices = knn_model.kneighbors(movie_features, n_neighbors=6)
    
    # Extraer las 5 películas más similares (excluyendo la misma película)
    similar_indices = indices.flatten()[1:]  # Excluye la película misma
    similar_movies = movies_ml.iloc[similar_indices]
    
    # Limitar las recomendaciones a las 5 primeras
    recommended_titles = similar_movies['title'].head(5).tolist()

    return {'Recomendación': recommended_titles}
=======
>>>>>>> c01d6efabf0fe67d02a8016aefe79cacb413aeff
