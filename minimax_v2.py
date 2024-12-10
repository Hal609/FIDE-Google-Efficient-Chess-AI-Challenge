import chess
from collections import Counter
import random


def calc_heuristic(state, depth):
    if state.is_checkmate():
        # Depth-weighted checkmate value
        return (999999 if state.turn else -999999) - depth

    if state.is_check():
        return 50 if state.turn else -50

    # Material evaluation
    piece_values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9
    }
    board = str(state.board_fen()).replace('/', '')
    piece_counts = Counter(board)

    return sum(piece_values.get(piece, 0) * count for piece, count in piece_counts.items())


def quiescence(state, alpha, beta):
    stand_pat = calc_heuristic(state, depth=0)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in state.legal_moves:
        if state.is_capture(move) or state.gives_check(move):
            state.push(move)
            score = -quiescence(state, -beta, -alpha)
            state.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def minimax(state, depth, alpha, beta, maximizingPlayer, transposition_table):
    zobrist_hash = hash(state.board_fen())  # Use the FEN hash
    if zobrist_hash in transposition_table:
        return transposition_table[zobrist_hash]

    if depth == 0:
        return quiescence(state, alpha, beta), None

    best_move = None

    # Order moves by heuristic priority: checks > captures > promotions
    moves = list(state.legal_moves)
    moves.sort(key=lambda move: (state.gives_check(move), state.is_capture(move), move.promotion), reverse=True)

    if maximizingPlayer:
        max_value = -float('inf')
        for move in moves:
            state.push(move)
            value, _ = minimax(state, depth - 1, alpha, beta, False, transposition_table)
            state.pop()
            if value > max_value:
                max_value = value
                best_move = move
            alpha = max(alpha, max_value)
            if beta <= alpha:
                break
        transposition_table[zobrist_hash] = max_value, best_move
        return max_value, best_move
    else:
        min_value = float('inf')
        for move in moves:
            state.push(move)
            value, _ = minimax(state, depth - 1, alpha, beta, True, transposition_table)
            state.pop()
            if value < min_value:
                min_value = value
                best_move = move
            beta = min(beta, min_value)
            if beta <= alpha:
                break
        transposition_table[zobrist_hash] = min_value, best_move
        return min_value, best_move


def dynamic_depth(state):
    piece_count = len(state.piece_map())
    if piece_count <= 10:  # Endgame
        return 4
    elif piece_count <= 20:  # Midgame
        return 4
    else:  # Opening
        return 4


def chess_bot(obs):
    """
    Args:
        obs: An object with a 'board' attribute representing the current board state as a FEN string.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    game = chess.Board(obs.board)
    depth = dynamic_depth(game)
    transposition_table = {}

    moves = list(game.legal_moves)
    if len(moves) == 1:
        return str(moves[0])  # Single move left, no need for further calculations

    best_value = -float('inf')
    best_move = None

    # Evaluate all moves using minimax
    for move in moves:
        game.push(move)
        value, _ = minimax(game, depth - 1, -float('inf'), float('inf'), False, transposition_table)
        game.pop()
        if value > best_value:
            best_value = value
            best_move = move

    return str(best_move)
