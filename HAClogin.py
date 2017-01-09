import requests
import datetime

#Gets HAC login information from user
user = input('HAC Username: ')
password = input('HAC Password: ')
makeGCalendar = 0
while(makeGCalendar != 1 and makeGCalendar != 2):
    makeGCalendar = int(input('Would you like to create a Google Calendar (1) or Export to a .txt file (2): '))
    if(makeGCalendar != 1 and makeGCalendar != 2):
        print('Please enter a number 1 or 2.')

#the webpages that the program uses
loginUrl = 'https://hac.friscoisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2fClasses'
gradesUrl = 'https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx'

#Class used to hold metadata of assignments
class Assignment():
    #date is the due date, title is the name of the assignment, cate is the category of the assignment (daily/minor/major)
    def __init__(self, date=None, title=None, cate=None, nameOfClass=None):
        if date is None:
            self.dueDate = datetime.datetime()
        else:
            self.dueDate = date
        if title is None:
            self.name = ''
        else:
            self.name = title
        if cate is None:
            self.category = ''
        else:
            self.category = cate
        if nameOfClass is None:
            self.className = ''
        else:
            self.className = nameOfClass

#Array to hold assignments
assignments = []

#parses a date from a string, returns 
def parseDate(dateStr):
    date = datetime.datetime.strptime(dateStr, '%m/%d/%Y')
    return date

#Accessing HAC
with requests.Session() as c:
    #logs into hac
#     response = c.get(loginUrl)
#     print(response.text)
    payload = {'LogOnDetails.UserName': user,
               'LogOnDetails.Password': password,
               'Database': '10'}
    c.post(loginUrl, data=payload, headers={"Referer": "http://google.com/"})
    #gets the page with assignments
    response = c.get(gradesUrl)
    if '<label class="sg-logon-left" for="LogOnDetails_Password">Password:</label>' in response.text:
        raise ValueError('An incorrect login was used.')
    #splits the data into the rows of the data tables
    tableRows = response.text.split('</tr><tr class="sg-asp-table-data-row">')
    for row in tableRows:
        #separates out dates
        possiableDate = row.split('</td>')[0].strip()
        possiableDate = possiableDate[4:]
        try:
            #get the date for the assignment
            dueDate = parseDate(possiableDate)
            #get the name for the assignment
            name = row[(row.index(';">')+3):row.index('</a>')].strip()
            #get the category of the assignment
            category = row.split('</td><td>')[3]
            #creates a new assignment with the data and saves it to the assignments array
            assignment = Assignment(dueDate, name, category, className)  # @UndefinedVariable
            assignments.append(assignment)
        except:
            try:
                #splits the row at headers for classes and obtains the last class in the row
                classLocations = row.split('<div class="AssignmentClass">')
                lastLocation = classLocations[len(classLocations)-1]
                #gets the class name
                possiableLines = lastLocation[:lastLocation.index('</a>')].split('\n')
                className = possiableLines[len(possiableLines)-2].strip()
                className = className[12:].strip()
            except:
                pass
        
        #print(row+'\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
for item in assignments:
    print(item.className+', '+str(item.dueDate)+', '+item.name+', '+item.category+'\n')
