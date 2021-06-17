tools for options

opcurve - tool to visualize options prices at different strike prices and expiry dates

usage

python opcurve.py \<ticker\> \<expiry day\> \<expiry month\> \<expiry year\> \<min strike\> \<max strike\> \<c/p\> \<strike increment\>

python opcurveexp.py \<ticker\> \<start day\> \<start month\> \<start year\> \<end day\> \<end month\> \<end year\> \<strike\> \<c/p\> \<DTE increment\>

examples

python opcurve.py AAPL 18 06 2021 100 150 c 5 - plot option prices for AAPL calls expiring on 06/18/2021, with strike prices 100, 105, 110, ..., 145, 150

python opcurveexp.py AMZN 18 06 2021 31 12 2021 3000 p 7 - plot option prices for weekly AMZN puts expiring between 06/18/2021 and 12/31/2021, with strike price 3000
