---
tag: GHTYAP
kind: algorithm
slug: support-enumeration
name: Support enumeration
aliases:
- Porter-Nudelman-Shoham algorithm
- support enumeration for bimatrix games
area: algorithmic-game-theory/computing-equilibria
level: core
summary: Finds Nash equilibria of a bimatrix game by trying pairs of supports and solving the linear indifference equations for each pair.
solves: [nash-equilibrium-computation]
model: real-ram
complexity:
  vars: {m: the number of pure strategies of the row player, n: the number of pure strategies of the column player}
  time: {worst: "O(2^(m + n) (m n + min(m, n)^3))"}
  space: {extra: O(m n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2004
  people: [Ryan Porter, Eugene Nudelman, Yoav Shoham]
  note: The plain method is a basic textbook method; Porter, Nudelman and Shoham (AAAI 2004, journal version 2008) ordered the supports from small and balanced to large, and found that this order makes it fast on many test games.
prereqs: [bimatrix-game, best-response, indifference-principle, nash-equilibrium]
see_also: [nash-equilibrium-computation, lemke-howson-algorithm, best-response-polytope, vertex-enumeration, zero-sum-game-linear-programming, hardness-of-optimal-nash-equilibria, lipton-markakis-mehta-algorithm, savani-von-stengel-theorem]
sources:
  - paper: doi:10.1016/j.geb.2006.03.015
    title: "Ryan Porter, Eugene Nudelman and Yoav Shoham, Simple search methods for finding a Nash equilibrium, Games and Economic Behavior 63(2) (2008), 642-662"
    locator: the support search for two-player games, with the order of the supports by size and balance and the pruning by conditional dominance
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel, Equilibrium computation for two-player games in strategic and extensive form), nondegenerate games, equal support sizes and support enumeration
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 4 (computing Nash equilibria of two-player general-sum games, the search over supports)
---

Support enumeration finds the Nash equilibria of a two-player game in strategic form (a [bimatrix game](/bimatrix-game/)) by guessing which pure strategies each player uses, the supports, and solving a small linear system for each guess. A pair of supports gives equations that make each player indifferent among the strategies in its own support, by the [indifference principle](/indifference-principle/); if the solution is a pair of probability vectors and no outside strategy does better, it is an equilibrium. The method is one of the basic exact methods behind the problem of [Nash equilibrium computation](/nash-equilibrium-computation/), which gives the overview; this page goes deep on the enumeration. It is exponential in the worst case, while the [Lemke-Howson algorithm](/lemke-howson-algorithm/) follows one path of pivots to one equilibrium and is also exponential in the worst case.

## In plain words

In a mixed equilibrium, each player mixes only among moves that are equally good for it, given the mix of the other player. If we knew which moves each player uses, we could write "these moves give the same payoff" as linear equations and solve them. We do not know the moves, so we try every choice: one move each, then two moves each, and so on. For each choice we solve the equations, throw the answer away if a chance is not positive, and check that no unused move pays more. Every answer that passes is an equilibrium. In a game without special ties, both players always use the same number of moves, which cuts the search.

## The problem

The input is two $m \times n$ matrices $A$ and $B$ with rational entries. On this page $m$ and $n$ are the numbers of pure strategies of the row player and the column player, not the number of players. If the row player plays row $i$ and the column player plays column $j$, the row player gets $A_{ij}$ and the column player gets $B_{ij}$, and both maximize. A mixed strategy is $x \in \Delta_m = \{x \ge 0, \sum_i x_i = 1\}$ for the row player and $y \in \Delta_n$ for the column player. The support of $x$ is $\operatorname{supp}(x) = \{i : x_i > 0\}$.

A pair $(x, y)$ is a [Nash equilibrium](/nash-equilibrium/) if $x$ is a [best response](/best-response/) to $y$ and $y$ is a best response to $x$. The best response fact makes this a finite test: $x$ is a best response to $y$ if and only if every row in $\operatorname{supp}(x)$ maximizes $(Ay)_i$, and the same holds for $y$ with the columns $(x^{\mathsf T} B)_j$. The output is a list of equilibria; for a nondegenerate game it is the list of all of them.

The game is **nondegenerate** if no mixed strategy with a support of $k$ pure strategies has more than $k$ pure best responses. Random games with continuous payoffs are nondegenerate with probability 1, but games with structure, such as integer payoffs with many ties, often are not.

## The algorithm

```pseudo id=main
SUPPORT-ENUMERATION(A, B)                 ▷ A, B are m by n; row player gets A, column player gets B
L1  for k ← 1 to min(m, n)
L2      for each set I of k rows and each set J of k columns
L3          solve Σ_{j∈J} A[i][j] y_j = u for i in I, and Σ_{j∈J} y_j = 1     ▷ unknowns y_J, u
L4          solve Σ_{i∈I} x_i B[i][j] = v for j in J, and Σ_{i∈I} x_i = 1     ▷ unknowns x_I, v
L5          if a system is singular, or some y_j or x_i is not positive: skip this pair
L6          set x_i ← 0 for i not in I and y_j ← 0 for j not in J
L7          if (A y)_i ≤ u for every row i and (xᵀ B)_j ≤ v for every column j
L8              output (x, y)
```

Line L3 makes the row player indifferent among the rows of $I$: it is a square system of $k + 1$ equations in the $k + 1$ unknowns $y_j$ ($j \in J$) and $u$. Note that $y$, the strategy of the column player, is found from the payoffs $A$ of the row player, because $y$ must make the rows of $I$ equally good. Line L4 is the same for the column player, with $B$. Line L7 is the best response test: the rows in $I$ all earn $u$, so they are best responses if no other row earns more, and the same for the columns.

Only supports of equal size are tried. In a nondegenerate game this loses nothing (see Correctness). In a degenerate game the method can miss equilibria, and the complete version tries all pairs $(I, J)$ of any sizes and solves the systems as feasibility problems, which allows a set of solutions instead of one point.

## Example

Take the $3 \times 2$ game of von Stengel's chapter in NRTV, which is nondegenerate:

$$A = \begin{pmatrix} 3 & 3 \\ 2 & 5 \\ 0 & 6 \end{pmatrix}, \qquad B = \begin{pmatrix} 3 & 2 \\ 2 & 6 \\ 3 & 1 \end{pmatrix}.$$

For $k = 1$ there are 6 pure pairs, and only (row 0, column 0) passes line L7: row 0 is best against column 0 ($3 \ge 2, 0$), and column 0 is best against row 0 ($3 \ge 2$). For $k = 2$ the column set is $\{0, 1\}$ and there are three row sets.

| rows $I$ | line L3: $y$, $u$ | line L4: $x$, $v$ | line L7 | result |
|---|---|---|---|---|
| $\{0, 1\}$ | $3y_0 + 3y_1 = 2y_0 + 5y_1$ gives $y = (2/3, 1/3)$, $u = 3$ | $3x_0 + 2x_1 = 2x_0 + 6x_1$ gives $x = (4/5, 1/5, 0)$, $v = 14/5$ | row 2 earns $2 \le 3$ | equilibrium |
| $\{0, 2\}$ | $y = (1/2, 1/2)$, $u = 3$ | $x_0 = -2x_2$, not positive | | skipped at L5 |
| $\{1, 2\}$ | $y = (1/3, 2/3)$, $u = 4$ | $x = (0, 1/3, 2/3)$, $v = 8/3$ | row 0 earns $3 \le 4$ | equilibrium |

So the game has exactly three equilibria, with payoffs $(3, 3)$, $(3, 14/5)$ and $(4, 8/3)$. The number is odd, as it is in every nondegenerate game. The same game is the example of the [Lemke-Howson](/lemke-howson-algorithm/) page, where only the first and the third equilibrium are reached from the artificial start.

Two more check values. In battle of the sexes, $A = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$ and $B = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix}$, the method returns the two pure equilibria and $x = (2/3, 1/3)$, $y = (1/3, 2/3)$, where the row player gets $2/3$. In matching pennies and rock-paper-scissors it returns only the uniform pair.

## Correctness

Each output is an equilibrium. At line L8 the strategies are distributions by lines L3 to L6. Every row in $I = \operatorname{supp}(x)$ earns exactly $u$ against $y$ by line L3, and no row earns more by line L7, so by the best response fact $x$ is a best response to $y$. The same argument with line L4 shows that $y$ is a best response to $x$.

In a nondegenerate game, each equilibrium is found. Let $(x, y)$ be an equilibrium with supports $I$ and $J$. Each column of $J$ is a best response to $x$, so $|J| \le |I|$ by nondegeneracy; in the same way $|I| \le |J|$, so the sizes are equal. Then $y$ and $u = \max_i (Ay)_i$ solve the system of line L3. That system has only this solution: if it had a line of solutions, move $y$ along the line inside the simplex. The move must stop where a $y_j$ becomes 0 or where an outside row ties with $u$, and at that point a strategy with a support of at most $k$ has more than $k$ pure best responses, or one with a support of $k - 1$ has $k$, which nondegeneracy forbids. So the solver finds $y$, the same holds for $x$, and the pair passes lines L5 and L7. The proof file has the details.

## Complexity

The number of support pairs of equal size is $\sum_{k} \binom{m}{k}\binom{n}{k} = \binom{m+n}{m} - 1$, by Vandermonde's identity. For each pair, lines L3 and L4 solve two systems of size $k + 1$ by Gaussian elimination in $O(k^3)$ arithmetic operations, and line L7 costs $O(m n)$. So the time is $O\big(\binom{m+n}{m}(m n + \min(m, n)^3)\big)$ in the worst case, which is at most $O(2^{m+n}(m n + \min(m, n)^3))$, and about $4^n / \sqrt{n}$ systems for an $n \times n$ game. The space is $O(m n)$ besides the output.

The exponential time is not only an artifact of the search. The coordination game $A = B = I_n$ has $2^n - 1$ equilibria, one for each nonempty support (both players uniform on the same set), so any method that lists all equilibria needs exponential time on it. The solutions are rational numbers with a polynomial number of digits, because each is the solution of a square system with entries from $A$ or $B$. This is special to two players: games with three or more players can have only irrational equilibria. The code uses exact rational arithmetic, so the cost of one operation grows with the bit length of the entries.

## Properties

- **Exact.** With rational input, every equilibrium is computed exactly, and the best response test is an exact comparison.
- **Complete for nondegenerate games.** It lists every equilibrium. For a degenerate game the list is correct but can be incomplete.
- **Embarrassingly parallel.** The support pairs are independent.
- **Any order works.** The method can stop at the first equilibrium, and the order of the pairs then decides the running time but not the correctness.

## Variants and improvements

- **Heuristic order (Porter, Nudelman and Shoham).** Try small supports first and, among supports of the same total size, balanced ones first, and prune a support when one of its strategies is dominated given the supports. On many generated test games this finds one equilibrium faster than Lemke-Howson. The same search with nonlinear feasibility problems handles games with more players.
- **Degenerate games.** Enumerate all pairs $(I, J)$ of any sizes and replace the square systems by LP feasibility problems, or enumerate the vertices of the two [best response polytopes](/best-response-polytope/) and match their labels ([vertex enumeration](/vertex-enumeration/)). In a degenerate game the equilibria form a finite union of polytopes, and vertex enumeration gives the extreme points of these sets.
- **One equilibrium.** The [Lemke-Howson algorithm](/lemke-howson-algorithm/) finds one equilibrium by pivoting without a search, and is often faster, but it can take exponential time ([Savani-von Stengel theorem](/savani-von-stengel-theorem/)).
- **Approximate equilibria.** Restricting the supports to size $O(\log n / \varepsilon^2)$ gives an $\varepsilon$-Nash equilibrium in quasi-polynomial time ([Lipton-Markakis-Mehta algorithm](/lipton-markakis-mehta-algorithm/)).
- **Zero-sum games.** For $B = -A$, use the [linear program](/zero-sum-game-linear-programming/), which takes polynomial time.

## When to use it

Use it for small games, when all equilibria are needed, for example to choose the best one, since selecting an equilibrium by welfare or support is NP-hard in general ([hardness of optimal Nash equilibria](/hardness-of-optimal-nash-equilibria/)). Use it as a reference to test other methods, as the tests of this site do. Use the heuristic order when one equilibrium is enough and the game is expected to have one with small supports. For large games, use Lemke-Howson or a learning method, or the LP when the game is zero-sum.

## Pitfalls

- **Swapping the payoff matrices.** The column player's mix $y$ comes from the row player's payoffs $A$, and $x$ comes from $B$. Using $A$ for $x$ is the most common bug.
- **Forgetting the outside strategies.** Indifference on the support is not enough. Line L7 must check every row and every column, also those outside the supports.
- **Accepting zero probabilities.** A solution with $y_j = 0$ for some $j \in J$ belongs to a smaller support; accepting it gives duplicates, and with $y_j < 0$ it is not a strategy at all.
- **Assuming completeness on degenerate games.** In $A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$, $B = \begin{pmatrix} 1 & 1 \\ 0 & 3 \end{pmatrix}$, row 0 has two best responses. The equilibria with $x = (1, 0)$ form the segment $y = (p, 1 - p)$ for $p \ge 1/2$; the method finds the end point $y = (1, 0)$ but not $y = (1/2, 1/2)$.
- **Floating point.** With floats, the tests of lines L5 and L7 need tolerances, and a degenerate game can give false equilibria. Use rationals for an exact list.

## Implementations

The Python code follows lines L1 to L8 in exact rational arithmetic and includes a test for nondegeneracy on small games. The tests check battle of the sexes, chicken, matching pennies, rock-paper-scissors, the coordination games $I_n$ with $2^n - 1$ equilibria, and the example above. On 60 random nondegenerate games, every output is checked as an equilibrium by all pure deviations, the number of equilibria is odd, the supports have equal sizes, and the list equals the one found by an independent vertex enumeration of the best response polytopes. On random degenerate games every output must still be an equilibrium and an extreme one, and the degenerate example of the pitfalls must show the missed end point.

## History

Solving the indifference equations on a guessed support is the basic way to compute a mixed equilibrium by hand, and textbooks such as von Stengel's chapter in NRTV (2007) give it as the first exact method for bimatrix games, together with the fact that equilibrium supports have equal sizes in nondegenerate games. Porter, Nudelman and Shoham presented the ordered search at AAAI 2004 and in the journal version of 2008, and showed that it competes with Lemke-Howson on generated test games.

## References
