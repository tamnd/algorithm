---
tag: TG0PBP
kind: technique
slug: presolve
name: Presolve
aliases:
- MIP presolve
- preprocessing for integer programs
area: optimization/integer-programming
level: advanced
summary: Reductions that shrink and tighten a mixed integer program before and during branch-and-bound.
prereqs: [mixed-integer-programming, lp-relaxation, binary-integer-programming]
see_also: [branch-and-cut, constraint-propagation, fourier-motzkin-elimination, implication-graph, big-m-formulation, cover-inequality, lp-relaxation, integer-hull]
sources:
  - paper: doi:10.1287/ijoc.6.4.445
    title: Martin W. P. Savelsbergh, Preprocessing and probing techniques for mixed integer programming problems, ORSA Journal on Computing 6(4), 1994
    locator: pp. 445 to 454 (bound tightening, coefficient tightening, probing and implications)
  - paper: doi:10.1287/ijoc.2018.0857
    title: Tobias Achterberg, Robert E. Bixby, Zonghao Gu, Edward Rothberg and Dieter Weninger, Presolve reductions in mixed integer programming, INFORMS Journal on Computing 32(2), 2020
    locator: pp. 473 to 506; Section 2 and Table 1 (Gurobi 6.5 with presolve disabled, 3182 models)
  - paper: "Tobias Achterberg and Roland Wunderling, Mixed integer programming: analyzing 12 years of progress, in Facets of Combinatorial Optimization, Springer, 2013, 449 to 481"
    locator: the presolve rows of the feature tables (CPLEX, the bracket of models that take at least 10 seconds)
  - paper: "A. L. Brearley, G. Mitra and H. P. Williams, Analysis of mathematical programming problems prior to applying the simplex algorithm, Mathematical Programming 8, 1975, 54 to 83"
    locator: early LP reductions (singleton rows, redundant rows, fixed and dominated columns)
---

Presolve is the set of reductions that a solver for [mixed integer programs](/mixed-integer-programming/) applies before branch and bound, and often again at nodes of the tree. Each reduction either removes rows, columns or nonzeros, or tightens bounds and coefficients so that the [LP relaxation](/lp-relaxation/) comes closer to the [integer hull](/integer-hull/), and each one keeps the optimal value. A postsolve step maps a solution of the reduced problem back to the original one. Measurements on large test sets show that presolve is one of the most important parts of a modern solver, but its effect is a measured average, not a guarantee for each instance.

## In plain words

Models written by people or produced by programs often contain constraints that can never be tight, variables whose best value is clear at once, and coefficients that are larger than they need to be. Presolve finds and removes these before the hard search starts.

The basic tool is simple reasoning about each constraint alone. If the other variables of a constraint can only add so much, a variable cannot be larger than what is left over. If a whole number variable can only be zero or one, a coefficient can often be made smaller without losing any whole number answer, while it removes fractional answers. The solver repeats these steps until nothing changes. It keeps a record of every step so that it can rebuild the answer to the original model at the end.

## When it applies

- A mixed integer program $\max\{c^\top x : A x \le b,\ \ell \le x \le u,\ x_j \in \mathbb{Z} \text{ for } j \in I\}$ with some finite bounds. Equations and other row types are handled the same way.
- The user needs one optimal solution and the optimal value. Reductions that use the objective, called dual reductions, can remove other optimal solutions, so they are turned off when all optimal solutions or a fixed model structure are needed.
- A postsolve stack can be kept, with enough information to undo each reduction.

## The template

The holes are REDUCTIONS (the ordered list of reduction routines), LIMIT (the work limit) and, for each reduction, its UNDO step. The *activity bounds* of row $i$ are
$$L_i = \sum_{a_{ij} > 0} a_{ij} \ell_j + \sum_{a_{ij} < 0} a_{ij} u_j, \qquad U_i = \sum_{a_{ij} > 0} a_{ij} u_j + \sum_{a_{ij} < 0} a_{ij} \ell_j,$$
the least and the largest value of $a_i^\top x$ over the bounds.

```pseudo id=main
PRESOLVE(P)
L1  stack ← empty
L2  repeat
L3      changed ← false
L4      for each routine R in REDUCTIONS, cheapest first do
L5          apply R to P and push UNDO(R) on stack
L6          if R proved P infeasible or unbounded then return that status
L7          if R changed P then changed ← true
L8  until not changed or LIMIT is reached
L9  return P, stack

POSTSOLVE(x, stack)
L10 while stack is not empty do
L11     pop an UNDO step and apply it to x            ▷ reverse order
L12 return x
```

The reductions below are the core of REDUCTIONS. Each one keeps at least one optimal solution, so the reduced problem has the same optimal value.

- **Infeasible and redundant rows.** If $L_i > b_i$, no point satisfies row $i$ within the bounds, so the problem is infeasible. If $U_i \le b_i$, row $i$ holds for every point within the bounds and can be removed.
- **Bound tightening.** For $a_{ik} > 0$, every feasible point has $a_{ik} x_k \le b_i - (L_i - a_{ik} \ell_k)$, since the other terms are at least their part of $L_i$. So $u_k$ can be lowered to $\ell_k + (b_i - L_i)/a_{ik}$, and rounded down if $k \in I$. The case $a_{ik} < 0$ is symmetric.
- **Coefficient tightening.** Let $x_k$ be binary with $a_{ik} > 0$, and let $d = b_i - (U_i - a_{ik})$. If $d > 0$, replace $a_{ik}$ by $a_{ik} - d$ and $b_i$ by $b_i - d$. For $x_k = 1$ the row is unchanged, and for $x_k = 0$ both rows hold for all points within the bounds, because the other terms are at most $U_i - a_{ik} = b_i - d$. So the integer feasible points stay the same, while the LP relaxation becomes smaller.
- **Dual fixing.** If $c_k \le 0$ and $a_{ik} \ge 0$ in every row, then lowering $x_k$ never breaks a row and never lowers the objective. If $\ell_k$ is finite, fix $x_k = \ell_k$; some optimal solution has this value. The undo step restores the fixed value.
- **Probing.** For a binary $x_k$, propagate $x_k = 0$ and $x_k = 1$ separately with bound tightening. If one side is infeasible, fix $x_k$ to the other. If both sides give the same bound on some $x_j$, that bound holds in general. The implications found go into an [implication graph](/implication-graph/) used later for cuts.
- **Singletons and duplicates.** A row with one variable is a bound. Two rows that are multiples of each other are merged. A continuous column that appears in only one row can often be removed and its value recovered from the row in postsolve.

**Example.** Take $x, y$ binary, $z$ integer in $[0, 10]$, $w$ continuous in $[0, 10]$, and
$$\max\ 3x + 2y + z - w \quad \text{s.t.} \quad z + 5x \le 7, \quad 3x + 2y \le 4, \quad x + w \le 3.$$

| step | reduction | result |
|---|---|---|
| 1 | dual fixing on $w$: $c_w = -1$, and $w$ has a positive coefficient in its only row | $w = 0$ |
| 2 | the row $x + w \le 3$ now has $U = 1 \le 3$ | row removed |
| 3 | bound tightening on $z$ in $z + 5x \le 7$: $L = 0$ | $u_z = 7$ |
| 4 | coefficient tightening on $x$ in $3x + 2y \le 4$: $U = 5$, $d = 4 - 2 = 2$ | $x + 2y \le 2$ |
| 5 | coefficient tightening on $y$ in $x + 2y \le 2$: $U = 3$, $d = 2 - 1 = 1$ | $x + y \le 1$ |

The reduced problem is $\max\ 3x + 2y + z$ with $z + 5x \le 7$, $x + y \le 1$ and $z \in [0, 7]$. The fractional point $(x, y) = (1, \tfrac12)$, which satisfies $3x + 2y \le 4$, is no longer feasible for the LP relaxation. Both problems have the optimum 9 at $x = 0$, $y = 1$, $z = 7$, and postsolve sets $w = 0$.

## Classic examples

- **Linear programming presolve.** Brearley, Mitra and Williams (1975) described the removal of singleton rows, redundant rows and fixed or dominated columns before the simplex method. These reductions are still the first step of every LP code.
- **Zero-one programs.** Crowder, Johnson and Padberg (1983) and Savelsbergh (1994) used coefficient tightening and probing on binary variables. Coefficient tightening often turns a [big-M](/big-m-formulation/) constraint into the tightest constraint of its form.
- **Commercial solvers.** Achterberg, Bixby, Gu, Rothberg and Weninger (2020) describe the presolve of Gurobi. On their test set of 3182 models, turning off presolve made Gurobi 6.5 about 9 times slower on average over the models that take at least 10 seconds, and 488 more models hit the time limit. They report that Achterberg and Wunderling (2013) measured a factor of 11.4 for CPLEX in the same kind of test. These are averages over the test sets of the solver vendors, not bounds.

## Variations

- **Node presolve.** At a node of the tree some bounds are tighter, so bound tightening and probing find more. Solvers run a cheap version at nodes; this is the same as [constraint propagation](/constraint-propagation/) in constraint programming.
- **Restarts.** If many variables get fixed during the root cut loop, the solver presolves the problem again and restarts.
- **Dominated columns.** If column $j$ is at least as good as column $k$ in the objective and in every row, an optimal solution exists with $x_k$ at a bound or with $x_j$ at a bound, which allows a fixing or a new inequality.
- **Parallel and exact presolve.** Libraries such as PaPILO run reductions in parallel, and exact solvers apply them in rational arithmetic.
- **Symmetry detection.** Some solvers detect the symmetry group of the problem during presolve and use it later, for example in [orbital branching](/orbital-branching/).

## Pitfalls

- **Dual reductions change the solution set.** They keep one optimal solution, not all of them. They are wrong when the user adds constraints later, enumerates solutions or needs a solution in a part of the space that was cut away.
- **Infinite bounds.** Activity bounds with an infinite term give no information for most variables of the row. Track the number of infinite terms in each activity bound; with exactly one, the bound of that one variable can still be tightened.
- **Numerical drift.** Repeated bound tightening with tiny coefficients produces bounds that change by tiny amounts many times, or values that are wrong by a rounding error. Use tolerances and accept a new bound only if it improves the old one by a clear amount.
- **Integer rounding on continuous variables.** Rounding a tightened bound is correct only for integer variables.
- **Postsolve of duals.** Dual values and reduced costs of the reduced LP do not transfer directly. Each undo step must also say how to recover them if they are needed.

## Exercises

1. Prove that bound tightening on a row never removes an integer feasible point.
2. Show that after coefficient tightening the new row is still valid for every integer feasible point, and that its LP relaxation is contained in the old one.
3. In the example, apply probing to $x$. Which bounds on $z$ and $y$ follow from $x = 1$?
4. Give a model where dual fixing removes an optimal solution, but not all of them.
5. Design the undo step for the removal of a continuous column that appears in only one equation, with bounds on it.

## References
