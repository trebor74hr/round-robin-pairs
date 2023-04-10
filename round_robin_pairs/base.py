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

from typing import List, Tuple, Dict, Optional
from pprint import pprint
from collections import OrderedDict
from copy import deepcopy
import enum
import random
from dataclasses import dataclass, field

try:
    # optional
    import colorama 
except ImportError:
    colorama = None

PlayerName = str
RoundRobinRow = List[Tuple[PlayerName, PlayerName]]
RoundRobnRounds = List[RoundRobinRow]
JustScore = float

FMT_WIDTH = 1

def pp_players_row(players_row, fmt_width: int = FMT_WIDTH):
    return " ".join([f"{pl:>{fmt_width}}" for pl in players_row])

def get_fmt_pair_same_width(fmt_width: Optional[int] = None):
    if not fmt_width:
        fmt_width = FMT_WIDTH
    return f"{{:>{fmt_width}}}-{{:>{fmt_width}}}" 

def get_fmt_pl_same_width(fmt_width: Optional[int] = None):
    if not fmt_width:
        fmt_width = FMT_WIDTH
    return f"{{:>{fmt_width}}}"

def pp_player_pairs_row(player_pairs_row: RoundRobinRow, fmt_width: int = FMT_WIDTH) -> str:
    fmt_same_width = get_fmt_pair_same_width(fmt_width)
    return " ".join([fmt_same_width.format(pl1, pl2) for pl1, pl2 in player_pairs_row])

def round_robin_rounds_to_str_list(round_robin_rounds: RoundRobnRounds, fmt_width:int = FMT_WIDTH, mark_players:Optional[PlayerName]=None) -> List[str]:
    fmt_same_width = get_fmt_pair_same_width(fmt_width)
    output = []
    fmt_rd = f"{{:>{fmt_width}}}"
    sep = " " if fmt_width== 1 else "  "
    if fmt_width>1:
        pair_len = len(fmt_same_width.format("x", "y"))
        game_round0 = round_robin_rounds[0]
        header ="Round {}  {}".format(fmt_rd.format(""), sep.join([f"{nr:>{pair_len}}" for nr, _ in enumerate(game_round0, 1)])) 
        output.append(header)
        output.append("-" * len(header))

    if colorama and mark_players:
        all_colors = [
                    [colorama.Back.BLUE], 
                    [colorama.Fore.BLACK, colorama.Back.YELLOW], 
                    [colorama.Fore.MAGENTA], 
                    [colorama.Fore.GREEN], 
                    [colorama.Fore.BLUE], 
                    [colorama.Fore.RED],
                    ]
        # 'LIGHTBLACK_EX', 'LIGHTBLUE_EX', 'LIGHTCYAN_EX', 'LIGHTGREEN_EX', 'LIGHTMAGENTA_EX', 'LIGHTRED_EX', 
        # 'LIGHTWHITE_EX', 'LIGHTYELLOW_EX', 'RED', 'RESET', 'WHITE', 
        assert len(mark_players) <= len(all_colors)
        player_colors = dict([(pl, all_colors[idx]) for idx, pl in enumerate(mark_players)])
    else:
        player_colors = {}


    fmt_pl = get_fmt_pl_same_width(fmt_width)

    for rd, game_round in enumerate(round_robin_rounds, 1):
        pair_out = []
        for p1, p2 in game_round:

            p1_str, p2_str = fmt_pl.format(p1), fmt_pl.format(p2)
            if colorama:
                if p1 in player_colors:
                    p1_str = "".join(player_colors[p1]) + p1_str + colorama.Style.RESET_ALL
                if p2 in player_colors:
                    p2_str = "".join(player_colors[p2]) + p2_str + colorama.Style.RESET_ALL
            # fmt_same_width.format(p1, p2)
            pair_out.append(f"{p1_str}-{p2_str}")
        output.append("Round {}: {}".format(fmt_rd.format(rd), sep.join(pair_out)))

    if fmt_width>1:
        output.append("-" * len(header))
    return output

def pprint_player_pairs_row(round_robin_rounds: RoundRobnRounds, fmt_width:int = FMT_WIDTH, mark_players:Optional[PlayerName]=None) -> None:
    print("\n".join(round_robin_rounds_to_str_list(round_robin_rounds, fmt_width=fmt_width, mark_players=mark_players)))

def pprint_schedules(schedule_dict: Dict, players: List, nr_schedules:int):
    schedules = range(1, nr_schedules+1)
    sch_header = [f"{sch:>2} " for sch in schedules]
    print(f"Pl. {' '.join(sch_header)}")
    for pl in players:
        sch_dict = schedule_dict[pl]
        out = []
        for sch in schedules:
            cnt = sch_dict[sch]
            mark = " "
            if cnt==2:
                cnt = "-"
            elif cnt not in (1, 2):
                mark = "*"
            out.append("{:>2}{}".format(cnt, mark))
        print(f"{pl:<2}. {' '.join(out)}")


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


def get_just_score(players: List[PlayerName], 
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
            if True:
                if sch_cnt==2:
                    add = 0
                elif sch_cnt<2:
                    # 1 -> 1, 0->2
                    add = (2 - sch_cnt)
                else:
                    # 3 -> 2, 4 -> 3, ...
                    add = (sch_cnt - 2) + 1
            else:
                add = abs(sch_cnt -1) 
            score_by_players[pl] += add
            # new:
            #   a) ako ima 1 za termin -> 1
            #   b) ako ima 2 za termin -> 0
            #   c) ako ima 0 za termin -> -2
            #   d) ako ima 3+ za termin -> +1 * (N-2), npr. 3 ima (3-1) = +2
            # old:
            #   a) ako ima 1 za termin -> 0
            #   b) ako ima 2 za termin -> +1
            #   c) ako ima 0 za termin -> +1
            #   d) ako ima 3+ za termin -> +1 * (N-1), npr. 3 ima (3-1) = +2

    score = sum(score_by_players.values())
    if verbose:
        print("== Schedule dict - players by schedule -> count:")
        pprint_schedules(schedule_dict, players, nr_schedules)

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


class EqualizeType(str, enum.Enum):
    # L = left
    # R = right
    # 2 = To
    DIAG_L2R = "DIAG_L2R"
    DIAG_R2L = "DIAG_R2L"
    DIAG_R2L2R = "DIAG_R2L2R"
    DIAG_L2R2L = "DIAG_L2R2L"
    BRUTE_FORCE = "BRUTE_FORCE"
    CROSS = "CROSS"

    @classmethod
    def values(cls):
        return [k for k,v in EqualizeType.__members__.items()]


def equalize_schedules_in_rounds(
        round_robin_rounds: RoundRobnRounds, 
        eq_type: EqualizeType, 
        offset_x: int = 0,
        players: Optional[List[PlayerName]] = None, 
        stats_only_rounds: Optional[RoundRobnRounds] = None,
        verbose:bool = False) -> Tuple[RoundRobnRounds, JustScore, JustScore]:
    " will try to accomplish that each player have nearly equal nr of schedules - to be as just as possible - returns score before and after " 
    # players if provided - only for correct order
    #
    # for pairs_list in rounds: 
    # check how just system is:
    #   - nearly equal times of schedule order 
    #   - nearly equal times of first in a pair

    players_detect: List[PlayerName] = []
    schedules: List[int] = []
    for round_pairs in round_robin_rounds:
        for sch_nr, (pl1, pl2) in enumerate(round_pairs, 1):
            if sch_nr not in schedules:  # TODO: silly, this is fixed
                schedules.append(sch_nr)
            if pl1 not in players_detect:
                players_detect.append(pl1)
            if pl2 not in players_detect:
                players_detect.append(pl2)

    if players:
        set_d, set_p = set(players_detect), set(players)
        if set_d!=set_p:
            raise Exception(f"From schedules detected players which differs from given players: {set_d - set_p} / {set_p - set_d}")
    else:
        players = players_detect

    mark_players=[players[-1], players[0], players[1]]
    if verbose or stats_only_rounds:
        print("=== Rounds - before:")
        pprint_player_pairs_row(round_robin_rounds, fmt_width=2, mark_players=mark_players)


    nr_of_players = len(players)
    # TODO: consider: nr_schedules = nr_of_players // 2 + nr_of_players % 2
    nr_schedules = nr_of_players // 2
    if nr_schedules != len(schedules):
        raise Exception(f"Expected number of schedules {nr_schedules}, got {len(schedules)}")

    score_by_players, score_before, schedule_dict, first_dict = \
            get_just_score(players=players, 
                           nr_schedules=nr_schedules, 
                           round_robin_rounds=round_robin_rounds, 
                           verbose=verbose or stats_only_rounds)
    # if verbose:
    #     print_unjust_schedules(schedule_dict)

    if stats_only_rounds:
        round_robin_rounds = stats_only_rounds
    else:
        round_robin_rounds = deepcopy(round_robin_rounds)

        nr_rounds = len(round_robin_rounds)
        idx_fixed = 0

        if eq_type==EqualizeType.BRUTE_FORCE:
            random.seed()
            random_swaps = []
            for rnr, round_pairs in enumerate(round_robin_rounds, 0):
                # 1. the most simple method:
                #    berger and cricle put fixed player in first schedule
                #    this method swaps first pair based on round number
                l2r = None
                if not random_swaps:
                    random_swaps = list(range(nr_schedules))
                    random.shuffle(random_swaps)
                    # print("random", rnr, random_swaps)
                idx_other = random_swaps.pop(0)
                # print("random", idx_other)
                idxs_to_swap = [idx_fixed, idx_other]
                # if verbose: print(rnr, div, idxs_to_swap)
                swap(round_pairs, idxs_to_swap, verbose=verbose)
        else:
            for rnr, round_pairs in enumerate(round_robin_rounds, 0):
                if eq_type==EqualizeType.CROSS:
                    # div = rnr // nr_schedules
                    if rnr % 2 ==0:
                        l2r = True
                        nr = rnr // 2
                        idx_other = nr % nr_schedules
                    else:
                        l2r = False
                        idx_other = -1 * ((nr+1) % nr_schedules)
                    # print(rnr, idx_other)
                elif eq_type==EqualizeType.DIAG_L2R:
                    l2r = True
                    idx_other = rnr % nr_schedules
                    # print(rnr, idx_other)
                elif eq_type==EqualizeType.DIAG_R2L:
                    l2r = False
                    idx_other = -1 * ((rnr+1) % nr_schedules)
                elif eq_type==EqualizeType.DIAG_L2R2L:
                    div = rnr // nr_schedules
                    if div % 2 == 0:
                        l2r = True
                        idx_other = rnr % nr_schedules
                    else:
                        l2r = False
                        idx_other = -1 * ((rnr+2) % nr_schedules)
                    # print(idx_other)
                elif eq_type==EqualizeType.DIAG_R2L2R:
                    div = rnr // nr_schedules
                    if div % 2 == 0:
                        l2r = False
                        idx_other = -1 * ((rnr+1) % nr_schedules)
                    else:
                        l2r = True
                        idx_other = ((rnr+1) % nr_schedules)
                else:
                    raise Exception(f"Unknown for {eq_type}. Select one of: {', '.join(EqualizeType.values())}")

                if offset_x:
                    idx_other = (idx_other + offset_x) 
                    if abs(idx_other) >= nr_schedules:
                        idx_other = ((idx_other + 0) % nr_schedules) * +1

                idxs_to_swap = [idx_fixed, idx_other]
                # if verbose: print(rnr, div, idxs_to_swap)
                # print("---", rnr, idxs_to_swap)
                swap(round_pairs, idxs_to_swap, verbose=verbose)

    # if verbose:
    #     first_nearly_equal = ((nr_of_players-1) // 2, (nr_of_players-1) // 2 +1)
    #     for pl, first_cnt in first_dict.items():
    #         if first_cnt not in first_nearly_equal:
    #             print(f"First unjust: pl={pl} -> first count={first_cnt}")

    _, score_after, schedule_dict, _ = \
            get_just_score(players=players, 
                           nr_schedules=nr_schedules, 
                           round_robin_rounds=round_robin_rounds, 
                           verbose=verbose or stats_only_rounds)
    if verbose or stats_only_rounds:
        # print("=== Schedule dict - after:")
        # print_unjust_schedules(schedule_dict)
        print("=== Rounds - after:")
        pprint_player_pairs_row(round_robin_rounds, fmt_width=2, mark_players=mark_players)

        # best score
        # od 13 rundi, svaku igra 2x, osim jedne. svaki igrač onda ima po 1. za 14 igrača -> 14 x 1
        score_ideal = len(players) * 1
        print(f"=== Score benefit: {score_before} => {score_after}, gain (- is good): {score_after - score_before}")
        print(f"    Score to ideal solution => {score_ideal} (smaller the better, 0 is IDEAL): {score_after - score_ideal}")


    return round_robin_rounds, score_before, score_after


@dataclass
class BestResult:
    players : List[PlayerName] = field(repr=False)
    # nr_schedules : int = field(repr=False)
    has_ideal: bool = field(init=False) 
    best_score: Optional[JustScore] = None
    best_eq_type: Optional[EqualizeType] = None
    best_offset_x: Optional[int] = None
    score_before: Optional[JustScore] = None
    best_rounds: Optional[RoundRobnRounds] = field(repr=False, default=None)
    score_ideal: JustScore = field(init=False, repr=True)

    def __post_init__(self):
        self.has_ideal = has_ideal(len(self.players))
        self.score_ideal = len(self.players) * 1

    def is_ideal(self):
        return self.best_score == self.score_ideal


def _find_best_iteration(
    round_robin_rounds: RoundRobnRounds, 
    eq_type: EqualizeType,
    best_result: BestResult, # inout
    offset_x: int = 0,
    players: Optional[List[PlayerName]] = None, 
    verbose:bool = False) -> bool:

    rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type=eq_type, offset_x=offset_x, players=players, verbose=False)
    if best_result.score_before is None:
        best_result.score_before = score_before
    else:
        assert best_result.score_before == score_before

    if best_result.best_score is None or score_after < best_result.best_score:
        best_result.best_score = score_after 
        best_result.best_eq_type = eq_type
        best_result.best_offset_x = offset_x
        best_result.best_rounds = rounds_new
        selected = True
    else:
        selected = False

    if verbose and selected:
        print(f"-- SELECTED: eq={eq_type:<10} + {offset_x:>2}, before={score_before:>3}, after={score_after:>3}, gain={score_after-score_before:>3}  {'*' if selected else ' '}")

    return selected

def has_ideal(nr_of_players:int) -> bool:
    return (nr_of_players - 4) % 6 != 0

def find_best_equalize_solution(
        round_robin_rounds: RoundRobnRounds, 
        players: List[PlayerName],
        brute_force_factor: Optional[int] = 1000,
        verbose:bool = False) -> BestResult:

    nr_of_players = len(players)

    nr_schedules = len(round_robin_rounds[0])

    best_result = BestResult(players=players)
    if best_result.has_ideal:
        _find_best_iteration(
            round_robin_rounds= round_robin_rounds,
            eq_type = "DIAG_R2L2R",
            offset_x = 0,
            best_result = best_result,
            players = players,
            verbose = verbose,
            )
    else:
        for eq_type in ("DIAG_L2R", "DIAG_R2L", "DIAG_L2R2L", "DIAG_R2L2R", "CROSS"):
            # for offset_x in range(0, nr_schedules):
            for offset_x in range(0, nr_schedules):
                _find_best_iteration(
                    round_robin_rounds= round_robin_rounds,
                    eq_type = eq_type,
                    offset_x = offset_x,
                    best_result = best_result,
                    players = players,
                    verbose = verbose,
                    )

        if brute_force_factor:
            for random_nr in range(0, nr_schedules * brute_force_factor):
                selected = _find_best_iteration(
                    round_robin_rounds= round_robin_rounds,
                    eq_type = EqualizeType.BRUTE_FORCE,
                    best_result = best_result,
                    offset_x = 0,
                    players = players,
                    verbose = verbose,
                    )

    if verbose:
        # just to show verbose data
        equalize_schedules_in_rounds(round_robin_rounds, stats_only_rounds=best_result.best_rounds, 
                                     eq_type=best_result.best_eq_type, offset_x=best_result.best_offset_x, players=players)

        print("=" * 80)
        print(f"{('__IDEAL__' if best_result.is_ideal() else 'ACCEPT') if best_result.score_before > best_result.best_score else 'TO-REJECT'} {best_result}")
        print("=" * 80)

    return best_result



if __name__=="__main__":
    pass # TODO: CLI

