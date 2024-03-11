# pylint: disable=E0401
"""
This module contains a few basic functions for interacting with the configuration files.
"""

import os
import json
import fastf1


def get_exclude_dir() -> str:
    """
    Gets the path to the directory containing the exclude files

    :return: The path to the directory containing the exclude files
    """
    # find the filename in the config.json
    config_json_path = os.path.join(os.path.dirname(__file__), 'config.json')

    # open json in a with statement to ensure the file is closed
    exclude_name = "excludes.txt"  # default value
    with open(config_json_path, encoding="utf-8") as config_file:
        config_json = json.load(config_file)
        exclude_name = config_json['path_to_excludes']

    exclude_dir = os.path.join(os.path.dirname(__file__), exclude_name)
    return exclude_dir


def get_excludes() -> list[tuple[int, str]]:
    """
    Gets a list of Races that should be excluded

    :return: The races that should be excluded as a list of tuples (Year,Race)
    """

    # get the path to the config file
    config_path = get_exclude_dir()

    results = []
    with open(config_path, 'r', encoding="utf-8") as file:
        # read the file and split it into lines
        lines = file.read().splitlines()
        for line in lines:
            # clean up line
            line = line.strip()
            # split the line into year and race
            season, race = line.split(':')
            season = int(season)
            results.append((season, race))

    return results


def get_train_races() -> list[tuple[int, str]]:
    """
    This returns the list of the races that should be used to train the model

    :return: List of races to train the model on. items in list are format: tuple[season,race]
    """

    # set up fastf1 instance
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'cache'))

    fastf1.Cache.enable_cache(path)

    start_year = 2022
    end_year = 2023
    excludes = get_excludes()

    races = []

    config_json_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_json_path, encoding="utf-8") as config_file:
        config_json = json.load(config_file)
        start_year = config_json['season_train_start']
        end_year = config_json['season_train_end']

    for year in range(start_year, end_year + 1):

        # get all races in this year
        year_sched = fastf1.get_event_schedule(year)
        year_sched = year_sched[year_sched['EventFormat'] != 'testing']
        year_races = year_sched['EventName'].tolist()
        for race in year_races:
            if (year, race) not in excludes:
                races.append((year, race))

    return races
