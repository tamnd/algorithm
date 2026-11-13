---
tag: 97PW5C
kind: definition
slug: solved-game
name: Solved game
aliases:
- weakly solved game
- strongly solved game
area: games-and-search/game-tree-search
level: advanced
summary: A game whose value with perfect play is known (ultra-weakly solved), with a strategy that reaches it from the start (weakly) or from every position (strongly).
prereqs: [zermelo-theorem, minimax, winning-losing-states]
see_also: [retrograde-analysis, endgame-tablebase, endgame-solving, proof-number-search, strategy-stealing-argument, hex-game, branching-factor, game-tree]
sources:
  - paper: doi:10.26481/dis.19940923la
    title: Louis Victor Allis, Searching for solutions in games and artificial intelligence, PhD thesis, University of Limburg, Maastricht (1994)
    locator: Section 1.5 (the definitions of ultra-weakly, weakly and strongly solved games) and Section 6.2.4 (state-space and game-tree complexity, with tic-tac-toe and its 5,478 positions)
  - paper: doi:10.1126/science.1144079
    title: Jonathan Schaeffer, Neil Burch, Yngvi Björnsson, Akihiro Kishimoto, Martin Müller, Robert Lake, Paul Lu and Steve Sutphen, Checkers is solved, Science 317(5844) (2007)
    locator: pp. 1518 to 1522 (checkers is weakly solved as a draw, with endgame databases and a proof search of the opening)
  - paper: doi:10.1111/j.1467-8640.1996.tb00251.x
    title: Ralph Gasser, Solving nine men's morris, Computational Intelligence 12(1) (1996)
    locator: pp. 24 to 41 (databases of the midgame and endgame and a search of the opening phase; the game is a draw)
  - paper: doi:10.1109/MC.2003.1236468
    title: John W. Romein and Henri E. Bal, Solving awari with parallel retrograde analysis, IEEE Computer 36(10) (2003)
    locator: pp. 26 to 33 (the value of all 889,063,398,406 positions, by parallel retrograde analysis; the start is a draw)
  - url: https://arxiv.org/abs/2310.19387
    title: Hiroki Takizawa, Othello is solved, arXiv preprint 2310.19387 (2023)
    locator: the whole preprint (the claim that 8 by 8 Othello is weakly solved as a draw)
  - paper: "A knowledge-based approach of Connect-Four. The game is solved: White wins"
    title: Louis Victor Allis, MSc thesis, Vrije Universiteit Amsterdam, report IR-163 (1988)
    locator: the whole thesis (a weak solution of Connect Four on the 7 by 6 board, found independently of James D. Allen in the same month)
---

A game is *solved* when its outcome with perfect play by both players is known. Allis (1994) gave three levels. A game is *ultra-weakly solved* if the value of the start position is known, *weakly solved* if a strategy is known that gets this value from the start against any play of the opponent, and *strongly solved* if the value of every legal position is known, with a strategy that gets it. By [Zermelo's theorem](/zermelo-theorem/) every finite two-player game with [perfect information](/perfect-information-game/) and no chance has such a value, so the question is only whether it can be computed. Tic-tac-toe is strongly solved, and it is a draw. Checkers is weakly solved as a draw. Chess and Go are not solved.

## Definition

Take a finite two-player [zero-sum game](/zero-sum-game/) with perfect information and no chance, with the [minimax](/minimax/) value $V(p)$ of each position $p$, for example $+1$ for a first-player win, $0$ for a draw and $-1$ for a loss. Allis (1994, Section 1.5) defines:

- **Ultra-weakly solved.** $V(\text{start})$ is known.
- **Weakly solved.** For each player, a strategy is known that, from the start, gets at least $V(\text{start})$ for that player against every strategy of the opponent, within reasonable computing resources.
- **Strongly solved.** For every legal position $p$, $V(p)$ is known, and a strategy that gets $V(p)$ from $p$ is known, within reasonable computing resources.

Each level implies the one above it. A strong solution is a table of the [winning and losing states](/winning-losing-states/) of the whole game graph. A weak solution can be much smaller: it needs a strategy only for the positions that can arise when one side follows it, and it can prove the value with a search that skips the rest, for example by [proof-number search](/proof-number-search/). An ultra-weak solution can be a proof of existence with no strategy at all, as the [strategy-stealing argument](/strategy-stealing-argument/) gives for Hex. Allis says that a game is solved when it is at least weakly solved.

The words "reasonable resources" matter. In principle, [minimax](/minimax/) solves every finite game, so the definition asks for a strategy that can be computed and used in practice, not only one that exists.

A claim that a game is solved is always for one set of rules: the board size, the start position, and the rules for draws and repetitions.

## Examples and non-examples

**Tic-tac-toe is strongly solved, and it is a draw.** The tests solve it in full. They find 5,478 positions that can be reached from the empty board (765 up to the 8 symmetries of the square), of which 958 are over. Of the 5,478 positions, 2,936 are won for X, 1,474 are won for O and 1,068 are draws with best play. Each of the 9 first moves of X keeps the draw. After X takes the centre, O must reply in a corner; after X takes a corner, O must take the centre, and every other reply loses. A strategy that always moves to a child with the same value never loses, which the tests check against every line of play of the opponent. The game tree has 549,946 nodes and 255,168 leaves: X wins 131,184 games, O wins 77,904, and 46,080 are draws.

**Solved games.**

| game | value with perfect play | level | by |
| --- | --- | --- | --- |
| tic-tac-toe | draw | strong | easy by hand or computer |
| Nim, any heaps | first player wins unless the XOR of the heaps is 0 | strong, by a formula | Bouton, see [Nim](/nim/) |
| Connect Four, 7 by 6 | first player wins | weak | James D. Allen and Victor Allis, independently, October 1988 |
| nine men's morris | draw | solved with databases of all midgame and endgame positions | Gasser 1996 |
| awari | draw | strong, all 889,063,398,406 positions | Romein and Bal 2002 and 2003 |
| checkers, 8 by 8 | draw | weak | Schaeffer et al. 2007 |
| Hex, $n$ by $n$ | first player wins | ultra-weak for every $n$, by strategy stealing; weak for small $n$ by computer | see [Hex](/hex-game/) |
| Othello, 8 by 8 | draw | weak, claimed | Takizawa 2023, a preprint that has not been checked by others |

For Connect Four, Allis also gave a strategy based on rules that a person can learn. The checkers project ran from 1989 to 2007. It used [endgame databases](/endgame-tablebase/) of all positions with 10 or fewer pieces, built by [retrograde analysis](/retrograde-analysis/), and a proof search from the start to these databases. Awari was solved by retrograde analysis on a parallel computer, which gives the value of every position.

**Non-example: chess.** Chess is not solved at any level. Its game-tree complexity is estimated at $10^{123}$ (Allis), and its number of positions is far beyond what can be stored. Only the positions with at most 7 pieces are strongly solved, as endgame tablebases; see [endgame solving](/endgame-solving/).

**Non-example: Go on the $19 \times 19$ board.** Programs play it better than any person, but its value is not known. Strong play is not a solution.

**Non-example: a game that is solved on paper only.** By Zermelo's theorem, the value of chess exists. Knowing that it exists is not even an ultra-weak solution, because the value itself is not known.

## Related definitions

- [Zermelo's theorem](/zermelo-theorem/): the value exists for every finite game of this kind.
- [Winning and losing states](/winning-losing-states/): the labels that a strong solution gives to every position.
- [Retrograde analysis](/retrograde-analysis/) and [endgame tablebase](/endgame-tablebase/): the method and the data structure of strong solutions.
- [Endgame solving](/endgame-solving/): the problem of solving one position.
- [Proof-number search](/proof-number-search/): a search that proves the value of a position without full width, used for weak solutions.
- [Strategy-stealing argument](/strategy-stealing-argument/): a proof of existence, which can give an ultra-weak solution.
- **State-space and game-tree complexity.** Allis compared games by the number of positions and by $b^d$ from the [branching factor](/branching-factor/); games with small values of both were the first to be solved.

## References
