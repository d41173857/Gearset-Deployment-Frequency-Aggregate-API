import os
import sys
import requests
import urllib.parse
import json
import csv
import subprocess

GS_TOKEN = os.environ['MY_SECRET_KEY']

def fetch_and_write_data(uStart, uEnd, uInterval, uGroupBy):
    # Perform the API request
    url = "https://api.gearset.com/public/reporting/deployment-frequency/aggregate?StartDate="+uStart+"&EndDate="+uEnd+"&Interval="+uInterval+"&GroupBy="+uGroupBy
    print (url)

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

def get_user_input():
    start_datetime = input("Enter the start datetime (ISO 8601 format, e.g., 2024-01-01T00:00:00Z): ")
    end_datetime = input("Enter the end datetime (ISO 8601 format, e.g., 2024-01-31T23:59:59Z): ")
    uInterval = input("Enter the Interval option (Daily, Weekly, Monthly): ")
    uGroupBy = input("Enter the GroupBy option (TotalDeploymentCount, Status, Owner, SourceUsername, TagetUsername, DeploymentType): ")
    return start_datetime, end_datetime, uInterval, uGroupBy

def main():
    num_of_args = len(sys.argv) - 1

    if num_of_args == 0:
        start_datetime, end_datetime, uInterval, uGroupBy = get_user_input()
        #uStart = urllib.parse.quote(start_datetime)
        #uEnd = urllib.parse.quote(end_datetime)
        # fetch_and_write_data(uStart, uEnd, uInterval, uGroupBy)
        fetch_and_write_data(start_datetime,end_datetime, uInterval, uGroupBy)
        # Open the CSV file in Excel
        subprocess.Popen(['C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE', 'output.csv'])
    elif num_of_args == 4:
        _, uStart, uEnd, uInterval, uGroupBy = sys.argv # The underscore _ is a common convention for a variable whose value you don’t care about (in this case, the script name).
        fetch_and_write_data(uStart, uEnd, uInterval, uGroupBy)
    else:
        print("Oops")

if __name__ == "__main__":
    main()