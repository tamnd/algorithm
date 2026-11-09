---
tag: 09SW6A
kind: algorithm
slug: benders-decomposition
name: Benders decomposition
aliases:
- Benders cuts
- Benders' method
- L-shaped method
area: optimization/integer-programming
level: advanced
summary: Solve a mixed integer program by a master problem over the integer variables and a linear subproblem over the continuous ones, whose dual solutions become cuts for the master.
solves: [mixed-integer-programming]
model: real-ram
complexity:
  vars: {K: the number of iterations, M: the time of one master solve, T: the time of one linear program solve, m: the number of rows that link the two groups of variables}
  time: {worst: O(K (M + T))}
  space: {extra: O(K m)}
properties: {deterministic: true, recursive: false}
prereqs: [mixed-integer-programming, lp-duality, farkas-lemma, lp-relaxation]
see_also: [dantzig-wolfe-decomposition, column-generation, branch-and-cut, branch-and-price, lagrangian-relaxation, cutting-plane-method, dual-simplex-method, capacitated-facility-location]
sources:
  - paper: doi:10.1007/BF01386316
    title: J. F. Benders, Partitioning procedures for solving mixed-variables programming problems, Numerische Mathematik 4, 1962
    locator: pp. 238 to 252
  - paper: doi:10.1137/0117061
    title: R. M. Van Slyke and R. Wets, L-shaped linear programs with applications to optimal control and stochastic programming, SIAM Journal on Applied Mathematics 17(4), 1969
    locator: pp. 638 to 663
  - paper: doi:10.1007/BF00934810
    title: A. M. Geoffrion, Generalized Benders decomposition, Journal of Optimization Theory and Applications 10(4), 1972
    locator: pp. 237 to 260
  - paper: doi:10.1287/opre.29.3.464
    title: T. L. Magnanti and R. T. Wong, Accelerating Benders decomposition, algorithmic enhancement and model selection criteria, Operations Research 29(3), 1981
    locator: pp. 464 to 484 (Pareto-optimal cuts)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 8, Reformulations and Relaxations (Benders decomposition)
  - paper: "G. Codato and M. Fischetti, Combinatorial Benders' cuts for mixed-integer linear programming, Operations Research 54(4), 2006"
    locator: pp. 756 to 766
  - paper: "J. N. Hooker and G. Ottosson, Logic-based Benders decomposition, Mathematical Programming 96(1), 2003"
    locator: pp. 33 to 60
  - paper: doi:10.1016/j.ejor.2016.12.005
    title: R. Rahmaniani, T. G. Crainic, M. Gendreau and W. Rei, The Benders decomposition algorithm, a literature review, European Journal of Operational Research 259(3), 2017
    locator: pp. 801 to 817
---

Benders decomposition solves a [mixed integer program](/mixed-integer-programming/) by splitting its variables into two groups. A *master problem* chooses the integer variables. For that choice, a *subproblem* is a linear program in the continuous variables, and [LP duality](/lp-duality/) turns its solution into one linear inequality, a *Benders cut*, that the master problem must respect from then on. The method stops after finitely many cuts, because each cut comes from a vertex or an extreme ray of one fixed dual polyhedron. Benders published it in 1962. In stochastic programming it is the L-shaped method, and it is the standard tool for problems where a few integer decisions control a large linear model.

## In plain words

Some problems have a few hard whole-number decisions, such as which plants to build, and many easy decisions that follow from them, such as how much to ship on each road. When the hard decisions are fixed, the easy part is a linear program, which is fast to solve.

Benders decomposition asks a "manager" to guess the hard decisions. A "worker" then solves the easy part for that guess. The worker also returns a rule that is true for every guess: "with your choice of plants, the shipping cost is at least this much", or "a choice of plants like this one can never meet the demand". The manager adds the rule and guesses again. The manager's best guess gives a lower limit on the true cost, and each worker answer gives a real plan and an upper limit. When the two limits meet, the plan is optimal.

## The problem

This page uses a form with the integer variables apart. Let $x \in \mathbb{Z}^p$ be the integer variables and $y \in \mathbb{R}^q$ the continuous ones. The problem is

$$\min\ c^\top x + d^\top y \quad \text{subject to} \quad G x + B y \ge h,\quad y \ge 0,\quad x \in X,$$

where $G$ is $m \times p$, $B$ is $m \times q$, $h \in \mathbb{Q}^m$, all data are rational, and $X \subseteq \mathbb{Z}^p$ is a finite set (for example the integer points of a box). The $m$ rows link the two groups of variables. The output is an optimal pair $(x^*, y^*)$ with its value, or the answer "infeasible", or "unbounded".

For a fixed $\hat{x} \in X$, write $r = h - G\hat{x}$. The *subproblem* and its [dual](/dual-linear-program/) are

$$\mathrm{SP}(\hat{x}) = \min\{d^\top y : B y \ge r,\ y \ge 0\}, \qquad \mathrm{DSP}(\hat{x}) = \max\{u^\top r : B^\top u \le d,\ u \ge 0\}.$$

The dual feasible set $D = \{u \ge 0 : B^\top u \le d\}$ does not depend on $\hat{x}$. This is the fact that makes the method work: only the objective of the dual changes from one master solution to the next.

## The algorithm

The master problem holds a set $F$ of *feasibility cuts* (vectors $\rho \ge 0$ with $B^\top \rho \le 0$) and a set $O$ of *optimality cuts* (vertices $u$ of $D$). It is

$$\min\ c^\top x + \eta \quad \text{subject to} \quad x \in X,\quad \rho^\top (h - G x) \le 0 \ (\rho \in F),\quad \eta \ge u^\top (h - G x) \ (u \in O).$$

While $O$ is empty, $\eta$ has no lower bound, and the master returns any $x \in X$ that meets the feasibility cuts, with $\eta = -\infty$.

```pseudo id=main
BENDERS(c, d, G, B, h, X)
L1  F ← ∅;  O ← ∅
L2  repeat
L3      solve the master problem over X with the cuts F and O
L4      if the master problem is infeasible then return INFEASIBLE
L5      (x̂, η̂) ← an optimal master solution;  r ← h − G x̂
L6      (ρ, w) ← an optimal solution and value of max{ρᵀr : Bᵀρ ≤ 0, 1ᵀρ ≤ 1, ρ ≥ 0}
L7      if w > 0 then add ρ to F and go to L2        ▷ SP(x̂) is infeasible
L8      solve DSP(x̂) = max{uᵀr : Bᵀu ≤ d, u ≥ 0} by the simplex method
L9      if DSP(x̂) is infeasible then return UNBOUNDED
L10     (u, s) ← its optimal vertex and value;  if η̂ ≥ s then return x̂ and an optimal y of SP(x̂)
L11     add u to O
```

Line L6 is a [Farkas](/farkas-lemma/) test. The ray LP is always feasible ($\rho = 0$) and bounded (its feasible set lies in the simplex $\rho \ge 0$, $1^\top \rho \le 1$). Its value $w$ is positive exactly when $\mathrm{SP}(\hat{x})$ has no solution, and then $\rho$ gives the cut $\rho^\top (h - G x) \le 0$, which removes $\hat{x}$ and every other $x$ that fails for the same reason. Line L8 runs only when $\mathrm{SP}(\hat{x})$ is feasible. Then $\mathrm{DSP}(\hat{x})$ is not unbounded, so it is either infeasible (and $\mathrm{SP}(\hat{x})$ is unbounded) or it has an optimal vertex $u$ with value $s = \mathrm{SP}(\hat{x})$. The cut $\eta \ge u^\top (h - G x)$ is valid for every $x$, because $u$ stays dual feasible for every right-hand side.

The two classic bounds are the master value $LB = c^\top \hat{x} + \hat{\eta}$, a lower bound on the optimum, and $UB = \min c^\top \hat{x} + s$ over the iterations, an upper bound. The test $\hat{\eta} \ge s$ of line L10 is the same as $LB \ge c^\top \hat{x} + s \ge UB$.

## Example

Two plants can each be built in up to 2 modules. A module of plant 1 costs 5 and gives capacity 5; a module of plant 2 costs 3 and gives capacity 4. Shipping from plant 1 costs 1 per unit, from plant 2 costs 3 per unit, and the demand is 6. So $x \in \{0, 1, 2\}^2$, $c = (5, 3)$, $d = (1, 3)$, and the rows are $y_1 + y_2 \ge 6$, $5x_1 - y_1 \ge 0$ and $4x_2 - y_2 \ge 0$. The master enumerates $X$ in the order $(0,0), (0,1), (0,2), (1,0), \dots$ and takes the first minimum.

| iteration | $\hat{x}$ | $\hat{\eta}$ | subproblem | new cut | LB | UB |
|---|---|---|---|---|---|---|
| 1 | (0, 0) | $-\infty$ | infeasible, $\rho = (1/3, 1/3, 1/3)$ | $5x_1 + 4x_2 \ge 6$ | $-\infty$ | $\infty$ |
| 2 | (0, 2) | $-\infty$ | $s = 18$, $u = (3, 2, 0)$ | $\eta \ge 18 - 10x_1$ | $-\infty$ | 24 |
| 3 | (2, 0) | $-2$ | $s = 6$, $u = (1, 0, 0)$ | $\eta \ge 6$ | 8 | 16 |
| 4 | (1, 1) | 8 | $s = 8$ | none: $\hat{\eta} \ge s$ | 16 | 16 |

The feasibility cut says that the capacity must cover the demand, and it removes $(0,0)$, $(0,1)$ and $(1,0)$ at once. In iteration 3 the master value is $c^\top \hat{x} + \hat{\eta} = 10 - 2 = 8$. In iteration 4 the master has $\eta \ge \max(18 - 10x_1, 6)$; both $(1,1)$ and $(2,0)$ give $16$, and the first one in the order is $(1,1)$. Its subproblem ships $y = (5, 1)$ at cost 8, so the optimum is $5 + 3 + 5 + 3 = 16$. The solution $(2, 0)$ with $y = (6, 0)$ is also optimal. Brute force over the 9 points of $X$ gives the same value.

## Correctness

**Theorem.** If $X$ is finite, BENDERS stops after finitely many iterations. It returns INFEASIBLE exactly when the problem has no solution, UNBOUNDED exactly when it has solutions of arbitrarily small value, and otherwise an optimal solution.

The full proof is below. It has three parts. Each cut is valid: a feasibility cut holds at every $x$ with a feasible subproblem, by the easy half of Farkas' lemma, and an optimality cut holds at every $x$, by [weak duality](/weak-duality/). So the master is a relaxation, and its value is a lower bound. At the return of line L10, the returned pair reaches this lower bound. Finally, each iteration that does not stop adds a cut that the current master solution violates, so the cut is new. The cuts are vertices of two fixed polyhedra, so there are finitely many of them.

## Complexity

Let $K$ be the number of iterations. Each iteration solves one master problem (time $M$) and at most two linear programs of size $m \times q$ (time $T$). The extra space holds the cuts, each a vector of $m$ numbers. So the time is $O(K(M + T))$ and the extra space is $O(K m)$, in the worst case.

The proof of finiteness gives $K \le |V(D)| + |V(R)| + 1$, where $V(D)$ is the set of vertices of $D$ and $V(R)$ the set of vertices of the ray polytope $R = \{\rho \ge 0 : B^\top \rho \le 0,\ 1^\top \rho \le 1\}$. Both counts can be exponential in $m$ and $q$, so this bound is not polynomial, and no polynomial bound on $K$ is known in general. Each master solve is also an integer program, which is [NP-hard](/np-hard/) in general. In practice the number of iterations depends on the formulation and on the cut choices, and it is often the bottleneck.

The implementation on this page solves the master problem by enumeration of $X$, so $M = O(|X| K m p)$. A real code solves the master with [branch and cut](/branch-and-cut/), and it uses the [dual simplex method](/dual-simplex-method/) to resolve the subproblem from the last basis, because only the objective of the dual changes.

## Properties

- **Exact.** With exact arithmetic, the method returns an optimal solution, not an approximation.
- **The master is a relaxation.** Its value never decreases from one iteration to the next, because each iteration only adds constraints.
- **The cuts are global.** A Benders cut is valid for every $x \in X$, not only near the point that produced it.
- **Deterministic.** The simplex method with [Bland's rule](/bland-rule/) and a fixed order of $X$ make each run the same.

## Variants and improvements

- **L-shaped method.** For a two-stage stochastic program the subproblem splits into one linear program for each scenario. Van Slyke and Wets add one cut for the sum of the scenarios (single cut) or one variable $\eta_k$ and one cut for each scenario (multi-cut).
- **Generalized Benders decomposition.** Geoffrion replaces the linear subproblem with a convex program, and uses its Lagrange multipliers in place of the dual vertex.
- **Pareto-optimal cuts.** When $\mathrm{DSP}(\hat{x})$ has many optimal vertices, Magnanti and Wong choose one whose cut is not dominated by the cut of any other.
- **Branch and Benders cut.** Modern codes solve the master problem only once by [branch and cut](/branch-and-cut/), and they add Benders cuts at the nodes of the tree as lazy constraints, instead of solving a new master problem from the start in each iteration.
- **Combinatorial and logic-based Benders.** Codato and Fischetti use cuts of the form "not this set of binary values", and Hooker and Ottosson allow any subproblem whose infeasibility can be explained by a logical rule.
- **Dual view.** Benders decomposition of a linear program is [Dantzig-Wolfe decomposition](/dantzig-wolfe-decomposition/) applied to its dual: Benders adds rows (cuts) where Dantzig-Wolfe adds columns ([column generation](/column-generation/)).

## When to use it

Use Benders decomposition when fixing a small group of variables leaves a linear program that is large but easy, or that splits into many independent parts: facility location, network design, two-stage stochastic programs and unit commitment. The subproblem is a linear program, so the cuts are exact. If the coupling rows are few and the remaining problem has a special structure, the subproblem can even be solved by a combinatorial algorithm, such as a [flow](/min-cost-flow-lp-formulation/) solver. If the integer and continuous variables are mixed in all constraints, the split gives no gain, and a direct [branch and cut](/branch-and-cut/) on the whole model is usually better.

## Pitfalls

- **Forgetting the feasibility cuts.** If $\mathrm{SP}(\hat{x})$ can be infeasible and the code only adds optimality cuts, it loops or crashes. Add the Farkas ray cut of lines L6 and L7. The test case with demand 10 above the capacity 9 checks the INFEASIBLE answer.
- **An unbounded ray LP.** Without the normalization $1^\top \rho \le 1$, the Farkas LP is a cone and is unbounded whenever a ray exists. Keep the normalization, or take the ray from the unbounded dual.
- **Taking an unbounded subproblem for an infeasible one.** If $\mathrm{DSP}(\hat{x})$ is infeasible, then $\mathrm{SP}(\hat{x})$ is either infeasible or unbounded. Only after the Farkas test of line L6 says "feasible" may the code return UNBOUNDED. The test with $\min x - y$ subject to $x + y \ge 1$ checks this case.
- **Missing lower bound on $\eta$.** While $O$ is empty the master value is $-\infty$. A code that sets $\eta \ge 0$ by habit is wrong when the subproblem cost can be negative.
- **Tolerance.** With floating-point arithmetic the stop test $\hat{\eta} \ge s$ needs a tolerance, or the method can add the same cut again and again.

## Implementations

The Python code uses `fractions.Fraction` and a two-phase tableau simplex with Bland's rule, so every cut is exact. The master problem is solved by enumeration of a box of integer points. The tests compare the result with brute force over the box, where each point solves its own subproblem, on random instances that include infeasible and unbounded ones.

## History

Benders published the method in 1962, for problems with "mixed variables". Van Slyke and Wets gave the L-shaped method for stochastic programs in 1969. Geoffrion extended the method to convex subproblems in 1972, and Magnanti and Wong introduced Pareto-optimal cuts in 1981. The survey of Rahmaniani, Crainic, Gendreau and Rei (2017) covers the later work.

## References
