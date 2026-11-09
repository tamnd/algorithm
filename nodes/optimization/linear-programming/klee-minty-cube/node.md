---
tag: F2XJDA
kind: concept
slug: klee-minty-cube
name: Klee-Minty cube
aliases:
- Klee-Minty example
- Klee-Minty problem
area: optimization/linear-programming
level: advanced
summary: Deformed cube on which Dantzig's simplex rule visits exponentially many vertices.
prereqs: [simplex-method, dantzig-pivot-rule, basic-feasible-solution]
see_also: [dantzig-pivot-rule, bland-rule, steepest-edge-pivot-rule, hirsch-conjecture, smoothed-simplex-analysis, lp-in-p, ellipsoid-method, gray-code]
sources:
  - paper: "Victor Klee and George J. Minty, How good is the simplex algorithm?, in O. Shisha (ed.), Inequalities III, Academic Press, 1972"
    locator: pages 159 to 175, the deformed cubes on which the largest coefficient rule visits all 2^n vertices
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 4, How fast is the simplex method (the Klee-Minty examples in the form with powers of 10 and 100)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.7, Computational efficiency of the simplex method (the deformed cube with a parameter epsilon)
  - paper: doi:10.1007/BFb0121192
    title: David Avis and Vašek Chvátal, Notes on Bland's pivoting rule, Mathematical Programming Study 8, 1978
    locator: pages 24 to 34, exponential examples for Bland's rule
  - paper: doi:10.1016/0166-218X(79)90004-0
    title: Donald Goldfarb and William Y. Sit, Worst case behavior of the steepest edge simplex method, Discrete Applied Mathematics 1(4), 1979
    locator: pages 277 to 285, exponential examples for the steepest-edge rule
  - paper: doi:10.1016/0012-365X(73)90171-4
    title: Robert G. Jeroslow, The simplex algorithm with the pivot rule of maximizing criterion improvement, Discrete Mathematics 4(4), 1973
    locator: pages 367 to 377, exponential examples for the largest improvement rule
---

The Klee-Minty cube is a family of linear programs in $n$ variables whose feasible region is a slightly squashed $n$-dimensional cube, built so that the [simplex method](/simplex-method/) with [Dantzig's pivot rule](/dantzig-pivot-rule/) visits all $2^n$ vertices before it stops. Klee and Minty published it in 1972 to answer the question "how good is the simplex algorithm?": in the worst case the method with this rule takes exponential time. Later variants gave the same lower bound for almost every pivot rule that was studied, which led to the search for [polynomial methods](/lp-in-p/) and for a bound on the diameter of polytopes, the [Hirsch conjecture](/hirsch-conjecture/).

## In plain words

Take a cube and squash it a little, so that the corners are at different heights. The simplex method starts at the lowest corner and must reach the highest one, always moving along an edge to a higher corner. A good choice of edges reaches the top in a few moves.

Dantzig's rule always takes the edge that rises fastest at the start. Klee and Minty tilted the cube so that this choice is always the wrong one: the fast edge leads to a corner just a bit higher, and from there the walk must visit every corner of a smaller cube again. The result is a walk that visits every corner of the cube, one at a time. For a cube in 50 dimensions that is about a million billion moves.

## The idea

**The program.** In the form of Chvátal's textbook, written as a minimization:
$$\text{minimize } -\sum_{j=1}^{n} 10^{n-j} x_j \quad \text{subject to} \quad 2\sum_{j=1}^{i-1} 10^{i-j} x_j + x_i \le 100^{i-1} \ (i = 1, \ldots, n), \quad x \ge 0.$$
Add a slack $s_i$ to constraint $i$. Call $\{x_i, s_i\}$ the pair $i$. The start is the slack basis at the origin.

**Theorem.** From the slack basis, the simplex method with Dantzig's rule makes exactly $2^n - 1$ pivots and visits all $2^n$ vertices.

*Step 1: the bases.* Let $S_0 = 0$ and $S_i = \sum_{j \le i} 10^{i-j} x_j = 10 S_{i-1} + x_i$, so the objective is $-S_n$ and constraint $i$ reads $x_i + s_i = 100^{i-1} - 20 S_{i-1}$. At every feasible point, $S_i \le 10S_{i-1} + 100^{i-1} - 20S_{i-1} \le 100^{i-1}$, so $x_i + s_i \ge 100^{i-1} - 20 \cdot 100^{i-2} > 0$ for $i \ge 2$, and $x_1 + s_1 = 1$. So $x_i$ and $s_i$ are never both zero. A basis has $n$ variables, so a feasible basis contains exactly one variable of each pair, and its basic solution has no zero basic variable. Conversely, each of the $2^n$ choices of one variable from each pair gives a feasible basis: set the other one of each pair to zero and solve the constraints in the order $i = 1, \ldots, n$; each basic value is $100^{i-1} - 20S_{i-1} > 0$. So the region has exactly $2^n$ vertices, none degenerate.

*Step 2: the reduced costs.* Fix such a basis and let $v_j$ be the nonbasic variable of pair $j$. By induction on $i$, $S_i$ is a constant plus $\sum_{j \le i} \pm 10^{i-j} v_j$. If $x_i$ is nonbasic, $S_i = 10S_{i-1} + x_i$. If $x_i$ is basic, $x_i = 100^{i-1} - 20S_{i-1} - s_i$, so $S_i = 100^{i-1} - 10S_{i-1} - s_i$. In both cases the coefficients of the earlier $v_j$ are multiplied by $\pm 10$ and the new $v_i$ gets $\pm 1$. So the [reduced cost](/reduced-cost/) of $v_j$ in the objective $-S_n$ is $\pm 10^{n-j}$. More exactly, write $b_i = 1$ if $x_i$ is basic and $b_i = 0$ if not. Then the reduced cost of $v_j$ is negative exactly when $P_j = \sum_{i \ge j} b_i$ is even.

*Step 3: the walk.* The magnitudes $10^{n-j}$ are all different, so Dantzig's rule enters $v_j$ for the smallest $j$ with $P_j$ even. The new basis is feasible, so by Step 1 the leaving variable is the other variable of pair $j$, and the pivot flips $b_j$. This toggles the parities of $P_1, \ldots, P_j$ and leaves the others. Let $o_k = 1$ if $P_k$ is odd, and read $N = \sum_k o_k 2^{k-1}$ as a binary number. Before the pivot $o_1 = \cdots = o_{j-1} = 1$ and $o_j = 0$; after it $o_j = 1$ and $o_1 = \cdots = o_{j-1} = 0$. So each pivot adds exactly $1$ to $N$. At the start all $b_i = 0$, so $N = 0$. The method stops when no reduced cost is negative, that is when all $P_k$ are odd and $N = 2^n - 1$. So it makes $2^n - 1$ pivots, every basis on the way is different, and it visits all $2^n$ vertices. $\blacksquare$

The order in which the pivots flip the pairs is the same as in the binary reflected [Gray code](/gray-code/): pair 1 flips at every second step, pair 2 at every fourth, and pair $n$ once, in the middle.

**The deformed cube.** Bertsimas and Tsitsiklis use the form $0 \le x_1 \le 1$ and $\varepsilon x_{i-1} \le x_i \le 1 - \varepsilon x_{i-1}$ for $i = 2, \ldots, n$, with $0 < \varepsilon < 1/2$ and the objective "maximize $x_n$". It is a small perturbation of the unit cube, and they show that it has a path along edges through all $2^n$ vertices on which the objective improves at every step.

## Examples

**Three variables.** The program is: minimize $-100x_1 - 10x_2 - x_3$ subject to $x_1 \le 1$, $20x_1 + x_2 \le 100$, $200x_1 + 20x_2 + x_3 \le 10000$, $x \ge 0$. Dantzig's rule makes 7 pivots:

| pivot | vertex $(x_1, x_2, x_3)$ | value | entering |
|---|---|---|---|
| 0 | $(0, 0, 0)$ | $0$ | $x_1$ (reduced cost $-100$) |
| 1 | $(1, 0, 0)$ | $-100$ | $x_2$ ($-10$) |
| 2 | $(1, 80, 0)$ | $-900$ | $s_1$ ($-100$) |
| 3 | $(0, 100, 0)$ | $-1000$ | $x_3$ ($-1$) |
| 4 | $(0, 100, 8000)$ | $-9000$ | $x_1$ ($-100$) |
| 5 | $(1, 80, 8200)$ | $-9100$ | $s_2$ ($-10$) |
| 6 | $(1, 0, 9800)$ | $-9900$ | $s_1$ ($-100$) |
| 7 | $(0, 0, 10000)$ | $-10000$ | none: optimal |

The first three pivots solve the problem in $x_1, x_2$ alone. Then $x_3$ enters, and the next three pivots walk back through the same face in reverse.

**Other pivot rules on the same program.** Pivot counts from the slack basis:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Dantzig's rule | 1 | 3 | 7 | 15 | 31 | 63 | 127 | 255 | 511 | 1023 |
| [Bland's rule](/bland-rule/) | 1 | 3 | 5 | 9 | 15 | 25 | 41 | 67 | 109 | 177 |
| [steepest edge](/steepest-edge-pivot-rule/) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Steepest edge goes straight from the origin to the optimum $(0, \ldots, 0, 100^{n-1})$, which is adjacent to it. Other deformations defeat the other rules: Jeroslow (1973) for the largest improvement rule, Avis and Chvátal (1978) for Bland's rule, and Goldfarb and Sit (1979) for steepest edge.

## Where it is used

- **Lower bounds for pivot rules.** It is the model for the exponential examples of nearly all deterministic pivot rules. No pivot rule is known to make a polynomial number of pivots on every program.
- **The case for other methods.** The exponential worst case of the simplex method, against its good behavior in practice, motivated the [ellipsoid method](/ellipsoid-method/) and [interior-point methods](/interior-point-method/), whose worst case is polynomial, and the [smoothed analysis](/smoothed-simplex-analysis/) of Spielman and Teng, which explains the practical behavior.
- **Diameter and paths.** The cube itself has diameter $n$, so the long walk is a property of the rule, not of the polytope. The question of how short a path always exists is the [Hirsch conjecture](/hirsch-conjecture/).
- **Testing codes.** The program is a standard small test for pivot rules and exact solvers: its coefficients grow like $100^n$, so it also tests the handling of large numbers.

## References
