import itertools
from datetime import datetime
from functools import partial

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing

round2 = partial(round, ndigits=2)


def runner():
    data = pd.read_csv('Historical_Air_Quality.csv', header=0, parse_dates=["Date"], index_col="Date")
    data = data.sort_index()

    fig = go.Figure()

    # Update layout
    fig.update_layout(
        template="plotly_dark",
        dragmode="zoom",
        hovermode="x",
        legend=dict(traceorder="reversed"),
        height=600,
        margin=dict(
            t=100,
            b=100
        ),
    )

    y_colors = [
        "F1AC4E",
        "90A39E",
        "B56154",
        "BEC8AE",
    ]

    data_names = [
        "PM2.5 Mass",
        "Methane",
        "Ozone",
        "Air Quality Index",
    ]

    outlier_limits = [
        100,
        None,
        None,
        None,
    ]

    units = [
        "ug/m3",
        "ppm",
        "ppm",
        "AQI"
    ]

    seasonality = [
        4,
        12,
        0,
        12,
    ]

    buttons = []

    for i, station in enumerate(data["Station Name"].unique()):
        station_data = data[(data['Station Name'] == station)]
        for dni, dn in enumerate(data_names):
            data_for_pred = station_data[station_data['Parameter'] == dn]
            data_for_pred['Average Daily Value'] = data_for_pred['Average Daily Value'].replace(0, np.nextafter(0, 1))
            if outlier_limits[dni]:
                data_for_pred = data_for_pred[data_for_pred['Average Daily Value'] <= outlier_limits[dni]]
            data_for_pred = data_for_pred[['Average Daily Value']]
            data_for_pred = data_for_pred.sort_index().squeeze().resample('1M').mean().bfill()

            have_prediction = False

            if seasonality[dni]:
                try:
                    prediction_model = ExponentialSmoothing(data_for_pred,
                                                            damped_trend=True,
                                                            seasonal="mul",
                                                            seasonal_periods=seasonality[dni],
                                                            trend="add",
                                                            use_boxcox=True
                                                            )

                    fitted = prediction_model.fit(remove_bias=False)
                    have_prediction = True
                except ValueError as e:
                    print(e)

            if have_prediction:
                predicted_values = pd.concat([fitted.fittedvalues, fitted.forecast(12)])
                predicted_values.name = "Average Daily Value"

                pframe = predicted_values.to_frame()
                pframe['Count'] = 1
                pframe["txt"] = pframe["Average Daily Value"].apply(round2).astype(str) + f" {units[dni]}"

            data_for_display = station_data[station_data['Parameter'] == dn]
            data_for_display = data_for_display.resample('1M').mean().interpolate(
                method='linear',
                limit_direction='forward',
                axis=0)
            data_for_display["txt"] = data_for_display["Average Daily Value"].apply(round2).astype(str) + f" {units[dni]}"

            # Add traces
            fig.add_trace(go.Scatter(
                x=data_for_display.index,
                y=data_for_display["Average Daily Value"],
                text=data_for_display["txt"],
                name=f"{station} - ${data_names[dni]}",
                yaxis="y" if dni == 0 else f"y{dni+1}",
                line={"color": f"#{y_colors[dni]}"},
                visible=True if i == 0 else False,
            ))

            if have_prediction:
                fig.add_trace(go.Scatter(
                    x=pframe.index,
                    y=pframe["Average Daily Value"],
                    text=pframe["txt"],
                    name=f"{station} - Forecast ${data_names[dni]}",
                    yaxis="y" if dni == 0 else f"y{dni+1}",
                    line={"color": f"#{y_colors[dni]}", "dash": "dot"},
                    visible=True if i == 0 else False
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=[],
                    y=[],
                    text=[],
                    name=f"{station} - Forecast ${data_names[dni]}",
                    yaxis="y" if dni == 0 else f"y{dni+1}",
                    line={"color": f"#{y_colors[dni]}", "dash": "dot"},
                    visible=True if i == 0 else False
                ))

    # style all the traces
    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 8},
        mode="lines",
        showlegend=False
    )

    units = [
        "ug/m3", "ppm", "ppm", "AQI"
    ]

    common_params = {
        "anchor": "x",
        "autorange": True,
        "mirror": True,
        "showline": True,
        "side": "right",
        "tickmode": "auto",
        "ticks": "",
        "type": "linear",
        "zeroline": False,
        "nticks": 3,
    }

    r = [(datetime.now() - relativedelta(years=15)).date(), (datetime.now() + relativedelta(months=1)).date()]

    axis_params = {}
    for i in range(len(y_colors)):
        specific_params = {
            "domain": [
                (1 / len(y_colors) * i),
                (1 / len(y_colors) * (i + 1)) - 0.01
            ],
            "title": units[i],
            "linecolor": f"#{y_colors[i]}",
            "tickfont": {"color": f"#{y_colors[i]}"},
            "titlefont": {"color": f"#{y_colors[i]}"},
        }
        axis_params[f"yaxis{i + 1}" if i else "yaxis"] = {**common_params, **specific_params}

    fig.update_layout(
        xaxis=dict(
            autorange=False,
            rangeslider=dict(
                visible=True,
                autorange=True,
            ),
            type="date"
        ),
        **axis_params
    )
    fig.update_xaxes(rangeslider_range=r)
    fig.update_xaxes(range=r)

    for i, station in enumerate(data["Station Name"].unique()):
        hide = itertools.repeat(False, i * 8)
        show = itertools.repeat(True, 8)
        hide_after = itertools.repeat(False, len(fig.data) - ((i + 1) * 8))

        buttons.append(
            dict(
                args=[{"visible": list(itertools.chain(hide, show, hide_after))}],
                label=station,
                method="update"
            ))

    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="left",
                y=1.5,
                yanchor="top"
            ),
        ]
    )

    fig.write_json("input/recent_history.json")


if __name__ == '__main__':
    runner()
