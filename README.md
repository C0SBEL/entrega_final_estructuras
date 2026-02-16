# Proyecto final: Estructuras de datos y su almacenamiento

## Estructura del Proyecto

```
project/
│
├── src/
│   ├── db/
│   │   └── MovieDatabase.py        # Gestión y acceso a la base de datos de películas (MongoDB)
│   │
│   ├── etl/
│   │   ├── Extract.py              # Extracción de datos desde Kaggle
│   │   ├── Transform.py            # Transformación y limpieza de datos
│   │   └── Load.py                 # Carga de datos en MongoDB
│
├── analysis/
│   └── EntregaFinal.ipynb          # Notebook con preparación de datos, limpieza, EDA, modelado y evaluación
│
├── .env                             # Variables de entorno para conexión a MongoDB
├── main.py                           # Script principal para ejecutar ETL completo
├── README.md
└── requirements.txt                 # Dependencias necesarias
```

> Todos los directorios dentro de `src/` son paquetes Python, mientras que `analysis/` contiene únicamente el notebook.

---

## Tecnologías y librerías

- Python 3.10+
- Polars para manipulación eficiente de DataFrames y LazyFrames.
- pandas para compatibilidad y transformación de datos.
- H2O AutoML para modelado predictivo.
- MongoDB como base de datos NoSQL para almacenamiento de películas, géneros, compañías, idiomas y países.
- pymongo para conexión con MongoDB.
- kagglehub para descarga y carga de datasets desde Kaggle.
- Jupyter Notebook para análisis exploratorio y visualización de datos.
- NumPy / SciPy para operaciones numéricas.

---

## Descripción de paquetes y archivos

### `src.db`
Contiene la lógica de acceso a la base de datos MongoDB.

- `MovieDatabase.py`
  - Funciones para conectar, consultar, insertar y actualizar registros de películas, géneros, compañías, idiomas y países.
  - Usa índices únicos para garantizar consistencia de datos.
  - Ejemplo de uso:
    ```python
    from src.db.MovieDatabase import MovieDatabase

    db = MovieDatabase()  # Usa URI y DB por defecto de .env
    movies = db.movies.find({})
    ```

### `src.etl`
Contiene el pipeline ETL.

- `Extract.py`  
  - Clase `Extractor` para extraer datasets desde Kaggle usando `kagglehub`.
  - Permite limitar el número de filas para pruebas rápidas.
- `Transform.py`  
  - Clase `Transformer` para limpiar, transformar y mapear campos complejos (géneros, idiomas, compañías, países) a IDs.
- `Load.py`  
  - Clase `Loader` para insertar datos transformados en MongoDB.
  - Convierte LazyFrames de Polars a DataFrames y luego a diccionarios para insertar en la base de datos.

### `analysis/`
Contiene el notebook principal.

- `EntregaFinal.ipynb`  
  - Preparación de datos: limpieza, transformación y feature engineering.  
  - EDA (Exploratory Data Analysis): estadísticas descriptivas y visualizaciones.  
  - Modelado: predicción de ingresos (`revenue`) usando H2O AutoML.  
  - Evaluación: métricas de desempeño y comparación de modelos.

### `main.py`
Script principal que ejecuta todo el pipeline ETL completo: extracción, transformación y carga en MongoDB.

### `.env`
Variables de entorno para la conexión a MongoDB:

```
MONGO_URI=mongodb://localhost:59130/
MONGO_DB=tmdb_movies_db
PYTHON_ENV=development
```

---

## Cómo ejecutar el proyecto

1. Clonar el repositorio
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd project
   ```

2. Instalar dependencias
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar MongoDB
   - Asegúrate de que MongoDB esté corriendo en el puerto indicado en `.env` (por defecto 59130).

4. Ejecutar ETL completo
   ```bash
   python main.py
   ```

5. Ejecutar el notebook para análisis
   ```bash
   jupyter notebook analysis/EntregaFinal.ipynb
   ```

---

## Requisitos (`requirements.txt`)

```
polars>=0.19.12
pandas>=2.1.0
numpy>=1.25.0
scipy>=1.11.1
pymongo>=4.6.1
h2o>=3.44.0.4
kagglehub>=0.1.13
python-dotenv>=1.0.0
jupyter>=1.0.0
```

