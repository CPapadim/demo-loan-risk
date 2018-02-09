import os
import pandas as pd
import numpy as np

from s3_connect import s3_connect

# tmp_localdir = '/home/jupyter/'
tmp_localdir = '~'

# Config AWS connection
s3_conn = s3_connect(access=os.environ['AWS_CLOUD_BUCKET_KEY'],
                     secret=os.environ['AWS_CLOUD_BUCKET_SECRET_KEY'],
                     bucketname='ds-cloud-public-shared')

# Load features from S3
feats = s3_conn.pull_pickle_from_s3(key='demos/loan-risk/data/feats.p',
                                    tmp_localdir=tmp_localdir)

# Load trained loan default prediction model
model = s3_conn.pull_pickle_from_s3(key='demos/loan-risk/models/RF.p',
                                    tmp_localdir=tmp_localdir)

def transform_data(data):
    """
    Inputs a json dictionary, performs feature engineering,
    and returns dataframe
    """

    # Convert from dictionary to dataframe
    df = pd.DataFrame(data)

    # Dummify features
    for dummy_feat in feats['to_dummify']:
        if dummy_feat in df:
            df = pd.concat([df, pd.get_dummies(df[dummy_feat],
                            prefix=dummy_feat)], axis=1)

            # Drop un-dummified features
            df = df.drop(dummy_feat, axis=1)

    # Include dummified features in cols_to_use
    cols_to_use = [col for col in df.columns
                   if col in feats['as_is']
                   or any([dummy_feat in col for dummy_feat in feats['to_dummify']])]

    # Drop NA and subset
    df = df[cols_to_use].dropna()

    # If after dummifying we are missing any features wrt the training data feature space, add a column of zeros for that feature
    for training_feat in feats['trained_features']:
        if training_feat not in df:
            df[training_feat] = np.zeros((df.shape[0], 1))

    return df

def predict_default_probability(data, transform=1):
    """
    Predicts the probability of default for a single instance

    Data: JSON-like data structure with the following field/features:
    feats = 'loan_amnt'
    'int_rate'
    'dti'
    'annual_inc'
    'delinq_2yrs',
    'open_acc'
    'revol_util'
    'term'
    'purpose'
    'addr_state',
    'home_ownership'
    """
    if transform:
        data = transform_data(data)
    return map(lambda x: x[1], model.predict_proba(data))

example_JSON = {"data":
     [
     {"addr_state": "AZ",  "annual_inc": "24000.0",  "delinq_2yrs": "0.0",  "dti": "27.649999999999999",  "home_ownership": "RENT",  "int_rate": "10.65",  "loan_amnt": "5000.0",  "open_acc": "3.0",  "purpose": "credit_card",  "revol_util": "83.700000000000003",  "term": " 36 months"}
     ],
     "transform": 1
     }

# print(predict_default_probability(**example_JSON))
