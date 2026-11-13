---
tag: AJJEWV
kind: concept
slug: evaluation-function
name: Evaluation function
aliases:
- static evaluation
- heuristic evaluation
area: games-and-search/game-tree-search
level: advanced
summary: A function that scores a game position without search, as an estimate of its minimax value. A depth-limited search uses it at the positions where it stops.
prereqs: [minimax, game-tree]
see_also: [heuristic-function, quiescence-search, horizon-effect, expectiminimax, best-move-selection, temporal-difference-learning, monte-carlo-tree-search, endgame-tablebase]
sources:
  - paper: doi:10.1080/14786445008521796
    title: Claude E. Shannon, Programming a computer for playing chess, Philosophical Magazine, Series 7, 41(314) (1950)
    locator: pp. 256 to 275 (the approximate evaluating function f(P) with material, pawn structure and mobility terms, and its use at the end of a search of fixed depth)
  - paper: doi:10.1147/rd.33.0210
    title: Arthur L. Samuel, Some studies in machine learning using the game of checkers, IBM Journal of Research and Development 3(3) (1959)
    locator: pp. 210 to 229 (a scoring polynomial for checkers whose terms and weights the program learns from play)
  - paper: doi:10.1016/0004-3702(82)90002-9
    title: Dana S. Nau, An investigation of the causes of pathology in games, Artificial Intelligence 19(3) (1982)
    locator: pp. 257 to 278 (game tree models in which a deeper search with an evaluation function gives worse decisions)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 5, Section 5.3 (heuristic alpha-beta tree search, evaluation functions as weighted sums of features, and the cutoff test)
---

An evaluation function scores a position of a game without looking ahead. A search for a game like chess cannot reach the ends of the game, so it stops at some depth and calls the evaluation function at the positions where it stops. The scores take the place of the true outcomes, and the search computes the [minimax](/minimax/) value of the cut tree from them. A good evaluation function sorts positions in the same order as their true values, so that the move it points to is a good one. It is not the same as a [heuristic function](/heuristic-function/) in single-agent search: that one estimates the cost from a state to a goal, and its main property is that it does not overestimate. An evaluation function estimates who is winning and by how much, and the search only uses the order of its scores, not a bound.

## In plain words

When you play chess, you cannot think through every game to the end. You think a few moves ahead, look at the board you would get, and judge it: who has more pieces, whose pieces can move more freely, whose king is safe.

An evaluation function is that judgment written as a formula. It gives each board a number: large when White is doing well, small when Black is. The program looks a few moves ahead, scores the boards it reaches, and plays toward the best score that the opponent cannot prevent.

The scores are guesses. A board in the middle of an exchange of pieces looks good or bad depending on the exact moment, so programs score only calm boards. And a better guess is worth more than a deeper search with a bad one.

## The idea

### What it is

An evaluation function is a map $e$ from positions to numbers. In the minimax form, $e(p)$ is the score for MAX; in the [negamax](/negamax/) form, it is the score for the player to move at $p$, so $e_{\text{negamax}}(p) = \pm e(p)$ with the sign of the side to move. A depth-limited search computes
$$ V_d(p) = \begin{cases} \mathrm{UTILITY}(p) & p \text{ terminal}, \\ e(p) & d = 0, \\ \max_c V_{d-1}(c) \text{ or } \min_c V_{d-1}(c) & \text{otherwise}, \end{cases} $$
and plays the move that gives the best $V_{d-1}$ at the root. "Static" means that $e$ looks at the position only, with no moves played. Terminal positions keep their exact outcome, and the scale of $e$ should place a sure win above every non-terminal score.

### The usual form

Most hand-made evaluation functions are weighted sums of features:
$$ e(p) = w_1 f_1(p) + w_2 f_2(p) + \cdots + w_k f_k(p). $$
Each feature $f_i$ is a count that is easy to compute, such as the difference in material, mobility or pawn structure. Shannon (1950) gave this example for chess:
$$ f(P) = 200(K - K') + 9(Q - Q') + 5(R - R') + 3(B - B' + N - N') + (P - P') - 0.5(D - D' + S - S' + I - I') + 0.1(M - M') + \cdots $$
Here $K, Q, R, B, N, P$ count the white kings, queens, rooks, bishops, knights and pawns, $D, S, I$ count the doubled, backward and isolated white pawns, $M$ is the number of legal white moves, and the primed letters count the same things for Black. Shannon said that the weights 0.5 and 0.1 were only his rough estimate. Samuel (1959) let a checkers program choose terms and adjust their weights from its own play. Later programs learn the whole function, for example with [temporal difference learning](/temporal-difference-learning/) or with a neural network trained on game results.

### What matters about it

- **Only the order counts in minimax.** If $g$ is strictly increasing, then $g \circ e$ gives the same move at every depth: max and min commute with $g$. The minimax tests check this on random trees. The numbers matter only for cutoff margins in pruning and for comparisons between iterations.
- **With chance nodes, the scale counts.** [Expectiminimax](/expectiminimax/) takes averages, and averages do not commute with $g$. The evaluation must then be a linear function of the expected outcome, such as a win probability.
- **Quiet positions only.** A score in the middle of an exchange is wrong by a whole piece. Programs extend the search at such positions with [quiescence search](/quiescence-search/). A search that stops just before a loss that it could have seen one ply deeper shows the [horizon effect](/horizon-effect/).
- **Speed against accuracy.** The function runs at almost every leaf, so a cheap one allows a deeper search. Designers trade terms against depth.
- **Deeper is not always better.** In some models of game trees, with an evaluation whose errors are independent at each leaf, a deeper search chooses worse moves; Nau (1982) called this pathology and studied its causes. In real games such as chess, deeper search helps, because the positions near each other in the tree have related values.
- **Exact values.** In positions that are solved, the program can use the exact value from an [endgame tablebase](/endgame-tablebase/) in place of the estimate.

### Against a heuristic function

| | evaluation function | heuristic function |
| --- | --- | --- |
| setting | a game for two players | search for a goal by one agent |
| estimates | the outcome for MAX (or the player to move) | the cost from a state to a goal |
| key property | sorts positions like their true values | admissible (never too high) or consistent |
| used where | at the positions where a depth-limited search stops | to order or to prune the search, as in A* |
| scale | arbitrary for minimax, linear for chance nodes | in units of path cost |

## Examples

**Material in chess.** With Shannon's function, a position where White has an extra knight and the rest is equal scores 3. A position where White has a queen and Black a rook in its place, and White has two doubled pawns while Black has none, scores $9 - 5 - 0.5 \cdot 2 = 3$, before mobility.

**Open lines in tic-tac-toe.** Let $e(p)$ be the number of lines (rows, columns, diagonals) with no O in them, minus the number of lines with no X. The empty board scores 0. An X in the centre scores $8 - 4 = 4$, because the centre lies on four lines and takes them from O; an X in a corner scores 3, and an X on an edge scores 2. A search of depth 2 with this function, with X to move on the empty board, finds the values 1 for the centre, $-1$ for a corner and $-2$ for an edge, and plays the centre. After X takes a corner, a search of depth 1 for O scores the replies: the centre $-1$, the far corners 0, and the edges next to X 1. So O replies in the centre, which is the only reply that draws. The scores were computed by a short script. This function is crude: it does not see a threat of two in a row, which a deeper search must find.

**Scale with chance.** MAX chooses between move A, which leads with probability $\frac12$ each to positions scored 0 and 6, and move B, which leads for sure to a position scored 4. The expected scores are 3 for A and 4 for B, so MAX plays B. Square every score, which keeps the order of positions: A now gives $\frac12 (0 + 36) = 18$ and B gives 16, so MAX plays A. With no chance node, squaring would not change any choice.

## Where it is used

- **Depth-limited search.** Every [alpha-beta](/alpha-beta-pruning/) program for chess, checkers or Othello calls an evaluation function at its leaves, and [best move selection](/best-move-selection/) at the root depends on it.
- **Move ordering.** A cheap evaluation of the children sorts them before the search, which helps alpha-beta to cut off early.
- **Forward pruning.** Futility pruning and similar methods skip moves whose static score plus a margin cannot reach the current bound; see [pruning in game trees](/pruning/).
- **Monte Carlo tree search.** [MCTS](/monte-carlo-tree-search/) can replace the evaluation by random playouts, or use a learned evaluation (a value network) in place of the playout.

## References
