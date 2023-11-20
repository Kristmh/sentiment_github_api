import re
from enum import Enum
from typing import List, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sentiment_github.fetch_github import fetch_github_issues
from sentiment_github.sentiment_analysis import predict_emotions, predict_sentiment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class AnalysisType(str, Enum):
    sentiment = "sentiment"
    emotion = "emotion"


class AnalyzeRequest(BaseModel):
    url: str
    analysis_type: AnalysisType


@app.post("/analyze")
async def analyze_github(request: AnalyzeRequest):
    url: str = request.url
    analysis_type: AnalysisType = request.analysis_type

    # Get github owner and repo
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)

    if not match:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    owner, repo = match.groups()

    # Fetch GitHub issues
    try:
        issues: List[str] = fetch_github_issues(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Perform analysis
    try:
        if analysis_type == AnalysisType.sentiment:
            sentiment_results: Tuple[List[str], int, int] = predict_sentiment(issues)
            positive, negative = sentiment_results[1], sentiment_results[2]
            return {
                "url": url,
                "analysis": analysis_type,
                "positive_issues": positive,
                "negative_issues": negative,
                "results": sentiment_results[0],
            }
        elif analysis_type == AnalysisType.emotion:
            emotion_results: List[str] = predict_emotions(issues)
            return {"url": url, "analysis": analysis_type, "results": emotion_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
