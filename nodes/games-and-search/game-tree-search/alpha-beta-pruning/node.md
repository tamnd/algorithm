---
tag: AYQW86
kind: algorithm
slug: alpha-beta-pruning
name: Alpha-beta pruning
aliases:
- alpha-beta search
- alpha-beta
area: games-and-search/game-tree-search
level: core
summary: Minimax search that carries a window (alpha, beta) of useful values and skips every subtree that cannot change the root value. It returns the minimax value with fewer leaves.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth in plies}
  time: {worst: O(b^d), best: O(b^(d/2))}
  space: {extra: O(b d)}
properties: {deterministic: true, recursive: true}
prereqs: [negamax, pruning]
see_also: [knuth-moore-theorem, move-ordering, transposition-table, principal-variation-search, aspiration-search, mtdf, sss-star, best-move-selection]
sources:
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326; Section 2 (the procedures F1 and F2 in negamax form and the conditions on their results), Section 5 (history), Sections 6 and 7 (the best case and the worst case)
  - paper: doi:10.1145/358589.358616
    title: Judea Pearl, The solution for the branching factor of the alpha-beta pruning algorithm and its optimality, Communications of the ACM 25(8) (1982)
    locator: pp. 559 to 564 (the branching factor ξ_b/(1 - ξ_b) on random uniform trees, and its optimality among directional algorithms)
  - paper: doi:10.1016/0004-3702(80)90037-5
    title: Judea Pearl, Asymptotic properties of minimax trees and game-searching procedures, Artificial Intelligence 14(2) (1980)
    locator: pp. 113 to 138 (the random uniform tree model and the lower bound for directional algorithms)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson (2020)
    locator: Chapter 5, Section 5.2 (alpha-beta pruning and move ordering)
  - paper: "Timothy P. Hart and Daniel J. Edwards, The tree prune (TP) algorithm, MIT Artificial Intelligence Project Memo 30 (1961), revised as The alpha-beta heuristic (1963)"
    title: Hart and Edwards 1961
    locator: the whole memo (examples of the method with deep cutoffs, and Levin's count of the best case)
---

Alpha-beta pruning computes the [minimax](/minimax/) value of a game tree and skips the subtrees that cannot change it. The search carries a window $(\alpha, \beta)$. The value $\alpha$ is the score that the side to move is already sure of from an earlier move, and $\beta$ is the score above which the opponent will never let the game reach this node. When one move at a node scores $\beta$ or more, the other moves at that node need no search: this is a cutoff. With the full window $(-\infty, +\infty)$ the result is exactly the [negamax](/negamax/) value, so the program picks the same move as plain minimax. The saving depends on the order of the moves. In the best order a uniform tree of branching factor $b$ and depth $d$ needs only $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ of its $b^d$ leaves, and no algorithm can do with fewer ([Knuth-Moore theorem](/knuth-moore-theorem/)). For some leaf values it visits all of them. The general idea of a cutoff in a game tree is on [pruning](/pruning/).

## In plain words

You look at your moves one by one. After the first move you know a score you can surely get. Now you try a second move and look at the replies of your opponent. If one reply already leaves you worse off than your first move, you can stop with this second move: your opponent would choose that reply or a better one, so the second move is no good, and how bad it is exactly does not matter.

The same thing happens at every level of the tree, for both players. Each player brings down the best score that they already have somewhere above, and a branch is dropped as soon as it is clear that one of the two players will avoid it.

The answer is the same as when you look at every branch. If you try the good moves first, you drop most of the tree.

## The problem

The input is a finite [game tree](/game-tree/) of a two-player [zero-sum game](/zero-sum-game/) with perfect information, a function EVALUATE on the terminal nodes, and a window $(\alpha, \beta)$ with $\alpha < \beta$. As on the [negamax](/negamax/) page, every value is for the side to move at that node, and $N(n)$ is the negamax value of node $n$. The output is a number $r$ such that
- if $N(n) \le \alpha$ then $r \le \alpha$,
- if $\alpha < N(n) < \beta$ then $r = N(n)$,
- if $N(n) \ge \beta$ then $r \ge \beta$.

With $\alpha = -\infty$ and $\beta = +\infty$ the second case always applies, so the output is the value of the root. This is the [game tree evaluation](/game-tree-evaluation/) problem. The smaller windows are used inside the search, and also at the root by [aspiration search](/aspiration-search/), [principal variation search](/principal-variation-search/) and [MTD(f)](/mtdf/).

## The algorithm

```pseudo id=main
ALPHABETA(n, α, β)
L1  if n is terminal then return EVALUATE(n)
L2  m ← −∞                       ▷ fail-soft; the fail-hard form starts with m ← α
L3  for each child c of n, in order, do
L4      t ← −ALPHABETA(c, −β, −max(m, α))
L5      if t > m then m ← t
L6      if m ≥ β then return m   ▷ cutoff: the other children are skipped
L7  return m
```

The value $\max(m, \alpha)$ in line L4 is the best score that the side to move at $n$ already has, from this node or from a node above it. The child $c$ sees the window from the other side: it must beat $-\beta$ to matter to its parent's parent, and anything above $-\max(m, \alpha)$ is too good for the opponent to allow. So the window of the child is $(-\beta, -\max(m, \alpha))$, the window of the parent negated and swapped.

A cutoff whose bound comes from the parent is a *shallow* cutoff. A cutoff whose bound comes from a node two or more levels up is a *deep* cutoff. Line L4 passes both bounds down, so the procedure makes both kinds. Knuth and Moore call this procedure F2. Their procedure F1 passes only one bound and makes only the shallow cutoffs.

The two forms differ in line L2. In the *fail-hard* form, which is F2 of Knuth and Moore, $m$ starts at $\alpha$, so an inner node that fails low returns $\alpha$ itself. In the *fail-soft* form $m$ starts at $-\infty$, and a node that fails low returns the best score that it found, which is a tighter bound. Both forms visit the same leaves. The fail-soft form gives more information for the same work, and [transposition tables](/transposition-table/), [MTD(f)](/mtdf/) and [aspiration search](/aspiration-search/) use it.

## Example

Take a tree of depth 3 with MAX to move at the root A, MIN at B and C, and MAX at D, E, F and G. The leaves, as values for MAX, are 3 and 17 under D, 19 and 12 under E, 2 and 5 under G, and 15 and 25 under F. The children are searched in the order B, C at A, D, E at B and G, F at C. The table gives each node in the order in which it returns. The window is written for MAX; in the negamax form a MIN node gets the window $(-\beta, -\alpha)$ and returns the negated value.

| node | to move | window for MAX | values of the searched children | result (fail-soft) | result (fail-hard) |
| --- | --- | --- | --- | --- | --- |
| D | MAX | $(-\infty, +\infty)$ | 3, 17 | 17 | 17 |
| E | MAX | $(-\infty, 17)$ | 19, then cutoff | 19 | 19 |
| B | MIN | $(-\infty, +\infty)$ | 17, 19 | 17 | 17 |
| G | MAX | $(17, +\infty)$ | 2, 5 | 5 | 17 |
| C | MIN | $(17, +\infty)$ | 5, then cutoff | 5 | 17 |
| A | MAX | $(-\infty, +\infty)$ | 17, then C | 17 | 17 |

At E the first leaf is 19. MIN at B already has 17 from D, so MIN will never let the game reach a node worth 19 or more to MAX, and the leaf 12 is skipped. At C the first child G is worth at most 5 to MAX, and MAX already has 17 from B, so F with its leaves 15 and 25 is skipped. The search evaluates 5 of the 8 leaves, which is $2^2 + 2^1 - 1 = 5$, the minimum of the [Knuth-Moore theorem](/knuth-moore-theorem/) for $b = 2$ and $d = 3$. The root value is 17, the same as minimax.

The two forms differ only in the bound that a failed node returns. G fails low in the window $(17, +\infty)$. The fail-soft form returns 5, which says "the value of G is at most 5". The fail-hard form returns 17, which says only "the value of G is at most 17". The exact values are $G = 5$ and $C = 5$.

In tic-tac-toe from the empty board, with the squares tried in reading order, alpha-beta evaluates 7330 terminal positions. Plain minimax evaluates all 255168 of them. Both return 0, a draw.

## Correctness

The [proof](proofs/correctness/) shows the three cases of the problem statement by induction on the height of the node, in both forms. The key invariant is about line L5: while there is no cutoff, $\max(m, \alpha)$ is equal to $\max(\alpha, W)$, where $W$ is the best true score of the children searched so far. A child whose value lies inside its window returns that value exactly. A child that fails returns a bound that is on the far side of the window, so it does not change $\max(m, \alpha)$.

- **A cutoff.** The child that causes it returns $t \ge \beta$, so its true score is at least $\beta$, and so is the value of the node.
- **No cutoff.** Then $\max(r, \alpha) = \max(N(n), \alpha)$, which gives the exact value when it is above $\alpha$ and a value at most $\alpha$ when it is not.
- **Fail-soft bounds.** In the fail-soft form the result is itself a bound: $r \le \alpha$ implies $N(n) \le r$, and $r \ge \beta$ implies $N(n) \ge r$.

With the full window this gives the negamax value. The tests compare both forms with plain minimax on random uniform and irregular trees with integer and fraction leaves, check all the bound relations for random windows, check that the two forms evaluate the same leaves, and run tic-tac-toe positions against negamax.

## Complexity

The costs are in the [word RAM](/word-ram/), with each call of the move generator and of EVALUATE counted as $O(1)$, on a uniform tree of branching factor $b$ and depth $d$.

**Worst case.** If no cutoff happens, the search visits all $b^d$ leaves, the same as minimax. This happens when the leaf values put the value of every node strictly inside its window, with the children in increasing order of their score for the side to move. Knuth and Moore show that such values exist for every tree shape. To sort the children worst first is not enough from depth 4 on, because a child that is worse than the bound $\alpha$ from above can still cut off inside (see [Knuth-Moore theorem](/knuth-moore-theorem/)). So the time is $O(b^d)$.

**Best case.** If the first child of every node is a best move, alpha-beta evaluates exactly
$$ b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1 $$
leaves, about $2 b^{d/2}$. Knuth and Moore proved that every algorithm that finds the minimax value of a uniform tree must evaluate at least this many leaves, whatever the leaf values and the order, so this is optimal. In the same time, the search goes about twice as deep as minimax.

**Random trees.** Let the leaf values be independent with the same continuous distribution. Pearl (1982) proved that the expected number of leaves grows as $R_b^d$ with
$$ R_b = \frac{\xi_b}{1 - \xi_b}, $$
where $\xi_b$ is the positive root of $x^b + x - 1 = 0$, and that no directional algorithm has a smaller branching factor on this model. Some values:

| $b$ | 2 | 3 | 4 | 5 | 10 | 20 | 40 | 100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\xi_b$ | 0.618 | 0.682 | 0.724 | 0.755 | 0.835 | 0.894 | 0.934 | 0.967 |
| $R_b$ | 1.618 | 2.148 | 2.630 | 3.080 | 5.064 | 8.425 | 14.203 | 28.926 |
| $b^{3/4}$ | 1.682 | 2.280 | 2.828 | 3.344 | 5.623 | 9.457 | 15.905 | 31.623 |

The value $b^{3/4}$ is a good fit in this range, which is why it is often quoted, but it is not the limit: $R_b = \Theta(b / \ln b)$ as $b$ grows, and the exponent $\log R_b / \log b$ goes up from 0.69 at $b = 2$ to 0.73 at $b = 100$ and on toward 1. On random trees the saving is much smaller than with perfect ordering, which is why real programs work hard on [move ordering](/move-ordering/).

**Space.** At most $d + 1$ calls are active, so the space is $O(bd)$ with a list of children per call and $O(d)$ when the program makes and unmakes moves on one board.

## Properties

- **Exact.** With the full window it returns the minimax value. Inside a window it returns the value or a bound of known direction.
- **Directional.** It looks at the leaves from left to right, and its decision to look at a leaf depends only on the leaves to its left. Pearl's optimality result is for this class of algorithms.
- **Depends on the order.** The value does not depend on the order of the moves, but the work does, from about $2 b^{d/2}$ leaves to $b^d$.
- **Depth-first and small.** It needs only the current path, like minimax. [SSS*](/sss-star/) can skip more leaves, but it keeps a large list of open nodes.
- **Fail-soft costs nothing.** The fail-soft form visits the same leaves and returns tighter bounds.

## Variants and improvements

- **Shallow cutoffs only (F1).** Pass one bound and keep only the cutoffs against the parent. It is simpler and visits more leaves.
- **[Move ordering](/move-ordering/).** The [killer heuristic](/killer-heuristic/), the [history heuristic](/history-heuristic/) and the best move from a [transposition table](/transposition-table/) put good moves first and bring the search close to the best case.
- **[Iterative deepening](/iterative-deepening-search/).** Search to depth 1, 2, 3 and so on. Each search orders the next one, and the program can stop at any time; see [best move selection](/best-move-selection/).
- **Narrow windows.** [Aspiration search](/aspiration-search/) starts the root with a small window around a guess. [Scout](/scout-search/) and [principal variation search](/principal-variation-search/) test the later moves with a null window. [MTD(f)](/mtdf/) uses only null windows and a transposition table.
- **Best-first forms.** [SSS*](/sss-star/) never evaluates a leaf that alpha-beta skips; it is equivalent to a sequence of null-window alpha-beta searches with memory.
- **Unsafe pruning.** [Null-move pruning](/null-move-pruning/), [futility pruning](/futility-pruning/) and [late move reductions](/late-move-reductions/) skip more of the tree and can change the value.
- **[Parallel alpha-beta](/parallel-alpha-beta/).** Search the children of a node on several processors, with a cost in extra work.

## When to use it

Use alpha-beta, in the negamax form and with good move ordering, for any two-player zero-sum game with perfect information that is searched to a fixed depth with an [evaluation function](/evaluation-function/). It is the core of classical chess, checkers and Othello programs. Use plain [minimax](/minimax/) only for teaching or for very small trees. For games with chance nodes use [expectiminimax](/expectiminimax/), and for games with a large branching factor and no good evaluation function, [Monte Carlo tree search](/monte-carlo-tree-search/) is often better.

## Pitfalls

- **The window of the child.** It is $(-\beta, -\max(m, \alpha))$. Swapping the two values, or forgetting the negation, gives a search that runs and returns wrong values.
- **A bound is not a value.** A node that fails returns only a bound. Storing it as an exact value, for example in a [transposition table](/transposition-table/), gives wrong results later. Store a flag with it.
- **Root move choice.** At the root, a later move that fails low returns a value that can equal the best value so far. Change the best move only on a strict improvement, as on [best move selection](/best-move-selection/).
- **The test in line L6.** The test $m \ge \beta$ is correct. The test $m > \beta$ is also correct but prunes less. A test against $\alpha$ instead of $\beta$ is wrong.
- **Infinite values.** In two's complement integers, $-(\text{INT\_MIN})$ overflows. Use a value INF well inside the integer range, larger than every score.
- **Evaluation from a fixed side.** In the negamax form EVALUATE must score for the side to move, as on [negamax](/negamax/).
- **Mate scores and depth.** A score such as "win in $k$ moves" must change with the depth, or the window comparisons mix scores from different depths.

## Implementations

## History

In the history section of their paper, Knuth and Moore (1975) trace the idea to John McCarthy at the Dartmouth conference of 1956. Newell, Shaw and Simon (1958) published the first account of pruning in a game tree, but only of the one-sided form F1. Hart and Edwards gave examples with deep cutoffs in an MIT memo in 1961, and Michael Levin found the best case count in the same year, without a written proof. Alexander Brudno found the full method independently in the Soviet Union and published it with a proof in 1963. Slagle and Dixon (1969) gave a clear account in English. Knuth and Moore wrote the procedure in negamax form, proved the bounds on its result, proved the best case bound for all algorithms, and showed that the deep cutoffs first appear at the fourth level of the tree. The fail-soft form is usually credited to John Fishburn, who described it around 1980. Baudet (1978) gave bounds on the branching factor on random trees, and Pearl (1980, 1982) found its exact value and showed that it is optimal among directional algorithms.

## References
