'''
Created on Nov 06, 2017
Scrapes through LinkedIn Profile's PDF and extracts data relative to each section.
All data is stored in a Panda DataFrame as generated below. 

@author: Sharan Jhangiani
@contact: sharan@uw.edu

If questions, email above.
'''

from bs4 import BeautifulSoup
import pandas as pd
import glob, os
import subprocess
from cStringIO import StringIO

globalExperienceCount = 0
globalEducationCount = 0


#set directory where PDFs are located
os.chdir("/Users/sharan/Google Drive/College/Extra Curriculars/PDFs Temp Storage")

#convert all PDFs to HTML files for more accurate analysis 
for file in glob.glob("*.pdf"):
    currFile = open(file, 'rv')
    name = currFile.name
    subprocess.call(['pdf2htmlEX', '--zoom', '1.3', name])

index = []

#count instances and analyze all the html files 
for file in glob.glob("*.html"):
        htmlFile = open(file, 'rv').read()
        soup = BeautifulSoup(htmlFile, "lxml")
        stringAll = str(soup)
        mutableString = stringAll

        #find the name
        nameStart = stringAll[stringAll.find("fs1 fc1 sc0 ls0 ws0") + 21 :]
        newName = nameStart[ : nameStart.find("<")]
        name = stringAll[stringAll.find("fs1 fc1 sc0 ls0 ws0") + 21 : stringAll[stringAll.find("fs1 fc1 sc0 ls0 ws0") + 21 :].find("<")]
        index.append(newName)

        indexOfSummaryHTML = stringAll.find("fs3 fc2 sc0 ls0 ws0") + 28
        indexOfExperienceHTML = indexOfSummaryHTML + stringAll[indexOfSummaryHTML + 50 :].find("ff1 fs3 fc2 sc0 ls0 ws0") + 25
        indexOfEducationHTML = indexOfExperienceHTML + stringAll[indexOfExperienceHTML + 70 :].find("ff1 fs3 fc2 sc0 ls0 ws0") + 25

        #experience section
        experienceString = stringAll[indexOfExperienceHTML : indexOfEducationHTML]

        #find the number of  experience columns needed
        experienceCountString = experienceString
        experienceCount = 0
        while "ff1 fs4 fc0 sc0 ls0 ws0" in experienceCountString:
                years = ["1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]
                for year in years:
                        if year and "ff1 fs4 fc0 sc0 ls0 ws0" in experienceCountString:
                                        experienceCount+= 1
                                        experienceCountString = experienceCountString[experienceCountString.find("ff1 fs4 fc0 sc0 ls0 ws0") + 60 :]
        if experienceCount > globalExperienceCount:
                globalExperienceCount = experienceCount

        #education section
        educationString =  stringAll[indexOfEducationHTML : ]

        #find the number of edcuation columns needed
        educationCountString = educationString
        educationCount = 0
        while "ff1 fs4 fc0 sc0 ls0 ws0" in educationCountString:
                years = ["1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]
                for year in years:
                        if year and "ff1 fs4 fc0 sc0 ls0 ws0" in educationCountString:
                                        educationCount+= 1
                                        educationCountString = educationCountString[educationCountString.find("ff1 fs4 fc0 sc0 ls0 ws0") + 60 :]
        
        if educationCount > globalEducationCount:
                globalEducationCount = educationCount


#set the columns in the pandas dataframe based on the number achieved above
column = ["Summary"]
indexExperience = 0
while indexExperience < globalExperienceCount:
        column.append("Experience Title " + str(indexExperience + 1))
        column.append("Experience Date " + str(indexExperience + 1))
        column.append("Experience Description " + str(indexExperience + 1))
        indexExperience += 1

indexEducation = 0
while indexEducation < globalEducationCount:
        column.append("Name of School " + str(indexEducation + 1))
        column.append("Education Date " + str(indexEducation + 1))
        column.append("Education Type " + str(indexEducation + 1))
        column.append("Education Description " + str(indexEducation + 1))
        indexEducation += 1

#create the pandas DataFrame
df = pd.DataFrame(index=index, columns=column)

#Analyze and extract the data from the html files
for file in glob.glob("*.html"):
        htmlFile = open(file, 'rv').read()
        soup = BeautifulSoup(htmlFile, "lxml")
        stringAll = str(soup)
        mutableString = stringAll

        #find the name to use as a index 
        nameStart = stringAll[stringAll.find("fs1 fc1 sc0 ls0 ws0") + 21 :]
        newName = nameStart[ : nameStart.find("<")]
        name = stringAll[stringAll.find("fs1 fc1 sc0 ls0 ws0") + 21 : stringAll[stringAll.find("fs1 fc1 sc0 ls0 ws0") + 21 :].find("<")]

        indexOfSummaryHTML = stringAll.find("fs3 fc2 sc0 ls0 ws0") + 25
        indexOfExperienceHTML = indexOfSummaryHTML + stringAll[indexOfSummaryHTML + 25 :].find("ff1 fs3 fc2 sc0 ls0 ws0") + 25
        indexOfEducationHTML = indexOfExperienceHTML + stringAll[indexOfExperienceHTML + 25 :].find("ff1 fs3 fc2 sc0 ls0 ws0") + 25

        #find and set the summary into the dataframe
        summary = ""
        stringSummary = mutableString[indexOfSummaryHTML : indexOfExperienceHTML]
        while "ff1 fs4 fc0 sc0 ls0 ws0" in stringSummary:
               indexOfSummaryStart = stringSummary.find("ff1 fs4 fc0 sc0 ls0 ws0") + 25
               stringSummary = stringSummary[indexOfSummaryStart :]
               indexOfSummaryEnd = stringSummary.find("<")
               summary += " " + stringSummary[ : indexOfSummaryEnd]
        
        df.set_value(newName, "Summary", summary)

        #find and set experience title
        experienceTitle = ""
        stringExperienceTitle = mutableString[indexOfExperienceHTML : indexOfEducationHTML]
        indexExperienceTitle = 0
        while indexExperienceTitle < globalExperienceCount:
                if "ff2 fs4 fc0 sc0 ls0 ws0" in stringExperienceTitle: 
                        indexOfExperienceTitleStart = stringExperienceTitle.find("ff2 fs4 fc0 sc0 ls0 ws0") + 25
                        stringExperienceTitle = stringExperienceTitle[indexOfExperienceTitleStart :]
                        indexOfExperienceEndTitle = stringExperienceTitle.find("<")
                        experienceTitle = " " + stringExperienceTitle[ : indexOfExperienceEndTitle]
                        df.set_value(newName, "Experience Title " + str(indexExperienceTitle + 1), experienceTitle)
                indexExperienceTitle += 1
        
        #find and set experience date and Summary
        experienceDate = ""
        stringExperienceDate = mutableString[indexOfExperienceHTML : indexOfEducationHTML]
        indexExperienceDate = 0
        while indexExperienceDate < globalExperienceCount:
                if "ff2 fs4 fc0 sc0 ls0 ws0" in stringExperienceDate: 
                        indexOfExperienceDateStart = stringExperienceDate.find("ff1 fs4 fc0 sc0 ls0 ws0") + 25
                        stringExperienceDate = stringExperienceDate[indexOfExperienceDateStart :]
                        indexOfExperienceEndDate = stringExperienceDate.find("<")
                        experienceDate = stringExperienceDate[ : indexOfExperienceEndDate]
                        df.set_value(newName, "Experience Date " + str(indexExperienceDate + 1), experienceDate)
                        description = ""
                        stringExperienceSummary = stringExperienceDate[indexOfExperienceEndDate : stringExperienceDate.find("ff2 fs4 fc0 sc0 ls0 ws0")]
                        if "ff1 fs4 fc3 sc0 ls0 ws0" in stringExperienceSummary:
                                indexOfExperienceDescriptionStart = stringExperienceSummary.find("ff1 fs4 fc3 sc0 ls0 ws0") + 25
                                stringExperienceSummary = stringExperienceSummary[indexOfExperienceDescriptionStart :]
                                indexOfExperienceDescriptionEnd = stringExperienceSummary.find("<")
                                description += stringExperienceSummary[ : indexOfExperienceDescriptionEnd]
                                df.set_value(newName, "Experience Description " + str(indexExperienceDate + 1), description)
                indexExperienceDate += 1

        #find and set education name and Activities and Society 
        educationTitle = ""
        stringEducationTitle = mutableString[indexOfEducationHTML : ]
        indexEducationTitle = 0
        while indexEducationTitle < globalEducationCount:
                if "ff2 fs4 fc0 sc0 ls0 ws0" in stringEducationTitle: 
                        indexOfEducationTitleStart = stringEducationTitle.find("ff2 fs4 fc0 sc0 ls0 ws0") + 25
                        stringEducationTitle = stringEducationTitle[indexOfEducationTitleStart :]
                        indexOfEducationTitleEnd = stringEducationTitle.find("<")
                        educationTitle = stringEducationTitle[ : indexOfEducationTitleEnd]
                        if educationTitle == "Activities and Societies: ":
                                educationDescriptionStart = indexOfEducationTitleEnd + 18
                                stringEducationTitle = stringEducationTitle[educationDescriptionStart :]
                                educationDescriptionEnd = stringEducationTitle.find("<")
                                educationDescription = stringEducationTitle[: educationDescriptionEnd]
                                df.set_value(newName, "Education Description " + str(indexEducationTitle), educationDescription)
                        else: 
                                df.set_value(newName, "Name of School " + str(indexEducationTitle + 1), educationTitle)
                                indexEducationTitle += 1 
                else:
                        indexEducationTitle += 1
        educationDescription = ""
        while "ff2 fs4 fc0 sc0 ls0 ws0" in stringEducationTitle: 
                        indexOfEducationTitleStart = stringEducationTitle.find("ff2 fs4 fc0 sc0 ls0 ws0") + 25
                        stringEducationTitle = stringEducationTitle[indexOfEducationTitleStart :]
                        indexOfEducationTitleEnd = stringEducationTitle.find("<")
                        educationTitle = stringEducationTitle[ : indexOfEducationTitleEnd]
                        if educationTitle == "Activities and Societies: ":
                                educationDescriptionStart = indexOfEducationTitleEnd + 18
                                stringEducationTitle = stringEducationTitle[educationDescriptionStart :]
                                educationDescriptionEnd = stringEducationTitle.find("<")
                                educationDescription += stringEducationTitle[: educationDescriptionEnd]
                                df.set_value(newName, "Education Description " + str(indexEducationTitle), educationDescription)

        #find and set education date
        educationDate = ""
        stringEducationDate = mutableString[indexOfEducationHTML :]
        indexEducationDate = 0
        while indexEducationDate < globalEducationCount:
                if "ff1 fs4 fc0 sc0 ls0 ws0" in stringEducationDate: 
                        indexOfEducationDateStart = stringEducationDate.find("ff1 fs4 fc0 sc0 ls0 ws0") + 25
                        stringEducationDate = stringEducationDate[indexOfEducationDateStart :]
                        indexOfEducationEndDate = stringEducationDate.find("<")
                        educationDateWithType = stringEducationDate[ : indexOfEducationEndDate]
                        educationReverse = educationDateWithType[::-1]
                        educationDate = educationReverse[: educationReverse.find(",")][::-1]
                        educationType = educationDateWithType[ : educationDateWithType.find(educationDate)]
                        if "-" in educationDate:
                                df.set_value(newName, "Education Date " + str(indexEducationDate + 1), educationDate)
                        df.set_value(newName, "Education Type " + str(indexEducationDate + 1), educationType)
                indexEducationDate += 1
print df
print "DataFrame generated. SUCCESS."