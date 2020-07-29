import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
import pickle
import requests


def save_ftse100_tickers():
    # Scrapes wikipedia list for FTSE100 tickers (EPIC), then pickles them
    resp = requests.get('https://en.wikipedia.org/wiki/FTSE_100_Index')
    soup = bs.BeautifulSoup(resp.text, "lxml") #text of source code
    table = soup.find('table', {'class': 'wikitable sortable', 'id': 'constituents'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        # Stocks on LSE have .L appended when searching Yahoo! Finance
        if ticker.endswith('.'):
            ticker = ticker + 'L'
        else:
            ticker = ticker + '.L'
        tickers.append(ticker)
    with open("ftse100tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

def get_data_from_yahoo(reload_ftse100=False, reload_ticker_data=False):
    # Requests historical stock data from Yahoo! finance using tickers in pickle. Puts data into Pandas dataframe then writes to CSV file
    if reload_ftse100:
        tickers = save_ftse100_tickers()
    else:
        with open("ftse100tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if reload_ticker_data:
        if os.path.exists('stock_dfs_ftse100'):
            for filename in os.listdir('stock_dfs_ftse100'):
                path = os.path.join('stock_dfs_ftse100', filename)
                os.remove(path)
        if not os.path.exists('stock_dfs_ftse100'):
            os.makedirs('stock_dfs_ftse100')

        start, end = get_dates()

        for ticker in tickers:
            try:
                print(ticker)
                df = web.get_data_yahoo(ticker, start, end)
                df.to_csv('stock_dfs_ftse100/{}.csv'.format(ticker))

            except:
                pass

        compile_data()


def get_dates():
    # Start and end dates of stock data
    print("\n******* Historical start date of stock data *******\n")
    startyear, startmonth, startday = input("Enter start date (yyyy mm dd): ").split()
    start = dt.datetime(int(startyear), int(startmonth), int(startday))
    print("\n******* End date of portfolio asset data *******\n")
    if input("Collect data up to today?(y/n): ").upper() == 'Y':
        end = dt.datetime.now()
    else:
        endyear, endmonth, endday = input("Enter end date (yyyy mm dd): ").split()
        end = dt.datetime(int(endyear), int(endmonth), int(endday))
    print("\n******* Processing *******\n")

    return start, end

def compile_data():
    # Reads in individual dataframes of stocks, strips all but Adjusted Close, and compiles into single dataframe for visualising
    print("************ Compiling data ************")
    with open("ftse100tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs_ftse100/{}.csv'.format(ticker))
            df.set_index('Date', inplace=True)

            df.rename(columns = {'Adj Close':ticker}, inplace=True)
            df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')

        except:
            pass

    main_df.to_csv('ftse100_joined_closes.csv')

def visualise_data():
    # Computes correlation between historical stock data, plots it using a heatmap for Pos correlation->Neg correlation
    df = pd.read_csv('ftse100_joined_closes.csv')

    df_corr = df.corr()

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels, fontsize=8)
    ax.set_yticklabels(row_labels, fontsize=7)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.title("Historical FTSE100 stock correlation")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    ticker_reload = False
    data_reload = False
    if input("\nReload list of FTSE100 tickers?(y/n): ").upper() == 'Y':
        ticker_reload = True
    if input("\nReload Yahoo ticker data?(y/n: ").upper() == 'Y':
        data_reload = True
    get_data_from_yahoo(ticker_reload, data_reload)
    visualise_data()


