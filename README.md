# Data-Wrangling-
## In this project, I performed the below wrangling processes to make the data clean and ready for analysis.

- Data Gathering
- Data Assement
- Data Cleaning

### Data Gathering: I will describe my approach to collecting data and explain the methods that I utilized in this process.
- The pandas library was utilized to import the provided Excel/CSV file from Udacity, and a data frame named 'tweet_archive' was created to store the imported data.
- I utilized the request library to retrieve the text document containing image predictions from the internet. Subsequently, I successfully collected the information from the web and saved it as a CSV file in a data frame.
- Since I was not able to get data using Twitter API, I used another source of information provided by Udacity and saved it in a text file. Then, I created a table called "df1" and put the information from the text file into it.

### Data Assessment
In this section, I examined the data to ensure that it met the criteria of quality and tidiness. To assess the quality of the data, I checked for any inaccuracies, inconsistencies, and missing values that could affect the overall reliability of the dataset. Additionally, I assessed the tidiness of the data to ensure that it was well-structured and organized, with each variable forming a column, each observation forming a row, and each type of observational unit forming a separate table.

A. tweet_archive Dataset 
 
i. Quality Issues 
*  Invalid Timestamp Data Type(String Not Datetime) 
*  In several columns null objects are represented as 'None' instead of NaN 
*  Dog Name column have invalid names i.e 'None', 'quite', 'such', 'the 'a', 'an' etc.  ➢   Some Columns are float instead of String 
 
ii.  Tidyness Issues 
* Dog stages were spread in different Columns 
* Dataset contained tweets instead of original tweets
