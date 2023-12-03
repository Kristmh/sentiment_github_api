import logging

from transformers import AutoTokenizer, pipeline

from api.fetch_github import extract_specific_fields, fetch_issues

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# TODO: refactor into one function
def predict_emotions(text):
    model = "SamLowe/roberta-base-go_emotions"
    pipe = pipeline("text-classification", model=model)

    tokenizer = AutoTokenizer.from_pretrained(model)

    # Get the maximum length the model can handle
    max_length = tokenizer.model_max_length

    # Tokenize and truncate the text
    tokens = tokenizer.encode(
        text,
        add_special_tokens=True,
        truncation=True,
        max_length=max_length,
    )

    # Convert the tokens back to text string
    truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)

    # Pass the truncated text to the pipeline
    sentiment = pipe(truncated_text)
    sentiment["label"] = sentiment[0]["label"]
    sentiment["score"] = sentiment[0]["score"]

    logging.info(sentiment)
    return sentiment


def predict_sentiment(issue: str):
    model = "distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_pipeline = pipeline("sentiment-analysis", model=model)

    tokenizer = AutoTokenizer.from_pretrained(model)

    # Get the maximum length the model can handle
    max_length = tokenizer.model_max_length

    # Tokenize and truncate the text
    tokens = tokenizer.encode(
        issue, add_special_tokens=True, truncation=True, max_length=max_length
    )

    # Convert the tokens back to text string
    truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)

    # Pass the truncated text to the pipeline
    sentiment = sentiment_pipeline(truncated_text)

    sentiment = {"label": sentiment[0]["label"], "score": sentiment[0]["score"]}
    logging.info(sentiment)

    return sentiment


if __name__ == "__main__":
    data = fetch_issues("microsoft", "vscode")
    filtered = extract_specific_fields(data)
    sentiment = predict_emotions(filtered)
    logging.info(sentiment)
