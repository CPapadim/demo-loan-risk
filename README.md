![](https://s8.postimg.org/9p7awpe5x/Lending_Club_Logo.jpg)
# Predicting Loan Defaults and Optimizing Your Investment Strategy

# Introduction

Peer-to-peer (P2P) lending is the practice of lending money to individuals or businesses through online services that match lenders with borrowers, enabling anyone to play the role of the bank and fund loans with fixed interest rates. P2P lending is a boom industry: Lending Club is the largest P2P platform today and boasts a total of [$26 billion in issued loans since its inception in 2007.](https://www.lendingclub.com/info/statistics.action)

Say you are a large institutional investor that has been trusted with $1M to invest, and you're interested in investing your money on Lending Club. How should you invest your $1M bankroll? With hundreds of new loans possible options available to you daily, it's difficult to manually eyeball your options. Plus, your competitors are using automated models to snatch up the juicy loans before you even have a chance to blink. What you need is a data-driven solution: you need a machine learning model that can automatically pick out the best loans in a matter of seconds to maintain your competitive edge.

In this demo, we will demonstrate how you can use machine learning on the DataScience Platform to optimize your loan selection strategy.

# Dataset

Dataset used here contains metadata for over 500K Lending Club loans. These data range from 2007-2017 and [are publicly available.](https://www.lendingclub.com/info/download-data.action)

The data includes hundreds of features including:
* Interest rate
* Debt to Income ratio (DTI)
* Term (Loan Length)
* Purpose of Loan
* And many more

With the following binary response variable that determines whether a loan ultimately was paid-off or defaulted:
* Default

# Goals

The primary goal of this demo is to use machine learning to automatically select Lending Club loans that provide the best return on investment. 

This goal can be broken into several subgoals:

1. We will use **notebook containers** to utilize the popular Python machine learning package scikit-learn to develop a random forest model for predicting the probability of default for a given loan. 
2. We will synthesize any insights or methodology into **reports** to keep our stakeholders informed about our efforts.
3. We will **deploy an API** for our random forest model so that we productionize it to power any internal application we choose.
4. We will use the DataScience platform's **scheduled runs** feature to productionized our model to make automatic data-driven decision on daily batches of new loans, selecting out the best loan for our portfolio in seconds. 

# Key Benefits of the Platform For This Demo

The features of the DataScience Platform can help us achieve these goals with the following:

1. **Notebook containers** allow you to launch sessions with scalable resource allocations. This ensures that you have all the resources you need on-demand to implement sophisiticated machine learning models. This also ensures that your session does not overwhelm the resources available to the rest of your team. Finally, GitHub integrations allow you to sync the work you do within a session by simply clicking a button.
2. **Reports** allow you to effortlessly convert any notebook or Markdown formatted code into a polished report in one centralized location. No need to search through your inbox for that email with the screenshots from your analysis. Simply share the link to the report with your colleagues and you're done! 
3. **Deployed API** allows you to productionize any model you create. This API can be shared with a colleague for his or her own project, used to power any internal application, or implemented in an automated scheduled run.
4. **Scheduled runs** allow you to automate a process hourly, daily, or at a time interval of your choice. This feature has synergy with the deployed API: you can schedule a model to score daily batches of new loans at the same time every day. 

# Structure of this Demo

This demo will include the following steps:

1. We will begin with a brief explatory data analysis of the features of the Lending Club data and how they relate to default rates. In particular, we will discuss how interest rates, debt to income ratio, and the interaction of these two features impact the rate of default. [**Report "EDA Concise"**](https://demo.datascience.com/project/optimizing-your-investment-strategy/outputs/eda-concise-UG9zdFR5cGU6MTYw)
2. After exploring the data, we will launch a notebook container with the appropriate resources, and build a random forest model to predict loan default. **Notebook Container**
3. Next, we will productionize our random forest model by deploying it behind a RESTful API. We can call this API to figure out the probability of default for any given loan. Later, we will use this API in a scheduled run. This API will also enable our team to use our work to power any future internal applications. [**Deploy A Model API**](https://demo.datascience.com/project/optimizing-your-investment-strategy/outputs/predict-loan-default-142978/versions/5)
4. We will then create a report that communicates how we intend to utilize our deployed model to key stakeholders. We will discuss the model's use-case and as well as our profit optimization methodology. [**Report "Optimize Loan Selection"**](https://demo.datascience.com/project/optimizing-your-investment-strategy/outputs/optimizing-loan-selection-UG9zdFR5cGU6MTU4)
5. To close the loop, we will setup a scheduled run that will pull the metadata for all new loans available on Lending Club and score the profitability of each loan using our deployed model API. [**Scheduled run**](https://demo.datascience.com/project/optimizing-your-investment-strategy/job/daily-loan-scoring-166439)
6. We can also demonstrate a sample use case for the deployed model in [Loan Allocation Application](http://loan-demo-app.herokuapp.com/)
