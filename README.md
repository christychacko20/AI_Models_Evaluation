# AI Technology Evaluation and Business Transformation Dashboard

A Streamlit dashboard for comparing generative AI models and translating model performance into business adoption recommendations.

## Features

- Weighted benchmarking across accuracy, latency, reliability, and cost efficiency
- Executive KPI cards and model ranking
- Interactive quality/speed/cost trade-off visualization
- Business-use-case fit matrix for five transformation opportunities
- Phased adoption roadmap with governance principles
- CSV upload for replacing the illustrative benchmark dataset

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## CSV format

The uploader expects these columns:

```text
Model,Provider,Accuracy,Latency (ms),Reliability,Cost / 1K requests ($)
```

`Accuracy` and `Reliability` should be percentages from 0 to 100. Latency is measured in milliseconds and cost is expressed in dollars per 1,000 requests.
