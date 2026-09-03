"""
Pydantic Schemas for Request and Response Validation (Pydantic v2 compliant)
Unified REST API — Assignment 02
"""

from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------------------------
# 1. Diabetes Prediction Schemas
# ---------------------------------------------------------------------------
class DiabetesRequest(BaseModel):
    gender: Literal["Female", "Male", "Other"] = Field(..., description="Biological sex of patient")
    age: float = Field(..., ge=0.0, le=120.0, description="Age in years")
    hypertension: Literal[0, 1] = Field(..., description="0 = No hypertension, 1 = Has hypertension")
    heart_disease: Literal[0, 1] = Field(..., description="0 = No heart disease, 1 = Has heart disease")
    smoking_history: Literal["never", "No Info", "current", "former", "ever", "not current"] = Field(
        ..., description="Smoking status"
    )
    bmi: float = Field(..., ge=10.0, le=70.0, description="Body Mass Index")
    HbA1c_level: float = Field(..., ge=3.0, le=15.0, description="Hemoglobin A1c level (%)")
    blood_glucose_level: int = Field(..., ge=50, le=400, description="Blood glucose level (mg/dL)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "gender": "Female",
                "age": 60.0,
                "hypertension": 1,
                "heart_disease": 0,
                "smoking_history": "former",
                "bmi": 32.5,
                "HbA1c_level": 7.5,
                "blood_glucose_level": 200
            }
        }
    )


class DiabetesResponse(BaseModel):
    prediction: int = Field(..., description="0 = Non-Diabetic, 1 = Diabetic")
    diagnosis: str = Field(..., description="Human-readable diagnosis")
    probability: float = Field(..., description="Predicted probability of having diabetes (0.0 to 1.0)")
    risk_level: str = Field(..., description="Low, Moderate, or High risk")


# ---------------------------------------------------------------------------
# 2. House Price Prediction Schemas
# ---------------------------------------------------------------------------
class HousePriceRequest(BaseModel):
    Area: float = Field(..., gt=100.0, le=20000.0, description="Living area in square feet")
    Bedrooms: int = Field(..., ge=1, le=10, description="Number of bedrooms")
    Bathrooms: int = Field(..., ge=1, le=8, description="Number of bathrooms")
    Stories: int = Field(..., ge=1, le=6, description="Number of stories/floors")
    Parking: int = Field(..., ge=0, le=5, description="Parking capacity count")
    Age: int = Field(..., ge=0, le=100, description="Property age in years")
    City: Literal["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Kolkata", "Pune", "Chennai"] = Field(
        ..., description="City location"
    )
    Furnishing: Literal["Furnished", "Semi-Furnished", "Unfurnished"] = Field(
        ..., description="Furnishing state"
    )
    Main_Road: Literal["Yes", "No"] = Field(..., alias="Main Road", description="Connected to main road")
    Guest_Room: Literal["Yes", "No"] = Field(..., alias="Guest Room", description="Has dedicated guest room")
    Basement: Literal["Yes", "No"] = Field(..., description="Has basement")
    Water_Supply: Literal["Corporation", "Borewell", "Both"] = Field(..., alias="Water Supply", description="Source of water")
    Air_Conditioning: Literal["Yes", "No"] = Field(..., alias="Air Conditioning", description="Has AC")
    Preferred_Tenant: Literal["Family", "Bachelor", "Company"] = Field(..., alias="Preferred Tenant", description="Preferred tenant type")
    Locality_Rating: int = Field(..., ge=1, le=10, alias="Locality Rating", description="Locality score (1-10)")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "Area": 3000.0,
                "Bedrooms": 4,
                "Bathrooms": 3,
                "Stories": 2,
                "Parking": 2,
                "Age": 5,
                "City": "Mumbai",
                "Furnishing": "Furnished",
                "Main Road": "Yes",
                "Guest Room": "Yes",
                "Basement": "No",
                "Water Supply": "Corporation",
                "Air Conditioning": "Yes",
                "Preferred Tenant": "Family",
                "Locality Rating": 8
            }
        }
    )


class HousePriceResponse(BaseModel):
    predicted_price: float = Field(..., description="Estimated house valuation in USD")
    formatted_price: str = Field(..., description="Formatted price string with commas")
    currency: str = Field(default="USD", description="Valuation currency")


# ---------------------------------------------------------------------------
# 3. E-Commerce Customer Behavior Schemas
# ---------------------------------------------------------------------------
class EcommerceRequest(BaseModel):
    Age: int = Field(..., ge=18, le=100, description="Customer age in years")
    Rating: int = Field(..., ge=1, le=5, description="Customer rating from 1 to 5 stars")
    Positive_Feedback_Count: int = Field(0, ge=0, alias="Positive Feedback Count", description="Helpful review votes")
    Division_Name: Literal["General", "General Petite", "Initmates", "Unknown"] = Field(
        "General", alias="Division Name", description="Product Division"
    )
    Department_Name: Literal["Tops", "Dresses", "Bottoms", "Intimate", "Jackets", "Trend", "Unknown"] = Field(
        "Dresses", alias="Department Name", description="Product Department"
    )
    Class_Name: str = Field("Dresses", alias="Class Name", description="Product Category Class")
    Review_Text: str = Field("", alias="Review Text", description="Natural language customer review")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "Age": 32,
                "Rating": 5,
                "Positive Feedback Count": 4,
                "Division Name": "General",
                "Department Name": "Dresses",
                "Class Name": "Dresses",
                "Review Text": "In love with this dress! Super comfortable and high quality."
            }
        }
    )


class EcommerceResponse(BaseModel):
    recommended: int = Field(..., description="0 = Not Recommended, 1 = Recommended")
    recommendation_label: str = Field(..., description="Human-readable status")
    confidence: float = Field(..., description="Model confidence probability (0.0 to 1.0)")
    sentiment_hint: str = Field(..., description="Estimated sentiment polarity based on text and score")


# ---------------------------------------------------------------------------
# Health Check Schema
# ---------------------------------------------------------------------------
class HealthCheckResponse(BaseModel):
    status: str
    models_loaded: dict
