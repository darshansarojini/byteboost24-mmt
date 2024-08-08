import itertools as it
import networkx as nx
import numpy as np
import pandas as pd

from .util import geodesic_kilometers


def create_transport_graph_distance(
    trips: pd.DataFrame,
    vertiports: pd.DataFrame,
    routes: pd.DataFrame,
) -> nx.DiGraph:

    # create distance graph
    G = nx.DiGraph()

    # add existing transit edges to the graph
    for modality, group in trips.groupby("modality"):
        G.add_weighted_edges_from(
            zip(
                trips["source nodeid"],
                trips["target nodeid"],
                trips["distance"],
            ),
            modality=modality,
        )

    vertiports = vertiports.copy()
    vertiports.reset_index(drop=True, inplace=True)
    vertiports["nodeid"] = vertiports.index

    # add vertiport nodes and edges to the graph
    longitude_lookup = dict(zip(vertiports["nodeid"], vertiports["longitude"]))
    latitude_lookup = dict(zip(vertiports["nodeid"], vertiports["latitude"]))
    routes["source longitude"] = routes["source nodeid"].map(
        longitude_lookup,
    )
    routes["source latitude"] = routes["source nodeid"].map(
        latitude_lookup,
    )
    routes["target longitude"] = routes["target nodeid"].map(
        longitude_lookup,
    )
    routes["target latitude"] = routes["target nodeid"].map(
        latitude_lookup,
    )
    routes["distance"] = list(
        it.starmap(
            geodesic_kilometers,
            zip(
                zip(routes["source latitude"], routes["source longitude"]),
                zip(routes["target latitude"], routes["target longitude"]),
            ),
        )
    )
    G.add_weighted_edges_from(
        zip(
            routes["target nodeid"],
            routes["source nodeid"],
            routes["distance"],
        ),
        modality="evtol",
    )

    # connect vertiport nodes to transit nodes
    for what in ["source", "target"]:
        for _, row in vertiports.iterrows():
            trip_source_distances = np.fromiter(
                it.starmap(
                    geodesic_kilometers,
                    zip(
                        zip(
                            routes[f"{what} latitude"],
                            routes[f"{what} longitude"],
                        ),
                        it.repeat((row["latitude"], row["longitude"])),
                    ),
                ),
                dtype=float,
            )
            numclosest = min(3, len(trip_source_distances))
            if numclosest == 1:
                closest = [0]
            else:
                closest = np.argpartition(trip_source_distances, numclosest)[
                    :numclosest
                ]

            for modality in ["driving", "walking"]:
                G.add_weighted_edges_from(
                    zip(
                        it.repeat(row["nodeid"]),
                        routes.loc[closest, f"{what} nodeid"],
                        trip_source_distances[closest],
                    ),
                    modality=modality,
                )
                G.add_weighted_edges_from(
                    zip(
                        routes.loc[closest, f"{what} nodeid"],
                        it.repeat(row["nodeid"]),
                        trip_source_distances[closest],
                    ),
                    modality=modality,
                )

    return G


def create_transport_graph_cost(
    distance_graph: nx.DiGraph,
    params: dict,
) -> nx.DiGraph:

    G = distance_graph.copy()
    for u, v, d in G.edges(data=True):
        marginal_cost = params.get(f"{d['modality']} marginal cost", 0)
        base_cost = params.get(f"{d['modality']} base cost", 0)
        d["weight"] = d["weight"] * marginal_cost + base_cost

    return G


def create_transport_graph_time(
    distance_graph: nx.DiGraph,
    params: dict,
) -> nx.DiGraph:

    G = distance_graph.copy()
    for u, v, d in G.edges(data=True):
        speed = params.get(f"{d['modality']} speed")
        boarding_time = params.get(f"{d['modality']} boarding time", 0)
        d["weight"] = d["weight"] / speed + boarding_time

    return G
