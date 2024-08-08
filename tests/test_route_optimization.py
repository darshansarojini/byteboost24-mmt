import os
from pylib.decide_trips import (
    load_trips_from_csv,
    decide_trips,
)
from pylib.decide_trips_testing import (
    get_default_params,
)
from pylib.setup_vertiport_optimization import (
    vertiport_route_optimization
)
import pandas as pd
import random


def make_dummy_vertiports(trips: pd.DataFrame) -> pd.DataFrame:
    data = [
        [0, 39.7332951667, -121.5952684164],
        [1, 39.8005882542, -121.1974720985],
        [2, 39.7642005404, -121.7362872902],
        [3, 39.6816951682, -121.2539154941],
        [4, 39.7783275821, -121.6473392442],
        [5, 39.4655315708, -121.1028219319],
        [6, 39.9253078505, -121.0833032838],
        [7, 39.7164979505, -121.2956565353],
        [8, 39.4933481981, -121.4394756055],
        [9, 39.7340653610, -121.8353993572],
        [10, 39.8334197568, -121.6543651566],
        [11, 40.0246601939, -122.0091110581],
        [12, 39.5422222065, -121.2281749676],
        [13, 39.6191086850, -121.5800596202],
        [14, 39.7549169493, -121.8144041996],
        [15, 40.0407450597, -121.5707295166],
        [16, 39.8697140334, -121.2958754744],
        [17, 39.9952152570, -121.3653115969],
        [18, 39.6281277813, -121.8927546903],
    ]
    df = pd.DataFrame(data, columns=["NodeID", "Latitude", "Longitude"])
    return df


def make_dummy_routes(vertiports: pd.DataFrame) -> pd.DataFrame:
    rand = random.Random(0)
    vertiports["nodeid"] = range(len(vertiports))
    routes = dict(
        rand.sample(vertiports["nodeid"].to_list(), 2) for _ in range(10)
    )

    return pd.DataFrame(
        [
            {
                "source nodeid": source,
                "target nodeid": target,
            }
            for source, target in routes.items()
        ]
    )


def test_decide_trips():
    base_dir = os.path.dirname(__file__)
    trips_file = os.path.join(base_dir, "assets", "trips_dummy.csv")

    trips = load_trips_from_csv(trips_file)
    vertiports = make_dummy_vertiports(trips)
    routes = make_dummy_routes(vertiports)
    params = get_default_params()

    vertiport_route_optimization(
        trips=trips,
        vertiports=vertiports,
        routes=routes,
        params=params
    )
