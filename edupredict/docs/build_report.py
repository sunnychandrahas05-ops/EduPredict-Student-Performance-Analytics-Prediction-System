"""
build_report.py
Builds the 15-section Project Report PDF required by the VITyarthi
submission guidelines, embedding the diagrams and charts already
generated under docs/diagrams/ and reports/.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, ListFlowable, ListItem
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAGRAMS = os.path.join(ROOT, "docs", "diagrams")
REPORTS = os.path.join(ROOT, "reports")
OUT_PATH = os.path.join(ROOT, "reports", "EduPredict_Project_Report.pdf")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1Custom", fontSize=18, leading=22, spaceAfter=14, textColor=colors.HexColor("#1A237E"), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="H2Custom", fontSize=14, leading=18, spaceBefore=14, spaceAfter=8, textColor=colors.HexColor("#283593"), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="BodyCustom", fontSize=10.5, leading=15, spaceAfter=8, fontName="Helvetica"))
styles.add(ParagraphStyle(name="CoverTitle", fontSize=26, leading=32, alignment=TA_CENTER, textColor=colors.HexColor("#1A237E"), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CoverSub", fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#424242")))
styles.add(ParagraphStyle(name="Caption", fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#616161"), fontName="Helvetica-Oblique"))

story = []


def h1(text):
    story.append(Paragraph(text, styles["H1Custom"]))


def h2(text):
    story.append(Paragraph(text, styles["H2Custom"]))


def body(text):
    story.append(Paragraph(text, styles["BodyCustom"]))


def bullets(items):
    story.append(ListFlowable([ListItem(Paragraph(i, styles["BodyCustom"])) for i in items],
                               bulletType="bullet", start="circle", leftIndent=18))


def image(path, width=15 * cm, caption=None):
    if os.path.exists(path):
        img = Image(path, width=width, height=width * 0.62)
        story.append(img)
        if caption:
            story.append(Paragraph(caption, styles["Caption"]))
        story.append(Spacer(1, 10))
    else:
        body(f"<i>[Diagram not found: {os.path.basename(path)}]</i>")


# ============================================================ 1. COVER PAGE
story.append(Spacer(1, 5 * cm))
story.append(Paragraph("EduPredict", styles["CoverTitle"]))
story.append(Paragraph("Student Performance Analytics &amp; Prediction System", styles["CoverSub"]))
story.append(Spacer(1, 1.5 * cm))
story.append(Paragraph("Project Report", styles["CoverSub"]))
story.append(Spacer(1, 3 * cm))
story.append(Paragraph("Course: Fundamentals of AI and ML", styles["CoverSub"]))
story.append(Paragraph("Submission Type: Build Your Own Project (Flipped Course Evaluation)", styles["CoverSub"]))
story.append(Paragraph("Platform: VITyarthi", styles["CoverSub"]))
story.append(PageBreak())

# ============================================================ 2. INTRODUCTION
h1("2. Introduction")
body("""EduPredict is a command-line artificial intelligence / machine learning system that
forecasts a student's likely academic outcome -- pass or fail, and an estimated final score --
from four everyday, easily collected inputs: daily study hours, attendance percentage, prior
exam score, and the number of assignments submitted. The project was built for the
"Fundamentals of AI and ML" flipped-course evaluation, and applies core course concepts
end-to-end: a documented data-generation process, supervised classification and regression
with scikit-learn's RandomForest family, standard evaluation metrics, and a small
production-style application (CLI, persistent storage, logging, tests) wrapped around the
model.""")

# ============================================================ 3. PROBLEM STATEMENT
h1("3. Problem Statement")
body("""Educators and mentors typically discover that a student is struggling only after a
graded assessment has already been missed or failed -- by which point there is little time
left to intervene. The early-warning signals, however, are usually available well before the
final result: how much a student studies, how consistently they attend class, how they
performed previously, and how engaged they are with coursework. EduPredict turns these
everyday signals into an early, data-driven forecast of student outcome, so that
intervention -- extra support, tutoring, outreach -- can happen while it can still change the
result.""")

# ============================================================ 4. FUNCTIONAL REQUIREMENTS
h1("4. Functional Requirements")
body("The system implements three major functional modules, each with a clear input/output structure:")
bullets([
    "<b>Data Management Module</b> -- create, read, update, and delete (CRUD) student "
    "records in a local SQLite database, with input validation and 'record not found' handling.",
    "<b>Prediction Engine (ML Module)</b> -- generate a documented synthetic training dataset, "
    "train a RandomForest classifier (pass/fail) and a RandomForest regressor (final score), "
    "persist the trained models, and expose a predict() function for new student profiles.",
    "<b>Analytics &amp; Reporting Module</b> -- compute aggregate statistics over the stored "
    "student population (averages, pass rate, min/max score) and generate chart images "
    "(score distribution, feature importance, study-hours-vs-score) plus a text report.",
])
body("The logical workflow (input &rarr; process &rarr; output) is: a student record is entered or "
     "seeded &rarr; the model is trained/evaluated on the accumulated data &rarr; predictions are "
     "generated for new students &rarr; analytics/reports summarise the whole population. "
     "See Section 7.2 for the workflow diagram.")

# ============================================================ 5. NON-FUNCTIONAL REQUIREMENTS
h1("5. Non-Functional Requirements")
nfr_data = [
    ["Requirement", "How EduPredict addresses it"],
    ["Performance", "Training on 800 synthetic samples completes in under 2 seconds; "
                     "predictions on persisted models are near-instant."],
    ["Reliability", "All database writes run inside transactions with automatic rollback on failure."],
    ["Usability", "A single, discoverable CLI with --help on every command and readable tabular output."],
    ["Maintainability", "Each module has one responsibility; modules communicate through small, "
                         "well-defined function signatures rather than shared global state."],
    ["Scalability", "SQLite + RandomForest comfortably handle tens of thousands of records for this "
                     "workload; the storage and model layers are isolated so either could be swapped out."],
    ["Security", "All external input is validated before it reaches the database or model layer, "
                 "preventing malformed or out-of-range values from being persisted."],
    ["Logging / Monitoring", "Every CRUD operation, training run, and prediction is logged with a "
                              "timestamp to reports/edupredict.log."],
    ["Error handling strategy", "A dedicated exception hierarchy (ValidationError, RecordNotFoundError, "
                                 "ModelNotTrainedError) lets the CLI distinguish user mistakes from "
                                 "system faults and report clear messages instead of raw tracebacks."],
]
t = Table(nfr_data, colWidths=[4.5 * cm, 11 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3949AB")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(PageBreak())

# ============================================================ 6. SYSTEM ARCHITECTURE
h1("6. System Architecture")
body("""EduPredict follows a layered architecture: a thin CLI layer parses user commands and
delegates to three independent functional modules (Data Management, Prediction Engine,
Analytics &amp; Reporting), all of which share a common Utilities module for logging, validation,
and exception types. Each functional module reads from and writes to its own area of
persistent storage (the SQLite database, the models/ directory, or the reports/ directory),
keeping responsibilities cleanly separated.""")
image(os.path.join(DIAGRAMS, "architecture_diagram.png"), caption="Figure 6.1 -- System Architecture Diagram")

# ============================================================ 7. DESIGN DIAGRAMS
h1("7. Design Diagrams")

h2("7.1 Use Case Diagram")
body("The primary actor (student, instructor, or evaluator) interacts with the system through eight core use cases exposed as CLI subcommands.")
image(os.path.join(DIAGRAMS, "use_case_diagram.png"), caption="Figure 7.1 -- Use Case Diagram")

h2("7.2 Workflow Diagram")
body("The end-to-end process flow, from populating data through to generating the final analytics report.")
image(os.path.join(DIAGRAMS, "workflow_diagram.png"), caption="Figure 7.2 -- Process Workflow Diagram")

h2("7.3 Sequence Diagram (Prediction Flow)")
body("Illustrates the message flow for the most frequently used operation: predicting a new student's outcome.")
image(os.path.join(DIAGRAMS, "sequence_diagram.png"), caption="Figure 7.3 -- Sequence Diagram: Predict Command")

h2("7.4 Class / Component Diagram")
body("Shows the core classes/modules, their key members, and their dependencies.")
image(os.path.join(DIAGRAMS, "class_diagram.png"), caption="Figure 7.4 -- Class / Component Diagram")

h2("7.5 ER Diagram (Database Schema)")
body("EduPredict uses a single, denormalised students table -- sufficient for this project's scope -- "
     "with nullable outcome columns that are populated once known (or by the prediction engine).")
image(os.path.join(DIAGRAMS, "er_diagram.png"), width=9 * cm, caption="Figure 7.5 -- Entity-Relationship Diagram")
story.append(PageBreak())

# ============================================================ 8. DESIGN DECISIONS
h1("8. Design Decisions &amp; Rationale")
bullets([
    "<b>SQLite over a heavier DBMS:</b> zero external setup is required, matching the "
    "'fully executable via command line' requirement with no server dependency.",
    "<b>RandomForest over a single decision tree or linear model:</b> robust to the noise "
    "injected into the synthetic dataset, handles non-linear feature interactions, and "
    "yields directly interpretable feature-importance scores -- valuable both for accuracy "
    "and for explaining predictions to a non-technical user (an instructor).",
    "<b>Separate classifier and regressor</b> rather than one multi-output model: pass/fail and "
    "exact score answer different questions (a threshold decision vs. a continuous estimate) "
    "and benefit from independently tuned hyperparameters.",
    "<b>Documented synthetic dataset generator</b> instead of scraping/using a public dataset: "
    "keeps the project self-contained, reproducible, and free of privacy concerns, while the "
    "generative rule is explicit so evaluators can verify the model is learning a real, "
    "checkable signal rather than memorising noise.",
    "<b>joblib model persistence:</b> avoids retraining on every prediction call, keeping the "
    "'predict' command fast (performance requirement).",
    "<b>argparse subcommands</b> over a single flag-heavy command: keeps each operation's "
    "required inputs explicit and self-documenting via --help (usability requirement).",
])

# ============================================================ 9. IMPLEMENTATION DETAILS
h1("9. Implementation Details")
body("The codebase is organised into three functional modules plus a shared utilities module, orchestrated by a single CLI entry point:")
bullets([
    "<b>src/database.py</b> -- StudentDatabase class; context-managed SQLite connections; "
    "transactional writes with rollback on error.",
    "<b>src/ml_model.py</b> -- generate_synthetic_dataset() builds the training data from a "
    "documented weighted-noise formula; PerformancePredictor wraps train()/predict() for both "
    "a RandomForestClassifier and a RandomForestRegressor, persisting each to models/*.joblib.",
    "<b>src/analytics.py</b> -- pure functions that take plain student-record lists/metric "
    "dictionaries and return summary statistics or saved chart file paths (matplotlib, Agg backend "
    "for headless/CLI environments).",
    "<b>src/utils.py</b> -- centralised logging configuration (console + reports/edupredict.log) "
    "and a small exception hierarchy (ValidationError, RecordNotFoundError, ModelNotTrainedError).",
    "<b>main.py</b> -- argparse-based CLI with eight subcommands (add, list, update, delete, "
    "seed, train, predict, report), each delegating to the modules above and translating "
    "exceptions into clean, user-facing error messages.",
])
body("Total: 5 source modules + 1 CLI entry point + 3 test modules = 9 Python files, "
     "satisfying the minimum 5-10 meaningful modules/files requirement, in a "
     "src/ + tests/ + docs/ package structure with Git version control.")

# ============================================================ 10. SCREENSHOTS / RESULTS
h1("10. Screenshots / Results")
body("The following charts were generated by running <font face='Courier'>python main.py report</font> "
     "on a database seeded with 200 synthetic student records, after training on 800 samples "
     "with <font face='Courier'>python main.py train --n 800</font>.")
image(os.path.join(REPORTS, "score_distribution.png"), caption="Figure 10.1 -- Distribution of Final Scores")
image(os.path.join(REPORTS, "feature_importance.png"), caption="Figure 10.2 -- Feature Importance (Pass/Fail Classifier)")
image(os.path.join(REPORTS, "study_vs_score.png"), caption="Figure 10.3 -- Study Hours vs Final Score")
story.append(PageBreak())

h2("10.1 Model Evaluation Results (800-sample training run)")
eval_data = [
    ["Metric", "Value"],
    ["Classification accuracy", "97.5%"],
    ["Classification precision", "0.9809"],
    ["Classification recall", "0.9935"],
    ["Classification F1-score", "0.9872"],
    ["Regression MAE", "5.63 points"],
    ["Regression R\u00b2", "0.7856"],
]
t2 = Table(eval_data, colWidths=[9 * cm, 6.5 * cm])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3949AB")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t2)
body("Feature importances (pass/fail classifier): attendance_percentage (0.349) &gt; "
     "prior_exam_score (0.242) &gt; study_hours_per_day (0.238) &gt; assignments_submitted (0.170) "
     "-- consistent with the weighting used to generate the dataset, confirming the model has "
     "learned the intended signal rather than spurious noise.")

# ============================================================ 11. TESTING APPROACH
h1("11. Testing Approach")
body("Unit testing (Python's built-in <font face='Courier'>unittest</font> framework) covers all three "
     "functional modules with 15 tests in total:")
bullets([
    "<b>tests/test_database.py</b> (7 tests) -- CRUD happy paths, validation-error paths "
    "(empty name, out-of-range study hours/attendance), and not-found-error paths for both "
    "get and delete.",
    "<b>tests/test_ml_model.py</b> (4 tests) -- synthetic dataset shape/columns and value-range "
    "checks; the 'predict before training' guard; and a full train-then-predict integration "
    "test asserting a strong student profile is predicted to pass.",
    "<b>tests/test_analytics.py</b> (4 tests) -- summary statistics on empty and populated "
    "student lists, and chart-file-creation checks for two plot functions.",
])
body("Run with: <font face='Courier'>python -m unittest discover -s tests -v</font>. "
     "All 15 tests pass. Each test uses an isolated temporary SQLite file (test_database.py) "
     "or plain in-memory sample data, so the suite has no side effects on the real "
     "data/edupredict.db used during manual CLI testing.")

# ============================================================ 12. CHALLENGES FACED
h1("12. Challenges Faced")
bullets([
    "<b>Balancing dataset realism with reproducibility:</b> a purely random dataset would give "
    "meaningless accuracy scores, while a deterministic rule would make classification trivial. "
    "Resolved by using a weighted-feature formula plus Gaussian noise with a fixed random seed, "
    "so results are both reproducible and genuinely non-trivial to predict.",
    "<b>Keeping the CLI usable without a GUI:</b> designed subcommands (add/list/update/delete/"
    "seed/train/predict/report) around natural user tasks rather than exposing low-level "
    "flags, and added --help text throughout.",
    "<b>Avoiding tight coupling between modules:</b> the analytics module could easily have "
    "imported the database or ML module directly; instead it only accepts plain "
    "lists/dictionaries, which is what made it straightforward to unit-test in isolation.",
    "<b>Headless chart generation:</b> matplotlib defaults to a GUI backend that fails in a "
    "pure command-line/CI environment; switched to the 'Agg' backend explicitly.",
])

# ============================================================ 13. LEARNINGS
h1("13. Learnings &amp; Key Takeaways")
bullets([
    "Applied the full supervised-learning workflow end-to-end: problem framing, feature "
    "selection, train/test split, model training, and metric-based evaluation (accuracy, "
    "precision, recall, F1, MAE, R\u00b2) for both a classification and a regression task.",
    "Learned to interpret RandomForest feature importances as a sanity check that a model "
    "has learned the intended relationship rather than memorising noise.",
    "Practised separating a system into independently testable modules connected by small, "
    "explicit interfaces rather than shared state -- directly improving testability.",
    "Reinforced that defensive input validation and a custom exception hierarchy make a "
    "command-line tool meaningfully more usable than one that surfaces raw tracebacks.",
])

# ============================================================ 14. FUTURE ENHANCEMENTS
h1("14. Future Enhancements")
bullets([
    "Replace the synthetic dataset with a real, anonymised institutional dataset once one "
    "is available, and re-validate model performance.",
    "Add hyperparameter tuning (e.g. grid search / cross-validation) to improve regression R\u00b2 "
    "beyond the current 0.79.",
    "Expose the same functionality through a lightweight REST API so a future web or mobile "
    "front end could reuse the same prediction engine.",
    "Add time-series tracking per student (multiple snapshots over a term) to predict "
    "trajectory, not just a single-point outcome.",
    "Add role-based access (instructor vs. student) if the system were extended beyond a "
    "single-user CLI tool.",
])

# ============================================================ 15. REFERENCES
h1("15. References")
bullets([
    "Pedregosa, F. et al. (2011). <i>Scikit-learn: Machine Learning in Python.</i> Journal of "
    "Machine Learning Research, 12, 2825-2830.",
    "Python Software Foundation. <i>sqlite3 -- DB-API 2.0 interface for SQLite databases.</i> "
    "Python 3 Standard Library Documentation.",
    "Hunter, J. D. (2007). <i>Matplotlib: A 2D Graphics Environment.</i> Computing in Science "
    "&amp; Engineering, 9(3), 90-95.",
    "McKinney, W. (2010). <i>Data Structures for Statistical Computing in Python.</i> "
    "Proceedings of the 9th Python in Science Conference.",
    "Course materials: Fundamentals of AI and ML (VITyarthi flipped-course evaluation).",
])

doc = SimpleDocTemplate(OUT_PATH, pagesize=A4,
                         topMargin=2 * cm, bottomMargin=2 * cm,
                         leftMargin=2 * cm, rightMargin=2 * cm,
                         title="EduPredict Project Report")
doc.build(story)
print("Report written to", OUT_PATH)
