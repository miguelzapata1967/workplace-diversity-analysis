# Analysis definitions and limitations

This script was generated with ChatGPT/Codex assistance for an educational project.
Percentages use the population named in each output. Missing categories are retained.
Sex categories are the source labels, not inferred gender identities.
Signing bonus values are validated as 0/1; interpreting 1 as receipt requires the data dictionary.
Reporting depth counts manager links to the CEO and is not a formal job grade.
A manager has at least one direct report. Team composition covers direct reports only.
Matched salary comparisons use exact department, degree, experience, and reporting depth.
Only cells containing both M and F are compared; groups under five are flagged.
These comparisons are descriptive and do not control for all compensation determinants.
IQR salary flags are review prompts, not confirmed errors. No flagged records are removed.
Missing job titles, formal levels, tenure, location, performance, working hours, currency,
salary period, and hiring/promotion history limit interpretation.
These data cannot establish discrimination, causation, or promotion rates.
The CEO's missing manager ID is preserved. Source CSVs are not overwritten.
Outputs are regenerated under Data/Analysis_Outputs and Graphics on each run.
