---
tag: W47DAN
kind: algorithm
slug: lemke-howson-algorithm
name: Lemke-Howson algorithm
aliases:
- Lemke-Howson
- complementary pivoting for bimatrix games
area: algorithmic-game-theory/computing-equilibria
level: core
summary: Finds a Nash equilibrium of a nondegenerate bimatrix game by following a path of almost complementary vertices by pivoting.
solves: [nash-equilibrium-computation]
model: real-ram
complexity:
  vars: {m: the number of pure strategies of the row player, n: the number of pure strategies of the column player}
  time: {worst: "O(2^(m + n) (m + n)^3)"}
  space: {extra: O((m + n)^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1964
  people: [Carlton E. Lemke, Joseph T. Howson Jr.]
  note: Lemke and Howson published the method in the Journal of SIAM in 1964; it gave a constructive proof that every bimatrix game has an equilibrium and that a nondegenerate one has an odd number of them.
prereqs: [bimatrix-game, best-response-polytope, simplex-method, nash-equilibrium]
see_also: [lemke-algorithm, support-enumeration, savani-von-stengel-theorem, ppad, end-of-the-line-problem, nash-equilibrium-computation, linear-complementarity-problem, nash-existence-theorem]
sources:
  - paper: doi:10.1137/0112033
    title: "C. E. Lemke and J. T. Howson Jr., Equilibrium points of bimatrix games, Journal of the Society for Industrial and Applied Mathematics 12(2) (1964), 413-423"
    locator: the complementary pivoting method for bimatrix games and the parity of the number of equilibria
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel, Equilibrium computation for two-player games in strategic and extensive form), best response polytopes, labels and the Lemke-Howson paths
  - paper: doi:10.1111/j.1468-0262.2006.00667.x
    title: "Rahul Savani and Bernhard von Stengel, Hard-to-solve bimatrix games, Econometrica 74(2) (2006), 397-429"
    locator: games on which every Lemke-Howson path, from every missing label, is exponentially long
  - paper: doi:10.1145/2465769.2465774
    title: "Paul W. Goldberg, Christos H. Papadimitriou and Rahul Savani, The complexity of the homotopy method, equilibrium selection, and Lemke-Howson solutions, ACM Transactions on Economics and Computation 1(2) (2013), article 9"
    locator: Theorem 7 (finding any of the equilibria that the Lemke-Howson algorithm constructs is PSPACE-complete)
---

The Lemke-Howson algorithm finds one Nash equilibrium of a two-player game in strategic form (a [bimatrix game](/bimatrix-game/)) by pivoting, as the [simplex method](/simplex-method/) does, on the two [best response polytopes](/best-response-polytope/) of the game. It starts at an artificial point that is not an equilibrium, drops one label, and follows a unique path of almost complementary vertices until the dropped label comes back, which happens exactly at an equilibrium. The problem itself and the other methods are on the [Nash equilibrium computation](/nash-equilibrium-computation/) page. It differs from [Lemke's algorithm](/lemke-algorithm/), which solves a general [linear complementarity problem](/linear-complementarity-problem/) with an extra covering variable, and from [support enumeration](/support-enumeration/), which lists all equilibria by a search. The method assumes a nondegenerate game; for a degenerate game it needs a lexicographic pivot rule, which the code on this page uses.

## In plain words

Draw for each player a shape whose corners are the useful ways to play, and tag each corner with labels: "this move is not used" or "this move of the other player is a best reply". An equilibrium is a pair of corners that together carry every label. The pair "nobody plays anything" also carries every label, but it is not a real answer. Start there and give up one chosen label. Now exactly one label is carried twice. Move one player along an edge to get rid of the double, which gives a new label to that player; if that label is again a double, move the other player. Each step is forced, the path never comes back, and it can end only when the given-up label returns, at an equilibrium.

## The problem

The input is two $m \times n$ matrices $A$ and $B$ with rational entries. On this page $m$ and $n$ are the numbers of pure strategies of the row player and the column player, not the number of players. The row player gets $A_{ij}$ and the column player gets $B_{ij}$, and both maximize. The output is one Nash equilibrium $(x, y)$, $x \in \Delta_m$, $y \in \Delta_n$. The test is the best response fact: $x$ is a [best response](/best-response/) to $y$ if and only if each row with $x_i > 0$ maximizes $(Ay)_i$, and the same for $y$ with the columns $(x^{\mathsf T} B)_j$.

Adding a constant to all entries of $A$ or of $B$ does not change the equilibria, so assume that $A' = A + c$ and $B' = B + d$ have all entries at least 1. The best response polytopes are

$$P = \{x \in \mathbb{R}^m : x \ge 0,\; B'^{\mathsf T} x \le \mathbf 1\}, \qquad Q = \{y \in \mathbb{R}^n : A' y \le \mathbf 1,\; y \ge 0\}.$$

Number the labels $0, \ldots, m - 1$ for the rows and $m, \ldots, m + n - 1$ for the columns. A point $x \in P$ has label $i$ if $x_i = 0$ and label $m + j$ if $(B'^{\mathsf T} x)_j = 1$, that is, if column $j$ is a best response to $x$. A point $y \in Q$ has label $i$ if $(A' y)_i = 1$ (row $i$ is a best response to $y$) and label $m + j$ if $y_j = 0$. A pair $(x, y)$ is **completely labeled** if every label appears at $x$ or at $y$. The completely labeled pairs other than $(0, 0)$ are exactly the equilibria, after scaling $x$ and $y$ to sum 1: a strategy is either unused or a best response.

The game is **nondegenerate** if no point of $P$ has more than $m$ labels and no point of $Q$ has more than $n$, which is the same as: no mixed strategy with $k$ strategies in its support has more than $k$ pure best responses.

## The algorithm

Write $P$ as the tableau $T_1$: $B'^{\mathsf T} x + s = \mathbf 1$ with slack variables $s_j$, and $Q$ as the tableau $T_2$: $r + A' y = \mathbf 1$ with slacks $r_i$. Give $x_i$ and $r_i$ the label $i$, and $s_j$ and $y_j$ the label $m + j$. Then the labels of a vertex are the labels of its nonbasic variables, and the pair of basic solutions is completely labeled when no label is basic in both tableaux.

```pseudo id=main
LEMKE-HOWSON(A, B, k)                 ▷ labels 0..m-1 for rows, m..m+n-1 for columns; k is dropped
L1  shift A, B to A', B' ≥ 1; T1: B'ᵀ x + s = 1 with basis s; T2: r + A' y = 1 with basis r
L2  ℓ ← k; T ← T1 if k < m, else T2           ▷ start at the artificial pair (0, 0)
L3  repeat
L4      enter the variable with label ℓ into the basis of T; ℓ' ← the label of the leaving variable
                                                ▷ the minimum ratio test is lexicographic
L5      ℓ ← ℓ'                                  ▷ ℓ is now nonbasic in both tableaux: the double label
L6      if ℓ = k then stop the loop             ▷ k is back: the pair is completely labeled
L7      T ← the other tableau
L8  return x / Σ x and y / Σ y, read from T1 and T2
```

At each pair on the path every label except $k$ appears, and exactly one label, $\ell$, appears at both points. Line L4 removes $\ell$ from the point where it was just picked up by moving the other point along an edge of its polytope, which is the only edge that keeps all the other labels. The leaving variable gives a new label, and if it is not $k$ it is the next double label.

Ties in the minimum ratio test of line L4 occur only in degenerate games. The lexicographic rule breaks them by comparing, after the right-hand side, the columns of the first basis, each divided by the pivot entry. This is the same as solving a slightly perturbed nondegenerate game, so the path is still unique and still ends.

## Example

Take the nondegenerate $3 \times 2$ game of von Stengel's chapter in NRTV,

$$A = \begin{pmatrix} 3 & 3 \\ 2 & 5 \\ 0 & 6 \end{pmatrix}, \qquad B = \begin{pmatrix} 3 & 2 \\ 2 & 6 \\ 3 & 1 \end{pmatrix},$$

with labels 0, 1, 2 for the rows and 3, 4 for the columns. The code shifts $A$ by 1, so $A' = A + 1$, and keeps $B' = B$. Its three equilibria, found by [support enumeration](/support-enumeration/), are $((1, 0, 0), (1, 0))$, $((4/5, 1/5, 0), (2/3, 1/3))$ and $((0, 1/3, 2/3), (1/3, 2/3))$. The path for the dropped label $k = 1$:

| step | tableau | enters | leaves | point after the step | labels of $x$ | labels of $y$ |
|---|---|---|---|---|---|---|
| start | | | | $x = (0, 0, 0)$, $y = (0, 0)$ | 0, 1, 2 | 3, 4 |
| 1 | $T_1$ | 1 | 4 | $x = (0, 1/6, 0)$ | 0, 2, 4 | 3, 4 |
| 2 | $T_2$ | 4 | 2 | $y = (0, 1/7)$ | 0, 2, 4 | 2, 3 |
| 3 | $T_1$ | 2 | 3 | $x = (0, 1/8, 1/4)$ | 0, 3, 4 | 2, 3 |
| 4 | $T_2$ | 3 | 1 | $y = (1/15, 2/15)$ | 0, 3, 4 | 1, 2 |

After step 4 label 1 is back, and scaling gives the equilibrium $x = (0, 1/3, 2/3)$, $y = (1/3, 2/3)$. The paths for all five labels:

| dropped label | pivots (enters, leaves) | equilibrium reached |
|---|---|---|
| 0 | (0, 3), (3, 0) | $((1, 0, 0), (1, 0))$ |
| 1 | (1, 4), (4, 2), (2, 3), (3, 1) | $((0, 1/3, 2/3), (1/3, 2/3))$ |
| 2 | (2, 3), (3, 0), (0, 2) | $((1, 0, 0), (1, 0))$ |
| 3 | (3, 0), (0, 3) | $((1, 0, 0), (1, 0))$ |
| 4 | (4, 2), (2, 3), (3, 1), (1, 4) | $((0, 1/3, 2/3), (1/3, 2/3))$ |

The middle equilibrium $((4/5, 1/5, 0), (2/3, 1/3))$ is reached from no label. For each label, the path from $(0, 0)$ uses one of the other two equilibria as its end, and the remaining two equilibria are the two ends of a second path with the same dropped label. In battle of the sexes, $A = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$ and $B = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix}$, the labels 0 and 2 lead to $((1, 0), (1, 0))$, the labels 1 and 3 lead to $((0, 1), (0, 1))$, and the mixed equilibrium $((2/3, 1/3), (1/3, 2/3))$ is never reached from $(0, 0)$.

## Correctness

Fix the dropped label $k$ and look at the graph whose nodes are the vertex pairs $(x, y) \in P \times Q$ that have every label except possibly $k$, with an edge between two pairs that differ by one pivot in one polytope and keep all labels other than $k$. In a nondegenerate game:

- a completely labeled pair, which is $(0, 0)$ or an equilibrium, has exactly one neighbor: the edge that drops label $k$ at the point that has it;
- every other pair has exactly one double label, and exactly two neighbors: drop the double label at $x$, or drop it at $y$.

So the graph is a union of disjoint paths and cycles, and the ends of the paths are the completely labeled pairs. The path that starts at $(0, 0)$ cannot cycle and cannot stop in the middle, and the polytopes are bounded, so a pivot row always exists in line L4. The graph is finite, so the path ends at another completely labeled pair, which is an equilibrium. The proof file gives the details, also for the lexicographic rule.

The same argument shows that a nondegenerate game has an odd number of equilibria: the completely labeled pairs are matched in pairs by the paths of label $k$, and one of them is the artificial pair $(0, 0)$. It is the two-player case of the [Nash existence theorem](/nash-existence-theorem/), with a constructive proof.

## Complexity

Each pivot costs $O((m + n) \max(m, n))$ arithmetic operations on the tableau. The path visits each pair of vertices at most once. A vertex of $P$ in a nondegenerate game is fixed by its $m$ labels, and given the labels of $x$, at most $m + n + 1$ sets of labels for $y$ complete them up to label $k$, so the path has at most $\binom{m+n}{m}(m + n + 1)$ steps. This gives the worst-case bound $O(2^{m+n}(m + n)^3)$.

The exponential bound is real: Savani and von Stengel (2006) built square games on which every Lemke-Howson path, for every dropped label, is exponentially long in the number of strategies ([Savani-von Stengel theorem](/savani-von-stengel-theorem/)). Goldberg, Papadimitriou and Savani (2013) showed that computing any equilibrium that the Lemke-Howson algorithm would find is PSPACE-complete. Finding some equilibrium of a bimatrix game is [PPAD](/ppad/)-complete (Chen, Deng and Teng), and the path structure above is the reason it lies in PPAD: it is an instance of the [end of the line problem](/end-of-the-line-problem/). By the same work of Chen, Deng and Teng, no algorithm runs in polynomial time in the [smoothed analysis](/smoothed-analysis/) model unless PPAD is in RP. In practice the paths are often short.

With exact rational arithmetic the numbers in the tableau stay of polynomial bit length, as in the simplex method, and the result is the exact rational equilibrium. Two-player games always have rational equilibria; games with three or more players can have only irrational ones, so no method of this kind works there. The space is two tableaux, $O((m + n)^2)$ numbers.

## Properties

- **Exact.** With rationals, the output is an exact equilibrium.
- **One equilibrium per label.** Each dropped label gives one equilibrium. Different labels can give the same one, and some equilibria are reached from no label (the middle one in the example).
- **Not all equilibria.** Starting from an equilibrium instead of $(0, 0)$ reaches more of them, but even the graph of all such paths does not have to connect all equilibria.
- **Deterministic.** The label and the pivot rule fix the path.

## Variants and improvements

- **Lemke's algorithm.** The pair of conditions $0 \le x \perp \mathbf 1 - A' y \ge 0$ and $0 \le y \perp \mathbf 1 - B'^{\mathsf T} x \ge 0$ is a linear complementarity problem with $q = \mathbf 1$, whose trivial solution $(0, 0)$ is the artificial start of this method. [Lemke's algorithm](/lemke-algorithm/) uses an equivalent form with positive cost matrices and $q = -\mathbf 1$, and a covering vector instead of a dropped label.
- **Starting from other points.** With a covering vector chosen from a given pair of mixed strategies, a Lemke path can start from that pair instead of from $(0, 0)$, and so it can give other equilibria.
- **Degenerate games.** The lexicographic rule of line L4, or a perturbation of the right-hand side by $(\varepsilon, \varepsilon^2, \ldots)$, makes the path unique.
- **Integer pivoting.** Keeping the tableau in integers, with all entries divided by the previous pivot element, avoids fractions and keeps the numbers small.
- **All equilibria.** For the full list use [support enumeration](/support-enumeration/) or the enumeration of the vertices of both polytopes.

## When to use it

Use it to find one exact equilibrium of a general-sum bimatrix game of moderate size, where support enumeration is too slow. Use the [LP](/zero-sum-game-linear-programming/) if the game is zero-sum, because that takes polynomial time. Do not use it to select a specific equilibrium, such as the one with the best welfare: it gives an arbitrary one, and selection is NP-hard in general. For games with more than two players use other methods, such as [Scarf's algorithm](/scarf-algorithm/) for approximate fixed points.

## Pitfalls

- **Ignoring degeneracy.** With the plain minimum ratio test, a tie in a degenerate game can make the path cycle or end at a pair that is not completely labeled. Use the lexicographic rule.
- **Mixing up the matrices.** $P$ uses $B$, the payoffs of the column player, because the labels of $x$ say which columns are best responses to $x$. $Q$ uses $A$.
- **Forgetting the shift.** With zero or negative entries the polytopes are not bounded, and the method breaks. Shift both matrices to positive entries first; the equilibria do not change.
- **Forgetting to scale.** The vertex pair is not a pair of strategies until $x$ and $y$ are divided by their sums.
- **Expecting a polynomial bound.** The method is exponential in the worst case, even if it is fast on most games.

## Implementations

The Python code keeps the two tableaux in Fraction, with the column index equal to the label, and pivots by lines L1 to L8 with the lexicographic minimum ratio test; it can record the trace of pivots. The tests check the traces of the example for all five labels, battle of the sexes, matching pennies and rock-paper-scissors (the uniform pair from every label), and that shifting the payoffs does not change the result. On 60 random nondegenerate games, every output for every label is checked as an equilibrium by all pure deviations and must be one of the equilibria found by an independent support enumeration, whose number must be odd. On 150 random degenerate games with many ties, and on a constant game, every path must end at an equilibrium.

## History

Lemke and Howson published the method in 1964. It gave an algorithmic proof that bimatrix games have equilibria, and the parity result, and Lemke extended it in 1965 to a general method for linear complementarity problems. Savani and von Stengel (2006) answered the question of its worst case with games on which all paths are exponentially long, and Goldberg, Papadimitriou and Savani (2013) showed that the specific equilibria it finds are PSPACE-complete to compute.

## References
