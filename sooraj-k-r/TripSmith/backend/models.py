# backend/models.py
from pydantic import BaseModel, Field

class TripRequest(BaseModel):
    # Field(...) means the field is required. We also add basic validation rules.
    starting_location: str = Field(..., min_length=2, description="Where the user is starting from")
    destination: str = Field(..., min_length=2, description="Destination in Kerala")
    travel_days: int = Field(..., gt=0, le=30, description="Number of days (1 to 30)")
    travelers: int = Field(..., gt=0, le=20, description="Number of people traveling")
    total_budget: float = Field(..., gt=0, description="Total budget for the trip in INR")

class TripResponse(BaseModel):
    # For now, this is a placeholder response. We will expand this in later phases.
    status: str
    message: str
    received_data: dict

    