---
tag: 3338AZ
kind: problem
slug: parametric-query-optimization
name: Parametric query optimization
aliases:
- PQO
area: databases/query-planning
level: advanced
summary: "Given a query whose cost depends on parameters unknown at compile time, find a set of plans and a rule that picks, for each parameter value, a plan that is optimal for it."
prereqs: [query-optimization, cost-model, convex-set]
see_also: [mid-query-reoptimization, selinger-join-enumeration, parametric-linear-programming, half-plane-intersection, polyhedron, cardinality-estimation, eddies, join-ordering]
sources:
  - paper: "Yannis E. Ioannidis, Raymond T. Ng, Kyuseok Shim and Timos K. Sellis, Parametric query optimization, Proceedings of VLDB 1992, 103 to 114"
    title: Parametric query optimization
    locator: the statement of the problem, with parameters such as the size of the buffer memory, and randomized search methods that find plans for many parameter values at once
  - paper: doi:10.1007/s007780050037
    title: Yannis E. Ioannidis, Raymond T. Ng, Kyuseok Shim and Timos K. Sellis, Parametric query optimization, The VLDB Journal 6(2) (1997), 132 to 151
    locator: the journal version of the 1992 paper
  - paper: doi:10.1145/67544.66960
    title: Goetz Graefe and Karen Ward, Dynamic query evaluation plans, Proceedings of ACM SIGMOD 1989, 358 to 366
    locator: the choose-plan operator, which keeps several subplans whose costs cannot be compared at compile time and picks one when the query starts
  - paper: doi:10.1145/191843.191872
    title: Richard L. Cole and Goetz Graefe, Optimization of dynamic query evaluation plans, Proceedings of ACM SIGMOD 1994
    locator: the optimization of plans with choose-plan operators when costs are intervals, in the Volcano optimizer generator
---

Parametric query optimization asks for the best plan of a query not at one point but over a whole range of values of some parameters that are unknown when the query is compiled. Typical parameters are the selectivity of a predicate with a host variable, the size of a relation, or the memory the query will get. The answer is a set of plans and a rule that, given the actual values at run time, picks a plan that is optimal for them. Yannis E. Ioannidis, Raymond T. Ng, Kyuseok Shim and Timos K. Sellis named the problem in 1992. Goetz Graefe and Karen Ward had given dynamic plans in 1989, where a choose-plan operator keeps the alternatives in the plan. When each plan cost is a linear function of the parameters, the region where a plan is optimal is convex, which this page proves; with piecewise linear costs, this is not true in general.

## In plain words

A query can be compiled once and run many times with different values, for example "the orders of customer number ?". For one customer the query returns three rows, and for another it returns a million. The best plan for three rows is not the best for a million.

Normal optimization picks one plan for one guess of the values. Parametric optimization finds, before the query runs, a small set of plans and a map that says which plan is best for which values. At run time, the database looks at the real values, finds them on the map and runs that plan, with no new optimization.

The work is to find all plans that are best somewhere, and the borders between them, without optimizing again for every possible value.

## Definition

**Input.** A query $Q$, a parameter space $\Theta \subseteq \mathbb{R}^d$ (for example $[0, 1]^d$ for $d$ selectivities), the set $\mathcal{P}$ of plans for $Q$, and a cost function $c(P, \theta)$ for each plan $P \in \mathcal{P}$ and parameter value $\theta \in \Theta$.

**Output.** A set $S \subseteq \mathcal{P}$ and a map $\pi : \Theta \to S$ such that $c(\pi(\theta), \theta) = \min_{P \in \mathcal{P}} c(P, \theta)$ for every $\theta \in \Theta$. A set $S$ with this property is a parametric optimal set of plans. The region of $P$ is $R_P = \{\theta \in \Theta : c(P, \theta) \le c(P', \theta) \text{ for all } P' \in \mathcal{P}\}$, and the regions of the plans in $S$ cover $\Theta$.

**Goal.** Make $S$ small and the map fast to evaluate, and find them with far fewer calls to the optimizer than there are points in $\Theta$.

## Variants

- **Linear costs.** Each cost has the form $c(P, \theta) = a_P + b_P \cdot \theta$. This holds, for example, when $\theta$ is the selectivity of one predicate and the rest of the plan is fixed.
- **Piecewise linear or nonlinear costs.** Costs change slope where an input stops fitting in memory, and products of selectivities make costs nonlinear in several parameters.
- **Approximate PQO.** Accept a plan whose cost is at most $(1 + \epsilon)$ times the optimum at each $\theta$. This can make $S$ much smaller.
- **Dynamic plans.** Keep the choice inside the plan as choose-plan operators, decided when the query starts (Graefe and Ward, 1989).
- **Discrete parameters.** The memory size or the number of available processors can take only a few values; then PQO is a separate optimization for each value, with shared work.

## Examples

**One parameter, three plans.** Let $s \in [0, 1]$ be the selectivity of a predicate with a host variable, and let the optimizer have three plans with linear costs.

| plan | cost |
|---|---|
| $P_1$: index scan and [index nested loop join](/index-nested-loop-join/) | $100 + 40{,}000 s$ |
| $P_2$: full scan and [hash join](/hash-join/) | $12{,}000 + 2000 s$ |
| $P_3$: full scan and sort-merge join | $13{,}000 + 200 s$ |

$P_1$ and $P_2$ cost the same at $s = 11{,}900/38{,}000 \approx 0.3132$, and $P_2$ and $P_3$ at $s = 1000/1800 \approx 0.5556$. $P_1$ and $P_3$ cost the same at $s = 12{,}900/39{,}800 \approx 0.3241$, which is inside the region of $P_2$, so it is not a border. The answer is $S = \{P_1, P_2, P_3\}$ with the regions $[0, 0.3132]$, $[0.3132, 0.5556]$ and $[0.5556, 1]$. A system that compiled the query for $s = 0.01$ and kept $P_1$ would pay 36,100 at $s = 0.9$, where $P_3$ costs 13,180.

**Piecewise linear costs give a region that is not convex.** Plan $X$ is an index nested loop join with cost $2000 + 10{,}000 s$. Plan $Y$ is a hash join whose build input fits in memory up to $s = 0.5$ and spills to disk after that, with cost $2500 + 1000 s$ for $s \le 0.5$ and $3000 + 40{,}000(s - 0.5)$ for $s > 0.5$. Both costs grow with $s$. $X$ is cheaper when $9000 s \le 500$, that is $s \le 1/18 \approx 0.056$, and again when $3000 + 40{,}000(s - 0.5) \ge 2000 + 10{,}000 s$, that is $s \ge 19/30 \approx 0.633$. At $s = 0.5$, $Y$ costs 3000 and $X$ costs 7000. So the region of $X$ is $[0, 1/18] \cup [19/30, 1]$, which is not convex. This corrects the claim that piecewise linear costs give convex regions; the claim holds for linear costs, below.

## Known algorithms

- **Optimize at sample points.** Run the normal optimizer at the points of a grid over $\Theta$ and keep the plans found. This is simple, but it can miss a plan whose region falls between the grid points, so it gives no guarantee.
- **Randomized search for many values at once.** Ioannidis et al. (1992) used randomized search methods, such as iterative improvement and simulated annealing, and shared the work between the searches for different parameter values.
- **Choose-plan operators.** Graefe and Ward (1989) keep two subplans in the plan when their costs cannot be compared at compile time, under a choose-plan operator that evaluates the costs when the query starts. Cole and Graefe (1994) optimized such plans with costs given as intervals.
- **Linear costs, one parameter.** If the optimizer can return all plans that are optimal at some $s$, the regions are the pieces of the lower envelope of the lines $a_P + b_P s$. Sort the lines by slope and keep the lines of the envelope with a stack, as in [half-plane intersection](/half-plane-intersection/); for $m$ lines this costs $O(m \log m)$ time.
- **Linear costs, vertex checks.** By the convexity theorem below, if the same plan is optimal at all vertices of a convex polytope $T \subseteq \Theta$, it is optimal on all of $T$. So an algorithm can optimize at the vertices of $\Theta$, stop where they agree, and split $\Theta$ where they do not. Later work by Ganguly (1998) and by Hulgeri and Sudarshan (2002) built PQO algorithms on this idea for linear and piecewise linear costs.

## Bounds

**Linear costs give convex regions (proved).** If $\Theta$ is convex and every cost is linear, $c(P, \theta) = a_P + b_P \cdot \theta$, then every region $R_P$ is a convex set, and a [polyhedron](/polyhedron/) if $\Theta$ is one.

*Proof.* For each other plan $P'$, the set $\{\theta : a_P + b_P \cdot \theta \le a_{P'} + b_{P'} \cdot \theta\}$ is $\{\theta : (b_P - b_{P'}) \cdot \theta \le a_{P'} - a_P\}$, a closed half-space (or all of $\mathbb{R}^d$, or the empty set). So $R_P$ is the intersection of $\Theta$ with finitely many half-spaces, and an intersection of [convex sets](/convex-set/) is convex. $\square$

Two consequences follow. Each plan of $S$ has one connected region, so in one dimension the range $[0, 1]$ splits into at most $|S|$ intervals. And the optimal cost $\theta \mapsto \min_P c(P, \theta)$ is the minimum of linear functions, so it is concave and piecewise linear.

**Hardness.** For a single parameter value, PQO is normal query optimization, which contains [join ordering](/join-ordering/), NP-hard in general. So PQO is at least as hard. The size of $S$ depends on the query and the cost model; for nonlinear costs, a plan can be optimal on many separate pieces of $\Theta$, as the example shows.

## Reductions

- **From query optimization.** Normal optimization is PQO with $|\Theta| = 1$.
- **To a lower envelope.** With linear costs over a known set of candidate plans, PQO is the computation of the lower envelope of $m$ hyperplanes in $\mathbb{R}^{d+1}$, which is the upper boundary of the intersection of the $m$ half-spaces below them.
- **To parametric linear programming.** When the costs come from a linear program whose objective depends on $\theta$, the regions of the optimal bases are the regions of [parametric linear programming](/parametric-linear-programming/), and they are convex for the same reason.

## Applications

- **Prepared statements and stored procedures.** The query is compiled once with host variables, and the plan is picked per call, so each call gets a good plan without a full optimization.
- **Unknown memory or load.** The memory a query gets and the number of processors are known only when the query starts.
- **Plan caching.** A database can cache the set $S$ and the map for a frequent query, in place of one plan that is bad for some values.
- **A step toward run-time adaptivity.** When the true values are still not known at start-up, [mid-query re-optimization](/mid-query-reoptimization/) checks them during the run, and [eddies](/eddies/) change the plan for each tuple.

## References
