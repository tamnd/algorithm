---
tag: HH5D7N
kind: concept
slug: slack-variables
name: Slack variables
aliases:
- slack form
- slack variable
- surplus variable
area: optimization/linear-programming
level: intro
summary: Extra variables that turn inequalities into equalities for the simplex method.
prereqs: [lp-standard-form]
see_also: [lp-slack-form, basic-feasible-solution, complementary-slackness, simplex-method, initial-basic-feasible-solution, two-phase-simplex-method]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.1, Standard and slack forms (the slack variable of each inequality and the conversion to slack form)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 2, How the simplex method works (slack variables and the first dictionary)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 1.1 (slack and surplus variables in the reduction to standard form)
---

A slack variable is a new nonnegative variable $s$ that measures how far an inequality $a^\top x \le \beta$ is from being tight: $s = \beta - a^\top x$. With one slack per row, the system $Ax \le b$ becomes the system of equations $Ax + s = b$ with $s \ge 0$, which is the shape the [simplex method](/simplex-method/) works on. A slack of zero means the constraint is tight, and a positive slack means a resource is left over. The slacks also give the first [basis](/basic-feasible-solution/) of the simplex method, and they pair with the dual variables in [complementary slackness](/complementary-slackness/).

## In plain words

A limit such as "use at most four hours of machine time" is an inequality. You can turn it into an exact equation by adding a new quantity: the hours you do not use. Used hours plus unused hours equal four, and unused hours cannot be negative. This new quantity is the slack.

Equations are easier for algorithms than inequalities, so this trick is the first step of the simplex method. The slack also tells you something useful at the end. If a resource has slack left at the best plan, more of that resource is worth nothing. If its slack is zero, the resource is a bottleneck, and more of it can help.

## The idea

**Definition.** For an inequality $a_i^\top x \le b_i$, the slack variable is $s_i = b_i - a_i^\top x$, and the inequality holds exactly when $s_i \ge 0$. For an inequality $a_i^\top x \ge b_i$, the *surplus* variable $s_i = a_i^\top x - b_i \ge 0$ plays the same role. So, with $I_m$ the identity matrix,

$$\{x : Ax \le b,\ x \ge 0\} \;=\; \Big\{x : \text{there is } s \text{ with } \begin{pmatrix} A & I_m \end{pmatrix} \begin{pmatrix} x \\ s \end{pmatrix} = b,\ x \ge 0,\ s \ge 0\Big\},$$

and the map $x \mapsto (x, b - Ax)$ is a bijection between the two feasible sets that keeps the objective $c^\top x$. This is one rule of the conversion to [standard form](/lp-standard-form/).

**Geometry.** The slack $s_i$ is a scaled distance: the point $x$ lies at Euclidean distance $s_i / \lVert a_i \rVert$ from the hyperplane $a_i^\top x = b_i$, on the feasible side when $s_i \ge 0$. A constraint is *tight* (or *active*, or *binding*) at $x$ when $s_i = 0$.

**Vertices and zeros.** In the space of the $n + m$ variables $(x, s)$, every constraint of $\{Ax \le b, x \ge 0\}$ is a sign condition: either $x_j \ge 0$ or $s_i \ge 0$. A point is a vertex when the constraints that are tight there have rank $n$, so at a vertex at least $n$ of the $n + m$ variables are zero. When exactly $n$ are zero, the vertex is *nondegenerate*, and the $m$ nonzero ones are the basic variables of a [basic feasible solution](/basic-feasible-solution/).

**The first basis.** The columns of the slacks form the identity matrix, so the slacks are always a basis of $\begin{pmatrix} A & I_m \end{pmatrix}$. The basic solution of this basis is $x = 0$, $s = b$. It is feasible exactly when $b \ge 0$. Then the simplex method can start at once from the [slack form](/lp-slack-form/) with the slacks as basic variables. When some $b_i < 0$, the origin is not feasible, and the method first needs an [initial basic feasible solution](/initial-basic-feasible-solution/), for example by the [two-phase method](/two-phase-simplex-method/) or the [big-M method](/big-m-method/), which add *artificial* variables. An artificial variable is not a slack: it has no meaning in the problem and must reach zero in a feasible solution.

**Slacks and duals.** For the pair $\max c^\top x$, $Ax \le b$, $x \ge 0$ and $\min b^\top y$, $A^\top y \ge c$, $y \ge 0$, the primal slack $s_i$ pairs with the dual variable $y_i$, and the dual surplus $t_j = (A^\top y - c)_j$ pairs with $x_j$. A feasible pair is optimal exactly when $s_i y_i = 0$ for all $i$ and $t_j x_j = 0$ for all $j$. This is [complementary slackness](/complementary-slackness/), and the name comes from these slacks.

## Examples

**The running example.** The program $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$ gets three slacks:

$$x_1 + x_2 + s_1 = 4, \qquad x_1 + 3x_2 + s_2 = 9, \qquad x_1 + s_3 = 3, \qquad x, s \ge 0.$$

At each of the five vertices, exactly two of the five variables are zero, so no vertex is degenerate:

| vertex $(x_1, x_2)$ | $(s_1, s_2, s_3)$ | zero variables | $3x_1 + 2x_2$ |
|---|---|---|---|
| $(0, 0)$ | $(4, 9, 3)$ | $x_1, x_2$ | 0 |
| $(3, 0)$ | $(1, 6, 0)$ | $x_2, s_3$ | 9 |
| $(3, 1)$ | $(0, 3, 0)$ | $s_1, s_3$ | 11 |
| $(3/2, 5/2)$ | $(0, 0, 3/2)$ | $s_1, s_2$ | 19/2 |
| $(0, 3)$ | $(1, 0, 3)$ | $x_1, s_2$ | 6 |

At the optimum $(3, 1)$, the second resource has 3 units left, and its optimal dual value, its [shadow price](/shadow-price/), is 0. The first and the third resources are used up, and their shadow prices are 2 and 1.

**A surplus.** The constraint $2x_1 + x_2 \ge 5$ becomes $2x_1 + x_2 - s = 5$ with $s \ge 0$. At $x = (2, 3)$ the surplus is $s = 2$.

**A degenerate vertex.** Replace the second constraint of the running example by $x_1 + 3x_2 \le 6$. At $(3, 1)$ the slacks are $(0, 0, 0)$, so three variables are zero although the dimension is 2. Three different bases describe this one vertex, and the simplex method may [pivot](/pivot-operation/) between them without moving; see [degeneracy](/lp-degeneracy/).

**The origin is infeasible.** For $x_1 + x_2 \ge 1$, written as $-x_1 - x_2 \le -1$, the slack basis gives $s = -1 < 0$. The slack basis is not feasible, and a phase one is needed.

**Not a slack in this sense.** In a soft-margin [support vector machine](/support-vector-machine/), the variables $\xi_i \ge 0$ in $y_i (w^\top x_i + b) \ge 1 - \xi_i$ are also called slacks. They are different: they appear in the objective with a positive cost, so they relax the constraint at a price instead of only rewriting it.

## Where it is used

- [Slack form](/lp-slack-form/) and the [simplex method](/simplex-method/): the slacks are the first basic variables.
- [Standard form](/lp-standard-form/): one of the conversion rules.
- [Complementary slackness](/complementary-slackness/) and [shadow prices](/shadow-price/): a positive slack forces a zero dual value.
- [Interior point methods](/interior-point-method/): the barrier term $-\sum_i \log s_i$ keeps every slack positive along the [central path](/central-path/).
- [Sensitivity analysis](/lp-sensitivity-analysis/): a change of $b_i$ that is smaller than the slack $s_i$ of a non-tight row does not change the optimal solution.

## References
