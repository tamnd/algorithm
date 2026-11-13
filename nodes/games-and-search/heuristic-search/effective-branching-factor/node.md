---
tag: D83533
kind: definition
slug: effective-branching-factor
name: Effective branching factor
aliases:
- EBF
- b*
area: games-and-search/heuristic-search
level: core
summary: The branching factor b* that a uniform tree of the solution depth d would need to hold the N nodes that a search generated, from N + 1 = 1 + b* + ... + (b*)^d. A measured statistic of a run.
prereqs: [branching-factor, heuristic-function, bisection-method]
see_also: [heuristic-dominance, a-star-search, iterative-deepening-a-star, search-tree, admissible-heuristic, pattern-database, sliding-tile-puzzle, geometric-series]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.6.1 (the effect of heuristic accuracy on performance, the definition of b* and the example of 52 nodes at depth 5)
  - paper: doi:10.1016/S0004-3702(01)00094-7
    title: Richard E. Korf, Michael Reid and Stefan Edelkamp, Time complexity of iterative-deepening-A*, Artificial Intelligence 129(1-2) (2001)
    locator: pp. 199 to 218 (the brute-force branching factor of regular search spaces, the prediction of IDA* expansions from the distribution of heuristic values, and the result that the heuristic branching factor equals the brute-force one)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 5 (the brute-force branching factor of search trees and the prediction of the search effort of IDA*)
---

The effective branching factor $b^*$ of a search run is a number that sums up how many nodes the run generated, relative to the depth of the solution that it found. If the run generated $N$ nodes and found a solution at depth $d$, then $b^*$ is the branching factor that a uniform tree of depth $d$ would need in order to hold $N + 1$ nodes, the root included. So $b^*$ solves $N + 1 = 1 + b^* + (b^*)^2 + \cdots + (b^*)^d$, which is solved numerically, for example by bisection. A search that walks straight to the goal has $b^* = 1$, and a blind search of a uniform tree has $b^*$ close to its true [branching factor](/branching-factor/). Russell and Norvig use $b^*$ to compare [heuristic functions](/heuristic-function/): the closer to 1, the better the heuristic on that problem. It is a measured statistic of one run on one instance, not a property of the problem.

## Definition

Let a search find a solution at depth $d \ge 1$ after it has generated $N \ge d$ nodes, the start not counted. The **effective branching factor** of the run is the unique real number $b^* \ge 1$ with

$$ \sum_{i=1}^{d} (b^*)^i = N. $$

This is the same as $N + 1 = 1 + b^* + \cdots + (b^*)^d$, the form of Russell and Norvig. Some authors count expanded nodes instead of generated ones. A page or a paper must say which count it uses, and it should average over many instances of each depth, since one run says little.

**Fact 1 (existence, uniqueness and bounds).** For $N \ge d \ge 1$, the number $b^*$ exists, is unique and satisfies

$$ \left(\frac{N}{d}\right)^{1/d} \le b^* \le N^{1/d}. $$

*Proof.* The function $S(b) = b + b^2 + \cdots + b^d$ is continuous and strictly increasing on $b \ge 0$, with $S(1) = d \le N$ and $S(b) \to \infty$. So $S(b) = N$ has exactly one root, and it is at least 1. For $b \ge 1$ the largest term is $b^d$, so $b^d \le S(b) \le d\, b^d$. At $b = b^*$ this gives $(b^*)^d \le N \le d\,(b^*)^d$, which are the two bounds. $\square$

**Fact 2 (bisection).** Start with $[\ell, u] = [1, N]$, where $S(1) \le N \le S(N)$. At each step evaluate $S$ at the midpoint $m$ and keep the half in which $S - N$ changes sign. After $k$ steps the interval has width $(N - 1)/2^k$ and contains $b^*$, so its midpoint is within $\tau$ of $b^*$ as soon as $k \ge \log_2((N - 1)/(2\tau))$. With rational arithmetic and Horner's rule each evaluation costs $O(d)$ operations and the result is exact to the stated tolerance, see [the bisection method](/bisection-method/). The implementation of [A*](/a-star-search/) has a function `effective_branching_factor(n, d, tol)` that works this way with Python fractions.

## Examples and non-examples

- **The example of Russell and Norvig.** $N = 52$ and $d = 5$. With exact fractions, $S(1.9167) = 51.9967\ldots < 52$ and $S(1.9168) = 52.0078\ldots > 52$, so $b^*$ lies between 1.9167 and 1.9168. Bisection to the tolerance $10^{-6}$ gives $1.916729\ldots$, which rounds to the value 1.92 of the book.
- **Exact cases.** A complete binary tree of depth 10 has $N = 2 + 4 + \cdots + 2^{10} = 2046$ nodes below the root, so $b^* = 2$. For $N = 30$ and $d = 2$, $5 + 25 = 30$ gives $b^* = 5$. A search that generates only the $d$ nodes of the solution path has $N = d$ and $b^* = 1$.
- **The same $N$ at different depths.** For $N = 1000$, $b^*$ is about 3.7421 at $d = 5$, 1.8459 at $d = 10$ and 1.3155 at $d = 20$. So a value of $b^*$ means nothing without its depth, and values of $b^*$ for runs of different depths are not directly comparable.
- **The brute-force branching factor of the 8-puzzle.** Without a heuristic and with moves back to the parent pruned, the number of nodes in the search tree of the 8-puzzle grows by factors of 2 and 1.5 in turn, counted exactly by the moves of the blank. So the asymptotic branching factor is $\sqrt{3} \approx 1.732$, and $b^*$ of a blind search tends to it as $d$ grows. This number is a property of the space, not of a run.
- **Measured values for two heuristics.** The page [heuristic dominance](/heuristic-dominance/) gives $b^*$ of A* on seeded 8-puzzle instances with the misplaced tiles and with the Manhattan distance. The heuristic that dominates has the smaller $b^*$ at each depth.
- **Not the branching factor of a game.** The [branching factor](/branching-factor/) of a game tree is the number of legal moves at a node, or its average. It is a property of the game. The effective branching factor is computed from the work of one search and changes with the heuristic, the tie rule, the instance and the depth.
- **Not the ratio of two layers.** The ratio of the nodes at depth $i + 1$ to those at depth $i$ in a search tree is a local growth rate. The value $b^*$ fits one number to the whole run, so a run with a large first layer and small later layers can have the same $b^*$ as a uniform tree.

## Related definitions

- **[Branching factor](/branching-factor/).** The number of children of a node, of a game tree or of a [search tree](/search-tree/).
- **Brute-force branching factor.** The limit of the ratio of the number of nodes at depth $d$ to those at depth $d - 1$ in the tree that a search without a heuristic generates. Korf, Reid and Edelkamp (2001) compute it exactly for regular spaces such as the sliding tile puzzles.
- **Heuristic branching factor.** The same ratio for the nodes that IDA* expands with a heuristic. Korf, Reid and Edelkamp showed that, for a consistent heuristic, it tends to the brute-force branching factor as the depth grows. A heuristic lowers the effective depth of the search, not the base of its growth. With $N_i = b^i$ in the formula below, the number of expansions is about a constant fraction of $b^d$, so $b^*$ is below $b$ at moderate depths but tends to $b$ as $d$ grows.
- **Prediction from the heuristic distribution.** Korf, Reid and Edelkamp predict the number of IDA* expansions as $\sum_{i=0}^{d} N_i P(d - i)$, where $N_i$ is the number of nodes at depth $i$ of the brute-force tree and $P(x)$ is the fraction of states with $h \le x$ in the equilibrium distribution. This replaces $b^*$ when the aim is to predict effort, not to sum it up.
- **[Heuristic dominance](/heuristic-dominance/).** A heuristic that dominates another expands no more states, up to ties, so its $b^*$ on the same instances is no larger, when $N$ counts expanded states.

## References
