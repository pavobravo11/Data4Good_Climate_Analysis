import itertools
import time
from functools import partial
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

    buttons = []

    for i, station in enumerate(data["Station Name"].unique()):
        station_data = data[(data['Station Name'] == station)]
        pm_data = station_data[station_data['Parameter'] == "PM2.5 Mass"].resample('1M').mean().interpolate(
            method='linear',
            limit_direction='forward',
            axis=0)
        methane_data = station_data[station_data['Parameter'] == "Methane"].resample('1M').mean().interpolate(
            method='linear', limit_direction='forward', axis=0)
        ozone = station_data[station_data['Parameter'] == "Ozone"].resample('1M').mean().interpolate(method='linear',
                                                                                                     limit_direction='forward',
                                                                                                     axis=0)
        aqi = station_data[station_data['Parameter'] == "Air Quality Index"].resample('1M').mean().interpolate(
            method='linear', limit_direction='forward', axis=0)

        pm_data["txt"] = pm_data["Average Daily Value"].apply(round2).astype(str) + " ug/m3"
        methane_data["txt"] = methane_data["Average Daily Value"].apply(round2).astype(str) + " ppm"
        ozone["txt"] = ozone["Average Daily Value"].apply(round2).astype(str) + " ppm"
        aqi["txt"] = aqi["Average Daily Value"].apply(round2).astype(str)

        # Add traces
        fig.add_trace(go.Scatter(
            x=pm_data.index,
            y=pm_data["Average Daily Value"],
            text=pm_data["txt"],
            name=f"{station} - PM2.5",
            yaxis="y",
            line={"color": f"#{y_colors[0]}"},
            visible=True if i == 0 else False
        ))

        fig.add_trace(go.Scatter(
            x=methane_data.index,
            y=methane_data["Average Daily Value"],
            text=methane_data["txt"],
            name=f"{station} - Methane",
            yaxis="y2",
            line={"color": f"#{y_colors[1]}"},
            visible=True if i == 0 else False

        ))

        fig.add_trace(go.Scatter(
            x=ozone.index,
            y=ozone["Average Daily Value"],
            text=ozone["txt"],
            name=f"{station} - Ozone",
            yaxis="y3",
            line={"color": f"#{y_colors[2]}"},
            visible=True if i == 0 else False

        ))

        fig.add_trace(go.Scatter(
            x=aqi.index,
            y=aqi["Average Daily Value"],
            text=aqi["txt"],
            name=f"{station} - Air Quality Index",
            yaxis="y4",
            line={"color": f"#{y_colors[3]}"},
            visible=True if i == 0 else False

        ))

    # style all the traces
    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 8},
        mode="lines+markers",
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
            "linecolor": fig.data[i].line.color,
            "tickfont": {"color": fig.data[i].line.color},
            "titlefont": {"color": fig.data[i].line.color},
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
        hide = itertools.repeat(False, i * 4)
        show = itertools.repeat(True, 4)
        hide_after = itertools.repeat(False, len(fig.data) - ((i + 1) * 4))

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
