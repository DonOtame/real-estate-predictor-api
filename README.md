# Predicción de Precios de Alquiler - Ecuador

Este proyecto utiliza Machine Learning para predecir el precio de alquiler de bienes inmuebles en Ecuador basándose en características físicas y ubicación geográfica.

## Estructura del Proyecto
* **api/**: Código fuente de la API (FastAPI).
* **static/**: Código interface html.
* **data/**: Datasets originales y procesados.
* **models/**: Modelo entrenado (.pkl).
* **notebooks/**: Análisis exploratorio y entrenamiento del modelo.

---

## Descripción de la Solución
1. **Procesamiento:** Limpieza de datos inconsistentes (ej. áreas menores a 5m²), imputación de nulos mediante la mediana y normalización de texto.
2. **Modelado:** Implementación de un `RandomForestRegressor` dentro de un `Pipeline` de Scikit-Learn que automatiza la codificación de categorías (One-Hot Encoding) y el escalado de datos.
3. **Despliegue:** API REST funcional que expone el modelo para predicciones en tiempo real.

---

## Instrucciones de Uso de la API

### Ejecución Local

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/DonOtame/real-estate-predictor-api
    cd real-estate-predictor-api
    ```

2.  **Crear y activar entorno virtual (venv):**
    * **Windows:**
        ```bash
        python -m venv venv
        source venv/Scripts/activate
        ```
    * **Mac/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Iniciar el servidor:**
    ```bash
    uvicorn api.main:app --reload
    ```

5.  **Documentación interactiva:** Accede a `http://127.0.0.1:8000/docs` para probar el endpoint directamente desde el navegador.

### URL Pública (Despliegue)
**Interface:** `https://real-estate-predictor-api-1.onrender.com`

**Documentacion:** `https://real-estate-predictor-api-1.onrender.com/docs`

**Endpoint:** `https://real-estate-predictor-api-1.onrender.com/predict`

---

## Ejemplo de Request (cURL)

```bash
curl --location 'https://real-estate-predictor-api-1.onrender.com/predict' \
--header 'Content-Type: application/json' \
--data '{
  "provincia": "Pichincha",
  "lugar": "Quito",
  "num_dormitorios": 3,
  "num_banos": 2,
  "area": 120,
  "num_garages": 1
}'
```

## Ejecución con Docker

Para garantizar la portabilidad, el proyecto incluye un `Dockerfile` que empaqueta la API y sus dependencias en un contenedor aislado.

### 1. Construir la imagen
Desde la raíz del proyecto, ejecuta:
```bash
docker build -t api-alquileres-ecuador
```
### 2. Correr el contenedor
Mapea el puerto local 8000 al puerto del contenedor:

```bash
docker run -p 8000:8000 api-alquileres-ecuador
```
### 3. Verificar
La API estará disponible en http://localhost:8000/docs con toda la documentación interactiva de FastAPI.

## Interfaz Web de Usuario

Se ha desarrollado una **Single Page Application (SPA)** moderna e integrada directamente en el servicio de FastAPI, permitiendo interactuar con el modelo de forma visual y amigable.

### Características de la Interfaz:
* **Framework CSS:** Tailwind CSS (vía Play CDN) para un diseño limpio y profesional.
* **Diseño Responsivo:** Optimizado para visualización en dispositivos móviles y escritorio.
* **Consumo Asíncrono:** Uso de `Fetch API` para comunicarse con el endpoint `/predict` sin recargar la página.

### ¿Cómo acceder?
1.  Inicia el servidor localmente o accede a la URL de Render.
2.  Navega a la raíz del proyecto: `http://localhost:8000/`
3.  Completa el formulario y presiona **"Calcular Estimación"**.
