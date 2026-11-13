---
tag: KJ0XFA
kind: problem
slug: endgame-solving
name: Endgame solving
aliases:
- endgame analysis
area: games-and-search/game-tree-search
level: advanced
summary: Determine the exact outcome and optimal play of positions with few remaining pieces.
prereqs: [perfect-information-game, winning-losing-states, game-tree]
see_also: [retrograde-analysis, endgame-tablebase, proof-number-search, df-pn, alpha-beta-pruning, solved-game, games-on-graphs, exptime]
sources:
  - paper: doi:10.1016/0097-3165(81)90016-9
    title: Aviezri S. Fraenkel and David Lichtenstein, Computing a perfect strategy for n x n chess requires time exponential in n, Journal of Combinatorial Theory, Series A 31(2) (1981)
    locator: pp. 199 to 214 (the problem of deciding the winner of a position of chess generalized to an n by n board is complete for exponential time)
  - paper: doi:10.3233/ICG-1986-9302
    title: Ken Thompson, Retrograde analysis of certain endgames, ICCA Journal 9(3) (1986)
    locator: pp. 131 to 139 (the exact values of all positions of chess endgames with up to five pieces)
  - url: https://www.chessprogramming.org/Syzygy_Bases
    title: Chess Programming Wiki, Syzygy Bases
    locator: the description of the WDL and DTZ metrics and of the fifty-move rule in the tables
---

Endgame solving is the problem of finding the exact value of a game position, win, draw or loss with perfect play by both sides, together with a way to get that value: a move to play and, for a won or lost position, the number of plies to the end. The word *endgame* means that the position has few pieces, so the set of positions that can follow it is small enough to search to the end of the game, with no evaluation function and no guess. It differs from [game tree evaluation](/game-tree-evaluation/) with a depth limit, which gives the value of a search to a fixed depth, not the value of the game. Two cases are usual. One position is solved by a forward search, such as [proof-number search](/proof-number-search/). All positions of an endgame are solved at once by [retrograde analysis](/retrograde-analysis/), and the answers are stored in an [endgame tablebase](/endgame-tablebase/).

## In plain words

When only a few pieces are left on a chess board, a program can stop guessing. It can follow every line of play to the end and know for sure whether the position is a win, a draw or a loss.

The answer has two parts. The first part is the result. The second part is how to get it: which move to play, and how many moves are left. A win that is never finished is worth nothing, so the program must also make progress.

Some endgames are small enough to solve every position once and store the answers in a table. In others, the program solves only the one position in front of it.

## Definition

**Input.** The rules of a finite game with [perfect information](/perfect-information-game/) and two players who move in turn; a finite set $S$ of positions, the *endgame*, that contains the position $p$ to solve; and the value of each move that leaves $S$, for example a capture into a smaller endgame. A game in which the side to move is mated has lost.

**Output.** The value $\text{val}(p) \in \{\text{WIN}, \text{DRAW}, \text{LOSS}\}$ for the side to move, and, when $p$ is won or lost, its distance $d(p)$ and an optimal move.

Let $L_0$ be the positions of $S$ in which the side to move has lost. For $n \ge 1$, let $W_n$ be the positions with a move into $L_{n-1}$, and $L_n$ the positions that have moves, all of which stay in $S$ and lead into $W_{n-1}$, together with $L_{n-1}$; let $W_n$ also contain $W_{n-1}$. Then:

- $\text{val}(p) = \text{WIN}$ when $p \in W_n$ for some $n$, LOSS when $p \in L_n$ for some $n$, and DRAW otherwise. Moves out of $S$ count with their given values.
- $d(p)$ is the least such $n$. This is the *distance to mate* (DTM): the winner ends the game as fast as possible, and the loser delays the end as long as possible.
- An optimal move of a won $p$ leads to a lost position $q$ with $d(q) = d(p) - 1$. An optimal move of a lost $p$ leads to a won $q$ with $d(q) = d(p) - 1$. An optimal move of a drawn $p$ leads to a drawn position.

Following optimal moves from $p$ gives a *main line*, a move sequence that ends in mate after exactly $d(p)$ plies. A drawn position may have no end: the play can go on for ever, for example by repetition.

## Variants

- **One position or all.** Solve one position $p$, or give the value of every position of $S$. The second is the work of a tablebase.
- **Value only.** Return only win, draw or loss, the WDL metric, with no distance. This is enough inside a search, but not to play: a program that only keeps a win may never finish it.
- **Other distances.** Distance to conversion (DTC) counts the plies to a capture or promotion that leaves $S$. Distance to zeroing (DTZ) counts the plies to a capture or pawn move, the moves that reset the fifty-move counter.
- **The fifty-move rule.** Under this rule of chess, a player may claim a draw after 50 moves by each side with no capture and no pawn move. Some wins in DTM take longer and are draws under the rule. The rule makes the value depend on the move counter.
- **Mate in $n$.** Decide whether the side to move can force mate within $n$ moves, as in chess problems. This is a depth-bounded question and has no draws by repetition within the bound.
- **Games with scores.** In games such as awari, the value is a number of stones, not only win or loss; see [solved game](/solved-game/).
- **Generalized boards.** The game is played on an $n$ by $n$ board, with the number of pieces fixed or growing with $n$. This is the setting of the bounds below.

## Examples

**A won position.** The tests of [retrograde analysis](/retrograde-analysis/) use a chess-like toy, not chess: king and rook against king on a 4 by 4 board, with no other pieces and no move counter. A stalemate and the capture of the rook are draws. The set $S$ has 3,496 positions, and every position with White to move is won. White Ka1, Rd2 against Black Kc3, with White to move, is won with $d = 13$ plies, one of the longest. A main line is 1. Rd1 Kc2 2. Rb1 Kc3 3. Rc1+ Kd4 4. Kb1 Kd3 5. Kb2 Kd4 6. Kb3 Kd3 7. Rd1 mate.

**A draw by a move out of the endgame.** In the same toy, White Ka1, Rd4 against Black Kc3, with Black to move, is a draw. The black king takes the rook, which the white king does not guard, and the game leaves $S$ with the value draw.

**A draw by endless play.** In a variant of the toy in which the white king may not move, the tests of the [endgame tablebase](/endgame-tablebase/) find 944 positions with White to move that are draws, and none of them has a capture. Neither side can force a mate, and the play can go on for ever. A solver must find these draws, and a forward search that does not handle repetitions will loop on them.

## Known algorithms

- **[Retrograde analysis](/retrograde-analysis/).** Solves every position of $S$ in $O(v + e)$ time for $v$ positions and $e$ moves, working backward from the mates, and gives the exact distances. The rule behind it is on the page on [winning and losing states](/winning-losing-states/).
- **[Endgame tablebase](/endgame-tablebase/).** Stores the output of retrograde analysis with an index function and compression, so that later a single position is solved by one probe.
- **[Proof-number search](/proof-number-search/) and [df-pn](/df-pn/).** Forward best-first searches that prove or disprove a single goal, such as "White wins", in a large set of positions. They give the value, and a proof tree as the strategy.
- **[Alpha-beta](/alpha-beta-pruning/) to the end of the game.** A depth-first search with mate scores and a [transposition table](/transposition-table/), deepened until it finds a mate; it gives the value and a main line for one position.
- **Search on the graph of positions.** When $S$ is given as a graph, the methods for [games on graphs](/games-on-graphs/) apply.

## Bounds

- **Generalized chess.** Deciding the winner of a position of chess generalized to an $n$ by $n$ board, with a number of pieces that grows with $n$, is complete for [EXPTIME](/exptime/) (Fraenkel and Lichtenstein, 1981). So it needs time exponential in $n$ in the worst case, because EXPTIME is not in P by the time hierarchy theorem.
- **A fixed number of pieces.** With $k$ pieces fixed, an endgame on an $n$ by $n$ board has at most $2 \cdot n^{2k}$ positions, and each chess piece has $O(n)$ moves. So retrograde analysis solves all positions in time $O(k \cdot n^{2k+1})$, which is polynomial in $n$ for each fixed $k$. The exponent grows with $k$, which is why tablebases stop at a few pieces.
- **A move limit.** If the game must end within a number of plies polynomial in the size of the position, a depth-first search of the game tree uses polynomial space, and the problem is in [PSPACE](/pspace/).
- **All positions.** An algorithm that outputs the value of every position of $S$ writes $v$ answers, so it needs $\Omega(v)$ time.

## Reductions

- **To winning and losing states.** Make a graph with one vertex per position of $S$ and one edge per move. The positions with the side to move mated are lost, and the moves out of $S$ are edges to vertices with fixed values. The values of endgame solving are then the labels of [winning and losing states](/winning-losing-states/), with draws for the vertices that get no label.
- **To smaller endgames.** A capture or a promotion leads to an endgame with other pieces. Its values are part of the input, so a set of endgames is solved in order, the smaller ones first.
- **Hardness.** Fraenkel and Lichtenstein reduce a game on Boolean formulas, which is complete for exponential time, to generalized chess, with a position built for each formula.

## Applications

- **Chess programs.** Engines probe tablebases in the search and at the root, to play endgames without error.
- **Solving games.** Large endgame databases were part of the solution of checkers; see [solved game](/solved-game/).
- **Endgame theory.** Exact values check the claims of chess books and show endgames in which a win takes more moves than the fifty-move rule allows.
- **Testing.** The exact values are a reference for the search and evaluation of a game program.

## References
