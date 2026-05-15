#!/usr/bin/env python
# coding: utf-8

# In[23]:


#load/import needed databases and libraries
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


# In[4]:


##Part 1: Data Management


# In[6]:


#create a SQLite database
#conn = sqlite3.connect('cell-count.csv')
#Never done this before... will investigate more


# Connect to SQLite database (created by init_db.py)
conn = sqlite3.connect('cell_count.db')

# Load cell_counts table into a df
celldf = pd.read_sql_query('SELECT * FROM cell_counts', conn)
conn.close()


# In[13]:


#read in the csv data file
#celldf = pd.read_csv('cell-count.csv')
#print(celldf.head())


# In[14]:


##Part 2: Data Overview


# In[15]:


#simple dataframe check
celldf.shape


# In[16]:


#add up total cell counts for each sample
celldf['total_count'] = celldf[['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']].sum(axis=1)


# In[17]:


#check it worked
#print(celldf.head())


# In[11]:


#create more sepecific df
sumdf = celldf[['sample', 'total_count', 'b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']].copy()

#create column with percentage for each cell type for each sample
sumdf['b_cell_%'] = (sumdf['b_cell'] / sumdf['total_count']) * 100
sumdf['cd8_t_cell_%'] = (sumdf['cd8_t_cell'] / sumdf['total_count']) * 100
sumdf['cd4_t_cell_%'] = (sumdf['cd4_t_cell'] / sumdf['total_count']) * 100
sumdf['nk_cell_%'] = (sumdf['nk_cell'] / sumdf['total_count']) * 100
sumdf['monocyte_%'] = (sumdf['monocyte'] / sumdf['total_count']) * 100

#print(sumdf.head())


# In[13]:


#reorganize df
sumdf= sumdf[['sample', 'total_count', 'b_cell', 'b_cell_%', 'cd8_t_cell', 'cd8_t_cell_%', 'cd4_t_cell', 'cd4_t_cell_%', 'nk_cell', 'nk_cell_%',
              'monocyte', 'monocyte_%']]
#print(sumdf.head())
#save to csv for easier showing
sumdf.to_csv("cell_count_summary.csv", index = False)


# In[28]:


##Part 3: Statistical Analysis


# In[16]:


#create new df with desired information
statdf = celldf[(celldf['treatment'] == 'miraclib') & (celldf['sample_type'] == 'PBMC')][['sample','treatment', 'sample_type', 'response']]
#print(statdf.head())


# In[18]:


#select data from other df to add to above
cellfq = sumdf[['sample', 'b_cell_%', 'cd8_t_cell_%', 'cd4_t_cell_%', 'nk_cell_%', 'monocyte_%']]
#print(cellfq.head())


# In[19]:


#Combine dfs so statdf has desired information
statdf = statdf.merge(cellfq, on = 'sample', how = 'left')
#print(statdf.head())


# In[22]:


#reformat df so it can be graphed
melted = statdf.melt(id_vars=['response'], value_vars=['b_cell_%', 'cd8_t_cell_%', 'cd4_t_cell_%', 'nk_cell_%', 'monocyte_%'], var_name='cell_type',
                     value_name='percentage')

#Plotting
fig, ax = plt.subplots(figsize=(14, 6))

sns.boxplot(
    data=melted, x='cell_type', y='percentage', hue='response', ax=ax )

ax.set_xlabel('Cell Type')
ax.set_ylabel('Percentage (%)')
ax.set_title('Cell Type Percentages by Response')

plt.tight_layout()
#save plot image
plt.savefig('Cell_Type_by_Response.png', dpi=150)
plt.show()


# In[37]:


#Statistical test #1
#Mann-Whitney U test
cell_per = ['b_cell_%', 'cd8_t_cell_%', 'cd4_t_cell_%', 'nk_cell_%', 'monocyte_%']

mann_whit = []
for cell in cell_per:
    yes_group = statdf[statdf['response'] == 'yes'][cell]
    no_group  = statdf[statdf['response'] == 'no'][cell]
    
    _, p = stats.mannwhitneyu(yes_group, no_group, alternative='two-sided')
    mann_whit.append({'cell_type': cell, 'p_value': round(p, 4)})

mann_whit_df = pd.DataFrame(mann_whit)
mann_whit_df.to_csv("mann_whit_results.csv", index=False)


# In[45]:


#Statistical test #2
#T-test

t_test = []
for cell in cell_per:
    yes_group = statdf[statdf['response'] == 'yes'][cell]
    no_group  = statdf[statdf['response'] == 'no'][cell]
    
    t_stat, p = stats.ttest_ind(yes_group, no_group)
    t_test.append({'cell_type': cell, 'p_value': round(p, 4)})
    stat, p = stats.ttest_ind(yes_group, no_group)
    
t_test_df = pd.DataFrame(t_test)
t_test_df.to_csv("t_test_results.csv", index = False)


# In[30]:


##Part 4: Data Subset Analysis


# In[33]:


#create a subset of the df
subset = celldf[(celldf['condition'] == 'melanoma') & (celldf['sample_type'] == 'PBMC') & (celldf['time_from_treatment_start'] == 0)
                & (celldf['treatment'] == 'miraclib')][['project', 'condition', 'sex', 'treatment', 'response', 'sample_type',
                                                        'time_from_treatment_start']]
#print(subset.head())


# In[47]:


#How many samples from each project?
project = subset.groupby('project').size().reset_index(name='count')

project.to_csv("Project_counts.csv", index = False)


# In[50]:


#How many subject were (non)responders?
response = subset.groupby('response').size().reset_index(name='count')
response.to_csv("Response_counts.csv", index = False)


# In[51]:


#How many subjects were Male/Female?
sex = subset.groupby('sex').size().reset_index(name='count')
sex.to_csv("Sex_counts.csv", index = False)


# In[53]:


qdf = celldf[(celldf['condition'] == 'melanoma') & (celldf['sex'] == 'M') & (celldf['response'] == 'yes') &
             (celldf['time_from_treatment_start'] == 0)][['b_cell']]


# In[54]:


print(qdf['b_cell'].mean())


# In[ ]:




