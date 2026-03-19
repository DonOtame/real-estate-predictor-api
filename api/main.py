from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os

app = FastAPI(
    title="Real Estate Predictor API",
    description="API para predecir precios de alquiler en Ecuador basándose en un modelo de Random Forest."
)

current_file_path = os.path.abspath(__file__)
api_dir = os.path.dirname(current_file_path)

root_dir = os.path.dirname(api_dir)
static_path = os.path.join(root_dir, "static")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
else:
    print(f"Error: No se encontró la carpeta static en {static_path}")


@app.get("/")
async def read_index():
    index_file = os.path.join(static_path, 'index.html')
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "index.html no encontrado", "path_buscado": index_file}


MODEL_PATH = os.path.join(os.path.dirname(
    __file__), "..", "models", "modelo_rf_alquileres.pkl")


model = joblib.load(MODEL_PATH)


class PredictionInput(BaseModel):
    provincia: str = Field(..., example="Pichincha")
    lugar: str = Field(..., example="Quito")
    num_bedrooms: int = Field(..., alias="num_dormitorios", example=3)
    num_bathrooms: int = Field(..., alias="num_banos", example=2)
    area: float = Field(..., example=120.0)
    num_garages: int = Field(..., example=1)

    class Config:
        populate_by_name = True


@app.post("/predict")
def predict(data: PredictionInput):
    input_df = pd.DataFrame([{
        'Provincia': data.provincia,
        'Lugar': data.lugar,
        'Num. dormitorios': data.num_bedrooms,
        'Num. banos': data.num_bathrooms,
        'Area': data.area,
        'Num. garages': data.num_garages
    }])

    prediction = model.predict(input_df)[0]
    return {"prediction": round(float(prediction), 2)}
