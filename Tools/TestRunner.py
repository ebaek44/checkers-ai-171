"""
TestRunner.py

Run two AI checkers players against each other multiple times and report
wins / losses / ties, without printing the board every game.

Usage:
    python3 TestRunner.py <col> <row> <k> <ai_path_1> <ai_path_2>

Example:
    python3 TestRunner.py 7 7 2 ../src/checkers-python/main.py Sample_AIs/Average_AI/main.py
"""

import sys

sys.path.append("./Sample_AIs/Random_AI/")
sys.path.append("./Sample_AIs/Random_AI/AI_Extensions/")

from GameLogic import GameLogic

NUM_GAMES = 100
TIME_LIMIT = 1200  # seconds, same as main.py uses

def run_series(col, row, k, ai_path_1, ai_path_2, num_games=NUM_GAMES, time_limit=TIME_LIMIT):
    """
    Runs num_games games between ai_path_1 and ai_path_2.
    We alternate who goes first to avoid bias.

    Assumes GameLogic.Run(...) returns:
        1 -> player 1 (ai_path_1 in that game instance)
        2 -> player 2 (ai_path_2 in that game instance)
        0 or None -> tie (adjust if your skeleton returns something else)
    """
    stats = {
        "ai1_wins": 0,
        "ai2_wins": 0,
        "ties": 0
    }

    for i in range(num_games):
        # Alternate sides each game:
        # even i: ai1 = P1, ai2 = P2
        # odd  i: ai2 = P1, ai1 = P2
        if i % 2 == 0:
            p1_path, p2_path = ai_path_1, ai_path_2
            ai1_is_p1 = True
        else:
            p1_path, p2_path = ai_path_2, ai_path_1
            ai1_is_p1 = False

        print(f"Game {i+1}/{num_games} (P1: {p1_path}, P2: {p2_path})")

        # debug=False to avoid board printing
        game = GameLogic(col, row, k, 'l', debug=False)

        # IMPORTANT: this assumes Run returns winner as 1, 2, or 0/None for tie.
        winner = game.Run(mode='l', ai_path_1=p1_path, ai_path_2=p2_path, time=time_limit)
        

        # Normalize winner to int
        if winner is None:
            winner = 0

        if winner == 1:
            # Player 1 wins in this game
            if ai1_is_p1:
                stats["ai1_wins"] += 1
            else:
                stats["ai2_wins"] += 1
        elif winner == 2:
            # Player 2 wins in this game
            if ai1_is_p1:
                stats["ai2_wins"] += 1
            else:
                stats["ai1_wins"] += 1
        else:
            # tie
            stats["ties"] += 1

    return stats

def main():
    if len(sys.argv) != 6:
        print("Usage: python3 Batch_Runner.py <col> <row> <k> <ai_path_1> <ai_path_2>")
        sys.exit(1)

    col = int(sys.argv[1])
    row = int(sys.argv[2])
    k   = int(sys.argv[3])
    ai_path_1 = sys.argv[4]
    ai_path_2 = sys.argv[5]

    stats = run_series(col, row, k, ai_path_1, ai_path_2)

    print("\n===== RESULTS AFTER", NUM_GAMES, "GAMES =====")
    print(f"AI 1 ({ai_path_1}) wins: {stats['ai1_wins']}")
    print(f"AI 2 ({ai_path_2}) wins: {stats['ai2_wins']}")
    print(f"Ties: {stats['ties']}")
    print("=======================================")

if __name__ == "__main__":
    main()
