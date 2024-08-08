import random
import typing

import pandas as pd
import numpy as np


def get_default_params() -> typing.Dict[str, typing.Any]:
    return {
        "driving base cost": float(5.0),  # ($/km)
        "driving marginal cost": float(0.4),  # ($/km)
        "driving speed": float(70),  # (mph)
        "ground transit base cost": float(5.00),  # ($)
        "ground transit marginal cost": float(0.50),  # ($/km)
        "ground transit boarding time": float(0.05),  # (h)
        "ground transit speed": float(65),  # (km/h)
        "foot speed": float(5),  # (5km/h)
        "evtol base cost": float(0),  #  ($)
        "evtol marginal cost": float(0),  # ($/km)
        "evtol speed": float(240),  # (km/h)
        "evtol boarding time": float(0.07),  # (h)
        "evtol traveler capacity": int(4),  # (travelers)
        "evtol range": float(80),  # (km)
        "fraction cost sensitive travelers": float(0.5),  #
    }


def make_dummy_vertiports(trips: pd.DataFrame) -> pd.DataFrame:
    file_path = "make_dummy_nodes.csv"
    df = pd.read_csv(file_path)
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
