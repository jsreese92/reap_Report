#!/nas02/apps/python-2.6.5/bin/python

'''
Created on Aug 16, 2012

@author: jsreese
'''
import cgi;
import sys;
import cgitb; cgitb.enable()

import os.path

import loadCounty, genReap, loadNC;

#Displays an error page as html
def printError(message):
    print "Content-Type: text/html"
    print 
    print "<HR><H1>Error generating PDF.</H1>";
    print message
    print "<HR>";
    print "Please send email to dfduncan@email.unc.edu if you need help resolving this error.";

#Ensures county parameter is valid
def checkCounty(county):
    infile = open("./counties.txt", 'r');

    counties = [];

    for line in infile.readlines():
        counties.append(line.strip());

    infile.close();

    if county in counties:
        return "OK";
    else:
        return "ERROR";

#Ensures label parameter is valid
def checkLabel(label):
    if label in ["", "County", "Counties"]:
        return "OK";
    else:
        return "ERROR";

#parses YYYYMM from URL to YYYYQ to query reap dataset
def convertYear(theYear):
  originalYear = theYear[:-2]
  originalMonth = theYear[4:]

  originalQuarter = 0
  if (originalMonth == "01") or (originalMonth == "02") or \
  (originalMonth == "03"):
    originalQuarter = 1
  elif (originalMonth == "04") or (originalMonth == "05") or \
  (originalMonth == "06"):
    originalQuarter = 2
  elif (originalMonth == "07") or (originalMonth == "08") or \
  (originalMonth == "09"):
    originalQuarter = 3
  elif (originalMonth == "10") or (originalMonth == "11") or \
  (originalMonth == "12"):
    originalQuarter = 4

  carry = 0
  newQuarter = 0
  newYear = 0

  if originalQuarter == 1:
    newQuarter = 4
    carry = 1
  else:
    newQuarter = originalQuarter -1

  newYear = int(originalYear) - 1 - carry
  l = []
  l.append(str(newYear))
  l.append(str(newQuarter))

  year = "".join(l)
  return year

#If there are no errors, constructs and displays the pdf page        
def main():
    form = cgi.FieldStorage();
    county = form.getvalue("county", "");
    label = form.getvalue("label", "");
    lib = form.getvalue("lib", "");
    #titleYear = form.getvalue("year","");
    #year = convertYear(titleYear)
    year = form.getvalue("year","")
    titleYear = year

    if checkCounty(county) != "OK":
        printError(county+" county not found.");
    elif checkLabel(label) != "OK":
        printError(label+" label not found.");
    else:
        loadPageResult = loadCounty.getPage(lib, county, year);
        loadPageResult2 = loadNC.getPage(lib, county, year);
        if loadPageResult != "OK":
            printError(loadPageResult);
        elif loadPageResult2 != "OK":
            printError(loadPageResult2);
        else:
            genReap.constructPage(county, label, year, titleYear);
            print "Content-Type: application/pdf"
            print
            print open("./reapRep.pdf").read(), 

main();
