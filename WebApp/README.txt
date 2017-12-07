Synopsis: 

The Trip Evaluator allows MainStreeter, a Non Emergency Medical Transportation Company to
calculate certain aspects of a trip based off of the minimal information that is given. 
This takes the minimal information given for an individual trip and calculates more data based off the intial inputs.  
It calculates things like distance, duration, revenue, cogs, and gross profit.  
It then exports this data to a csv file where futher data analytics can be conductedbe able nd exports it then 
submits into a csv file giving us the ability to anayze further. 

Installation: 
Packages to install: 

-r requirements.txt
flask
urllib.parse
bs4
requests
csv
urllib.request

Motivation: 
Chris has started his own business, MAinStreeter. This motivated him to find the best way to evaluate 
the non emergency medical transportation trips and be able to log data to evaluate and analyze all of the trips carried out. 


API Reference: 
We used the googles distance matrix API to calculate the distance and duration. It takes a beginning address and an ending address that is submitted from the web app.
 