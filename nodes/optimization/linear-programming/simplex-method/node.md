---
tag: 1FHAJA
kind: algorithm
slug: simplex-method
name: Simplex method
aliases:
- Dantzig's simplex method
- primal simplex method
- simplex algorithm
area: optimization/linear-programming
level: core
summary: Walk along adjacent vertices of the feasible polyhedron until an optimal vertex is reached.
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of equality constraints}
  time: {worst: O(2^n m n)}
  space: {extra: O(m n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1947
  people: [George B. Dantzig]
  note: Dantzig designed the method in 1947 for planning problems of the US Air Force and published it in 1951.
prereqs: [linear-programming-problem, lp-standard-form, basic-feasible-solution, reduced-cost]
see_also: [pivot-operation, ratio-test, bland-rule, two-phase-simplex-method, revised-simplex-method, dual-simplex-method, klee-minty-cube, interior-point-method]
sources:
  - paper: "George B. Dantzig, Maximization of a linear function of variables subject to linear inequalities, in T. C. Koopmans (ed.), Activity Analysis of Production and Allocation, Cowles Commission Monograph 13, Wiley, 1951"
    locator: Chapter XXI, the first published account of the simplex method
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 2 (How the simplex method works) and Chapter 3 (Pitfalls and how to avoid them)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Chapter 3, Sections 3.1 to 3.3 (optimality conditions, development and implementations of the simplex method) and Section 3.7 (computational efficiency)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.3, The simplex algorithm
  - book: isbn:9780691059136
    title: George B. Dantzig, Linear Programming and Extensions, Princeton University Press, 1963 (reprint 1998)
    locator: Chapter 2, Origins and influences (the Air Force planning problem and the origin of the method in 1947)
  - paper: doi:10.1002/nav.3800020406
    title: E. M. L. Beale, Cycling in the dual simplex algorithm, Naval Research Logistics Quarterly 2(4), 1955
    locator: pages 269 to 275, the cycling example
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977
    locator: pages 103 to 107, the least-index rule
  - paper: "Victor Klee and George J. Minty, How good is the simplex algorithm?, in O. Shisha (ed.), Inequalities III, Academic Press, 1972"
    locator: pages 159 to 175, the exponential example for Dantzig's rule
  - paper: doi:10.1007/bf01917108
    title: Karl Heinz Borgwardt, The average number of pivot steps required by the simplex-method is polynomial, Zeitschrift für Operations Research 26, 1982
    locator: pages 157 to 177
  - paper: doi:10.1145/990308.990310
    title: Daniel A. Spielman and Shang-Hua Teng, Smoothed analysis of algorithms, why the simplex algorithm usually takes polynomial time, Journal of the ACM 51(3), 2004
    locator: pages 385 to 463
---

The simplex method solves a [linear program](/linear-programming-problem/) by moving from one [basic feasible solution](/basic-feasible-solution/) (a vertex of the feasible [polyhedron](/polyhedron/)) to an adjacent one with a better or equal objective value, until no adjacent vertex is better. Each move is a [pivot](/pivot-operation/): one variable enters the basis, chosen by a pivot rule, and one leaves, chosen by the [ratio test](/ratio-test/). It stops with an optimal vertex and a dual certificate, or with a ray along which the objective goes to minus infinity. In the worst case it takes exponentially many pivots, but in practice the number of pivots is a small multiple of the number of constraints, and it is still a main method of LP solvers.

## In plain words

The feasible points of a linear program form a solid with flat faces and corners. If the problem has a best value, then some corner has that value. The simplex method starts at a corner and looks at the edges that leave it. If an edge goes downhill for the objective, it walks along that edge to the next corner. If no edge goes downhill, the corner is the best one, because the solid is convex and a local best is a global best. If some edge goes downhill forever, the problem has no best value.

At each corner the method keeps a small system of equations. A walk along one edge is one exchange of a variable in that system. The method needs only additions, multiplications and divisions, so with exact fractions it gives an exact answer.

## The problem

The input is a linear program in [standard form](/lp-standard-form/):

$$\text{minimize } c^\top x \quad \text{subject to } Ax = b,\ x \ge 0,$$

with $A \in \mathbb{Q}^{m \times n}$, $b \in \mathbb{Q}^m$, $c \in \mathbb{Q}^n$. A *basis* is a list $B = (B(1), \ldots, B(m))$ of $m$ column indices such that the matrix $A_B$ of these columns is nonsingular. Its *basic solution* is $x_B = A_B^{-1} b$, $x_N = 0$ on the other indices $N$. The basis is *feasible* if $x_B \ge 0$. This page assumes that $A$ has rank $m$ and that a feasible basis is given. Phase one of the [two-phase method](/two-phase-simplex-method/) finds one, or shows that the program is [infeasible](/linear-feasibility/), and drops the redundant rows.

The output is one of two answers:

- **optimal**: a basic feasible solution $x^*$ and a vector $y$ with $A^\top y \le c$ and $b^\top y = c^\top x^*$. By [weak duality](/weak-duality/), $y$ proves that $x^*$ is optimal.
- **unbounded**: a feasible $x$ and a direction $d \ge 0$ with $Ad = 0$ and $c^\top d < 0$. Then $x + t d$ is feasible for each $t \ge 0$, and $c^\top (x + td) \to -\infty$.

## The algorithm

For a basis $B$, let $y = A_B^{-\top} c_B$ be the simplex multipliers. The [reduced cost](/reduced-cost/) of column $j$ is $r_j = c_j - y^\top A_j$. It is $0$ for each basic column.

```pseudo id=main
SIMPLEX(A, b, c, B)                     ▷ B is a feasible basis
L1  loop
L2      x_B ← A_B⁻¹ b,  y ← A_B⁻ᵀ c_B,  r_j ← c_j − yᵀA_j for each j
L3      if r_j ≥ 0 for every j then return OPTIMAL(x, y)
L4      choose q with r_q < 0                       ▷ the pivot rule
L5      d ← A_B⁻¹ A_q                               ▷ x_B changes by −t d when x_q = t
L6      if d ≤ 0 then return UNBOUNDED(x, direction with x_q = 1, x_B = −d)
L7      choose p with d_p > 0 that minimizes x_B(p) / d_p   ▷ the ratio test
L8      B(p) ← q                                    ▷ the pivot: q enters, B(p) leaves
```

Line L2 computes the current vertex and the reduced costs. A tableau implementation does not solve these systems from scratch: it keeps the matrix $A_B^{-1} [A \mid b]$ and the row of reduced costs, and each pivot updates them with one Gauss-Jordan step, as in the [pivot operation](/pivot-operation/). The [revised simplex method](/revised-simplex-method/) keeps a factorization of $A_B$ instead.

Line L4 picks an improving direction. If $x_q$ rises from $0$ to $t$ and the other nonbasic variables stay at $0$, then $Ax = b$ forces $x_B = A_B^{-1} b - t d$, and the objective changes by $t\, r_q$. So a negative $r_q$ means that the objective falls along this edge. Which negative $r_q$ to take is the *pivot rule*: [Dantzig's rule](/dantzig-pivot-rule/) takes the most negative one, [Bland's rule](/bland-rule/) the one with the least index, and the [steepest-edge rule](/steepest-edge-pivot-rule/) the one with the most descent per unit of length.

Line L6 tests whether the edge is a ray. If no entry of $d$ is positive, then no basic variable falls as $t$ grows, every $t \ge 0$ is feasible, and the objective is unbounded below.

Line L7 is the [minimum ratio test](/ratio-test/). The step $t$ can grow until the first basic variable reaches $0$. That variable leaves. The new basis is again feasible, and it is a basis because $d_p \ne 0$. If the minimum ratio is $0$, the step has length zero: the vertex is [degenerate](/lp-degeneracy/), the basis changes but the point does not.

## Example

Minimize $-3x_1 - 5x_2$ subject to $x_1 \le 4$, $2x_2 \le 12$, $3x_1 + 2x_2 \le 18$ and $x \ge 0$. Add the slack variables $x_3, x_4, x_5$ to get the standard form with $b = (4, 12, 18)$. The slack columns form an identity matrix, so $B = (3, 4, 5)$ is a feasible basis at the origin. The rule is Dantzig's rule.

| step | basis | $x$ | $c^\top x$ | reduced costs $r_1, \ldots, r_5$ | entering, $d$ | ratios | leaving |
|---|---|---|---|---|---|---|---|
| 0 | $(3, 4, 5)$ | $(0, 0, 4, 12, 18)$ | $0$ | $-3, -5, 0, 0, 0$ | $x_2$, $(0, 2, 2)$ | $-, 6, 9$ | $x_4$ |
| 1 | $(3, 2, 5)$ | $(0, 6, 4, 0, 6)$ | $-30$ | $-3, 0, 0, 5/2, 0$ | $x_1$, $(1, 0, 3)$ | $4, -, 2$ | $x_5$ |
| 2 | $(3, 2, 1)$ | $(2, 6, 2, 0, 0)$ | $-36$ | $0, 0, 0, 3/2, 1$ | | | |

At step 2 all reduced costs are nonnegative, so $x^* = (2, 6)$ is optimal with value $-36$. The multipliers are $y = (0, -3/2, -1)$: each reduced cost of a slack column is $0 - y_i$. Then $A^\top y \le c$ and $b^\top y = -18 - 18 = -36$, which proves optimality. The method visited 3 of the 5 vertices of the feasible polygon.

## Correctness

Three invariants hold at line L1: $B$ is a basis, its basic solution is feasible, and $c^\top x$ never rises. At line L3 the vector $y$ is dual feasible, since $A^\top y \le c$ is the statement $r \ge 0$, and $b^\top y = c_B^\top A_B^{-1} b = c^\top x$. So weak duality proves that $x$ is optimal. At line L6 the direction is a ray of descent. Each step either lowers $c^\top x$ by $\theta\, |r_q| > 0$ or keeps the same point. Bases never repeat when every step lowers the objective, and with Bland's rule they never repeat at all ([simplex termination](/simplex-termination/)). There are finitely many bases, so the method stops. The full proof is in the proof file below.

## Complexity

Model: arithmetic operations on rationals have unit cost (the [real RAM](/real-ram/)); for the bit cost, the entries of the tableau are ratios of subdeterminants of $[A \mid b]$, so their length is polynomial in the input length.

- **One pivot.** The tableau has $m + 1$ rows and $n + 1$ columns, and one Gauss-Jordan step updates each entry once, so a pivot takes $O(mn)$ operations. The ratio test takes $O(m)$, and Dantzig's or Bland's rule takes $O(n)$.
- **The number of pivots.** If no basis repeats, the number of pivots is at most the number of bases, $\binom{n}{m} \le 2^n$. This gives the bound $O(2^n m n)$ of the front matter for Bland's rule.
- **Worst case.** The bound is exponential for each common rule. On the [Klee-Minty cube](/klee-minty-cube/) with $n$ variables, Dantzig's rule takes $2^n - 1$ pivots. Bland's rule and the steepest-edge rule also have exponential examples. No pivot rule is known to take a polynomial number of pivots; this is tied to the [Hirsch conjecture](/hirsch-conjecture/) on the diameter of polytopes.
- **Average and smoothed case.** Borgwardt proved a polynomial bound on the expected number of pivots of the shadow vertex rule for random programs with a rotation-invariant distribution. Spielman and Teng proved a polynomial [smoothed bound](/smoothed-simplex-analysis/) for the same rule.
- **Space.** The tableau needs $O(mn)$ numbers.

In practice the number of pivots on real problems is usually between $m$ and a small multiple of $m$.

## Properties

- **Exact.** With rational input and exact arithmetic, the output is an exact vertex and an exact dual certificate.
- **Vertex output.** The answer is a basic solution, with at most $m$ nonzero entries. [Interior-point methods](/interior-point-method/) need an extra step to reach a vertex.
- **Warm start.** A basis from a previous run is a valid start after a change of $c$, so the method is fast in branch and bound and in [sensitivity analysis](/lp-sensitivity-analysis/).
- **Not polynomial.** No known pivot rule is polynomial in the worst case.

## Variants and improvements

- **[Two-phase method](/two-phase-simplex-method/) and the [big-M method](/big-m-method/).** They find the first feasible basis.
- **[Revised simplex method](/revised-simplex-method/).** It keeps a factorization of $A_B$ and computes only the column $d$ and the row of reduced costs that the rule needs. It is the form that solvers use.
- **[Dual simplex method](/dual-simplex-method/).** It keeps $r \ge 0$ and moves toward $x_B \ge 0$. It suits a program after the addition of a constraint.
- **Pivot rules.** [Dantzig's rule](/dantzig-pivot-rule/), [Bland's rule](/bland-rule/), the [steepest-edge rule](/steepest-edge-pivot-rule/), the lexicographic rule, and randomized rules such as random edge and random facet.
- **Bounded variables.** Bounds $\ell \le x \le u$ are kept implicit: a nonbasic variable sits at one of its bounds, and the ratio test also stops when the entering variable reaches its other bound.
- **[Network simplex](/network-simplex/).** For [minimum-cost flow](/min-cost-flow-lp-formulation/), a basis is a spanning tree, and a pivot is a cycle in a tree.

## When to use it

Use the simplex method when you need an exact vertex, a dual solution, or a warm start from a nearby problem, as in branch and bound for [integer programming](/lp-relaxation/) and in [column generation](/column-generation/). Use an [interior-point method](/interior-point-method/) for very large sparse programs where many pivots would be needed, and when a polynomial bound matters. The [ellipsoid method](/ellipsoid-method/) is polynomial but slow, and it is mainly a tool of theory. In fixed small dimension, [Seidel's algorithm](/seidel-linear-programming/) and [Megiddo's algorithm](/megiddo-fixed-dimension-lp/) take linear time in the number of constraints.

## Pitfalls

- **Cycling.** With Dantzig's rule and a tie rule of least index, the method cycles on Beale's example: after 6 pivots of length zero it returns to the first basis. Use Bland's rule, the lexicographic rule or a perturbation in line L4 and line L7.
- **The wrong sign in the ratio test.** Line L7 takes only rows with $d_p > 0$. A row with $d_p < 0$ or $d_p = 0$ gives no bound, and a ratio with a negative $d_p$ makes the next basis infeasible.
- **A start that is not feasible.** Line L1 assumes $A_B^{-1} b \ge 0$. With $b \not\ge 0$ the slack basis is not feasible; run phase one first.
- **Floating-point ties.** In floating point, a reduced cost of $-10^{-15}$ is noise. Solvers use tolerances on lines L3, L6 and L7, and refactorize the basis from time to time. This page uses exact fractions so that the tests decide ties exactly.
- **Redundant rows.** If $A$ does not have rank $m$, no basis of size $m$ exists. Phase one detects these rows.

## Implementations

The Python version keeps a dense tableau of `Fraction` values. `simplex_method` is phase two from a given feasible basis, with the rules `"bland"`, `"dantzig"` and `"steepest-edge"`, and it reports `"cycle"` if a basis repeats. `solve` adds a phase one. The tests compare the result with an enumeration of all bases, on feasible, infeasible, unbounded and degenerate programs, and check the dual certificate and [complementary slackness](/complementary-slackness/). They also check that Dantzig's rule cycles on Beale's example while Bland's rule reaches the optimum $-5/4$, and that Dantzig's rule takes $2^n - 1$ pivots on the Klee-Minty program for $n \le 7$.

## History

George Dantzig designed the simplex method in 1947, for the planning problems of the US Air Force, and published it in 1951 in the Cowles Commission volume edited by Koopmans. Beale gave a small example of cycling in 1955, and Bland gave his simple rule against cycling in 1977. Klee and Minty showed in 1972 that Dantzig's rule can take exponentially many pivots. Borgwardt (1982) and Spielman and Teng (2004) gave two explanations of why the method is fast in practice: an average-case bound and a smoothed bound.

## References
