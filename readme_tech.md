# Workplace Diversity Analysis — Technical Methods

[Introduction](README.md) · [Analysis](readme_analysis.md)

## Inputs and Join

The script reads `Data/company_hierarchy.csv` and `Data/employee.csv`. If the canonical name is absent, it accepts exactly one matching downloaded name such as `employee(1).csv`. Input filenames are resolved independently; source files are not overwritten.

| Table | Rows | Columns |
| --- | ---: | --- |
| Hierarchy | 10,000 | employee_id, boss_id, dept |
| Employees | 10,000 | employee_id, signing_bonus, salary, degree_level, sex, yrs_experience |

Initial inspection found no exact duplicates, repeated employee IDs, blank category labels, or surrounding whitespace. Employee attributes have no missing values. The hierarchy has one missing boss ID on the CEO record. All employee IDs match across tables.

## Cleanup Record

| Operation | Reason | Effect |
| --- | --- | --- |
| Convert boss_id from float64 to nullable Int64 | Manager IDs are whole-number identifiers | Removes `.0`; preserves the missing CEO manager as `<NA>` |
| Parse salary, experience, and signing_bonus as numeric with errors raised | Validate numeric fields | Invalid numeric text stops the script rather than being silently replaced |
| Validate IDs and merge one-to-one | Prevent duplicated or lost employee rows | Retains all 10,000 employees |

No rows were removed, no missing manager was imputed, and source category labels remain unchanged. An earlier cleanup snippet saved `Data/company_hierarchy_cleaned.csv`; the full analysis script instead converts the original hierarchy in memory and saves its enriched output separately.

## Validation and Derived Fields

- Required columns must exist; missing or repeated employee IDs stop execution.
- Employee ID sets must match before a one-to-one merge.
- Nonmissing signing_bonus values must be 0 or 1. This validates encoding, not business meaning.
- The CEO is identified by the single department label `CEO`, ignoring case. The script requires exactly one such record.
- Reporting paths are followed until the CEO, another root, a missing referenced manager, or a cycle. Each employee receives a status and, for valid paths, a reporting depth.
- CEO depth is zero. Other depths count manager links; depth is not a formal job level.
- Direct-report counts come from boss_id references. Employees with at least one direct report are classified as managers.
- Experience bands are 5 or fewer, 6–10, 11–20, and 21+ years. Negative/nonintegral values are separately flagged for review.

All 10,000 reporting paths reach the CEO in the supplied data. There are 999 managers.

## Analysis Methods and Denominators

Representation percentages use total headcount overall, department headcount within departments, or the relevant education/team/manager-status population. Missing grouping categories are retained where supported by the group operation.

Experience and salary summaries include count, mean, standard deviation, minimum, quartiles, median, and maximum. Signing-bonus percentages use known indicator values; total and known counts are both exported.

Comparable salary groups match exactly on department, degree_level, yrs_experience, and reporting_depth. Only employees whose reporting path reaches the CEO and whose sex is F or M enter these comparisons. Differences are F minus M, calculated separately for mean and median salaries. Groups containing only one category do not enter the difference table, but appear in the cell summary. Either category having fewer than five observations triggers a small-group flag. There are 272 matched groups.

## Review Flags and Exclusions

Global salary IQR fences are Q1 − 1.5×IQR and Q3 + 1.5×IQR. Salaries outside these fences are review candidates, not confirmed errors. Numeric checks flag missing/nonpositive salary and missing/negative/nonintegral experience. Self-reporting and invalid hierarchy paths are also flagged.

Flagged records remain in the enriched dataset and descriptive summaries. Only the comparable-group analysis uses the explicit restrictions above. Histograms omit missing experience. No causal or inferential model is fitted.

## Outputs and Reproduction

Install Pandas and Matplotlib in your Python environment. No dependency versions are pinned. The user successfully ran the script using Python 3.14; the outputs were also checked on the supplied CSVs during development.

Save the script in `Scripts/Workplace_Diversity_Analysis.py`, then run from the project root:

```powershell
python .\Scripts\Workplace_Diversity_Analysis.py
```

The default project root is the script's parent folder's parent, so running a Downloads copy requires an explicit root:

```powershell
python "C:\Users\mexar\Downloads\Workplace_Diversity_Analysis.py" --project-root "C:\Users\mexar\OneDrive\DE_Academy\Workplace_Diversity_Analysis"
```

The script writes CSV summaries, enriched employee records, reporting paths, hierarchy issues, review candidates, and analysis notes to `Data/Analysis_Outputs/`. Five charts go to `Graphics/`. Existing generated files with the same names are overwritten when rerun; raw inputs remain unchanged.

The enriched file contains compensation and employee identifiers. Presentation findings use aggregate outputs. Input provenance and redistribution terms have not been established by these CSVs.

## AI Contribution

ChatGPT/Codex generated the script and this documentation with the user's guidance. The user ran the workflow and reviewed its outputs. The work is shared as an AI-assisted Academy learning project, with assumptions and limitations disclosed in the analysis README.

## GitHub Repository

For the complete project, including datasets, Python analysis, outputs, and documentation, visit the GitHub repository:

🔗 **GitHub Repository:** [Workplace Diversity Analysis](YOUR_GITHUB_REPOSITORY_URL)