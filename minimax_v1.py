import chess
from copy import deepcopy
from collections import Counter
import numpy as np
import random


def calc_heuristic(state):
    if state.is_checkmate():
        return (state.turn*2 - 1) * -float('inf')

    if state.is_check():
        return 50 if state.turn else -50

    piece_values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9
    }
    board = str(state.board_fen()).replace('/', '')
    piece_counts = Counter(board)

    return sum(piece_values.get(piece, 0) * count for piece, count in piece_counts.items())


def minimax(state, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or state.is_checkmate():
        return calc_heuristic(state), None

    best_move = None

    moves = list(state.legal_moves)
    white_king_square = chess.square_name(state.king(chess.WHITE))
    no_king_moves = [move for move in moves if white_king_square != str(move)[:2]]
    if len(no_king_moves) > 0: moves = no_king_moves
    random.shuffle(moves)
    moves.sort(key=lambda move: state.is_capture(move), reverse=True)

    if maximizingPlayer:
        max_value = -float('inf')
        for move in moves:
            state.push(move)
            value, _ = minimax(state, depth - 1, alpha, beta, False)
            state.pop()
            if value > max_value:
                max_value = value
                best_move = move
            alpha = max(alpha, max_value)
            if beta <= alpha:  # Prune
                break
        return max_value, best_move
    else:  # minimizing player
        min_value = float('inf')
        for move in moves:
            state.push(move)
            value, _ = minimax(state, depth - 1, alpha, beta, True)
            state.pop()
            if value < min_value:
                min_value = value
                best_move = move
            beta = min(beta, min_value)
            if beta <= alpha:  # Prune
                break
        return min_value, best_move


def chess_bot(obs):
    """
    Args:
        obs: An object with a 'board' attribute representing the current board state as a FEN string.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    # 0. Parse the current board state and generate legal moves using Chessnut library
    game = chess.Board(obs.board)
    moves = list(game.legal_moves)

    _, move = minimax(game, depth=4, alpha=-float('inf'), beta=float('inf'), maximizingPlayer=game.turn)

    if move is None:
        move = random.choice(list(game.legal_moves))

    return str(move)
