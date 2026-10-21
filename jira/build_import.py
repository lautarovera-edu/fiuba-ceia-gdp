import csv
import datetime

OUT_DIR = "/home/lautaro/ceia/4b2026/gdp/fiuba-ceia-gdp/jira"

# ---------------------------------------------------------------------------
# 1. Sprint calendar (cuadro 5 of the project charter + start 2026-08-25,
#    end = public defense on 2027-11-15)
# ---------------------------------------------------------------------------
start = datetime.date(2026, 8, 25)

blocks = [
    ("Sprint 0", 10),
    ("Sprint 1", 3),
    ("Sprint 2", 3),
    ("Break", 4),
    ("Sprint 3", 3),
    ("Sprint 4", 3),
    ("Sprint 5", 3),
    ("Sprint 6", 3),
    ("Sprint 7", 3),
    ("Sprint 8", 3),
    ("Sprint 9", 3),
    ("Sprint 10", 3),
    ("Contingency", 2),
    ("Sprint 11", 18),
]

sprint_dates = {}
cursor = start
for name, weeks in blocks:
    end = cursor + datetime.timedelta(weeks=weeks) - datetime.timedelta(days=1)
    sprint_dates[name] = (cursor, end)
    cursor = end + datetime.timedelta(days=1)

total_weeks = sum(w for _, w in blocks)
assert total_weeks == 64, total_weeks

with open(f"{OUT_DIR}/sprint_dates.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Block", "Start", "End", "Weeks"])
    for name, weeks in blocks:
        s, e = sprint_dates[name]
        w.writerow([name, s.isoformat(), e.isoformat(), weeks])

print("Computed defense date:", sprint_dates["Sprint 11"][1], "(target: 2027-11-15)")

# ---------------------------------------------------------------------------
# 2. Epics
# ---------------------------------------------------------------------------
epics = [
    ("E1", "Data ingestion and understanding"),
    ("E2", "CIR preprocessing and representation"),
    ("E3", "Modeling and optimization for the embedded system"),
    ("E4", "Deployment and validation on the embedded system"),
    ("E5", "Project management and closeout (not part of the backlog)"),
]

# ---------------------------------------------------------------------------
# 3. User stories (cuadro 2 + section 7 acceptance criteria of the charter)
# ---------------------------------------------------------------------------
PRIORITY_MAP = {"Alta": "High", "Media": "Medium", "Baja": "Low"}

stories = [
    dict(id="HU1", epic="E1", sp=5, prio="Alta",
         summary="Reproducible ingestion pipeline for the eWINE dataset",
         desc="As a model developer, I want a reproducible pipeline that converts the eWINE dataset "
              "into labeled CIR tensors, so that I can train models without repeating the preparation "
              "work for every experiment.",
         ac=[
             "The pipeline processes all records and finishes in under 5 minutes on the development machine.",
             "Two runs with the same seed produce identical training/validation/test splits, verified by an index checksum.",
             "The test set preserves the LoS/NLoS class ratio of the original dataset within 1 percentage point.",
             "The pipeline aborts with an explicit message if any of the seven source subsets is missing or has an unexpected number of columns.",
         ]),
    dict(id="HU2", epic="E1", sp=5, prio="Media",
         summary="Exploratory analysis of the CIR by class and by environment",
         desc="As a model developer, I want an exploratory analysis of the CIR broken down by class "
              "and by environment, so that I can identify distribution biases and define a partition "
              "scheme that measures generalization.",
         ac=[
             "The report shows, for each of the seven environments, the sample count per class and descriptive statistics of the channel metrics.",
             "The report includes the average CIR and the 10th/90th percentile bands for each class and environment.",
             "The report quantifies the imbalance between environments and explicitly states the detected biases and their expected effect on generalization.",
             "The report is regenerated automatically from the data pipeline, with no manual steps.",
         ]),
    dict(id="HU3", epic="E2", sp=8, prio="Alta",
         summary="CIR alignment and normalization",
         desc="As a model developer, I want to align each CIR to its detected first path and normalize "
              "its amplitude, so that the model learns the shape of the multipath profile rather than "
              "the absolute position of the capture window.",
         ac=[
             "The alignment module places the first path at the same window position for 100% of the processed samples.",
             "Each normalized CIR has unit energy, verified with a relative tolerance of 10^-6.",
             "The accuracy comparison between at least two normalization schemes is documented on a reference classifier, using the same split and seed.",
             "The preprocessing is expressed as a chainable transform, applied identically during training and inference.",
         ]),
    dict(id="HU4", epic="E2", sp=8, prio="Media",
         summary="CIR window width selection",
         desc="As a model developer, I want to reduce the CIR window to the smallest number of samples "
              "that preserves accuracy, so that I can bound the working memory the model requires on "
              "the device.",
         ac=[
             "A sweep of window widths is run with at least four values between 32 and 256 samples.",
             "For each width, validation accuracy and required working memory (in bytes) are recorded.",
             "The selected width does not reduce validation accuracy by more than 1 percentage point relative to the best value in the sweep.",
             "The decision is documented together with the accuracy-vs-memory trade-off curve.",
         ]),
    dict(id="HU5", epic="E3", sp=8, prio="Alta",
         summary="Baseline 1D CNN for LoS/NLoS classification",
         desc="As a model developer, I want to train a one-dimensional convolutional network on the "
              "preprocessed CIR, so that I get a baseline LoS/NLoS classification to compare later "
              "variants against.",
         ac=[
             "The network reaches an F1 score of 0.88 or higher on the test set with stratified split.",
             "Accuracy, precision, recall, F1, ROC-AUC and the confusion matrix are reported.",
             "The network outperforms, in F1, the two comparison models trained on the channel metrics.",
             "Results are reproducible from the experiment log, which retains configuration, seed and weights for each run.",
         ]),
    dict(id="HU6", epic="E3", sp=13, prio="Alta",
         summary="Architecture search under a memory budget, with pruning",
         desc="As a model developer, I want to explore architecture variants subject to an explicit "
              "memory budget, so that I can choose the best accuracy-vs-size trade-off for the model.",
         ac=[
             "The search evaluates at least twelve configurations with different depth, filter counts and kernel size.",
             "Every evaluated configuration respects the fixed memory budget; configurations that exceed it are discarded automatically before training.",
             "The accuracy-vs-model-size trade-off frontier is built, and the chosen architecture is justified against it.",
             "The pruned model retains an F1 that does not drop more than 1 percentage point relative to the equivalent dense model.",
         ]),
    dict(id="HU7", epic="E3", sp=13, prio="Alta",
         summary="INT8 quantization and CMSIS-NN acceleration",
         desc="As a firmware developer, I want to quantize the selected model to 8-bit integers, so "
              "that I reduce its program-memory footprint and enable accelerated execution with "
              "CMSIS-NN.",
         ac=[
             "The quantized model occupies 64 kB of program memory or less.",
             "The F1 drop of the quantized model relative to the floating-point model does not exceed 2 percentage points.",
             "All operators in the quantized graph belong to the set implemented by LiteRT for Microcontrollers (verified with the graph-inspection tool).",
             "The most compute-intensive operations are resolved with optimized CMSIS-NN kernels (verified with the interpreter's operator profiler).",
             "The quantization procedure is documented, including the composition of the representative calibration set.",
         ]),
    dict(id="HU8", epic="E4", sp=13, prio="Alta",
         summary="Running the quantized model on the Cortex-M33 SoC",
         desc="As a firmware developer, I want to run the quantized model on the ARM Cortex-M33-based "
              "SoC, so that I can verify the inference fits in available memory and responds within "
              "the required time.",
         ac=[
             "The firmware compiles without warnings and is flashed to the evaluation board following the documented procedure.",
             "The interpreter's working memory is explicitly sized, and the firmware reports the actually used value over the console.",
             "The test harness injects at least 100 stored CIR samples and returns the inferred class for each one over the serial port.",
             "The firmware runs 1000 consecutive inferences with no resets or stack overflows.",
         ]),
    dict(id="HU9", epic="E4", sp=8, prio="Alta",
         summary="Memory, latency and PC-vs-device parity measurement",
         desc="As a firmware developer, I want to measure and compare memory usage, latency and "
              "accuracy between the personal computer and the device, so that I can demonstrate that "
              "the degradation introduced by quantization stays bounded.",
         ac=[
             "Program memory and working memory usage are reported, obtained from the linker's memory map.",
             "Inference latency is reported as median and 95th percentile over at least 1000 repetitions, measured with the processor's cycle counter; the median is 10 ms or lower.",
             "The class inferred on the device matches the class inferred on the personal computer for at least 99% of the test-set samples, with discrepancies analyzed.",
         ]),
    dict(id="HU10", epic="E4", sp=8, prio="Baja",
         summary="Comparison against the deterministic reference criterion (optional)",
         desc="As the product technical lead, I want to compare the deep-learning-based detector "
              "against the deterministic reference criterion, so that I can quantify the improvement "
              "the proposed solution provides. Optional story.",
         ac=[
             "The deterministic reference indicator is obtained for the entire test set.",
             "Confusion matrices and ROC curves for both criteria are presented on the same test set.",
             "The comparison is accompanied by a 95% confidence interval for the F1 difference between both criteria.",
             "The conclusions explicitly identify the cases where the deterministic criterion is preferable.",
         ]),
]

# ---------------------------------------------------------------------------
# 4. Tasks from cuadro 4 (section 10) -> Sub-tasks (under an HU) or Tasks (E5)
# ---------------------------------------------------------------------------
# (parent, sprint, summary, hours, priority_override)
tasks = [
    # Sprint 0 -> E5, standalone tasks
    (None, "Sprint 0", "Review the proposal and agree on scope with the client", 6, "Medium"),
    (None, "Sprint 0", "Draft the project plan using the course template", 16, "Medium"),
    (None, "Sprint 0", "Study the dataset documentation and the embedded interpreter", 8, "Medium"),

    # Sprint 1 -> HU1
    ("HU1", "Sprint 1", "Download and version the eWINE dataset and verify its integrity", 4, None),
    ("HU1", "Sprint 1", "Implement the reader that builds the CIR array and the label vector", 8, None),
    ("HU1", "Sprint 1", "Implement the reproducible stratified split by seed", 6, None),
    ("HU1", "Sprint 1", "Build the reproducible environment with a container and version control", 8, None),
    ("HU1", "Sprint 1", "Write unit tests for the reader and the split", 8, None),
    ("HU1", "Sprint 1", "Debug format inconsistencies across the seven subsets", 8, None),
    ("HU1", "Sprint 1", "Document the data pipeline and log the sprint results", 6, None),

    # Sprint 2 -> HU2
    ("HU2", "Sprint 2", "Compute descriptive statistics of the channel metrics by class and by environment", 5, None),
    ("HU2", "Sprint 2", "Plot the average CIR and its percentile bands by class and environment", 6, None),
    ("HU2", "Sprint 2", "Quantify the imbalance between environments", 4, None),
    ("HU2", "Sprint 2", "Implement the reusable exploratory analysis notebook", 8, None),
    ("HU2", "Sprint 2", "Analyze the separability of the channel metrics by class", 8, None),
    ("HU2", "Sprint 2", "Define and validate the leave-one-environment-out scheme", 8, None),
    ("HU2", "Sprint 2", "Verify the analysis reproducibility with different seeds", 4, None),
    ("HU2", "Sprint 2", "Document the findings and the biases of the dataset", 5, None),

    # Sprint 3 -> HU3
    ("HU3", "Sprint 3", "Implement first-path index detection and CIR alignment", 8, None),
    ("HU3", "Sprint 3", "Implement the energy-based and max-amplitude normalization variants", 5, None),
    ("HU3", "Sprint 3", "Compare the effect of each normalization on a reference classifier", 6, None),
    ("HU3", "Sprint 3", "Implement augmentation via Gaussian noise and window shifting", 8, None),
    ("HU3", "Sprint 3", "Evaluate the impact of augmentation on the validation set", 8, None),
    ("HU3", "Sprint 3", "Refactor the preprocessing as a chainable transform", 8, None),
    ("HU3", "Sprint 3", "Document the adopted preprocessing decisions", 5, None),

    # Sprint 4 -> HU4
    ("HU4", "Sprint 4", "Parameterize the CIR window width around the first path", 4, None),
    ("HU4", "Sprint 4", "Run the window-width sweep between 32 and 256 samples", 8, None),
    ("HU4", "Sprint 4", "Select the window width and document the trade-off", 3, None),
    ("HU4", "Sprint 4", "Instrument memory usage computation per configuration", 8, None),
    ("HU4", "Sprint 4", "Run the combined window-and-subsampling sweep", 8, None),
    ("HU4", "Sprint 4", "Analyze accuracy sensitivity to first-path detection error", 8, None),
    ("HU4", "Sprint 4", "Consolidate and version the final preprocessed dataset", 9, None),

    # Sprint 5 -> HU5
    ("HU5", "Sprint 5", "Implement the baseline one-dimensional convolutional network", 8, None),
    ("HU5", "Sprint 5", "Configure the training loop with early stopping and experiment logging", 6, None),
    ("HU5", "Sprint 5", "Train the comparison models (logistic regression and SVM) on the channel metrics", 6, None),
    ("HU5", "Sprint 5", "Train and compare the network against the comparison models", 8, None),
    ("HU5", "Sprint 5", "Evaluate the network with the leave-one-environment-out scheme", 8, None),
    ("HU5", "Sprint 5", "Analyze errors by environment and by signal-to-noise ratio", 8, None),
    ("HU5", "Sprint 5", "Document the baseline and its metrics", 4, None),

    # Sprint 6 -> HU6 (part 1)
    ("HU6", "Sprint 6", "Define the per-layer memory budget and the cost function guiding the search", 5, None),
    ("HU6", "Sprint 6", "Run the hyperparameter search over filter count, depth and kernel size", 8, None),
    ("HU6", "Sprint 6", "Implement automatic logging of experiments and their artifacts", 8, None),
    ("HU6", "Sprint 6", "Run the first search round over depth and filters", 8, None),
    ("HU6", "Sprint 6", "Run the second search round over kernel size and regularization", 8, None),
    ("HU6", "Sprint 6", "Build the accuracy-vs-memory trade-off frontier", 8, None),
    ("HU6", "Sprint 6", "Document the search results", 3, None),

    # Sprint 7 -> HU6 (part 2)
    ("HU6", "Sprint 7", "Apply structured filter pruning to the selected model", 8, None),
    ("HU6", "Sprint 7", "Retrain the pruned model and verify accuracy recovery", 8, None),
    ("HU6", "Sprint 7", "Compare the pruned model against the dense model in memory and accuracy", 8, None),
    ("HU6", "Sprint 7", "Select the final architecture and freeze its weights", 6, None),
    ("HU6", "Sprint 7", "Refactor the training code for the quantization stage", 8, None),
    ("HU6", "Sprint 7", "Verify the traceability of the logged experiments", 4, None),
    ("HU6", "Sprint 7", "Prepare the technical material for the interim review", 6, None),

    # Sprint 8 -> HU7
    ("HU7", "Sprint 8", "Apply post-training quantization to 8-bit integers", 6, None),
    ("HU7", "Sprint 8", "Verify the graph operators in LiteRT and their CMSIS-NN coverage", 5, None),
    ("HU7", "Sprint 8", "Apply quantization-aware training (if the F1 drop requires it)", 8, None),
    ("HU7", "Sprint 8", "Build the representative set for scale calibration", 5, None),
    ("HU7", "Sprint 8", "Compare floating-point vs. quantized model accuracy by environment", 8, None),
    ("HU7", "Sprint 8", "Analyze the activation distribution and adjust quantization ranges", 8, None),
    ("HU7", "Sprint 8", "Verify numerical equivalence against the reference interpreter", 4, None),
    ("HU7", "Sprint 8", "Document the quantization procedure", 4, None),

    # Sprint 9 -> HU8
    ("HU8", "Sprint 9", "Set up the firmware project with LiteRT for Microcontrollers and CMSIS-NN", 8, None),
    ("HU8", "Sprint 9", "Convert the quantized model into a C array and integrate it into the firmware image", 4, None),
    ("HU8", "Sprint 9", "Implement the test harness that injects CIR samples and replies over the serial port", 8, None),
    ("HU8", "Sprint 9", "Configure the build/debug toolchain and archive the pinned SDK version", 8, None),
    ("HU8", "Sprint 9", "Resolve interpreter working-memory allocation errors", 8, None),
    ("HU8", "Sprint 9", "Implement loading of test vectors from non-volatile memory", 8, None),
    ("HU8", "Sprint 9", "Write the internal guide for integrating the model into the firmware", 4, None),

    # Sprint 10 -> HU9 / HU10
    ("HU9", "Sprint 10", "Measure program memory and working memory usage (linker memory map)", 4, None),
    ("HU9", "Sprint 10", "Measure inference latency with the cycle counter over 1000 repetitions", 5, None),
    ("HU9", "Sprint 10", "Compare model outputs on the PC and on the device", 6, None),
    ("HU9", "Sprint 10", "Automate the measurement campaign over the full test set", 8, None),
    ("HU9", "Sprint 10", "Analyze discrepancies between both execution platforms", 8, None),
    ("HU10", "Sprint 10", "Extract the deterministic NLoS reference indicator for the test set", 6, None),
    ("HU10", "Sprint 10", "Build the confusion-matrix and ROC-curve comparison (deterministic vs. model)", 6, None),
    ("HU9", "Sprint 10", "Write the model's technical datasheet with the prototype results", 5, None),

    # Sprint 11 TTFA -> E5
    (None, "Sprint 11", "TTFA - Write chapter 1 of the thesis (general introduction)", 8, "Medium"),
    (None, "Sprint 11", "TTFA - Write chapter 2 of the thesis (specific introduction)", 10, "Medium"),
    (None, "Sprint 11", "TTFA - Write chapter 3 of the thesis (design and implementation)", 14, "Medium"),

    # Sprint 11 TTFB -> E5
    (None, "Sprint 11", "TTFB - Write chapter 4 of the thesis (experiments and results)", 12, "Medium"),
    (None, "Sprint 11", "TTFB - Write chapter 5 of the thesis (conclusions)", 5, "Medium"),
    (None, "Sprint 11", "TTFB - Review, edit and typeset the final version of the thesis", 6, "Medium"),
    (None, "Sprint 11", "TTFB - Prepare the defense presentation", 9, "Medium"),
    (None, "Sprint 11", "TTFB - Rehearse the defense and adjust the timing", 6, "Medium"),

    # Cross-cutting -> E5, no sprint (spans the whole project), labeled "cross-cutting"
    (None, None, "Hold six review meetings with the client and the advisor", 12, "Medium"),
    (None, None, "Write the progress report", 8, "Medium"),
]

# ---------------------------------------------------------------------------
# 5. Checks
# ---------------------------------------------------------------------------
total_sp = sum(s["sp"] for s in stories)
assert total_sp == 89, total_sp

total_hours = sum(h for _, _, _, h, _ in tasks)
assert total_hours == 600, total_hours

for s in stories:
    assert len(s["ac"]) >= 3, s["id"]

story_by_id = {s["id"]: s for s in stories}

# ---------------------------------------------------------------------------
# 6. Write jira_import.csv
# ---------------------------------------------------------------------------
HEADER = [
    "Issue Id", "Parent Id", "Issue Type", "Summary", "Description",
    "Epic Name", "Priority", "Story Points", "Sprint",
    "Original Estimate", "Labels",
]

rows = []

# Epics (empty Parent Id: they are the root of the hierarchy)
for eid, ename in epics:
    rows.append([eid, "", "Epic", ename, "", ename, "", "", "", "", ""])

# Stories (Parent Id = its epic's id -> Jira resolves it as Epic Link)
for s in stories:
    desc = s["desc"] + "\n\nAcceptance criteria:\n" + "\n".join(f"- {a}" for a in s["ac"])
    rows.append([
        s["id"], s["epic"], "Story", s["summary"], desc, "",
        PRIORITY_MAP[s["prio"]], s["sp"], "", "", "",
    ])

# Sub-tasks (parent = HU -> Jira resolves it as sub-task) and Tasks (parent = E5 -> Epic Link)
for i, (parent, sprint, summary, hours, prio_override) in enumerate(tasks, start=1):
    task_id = f"T{i}"
    if parent:
        story = story_by_id[parent]
        issue_type = "Subtask"
        priority = PRIORITY_MAP[story["prio"]]
        parent_id = parent
        labels = ""
    else:
        issue_type = "Task"
        priority = prio_override or "Medium"
        parent_id = "E5"
        labels = "cross-cutting" if sprint is None else ""
    rows.append([
        task_id, parent_id, issue_type, summary, "", "",
        priority, "", sprint or "", f"{hours}h", labels,
    ])

with open(f"{OUT_DIR}/jira_import.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    w.writerows(rows)

print(f"Rows written: {len(rows)} (5 epics + {len(stories)} stories + {len(tasks)} tasks)")
print(f"Total Story Points: {total_sp}")
print(f"Total hours: {total_hours}")
