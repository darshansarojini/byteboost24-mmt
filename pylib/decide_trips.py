import typing

import networkx as nx
import numpy as np
import pandas as pd

from .create_transport_graph import (
    create_transport_graph_distance,
    create_transport_graph_cost,
    create_transport_graph_time,
)


def load_trips_from_csv(
    filename: str, params: typing.Dict[str, typing.Any]
) -> pd.DataFrame:
    df = (
        pd.read_csv(filename)
        .rename(
            columns={
                # old data
                "origin_lon": "origin longitude",
                "origin_lat": "origin latitude",
                "destination_lon": "destination longitude",
                "destination_lat": "destination latitude",
                # new data
                "Lat_from": "origin latitude",
                "Lon_from": "origin longitude",
                "Lat_to": "destination latitude",
                "Lon_to": "destination longitude",
                "Trips_median": "number of travelers",
            },
        )
        .dropna()
    )
    driving = df.copy()
    driving["modality"] = "driving"
    driving["distance"] = driving["driving_time"] * params["driving speed"]

    ground_transit = df.copy()
    ground_transit["modality"] = "ground transit"
    ground_transit["ground transit time"] = (
        ground_transit["Walk_to_start_time"]
        + ground_transit["Walk_from_end_time"]
        + ground_transit["In_vehicle_time"]
    )
    ground_transit["distance"] = np.clip(
        (
            ground_transit["ground transit time"]
            - params["ground transit boarding time"]
        )
        * params["ground transit speed"],
        a_min=0.0,
        a_max=None,
    )

    res = pd.concat([driving, ground_transit], ignore_index=True)
    res["source nodeid"] = -res.index - 1
    res["target nodeid"] = -res.index - 1 - len(res)
    return res[
        [
            "source nodeid",
            "target nodeid",
            "origin longitude",
            "origin latitude",
            "destination longitude",
            "destination latitude",
            "number of travelers",
            "distance",
            "modality",
        ]
    ].reset_index(drop=True)


def decide_trips(
    trips: pd.DataFrame,
    vertiports: pd.DataFrame,
    routes: pd.DataFrame,
    params: typing.Dict[str, typing.Any],
) -> pd.DataFrame:

    res = trips.copy()

    G = create_transport_graph_distance(trips, vertiports, routes)
    G_time = create_transport_graph_time(G, params)
    time_paths = dict(nx.all_pairs_dijkstra_path(G_time))

    G_cost = create_transport_graph_cost(G, params)
    cost_paths = dict(nx.all_pairs_dijkstra_path(G_cost))

    distance_driving = []
    distance_ground_transit = []
    distance_evtol = []
    distance_walking = []
    for source_nodeid, target_nodeid in res[
        ["source nodeid", "target nodeid"]
    ].values:
        path = time_paths[source_nodeid][target_nodeid]
        distance_driving.append(
            sum(
                G.get_edge_data(path[i], path[i + 1])["distance"]
                for i in range(len(path) - 1)
                if G.get_edge_data(path[i], path[i + 1])["modality"]
                == "driving"
            )
        )
        distance_ground_transit.append(
            sum(
                G.get_edge_data(path[i], path[i + 1])["distance"]
                for i in range(len(path) - 1)
                if G.get_edge_data(path[i], path[i + 1])["modality"]
                == "ground transit"
            )
        )
        distance_evtol.append(
            sum(
                G.get_edge_data(path[i], path[i + 1])["distance"]
                for i in range(len(path) - 1)
                if G.get_edge_data(path[i], path[i + 1])["modality"] == "evtol"
            )
        )
        distance_walking.append(
            sum(
                G.get_edge_data(path[i], path[i + 1])["distance"]
                for i in range(len(path) - 1)
                if G.get_edge_data(path[i], path[i + 1])["modality"]
                == "walking"
            )
        )

    res["distance driving"] = distance_driving
    res["distance ground transit"] = distance_ground_transit
    res["distance evtol"] = distance_evtol
    res["distance walking"] = distance_walking

    res["trip cost"] = (
        res["distance driving"].astype(bool) * params["driving base cost"]
        + res["distance driving"] * params["driving marginal cost"]
        + res["distance ground transit"].astype(bool)
        * params["ground transit base cost"]
        + res["distance ground transit"]
        * params["ground transit marginal cost"]
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
