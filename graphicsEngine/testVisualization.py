import os

import pandas as pd
import plotly.graph_objects as go

import dataConfig as cfg
from util.lib.timeConverter import time_converter

ohlc_src: str = os.path.join(cfg.OHLC_DP, 'BTCUSDT-1h-2021-01.csv')
vol_src: str = os.path.join(cfg.VOLP_DP, 'BTCUSDT-aggTrades-2021-01.csv')
ohlc: pd.DataFrame = pd.read_csv(ohlc_src, sep=',', names=cfg.OHLC_CNL)
volume: pd.DataFrame = pd.read_csv(vol_src, sep=',')
ohlc[cfg.OHLC_CN['ots']] = ohlc[cfg.OHLC_CN['ots']].map(time_converter)
volume[cfg.VOLP_CN['px']] = volume[cfg.VOLP_CN['px']].map(lambda x: round(x / 100) * 100)

fig = go.Figure(
    data=[
        go.Candlestick(
            x=ohlc[cfg.OHLC_CN['ots']],
            open=ohlc[cfg.OHLC_CN['open']],
            high=ohlc[cfg.OHLC_CN['high']],
            low=ohlc[cfg.OHLC_CN['low']],
            close=ohlc[cfg.OHLC_CN['close']],
            xaxis='x',
            yaxis='y',
            showlegend=False
        ),
        go.Bar(
            x=volume[cfg.VOLP_CN['qx']],
            y=volume[cfg.VOLP_CN['px']],
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
            x=ohlc[cfg.OHLC_CN['ots']],
            open=ohlc[cfg.OHLC_CN['open']],
            high=ohlc[cfg.OHLC_CN['high']],
            low=ohlc[cfg.OHLC_CN['low']],
            close=ohlc[cfg.OHLC_CN['close']],
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
            x=volume[cfg.VOLP_CN['px']],
            y=volume[cfg.VOLP_CN['qx']],
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
            x=volume[cfg.VOLP_CN['px']],
            y=volume[cfg.VOLP_CN['qx']],
            orientation='h',
            xaxis='x',
            yaxis='y',
            showlegend=False,
            marker=go.bar.Marker(color='#000')
        ),
        go.Bar(
            base=0,
            x=volume[cfg.VOLP_CN['px']],
            y=volume[cfg.VOLP_CN['qx']],
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
# fig_ohlc.show()
# fig_volume.show()
# fig_volume_h.show()