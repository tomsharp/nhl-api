import requests
from enum import Enum
from datetime import date, timedelta, datetime
from pytz import timezone
from typing import Optional, Tuple


class Teams(str, Enum):
    PHL = "Philadelphia Flyers"
    # TODO - finish
    # fixme - come up with better enum structure


def _localize_datetime(utc_datetime):
    est_datetime = utc_datetime + timedelta(hours=-5)
    return est_datetime

def _get_teams_raw():
    r = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
    teams = r.json()["teams"]
    return teams


def _get_team_info_raw(full_teamname):
    teams = _get_teams_raw()
    result = [t for t in teams if t.get("name") == full_teamname]
    if len(result) == 0:
        raise ValueError("No such teamname")
    return result[0]

def _get_schedule_raw(
    team_id: int,
    date_range: Tuple[date, date] = (date.today(), date.today()),
    broadcasts: bool = True,
):
    """
    team_id:
        id of the team
    date_range:
        Tuple representing (start_date, end_date) of a date range (inclusive). If start-date and end_date are the same, returns game (if any) for that specific date
    broadcasts:
        Whether to show the broadcasts of each game
    """
    request_str = f"https://statsapi.web.nhl.com/api/v1/schedule?teamId={team_id}"
    request_str = request_str + f"&startDate={date_range[0].strftime('%Y-%m-%d')}"
    request_str = request_str + f"&endDate={date_range[1].strftime('%Y-%m-%d')}"
    if broadcasts == True:
        request_str = request_str + "&expand=schedule.broadcasts"
    r = requests.get(request_str)
    return r.json()

def _last_game(team_id: int):
    r = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams/{team_id}?expand=team.schedule.previous")
    return r.json()


def _next_game(team_id: int, broadcasts:bool=True):
    request_str = f"https://statsapi.web.nhl.com/api/v1/teams/{team_id}?expand=team.schedule.next"
    if broadcasts == True:
        request_str = request_str + "&expand=schedule.broadcasts"
    r = requests.get(request_str)
    return r.json()


def _team_id(full_teamname):
    """Return the team_id for the specified team."""
    team_info = _get_team_info_raw(full_teamname)
    return team_info.get("id")


def _upcoming_games(team_id: int, days_out:int=1, broadcasts:bool=True):
    """Get all upcoming game for a particular team in the timeframe provided."""
    schedule = _get_schedule_raw(team_id, (date.today(), date.today()+timedelta(days=days_out)), broadcasts)
    return schedule

def next_game(team_id: int):
    next_game = _next_game(team_id, broadcasts=True)
    date_time = datetime.strptime(next_game['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['gameDate'], "%Y-%m-%dT%H:%M:%SZ")
    date_time = _localize_datetime(date_time).strftime("%Y-%m-%d %H:%M:%S")
    date = date_time.split(' ')[0]
    time = date_time.split(' ')[1]
    broadcasts = next_game['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['broadcasts']
    home_team = next_game['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['team']['name']
    away_team = next_game['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['team']['name']
    home_record = next_game['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['leagueRecord']
    away_record = next_game['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['leagueRecord']

    # FIXME - grabbing for later
    radio_broadcasts = next_game['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['radioBroadcasts']
    content = next_game['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['content']

    return {
        'date': date,
        'time': time, 
        'broadcasts': broadcasts,
        'home_team': home_team,
        'home_record': home_record,
        'away_team': away_team,
        'away_record': away_record,
    }
   

def previous_game_results(team_id: int):
    """Get score and stats from the most recent game for a particular team."""
    last_game = _last_game(team_id)
    date = last_game['teams'][0]['previousGameSchedule']['dates'][0]['date']
    last_game = last_game['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]
    print(last_game.keys())
    away_team = last_game['teams']['away']['team']['name']
    home_team = last_game['teams']['home']['team']['name']
    away_score = last_game['teams']['away']['score']
    home_score = last_game['teams']['home']['score']
    return {'date':date, 'home_team': home_team, 'home_score':home_score, 'away_team':away_team, 'away_score':away_score}

def team_rankings():
    """Get regularSeasonStatRankings for a particular team."""
    raise NotImplementedError


def live_game():
    """link : /api/v1/game/2020020266/feed/live,"""
    return None