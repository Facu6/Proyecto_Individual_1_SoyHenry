# Proyecto Individual 1 - SoyHenry
Este es el primer proyecto individual realizado como parte del curso de SoyHenry. A continuación, se describen las tareas realizadas y los objetivos alcanzados.

### Transformaciones de Datos
Para preparar los datos para su análisis y uso en una API, se realizaron las siguientes transformaciones:

- Desanidado de Campos: Se desanidaron campos como belongs_to_collection y production_companies para facilitar el acceso y análisis. Se buscaron métodos alternativos para manejar estos datos sin desanidarlos completamente.

- Relleno de Valores Nulos:
Los campos revenue y budget con valores nulos se rellenaron con 0.
Los registros con valores nulos en release_date fueron eliminados.

- Formateo de Fechas: Se formatearon las fechas en AAAA-mm-dd y se creó la columna release_year extrayendo el año de la fecha de estreno.

- Cálculo del Retorno de Inversión: Se añadió una columna return, calculada como revenue / budget, asignando 0 cuando los datos eran insuficientes.

- Eliminación de Columnas Innecesarias: Se eliminaron las columnas video, imdb_id, adult, original_title, poster_path y homepage que no eran relevantes para el análisis.

### Desarrollo de la API
Se desarrolló una API utilizando el framework FastAPI para proporcionar acceso a los datos transformados. Los endpoints creados son los siguientes:

- Cantidad de Filmaciones por Mes

- Cantidad de Filmaciones por Día

- Score por Título

- Votos por Título

- Información de Actor

- Información de Director

### Despliegue
La API se puede desplegar en servicios como Render o Railway para que sea accesible desde la web.

### Análisis Exploratorio de Datos (EDA)
Se realizó un análisis exploratorio de los datos (EDA) para investigar relaciones entre variables, identificar outliers y descubrir patrones interesantes. 

### Sistema de Recomendación
Se implementó un sistema de recomendación de películas utilizando un modelo de machine learning basado en K Vecinos Más Cercanos (KNN). El modelo se entrenó con la métrica "cosine" y el algoritmo "brute". Este modelo encuentra similitudes entre películas y recomienda las más similares. La función recomendacion devuelve una lista de 5 películas con mayor similitud al título ingresado.


## ¡Gracias por revisar este proyecto!