from typing import List

from transformers import AutoTokenizer, pipeline

from api.fetch_github import fetch_issues


def predict_emotions(text: list):
    emotions = []

    model = "SamLowe/roberta-base-go_emotions"
    pipe = pipeline("text-classification", model=model)

    tokenizer = AutoTokenizer.from_pretrained(model)

    # Get the maximum length the model can handle
    max_length = tokenizer.model_max_length

    for issue in text:
        if issue:
            # Tokenize and truncate the text
            tokens = tokenizer.encode(
                issue, add_special_tokens=True, truncation=True, max_length=max_length
            )

            # Convert the tokens back to text string
            truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)

            # Pass the truncated text to the pipeline
            sentiment = pipe(truncated_text)
            print(sentiment)
            emotions.append({"issue": issue, "sentiment": sentiment})
    return emotions


def predict_sentiment(text: list):
    sentiments: List = []
    positive_issues: int = 0
    negative_issues: int = 0

    model = "distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_pipeline = pipeline("sentiment-analysis", model=model)

    tokenizer = AutoTokenizer.from_pretrained(model)

    # Get the maximum length the model can handle
    max_length = tokenizer.model_max_length

    for issue in text:
        if issue:
            # Tokenize and truncate the text
            tokens = tokenizer.encode(
                issue, add_special_tokens=True, truncation=True, max_length=max_length
            )

            # Convert the tokens back to text string
            truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)

            # Pass the truncated text to the pipeline
            sentiment = sentiment_pipeline(truncated_text)
            print(sentiment)
            sentiments.append({"issue": issue, "sentiment": sentiment})
            results = sentiment[0]
            if results["label"] == "POSITIVE":
                positive_issues += 1
            elif results["label"] == "NEGATIVE":
                negative_issues += 1
    return sentiments, positive_issues, negative_issues


if __name__ == "__main__":
    data = fetch_issues("microsoft", "vscode")
    emotions = predict_emotions(data)
    print(emotions)
    sent, pos, neg = predict_sentiment(data)
    # print(sent)
    total = pos + neg
    print(f"Positive issues: {pos} out of {total}")
    print(f"Negative issues: {neg} out of {total}")
