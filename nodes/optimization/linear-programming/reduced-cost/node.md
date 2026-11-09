---
tag: BGBD8R
kind: concept
slug: reduced-cost
name: Reduced costs
aliases:
- reduced cost coefficients
- reduced cost
- relative cost
- simplex multipliers
area: optimization/linear-programming
level: core
summary: Objective coefficients after eliminating basic variables; their signs test optimality and choose entering variables.
prereqs: [basic-feasible-solution, dual-linear-program]
see_also: [simplex-method, dantzig-pivot-rule, shadow-price, complementary-slackness, lp-sensitivity-analysis, column-generation, potential-function-reduced-costs, lp-degeneracy]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.1, Optimality conditions (Definition 3.2, reduced cost, and Theorem 3.1, the optimality test), and Section 4.2 (reduced costs as dual slacks)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 2, How the simplex method works (the coefficients of the objective row of a dictionary)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 5, The simplex method (the last row of the tableau and the optimality test)
---

The reduced cost of a variable, for a given basis of a linear program, is the rate at which the objective changes when that variable is raised from zero and the basic variables adjust to keep the equations true. It is the coefficient of the variable in the objective row of the [slack form](/lp-slack-form/) for that basis. If no reduced cost has the improving sign, the [basic feasible solution](/basic-feasible-solution/) is optimal; otherwise a variable with an improving reduced cost can enter the basis, which is the step of the [simplex method](/simplex-method/). In the language of duality, the reduced costs are the slacks of the [dual](/dual-linear-program/) constraints at the price vector of the basis.

## In plain words

At a corner of the allowed region, some variables are zero and the others are fixed by the equations. Ask, for each zero variable: if I raise it a little and let the others follow, how much does the cost change for each unit? That rate is its reduced cost. A negative rate, in a problem where you want low cost, means that this variable is worth bringing in. If every rate is zero or positive, no single move helps, and the corner is the best one. The same numbers also say how much a variable's own cost must fall before it becomes worth using.

## The idea

**Setting.** $\min c^\top x$ subject to $Ax = b$, $x \ge 0$, with $A \in \mathbb{R}^{m \times n}$ of rank $m$. Let $B$ be a basis, $A_B$ its columns, and $N$ the other indices.

**Definition.** The *simplex multipliers* of $B$ are $y^\top = c_B^\top A_B^{-1}$, the solution of $A_B^\top y = c_B$. The *reduced cost* of variable $j$ is

$$\bar c_j = c_j - y^\top A_j = c_j - c_B^\top A_B^{-1} A_j.$$

For $j \in B$, $\bar c_j = 0$. The vector $\bar c^\top = c^\top - y^\top A$ is the objective with the basic variables eliminated: for every $x$ with $Ax = b$,

$$c^\top x = y^\top A x + \bar c^\top x = y^\top b + \sum_{j \in N} \bar c_j x_j.$$

So $\bar c_N$ is the objective row of the slack form of $B$, and $y^\top b = c_B^\top x_B$ is the value of the basic solution.

**The rate of change.** Raise a nonbasic $x_j$ to $\theta$ and keep the other nonbasic variables at 0. The equations force $x_B = A_B^{-1} b - \theta A_B^{-1} A_j$, so the point moves along the direction $d$ with $d_j = 1$, $d_B = -A_B^{-1} A_j$, and $d_k = 0$ for the other $k \in N$. The objective changes at the rate $c^\top d = c_j - c_B^\top A_B^{-1} A_j = \bar c_j$.

**The optimality test.** Let $x$ be the basic feasible solution of $B$.

1. If $\bar c \ge 0$, then $x$ is optimal.
2. If $x$ is nondegenerate and $\bar c_j < 0$ for some $j$, then $x$ is not optimal.

*Proof.* (1) For every feasible $x'$, the identity above gives $c^\top x' = y^\top b + \bar c^\top x' \ge y^\top b = c^\top x$, because $\bar c \ge 0$ and $x' \ge 0$. (2) Nondegenerate means $x_B > 0$, so a small $\theta > 0$ keeps $x + \theta d \ge 0$, and the value drops by $\theta |\bar c_j|$. $\square$

At a degenerate vertex the converse of (1) can fail: the vertex can be optimal while the basis that describes it has a negative reduced cost. The example below shows this.

**The dual view.** The condition $\bar c \ge 0$ is $A^\top y \le c$, which says that $y$ is feasible for the dual $\max b^\top y$, $A^\top y \le c$. So $\bar c_j$ is the slack of dual constraint $j$, and the test says: a basis is optimal when its multipliers are dual feasible. The products $x_j \bar c_j$ are always zero for a basic solution ($x_j = 0$ off $B$, $\bar c_j = 0$ on $B$), which is [complementary slackness](/complementary-slackness/). At an optimal basis, $y$ is the vector of [shadow prices](/shadow-price/).

**Sign conventions.** For a maximization, the improving sign is positive, and a basis is optimal when all reduced costs are at most zero. The slack form of CLRS writes $z = v + \sum_{j \in N} c_j x_j$ for a maximization, so its $c_j$ are the reduced costs with this sign.

## Examples

**The running example.** $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$ becomes, with slacks $s_1, s_2, s_3$, the minimization of $c^\top x$ with $c = (-3, -2, 0, 0, 0)$. The reduced costs $(\bar c_{x_1}, \bar c_{x_2}, \bar c_{s_1}, \bar c_{s_2}, \bar c_{s_3})$ of the five feasible bases:

| basis | vertex | $y$ | reduced costs | verdict |
|---|---|---|---|---|
| $s_1, s_2, s_3$ | $(0, 0)$ | $(0, 0, 0)$ | $(-3, -2, 0, 0, 0)$ | not optimal; $x_1$ or $x_2$ can enter |
| $x_1, s_1, s_2$ | $(3, 0)$ | $(0, 0, -3)$ | $(0, -2, 0, 0, 3)$ | not optimal; $x_2$ enters |
| $x_2, s_1, s_3$ | $(0, 3)$ | $(0, -2/3, 0)$ | $(-7/3, 0, 0, 2/3, 0)$ | not optimal; $x_1$ enters |
| $x_1, x_2, s_3$ | $(3/2, 5/2)$ | $(-7/2, 1/2, 0)$ | $(0, 0, 7/2, -1/2, 0)$ | not optimal; $s_2$ enters |
| $x_1, x_2, s_2$ | $(3, 1)$ | $(-2, 0, -1)$ | $(0, 0, 2, 0, 1)$ | optimal |

At the optimal basis, $c^\top x = y^\top b + 2 s_1 + s_3 = -11 + 2 s_1 + s_3$. With the sign of the maximization this is $z = 11 - 2 s_1 - s_3$, the last slack form on the [slack form](/lp-slack-form/) page. The reduced cost $-1/2$ of $s_2$ at $(3/2, 5/2)$ says that raising $s_2$, that is, leaving the line of the second row along the line of the first, moves the point toward $(3, 1)$ and gains $1/2$ per unit of $s_2$: from 19/2 at $s_2 = 0$ to 11 at $s_2 = 3$.

**A degenerate optimal vertex with a negative reduced cost.** Change the second row to $x_1 + 3x_2 \le 6$. The optimum $(3, 1)$ now has $s_1 = s_2 = s_3 = 0$, and the three bases $\{x_1, x_2, s_i\}$ all describe it. For $\{x_1, x_2, s_3\}$ the multipliers are $y = (-7/2, 1/2, 0)$, and the reduced cost of $s_2$ is $-1/2 < 0$, although the vertex is optimal. Raising $s_2$ would need $s_3$ to drop below zero, so the step has length 0. A pivot to $\{x_1, x_2, s_2\}$ gives $y = (-2, 0, -1)$ and reduced costs $(0, 0, 2, 0, 1) \ge 0$, which proves optimality.

**Network flows.** In a minimum cost flow problem, the multipliers are node potentials $\pi$, and the reduced cost of arc $(u, v)$ is $c_{uv} - \pi_u + \pi_v$; see [reduced costs with potentials](/potential-function-reduced-costs/). A flow is optimal when no arc of the [residual graph](/residual-graph/) has negative reduced cost.

## Where it is used

- [Simplex method](/simplex-method/): the optimality test, and the choice of the entering variable. The [Dantzig rule](/dantzig-pivot-rule/) picks the most negative reduced cost, and the [steepest edge rule](/steepest-edge-pivot-rule/) scales it by the length of the edge.
- [Revised simplex method](/revised-simplex-method/): it computes $y$ once per iteration and then each $\bar c_j$ by one inner product, which is called *pricing*.
- [Column generation](/column-generation/): the pricing problem looks for a column with negative reduced cost among very many columns, without listing them.
- [Sensitivity analysis](/lp-sensitivity-analysis/): the basis stays optimal while a change in $c$ keeps all reduced costs nonnegative, and a nonbasic $x_j$ enters only after $c_j$ falls by $\bar c_j$.
- [Branch and bound](/land-doig-algorithm/): reduced cost fixing. If $\bar c_j$ exceeds the gap between the LP bound and the best known integer solution, $x_j$ can be fixed at its bound.
- Network algorithms: [network simplex](/network-simplex/), [successive shortest paths](/successive-shortest-path/) and the [Hungarian algorithm](/hungarian-algorithm/) work with reduced costs of arcs.

## References
