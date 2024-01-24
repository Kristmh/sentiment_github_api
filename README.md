# Sentiment Analysis on GitHub issues

## Description

Find sentiment of GitHub issues using machine learning.
Can choose between using 2 models.
One finds if issues are positive or negative. Model: [A version of Distilbert](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english).
The seconds finds emotions in issues like confusion, joy, nervousness, surprise. Model [Based on roberta model](https://huggingface.co/SamLowe/roberta-base-go_emotions).

## Why?

This tool can help developers understand how they write issues and how the reader perceives the language used when writing issues.
When reading issues you can get an insight into what emotion the creator of the issues used, for example if they are confused or angry.

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Kristmh/sentiment_github.git
```

Cd into the project

```bash
cd frontend
```

Install dependencies:

```bash
yarn install
```

Run servers.
This will run both Next.js and fastapi servers.

```bash
yarn dev
```

If you only want to run next.js server:

```bash
yarn next-dev
```

If you only want to run fastapi server:

```bash
yarn fastapi-dev
```

## Usage

Navigate to the website running on [http://localhost:3000](http://localhost:3000)
Enter a GitHub repository, select a model and click submit.
Include the full URL like this: https://github.com/neovim/neovim

Backend Running on [http://localhost:8000](http://localhost:8000)
