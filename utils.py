import os
from s3_connect import s3_connect

api_secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjMjBkMzAyNC00NmU0LTQwZTAtODk3MS0zY2UyOWFiZDFjZGQiLCJzZXJ2aWNlTmFtZSI6ImRlcGxveS1wcmVkaWN0LWRlZmF1bHQtcHJvYmFiaWxpLTg0OS12MyIsImlhdCI6MTUwMDU4ODg5NX0.3394Ay3g3NyUQ0BDYuV_ACYW3hmJUcjR0I4v8KxbBhY'

tmp_localdir = '/home/jupyter/'

# Setup S3 connection object
s3_conn = s3_connect(access=os.environ['AWS_CLOUD_BUCKET_KEY'],
                     secret=os.environ['AWS_CLOUD_BUCKET_SECRET_KEY'],
                     bucketname='ds-cloud-public-shared')

def get_LC_data():
    # Returns lending club data
    return s3_conn.pull_pickle_from_s3(key='demos/loan-risk/data/scheduled_run_data.p',tmp_localdir=tmp_localdir)

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
