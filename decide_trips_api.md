
## Trip Selection Model

considered travel modalities:
- driving
- ground transit
- foot


### Inputs

1. trips: pandas.DataFrame
- origin longitude: float
- origin latitude: float
- destination longitude: float
- destination latitude: float
- number of travelers: int
- modality: str["car", "transit", "foot"]
- duration: h
- distance: km

2. vertiports: pandas.DataFrame (nodes)
- nodeid: int
- longitude: float
- latitude: float

3. routes: pd.DataFrame (edges)
- source nodeid: int
- target nodeid: int

4. params: dict
- driving marginal cost: float ($$/km) [0.4 $/km]
- driving speed: float (km/h) [default: 45 mph]
- ground transit base cost: float ($$)
- ground transit marginal cost: float ($$/km)
- ground transit boarding time: float (h)
- ground transit speed: float (km/h)
- foot speed: float (km/h) [default: 5km/h]
- evtol base cost: float ($$)
- evtol marginal cost: float ($$/km)
- evtol speed: float (km/h) [default: 240km/h]
- evtol boarding time: float (h) [default: 0.07h]
- evtol traveler capacity: int (travelers) [default: 4]
- evtol range: float (km) [default: 80km]
- fraction cost sensitive travelers: float [default: 0.5]

### Outputs

1. trips taken information: pandas.DataFrame
- origin longitude: float
- origin latitude: float
- destination longitude: float
- destination latitude: float
- number of travelers: int (travelers)
- trip cost: float ($$)
- trip duration: float (h)
- trip duration: float (h)
- distance driving: float (km)
- distance walking: float (km)
- distance ground transit: float (km)
- distance evtol: float (km)
