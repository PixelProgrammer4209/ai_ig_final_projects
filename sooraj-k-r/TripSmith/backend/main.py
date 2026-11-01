from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import TripRequest, TripResponse # Import our new models

app = FastAPI(title="TripSmith API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to TripSmith API! The backend is working."}

# Add our new POST endpoint
@app.post("/api/plan-trip", response_model=TripResponse)
def plan_trip(request: TripRequest):
    """
    Endpoint to receive trip details and eventually generate an itinerary.
    """
    try:
        # A simple check: initially, we only support Kerala
        if "kerala" not in request.destination.lower():
            # HTTPException is how FastAPI returns error codes like 400 Bad Request
            raise HTTPException(status_code=400, detail="Currently, we only support destinations in Kerala.")

        return TripResponse(
            status="success",
            message=f"Trip planning initiated for {request.destination}",
            received_data=request.model_dump() # Converts the Pydantic model back to a Python dictionary
        )

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions so FastAPI handles them normally
        raise http_exc
    except Exception as e:
        # Catch any unexpected server errors (500)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")