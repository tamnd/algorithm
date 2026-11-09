---
tag: PCX05V
kind: problem
slug: linear-programming-problem
name: Linear programming
aliases: [LP, linear program, linear optimization]
area: optimization/linear-programming
level: core
summary: Optimize a linear objective function subject to linear equality and inequality constraints over real-valued variables.
prereqs: [polyhedron, convex-set]
see_also: [lp-standard-form, linear-feasibility, fundamental-theorem-of-lp, lp-duality, simplex-method, ellipsoid-method, interior-point-method, lp-in-p]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Chapter 1 (the forms of a linear program and the examples), Chapter 2 (the geometry), Chapter 8 (the ellipsoid method) and Chapter 9 (interior point methods)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 10 (sizes of solutions and the complexity of linear programming), Chapter 13 (Khachiyan's method) and Chapter 15 (further polynomiality results, with Karmarkar's method, Tardos' method and Megiddo's method)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 1 (what a linear program is), Chapter 2 (examples) and Chapter 7 (the ellipsoid and interior point methods)
  - paper: "L. G. Khachiyan, A polynomial algorithm in linear programming, Doklady Akademii Nauk SSSR 244 (1979), 1093 to 1096; English translation in Soviet Mathematics Doklady 20 (1979), 191 to 194"
    locator: the main theorem (linear programming over the rationals in time polynomial in the input length)
  - paper: doi:10.1007/BF02579150
    title: N. Karmarkar, A new polynomial-time algorithm for linear programming, Combinatorica 4(4), 373 to 395 (1984)
    locator: the main theorem (O(n^3.5 L) arithmetic operations)
  - paper: "Victor Klee and George J. Minty, How good is the simplex algorithm?, in O. Shisha (editor), Inequalities III, Academic Press, 1972, pages 159 to 175"
    locator: the deformed cube on which Dantzig's rule visits all 2^n vertices
  - paper: "Steve Smale, Mathematical problems for the next century, The Mathematical Intelligencer 20(2), 7 to 15 (1998)"
    locator: Problem 9 (is there a strongly polynomial algorithm for linear programming)
  - paper: "David P. Dobkin, Richard J. Lipton and Steven P. Reiss, Linear programming is log-space hard for P, Information Processing Letters 8(2), 96 to 97 (1979)"
    locator: the whole note
---

The linear programming problem asks for a point that minimizes or maximizes a linear function over the set of points that satisfy finitely many linear equations and inequalities. That set is a [polyhedron](/polyhedron/), so each instance is either infeasible, unbounded, or has an optimum that is attained at a vertex when the polyhedron has one. The [simplex method](/simplex-method/) solves it fast in practice, and the [ellipsoid method](/ellipsoid-method/) and [interior point methods](/interior-point-method/) solve it in time polynomial in the bit length of the input. It is the base of [integer programming](/mixed-integer-programming/), of many approximation algorithms, and of the duality theory of network flows.

## In plain words

You have a few quantities to choose, for example how much of each product a factory makes. Each choice earns or costs money at a fixed rate per unit. Each resource, such as machine hours or raw material, puts a limit on a sum of the quantities, again with fixed rates. You want the choice that earns the most and keeps every limit.

All the allowed choices form a region with flat sides and sharp corners, like a cut gem. The best value, if there is one, is always found at a corner. The problem can also have no allowed choice at all, or it can let the earnings grow without end. A solver must find out which of these three things is true and, in the first case, return a best choice.

## Definition

**Notation.** The page uses the conventions of the optimization area: $n$ is the number of variables, $m$ the number of constraints, $x \in \mathbb{R}^n$ the vector of variables, and $L$ the number of binary digits needed to write the input. The data are rational, so that $L$ is defined.

**General form.** The input is a cost vector $c \in \mathbb{Q}^n$, a matrix $A \in \mathbb{Q}^{m \times n}$ and a vector $b \in \mathbb{Q}^m$, together with a partition of the rows into the types $\le$, $=$ and $\ge$ and a choice, for each variable, of $x_j \ge 0$, $x_j \le 0$ or $x_j$ free. The *feasible set* $P$ is the set of all $x \in \mathbb{R}^n$ that satisfy each row $a_i^\top x \ \square_i\ b_i$ and each sign condition. The task is

$$\text{minimize } c^\top x \quad \text{subject to } x \in P.$$

A maximization problem is the minimization of $-c^\top x$, so nothing is lost by fixing the sense.

**The two working forms.** Each general LP converts, with at most a doubling of the variables plus one slack per inequality, to the *equality form*

$$\min\ c^\top x \quad \text{s.t.} \quad Ax = b,\ x \ge 0,$$

which is the default form of the optimization pages, and to the *inequality form* $\max c^\top x$ s.t. $Ax \le b$, $x \ge 0$. The page [standard form](/lp-standard-form/) gives both, the names that different books use for them, and the conversion rules.

**The output.** Exactly one of three cases holds, and a solver must report which one:

1. *Infeasible*: $P = \emptyset$.
2. *Unbounded*: $P \ne \emptyset$ and $\inf_{x \in P} c^\top x = -\infty$.
3. *Optimal*: there is $x^* \in P$ with $c^\top x^* = \min_{x \in P} c^\top x = f^*$.

That no fourth case exists (a finite infimum that is not attained) is part of the [fundamental theorem of linear programming](/fundamental-theorem-of-lp/). In case 3 a solver returns $x^*$, and a good solver also returns a *certificate*: an optimal [dual](/dual-linear-program/) solution $y^*$ with $b^\top y^* = c^\top x^*$. In case 1 the certificate is a [Farkas](/farkas-lemma/) vector, and in case 2 it is a feasible point and a ray $d \ge 0$ with $Ad = 0$ and $c^\top d < 0$.

## Variants

- **Feasibility.** Decide whether $P \ne \emptyset$, and find a point of $P$ if so. This is the [linear feasibility problem](/linear-feasibility/). It is as hard as optimization up to a polynomial factor (see Reductions).
- **Decision version.** Given also a rational $t$, decide whether some $x \in P$ has $c^\top x \le t$. With rational data this problem is in [P](/p/).
- **Fixed dimension.** When $n$ is a constant, the problem is solved in $O(m)$ time by [Megiddo's algorithm](/megiddo-fixed-dimension-lp/) and in expected $O(m)$ time by [Seidel's randomized algorithm](/seidel-linear-programming/). Each is an [LP-type problem](/lp-type-problem/) method.
- **Integer and mixed integer programming.** Add the condition that some or all $x_j$ are integers. The problem becomes [NP-hard](/np-hard/); see [mixed integer programming](/mixed-integer-programming/) and the [LP relaxation](/lp-relaxation/).
- **Parametric programming.** The data $b$ or $c$ depend on a parameter $\lambda$, and the answer is the optimal value as a function of $\lambda$; see [parametric linear programming](/parametric-linear-programming/).
- **Network LPs.** When $A$ is the [incidence matrix](/incidence-matrix/) of a directed graph, the LP is a flow problem: [maximum flow](/max-flow-lp-formulation/), [minimum cost flow](/min-cost-flow-lp-formulation/) or [shortest paths](/shortest-paths-lp-formulation/).
- **Approximate solution.** Interior point and first order methods return $x$ with $c^\top x - f^* \le \varepsilon$ and a small violation of the constraints. With rational data and $\varepsilon = 2^{-O(L)}$, such a point rounds to an exact vertex.

## Examples

**An instance with an optimum.** Maximize $3x_1 + 2x_2$ subject to

$$x_1 + x_2 \le 4, \qquad x_1 + 3x_2 \le 9, \qquad x_1 \le 3, \qquad x_1, x_2 \ge 0.$$

The feasible set is a pentagon. Its vertices and the objective at each one are:

| vertex | tight constraints | $3x_1 + 2x_2$ |
|---|---|---|
| $(0, 0)$ | $x_1 \ge 0$, $x_2 \ge 0$ | 0 |
| $(3, 0)$ | $x_1 \le 3$, $x_2 \ge 0$ | 9 |
| $(3, 1)$ | $x_1 + x_2 \le 4$, $x_1 \le 3$ | **11** |
| $(3/2, 5/2)$ | $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$ | 19/2 |
| $(0, 3)$ | $x_1 + 3x_2 \le 9$, $x_1 \ge 0$ | 6 |

So $x^* = (3, 1)$ and $f^* = 11$. The dual solution $y^* = (2, 0, 1)$ (one multiplier per constraint) certifies it: $2(x_1 + x_2) + 0(x_1 + 3x_2) + 1 \cdot x_1 = 3x_1 + 2x_2$, so each feasible $x$ has $3x_1 + 2x_2 \le 2 \cdot 4 + 0 \cdot 9 + 1 \cdot 3 = 11$. This instance is the running example of the pages on [duality](/dual-linear-program/), [shadow prices](/shadow-price/) and [sensitivity analysis](/lp-sensitivity-analysis/).

**Many optimal points.** With the objective $x_1 + x_2$ on the same pentagon, the vertices $(3, 1)$ and $(3/2, 5/2)$ both give 4, and so does each point of the edge between them. The optimum is unique in value, not in position.

**Infeasible.** The constraints $x_1 + x_2 \le 1$, $x_1 \ge 2$, $x_1, x_2 \ge 0$ have no solution: the first and the third give $x_1 \le 1$. The multipliers $1$ and $1$ on the rows $x_1 + x_2 \le 1$ and $-x_1 \le -2$, and $1$ on $-x_2 \le 0$, add up to $0 \le -1$.

**Unbounded.** Maximize $x_1 + x_2$ subject to $x_1 - x_2 \le 1$, $x_1, x_2 \ge 0$. The points $(1 + t, t)$ are feasible for each $t \ge 0$ and have objective $1 + 2t$. The ray direction is $d = (1, 1)$.

**A non-example.** Minimize $x_1$ subject to $x_1 x_2 \ge 1$, $x \ge 0$. The infimum is 0, but no feasible point reaches it. The constraint is not linear, and this gap cannot happen for a linear program.

## Known algorithms

| method | cost | notes |
|---|---|---|
| [Simplex method](/simplex-method/) (Dantzig, 1947) | $O(mn)$ arithmetic operations per [pivot](/pivot-operation/); the number of pivots is $2^n - 1$ on the [Klee-Minty cube](/klee-minty-cube/) with [Dantzig's rule](/dantzig-pivot-rule/) | fast in practice; polynomial in the [smoothed](/smoothed-simplex-analysis/) sense; exact certificates |
| [Ellipsoid method](/ellipsoid-method/) (Khachiyan, 1979) | $O(n^2 L)$ iterations, each with $O(n^2 + mn)$ arithmetic operations | the first polynomial algorithm; works with a [separation oracle](/separation-oracle/) |
| [Karmarkar's algorithm](/karmarkar-algorithm/) (1984) | $O(nL)$ iterations, $O(n^{3.5} L)$ arithmetic operations | the first practical polynomial method |
| [Interior point methods](/interior-point-method/) | $O(\sqrt{n}\, L)$ iterations, each a linear system solve | path following along the [central path](/central-path/) |
| [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) | up to $4(m/4)^{2^n}$ inequalities | exact, decides feasibility; only for tiny $n$ |
| [Vertex enumeration](/vertex-enumeration/) over all bases | $\binom{n}{m}$ bases of the equality form, $O(m^3)$ each | exact brute force; the reference for tests |
| [Megiddo](/megiddo-fixed-dimension-lp/), [Seidel](/seidel-linear-programming/) | $O(m)$ for fixed $n$ (the constant grows faster than exponentially in $n$) | geometry of low dimension |

The [network simplex method](/network-simplex/) and the combinatorial flow algorithms solve the network special cases faster than a general LP solver.

## Bounds

**Upper bound.** Linear programming with rational data is in [P](/p/). This was first shown by Khachiyan with the ellipsoid method. The proof needs a bound on the size of a vertex: by [Cramer's rule](/cramers-rule/), each coordinate of a vertex is a ratio of two subdeterminants of the data, and by the [Hadamard bound](/hadamard-bound/) each such determinant has $O(L)$ binary digits. So it is enough to find a point that is optimal up to $2^{-O(L)}$ and round it. The page [LP in P](/lp-in-p/) has the details.

**Not strongly polynomial.** All known polynomial algorithms take a number of arithmetic operations that grows with $L$, not only with $n$ and $m$. Whether a *strongly polynomial* algorithm exists, with a number of operations bounded by a polynomial in $n$ and $m$ alone, is open; Smale listed it as the ninth of his problems for the 21st century. Tardos gave an algorithm whose number of arithmetic operations is polynomial in the size of $A$ alone, not of $b$ and $c$. So the LPs of network flow problems, whose matrices have entries 0 and $\pm 1$, are solved in strongly polynomial time. For the simplex method with any known pivot rule, an exponential lower bound on some family of instances is known, and the [polynomial Hirsch conjecture](/hirsch-conjecture/) on the diameter of polyhedra is open.

**Lower bounds.** No lower bound beyond reading the input is known for general LP in the arithmetic model. Linear programming is P-complete under logarithmic space reductions (Dobkin, Lipton and Reiss, 1979), so it is unlikely to have a fast parallel algorithm.

## Reductions

- **Optimization to feasibility.** Put the primal constraints, the dual constraints and the inequality $c^\top x \le b^\top y$ in one system. By [strong duality](/strong-duality/), this system is feasible exactly when the LP has an optimum, and each solution gives an optimal pair. The system has $O(m + n)$ rows and data of size $O(L)$.
- **Feasibility to optimization.** Add one artificial variable per row and minimize their sum, as in [phase one](/two-phase-simplex-method/) of the simplex method. The LP is feasible exactly when the optimum is 0.
- **General form to standard form.** Replace a free variable by the difference of two nonnegative ones, add a [slack variable](/slack-variables/) to each inequality, and negate a maximization. The size grows by a constant factor.
- **From other problems.** [Maximum flow](/max-flow-lp-formulation/), [minimum cost flow](/min-cost-flow-lp-formulation/), [shortest paths](/shortest-paths-lp-formulation/), [difference constraints](/difference-constraints/), the [assignment problem](/assignment-problem/) and the value of a [zero-sum game](/zero-sum-game/) are all linear programs. The page [reduction to linear programming](/reduction-to-linear-programming/) collects the patterns.

## Applications

- **Planning and economics.** Production planning, blending, transport and the allocation of resources were the first uses, and the [shadow prices](/shadow-price/) of the constraints are the marginal values of the resources.
- **Combinatorial optimization.** Polyhedral methods write a combinatorial problem as an LP over the convex hull of its solutions; [total unimodularity](/total-unimodularity/) explains when this LP has integral vertices.
- **Approximation algorithms.** [LP rounding](/linear-programming-rounding/) and the [primal-dual schema](/primal-dual-schema/) build approximate solutions to hard problems from an LP relaxation and its dual.
- **Integer programming solvers.** [Branch and bound](/land-doig-algorithm/) and [branch and cut](/branch-and-cut/) solve one LP relaxation at each node of its search tree.
- **Game theory.** The optimal mixed strategies of a two-player [zero-sum game](/zero-sum-game/) are the optimal solutions of a primal and dual pair, which is one proof of the [minimax theorem](/minimax-theorem/).

## References
