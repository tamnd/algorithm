---
tag: 6TK6XY
kind: algorithm
slug: explicit-mpc
name: Explicit MPC
aliases:
- explicit model predictive control
area: control/optimal-and-predictive-control
level: advanced
summary: Solves the linear MPC quadratic program offline for all states as a multiparametric QP, so the online controller only finds the polyhedral region of x and applies its affine law.
solves: [multiparametric-quadratic-programming]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, N: the horizon, c: the number of constraint rows of the QP, M: the number of regions, L: the cost of one linear program in n + 1 variables}
  time: {worst: "O(2^c (N^3 m^3 + c N m n + L))", online: "O(M (c + n) n)"}
  space: {extra: "O(M (c + n) (n + N m))"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 2002
  people: [Alberto Bemporad, Manfred Morari, Vivek Dua, Efstratios N. Pistikopoulos]
  note: "Bemporad, Morari, Dua and Pistikopoulos (2002) showed that the linear MPC law is continuous and piecewise affine and computed it offline by multiparametric quadratic programming."
prereqs: [linear-mpc, multiparametric-quadratic-programming, kkt-conditions, polyhedron]
see_also: [model-predictive-control, parametric-linear-programming, planar-point-location, maximal-positively-invariant-set, hybrid-mpc, quadratic-programming, interior-point-method, mpc-stability-theorem]
sources:
  - paper: doi:10.1016/S0005-1098(01)00174-1
    title: Alberto Bemporad, Manfred Morari, Vivek Dua and Efstratios N. Pistikopoulos, The explicit linear quadratic regulator for constrained systems, Automatica 38(1), 3-20, 2002
    locator: the critical regions, the continuous piecewise affine law, the convex piecewise quadratic value function, and the geometric algorithm that explores the parameter space
  - paper: "Petter Tøndel, Tor Arne Johansen and Alberto Bemporad, An algorithm for multi-parametric quadratic programming and explicit MPC solutions, Automatica 39(3), 489-497, 2003"
    locator: the exploration of neighboring regions across facets by changing one active constraint at a time
  - paper: doi:10.1016/S0005-1098(02)00308-4
    title: Petter Tøndel, Tor Arne Johansen and Alberto Bemporad, Evaluation of piecewise affine control via binary search tree, Automatica 39(5), 945-950, 2003
    locator: the binary search tree over the regions, with an online time logarithmic in the number of regions for a balanced tree
  - paper: doi:10.1016/j.automatica.2011.06.019
    title: Arun Gupta, Sharad Bhartiya and P. S. V. Nataraj, A novel approach to multiparametric quadratic programming, Automatica 47(9), 2112-2117, 2011
    locator: the enumeration of candidate active sets with pruning, instead of the exploration of the parameter space
  - book: isbn:9781107016880
    title: Francesco Borrelli, Alberto Bemporad and Manfred Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017
    locator: the chapters on multiparametric programming and on the explicit solution of constrained linear quadratic control
---

Explicit MPC computes the [linear MPC](/linear-mpc/) law for every state in advance. The MPC quadratic program depends on the state $x$ only through its linear term and its right-hand side, so it is a [multiparametric quadratic program](/multiparametric-quadratic-programming/) (mp-QP) with the parameter $x$. Bemporad, Morari, Dua and Pistikopoulos (2002) showed that its solution is a continuous piecewise affine function of $x$: the feasible states split into finitely many polyhedral critical regions, one per optimal active set, and on each region the optimal plan is $z^*(x) = K_i x + k_i$. Explicit MPC computes the regions and the gains offline. Online, the controller finds the region that contains the measured state and applies one affine law, with no QP solver. The price is the number of regions: it is exponential in the number of constraints in the worst case, and the counts of real problems are measurements.

## In plain words

Online MPC solves an optimization problem at every tick. For a linear model, a quadratic cost and linear limits, that problem changes in a simple way with the state. For each choice of which limits are tight, the best plan is a fixed linear formula of the state. The states where that choice is the right one form a region with flat sides. So you can solve the problem for all states before the system runs. You store a list of regions, each with its own formula. At run time the controller only checks which region holds the state and evaluates that formula. This needs little computing power and gives a fixed run time, which helps on small hardware and for fast systems.

## The problem

Input: the mp-QP of a linear MPC problem,

$$\min_z \ \tfrac12 z^T H z + x^T F^T z \quad \text{subject to} \quad G z \le w + E x,$$

with $H > 0$ of size $s = N m$ (the stacked inputs), $c$ constraint rows, and a box $\mathbb{X} = \{x : |x_i| \le \bar x_i\}$ of states of interest. Output: a list of regions $CR_1, \dots, CR_M$, each a polyhedron with an affine law $z = K_i x + k_i$, such that the regions cover $S = \{x \in \mathbb{X} : \text{the QP is feasible}\}$ and $z^*(x) = K_i x + k_i$ for $x \in CR_i$. The online problem is: given $x$, return $z^*(x)$, or report that $x \notin S$.

**The law of one active set.** For a set $A$ of rows with linearly independent $G_A$ (the linear independence constraint qualification, LICQ), the [KKT conditions](/kkt-conditions/) with exactly the rows $A$ active are linear in $(z, \lambda_A)$ and give

$$\lambda_A(x) = -M_A^{-1}\left(w_A + (E_A + G_A H^{-1} F) x\right), \qquad z_A(x) = -H^{-1}\left(F x + G_A^T \lambda_A(x)\right), \qquad M_A = G_A H^{-1} G_A^T.$$

The critical region of $A$ is the set of $x$ where $z_A(x)$ is feasible and $\lambda_A(x) \ge 0$. Both conditions are affine inequalities in $x$, so it is a polyhedron.

## The algorithm

```pseudo id=main
EXPLICIT-MPC(H, F, G, w, E, box)                  ▷ offline
L1   regions ← ∅
L2   for each set A of at most s rows of G         ▷ candidate active sets
L3       M ← G_A H⁻¹ G_Aᵀ;  skip A if M is singular   ▷ LICQ
L4       λ_A(x) = L x + l:  L ← -M⁻¹ (E_A + G_A H⁻¹ F),  l ← -M⁻¹ w_A
L5       z_A(x) = K x + k:  K ← -H⁻¹ (F + G_Aᵀ L),  k ← -H⁻¹ G_Aᵀ l
L6       CR ← {x in box : G (K x + k) ≤ w + E x,  L x + l ≥ 0}
L7       if the Chebyshev radius of CR is > ε then add (A, CR, K, k) to regions
L8   return regions
EVALUATE(regions, x)                               ▷ online, at each sampling instant
L9   for each (A, CR, K, k) in regions
L10      if x ∈ CR then return K x + k
L11  return "x is not in the covered set"
```

Line L2 enumerates every set of at most $s$ rows. Larger sets cannot have linearly independent rows in $\mathbb{R}^s$, and line L3 drops the dependent ones. Lines L4 and L5 are the formulas above. Line L6 writes the region as inequalities in $x$: primal feasibility of $z_A(x)$ for all $c$ rows, and dual feasibility of the multipliers. Line L7 solves one linear program for the Chebyshev radius, the radius of the largest ball inside $CR$; a positive radius means the region has an interior point, and regions without one are dropped. The online part is a sequential search. Only the first $m$ entries of $z$ are needed online, so a controller stores only the first $m$ rows of $K$ and $k$.

This enumeration is the simplest correct method, close in spirit to the combinatorial method of Gupta, Bhartiya and Nataraj (2011), which prunes the candidate sets. Bemporad et al. (2002) explore the parameter space instead, and Tøndel, Johansen and Bemporad (2003) step from a region to its neighbors across facets. All of them return the same partition up to regions without interior points.

## Example

Take the double integrator of the [linear MPC](/linear-mpc/) page, $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, $B = \begin{bmatrix} 0.5 \\ 1 \end{bmatrix}$, $Q = I$, $R = 1$, the DARE solution as terminal weight $P$, the horizon $N = 3$ and only the input limits $|u_k| \le 1$. The mp-QP has $s = 3$ variables and $c = 6$ rows, in the order $u_0 \le 1$, $u_0 \ge -1$, $u_1 \le 1$, $u_1 \ge -1$, $u_2 \le 1$, $u_2 \ge -1$. The box is $|x_i| \le 10$.

- **Candidates.** There are $\binom60 + \binom61 + \binom62 + \binom63 = 42$ sets of at most 3 rows. A set that contains both limits of the same input has a singular $M$ and is skipped, which leaves $3^3 = 27$ sets.
- **Regions.** 19 of the 27 regions have an interior point inside the box (measurement with the implementation).
- **The unconstrained region** ($A = \emptyset$) contains the origin and has the law $u_0 = -0.4345 x_1 - 1.0285 x_2$, the LQR law $u = -K x$.
- **One input limit active.** For $A = \{u_1 \ge -1\}$ the law is $u_0 = -0.3824 x_1 - 1.1172 x_2 + 0.4882$. For $A = \{u_1 \ge -1, u_2 \ge -1\}$ it is $u_0 = -0.3174 x_1 - 1.1236 x_2 + 0.9338$. The regions with $u_1 \le 1$ active have the same gains with the opposite offsets.
- **Saturated regions.** In 14 regions $u_0 = 1$ or $u_0 = -1$. So the first input has only 7 different affine pieces on the 19 regions.

**Online evaluation.** For $x = (-5, 3)$ the search finds the region of $\{u_1 \ge -1\}$, and the law gives $z = (-0.9516, -1, -0.6753)$. As in the [linear MPC](/linear-mpc/) example with $N = 5$ from the same state, only the row $u_1 \ge -1$ is active. For $x = (3, 2)$ the region is $\{u_0, u_1, u_2 \ge -1\}$ and $z = (-1, -1, -1)$. The tests compare the law with a brute-force QP solution at 300 random states and find agreement to $10^{-7}$.

**Region counts.** For the same plant with $|u| \le 1$ inside $|x_i| \le 10$ (measurement with the implementation):

| $N$ | rows $c$ | regions $M$ |
|---|---|---|
| 2 | 4 | 9 |
| 3 | 6 | 19 |
| 4 | 8 | 33 |
| 5 | 10 | 43 |

With the state limits $|x_{k,i}| \le 5$ added and $N = 2$, the covered set shrinks: the state $(4, 2)$, for which no input meets the limits, lies in no region.

## Correctness

The proofs are in proofs/correctness.md.

1. **One active set gives an affine law.** If $G_A$ has independent rows, $M_A$ is positive definite, so the linear KKT system with the rows $A$ active has the unique solution of the formulas above, affine in $x$.
2. **Inside its region the law is optimal.** For $x \in CR_A$, $z_A(x)$ is feasible, $\lambda_A(x) \ge 0$, complementarity holds because the rows in $A$ are active, and stationarity holds by construction. For a convex QP the KKT conditions are sufficient, and $H > 0$ makes the minimizer unique.
3. **Every feasible state is in some region.** At the optimum $z^*(x)$, the vector $-(H z^* + F x)$ is a nonnegative combination of the active rows. By [Carathéodory's theorem](/caratheodory-theorem/) for cones, a linearly independent subset of the active rows is enough. That subset is a set $A$ of line L2 with $x \in CR_A$.
4. **The kept regions cover $S$.** Regions without interior points lie in proper affine subspaces, which have measure zero. If $S$ has an interior point, a finite union of such sets cannot contain the open set that a missed point would need, so the full-dimensional regions alone cover $S$.
5. **The online search is correct.** By point 4, a state in $S$ lies in a kept region, and by point 2 its law gives $z^*(x)$. Every region lies in $S$, so a state outside $S$ is in none.

The law is continuous on $S$, because the affine pieces agree on shared boundaries (both equal the unique minimizer). The value function is convex, because the MPC cost is jointly convex in $(z, x)$, and it is quadratic on each region.

## Complexity

Costs are in the [real-RAM model](/real-ram/), with $s = N m$ variables and $c$ rows.

- **Offline.** Line L2 visits $\sum_{k \le s} \binom{c}{k} \le 2^c$ sets. Each costs $O(s^3)$ for the solves of lines L3 to L5, $O(c s n)$ to write the region, and one LP for the Chebyshev radius. The total is $O(2^c (N^3 m^3 + c N m n + L))$. This is a theorem about this enumeration; exploration methods visit fewer sets in practice, but they share the bound below on the output.
- **Number of regions.** Each region belongs to a different active set with independent rows, so $M \le \sum_{k \le s} \binom{c}{k}$. The bound is exponential in the number of constraints, and the count can grow quickly with $N$. The counts in the table are measurements.
- **Online.** The sequential search tests at most $M$ regions with $O(c + n)$ inequalities each, so $O(M (c + n) n)$ in the worst case. A binary search tree over the hyperplanes of the partition (Tøndel, Johansen and Bemporad 2003) gives a time logarithmic in $M$ for a balanced tree; building the tree is an offline cost. In two dimensions this is [planar point location](/planar-point-location/).
- **Space.** $O(M (c + n) (n + N m))$ for the inequalities and the gains; $O(M (c + n) n + M m n)$ if only the first input is stored.

## Properties

- **Exact.** In exact arithmetic the stored law equals the QP solution on all of $S$. It is not an approximation.
- **Continuous piecewise affine law** and **convex piecewise quadratic value function** (theorem, Bemporad et al. 2002), when $H > 0$.
- **Same closed loop as online MPC.** The explicit law is the same function as the online law, so the stability and feasibility properties of [linear MPC](/linear-mpc/) carry over unchanged.
- **Fixed online time.** The worst case of the online search is known in advance, which matters for certification.
- **Offline only for a fixed problem.** Any change of the model, the weights or the limits needs a new offline computation.

## Variants and improvements

- **Geometric exploration** (Bemporad et al. 2002): start from a region, and explore the rest of the parameter space region by region.
- **Facet stepping** (Tøndel, Johansen and Bemporad 2003): cross each facet of a region and guess the neighbor's active set by adding or removing the constraint of that facet.
- **Combinatorial enumeration with pruning** (Gupta, Bhartiya and Nataraj 2011): if a set of rows is infeasible as an active set, all its supersets are too, which cuts the search.
- **Merging regions.** Regions with the same first-input law can be merged into fewer, possibly nonconvex, pieces; the example has 19 regions but 7 different laws for $u_0$.
- **Approximate explicit MPC.** Accept a law that is suboptimal by a bounded amount in exchange for far fewer regions.
- **Explicit hybrid MPC.** For piecewise affine models the regions may overlap and the law can be discontinuous. See [hybrid MPC](/hybrid-mpc/).
- **Explicit LP-based MPC.** With a 1-norm or infinity-norm cost the problem is a [parametric linear program](/parametric-linear-programming/), and the law is again piecewise affine.

## When to use it

Use it for small problems: a few states, one to three inputs, a short horizon, and few constraints, on hardware that cannot run a QP solver in the sampling period, or where a verified fixed run time is required. For larger problems the number of regions makes the offline time and the memory too large; use an online QP solver as in [linear MPC](/linear-mpc/). Rule of thumb: the region count, not the number of states alone, decides. Compute it for the real problem before you commit.

## Pitfalls

- **Region explosion.** The count can grow fast with $N$, $m$ and the number of constraints. Measure it for the real problem before you choose explicit MPC.
- **Lost thin regions.** In floating point, a region with a Chebyshev radius below the threshold $\varepsilon$ is dropped. States in it are then not covered. Check the coverage of $S$ by sampling, as the tests do.
- **The box of states.** The partition covers only the chosen box. A state outside it is reported as not covered, even if the QP is feasible there.
- **Degenerate problems.** When more than $s$ rows are active at the solution, or LICQ fails, several active sets describe the same region, and exploration methods that rely on one active set per region can miss regions. The enumeration of this page handles it, at the cost of more candidates.
- **Ties on boundaries.** A state on a shared boundary is in several regions. All give the same value, but the floating-point tests can disagree; use a small tolerance in the membership test.
- **Equality constraints written as two inequalities.** Then $S$ has no interior point and every region is dropped by the radius test. Eliminate the equalities first.

## Implementations

## History

Bemporad, Morari, Dua and Pistikopoulos (2002) showed that the constrained linear quadratic regulator over a finite horizon is a continuous piecewise affine function of the state and gave an algorithm that computes it. Tøndel, Johansen and Bemporad (2003) gave a faster exploration across facets, and in a second paper a binary search tree for fast online evaluation. Gupta, Bhartiya and Nataraj (2011) replaced the exploration of the state space by an enumeration of active sets with pruning. The book of Borrelli, Bemporad and Morari presents the theory for linear and hybrid systems.

## References
