from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.fallenlondon.com/profile/Alfaksan')

time.sleep(3)
#Outbut dictionary:
output = {'Title':'','Date':'','Location':'','Content':''}
outputList = []
#Get all snippets from first given page
divList = [div.text for div in driver.find_elements(by=By.TAG_NAME, value='div') if 'journal-entry' == div.get_attribute('class')]
for div in divList:
    templist = div.split('\n',3)
    #Clearly sometimes you can have no title or content https://www.fallenlondon.com/profile/Alfaksan/24808342
    #Current handling of these snippets causes them to have location in date field
    #For now let's just fix them manually if needed
    try:
        output['Title']=templist[0]
    except:
        output['Title']=''
    try:
        output['Date']=templist[1]
    except:
        output['Date']=''
    try:
        output['Location']=templist[2]
    except:
        output['Location']=''
    try:
        output['Content']=templist[3]
    except:
        output['Content']=''
    outputList.append(dict(output))

#Check if there is left arrow active on first given page to cycle journal
buttons = driver.find_elements(by=By.TAG_NAME, value='i')
for button in buttons:
    if button.get_attribute('class') == 'fa fa-arrow-left':
        canGoLeft = True
        break
    canGoLeft = False

#debugCounter = 0 #In case we need to dind on which page exception is thrown
cycleCounter = 0
#Cycle through all pages of the journal while possible
while canGoLeft:
    buttons = driver.find_elements(by=By.TAG_NAME, value='i')
    for button in buttons:
        if button.get_attribute('class') == 'fa fa-arrow-left':
            button.click()
            canGoLeft = True
            break
        canGoLeft = False
    time.sleep(2)
    if canGoLeft == False: break
    #debugCounter+=1
    #print(debugCounter)
    
    #After many left arrow clicks it crashes, maybe this will help
    cycleCounter+=1
    if cycleCounter >= 10:
        time.sleep(20)
        cycleCounter = 0
    divList = [div.text for div in driver.find_elements(by=By.TAG_NAME, value='div') if 'journal-entry' == div.get_attribute('class')]
    for div in divList:
        templist = div.split('\n',3)
        try:
            output['Title']=templist[0]
        except:
            output['Title']=''
        try:
            output['Date']=templist[1]
        except:
            output['Date']=''
        try:
            output['Location']=templist[2]
        except:
            output['Location']=''
        try:
            output['Content']=templist[3]
        except:
            output['Content']=''
        outputList.append(dict(output))

file=open('text.json','w')
json.dump(outputList,file)
print('Hopefully reached end')
file.close()