import requests
import json
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

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
terms = []
stopwords = ["for", "of", "the", ",", "or", "a", "to"]
for i in range(len(obj["bills"])):
  title = obj["bills"][i]["title"]
  latestActionDate = obj["bills"][i]["latestAction"]["actionDate"]
  tokenlist = word_tokenize(title)
  for token in tokenlist:
    if token not in terms and token not in stopwords:
      terms.append(token)
  print(latestActionDate, title)
print(terms)



# Stopwords
# Lemmatization AND / OR Stemming
# Tokenization Inverted Index OR other method

# WRITE KEY PERFORMANCE INDICATORS
# Query Time
# Index Time
# Precision
# Recall
# F-Measure

# WRITE CHARTS
# Count of Keywords Monthly Bar Chart

# WRITE QUERY-ABILITY - SINGLE & MULTIPLE TERM
# {"healthcare"} or {"health care"} or {"healthcare", "standards", "consumer"}
# Lemmtization AND / OR Stemming on Query