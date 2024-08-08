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
    params = get_default_params()
    trips = load_trips_from_csv(params)
    vertiports = make_dummy_vertiports(trips)
    routes = make_dummy_routes(vertiports)
    assert set(routes["source nodeid"]) <= set(vertiports["nodeid"])
    assert set(routes["target nodeid"]) <= set(vertiports["nodeid"])

    res = decide_trips(trips, vertiports, routes, params)
    print(res)
