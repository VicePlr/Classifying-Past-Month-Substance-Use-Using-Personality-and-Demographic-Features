# ADY201m 

## Raw dataset

The project uses the **Drug Consumption (Quantified)** dataset from the
[UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/373/drug+consumption+quantified).
The local copy is [`data/raw/drug_consumption.data`](data/raw/drug_consumption.data).

The file contains 1,885 records and 32 comma-separated fields per record. It has
no header row; fields appear in the following order:

| Position | Field(s) | Description |
| --- | --- | --- |
| 1 | `ID` | Record reference from the original database. It does not identify a participant. |
| 2–6 | `Age`, `Gender`, `Education`, `Country`, `Ethnicity` | Participant demographics. Values are numeric encodings of categories, not raw text. |
| 7–11 | `Nscore`, `Escore`, `Oscore`, `Ascore`, `Cscore` | NEO-FFI-R personality scores: Neuroticism, Extraversion, Openness to experience, Agreeableness, and Conscientiousness. |
| 12 | `Impulsive` | Impulsiveness score measured by BIS-11. |
| 13 | `SS` | Sensation-seeking score measured by ImpSS. |
| 14–32 | `Alcohol`, `Amphet`, `Amyl`, `Benzos`, `Caff`, `Cannabis`, `Choc`, `Coke`, `Crack`, `Ecstasy`, `Heroin`, `Ketamine`, `Legalh`, `LSD`, `Meth`, `Mushrooms`, `Nicotine`, `Semer`, `VSA` | Consumption class for each named substance. `Semer` is the fictitious drug Semeron; `VSA` is volatile substance abuse. |

The demographic and questionnaire fields use the numeric encodings provided by
UCI; the values are not original questionnaire responses. Each substance field
uses an ordinal `CL` code describing reported recency of use:

| Code | Meaning |
| --- | --- |
| `CL0` | Never used |
| `CL1` | Used over a decade ago |
| `CL2` | Used in the last decade |
| `CL3` | Used in the last year |
| `CL4` | Used in the last month |
| `CL5` | Used in the last week |
| `CL6` | Used in the last day |