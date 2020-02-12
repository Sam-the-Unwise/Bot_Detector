'''
AUTHOR: Samantha Muellner
DESCRIPTION: Script that runs a query on Github repositories and analyzes the information to determine if the user is a bot or not
'''

# imports
import requests, time, json, datetime, csv, pymongo
from variables import AUTHO_TOKEN

# Variables
PERCENTAGE = 0
headers = {"Authorization": AUTHO_TOKEN}

# Defines the query to run
def create_query(author_name):
    order_by = "{field: CREATED_AT, direction: ASC}"

    query = f'''
    query {{
        user (login: "{author_name}")
        {{
            repositoriesContributedTo(orderBy: {order_by})
            {{
                edges
                {{
                    node
                    {{
                        name
                        id
                        createdAt
                    }}
                }}
            }}
        }}
    }}'''

    return query


# Funtion that uses requests.post to make the API call
def run_query(query):
    
    request = requests.post('https://api.github.com/graphql', json = {'query': query}, headers = headers)

    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f'ERROR [{request.status_code}]: Query failed to execute...\nRESPONSE: {request.text}')

# function that will seek out the users with a bot % above 80
#   users are found through teh csv file that's been passed in
def find_users(csv_file):
    with open(csv_file,'rt') as filehandler:
        #to avoid complications with the null byte
        data = csv.reader(x.replace('\0', '') for x in filehandler)

        for row in data:
            if row[PERCENTAGE] > 80:
                print("true")
                
# function that will simply run a test through our query function with known users to see if 
#   it is succesfully able to access github and provide information 
def test_run_query():
    user_list = ["Sam-the-Unwise", "cforonda", "igorsteinmacher", "gabetgreen"]

    for item in user_list:
        query = create_query(item)
        output = run_query(query)

        print(output)



test_run_query()