# The Five-Factor Model of Personality and Evaluation of Drug Consumption Risk

**Course:** ADY201m - AI, Data Science with Python & SQL

**Class:** AI2104 | **Group:** 7

This coursework project explores associations between demographic characteristics, Big Five personality scores, impulsivity, sensation seeking, and self-reported substance use. It uses Python and SQLite for data preparation, exploratory data analysis (EDA), and baseline binary classification.

The classification task is to identify respondents who reported using **at least one of eight selected substances within the month before the survey**. Although the project title refers to *risk*, the models classify reported recent use; they do not predict future use or diagnose dependence.

## Repository contents

| File | Purpose |
| --- | --- |
| [Group_7_ongoing_1.ipynb](Group_7_ongoing_1.ipynb) | Project framing, data inspection, cleaning, and SQLite table creation. |
| [Group_7_ongoing_2.ipynb](Group_7_ongoing_2.ipynb) | Target construction, EDA, feature engineering, and model evaluation. |
| [data/raw/drug_consumption.data](data/raw/drug_consumption.data) | Original survey file: 1,885 rows and 32 fields, without a header. |
| [sqlite3/database.sqlite3](sqlite3/database.sqlite3) | Database containing the selected raw fields and cleaned data. |
| [requirements.txt](requirements.txt) | Analysis dependencies: NumPy, pandas, Matplotlib, seaborn, and scikit-learn. |

## Dataset and target

The project uses the [UCI Drug Consumption (Quantified) dataset](https://archive.ics.uci.edu/dataset/373/drug+consumption+quantified). Its demographic variables and questionnaire scores are supplied as quantified numeric values, rather than raw questionnaire responses.

Ongoing 1 selects 21 of the source file's 32 fields:

| Fields | Role |
| --- | --- |
| `ID` | Record reference, excluded from model inputs. |
| `Age`, `Gender`, `Education`, `Country`, `Ethnicity` | Demographic variables. |
| `Nscore`, `Escore`, `Oscore`, `Ascore`, `Cscore` | Big Five scores: Neuroticism, Extraversion, Openness, Agreeableness, and Conscientiousness. |
| `Impulsive`, `SS` | Impulsivity and sensation-seeking scores. |
| `Amphet`, `Cannabis`, `Coke`, `Ketamine`, `LSD`, `Mushrooms`, `Legalh`, `Ecstasy` | Eight selected substance-use fields, described in the reports as the month-based Ecstasy pleiad. |

The substance fields record recency of use. Ongoing 1 converts each selected field to a binary indicator:

| Source code | Reported recency | Indicator |
| --- | --- | ---: |
| `CL0` | Never used | 0 |
| `CL1` | More than a decade ago | 0 |
| `CL2` | Within the last decade | 0 |
| `CL3` | Within the last year | 0 |
| `CL4` | Within the last month | 1 |
| `CL5` | Within the last week | 1 |
| `CL6` | Within the last day | 1 |

Ongoing 2 defines `User = 1` if **any** of the eight indicators is 1, and `User = 0` otherwise. The reports call these classes “User” and “Non-User.” Here, “Non-User” means no reported use of those eight substances in the last month; it does **not** mean lifetime abstinence or no use of other substances.

Recomputing the target from the substance indicators gives **921 Users (48.86%)** and **964 Non-Users (51.14%)**. The stored `User` column in the supplied database is currently all zeros; see the execution notes below before querying it directly.

## Analysis workflow

### Ongoing 1: inspection and cleaning

- Selects the 21 project fields and writes them to `data_raw`. This table is a subset of the source file, not a copy of all 32 fields.
- Checks for missing values and duplicates, excluding `ID` from the duplicate comparison. Neither check removes any rows.
- Converts substance recency codes to binary indicators. Maps age to six category codes (`0`-`5`), education to nine (`0`-`8`), gender to `0` (Female) or `1` (Male), and country and ethnicity to text labels.
- Caps the seven psychological scores at their respective `Q1 - 1.5 × IQR` and `Q3 + 1.5 × IQR` limits. This affects 82 values across 81 records and retains all 1,885 rows.
- Writes the cleaned base table to `data_clean`, with 21 columns before Ongoing 2 adds `User`.

### Ongoing 2: exploration and modeling

- Constructs `User` and explores distributions, category balance, feature-target relationships, and correlations. It also compares User rates across Age × SS, Gender × SS, and Impulsive × SS groups.
- Uses ten source features: `Age`, `Gender`, `Education`, the five personality scores, `Impulsive`, and `SS`. Country and ethnicity are explored but omitted from modeling because the sample is concentrated in a few categories.
- One-hot encodes age and education with reference categories dropped, retains binary gender, and produces **21 model input columns**. Neither `ID` nor the substance indicators are model inputs; the indicators define the target.
- Makes a stratified 80/20 split with `random_state=42`: **1,508 training rows** and **377 test rows**. Fits `StandardScaler` on the training psychological scores and applies it to the test scores.
- Trains Logistic Regression (`max_iter=1000`), Decision Tree, and Random Forest. Both tree models use `random_state=42`; other settings use library defaults.

## Baseline results

The saved model-training output reports the following scores. They were also reproduced with Python 3.11.9 during the README review. Precision, recall, and F1 refer to the positive class (`User = 1`).

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.7825 | 0.8312 | 0.6957 | 0.7574 | 0.8705 |
| Decision Tree | 0.6976 | 0.7059 | 0.6522 | 0.6780 | 0.6966 |
| Random Forest | 0.7719 | 0.8101 | 0.6957 | 0.7485 | 0.8538 |

Logistic Regression has the highest F1 and ROC-AUC on this split. These are preliminary baseline results: the same test set is used to compare and select models, and the IQR capping limits were calculated on the full dataset before splitting. A stronger evaluation should fit data-dependent preprocessing within training folds, select models and thresholds using validation data, and reserve a separate test set for final evaluation.

## Running the notebooks

Use Python 3.11 and run commands from the repository root. For a local JupyterLab setup on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt jupyterlab
.\.venv\Scripts\python.exe -m jupyterlab
```

Alternatively, open the notebooks in VS Code with the Python and Jupyter extensions and select the environment containing the analysis dependencies. `requirements.txt` does not include a notebook interface or kernel package; install `ipykernel` in that environment if needed. SQLite support is included with Python.

1. Review the execution notes below and apply the two Ongoing 2 corrections before a complete rerun.
2. Run **Group_7_ongoing_1.ipynb** from top to bottom to rebuild `data_raw` and `data_clean`.
3. Run **Group_7_ongoing_2.ipynb** from top to bottom to construct the target and run the analysis and models.

Both notebooks use paths relative to the repository root. Ongoing 1 replaces the database tables, so rerun Ongoing 2 after rebuilding them. Dependency versions are not pinned, so results may vary with library versions.

### Current execution notes

**Target updates are not committed.** Ongoing 2 calculates the correct `User` values within its first database connection, but `contextlib.closing` closes that connection without committing the `UPDATE`. The supplied database consequently has 1,885 stored zeros in `User`. In the target-construction cell, add `connection.commit()` immediately after the update, at the same indentation:

```python
    cursor.execute(update_target_column)
    connection.commit()
```

Rerunning this cell may print `duplicate column name: User` because the column already exists. The exception is caught, and the target update still runs. After committing, the stored class counts should be 964 zeros and 921 ones.

**The model-comparison cell uses a different F1 column name.** Training creates `results_df["F1"]`, but comparison looks for `"F1-Score"`, which raises `KeyError` on a fresh run. Replace the selection line with:

```python
best_model_name = results_df.loc[results_df["F1"].idxmax(), "Model"]
```

**Country and ethnicity remain text.** Ongoing 1 attempts to cast their decoded labels to `float32` and prints caught conversion errors. Remove `Country` and `Ethnicity` from that casting cell's `numeric_cols` list; retain them as text. Only the seven psychological-score columns should be cast there.

## Limitations and next steps

The survey is self-reported and observational, so the analysis describes associations within this sample and cannot establish causation. The sample is concentrated in the UK and USA, and 91.25% of respondents are recorded as White; results should not be interpreted as population prevalence or assumed to generalize to other populations.

Cross-validation, hyperparameter tuning, threshold selection, and a Streamlit demonstration are proposed in the reports but are not implemented in this repository. There is no saved model or deployed application. The current outputs are for exploratory coursework and should not be used to diagnose or make adverse decisions about individuals.

## Dataset attribution

Fehrman, E., Egan, V., & Mirkes, E. (2015). *Drug Consumption (Quantified)* [Dataset]. UCI Machine Learning Repository. [doi:10.24432/C5TC7S](https://doi.org/10.24432/C5TC7S).

UCI lists the dataset under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This attribution applies to the source dataset; the repository does not include a separate project license.
