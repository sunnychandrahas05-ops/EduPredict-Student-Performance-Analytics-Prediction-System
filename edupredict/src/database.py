"""
database.py
------------
Functional Module 1: Data Management

Provides a thin, well-tested data-access layer over SQLite for student
records. This is intentionally decoupled from the ML and analytics
modules (single-responsibility) so it can be swapped for another
storage backend without touching the rest of the system (maintainability
non-functional requirement).

Schema (see docs/diagrams/er_diagram.png for the visual ER diagram):

    students
    --------
    id                      INTEGER PRIMARY KEY AUTOINCREMENT
    name                    TEXT NOT NULL
    study_hours_per_day     REAL NOT NULL
    attendance_percentage   REAL NOT NULL
    prior_exam_score        REAL NOT NULL
    assignments_submitted   INTEGER NOT NULL
    final_score             REAL            -- nullable until known/predicted
    passed                  INTEGER         -- 0/1, nullable until known/predicted
    created_at              TEXT NOT NULL
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Optional, List, Dict, Any

from src.utils import get_logger, RecordNotFoundError, validate_student_input

logger = get_logger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    study_hours_per_day REAL NOT NULL,
    attendance_percentage REAL NOT NULL,
    prior_exam_score REAL NOT NULL,
    assignments_submitted INTEGER NOT NULL,
    final_score REAL,
    passed INTEGER,
    created_at TEXT NOT NULL
);
"""


class StudentDatabase:
    """Encapsulates all CRUD operations against the students table."""

    def __init__(self, db_path: str = "data/edupredict.db"):
        self.db_path = db_path
        self._init_schema()
        logger.info("Connected to database at %s", db_path)

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(SCHEMA)

    # ---------------------------------------------------------------- CREATE
    def add_student(self, name: str, study_hours: float, attendance: float,
                     prior_score: float, assignments_submitted: int,
                     final_score: Optional[float] = None,
                     passed: Optional[int] = None) -> int:
        validate_student_input(name, study_hours, attendance, prior_score, assignments_submitted)
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO students
                   (name, study_hours_per_day, attendance_percentage, prior_exam_score,
                    assignments_submitted, final_score, passed, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, study_hours, attendance, prior_score, assignments_submitted,
                 final_score, passed, datetime.now().isoformat(timespec="seconds")),
            )
            new_id = cur.lastrowid
            logger.info("Added student '%s' with id=%d", name, new_id)
            return new_id

    # ------------------------------------------------------------------ READ
    def get_student(self, student_id: int) -> Dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
        if row is None:
            raise RecordNotFoundError(f"No student found with id={student_id}")
        return dict(row)

    def list_students(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
        return [dict(r) for r in rows]

    # ---------------------------------------------------------------- UPDATE
    def update_student(self, student_id: int, **fields) -> None:
        if not fields:
            return
        self.get_student(student_id)  # raises RecordNotFoundError if missing
        columns = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [student_id]
        with self._connect() as conn:
            conn.execute(f"UPDATE students SET {columns} WHERE id = ?", values)
        logger.info("Updated student id=%d fields=%s", student_id, list(fields.keys()))

    # ---------------------------------------------------------------- DELETE
    def delete_student(self, student_id: int) -> None:
        self.get_student(student_id)  # raises RecordNotFoundError if missing
        with self._connect() as conn:
            conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        logger.info("Deleted student id=%d", student_id)

    def count(self) -> int:
        with self._connect() as conn:
            return conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
