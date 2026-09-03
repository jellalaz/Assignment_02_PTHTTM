"""
Unified REST API & Web Server — Assignment 02
Posts and Telecommunications Institute of Technology (PTIT)
Intelligent System Development

Serves:
- REST API endpoints for Diabetes, House Price, and E-commerce predictions.
- Auto-generated Swagger documentation at /docs.
- Mobile-accessible responsive Web application at / with LAN support (0.0.0.0).
"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from api.schemas import (
    DiabetesRequest, DiabetesResponse,
    HousePriceRequest, HousePriceResponse,
    EcommerceRequest, EcommerceResponse,
    HealthCheckResponse
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
WEB_DIR = PROJECT_ROOT / "web"

# Model paths
DIABETES_MODEL_PATH = MODELS_DIR / "diabetes" / "diabetes_pipeline.joblib"
HOUSE_MODEL_PATH = MODELS_DIR / "house_price" / "house_pipeline.joblib"
ECOMMERCE_MODEL_PATH = MODELS_DIR / "ecommerce" / "ecommerce_pipeline.joblib"

loaded_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load all three ML pipelines into memory
    print("=" * 60)
    print("STARTING UNIFIED INTELLIGENT SYSTEM API SERVER...")
    print(f"Using Python: {sys.executable}")
    print("=" * 60)

    try:
        loaded_models["diabetes"] = joblib.load(DIABETES_MODEL_PATH)
        print(f"✓ Loaded Diabetes Pipeline from: {DIABETES_MODEL_PATH}")
    except Exception as e:
        print(f"✗ Failed to load Diabetes pipeline: {e}")

    try:
        loaded_models["house_price"] = joblib.load(HOUSE_MODEL_PATH)
        print(f"✓ Loaded House Price Pipeline from: {HOUSE_MODEL_PATH}")
    except Exception as e:
        print(f"✗ Failed to load House Price pipeline: {e}")

    try:
        loaded_models["ecommerce"] = joblib.load(ECOMMERCE_MODEL_PATH)
        print(f"✓ Loaded E-Commerce Pipeline from: {ECOMMERCE_MODEL_PATH}")
    except Exception as e:
        print(f"✗ Failed to load E-Commerce pipeline: {e}")

    yield

    # Shutdown
    loaded_models.clear()
    print("Server shutting down. Cleared loaded models.")


app = FastAPI(
    title="Intelligent System Development — Assignment 02 API",
    description="Unified Prediction API serving 3 Machine Learning systems (Diabetes Classification, House Price Regression, E-Commerce Customer Behavior).",
    version="1.0.0",
    lifespan=lifespan
)

# Allow CORS for LAN and multi-device access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Templates configuration
if (WEB_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(WEB_DIR / "templates"))


# ---------------------------------------------------------------------------
# Web UI Root Route
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse, summary="Responsive Web Application Dashboard")
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# ---------------------------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthCheckResponse, summary="Server Health Check")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": {
            "diabetes": "diabetes" in loaded_models,
            "house_price": "house_price" in loaded_models,
            "ecommerce": "ecommerce" in loaded_models
        }
    }


# ---------------------------------------------------------------------------
# 1. Diabetes Prediction Endpoint
# ---------------------------------------------------------------------------
@app.post("/predict/diabetes", response_model=DiabetesResponse, summary="Dự đoán bệnh tiểu đường", description="Nhận thông tin bệnh nhân và trả về kết quả dự đoán.")
async def predict_diabetes(payload: DiabetesRequest):
    if "diabetes" not in loaded_models:
        raise HTTPException(status_code=503, detail="Diabetes model pipeline is not loaded.")

    try:
        input_data = pd.DataFrame([{
            "gender": payload.gender,
            "age": payload.age,
            "hypertension": payload.hypertension,
            "heart_disease": payload.heart_disease,
            "smoking_history": payload.smoking_history,
            "bmi": payload.bmi,
            "HbA1c_level": payload.HbA1c_level,
            "blood_glucose_level": payload.blood_glucose_level
        }])

        model = loaded_models["diabetes"]
        pred = int(model.predict(input_data)[0])
        prob = float(model.predict_proba(input_data)[0][1])

        diagnosis = "Có nguy cơ mắc bệnh tiểu đường (Rủi ro cao)" if pred == 1 else "Không thuộc nhóm mắc bệnh (Rủi ro thấp)"
        risk = "Cao" if prob >= 0.7 else ("Trung bình" if prob >= 0.3 else "Thấp")

        return {
            "prediction": pred,
            "diagnosis": diagnosis,
            "probability": round(prob, 4),
            "risk_level": risk
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


# ---------------------------------------------------------------------------
# 2. House Price Prediction Endpoint
# ---------------------------------------------------------------------------
@app.post("/predict/house", response_model=HousePriceResponse, summary="Dự đoán giá nhà", description="Nhận thông tin bất động sản và trả về giá trị thị trường dự đoán.")
async def predict_house_price(payload: HousePriceRequest):
    if "house_price" not in loaded_models:
        raise HTTPException(status_code=503, detail="House price model pipeline is not loaded.")

    try:
        input_data = pd.DataFrame([{
            "Area": payload.Area,
            "Bedrooms": payload.Bedrooms,
            "Bathrooms": payload.Bathrooms,
            "Stories": payload.Stories,
            "Parking": payload.Parking,
            "Age": payload.Age,
            "City": payload.City,
            "Furnishing": payload.Furnishing,
            "Main Road": payload.Main_Road,
            "Guest Room": payload.Guest_Room,
            "Basement": payload.Basement,
            "Water Supply": payload.Water_Supply,
            "Air Conditioning": payload.Air_Conditioning,
            "Preferred Tenant": payload.Preferred_Tenant,
            "Locality Rating": payload.Locality_Rating
        }])

        model = loaded_models["house_price"]
        pred_price = float(model.predict(input_data)[0])

        return {
            "predicted_price": round(pred_price, 2),
            "formatted_price": f"${pred_price:,.2f}",
            "currency": "USD"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


# ---------------------------------------------------------------------------
# 3. E-Commerce Customer Behavior Prediction Endpoint
# ---------------------------------------------------------------------------
@app.post("/predict/ecommerce", response_model=EcommerceResponse, summary="Dự đoán đề xuất sản phẩm", description="Dự đoán khả năng khách hàng sẽ đề xuất sản phẩm dựa trên nội dung đánh giá và thông tin khác.")
async def predict_ecommerce(payload: EcommerceRequest):
    if "ecommerce" not in loaded_models:
        raise HTTPException(status_code=503, detail="E-Commerce model pipeline is not loaded.")

    try:
        full_review = payload.Review_Text.strip()

        input_data = pd.DataFrame([{
            "Age": payload.Age,
            "Rating": payload.Rating,
            "Positive Feedback Count": payload.Positive_Feedback_Count,
            "Division Name": payload.Division_Name,
            "Department Name": payload.Department_Name,
            "Class Name": payload.Class_Name,
            "full_review": full_review
        }])

        model = loaded_models["ecommerce"]
        pred = int(model.predict(input_data)[0])
        prob = float(model.predict_proba(input_data)[0][1])

        label = "Khách hàng có khả năng đề xuất sản phẩm" if pred == 1 else "Khách hàng có khả năng không đề xuất sản phẩm"
        sentiment = "Tích cực" if prob >= 0.6 else ("Tiêu cực" if prob <= 0.4 else "Trung tính")

        return {
            "recommended": pred,
            "recommendation_label": label,
            "confidence": round(prob, 4),
            "sentiment_hint": sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    # Bind to 0.0.0.0 to enable LAN mobile device access
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
