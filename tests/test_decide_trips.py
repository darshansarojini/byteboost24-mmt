import os
from pylib.decide_trips import (
    load_trips_from_csv,
    decide_trips,
)
from pylib.decide_trips_testing import (
    get_default_params,
    make_dummy_vertiports,
    make_dummy_routes,
)

def test_decide_trips():
    base_dir = os.path.dirname(__file__)
    trips_file = os.path.join(base_dir, "assets", "trips_dummy.csv")

    trips = load_trips_from_csv(trips_file)
    vertiports = make_dummy_vertiports(trips)
    routes = make_dummy_routes(vertiports)
    params = get_default_params()

    res = decide_trips(trips, vertiports, routes, params)
    print(res)
