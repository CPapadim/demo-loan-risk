from __future__ import print_function
import requests
import subprocess
import json
import time

import os
import sys


print("Starting mleap \n", file=sys.stderr)

#Step 1 - Start mleap
subprocess.Popen(["sudo", "/opt/docker/bin/mleap-serving"]) #By default mleap serves on port 65327
time.sleep(5) # wait for mleap to start

print("Loading model to server \n", file=sys.stderr)

#Step 2 - Load model onto mleap server
payload = {"path":"/tmp/loan-risk-demo/SparkExamples/harry_lc_pipeline_rf2.zip"}
headers = {'content-type': 'application/json'}
put_resp = requests.put("http://localhost:65327/model", json=payload, headers=headers) #By default mleap serves on port 65327


#Step 3 - Define model input schema - the leapframe

features = {
  "schema": {
    "fields": [{
      "name": "loan_amnt",
      "type": "double"
    }, {
      "name": "dti",
      "type": "double"
    }, {
      "name": "int_rate",
      "type": "double"
    }, {
      "name": "annual_inc",
      "type": "double"
    }, {
      "name": "delinq_2yrs",
      "type": "double"
    }, {
      "name": "term_ 36 months",
      "type": "double"
    }, {
      "name": "term_ 60 months",
      "type": "double"
    }, {
      "name": "purpose_car",
      "type": "double"
    }, {
      "name": "purpose_credit_card",
      "type": "double"
    }, {
      "name": "purpose_debt_consolidation",
      "type": "double"
    }, {
      "name": "purpose_educational",
      "type": "double"
    }]
  }
}

print("Initialization complete", file=sys.stderr)
def predict(features_lst):
    feats = features #create local copy of the schema
    feats['rows'] = [features_lst]  #To pass in data to the model, we need to add it to the ['rows'] key of the leapframe

    #get prediction
    resp = requests.post("http://localhost:65327/transform", 
                    json = feats)
    
    output_dict = json.loads(resp.text)
    
    dat_class = output_dict['rows'][0][-1] # the class is stored in the last entry in rows
    class_probs = output_dict['rows'][0][-2]['values'] #this holds the class probabilities
    
    return (dat_class, class_probs)
