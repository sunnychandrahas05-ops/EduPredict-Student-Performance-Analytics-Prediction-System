import os
import unittest

from src.analytics import summarize_students, plot_score_distribution, plot_study_vs_score


SAMPLE_STUDENTS = [
    {"study_hours_per_day": 5, "attendance_percentage": 90, "prior_exam_score": 70,
     "assignments_submitted": 10, "final_score": 82, "passed": 1},
    {"study_hours_per_day": 2, "attendance_percentage": 55, "prior_exam_score": 40,
     "assignments_submitted": 4, "final_score": 35, "passed": 0},
]


class TestAnalytics(unittest.TestCase):
    def test_summarize_students_empty(self):
        summary = summarize_students([])
        self.assertEqual(summary["count"], 0)

    def test_summarize_students(self):
        summary = summarize_students(SAMPLE_STUDENTS)
        self.assertEqual(summary["count"], 2)
        self.assertIn("avg_final_score", summary)
        self.assertIn("pass_rate_pct", summary)
        self.assertEqual(summary["pass_rate_pct"], 50.0)

    def test_plot_score_distribution_creates_file(self):
        path = plot_score_distribution(SAMPLE_STUDENTS, out_path="/tmp/test_score_dist.png")
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_plot_study_vs_score_creates_file(self):
        path = plot_study_vs_score(SAMPLE_STUDENTS, out_path="/tmp/test_study_vs_score.png")
        self.assertTrue(os.path.exists(path))
        os.remove(path)


if __name__ == "__main__":
    unittest.main()
