"""
utils.py
--------
Shared utilities for the EduPredict system:
- Centralized logging configuration (for monitoring / observability)
- Custom exception classes (for structured error handling)
- Small validation helpers used across modules

Keeping these in one place avoids duplicating error-handling / logging
logic in every module (maintainability, DRY).
"""

import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "edupredict.log")


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger that writes to console + a shared log file."""
    logger = logging.getLogger(name)
    if logger.handlers:  # avoid duplicate handlers if called more than once
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


class EduPredictError(Exception):
    """Base class for all application-specific errors."""


class ValidationError(EduPredictError):
    """Raised when user-supplied input fails validation."""


class RecordNotFoundError(EduPredictError):
    """Raised when a requested student record does not exist."""


class ModelNotTrainedError(EduPredictError):
    """Raised when a prediction is requested before a model has been trained."""


def validate_student_input(name: str, study_hours: float, attendance: float,
                            prior_score: float, assignments_submitted: int) -> None:
    """
    Validate raw student input before it enters the system.
    Raises ValidationError with a clear, actionable message on failure.
    """
    if not name or not name.strip():
        raise ValidationError("Student name cannot be empty.")
    if not (0 <= study_hours <= 24):
        raise ValidationError("study_hours must be between 0 and 24.")
    if not (0 <= attendance <= 100):
        raise ValidationError("attendance must be a percentage between 0 and 100.")
    if not (0 <= prior_score <= 100):
        raise ValidationError("prior_score must be between 0 and 100.")
    if not (0 <= assignments_submitted <= 20):
        raise ValidationError("assignments_submitted must be between 0 and 20.")
