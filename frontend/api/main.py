import re
from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.fetch_github import fetch_issues, extract_specific_fields
from api.sentiment_analysis import predict_emotions, predict_sentiment

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
    num_issues: int
    per_page: int


@app.post("/api/analyze")
async def analyze_github(request: AnalyzeRequest):
    url: str = request.url
    num_issues: int = int(request.num_issues)
    per_page: int = int(request.per_page)
    analysis_type: AnalysisType = request.analysis_type

    # Get github owner and repo
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)

    if not match:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    owner, repo = match.groups()

    # Fetch GitHub issues
    try:
        issues = fetch_issues(owner, repo, num_issues, per_page)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Perform analysis
    results = []
    try:
        for issue in issues:
            filtered_issue = extract_specific_fields(issue)
            # TODO: this might change when refactoring other functions.
            if analysis_type == AnalysisType.emotion:
                sentiment_results = predict_emotions(filtered_issue["text_clean"])
            elif analysis_type == AnalysisType.sentiment:
                sentiment_results = predict_sentiment(filtered_issue["text_clean"])
            filtered_issue["score"] = sentiment_results["score"]
            filtered_issue["label"] = sentiment_results["label"]
            results.append(filtered_issue)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
