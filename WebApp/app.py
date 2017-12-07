from flask import Flask, request, render_template
from urllib.parse import urlencode
import requests
import csv
from bs4 import BeautifulSoup
import urllib.request

app = Flask(__name__) #app runs using flask 


submissions = [] #creates an empty list that all submissions will populate


def getDistanceMatrix(location1, location2):
    '''
    This function draws upon the google's distance matrix API taking two locations and determines
    the distance between the two locations and the approximate duration of the trip
    '''
    location = {"origins": location1, "destinations": location2} #sets location variable equal to a dictionary setting the origin and destination from the google api to the the inputted beginning and end locations
    API_ENDPOINT = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&" + urlencode(location) #accesses api location
    r = requests.get(API_ENDPOINT) #sets r equal to an api request

    status = r.json()["status"] #this requests the api in json format
    response = {} #creates a dictionary with the distance and duration

    if status == "OK": #if value no error
        response["distance"] = r.json()["rows"][0]["elements"][0]["distance"] #finds the distance from the api output based on inputs
        response["duration"] = r.json()["rows"][0]["elements"][0]["duration"] #finds the duration from the api output based on inputs
    else: #if error
        response["distance"] = {"text": "0 mi", "value": 0} #outputs the distance as 0 miles
        response["duration"] = {"text": "0 hours", "value": 0} #outputs the duration as 0 hours
    
    response["status"] = status

    return response #returns a dictionary with the distance and the duration outputs 


@app.route('/', methods=['POST', 'GET'])
def index():
    """

    Home page

    """
    if request.method == 'POST':
        #To get form submission value, do request.form['name'] --> Name is name="value" on input field
        submission = {} #creates a dictionary with the submission variables and their corresponing values

        date = request.form['date'] #sets variables equal to what was inputted on the form of the web app
        pickup = request.form['pickup']
        pickupAddress = request.form['pickupAddress']
        dropoffAddress = request.form['dropoffAddress']
        waitTime = request.form['waitTime']

        submission["date"] = date #sets the input variables to submissions for javascript 
        submission["pickup"] = pickup
        submission["pickupAddress"] = pickupAddress
        submission["dropoffAddress"] = dropoffAddress
        submission["waitTime"] = waitTime


        response = getDistanceMatrix(pickupAddress,dropoffAddress) #calls upon getDistanceMatrix function that will set "response" equal to the distance and duration that the function returns

        distance = round(response["distance"]["value"] * 0.000621371, 2) #sets distance variable and rounds the distance to two places. Also converts it to miles
        duration = round((response["duration"]["value"] / 60)/60, 2) #sets duration variable and rounds the duration to two places. Also converts it to hours
        baseRate = 13 #predetermined base rate
        mileageRate = 1.6 #predetermined mileage rate
        waitTimeRate = 15 #predetermined wait time rate
        if not waitTime: #if no wait time submitted, waitTime will be et to zero
            waitTime = 0
        timeWaited = float(waitTime) #sets float variable
        revenue = baseRate + distance*mileageRate + waitTimeRate*timeWaited #predetermined formula used to calculate revenue using the inputs and created variables 
        
        driverPay = 25 #predetermined driver wage
        reimbursementInDollars = .535 #predetermined driver mileage reimbursement rate

        cogs = driverPay*duration + distance*reimbursementInDollars #predetermined formula used to calculate revenue using the inputs and created variables

        grossProfit = revenue-cogs #sets a variable to gross profit subtracting what was calculated for the cogs from the revenue

        #how these will be shown when they are outputted in the csv file and on the web app
        submission["revenue"] = "$" + str(round(revenue,2)) #takes calculated revenue from above and adds a dollar sign in front, turns into string and rounds two places. Also sets as a submisison for javascript
        submission["cogs"] = "$" + str(round(cogs,2)) #takes calculated cogs from above and adds a dollar sign in front, turns into string and rounds two places. Also sets as a submisison for javascript
        submission["gross"] = "$" + str(round(grossProfit,2)) #takes calculated gross profit from above and adds a dollar sign in front, turns into string and rounds two places. Also sets as a submisison for javascript
        submission["distance"] = str(distance) + " " + "mi" #takes the distance gotten above and adds "mi" to it, and turns it into a string. Also sets as a submisison for javascript 
        submission["duration"] = str(duration) + " " + "hours" #takes the duration gotten above and adds "hours" to it, and turns it into a string. Also sets as a submisison for javascript

        if revenue > cogs: #if the value calculated for revenue is higher than the value calculated for cogs, the profitbale submission variable will be set to YES
            submission["profitable"] = "YES"
        else: ##if the value calculated for revenue is higher than the value calculated for cogs, the profitbale submission variable will be set to YES
            submission["profitable"] = "NO"

        global submissions 
        
        submissions.append(submission) #this adds all the newly inputted, calculated, and set variables classified as submission variables to the submissions list
        with open('trip_data.csv', 'w', encoding='utf-8', newline='') as f: #creates csv file
        
            writer = csv.writer(f) #sets variable equal to the csv writer command

            #sets the fields variable to the column titles
            fields = ('Date','Pick Up Time','Pick Up Address','Drop Off Address','Wait Time','Revenue','Cost of Goods Sold','Gross Profit','Trip Distance','Trip Time','Profitable')
            writer.writerow(fields) #this writes the first row with the column names created above

            writer.writerow(submission.values()) #this writes the rest of the rows with all the submission values correspinding to the correct column name
        

        return render_template('index.html', submissions=submissions) #renders the index.html file as a post request
    elif request.method == 'GET':        
        return render_template('index.html', submissions=submissions) #renders the index.html file as a get request



if __name__ == '__main__':
    app.run() #runs app
