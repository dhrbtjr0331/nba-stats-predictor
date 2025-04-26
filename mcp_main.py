from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("nba-stats-predictor", server_version="1.0")

# Constants
NSP_API_BASE = "https://localhost:8000"
USER_AGENT = "nba-stats-predictor/1.0"

async def make_api_request(
    url: str,
    method: str = "GET",
    payload: dict[str, Any] | None = None
) -> dict[str, Any] | None:
    """Make a request to FastAPI app with proper headers and error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            else:
                raise ValueError("Unsupported HTTP method.")

            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Request to {url} failed: {e}")
            return None

@mcp.tool()
async def predict_player_stats(player_name: str, opponent_team: str, home_or_away: str) -> str:
    """Predict a player's stat line against an opponent.

    Args:
        player_name: Full name of the player (e.g. LeBron James)
        opponent_team: 3-letter abbreviation (e.g. BOS, LAL)
        home_or_away: "Home" or "Away"
    """
    url = "http://localhost:8000/predict"
    payload = {
        "player_name": player_name,
        "opponent_team": opponent_team,
        "home_or_away": home_or_away
    }

    response = await make_api_request(url, method="POST", payload=payload)

    if not response:
        return f"❌ Prediction failed for {player_name} vs {opponent_team}."

    return (
        f"📊 Predicted stats for {player_name} vs {opponent_team}:\n"
        f"PTS: {response['PTS']:.1f} | AST: {response['AST']:.1f} | TRB: {response['TRB']:.1f}\n"
        f"FG%: {response['FG_PCT']:.2f} | STL: {response['STL']:.1f} | BLK: {response['BLK']:.1f}"
    )

if __name__ == "__main__":
    # Initialize and run the server
    print("running")
    mcp.run(transport='stdio')
