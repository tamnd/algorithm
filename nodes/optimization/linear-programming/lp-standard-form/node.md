---
tag: EX9JNH
kind: definition
slug: lp-standard-form
name: Standard form of a linear program
aliases:
- canonical form
- standard form LP
- equational form
- inequality form
area: optimization/linear-programming
level: intro
summary: Maximize c·x subject to Ax ≤ b and x ≥ 0, or minimize c·x subject to Ax = b and x ≥ 0; every LP converts to each form.
prereqs: [linear-programming-problem]
see_also: [lp-slack-form, slack-variables, basic-feasible-solution, dual-linear-program, simplex-method, polyhedron]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.1, Standard and slack forms (standard form, equivalent linear programs and the four conversion steps)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 1.1 (the general form and the reduction to standard form Ax = b, x ≥ 0)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 1, Introduction (problems in standard form, max cx subject to Ax ≤ b and x ≥ 0)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 4, Section 4.1 (equational form and the conversion of a general linear program to it)
---

A linear program is in *standard form* when it has one of two fixed shapes: all constraints are inequalities $Ax \le b$ and all variables are nonnegative, or all constraints are equations $Ax = b$ and all variables are nonnegative. Books do not agree on which of the two shapes gets the name, so a page or a paper must say which one it means. Each [linear program](/linear-programming-problem/) converts to each shape with a small, explicit change of variables, so an algorithm needs to handle only one of them. The [simplex method](/simplex-method/) and the [basic feasible solutions](/basic-feasible-solution/) are defined on the equation shape.

## Definition

Let $A \in \mathbb{R}^{m \times n}$, $b \in \mathbb{R}^m$ and $c \in \mathbb{R}^n$.

**Inequality standard form.** This is the form that CLRS and Chvátal call standard form:

$$\text{maximize } c^\top x \quad \text{subject to } Ax \le b,\ x \ge 0.$$

**Equality standard form.** This is the form that Bertsimas and Tsitsiklis call standard form and that Matoušek and Gärtner call *equational form*:

$$\text{minimize } c^\top x \quad \text{subject to } Ax = b,\ x \ge 0.$$

The optimization pages of this site use the equality form by default, with $n$ variables and $m$ equations. Papadimitriou and Steiglitz use *canonical form* for $\min c^\top x$ subject to $Ax \ge b$, $x \ge 0$. The [slack form](/lp-slack-form/) of CLRS is a third shape, the equality form written as a dictionary for the simplex method.

**Equivalence.** Two linear programs $L$ (in variables $x$) and $L'$ (in variables $x'$), both maximizations, are *equivalent* if there are maps $\phi$ from the feasible solutions of $L$ to those of $L'$ and $\psi$ back, both preserving the objective value. Then $L$ is infeasible, unbounded or optimal exactly when $L'$ is, the optimal values are equal, and $\psi$ maps an optimal solution of $L'$ to an optimal solution of $L$. A minimization is compared through its negated objective.

**The conversion rules.** Each rule gives an equivalent program, and the maps are linear.

| in the given LP | replace with | $\psi$ back |
|---|---|---|
| minimize $c^\top x$ | maximize $-c^\top x$ | identity |
| $a^\top x \ge \beta$ | $-a^\top x \le -\beta$ | identity |
| $a^\top x = \beta$ (to inequality form) | $a^\top x \le \beta$ and $-a^\top x \le -\beta$ | identity |
| $a^\top x \le \beta$ (to equality form) | $a^\top x + s = \beta$, $s \ge 0$ | drop $s$ |
| $x_j \le 0$ | $x_j = -x_j'$ with $x_j' \ge 0$ | $x_j = -x_j'$ |
| $x_j \ge \ell_j$ | $x_j = \ell_j + x_j'$ with $x_j' \ge 0$, and $b \leftarrow b - \ell_j A_j$ | $x_j = \ell_j + x_j'$ |
| $x_j$ free | $x_j = x_j^+ - x_j^-$ with $x_j^+, x_j^- \ge 0$ | $x_j = x_j^+ - x_j^-$ |

The new variable $s$ is a [slack variable](/slack-variables/), and a variable $s \ge 0$ with $a^\top x - s = \beta$ is a *surplus variable*. For the rule on a free variable, $\phi(x)$ takes $x_j^+ = \max(x_j, 0)$ and $x_j^- = \max(-x_j, 0)$; each feasible point of the new program maps back to a feasible point with the same objective because the objective and the constraints depend only on $x_j^+ - x_j^-$.

**Size.** From a general program with $n$ variables and $m$ constraints, the inequality form has at most $2n$ variables and $2m$ constraints, and the equality form has at most $2n + m$ variables and $m$ equations. The bit length grows by a constant factor.

**Rank.** For the equality form one usually adds the condition that $A$ has full row rank $m$. This loses nothing: if $Ax = b$ has a solution, the rows that are linear combinations of others can be removed by [Gaussian elimination](/gaussian-elimination/) without a change of the solution set; if it has none, the program is infeasible. The definition of a basis needs this condition.

## Examples and non-examples

**A conversion.** Minimize $x_1 + 2x_2$ subject to $x_1 + x_2 \ge 3$, $x_1 - x_2 = 1$, $x_1 \ge 0$, $x_2$ free. The equation gives $x_1 = 1 + x_2$, and then the constraints say $x_2 \ge 1$, so the optimum is $x = (2, 1)$ with value 4.

- *Equality form.* Write $x_2 = u - v$ and add a surplus $s$:
$$\min\ x_1 + 2u - 2v \quad \text{s.t.} \quad x_1 + u - v - s = 3,\quad x_1 - u + v = 1,\quad x_1, u, v, s \ge 0.$$
Of the $\binom{4}{2} = 6$ column pairs, the pair $(u, v)$ is singular because the two columns are negatives of each other. The other five pairs give basic solutions, and only $(x_1, u, v, s) = (2, 1, 0, 0)$ is feasible. It has value 4.
- *Inequality form.* Negate the objective, flip the $\ge$ row and split the equation:
$$\max\ -x_1 - 2u + 2v \quad \text{s.t.} \quad -x_1 - u + v \le -3,\quad x_1 - u + v \le 1,\quad -x_1 + u - v \le -1,\quad x_1, u, v \ge 0.$$
The optimal value is $-4$, at $(2, 1 + t, t)$ for each $t \ge 0$. The only vertex is $t = 0$. The whole ray is optimal because only $u - v$ matters.

**Already standard.** The [running example](/linear-programming-problem/) $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$ is in inequality form. Three slacks turn it into the equality form with $A = \begin{pmatrix} 1 & 1 & 1 & 0 & 0 \\ 1 & 3 & 0 & 1 & 0 \\ 1 & 0 & 0 & 0 & 1 \end{pmatrix}$ and $b = (4, 9, 3)$.

**Non-examples.**

- $\max x$ subject to $x < 1$. A strict inequality is not allowed. This program has supremum 1 and no optimum, which no linear program can have.
- $\min x_1$ subject to $x_1 \in \{0, 1\}$. An integrality condition makes an [integer program](/binary-integer-programming/), and no conversion rule removes it.
- $\min |x_1| + |x_2|$ subject to $x_1 + x_2 = 1$. The objective is not linear. The program still *converts* to an LP with the split $x_j = x_j^+ - x_j^-$ and the objective $x_1^+ + x_1^- + x_2^+ + x_2^-$, because at an optimum $x_j^+ x_j^- = 0$. This trick works for a sum of absolute values that is minimized, and fails when it is maximized.
- $\max c^\top x$ subject to $Ax \le b$ with $x$ free is in neither form until the free variables are split, although many geometry pages, such as [Seidel's algorithm](/seidel-linear-programming/), work in this shape directly.

**Pitfalls.**

- *Splitting free variables destroys uniqueness.* The pair $(x_j^+ + t, x_j^- + t)$ gives the same $x$ for each $t \ge 0$, so the converted program has unbounded optimal faces even when the original has a unique optimum. A vertex of the converted program still has $x_j^+ x_j^- = 0$, because the two columns are negatives of each other and cannot both be in a basis.
- *Equations to two inequalities.* This doubles the rows and makes every vertex degenerate in the inequality form, because the two rows are tight together but count only once toward the rank. Solvers keep equations as equations.
- *The sign of the dual.* The dual of each form has its own sign rules. Converting the primal changes the shape of the [dual](/dual-linear-program/), not its optimal value.

## Related definitions

- [Slack form](/lp-slack-form/): the equality form solved for a set of basic variables.
- [Slack variables](/slack-variables/): the variables that the conversion adds.
- [Polyhedron](/polyhedron/): the feasible set of either form; in the equality form it lies in the nonnegative orthant and has a vertex whenever it is not empty.
- [Basic feasible solution](/basic-feasible-solution/): a vertex of the equality form, given by a set of $m$ independent columns.
- [Dual linear program](/dual-linear-program/): the dual of $\max c^\top x$, $Ax \le b$, $x \ge 0$ is $\min b^\top y$, $A^\top y \ge c$, $y \ge 0$, and the dual of $\min c^\top x$, $Ax = b$, $x \ge 0$ is $\max b^\top y$, $A^\top y \le c$.

## References
