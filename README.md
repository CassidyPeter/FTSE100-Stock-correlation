# FTSE100-Stock-correlation

A visual representation of correlation between consistuent stocks of the FTSE100, built as part of Sentdex's Algorithmic Trading series. Stock correlation can be used for risk management to minimise losses. Where a portfolio is diversified with non-correlated stocks, volatility is mitigated - but where a portfolio is diversified with negatively correlated stocks, risk is reduced.

Dependencies:
 - beautifulsoup4
 - pandas
 - Pandas-datareader
 - Matplotlib
 - numpy
 - pickle
 - requests

Note: There is a bug with the Natwest Group EPIC on Yahoo! Finance, hence the streaks of absent data.

![Correlation](https://github.com/CassidyPeter/FTSE100-Stock-correlation/blob/master/FTSE100_correlation.png?raw=true)
