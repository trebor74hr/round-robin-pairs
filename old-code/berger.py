# PLACEHOLDER = "."
# def berger_tables_complex_and_wrong_order(players: List[PlayerName], verbose:bool = False) -> RoundRobnRounds:
#     """ 
#     berger-tables based on crosstable
#     references:
#         - https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
#         - https://handbook.fide.com/chapter/C05Annex1
#     """
#     n = len(players)
#     if verbose:
#         print(players)
#     assert n > 0 
#     if n % 2 == 1:
#         players.append("BYE")
#         n = len(players)
#     
#     diag_table = []
#     idx_start = n - 2
#     # 2 - 13, 1 - 14
#     cols_nr = n -1 +  n - 2
#     n_half = n // 2
#     assert  n_half * 2 == n
#     for idx1 in range(n-1):
#         row = []
#         players_round = list(range(1, len(players)))
#         for idx2 in range(cols_nr):
#             if idx2 >= idx_start and players_round:
#                 val = players_round.pop(0)
#             else:
#                 val = PLACEHOLDER
#             row.append(val)
#         diag_table.append(row)
#         idx_start -= 1
# 
#     header = players[1:-1] + players[:-1]
#     if verbose:
#         print(f"{'*':>{FMT_WIDTH}}  {pp_players_row(header)}")
# 
#     rounds = OrderedDict([(round_nr, []) for round_nr in range(1, n-1+1)])
# 
#     for idx, row in enumerate(diag_table, 0):
#         pl1 = players[idx]
#         for idx2, round_nr in enumerate(row, 0):
#             if round_nr!=PLACEHOLDER and len(rounds[round_nr]) <= n_half:
#                 pl2 = header[idx2]
#                 if pl2 == pl1:
#                     pl2 = players[-1] 
#                 pair = (pl1, pl2)
#                 rounds[round_nr].append(pair)
# 
#         if verbose:
#             print(f"{pl1:>{FMT_WIDTH}}. {pp_players_row(row)}")
# 
#     if verbose:
#         for round_nr, pairs_row in rounds.items():
#             print(f"{round_nr:>{FMT_WIDTH}}. {pp_player_pairs_row(pairs_row)}")
# 
#     return rounds.values()
# 

