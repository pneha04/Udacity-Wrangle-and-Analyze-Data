#!/usr/bin/env python
# coding: utf-8

# # Project - Wrangle and Analyze data
# 
# Tasks in this project are as follows:
# 
# Data wrangling, which consists of:
# 
# Gathering data
# 
# Assessing data
# 
# Cleaning data
# 
# Storing, analyzing, and visualizing  wrangled data
# 
# Reporting on 1)  data wrangling efforts and 2)  data analyses and visualizations

# ## Introduction
# The dataset that I will be wrangling (and analyzing and visualizing) is the tweet archive of Twitter user @dog_rates, also known as WeRateDogs. WeRateDogs is a Twitter account that rates people's dogs with a humorous comment about the dog. These ratings almost always have a denominator of 10. The numerators, though? Almost always greater than 10. 11/10, 12/10, 13/10, etc. Why? Because "they're good dogs Brent." WeRateDogs has over 4 million followers and has received international media coverage.
# 
# Wrangling of data is done in three steps:
# 1. Gather
# 2. Assess
# 3. Clean

# Below all the steps are explained and shown in detail

# ## Gather
# Data can be gathered from many sources and in many ways. In this projext I will gather data using three ways.
# 1. File on hand. In this case I alreday have the file and just need to open it using Pandas DataFrame.
# 2. Downloading a file programmatically from a given url using request().
# 3. Gathering data from a specfic website/archive using API.

# In[191]:


# Import necessary packages
import pandas as pd
import requests
import os
import json
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import re


# In[192]:


#Open file 'twitter-archive-enhanced.csv' into a pandas DataFrame
twitter_archive=pd.read_csv('twitter-archive-enhanced.csv')
twitter_archive.head()


# In[193]:


# Download the file programmatically using request()
image_url='https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
response=requests.get(image_url)
response.content


# As we can see the contents of the response variable are in bytes format. To make the contents in human readable format we have to write the contents of the response variable in a file with mode as 'write binary'.
# When we open the file into a pandas DataFrame, the contents become human readable.
# 

# In[194]:


#Write response.content into a file with mode as 'write binary(wb)'
with open(os.path.join(image_url.split('/')[-1]),mode='wb') as file:
    file.write(response.content)


# In[195]:


# Read file into a pandas DataFrame
image_df=pd.read_csv('image-predictions.tsv',sep='\t')
image_df.head()


# 
# ## Disclaimer: The tweets which have been deleted from twitter archive- I will be filling those with Null values

# In[196]:


# Authenticate your credentials
'''
import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
'''


# In[197]:


#Gather data from Twitter API using tweepy package.
'''
id_list=list(twitter_archive.tweet_id)
data={}
data['tweet']=[]
for id_of_tweet in id_list:
        try:
            tweet = api.get_status(id_of_tweet,tweet_mode='extended',parser=tweepy.parsers.JSONParser())
            
            favourites_count =tweet['user']['favourites_count']
            retweet_count=tweet['retweet_count']
            day_of_the_week=tweet['created_at'].split()[0]
            month=tweet['created_at'].split()[1]
        except:
            favourites_count =None
            retweet_count=None
            day_of_the_week=None
            month=None
        
        data['tweet'].append({'tweet_id':id_of_tweet,
                             'favourites_count':favourites_count,
                             'retweet_count':retweet_count,
                             'day_of_the_week':day_of_the_week,
                             'month':month})
'''


# In[198]:


# Write the json object(dictnary) into a file
'''
with open('tweet_json.txt', 'w') as outfile:  
    json.dump(data, outfile)
'''


# In[199]:


# Read the file into a pandas DataFrame
tweet_id=[]
favourites_count=[]
retweet_count=[]
day_of_the_week=[]
month=[]
with open('tweet_json.txt') as json_file:  
    data = json.load(json_file)
    for p in data['tweet']:
        retweet_count.append(p['retweet_count'])
        favourites_count.append(p['favourites_count'])
        tweet_id.append(p['tweet_id'])
        day_of_the_week.append(p['day_of_the_week'])
        month.append(p['month'])


# In[200]:



twitter_api=pd.DataFrame({'tweet_id':tweet_id,
               'favourites_count':favourites_count,
               'retweet_count':retweet_count,
                         'day_of_the_week':day_of_the_week,
                         'month':month})
twitter_api.head()


# ## Assess
# The second step in data wrangling process is assessing the data. Once the data has been gathered, it has to be inspected for two things 
# 1. Quality : Data that has quality issues has issues with content like missing, duplicate or incorrect data. This type of data is called dirty data.
# 2. Tidiness : Data that has tidiness issues has specific structural issues. These structural issues slow down the process of cleaning and visualising data. This type of data is called messy data. Data to be tidy it has to satisfy 3 critera.
# a. Each variable forms a column.
# b. Each observation forms a row.
# c. Each observational unit forms a table
# 
# Data can be both dirty and messy.
# 
# Data can be assessed for these two issues in two ways
# 1. Visual
# 2. Programmatic
# 
# These assessments are then documented so that the cleaning process becomes easier. Only the observation is written down and not how to clean the data.

# ### Visual Assessment
# Visual Assessment is done simply by going through the dataset and catching anything that looks wrong. Visual assessment in python is difficult as large datasets are collasped by python. Visual assessment is better carried out in Google docs or sheets.

# In[201]:


#Visual assessment of twitter_archive_enhanced.csv dataset
twitter_archive


# In[202]:


#Visual assessment of image_predictions.tsv dataset
image_df


# In[203]:


# Visual assessment of tweet_json.txt dataset
twitter_api


# ### Programmatic Assessment
# Programmatic assessment means using python functions such as info(), describe() or sample() to find dirty or untidy data.
# Common functions are 
# 1. info()
# 2. describe()
# 3. values_count()
# 4. isnull()
# 5. sample()

# In[204]:


twitter_archive.info()


# In[205]:


image_df.info()


# In[206]:


twitter_api.info()


# In[207]:


twitter_archive.describe()


# In[208]:


twitter_api.describe()


# In[209]:


twitter_archive.sample(5)


# In[210]:


image_df.sample(5)


# In[211]:


twitter_archive['rating_numerator'].value_counts()


# In[212]:


twitter_archive['name'].value_counts()


# In[213]:


twitter_archive['source'].value_counts()


# In[214]:


image_df['p1_dog'].value_counts()


# In[215]:


image_df['p2_dog'].value_counts()


# In[216]:


image_df['p3_dog'].value_counts()


# In[217]:


twitter_api['day_of_the_week'].value_counts()


# In[218]:


twitter_api['month'].value_counts()


# In[219]:


sum(twitter_archive.duplicated())


# In[220]:


sum(twitter_api.duplicated())


# In[221]:


sum(image_df.duplicated())


# ### Quality
# 
# #### `twitter_archive table`
# -  rating_denominator has values more than 10
# -  for tweet_id 887517139158093824 name is 'such'
# -  name column has 'O' instead of O'Malley
# -  Erroneous datatpes (timestamp, retweeted_status_timestamp)
# -  Decimal values such 13.5 are interpreted as 5.
# -  name column has names such as 'a' ,'the' ,'an'
# -  html tags in source column
# -  missing values have None instead of Nan
# 
# 
# #### `image_predictions table`
# -  smallcase names in p1,p2 and p3
# -  names have '_' or '-' instead of space between them
# -  missing data (2075 instead of 2356)
# -  ambigous column names (p1,p1_conf,p1_dog)
# 
# #### `json_tweet table`
# -  missing values in favourites_count,retweet_count,day_of_the_week and month
# 
# ### Tidiness
# 
# #### `twitter_archive table`
# -  instead of seperate column for each dog stage(doggo,floofer,pupper,puppo) single column called dog_stage
# 
# #### `json_tweet table`
# -  should be joined with twitter archive table as it contains the information regarding the tweets.
# 
# #### `image_predictions table`
# -  can be joined with twitter archive table as single column for dog_breed

# ## Clean
# The final step of data wrangling process is data cleaning.There are three steps in data cleaning.
# 
# 1. Define- In words define the approach to clean data
# 2. Code- Code to clean data
# 3. Test-Test whether your code has worked properly or not
# 

# In[222]:


# Make copies of tables
twitter_archive_clean=twitter_archive.copy()
image_df_clean=image_df.copy()
twitter_api_clean=twitter_api.copy()


# ### Missing data
# **Quality Issue-1**
# 
# All the tables have columns which have missing data. 
# `twitter_archive table` has columns like in_reply_to_status_id, in_reply_to_user_id etc that have missing data. This either means that that data does not exsist at all or there was some issues while retriving the data. Getting this data is impossible and hence it will remain as it is.
# `image_predictions table` has only 2075 records whereas there are supposed to be 2356. It means that the data was lost while it was being documented. Retrieving this data is almost impossible.
# `json_tweet table` also has missing data. These tweets have been deleted from the twitter archive. To make joining of twitter_archive and json_tweet tables easier I will drop the coressponding tweet_id from twitter_archive table

# **Define**
# 
# Drop rows from `twitter_archive and json_tweet table` of tweet_id that have missing data in `json_tweet table`

# **Code**

# In[223]:


#Create list of tweet_id's that have missing data
missing_tweet_list=list(twitter_api_clean[twitter_api_clean['favourites_count'].isnull()]['tweet_id'])
missing_tweet_list


# In[224]:


#Drop rows from twitter_archive and json_tweet tables
for tweet_id in missing_tweet_list:
    twitter_archive_clean=twitter_archive_clean.drop(twitter_archive_clean[twitter_archive_clean.tweet_id==tweet_id].index)
    twitter_api_clean=twitter_api_clean.drop(twitter_api_clean[twitter_api_clean.tweet_id==tweet_id].index)


# **Test**

# In[225]:


# Check the number of rows in both datasets
twitter_archive_clean.shape,twitter_api_clean.shape


# **Quality Issue-2**
# 
# **image_predictions table**
# 
# **smallcase names in p1,p2 and p3**
# 
# **names have '_' or '-' instead of space between them**

# **Define**
# 
# Capitalize the words and replace '-','_' with blank space in p1,p2,p3

# **Code**
# 

# In[226]:


# Replace '_' and '-' with blank space and capitalise the words in p1
p1_clean=[]
for name in image_df_clean.p1:
    if '_' in name:
        s=name.split('_')
        var=" ".join(s)
    elif '-' in name:
        s=name.split('-')
        var=" ".join(s)
    else:
        var=name
    p1_clean.append(var.title())
image_df_clean.p1=p1_clean


# In[227]:


# Replace '_' and '-' with blank space and capitalise the words in p2
p2_clean=[]
for name in image_df_clean.p2:
    if '_' in name:
        s=name.split('_')
        var=" ".join(s)
    elif '-' in name:
        s=name.split('-')
        var=" ".join(s)
    else:
        var=name
    p2_clean.append(var.title())
image_df_clean.p2=p2_clean


# In[228]:


# Replace '_' and '-' with blank space and capitalise the words in p3
p3_clean=[]
for name in image_df_clean.p3:
    if '_' in name:
        s=name.split('_')
        var=" ".join(s)
    elif '-' in name:
        s=name.split('-')
        var=" ".join(s)
    else:
        var=name
    p3_clean.append(var.title())
image_df_clean.p3=p3_clean


# **Test**

# In[229]:


image_df_clean.head()


# **Define**
# 
# Extract the 'pupper','doggo','puppo','floofer' keywords from the text to form a single column 'dog_stage' and drop the remaining columns.

# **Code**

# In[230]:


#Extract the dog stage keywords from the text column
twitter_archive_clean['dog_stage'] = twitter_archive_clean['text'].str.extract('(doggo|floofer|pupper|puppo)',expand=False)


# In[231]:


#Drop the previous columns
twitter_archive_clean=twitter_archive_clean.drop(['pupper','doggo','puppo','floofer'],axis=1)


# **Test**

# In[232]:


twitter_archive_clean.head()


# In[233]:


twitter_archive_clean.shape


# **Tidiness Issue-2**
# 
# **All 3 tables should be merged together**

# **Define**
# 
# Merge the `twitter_archive and json_tweet tables and 'image_predictions table`

# **Code**

# In[234]:


#Merge twitter_archive and json_tweet tables
twitter_archive_clean=twitter_archive_clean.join(twitter_api_clean.set_index('tweet_id'), on='tweet_id')


# In[235]:


#Merge twitter_archive and imgae_predictions tables
twitter_archive_clean=twitter_archive_clean.join(image_df_clean.set_index('tweet_id'), on='tweet_id')


# **Test**

# In[236]:


twitter_archive_clean.head()


# In[237]:


twitter_archive_clean.info()


# ### Quality

# **Quality Issue-3**
# 
# **twitter_archive table**
# 
# **rating_denominator in twitter_archive table has values more than 10. It should be 10 only.**

# **Define**
# 
# Assign all values of rating_denominator in twitter_archive to be 10.

# **Code**

# In[238]:


# Assign all values of rating_denominator to be 10
twitter_archive_clean['rating_denominator']=10


# **Test**

# In[239]:


twitter_archive_clean['rating_denominator'].value_counts()


# **Quality Issue-4**
# 
# **twitter_archive table**
# 
# **name column has names such as 'a' ,'the' ,'an','such' etc**
# 
# **name column has 'O' instead of O'Malley**

# **Define**
# 
# Change the names such as 'a','an','the' to NaN
# 
# Change O to O'Malley in name column
# 
# All the incorrect names are in lowercase

# **Code**

# In[240]:


#Create list of all lowercase names
lower_name_list=[]
for name in twitter_archive_clean.name:
    if name is not None:
        if name.islower() and name not in lower_name_list:
            lower_name_list.append(name)
lower_name_list


# In[241]:


# Replace thses names by NaN
twitter_archive_clean.replace(lower_name_list,np.NaN,inplace=True)


# In[242]:


# Replace O with O'Malley
twitter_archive_clean.replace('O',"O'Malley",inplace=True)


# **Test**

# In[243]:


# Check for any lowercase names
twitter_archive_clean.name.value_counts()


# In[244]:


# Check whether name O'Malley is correctly reflected
twitter_archive_clean[twitter_archive_clean['name']=="O'Malley"]['name']


# **Quality Issue-5**
# 
# **twitter_archive table**
# 
# **Erroneous datatpes (timestamp, retweeted_status_timestamp)**

# **Define**
# 
# Convert timestamp and retweeted_status_timestamp from string to Datetime datatype

# **Code**

# In[245]:


# Convert above columns to Datetime
twitter_archive_clean.timestamp = pd.to_datetime(twitter_archive_clean.timestamp)
twitter_archive_clean.retweeted_status_timestamp = pd.to_datetime(twitter_archive_clean.retweeted_status_timestamp)


# **Test**

# In[246]:


twitter_archive_clean.info()


# **Quality Issue-6**
# 
# **twitter_archive table**
# 
# **decimal values such as 13.5 extracted as 5**

# **Define**
# 
# Extract the decimal ratings correctly.

# **Code**

# In[247]:


# Obtain all text, indices, and ratings for tweets that contain a decimal in the numerator of rating
decimals_text = []
decimals_index = []
decimals = []

for i, text in twitter_archive_clean['text'].iteritems():
    if bool(re.search('\d+\.\d+\/\d+', text)):
        decimals_text.append(text)
        decimals_index.append(i)
        decimals.append(re.search('\d+\.\d+', text).group())

# Print the text to confirm presence of ratings with decimals        
decimals_text


# In[248]:


# Print the index of text with decimal ratings
decimals_index


# In[249]:


# Change contents of 'rating_numerator' 
twitter_archive_clean.loc[decimals_index[0],'rating_numerator'] = float(decimals[0])
twitter_archive_clean.loc[decimals_index[1],'rating_numerator'] = float(decimals[1])
twitter_archive_clean.loc[decimals_index[2],'rating_numerator'] = float(decimals[2])
twitter_archive_clean.loc[decimals_index[3],'rating_numerator'] = float(decimals[3])
twitter_archive_clean.loc[decimals_index[4],'rating_numerator'] = float(decimals[4])


# **Test**

# In[250]:


# Check contents of row with index 40 to ensure the rating is corrected
twitter_archive_clean.loc[45]


# In[251]:


# Check contents of row with index 40 to ensure the rating is corrected
twitter_archive_clean.loc[340]


# **Quality Issue-7**
# 
# **twitter_archive table**
# 
# **None in columns instead of NaN**

# **Define**
# 
# Replace None with NaN in all the columns to maintian uniformity

# **Code**

# In[252]:


# Replace None with NaN in all columns
twitter_archive_clean.replace('None',np.NaN,inplace=True)


# **Test**

# In[253]:


twitter_archive_clean.sample(5)


# **Quality Issue-8**
# 
# **twitter_archive table**
# 
# **Ambiguous columns names such as p1,conf_p1,p1_dog**

# **Define**
# 
# Change ambiguous column names to meaning full names

# **Code**

# In[254]:


#Rename column nanmes
twitter_archive_clean.rename(columns={'p1':'prediction1(p1)',
                        'conf_p1':'confidence_p1',
                        'p1_dog':'is_p1_dog',
                        'p2':'prediction2(p2)',
                        'conf_p2':'confidence_p2',
                        'p2_dog':'is_p2_dog',
                        'p3':'prediction3(p3)',
                        'conf_p3':'confidence_p3',
                        'p3_dog':'is_p3_dog'},inplace=True)


# **Test**

# In[255]:


# List column names
twitter_archive_clean.columns


# **Quality Issue-9**
# 
# **twitter_archive table**
# 
# retweeted_status is not NaN
# 
# **Define**
# 
# Drop rows where retweeted_status is not NaN
# 

# **Code**

# In[256]:


# Drop rows where retweet status is not null
twitter_archive_clean = twitter_archive_clean[np.isnan(twitter_archive_clean.retweeted_status_id)]


# In[257]:


# Drop null columns
twitter_archive_clean = twitter_archive_clean.drop(['retweeted_status_id', 
                        'retweeted_status_user_id', 
                        'retweeted_status_timestamp'], 
                       axis=1)


# **Test**

# In[258]:


twitter_archive_clean.info()


# ## Storing

# In[259]:


# Store twitter_archive table to a csv file
twitter_archive_clean.to_csv('twitter_archive_master.csv',index=False)


# ## Visualisation
# 

# In[260]:


# Read twitter table from csv file
twitter_df=pd.read_csv('twitter_archive_master.csv')
twitter_df.head()


# **Visulaisation -1**
# 
# Plot of how retweets and favourites_count differs on a particular day of the week.

# In[261]:


# Get the number of retweets for each day of the week
retweet=twitter_df.groupby('day_of_the_week')['retweet_count'].sum()
retweet


# In[262]:


# Store the no. of retweets in a seperate list
retweet_count=[retweet[1],retweet[5],retweet[6],retweet[4],retweet[0],retweet[2],retweet[3]]
retweet_count


# In[263]:


# Define lables
label=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
label


# In[264]:


# Plot graph with apt lables
plt.figure(figsize=(15,8))
index = np.arange(len(label))
plt.bar(index, retweet_count,color='yellow',alpha=0.5);
plt.xlabel('Day of the Week', fontsize=14)
plt.ylabel('No. of retweets(in lakhs)', fontsize=14)
plt.xticks(index, label)
plt.title('Day V/S Retweet Count',fontsize=14)
plt.show()


# In[265]:


# Get the number of favourites count for each day of the week
fav=twitter_df.groupby('day_of_the_week')['favourites_count'].sum()
fav


# In[266]:


# Store the no. of favourites count in a seperate list
fav_count=[fav[1],fav[5],fav[6],fav[4],fav[0],fav[2],fav[3]]
fav_count


# In[267]:


# Plot graph with apt lables
plt.figure(figsize=(15,8))
index = np.arange(len(label))
plt.bar(index, fav_count,color='blue',alpha=0.3);
plt.xlabel('Day of the Week', fontsize=14)
plt.ylabel('No. of favourites count(in lakhs)', fontsize=14)
plt.xticks(index, label)
plt.title('Day V/S Favourites Count',fontsize=14)
plt.show()


# **Observation**
# 
# As we can see from the two graphs that maximum number of retweets happen on Wednesday. Since the count is in lakhs(millions) the difference is quite significant.
# 
# Similarly the maximum number of favourites takes place on Monday. Here also the difference in count is quite significant

# **Visualisation-2**
# 
# Plot of how retweets and favourites count differ with month.

# In[268]:


# Get the number of favourites count for each month of the year
fav=twitter_df.groupby('month')['favourites_count'].sum()
fav


# In[269]:


# Store the no. of favourites count in a seperate list
fav_count=[fav[4],fav[3],fav[7],fav[0],fav[8],fav[5],fav[6],fav[1],fav[-1],fav[-2],fav[-3],fav[2]]
fav_count


# In[270]:


#Create Labels
label=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
label


# In[271]:


# Plot graph with apt lables
plt.figure(figsize=(15,8))
index = np.arange(len(label))
plt.bar(index, fav_count,color='green',alpha=0.3);
plt.xlabel('Month', fontsize=14)
plt.ylabel('No. of favourites count(in lakhs)', fontsize=14)
plt.xticks(index, label)
plt.title('Month V/S Favourites Count',fontsize=14)
plt.show()


# In[272]:


# Get the number of retweets for each month
retweet=twitter_df.groupby('month')['retweet_count'].sum()
retweet


# In[273]:


# Store the no. of retweet count in a seperate list
retweet_count=[retweet[4],retweet[3],retweet[7],retweet[0],retweet[8],retweet[5],retweet[6],
               retweet[1],retweet[-1],retweet[-2],retweet[-3],retweet[2]]
retweet_count


# In[274]:


# Plot graph with apt lables
plt.figure(figsize=(15,8))
index = np.arange(len(label))
plt.bar(index, retweet_count,color='red',alpha=0.5);
plt.xlabel('Month', fontsize=14)
plt.ylabel('No. of retweets(in lakhs)', fontsize=14)
plt.xticks(index, label)
plt.title('Month V/S Retweet Count',fontsize=14)
plt.show()


# **Observation**
# 
# As we can see from the two graphs that the activity on twitter or in this case for the account @WeRateDogs is more during the month of January, December, June and July compared to months of March, April, August and September. This may be because they are the holiday months and people have more time to dedicate to social media. It is highest in January and December because most parts of the world experience winter season during that time and people tend to stay indoors during time compared to June and July.

# **Visualisation-3**
# 
# Plot to see the relationship between retweet count ad favourites count

# In[275]:


plt.figure(figsize=(15,8))
plt.scatter(y=twitter_df['favourites_count'], x=twitter_df['retweet_count']);
plt.xlabel('Retweet Count',fontsize=14)
plt.ylabel('Favourites Count',fontsize=14)
plt.title('Retweet Count V/S Favourites Count',fontsize=14)
plt.show()


# In[276]:


import seaborn as sns


# In[277]:


# Plot scatterplot of retweet vs favorite count
sns.lmplot(x="retweet_count", 
           y="favourites_count", 
           data=twitter_archive_clean,
           size = 5,
           aspect=1.3,
           scatter_kws={'alpha':1/5})
plt.title('Favorite vs. Retweet Count')
plt.xlabel('Retweet Count')
plt.ylabel('Favorite Count');


# **Observation**
# 
# Retweet count and favourites count are positively co-related.

# ## Conclusion
# Data wrangling is an important step in the Data Analysis process. Data warngling itself has three steps Gather, Assess and Clean. Gathereing relevant data is important otherwise our finds and observations will not come out correctly. Assessing the data for dirty or untidy data and then cleaning and documenting these process id helpful to get correct insights.
# 

# ## Limitations
# Real world data is messy and untidy. Gathering itself is a painful process. Assessing data was the toughest pat because there are so many discrepancies and one cannot address all of them. Cleaning the data was also difficult but with the help of stackoverflow and python documentations I was able to complete the project

# ## Achnowledgment
# -  https://stackoverflow.com
# -  https://pythonspot.com
# -  https://docs.python.org/3/

# In[ ]:




