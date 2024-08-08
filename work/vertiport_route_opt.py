from pylib.decide_trips import (
    load_trips_from_csv,
    load_vertiports_from_csv
)
from pylib.decide_trips_testing import (
    get_default_params,
    make_dummy_routes,
)

from pylib.setup_vertiport_optimization import vertiport_route_optimization


params = get_default_params()
trips = load_trips_from_csv(params)
vertiports = load_vertiports_from_csv().head(10).sample(frac=1.0).reset_index(drop=True)
routes = make_dummy_routes(vertiports)

vertiport_route_optimization(
    trips=trips, vertiports=vertiports, routes=routes, params=params
)
