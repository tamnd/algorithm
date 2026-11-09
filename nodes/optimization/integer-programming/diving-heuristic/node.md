---
tag: 5DXE8N
kind: technique
slug: diving-heuristic
name: Diving heuristic
aliases:
- diving
- dive-and-fix
area: optimization/integer-programming
level: advanced
summary: Primal heuristic that repeatedly rounds or fixes one fractional variable and resolves the LP, going down one path of the tree.
prereqs: [lp-relaxation, mixed-integer-programming, land-doig-algorithm, incumbent-solution]
see_also: [feasibility-pump, relaxation-induced-neighborhood-search, local-branching, pseudocost-branching, depth-first-branch-and-bound, branch-and-cut, randomized-rounding, incumbent-solution]
sources:
  - paper: "Timo Berthold, Primal heuristics for mixed integer programs, Diploma thesis, Technische Universität Berlin, 2006"
    locator: the chapter on diving heuristics (fractional, coefficient, guided, pseudocost and vector length diving; chapter number unsure)
  - paper: doi:10.1007/s10107-004-0518-7
    title: E. Danna, E. Rothberg and C. Le Pape, Exploring relaxation induced neighborhoods to improve MIP solutions, Mathematical Programming 102(1), 2005
    locator: pp. 71 to 90 (guided dives, which round toward the incumbent)
  - paper: "Tobias Achterberg, Constraint Integer Programming, PhD thesis, Technische Universität Berlin, 2007"
    locator: the chapter on primal heuristics in SCIP (diving and its single backtrack; chapter number unsure)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 12 (heuristic algorithms, dive-and-fix; section unsure)
---

A diving heuristic is a primal heuristic for [mixed integer programs](/mixed-integer-programming/) that goes down a single path of the branch and bound tree. At each step it picks one fractional integer variable of the [LP relaxation](/lp-relaxation/), rounds it by changing one bound, and solves the LP again, until the LP solution is integral, the LP becomes infeasible, or a limit is reached. Each solution it returns is feasible, but it does not search for the optimum, and a dive can fail. Solvers run many diving rules that differ only in which variable they round and in which direction.

## In plain words

The relaxed problem, in which whole-number variables may be fractions, is easy to solve but its answer usually has fractions. A dive repairs the answer one variable at a time. It takes one variable with a fraction, decides to round it up or down, adds that decision as a rule, and solves the relaxed problem again. The other variables can move to make up for the change.

After a few rounds, either all the variables are whole numbers, which gives a real solution, or the rules contradict each other and the dive fails. The choice of which variable to round, and in which direction, is the whole art. A dive is cheap because it follows only one path, but it can make a bad choice early and not recover.

## When it applies

- A mixed integer program whose LP relaxation is solved inside [branch and bound](/land-doig-algorithm/) or [branch-and-cut](/branch-and-cut/), often with no good [incumbent](/incumbent-solution/) yet.
- An LP solver that changes one bound and restarts fast from the current basis, usually the dual simplex method.
- The model has many integer variables whose LP values are already integral or nearly integral, so that a few roundings are enough.

## The template

The holes are SELECT (which fractional variable, and which direction), PROPAGATE (bound propagation after each change, or nothing), ON-INFEASIBLE (stop, or undo the last change once and try the other direction) and the limit MAX-STEPS. The problem is a maximization and $z^*$ is the value of the incumbent, or $-\infty$.

```pseudo id=main
DIVE(N, z*)
L1  ℓ, u ← the bounds of node N
L2  for step ← 1 to MAX-STEPS do
L3      solve the LP with the bounds ℓ, u;  let x̄ be optimal and v its value
L4      if the LP is infeasible then apply ON-INFEASIBLE; if it stops, return none
L5      if v ≤ z* then return none                    ▷ no better point on this path
L6      if x̄_j is integral for all j ∈ I then return x̄
L7      (j, dir) ← SELECT(x̄)                           ▷ a fractional x̄_j and a direction
L8      if dir = down then u_j ← ⌊x̄_j⌋ else ℓ_j ← ⌈x̄_j⌉
L9      PROPAGATE(ℓ, u)
L10 return none
```

Common SELECT rules: *fractional diving* rounds the variable closest to an integer in the direction of that integer; *coefficient diving* prefers variables that can be rounded in a direction that breaks few rows; *guided diving* rounds toward the value of the variable in the incumbent; *pseudocost diving* uses the [pseudocosts](/pseudocost-branching/) to choose the direction with the smaller expected loss; *vector length diving* prefers variables whose rounding changes the objective least per affected row.

**What is guaranteed.** If the dive returns $\bar{x}$ at line L6, then $\bar{x}$ satisfies all the rows of the LP, its integer variables have integer values, and $\ell \le \bar{x} \le u$ for bounds inside the original ones. So $\bar{x}$ is a feasible point of the program, and line L5 ensures $c^\top \bar{x} > z^*$. The dive also stops: each step changes the bound of an integer variable so that it excludes the current fractional value, so with bounded integer variables the number of steps is at most $\sum_{j \in I} (u_j - \ell_j) + 1$, and MAX-STEPS bounds it in any case.

**What is not guaranteed.** The returned point need not be optimal, and a dive may return nothing although feasible points exist. The ranking of the SELECT rules is a matter of measurement on test sets.

**Example.** Take
$$\max\ 3x_1 + 5x_2 + 6x_3 \quad \text{s.t.} \quad 9x_1 + 6x_2 + 2x_3 \le 14,\quad 7x_1 + 6x_2 + 8x_3 \le 14,\quad x \in \{0, 1, 2, 3\}^3,$$
with fractional diving and no incumbent.

| step | LP optimum | LP value | rounding |
|---|---|---|---|
| 1 | $(0, \tfrac73, 0)$ | $\tfrac{35}{3}$ | $x_2$ is $\tfrac13$ from 2: $x_2 \le 2$ |
| 2 | $(0, 2, \tfrac14)$ | $\tfrac{23}{2}$ | $x_3$ is $\tfrac14$ from 0: $x_3 \le 0$ |
| 3 | $(\tfrac29, 2, 0)$ | $\tfrac{32}{3}$ | $x_1$ is $\tfrac29$ from 0: $x_1 \le 0$ |
| 4 | $(0, 2, 0)$ | 10 | integral: return it |

The dive finds the feasible point $(0, 2, 0)$ with value 10 after four LP solves. The optimum is 11, at $(0, 1, 1)$, so the first rounding, $x_2 \le 2$, kept a path that does not lead to it. The point found still gives branch and bound an incumbent with which it can prune nodes whose bound is at most 10.

## Classic examples

- **Dive-and-fix.** Wolsey describes a simple heuristic for 0-1 programs that fixes variables whose LP values are close to 0 or 1 and dives with the rest.
- **Guided dives.** Danna, Rothberg and Le Pape (2005) introduced guided dives, which round each variable toward its value in the incumbent, and used them as one of the heuristics compared with RINS.
- **SCIP.** SCIP contains a family of diving heuristics that share the template and differ in SELECT, among them fractional, coefficient, guided, pseudocost, vector length and line search diving, as described in the theses of Berthold and Achterberg. They run at selected nodes of the tree, with limits on the LP iterations they may spend.
- **Diving as node selection.** In [depth-first branch and bound](/depth-first-branch-and-bound/), the search itself dives until it finds a feasible point. A diving heuristic does the same thing outside the tree, and its nodes are discarded afterwards.

## Variations

- **Single backtrack.** If the LP becomes infeasible, undo the last bound change once and take the other direction. SCIP uses this rule.
- **Fixing many variables at once.** Fix all integer variables whose LP values are integral, or within a small distance of an integer, before the next LP solve. This makes the dive shorter but more likely to fail.
- **Diving without LP solves.** Propagate the bound changes instead of solving the LP after each one, and solve the LP only at the end or after several changes. This is cheaper per step.
- **Sub-MIP after a dive.** If the dive fixes most variables and then fails, the remaining small problem can be solved with a limited branch and bound, as in [RINS](/relaxation-induced-neighborhood-search/).
- **The [feasibility pump](/feasibility-pump/)** rounds all variables at once and moves the LP point toward the rounded point, instead of fixing one variable at a time.

## Pitfalls

- **No feasible point found.** A dive is a single path. Models with tight equality structure often make every path infeasible after a few steps; the heuristic then only costs time.
- **Rounding toward a bad incumbent.** Guided diving follows the incumbent, so it searches near a point that may be far from the optimum.
- **Shared state with the search.** The bound changes of a dive must be undone fully before branch and bound continues, and the pseudocosts learned during a dive describe nodes that are not part of the tree.
- **LP cost.** Each step is one LP solve. Without a limit on the iterations, a dive at every node can cost more than the search itself.
- **Continuous variables.** Only integer variables are rounded. Rounding a continuous variable cuts away feasible points for no reason.

## Exercises

1. Check each LP optimum in the example table.
2. Run the dive of the example with guided diving toward the incumbent $(0, 1, 1)$. Which point does it reach?
3. Prove the bound $\sum_{j \in I} (u_j - \ell_j) + 1$ on the number of LP solves of a dive without backtracking.
4. Give a 0-1 program with a feasible point for which fractional diving from the root, without backtracking, ends with an infeasible LP. Hint: two equality rows in three variables are enough.
5. Design a SELECT rule that uses the number of rows a rounding could break, and explain how to compute it from the activity bounds of the rows.

## References
