from typing import List
import plotly.graph_objects as go
import pandas as pd
import os
from util.lib.timeConverter import time_converter

ohlc_trades_data: str = os.path.join('/home', 'len', 'FutureTrading', 'data', 'ohlc', 'BTCUSDT-1h-2021-01.csv')
ohlc_column_names: List[str] = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime',
                                    'QuoteAssetVol', 'NumberOfTrades', 'TakerBuyBaseAssetVol',
                                    'TakerBuyQuoteAssetVol', 'Ignore']
volume_data: str = os.path.join('/home', 'len', 'FutureTrading', 'data', 'volumeProfile', 'BTCUSDT-aggTrades-2021-01.csv')
df: pd.DataFrame = pd.read_csv(ohlc_trades_data, sep=',', names=ohlc_column_names)
volume: pd.DataFrame = pd.read_csv(volume_data, sep=',')
df['OpenTime'] = df['OpenTime'].map(time_converter)
volume['Price'] = volume['Price'].map(lambda x: round(x/100)*100)


fig = go.Figure(
    data=[
        go.Candlestick(
            x=df['OpenTime'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            xaxis='x',
            yaxis='y',
            showlegend=False
        ),
        go.Bar(
            x=volume['Quantity'],
            y=volume['Price'],
            # base=50,
            orientation='h',
            xaxis='x2',
            yaxis='y2',
            showlegend=False,
            marker=go.bar.Marker(color='#000')
        )
    ],
    layout=go.Layout(
        title=go.layout.Title(text='Candlestick with Volume Profile from 2021-01'),
        xaxis=go.layout.XAxis(
            side='bottom',
            title='Date',
            showticklabels=True,
            overlaying='x2'
        ),
        yaxis=go.layout.YAxis(
            side='left',
            title='Price',
            showticklabels=True,
            overlaying='y2'
        ),
        xaxis2=go.layout.XAxis(
            side='top',
            rangeslider=go.layout.xaxis.Rangeslider(visible=False),
            showticklabels=True
        ),
        yaxis2=go.layout.YAxis(
            showticklabels=False,
            side='right',
            # title='Price',
            matches='y'
        )
    )
)

fig_ohlc = go.Figure(
    data=[
        go.Candlestick(
            x=df['OpenTime'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            xaxis='x',
            yaxis='y',
            showlegend=False
        )
    ]
)

fig_volume = go.Figure(
    data=[
        go.Bar(
            base=50,
            x=volume['Price'],
            y=volume['Quantity'],
            orientation='v',
            xaxis='x',
            yaxis='y',
            offset=100,
            showlegend=False,
            marker=go.bar.Marker(color='#000')
        )
    ]
)

fig_volume_h = go.Figure(
    data=[
        go.Bar(
            base=50,
            y=volume['Price'],
            x=volume['Quantity'],
            orientation='h',
            xaxis='x',
            yaxis='y',
            showlegend=False,
            marker=go.bar.Marker(color='#000')
        ),
        go.Bar(
            base=0,
            y=volume['Price'],
            x=volume['Quantity'],
            orientation='h',
            xaxis='x',
            yaxis='y',
            showlegend=False,
            marker=go.bar.Marker(color='#ff0000')
        )
    ],
    # layout=go.Layout(
    #     xaxis=go.layout.XAxis(
    #         range=[90,500]
    #     )
    # )
)

fig.show()
#fig_ohlc.show()
#fig_volume.show()
#fig_volume_h.show()