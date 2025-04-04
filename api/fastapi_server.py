from fastapi import FastAPI
from pydantic import BaseModel
from models.predict import Predictor


app = FastAPI(
    title="NBA Stat Projection API",
    description="Predict NBA player stat lines based on opponent and recent performance",
    version="1.0.0"
)

predictor = Predictor()

class PredictionRequest(BaseModel):
    player_name: str
    opponent_team: str
    home_or_away: str

@app.post("/predict")
def predict_stats(request: PredictionRequest):
    """
    Takes a request from the client of player name, opponent team, and home away
    and predicts the stat line based on the input
    """
    result = predictor.predict(
        player_name=request.player_name,
        opponent_team=request.opponent_team,
        home_or_away=request.home_or_away
    )

    if result.empty:
        return {"message": "Prediction failed."}
    
    return result.to_dict(orient="records")[0]