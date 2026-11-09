---
tag: Y8HGH5
kind: technique
slug: lagrangian-relaxation
name: Lagrangian relaxation
aliases:
- Lagrangian duality method
- Lagrangean relaxation
area: optimization/combinatorial-optimization
level: advanced
summary: Dualize hard constraints with multipliers to get bounds and easier subproblems.
prereqs: [lagrangian-duality, subgradient, lp-relaxation, combinatorial-optimization-problem]
see_also: [lagrangian-duality, subgradient, held-karp-bound, dantzig-wolfe-decomposition, dual-decomposition, bundle-method, lp-relaxation, knapsack-branch-and-bound]
sources:
  - paper: doi:10.1287/mnsc.27.1.1
    title: Marshall L. Fisher, The Lagrangian relaxation method for solving integer programming problems, Management Science 27(1), 1 to 18, 1981
    locator: the whole paper (the method, the subgradient step rule, and the applications)
  - paper: "Arthur M. Geoffrion, Lagrangean relaxation for integer programming, Mathematical Programming Study 2, 82 to 114, 1974"
    locator: the theorem that the Lagrangian bound equals the LP bound over the convex hull of the kept constraints, and the integrality property
  - paper: doi:10.1287/opre.18.6.1138
    title: Michael Held and Richard M. Karp, The traveling-salesman problem and minimum spanning trees, Operations Research 18(6), 1138 to 1162, 1970
    locator: the 1-tree relaxation of the degree constraints
  - paper: doi:10.1007/BF01584070
    title: Michael Held and Richard M. Karp, The traveling-salesman problem and minimum spanning trees, part II, Mathematical Programming 1(1), 6 to 25, 1971
    locator: subgradient optimization of the multipliers
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 10, Lagrangian duality
---

Lagrangian relaxation is a technique for hard [integer programs](/mixed-integer-programming/) of the form $\min \{ c^\top x : A x \le b, \; x \in X \}$, where optimizing over $X$ alone is easy and the constraints $A x \le b$ make the problem hard. It moves the hard constraints into the objective with nonnegative multipliers $\lambda$, which gives the subproblem $L(\lambda) = \min_{x \in X} \bigl( c^\top x + \lambda^\top (A x - b) \bigr)$. Each $L(\lambda)$ is a lower bound on the optimum, and the best such bound, $\max_{\lambda \ge 0} L(\lambda)$, is the [Lagrangian dual](/lagrangian-duality/). The dual function is concave and piecewise linear, and it is maximized with [subgradient](/subgradient/) or [bundle](/bundle-method/) methods. The bound is never worse than the [LP relaxation](/lp-relaxation/), and it is strictly better when the convex hull of $X$ is smaller than its LP relaxation (Geoffrion 1974). The method gives bounds for [branch and bound](/knapsack-branch-and-bound/), near-feasible solutions for heuristics, and reduced costs for fixing variables. Its best known use is the [Held-Karp bound](/held-karp-bound/) for the traveling salesman problem.

## In plain words

Some problems would be easy if one or two kinds of rules were removed. Lagrangian relaxation removes those rules, but charges a price for each unit by which a solution breaks them. You then solve the easy problem with the prices included.

The answer of the easy problem is never worse than the true best answer, so it gives a guaranteed limit. If a rule is broken a lot, you raise its price; if a rule is met with room to spare, you lower its price. After some rounds the limit gets close to the best possible limit, and the easy solutions are often nearly valid. A small repair then gives a good valid solution.

## When it applies

- **Easy core, few hard constraints.** The problem is $\min \{ c^\top x : A x \le b, \; x \in X \}$, where $X$ is a set with a fast exact algorithm (shortest paths, spanning trees, knapsacks, assignments, independent blocks) and $A x \le b$ is a small or simple set of complicating constraints. For equality constraints $A x = b$ the multipliers are free in sign.
- **Decomposable structure.** If dropping the hard constraints splits the problem into independent blocks, each block is solved on its own. This is [dual decomposition](/dual-decomposition/).
- **A bound is needed.** The method gives a lower bound for every $\lambda \ge 0$, so it is useful inside branch and bound, and to measure how good a heuristic solution is.
- **The LP bound is weak.** If $X$ does not have the integrality property, that is, the LP relaxation of $X$ is not $\operatorname{conv}(X)$, then the Lagrangian bound can be much stronger than the LP bound.
- **Not useful** when the subproblem is as hard as the original, or when $X$ has the integrality property and an LP solver is fast enough: then the Lagrangian bound equals the LP bound, and the LP gives it directly.

## The template

```pseudo id=main
LAGRANGIAN-RELAXATION(c, A, b, X)
L1  λ ← 0;  LB ← −∞;  UB ← +∞
L2  for k ← 0, 1, 2, … until a stopping rule holds
L3      x ← a minimizer of c·x + λ·(A x − b) over x ∈ X        ▷ the easy subproblem
L4      LB ← max(LB, c·x + λ·(A x − b))                       ▷ a valid lower bound
L5      if A x ≤ b then UB ← min(UB, c·x)                        ▷ or repair x by a heuristic
L6      g ← A x − b                                            ▷ a subgradient of L at λ
L7      if g = 0 or UB − LB is small enough then stop
L8      choose a step t_k > 0, for example t_k = θ_k (UB − L(λ)) / ‖g‖²
L9      λ ← max(0, λ + t_k g)                                   ▷ componentwise
L10 return LB, UB and the best feasible x
```

**Why line L4 is a bound.** If $x^*$ is optimal for the original problem, then $A x^* - b \le 0$ and $\lambda \ge 0$, so $L(\lambda) \le c^\top x^* + \lambda^\top (A x^* - b) \le c^\top x^*$. This is weak duality.

**Why line L6 is a subgradient.** $L$ is a minimum of the affine functions $\lambda \mapsto c^\top x + \lambda^\top (A x - b)$, one for each $x \in X$, so it is concave. The function for the minimizer $x$ touches $L$ at $\lambda$ and lies above it elsewhere, so its slope $A x - b$ is a subgradient. Line L9 moves along it, and line L8 is the step of Polyak with a factor $\theta_k \in (0, 2]$, as used by Held, Wolfe and Crowder. With steps $t_k \to 0$ and $\sum t_k = \infty$, the best value $\max_{j \le k} L(\lambda_j)$ converges to the dual optimum, but slowly, and $L(\lambda_k)$ itself does not rise at every step.

**How strong the bound is (Geoffrion 1974).** For a finite set $X$, or a set of integer points of a rational polyhedron,
$$\max_{\lambda \ge 0} L(\lambda) = \min \{ c^\top x : A x \le b, \; x \in \operatorname{conv}(X) \}.$$
So the Lagrangian dual is at least the LP bound, and it equals the LP bound when $X$ has the integrality property.

**Example.** Find a cheapest path from $s$ to $t$ with total delay at most $T = 5$, in a graph with three paths:

| path | cost | delay | $L$ term $\text{cost} + \lambda (\text{delay} - 5)$ |
| --- | --- | --- | --- |
| $s \to a \to t$ | 3 | 10 | $3 + 5\lambda$ |
| $s \to b \to t$ | 5 | 6 | $5 + \lambda$ |
| $s \to t$ | 8 | 3 | $8 - 2\lambda$ |

Only $s \to t$ meets the delay limit, so the optimum is 8. Relaxing the delay constraint leaves a [shortest path](/constrained-shortest-path/) problem with arc lengths $\text{cost} + \lambda \cdot \text{delay}$. Then $L(\lambda) = \min(3 + 5\lambda, \; 5 + \lambda, \; 8 - 2\lambda)$, which is largest at $\lambda = 1$ with $L(1) = 6$. A subgradient run with $t_k = 1 / (5(k + 1))$ and ties broken in table order gives:

| $k$ | $\lambda_k$ | path chosen | $L(\lambda_k)$ | $g$ = delay $- 5$ |
| --- | --- | --- | --- | --- |
| 0 | 0 | $s \to a \to t$ | 3 | 5 |
| 1 | 1 | $s \to b \to t$ | 6 | 1 |
| 2 | 1.1 | $s \to t$ | 5.8 | $-2$ |
| 3 | 0.967 | $s \to b \to t$ | 5.967 | 1 |
| 4 | 1.017 | $s \to t$ | 5.967 | $-2$ |

The bound stays at $LB = 6$ and the multiplier oscillates around 1. At $k = 2$ the subproblem returns the feasible path $s \to t$, so $UB = 8$. The gap $8 - 6 = 2$ remains, because the LP relaxation has the same value: $\tfrac{2}{3}$ of path $s \to b \to t$ and $\tfrac{1}{3}$ of $s \to t$ have delay 5 and cost 6. Shortest paths have the integrality property, so Geoffrion's theorem says no Lagrangian bound can beat the LP bound here. Branching on the delay closes the gap.

## Classic examples

- **[Held-Karp bound](/held-karp-bound/) for the TSP.** Keep the 1-tree structure and dualize the degree-2 constraints with vertex multipliers. Each subproblem is a [minimum spanning tree](/minimum-spanning-tree/) with modified edge costs. The best bound equals the subtour LP bound, and in experiments on random uniform instances it is often within about 1 percent of the optimum.
- **[Generalized assignment](/generalized-assignment-problem/).** Dualize the constraints that assign each job once, and the problem splits into one [knapsack problem](/knapsack-problem/) per machine. Since knapsack lacks the integrality property, this bound can beat the LP bound. Dualizing the capacity constraints instead leaves a problem with the integrality property, so that bound is only the LP bound.
- **[Facility location](/facility-location-problem/).** Dualize the constraints that each customer is served once. The subproblem decides each facility independently by the sign of a reduced cost. The bound equals the strong LP bound of the uncapacitated problem.
- **[Constrained shortest path](/constrained-shortest-path/).** Dualize the resource limit, as in the example. The subproblem is a plain shortest path.
- **[Set cover](/set-cover/).** Dualize the covering constraints; the subproblem picks each set whose reduced cost is negative. Combined with greedy repair, this gives strong heuristics for large instances.
- **Network problems with side constraints** and **scheduling** problems where machine capacity couples otherwise independent jobs, for example in unit commitment for power systems.

## Variations

- **Dual decomposition.** Copy shared variables, dualize the copy constraints, and solve independent blocks in parallel. See [dual decomposition](/dual-decomposition/).
- **Bundle and cutting plane methods.** Instead of subgradient steps, keep the affine pieces seen so far and maximize a stabilized model of $L$. See [bundle methods](/bundle-method/). Kelley's cutting plane method on the dual is equivalent to [Dantzig-Wolfe decomposition](/dantzig-wolfe-decomposition/) solved by [column generation](/column-generation/), and both reach the same bound.
- **Lagrangian decomposition (variable splitting).** Duplicate the variables, keep one set of constraints on each copy, and dualize the equality of the copies. The bound is at least as strong as relaxing either set alone.
- **Relax-and-cut.** Dualize cutting planes found on the fly, as in branch and cut, but without adding them to an LP.
- **Lagrangian heuristics.** Repair the subproblem solution $x$ at each step, for example by a greedy fix of the violated constraints, to get upper bounds.
- **Surrogate relaxation.** Replace the constraints by one weighted sum $\lambda^\top A x \le \lambda^\top b$ and keep it as a constraint. The bound is at least as good as the Lagrangian one, but the subproblem is often harder.
- **Variable fixing.** With a dual value $L(\lambda)$ and an upper bound $UB$, any variable whose reduced cost would push $L(\lambda)$ above $UB$ can be fixed, which shrinks the problem for branch and bound.

## Pitfalls

- **Relaxing the wrong constraints.** If the remaining set $X$ has the integrality property, the bound is only the LP bound. If $X$ is still hard, each step is expensive. The choice is a trade-off between bound strength and subproblem speed.
- **Expecting a feasible solution.** The subproblem solution usually violates the dualized constraints. Even at the optimal $\lambda$, a duality gap can remain, as in the example. A repair heuristic or branch and bound is needed for a feasible solution.
- **Step size.** Fixed steps do not converge, and steps that shrink too fast stop far from the optimum. Polyak steps need a good target value; the factor $\theta_k$ is usually halved when the bound does not improve for some iterations.
- **Non-monotone progress.** $L(\lambda_k)$ goes up and down, so keep the best value seen, as in line L4.
- **Sign rules.** Multipliers of inequality constraints must stay nonnegative (line L9), and multipliers of equality constraints are free. For maximization problems, all signs flip and the method gives upper bounds.
- **Stopping on $g = 0$.** A zero subgradient with complementary slackness, $\lambda^\top (A x - b) = 0$, proves that $x$ is optimal. With $A x \le b$ but $\lambda^\top (A x - b) < 0$, $x$ is feasible but not proved optimal.

## Exercises

1. Show that $L(\lambda)$ is concave and piecewise linear when $X$ is finite, and that $A x - b$ is a subgradient at $\lambda$ for every minimizer $x$.
2. In the example, show that no choice of $\lambda$ gives a bound above 6, and find the LP solution that has value 6.
3. For the generalized assignment problem, compare the bound from dualizing the assignment constraints with the bound from dualizing the capacity constraints. Which one has the integrality property?

## References
