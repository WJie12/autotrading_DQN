from datetime import datetime
import os
from matplotlib import pyplot as plt
import h5py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.dates as mdate
import matplotlib.dates as mdates


def get_data(stock_name, stock_tabel):
    """ Returns a 3 x n_step array """

    industry = pd.read_csv('data/{}.csv'.format(stock_tabel))["code"].astype("str")
    data = pd.read_csv('data/{}.csv'.format(stock_name)).drop(columns="DateTime")
    data = data[industry].astype("float")
    data = np.array(data.T)
    return data


def get_scaler(env):
    """ Takes a env and returns a scaler for its observation space """
    low = [0] * (env.n_stock * 2 + 1)

    high = []
    max_price = env.stock_price_history.max(axis=1)
    min_price = env.stock_price_history.min(axis=1)
    max_cash = env.init_invest * 3  # 3 is a magic number...
    max_stock_owned = max_cash // min_price
    for i in max_stock_owned:
        high.append(i)
    for i in max_price:
        high.append(i)
    high.append(max_cash)

    scaler = StandardScaler()
    scaler.fit([low, high])
    return scaler


def maybe_make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def buy_and_hold_benchmark(stock_name, init_invest, test):
    df = pd.read_csv('./data/{}.csv'.format(stock_name)).iloc[test:, :]
    dates = df['DateTime'].astype("str")
    per_num_holding = init_invest // 19
    num_holding = per_num_holding // df.iloc[0, 1:]
    balance_left = init_invest % 19 + ([per_num_holding for _ in range(19)] % df.iloc[0, 1:]).sum()
    buy_and_hold_portfolio_values = (df.iloc[:, 1:] * num_holding).sum(axis=1) + balance_left
    buy_and_hold_return = buy_and_hold_portfolio_values.iloc[-1] - init_invest
    return dates, buy_and_hold_portfolio_values, buy_and_hold_return


def plot_all(stock_name, daily_portfolio_value, env, test):
    '''combined plots of plot_portfolio_transaction_history and plot_portfolio_performance_comparison'''
    fig, ax = plt.subplots(2, 1, figsize=(16, 8), dpi=100)

    portfolio_return = daily_portfolio_value[-1] - 20000
    df = pd.read_csv('./data/{}.csv'.format(stock_name)).iloc[test:, :]
    dates = df['DateTime'].astype("str")
    dates = [datetime.strptime(d, '%Y%m%d').date() for d in dates]

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    ax[0].set_title('{} Total Return on {}: ${:.2f}'.format("DQN", stock_name, portfolio_return))
    ax[0].plot(dates, daily_portfolio_value, color='red', label=stock_name)
    ax[0].set_ylabel('Price')
    ax[0].xaxis.set_major_formatter(mdate.DateFormatter('%Y%m%d'))
    ax[0].legend()
    ax[0].grid()

    dates, buy_and_hold_portfolio_values, buy_and_hold_return = buy_and_hold_benchmark(stock_name, env.init_invest, test)
    agent_return = daily_portfolio_value[-1] - env.init_invest
    ax[1].set_title('{} vs. Buy and Hold'.format("DQN"))
    dates = [datetime.strptime(d, '%Y%m%d').date() for d in dates]
    ax[1].plot(dates, daily_portfolio_value, color='green',
               label='{} Total Return: ${:.2f}'.format("DQN", agent_return))
    ax[1].plot(dates, buy_and_hold_portfolio_values, color='blue',
               label='{} Buy and Hold Total Return: ${:.2f}'.format(stock_name, buy_and_hold_return))
    ax[1].set_ylabel('Portfolio Value (..)')
    # print(len(dates),)
    ax[1].xaxis.set_major_formatter(mdate.DateFormatter('%Y%m%d'))
    plt.xticks(pd.date_range('2018-1-02', '2019-08-22', freq='1m'))
    # ax[1].set_xticks(np.linspace(0, len(df), 1))
    ax[1].legend()
    # ax[1].grid()
    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(hspace=0.5)
    plt.show()

