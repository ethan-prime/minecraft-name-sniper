import requests
import datetime
import math
import json

info = []

with open('userdata.txt') as f:
    userdata = f.readlines()

for line in userdata:
    info.append(line)

email = info[0].split(':')[1].replace('\n','')
password = info[1].split(':')[1]

print(info)
print(email)
print(password)

payload = {
    'username': email,   
    'password': password    
}

get_token = requests.post("https://authserver.mojang.com/authenticate",headers={'content-type':'application/json'}, json=payload)
#print(get_token.content.decode('utf-8'))
token = json.loads(get_token.content)
auth = 'Bearer ' + token['accessToken']
#auth = input('Please input your authorization token: ') #get auth token 
link = 'https://api.minecraftservices.com/minecraft/profile/name/' #link used to navigate api
heads = {'authorization':auth, 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'} #simple headers
name = input('Please input you requested name: ') #desired name
time = input('Please input the time and second (00:00): ') #time in form minutes:seconds name is released (ex. 6:04:15 = 04:15) -- hour is excluded
clock_delay = input('How far behind you clock is in seconds (time.is): ') #time in full seconds clock is delayed by -- used for timing
manual_delay = input('How many ms to delay snipe by (defaults at 0 ms): ') #add delay based on your clock delay (ex. clock is behind a fraction of a second) to make up for it, or just to adjust timings



#setting defaults
if clock_delay == '':
    clock_delay = 0
if manual_delay == '':
    manual_delay = 0

#converting inputs to integers
manual_delay = int(manual_delay)
clock_delay = int(clock_delay)

#making time readable by code
time = time.split(':')

#while loop variables
a = False
n = 0
s = False

#check if it is ready to execute code based upon time
while s == False:
    #print(datetime.datetime.now().strftime("%M:%S"))
    if datetime.datetime.now().strftime("%M") == time[0] and int(datetime.datetime.now().strftime("%S")) == int(time[1])-clock_delay and int(datetime.datetime.now().strftime("%f")) >= manual_delay*1000:
        s = True #closes loop
        print('[STARTED TASK]')
        print('STARTED ON TIME + ' + str(manual_delay))
        #loop until name is available -- usually available within one-two requests
        while a == False:
            availability = requests.get(link+name+'/available', headers=heads)
            print(availability.status_code)
            #print(availability.content)
            if "AVAILABLE" in availability.content.decode('utf-8'):
                print('AVAILABLE NOW')
                a = True #closes loop
                #requests to change name through api
                #change = requests.put(link+name,headers=heads)
                print('STATUS CODE [' + str(change.status_code) + ']')
                #results -- read prints for description of status codes
                if change.status_code == 200:
                    a == True
                    print('[SUCCESSFUL NAME CHANGE] ' + name)
                elif change.status_code == 403:
                    print('[FAILURE] NAME TAKEN')
                elif change.status_code == 401:
                    a == True
                    print('[FAILURE] UNAUTHORIZED')
                elif change.status_code == 429:
                    a == True
                    print('[FAILURE] TOO MANY REQUESTS')
                else:
                    print('[FAILURE] ERROR UNKNOWN')