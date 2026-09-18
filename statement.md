# Problem Statement

## Problem Statement

Educators and academic mentors often only discover that a student is
struggling after a graded assessment has already been missed or failed,
by which point there is little time left to intervene. Meanwhile, the
early-warning signals — how much a student studies, how consistently
they attend class, how they performed previously, and how engaged they
are with coursework — are usually available well before the final
result. **EduPredict** addresses this gap by turning those everyday
signals into an early, data-driven forecast of whether a student is on
track to pass and what final score they are likely to achieve, so
intervention (extra support, tutoring, outreach) can happen while there
is still time to change the outcome.

## Scope of the Project

EduPredict is a command-line AI/ML system, built for the "Fundamentals
of AI and ML" course, that:

- Stores and manages student academic-input records (study hours,
  attendance, prior score, assignments submitted) in a local SQLite
  database, with full create/read/update/delete support.
- Trains a supervised machine learning pipeline (a classification model
  for pass/fail and a regression model for the numeric final score) on a
  documented, realistic synthetic dataset that mirrors known relationships
  between study habits and academic outcome.
- Evaluates the trained models with standard metrics (accuracy,
  precision, recall, F1-score, confusion matrix, MAE, R²) so performance
  is transparent and inspectable, not just claimed.
- Predicts the likely outcome for any new student profile on demand.
- Produces aggregate analytics (class averages, pass rate, score range)
  and chart visualizations (score distribution, feature importance,
  study-hours-vs-score) to support review.

Out of scope: a graphical/web front end (the project is deliberately
CLI-only per the assignment's executability requirement), real
institutional student data (a documented synthetic generator is used
instead, both for privacy and reproducibility), and integration with any
live school information system.

## Target Users

- **Course instructors / academic mentors** who want an early indication
  of which students may need additional support.
- **Students** who want to understand, from their own study/attendance
  inputs, what outcome they are currently trending toward.
- **Evaluators of this project**, who can run every command from a plain
  terminal with no setup beyond `pip install -r requirements.txt`.

## High-Level Features

1. **Data Management Module** — SQLite-backed CRUD for student records,
   with input validation and clear "record not found" handling.
2. **Prediction Engine (ML Module)** — synthetic dataset generation,
   RandomForest classifier + regressor training, persisted models, and a
   simple `predict()` API used by the CLI.
3. **Analytics & Reporting Module** — summary statistics and three saved
   chart images, plus a plain-text analytics report.
4. **Command-Line Interface** — a single `main.py` entry point with
   `add`, `list`, `update`, `delete`, `seed`, `train`, `predict`, and
   `report` subcommands, each with `--help` documentation.
5. **Logging & structured error handling** — every action is logged to
   `reports/edupredict.log`; user-facing errors are clear and specific
   rather than raw stack traces.
