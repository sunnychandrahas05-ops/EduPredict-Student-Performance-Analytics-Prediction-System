"""
analytics.py
-------------
Functional Module 3: Reporting & Analytics

Turns raw student records (from the Data Management module) and model
metrics (from the Prediction Engine) into human-readable summaries and
saved chart images. Kept independent of both other modules -- it only
receives plain data structures -- so it can be reused or tested without
a live database/model (loose coupling, maintainability).
"""

import os
import statistics
from typing import List, Dict, Any

import matplotlib
matplotlib.use("Agg")  # headless/CLI-safe backend, no GUI required
import matplotlib.pyplot as plt

from src.utils import get_logger

logger = get_logger(__name__)

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def summarize_students(students: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute aggregate statistics over the stored student population."""
    if not students:
        return {"count": 0}

    study_hours = [s["study_hours_per_day"] for s in students]
    attendance = [s["attendance_percentage"] for s in students]
    prior = [s["prior_exam_score"] for s in students]
    finals = [s["final_score"] for s in students if s.get("final_score") is not None]
    passed = [s["passed"] for s in students if s.get("passed") is not None]

    summary = {
        "count": len(students),
        "avg_study_hours": round(statistics.mean(study_hours), 2),
        "avg_attendance": round(statistics.mean(attendance), 2),
        "avg_prior_score": round(statistics.mean(prior), 2),
    }
    if finals:
        summary["avg_final_score"] = round(statistics.mean(finals), 2)
        summary["min_final_score"] = round(min(finals), 2)
        summary["max_final_score"] = round(max(finals), 2)
    if passed:
        summary["pass_rate_pct"] = round(100 * sum(passed) / len(passed), 2)
    logger.info("Computed summary statistics for %d students", len(students))
    return summary


def plot_score_distribution(students: List[Dict[str, Any]], out_path: str = None) -> str:
    """Save a histogram of predicted/known final scores. Returns file path."""
    out_path = out_path or os.path.join(REPORTS_DIR, "score_distribution.png")
    scores = [s["final_score"] for s in students if s.get("final_score") is not None]
    plt.figure(figsize=(6, 4))
    if scores:
        plt.hist(scores, bins=10, color="#4C72B0", edgecolor="white")
    plt.title("Distribution of Final Scores")
    plt.xlabel("Final Score")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    logger.info("Saved score distribution chart to %s", out_path)
    return out_path


def plot_feature_importance(feature_importances: Dict[str, float], out_path: str = None) -> str:
    """Save a bar chart of model feature importances. Returns file path."""
    out_path = out_path or os.path.join(REPORTS_DIR, "feature_importance.png")
    names = list(feature_importances.keys())
    values = list(feature_importances.values())
    plt.figure(figsize=(6, 4))
    plt.barh(names, values, color="#55A868")
    plt.title("Feature Importance (Pass/Fail Classifier)")
    plt.xlabel("Relative Importance")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    logger.info("Saved feature importance chart to %s", out_path)
    return out_path


def plot_study_vs_score(students: List[Dict[str, Any]], out_path: str = None) -> str:
    """Save a scatter plot of study hours vs final score. Returns file path."""
    out_path = out_path or os.path.join(REPORTS_DIR, "study_vs_score.png")
    hours = [s["study_hours_per_day"] for s in students]
    scores = [s.get("final_score") for s in students]
    plt.figure(figsize=(6, 4))
    pairs = [(h, s) for h, s in zip(hours, scores) if s is not None]
    if pairs:
        hs, ss = zip(*pairs)
        plt.scatter(hs, ss, alpha=0.7, color="#C44E52")
    plt.title("Study Hours vs Final Score")
    plt.xlabel("Study Hours / Day")
    plt.ylabel("Final Score")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    logger.info("Saved study-vs-score chart to %s", out_path)
    return out_path


def generate_text_report(students: List[Dict[str, Any]], metrics: Dict[str, Any] = None) -> str:
    """Build a plain-text analytics report and write it to reports/analytics_report.txt."""
    summary = summarize_students(students)
    lines = ["EduPredict Analytics Report", "=" * 32, ""]
    for k, v in summary.items():
        lines.append(f"{k}: {v}")
    if metrics:
        lines.append("")
        lines.append("Latest Model Evaluation")
        lines.append("-" * 32)
        for section, values in metrics.items():
            lines.append(f"[{section}]")
            if isinstance(values, dict):
                for mk, mv in values.items():
                    lines.append(f"  {mk}: {mv}")
            else:
                lines.append(f"  {values}")
    report_text = "\n".join(lines)
    out_path = os.path.join(REPORTS_DIR, "analytics_report.txt")
    with open(out_path, "w") as f:
        f.write(report_text)
    logger.info("Wrote text analytics report to %s", out_path)
    return report_text
