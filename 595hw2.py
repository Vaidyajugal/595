# Importing the required packages

from bs4 import BeautifulSoup
import requests
import openpyxl
import pandas as pd
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Creatinig a workbook for appending the data

file= openpyxl.Workbook()
sheet= file.active
sheet.title="Fake Companies"
sheet.append(["Name","Purpose"])

# Running a loop times for scraping the data for 50 companies

for i in range(0, 50):

    # Request is done inside the loop to get different company each time
    source = requests.get("http://3.85.131.173:8000/random_company")

    # Parsing HTML with BeautifulSoup
    soup = BeautifulSoup(source.text, 'html.parser')
    fake_company = soup.find('ol').find_all('li')

    # Getting the Name and Purpose of each company
    for i in fake_company:
        for j in i:
            if "Name" in j:
                Name = i.text.split(":")[1].strip(" ")
            if "Purpose" in j:
                Purpose = i.text.split(":")[1].strip(" ")

    sheet.append([Name, Purpose])

file.save("fake_co.csv")

# Changing the working directory to load the files of the team members
import os
os.getcwd()
os.chdir("C:/Users/jugal vaidya")

yash_file= pd.read_csv("Final_Excel.csv")
myfile= pd.read_csv("fake_co.csv")
Rishi_file= pd.read_csv("myfile.csv").rename(columns={"Company Name":"Name"})
Ameya_file= pd.read_csv("Assign1.txt",delimiter=";").rename(columns={"# Name":"Name"})

# Combining the data of all team members in a data frame.
alldata= [myfile,yash_file,Rishi_file,Ameya_file]
combined= pd.concat(alldata)
combined.index = range(200)

# Using the Sentiment Intensity Analyzer to get the polarity scores on the basis of "purpose" of companies.

analyzer= SentimentIntensityAnalyzer()

combined['compound'] = [analyzer.polarity_scores(x)['compound'] for x in combined['Purpose']]
combined['Negative'] = [analyzer.polarity_scores(x)['neg'] for x in combined['Purpose']]
combined['Neutral'] = [analyzer.polarity_scores(x)['neu'] for x in combined['Purpose']]
combined['Positive'] = [analyzer.polarity_scores(x)['pos'] for x in combined['Purpose']]

# Sorting the data on the basis of compound score
combined=combined.sort_values('compound',ascending=False)

print(combined)

# Top 5 companies with highest compound score
combined_head = combined.head(5)
print(combined_head)

# Viewing the entire sentence of the Purpose column.
for i in combined.head["Purpose"]:
    print(i)

# If we observe the purpose of these comapnies, there is a heavy usage of positive words or we can say that they are showing the optimism. The words such as Success, efficient, innovate, empower, non-volatile, fresh-thinking, optimized, loyalty, advanced, impactful, visionary, upward-trending are being used in these sentences. And there are very few or no negative words here, leading to overall high compound scores.

# Bottom 5 companies with lowest compouns score
combined_tail = combined.tail(5)
print(combined_tail)

# Viewing the entire sentence of the Purpose column.
for i in combined_tail["Purpose"]:
    print(i)

# There is no presence of strong postive words here. most of the words are neutral and the presence of the words "Killer", "Exploit", "Bleeding-edge" etc. might have caused occurance of negative impression overall, leading to negative or zero compound scores.