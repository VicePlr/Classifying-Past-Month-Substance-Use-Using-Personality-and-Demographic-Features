# The Five-Factor Model of Personality and Drug Consumption Risk

**Course:** ADY201m - AI, Data Science with Python & SQL | **Class:** AI2104 | **Group:** 7

## Project overview

This project explores how demographic characteristics, Big Five personality scores, impulsivity, and sensation seeking are associated with self-reported recent use of selected substances. It also builds baseline binary-classification models using the UCI Drug Consumption (Quantified) survey dataset.

The project title uses the word *risk*, but the current target is specifically **reported use of at least one selected substance during the month before the survey**. The model does not diagnose substance use disorder, predict future use, or establish that personality causes substance use. Findings are exploratory and intended for coursework and public-health discussion.

## Dataset

The source is the [Drug Consumption (Quantified) dataset](https://archive.ics.uci.edu/dataset/373/drug+consumption+quantified) from the UCI Machine Learning Repository. The local raw file is [`data/raw/drug_consumption.data`](data/raw/drug_consumption.data).

The source file contains 1,885 records and 32 comma-separated fields, with no header row. The demographic and questionnaire fields use numeric encodings supplied by UCI; they are not raw questionnaire responses.

| Position | Field(s) | Description |
| --- | --- | --- |
| 1 | `ID` | Source-record reference; it is not used as a model feature. |
| 2-6 | `Age`, `Gender`, `Education`, `Country`, `Ethnicity` | Demographic categories represented by numeric codes. |
| 7-11 | `Nscore`, `Escore`, `Oscore`, `Ascore`, `Cscore` | NEO-FFI-R scores: Neuroticism, Extraversion, Openness, Agreeableness, and Conscientiousness. |
| 12 | `Impulsive` | BIS-11 impulsiveness score. |
| 13 | `SS` | ImpSS sensation-seeking score. |
| 14-32 | `Alcohol`, `Amphet`, `Amyl`, `Benzos`, `Caff`, `Cannabis`, `Choc`, `Coke`, `Crack`, `Ecstasy`, `Heroin`, `Ketamine`, `Legalh`, `LSD`, `Meth`, `Mushrooms`, `Nicotine`, `Semer`, `VSA` | Ordered recency-of-use classes for the named substances. `Semer` is the fictitious drug Semeron; `VSA` is volatile substance abuse. |

Each substance field uses one of the source's ordered `CL` codes:

| Code | Reported recency |
| --- | --- |
| `CL0` | Never used |
| `CL1` | More than a decade ago |
| `CL2` | Within the last decade |
| `CL3` | Within the last year |
| `CL4` | Within the last month |
| `CL5` | Within the last week |
| `CL6` | Within the last day |

### Target and model features

Ongoing 1 focuses on eight members of the Ecstasy pleiad: `Amphet`, `Cannabis`, `Coke`, `Ketamine`, `LSD`, `Mushrooms`, `Legalh`, and `Ecstasy`. For each selected substance, the report maps `CL0`-`CL3` to 0 and `CL4`-`CL6` to 1. Ongoing 2 defines `User` as 1 when any of those eight indicators is 1, and 0 otherwise.

The current model uses `Age`, `Gender`, `Education`, the five personality scores, `Impulsive`, and `SS`. `Age` and `Education` are one-hot encoded, `Gender` is retained as a binary feature, and the seven psychological scores are standardized. `Country` and `Ethnicity` are examined in EDA but left out of the main model because the sample is heavily concentrated in a few categories.

## Work completed

### Ongoing 1 - business understanding and data preparation

- Inspected the raw UCI survey and selected the demographic, personality, impulsivity, sensation-seeking, and eight substance fields relevant to the project.
- Loaded the source and cleaned data into the SQLite database at [`sqlite3/database.sqlite3`](sqlite3/database.sqlite3), in tables named `data_raw` and `data_clean`.
- The cleaned base table has 1,885 rows and 21 columns. The report found no missing values or duplicate rows.
- Capped psychological-score outliers using IQR limits while keeping all 1,885 records. The report detected 82 outlier values across 81 records before capping.

### Ongoing 2 - EDA, feature engineering, and baseline models

- Examined target and feature distributions, category balance, bivariate relationships, correlations, and three multivariate combinations: Age x SS, Gender x SS, and Impulsive x SS, each compared against `User`.
- Found 921 Users (48.86%) and 964 Non-Users (51.14%) in the sample. The strongest reported Pearson correlations with `User` were SS (0.442), Age (-0.431), Openness / `Oscore` (0.376), and Impulsivity (0.320). Correlation describes association, not causation.
- Used a stratified 80/20 train-test split (`random_state=42`), resulting in 1,508 training rows and 377 test rows.
- Compared Logistic Regression, Decision Tree, and Random Forest baselines. The saved Ongoing 2 results are:

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.7825 | 0.8312 | 0.6957 | 0.7574 | 0.8705 |
| Decision Tree | 0.6976 | 0.7059 | 0.6522 | 0.6780 | 0.6966 |
| Random Forest | 0.7719 | 0.8101 | 0.6957 | 0.7485 | 0.8538 |

These are preliminary results from one holdout split. The report compares and selects models using the same test split, so the scores should not be treated as a final unbiased estimate. Cross-validation, hyperparameter tuning, and threshold analysis are planned follow-up work.

### Supplementary country investigation

[`on_going 2.ipynb`](<on_going 2.ipynb>) is a separate descriptive analysis. It recomputes `User` in memory, compares country-level rates with Wilson confidence intervals, and examines UK/USA age composition and within-age rates. In this sample, the observed rate was 23.7% in the UK (247/1,044) and 85.5% in the USA (476/557). The notebook notes that these differences are descriptive and do not establish a country effect or national representativeness; some country-age groups are very small.

## Repository layout

```text
.
├── Group_7_ongoing_1.ipynb       # Business understanding, data inspection, and cleaning
├── Group_7_ongoing_2.ipynb       # EDA, feature preparation, and baseline classification
├── on_going 2.ipynb              # Supplementary country and age investigation
├── data/
│   └── raw/
│       └── drug_consumption.data # Original UCI data file
├── sqlite3/
│   └── database.sqlite3          # SQLite database used by the reports
├── requirements.txt
└── README.md
```

## Running the notebooks

Install the analysis dependencies in a Python environment:

```bash
python -m pip install -r requirements.txt
```

Open the notebooks in Jupyter or VS Code from the repository root; their data and database paths are relative to that directory. Run Ongoing 1 first when rebuilding the SQLite tables, then use Ongoing 2. The supplementary country notebook reads the cleaned table and derives `User` in memory without changing the database.

**Current execution note:** In Ongoing 2, the model-training cell names its metric column `F1`, while the model-comparison cell looks for `F1-Score`. Align those names before rerunning the model-comparison cell; the table above reflects the saved report results.

## Limitations and responsible use

- The dataset is self-reported and observational. It cannot support causal conclusions.
- The sample is concentrated in the UK and USA and is 91.25% White, limiting how well results represent other populations.
- The target represents recent self-reported use of the selected substances only; it is not a diagnosis, a measure of dependence, or a prediction of future behavior.
- Model outputs should not be used to label or make adverse decisions about individuals. Any future use would require broader validation, careful privacy protections, and assessment of sampling bias and misclassification.
