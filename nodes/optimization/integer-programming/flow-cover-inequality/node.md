---
tag: T195G0
kind: concept
slug: flow-cover-inequality
name: Flow cover inequality
aliases:
- flow cover cut
- lifted flow cover inequality
area: optimization/integer-programming
level: research
summary: Cover-type cut for fixed-charge network flow structures.
prereqs: [cover-inequality, big-m-formulation, mixed-integer-programming]
see_also: [cover-inequality, mixed-integer-rounding-inequality, big-m-formulation, indicator-constraint, facility-location-problem, min-cost-flow-problem, branch-and-cut, cutting-plane-method-integer-programming]
sources:
  - paper: "Manfred W. Padberg, Tony J. Van Roy and Laurence A. Wolsey, Valid linear inequalities for fixed charge problems, Operations Research 33 (1985), 842 to 861"
    locator: flow cover inequalities for the single-node fixed-charge flow set and the facet conditions
  - paper: "Tony J. Van Roy and Laurence A. Wolsey, Valid inequalities for mixed 0-1 programs, Discrete Applied Mathematics 14 (1986), 199 to 213"
    locator: the generalized flow cover inequality with inflow and outflow arcs
  - paper: "Tony J. Van Roy and Laurence A. Wolsey, Solving mixed integer programming problems using automatic reformulation, Operations Research 35 (1987), 45 to 57"
    locator: automatic separation of flow covers in a general MIP code
  - paper: "Zonghao Gu, George L. Nemhauser and Martin W. P. Savelsbergh, Lifted flow cover inequalities for mixed 0-1 integer programs, Mathematical Programming 85 (1999), 439 to 467"
    locator: lifting of flow cover inequalities and computational results
  - paper: "Hugues Marchand and Laurence A. Wolsey, Aggregation and mixed integer rounding to solve MIPs, Operations Research 49 (2001), 363 to 371"
    locator: flow covers obtained as MIR cuts of aggregated rows
  - book: isbn:9780471828198
    title: George L. Nemhauser and Laurence A. Wolsey, Integer and Combinatorial Optimization, Wiley, 1988
    locator: Part II, the section on the single-node fixed-charge flow model
---

A flow cover inequality is a valid inequality for a set of arcs into one node, where each arc can carry flow only if a binary variable opens it. It is the mixed-integer version of the knapsack [cover inequality](/cover-inequality/): a set of arcs whose capacities add up to more than the demand is a *flow cover*, and the inequality says how much flow these arcs can carry when some of them are closed. Padberg, Van Roy and Wolsey (1985) introduced it for fixed-charge problems. It is one of the main cuts for network design, lot sizing and facility location models, and MIP solvers separate it on any row with variable upper bounds.

## In plain words

A warehouse can receive at most 10 units. Three suppliers can send at most 6, 5 and 4 units, and each supplier must be paid a fixed fee to be used at all. In the relaxed problem, the solver can open a supplier "four fifths" of the way and still let it send 4 units. That makes the fixed fee look cheaper than it is.

Take suppliers 1 and 2. Together they can send 11 units, which is 1 more than the warehouse takes. If supplier 1 is closed, supplier 2 alone sends at most 5. If supplier 2 is closed, supplier 1 sends at most 6. The flow cover inequality puts these facts into one linear rule. It removes the fractional answer, and it keeps every answer where each supplier is fully open or fully closed.

## The idea

**The single-node flow set.** Let $N = N_1 \cup N_2$, where $N_1$ holds the inflow arcs and $N_2$ the outflow arcs of a node, and let

$$X = \Big\{(x, y) \in \mathbb{R}^N_+ \times \{0,1\}^N : \sum_{j \in N_1} x_j - \sum_{j \in N_2} x_j \le b,\ \ x_j \le u_j y_j \ (j \in N)\Big\},$$

with capacities $u_j > 0$. The constraints $x_j \le u_j y_j$ are [big-M](/big-m-formulation/) links between the flow and the switch. Many MIP rows can be brought into this form by aggregation and bound substitution.

**The flow cover inequality, inflows only.** Let $N_2 = \emptyset$. A set $C \subseteq N_1$ is a *flow cover* if $\lambda = \sum_{j \in C} u_j - b > 0$. Then

$$\sum_{j \in C} x_j + \sum_{j \in C} (u_j - \lambda)^+ (1 - y_j) \le b$$

is valid for $X$, where $t^+ = \max(t, 0)$.

*Proof.* Fix a feasible $(x, y)$ and let $T = \{j \in C : y_j = 0\}$, so $x_j = 0$ for $j \in T$. If $T = \emptyset$, the inequality reads $\sum_{C} x_j \le b$, which holds. Otherwise,

$$\sum_{j \in C} x_j \le \min\Big(b,\ \sum_{j \in C \setminus T} u_j\Big) = b - \Big(\sum_{j \in T} u_j - \lambda\Big)^+.$$

Let $T' = \{j \in T : u_j > \lambda\}$. If $T' \ne \emptyset$, then $\sum_{j \in T} (u_j - \lambda)^+ = \sum_{j \in T'} u_j - |T'| \lambda \le \sum_{j \in T} u_j - \lambda$. So in all cases $\sum_{j \in T}(u_j - \lambda)^+ \le (\sum_{j \in T} u_j - \lambda)^+$, and adding this to the bound above gives the inequality. $\square$

When exactly one arc $k \in C$ is closed, the inequality says $\sum_{C \setminus k} x_j \le b - (u_k - \lambda)^+ = \min(b, \sum_{C \setminus k} u_j)$, which is the true limit. Padberg, Van Roy and Wolsey (1985) showed that it defines a facet of $\operatorname{conv}(X)$ when $\max_{j \in C} u_j > \lambda$.

**The general form.** For $C_1 \subseteq N_1$ and $C_2 \subseteq N_2$ with $\lambda = \sum_{C_1} u_j - \sum_{C_2} u_j - b > 0$, and any $L_2 \subseteq N_2 \setminus C_2$, the inequality

$$\sum_{j \in C_1} x_j + \sum_{j \in C_1} (u_j - \lambda)^+ (1 - y_j) \le b + \sum_{j \in C_2} u_j + \lambda \sum_{j \in L_2} y_j + \sum_{j \in N_2 \setminus (C_2 \cup L_2)} x_j$$

is valid (Van Roy and Wolsey, 1986). Outflow arcs in $C_2$ are treated as always open, and an outflow arc in $L_2$ can add at most $\lambda$ of extra room when it opens.

**Separation and lifting.** Finding the most violated flow cover is a knapsack-type problem, so solvers use heuristics: they pick $C$ from the arcs with large $x^*_j$ and $y^*_j$ close to 1. Variables outside $C$ can be lifted into the inequality, as for knapsack covers (Gu, Nemhauser and Savelsbergh, 1999). Marchand and Wolsey (2001) showed that flow covers also come out of the [MIR](/mixed-integer-rounding-inequality/) procedure applied to the aggregated row with the right divisor, and many solvers generate them that way.

## Examples

Take $x_1 + x_2 + x_3 \le 10$ with $x_j \le u_j y_j$, $u = (6, 5, 4)$, $x \ge 0$ and $y \in \{0,1\}^3$.

- **Cover $C = \{1, 2\}$.** Here $\lambda = 11 - 10 = 1$, and the inequality is
$$x_1 + x_2 + 5(1 - y_1) + 4(1 - y_2) \le 10.$$
With $y_1 = 0$ it says $x_2 \le 5$, and with $y_2 = 0$ it says $x_1 \le 6$. The LP point $x = (6, 4, 0)$, $y = (1, \tfrac45, 0)$ satisfies all the original constraints, since $x_2 = 4 = 5 \cdot \tfrac45$, but the left side is $10 + \tfrac45 > 10$. So the cut removes it.
- **Cover $C = \{1, 2, 3\}$.** Here $\lambda = 5$, so only arc 1 has $u_j > \lambda$, and the inequality is $x_1 + x_2 + x_3 + (1 - y_1) \le 10$. If arc 1 is closed, arcs 2 and 3 carry at most 9 units.
- **Facets.** Both inequalities have six affinely independent tight points in $X$, and $\operatorname{conv}(X)$ is 6-dimensional, so both define facets.

## Where it is used

- **Fixed-charge network design.** Each node balance row with arc switches gives a single-node flow set. Flow covers strengthen the weak big-M links, which otherwise let the LP pay a small part of each fixed cost.
- **Lot sizing.** In capacitated lot sizing, the setup variables switch production on, and flow covers on the stock balance rows close much of the gap.
- **[Facility location](/facility-location-problem/).** Capacity rows of capacitated facility location models have the same structure.
- **General MIP solvers.** Since Van Roy and Wolsey (1987), solvers find single-node flow sets automatically in any row with variable upper bounds and separate flow covers there, today mostly through the c-MIR routine.

## References
