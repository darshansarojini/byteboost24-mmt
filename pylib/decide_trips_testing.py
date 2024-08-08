import itertools as it
import typing

import pandas as pd


def get_default_params() -> typing.Dict[str, typing.Any]:
    return {
        "driving base cost": float(5.0),  # ($/km)
        "driving marginal cost": float(0.4),  # ($/km)
        "driving speed": float(70),  # (mph)
        "ground transit base cost": float(5.00),  # ($)
        "ground transit marginal cost": float(0.50),  # ($/km)
        "ground transit boarding time": float(0.05),  # (h)
        "ground transit speed": float(65),  # (km/h)
        "walking speed": float(5),  # (5km/h)
        "evtol base cost": float(0),  #  ($)
        "evtol marginal cost": float(0),  # ($/km)
        "evtol speed": float(240),  # (km/h)
        "evtol boarding time": float(0.07),  # (h)
        "evtol traveler capacity": int(4),  # (travelers)
        "evtol range": float(80),  # (km)
        "fraction cost sensitive travelers": float(0.5),  #
    }


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
    ]
    df = pd.DataFrame(data, columns=["nodeid", "latitude", "longitude"])
    return df


def make_dummy_routes(vertiports: pd.DataFrame) -> pd.DataFrame:
    vertiports["nodeid"] = range(len(vertiports))

    res = pd.DataFrame(
        [
            {
                "source nodeid": source,
                "target nodeid": target,
            }
            for source, target in it.product(vertiports["nodeid"], repeat=2)
        ]
    )
    assert len(res) == len(vertiports) ** 2
    return res
