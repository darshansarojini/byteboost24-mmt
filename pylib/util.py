from geopy.distance import geodesic


def geodesic_kilometers(*args) -> float:
    return geodesic(*args).kilometers
