import random
import time

import requests
import uvicorn
from fastapi import FastAPI

from exceptions.StatsNotFoundException import StatsNotFoundException
from models.StatsDto import PlayerStatsDto, PlayerStats
from models.StatsModel import StatsModel

app = FastAPI()


@app.post("/players/stats")
def get_player(stats_dto: PlayerStatsDto):
    player_stats = []
    response = {
        "players": player_stats
    }
    for player in stats_dto.players:
        points = fetch_player_stats(player)
        player_response = {
            "first_name": player.first_name,
            "last_name": player.last_name,
            "points": points
        }
        player_stats.append(player_response)
        # since we dont care about speed...
        # sleep for a random amount of time between 1-4s to avoid getting rate limited
        time.sleep(random.uniform(1, 4))
    return response


def fetch_player_stats(player_stats_dto: PlayerStats):
    base_url = 'https://www.pro-football-reference.com/players'
    formatted_name_only = format_name_only(player_stats_dto.first_name, player_stats_dto.last_name)
    counter = 0
    formatted_stats_url = f"{base_url}/{player_stats_dto.last_name[0].upper()}/{formatted_name_only}0{counter}.htm"
    try:
        points = get_player_stats(formatted_stats_url, player_stats_dto.week)
    except StatsNotFoundException as ex:
        print(f"Unable to get stats for {ex.message}")
        return None
    while points is None or points == 0:
        counter = counter + 1
        formatted_stats_url = f"{base_url}/{player_stats_dto.last_name[0].upper()}/{formatted_name_only}0{counter}.htm"
        try:
            points = get_player_stats(formatted_stats_url, player_stats_dto.week)
        except StatsNotFoundException as ex:
            print(f"Unable to get stats for {ex.message}")
            return None
    return points


def get_player_stats(url: str, week: int):
    response = requests.get(url)
    if response.status_code > 207:
        raise StatsNotFoundException(f"received non 200 error code while trying to fetch: {url}")
    else:
        temp = open('temp_file', 'w', encoding="utf-8")
        temp.write(response.text)
        temp.close()
        temp = open('temp_file', 'r', encoding="utf-8")
        lines = temp.readlines()

        stats_line = 'data-stat="week_num" >' + str(week) + '</td>'
        for line in lines:
            if stats_line in line:
                player_stats = StatsModel()
                player_stats.convert_stat_line(line)
                stats = player_stats.calculate_points()
                print(stats)
                return stats


def format_name_only(first_name, last_name):
    return f"{last_name[0:4]}{first_name[0:2]}"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
