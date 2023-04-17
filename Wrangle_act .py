#!/usr/bin/env python
# coding: utf-8

# Load Libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import requests
import os
import tweepy
import json
import time
from tweepy import OAuthHandler


# ## 1. Gathering Data

# ## A.Data From Tweeter Archive

# In[2]:


tweet_archive= pd.read_csv(r"C:\Users\BOUQSESH-PC\Downloads\twitter-archive-enhanced.csv")


#  ## B.Image Predictions

# In[3]:


url= "https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv"
response= requests.get(url)
with open('image-predictions.tsv', mode = 'wb') as file:
    file.write(response.content)
with open(url.split('/')[-1], mode = 'wb') as file:
    file.write(response.content)
    
#read the image into a dataframe called image
image= pd.read_csv('image-predictions.tsv', sep= '\t')    


# ## C.Tweeter Json

# In[4]:



#reading the Json.txt file line by line into Pandas DataFrame with tweet_id, retweet_count and favorite_count
df = []
with open(r"C:\Users\BOUQSESH-PC\Downloads\tweet-json.txt") as Json_file:
    for line in Json_file:
        tweet = (json.loads(line))
        tweet_id = tweet['id']
        retweet_count = tweet['retweet_count']
        favorite_count = tweet['favorite_count']
        create_date = tweet['created_at']
        df.append({'retweet_count' : retweet_count,
                  'favorite_count' : favorite_count,
                  'create_date' : create_date,
                  'tweet_id' : tweet_id})
        
#saving the tweet-json.txt file into a dataframe called twitter_extra
df1 = pd.DataFrame(df, columns = ['tweet_id', 'retweet_count', 'favorite_count', 'create_date'])


# In[5]:


# converting the txt file to a data list where each element contain list of element
df_list = []
with open(r"C:\Users\BOUQSESH-PC\Downloads\tweet-json.txt") as file:
    for line in file:
        df_list.append(json.loads(line))


# In[6]:


print(df_list[0])


# # 2. Assessing Data

# # A. Assessing The Twitter Archive Data

# In[6]:


# Visual Assessment of the Twitter Archive Data
tweet_archive


# In[7]:


# Visual Assessment of the Image Prediction Data
image


# In[8]:


# Visual Assessment of the Twitter API Dataset
df1


# ## Programmatic Inspection of the twitter archive

# In[9]:


# View the firstt 5 rows of the twitter archive data
tweet_archive.head()


# In[10]:


# check column data types of the twitter archieve dataset
tweet_archive.info()


# In[11]:


# summary Statistics of the tweeter archive dataset
tweet_archive.describe().T


# In[12]:


# check for duplicate data in the tweeter archive
sum(tweet_archive.duplicated())


# In[13]:


tweet_archive.rating_denominator.value_counts().sort_index()


# In[14]:


# checking for duplicated expanded urls
tweet_archive[tweet_archive.expanded_urls.duplicated()]


# In[15]:


# programatically assessing the name column for rows with name as 'a', 'quite', 'None' etc 
tweet_archive[tweet_archive['name'] == 'a']
tweet_archive[tweet_archive['name'] == 'quite']
tweet_archive[tweet_archive['name'] == 'None']


# In[16]:


#checking the numerator and denominator column values
tweet_archive['rating_numerator'].value_counts()
tweet_archive['rating_denominator'].value_counts()


# # Quality Issues Of the Twitter Archive
#  - Invalid Timestamp Data Type(String Not Datetime)
#  - In several columns null objects are represented as 'None' instead of NaN
#  - Dog Name column have invalid names i.e 'None', 'quite', 'such', 'the 'a', 'an' etc. 
#  - Some Columns are float instead of String
#  - Invalid tweet_id datatype
#  
#  

# ## Tidyness Issues

#  - The dog stage is one variable and hence should form single column. But this variable is spread across 4 columns - doggo, floofer, pupper, puppo.
#  -  Information about one type of observational unit (tweets) is spread across three different files/dataframes. 

# # B. Assessing The Image Prediction Dataset
# 

# In[17]:


image


# In[18]:


#Check For Data Type and Missing Values
image.info()


# In[19]:


#Summary statistics of the image prediction
image.describe()


# In[20]:


# check for duplicate of the image prediction
sum(image.duplicated())


# In[21]:


#assessing the img_num column
image.img_num.value_counts()


# In[22]:


#assessing sample rows of the img_num column
image.img_num.sample(5)


# In[23]:


sum(image.jpg_url.duplicated())


# In[24]:


#checking the image jpg_url column
image['jpg_url'].nunique()


# In[25]:


#checking to see the row data of a jpg_url that's duplicated
image[image['jpg_url'] == 'https://pbs.twimg.com/media/CZhn-QAWwAASQan.jpg']


# # Quality Issue of The Image Dataset
# - tweet_id are numerical and not string
# - pi, p2 and p3 contains underscore instead of spaces in the labels
# - Some tweet_id have the same jpg_url
# - Some P names start with small names
# 
# 

# # C. Assessing the Twitter Json

# In[26]:


df1.head()


# In[27]:


sum(df1.duplicated())


# In[28]:


df1.info()


# In[29]:


df1.describe()


# # Quality Issues with the Json Data
# - There are Missing ID's

# # 3. Data Cleaning

# In[30]:


# Make copies of original dataset
tweet_archive_clean = tweet_archive.copy()
image_clean = image.copy()
df1_clean = df1.copy()


# All the issues while asessing the dataset will be resolved

# # A. Tweet Archive

# ## Define
# 
#  Convert timestamp Datatype form object Datatype to Datetime using to_datetime

# ## Code

# In[31]:


tweet_archive_clean['timestamp']= pd.to_datetime(tweet_archive_clean['timestamp'])
tweet_archive_clean['retweeted_status_timestamp']= pd.to_datetime(tweet_archive_clean['retweeted_status_timestamp'])


# ## Test

# In[32]:


tweet_archive_clean.info()


# ## Define
# change values represented in twitter dataframe columns name, doggo, floofer, pupper, puppo as None to NaN

# ## Code

# In[34]:


tweet_archive_clean['name'].replace('None', np.NAN, inplace =True)
tweet_archive_clean['doggo'].replace('None', np.NAN, inplace =True)
tweet_archive_clean['floofer'].replace('None', np.NAN, inplace =True)
tweet_archive_clean['pupper'].replace('None', np.NAN, inplace =True)
tweet_archive_clean['puppo'].replace('None', np.NAN, inplace =True)


# ## Test

# In[35]:


tweet_archive_clean['name'].value_counts()
tweet_archive_clean['doggo'].value_counts()
tweet_archive_clean['floofer'].value_counts()
tweet_archive_clean['pupper'].value_counts()
tweet_archive_clean['puppo'].value_counts()


# In[36]:


tweet_archive_clean.name.value_counts()


# # Define
# Merge the 4 columns into a column called Dog_stage

# ## Code

# In[37]:


print(tweet_archive_clean.doggo.value_counts())
print(tweet_archive_clean.floofer.value_counts())
print(tweet_archive_clean.pupper.value_counts())
print(tweet_archive_clean.puppo.value_counts())


# In[38]:


tweet_archive_clean['dog_stage'] = tweet_archive_clean['text'].str.extract('(doggo|floofer|pupper|puppo)')


# ## Test

# In[71]:


pd.value_counts(tweet_archive_clean['dog_stage'])


# # Define

#  Change datatypes of these columns-(in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id and tweet_id) to string

# ## Code

# In[39]:


tweet_archive_clean['tweet_id'] = tweet_archive_clean['tweet_id'].astype(object)
tweet_archive_clean['in_reply_to_status_id'] = tweet_archive_clean['in_reply_to_status_id'].astype(object)
tweet_archive_clean['in_reply_to_user_id'] = tweet_archive_clean['in_reply_to_user_id'].astype(object)
tweet_archive_clean['retweeted_status_id'] = tweet_archive_clean['retweeted_status_id'].astype(object)
tweet_archive_clean['retweeted_status_user_id'] = tweet_archive_clean['retweeted_status_user_id'].astype(object)


# ## Test

# In[40]:


tweet_archive_clean.info()


# ## Define
#  Change names with words like 'a', 'an', 'such' to NAN values

# In[41]:


# creating an empty list to append the result to
tweet_archive_clean[tweet_archive_clean.name.str.islower()==True]['name'].unique()
    


# In[42]:


faulty_names = ['such', 'a', 'quite', 'not', 'one', 'incredibly', 'mad', 'an',
       'very', 'just', 'my', 'his', 'actually', 'getting', 'this',
       'unacceptable', 'all', 'old', 'infuriating', 'the', 'by',
       'officially', 'life', 'light', 'space']


# In[43]:


for i in faulty_names :
    tweet_archive_clean.name.replace(i,np.NAN, inplace= True)


# ## Test

# In[44]:


tweet_archive_clean.name.unique()


# In[45]:


#checking the new name column value
tweet_archive_clean['name'].value_counts()


# ## Define 
# 
# 

# Convert tweet id datatype From Int to String

# ## Code

# In[46]:


tweet_archive_clean.tweet_id = tweet_archive_clean.tweet_id.astype(str)


# ## Test

# In[47]:


tweet_archive_clean.head()


# ## Define

# Create the 'dog_stage' column by combining 'doggo' , 'floofer' , 'puppa' and 'puppo' 

# In[48]:


tweet_archive_clean['dog_stage'] = tweet_archive_clean['text'].str.extract('(doggo|floofer|pupper|puppo)')


# In[49]:


#drop the columns
tweet_archive_clean.drop(['doggo', 'floofer' , 'pupper' , 'puppo'], axis= 1 , inplace = True)


# ## Test

# In[50]:


pd.value_counts(tweet_archive_clean['dog_stage'])


# In[51]:


tweet_archive_clean.retweeted_status_id.isnull()
tweet_archive_clean.retweeted_status_user_id.isnull()
tweet_archive_clean.retweeted_status_timestamp.isnull()


# # B. Image Predictions

# # Define 
# 
# Convert tweet_id from numerical to string

# ## Code

# In[52]:


image_clean['tweet_id'] = image_clean['tweet_id'].astype(object)


# ## Test

# In[53]:


image_clean.info()


# # Define

# Capitalize p1,p2 and p3 columns

# ## Code

# In[54]:


image_clean.p1 = image.p1.str.title
image_clean.p2 = image.p2.str.title
image_clean.p3 = image.p3.str.title


# ## Test

# In[55]:


image_clean.head()


# # Define

# Replace - and _ with Whitespaces in p1, p2 and p3

# Code

# In[56]:



image_clean.p1 = image.p1.str.replace("-"," ")
image_clean.p2 = image.p2.str.replace("-"," ")
image_clean.p3 = image.p3.str.replace("-"," ")


image_clean.p1 = image.p1.str.replace("_"," ")
image_clean.p2 = image.p2.str.replace("_"," ")
image_clean.p3 = image.p3.str.replace("_"," ")



image_clean.p1 = image.p1.str.replace("-"," ")
image_clean.p2 = image.p2.str.replace("-"," ")
image_clean.p3 = image.p3.str.replace("-"," ")


# Test

# In[57]:


image_clean.head()


# # Define

# Drop Duplicated jpg_urls

# ## Code

# In[58]:


image_clean.drop_duplicates(subset='jpg_url', inplace = True)


# ## Test

# In[59]:


sum(image_clean.jpg_url.duplicated())


# ## Define

# Delete Rows with Missing rows

# In[60]:


image_clean = image_clean [image_clean.jpg_url.notnull()]


# ## Test

# In[61]:


image_clean.info()


# # C. Twitter  Json

# ## Drop create_date 

# ## Code

# In[62]:


df1_clean = df1_clean.drop('create_date', 1)


# ## Test 

# In[63]:


df1_clean.head()


# ## Define 

# Change tweet_Id for all 3 Dataframe to have consistency

# In[64]:


# Change format tweet_id for all dataframe
tweet_archive_clean ['tweet_id'] = tweet_archive_clean ['tweet_id'].astype('str')
image_clean ['tweet_id'] = image_clean ['tweet_id'].astype('str')
df1_clean ['tweet_id'] = df1_clean ['tweet_id'].astype('str')


# ## Test

# In[65]:


type(tweet_archive_clean ['tweet_id'].iloc[0]) 
type(image_clean ['tweet_id'].iloc[0])
type(df1_clean ['tweet_id'].iloc[0])


# # Define

# Merge the tweet_archive_clean, image_clean , df1_clean

# ## Code

# In[66]:


#merging all datasets into one
df_merge =pd.merge(tweet_archive_clean, image_clean, how= 'inner', on =['tweet_id']) 
df_merge = pd.merge(df_merge,df1_clean, how='inner', on= 'tweet_id')                                                 


# In[67]:


#create rating column
df_merge['rating'] = df_merge['rating_numerator'].astype(str) + '/'+ df_merge['rating_denominator'].astype(str) 


# In[68]:


#drop columns that are not necessary again
df_merge.drop(['rating_numerator', 'rating_denominator', 'expanded_urls'], axis =1, inplace= True)


# In[69]:


#dropping duplicates
df_merge= df_merge.drop_duplicates()


# ## Test

# In[70]:


#Check the merge data
df_merge.head()


# In[71]:


df_merge.info()


# In[72]:


# Drop Unnecessary columns
df_merge.drop(['retweeted_status_id', 'retweeted_status_user_id','retweeted_status_timestamp'], axis=1, inplace= True)


# In[73]:


df_merge.head()


# In[74]:


#dropping duplicates
df_merge= df_merge.drop_duplicates()


# In[87]:


df_merge.head()


# ## STORAGE DATA
#  Save gathered, assessed, and cleaned master dataset to a CSV file named "twitter_archive_master.csv".

# In[75]:


df_merge.to_csv("twitter_archive_master.csv", index= False, encoding='utf-8')


# ANALYSIS AND VISUALIZATION

# In[76]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# In[77]:


# loading the stored data
df_twitter = pd.read_csv(r"C:\Users\BOUQSESH-PC\twitter_archive_master.csv")


# In[78]:


# summary statistics
df_twitter.info()


# ## Insights and Visualisation

# - What is the Most common Dog Stage?
# - Which Dog has the highest retweet Count?
# - What is the Most Dog Name?
# - what is the correlation between retweet and favorite count?

# In[79]:


#the most common dog stage
df_twitter.dog_stage.value_counts()


# In[80]:


# Dog stage with the highest retweet count
df_twitter.groupby('dog_stage')['retweet_count'].mean().sort_values(ascending=False).astype(int)


# In[81]:


# Most common Dog Names
df_twitter.name.value_counts().nlargest(5)


# In[82]:


# Wordcloud for dog_name visualization:
text = df_twitter.loc[:, 'name'].str.cat(others=None, sep=' ')

# Instantiate word cloud object
wc = WordCloud(background_color='white', max_words=200,  stopwords=STOPWORDS,
              width=400, height=350,contour_width=0.1, 
                      contour_color='green')

# Generate word cloud
wc.generate(text)
# Show word cloud
plt.figure(figsize=(20,10))
plt.imshow(wc, interpolation='bilinear')
plt.title('Dog Name', fontsize=20)
plt.axis('off')
("")


# In[83]:


#plotting an horizontal bar chart to show top 5 dog names by favorite counts
top_name = df_twitter.groupby('name')['favorite_count'].sum().sort_values(ascending=True).nlargest(5)
plt.figure(figsize=(12,8))
plt.title("Top 5 dog names by favorite counts", size=20)
top_name.plot(kind='bar',fontsize=12,color='g')
plt.xlabel('favorite counts', fontsize=12)
plt.ylabel('Dog Name', fontsize=12);
sns.set_style("whitegrid");


# In[84]:


#plotting a bar chart to show top 5 dog Stage by favorite counts
top_stage = df_twitter.groupby('dog_stage')['favorite_count'].sum().sort_values(ascending=False)
plt.figure(figsize=(12,8))
plt.title("Top dog stages by favorite counts", size=20)
top_stage.plot(kind='bar',fontsize=12,color='g')
plt.xlabel('favorite counts', fontsize=12)
plt.ylabel('Dog stage', fontsize=12);
sns.set_style("whitegrid");


# In[86]:


sns.set(rc={'figure.figsize':(12,8)}, style="whitegrid")
sns.regplot(x='favorite_count', y='retweet_count', data=df_twitter)

plt.title("Favorite counts vs. Retweet counts",color="r", size=20)
plt.ylabel("Retweet Counts", size=12)
plt.xlabel("Favorite Counts", size=12);

data_corr = df_twitter.corr()

print("The Correlation Between favorite counts And retweet counts is ",data_corr.loc['favorite_count','retweet_count']);


# In[ ]:




