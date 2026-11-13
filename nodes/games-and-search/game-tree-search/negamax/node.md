---
tag: XN376A
kind: algorithm
slug: negamax
name: Negamax
aliases:
- negamax search
area: games-and-search/game-tree-search
level: core
summary: Minimax for two-player zero-sum games written as one rule, v(n) = max over children of -v(child), with every value taken from the point of view of the side to move.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth in plies}
  time: {worst: O(b^d), best: O(b^d)}
  space: {extra: O(b d)}
properties: {deterministic: true, recursive: true}
prereqs: [minimax, zero-sum-game]
see_also: [alpha-beta-pruning, principal-variation-search, best-move-selection, evaluation-function, game-tree-evaluation, knuth-moore-theorem, transposition-table, mtdf]
sources:
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326 (the negamax formulation of the value of a position, and the procedures F1 and F2 written in that form)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: the part on game-playing programs (the minimax value of game trees and the search procedures that compute it)
  - paper: doi:10.1080/14786445008521796
    title: Claude E. Shannon, Programming a computer for playing chess, Philosophical Magazine, Series 7, 41(314) (1950)
    locator: pp. 256 to 275 (the minimax rule with an evaluating function for chess)
---

Negamax is the [minimax algorithm](/minimax/) for two-player [zero-sum games](/zero-sum-game/) written with one rule instead of two. Every value is taken from the point of view of the player to move at the node, and the value of a node is
$$ N(n) = \max_{c} \bigl(-N(c)\bigr) $$
over its children $c$. The rule works because in a zero-sum game a value $x$ for one player is the value $-x$ for the other, and $\min(a, b) = -\max(-a, -b)$. It returns the same numbers as minimax, up to the sign of the player to move, and it costs the same. Most game programs write minimax and [alpha-beta pruning](/alpha-beta-pruning/) in this form, because it has half the code and no branch on the player.

## In plain words

In a game where one player's gain is the other's loss, a score that is good for me is bad for you by the same amount. So both players can use the same question: "what is the best I can get from here?"

To answer it, look at each move you can make. After the move it is your opponent's turn, and you ask the same question for them. Whatever the best is for them, flip its sign, and that is what the move gives you. Take the move with the largest flipped score.

You never need to remember whose side a score is on, because each score belongs to the player to move. The only care needed is at the end of the game: the final score must also be given for the player who would move next.

## The problem

The input is a finite [game tree](/game-tree/) of a zero-sum game for two players with [perfect information](/perfect-information-game/), and a function EVALUATE on the terminal nodes. On this page every value, also the one that EVALUATE returns, is from the point of view of the player to move at that node. If $u(t)$ is the outcome for MAX, then EVALUATE$(t) = u(t)$ when MAX would move at $t$ and $-u(t)$ when MIN would. The output is the value of the root for the player to move there. This is the [game tree evaluation](/game-tree-evaluation/) problem, and the minimax value $V$ follows as $V = N$ when MAX moves at the root and $V = -N$ when MIN moves.

## The algorithm

```pseudo id=main
NEGAMAX(n)
L1  if n is terminal then return EVALUATE(n)
L2  v ← −∞
L3  for each child c of n do v ← max(v, −NEGAMAX(c))
L4  return v
```

The procedure has no player flag. The player is implicit in the position, and the minus sign in line L3 changes the point of view at each move. An evaluation function that scores for a fixed player, for example White in chess, must be multiplied by $+1$ or $-1$ for the side to move before line L1 returns it.

## Example

Take the tree of the [minimax](/minimax/) page: MAX moves at A, MIN at B and C, MAX at D, E, F and G, and the outcomes for MAX are the leaves 3, 17 under D, 2, 12 under E, 15, 25 under F and 2, 5 under G. MIN would move at the leaves, so EVALUATE returns the negated outcomes: $-3, -17, -2, -12, -15, -25, -2, -5$.

| node | to move | values $-N(c)$ of the children | $N(n)$ |
| --- | --- | --- | --- |
| D | MAX | 3, 17 | 17 |
| E | MAX | 2, 12 | 12 |
| F | MAX | 15, 25 | 25 |
| G | MAX | 2, 5 | 5 |
| B | MIN | $-17$, $-12$ | $-12$ |
| C | MIN | $-25$, $-5$ | $-5$ |
| A | MAX | 12, 5 | 12 |

At B the value for MIN is $-12$, that is 12 for MAX, as on the minimax page. The root value is 12 for MAX, and the best move from A is to B, the child with $-N(B) = N(A)$.

In tic-tac-toe with the board X X _ / O O _ / _ _ _ and X to move, NEGAMAX returns $+1$, a win for X. If EVALUATE wrongly returns the result for X at every leaf, the same call returns $-1$. The tests run both calls.

## Correctness

The [proof](proofs/correctness/) shows by induction on the height that NEGAMAX(n) $= s(n)\, V(n)$, where $V$ is the minimax value for MAX and $s(n)$ is $+1$ when MAX moves at $n$ and $-1$ when MIN moves.

- **Leaves.** EVALUATE returns $s(t)\, u(t)$ by its definition.
- **Inner nodes.** The children have the opposite sign, so $-N(c) = s(n)\, V(c)$. At a MAX node the maximum of these is $\max_c V(c) = V(n)$. At a MIN node it is $\max_c (-V(c)) = -\min_c V(c) = -V(n)$.

So negamax and minimax pick the same best moves, and their root values agree, with a sign change when MIN moves at the root. The tests check this exact agreement, and a level-by-level brute force, on random uniform trees with $b$ from 2 to 4 and $d$ from 1 to 6 and on random irregular trees.

## Complexity

The costs are in the [word RAM](/word-ram/), with each call of the move generator and of EVALUATE counted as $O(1)$. Negamax is minimax with a different sign convention, so it has the same costs.

**Time.** One call per node, so $b^d$ leaves and $\Theta(b^d)$ time on a uniform tree of branching factor $b$ and depth $d$, in every case.

**Space.** At most $d + 1$ active calls, so $O(bd)$ with a list of children per call and $O(d)$ when the program makes and unmakes moves on one board.

The saving is in the code, not in the time. Each node does one negation more than in minimax, and a branch on the player less.

## Properties

- **Same values as minimax.** The value is for the side to move, and the best move is the same.
- **One code path.** There is no copy of the loop for the second player, so the two branches cannot drift apart when the code changes.
- **Needs a zero-sum game with two players.** The rule depends on the value for one player being the negation of the value for the other. A constant-sum game works after a shift of the values to sum zero.
- **Needs a symmetric value range.** The negation must map the set of values to itself.

## Variants and improvements

- **Negamax with alpha-beta.** Search with a window $(\alpha, \beta)$, call each child with $(-\beta, -\alpha)$, and cut off when $v \ge \beta$. This is how Knuth and Moore wrote their procedure F2; see [alpha-beta pruning](/alpha-beta-pruning/).
- **Negamax with a color.** Pass $\sigma = \pm 1$ and return $\sigma \cdot$ EVALUATE$(t)$ at the leaves, when EVALUATE scores for a fixed player.
- **[Principal variation search](/principal-variation-search/) and [MTD(f)](/mtdf/).** Faster searches with null windows, almost always written in negamax form.
- **Negamax with a [transposition table](/transposition-table/).** Stored values are for the side to move in the stored position, so they can be reused without a sign change in that position.

## When to use it

Use negamax as the default way to write any minimax search of a two-player zero-sum game with alternate moves. Use the two-branch [minimax](/minimax/) form for teaching, when the players are not symmetric in the code, or when a move can leave the same player to move. Do not use negamax for games with more than two players or for games that are not zero-sum.

## Pitfalls

- **Evaluation from a fixed side.** The most common bug. EVALUATE must score for the side to move. The example above shows the wrong sign at once.
- **Overflow of the infinity.** In two's complement integers, $-(\text{INT\_MIN})$ overflows. Use a value $-\text{INF}$ with $\text{INF}$ much less than the largest integer, so that $-v$ is always defined.
- **Mate scores.** A score such as "win in $k$ moves" must change by one at each ply as it goes up, or the program prefers a slow win. With negamax the change and the sign change go together.
- **Turns that do not alternate.** If a move can leave the same player to move, as in a pass that keeps the turn, do not negate for that move.
- **Draws and terminal nodes.** A draw is 0 for both players, which is fine. A terminal value that is not symmetric, such as a draw worth $+1$ for one side, breaks the rule.

## Implementations

## History

The minimax rule goes back to von Neumann and to Shannon (1950), who proposed it for chess. Knuth and Moore (1975) gave the value of a position as the maximum of the negated values of its successors, and wrote their alpha-beta procedures F1 and F2 in that form. Their paper made the negamax form the standard for the analysis of alpha-beta and for game programs. Later searches such as NegaScout and MTD(f) are given in this form.

## References
