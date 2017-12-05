from flask import Flask, request, render_template
from urllib.parse import urlencode
import requests
import csv
from bs4 import BeautifulSoup
import urllib.request

app = Flask(__name__) 


submissions = []


def getDistanceMatrix(location1, location2):
    location = {"origins": location1, "destinations": location2}
    API_ENDPOINT = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&" + urlencode(location)
    r = requests.get(API_ENDPOINT)

    status = r.json()["status"]
    response = {}

    if status == "OK":
        response["distance"] = r.json()["rows"][0]["elements"][0]["distance"]
        response["duration"] = r.json()["rows"][0]["elements"][0]["duration"]
    else:
        response["distance"] = {"text": "0 mi", "value": 0}
        response["duration"] = {"text": "0 hours", "value": 0}
    
    response["status"] = status

    return response

DOWNLOAD_URL = 'https://www.eia.gov/petroleum/gasdiesel/'

def download_page(url):
    return urllib.request.urlopen(url)

def getGas(html):
    

    soup = BeautifulSoup(html)
    gas_table_soup = soup.find('table', attrs={'class': 'simpletable'})

    for gas_row in gas_table_soup.find_all('tr')[3]:
        avg_gas = gas_row.find('td')[3].string
        print(avg_gas)


@app.route('/', methods=['POST', 'GET'])
def index():
    """

    Home page

    """
    if request.method == 'POST':
        #To get form submission value, do request.form['name'] --> Name is name="value" on input field
        submission = {}

        date = request.form['date']
        pickup = request.form['pickup']
        pickupAddress = request.form['pickupAddress']
        dropoffAddress = request.form['dropoffAddress']
        waitTime = request.form['waitTime']

        submission["date"] = date
        submission["pickup"] = pickup
        submission["pickupAddress"] = pickupAddress
        submission["dropoffAddress"] = dropoffAddress
        submission["waitTime"] = waitTime


        response = getDistanceMatrix(pickupAddress,dropoffAddress)

        distance = round(response["distance"]["value"] * 0.000621371, 2)
        duration = round((response["duration"]["value"] / 60)/60, 2)
        baseRate = 13
        mileageRate = 1.6
        waitTimeRate = 15
        if not waitTime:
            waitTime = 0
        timeWaited = float(waitTime)
        revenue = baseRate + distance*mileageRate + waitTimeRate*timeWaited 

        url = DOWNLOAD_URL
        html = download_page(url)
        
        driverPay = 25
        reimbursementInDollars = .535

        cogs = driverPay*duration + distance*reimbursementInDollars

        grossProfit = revenue-cogs

        submission["revenue"] = "$" + str(round(revenue,2))
        submission["cogs"] = "$" + str(round(cogs,2))
        submission["gross"] = "$" + str(round(grossProfit,2))
        submission["distance"] = str(distance) + " " + "mi"
        submission["duration"] = str(duration) + " " + "hours"

        if revenue > cogs:
            submission["profitable"] = "YES"
        else:
            submission["profitable"] = "NO"

        global submissions
        print(submission.values())
        submissions.append(submission)
        with open('trip_data.csv', 'w', encoding='utf-8', newline='') as f:
        #change varaibles
        #figure out where this goes
        
            writer = csv.writer(f)

            fields = ('Date','Pick Up Time','Pick Up Address','Drop Off Address','Wait Time','Revenue','Cost of Goods Sold','Gross Profit','Trip Distance','Trip Time','Profitable')
            writer.writerow(fields)

            writer.writerow(submission.values())
        

        return render_template('index.html', submissions=submissions)
    elif request.method == 'GET':        
        return render_template('index.html', submissions=submissions)



if __name__ == '__main__':
    app.run()

#Fix csv writer
#fix gas website scraper
#fix github
#document code
#Finish readme to show what packages to install
#create server and domain