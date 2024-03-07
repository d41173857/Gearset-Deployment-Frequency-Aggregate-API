import os
import requests
import urllib.parse
import json
import csv
import subprocess

def fetch_and_write_data(uStart, uEnd, uInterval, uGroupBy, GS_TOKEN):
    # Perform the API request
    url = "https://api.gearset.com/public/reporting/deployment-frequency/aggregate?StartDate="+uStart+"&EndDate="+uEnd+"&Interval="+uInterval+"&GroupBy="+uGroupBy

    payload = {}
    headers = {
        'accept': 'application/json',
        'Authorization': f'token {GS_TOKEN}',
        'api-version': '1'
    }

    # Capture the response
    response = requests.get(url, headers=headers, data=payload)

    # Check if the request was successful (status code 200) and write to a json file
    if response.status_code == 200:
        # Write the response content to a text file
        with open('api_response.json', 'w') as file:
            file.write(response.text)

        print("API response saved to 'api_response.json'")

    else:
        print("API request failed with status code:", response.status_code)

    # Load the JSON data from the file
    with open('api_response.json') as file:
        data = json.load(file)

    # Extract the values and dates from the JSON data
    values = [item['Value'] for item in data['Items'][0]['Values']]
    dates = [item['Date'] for item in data['Items'][0]['Values']]

    # Write the values and dates to a CSV file with modified column names
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Counts']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, value in zip(dates, values):
            writer.writerow({'Date': date, 'Counts': value})

GS_TOKEN = os.environ['MY_SECRET_KEY']

# Hard coded date ranges
# start_datetime = "2023-09-01T00:00:00.000Z"
# end_datetime = "2023-09-30T23:59:59.000Z"

# Prompt the user to enter a datetime range in ISO 8601 format
start_datetime = input("Enter the start datetime (ISO 8601 format, e.g., 2023-01-01T00:00:00Z): ")
end_datetime = input("Enter the end datetime (ISO 8601 format, e.g., 2023-12-31T23:59:59Z): ")

# Hard coded Interval and GroupBy option
# uInterval = "Weekly"
# uGroupBy = "TotalDeploymentCount"

# Prompt the user to enter the Interval option
uInterval = input("Enter the Interval option (Daily, Weekly, Monthly): ")

# Prompt the user to enter the GroupBy option
uGroupBy = input("Enter the GroupBy option (TotalDeploymentCount, Status, Owner, SourceUsername, TagetUsername, DeploymentType): ")


# Convert date ranges into URL encoded strings
uStart = urllib.parse.quote(start_datetime)
uEnd = urllib.parse.quote(end_datetime)

# Call the function
fetch_and_write_data(uStart, uEnd, uInterval, uGroupBy, GS_TOKEN)

'''
# Perform the API request
url = "https://api.gearset.com/public/reporting/deployment-frequency/aggregate?StartDate="+uStart+"&EndDate="+uEnd+"&Interval="+uInterval+"&GroupBy="+uGroupBy
 


payload = {}
headers = {
    'accept': 'application/json',
    'Authorization': f'token {GS_TOKEN}',
    'api-version': '1'
}

# Capture the response
response = requests.get(url, headers=headers, data=payload)

# Check if the request was successful (status code 200) and write to a json file
if response.status_code == 200:
    # Write the response content to a text file
    with open('api_response.json', 'w') as file:
        file.write(response.text)

    print("API response saved to 'api_response.json'")

else:
    print("API request failed with status code:", response.status_code)

  
# Load the JSON data from the file
with open('api_response.json') as file:
    data = json.load(file)

# Extract the values and dates from the JSON data
values = [item['Value'] for item in data['Items'][0]['Values']]
dates = [item['Date'] for item in data['Items'][0]['Values']]

# Write the values and dates to a CSV file with modified column names
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['Date', 'Counts']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for date, value in zip(dates, values):
        writer.writerow({'Date': date, 'Counts': value})
    file.close()
'''

# print('CSV file created successfully!')

# Open the CSV file in Excel
subprocess.Popen(['C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE', 'output.csv'])
