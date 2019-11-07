#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import libraries, set options to display all columns in dataframes
import pandas as pd
import numpy as np
import re

pd.set_option('display.max_columns', None)  


# In[2]:


# Read in files
sub = pd.read_csv("2019_Q1/sub.txt", sep='\t')# parse_dates=['accepted'])) 
pre = pd.read_csv("2019_Q1/pre.txt", sep='\t') 
num = pd.read_csv("2019_Q1/num.txt", sep='\t')#, parse_dates=['ddate']) 
tag = pd.read_csv("2019_Q1/tag.txt", sep='\t') 
sub = sub.append(pd.read_csv("2019_Q2/sub.txt", sep='\t'))
pre = pre.append(pd.read_csv("2019_Q2/pre.txt", sep='\t'))
num = num.append(pd.read_csv("2019_Q2/num.txt", sep='\t'))#, parse_dates=['ddate']))
tsla = sub[sub['name'].str.contains('TESLA')]['cik']
tsla = tsla.values[0]
company = sub[sub['cik'] == tsla]
adsh = company['adsh']


# In[ ]:





# In[3]:


def get_statement():
    format_dates(num)
    line_itemsems = line_items(adsh)
    values = get_values(adsh)
    repor = seperate_reports()
    repor = seperate_years(repor)
    qtrs = pd.concat([repor['QTRS'], line_itemsems[0]], axis='columns').sort_values('line').dropna().set_index('plabel')
    return(qtrs)


# In[ ]:





# In[4]:


def format_dates(num):
    m = (num['ddate'])
    dms = list()
    for i in m.values:
        
        t = str(i)
        j = re.split(r'(\d\d\d\d)(\d\d)', t)[1:]
        dms.append("-".join(j))
    num['ddate'] = dms


# In[5]:


#format_dates(num)


# In[6]:


def line_items(adsh):
    line_items = list() 
    for item in adsh:
        tmp = pre[pre['adsh'] == item]
        tmp = tmp[tmp['stmt'] == 'IS']
        tmp = tmp.sort_values('line')
        tmp = tmp.set_index('tag')
        line_items.append(tmp)
    return(line_items)


# In[7]:


#line_itemsems = line_items(adsh)


# In[ ]:





# In[ ]:





# In[ ]:





# In[9]:


#repor = seperate_reports()


# In[10]:


def get_values(adsh):
    values = list()
    for item in adsh:
        values.append(num[num['adsh'] == item])
    return(values)


# In[11]:


values = get_values(adsh)


# In[12]:


def seperate_reports():
    for i in range(0,len(company)):
        if company.iloc[i]['form'] == '10-K':
            fy = values[i][values[i]['qtrs'] == 4]
            print("FY")
        elif company.iloc[i]['form'] == '10-Q':
            qtrs = values[i][values[i]['qtrs'] == 1]
            print("10Q")
        else:
            print("pass")
    reports = {"FY":fy, "QTRS":qtrs}
    return(reports)


# In[13]:


def seperate_years(repor):
    for k,v in repor.items():
        repor[k] = v.pivot(columns = 'ddate', values='value', index='tag')
    return(repor)


# In[92]:


repor = seperate_reports()


# In[ ]:





# In[497]:


#### START OF NEW METHOD


# In[514]:


## Items is list of tags for each filing, filings identified by adsh number
items = line_items(adsh)
# Get individual df from list of filings
items = items_df[0]
# Create series of the line items, used to select and order the correct values after getting them later
tmp = items[['line', 'plabel']]


# In[ ]:





# In[536]:


# Return the values that are reported as FY
fiscal_years_df = repor['FY']


# In[537]:


# Get the unique dates of the reports, convert them to string and select just the years to use as the labels
years = fiscal_years_df['ddate'].unique()
years = [str(x) for x in years]
year_labels = [x[:4] for x in years]
year_labels = sorted(year_labels)


# In[ ]:





# In[538]:


# Can probably combine this with the previous cell
fiscal_years = list(fiscal_years_df['ddate'].unique())
fiscal_years = sorted(fiscal_years)


# In[544]:


# Create dict of dicts
# First dict contains year_label string as keys
# Second dict contains tags as keys with amounts from the reports as values
data_dict = {}

# run loop for each of the reports
for i in range(0,len(year_labels)):
    # Get year_label for dict key and fiscal_year to select the desired year
    year_lab = year_labels[i]
    fiscal_year = fiscal_years[i]
    # Subset values df for each year
    df = fiscal_years_df[fiscal_years_df['ddate'] == fiscal_year]
    # Select the values and tags from df
    values = list(df['value'])
    tags = list(df['tag'])
    # Create dict from the tags and values and append it to the data_dict
    data_dict[year_lab] = dict(zip(tags,values))


# In[540]:


# Create df from data dict
all_values_df = pd.DataFrame(data_dict)
all_values_df.head()


# In[541]:


tmp.head()


# In[542]:


# Merge line items with values
final_df = pd.merge(tmp, all_values_df, left_index=True, right_index=True)


# In[543]:


final_df


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


pd.concat([repor['QTRS'], line_itemsems[0]], axis='columns').sort_values('line').dropna().set_index('plabel')


# In[33]:


get_statement()


# In[ ]:


########################

