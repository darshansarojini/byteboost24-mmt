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
    return pd.DataFrame()


def make_dummy_routes(vertiports: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame()
