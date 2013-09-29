#!/nas02/apps/python-2.6.5/bin/python

'''
Created on Aug 16, 2012

@author: jsreese
'''

import os, string, sys, string;

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import *
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize

import loadCounty;
import loadNC;

#Code to display page numbers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Times-Roman", 8)
        self.drawRightString(11.5*inch, .25*inch,
            "Page %d of %d" % (self._pageNumber, page_count))

        #In addition to the page number, display the url on each page                                                     
        #source = 'North Carolina Division of Social Services | Child Welfare Services \n Reaching for Excellence and Accountability in Practice-Training and Technical Assistance'
        #"Source: "+loadCounty.getSource();
        #self.drawCentredString(5.75*inch, .25*inch, source);

        #Also display the created/updated dates
        dates = loadCounty.getPageDates();
        self.drawString(.25*inch, .35*inch, dates[0]);
        self.drawString(.25*inch, .25*inch, dates[1]);

#Use the loadCounty module to get the data
def getDataCnty(tableNum):
    return loadCounty.getDataCnty(tableNum);

def getDataNC(tableNum):
    return loadNC.getDataNC(tableNum);

def formatPercentage(str):
    if len(str.strip()) <2:
        return str;
    else:
        return (string.atof(str)*100).__str__() + '%';

def isInteger(number):
    if cmp(number,'N/A')==0:
        return False;
    pointPosition = number.find('.');
    if pointPosition <= 0:
        return False;
    flag = 1;
    number = number[pointPosition+1:len(number)];
    for i in number:
        if cmp(i,'0') != 0:
            flag = 0;
    if flag == 1:
        return True;
    else:
        return False;


#Set formatting options for the monthy data table

#pretty sure this is unused...
def setStyle1():
    return [('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
          ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
          ('BOX', (0, 0), (0, -1), 1.5, colors.black),
          ('BOX', (0, 0), (-1, 0), 1.5, colors.black),
          ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
          ('FONTSIZE', (0, 0), (-1, -1), 6.5),
          ('LINEBELOW',(0, 3), (-1, 3), 1.3, colors.black),
          ('LINEBELOW',(0, 6), (-1, 6), 1.3, colors.black),
          ('LINEBELOW',(0, 9), (-1, 9), 1.3, colors.black),
          ('LINEBELOW',(0, 12), (-1, 12), 1.3, colors.black),
          ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
          ('GRID', (0, 0), (-1, -1), 1, colors.black),
          ('SPAN', (1, 0), (5, 0)),
          ('SPAN', (6, 0), (10, 0)),
          ('SPAN', (0, 0), (0, 1)),
          ('SPAN', (11, 0), (-1, -1))
         ]


#Set formatting options for the monthy data table
def setStyle():
    return [('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0,0), (0,23), 'LEFT'),
          ('ALIGN',(1,0), (3,34), 'CENTER'),
          ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
          ('BOX', (0, 0), (0, -1), 1.5, colors.black),
          ('BOX', (0, 0), (-1, 0), 1.5, colors.black),
          ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
          ('FONT', (3, 3), (3, 34), 'Times-Bold'),
          ('FONTSIZE', (0, 0), (-1, -1), 8),
          ('FONTSIZE', (0, 1), (0, 1), 9),
          ('FONT', (1, 5), (1, 5), 'Times-Bold'),
          ('FONT', (1, 15),(1, 15), 'Times-Bold'),
          ('FONTSIZE', (1, 21), (1, 21), 9), 
          ('LINEBELOW',(0, 9), (-1, 9), 1.3, colors.black),
          ('LINEBELOW',(0, 14), (-1, 14), 1.3, colors.black),
          ('LINEBELOW',(0, 20), (-1, 20), 1.3, colors.black),
          ('LINEBELOW',(0, 22), (-1, 22), 1.3, colors.black),
          ('LINEBELOW',(0, 24), (-1, 24), 1.3, colors.black),
          ('LINEBELOW',(0, 30), (-1, 30), 1.3, colors.black),
          ('LINEBELOW',(0, 34), (-1, 34), 1.3, colors.black),
          ('TEXTCOLOR',(0, 0), (-1, 0), colors.white),
          ('TEXTCOLOR',(0, 25), (-1, 25), colors.white),
          ('BACKGROUND', (0, 0), (-1, 0), colors.black),
          ('BACKGROUND', (0, 1), (-1, 1), colors.orange),
          ('BACKGROUND', (0, 6), (-1, 6), colors.orange),
          ('BACKGROUND', (0, 7), (-1, 7), colors.lightblue),
          ('BACKGROUND', (0, 10), (-1, 10), colors.lightblue),
          ('BACKGROUND', (0, 15), (-1, 15), colors.lightblue),
          ('BACKGROUND', (0, 21), (-1, 21), colors.lightblue),
          ('BACKGROUND', (0, 23), (-1, 23), colors.lightblue),
          ('BACKGROUND', (0, 25), (-1, 25), colors.black),
          ('BACKGROUND', (0, 26), (-1, 26), colors.lightblue),
          ('BACKGROUND', (0, 31), (-1, 31), colors.lightblue),
          ('BACKGROUND', (1, 4), (1, 5), colors.gray),
          ('BACKGROUND', (1, 8), (1, 9), colors.gray),
          ('BACKGROUND', (1, 12), (1, 14), colors.gray),
          ('BACKGROUND', (1, 20), (1, 20), colors.gray),
          ('BACKGROUND', (1, 28), (1, 30), colors.gray),
          ('BACKGROUND', (1, 32), (1, 34), colors.gray),
          ('GRID', (0, 0), (-1, -1), 1, colors.black)
         ]

nums = string.digits
def check(a):
    flag = 1;
    for i in a:
        if i not in nums:
            flag=0;
    if flag == 1:
            return True;
    else:
            return False;

def monthToQuarter(month):
  if month == "01" or month == "02" or month == "03":
    return 1
  elif month == "04" or month == "05" or month == "06":
    return 2
  elif month == "07" or month == "08" or month == "09":
    return 3
  elif month == "10" or month == "11" or month == "12":
    return 4
  else:
    return "error"

#takes a YYYYMM formatted string and returns quarters one year and one quarter back
def backwardsMonth(YYYYMM):
  theMonth = YYYYMM[4:]
  theYear = int(YYYYMM[:4])
  theQuarter = monthToQuarter(theMonth)
  if theQuarter == 1:
    fromQuarter == 4
    fromYear = theYear - 2
  else:
    fromQuarter = theQuarter -1
    fromYear = theYear - 1
  if fromQuarter == 1:
    toYear = fromYear
  else:
    toYear = fromYear+1

  if fromQuarter == 1:
    toQuarter = 4
  else:
    toQuarter = fromQuarter -1

  return str(fromYear) + ' Q' + str(fromQuarter) + ' - ' + str(toYear) + ' Q' + str(toQuarter)

#takes a YYYYQ and returns the string for the followng four quarters
def forwardQuarter_j(fromYYYYQ):
  fromYear = int(fromYYYYQ[:4])
  fromQuarter = int(fromYYYYQ[-1:])
  toYear = 0
  toQuarter = 0

  if fromQuarter == 1:
    toYear = fromYear
  else:
    toYear = fromYear+1

  if fromQuarter == 1:
    toQuarter = 4
  else: 
    toQuarter = fromQuarter - 1

  return str(fromYear) + ' Q' + str(fromQuarter) + ' - ' + str(toYear) + ' Q' + str(toQuarter)

#takes a YYYYQ and returns the string for the previous four quarters
def backwardQuarter(fromYYYYQ):
  fromYear = 0
  fromQuarter = 0
  toYear = 0
  toQuarter = 0

  originalYear = int(fromYYYYQ[:4])
  originalQuarter = int(fromYYYYQ[-1:])
  
  fromYear = originalYear - 1
  fromQuarter = originalQuarter
  if fromQuarter == 1:
    toQuarter = 4
    toYear = fromYear
  else:
    toQuarter = fromQuarter -1
    toYear = fromYear + 1

  return str(fromYear) + ' Q' + str(fromQuarter) + ' - ' + str(toYear) + ' Q' + str(toQuarter)

#Create the pdf
def constructPage(county, label, year, titleYear):

    #pretty sure this is unused...
    countyTitle = county+" "+label;

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
 
    # A basic document for us to write to 'reapRep.pdf'
    doc = SimpleDocTemplate('./reapRep.pdf')
    #doc.pagesize = landscape(A4)
    doc.pagesize = portrait(letter)
    #doc.pagesize = landscape(legal)
    
    
    #vv pretty sure this is unused
    table1Style = setStyle1();

    tableStyle = setStyle();

    

    #Our container for 'Flowable' objects
    elements = []
    
    ###########################################################table1####################################
    
    #table25data = getDataCnty(25);
    
    tableDataCnty = getDataCnty(1);
    tableDataNC = getDataNC(1);

    #Titles are rewritten by hand since they are an abbreviated version of the data contained in the html page
    
    titletext1 = "<font name = 'Times' size='15'><b>NORTH CAROLINA CHILD WELFARE ACHIEVEMENTS</b></font>"
    
    newYear = titleYear[:4]
    month = titleYear[4:]
    if month == "01":
      newMonth="January"
    elif month == "02":
      newMonth="February"
    elif month == "03":
      newMonth="March"
    elif month == "04":
      newMonth="April"
    elif month == "05":
      newMonth="May"
    elif month == "06":
      newMonth="June"
    elif month == "07":
      newMonth="July"
    elif month == "08":
      newMonth="August"
    elif month == "09":
      newMonth="September"
    elif month == "10":
      newMonth="October"
    elif month == "11":
      newMonth="November"
    elif month == "12":
      newMonth="December"
    else:
      newMonth="Not a Month"

    '''
    newYear= year[0:4]
    month=''
    quarter = year[4:5]
    if quarter == '1':
        month='January';
    elif quarter == '2':
        month='April';
    elif quarter == '3':
        month='July';
    else:
        month='October';
        '''
    


    titletext2 = county+" "+label+'  '+newMonth+" "+newYear
    elements.append(Paragraph(titletext1, styles["Title"]))
    elements.append(Paragraph(titletext2, styles["Title"]))
   #i=1;
    
    numRows = 35; #total number of rows in table
    
    #sets size of table, be sure to give row heights at :399
    a=[[0 for x in range(4)] for y in range(35)]
    for j in range(0,4):
        for k in range(0,numRows):
            a[k][j]="";
    
    # state fiscal year changes in July
    if int(month) < 07:
      SFYdate = int(newYear) - 1
    else:
      SFYdate = int(newYear)
    SFYdate = str(SFYdate)
        
    a[0][1]= 'FY'+ tableDataCnty[1][2]+ '\n Statewide \n Performance \n Standard'
#    a[0][2]= 'NC\'s \n Performance \n in FY'+ tableDataCnty[1][2]
    a[0][2]= 'NC\'s \n Most Recent \n Performance'
#    a[0][3]= county+'\n County\'s \n Performance \n SFY'+ tableDataCnty[1][2]
    a[0][3]= county+'\n County\'s \n Most Recent \n Performance'
    
    a[1][0]= 'Systemic Factors'
    
    a[2][0]= '1. Annual social worker departure rate (excluding retirements, deaths, and \n promotions)' +' [2011 CW Staffing Survey]'    
    a[2][1]= formatPercentage(tableDataNC[2][3])
    a[2][2]= formatPercentage(tableDataNC[1][3])    
    a[2][3]= formatPercentage(tableDataCnty[1][3])
    
    a[3][0]= '2. Child welfare staffing gap or surplus '+'[2011 CW Staffing Survey]'
    #a[3][1]= tableDataNC[2][4]    
    a[3][1]= ""
    a[3][2]= tableDataNC[1][4]
    a[3][3]= tableDataCnty[1][4]
    
    a[4][0]= '3. Increase in the annual percent of supervisors certified in child welfare supervision'

    a[5][0]= '4. Increase in the annual percent of managers certified in child welfare supervision'
    
    a[6][0]= 'Core Child Welfare Achievements'
    
    a[7][0]= 'Prevention'
    
    a[8][0]='5. Annual rate of reports of child maltreatment (per 1,000 children) [SFY ' + SFYdate + ']'
    #a[8][1]= tableDataNC[2][7]
    a[8][1]= ""
    a[8][2]= tableDataNC[1][7]
    a[8][3]= tableDataCnty[1][7]
    
    a[9][0]= '6. Annual rate of child victimization (per 1,000 children) [SFY ' + SFYdate + ']'
    #a[9][1]= tableDataNC[2][8]
    a[9][1]= ""
    a[9][2]= tableDataNC[1][8]
    a[9][3]= tableDataCnty[1][8]
    
    a[10][0]= 'Child Protective Services'
    
    a[11][0]= '7. Annual % of maltreated children who are not repeat victims of indicated maltreatment'+'['+backwardsMonth(year)+']'
    a[11][1]= formatPercentage(tableDataNC[2][9])
    a[11][2]= formatPercentage(tableDataNC[1][9])
    a[11][3]= formatPercentage(tableDataCnty[1][9])
    
    a[12][0]= '8. Annual % of CPS reports screened out '+'[2011 CW Staffing Survey]'
    #a[12][1]= formatPercentage(tableDataNC[2][10])
    a[12][1]= ""
    a[12][2]= formatPercentage(tableDataNC[1][10])
    a[12][3]= formatPercentage(tableDataCnty[1][10])
    
    a[13][0]= '9. Annual % of children who enter foster care who are nonwhite '+'[SFY ' + SFYdate + ']'
    #a[13][1]= formatPercentage(tableDataNC[2][11])
    a[13][1]= ""
    a[13][2]= formatPercentage(tableDataNC[1][11])
    a[13][3]= formatPercentage(tableDataCnty[1][11])
    
    a[14][0]= '10. Annual % of repeat maltreatment for children who receive in-home services'
    #a[14][1]= formatPercentage(tableDataNC[2][12])
    a[14][1]= ""
    #a[14][2]= formatPercentage(tableDataNC[1][12])
    a[14][2]= ""
    #a[14][3]= formatPercentage(tableDataCnty[1][12])
    a[14][3]=""
    
    a[15][0]= 'Foster Care'
    
    a[16][0]= '11. Annual % of children in foster care who have not been \n maltreated by a foster parent or facility staff member '+'['+backwardsMonth(year)+']'
    a[16][1]= formatPercentage(tableDataNC[2][13])
    a[16][2]= formatPercentage(tableDataNC[1][13])
    a[16][3]= formatPercentage(tableDataCnty[1][13])
    
    a[17][0]= '12. Annual % of foster youth in care for 12 months or less who have 2 or fewer placements '+'['+backwardsMonth(year)+']'
    a[17][1]= formatPercentage(tableDataNC[2][14])
    a[17][2]= formatPercentage(tableDataNC[1][14])
    a[17][3]= formatPercentage(tableDataCnty[1][14])
    
    a[18][0]= '13. Annual % of foster youth in care for 12 months but less than 24 months who have \n 2 or fewer placements '+'['+backwardsMonth(year)+']'
    a[18][1]= formatPercentage(tableDataNC[2][15] )
    a[18][2]= formatPercentage(tableDataNC[1][15] )
    a[18][3]= formatPercentage(tableDataCnty[1][15] )
    
    a[19][0]= '14. Annual % of foster youth in care for more than 24 months who have \n 2 or fewer placements '+'['+backwardsMonth(year)+']'
    a[19][1]= formatPercentage(tableDataNC[2][16])
    a[19][2]= formatPercentage(tableDataNC[1][16])
    a[19][3]= formatPercentage(tableDataCnty[1][16])
    
    a[20][0]= '15. Annual % of nonwhite children in foster care '+'['+backwardsMonth(year)+']'
    #a[20][1]= formatPercentage(tableDataNC[2][17])
    a[20][1]= ""
    a[20][2]= formatPercentage(tableDataNC[1][17])
    a[20][3]= formatPercentage(tableDataCnty[1][17])
    
    a[21][0]= 'Permanency'
    
    a[22][0]= '16. Annual % of children experiencing re-entries into foster care within \n 12 months of their discharge '+'['+backwardsMonth(year)+']'
    a[22][1]= formatPercentage(tableDataNC[2][18])
    a[22][2]= formatPercentage(tableDataNC[1][18])
    a[22][3]= formatPercentage(tableDataCnty[1][18])
    
    a[23][0]= 'Reunification'
    
    a[24][0]='17. Percentage of youth who achieve permanency through \n reunification within 12 months (assuming in care 8 days)'+'['+backwardsMonth(year)+']'
    a[24][1]= formatPercentage(tableDataNC[2][19])
    a[24][2]= formatPercentage(tableDataNC[1][19])
    a[24][3]= formatPercentage(tableDataCnty[1][19])
   
    a[25][0]= ''
    a[25][1]= 'FY'+ tableDataCnty[1][2]+ '\n Statewide \n Performance \n Standard'
    a[25][2]= 'NC\'s \n Most Recent \n Performance'
    a[25][3]= county+'\n County\'s \n Most Recent \n Performance'
    '''
    a[25][1]= 'FY'+ tableDataCnty[1][2]+ '\n Statewide \n Performance \n Standard'
    a[25][2]= 'NC\'s \n Performance \n in FY'+ tableDataCnty[1][2]
    a[25][3]= county+'\n County\'s \n Performance \n SFY'+ tableDataCnty[1][2]
    '''
    
    a[26][0]= 'Adoption'
    
    a[27][0]= '18. Annual percentage of children who left foster care through adoption in last \n 12 months who were adopted within 24 months of their last entry into foster care '+'['+backwardsMonth(year)+']'
    a[27][1]= formatPercentage(tableDataNC[2][20])
    a[27][2]= formatPercentage(tableDataNC[1][20])
    a[27][3]= formatPercentage(tableDataCnty[1][20])
    
    a[28][0]= '19. Annual percentage of nonwhite children free for adoption who are adopted \n within 1 year of TPR [TPR '+backwardsMonth(year)+']'
    #a[28][1]= formatPercentage(tableDataNC[2][21])
    a[28][1]= ""
    a[28][2]= formatPercentage(tableDataNC[1][21])
    a[28][3]= formatPercentage(tableDataCnty[1][21])
    
    a[29][0]= '20. Decrease in the annual percentage of adoptions that disrupt or dissolve'
    
    a[30][0]= '21. Increase in the annual percentage of TPRs that are finalized timely'
    
    a[31][0]= 'Transitions from Foster Care to Adulthood'

    # have to do this since the earnings updates funny
    theMonth = year[4:]
    theYear = year[:4]
    if theMonth == "01":
      newMonth = "12"
      newYear = int(theYear) - 1
      year22 = ""
      year22+=newYear
      year22 += newMonth
    else:
      year22 = int(year) - 1

    year22 = str(year22)


    
    a[32][0]= '22. Percentage of youth aging who have employment earnings in the first \n year after turning 18 [turned 18 '+backwardsMonth(year22)+']'
    #a[32][1]= formatPercentage(tableDataNC[2][24])
    a[32][1]= ""
    a[32][2]= formatPercentage(tableDataNC[1][24])
    a[32][3]= formatPercentage(tableDataCnty[1][24])
    
    a[33][0]= '23. Annual percentage of eligible youth 18-21 who sign a CARS agreement'
    
    a[34][0]= '24. Percentage of eligible youth who pursue post-secondary education with NC \n Reach and ETV'
    
    for i in range(0,4):
      for j in range(0,numRows):
        #takes away random whitespace before and after
        a[j][i] = a[j][i].strip()
        if a[j][i]=='.':
          a[j][i]='N/A'; 

        
    table1 = Table(a, colWidths=[403, 60, 60, 60], rowHeights=[55, 18, 28, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 28, 18, 28, 28, 18, 18, 28, 18, 28, 55, 18, 28, 28, 18, 18, 18, 28, 18, 28], style=tableStyle)
    elements.append(table1)
        
    elements.append(Spacer(1, 0.5*inch));
    
    note1 = "North Carolina Division of Social Services | Child Welfare Services";
    note2 = "<b>R</b>eaching for <b>E</b>xcellence and <b>A</b>ccountability in <b>P</b>ractice-Training and Technical Assistance";
    elements.append(Paragraph(note1, styles["Normal"]))
    elements.append(Spacer(1, .01*inch))
    elements.append(Paragraph(note2, styles["Normal"]))


    doc.build(elements, canvasmaker=NumberedCanvas);


