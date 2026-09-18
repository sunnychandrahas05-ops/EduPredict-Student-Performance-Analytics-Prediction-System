"""
generate_diagrams.py
Generates all design-documentation diagrams (architecture, workflow,
use case, class, sequence, ER) as PNG files under docs/diagrams/,
using Graphviz. Run once: python docs/generate_diagrams.py
"""
import graphviz
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")
os.makedirs(OUT, exist_ok=True)


def save(g: graphviz.Digraph, name: str):
    g.render(filename=name, directory=OUT, format="png", cleanup=True)
    print(f"saved {name}.png")


# ---------------------------------------------------------------- 1. Architecture
arch = graphviz.Digraph("architecture", format="png")
arch.attr(rankdir="TB", fontsize="11", fontname="Helvetica")
arch.attr("node", shape="box", style="rounded,filled", fontname="Helvetica", fontsize="11")

arch.node("CLI", "CLI Layer\n(main.py / argparse)", fillcolor="#FFE0B2")
arch.node("DB", "Data Management Module\n(src/database.py)\nSQLite CRUD", fillcolor="#C8E6C9")
arch.node("ML", "Prediction Engine\n(src/ml_model.py)\nRandomForest Classifier + Regressor", fillcolor="#BBDEFB")
arch.node("AN", "Analytics & Reporting\n(src/analytics.py)\nStats + Charts", fillcolor="#D1C4E9")
arch.node("UT", "Utilities\n(src/utils.py)\nLogging, Validation, Exceptions", fillcolor="#F0F4C3")
arch.node("STORE", "Persistent Storage\ndata/edupredict.db\nmodels/*.joblib\nreports/*", shape="cylinder", fillcolor="#FFCDD2")

arch.edge("CLI", "DB")
arch.edge("CLI", "ML")
arch.edge("CLI", "AN")
arch.edge("DB", "UT", style="dashed")
arch.edge("ML", "UT", style="dashed")
arch.edge("AN", "UT", style="dashed")
arch.edge("DB", "STORE")
arch.edge("ML", "STORE")
arch.edge("AN", "STORE")
save(arch, "architecture_diagram")

# ---------------------------------------------------------------- 2. Workflow
wf = graphviz.Digraph("workflow", format="png")
wf.attr(rankdir="LR", fontsize="11", fontname="Helvetica")
wf.attr("node", shape="box", style="rounded,filled", fillcolor="#E1F5FE", fontname="Helvetica", fontsize="10")

wf.node("start", "Start", shape="ellipse", fillcolor="#C8E6C9")
wf.node("seed", "1. Seed / Add\nStudent Records")
wf.node("train", "2. Train Models\n(classifier + regressor)")
wf.node("eval", "3. Evaluate\n(accuracy, F1, R2, MAE)")
wf.node("predict", "4. Predict Outcome\nfor a New Student")
wf.node("report", "5. Generate Analytics\nReport + Charts")
wf.node("end", "End", shape="ellipse", fillcolor="#FFCDD2")

wf.edge("start", "seed")
wf.edge("seed", "train")
wf.edge("train", "eval")
wf.edge("eval", "predict")
wf.edge("predict", "report")
wf.edge("report", "end")
save(wf, "workflow_diagram")

# ---------------------------------------------------------------- 3. Use Case
uc = graphviz.Digraph("usecase", format="png")
uc.attr(rankdir="LR", fontsize="11", fontname="Helvetica")
uc.node("Student/Admin", shape="none", fontname="Helvetica", fontsize="11")
uc.attr("node", shape="ellipse", style="filled", fillcolor="#FFF9C4", fontname="Helvetica", fontsize="10")
for uc_name in ["Add Student Record", "View / List Students", "Update Record",
                "Delete Record", "Seed Synthetic Data", "Train Model",
                "Predict Performance", "Generate Report"]:
    uc.node(uc_name)
    uc.edge("Student/Admin", uc_name)
save(uc, "use_case_diagram")

# ---------------------------------------------------------------- 4. Class Diagram
cls = graphviz.Digraph("class", format="png")
cls.attr(rankdir="TB", fontsize="10", fontname="Helvetica")
cls.attr("node", shape="record", fontname="Helvetica", fontsize="9")

cls.node("StudentDatabase", "{StudentDatabase|+ db_path: str|+ add_student()\\l+ get_student()\\l"
                             "+ list_students()\\l+ update_student()\\l+ delete_student()\\l+ count()\\l}")
cls.node("PerformancePredictor", "{PerformancePredictor|+ classifier: RandomForestClassifier|"
                                  "+ regressor: RandomForestRegressor|+ train()\\l+ predict()\\l}")
cls.node("AnalyticsModule", "{analytics (module)||+ summarize_students()\\l+ plot_score_distribution()\\l"
                             "+ plot_feature_importance()\\l+ plot_study_vs_score()\\l+ generate_text_report()\\l}")
cls.node("Utils", "{utils (module)||+ get_logger()\\l+ validate_student_input()\\l"
                   "+ ValidationError\\l+ RecordNotFoundError\\l+ ModelNotTrainedError\\l}")
cls.node("CLI", "{main (CLI)||+ build_parser()\\l+ cmd_add() / cmd_list() / ...\\l+ main()\\l}")

cls.edge("CLI", "StudentDatabase", label="uses")
cls.edge("CLI", "PerformancePredictor", label="uses")
cls.edge("CLI", "AnalyticsModule", label="uses")
cls.edge("StudentDatabase", "Utils", label="uses", style="dashed")
cls.edge("PerformancePredictor", "Utils", label="uses", style="dashed")
save(cls, "class_diagram")

# ---------------------------------------------------------------- 5. Sequence (predict flow)
seq = graphviz.Digraph("sequence", format="png")
seq.attr(rankdir="LR", fontsize="10", fontname="Helvetica")
seq.attr("node", shape="box", style="filled", fillcolor="#E8EAF6", fontname="Helvetica", fontsize="9")
seq.node("User")
seq.node("CLI_n", "CLI (main.py)")
seq.node("Predictor", "PerformancePredictor")
seq.node("Model", "Saved Model\n(joblib)")

seq.edge("User", "CLI_n", label="python main.py predict ...")
seq.edge("CLI_n", "Predictor", label="predict(features)")
seq.edge("Predictor", "Model", label="load / infer")
seq.edge("Model", "Predictor", label="prediction")
seq.edge("Predictor", "CLI_n", label="result dict")
seq.edge("CLI_n", "User", label="printed prediction")
save(seq, "sequence_diagram")

# ---------------------------------------------------------------- 6. ER Diagram
er = graphviz.Digraph("er", format="png")
er.attr(rankdir="LR", fontsize="10", fontname="Helvetica")
er.attr("node", shape="record", fontname="Helvetica", fontsize="9")
er.node("students", "{students|"
                     "id : INTEGER (PK)\\l"
                     "name : TEXT\\l"
                     "study_hours_per_day : REAL\\l"
                     "attendance_percentage : REAL\\l"
                     "prior_exam_score : REAL\\l"
                     "assignments_submitted : INTEGER\\l"
                     "final_score : REAL (nullable)\\l"
                     "passed : INTEGER (nullable)\\l"
                     "created_at : TEXT\\l}")
save(er, "er_diagram")

print("All diagrams generated in", OUT)
