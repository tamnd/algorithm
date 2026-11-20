---
tag: MQFKCA
kind: algorithm
slug: power-index-dynamic-programming
name: Power indices by dynamic programming
aliases:
- generating function method for voting power
area: algorithmic-game-theory/cooperative-games
level: core
summary: Computes the Banzhaf and Shapley-Shubik indices of a weighted voting game in time pseudo-polynomial in the weights by counting coalitions.
model: word-ram
complexity:
  vars: {n: the number of players, q: the quota}
  time: {worst: O(n^3 q), banzhaf: O(n^2 q)}
  space: {extra: O(n q)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1962
  people: [Irwin Mann, Lloyd S. Shapley, Tomomi Matsui, Yasuko Matsui]
  note: Mann and Shapley computed the Shapley-Shubik index of the Electoral College exactly in 1962. Matsui and Matsui surveyed the counting algorithms for both indices and their running times in 2000.
prereqs: [weighted-voting-game, shapley-shubik-index, banzhaf-index, knapsack-dynamic-programming]
see_also: [subset-sum-problem, knapsack-problem, power-index-hardness, pseudo-polynomial-time, weak-np-hardness, polynomial-multiplication, shapley-value-sampling, marginal-contribution-nets]
sources:
  - paper: doi:10.15807/jorsj.43.71
    title: "Tomomi Matsui and Yasuko Matsui, A survey of algorithms for calculating power indices of weighted majority games, Journal of the Operations Research Society of Japan 43(1) (2000), 71-86"
    locator: the dynamic programming algorithms for the Banzhaf and Shapley-Shubik indices and their running times in terms of the number of players and the weights
  - book: isbn:9781608456529
    title: Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Morgan and Claypool, 2011
    locator: Chapter 4, Weighted voting games (the pseudo-polynomial algorithm for the power indices and the hardness for large weights)
  - paper: doi:10.1007/BF01753703
    title: "Kislaya Prasad and Jerry S. Kelly, NP-completeness of some problems concerning voting games, International Journal of Game Theory 19(1) (1990), 1-9"
    locator: the hardness results that make a pseudo-polynomial algorithm the best one can expect
  - paper: doi:10.1287/moor.19.2.257
    title: "Xiaotie Deng and Christos H. Papadimitriou, On the complexity of cooperative solution concepts, Mathematics of Operations Research 19(2) (1994), 257-266"
    locator: the #P-completeness of the Shapley value of weighted voting games and the remark that it is pseudo-polynomial
---

This algorithm computes the [Banzhaf](/banzhaf-index/) and [Shapley-Shubik](/shapley-shubik-index/) indices of a [weighted voting game](/weighted-voting-game/) $[q; w_1, \ldots, w_n]$ with integer weights exactly. Both indices only need, for each player $i$ and each size $s$, the number of coalitions of the other players with size $s$ whose weight lies in the window $[q - w_i, q - 1]$. A table indexed by size and weight, filled like the table of the [0/1 knapsack](/knapsack-dynamic-programming/) dynamic program, gives these counts. The running time is $O(n^2 q)$ arithmetic operations per player, polynomial in $n$ and in the value of the quota but not in its number of digits, so the algorithm is [pseudo-polynomial](/pseudo-polynomial-time/). That is the best one can expect: with weights in binary, both indices are #P-complete ([hardness of power indices](/power-index-hardness/)).

## In plain words

A player has power in a coalition when the coalition is just short of the quota, and the player's weight pushes it over. So we need to know how many groups of the other players have a total weight just below the quota. We build a table that says, for each group size and each total weight, how many groups of the other players have that size and weight. We add the players one by one, as in the knapsack table. Then we read off the groups whose weight is short of the quota by less than the player's weight. Their number gives the Banzhaf index, and their numbers by size give the Shapley-Shubik index.

## The problem

The input is a weighted voting game: integer weights $w_1, \ldots, w_n \ge 0$ and an integer quota $q$ with $1 \le q \le w(N)$, where $w(S) = \sum_{j \in S} w_j$. A coalition $S$ wins if $w(S) \ge q$. A set $S \subseteq N \setminus \{i\}$ is a *swing* of player $i$ if $w(S) < q \le w(S) + w_i$. The output, for each player $i$, is:

- the number $\eta_i$ of swings of $i$;
- the raw Banzhaf index $\beta'_i = \eta_i / 2^{n-1}$, and the normalized index $\eta_i / \sum_j \eta_j$;
- the Shapley-Shubik index $\varphi_i = \sum_{S \text{ a swing of } i} |S|!\,(n - |S| - 1)!/n!$.

## The algorithm

For a player $i$, the table $C[s][k]$ counts the sets $S \subseteq N \setminus \{i\}$ with $|S| = s$ and $w(S) = k$, for $0 \le k \le q - 1$. Sets of weight $q$ or more are never needed, so the table stops at $q - 1$.

```pseudo id=main
POWER-INDICES(w, q, i)                  ▷ the indices of player i in [q; w_1, ..., w_n]
L1  C[s][k] ← 0 for 0 ≤ s ≤ n-1 and 0 ≤ k ≤ q-1; C[0][0] ← 1
L2  for each player j ≠ i do
L3      for s ← n-2 downto 0 do              ▷ downward, so row s is still the old row
L4          for k ← q-1-w_j downto 0 do
L5              C[s+1][k+w_j] ← C[s+1][k+w_j] + C[s][k]
L6  c_s ← the sum of C[s][k] for max(0, q-w_i) ≤ k ≤ q-1, for each 0 ≤ s ≤ n-1
L7  β'_i ← (c_0 + c_1 + ... + c_{n-1}) / 2^(n-1)
L8  φ_i ← the sum over 0 ≤ s ≤ n-1 of s! (n-1-s)! / n! · c_s
L9  return (c_0 + ... + c_{n-1}, β'_i, φ_i)
```

Run it once for each player, and divide the swing counts by their total for the normalized Banzhaf index. If $w_j \ge q$, the loop of line L4 is empty: every set that contains $j$ has weight at least $q$ and is never counted.

## Example

Take $[51; 50, 49, 1]$ and player 1, with $w_1 = 50$. The other weights are 49 and 1. The table starts with $C[0][0] = 1$.

- Add player 2 ($w_2 = 49$). For $s = 1$ nothing is stored yet. For $s = 0$, line L5 sets $C[1][49] = 1$.
- Add player 3 ($w_3 = 1$). For $s = 1$, line L5 adds $C[1][49]$ to $C[2][50]$, so $C[2][50] = 1$. For $s = 0$, it adds $C[0][0]$ to $C[1][1]$, so $C[1][1] = 1$.

The nonzero entries are $C[0][0] = 1$ (the empty set), $C[1][1] = 1$ ($\{3\}$), $C[1][49] = 1$ ($\{2\}$) and $C[2][50] = 1$ ($\{2, 3\}$). The window is $\max(0, 51 - 50) = 1 \le k \le 50$, so $c_0 = 0$, $c_1 = 2$ and $c_2 = 1$. Player 1 has 3 swings, and

$$\beta'_1 = \frac{3}{4}, \qquad \varphi_1 = \frac{1!\,1!}{3!} \cdot 2 + \frac{2!\,0!}{3!} \cdot 1 = \frac{1}{3} + \frac{1}{3} = \frac{2}{3}.$$

For player 2 ($w_2 = 49$), the other weights are 50 and 1. The set $\{1, 3\}$ has weight 51 and is never stored. The window is $2 \le k \le 50$, which holds only $\{1\}$ with weight 50, so $c_1 = 1$, $\beta'_2 = 1/4$ and $\varphi_2 = 1/6$. Player 3 is the same by symmetry of the game. The swings are $3, 1, 1$, the normalized Banzhaf index is $(3/5, 1/5, 1/5)$ and the Shapley-Shubik index is $(2/3, 1/6, 1/6)$.

For the Council of the EEC in 1958, $[12; 4, 4, 4, 2, 2, 1]$, the same steps give the swing counts $(10, 10, 10, 6, 6, 0)$ and the Shapley-Shubik index $(7/30, 7/30, 7/30, 3/20, 3/20, 0)$.

## Correctness

The invariant of the loop of line L2 is that $C[s][k]$ counts the subsets of the players handled so far with size $s$ and weight $k$, for every $k \le q - 1$. Adding player $j$ splits each new set into the sets without $j$ (the old entry) and the sets with $j$ (the old entry at size $s - 1$ and weight $k - w_j$). The downward loop of line L3 makes every read of row $s$ see the old value, because row $s$ is written only later, at the step $s - 1$. Dropping the sets of weight $q$ or more is safe, because adding players never lowers a weight. At the end, the window of line L6 is exactly the set of weights of the swings of $i$. The Shapley-Shubik index is the Shapley value of the game, and its subset formula groups the swings by size, which gives line L8. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

- **Time per player.** Lines L2 to L5 run $n - 1$ times over $n - 1$ rows and at most $q$ columns, so $O(n^2 q)$ additions. Lines L6 to L8 add $O(n q)$ more. All $n$ players take $O(n^3 q)$.
- **Banzhaf only.** Without the size index, the table is one row of length $q$, filled as in the [subset sum](/subset-sum-problem/) counting program, in $O(n q)$ per player and $O(n^2 q)$ for all players.
- **Space.** $O(n q)$ numbers for the table, or $O(q)$ for the Banzhaf index alone.
- **Number size.** The counts reach $\binom{n-1}{s} < 2^{n-1}$, so they have up to $n$ bits. On a word RAM with $w$-bit words, each addition costs $O(\lceil n / w \rceil)$ word operations, which adds this factor to the bounds above. The final fractions have denominators $2^{n-1}$ and $n!$.

The bounds are pseudo-polynomial: they depend on the value $q$, which can be exponential in the input length. Since $q \le w(N) \le n\, w_{\max}$, they are polynomial when the weights are bounded by a polynomial in $n$, for example when the weights are seat counts or votes written in unary. The [hardness theorem](/power-index-hardness/) shows that the dependence on $q$ cannot be removed unless P = NP, so the problem is only [weakly NP-hard](/weak-np-hardness/).

## Properties

- **Exact.** The counts are integers and the indices are exact rationals. No rounding is involved.
- **Deterministic.**
- **Per player.** One run gives the indices of one player, but the variant below gives all players from one table.
- **Truncated at the quota.** Only the weights below $q$ are stored, which also bounds the table by $q$ and not by $w(N)$.

## Variants and improvements

- **Deletion instead of recomputation.** Build the table once with all $n$ players, in $O(n^2 q)$ time. The table without player $i$ follows from it by running line L5 backwards: for $s$ upward from 1, $C_{-i}[s][k] = C[s][k] - C_{-i}[s-1][k - w_i]$. This takes $O(n q)$ per player, so all Shapley-Shubik indices take $O(n^2 q)$ in total, and all Banzhaf indices $O(n q)$. The truncation at $q$ stays valid, because a set of weight $k < q$ with $i$ comes from a set of weight $k - w_i < q$ without $i$.
- **Generating functions.** The counts are the coefficients of $\prod_{j \ne i} (1 + y\, x^{w_j})$, where $x$ marks the weight and $y$ the size. Multiplying the factors one by one is the table above. With fast [polynomial multiplication](/polynomial-multiplication/), a product tree speeds up the computation when $q$ is large compared with $n$.
- **Other indices.** The same table gives every index that depends only on the number of swings of each size, such as the semivalues.
- **Large weights.** When $q$ is too large for a table, use [sampling](/shapley-value-sampling/) for an additive approximation, or a table keyed by the weights that occur, which is small when many players share the same weight.

## When to use it

Use it for exact indices of a voting body whose weights are moderate integers: seat counts of parties, votes in a council, or weights scaled to integers. A council of 30 members with weights up to a few thousand is computed in a fraction of a second. For weights in the millions, such as shares or populations, the table grows with $q$, and sampling or a coarser exact weighting may be better. For other compact games, use the representation that fits, for example [marginal contribution nets](/marginal-contribution-nets/).

## Pitfalls

- **The direction of the loop.** Line L3 must go down in $s$, or line L4 must go down in $k$ when there is no size index. An upward loop counts sets that contain player $j$ twice, which is the unbounded knapsack and gives wrong counts.
- **The window.** The lower end is $\max(0, q - w_i)$, not $q - w_i$, and the upper end is $q - 1$. A player with $w_i \ge q$ swings for every losing coalition of the others.
- **The quota convention.** "More than half of $W$" means $q = \lfloor W/2 \rfloor + 1$. "At least half" is a different game when $W$ is even, with different indices.
- **Rounding weights.** Scaling real weights to integers and rounding can change the game, because a coalition near the quota can flip from losing to winning. Scale exactly, or check that no coalition weight lies near the quota.
- **Overflow.** The counts reach $2^{n-1}$, which overflows 64-bit integers for $n > 64$. Use big integers or exact fractions.
- **Raw against normalized.** The raw Banzhaf indices do not sum to 1. Say which form a table uses.

## Implementations

The Python version returns the swing counts, both Banzhaf forms and the Shapley-Shubik index as exact Fractions, and rejects negative weights and a quota outside $[1, w(N)]$.

## History

Mann and Shapley (1962) computed the Shapley-Shubik index of the United States Electoral College exactly at RAND, after an earlier Monte Carlo estimate (1960). Counting the coalitions by weight with generating functions or tables became the standard exact method for weighted voting games. Prasad and Kelly (1990) and Deng and Papadimitriou (1994) proved that the indices are #P-complete, which explains why all exact methods depend on the size of the weights. Matsui and Matsui (2000) surveyed the algorithms for both indices and their running times.

## References
