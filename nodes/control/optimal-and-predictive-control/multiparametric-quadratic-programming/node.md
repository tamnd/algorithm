---
tag: 00MC8N
kind: problem
slug: multiparametric-quadratic-programming
name: Multiparametric quadratic programming
aliases:
- mp-QP
- parametric quadratic programming
area: control/optimal-and-predictive-control
level: advanced
summary: Find the solution of a strictly convex quadratic program as a function of a parameter in its linear cost term and constraint bounds; it is piecewise affine on polyhedral critical regions.
model: real-ram
prereqs: [quadratic-programming, kkt-conditions, polyhedron, parametric-linear-programming]
see_also: [explicit-mpc, linear-mpc, lp-sensitivity-analysis, fourier-motzkin-elimination, planar-point-location, convex-function, lagrangian-duality, caratheodory-theorem]
sources:
  - paper: doi:10.1016/S0005-1098(01)00174-1
    title: Alberto Bemporad, Manfred Morari, Vivek Dua and Efstratios N. Pistikopoulos, The explicit linear quadratic regulator for constrained systems, Automatica 38(1), 3-20, 2002
    locator: the mp-QP formulation, the polyhedral critical regions, the continuous piecewise affine optimizer, the convex piecewise quadratic value function, and the geometric algorithm
  - paper: "Petter Tøndel, Tor Arne Johansen and Alberto Bemporad, An algorithm for multi-parametric quadratic programming and explicit MPC solutions, Automatica 39(3), 489-497, 2003"
    locator: the exploration of the parameter space across the facets of the critical regions
  - paper: doi:10.1016/S0005-1098(02)00308-4
    title: Petter Tøndel, Tor Arne Johansen and Alberto Bemporad, Evaluation of piecewise affine control via binary search tree, Automatica 39(5), 945-950, 2003
    locator: the binary search tree for the online point location in the partition
  - paper: doi:10.1016/j.automatica.2011.06.019
    title: Arun Gupta, Sharad Bhartiya and P. S. V. Nataraj, A novel approach to multiparametric quadratic programming, Automatica 47(9), 2112-2117, 2011
    locator: the combinatorial enumeration of optimal active sets with pruning
  - book: isbn:9781107016880
    title: Francesco Borrelli, Alberto Bemporad and Manfred Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017
    locator: the chapter on multiparametric programming, with the properties of mp-LP and mp-QP solutions and the algorithms
---

Multiparametric quadratic programming (mp-QP) asks for the solution of a [quadratic program](/quadratic-programming/) not at one data point but for every value of a parameter vector $\theta$ that enters its linear cost term and the right-hand side of its constraints. For a strictly convex QP the answer has a clean structure (Bemporad, Morari, Dua and Pistikopoulos 2002): the parameters for which the QP is feasible form a polyhedron, it splits into polyhedral critical regions, one for each optimal active set, and on each region the optimizer is an affine function of $\theta$. The optimizer is continuous and piecewise affine, and the optimal value is convex and piecewise quadratic. The main application is [explicit MPC](/explicit-mpc/), where $\theta$ is the state and the solution is the MPC law for all states. The number of critical regions can be exponential in the number of constraints.

## In plain words

A quadratic program finds the best point of a bowl-shaped cost inside a region with flat walls. Now let some of the numbers of the problem depend on a knob. Turning the knob moves the bowl and the walls a little, and the best point moves with it. For a fixed choice of which walls the best point touches, the best point moves along a straight line or plane as the knob turns. When the best point reaches a new wall or leaves one, a new piece starts. So the knob settings fall into pieces with flat sides, and on each piece there is a simple formula for the answer. The task is to find all the pieces and their formulas before anyone asks.

## Definition

**Input.** A positive definite $H \in \mathbb{R}^{s \times s}$, matrices $F \in \mathbb{R}^{s \times n}$, $G \in \mathbb{R}^{c \times s}$, $E \in \mathbb{R}^{c \times n}$, a vector $w \in \mathbb{R}^c$, and a polyhedron $\Theta \subseteq \mathbb{R}^n$ of parameters of interest. For each $\theta$, the QP is

$$V^*(\theta) = \min_{z} \ \tfrac12 z^T H z + \theta^T F^T z \quad \text{subject to} \quad G z \le w + E \theta.$$

**Output.** The feasible parameter set $\Theta^* = \{\theta \in \Theta : \text{the QP is feasible}\}$; a finite list of polyhedra $CR_1, \dots, CR_M$ that cover $\Theta^*$ and have disjoint interiors; and for each $CR_i$ an affine law $z^*(\theta) = K_i \theta + k_i$ (and, if wanted, $V^*$ as a quadratic function on $CR_i$).

**The critical region of an active set** $A \subseteq \{1, \dots, c\}$ with linearly independent rows $G_A$ is the set of $\theta$ for which the solution of the [KKT conditions](/kkt-conditions/) with exactly the rows $A$ held as equalities is feasible and has nonnegative multipliers. Both conditions are affine in $\theta$, so $CR_A$ is a polyhedron, and on it

$$\lambda_A(\theta) = -(G_A H^{-1} G_A^T)^{-1}\left(w_A + (E_A + G_A H^{-1} F)\theta\right), \qquad z^*(\theta) = -H^{-1}\left(F\theta + G_A^T \lambda_A(\theta)\right).$$

**Structure (theorem, Bemporad et al. 2002).** With $H > 0$: $\Theta^*$ is a polyhedron; $z^*$ is unique, continuous and piecewise affine on $\Theta^*$; $V^*$ is continuous, convex and piecewise quadratic; the critical regions are polyhedra.

## Variants

- **Parameter in the cost only, or in the bounds only.** Both are special cases. With $E = 0$ the feasible set does not depend on $\theta$. With $F = 0$ only the walls move.
- **Single parameter.** For $n = 1$ the regions are intervals, and the solution is a piecewise affine path in $z$. This is the classical setting of parametric quadratic programming, solved by homotopy methods that follow the path and change one active constraint at each breakpoint.
- **Positive semidefinite $H$.** The optimizer may be nonunique. The value function is still convex and piecewise quadratic, but a continuous piecewise affine selection of the optimizer needs extra care.
- **Multiparametric linear programming.** With $H = 0$, the problem is an mp-LP: the value is convex and piecewise affine, and the optimizer can be chosen piecewise affine; see [parametric linear programming](/parametric-linear-programming/).
- **Parameter in $H$ or in $G$.** Then the solution is no longer piecewise affine in general, and the regions are not polyhedra.
- **Mixed-integer versions.** mp-MILP and mp-MIQP arise from [hybrid MPC](/hybrid-mpc/); the regions can overlap and the value function need not be convex.

## Examples

**One variable, one constraint.** $\min_z \tfrac12 z^2 - \theta z$ subject to $z \le 1$, for $\theta \in \mathbb{R}$. Here $H = 1$, $F = -1$, $G = 1$, $w = 1$, $E = 0$. There are two critical regions:

| region | active set | $z^*(\theta)$ | multiplier | $V^*(\theta)$ |
|---|---|---|---|---|
| $\theta \le 1$ | $\emptyset$ | $\theta$ | none | $-\theta^2/2$ |
| $\theta \ge 1$ | $\{1\}$ | $1$ | $\theta - 1 \ge 0$ | $\tfrac12 - \theta$ |

$z^* = \min(\theta, 1)$ is continuous and piecewise affine, and $V^*$ is convex, quadratic on one region and affine on the other. The two pieces agree at $\theta = 1$.

**A box: exponentially many regions.** $\min_z \tfrac12 \|z\|^2 - \theta^T z$ subject to $-1 \le z_i \le 1$ for $i = 1, \dots, s$, with $\theta \in \mathbb{R}^s$. The QP separates by coordinates, and $z_i^* = \max(-1, \min(\theta_i, 1))$. For each coordinate there are three cases (lower bound active, no bound active, upper bound active), so there are exactly $3^s$ critical regions, each a box product of the intervals $(-\infty, -1]$, $[-1, 1]$, $[1, \infty)$. With $c = 2s$ rows this is $3^{c/2} = (\sqrt 3)^c$ regions.

**Explicit MPC of a double integrator.** The [explicit MPC](/explicit-mpc/) page solves the mp-QP of a [linear MPC](/linear-mpc/) problem with $s = 3$ variables, $c = 6$ rows and $\theta = x \in \mathbb{R}^2$: 27 candidate active sets have independent rows, and 19 of them give regions with an interior point (measurement). The first input has only 7 different affine pieces on these 19 regions.

## Known algorithms

- **Geometric exploration** (Bemporad et al. 2002). Solve the QP at one parameter, build its critical region, split the rest of the parameter set into polyhedra, and repeat in each piece.
- **Facet stepping** (Tøndel, Johansen and Bemporad 2003). From each facet of a known region, step a little across, and get the neighbor's active set by adding or removing the constraint of that facet. This avoids the artificial splits of the geometric method.
- **Active set enumeration** (Gupta, Bhartiya and Nataraj 2011). Enumerate candidate active sets in a tree by size, test each with a linear program, and prune all supersets of an infeasible set. The [explicit MPC](/explicit-mpc/) page implements a simple enumeration without pruning.
- **Online point location.** Once the partition is known, the online task is to find the region that contains $\theta$. A sequential search costs $O(M c n)$; a binary search tree on the hyperplanes of the partition (Tøndel, Johansen and Bemporad 2003) gives a depth logarithmic in $M$ when it is balanced. In two dimensions this is [planar point location](/planar-point-location/).

## Bounds

All in the [real-RAM model](/real-ram/), with $s$ variables, $c$ constraint rows and $n$ parameters.

- **Upper bound on the regions (theorem).** Different full-dimensional regions belong to different active sets with independent rows, and an independent set has at most $s$ rows. So $M \le \sum_{k=0}^{\min(s, c)} \binom{c}{k} \le 2^c$.
- **Lower bound (theorem).** The box example has $3^{c/2}$ regions, so no algorithm that lists the regions explicitly can run in time polynomial in $c$ for all inputs.
- **Size of one region.** A critical region is given by $c - |A|$ primal inequalities and $|A|$ dual inequalities, so $c$ inequalities in $\mathbb{R}^n$, many of them often redundant. Removing the redundant ones costs one linear program per row.
- **Per candidate set.** Building the law and the region of one active set costs $O(s^3 + c s n)$, plus a linear program to test for an interior point.
- **Measured counts** in MPC grow quickly with the horizon and the number of constraints; the counts on the [explicit MPC](/explicit-mpc/) page are 9, 19, 33 and 43 regions for horizons 2 to 5 (measurement).

## Reductions

- **Parameter in the cost to parameter in the bounds.** The substitution $z = y - H^{-1} F \theta$ turns the cost into $\tfrac12 y^T H y$ plus a term in $\theta$ alone, and the constraints into $G y \le w + (E + G H^{-1} F)\theta$. So every mp-QP with $H > 0$ is equivalent to one with the parameter only in the right-hand side.
- **Constrained linear MPC to mp-QP.** Eliminating the states from a linear MPC problem with a quadratic cost gives an mp-QP with $\theta = x$, $s = N m$ variables and one row per constraint; see [linear MPC](/linear-mpc/).
- **Fixed parameter to QP.** For each fixed $\theta$ the problem is an ordinary QP, so any QP method gives one point of the solution, and the KKT multipliers identify its active set.
- **Feasible set to projection.** $\Theta^*$ is the projection of the polyhedron $\{(z, \theta) : G z - E \theta \le w\}$ onto $\theta$, computable by [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) or by the union of the critical regions.
- **Dual problem.** By [Lagrangian duality](/lagrangian-duality/), the dual of the QP is a QP in the multipliers with $\theta$ in its linear term, and its piecewise affine multipliers $\lambda(\theta)$ are the dual counterpart of $z^*(\theta)$.

## Applications

- **Explicit MPC.** The MPC law for every state, evaluated online by point location; see [explicit MPC](/explicit-mpc/).
- **Constrained LQR by backward recursion.** In the backward recursion of a constrained linear quadratic problem, the cost to go is piecewise quadratic, and each step can be solved as one mp-QP per piece of the cost to go. This is another way to get the finite-horizon constrained LQR law as a piecewise affine function.
- **Sensitivity analysis.** How the solution of a QP changes when its data change; for linear programs see [LP sensitivity analysis](/lp-sensitivity-analysis/).
- **Design under uncertainty and bilevel problems.** When an inner QP depends on the decisions of an outer problem, its parametric solution replaces the inner problem by a finite list of affine laws.

## References
