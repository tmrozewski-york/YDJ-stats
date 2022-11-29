"""
by Tomasz Mrozewski tmrozews@yorku.ca
last updated November 29, 2022
As of then, everything works
"""

# import required modules
import os
import pandas as pd
import requests
import json
import datetime

# set the working directory
my_dir = ' ' # wd set here
os.chdir(my_dir)

# open the CSV file with credentials and endpoints for all journals
my_keys = pd.read_csv(" ") # file name here

# set the value for last month in YY-MM format
# used later as a lookup value to identify's last month statistics in the certain API calls
# also used to identify the month of the stats pull
today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
monthLookup = lastMonth.strftime("%Y-%m")


# create empty lists for final output
# hese will be populated by the code in the for loop
# each datapoint is described in metric_list and the value is given in value_list
journal_list = []
month_list = []
metric_list = []
value_list = []

# iterate through the credentials file
# query all endpoints for each journal, using the API token
# order of queries is:
    # 1. published submissions (total)
    # 2. published issues (total)
    # 3. abstract views (last month)
    # 4. galley views (last month)
# query looks at total published submissions and total issues because published back issues would not be returned if we queried by date
for ind in my_keys.index:
    # assign journal ID (jabbr), endpoint, and token values from CSV to variables
    abbr = my_keys['jabbr'][ind]
    subs = my_keys['subs_endpoint'][ind]
    issues = my_keys['issues_endpoint'][ind]
    abviews = my_keys['abstractViews_endpoint'][ind]
    galviews = my_keys['galleyViews_endpoint'][ind]
    key = my_keys['token'][ind]


    # 1. PUBLISHED SUBMISSIONS (TOTAL)
    # call for submissions data, using submissions endpoint and API token
    # status:3 means that we're only requesting published submissions
    subs_call = requests.get(
    subs,
    params={'apiToken':key,
    'status':'3'}
    )
    
    # read the JSON file from the submissions data call
    y = json.dumps(subs_call.json())
    z = json.loads(y)
    
    # extract the desired datapoint (itemsMax) as variable x
    x = z["itemsMax"]
    
    #write the journal identifier, month, metric type, and value to the lists
    journal_list.append(abbr)
    month_list.append(monthLookup)
    metric_list.append ('published submissions')
    value_list.append(x)
    
    # 2. PUBLISHED ISSUES (TOTAL)
    # call for submissions data, using submissions endpoint and API token
    # isPublished:true means that we're only requesting published issues
    issues_call = requests.get(
        issues,
        params={'apiToken':key,
        'isPublished':'true'}
        )
    
    # read the JSON file from the submissions data call
    q = json.dumps(issues_call.json())
    r = json.loads(q)
    
    # extract the desired datapoint (itemsMax) as variable p
    p = r["itemsMax"]
    
    #write the journal identifier, month, metric type, and value to the lists
    journal_list.append(abbr)
    month_list.append(monthLookup)
    metric_list.append ('published issues')
    value_list.append(p)
    
    # 3. ABSTRACT VIEWS (LAST MONTH)
    # call for abstract views data, using views endpoint and API token
    # pulls for views back to 2001 by default, which is as far back as the API goes
    # could update this later to maybe only pull last month's stats
    abviews_call = requests.get(
    abviews,
    params={'apiToken':key,
    'dateStart':'2001-01-01'}
    )
    
    # read the JSON file from the abstract views call
    # use the monthLookup variable (defined earlier) to extract only last month's data
    # get the month and 
    b = json.dumps(abviews_call.json())
    c = json.loads(b)
    d = next(item for item in c if item["date"] == monthLookup)
    
    # extract the desired datapoint (value) as variable a
    a = d.get('value')
    
    #write the journal identifier, month, metric type, and value to the lists
    journal_list.append(abbr)
    month_list.append(monthLookup)
    metric_list.append ('abstract views')
    value_list.append(a)
    
    # 4. GALLEY VIEWS (LAST MONTH)
    # call for galley views data, using views endpoint and API token
    # pulls for views back to 2001 by default, which is as far back as the API goes
    # could update this later to maybe only pull last month's stats
    galviews_call = requests.get(
    galviews,
    params={'apiToken':key,
    'dateStart':'2001-01-01'}
    )
    
    # read the JSON file from the galley views call
    # use the monthLookup variable (defined earlier) to extract only last month's data
    # get the month and 
    f = json.dumps(galviews_call.json())
    g = json.loads(f)
    h = next(item for item in g if item["date"] == monthLookup)
    
    # extract the desired datapoint (value) as variable a
    e = h.get('value')
    
    # write the journal identifier, month, metric type, and value to the lists
    journal_list.append(abbr)
    month_list.append(monthLookup)
    metric_list.append ('galley views')
    value_list.append(e)
    
    # print which journal just finished, to help debugging
    print(abbr)
    
# create dataframe df by zipping the lists that were populated by the lookups
# again, each datapoint is described in metric_list and the value is given in value_list
df = pd.DataFrame(list(zip(journal_list,month_list,metric_list, value_list)),
                  columns = ['journal','month','metric', 'value'])

# flatten the dataframe by using a pivot function
# one line for each journal for the month, containing all values. metrics as column titles
pivoted = pd.pivot_table(df, values='value', index=['journal','month'], columns='metric')

# write output to CSV in working directory
pivoted.to_csv(monthLookup +'.csv')

# print message for successful completion of script
print('If you\'re reading this, the script probably worked!')