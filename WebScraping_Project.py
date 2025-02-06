#!/usr/bin/env python
# coding: utf-8

# # Web Scraping Job Vacancies - Web Scraping Data Analysis Case Study

# ## Introduction
# 
# In this project, we'll build a web scraper to extract job listings from a popular job search platform. We'll extract job titles, companies, locations, job descriptions, and other relevant information.
# 
# Here are the main steps we'll follow in this project:
# 
# 1. Setup our development environment
# 2. Understand the basics of web scraping
# 3. Analyze the website structure of our job search platform
# 4. Write the Python code to extract job data from our job search platform
# 5. Save the data to a CSV file
# 6. Test our web scraper and refine our code as needed
# 
# ## Prerequisites
# 
# Before starting this project, you should have some basic knowledge of Python programming and HTML structure. In addition, you may want to use the following packages in your Python environment:
# 
# - requests
# - BeautifulSoup
# - csv
# - datetime
# 
# These packages should already be installed in Coursera's Jupyter Notebook environment, however if you'd like to install additional packages that are not included in this environment or are working off platform you can install additional packages using `!pip install packagename` within a notebook cell such as:
# 
# - `!pip install requests`
# - `!pip install BeautifulSoup`

# ## Step 1: Importing Required Libraries

# ## Step 2: Understand the basics of web scraping
# Scraping job listings can be a valuable way to gather data for analysis, but it's essential to consider the legal and ethical implications, as well as the terms of service of the websites you intend to scrape. Many popular job search platforms have terms of service that prohibit or restrict web scraping. For instance, platforms like Indeed, LinkedIn, and Glassdoor have been known to enforce anti-scraping measures and have taken legal action against unauthorized data extraction. It's crucial to review each platform's terms of service to understand their specific policies regarding data extraction. For this reason, I will be searching for an open data platform where I can get a dataset useful for my project needs. 

# ## Step 3: Find Open Data Platforms
# As I mentioned in the Step 2, identifying companies that explicitly permit web scraping can be challenging, as many organizations have policies that restrict automated data extraction. However, some platforms are more lenient or even encourage data extraction through APIs or open data initiatives. I choose the European Union Open Data Portal (EUODP) to extract job listings from. The European Union Open Data Portal provides structured datasets that can be used for analysis, making it a legal and ethical source for job data. Let's do it!
# 

# ## Method 1 (Warm Up): Download or Access the dataset via API
# I will try the analysis using multiple methods. As Method 1 I will download the dataset and then load it using Pandas. We can think of this method as a warm up step before an actual webscraping data analysis.
# 
# For the Method 2, I will try to actually scraping the same dataset from the EUODP.
# 
# The dataset I am going to use is "Open job vacancies by Infrabel". I am going to download the .csv file (CSV uses semicolon (;) as a separator.).

# ## Step 4: Load the data into Python

# In[100]:


# Use pandas to load and inspect the dataset
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
file_path = 'D:/Courses_for_development/Portfolio_DataAnalysis_projects/WebScraping_DataAnalysisProject_Coursera/joblistinfrabel.csv' 
job_list = pd.read_csv(file_path, sep = ';')
# preview the first few rows
job_list.head()


# ## Step 5: Clean and Process the Data
# What does the "cleaning data" step contains? It may contain finding anomalies (find unwanted outliers), removing duplicates, standardize column names (fix structural errors), finding missing data, filtering the information needed, etc.

# ## List column names and Null values
# To clean the dataset I wanted to first know how much null value we have for each column. So, I listed columns and summed up nulls in each column.

# In[45]:


# list(job_list.columns) # listing column names 
# column = ['Job title  FR','Job title NL','Job Id','Language role','Type','Type.1','Type.2','Apply','Publication date','Address','Postal code','Municipality','Geo Shape','Geo Punt','Street name','Number','Street suffix',' street_name_with_number','Province']
# list(job_list.isnull().sum()) # list the number of null values for each column, without column names.
# len(job_list) # gives the number of rows
job_list.isnull().sum() # adding up all null values in each column


# ## Filter job listing for Bruxelles only

# In[46]:


jobsinb = job_list.loc[job_list['Municipality'] == 'Bruxelles'] # access only the rows that have a specific data. Focus on a specific rows.
len(jobsinb)
#jobsinb


# ## Handling Missing Values: Detect & Remove NaN values
# ##### Idea: 
# In Pandas, missing values are represented by None or NaN, which can occur due to uncollected data or incomplete entries. To identify and handle the missing values, Pandas provides two useful functions: isnull() and notnull(). These functions help detect whether a value is NaN or not, making it easier to clean and preprocess data in a DataFrame.
# 
# ##### Application: 
# I want to remove null values for Job titles first, because later I will check what is the most in-demand job (title) in Bruxelles. First I need to detect rows with missing values or nulls for Bruxelles.
# 
# ##### Observations: 
# number of total null values in column "Job title NL" for the whole dataset is 35. But if we restrict ourselves only to the Municipality Bruxelles (which is rather smaller dataset), the number of nulls drops to 9 which is plausable.
# 
# Now, what remains is to drop those rows with nulls and do the analysis of jobs considering the corresponding column.
# 
# ##### Observations: 
# num. of rows for Bruxelles was 27, after dropping 9-null job titles, we should remain 18 rows in total (which is the case, check Removing NaNs section below).

# ## Detecting NaNs
# ### Filtering Data Based on Missing Values
# 
# In this case, the isnull() function is applied to the “Job title NL” column to filter and display rows with missing job title information in NL.
# 
# Question: The filtering did not work for the "Job title FR" column for some reason. 

# In[47]:


#pd.isna(job_list['Job title NL'])
# jobsinb[jobsinb.loc[ :,['Job title NL', 'Job title FR']].isnull().sum(axis=1)==2]

null_job_titles = jobsinb[jobsinb['Job title NL'].isnull()]
#len(null_job_titles)
null_job_titles


# ### Removing NaNs
# Dropping missing values explained: https://www.geeksforgeeks.org/working-with-missing-data-in-pandas/
# 
# Since we are checking job titles specifically for Bruxelles, the dataset is not huge and contains only 18 rows after dropping nulls. 
# Lets see if the dataset will become even smaller by checking if we have duplicates.

# In[48]:


# clean/drop nulls in a specific column
jobs = jobsinb.dropna(subset = ['Job title NL'])
jobs
# len (jobs)


# ## Checking for duplicates
# Boolean value False indicates that the corresponding row is no duplicate; It seems like we do not have duplicates, i.e no any repititve row, in this small dataset. 

# In[49]:


#This code gives you a data frame indicating if a row has any repetition in the data frame:

# jobs.duplicated()
no_dup = jobs.drop_duplicates()
no_dup
# len(no_dup)


# ## Results as a single .csv file - Save the processed data
# Now, it is good to export the cleaned data for further use. We will use this csv file for exploratory analysis.

# In[123]:


# results = pd.ExcelWriter('D:/Courses_for_development/Portfolio_DataAnalysis_projects/WebScraping_DataAnalysisProject_Coursera/cleanedJobs.xlsx')

# jobs.to_excel(results, sheet_name = 'Job Title List')
# results.close()
jobs.to_csv("D:/Courses_for_development/Portfolio_DataAnalysis_projects/WebScraping_DataAnalysisProject_Coursera/cleaned_job_listings.csv", index=False)


# ## Step 6: Exploratory Data Analysis (EDA)
# Since I am done with the cleaning process (it didn't take much time as the dataset was not too huge), it is now time to do some analysis with the remaining data.
# This may contain:
# - Identifying most in-demand job titles
# - Finding top hiring companies
# - Analyzing salary trends (if available)
# - Visualizing results with Matplotlib/Seaborn, etc.
# 
# The dataset that I chose to use, unfortunately, does not contain company and salary information, so I will skip those steps for now and continue with the other two steps. Analysis of those two will be left for later where I will now choose much better dataset for my project.
# 

# ## Identifying most in-demand jobs
# If we were using SQL for this analysis, we would first Group by job titles, and then sum up those job titles to find the number of them or count, then Sort by DESC. 
# 
# It should not be too different with Python Pandas either. It turned out Pandas has the groupby() function that could be useful.
# 
# ##### Pandas groupby() function is a powerful tool used to split a DataFrame into groups based on one or more columns, allowing for efficient data analysis and aggregation. It follows a “split-apply-combine” strategy, where data is divided into groups, a function is applied to each group, and the results are combined into a new DataFrame. For example, if you have a dataset of sales transactions, you can use groupby() to group the data by product category and calculate the total sales for each category.
# 
# ##### Observations:
# After applying groupby() and count(), it turned out that each job title appears 3 times in the table which is weird; it looks like there is actually duplicates, e.g., there is 3 same row with job title "Stage - Analyse Software Requirements - Master". Maybe I need to remove duplicates using different method or by chosing different column? 
# 
# Oh noo..I manually checked the table and decided there is duplicates, but there is actually no duplicates as the function indicates. Because, if we look carefully to the column "Geo Shape", we can see that even though most of the information is the same for the row, the values for that column is different, which makes those rows no duplicates. So, we are good!
# 
# Now, we can conclude that in Bruxeles each job title is equally in-demand at different publication dates. Maybe, we can check the difference accordingt to the different dates and see if it differs from the previous result.
# 

# In[50]:


# counting job titles
job_counts = jobs.groupby("Job title NL")["Job Id"].count()
job_counts


# ### Checking for demand for jobs depending on the dates they are published.
# We find the number of jobs corresponding each date that are sorted in a ascending order, the jobs are not necessarily different. 
# E.g., for the date 2024-07-17 the number of job titles is 6, but 3 is "Bachelor Technieker Elektromechanica" and 3 is "Technieker Elektromechanica", so we have two different jobs in total for this date, not all 6 is different. 

# In[51]:


# sort values according to the dates
sort_dates = jobs.sort_values(by = "Publication date")
# find the number of jobs corresponding each date that are sorted in a ascending order
sort_dates.groupby("Publication date")["Job Id"].count()


# ## Visualizing most in-demand job with Matplotlib/Seaborn
# We can use Matplotlib and Seaborn to create effective visualizations. Different methods can be used here too, such as:
# 1. Bar Chart: Most In-Demand Job Titles
# 2. Time Series: Demand Trends Over Time
# 
# 

# ## Bar Chart 
# If you have a count of job titles, a bar chart is a good choice. Since we have found the count of jobs, we can try bar chart.
# 
# ##### Observations:
# As we can also see from the chart that each job title occurs 3 times for the giving dates in Bruxelles. Then, we can conclude all are equally common jobs titles.

# In[63]:


# Assuming jobs['Job title NL'] contains job titles and you already counted occurrences, btw this is equivalent to the one we did above.
job_count = jobs['Job title NL'].value_counts()

plt.figure(figsize=(5, 5))
sns.barplot(x=job_counts.values, y=job_counts.index, palette="Blues")
plt.xlabel("Number of Listings")
plt.ylabel("Job Titles")
plt.title("Most In-Demand Job Titles")
plt.show()


# ## Time Series 
# If you have dates for job postings, you can see how demand changes over time in Bruxelles.
# 
# For the sake of trying new method of visualizing, we will also use time series. 
# 
# ##### Observations:
# What we see here is what we observed when we checked for the number of jobs for each date above. That is, the number of jobs published on 2024-07-17 is 6, which shows on that very date deman for those jobs was higher compared to other dates. In fact, on other dates jobs share equal demand rate, i.e., demand for the jobs is constant/remains same. 
# 
# Quick reminder: This results are only for Bruxelles as we filtered out other Municipalities in Step 5.

# In[103]:


# Convert date column to datetime if it's not already
# jobs['Publication date'] = pd.to_datetime(jobs['Publication date'])

# Count job postings by date
job_trends = jobs.groupby('Publication date').size()
#job_trends

plt.figure(figsize=(12, 5))
sns.lineplot(x=job_trends.index, y=job_trends.values, marker ="o", color="blue")
plt.xlabel("Date")
plt.ylabel("Number of Job Listings")
plt.title("Job Postings Over Time")
plt.xticks(rotation=45)
plt.show()


# ## Conclusion & Future Work
# Since this was just a "warm-up" before the actual web scraping project, the results weren’t particularly insightful. The data I used was sourced from an open platform rather than a real job search website. Additionally, the dataset lacked crucial details such as company names, salaries, job descriptions, and other relevant information. Because of this, I was limited in my analysis, only being able to examine job demand.
# 
# To make this exercise a bit more interesting, I focused on job listings from a single city. However, this further reduced the dataset size. While working with a smaller dataset is a good starting point, it didn’t feel very practical since real-world data is often much larger and more complex. Now, it's time to take on a more meaningful challenge!
# 
# For the next step, I plan to work with a dataset that includes all essential job vacancy details. This will make the data analysis more engaging, insightful, and informative. As I progress, I’ll explore additional aspects to analyze and refine my approach accordingly.
# 

# ## Method 2: Actual Web Scraping Challenge
# #### Done with the "warm-up", now we can "work out"!

# In[ ]:





# In[ ]:




