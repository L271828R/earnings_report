# Description

The following report is a an aggregate of data collected from the below programs found on this repo.
The report gives you a landscape of tickers ordred by earnings date along with the respective straddle
spread needed to be profitable.

as an example:

```
index    ticker  earnings date         market cap sector                        straddle bands
______________________________________________________________________________________________________________________________________________________
6        snap    2019-10-22 00:00:00   18.648B    Technology                    3=15.4%      10=16.07%     17=16.73%     24=17.33%     
```

A straddle band of 3=15.4% means that in 3 days, the underlying price needs to move 15.4% for a straddle strategy to be profitable for a long
position, or needs to move less than 15.4% for a straddle position to be profitable for a short position.


If for a particular straddle band, the earnings date overlaps. One can historically see how much of a premium the earnings event affects the
straddle spread.


Data gathering programs:

* equity_basic_data_scrapper => obtains the earnings date for an equity/ticker
* straddle_finder => obtains the straddles in terms of a percentage for different maturities

The produced report looks as follows:

<img src="https://i.imgur.com/Ma16anN.jpg" width="500">


# Dependency

* Python3
* MongoClient

# How to run



