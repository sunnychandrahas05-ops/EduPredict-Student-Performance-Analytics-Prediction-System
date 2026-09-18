import unittest

from src.ml_model import generate_synthetic_dataset, PerformancePredictor, FEATURE_COLUMNS
from src.utils import ModelNotTrainedError


class TestSyntheticDataset(unittest.TestCase):
    def test_shape_and_columns(self):
        df = generate_synthetic_dataset(n_samples=100)
        self.assertEqual(len(df), 100)
        for col in FEATURE_COLUMNS + ["final_score", "passed"]:
            self.assertIn(col, df.columns)

    def test_value_ranges(self):
        df = generate_synthetic_dataset(n_samples=200)
        self.assertTrue((df["final_score"] >= 0).all() and (df["final_score"] <= 100).all())
        self.assertTrue(set(df["passed"].unique()).issubset({0, 1}))


class TestPerformancePredictor(unittest.TestCase):
    def test_predict_without_training_raises(self):
        predictor = PerformancePredictor()
        predictor.classifier = None
        predictor.regressor = None
        with self.assertRaises(ModelNotTrainedError):
            predictor.predict(5, 90, 75, 12)

    def test_train_and_predict(self):
        predictor = PerformancePredictor()
        df = generate_synthetic_dataset(n_samples=300)
        metrics = predictor.train(df)
        self.assertIn("classification", metrics)
        self.assertIn("regression", metrics)
        self.assertGreaterEqual(metrics["classification"]["accuracy"], 0.5)

        result = predictor.predict(8, 95, 90, 18)
        self.assertIn("predicted_final_score", result)
        self.assertIn("predicted_pass", result)
        # A strong student profile should very likely be predicted to pass
        self.assertTrue(result["predicted_pass"])


if __name__ == "__main__":
    unittest.main()
