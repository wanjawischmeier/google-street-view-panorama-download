import requests
from scipy.interpolate import interp1d
from requests.structures import CaseInsensitiveDict
from json import loads

class interp1d_ndo:
    """
    Initialize a 1-D linear interpolation class with support for n-D outputs.
    """
    def __init__(self, coords: list[tuple[float]]) -> None:
        values = list(zip(*coords))
        self.indicies = [i for i in range(len(coords))]
        self.tuple_size = len(values)
        self.interpolators = tuple([
            interp1d(self.indicies, values[i])
            for i in range(self.tuple_size)
        ])

    def __call__(self, index: float) -> tuple:
        return tuple([
            float(self.interpolators[i](index))
            for i in range(self.tuple_size)
        ])




class GeoapifyRouter:
    def __init__(self, api_key: str, mode: str="drive", base_url: str="https://api.geoapify.com/v1/routing") -> None:
        self.template = f"{base_url}?waypoints=WPOINTS&mode={mode}&apiKey={api_key}"

        self.headers = CaseInsensitiveDict()
        self.headers["Accept"] = "application/json"

    def __call__(self, waypoints: list[tuple[float]], subdivisions: int=10) -> list[tuple[float]]:
        waypoints_str = '|'.join([
            str(waypoint).replace(' ', '').strip('(').strip(')')
            for waypoint in waypoints
        ])
        url = self.template.replace("WPOINTS", waypoints_str)
        resp = loads(requests.get(url, headers=self.headers).__dict__["_content"])
        coords = resp["features"][0]["geometry"]["coordinates"][0]

        interp = interp1d_ndo(coords)
        subdivisions += 1
        interp_coords = [interp(i/subdivisions) for i in range((len(coords)-1)*subdivisions)]
        interp_coords.append(waypoints[len(waypoints)-1])

        return interp_coords