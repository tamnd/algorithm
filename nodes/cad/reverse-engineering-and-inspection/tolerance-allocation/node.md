---
tag: YWH6SS
kind: problem
slug: tolerance-allocation
name: Tolerance allocation
aliases:
- tolerance synthesis
- least-cost tolerance allocation
area: cad/reverse-engineering-and-inspection
level: core
summary: Choose part tolerances that meet an assembly tolerance at least manufacturing cost, from cost-tolerance curves, by Lagrange multipliers or optimisation.
prereqs: [tolerance-stack-up, lagrange-multiplier, convex-function]
see_also: [direct-linearization-method, monte-carlo-tolerance-analysis, kkt-conditions, geometric-programming, knapsack-problem, subset-sum-problem, pseudo-polynomial-time, bisection-method]
sources:
  - paper: doi:10.1115/1.3438222
    title: M. F. Spotts, Allocation of tolerances to minimize cost of assembly, Journal of Engineering for Industry 95(3), 762 to 764, 1973
    locator: the whole paper (allocation of tolerances by a cost model and Lagrange multipliers; general locator)
  - paper: "Kenneth W. Chase, W. H. Greenwood, B. G. Loosli and L. F. Hauglund, Least cost tolerance allocation for mechanical assemblies with automated process selection, Manufacturing Review 3(1), 49 to 59, 1990"
    locator: the whole paper (cost-tolerance models, allocation by Lagrange multipliers for worst-case and statistical stacks, and the choice of one process for each dimension; general locator)
  - book: isbn:9780070181311
    title: Paul J. Drake, Jr. (editor), Dimensioning and Tolerancing Handbook, McGraw-Hill, 1999
    locator: Chapter 14, the chapter by Kenneth W. Chase on minimum-cost tolerance allocation (Lagrange multipliers, the one-way clutch example and process selection)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.5 (geometric programming) and Section 5.5.3 (the KKT conditions are sufficient for convex problems)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A3, problem SP13 (Subset sum), and Section 4.2 (number problems and pseudo-polynomial time)
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: the chapter on the multiple-choice knapsack problem
---

Tolerance allocation, also called tolerance synthesis, is the inverse of tolerance analysis. Analysis takes the part tolerances and computes the variation of an assembly output. Allocation takes a required tolerance of the output and chooses the part tolerances. A tight tolerance costs more to make, so the choice minimizes the total manufacturing cost, given a cost-tolerance curve for each dimension. With a linear stack model and smooth convex costs, it is a convex optimization problem, and for reciprocal costs it has a closed form by [Lagrange multipliers](/lagrange-multiplier/), proved below. When each dimension must be made by one of a few processes, the problem becomes discrete and weakly NP-hard.

## In plain words

An assembly must work, so a gap or an angle must stay inside its limits. That limit sets a budget for the variation of all the parts together. Each part can use some of this budget. A part with a loose tolerance is cheap to make, and a part with a tight tolerance is expensive. The task is to share the budget among the parts so that the total cost is as low as possible. The rule that comes out is simple. A part that is expensive to make precisely gets a larger share. A part that has a large effect on the assembly gets a smaller share. When each part can only be made by one of a few machines, the task becomes a puzzle of choices, and it can be hard in the worst case.

## Definition

**Input.** An assembly output $G$ that depends on part dimensions $x_1, \dots, x_n$, with sensitivities $s_i = \partial G / \partial x_i$ at the nominal design; a required tolerance $T > 0$ of the output; and for each dimension a cost-tolerance function $c_i(T_i)$ that is positive and decreasing in the tolerance $T_i > 0$, optionally with process limits $l_i \le T_i \le u_i$. The sensitivities are the $a_i$ of the [stack-up page](/tolerance-stack-up/); this page writes them as $s_i$ and keeps $a_i$ for cost coefficients.

**Output.** Tolerances $T_1, \dots, T_n$ that minimize the total cost $C(T) = \sum_i c_i(T_i)$ subject to a stack constraint:

- worst case: $\sum_i |s_i| T_i \le T$;
- statistical (RSS): $\sum_i s_i^2 T_i^2 \le T^2$.

The two stack formulas are those of [tolerance stack-up](/tolerance-stack-up/), with their assumptions. They are not repeated here.

**The model of variation.** The output is modeled by its linear stack, $G \approx G_0 + \sum_i s_i \delta_i$. For a linear chain of dimensions this is exact. For an assembly with a nonlinear function, the $s_i$ are the first-order sensitivities at the nominal point, from the [direct linearization method](/direct-linearization-method/) or a torsor model, and the allocation inherits that first-order (small change) approximation. A check by [Monte Carlo tolerance analysis](/monte-carlo-tolerance-analysis/) of the allocated tolerances shows its effect.

**Cost models.** Common forms in the literature are reciprocal powers $c(T) = b + a/T^k$ and exponentials $c(T) = b + a e^{-m T}$, each fitted to data of a process. A constant $b$ does not change the optimal tolerances. All these are convex for $T > 0$ when $a, k, m > 0$.

## Variants

- **Continuous allocation.** The tolerances are real numbers, with or without process limits. With convex costs and either stack, this is a convex problem.
- **Process selection.** Each dimension $i$ must use one of $k_i$ processes, process $j$ with a fixed tolerance $t_{ij}$ and cost $c_{ij}$. Choose one process per dimension to minimize the total cost subject to the stack constraint. This is discrete.
- **Several outputs.** One dimension can appear in several stacks, such as two gaps of one assembly. Each output gives a constraint, and the continuous problem stays convex.
- **Other objectives.** A quality loss term for output variation, a cost of rejected assemblies, or a mean shift term for process drift can be added to the cost or to the stack. These change the formulas below.

## Examples

**The housing gap.** The gap $G = A - B - C - D$ of the [stack-up page](/tolerance-stack-up/) has $s = (1, -1, -1, -1)$. Take reciprocal costs $c_i = a_i / T_i$ with $a = (2, 1, 1, 1)$, so that dimension $A$ is twice as expensive to make precisely, and an RSS requirement $T = 0.15$ mm. The closed form below gives $S = 2^{2/3} + 3 = 4.5874$ and

| allocation | $T_A$ | $T_B = T_C = T_D$ | RSS stack | cost |
|---|---|---|---|---|
| optimal, closed form | $0.08824$ | $0.07003$ | $0.15$ | $65.50$ |
| equal tolerances | $0.075$ | $0.075$ | $0.15$ | $66.67$ |
| scaled from $(0.10, 0.05, 0.05, 0.05)$ | $0.11339$ | $0.05669$ | $0.15$ | $70.55$ |

The optimum is $S^{3/2}/T = 65.50$. The expensive dimension gets the largest tolerance, by the factor $2^{1/3} = 1.26$. The gain over equal tolerances is small here because the costs are similar; the objective is flat near its minimum. For a worst-case requirement $T = 0.25$ mm with the same costs, $T_i \propto \sqrt{a_i / |s_i|}$ gives $T_A = 0.08009$, $T_B = T_C = T_D = 0.05664$ and the cost $(\sum_i \sqrt{a_i |s_i|})^2 / T = (\sqrt2 + 3)^2/0.25 = 77.94$, against $80$ for the tolerances $(0.10, 0.05, 0.05, 0.05)$ of the stack-up page.

**Process selection.** Three dimensions with $s_i = 1$ and a worst-case budget of $0.12$ mm each choose a process, given as (tolerance in mm, cost):

| dimension | process 1 | process 2 | process 3 |
|---|---|---|---|
| 1 | $(0.02, 9)$ | $(0.04, 5)$ | $(0.08, 3)$ |
| 2 | $(0.01, 7)$ | $(0.03, 4)$ | $(0.06, 2)$ |
| 3 | $(0.02, 6)$ | $(0.05, 3)$ | |

Of the 18 choices, 11 meet the budget. The cheapest is $(0.04, 0.03, 0.05)$ at cost $12$, which uses the whole budget. The loosest process of dimension 1 is not in it: with $0.08$ the other two must take $(0.01, 0.02)$, which costs $3 + 7 + 6 = 16$. The dynamic program of the next section finds the same answer.

## Known algorithms

**Closed form for reciprocal costs and an RSS stack.** Let $c_i(T_i) = a_i / T_i$ with $a_i > 0$, let every $s_i \ne 0$, and let there be no process limits. Put $S = \sum_j (a_j |s_j|)^{2/3}$. Then the unique optimum is

$$ T_i = \frac{T}{\sqrt S} \left( \frac{a_i}{s_i^2} \right)^{1/3}, \qquad C^* = \frac{S^{3/2}}{T}. $$

*Derivation by Lagrange multipliers.* The cost decreases in every $T_i$, so at an optimum the constraint is active: otherwise some $T_i$ can grow and the cost falls. The Lagrangian is $\sum_i a_i/T_i + \lambda (\sum_i s_i^2 T_i^2 - T^2)$. Setting its partial derivative to zero gives $-a_i/T_i^2 + 2 \lambda s_i^2 T_i = 0$, so $T_i^3 = a_i / (2 \lambda s_i^2)$ and $T_i = \kappa (a_i / s_i^2)^{1/3}$ for one constant $\kappa > 0$. The active constraint gives $\kappa^2 \sum_i s_i^2 (a_i/s_i^2)^{2/3} = \kappa^2 S = T^2$, so $\kappa = T / \sqrt S$. The cost is $\sum_i a_i / T_i = (\sqrt S / T) \sum_i a_i^{2/3} |s_i|^{2/3} = S^{3/2}/T$.

*Proof that this is the global minimum.* The objective is a sum of the functions $a_i / T_i$, each with second derivative $2 a_i / T_i^3 > 0$, so it is strictly [convex](/convex-function/) on the open orthant $T > 0$. The feasible set, the part of the ellipsoid $\sum_i s_i^2 T_i^2 \le T^2$ in this orthant, is convex, and it has an interior point, so Slater's condition holds. The point above satisfies the [KKT conditions](/kkt-conditions/) with $\lambda = a_i / (2 s_i^2 T_i^3) > 0$, the same value for every $i$, and with an active constraint. For a convex problem the KKT conditions are sufficient (Boyd and Vandenberghe, Section 5.5.3), so the point is a global minimum, and strict convexity makes it the only one. $\blacksquare$

*A direct proof of the bound.* Put $b_i = a_i |s_i|$ and $y_i = |s_i| T_i$, so that $C = \sum_i b_i / y_i$ and the constraint is $\sum_i y_i^2 \le T^2$. Hölder's inequality with exponents $3/2$ and $3$ gives $\sum_i b_i^{2/3} = \sum_i (b_i/y_i)^{2/3}\, y_i^{2/3} \le (\sum_i b_i/y_i)^{2/3} (\sum_i y_i^2)^{1/3}$, that is $S \le C^{2/3} T^{2/3}$. So every feasible allocation costs at least $S^{3/2}/T$, and the closed form reaches the bound. $\blacksquare$

**Other closed forms.** The same steps give these results:

- worst-case stack, $c_i = a_i/T_i$: $T_i = T \sqrt{a_i/|s_i|} / \sum_j \sqrt{a_j |s_j|}$ and $C^* = (\sum_j \sqrt{a_j |s_j|})^2/T$; the bound follows from the Cauchy-Schwarz inequality;
- reciprocal power $c_i = a_i / T_i^k$: $T_i \propto (a_i / s_i^2)^{1/(k+2)}$ for the RSS stack and $T_i \propto (a_i / |s_i|)^{1/(k+1)}$ for the worst case, with the constant fixed by the active constraint.

The RSS optimum never costs more than the worst-case optimum for the same $T$, because $\sum_i s_i^2 T_i^2 \le (\sum_i |s_i| T_i)^2$, so every worst-case feasible allocation is RSS feasible. The RSS allocation accepts that a small fraction of assemblies is out of tolerance under its assumptions.

**Process limits by a search on the multiplier.** With limits $l_i \le T_i \le u_i$, a convex decreasing $c_i$ and the RSS stack, for each $\lambda > 0$ let $T_i(\lambda)$ minimize $c_i(T_i) + \lambda s_i^2 T_i^2$ over $[l_i, u_i]$. For reciprocal costs this is $(a_i / (2 \lambda s_i^2))^{1/3}$ clamped to $[l_i, u_i]$. The sum $g(\lambda) = \sum_i s_i^2 T_i(\lambda)^2$ does not increase in $\lambda$. If $g$ at all upper limits is at most $T^2$, the upper limits are optimal; if $\sum_i s_i^2 l_i^2 > T^2$, no allocation is feasible. Otherwise [bisection](/bisection-method/) on $\lambda$ finds $g(\lambda) = T^2$, and $T(\lambda)$ is optimal, because it minimizes the Lagrangian over the box and meets the constraint with equality, which are the KKT conditions of this convex problem. Each step costs $O(n)$.

**General convex costs.** With posynomial costs, such as sums of reciprocal powers, the problem is a [geometric program](/geometric-programming/): the objective is a posynomial and the constraint $\sum_i (s_i^2/T^2) T_i^2 \le 1$ is a posynomial at most $1$. Other convex costs, such as exponentials, give a smooth convex program. Both are solved to any accuracy by interior point methods (Boyd and Vandenberghe, Section 4.5).

**Process selection by dynamic programming.** If the stack contributions $|s_i| t_{ij}$ are integers in a unit of length, such as micrometres, and the budget is $B$ units, let $F_i(b)$ be the least cost of the first $i$ dimensions with total contribution at most $b$. Then $F_0(b) = 0$ and $F_i(b) = \min_j \{ F_{i-1}(b - |s_i| t_{ij}) + c_{ij} \}$ over the processes that fit. The answer is $F_n(B)$, in $O(B \sum_i k_i)$ time. For the RSS stack, use the squared contributions $s_i^2 t_{ij}^2$ and the budget $T^2$, in units that make them integers. This is the dynamic program of the [knapsack problem](/knapsack-problem/) with one choice from each group, the multiple-choice knapsack problem (Kellerer, Pferschy and Pisinger). Exhaustive search over all $\prod_i k_i$ choices and metaheuristics such as [genetic algorithms](/genetic-algorithm/) and [simulated annealing](/simulated-annealing/) are also used; the metaheuristics give no guarantee of optimality.

## Bounds

- **Continuous, reciprocal costs.** Every feasible allocation costs at least $S^{3/2}/T$ for the RSS stack and $(\sum_j \sqrt{a_j |s_j|})^2/T$ for the worst-case stack, proved above, and the closed forms reach these values in $O(n)$ time. The optimal cost is inversely proportional to the required tolerance $T$.
- **Continuous, convex costs.** Polynomial time to any fixed accuracy, as a convex program.
- **Process selection.** Weakly NP-hard (proved in the next section), and solvable in pseudo-polynomial time $O(B \sum_i k_i)$ by the dynamic program, so it is not strongly NP-hard unless P = NP ([pseudo-polynomial time](/pseudo-polynomial-time/)).

There are no standard benchmark instances for tolerance allocation. The numbers on this page are computed from the formulas, and no measured running times are claimed.

## Reductions

- **Subset sum reduces to process selection.** Given positive integers $w_1, \dots, w_n$ and a target $W$ of the [subset sum problem](/subset-sum-problem/), make one dimension per $w_i$ with $s_i = 1$ and two processes: a fine one with tolerance $1$ and cost $w_i$, and a coarse one with tolerance $w_i + 1$ and cost $0$. Take the worst-case budget $n + W$ and ask for a cost of at most $\sum_i w_i - W$. Let $L$ be the set of dimensions that use the coarse process. The stack is $n + \sum_{i \in L} w_i$, so it fits exactly when $\sum_{i \in L} w_i \le W$. The cost is $\sum_{i \notin L} w_i = \sum_i w_i - \sum_{i \in L} w_i$, so it is small enough exactly when $\sum_{i \in L} w_i \ge W$. Both hold exactly when $L$ is a subset with sum $W$. The construction takes polynomial time, and subset sum is NP-complete (Garey and Johnson, problem SP13), so the decision version of process selection is NP-hard. $\blacksquare$
- **Process selection reduces to multiple-choice knapsack.** The stack contributions are the weights, the budget is the capacity, and the costs, with signs changed, are the values; one item is chosen from each group.
- **Continuous allocation reduces to convex programming,** and for posynomial costs to [geometric programming](/geometric-programming/).
- **Allocation uses analysis.** The sensitivities come from tolerance analysis, by the stack-up chain or the [direct linearization method](/direct-linearization-method/), and the allocated tolerances can be checked by [Monte Carlo analysis](/monte-carlo-tolerance-analysis/).

## Applications

Tolerance allocation is used in the design of mechanical assemblies to set the tolerances on part drawings before production, and to choose among machining processes for each feature. It shows which dimensions carry the most cost per unit of output variation, which guides redesign: a dimension with a large sensitivity and a costly process is a candidate for a change of the design. The handbook chapter by Chase works the method on the one-way clutch of the [DLM page](/direct-linearization-method/).

## References
