"""AI-assisted educational analysis. Inputs remain unchanged.
Requires pandas and matplotlib. Run from any working directory.
"""
from pathlib import Path
import argparse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def resolve(data, stem):
    exact = data / f'{stem}.csv'
    if exact.exists():
        return exact
    candidates = list(data.glob(f'{stem}(*).csv'))
    if len(candidates) != 1:
        raise FileNotFoundError(f'Provide one {stem}.csv in {data}')
    return candidates[0]


def trace(start, parents, ceo):
    path, seen = [], set()
    node = start
    while True:
        if node in seen:
            return 'cycle', None, path + [node]
        if node not in parents:
            return 'missing_manager', None, path + [node]
        seen.add(node)
        path.append(node)
        if pd.isna(parents[node]):
            return ('reaches_CEO', len(path)-1, path) if node == ceo else ('other_root', None, path)
        node = int(parents[node])


def main(root):
    data, graphics = root / 'Data', root / 'Graphics'
    graphics.mkdir(parents=True, exist_ok=True)
    out = data / 'Analysis_Outputs'
    out.mkdir(parents=True, exist_ok=True)
    def save(frame, name):
        frame.to_csv(out / f'{name}.csv', index=False)
    def chart(name):
        plt.tight_layout()
        plt.savefig(graphics / f'{name}.png', dpi=160)
        plt.close()

    h = pd.read_csv(resolve(data, 'company_hierarchy'))
    e = pd.read_csv(resolve(data, 'employee'))
    for label, frame, required in [
        ('hierarchy', h, ['employee_id','boss_id','dept']),
        ('employee', e, ['employee_id','signing_bonus','salary','degree_level','sex','yrs_experience'])]:
        if not set(required).issubset(frame.columns):
            raise ValueError(f'{label}: missing required columns')
        if frame.employee_id.isna().any() or frame.employee_id.duplicated().any():
            raise ValueError(f'{label}: missing or duplicate employee IDs')
    h['boss_id'] = pd.to_numeric(h.boss_id, errors='raise').astype('Int64')
    if set(h.employee_id) != set(e.employee_id):
        raise ValueError('Employee ID sets differ. Review before joining.')
    for col in ['salary','yrs_experience','signing_bonus']:
        e[col] = pd.to_numeric(e[col], errors='raise')
    if not e.signing_bonus.dropna().isin([0,1]).all():
        raise ValueError('Signing bonus contains values outside 0/1.')
    df = e.merge(h, on='employee_id', validate='one_to_one')
    ceos = h.loc[h.dept.astype('string').str.casefold().eq('ceo'), 'employee_id']
    if len(ceos) != 1:
        raise ValueError('Expected exactly one CEO department record.')
    ceo = int(ceos.iloc[0])
    parents = h.set_index('employee_id').boss_id.to_dict()
    paths = []
    for employee in h.employee_id:
        status, depth, path = trace(int(employee), parents, ceo)
        paths.append({'employee_id':employee,'hierarchy_status':status,
                      'reporting_depth':depth,'path_to_root':' > '.join(map(str,path))})
    paths = pd.DataFrame(paths)
    paths['reporting_depth'] = paths.reporting_depth.astype('Int64')
    save(paths, 'hierarchy_paths')
    df = df.merge(paths.drop(columns='path_to_root'), on='employee_id', validate='one_to_one')
    counts = h.boss_id.dropna().value_counts()
    df['direct_reports'] = df.employee_id.map(counts).fillna(0).astype(int)
    df['is_manager'] = df.direct_reports.gt(0)
    save(df, 'workplace_diversity_enriched')
    save(paths[paths.hierarchy_status.ne('reaches_CEO')], 'hierarchy_issues')

    def representation(keys, name):
        table = df.groupby(keys, dropna=False).size().rename('employee_count').reset_index()
        if len(keys) == 1:
            table['percentage'] = 100 * table.employee_count / len(df)
        else:
            table['percentage'] = 100 * table.employee_count / table.groupby(keys[:-1], dropna=False).employee_count.transform('sum')
        save(table, name)
        return table
    overall = representation(['sex'], 'sex_representation_overall')
    department = representation(['dept','sex'], 'sex_representation_department')
    representation(['sex','degree_level'], 'education_within_sex')
    representation(['dept','degree_level'], 'education_within_department')
    representation(['dept','sex','degree_level'], 'education_within_department_and_sex')
    for keys, name in [(['sex'],'experience_by_sex'),(['dept','sex'],'experience_by_department_and_sex')]:
        save(df.groupby(keys, dropna=False).yrs_experience.describe().reset_index(),name)
    df['experience_band'] = pd.cut(df.yrs_experience, [-float('inf'),5,10,20,float('inf')], labels=['5 or fewer','6–10','11–20','21+'])
    for keys, name in [(['sex'],'salary_by_sex'),(['dept','sex'],'salary_by_department_and_sex'),
                       (['degree_level','sex'],'salary_by_degree_and_sex'),(['experience_band','sex'],'salary_by_experience_and_sex')]:
        save(df.groupby(keys, observed=True, dropna=False).salary.describe().reset_index(),name)

    # Exact matched groups. Sparse groups remain visible; no causal inference.
    keys = ['dept','degree_level','yrs_experience','reporting_depth']
    valid = df[df.hierarchy_status.eq('reaches_CEO') & df.sex.isin(['M','F'])]
    cells = valid.groupby(keys+['sex'], observed=True).salary.agg(['count','mean','median']).reset_index()
    save(cells,'comparable_group_salary_cells')
    male = cells[cells.sex.eq('M')].drop(columns='sex')
    female = cells[cells.sex.eq('F')].drop(columns='sex')
    matched = male.merge(female,on=keys,suffixes=('_M','_F'),how='inner')
    matched['mean_salary_F_minus_M'] = matched.mean_F - matched.mean_M
    matched['median_salary_F_minus_M'] = matched.median_F - matched.median_M
    matched['small_group_flag'] = matched[['count_M','count_F']].min(axis=1).lt(5)
    save(matched,'comparable_group_salary_differences')

    for keys, name in [(['sex'],'bonus_by_sex'),(['dept','sex'],'bonus_by_department_and_sex')]:
        bonus = df.groupby(keys,dropna=False).signing_bonus.agg(employee_count='size',known_bonus_count='count',bonus_indicator_1_count='sum',indicator_1_rate='mean').reset_index()
        bonus['indicator_1_percentage'] = 100 * bonus.pop('indicator_1_rate')
        save(bonus,name)
    leaders = df.groupby(['is_manager','sex'],dropna=False).size().rename('employee_count').reset_index()
    leaders['percentage_within_manager_status'] = 100 * leaders.employee_count / leaders.groupby('is_manager').employee_count.transform('sum')
    save(leaders,'leadership_representation')
    teams = df[df.boss_id.notna()].groupby(['boss_id','sex'],dropna=False).size().rename('employee_count').reset_index()
    teams['percentage_within_team'] = 100 * teams.employee_count / teams.groupby('boss_id').employee_count.transform('sum')
    save(teams,'direct_team_composition')
    save(df[df.is_manager][['employee_id','sex','dept','direct_reports','reporting_depth']], 'manager_structure')

    # Review flags preserve all records. IQR is a screening heuristic.
    q1,q3 = df.salary.quantile([.25,.75]); iqr = q3-q1
    flags = df[['employee_id','salary','yrs_experience','boss_id','hierarchy_status']].copy()
    flags['salary_IQR_review'] = df.salary.lt(q1-1.5*iqr) | df.salary.gt(q3+1.5*iqr)
    flags['numeric_review'] = df.salary.isna() | df.salary.le(0) | df.yrs_experience.isna() | df.yrs_experience.lt(0) | df.yrs_experience.mod(1).ne(0)
    flags['self_reporting'] = df.employee_id.eq(df.boss_id).fillna(False)
    flags['hierarchy_review'] = df.hierarchy_status.ne('reaches_CEO')
    save(flags[flags[['salary_IQR_review','numeric_review','self_reporting','hierarchy_review']].any(axis=1)],'records_for_review')

    overall.set_index('sex').employee_count.plot.bar(title='Workforce by recorded sex category',rot=0)
    plt.ylabel('Employees'); chart('workforce_representation')
    department.pivot(index='dept',columns='sex',values='percentage').plot.bar(stacked=True,title='Representation within department')
    plt.ylabel('Percentage of department'); chart('department_representation')
    df.boxplot(column='salary',by='sex'); plt.suptitle(''); plt.title('Salary distribution by recorded sex'); plt.ylabel('Salary (source units)'); chart('salary_by_sex')
    for sex, group in df.groupby('sex'):
        plt.hist(group.yrs_experience.dropna(),bins=range(0, int(df.yrs_experience.max())+2),alpha=.5,label=str(sex))
    plt.legend(); plt.xlabel('Years of experience'); plt.ylabel('Employees'); chart('experience_distribution')
    leaders.pivot(index='is_manager',columns='sex',values='percentage_within_manager_status').plot.bar(title='Representation by manager status',rot=0)
    plt.ylabel('Percentage within status'); chart('leadership_representation')
    notes = '''# Analysis definitions and limitations

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
'''
    (out/'analysis_notes.md').write_text(notes,encoding='utf-8')
    print('Hierarchy statuses:',paths.hierarchy_status.value_counts().to_dict())
    print(f'Employees: {len(df):,}; managers: {df.is_manager.sum():,}; matched groups: {len(matched):,}')
    print(f'Tables: {out}\nCharts: {graphics}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-root',type=Path,default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    main(args.project_root.resolve())
