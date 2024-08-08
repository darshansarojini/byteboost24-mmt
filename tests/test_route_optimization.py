import random

import pandas as pd

from pylib.decide_trips import (
    load_trips_from_csv,
)
from pylib.decide_trips_testing import (
    get_default_params,
    make_dummy_vertiports,
    make_dummy_routes,
)

from pylib.setup_vertiport_optimization import vertiport_route_optimization


def test_decide_trips():
    params = get_default_params()
    trips = load_trips_from_csv(params)
    vertiports = make_dummy_vertiports(trips)
    routes = make_dummy_routes(vertiports)

    vertiport_route_optimization(
        trips=trips, vertiports=vertiports, routes=routes, params=params
    )
