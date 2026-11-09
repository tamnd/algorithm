---
tag: CKF9R5
kind: problem
slug: linear-feasibility
name: Linear feasibility problem
aliases:
- LP feasibility
- linear inequality feasibility
- feasibility of linear inequalities
area: optimization/linear-programming
level: intro
summary: Decide whether a system of linear inequalities has a solution.
prereqs: [polyhedron]
see_also: [farkas-lemma, fourier-motzkin-elimination, linear-programming-problem, two-phase-simplex-method, ellipsoid-method, difference-constraints, megiddo-fixed-dimension-lp, lp-in-p]
sources:
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 10, Sizes and the theoretical complexity of linear inequalities and linear programming (polynomial size of solutions and certificates), Chapter 12, Primal-dual, elimination, and relaxation methods, and Chapter 13, Khachiyan's method for linear programming
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 2.8, Projections of polyhedra (Fourier-Motzkin elimination), Section 3.5, Finding an initial basic feasible solution, and Chapter 8, The ellipsoid method (Section 8.2, feasibility of a system of inequalities)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 24.4, Difference constraints and shortest paths, and Section 29.5, The initial basic feasible solution (the auxiliary program)
---

The linear feasibility problem asks whether a finite system of linear inequalities has a common solution, that is, whether a [polyhedron](/polyhedron/) given by inequalities is empty. It is linear programming with no objective, and it is no easier: by [LP duality](/lp-duality/), an optimization problem can be written as one feasibility problem. The answer always has a short proof: a solution if the system is feasible, and a [Farkas](/farkas-lemma/) vector of multipliers if it is not.

## In plain words

You are given a list of limits, each one a linear rule such as "twice the first amount plus the second is at most ten". The question is whether some choice of the amounts obeys all the limits at once. If the answer is yes, a valid choice proves it. If the answer is no, there is still a proof: weights that add the limits up to an obviously false statement. Fast methods find one of the two proofs. A special case, where each limit compares just two amounts, is solved by a shortest path method on a graph.

## Definition

**Input.** A matrix $A \in \mathbb{Q}^{m \times n}$ and a vector $b \in \mathbb{Q}^m$, given in binary. Let $L$ be the total bit length.

**Question.** Is there $x \in \mathbb{R}^n$ with $Ax \le b$?

**Search version.** Output such an $x$, or a vector $y \in \mathbb{Q}^m$ with $y \ge 0$, $y^\top A = 0$ and $y^\top b < 0$. By [Farkas' lemma](/farkas-lemma/) exactly one of the two exists.

If the system is feasible, it has a rational solution of size polynomial in $L$: by the [polyhedron](/polyhedron/) page, a nonempty polyhedron has a minimal face defined by a set of tight rows, and a point of it is a solution of a square nonsingular subsystem, whose size is bounded by [Cramer's rule](/cramers-rule/) and the [Hadamard bound](/hadamard-bound/). The same holds for a certificate $y$.

## Variants

- **Equality form.** Is there $x \ge 0$ with $Ax = b$? This is the feasible set of the [standard form](/lp-standard-form/), and it is equivalent to the inequality form by the conversions on that page.
- **Strict inequalities.** Is there $x$ with $Ax < b$, or with a mix of strict and weak rows? The certificate is Motzkin's transposition theorem. A strict system $Ax < b$ is feasible if and only if $\max\{t : Ax + t\mathbf{1} \le b,\ t \le 1\}$ is positive, so it reduces to LP.
- **Homogeneous systems.** Is there $x$ with $Ax < 0$, that is, are the rows of $A$ strictly separated from the origin? This is the problem of finding a linear classifier for separable data. The perceptron and the relaxation method of Agmon, Motzkin and Schoenberg solve it, with a number of steps that depends on the margin.
- **Two variables per inequality.** Each row has at most two nonzero coefficients. The special case $x_v - x_u \le w_{uv}$ is a system of [difference constraints](/difference-constraints/), solved by [Bellman-Ford](/bellman-ford/) in $O(mn)$ time. The general two-variable case also has strongly polynomial algorithms (Megiddo; Hochbaum and Naor).
- **Fixed dimension.** For constant $n$, feasibility is solved in $O(m)$ time by [Megiddo's algorithm](/megiddo-fixed-dimension-lp/) or in expected $O(m)$ time by [Seidel's algorithm](/seidel-linear-programming/).
- **Integer feasibility.** Is there an integral $x$ with $Ax \le b$? This is NP-complete; see [mixed integer programming](/mixed-integer-programming/).

## Examples

**Feasible.** The running system $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $-x_1 \le 0$, $-x_2 \le 0$ is feasible; $(0, 0)$ is a solution.

**Infeasible, with a certificate.** The system

$$x_1 + x_2 \le 1, \qquad -x_1 \le -2, \qquad -x_2 \le 0$$

has no solution. The multipliers $y = (1, 1, 1)$ give $0 x_1 + 0 x_2 \le -1$.

**Difference constraints.** The system $x_2 - x_1 \le 3$, $x_3 - x_2 \le -2$, $x_1 - x_3 \le -2$ is infeasible: adding the three rows gives $0 \le -1$, and in the constraint graph the cycle $1 \to 2 \to 3 \to 1$ has weight $3 - 2 - 2 = -1$, a [negative cycle](/negative-cycle/). With the last row changed to $x_1 - x_3 \le 0$, the cycle weight is $+1$, and shortest distances from an added source with 0-weight arcs give the solution $x = (-2, 0, -2)$.

**Optimization as feasibility.** The program $\max 3x_1 + 2x_2$ over the running system has optimum 11 if and only if the system plus $3x_1 + 2x_2 \ge 11$ is feasible and the system plus $3x_1 + 2x_2 \ge 11 + \varepsilon$ is not, for every $\varepsilon > 0$. The duality system below avoids the search over values.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) | up to $4(m/4)^{2^n}$ rows | exact, returns a point or a Farkas vector; practical only for small $n$ |
| Phase 1 of the [two-phase simplex method](/two-phase-simplex-method/) | exponential in the worst case | minimizes the sum of artificial variables; fast in practice |
| [Ellipsoid method](/ellipsoid-method/) | polynomial in $n$ and $L$ | Khachiyan (1979); needs only a [separation oracle](/separation-oracle/) |
| [Interior point methods](/interior-point-method/) | $O(\sqrt{n} L)$ iterations | homogeneous self-dual forms also return infeasibility certificates |
| [Bellman-Ford](/bellman-ford/) | $O(mn)$ | for [difference constraints](/difference-constraints/) only |
| [Megiddo](/megiddo-fixed-dimension-lp/), [Seidel](/seidel-linear-programming/) | $O(m)$ for fixed $n$ | the constant grows fast with $n$ |

## Bounds

- **In P.** Khachiyan's [ellipsoid method](/ellipsoid-method/) decides feasibility in time polynomial in $L$; see [LP is in P](/lp-in-p/).
- **Good characterization.** Before 1979 the problem was known to be in $\text{NP} \cap \text{coNP}$: a solution and a Farkas vector are both polynomial-size certificates, so it was a [good characterization](/good-characterization/).
- **Strongly polynomial: open.** No algorithm is known whose number of arithmetic operations is polynomial in $m$ and $n$ alone. Tardos (1986) gave an algorithm whose running time depends on the size of $A$ but not on the size of $b$ and $c$. It is strongly polynomial when the entries of $A$ are small integers, which covers all network problems.
- **P-complete.** Linear feasibility is P-complete under log-space reductions (Dobkin, Lipton and Reiss, 1979), so it probably has no fast parallel algorithm.
- **Equivalent to optimization.** Under polynomial-time reductions, deciding feasibility and solving LP optimization are equivalent.

## Reductions

- **Optimization to feasibility.** The optima of $\max c^\top x$, $Ax \le b$, $x \ge 0$ and its dual are exactly the solutions of $Ax \le b$, $x \ge 0$, $A^\top y \ge c$, $y \ge 0$, $c^\top x \ge b^\top y$, by [strong duality](/strong-duality/). So one feasibility call solves the LP, if it is optimal.
- **Feasibility to optimization.** $Ax \le b$ is feasible if and only if $\min \{ t : Ax - t \mathbf{1} \le b,\ t \ge 0 \}$ is 0. This program is always feasible (take $x = 0$ and $t$ large), so a solver for optimal LPs answers feasibility. Phase 1 of the simplex method is this reduction in the equality form.
- **Difference constraints to shortest paths.** A system of difference constraints is feasible if and only if its constraint graph has no negative cycle, and the shortest distances from a new source are a solution.
- **Projection.** [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) reduces feasibility in $n$ variables to feasibility in $n - 1$ variables, at the cost of more rows.

## Applications

- Finding a starting point for the [simplex method](/simplex-method/); see [initial basic feasible solution](/initial-basic-feasible-solution/).
- Checking that a set of design or scheduling rules can be met, and returning a certificate (a small set of conflicting rules) if it cannot.
- Testing whether two point sets are separable by a hyperplane, the first step of a [support vector machine](/support-vector-machine/).
- Temporal reasoning and timing analysis, through [difference constraints](/difference-constraints/).
- Deciding whether a point lies in the [convex hull](/convex-hull-problem/) of given points, a feasibility problem in the equality form.

## References
