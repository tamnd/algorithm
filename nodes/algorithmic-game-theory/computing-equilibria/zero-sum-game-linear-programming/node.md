---
tag: 6NAYNS
kind: algorithm
slug: zero-sum-game-linear-programming
name: Solving zero-sum games by linear programming
aliases:
- LP for matrix games
- linear programming solution of matrix games
area: algorithmic-game-theory/computing-equilibria
level: intro
summary: Computes the value and optimal mixed strategies of a two-player zero-sum matrix game with one linear program and its dual.
solves: [nash-equilibrium-computation]
model: real-ram
complexity:
  vars: {m: the number of rows (pure strategies of the row player), n: the number of columns, L: the bit length of the matrix}
  time: {worst: "poly(m, n, L)"}
  space: {extra: O(m n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1951
  people: [George B. Dantzig, John von Neumann]
  note: Von Neumann proved the minimax theorem in 1928; Dantzig published the equivalence of matrix games and linear programs in 1951, in the Cowles Commission volume edited by Koopmans.
prereqs: [zero-sum-game, minimax-theorem, lp-duality, simplex-method]
see_also: [nash-equilibrium-computation, strong-duality, complementary-slackness, sequence-form-linear-program, no-regret-zero-sum-theorem, yao-minimax-principle, minimax, support-enumeration]
sources:
  - paper: doi:10.1007/BF01448847
    title: "John von Neumann, Zur Theorie der Gesellschaftsspiele, Mathematische Annalen 100(1) (1928), 295-320"
    locator: the minimax theorem for finite two-person zero-sum games, which the LP computes
  - book: "Tjalling C. Koopmans (ed.), Activity Analysis of Production and Allocation, Cowles Commission Monograph 13, Wiley, 1951"
    title: "George B. Dantzig, A proof of the equivalence of the programming problem and the game problem"
    locator: pp. 330 to 335 (a matrix game as a linear program, and the reduction back)
  - paper: doi:10.1007/s00182-012-0328-8
    title: "Ilan Adler, The equivalence of linear programs and zero-sum games, International Journal of Game Theory 42(1) (2013), 165-177"
    locator: the case that Dantzig's reduction from linear programs to games misses, and a complete reduction
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 4 (computing the equilibria of two-player zero-sum games by linear programming)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel, Equilibrium computation for two-player games in strategic and extensive form), the LP of a zero-sum game and its dual
---

This algorithm solves a two-player zero-sum matrix game: it computes the value $v$ and an optimal [mixed strategy](/mixed-strategy/) for each player with one [linear program](/linear-programming-problem/), and reads the strategy of the second player from the dual solution. The [minimax theorem](/minimax-theorem/) says that the value exists; this page is the method that finds it, and [LP duality](/lp-duality/) is the reason it works. It differs from the [minimax](/minimax/) search of the games-and-search area, which walks a game tree of positions with pure moves, while here the input is a payoff matrix and the players randomize. The time is polynomial in the size of the matrix and the length of its numbers.

## In plain words

Two players choose at the same time. The row player picks a row of a table of numbers, the column player picks a column, and the column player pays the number in the cell to the row player. Each player may pick at random, with chosen chances. The row player wants a mix that earns the most on average against the worst reply. For a fixed mix, the worst reply is one column, so the condition is "earn at least the target against each column". This is a list of linear conditions on the chances and the target, and the row player wants the largest target. That is a linear program. Its partner program, the dual, is the same question for the column player, and the two answers meet in one number, the value of the game.

## The problem

The input is an $m \times n$ matrix $M$ with rational entries. On this page $m$ and $n$ are the numbers of pure strategies of the two players, not the number of players. If the row player plays row $i$ and the column player plays column $j$, the column player pays $M_{ij}$ to the row player; the row player maximizes and the column player minimizes. A mixed strategy of the row player is $x \in \Delta_m = \{x \in \mathbb{R}^m : x \ge 0, \sum_i x_i = 1\}$, and of the column player $y \in \Delta_n$. The expected payment is $x^{\mathsf T} M y$.

The output is the value $v$ and strategies $x^*$, $y^*$ with

$$\min_{j} (x^{*\mathsf T} M)_j \;=\; v \;=\; \max_{i} (M y^*)_i .$$

So $x^*$ earns at least $v$ against every column, and $y^*$ pays at most $v$ against every row. This pair is exactly a Nash equilibrium of the bimatrix game $(M, -M)$. Pure replies are enough in both tests, because $x^{\mathsf T} M y$ is linear in $y$ for a fixed $x$, so its minimum over $\Delta_n$ is at a vertex, a pure column. This is the best response fact: a mixed strategy is a [best response](/best-response/) if and only if each pure strategy in its support is one.

## The algorithm

```pseudo id=main
ZERO-SUM-LP(M)                    ▷ M is m by n; the column player pays M[i][j] to the row player
L1  k ← 1 - min over i, j of M[i][j]
L2  M' ← M with k added to each entry           ▷ now each entry is at least 1
L3  maximize v over x in R^m and v
L4      subject to v - Σ_i x_i M'[i][j] ≤ 0 for j = 1, ..., n     ▷ dual variable y_j ≥ 0
L5      and Σ_i x_i = 1, x ≥ 0, v ≥ 0                             ▷ dual variable w, free
L6  solve the LP by the simplex method: (x*, v*) optimal, (y*, w*) the optimal dual
L7  return (v* - k, x*, y*)
```

Lines L1 and L2 shift the matrix so that every entry is at least 1. The shift adds $k$ to every payoff $x^{\mathsf T} M y$, because $x$ and $y$ sum to 1, so it changes the value by $k$ and the optimal strategies not at all. After the shift the value is at least 1, so the bound $v \ge 0$ of line L5 cuts off nothing, and $v$ needs no split into two nonnegative parts. The LP of lines L3 to L5 has $m + 1$ variables, $n$ inequalities and one equation.

The dual of this LP is the problem of the column player. With $y_j \ge 0$ for the inequality of column $j$ and a free $w$ for the equation, the dual is

$$\min\; w \quad \text{subject to} \quad \sum_j M'_{ij} y_j \le w \;\; (i = 1, \ldots, m), \qquad \sum_j y_j \ge 1, \qquad y \ge 0 .$$

The constraint $\sum_j y_j \ge 1$ comes from the column of $v$; it holds with equality at the optimum, by [complementary slackness](/complementary-slackness/), because $v^* \ge 1 > 0$. So the dual solution $y^*$ is a mixed strategy, and line L6 gets both strategies from one run of the simplex method.

## Example

Take $M = \begin{pmatrix} 3 & -1 \\ -2 & 1 \end{pmatrix}$. Line L1 gives $k = 1 - (-2) = 3$ and $M' = \begin{pmatrix} 6 & 2 \\ 1 & 4 \end{pmatrix}$. The LP is: maximize $v$ subject to $v \le 6x_1 + x_2$, $v \le 2x_1 + 4x_2$, $x_1 + x_2 = 1$, $x \ge 0$.

| quantity | value |
|---|---|
| optimal primal solution | $x^* = (3/7, 4/7)$, $v^* = 22/7$ |
| optimal dual solution | $y^* = (2/7, 5/7)$, $w^* = 22/7$ |
| value of the game | $22/7 - 3 = 1/7$ |
| $x^{*\mathsf T} M$ (one entry per column) | $(1/7, 1/7)$ |
| $M y^*$ (one entry per row) | $(1/7, 1/7)$ |

Both strategies are fully mixed, and each makes the other player indifferent, as the [indifference principle](/indifference-principle/) says. A second example shows an unused row: for $M = \begin{pmatrix} 1 & 2 \\ 3 & 0 \\ 0 & 4 \end{pmatrix}$ the method returns $v = 12/7$, $x^* = (0, 4/7, 3/7)$ and $y^* = (4/7, 3/7)$. Against $y^*$ the first row earns only $4/7 + 6/7 = 10/7 < 12/7$, so it gets probability 0. For matching pennies and rock-paper-scissors the value is 0 and both strategies are uniform.

## Correctness

The LP is feasible: any $x \in \Delta_m$ with $v = 0$ satisfies all constraints. It is bounded: $v \le \sum_i x_i M'_{i1} \le \max_i M'_{i1}$. So the simplex method with [Bland's rule](/bland-rule/) ends with an optimal primal solution $(x^*, v^*)$ and an optimal dual solution $(y^*, w^*)$, and [strong duality](/strong-duality/) gives $v^* = w^*$. Primal feasibility says that $x^*$ earns at least $v^*$ in $M'$ against each column; dual feasibility says that $y^*$ pays at most $w^* = v^*$ in $M'$ against each row. Remove the shift and both statements hold for $M$ with $v^* - k$. The full proof, with the step that $y^*$ sums to 1, is in the proof file.

## Complexity

The LP has $m + 1$ variables and $n + 1$ constraints, and its numbers are those of $M$ plus a shift, so its bit length is $O(L)$, where $L$ is the bit length of $M$.

- With the ellipsoid method or an [interior point method](/interior-point-method/), the time is polynomial in $m$, $n$ and $L$. The value and the strategies are rational numbers with a polynomial number of digits, because they solve a square linear system made of entries of $M$.
- With the [simplex method](/simplex-method/), the number of pivots is exponential in the worst case for the common pivot rules (the [Klee-Minty cube](/klee-minty-cube/) for Dantzig's rule), but small in practice. Each pivot costs $O(m n)$ arithmetic operations on the tableau. In the [smoothed analysis](/smoothed-analysis/) model the shadow vertex simplex method takes polynomial time.
- The space is $O(m n)$ numbers for the tableau.

The code on this page uses exact rational arithmetic, so a pivot costs $O(m n)$ operations on numbers whose size grows with $L$.

## Properties

- **Exact.** With rational input and rational arithmetic, the value and the strategies are exact, and the equilibrium test of the problem statement is an exact comparison.
- **One LP for both players.** The dual solution gives the second strategy, so one run solves the game.
- **The optimal strategies form a polytope.** The set of optimal $x$ is the set of optimal solutions of the LP, a face of the feasible set, and the same holds for $y$. Any optimal $x$ pairs with any optimal $y$ (the equilibria are interchangeable), and all pairs give the same value. The method returns one vertex of each set.
- **Strategic equivalence.** Adding a constant to every entry, or multiplying every entry by a positive constant, changes the value in the same way and keeps the optimal strategies.

## Variants and improvements

- **No shift, a free value.** Keep $M$ and write $v = v^+ - v^-$ with $v^+, v^- \ge 0$. This avoids line L1, but gives one more column.
- **The scaled form.** With $M' > 0$, set $u = x / v$. Then the row player's LP becomes $\min \sum_i u_i$ subject to $M'^{\mathsf T} u \ge \mathbf 1$, $u \ge 0$, and $x = u / \sum_i u_i$, $v = 1 / \sum_i u_i$. This is the form in many textbooks.
- **Extensive-form games.** A zero-sum game tree with perfect recall has an LP of size linear in the tree, the [sequence-form linear program](/sequence-form-linear-program/). The matrix of the normal form can be exponentially larger.
- **Approximation by learning.** If two players run a no-regret algorithm such as [multiplicative weights](/multiplicative-weights-update/) against each other, the average payoff converges to the value ([no-regret zero-sum theorem](/no-regret-zero-sum-theorem/)). An $\varepsilon$-approximation with payoffs in $[0, 1]$ takes $O(\log(m + n) / \varepsilon^2)$ rounds of $O(m n)$ time each, which is faster than an LP for large games and moderate $\varepsilon$.
- **General sum.** Without $B = -A$ this LP does not apply. A Nash equilibrium of a general bimatrix game needs [support enumeration](/support-enumeration/) or the [Lemke-Howson algorithm](/lemke-howson-algorithm/), and the problem is PPAD-complete ([Nash equilibrium computation](/nash-equilibrium-computation/)).

## When to use it

Use it for any two-player zero-sum or constant-sum game given as a matrix, when an exact answer is needed and the matrix fits in memory. A constant-sum game with $A + B = c$ for a constant $c$ is the zero-sum game $(A, -A)$ shifted by $c$ for the second player, so it has the same equilibria. Use the sequence form when the game is a tree, and a learning method when the matrix is too large to write down but best responses are cheap.

## Pitfalls

- **Applying it to a general-sum game.** The LP of the row player then gives the maximin strategy of the row player, which in general is not part of a Nash equilibrium.
- **Forgetting the sign of $v$.** If $v \ge 0$ is kept as a bound while the value is negative, the LP becomes infeasible. Shift the matrix (lines L1 and L2) or split $v$.
- **Reading $y$ from the wrong place.** The column strategy is the vector of dual values of the $n$ column constraints, not of the equation. In a solver with a different sign convention for duals, check the signs.
- **Floating point.** With floats, the equilibrium test needs a tolerance, and degenerate games may give a strategy that is off by rounding. Use rationals when the result must be exact.
- **Expecting a unique answer.** Many games have many optimal strategies. The simplex method returns one vertex, and two solvers may return different ones.

## Implementations

The Python code builds the LP of lines L3 to L5 and solves it with the shared exact simplex code (two phases, Bland's rule, rational numbers). The tests check matching pennies and rock-paper-scissors, the examples above, and 150 random games: each output must guarantee the value against every row and column, must be a Nash equilibrium of $(M, -M)$ by a check of all pure deviations, and must match the value found by an independent method, a search over all square submatrices (the kernels of Shapley and Snow). The column player's LP, solved on its own, must give the same value.

## History

Von Neumann proved the minimax theorem in 1928. In 1951 Dantzig published a proof that a matrix game is a linear program and that a linear program reduces to a symmetric matrix game. Adler (2013) showed that the reduction from linear programs to games misses one case, and gave a complete reduction.

## References
