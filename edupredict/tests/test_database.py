import os
import unittest
import tempfile

from src.database import StudentDatabase
from src.utils import RecordNotFoundError, ValidationError


class TestStudentDatabase(unittest.TestCase):
    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp_file.close()
        self.db = StudentDatabase(db_path=self.tmp_file.name)

    def tearDown(self):
        os.unlink(self.tmp_file.name)

    def test_add_and_get_student(self):
        sid = self.db.add_student("Alice", 5.0, 90.0, 75.0, 12)
        student = self.db.get_student(sid)
        self.assertEqual(student["name"], "Alice")
        self.assertEqual(student["assignments_submitted"], 12)

    def test_list_students(self):
        self.db.add_student("Alice", 5.0, 90.0, 75.0, 12)
        self.db.add_student("Bob", 3.0, 60.0, 55.0, 8)
        students = self.db.list_students()
        self.assertEqual(len(students), 2)

    def test_update_student(self):
        sid = self.db.add_student("Alice", 5.0, 90.0, 75.0, 12)
        self.db.update_student(sid, final_score=88.5, passed=1)
        student = self.db.get_student(sid)
        self.assertEqual(student["final_score"], 88.5)
        self.assertEqual(student["passed"], 1)

    def test_delete_student(self):
        sid = self.db.add_student("Alice", 5.0, 90.0, 75.0, 12)
        self.db.delete_student(sid)
        with self.assertRaises(RecordNotFoundError):
            self.db.get_student(sid)

    def test_get_missing_student_raises(self):
        with self.assertRaises(RecordNotFoundError):
            self.db.get_student(999)

    def test_invalid_input_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self.db.add_student("", 5.0, 90.0, 75.0, 12)
        with self.assertRaises(ValidationError):
            self.db.add_student("Alice", 30.0, 90.0, 75.0, 12)  # study_hours > 24
        with self.assertRaises(ValidationError):
            self.db.add_student("Alice", 5.0, 150.0, 75.0, 12)  # attendance > 100

    def test_count(self):
        self.assertEqual(self.db.count(), 0)
        self.db.add_student("Alice", 5.0, 90.0, 75.0, 12)
        self.assertEqual(self.db.count(), 1)


if __name__ == "__main__":
    unittest.main()
