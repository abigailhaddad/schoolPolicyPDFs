# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 15:57:45 2021
This pulls all the continuous education plans for charter schools and parses answers to COVID questions
but it doesn't 100% work - PyPDF2 doesn't work when there are weird font issues
@author: HaddadAE
"""

import os
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import PyPDF2 

os.chdir(os.getcwd().replace("code", "data"))

def pullReport(site):
    #saves all of the PDFs with "Health" in the link to the name of the PDF
   page = requests.get(site) 
   soup = BeautifulSoup(page.text, 'html.parser')
   links = []
   for link in soup.findAll('a'):
       links.append(link.get('href'))
   healthLinks=[i for i in links if "Health" in str(i)]
   for i in healthLinks:
       name=i.split("/")[-1]
       response = requests.get(i)
       with open(name, 'wb') as f:
           f.write(response.content)
           
def getText(file):
    pdfFileObject = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    pages= pdfReader.numPages
    string=""
    for num in range(0, pages):
        pageObject = pdfReader.getPage(num)
        string=string+pageObject.extractText()
    pdfFileObject.close()
    return(string)

def pullSection(string):
    try:
        firstString="plan to ensure that results of such testing programs"
        secondString="plans to support COVID-19 vaccination"
        return(string.split(firstString)[1].split(secondString)[0])
    except:
        pass
      
def main():
    site1="https://osse.dc.gov/page/2021-22-lea-continuous-education-plans"
    #site2="https://osse.dc.gov/page/health-and-safety-plans-private-parochial-and-independent-schools"
    pullReport(site1)
    #pullReport(site2)
    links=os.listdir()
    listOfTexts=[getText(file) for file in os.listdir()]
    df = pd.DataFrame(list(zip(links, listOfTexts)), columns =['Name', 'text'])
    return(df)

