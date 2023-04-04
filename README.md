# round-robin-pairs - round-robin tournament system

Implementations of Round-robin tournament algorithms, namely  berger tables and circle algorithm.

Based on [Round-robin tournament / Scheduling algorithms (wikipedia)](https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm).

Task: given list of players will return list of game rounds. Each game round
has list of two players pairs.

Implementation of:

    - ˇcircle_tables()ˇ -> circle system
    - ˇberger_tables()ˇ -> berger tables

Functions have:

    * Input: list of players names
    * Output: list of rounds containing list of player pairs

Unit testing based on examples in [https://handbook.fide.com/chapter/C05Annex1](https://handbook.fide.com/chapter/C05Annex1).


