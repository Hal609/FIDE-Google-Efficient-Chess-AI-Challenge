import chess
from copy import deepcopy
from collections import Counter
import numpy as np
import random


def calc_heuristic(state):
    # Map pieces to their respective values
    piece_values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9,  # White pieces
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9  # Black pieces
    }

    # Count the occurrences of each piece using Counter
    board = str(state.board_fen()).replace('/', '')  # Remove slashes from FEN
    piece_counts = Counter(board)

    # Compute the heuristic value
    score = sum(piece_values.get(piece, 0) * count for piece, count in piece_counts.items())
    return score


def chess_bot(obs):
    """
    Simple chess bot that prioritizes checkmates, then captures, queen promotions, then randomly moves.

    Args:
        obs: An object with a 'board' attribute representing the current board state as a FEN string.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    # 0. Parse the current board state and generate legal moves using Chessnut library
    game = chess.Board(obs.board)
    moves = list(game.legal_moves)
    initial_score = calc_heuristic(game)

    # 1. Check a subset of moves for checkmate
    for move in moves:
        game.push(move)
        if game.is_checkmate():
            return str(move)
        if "q" in str(move).lower():
            return str(move)
        move_score = calc_heuristic(game)
        if move_score > initial_score:
                return str(move)
        game.pop()

    # 4. Random move if no checkmates or captures
    return str(random.choice(moves))
