""" 
Round-robin tournament system
------------------------------
based on 
    https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm

given list of players will return list of rounds. Each round has list of two
players pairs.

Implementation of:
    - circle_tables() -> circle system
    - berger_tables() -> berger tables

Functions have:

    Input: 
        - list of players names
    Output 
        - list of rounds containing list of player pairs

Unit testing based on examples in:
    https://handbook.fide.com/chapter/C05Annex1

"""

from typing import List, Tuple
from pprint import pprint
from collections import OrderedDict

PlayerName = str
RoundRobnRounds = List[List[Tuple[PlayerName, PlayerName]]]

FMT_WIDTH = 1

def pp_players_row(players_row):
    return " ".join([f"{pl:>{FMT_WIDTH}}" for pl in players_row])

def pp_player_pairs_row(player_pairs_row):
    return " ".join([f"{pl1:>{FMT_WIDTH}}-{pl2:>{FMT_WIDTH}}" for pl1, pl2 in player_pairs_row])

# https://en.wikipedia.org/wiki/Round-robin_tournament
def berger_tables(players: List[PlayerName], verbose:bool = False) -> RoundRobnRounds:
    n = len(players)
    if verbose:
        print(players)
    assert n > 0 
    if n % 2 == 1:
        players.append("BYE")
        n = len(players)
    n_half = n // 2

    fixed = players[-1]
    wheel = list(reversed(players[:-1]))

    rounds = []
    for round_nr in range(n-1):
        even_round = (round_nr % 2 == 0)
        pairs = []
        pair = (fixed, wheel[-1])
        if even_round:
            pair = list(reversed(pair))
        pairs.append(pair)

        even_round = True
        for idx in range(n_half-1):
            pair = (wheel[idx], wheel[-(idx+1+1)])
            if even_round:
                pair = list(reversed(pair))
            pairs.append(pair)

        if verbose:
            print(f"{round_nr+1:>2}. {pp_player_pairs_row(pairs)}")

        rounds.append(pairs)

        wheel = wheel[n_half-1:] + wheel[:n_half-1]
        # if round_nr > 4: break

    return rounds


def circle_tables(players: List[PlayerName], verbose:bool = False) -> RoundRobnRounds:
    n = len(players)
    assert n > 0 
    if n % 2 == 1:
        players.append("BYE")
        n = len(players)
    
    half_n = n // 2
    players_round = players[:]
    players_up   = players_round[:half_n]
    players_down = list(reversed(players_round[half_n:]))
    output = []
    
    for game_round in range(1, (n +1)-1):
        pairs = list(zip(players_up, players_down))
        output.append(pairs)
        if verbose:
            print(game_round, 
                    "\n", " ".join([f"{pl:>2}" for pl in players_up]), 
                    "\n", " ".join([f"{pl:>2}" for pl in players_down])) # , "\n", pairs)
        last_up    = players_up.pop(-1)
        first_down = players_down.pop(0)
        players_up.insert(0 + 1, first_down)
        players_down.append(last_up)


    return output


def round_robin_rounds_to_str_list(round_robin_rounds: RoundRobnRounds) -> List[str]:
    output = []
    for rd, game_round in enumerate(round_robin_rounds, 1):
        output.append("Round {}: {}".format(rd, " ".join([f"{p1}-{p2}" for p1, p2 in game_round])))
    return output


if __name__=="__main__":
    pass # TODO: CLI

