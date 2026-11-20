---
tag: WQZKXN
kind: algorithm
slug: ellipsoid-against-hope
name: Ellipsoid against hope
aliases:
- Papadimitriou-Roughgarden algorithm
area: algorithmic-game-theory/computing-equilibria
level: research
summary: Computes a correlated equilibrium of a succinct multiplayer game in polynomial time by running the ellipsoid method on an infeasible dual.
model: real-ram
complexity:
  vars: {n: the number of players, k: the largest number of pure strategies of a player, L: the bit length of the game description}
  time: {worst: "poly(n, k, L)"}
  space: {extra: "poly(n, k, L)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2005
  people: [Christos H. Papadimitriou, Tim Roughgarden, Albert Xin Jiang, Kevin Leyton-Brown]
  note: "Papadimitriou (2005) and Papadimitriou and Roughgarden (journal version 2008) gave the algorithm. Stein, Parrilo and Ozdaglar found that its numerical steps may fail to give an exact equilibrium, and Jiang and Leyton-Brown (2015) fixed it with an oracle that returns pure profiles."
prereqs: [correlated-equilibrium-linear-program, ellipsoid-method, lp-duality, stationary-distribution]
see_also: [correlated-equilibrium, graphical-game, potential-game, nash-equilibrium-computation, blum-mansour-reduction, regret-matching, separating-hyperplane-theorem, zero-sum-game-linear-programming]
sources:
  - paper: doi:10.1145/1379759.1379762
    title: "Christos H. Papadimitriou and Tim Roughgarden, Computing correlated equilibria in multi-player games, Journal of the ACM 55(3) (2008), article 14"
    locator: "the main theorem (a correlated equilibrium in polynomial time for succinct games of polynomial type with a polynomial expected utility algorithm), the lemma that every dual point has a product distribution with zero expected dual value, and the hardness of optimal correlated equilibria"
  - paper: doi:10.1016/j.geb.2013.02.002
    title: "Albert Xin Jiang and Kevin Leyton-Brown, Polynomial-time computation of exact correlated equilibrium in compact games, Games and Economic Behavior 91 (2015), 347-359"
    locator: the purified separation oracle (a pure profile found by the method of conditional probabilities) and the exact equilibrium with polynomial support
  - paper: "Sergiu Hart and David Schmeidler, Existence of correlated equilibria, Mathematics of Operations Research 14(1) (1989), 18-25"
    title: Existence of correlated equilibria
    locator: the existence proof by LP duality that the algorithm makes constructive
---

Ellipsoid against hope computes a [correlated equilibrium](/correlated-equilibrium/) of a game with many players in time polynomial in the size of a succinct description, such as a [graphical game](/graphical-game/), a polymatrix game or a congestion game. The [correlated equilibrium LP](/correlated-equilibrium-linear-program/) has one variable for each pure profile, which is exponentially many in the number of players, so it cannot even be written down for such games. Its dual has only $\sum_i k_i(k_i - 1)$ variables, and it is infeasible, because a correlated equilibrium exists. The algorithm runs the [ellipsoid method](/ellipsoid-method/) on this infeasible dual, "against hope", and records the constraints that cut it. These constraints correspond to a polynomial number of profiles, and an LP restricted to them has a solution, which is a correlated equilibrium. The algorithm is due to Papadimitriou and Roughgarden (2008); the form given here, with a pure-profile oracle, is the exact version of Jiang and Leyton-Brown (2015). It finds some correlated equilibrium, not one of maximum welfare; for many succinct classes that optimization problem is NP-hard. Learning methods such as the [Blum-Mansour reduction](/blum-mansour-reduction/) and [regret matching](/regret-matching/) also work on succinct games, but give only approximate equilibria.

## In plain words

Writing down a correlated equilibrium directly means giving a chance to every combination of moves, and with many players there are far too many combinations. So the method works on the other side of the problem. There, a candidate is a small table of weights, one for each player and each pair of moves, that would prove that no correlated equilibrium exists. Such a proof is impossible, since an equilibrium always exists. The method still searches for one with the ellipsoid method. Each time, it finds a single combination of moves that shows the current candidate is wrong. After a polynomial number of rounds the search has run out of room, and the few combinations that it found are enough: a small linear program over just those combinations finds the equilibrium.

## The problem

The input is a game with players $1, \ldots, n$, strategy sets $S_i$ with $|S_i| = k_i \le k$, and utilities $u_i$ (maximized), given in a succinct form of bit length $L$. The game must be of *polynomial type* ($n$ and $k$ are polynomial in $L$) and have a polynomial *expected utility algorithm*: given a product distribution $x = x_1 \times \cdots \times x_n$, it computes $\mathbb{E}_{s \sim x}[u_i(s)]$ in time polynomial in $L$. Graphical games, polymatrix games, congestion games and many other classes qualify. The output is a correlated equilibrium, given as a list of polynomially many profiles with their probabilities.

Write $U$ for the matrix of the incentive constraints. It has a row for each player $i$ and ordered pair $j \ne l$ in $S_i$, a column for each profile $s$, and the entry $u_i(s) - u_i(l, s_{-i})$ if $s_i = j$ and 0 otherwise. A distribution $p$ on profiles is a correlated equilibrium exactly when $Up \ge 0$. For a dual vector $y \ge 0$ with one entry $y_i(j, l)$ per row, the value of column $s$ is

$$g(y, s) = (U^\top y)_s = \sum_{i=1}^{n} \sum_{l \ne s_i} y_i(s_i, l)\,\big[u_i(s) - u_i(l, s_{-i})\big].$$

The primal LP "maximize $\sum_s p(s)$ subject to $Up \ge 0$, $p \ge 0$" is unbounded, because a correlated equilibrium exists and can be scaled. So by [LP duality](/lp-duality/), its dual system

$$y \ge 0, \qquad g(y, s) \le -1 \text{ for every profile } s$$

is infeasible. It has $d = \sum_i k_i(k_i - 1) \le n k^2$ variables and one constraint per profile.

## The algorithm

```pseudo id=main
ELLIPSOID-AGAINST-HOPE(G)
L1  E ← a ball of radius R around 0 in the space of the dual vectors y; X ← the empty set
L2  repeat
L3      y ← the center of E
L4      if y_r < 0 for some coordinate r, then cut E by the halfspace y_r ≥ 0
L5      else
L6          s ← ORACLE(y)                 ▷ a pure profile with g(y, s) ≥ 0
L7          add s to X, and cut E by the halfspace g(·, s) ≤ g(y, s)
L8          p ← a correlated equilibrium with support in X, from an LP, if one exists
L9          if p exists, return p
```

A cut replaces $E$ by the smallest ellipsoid that contains the half of $E$ on the given side of a hyperplane through its center. The oracle of line L6 works in two steps.

1. For each player $i$, the weights $y_i(j, l)$ define a continuous-time Markov chain on $S_i$ with rate $y_i(j, l)$ from $j$ to $l$. Let $x_i$ be a [stationary distribution](/stationary-distribution/) of this chain, so that $x_i(j) \sum_l y_i(j, l) = \sum_l x_i(l)\, y_i(l, j)$ for every $j$. Then for the product $x = x_1 \times \cdots \times x_n$, the expected value $\mathbb{E}_{s \sim x}\, g(y, s)$ is exactly 0. This is the key lemma of Papadimitriou and Roughgarden.
2. Fix the players one at a time. For player $i$, choose the strategy $a$ that maximizes the conditional expectation of $g(y, s)$, given the strategies already fixed and $s_{i+1}, \ldots, s_n$ drawn from $x$. The maximum is at least the average, so the conditional expectation never drops below 0, and the final pure profile has $g(y, s) \ge 0$. This step is the derandomization of Jiang and Leyton-Brown. Each conditional expectation is a sum of expected utilities under product distributions, so it uses the expected utility algorithm.

Since $g(y, s) \ge 0 > -1$, the profile $s$ gives a dual constraint that the center violates, and line L7 is a valid cut for the dual system. The original analysis runs the ellipsoid method for a fixed polynomial number of steps $N$, after which the volume argument shows that the cuts already make the dual infeasible, and then solves the LP of line L8 once. The code checks the LP each time $X$ grows, and stops at the first success.

## Example

Take chicken with strategies D = 0 and C = 1, and payoffs (D, D) = (0, 0), (D, C) = (7, 2), (C, D) = (2, 7), (C, C) = (6, 6). The dual vector is $y = (y_1(\text{D}, \text{C}), y_1(\text{C}, \text{D}), y_2(\text{D}, \text{C}), y_2(\text{C}, \text{D}))$, so $d = 4$. Start with the ball of radius $R = 10$.

| step | center $y$ | stationary $x_1$, $x_2$ | oracle profile $s$ | column of $s$ in $U$ | $g(y, s)$ | LP on $X$ |
|---|---|---|---|---|---|---|
| 1 | (0, 0, 0, 0) | any, say (1, 0), (1, 0) | (D, D) | (-2, 0, -2, 0) | 0 | infeasible |
| 2 | (1.414, 0, 1.414, 0) | (0, 1), (0, 1) | (D, C) | (1, 0, 0, 2) | 1.414 | $p(\text{D}, \text{C}) = 1$ |

In step 1 the oracle returns (D, D), and the cut keeps the half where $-2y_1(\text{D}, \text{C}) - 2y_2(\text{D}, \text{C}) \le 0$. For a ball, the new center moves a distance $R/(d + 1) = 2$ away from the cut hyperplane, along the unit vector $(1, 0, 1, 0)/\sqrt{2}$, so it is $(1.414, 0, 1.414, 0)$. At this center both chains flow only from D to C, so the stationary distributions sit on C. Starting from the product (C, C), player 1 compares $g$ at (D, C), which is $1.414 \cdot (7 - 6)$, with $g$ at (C, C), which is 0, and picks D; player 2 then picks C. The LP on $X = \{(\text{D}, \text{D}), (\text{D}, \text{C})\}$ finds the pure Nash equilibrium (D, C), which is a correlated equilibrium.

## Correctness

If line L9 returns $p$, then $p$ is a correlated equilibrium, because the LP of line L8 has exactly the incentive constraints, restricted to profiles in $X$. The oracle is correct by the two lemmas above, whose proofs are short: for a stationary $x_i$, the balance equations make $\sum_j x_i(j) \sum_l y_i(j, l)\,[v(j) - v(l)] = 0$ for any values $v$, which gives the first lemma after averaging over $s_{-i}$, and the second is the method of conditional expectations. The method terminates because of Farkas' lemma: if the cuts collected in $X$, together with $y \ge 0$, already form an infeasible system, then the LP of line L8 is feasible. Papadimitriou and Roughgarden, and in the exact form Jiang and Leyton-Brown, show with the volume argument of the ellipsoid method that this happens after a number of steps polynomial in $d$ and in the bit length of the constraints. The proof file proves the lemmas and the Farkas step; the step count is cited.

## Complexity

The ellipsoid method runs in dimension $d \le n k^2$. Each step costs one oracle call: $n$ stationary distributions of $k$-state chains, in $O(n k^3)$ time, and $O(n k)$ conditional expectations, each made of a polynomial number of calls to the expected utility algorithm. The number of steps is polynomial in $d$ and in the bit length of the payoffs, and so is $|X|$. The final LP has $|X|$ variables and $d + 1$ constraints. The total is polynomial in $n$, $k$ and $L$. The output has polynomial support: it is a distribution on at most $|X|$ pure profiles.

The code on this page is for games in normal form, where the conditional expectations sum over all profiles; one oracle call then costs $O(n k \cdot k^n)$. The ellipsoid steps use floating point, and the final LP is exact.

## Properties

- **Polynomial for succinct games.** For a game of polynomial type with a polynomial expected utility algorithm, the time is polynomial in the description, not in the number of profiles.
- **Exact.** The pure-profile oracle of Jiang and Leyton-Brown keeps all numbers of polynomial bit length, and the returned distribution satisfies the incentive constraints exactly.
- **Small support.** The equilibrium is supported on the polynomially many profiles in $X$.
- **Not optimizing.** It finds some correlated equilibrium. Maximizing welfare over the correlated equilibria is NP-hard for several succinct classes (Papadimitriou and Roughgarden, 2008), and those results also cover other linear objectives.

## Variants and improvements

- **Mixtures of product distributions.** The original version of Papadimitriou and Roughgarden used the product distributions $x$ themselves as cuts and returned a convex combination of them. Stein, Parrilo and Ozdaglar showed that this version can fail to give an exact equilibrium, because of the numerical precision of these cuts. The pure-profile oracle removes this problem.
- **Approximate equilibria by learning.** If every player runs a no-swap-regret algorithm, the empirical distribution of play is an approximate correlated equilibrium after a number of rounds polynomial in $n$, $k$ and $1/\varepsilon$, using the same expected utility algorithm in each round.
- **Coarse correlated equilibria.** The same scheme works with the smaller dual of the coarse constraints, which has one variable $y_i(l)$ per player and strategy. There, the product of the distributions $x_i$ proportional to $y_i$ has expected dual value 0, and no Markov chain is necessary.
- **Two players or a table.** When the normal form is given, the [correlated equilibrium LP](/correlated-equilibrium-linear-program/) is simpler and can optimize.

## When to use it

Use it when a game has many players but a short description with a fast expected utility algorithm, and an exact correlated equilibrium is needed. It is mainly of theoretical interest: the ellipsoid method is slow in practice, and for an approximate answer, no-regret learning is much simpler. For games given as a table, use the LP directly.

## Pitfalls

- **Expecting an optimal equilibrium.** Line L9 returns the first correlated equilibrium supported on $X$, not one of maximum welfare. Adding an objective to line L8 only optimizes over the support $X$.
- **A product distribution as the cut in line L7.** Cutting with $\mathbb{E}_x g(\cdot, s)$ for the product $x$ instead of a pure profile is the original version, which can fail to give an exact equilibrium because of numerical precision. Use a pure profile from the conditional expectations.
- **A wrong stationary distribution in line L6.** If a chain is reducible, a solution of the linear balance equations can have negative entries. Restrict the computation to a closed class of the chain, where the stationary distribution is unique and positive.
- **Stopping too early.** With a fixed small number of steps, the LP of line L8 can still be infeasible. The step bound must come from the bit lengths, or the LP must be checked as $X$ grows, as in the code.

## Implementations

The Python code implements lines L1 to L9 for games in normal form: central-cut ellipsoid steps in floating point, the stationary distributions on a closed class by Gaussian elimination, the conditional expectations by summing over the remaining profiles, and the LP of line L8 with the shared exact simplex code. The tests check the balance equations of the stationary step, that the oracle profile always violates its dual constraint, the unique correlated equilibria of matching pennies, rock-paper-scissors and the prisoner's dilemma, that the output on 40 random games with 2 and 3 players is an exact correlated equilibrium supported on $X$, and that restricted LPs can be infeasible.

## History

Hart and Schmeidler (1989) proved the existence of correlated equilibria with LP duality. Papadimitriou (2005) turned this proof into a polynomial-time algorithm for succinct games, and the journal version with Roughgarden (2008) gave the full analysis and hardness results for optimal correlated equilibria. Stein, Parrilo and Ozdaglar noticed a gap in the precision of the original method, and Jiang and Leyton-Brown (2015) closed it with the pure-profile oracle.

## References
