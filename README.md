# round-robin-pairs - round-robin tournament system

Implementations of Round-robin tournament algorithms, namely  berger tables and circle algorithm.

Based on [Round-robin tournament / Scheduling algorithms (wikipedia)](https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm).

Task: given list of players will return list of game rounds. Each game round
has list of two players pairs.

Implementation of:
 * `circle_tables()` -> circle system
 * `berger_tables()` -> berger tables

Functions have:
 * Input: list of players names
 * Output: list of rounds containing list of player pairs

Unit testing based on examples in [https://handbook.fide.com/chapter/C05Annex1](https://handbook.fide.com/chapter/C05Annex1).


## Usage / basic examples:

For Berger tables:

    from round_robin_pairs import berger_tables, circle_tables, round_robin_rounds_to_str_list 

    players = ["1", "2", "3", "4"]

    rounds = berger_tables(players)
    print(rounds)
        [[['1', '6'], ['2', '5'], ['3', '4']],
         [('6', '4'), ['5', '3'], ['1', '2']],
         [['2', '6'], ['3', '1'], ['4', '5']],
         [('6', '5'), ['1', '4'], ['2', '3']],
         [['3', '6'], ['4', '2'], ['5', '1']]]

    print("\n".join(round_robin_rounds_to_str_list(rounds)))
        Round 1: 1-6 2-5 3-4
        Round 2: 6-4 5-3 1-2
        Round 3: 2-6 3-1 4-5
        Round 4: 6-5 1-4 2-3
        Round 5: 3-6 4-2 5-1
    

Circle algorithm example:

    rounds = circle_tables(players)
    print(rounds)
        [[('1', '6'), ('2', '5'), ('3', '4')],
         [('1', '5'), ('6', '4'), ('2', '3')],
         [('1', '4'), ('5', '3'), ('6', '2')],
         [('1', '3'), ('4', '2'), ('5', '6')],
         [('1', '2'), ('3', '6'), ('4', '5')]]

    print("\n".join(round_robin_rounds_to_str_list(rounds)))
        Round 1: 1-6 2-5 3-4
        Round 2: 1-5 6-4 2-3
        Round 3: 1-4 5-3 6-2
        Round 4: 1-3 4-2 5-6
        Round 5: 1-2 3-6 4-5


## Unjust schedules and 'Modified Berger' solution

Ideally all players should play in all available schedules equally. 
For odd number of players this is satisfied for Berger case (circle haven't checked).

But, for even number of players algorithm is *unjust* to one player - for
Berger last, for circle first player, who is in all rounds in first schedule
(check previous examples, for Berger check player 6, for circle check player
1).

*Ideal* case does not exist, since there are N-1 rounds and N/2 schedules, so
in best case (*ideal*) every player should play every schedule 2 times, except,
for in one schedule it will play only once.
Example:

    nr. of players   (N)   = 14
    rounds           (N-1) = 13
    nr. of schedules (N/2) = 7
    best possible case:
        nr of schedules that will play twice (N/2 -1) = 6
        nr of schedules that will play once  (1)      = 1


Modification of Berger algorithm is provided which is available in 2/3 even-nr-of-players cases. 
It is not available for: 10, 16, 22, 28, ...

To get *ideal* i.e. one of best solutions (**modified Berger**), just pass
`ideal=True` parameter to `berger_tables` function.

    players = ["1", "2", "3", "4", "5", "6"]
    rounds = berger_tables(players, ideal=True)
    print("\n".join(round_robin_rounds_to_str_list(rounds)))
        Round 1: 3-4 2-5 1-6
        Round 2: 5-3 6-4 1-2
        Round 3: 2-6 3-1 4-5
        Round 4: 1-4 6-5 2-3
        Round 5: 5-1 4-2 3-6


## Round-robin tables

Ready to use tables:

 * [3 players ](tables/players-03.md)
 * [4 players (no ideal)](tables/players-04.md)
 * [5 players ](tables/players-05.md)
 * [6 players ](tables/players-06.md)
 * [7 players ](tables/players-07.md)
 * [8 players ](tables/players-08.md)
 * [9 players ](tables/players-09.md)
 * [10 players (no ideal)](tables/players-10.md)
 * [11 players](tables/players-11.md)
 * [12 players](tables/players-12.md)
 * [13 players](tables/players-13.md)
 * [14 players](tables/players-14.md)
 * [15 players](tables/players-15.md)
 * [16 players (no ideal)](tables/players-16.md)
 * [17 players](tables/players-17.md)
 * [18 players](tables/players-18.md)
 * [19 players](tables/players-19.md)
 * [20 players](tables/players-20.md)
 * [21 players](tables/players-21.md)
 * [22 players (no ideal)](tables/players-22.md)
 * [23 players](tables/players-23.md)
 * [24 players](tables/players-24.md)
 * [25 players](tables/players-25.md)


## NOTE: not yet on PyPI, sorry!
will be done ...

## TODO: implement improvement of the algorithm(s) to be more just:
work in progress in unit tests, check how just system is:
 * nearly equal times of schedule order 
 * nearly equal times of first in a pair

