from pydantic import BaseModel, StrictInt
from pydantic.types import StrictStr
import requests

def get_person(id:StrictInt):
    r = requests.get(f"https://statsapi.web.nhl.com/api/v1/people/{id}")
    return Person(**r.json()['people'][0])

class TimeZone(BaseModel):
    id: str
    offset: StrictInt
    tz: str


class Venue(BaseModel):
    name: str
    link: str
    city: str
    timeZone: TimeZone


class Divison(BaseModel):
    id: StrictInt
    name: str
    link: str


class Conference(BaseModel):
    id: StrictInt
    name: str
    link: str


class Franchise(BaseModel):
    franchiseId: StrictInt
    teamName: str
    link: str


class _Team(BaseModel):
    id: StrictInt
    name: str
    link: str
    venue: Venue
    abbreviation: str
    teamName: str
    locationName: str
    firstYearOfPlay: int
    division: Divison
    conference: Conference
    franchise: Franchise
    shortName: str
    officialSiteUrl: str
    franchiseId: StrictInt
    active: bool


class Team:
    def __init__(self, id: StrictInt):
        r = requests.get(f'https://statsapi.web.nhl.com/api/v1/teams/{id}')
        team = _Team(**r.json()['teams'][0])
        self.id = team.id
        self.name = team.name
        self.link = team.link
        self.venue = team.venue
        self.abbreviation = team.abbreviation
        self.teamName = team.teamName
        self.locationName= team.locationName
        self.firstYearOfPlay = team.firstYearOfPlay
        self.division= team.division
        self.conference = team.conference
        self.franchise = team.franchise
        self.shortName = team.shortName
        self.officialSiteUrl = team.officialSiteUrl
        self.franchiseId = team.franchiseId
        self.active = team.active


    @property
    def Roster(self):
        r = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams/{self.id}/roster")
        roster = r.json()["roster"]
        players = [get_person(p['person']['id']) for p in roster]

    @property
    def Division(self):
        r = requests.get(
            f"https://statsapi.web.nhl.com/api/v1/divisions/{self.division.id}"
        )
        return Divison(**r.json()["divisions"])

    @property
    def Conference(self):
        r = requests.get(
            f"https://statsapi.web.nhl.com/api/v1/conferences/{self.conference.id}"
        )
        return Conference(**r.json()["divisions"])

    @property
    def Schedule(self):
        r = requests.get(
            f"https://statsapi.web.nhl.com/api/v1/schedule?teamId={self.id}"
        )
        return r.json()["dates"]["games"]


class Position(BaseModel):
    code: StrictStr
    name: StrictStr
    type: StrictStr
    abbreviation: StrictStr


class Person:
    id: StrictInt
    fullName: StrictStr
    link: StrictStr
    firstName: StrictStr
    lastName: StrictStr
    primaryNumber: int
    birthDate: StrictStr
    currentAge: StrictInt
    birthCity: StrictStr
    birthStateProvince: StrictStr
    birthCountry: StrictStr
    nationality: StrictStr
    height: StrictStr
    weight: StrictInt
    active: bool
    alternateCaptain: bool
    captain: bool
    rookie: bool
    shootsCatches: StrictStr
    rosterStatus: bool
    primaryPosition: Position

    # def Team(self):