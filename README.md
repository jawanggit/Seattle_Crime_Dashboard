# Seattle_Crime_Dashboard
EDA project using Seattle Crime Data

## Project Overview & Background:
### Problem Description
Gaining insight into the understanding of the crime in your area can be very difficult. Not only is it important to understand the types and frequency of crimes happening in your area, it is critical to visualize this data across space and time. 

### Background
To show how insights can be gained from crime data, I took Seattle crime data from the [Seattle Police Department] (https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5) and built an interactive dashboard that allows users to create individual views of crime in their area by type, location, and date range. In addition, on the hypothese testing tab, you can hypothesis test if certain areas in Seattle have statistically signficant greater incidences of a certain crime than another.


## Data Set Assembly:

### Data Sources
The crime data comes from the [Seattle Police Department] (https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5) and ranges from Jan 2017 to Jan 2019. In order to translate inputted addresses, the app calls the MapQuest API which responds back wit a latitude and longitude. 

* Link to [MapQuest API] documenatation (https://developer.mapquest.com/documentation/open/)

### Cleaning the data
To gain a high-level understanding of the raw data, the pandas-profiling library was used generate an html report of the data. This report provides dataset statistics and variable types along with the distinct and missing counts for each variable. This report was extremely useful in quickly understanding what the different values in data represented and which features in the dataset were incomplete or would need to be excluded. 

* Link to profiling report



## Processing the data

### Helpful functions

## Dashboard 

### Functionality

## Hypthese Testing Page

### Functionality

## Key Findings








# systematic-identification-of-anomalies-in-earnings-report-reactions-in-us-stocks

## Project Overview & Background:
### Problem Description
The typical and expected model of stock behavior following quarterly earnings releases (henceforth referred to as "earnings events") is that companies that produce results that significantly beat expectations tend to experience positive returns and those that meaningfully miss expectations tend to experience negative returns.

However, in a significant minority of cases companies that produce earnings that meaningfully beat Wall Street consensus EPS estimates see their stocks fall substantially in value following the earnings event. These counter-intutitive reactions can be a major frustration to investors, many of whom devote substantial time and effort to research and model these quarterly results. 

### Project Description
Apply machine learning algorithms to company financial data in order to systematically identify situations where this sort of anomalous reaction (beat estimates; experience negative returns anyway) is likely.

![alt text](https://github.com/jlewis425/anomalies-in-earnings-release-reactions/blob/master/Project_overview.png)

### Background:
Fundamental investors in equity securities devote signficant effort in evaluating and forecasting the future
prospects of the companies in which they invest. Companies which trade in the public US equity markets provide
public releases of their financials on a quarterly basis. These quarterly earnings releases are therefore 
important signposts for investors; they are the main mechanism for evaluating the operational and financial
performance of their investments. 

Companies' earnings releases typically include a quarterly income statement, other financial statements,
and additional operating metrics (in either narrative or tablular form). Most public companies in the US also host a conference call on the same day as the earnings release. During these calls corporate managers discuss the company's results and outlook and field questions from investors and Wall Street analysts that follow the company.

Quarterly earnings releases are therefore understandably much anticipated by equity investors and by the 
Wall Street analysts that follow the comapnies. Because digesting and analyzing all of the relevant details
which are typically presented in a quarterly release can be time-consuming, the marketplace has developed a 
sort of shorthand heuristic. 

Quarterly earnings per share (EPS) which exceed the Wall Street "consensus" estimate are considered "beats" and those
that fall short are considered "misses". EPS that match the consensus estimate are said to be "in line". 
In reality, the consensus EPS estimate isn't a consensus at all, but is rather the arithmetic average of all of
the analyst estimates for that company that have been published (fairly recently) for the quarter in question.

## Data Set Assembly:

### Data Sources
The data set was assembled primarily using FactSet Research Systems' software package. FactSet's screening tool facilitates rule-based filtering of stocks and aggregation of related data. Supplementary data related to options and stock volatility was sourced from Quantcha via the Quandl internet platform. 

![alt text](https://github.com/jlewis425/anomalies-in-earnings-release-reactions/blob/master/Data_sources.png)

### Stock Sample Selection Criteria
Stocks for the data set were selected from the universe of US equities based on the following two criteria:

* Minimum reported sales of over $100 million total over previous four quarters; **AND**
* Minimum reported Average Daily Traded Value (stock price x trading volume) of $15 million over previous 3 months.

### Sample Time Frame
Data for earnings events from 1Q14 through 3Q18 were collected. The observations from 3Q18 were separated and held for out-of-sample testing. Following data cleaning there were an average of approximately 1,250 observations per quarter.

![alt text](https://github.com/jlewis425/anomalies-in-earnings-release-reactions/blob/master/obs_by_qtr.png)

### Stock Return Measurement
* Time Horizon: Measured price change from day before earnings events until three (trading) days following.
* Return Type: Converted to relative return by adjusting for return of S&P 1500 over same period. 

Relative returns for the nearly 24,000 earnings events remaining in the data set after data cleaning were centered around close to zero, with an approximately normal distribution and a standard deviation of almost 8%.

![alt text](https://github.com/jlewis425/anomalies-in-earnings-release-reactions/blob/master/rtns_all.png)

### Categorization
Observations were categorized based on the following criteria:
![alt text](https://github.com/jlewis425/anomalies-in-earnings-release-reactions/blob/master/Label_generation.png)

## Model Selection & Methodology:

### Model Selection
The key considerations relating to model selection are as follows:
* Significantly imbalanced classes
* Soft classification desired
* Mix of numerical and categorical data
* Standardization problematic due to mix of temporal spaces in data
* Significant complex interactions between features likely to exist

Based on the above, tree-based models (Random Forest & Gradient Boosting) most appropriate.

### Methodology Challenge
The proportion of observations in the target class shows a rising trend over time.

![alt text](https://github.com/jlewis425/anomalies-in-earnings-release-reactions/blob/master/targets_pct_plot.png)

Given that trend, typical random train/rest splitting and cross-validation methods showed significant instability.
It was also unclear whether training on a data set that contained a much smaller number of observations in the target class than the out-of-sample test set contained would introduce some kind of bias to the out-of-sample test results.

### Solution
Rather than train a single model on 18 quarters of data to predict the 19th, multiple models were trained and fit on 4- and 8-quarter lookback windows to forecast the target class for the 5th and 9th quarters, respectively.

This sequential simulation approach provided "back tested" results to observe the stability of the predictions over time and to evaluate whether a trading strategy derived from these results could be expected to be consistently profitable.

![alt text](https://github.com/jlewis425/anomalies-in-earnings-release-reactions/blob/master/Methodology_illustration.png)










