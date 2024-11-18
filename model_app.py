from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
import pandas as pd
import joblib

app = FastAPI()

# Input model for the request body
class Input(BaseModel):
    department: str
    region: str
    education: Optional[str]  # Allow 'education' to be optional
    gender: str
    recruitment_channel: str
    no_of_trainings: int
    age: int
    previous_year_rating: Optional[float]  # Optional because it might be missing
    length_of_service: int
    KPIs_met_over_80_percent: int
    awards_won: int
    avg_training_score: int

# Output model for the response
class Output(BaseModel):
    is_promoted: int

@app.post("/predict", response_model=Output)
def predict(data: Input) -> Output:
    try:
        # Prepare the input data for the model
        X_input = pd.DataFrame([[
            data.department, data.region, data.education, data.gender,
            data.recruitment_channel, data.no_of_trainings, data.age,
            data.previous_year_rating, data.length_of_service, 
            data.KPIs_met_over_80_percent, data.awards_won, data.avg_training_score
        ]])

        # Define the column names based on what the model expects
        X_input.columns = [
            'department', 'region', 'education', 'gender', 'recruitment_channel',
            'no_of_trainings', 'age', 'previous_year_rating', 'length_of_service',
            'KPIs_met_over_80_percent', 'awards_won', 'avg_training_score'
        ]

        # Load the pre-trained model
        model = joblib.load('jobchg_pipeline_model.pkl')

        # Get the prediction from the model
        prediction = model.predict(X_input)

        # Return the result as `is_promoted`
        return Output(is_promoted=int(prediction[0]))
    
    except ValidationError as e:
        # Raise HTTP 422 if the input data is invalid
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Catch other exceptions and return a generic error
        raise HTTPException(status_code=500, detail="Prediction failed: " + str(e))