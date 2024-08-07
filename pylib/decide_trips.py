import itertools as it
import typing

from geopy.distance import geodesic
import pandas as pd


def geodesic_kilometers(*args) -> float:
    return geodesic(*args).kilometers


def load_trips_from_csv(filename: str) -> pd.DataFrame:
    res = pd.read_csv(filename).rename(
        columns={
            "origin_lon": "origin longitude",
            "origin_lat": "origin latitude",
            "destination_lon": "destination longitude",
            "destination_lat": "destination latitude",
        },
    )
    res["number of travelers"] = 1
    return res


def decide_trips(
    trips: pd.DataFrame,
    vertiports: pd.DataFrame,
    routes: pd.DataFrame,
    params: typing.Dict[str, typing.Any],
) -> pd.DataFrame:

    res = trips.copy()
    res["distance"] = list(it.starmap(
        geodesic_kilometers,
        zip(
            zip(res["origin latitude"], res["origin longitude"]),
            zip(res["destination latitude"], res["destination longitude"]),
        )
    ))

    res["distance driving"] = res["distance"]
    res["distance ground transit"] = 0.0
    res["distance evtol"] = 0.0
    res["distance walking"] = 0.0

    res["trip cost"] = (
        res["distance driving"].astype(bool) * params["driving base cost"]
        + res["distance driving"] * params["driving marginal cost"]
        + res["distance ground transit"].astype(bool) * params["ground transit base cost"]
        + res["distance ground transit"] * params["ground transit marginal cost"]
        + res["distance evtol"].astype(bool) * params["evtol base cost"]
        + res["distance evtol"] * params["evtol marginal cost"]
    )

    res["trip duration"] = (
        res["distance driving"] / params["driving speed"]
        + res["distance ground transit"] / params["ground transit speed"]
        + res["distance evtol"] / params["evtol speed"]
        + res["distance evtol"].astype(bool) * params["evtol boarding time"]
        + res["distance walking"] / params["foot speed"]
    )

    return res[
        [
            "origin longitude",
            "origin latitude",
            "destination longitude",
            "destination latitude",
            "number of travelers",
            "trip cost",
            "trip duration",
            "distance driving",
            "distance walking",
            "distance ground transit",
            "distance evtol",
        ]
  ].reset_index(drop=True)
