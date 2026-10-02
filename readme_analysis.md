# Workplace Diversity Analysis — Findings

[Introduction](README.md) · [Technical methods](readme.tech.md)

This analysis gives a clear, business-level view of the workforce using the information available in the employee and reporting data. The questions below focus on what the data helps us understand, what we learned, and where more information is still needed. Technical details are documented separately in the technical README.

## Main Analytical Questions

### 1. Is the company reporting structure complete?
**Why we looked at this:** Before analyzing managers, teams, or other workforce patterns, we needed to make sure the reporting structure was connected and usable.

**What we learned:** The employee reporting structure connects through management to the CEO. This gives us confidence that the organizational relationships in the available data can be used for the rest of the analysis.

### 2. What does the workforce look like overall and across departments?
**Why we looked at this:** Understanding the makeup of the workforce gives us a starting point before looking at differences across other areas.

**What we learned:** Female and male representation is not the same across the company, and the balance also changes from one department to another. This gives us a clearer picture of where employees are represented across the organization.

### 3. How does education look across the company when we break it down by department and by sex?
**Why we looked at this:** Education is one of the employee characteristics available in the dataset, so we reviewed how it appears across departments and between the recorded sex groups.

**What we learned:** Education levels vary across the workforce. We describe what the available education data shows, but we do not treat education as a substitute for job role or job level.

### 4. How does employee experience compare across the workforce?
**Why we looked at this:** Experience helps us understand the background of the workforce and provides useful context when reviewing other employee information.

**What we learned:** The recorded experience levels for female and male employees are generally similar. The dataset does not tell us how long employees have worked for this company, so experience should not be interpreted as company tenure.

### 5. What do we see when we compare employees with similar backgrounds?
**Why we looked at this:** Company-wide comparisons can mix employees from very different parts of the organization. Looking at employees with similar recorded backgrounds gives us additional context.

**What we learned:** Some differences can still appear when employees with similar available characteristics are compared. However, the dataset does not contain enough information about job roles, job levels, performance, or other factors to explain why those differences exist.

### 6. What does the management workforce look like?
**Why we looked at this:** We wanted to understand not only the overall workforce, but also how female and male employees are represented in management.

**What we learned:** Male employees make up a larger share of the management workforce than female employees in the available data. This describes the current management representation but does not explain why the difference exists.

### 7. How are the teams organized?
**Why we looked at this:** Understanding the reporting structure helps show how employees and managers are organized across the company.

**What we learned:** Employees report to managers, and those managers are connected through the company’s reporting structure up to the CEO. This gives us a clear high-level view of how teams fit into the organization.

### 8. What information needs more review or clarification?
**Why we looked at this:** Some information in the dataset cannot be interpreted confidently without additional business context.

**What we learned:** Salary and signing-bonus information is available, but important details about what those values represent are missing or unclear. Before using this information to compare employees or draw conclusions, the definitions should be confirmed by the person or team responsible for the data. Other unusual or unclear records should also be reviewed rather than treated as errors without confirmation.

## Visual Evidence

![Workforce counts](Graphics/workforce_representation.png)

![Within-department representation](Graphics/department_representation.png)

![Experience distribution](Graphics/experience_distribution.png)

![Manager representation](Graphics/leadership_representation.png)

## Recommendations and Additional Business Questions

The current analysis gives us a useful picture of the workforce, but additional information would help answer deeper business questions.

| Additional information | What it would help us understand |
| --- | --- |
| Job title, job family, and job level | Whether employees being compared have similar roles and responsibilities |
| Location, pay period, working hours, and employment type | How compensation information should be interpreted and compared |
| Company tenure and relevant prior experience | Whether length of service or previous experience helps explain workforce differences |
| Performance information and compensation policies | How pay and bonuses are determined |
| Hiring, promotion, and departure information | How workforce representation changes over time |
| Signing-bonus definitions and eligibility | What the signing-bonus information actually represents |
| Department and management responsibilities | How responsibilities differ across teams and management levels |
| Dataset source and reporting period | What time period and employee population the data represents |

The next step should be to confirm unclear data definitions before making stronger comparisons or conclusions. In particular, salary and signing-bonus information should be clarified before it is used for compensation analysis.

## Limitations

The dataset does not include important information such as job titles, formal job levels, company tenure, location, performance, working hours, or hiring and promotion history. It also records sex using only the categories available in the source data.

Because of these limitations, the analysis can describe patterns in the available workforce data, but it cannot explain why those patterns exist or determine whether a particular employment decision was fair or unfair.
