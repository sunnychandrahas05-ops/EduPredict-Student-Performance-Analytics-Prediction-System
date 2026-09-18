#!/usr/bin/env python3
"""
main.py
--------
EduPredict: Student Performance Analytics & Prediction System
Command-line entry point.

Fully executable from a terminal -- no GUI required (see command list
below). This module is intentionally thin: it parses arguments,
validates high-level intent, and delegates to the three functional
modules (src/database.py, src/ml_model.py, src/analytics.py),
catching and reporting their custom exceptions cleanly.

USAGE
-----
    python main.py add --name "Aditi Rao" --study-hours 4.5 --attendance 88 \
                    --prior-score 76 --assignments 15 [--final-score 82 --passed 1]
    python main.py list
    python main.py update --id 3 --final-score 91 --passed 1
    python main.py delete --id 3
    python main.py seed --n 800                 # generate synthetic training data
    python main.py train                        # train classifier + regressor
    python main.py predict --study-hours 5 --attendance 90 --prior-score 70 --assignments 12
    python main.py report                       # analytics + charts
"""

import argparse
import sys

from src.database import StudentDatabase
from src.ml_model import PerformancePredictor, generate_synthetic_dataset
from src import analytics
from src.utils import get_logger, EduPredictError

logger = get_logger("main")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="edupredict",
        description="EduPredict: Student Performance Analytics & Prediction System",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new student record")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--study-hours", type=float, required=True)
    p_add.add_argument("--attendance", type=float, required=True)
    p_add.add_argument("--prior-score", type=float, required=True)
    p_add.add_argument("--assignments", type=int, required=True)
    p_add.add_argument("--final-score", type=float, default=None)
    p_add.add_argument("--passed", type=int, choices=[0, 1], default=None)

    sub.add_parser("list", help="List all student records")

    p_update = sub.add_parser("update", help="Update an existing student record")
    p_update.add_argument("--id", type=int, required=True)
    p_update.add_argument("--final-score", type=float)
    p_update.add_argument("--passed", type=int, choices=[0, 1])
    p_update.add_argument("--attendance", type=float)

    p_delete = sub.add_parser("delete", help="Delete a student record")
    p_delete.add_argument("--id", type=int, required=True)

    p_seed = sub.add_parser("seed", help="Populate the DB with a synthetic dataset")
    p_seed.add_argument("--n", type=int, default=200)

    p_train = sub.add_parser("train", help="Train the prediction models")
    p_train.add_argument("--n", type=int, default=800, help="Synthetic training samples")

    p_predict = sub.add_parser("predict", help="Predict outcome for a new student")
    p_predict.add_argument("--study-hours", type=float, required=True)
    p_predict.add_argument("--attendance", type=float, required=True)
    p_predict.add_argument("--prior-score", type=float, required=True)
    p_predict.add_argument("--assignments", type=int, required=True)

    sub.add_parser("report", help="Generate analytics summary + charts from stored records")

    return parser


def cmd_add(args, db: StudentDatabase):
    new_id = db.add_student(args.name, args.study_hours, args.attendance,
                             args.prior_score, args.assignments,
                             args.final_score, args.passed)
    print(f"[OK] Added student '{args.name}' with id={new_id}")


def cmd_list(args, db: StudentDatabase):
    students = db.list_students()
    if not students:
        print("No students in the database yet. Try 'python main.py add ...' or 'seed'.")
        return
    header = f"{'ID':<4}{'Name':<20}{'Hours':<8}{'Attend%':<10}{'Prior':<8}{'Assign':<8}{'Final':<8}{'Passed':<8}"
    print(header)
    print("-" * len(header))
    for s in students:
        print(f"{s['id']:<4}{s['name']:<20}{s['study_hours_per_day']:<8}{s['attendance_percentage']:<10}"
              f"{s['prior_exam_score']:<8}{s['assignments_submitted']:<8}"
              f"{str(s['final_score']):<8}{str(s['passed']):<8}")


def cmd_update(args, db: StudentDatabase):
    fields = {}
    if args.final_score is not None:
        fields["final_score"] = args.final_score
    if args.passed is not None:
        fields["passed"] = args.passed
    if args.attendance is not None:
        fields["attendance_percentage"] = args.attendance
    db.update_student(args.id, **fields)
    print(f"[OK] Updated student id={args.id}")


def cmd_delete(args, db: StudentDatabase):
    db.delete_student(args.id)
    print(f"[OK] Deleted student id={args.id}")


def cmd_seed(args, db: StudentDatabase):
    df = generate_synthetic_dataset(n_samples=args.n)
    for _, row in df.iterrows():
        db.add_student(
            name=f"Student_{row.name + 1}",
            study_hours=row["study_hours_per_day"],
            attendance=row["attendance_percentage"],
            prior_score=row["prior_exam_score"],
            assignments_submitted=int(row["assignments_submitted"]),
            final_score=row["final_score"],
            passed=int(row["passed"]),
        )
    print(f"[OK] Seeded database with {args.n} synthetic student records.")


def cmd_train(args, _db):
    predictor = PerformancePredictor()
    df = generate_synthetic_dataset(n_samples=args.n)
    metrics = predictor.train(df)
    print("[OK] Training complete.\n")
    print("Classification metrics (pass/fail):")
    for k, v in metrics["classification"].items():
        print(f"  {k}: {v}")
    print("\nRegression metrics (final score):")
    for k, v in metrics["regression"].items():
        print(f"  {k}: {v}")
    print("\nFeature importances:")
    for k, v in metrics["feature_importances"].items():
        print(f"  {k}: {v}")
    return metrics


def cmd_predict(args, _db):
    predictor = PerformancePredictor()
    result = predictor.predict(args.study_hours, args.attendance, args.prior_score, args.assignments)
    print("[OK] Prediction:")
    for k, v in result.items():
        print(f"  {k}: {v}")


def cmd_report(args, db: StudentDatabase):
    students = db.list_students()
    summary = analytics.summarize_students(students)
    print("[OK] Analytics Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    if students:
        p1 = analytics.plot_score_distribution(students)
        p2 = analytics.plot_study_vs_score(students)
        print(f"\nSaved charts:\n  {p1}\n  {p2}")
    analytics.generate_text_report(students)
    print("  reports/analytics_report.txt")


def main():
    parser = build_parser()
    args = parser.parse_args()
    db = StudentDatabase()

    dispatch = {
        "add": cmd_add,
        "list": cmd_list,
        "update": cmd_update,
        "delete": cmd_delete,
        "seed": cmd_seed,
        "train": cmd_train,
        "predict": cmd_predict,
        "report": cmd_report,
    }

    try:
        dispatch[args.command](args, db)
    except EduPredictError as e:
        logger.error("Application error: %s", e)
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:  # safety net -- never crash with a raw traceback
        logger.exception("Unexpected error")
        print(f"[FATAL] Unexpected error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
