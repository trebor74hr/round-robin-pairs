"""
Script used to generate markdown for documentation
"""
import unittest
from itertools import combinations
import os, sys

root_path = os.path.join(os.path.dirname(__file__), ".")
sys.path.insert(0, root_path)
tables_path = os.path.join(os.path.dirname(__file__), "tables")

from round_robin_pairs import (
        berger_tables, circle_tables, round_robin_rounds_to_str_list,
        equalize_schedules_in_rounds, EqualizeType, pprint_player_pairs_row,
        find_best_equalize_solution, has_ideal,
        )
from round_robin_pairs.base import FMT_WIDTH, create_demo_rounds_str_list

def generate_tables(nr_players_from:int, nr_players_to:int):
    assert nr_players_from < nr_players_to

    print(f"Generate to '{tables_path}' folder:", end=" ")
    for nr_players in range(nr_players_from, nr_players_to+1):
        fname = f"players-{nr_players:02d}.md"
        with open(os.path.join(tables_path, fname), "w") as fout:

            fout.write(f"# Round-robin pairs for {nr_players} players")
            fout.write("\n" * 1)
            fout.write("\n" * 1)

            variants = []
            if has_ideal(nr_players):
                if nr_players % 2 == 0:
                    variants.append(("Modified Berger (ideal)", {"berger": True, "ideal": True}))
                    variants.append(("Berger", {"berger": True}))
                else:
                    variants.append(("Berger (ideal)", {"berger": True}))
            else:
                fout.write(f"NOTE: **Currently ideal solution not available - issue with first schedule.**")
                fout.write("\n" * 2)
                variants.append(("Berger", {"berger": True}))
            variants.append(("Circle", {"berger": False}))

            for title, kwargs in variants:
                kwargs["fmt_width"] = 3
                str_list = create_demo_rounds_str_list(nr_players, **kwargs)
                fout.write(f"## {title}")
                fout.write("\n" * 1)
                fout.write("\n```\n")
                fout.write("\n".join(str_list))
                fout.write("\n```\n")
                fout.write("\n" * 2)
        print(f"{fname} ", end=" ")

    print(".")




if __name__=="__main__":
    generate_tables(3, 25)

