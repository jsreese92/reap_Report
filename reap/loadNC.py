#!/nas02/apps/python-2.6.5/bin/python

'''
Created on Aug 16, 2012

@author: jsreese
'''
import os, string, urllib;

#load the page
def getPage(lib, county, year):
    #a global variable to store the data retrieved from the webpage
    global fileData;
    fileData = [];
    
    #replace a space with a URL-encoded space so that the url opens properly
    #county = county.replace(" ", "%20");
    county= 'North%20Carolina';
     
    #a global variable to store the url for the webpage
    global source;
    #source = 'http://saswebtest.unc.edu/cgi-bin/broker?_service=default&_program='+lib+'.tbExpAllForPDF.sas&county='+county+'&label=County&format=html&entry=1&by=';
    #source = 'http://saswebtest.unc.edu/cgi-bin/broker?_service=default&_program='+lib+'.tbExpAllForPDF.sas&county='+county+'&label=County&format=html&entry=1&by=';
    #source = 'http://saswebtest.unc.edu/cgi-bin/broker?_service=default&_program='+lib+'.tbReap.sas&county='+county+'&label=&format=html&entry=2&year='+year;
    #source = 'http://sasweb.unc.edu/cgi-bin/broker?_service=default&_program='+lib+'.net.sas&county='+county+'&label=&format=html';
    
    source = 'http://sasweb.unc.edu/cgi-bin/broker?_service=default&_program='+lib+'.tbReapMonth.sas&county='+county+'&label=County&format=html&entry=2&year='+year;
    #open the url, and store the data in fileData
    print "source = " + source
    try:
        infile = urllib.urlopen(source);

        if infile.getcode() == 200:
            for line in infile.readlines():
                fileData.append(line);
            infile.close()
            return "OK";
        else:
            infile.close()
            return [str(infile.getcode())+" Error"];
    except IOError:
        return ["Error opening page."];

#return the table data from the page        
def getDataNC(tableNum):
    tableNum = tableNum ;  #because each table title is technically a table as well 
    
    data = [];
    row = [];
    tableCount = 0;

    for line in fileData:
        
        #figure out which table we are in
        if line.find("<table") >= 0: 
            tableCount = tableCount+1;

        #get column names
        if tableCount == tableNum and line.find("<th class") >= 0:
                dataStart = line.find(">") + 1;      #the index for the first character of the column header
                dataEnd = line.find("</th", 1) - 1;  #the index for the last character of the column header
                
                colName = line[dataStart:dataEnd+1];
                colName = colName.replace("<br>", " ");

                row.append(colName);

        #get data
        if tableCount == tableNum and line.find("<td class") >= 0:
                dataStart = line.find(">") + 1;      #the index for the first character of the data
                dataEnd = line.find("</td", 1) - 1;  #the index for the last character of the data
                
                value = line[dataStart:dataEnd+1];

                row.append(value);

        #found the end of a row, append the data to the dataset
        if tableCount == tableNum and line.find("</tr>") >= 0:
                data.append(row);
                row = [];

    return data;

#return the URL
def getSource():
    return source;

#return the created/updated dates
def getPageDates():

    created = ""
    updated = ""
        
    for line in fileData:
        if line.find("This table created") >= 0:
            dataStart = line.find("This table created");
            dataEnd = line.find("</td") - 1;
  
            created = line[dataStart:dataEnd + 1];
  
        if line.find("Data last updated") >= 0:
            dataStart = line.find("Data last updated");
            dataEnd = line.find("</td") - 1
  
            updated = line[dataStart:dataEnd + 1];

    return [created, updated];


