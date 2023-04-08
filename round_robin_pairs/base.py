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

from typing import List, Tuple, Dict
from pprint import pprint
from collections import OrderedDict
from copy import deepcopy

PlayerName = str
RoundRobinRow = List[Tuple[PlayerName, PlayerName]]
RoundRobnRounds = List[RoundRobinRow]
JustScore = float

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


def get_jsut_score(players: List[PlayerName], 
                   nr_schedules: int, 
                   round_robin_rounds: RoundRobnRounds, 
                   verbose:bool = False) -> Tuple[Dict[PlayerName, JustScore], JustScore, Dict, Dict]:

    schedule_dict = {pl : {sch_nr: 0 for sch_nr in range(1, nr_schedules+1)} for pl in players}
    first_dict = {pl : 0 for pl in players}

    for round_pairs in round_robin_rounds:
        for sch_nr, (pl1, pl2) in enumerate(round_pairs, 1):
            schedule_dict[pl1][sch_nr] += 1
            schedule_dict[pl2][sch_nr] += 1
            first_dict[pl1] +=1


    score_by_players = {pl : 0 for pl in players}

    for pl, sch_cnt_dict in schedule_dict.items():
        for sch_nr, sch_cnt in sch_cnt_dict.items():
            # only preffered values is 1 
            # each player plays in a schedule once 
            add = abs(sch_cnt -1) 
            # if sch_cnt==0:
            score_by_players[pl] += add
            # a) ako ima 1 za termin -> 0
            # b) ako ima 2 za termin -> +1
            # c) ako ima 0 za termin -> +1
            # d) ako ima 3+ za termin -> +1 * (N-1), npr. 3 ima (3-1) = +2

    score = sum(score_by_players.values())
    if verbose:
        # print("== Schedule dict - players by schedule -> count:")
        # pprint(schedule_dict)

        # RT: print("== First dict - for each player count when is first:")
        # RT: pprint(first_dict)

        # print(f"== Score by players:")
        # pprint(score_by_players)

        print(f"== Total score: {score}")


    return score_by_players, score, schedule_dict, first_dict


def print_unjust_schedules(schedule_dict: Dict) -> int:
    sch_nearly_equal = (1, 2)
    cnt = 0
    for pl, sch_cnt_dict in schedule_dict.items():
        for sch_nr, sch_cnt in sch_cnt_dict.items():
            if sch_cnt not in sch_nearly_equal:
                cnt +=1
                print(f"Schedule unjust: pl={pl:<4} -> sch={sch_nr}: count={sch_cnt}")
    return cnt


def swap(round_pairs: RoundRobinRow, idxs_to_swap: Tuple[int, int], verbose:bool = False):
    " swap pairs places based on pair indexes in the row "
    idx_1, idx_2 = idxs_to_swap
    if idx_1!=idx_2:
        pair_1, pair_2 = round_pairs[idx_1], round_pairs[idx_2]
        round_pairs[idx_1], round_pairs[idx_2] = pair_2, pair_1
    # if verbose:
    #     print("swap result", idxs_to_swap, round_pairs)


def equalize_schedules_in_rounds(round_robin_rounds: RoundRobnRounds, verbose:bool = False) -> Tuple[RoundRobnRounds, JustScore, JustScore]:
    " will try to accomplish that each player have nearly equal nr of schedules - to be as just as possible - returns score before and after " 
    # for pairs_list in rounds: 
    # check how just system is:
    #   - nearly equal times of schedule order 
    #   - nearly equal times of first in a pair

    # if verbose:
    #     print("=== Rounds - before:")
    #     pprint(round_robin_rounds)

    players: List[PlayerName] = []
    schedules: List[int] = []
    for round_pairs in round_robin_rounds:
        for sch_nr, (pl1, pl2) in enumerate(round_pairs, 1):
            if sch_nr not in schedules:
                schedules.append(sch_nr)
            if pl1 not in players:
                players.append(pl1)
            if pl2 not in players:
                players.append(pl2)

    nr_of_players = len(players)
    nr_schedules = nr_of_players // 2
    if nr_schedules != len(schedules):
        raise Exception(f"Expected number of schedules {nr_schedules}, bog {len(schedules)}")

    score_by_players, score_before, schedule_dict, first_dict = \
            get_jsut_score(players=players, 
                           nr_schedules=nr_schedules, 
                           round_robin_rounds=round_robin_rounds, 
                           verbose=verbose)
    if verbose:
        print_unjust_schedules(schedule_dict)

    round_robin_rounds_new = deepcopy(round_robin_rounds)
    nr_rounds = len(round_robin_rounds)
    for rnr, round_pairs in enumerate(round_robin_rounds, 0):
        round_robin_rounds_new 
        # 1. the most simple method:
        #    berger and cricle put fixed player in first schedule
        #    this method swaps first pair based on round number
        idxs_to_swap = [0, rnr % nr_schedules]
        swap(round_pairs, idxs_to_swap, verbose=verbose)

    # if verbose:
    #     first_nearly_equal = ((nr_of_players-1) // 2, (nr_of_players-1) // 2 +1)
    #     for pl, first_cnt in first_dict.items():
    #         if first_cnt not in first_nearly_equal:
    #             print(f"First unjust: pl={pl} -> first count={first_cnt}")

    _, score_after, schedule_dict, _ = \
            get_jsut_score(players=players, 
                           nr_schedules=nr_schedules, 
                           round_robin_rounds=round_robin_rounds, 
                           verbose=verbose)
    if verbose:
        print("=== Schedule dict - after:")
        print_unjust_schedules(schedule_dict)
        # print("=== Rounds - after:")
        # pprint(round_robin_rounds)

        print(f"Score benefit: {score_before} => {score_after}, gain (- is good): {score_after - score_before}")


    return round_robin_rounds_new, score_before, score_after



def round_robin_rounds_to_str_list(round_robin_rounds: RoundRobnRounds) -> List[str]:
    output = []
    for rd, game_round in enumerate(round_robin_rounds, 1):
        output.append("Round {}: {}".format(rd, " ".join([f"{p1}-{p2}" for p1, p2 in game_round])))
    return output


if __name__=="__main__":
    pass # TODO: CLI

