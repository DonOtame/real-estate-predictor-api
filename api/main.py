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

script_dir = os.path.dirname(__file__)
static_path = os.path.join(script_dir, "..", "static")

app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, 'index.html'))

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
