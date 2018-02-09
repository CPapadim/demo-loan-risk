from __future__ import division
import glob
import os
import pandas as pd
import numpy as np
from scipy.stats import binned_statistic, linregress, gaussian_kde
from scipy.stats import randint as sp_randint
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
import seaborn as sns
import statsmodels.api as sm
from IPython.display import clear_output

from s3_connect import s3_connect

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)

def kde_scipy( vals1, vals2, (a,b), (c,d), N ):

    x=np.linspace(a,b,N)
    y=np.linspace(c,d,N)
    X,Y=np.meshgrid(x,y)
    positions = np.vstack([Y.ravel(), X.ravel()])

    values = np.vstack([vals1, vals2])
    kernel = gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    return [x, y, Z]

def make_kdeplot((varX1, varY1), (varX2, varY2), (a,b), (c,d), N, colorsc, title, x_label, y_label):
    #varX, varY are lists, 1d numpy.array(s), or dataframe columns, storing the values of two variables

    x1, y1, Z1 = kde_scipy(varY1, varX1, (a,b), (c,d), N )
    x2, y2, Z2 = kde_scipy(varY2, varX2, (a,b), (c,d), N )

    data = go.Data([
       go.Contour(
           z=Z2-Z1,
           x=x1,
           y=y1,
           colorscale='Hot',
           reversescale=True,
           opacity=0.9,
           contours=go.Contours(
               showlines=False) )
     ])

    layout = go.Layout(
        title= title,
        font= go.Font(family='Georgia, serif',  color='#635F5D'),
        showlegend=False,
        autosize=False,
        width=650,
        height=650,
        xaxis=go.XAxis(
            range=[a,b],
            showgrid=False,
            nticks=7,
            title=x_label
        ),
        yaxis=go.YAxis(
            range=[c,d],
            showgrid=False,
            nticks=7,
            title=y_label
        ),
        margin=go.Margin(
            l=40,
            r=40,
            b=85,
            t=100,
        ),
    )

    return go.Figure( data=data, layout=layout )


def split_bin_data(df, feature, bins):
    # Split data into default vs paid dataframes
    df_paid = df.ix[df['default']==0]
    df_default = df.ix[df['default']==1]

    # Bin feature
    paid_bins = np.histogram(df_paid[feature],bins=bins)
    default_bins = np.histogram(df_default[feature], bins=bins)

    return paid_bins, default_bins

# Plotting continuous feature vs default rate
def default_rate_binned_barplot(df, feature, bins, xlabel, title):
    """Makes a barplot of a specified feature on the x-axis vs default rate on the y-axis.
       The independent variable is a continuous variable which is binned into bars.
       The dependent variable is the proportion of defaults within each bin."""

    # Split data into default vs paid dataframes and bin
    paid_bins, default_bins = split_bin_data(df, feature, bins)

    # Make plotly figure
    data = [
    go.Bar(
    x=paid_bins[1],
    y=default_bins[0] / (default_bins[0]+paid_bins[0])
    )]

    layout = go.Layout(
        title=title,
        xaxis={'title':xlabel},
        yaxis={'title':'Default Rate'}

    )

    return go.Figure(data=data, layout=layout)

# Plotting continuous feature vs default rate
def default_rate_scatter(df, feature, bins, xlabel, title):
    """Makes a barplot of a specified feature on the x-axis vs default rate on the y-axis.
       The independent variable is a continuous variable which is binned into bars.
       The dependent variable is the proportion of defaults within each bin."""

    # Split data into default vs paid dataframes and bin
    paid_bins, default_bins = split_bin_data(df, feature, bins)

    # Make plotly figure
    trace = go.Scatter(
        x = paid_bins[1],
        y = default_bins[0] / (default_bins[0]+paid_bins[0]),
        mode = 'markers'
    )

    data = [trace]

    # Plot and embed in ipython notebook!
    return go.Figure(data=data)


# Plotting categorical feature vs default rate
def default_rate_categorical_barplot(df, feature, xlabel, title):
    """Makes a barplot of a specified feature on the x-axis vs default rate on the y-axis.
       The independent variable is the categories of the feature.
       The dependent variable is the proportion of defaults within each categorical."""

    # Split data into default vs paid dataframes and bin
    df_grouped = df.groupby(feature).mean()['default'].sort_values()

    # Make plotly figure
    data = [
    go.Bar(
    x=df_grouped.index,
    y=df_grouped
    )]

    layout = go.Layout(
        title=title,
        xaxis={'title':xlabel},
        yaxis={'title':'Default Rate'}

    )

    return go.Figure(data=data, layout=layout)


def default_rate_by_state(df):
    """Creates a choropleth for default rate per state"""
    state_defaults = df.groupby('addr_state').mean()['default']

    scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
                [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

    data = [ dict(
            type='choropleth',
            colorscale = scl,
            autocolorscale = False,
            locations = state_defaults.index,
            z = state_defaults,
            locationmode = 'USA-states',
    #         text = df['text'],
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                ) ),
            colorbar = dict(
                title = "Default Rate")
            ) ]

    layout = dict(
            title = 'Default Rates by State',
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)'),
            yaxis = {'fixedrange': True},
            xaxis = {'fixedrange': True}
                 )

    return dict( data=data, layout=layout )
