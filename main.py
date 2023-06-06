import requests
import json

# Get all bills by last updated date
limit = 3
headers = {'Content-Type': 'application/json'}
url = "https://api.congress.gov/v3/bill?api_key=Y1hRdQCbKpOFFQVY1sUsxyiAzZ3XQgejdC45GRP1&limit=" + str(limit)
payload = {}
response = requests.request("GET", url, headers=headers, data=payload)
obj = json.loads(response.text)
json_formatted_str = json.dumps(obj, indent=4)
print(json_formatted_str)

# TOKENIZE TERMS & INDEX DOCUMENTS
for i in range(len(obj["bills"])):
  title = obj["bills"][i]["title"]
  latestActionDate = obj["bills"][i]["latestAction"]["actionDate"]
  print(latestActionDate, title)
# Stopwords
# Lemmatization AND / OR Stemming
# Tokenization Inverted Index

# WRITE KEY PERFORMANCE INDICATORS
# Query Time
# Index Time
# Precision
# Accuracy

# WRITE CHARTS
# Count of Keywords Monthly Bar Chart

# WRITE QUERY-ABILITY - SINGLE & MULTIPLE TERM
# {"healthcare"} or {"health care"} or {"healthcare", "standards", "consumer"}
# Lemmtization AND / OR Stemming on Query