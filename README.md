# chess-engine

A UCI-compatible chess engine written in Python. Polyglot opening book in the early game, then iterative-deepening alpha-beta minimax with a tapered PSQT evaluation.

Built for learning, not for ELO. The engine plays a sound opening, falls back to ~depth 5 in the middlegame under a 5-second time budget, and has no quiescence search — so it'll occasionally hang a piece in a tactical position. Honest about that up front.

## Run it

```bash
pip install -r requirements.txt
python main.py
# pick a color (w/b), enter moves in SAN ("e4", "Nf3", "O-O")
```

For UCI mode (plug into Arena, Cute Chess, lichess-bot, etc):

```bash
python uci.py
```

Then point your UCI GUI at `python /path/to/uci.py`.

## How it picks a move

1. **Opening book** ([books/human.bin](books/)) — a polyglot book of human master games. If the current position is in the book, weighted-choice a move and return it.
2. **Out of book** → iterative deepening, depth 1 up to 18, hard 5-second cap. Each ply runs alpha-beta minimax over all legal moves.
3. **Evaluation** ([evaluate.py](evaluate.py)) — material + piece-square tables, tapered between middlegame and endgame phases. Tables are PeSTO-derived (Stockfish lineage); the rest is mine.

```
main.py        REPL loop, board printing, SAN parsing
search.py      iterativeDeepening + minimax with alpha-beta
evaluate.py    evaluation function: material + PSQT, tapered MG/EG
uci.py         UCI protocol adapter for chess GUIs
books/         polyglot opening books (binary, ~36MB total)
```

## Known limitations

- **No quiescence search.** Cuts off at depth, so captures in the leaf nodes can lead to a "horizon effect" — engine thinks a position is good when there's an unresolved capture sequence one ply deeper.
- **No transposition table.** Same position is re-evaluated multiple times across the search tree. Cheap to add, would buy 1–2 plies of depth at the same time budget.
- **No move ordering beyond legal-move iteration order.** A killer-move heuristic + MVV-LVA on captures would prune the tree much harder.
- **Eval is material + PSQT only.** No mobility, no king safety, no pawn structure terms. The PSQT carries a lot of weight.

In short: this is a textbook minimax engine with the easy half of the optimizations skipped — a deliberate scope choice while learning the fundamentals.

## Books

The three polyglot books in [books/](books/) are weighted differently:

- `human.bin` — biased toward principled human play
- `computer.bin` — engine-vs-engine choices, sharper
- `pecg_book.bin` — Performance Chess Game Book, balanced

`search.py` defaults to `human.bin`; swap the filename to switch styles.
