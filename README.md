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

Example:

Berger tables:

    from round_robin_pairs import berger_tables, circle_tables, round_robin_rounds_to_str_list 

    players = ["1", "2", "3", "4"]

    rounds = berger_tables(players)
    print(rounds)
        [[['1', '4'], ['2', '3']],
         [('4', '3'), ['1', '2']],
         [['2', '4'], ['3', '1']]]
    print("\n".join(round_robin_rounds_to_str_list(rounds)))
        Round 1: 1-4 2-3
        Round 2: 4-3 1-2
        Round 3: 2-4 3-1
    
Circle algorithm:

    rounds = circle_tables(players)
    print(rounds)
        [[('1', '4'), ('2', '3')],
         [('1', '3'), ('4', '2')],
         [('1', '2'), ('3', '4')]]
    print("\n".join(round_robin_rounds_to_str_list(rounds)))
        Round 1: 1-4 2-3
        Round 2: 1-3 4-2
        Round 3: 1-2 3-4

## Round-robin tables

Ready to use tables:

 * [3 players ](tables/players-03.md)
 * [4 players ](tables/players-04.md)
 * [5 players ](tables/players-05.md)
 * [6 players ](tables/players-06.md)
 * [7 players ](tables/players-07.md)
 * [8 players ](tables/players-08.md)
 * [9 players ](tables/players-09.md)
 * [10 players](tables/players-10.md)
 * [11 players](tables/players-11.md)
 * [12 players](tables/players-12.md)
 * [13 players](tables/players-13.md)
 * [14 players](tables/players-14.md)
 * [15 players](tables/players-15.md)
 * [16 players](tables/players-16.md)
 * [17 players](tables/players-17.md)
 * [18 players](tables/players-18.md)
 * [19 players](tables/players-19.md)
 * [20 players](tables/players-20.md)
 * [21 players](tables/players-21.md)
 * [22 players](tables/players-22.md)
 * [23 players](tables/players-23.md)
 * [24 players](tables/players-24.md)
 * [25 players](tables/players-25.md)


## NOTE: not yet on PyPI, sorry!
will be done ...

## TODO: implement improvement of the algorithm(s) to be more just:
work in progress in unit tests, check how just system is:
 * nearly equal times of schedule order 
 * nearly equal times of first in a pair

