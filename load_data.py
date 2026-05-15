#!/usr/bin/env python
# coding: utf-8

# load/import needed libraries
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


##Part 1: Data Management

# Connect to the SQLite database (created by init_db.py)
conn = sqlite3.connect('cell_count.db')

# Load the cell_counts table into a dataframe
celldf = pd.read_sql_query('SELECT * FROM cell_counts', conn)
conn.close()


##Part 2: Data Overview

# Add up total cell counts for each sample
celldf['total_count'] = celldf[['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']].sum(axis=1)

# Create more specific df with percentages
sumdf = celldf[['sample', 'total_count', 'b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']].copy()

sumdf['b_cell_%']      = (sumdf['b_cell']      / sumdf['total_count']) * 100
sumdf['cd8_t_cell_%']  = (sumdf['cd8_t_cell']  / sumdf['total_count']) * 100
sumdf['cd4_t_cell_%']  = (sumdf['cd4_t_cell']  / sumdf['total_count']) * 100
sumdf['nk_cell_%']     = (sumdf['nk_cell']     / sumdf['total_count']) * 100
sumdf['monocyte_%']    = (sumdf['monocyte']    / sumdf['total_count']) * 100

# Reorganize and save summary table
sumdf = sumdf[['sample', 'total_count', 'b_cell', 'b_cell_%', 'cd8_t_cell', 'cd8_t_cell_%',
               'cd4_t_cell', 'cd4_t_cell_%', 'nk_cell', 'nk_cell_%', 'monocyte', 'monocyte_%']]
sumdf.to_csv("cell_count_summary.csv", index=False)
print("Saved: cell_count_summary.csv")


##Part 3: Statistical Analysis

# Filter to miraclib PBMC samples
statdf = celldf[(celldf['treatment'] == 'miraclib') & (celldf['sample_type'] == 'PBMC')][
    ['sample', 'treatment', 'sample_type', 'response']
]

# Merge in cell type percentages
cellfq = sumdf[['sample', 'b_cell_%', 'cd8_t_cell_%', 'cd4_t_cell_%', 'nk_cell_%', 'monocyte_%']]
statdf = statdf.merge(cellfq, on='sample', how='left')

# Plot: Cell Type Percentages by Response
melted = statdf.melt(
    id_vars=['response'],
    value_vars=['b_cell_%', 'cd8_t_cell_%', 'cd4_t_cell_%', 'nk_cell_%', 'monocyte_%'],
    var_name='cell_type',
    value_name='percentage'
)

fig, ax = plt.subplots(figsize=(14, 6))
sns.boxplot(data=melted, x='cell_type', y='percentage', hue='response', ax=ax)
ax.set_xlabel('Cell Type')
ax.set_ylabel('Percentage (%)')
ax.set_title('Cell Type Percentages by Response')
plt.tight_layout()
plt.savefig('Cell_Type_by_Response.png', dpi=150)
plt.close()
print("Saved: Cell_Type_by_Response.png")

# Statistical test #1: Mann-Whitney U test
cell_per = ['b_cell_%', 'cd8_t_cell_%', 'cd4_t_cell_%', 'nk_cell_%', 'monocyte_%']

mann_whit = []
for cell in cell_per:
    yes_group = statdf[statdf['response'] == 'yes'][cell]
    no_group  = statdf[statdf['response'] == 'no'][cell]
    _, p = stats.mannwhitneyu(yes_group, no_group, alternative='two-sided')
    mann_whit.append({'cell_type': cell, 'p_value': round(p, 4)})

mann_whit_df = pd.DataFrame(mann_whit)
mann_whit_df.to_csv("mann_whit_results.csv", index=False)
print("Saved: mann_whit_results.csv")

# Statistical test #2: T-test
t_test = []
for cell in cell_per:
    yes_group = statdf[statdf['response'] == 'yes'][cell]
    no_group  = statdf[statdf['response'] == 'no'][cell]
    _, p = stats.ttest_ind(yes_group, no_group)
    t_test.append({'cell_type': cell, 'p_value': round(p, 4)})

t_test_df = pd.DataFrame(t_test)
t_test_df.to_csv("t_test_results.csv", index=False)
print("Saved: t_test_results.csv")


##Part 4: Data Subset Analysis

# Subset: melanoma, PBMC, time=0, miraclib
subset = celldf[
    (celldf['condition'] == 'melanoma') &
    (celldf['sample_type'] == 'PBMC') &
    (celldf['time_from_treatment_start'] == 0) &
    (celldf['treatment'] == 'miraclib')
][['project', 'condition', 'sex', 'treatment', 'response', 'sample_type', 'time_from_treatment_start']]

# Samples per project
project = subset.groupby('project').size().reset_index(name='count')
project.to_csv("Project_counts.csv", index=False)
print("Saved: Project_counts.csv")

# Responders vs non-responders
response = subset.groupby('response').size().reset_index(name='count')
response.to_csv("Response_counts.csv", index=False)
print("Saved: Response_counts.csv")

# Sex distribution
sex = subset.groupby('sex').size().reset_index(name='count')
sex.to_csv("Sex_counts.csv", index=False)
print("Saved: Sex_counts.csv")

# Mean b_cell count for melanoma male responders at time 0
qdf = celldf[
    (celldf['condition'] == 'melanoma') &
    (celldf['sex'] == 'M') &
    (celldf['response'] == 'yes') &
    (celldf['time_from_treatment_start'] == 0)
][['b_cell']]

print(f"\nMean b_cell (melanoma, male, responders, time=0): {qdf['b_cell'].mean():.4f}")
print("\nPipeline complete.")
