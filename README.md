<p align="center">
  <img src="assets/readme/banner.svg" alt="Personality meets data: a constellation of the Big Five traits and project statistics" width="100%">
</p>

<h1 align="center">Classifying Past-Month Substance Use<br>Using Personality and Demographic Features</h1>

<p align="center">
  A seven-stage exploration of survey data, personality traits, and self-reported substance use.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&amp;logo=jupyter&amp;logoColor=white" alt="Jupyter Notebook">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&amp;logo=sqlite&amp;logoColor=white" alt="SQLite database">
  <img src="https://img.shields.io/badge/scikit--learn-Baselines-F7931E?style=for-the-badge&amp;logo=scikitlearn&amp;logoColor=white" alt="scikit-learn baseline models">
</p>

<p align="center">
  <strong>ADY201m</strong> · AI, Data Science with Python &amp; SQL · <strong>AI2104</strong> · <strong>Group 7</strong>
</p>

<p align="center">
  <a href="Final_Report.ipynb"><strong>Explore the notebook</strong></a> ·
  <a href="#results">Results</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="https://archive.ics.uci.edu/dataset/373/drug-consumption-quantified">Dataset</a>
</p>

---

## 🧭 The Research Question

**Can personality scores and demographic characteristics help classify recent substance use within this survey sample?**

We explore the Big Five personality traits, impulsivity, sensation seeking, and demographic variables using Python and SQLite. The project brings data inspection, SQL cleaning, exploratory analysis, feature preparation, and two classification baselines together in [one final report](Final_Report.ipynb).

> **What the target means:** `User = 1` indicates reported use of at least one of eight selected substances during the month before the survey. The analysis classifies reported past behavior; it does not predict future use or diagnose dependence.

| Respondents | Original fields | Model inputs after encoding | Baseline models |
| :---: | :---: | :---: | :---: |
| **1,885** | **32** | **21** | **2** |

## 🗺️ Dataset Atlas

The project uses the [UCI Drug Consumption (Quantified) dataset](https://archive.ics.uci.edu/dataset/373/drug-consumption-quantified). Its demographic variables and questionnaire scores already have numeric representations supplied by the dataset creators.

| Feature group | Variables | Role |
| --- | --- | --- |
| Demographics | `Age`, `Gender`, `Education` | Model inputs |
| Big Five personality | `Nscore`, `Escore`, `Oscore`, `Ascore`, `Cscore` | Model inputs |
| Behavioral scores | `Impulsive`, `SS` | Model inputs |
| Additional demographics | `Country`, `Ethnicity` | Explored during EDA; excluded from model inputs |
| Substance-use responses | Eight selected recency fields | Define the target |
| Record reference | `ID` | Used for identification; excluded from model inputs |

### Eight Selected Substance Fields

`Amphet` · `Cannabis` · `Coke` · `Ketamine` · `LSD` · `Mushrooms` · `Legalh` · `Ecstasy`

| Original response | Reported recency | Binary indicator |
| --- | --- | :---: |
| `CL0`–`CL3` | Never used, or last used more than a month ago | **0** |
| `CL4`–`CL6` | Used within the last month, week, or day | **1** |

The target is positive when **any** of the eight indicators equals 1.

| Target class | Records | Share |
| --- | ---: | ---: |
| **User** | 921 | 48.86% |
| **Non-User** | 964 | 51.14% |

“Non-User” describes the selected substances and time window. It does not mean lifetime abstinence.

## ✨ The Analysis Journey

```mermaid
flowchart TD
    A["Source survey<br/>.data file"] --> B["SQLite<br/>data_raw"]
    B --> C["Cleaning and mapping<br/>data_clean"]
    C --> D["Target construction<br/>and EDA"]
    D --> E["One-hot encoding<br/>Stratified 80/20 split"]
    E --> F["Training set<br/>Stratified 5-fold cross-validation"]
    F --> G["Logistic Regression pipeline<br/>Scaling within each training fold"]
    F --> H["Random Forest pipeline<br/>Scaling within each training fold"]
    G --> I["Select the model<br/>Highest mean CV F1"]
    H --> I
    I --> J["Refit selected pipeline<br/>Entire training set"]
    J --> K["Test evaluation<br/>Metrics, confusion matrix, and ROC curve"]

    classDef source fill:#15243b,stroke:#6ee7c9,color:#edf8ff;
    classDef analysis fill:#241d43,stroke:#b69af6,color:#f5f0ff;
    classDef model fill:#23352e,stroke:#80cdb0,color:#f0fff7;
    class A,B,C source;
    class D,E,F,I,K analysis;
    class G,H,J model;
```

| Stage | Chapter | What happens |
| :---: | --- | --- |
| **01** | Business Understanding | Define the question, scope, target, and evaluation criteria. |
| **02** | Dataset and Initial Inspection | Define columns, load the `.data` file, select fields, and import them into SQLite. |
| **03** | Data Cleaning | Check duplicates and missing values, inspect unique values, map categories, cast datatypes, and detect outliers. |
| **04** | Target Construction and Exploratory Data Analysis | Build `User`; explore distributions, correlations, and combinations of demographic and behavioral features. |
| **05** | Data Preparation | One-hot encode age and education, separate features and target, and create a stratified 80/20 split. |
| **06** | Baseline Model Training and Evaluation | Compare pipelines using stratified 5-fold CV with scaling fitted within each training fold; select by mean F1, refit on all training rows, and evaluate the selected model on the test set. |
| **07** | Discussion, Conclusions and Recommendations | Interpret findings, describe limitations, and identify future improvements. |

**Training set:** 1,508 records · **Test set:** 377 records · **Split seed:** `42`

<a id="results"></a>

## 📊 Results

The saved outputs in [Final_Report.ipynb](Final_Report.ipynb) separate training-set model comparison from evaluation of the selected model.

### Model Comparison on Training Data

Both candidate pipelines use **Stratified 5-Fold Cross-Validation** on the 1,508 training records, with `shuffle=True` and `random_state=42`. Each pipeline fits `StandardScaler` on the seven numerical features within each training fold and passes the encoded categorical features through unchanged.

| Model | Mean CV F1 | Std CV F1 |
| --- | ---: | ---: |
| **Logistic Regression** | **0.7788** | **0.0279** |
| Random Forest | 0.7664 | 0.0361 |

**Logistic Regression** is selected by the highest mean CV F1 and refitted on the entire training set. The standard deviations describe variation across folds; the score difference has not been tested for statistical significance.

### Selected Model on the Test Set

The fitted Logistic Regression pipeline is evaluated on the 377 test records:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Logistic Regression** | **78.25%** | **0.8312** | **0.6957** | **0.7574** | **0.8707** |

Precision, recall, and F1 refer to **`User = 1`**. The selected model correctly identifies 128 of 184 Users and misses 56. Its confusion matrix is `[[167, 26], [56, 128]]`, with rows representing actual classes and columns representing predicted classes in the order Non-User, User.

These are **preliminary baseline results**. The current workflow selects the model using training-set cross-validation. The test set was inspected in earlier project versions, so fresh independent evaluation data would strengthen confirmation of the results. Hyperparameter search with `GridSearchCV` and classification threshold tuning remain future work.

### Classification in View

![Confusion matrix and ROC curve for the Logistic Regression pipeline selected by cross-validation](assets/readme/model-evaluation.png)

### Relationships in the Data

![Saved correlation heatmap of demographic variables, personality scores, and the target](assets/readme/correlation-heatmap.png)

The heatmap describes associations within the sample. Correlation alone does not establish causation or a feature’s importance in a fitted model.

<a id="quick-start"></a>

## ⚙️ Quick Start

Use **Python 3.11** and run commands from the repository root.

### 1. Get the Project

```powershell
git clone https://github.com/VicePlr/The-Five-Factor-Model-of-personality-and-evaluation-of-drug-consumption-risk.git
cd The-Five-Factor-Model-of-personality-and-evaluation-of-drug-consumption-risk
```

### 2. Create the Environment and Open JupyterLab

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt jupyterlab
.\.venv\Scripts\python.exe -m jupyterlab Final_Report.ipynb
```

### 3. Run the Report

Select the project environment, restart the kernel, and run the notebook from top to bottom. In VS Code, open [Final_Report.ipynb](Final_Report.ipynb), select the `.venv` Python kernel, and use **Restart Kernel and Run All Cells**.

The import cells rebuild the SQLite tables. The source survey remains in [`data/drug_consumption.data`](data/drug_consumption.data). SQLite support is included with Python, so a separate database server is not required.

## 📂 Repository Map

```text
.
├── Final_Report.ipynb
├── README.md
├── requirements.txt
├── database.sqlite3
├── data/
│   └── drug_consumption.data
└── assets/
    └── readme/
        ├── banner.svg
        ├── model-evaluation.png
        └── correlation-heatmap.png
```

| Artifact | Purpose |
| --- | --- |
| [Final_Report.ipynb](Final_Report.ipynb) | Complete seven-chapter analysis and presentation notebook. |
| [Source survey](data/drug_consumption.data) | Original comma-separated `.data` file with 1,885 records and 32 fields. |
| [SQLite database](database.sqlite3) | Working storage for `data_raw` and `data_clean`. |
| [Dependencies](requirements.txt) | NumPy, pandas, Matplotlib, seaborn, and scikit-learn. |

## 🔭 Research Notes

- The survey is self-reported and observational. Findings describe associations within this sample.
- UK and USA respondents account for 84.93% of the sample; 91.25% of respondents are recorded as White. Generalization to other populations requires further evaluation.
- Section 3.5 detects IQR outliers and retains the original scores. Any future clipping thresholds should be fitted within training data or training folds.
- Age and Education are one-hot encoded before the train/test split. Moving the encoder inside the modeling pipeline is a further improvement for preprocessing separation.
- Eight source records report using the fictitious substance Semeron. A sensitivity analysis of these records remains an improvement to investigate.
- The repository currently contains notebook-based analysis, rather than a deployed application or saved inference pipeline.

## 👥 The Team

| Member | Student ID |
| --- | --- |
| Hoàng Trọng Hiếu | HE211206 |
| Nguyễn Quang Minh | HE211213 |
| Nguyễn Thái Bình Dương | HE211161 |
| Ngô Anh Duy | HE211165 |

## 📜 Dataset Attribution

Fehrman, E., Egan, V., & Mirkes, E. (2015). *Drug Consumption (Quantified)*. UCI Machine Learning Repository. [DOI: 10.24432/C5TC7S](https://doi.org/10.24432/C5TC7S).

The source dataset is available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Additional background is available in [The Five Factor Model of Personality and Evaluation of Drug Consumption Risk](https://arxiv.org/abs/1506.06297).

---

<p align="center"><strong>ADY201m · AI2104 · Group 7</strong><br>Personality, data, and a carefully defined research question.</p>
