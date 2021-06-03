from utils import _get_teams_raw
from api.teams import Team


class Client:
    def teams():
        teams_raw = _get_teams_raw()
        teams = [Team(t) for t in teams_raw]
