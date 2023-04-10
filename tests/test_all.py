"""
Unit testing based on examples in:
    https://handbook.fide.com/chapter/C05Annex1

run like:

    python test_all
    python -m unittest test_all.TestRoundRobin.test_4_circle
"""
import unittest
from itertools import combinations
from pprint import pprint
import os, sys

root_path = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, root_path)

from round_robin_pairs import (
        berger_tables, circle_tables, round_robin_rounds_to_str_list,
        equalize_schedules_in_rounds, EqualizeType, pprint_player_pairs_row,
        find_best_equalize_solution, has_not_ideal,
        )
from round_robin_pairs.base import FMT_WIDTH

class TestAll(unittest.TestCase):
    """
    Ideal solutions (R2L2R - V angled clockwise by 90 percent):
        2   yes (not possible to have not ideal)
        4   -   (not possible to have ideal)
        6   yes
        8   yes
        10  - 
        12  yes
        14  yes
        16  -
        18  yes
        20  yes
        22  -
        24  yes
        26  yes
        28  -
        30  yes
        32  yes
        34  -
        36  yes
        38  yes
        40  -
        42  yes
        44  yes
        46  -
        48  yes
        50  yes

    to conclude:
        X - 4 // 6 == 0
        4 10 16 22
        (10 - 4) % 6 == 0
        

    """

    def create_rounds_str_list(self, nr_of_players:int, berger:bool, verbose:bool = False, return_all:bool = False):
        players = list([f"{pl:>{FMT_WIDTH}d}" for pl in range(1,nr_of_players+1)])
        # print(players)
        function = berger_tables if berger else circle_tables
        round_robin_rounds = function(players, verbose=verbose)

        expected = set([tuple(sorted(pair)) for pair in combinations(players, 2)])
        got = [tuple(sorted(pair)) for row in round_robin_rounds for pair in row]
        #print(expected); print(got)
        self.assertEqual(len(expected), len(got), "found some duplicates or missing")
        self.assertEqual(expected, set(got), "some pair combinations not found" )

        rounds_str_list = round_robin_rounds_to_str_list(round_robin_rounds)
        if verbose:
            print("\n".join(rounds_str_list))

        if return_all:
            return rounds_str_list, round_robin_rounds, players
        return rounds_str_list

    def test_4_circle(self):
        # for README.md
        # players = ["1", "2", "3", "4"]
        # rounds = berger_tables(players)
        # print(rounds)
        # print("\n".join(round_robin_rounds_to_str_list(rounds)))
        # rounds = circle_tables(players)
        # print(rounds)
        # print("\n".join(round_robin_rounds_to_str_list(rounds)))
        self.assertEqual(self.create_rounds_str_list(4, berger=False, verbose=False), [
              "Round 1: 1-4 2-3" 
            , "Round 2: 1-3 4-2" 
            , "Round 3: 1-2 3-4" 
            ])

    def test_5_circle(self):
        rounds = self.create_rounds_str_list(5, berger=False, verbose=False)
        self.assertEqual(rounds, [
            'Round 1: 1-BYE 2-5 3-4',
            'Round 2: 1-5 BYE-4 2-3',
            'Round 3: 1-4 5-3 BYE-2',
            'Round 4: 1-3 4-2 5-BYE',
            'Round 5: 1-2 3-BYE 4-5',
            ])



    def test_6_circle(self):
        self.assertEqual(self.create_rounds_str_list(6, berger=False, verbose=False), [
            'Round 1: 1-6 2-5 3-4',
            'Round 2: 1-5 6-4 2-3',
            'Round 3: 1-4 5-3 6-2',
            'Round 4: 1-3 4-2 5-6',
            'Round 5: 1-2 3-6 4-5',
            ])

    def test_8_circle(self):
        self.assertEqual(self.create_rounds_str_list(8, berger=False, verbose=False), [
            'Round 1: 1-8 2-7 3-6 4-5',
            'Round 2: 1-7 8-6 2-5 3-4',
            'Round 3: 1-6 7-5 8-4 2-3',
            'Round 4: 1-5 6-4 7-3 8-2',
            'Round 5: 1-4 5-3 6-2 7-8',
            'Round 6: 1-3 4-2 5-8 6-7',
            'Round 7: 1-2 3-8 4-7 5-6',
            ])

    def test_14_circle(self):
        self.assertEqual(self.create_rounds_str_list(14, berger=False, verbose=False), [
            'Round 1: 1-14 2-13 3-12 4-11 5-10 6-9 7-8',
            'Round 2: 1-13 14-12 2-11 3-10 4-9 5-8 6-7',
            'Round 3: 1-12 13-11 14-10 2-9 3-8 4-7 5-6',
            'Round 4: 1-11 12-10 13-9 14-8 2-7 3-6 4-5',
            'Round 5: 1-10 11-9 12-8 13-7 14-6 2-5 3-4',
            'Round 6: 1-9 10-8 11-7 12-6 13-5 14-4 2-3',
            'Round 7: 1-8 9-7 10-6 11-5 12-4 13-3 14-2',
            'Round 8: 1-7 8-6 9-5 10-4 11-3 12-2 13-14',
            'Round 9: 1-6 7-5 8-4 9-3 10-2 11-14 12-13',
            'Round 10: 1-5 6-4 7-3 8-2 9-14 10-13 11-12',
            'Round 11: 1-4 5-3 6-2 7-14 8-13 9-12 10-11',
            'Round 12: 1-3 4-2 5-14 6-13 7-12 8-11 9-10',
            'Round 13: 1-2 3-14 4-13 5-12 6-11 7-10 8-9',
            ])

    def test_3_berger(self):
        self.assertEqual(self.create_rounds_str_list(3, berger=True, verbose=False), [
              "Round 1: 1-BYE 2-3" 
            , "Round 2: BYE-3 1-2" 
            , "Round 3: 2-BYE 3-1" 
            ])

    def test_4_berger(self):
        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(4, berger=True, verbose=False, return_all=True)
        self.assertEqual(rounds_str_list, [
              "Round 1: 1-4 2-3" 
            , "Round 2: 4-3 1-2" 
            , "Round 3: 2-4 3-1" 
            ])
        rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R", verbose=False)
        self.assertEqual((score_before, (score_after - score_before)), (7, 0))
        # self.assertEqual((score_before, (score_after - score_before)), (6, 0))


    def test_4_berger_cant_have_ideal(self):
        self.maxDiff = None

        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(4, berger=True, verbose=False, return_all=True)

        brute_force_factor = 1000
        best_result = \
                find_best_equalize_solution(round_robin_rounds, players=players, 
                        brute_force_factor=brute_force_factor, verbose=False)

        self.assertEqual(best_result.score_before, 7)

        # ------------------------------------------------------------
        # Can not be better, in every case one player will play 3x in 1st sch and 0 in 2nd sch
        # ------------------------------------------------------------
        self.assertEqual(best_result.best_score, 7, best_result.best_score)
        self.assertEqual(best_result.is_ideal(), False)
        self.assertTrue(best_result.best_eq_type in ("DIAG_L2R",), best_result.best_eq_type)


    def test_5_berger(self):
        rounds_str_list, round_robin_rounds, players = \
                self.create_rounds_str_list(5, berger=True, verbose=False, return_all=True)
        self.assertEqual(rounds_str_list, [
              "Round 1: 1-BYE 2-5 3-4"
            , "Round 2: BYE-4 5-3 1-2"
            , "Round 3: 2-BYE 3-1 4-5"
            , "Round 4: BYE-5 1-4 2-3"
            , "Round 5: 3-BYE 4-2 5-1"
            ])
        rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R", verbose=False)
        self.assertEqual((score_before, (score_after - score_before)), (13, -1))
        # self.assertEqual((score_before, (score_after - score_before)), (16, -4))


    def test_6_berger(self):
        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(6, berger=True, verbose=False, return_all=True)
        self.assertEqual(rounds_str_list, [
              "Round 1: 1-6 2-5 3-4"
            , "Round 2: 6-4 5-3 1-2"
            , "Round 3: 2-6 3-1 4-5"
            , "Round 4: 6-5 1-4 2-3"
            , "Round 5: 3-6 4-2 5-1"
            ])
        rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R", verbose=False)
        self.assertEqual((score_before, (score_after - score_before)), (13, -1))
        # self.assertEqual((score_before, (score_after - score_before)), (16, -4))

    def test_6_berger_has_ideal(self):
        self.maxDiff = None

        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(6, berger=True, verbose=False, return_all=True)

        brute_force_factor = 500
        best_result = \
                find_best_equalize_solution(round_robin_rounds, players=players, 
                        brute_force_factor=brute_force_factor, verbose=False)

        self.assertEqual(best_result.score_before, 13)

        # ------------------------------------------------------------
        # IDEAL
        # ------------------------------------------------------------
        self.assertEqual(best_result.best_score, 6, best_result.best_score)
        self.assertEqual(best_result.is_ideal(), True)
        self.assertEqual(best_result.best_eq_type, "DIAG_R2L2R", best_result.best_eq_type)


    def test_7_berger(self):
        self.assertEqual(self.create_rounds_str_list(7, berger=True, verbose=False), [
              "Round 1: 1-BYE 2-7 3-6 4-5"
            , "Round 2: BYE-5 6-4 7-3 1-2"
            , "Round 3: 2-BYE 3-1 4-7 5-6"
            , "Round 4: BYE-6 7-5 1-4 2-3"
            , "Round 5: 3-BYE 4-2 5-1 6-7"
            , "Round 6: BYE-7 1-6 2-5 3-4"
            , "Round 7: 4-BYE 5-3 6-2 7-1"
            ])

    def test_8_berger(self):
        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(8, berger=True, verbose=False, return_all=True)
        self.assertEqual(rounds_str_list, [
              "Round 1: 1-8 2-7 3-6 4-5"
            , "Round 2: 8-5 6-4 7-3 1-2"
            , "Round 3: 2-8 3-1 4-7 5-6"
            , "Round 4: 8-6 7-5 1-4 2-3"
            , "Round 5: 3-8 4-2 5-1 6-7"
            , "Round 6: 8-7 1-6 2-5 3-4"
            , "Round 7: 4-8 5-3 6-2 7-1"
            ])
        rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R", verbose=False)
        self.assertEqual((score_before, (score_after - score_before)), (19, 1))
        # self.assertEqual((score_before, (score_after - score_before)), (30, -2))

    def test_8_berger_has_ideal(self):
        self.maxDiff = None

        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(8, berger=True, verbose=False, return_all=True)

        brute_force_factor = 500
        best_result = \
                find_best_equalize_solution(round_robin_rounds, players=players, 
                        brute_force_factor=brute_force_factor, verbose=False)

        self.assertEqual(best_result.score_before, 19)
        # ------------------------------------------------------------
        # IDEAL
        # ------------------------------------------------------------
        self.assertEqual(best_result.best_score, 8, best_result.best_score)
        self.assertEqual(best_result.is_ideal(), True)
        self.assertEqual(best_result.best_eq_type, "DIAG_R2L2R", best_result.best_eq_type)

    def test_10_berger(self):
        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(10, berger=True, verbose=False, return_all=True)
        self.assertEqual(rounds_str_list, [
              "Round 1: 1-10 2-9 3-8 4-7 5-6"
            , "Round 2: 10-6 7-5 8-4 9-3 1-2"
            , "Round 3: 2-10 3-1 4-9 5-8 6-7"
            , "Round 4: 10-7 8-6 9-5 1-4 2-3"
            , "Round 5: 3-10 4-2 5-1 6-9 7-8"
            , "Round 6: 10-8 9-7 1-6 2-5 3-4"
            , "Round 7: 4-10 5-3 6-2 7-1 8-9"
            , "Round 8: 10-9 1-8 2-7 3-6 4-5"
            , "Round 9: 5-10 6-4 7-3 8-2 9-1"
            ])
        rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R", verbose=False)
        self.assertEqual((score_before, (score_after - score_before)), (25, 6))
        # self.assertEqual((score_before, (score_after - score_before)), (40, -4))

    def test_10_berger_find(self):
        self.maxDiff = None

        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(10, berger=True, verbose=False, return_all=True)

        brute_force_factor = 500
        best_result = \
                find_best_equalize_solution(round_robin_rounds, players=players, 
                        brute_force_factor=brute_force_factor, verbose=False)

        self.assertEqual(best_result.score_before, 25)
        # ------------------------------------------------------------
        self.assertTrue(best_result.best_score <= 23, best_result.best_score)
        self.assertEqual(best_result.is_ideal(), False)
        self.assertTrue(best_result.best_eq_type in ("BRUTE_FORCE", "DIAG_R2L2R"), best_result.best_eq_type)


    def test_12_berger(self):
        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(12, berger=True, verbose=False, return_all=True)
        self.assertEqual(rounds_str_list, [
              "Round 1: 1-12 2-11 3-10 4-9 5-8 6-7"
            , "Round 2: 12-7 8-6 9-5 10-4 11-3 1-2"
            , "Round 3: 2-12 3-1 4-11 5-10 6-9 7-8"
            , "Round 4: 12-8 9-7 10-6 11-5 1-4 2-3"
            , "Round 5: 3-12 4-2 5-1 6-11 7-10 8-9"
            , "Round 6: 12-9 10-8 11-7 1-6 2-5 3-4"
            , "Round 7: 4-12 5-3 6-2 7-1 8-11 9-10"
            , "Round 8: 12-10 11-9 1-8 2-7 3-6 4-5"
            , "Round 9: 5-12 6-4 7-3 8-2 9-1 10-11"
            , "Round 10: 12-11 1-10 2-9 3-8 4-7 5-6"
            , "Round 11: 6-12 7-5 8-4 9-3 10-2 11-1"
            ])
        rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R", verbose=False)
        self.assertEqual((score_before, (score_after - score_before)), (31, 11))
        # self.assertEqual((score_before, (score_after - score_before)), (70, -8))

    def test_12_berger_has_ideal(self):
        self.maxDiff = None

        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(12, berger=True, verbose=False, return_all=True)

        brute_force_factor = 500
        best_result = \
                find_best_equalize_solution(round_robin_rounds, players=players, 
                        brute_force_factor=brute_force_factor, verbose=False)

        self.assertEqual(best_result.score_before, 31)
        # ------------------------------------------------------------
        # IDEAL:
        # ------------------------------------------------------------
        self.assertEqual(best_result.best_score, 12, best_result.best_score)
        self.assertEqual(best_result.is_ideal(), True)
        self.assertEqual(best_result.best_eq_type, "DIAG_R2L2R", best_result.best_eq_type)

    def test_14_berger(self):
        self.maxDiff = None
        # nr_of_players = 14
        # # players = list([f"P{pl:02d}" for pl in range(1,nr_of_players+1)])
        # players = list([f"{pl}" for pl in range(1,nr_of_players+1)])
        # berger_tables(players, verbose=True)


        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(14, berger=True, verbose=False, return_all=True)
        self.assertEqual(rounds_str_list, [
              "Round 1: 1-14 2-13 3-12 4-11 5-10 6-9 7-8"
            , "Round 2: 14-8 9-7 10-6 11-5 12-4 13-3 1-2"
            , "Round 3: 2-14 3-1 4-13 5-12 6-11 7-10 8-9"
            , "Round 4: 14-9 10-8 11-7 12-6 13-5 1-4 2-3"
            , "Round 5: 3-14 4-2 5-1 6-13 7-12 8-11 9-10"
            , "Round 6: 14-10 11-9 12-8 13-7 1-6 2-5 3-4"
            , "Round 7: 4-14 5-3 6-2 7-1 8-13 9-12 10-11"
            , "Round 8: 14-11 12-10 13-9 1-8 2-7 3-6 4-5"
            , "Round 9: 5-14 6-4 7-3 8-2 9-1 10-13 11-12"
            , "Round 10: 14-12 13-11 1-10 2-9 3-8 4-7 5-6"
            , "Round 11: 6-14 7-5 8-4 9-3 10-2 11-1 12-13"
            , "Round 12: 14-13 1-12 2-11 3-10 4-9 5-8 6-7"
            , "Round 13: 7-14 8-6 9-5 10-4 11-3 12-2 13-1"
            ])
        # print("== Rounds Berger:"); pprint_player_pairs_row(round_robin_rounds)

        # rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R", players=players, verbose=False)
        # self.assertNotEqual(rounds_new, round_robin_rounds)
        # # print("== Rounds EQ-L2R:"); pprint_player_pairs_row(rounds_new, 2)
        # self.assertEqual((score_before, score_after - score_before), (37, 13))
        # # self.assertEqual((score_before, score_after - score_before), (96, -8))

        # rounds_new2, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_R2L", players=players, verbose=False)
        # self.assertNotEqual(rounds_new2, round_robin_rounds)
        # self.assertNotEqual(rounds_new2, rounds_new)
        # # print("== Rounds EQ-R2L:"); pprint_player_pairs_row(rounds_new2, 2)
        # self.assertEqual((score_before, score_after - score_before), (37, 19))
        # # self.assertEqual((score_before, score_after - score_before), (96, -10))

        # rounds_new3, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R2L", players=players, verbose=False)
        # self.assertNotEqual(rounds_new3, round_robin_rounds)
        # self.assertNotEqual(rounds_new3, rounds_new2)
        # self.assertNotEqual(rounds_new3, rounds_new)
        # # print("== Rounds EQ-R2L:"); pprint_player_pairs_row(rounds_new3, 2)
        # self.assertEqual((score_before, score_after - score_before), (37, 16))
        # # self.assertEqual((score_before, score_after - score_before), (96, -10))

        rounds_new4, score_before, score_after = \
                equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_R2L2R", players=players, verbose=False)
        self.assertNotEqual(rounds_new4, round_robin_rounds)

        # print("== Rounds EQ-R2L:"); pprint_player_pairs_row(rounds_new4, 2)
        # ------------------------------------------------------------
        # IDEAL:
        # ------------------------------------------------------------
        self.assertEqual((score_before, score_after - score_before), (37, -23))
        # self.assertEqual((score_before, score_after - score_before), (96, -12))


    def test_14_berger_has_ideal(self):
        self.maxDiff = None

        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(14, berger=True, verbose=False, return_all=True)

        brute_force_factor = 500
        best_result = \
                find_best_equalize_solution(round_robin_rounds, players=players, 
                        brute_force_factor=brute_force_factor, verbose=False)

        self.assertEqual(best_result.score_before, 37)
        # ------------------------------------------------------------
        # IDEAL:
        # ------------------------------------------------------------
        self.assertEqual(best_result.best_score, 14, best_result.best_score)
        self.assertEqual(best_result.is_ideal(), True)
        self.assertEqual(best_result.best_eq_type, "DIAG_R2L2R", best_result.best_eq_type)


    def test_16_berger(self):
        self.maxDiff = None
        nr_of_players = 16
        nr_schedules = nr_of_players // 2 + nr_of_players % 2
        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(nr_of_players, berger=True, verbose=False, return_all=True)
        self.assertEqual(rounds_str_list, [
              "Round 1: 1-16 2-15 3-14 4-13 5-12 6-11 7-10 8-9"
            , "Round 2: 16-9 10-8 11-7 12-6 13-5 14-4 15-3 1-2"
            , "Round 3: 2-16 3-1 4-15 5-14 6-13 7-12 8-11 9-10"
            , "Round 4: 16-10 11-9 12-8 13-7 14-6 15-5 1-4 2-3"
            , "Round 5: 3-16 4-2 5-1 6-15 7-14 8-13 9-12 10-11"
            , "Round 6: 16-11 12-10 13-9 14-8 15-7 1-6 2-5 3-4"
            , "Round 7: 4-16 5-3 6-2 7-1 8-15 9-14 10-13 11-12"
            , "Round 8: 16-12 13-11 14-10 15-9 1-8 2-7 3-6 4-5"
            , "Round 9: 5-16 6-4 7-3 8-2 9-1 10-15 11-14 12-13"
            , "Round 10: 16-13 14-12 15-11 1-10 2-9 3-8 4-7 5-6"
            , "Round 11: 6-16 7-5 8-4 9-3 10-2 11-1 12-15 13-14"
            , "Round 12: 16-14 15-13 1-12 2-11 3-10 4-9 5-8 6-7"
            , "Round 13: 7-16 8-6 9-5 10-4 11-3 12-2 13-1 14-15"
            , "Round 14: 16-15 1-14 2-13 3-12 4-11 5-10 6-9 7-8"
            , "Round 15: 8-16 9-7 10-6 11-5 12-4 13-3 14-2 15-1"
            ])
        # self.assertEqual((score_before, (score_after - score_before)), (126, -10))

        # for offset_x in range(0, nr_schedules):
        #     rounds_new, score_before, score_after = \
        #             equalize_schedules_in_rounds(
        #                     round_robin_rounds, 
        #                     # ok: 
        #                     eq_type="CROSS", 
        #                     # ok: eq_type="DIAG_R2L2R", 
        #                     # ok: eq_type="DIAG_L2R2L", 
        #                     # ok: eq_type="DIAG_L2R", 
        #                     # ok: eq_type="DIAG_R2L", 
        #                     offset_x=offset_x, players=players, verbose=True)
        # self.assertEqual((score_before, (score_after - score_before)), (0, 0))

    def test_16_berger_find(self):
        self.maxDiff = None
        nr_of_players = 16
        nr_schedules = nr_of_players // 2 + nr_of_players % 2
        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(nr_of_players, berger=True, verbose=False, return_all=True)

        brute_force_factor = 500
        # brute_force_factor = None # disabled

        best_result = \
                find_best_equalize_solution(round_robin_rounds, players=players, 
                        brute_force_factor=brute_force_factor, verbose=False)

        # NOTE: brute_force sometimes will find better result
        self.assertEqual(best_result.score_before, 43)
        self.assertTrue(best_result.best_score <= 43, best_result.best_score)
        self.assertTrue(best_result.best_eq_type in ("DIAG_R2L2R", "BRUTE_FORCE"), best_result.best_eq_type)

        # rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R", players=players, verbose=True)
        # self.assertEqual((score_before, (score_after - score_before)), (43, 18))
        # rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_R2L", players=players, verbose=True)
        # self.assertEqual((score_before, (score_after - score_before)), (43, 24))
        # rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_L2R2L", players=players, verbose=True)
        # self.assertEqual((score_before, (score_after - score_before)), (43, 24))
        # rounds_new, score_before, score_after = equalize_schedules_in_rounds(round_robin_rounds, eq_type="DIAG_R2L2R", players=players, verbose=True)
        # self.assertEqual((score_before, (score_after - score_before)), (43, -4))

    def test_18_berger_has_ideal(self):
        self.maxDiff = None
        nr_of_players = 18
        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(nr_of_players, berger=True, verbose=False, return_all=True)

        # brute_force_factor = 1000
        brute_force_factor = None # disabled

        best_result = \
                find_best_equalize_solution(round_robin_rounds, players=players, 
                        brute_force_factor=brute_force_factor, verbose=False)

        self.assertEqual(best_result.score_before, 49)
        # ------------------------------------------------------------
        # IDEAL
        # ------------------------------------------------------------
        self.assertEqual(best_result.best_score, 18, best_result.best_score)
        self.assertEqual(best_result.is_ideal(), True)
        self.assertEqual(best_result.best_eq_type, "DIAG_R2L2R", best_result.best_eq_type)


    def test_20_berger_has_ideal(self):
        self.maxDiff = None
        nr_of_players = 20
        rounds_str_list, round_robin_rounds, players = \
            self.create_rounds_str_list(nr_of_players, berger=True, verbose=False, return_all=True)

        # brute_force_factor = 1000
        brute_force_factor = None # disabled

        best_result = \
                find_best_equalize_solution(round_robin_rounds, players=players, 
                        brute_force_factor=brute_force_factor, verbose=False)

        self.assertEqual(best_result.score_before, 55)
        # ------------------------------------------------------------
        # IDEAL
        # ------------------------------------------------------------
        self.assertEqual(best_result.best_score, 20, best_result.best_score)
        self.assertEqual(best_result.is_ideal(), True)
        self.assertEqual(best_result.best_eq_type, "DIAG_R2L2R", best_result.best_eq_type)

    def test_22_plus_berger_find(self):
        self.maxDiff = None
        for nr_of_players, exp_score_before, exp_best_score, is_ideal in (
            (22, 61  , 55 , ""),
            (24, 67  , 24 , True),
            (26, 73  , 26 , True),
            (28, 79  , 71 , ""),
            (30, 85  , 30 , True),
            (32, 91  , 32 , True),
            (34, 97  , 87 , ""),
            (36, 103 , 36 , True),
            (38, 109 , 38 , True),
            (40, 115 , 103, ""),
            (42, 121 , 42 , True),
            (44, 127 , 44 , True),
            (46, 133 , 119, ""),
            (48, 139 , 48 , True),
            (50, 145 , 50 , True),
            ):

            rounds_str_list, round_robin_rounds, players = \
                self.create_rounds_str_list(nr_of_players, berger=True, verbose=False, return_all=True)

            brute_force_factor = None # disabled
            # brute_force_factor = 300

            best_result = \
                    find_best_equalize_solution(round_robin_rounds, players=players, 
                            brute_force_factor=brute_force_factor, verbose=False)

            # print(nr_of_players, best_result.score_before, best_result.best_score, best_result.is_ideal())

            self.assertEqual(best_result.score_before, exp_score_before)
            self.assertEqual(best_result.best_score, exp_best_score, best_result.best_score)
            if is_ideal:
                # ------------------------------------------------------------
                # IDEAL
                # ------------------------------------------------------------
                self.assertEqual(best_result.is_ideal(), True)
                self.assertEqual(best_result.best_eq_type, "DIAG_R2L2R", best_result.best_eq_type)
            else:
                self.assertIn(best_result.best_eq_type, ("brute_force", "DIAG_R2L2R"), best_result.best_eq_type)


    def test_has_not_ideal(self):
        self.assertEqual(has_not_ideal(4 ), True )
        self.assertEqual(has_not_ideal(6 ), False)
        self.assertEqual(has_not_ideal(8 ), False)
        self.assertEqual(has_not_ideal(10), True )
        self.assertEqual(has_not_ideal(12), False)
        self.assertEqual(has_not_ideal(14), False)
        self.assertEqual(has_not_ideal(16), True )
        self.assertEqual(has_not_ideal(18), False)
        self.assertEqual(has_not_ideal(20), False)
        self.assertEqual(has_not_ideal(22), True )
        self.assertEqual(has_not_ideal(24), False)
        self.assertEqual(has_not_ideal(26), False)
        self.assertEqual(has_not_ideal(28), True )
        self.assertEqual(has_not_ideal(30), False)
        self.assertEqual(has_not_ideal(32), False)
        self.assertEqual(has_not_ideal(34), True )
        self.assertEqual(has_not_ideal(36), False)
        self.assertEqual(has_not_ideal(38), False)
        self.assertEqual(has_not_ideal(40), True )
        self.assertEqual(has_not_ideal(42), False)
        self.assertEqual(has_not_ideal(44), False)
        self.assertEqual(has_not_ideal(46), True )
        self.assertEqual(has_not_ideal(48), False)
        self.assertEqual(has_not_ideal(50), False)


if __name__ == '__main__':
    unittest.main()

