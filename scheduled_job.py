import os
import requests
import pandas as pd
import numpy as np

from s3_connect import s3_connect

api_url = 'https://demo.datascience.com/deploy/deploy-predict-loan-default-142978-v3/'
api_secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjNGY1YzIxOS01Nzc1LTQ4M2MtOTkxOC1kNWE1ZjJiNzI2NDciLCJzZXJ2aWNlTmFtZSI6ImRlcGxveS1wcmVkaWN0LWxvYW4tZGVmYXVsdC0xNDI5NzgtdjMiLCJpYXQiOjE1MDYzNzM2MDh9._aOEXrW6FmdPsq1r7aqwaHwU7SESvVd0RzI7H5KR3OE'

tmp_localdir = os.path.expanduser("~")

# Setup S3 connection object
s3_conn = s3_connect(access=os.environ['AWS_CLOUD_BUCKET_KEY'],
                     secret=os.environ['AWS_CLOUD_BUCKET_SECRET_KEY'],
                     bucketname='ds-cloud-public-shared')

def get_LC_data():
    # Returns lending club data
    return s3_conn.pull_pickle_from_s3(key='/demos/loan-risk/data/scheduled_run_data.p',tmp_localdir=tmp_localdir)

def clean_api_output(body):
    # Converts text output from request into a list of floats
    return map(lambda x: float(x.replace('[','').replace(']','')), body.text.split(','))

def calculate_expected_profit(df):
    # Returns expected profit as a pandas series

    # Calculate monthly payments
    p = df['loan_amnt']
    r = df['int_rate'] / 12 / 100
    n = df['term'].map(lambda x: int(x.split(' ')[1]))
    payment = p * (r * (1+r)**n) / ((1+r)**n -1)

    # Calculate overall profit if loan reaches maturity
    df['profit'] = (n * payment) - p

    # Calculate expected profit given probability of default
    return ((1 - df['p_default']) * df['profit']) - (df['p_default'] * df['loan_amnt'])



def score_loans(expected_profit_threshold=1000):
    """
    Given a daily batch of new loans, return the ids of any loans that have
    an expected profit equal to or greater than `expect_profit_threshold`.
    """

    print("Loads a batch of Lending Club data for one day")
    data = get_LC_data()

    print("Use deploy API to predict loan default")
    body = requests.post(api_url,
        json={"data": data},
        cookies={'datascience-platform': api_secret_key}
    )

    print("Clean request output")
    default_probs = clean_api_output(body)

    print("Convert data to Pandas Dataframe")
    df = pd.DataFrame(data)
    df['p_default'] = default_probs

    print("Calculate expected profit")
    df['expected_profit'] = calculate_expected_profit(df)

    print("Find the ids of loans that meet our criteria")
    best_loan_ids = list(df.ix[df['expected_profit'] >= expected_profit_threshold].index)

    print("Return dataframe as well as best loan indices")
    return df, best_loan_ids


score_loans(expected_profit_threshold=1000)
