---
tag: 4KA77P
kind: algorithm
slug: minimax
name: Minimax algorithm
aliases:
- minimax search
- minimax
area: games-and-search/game-tree-search
level: intro
summary: Computes the value of a finite two-player zero-sum game tree by taking the maximum at MAX nodes and the minimum at MIN nodes, from the leaves up.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth in plies}
  time: {worst: O(b^d), best: O(b^d)}
  space: {extra: O(b d)}
properties: {deterministic: true, recursive: true}
prereqs: [game-tree, zero-sum-game, depth-first-search]
see_also: [negamax, alpha-beta-pruning, best-move-selection, evaluation-function, game-tree-evaluation, zermelo-theorem, expectiminimax, knuth-moore-theorem]
sources:
  - paper: doi:10.1080/14786445008521796
    title: Claude E. Shannon, Programming a computer for playing chess, Philosophical Magazine, Series 7, 41(314) (1950)
    locator: pp. 256 to 275 (the minimax rule applied to a tree cut off at a fixed depth with an approximate evaluating function, and the type A and type B strategies)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 5, Section 5.2 (the minimax value, the MINIMAX-SEARCH function, its cost, and the three-ply example tree with value 3)
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326 (the definition of the minimax value of a game tree and its negamax form, as the base of the alpha-beta analysis)
  - book: isbn:9780691130613
    title: John von Neumann and Oskar Morgenstern, Theory of Games and Economic Behavior, commemorative edition
    locator: the chapter on zero-sum two-person games, the part on games in which perfect information prevails
---

The minimax algorithm computes the value of a finite [game tree](/game-tree/) for two players who move in turn, in a [zero-sum game](/zero-sum-game/) with [perfect information](/perfect-information-game/). On this page all values are from the point of view of the player MAX. At a node where MAX moves, the value is the largest value of a child; at a node where MIN moves, it is the smallest. The algorithm walks the tree depth first and gives each node this value from the leaves up. It always looks at every node, so it costs $\Theta(b^d)$ on a tree of [branching factor](/branching-factor/) $b$ and depth $d$, and [alpha-beta pruning](/alpha-beta-pruning/) is the usual way to get the same value for less.

## In plain words

Two players take turns in a game, and every possible future of the game is drawn as a tree. At the bottom of the tree, each finished game has a score. One player wants the score high, the other wants it low.

To know what a position is worth, look at the positions one move away. If it is the high player's turn, the position is worth the best of those. If it is the low player's turn, it is worth the worst of those, because that player will pick it. Do this from the bottom up, and the top of the tree gets a number. That number is what the first player can count on if both play as well as possible. The method does not guess what the other player will do; it assumes the other player always makes the best reply.

## The problem

The input is a finite game tree. Each node is a position, and the flag max-to-move says who moves there. Each terminal node $t$ has a number $\mathrm{UTILITY}(t)$, the outcome for MAX. The output is the minimax value $V(\text{root})$, defined by $V(t) = \mathrm{UTILITY}(t)$ at a terminal node, $V(n) = \max_c V(c)$ at a MAX node and $V(n) = \min_c V(c)$ at a MIN node, over the children $c$. This is the [game tree evaluation](/game-tree-evaluation/) problem. To get a move instead of a number, see [best move selection](/best-move-selection/).

In a real game the tree is too big, so programs stop at a fixed depth and score the positions there with an [evaluation function](/evaluation-function/). The algorithm is the same; the leaves are then the cut-off positions, and the result is the minimax value of the cut-off tree, not of the game.

## The algorithm

```pseudo id=main
MINIMAX(n, max-to-move)
L1  if n is terminal then return UTILITY(n)
L2  if max-to-move then
L3      v ← −∞
L4      for each child c of n do v ← max(v, MINIMAX(c, false))
L5  else
L6      v ← +∞
L7      for each child c of n do v ← min(v, MINIMAX(c, true))
L8  return v
```

The first call is MINIMAX(root, true) when MAX moves first. Lines L3 and L6 start with the neutral element of max and min, so a node with one child gets the value of that child. A non-terminal node has at least one child, so the infinite start value never comes back. The [negamax](/negamax/) form writes the two branches as one, with values from the side to move.

## Example

The tree has depth 3 and branching factor 2. MAX moves at the root A, MIN at B and C, and MAX again at D, E, F and G. The leaves are the outcomes for MAX.

| node | player | children | value |
| --- | --- | --- | --- |
| D | MAX | leaves 3, 17 | 17 |
| E | MAX | leaves 2, 12 | 12 |
| F | MAX | leaves 15, 25 | 25 |
| G | MAX | leaves 2, 5 | 5 |
| B | MIN | D, E | min(17, 12) = 12 |
| C | MIN | F, G | min(25, 5) = 5 |
| A | MAX | B, C | max(12, 5) = 12 |

The value is 12, and the best play is A to B, B to E, E to the leaf 12. The largest leaf, 25, is under C, but MAX does not go to C, because MIN would reply with G and hold MAX to 5. The search makes 15 calls and evaluates all 8 leaves. With MIN to move at the root, the same tree has the value 3.

In the three-ply tree of Russell and Norvig, with the MIN nodes [3, 12, 8], [2, 4, 6] and [14, 5, 2] under a MAX root, the MIN values are 3, 2 and 2 and the root value is 3.

For tic-tac-toe, MINIMAX on the empty board visits 549,946 nodes, evaluates 255,168 finished games and returns 0, so the game is a draw with best play. After X takes the centre, 25,872 games remain and the value is still 0. The tests run both counts; see [solved game](/solved-game/) for the whole game.

## Correctness

The [proof](proofs/correctness/) shows two facts by induction on the height of a node.

- **The value is computed.** MINIMAX(n) returns $V(n)$. At a terminal node line L1 returns the utility. At a MAX node, after the loop of line L4 has seen the children $c_1, \ldots, c_i$, the variable $v$ holds $\max(V(c_1), \ldots, V(c_i))$, and after the last child it holds $V(n)$. The MIN case is the same.
- **The value is guaranteed.** If MAX always moves to a child with the same value, then against any play of MIN the outcome is at least $V(n)$, because a MIN move can only go to a child of value at least $V(n)$. In the same way MIN can hold the outcome to at most $V(n)$. So $V(n)$ is both the max-min and the min-max over pure strategies, which is [Zermelo's theorem](/zermelo-theorem/) in numbers.

## Complexity

The costs are in the [word RAM](/word-ram/), with each call of the move generator and of UTILITY counted as $O(1)$. The cost of a game-tree search is the number of leaves it evaluates.

**Time.** MINIMAX calls itself once on each node of the tree, in every case. On a uniform tree it evaluates exactly $b^d$ leaves, and the number of calls is the node count of a uniform tree given on [search tree](/search-tree/). So the best case and the worst case are both $\Theta(b^d)$. On a tree that is not uniform, the time is linear in the number of nodes.

**Space.** The search is a [depth-first search](/depth-first-search/), so at most $d + 1$ calls are active. If each call holds the list of its children, the space is $O(bd)$. If the move generator gives one child at a time, or the program makes and unmakes moves on one board, it is $O(d)$.

**How it compares.** A deterministic algorithm must read all leaves in the worst case, but on a good move order [alpha-beta pruning](/alpha-beta-pruning/) reads only $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves and gets the same value, which is the bound of the [Knuth-Moore theorem](/knuth-moore-theorem/). Minimax is therefore never better than alpha-beta, and on good move orders it is much worse.

## Properties

- **Exact.** It returns the value of the tree it is given, with no error from pruning or sampling.
- **Visits every node.** The cost does not depend on the order of the children, and the order does not change the value.
- **Unchanged by monotone changes of the leaves.** If every leaf value is replaced by $f(\text{value})$ for a strictly increasing $f$, each node value becomes $f$ of its old value, so the best move does not change. [Expectiminimax](/expectiminimax/) does not have this property.
- **Pessimistic.** It assumes a perfect opponent. Against a weak opponent it does not prefer moves that give the opponent more ways to go wrong.
- **Tree, not graph.** It has no memory of positions, so a position that can be reached by several move orders is searched once for each order.

## Variants and improvements

- **[Negamax](/negamax/).** One branch instead of two, with values from the side to move and $V(n) = \max_c (-V(c))$.
- **Depth-limited minimax.** Stop at depth $d$ and call an [evaluation function](/evaluation-function/) there. Shannon called the full-width form a type A strategy. [Quiescence search](/quiescence-search/) and [search extensions](/search-extensions/) deal with the [horizon effect](/horizon-effect/) that the fixed depth causes.
- **[Alpha-beta pruning](/alpha-beta-pruning/).** Skip the subtrees that cannot change the root value. It returns the same value. See [pruning in game trees](/pruning/) for the sound and the unsound kinds of cutoff.
- **Minimax with a table.** Store the value of each position in a [transposition table](/transposition-table/), so that a game graph is searched once per position. On a whole game graph with a counter per node this becomes [retrograde analysis](/retrograde-analysis/).
- **Chance nodes.** [Expectiminimax](/expectiminimax/) takes the expected value at chance nodes, for games with dice or cards.
- **More than two players.** The max^n rule of Luckhardt and Irani (1986) gives each node a vector of values, one per player, and lets the player to move pick the child best for that player.

## When to use it

Use plain minimax when the tree is small enough to search in full, as for tic-tac-toe or the endgame of a small game, or as a reference to test faster searches such as alpha-beta, [principal variation search](/principal-variation-search/) or [MTD(f)](/mtdf/). It is the simplest correct method, and its result is the definition that the faster ones must match. For any larger game, use alpha-beta with good [move ordering](/move-ordering/), or [Monte Carlo tree search](/monte-carlo-tree-search/) when no good evaluation function exists.

## Pitfalls

- **Utilities from the wrong side.** In minimax every leaf is a value for MAX. If the evaluation function gives a value for the side to move, negate it at MIN leaves, or use negamax. Mixing the two conventions gives wrong values without an error.
- **The flag is not the depth parity.** In games where a player can move twice, or pass, the player to move must come from the position, not from the depth.
- **Infinite trees.** A game with repeated positions has an infinite game tree. Without a depth limit or a rule that ends repeated play, the recursion does not stop.
- **Deep recursion.** In Python the default recursion limit is about 1,000 frames. Long games need a larger limit or an explicit stack.
- **Value is not the move.** The root value does not say which move to play; the program must keep the move, and how ties are broken changes the move but not the value. See [best move selection](/best-move-selection/).
- **Cut-off value is not the game value.** With an evaluation function at the depth limit, the result is only as good as the evaluation, and on some random tree models a deeper search plays worse (game tree pathology, on [evaluation function](/evaluation-function/)).

## Implementations

## History

Zermelo (1913) studied chess as a finite game and asked whether a player can force a win; see [Zermelo's theorem](/zermelo-theorem/) for what he proved. Von Neumann (1928) proved the [minimax theorem](/minimax-theorem/) for matrix games, and von Neumann and Morgenstern (1944) showed that a game with perfect information has a value in pure strategies, found by working back from the end. Shannon (1950) proposed to play chess by computer with this rule on a tree cut off at a fixed depth and scored by an evaluation function, and he estimated that the full chess tree is far too big to search. Knuth and Moore (1975) wrote the minimax value in the negamax form for their analysis of alpha-beta. The textbook of Russell and Norvig presents MINIMAX-SEARCH as the base of adversarial search.

## References
