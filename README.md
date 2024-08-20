## **_PROYECTO INDIVIDUAL 1 - MACHINE LEARNING OPERATIONS (MLOps)_**

---

## **INTRODUCCIÓN**

En este proyecto, se desarrolló un sistema de recomendación de películas mediante el análisis de datos proporcionados en un conjunto de películas. Se realizaron varias transformaciones de datos, se desarrolló una API usando FastAPI para disponibilizar los datos y consultas, y se implementó un modelo de machine learning para generar recomendaciones.

## **Objetivo**

El objetivo es transformar y limpiar los datos de películas, construir una API con FastAPI para responder a consultas específicas y entrenar un modelo de machine learning que permita recomendar películas basadas en su similitud.

## **Directorios y archivos del repositorio**

- [**Datasets**:](Datasets) Directorio donde se disponibilizan las fuentes de datos sin procesar. "movies_dataset" archivo excel / "Credits.parquet" archivo parquet.
- [**Transformaciones**:](Transformaciones) Directorio donde se disponibilizan las fuentes de datos procesadas.
- [**main.py**:](main.py) Archivo .py donde se desarrolla la API utilizando FastAPI.
- [**README**:](README.md) Archivo detallando el proyecto.
- [**Proyecto_Individual_1**:](Proyecto_Individual_1) Carpeta donde se creó el entorno virtual.
- [**__pycache__**:](__pycache__) Carpeta creada al confeccionar el entorno virtual (Mejora el rendimiento del código).
- [**requirements.txt**:](requirements.txt) Archivo para listar las dependencias del proyecto.

## **ETAPAS DEL PROYECTO**

---

### **1) Transformaciones de los datos**

Se realizaron las siguientes transformaciones clave:

- Desanidamiento de Campos --> Se desanidaron los campos "belongs_to_collection", "production_companies", entre otros, para acceder a los datos anidados.
- Manejo de Valores Nulos --> Los valores nulos en los campos "revenue" y "budget" se rellenaron con 0, mientras que los valores nulos en "release_date" fueron eliminados.
- Formateo de Fechas --> Las fechas se formatearon en AAAA-mm-dd y se creó una nueva columna "release_year" que extrae el año de la fecha de estreno.
- Cálculo de Retorno de Inversión --> Se creó la columna "return" calculando el retorno de inversión (revenue/budget), con un valor de 0 cuando faltaban datos.
- Eliminación de Columnas No Necesarias --> Se eliminaron las columnas "video", "imdb_id", "adult", "original_title", "poster_path" y "homepage" que no eran relevantes para el análisis.

### **2) Desarrollo de la API**

Se desarrollaron 6 endpoints utilizando FastAPI para disponibilizar los datos:

- **cantidad_filmaciones_mes(Mes)**: Devuelve la cantidad de películas estrenadas en un mes específico.
- **cantidad_filmaciones_dia(Dia)**: Devuelve la cantidad de películas estrenadas en un día específico.
- **score_titulo(titulo)**: Devuelve el título, año de estreno y score de una película.
- **votos_titulo(titulo)**: Devuelve el título, cantidad de votos y promedio de votaciones para películas con al menos 2000 votos.
- **get_actor(nombre_actor)**: Devuelve el éxito de un actor basado en el retorno de inversión.
- **get_director(nombre_director)**: Devuelve el éxito de un director, junto con detalles de sus películas.

### **3) Sistema de Recomendación**

Se entrenó un modelo de machine learning para recomendar películas basadas en similitud de puntuación. La función "recomendacion(titulo)" toma el nombre de una película y devuelve una lista de 5 películas similares, ordenadas por score de similitud en orden descendente.

### **4) Deployment**

El proyecto fue desplegado usando Render para que la API y el sistema de recomendación puedan ser accedidos desde la web.

## **CONCLUSIONES**

Se logró construir una API robusta capaz de responder a varias consultas sobre películas y un sistema de recomendación que ofrece sugerencias personalizadas basadas en la similitud. El análisis exploratorio permitió comprender mejor los datos, y las transformaciones aseguraron que la información esté limpia y lista para ser utilizada en aplicaciones reales.
