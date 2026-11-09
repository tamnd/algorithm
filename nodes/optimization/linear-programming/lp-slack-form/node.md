---
tag: M5BY7D
kind: definition
slug: lp-slack-form
name: Slack form of a linear program
aliases:
- Converting linear programs into slack form
- dictionary
- simplex dictionary
area: optimization/linear-programming
level: core
summary: Form of a linear program with equality constraints over nonnegative basic and nonbasic variables, on which simplex pivots operate.
prereqs: [lp-standard-form, slack-variables]
see_also: [simplex-method, pivot-operation, basic-feasible-solution, reduced-cost, ratio-test, lp-degeneracy]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.1, Standard and slack forms (the tuple (N, B, A, b, c, v)), and Section 29.3, The simplex algorithm (PIVOT and the lemma that the slack form is determined by its basis)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 2, How the simplex method works (dictionaries and feasible dictionaries)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 5, The simplex method (simplex tableaus, written in the same solved shape)
---

The slack form of a linear program writes the equality [standard form](/lp-standard-form/) solved for a chosen set of $m$ *basic* variables: each basic variable and the objective appear as an affine function of the $n$ *nonbasic* variables. The name is from CLRS; Chvátal calls the same object a *dictionary*, and a simplex *tableau* is the same data in a table. Setting the nonbasic variables to zero reads off a [basic solution](/basic-feasible-solution/) and its objective value. A [pivot](/pivot-operation/) of the [simplex method](/simplex-method/) maps one slack form to another with one variable swapped between the two sets.

## Definition

**Setting.** Start from the inequality form $\max c^\top x$ subject to $Ax \le b$, $x \ge 0$ with $A \in \mathbb{R}^{m \times n}$, and add one [slack variable](/slack-variables/) per row, named $x_{n+1}, \ldots, x_{n+m}$. The variables are now $x_1, \ldots, x_{n+m}$, all nonnegative, with $m$ equations.

**Slack form.** A slack form is a tuple $(N, B, A, b, c, v)$ where $B$ and $N$ partition $\{1, \ldots, n+m\}$ with $|B| = m$ and $|N| = n$, $A = (a_{ij})_{i \in B, j \in N}$, $b = (b_i)_{i \in B}$, $c = (c_j)_{j \in N}$ and $v$ is a number. It stands for the program

$$\begin{aligned} \text{maximize}\quad & z = v + \sum_{j \in N} c_j x_j \\ \text{subject to}\quad & x_i = b_i - \sum_{j \in N} a_{ij} x_j \quad (i \in B), \\ & x_j \ge 0 \quad (j \in B \cup N). \end{aligned}$$

The variables in $B$ are *basic* and those in $N$ are *nonbasic*. The constraints $x \ge 0$ are not written in the form; every variable is nonnegative. The sign convention matters: $a_{ij}$ appears with a minus sign, so these $a_{ij}$ are not the entries of the original matrix but of the form after pivots.

**The basic solution.** Setting $x_j = 0$ for $j \in N$ gives $x_i = b_i$ for $i \in B$ and $z = v$. The slack form is *feasible* when $b_i \ge 0$ for all $i \in B$; then this basic solution is a [basic feasible solution](/basic-feasible-solution/).

**Equivalence.** All the slack forms reached by pivots from the initial one describe the same set of points $(x_1, \ldots, x_{n+m}) \in \mathbb{R}^{n+m}$ and the same objective function on it, because each pivot solves one equation for one variable and substitutes it into the others, which is an invertible row operation.

**The form is fixed by its basis.** Two slack forms with the same set $B$ that describe the same equations and objective are equal. *Proof.* Let $(N, B, A, b, c, v)$ and $(N, B, A', b', c', v')$ be two such forms. Both express $x_i$ for $i \in B$ in terms of the free choice of $x_j$, $j \in N$, so for all real values of the nonbasic variables, $b_i - \sum_{j \in N} a_{ij} x_j = b'_i - \sum_{j \in N} a'_{ij} x_j$. Setting all $x_j = 0$ gives $b_i = b'_i$. Then setting one $x_k = 1$ and the others to 0 gives $a_{ik} = a'_{ik}$. The same argument on $z$ gives $v = v'$ and $c = c'$. $\square$

So a slack form is a function of its basis $B$. In matrix terms, with the equality form $\bar A \bar x = b$, $\bar A = (A \ \ I_m)$, and $A_B$ the columns of $B$, the form is $x_B = A_B^{-1} b - A_B^{-1} A_N x_N$ and $z = c_B^\top A_B^{-1} b + (c_N^\top - c_B^\top A_B^{-1} A_N)\, x_N$. The coefficients $c_j$ of the objective row are the [reduced costs](/reduced-cost/) of the nonbasic variables, in the sign convention of a maximization.

## Examples and non-examples

**The running example.** For $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$, the initial slack form has $B = \{3, 4, 5\}$ and $N = \{1, 2\}$:

$$z = 3x_1 + 2x_2, \qquad x_3 = 4 - x_1 - x_2, \qquad x_4 = 9 - x_1 - 3x_2, \qquad x_5 = 3 - x_1.$$

It is feasible, and its basic solution is the origin with $z = 0$. The variable $x_1$ has a positive coefficient in $z$, so increasing it helps. The tightest of its bounds $4/1$, $9/1$ and $3/1$ (the [ratio test](/ratio-test/)) is the last one, so $x_1$ enters and $x_5$ leaves. Solving $x_5 = 3 - x_1$ for $x_1$ and substituting gives

$$z = 9 + 2x_2 - 3x_5, \qquad x_3 = 1 - x_2 + x_5, \qquad x_4 = 6 - 3x_2 + x_5, \qquad x_1 = 3 - x_5.$$

Now $x_2$ enters, the ratios are $1/1$ and $6/3$, and $x_3$ leaves:

$$z = 11 - 2x_3 - x_5, \qquad x_2 = 1 - x_3 + x_5, \qquad x_4 = 3 + 3x_3 - 2x_5, \qquad x_1 = 3 - x_5.$$

All coefficients of $z$ are now at most zero. Since $x_3, x_5 \ge 0$, every feasible point has $z \le 11$, and the basic solution $(x_1, \ldots, x_5) = (3, 1, 0, 3, 0)$ reaches 11. So it is optimal. The negated coefficients of the slacks $x_3, x_4, x_5$ in the last objective row, $(2, 0, 1)$, form an optimal solution of the [dual](/dual-linear-program/).

**An infeasible slack form.** For the constraints $-x_1 - x_2 \le -1$ and $x_1 \le 2$, the initial form is $x_3 = -1 + x_1 + x_2$, $x_4 = 2 - x_1$. Its basic solution has $x_3 = -1 < 0$, so the form is not feasible, though the program is: $(1, 0)$ satisfies both rows. The simplex method first needs an [initial basic feasible solution](/initial-basic-feasible-solution/).

**A degenerate form.** If some $b_i = 0$ with $i \in B$, the basic variable $x_i$ is zero, and a pivot on a column with $a_{ij} > 0$ in row $i$ has step length 0: the form changes but the point and $z$ do not. This is [degeneracy](/lp-degeneracy/), the source of cycling.

**Non-examples.**

- $x_3 = 4 - x_1 - x_2$ together with $x_1 = 3 - x_5 - x_3$. The variable $x_3$ is basic in the first equation and appears on the right side of the second. In a slack form, the basic variables never appear on the right.
- A set $B$ whose columns of $(A \ \ I_m)$ are linearly dependent. No slack form has this basis, because the equations cannot be solved for those variables.

## Related definitions

- [Standard form](/lp-standard-form/): the slack form is the equality form, solved for a basis.
- [Slack variables](/slack-variables/): the variables $x_{n+1}, \ldots, x_{n+m}$ of the initial form.
- [Basic feasible solution](/basic-feasible-solution/): the point that a feasible slack form describes.
- [Reduced cost](/reduced-cost/): the coefficients $c_j$, $j \in N$, of the objective row.
- [Pivot operation](/pivot-operation/) and [ratio test](/ratio-test/): the step from one slack form to the next.
- [Simplex method](/simplex-method/): the sequence of slack forms from a feasible one to an optimal one.

## References
