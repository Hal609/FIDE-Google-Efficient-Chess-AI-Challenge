# Efficient Chess AI

A tiny chess agent that plays under strict CPU, memory and time limitations which placed 400th out of 967 teams in [FIDE & Google's Efficient Chess AI Challeng](https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/overview).
The constraints of the competition were:
- 10s time limit with 0.1s Simple Delay
- 5 MiB of RAM
- Dedicated CPU: a single 2.20GHz core
- 64KiB compressed submission size limit

## Features
- Miniaturised version of the legal move checking algorithm from the python-chess library to find legal moves
- Two move depth minimax search with alpha-beta pruning
- Time aware early stopping on search
- Prioritised searching of moves that involve captures or checks
- Custom heuristic to evaluate board positions based on piece values, checks, pawn structure and king positioning

Note: Code lacks comments to reduce file size and fit within the file size limit.
