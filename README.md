# EduPredict — Student Performance Analytics & Prediction System

**Course:** Fundamentals of AI and ML
**Type:** Command-line AI/ML application (Build-Your-Own-Project submission)

## Overview

EduPredict is a fully command-line system that helps identify students at
risk of poor academic performance and forecasts their likely final score.
It combines three functional modules — **data management**, a **machine
learning prediction engine**, and **analytics/reporting** — around a single
SQLite-backed student database.

A trained **RandomForestClassifier** predicts pass/fail, and a
**RandomForestRegressor** predicts the numeric final score, both from four
everyday academic signals: daily study hours, attendance percentage, prior
exam score, and assignments submitted. The system also generates summary
statistics and chart images (score distribution, feature importance, study
hours vs. score) from any stored student population.

## Features

- **Student record CRUD** — add, list, update, delete records in a local
  SQLite database (`src/database.py`)
- **Synthetic dataset generator** — produces a realistic, documented
  training set so the whole pipeline runs without needing an external
  dataset (`src/ml_model.py`)
- **Model training & evaluation** — trains both models and reports
  accuracy, precision, recall, F1, confusion matrix, MAE, R², and feature
  importances
- **Prediction** — given a new student's profile, predicts pass/fail
  probability and expected final score
- **Analytics & reporting** — aggregate statistics plus three saved chart
  images and a text report
- **Robust CLI** — every command validates input and reports clean error
  messages instead of raw tracebacks; all activity is logged to
  `reports/edupredict.log`
- **Unit tested** — 15 unit tests across all three modules (`tests/`)

## Technologies / Tools Used

| Purpose            | Tool                      |
|---------------------|---------------------------|
| Language            | Python 3.11               |
| ML                  | scikit-learn (RandomForest) |
| Data handling       | pandas, numpy              |
| Storage             | SQLite (stdlib `sqlite3`)  |
| Charts              | matplotlib                 |
| Model persistence   | joblib                     |
| Testing             | unittest (stdlib)          |
| Diagrams            | Graphviz                   |

## Project Structure

```
edupredict/
├── main.py                    # CLI entry point (argparse)
├── requirements.txt
├── src/
│   ├── database.py            # Module 1: Data Management (SQLite CRUD)
│   ├── ml_model.py            # Module 2: Prediction Engine (train/predict)
│   ├── analytics.py           # Module 3: Analytics & Reporting
│   └── utils.py                # Logging, custom exceptions, validation
├── tests/
│   ├── test_database.py
│   ├── test_ml_model.py
│   └── test_analytics.py
├── docs/
│   ├── generate_diagrams.py   # Script that (re)builds all diagrams
│   └── diagrams/               # architecture, workflow, UML, ER diagrams
├── data/                       # edupredict.db created at runtime
├── models/                     # trained .joblib models saved here
└── reports/                     # charts, text report, log file
```

## Steps to Install & Run

### 1. Clone and set up the environment

```bash
git clone https://github.com/<github-username>/<repo-name>.git
cd <repo-name>
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate training data and train the models

```bash
python main.py seed --n 200        # populate the DB with synthetic students
python main.py train --n 800       # train classifier + regressor, print metrics
```

### 3. Try the core commands

```bash
# Add a real student record
python main.py add --name "Aditi Rao" --study-hours 4.5 --attendance 88 \
                    --prior-score 76 --assignments 15

# List all stored students
python main.py list

# Update a record once the real outcome is known
python main.py update --id 1 --final-score 91 --passed 1

# Predict a new/unknown student's outcome
python main.py predict --study-hours 5 --attendance 90 --prior-score 70 --assignments 12

# Generate the analytics summary + charts
python main.py report

# Delete a record
python main.py delete --id 1
```

Run `python main.py --help` or `python main.py <command> --help` for the
full option list of any command.

## Instructions for Testing

```bash
python -m unittest discover -s tests -v
```

This runs 15 unit tests covering the data-management CRUD layer
(including validation and not-found error paths), the ML pipeline
(dataset generation, training, prediction, and the "model not trained"
guard), and the analytics layer (summary statistics and chart file
generation).

## Regenerating the Design Diagrams

```bash
python docs/generate_diagrams.py
```

Rebuilds `docs/diagrams/architecture_diagram.png`, `workflow_diagram.png`,
`use_case_diagram.png`, `class_diagram.png`, `sequence_diagram.png`, and
`er_diagram.png` from source using Graphviz.

## Non-Functional Requirements

- **Performance** — training on 800 synthetic samples completes in under
  two seconds; predictions are near-instant using pre-trained, persisted
  models.
- **Reliability** — all database writes are wrapped in transactions with
  rollback on failure; every CLI command catches and reports errors
  cleanly instead of crashing.
- **Usability** — a single, discoverable CLI (`--help` on every command)
  with human-readable tabular/summary output.
- **Maintainability** — one responsibility per module, no cross-module
  coupling beyond shared utilities, and a documented database schema.
- **Scalability** — SQLite and RandomForest comfortably scale to tens of
  thousands of student records for a course-project workload; storage and
  model backends are isolated behind a small API so either could be
  swapped for something larger later.
- **Logging/monitoring** — every operation (CRUD, training, prediction) is
  logged with timestamps to `reports/edupredict.log`.
- **Error handling** — a dedicated exception hierarchy
  (`ValidationError`, `RecordNotFoundError`, `ModelNotTrainedError`)
  distinguishes user-input mistakes from system faults.

## Screenshots

See `reports/score_distribution.png`, `reports/feature_importance.png`,
and `reports/study_vs_score.png`, generated by `python main.py report`.
