---
tag: ZW9A3T
kind: problem
slug: peg-solitaire
name: Peg solitaire
aliases:
- Solitaire
- Hi-Q
area: games-and-search/puzzles
level: intro
summary: "Jump pegs over neighbours into empty holes, removing the peg jumped, until one is left; position classes and pagoda functions prove games impossible, and the general problem is NP-complete."
prereqs: [depth-first-search, state-space]
see_also: [generic-backtracking-algorithm, memoization, duplicate-detection, invariant, np-complete, linear-programming-problem, breadth-first-search, lights-out-puzzle]
sources:
  - book: isbn:9780198532033
    title: "John D. Beasley, The Ins and Outs of Peg Solitaire, Oxford University Press, 1985"
    locator: "the whole book; boards, position classes, pagoda functions, and the 18-move central game"
  - book: isbn:9781568811444
    title: "Elwyn R. Berlekamp, John H. Conway and Richard K. Guy, Winning Ways for Your Mathematical Plays, volume 4, 2nd edition, A K Peters, 2004"
    locator: "chapter 23, Purging Pegs Properly, from p. 803; central solitaire, position classes, pagoda functions and the solitaire army"
  - paper: "Ryuhei Uehara and Shigeki Iwata, Generalized Hi-Q is NP-complete, The Transactions of the IEICE E73(2), 1990"
    locator: "pp. 270-273; NP-completeness on n x n boards with a given start and a given final hole"
---

Peg solitaire is a one-player puzzle on a board of holes filled with pegs, in which a move jumps a peg over an orthogonal neighbour into an empty hole and removes the peg jumped over, and the goal is usually to leave a single peg. On the 33-hole English board the central game starts with only the centre empty and must end with one peg in the centre; it takes 31 jumps, and the fewest moves, counting a chain of jumps by one peg as one move, is 18 (Bergholt 1912, proved optimal by Beasley in 1964). Position classes and pagoda functions prove many games impossible without search, and deciding whether a given start can be reduced to one peg in a given hole is [NP-complete](/np-complete/) (Uehara and Iwata 1990).

## In plain words

You have a board of holes, every hole but one filled with a peg. A move takes one peg, jumps it over a neighbouring peg in a straight line into an empty hole just beyond, and removes the peg it jumped over. Each move takes away exactly one peg, so the game always ends. You win if only one peg is left, often in a hole chosen in advance. Some starting positions cannot be won, and two simple tricks show this. One colours the holes in a repeating pattern and watches how a jump changes the colour counts. The other gives each hole a weight so that no jump can increase the total weight of the pegs. For other positions you must search through possible moves, and for large boards that search can take a very long time.

## Definition

**Board.** A finite set $B$ of holes in the square grid $\mathbb{Z}^2$. The English board is the cross of 33 holes $\{(x, y) : |x| \le 3, |y| \le 3, \min(|x|, |y|) \le 1\}$; the French board adds the four holes $(\pm 2, \pm 2)$ and has 37.

**Positions.** A position is the set $P \subseteq B$ of holes with a peg, so there are $2^{|B|}$ positions.

**Jumps.** If $a$, $b = a + d$ and $c = a + 2d$ are holes for a unit vector $d \in \{(\pm 1, 0), (0, \pm 1)\}$, with $a, b \in P$ and $c \notin P$, the jump $(a, b, c)$ gives $P - \{a, b\} + \{c\}$. The English board has 76 possible jumps. A *move* is a chain of consecutive jumps by the same peg.

**Problem.** Given a board, a start position $S$ and a goal position $G$, often a single peg in a given hole, decide whether a sequence of jumps turns $S$ into $G$, and find one, or one with the fewest moves.

Every jump removes one peg, so a game from $S$ to $G$ has exactly $|S| - |G|$ jumps, and the [state space](/state-space/) is a directed acyclic graph layered by the number of pegs.

## Variants

- **Boards.** The English 33-hole board, the French 37-hole board, the 15-hole triangle (with jumps in the six directions of the triangular grid), and rectangles.
- **Start and finish.** A *single-vacancy to single-survivor* game starts with one hole empty and ends with one peg; the *central game* uses the centre for both. Other games end with a given pattern.
- **Fewest moves.** Count moves rather than jumps. The 31 jumps of the central game group into at least 18 moves.
- **Diagonal jumps.** Allowing jumps along diagonals gives more games, with different invariants.
- **Conway's soldiers.** Pegs start below a line in the infinite plane, and the question is how far above the line one peg can reach.
- **Generalized boards.** Uehara and Iwata study $n \times n$ boards with an arbitrary start and a given final hole.

## Examples

**The central game.** A [depth-first search](/depth-first-search/) on the English board, from all holes full except $(0, 0)$, finds a sequence of 31 jumps that ends with the one peg at $(0, 0)$. The solution the search finds has 27 moves; the shortest has 18.

**Reversal.** If a jump $(a, b, c)$ turns $P$ into $P'$, then the same jump turns the complement $B \setminus P'$ into $B \setminus P$: in $B \setminus P'$ the holes $a, b$ are full and $c$ is empty. So a game from $S$ to $G$, played backwards with pegs and holes swapped, is a game from $B \setminus G$ to $B \setminus S$. For the central game these are the same start and finish, so every solution read backwards is another solution.

**Small boards by exhaustive search.** A [breadth-first search](/breadth-first-search/) over all positions reachable from each single vacancy gives:

| board | holes | jumps | vacancies that can end with one peg |
|---|---|---|---|
| triangle, side 4 | 10 | 18 | 6 (all but the three corners and the centre) |
| triangle, side 5 | 15 | 36 | all 15 |
| rectangle $3 \times 3$ | 9 | 12 | 0 |
| rectangle $3 \times 4$ | 12 | 20 | 8 |
| rectangle $4 \times 4$ | 16 | 32 | 8 |
| rectangle $3 \times 5$ | 15 | 28 | 2 |

The centre of the 10-hole triangle has no jump into it, so that game cannot start.

## Known algorithms

- **Depth-first search with dead positions.** Search jump sequences depth first, as in [backtracking](/generic-backtracking-algorithm/), and store every position from which the goal was shown unreachable. Since the state space is acyclic, [memoization](/memoization/) of failures is safe, and each position is expanded at most once, so the search costs $O(2^N \cdot J)$ time for $N$ holes and $J$ jumps. Positions that differ by a symmetry of the board can share one entry, as in [duplicate detection](/duplicate-detection/).
- **Breadth-first search by layers.** All positions with $k$ pegs form one layer, and each layer depends only on the one before. A forward search from $S$ and, by the reversal rule, a forward search from $B \setminus G$ can meet in the middle layer.
- **Pruning by position class.** A position whose class differs from the class of the goal is dropped at once.
- **Pruning by pagoda functions.** If a pagoda function gives the current position less weight than the goal, the position is dropped. A pagoda function that separates a start from a goal is a feasible point of a [linear program](/linear-programming-problem/) with one inequality per jump, so it can be computed rather than guessed.

## Bounds

**Position classes.** For a position $P$ let $s_k$ be the number of pegs on holes with $x + y \equiv k \pmod 3$, and $t_k$ the number with $x - y \equiv k \pmod 3$. A jump touches three consecutive holes in a row or column, which have three different values of $x + y \bmod 3$ and three different values of $x - y \bmod 3$, and changes each of the three by one. So every jump flips the parity of all of $s_0, s_1, s_2$ and of all of $t_0, t_1, t_2$, and the four parities of $s_0 + s_1$, $s_1 + s_2$, $t_0 + t_1$, $t_1 + t_2$ are an [invariant](/invariant/). They split the positions into 16 classes, and no sequence of jumps leaves a class.

- On the English board the central start is in the class of a single peg at exactly five holes: $(0, 0)$, $(\pm 3, 0)$ and $(0, \pm 3)$. A one-peg finish of the central start can only be at one of them.
- On the French board the central start is in the class of no single peg. So the central game on the French board has no solution, and no search is needed to show it.

**Pagoda functions.** A pagoda function is a weight $w : B \to \mathbb{R}$ with $w(a) + w(b) \ge w(c)$ for every jump $(a, b, c)$. A jump replaces the weights $w(a) + w(b)$ by $w(c)$, so the total weight $w(P) = \sum_{p \in P} w(p)$ never increases. If $w(S) < w(G)$, the game from $S$ to $G$ is impossible.

**Conway's soldiers.** Let $\varphi = (1 + \sqrt 5)/2$, so $\varphi^{-1} + \varphi^{-2} = 1$, and put $w(p) = \varphi^{-d(p)}$ on the infinite plane, with $d(p)$ the grid distance from $p$ to a target $t$. This is a pagoda function: a jump straight toward $t$ removes the weights $\varphi^{-(e+2)} + \varphi^{-(e+1)}$ and adds $\varphi^{-e}$, which is equal, and every other jump removes more weight than it adds. Take $t$ five rows above the line $y = 0$ and pegs only at $y \le 0$. Row $y$ contributes $\varphi^{-(5 - y)}(1 + 2\sum_{k \ge 1} \varphi^{-k}) = \varphi^{-(5 - y)} \varphi^3$, and the rows together give $\varphi^3 \cdot \varphi^{-5} \cdot \varphi^2 = 1 = w(t)$. A finite army has weight less than 1, so no peg can reach the fifth row.

**Length.** A game has at most $|B| - 1$ jumps, so a solution is a certificate of polynomial length, and the problem is in NP. Uehara and Iwata proved it NP-complete.

**Fewest moves.** The central game on the English board needs 18 moves. Bergholt gave an 18-move solution in 1912, and Beasley proved in 1964 that no shorter one exists.

## Reductions

- **Reachability in an implicit DAG.** A game is a path in the layered acyclic graph of positions, so any search for paths in an implicit graph applies, and the reversal rule turns a question about the goal into a question about a start.
- **NP-hardness.** Uehara and Iwata reduce a known NP-complete problem to the generalized puzzle on $n \times n$ boards with a given start and a given final hole.
- **Invariants and weights.** Position classes are linear invariants over $\mathbb{Z}_2$, like the parity rule of the [Lights Out puzzle](/lights-out-puzzle/), and pagoda functions are solutions of a system of linear inequalities, one per jump, so these impossibility proofs reduce to linear algebra and linear programming.

## Applications

- A test domain for search methods on acyclic state spaces, with a fixed depth and many transpositions.
- A classroom example of invariants: the position class argument and Conway's soldiers prove impossibility without enumerating any games.
- A source of hard instances for NP-complete search, with sizes that grow with the board.

## References
