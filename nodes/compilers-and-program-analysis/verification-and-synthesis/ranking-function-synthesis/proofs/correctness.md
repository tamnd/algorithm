---
title: The Podelski-Rybalchenko linear program is sound and complete for linear ranking functions over the rationals
proves: [correctness]
status: full
---

**Setting.** A single-path linear loop over $n$ rational variables is a relation $R = \{(x, x') \in \mathbb{Q}^n \times \mathbb{Q}^n : A x + A' x' \le b\}$, where $A$ and $A'$ are $m \times n$ matrices and $b \in \mathbb{Q}^m$. A run is a finite or infinite sequence $x_0, x_1, \ldots$ with $(x_j, x_{j+1}) \in R$ for each step; the loop *terminates* when every run is finite. A *linear ranking function* is a vector $\rho \in \mathbb{Q}^n$ with numbers $\delta_0$ and $\delta > 0$ such that for every $(x, x') \in R$

- (B) $\rho \cdot x \ge \delta_0$, and
- (D) $\rho \cdot x - \rho \cdot x' \ge \delta$.

Multipliers are row vectors in $\mathbb{Q}^m$; $\lambda \ge 0$ means that every entry is nonnegative. The algorithm solves the linear system

$$\lambda_1, \lambda_2 \ge 0, \quad \lambda_1 A' = 0, \quad (\lambda_1 - \lambda_2) A = 0, \quad \lambda_2 (A + A') = 0, \quad \lambda_2 b \le -1 \qquad (\ast)$$

and returns $\rho = \lambda_2 A'$, $\delta_0 = -\lambda_1 b$ and $\delta = -\lambda_2 b$, or "none" if $(\ast)$ has no solution.

## Lemma 1: affine Farkas lemma

**Claim.** Let $My \le c$ be a system over $\mathbb{Q}^k$. (1) If it has a solution, then all its solutions satisfy $w \cdot y \le \gamma$ if and only if $\lambda M = w$ and $\lambda c \le \gamma$ for some $\lambda \ge 0$. (2) It has no solution if and only if $\lambda M = 0$ and $\lambda c < 0$ for some $\lambda \ge 0$.

**Proof.** The "if" directions: in (1), $w \cdot y = \lambda M y \le \lambda c \le \gamma$; in (2), a solution would give $0 = \lambda M y \le \lambda c < 0$. The "only if" directions follow from the duality theorem of linear programming, see [the dual linear program](/dual-linear-program/): in (1), the problem "maximize $w \cdot y$ subject to $My \le c$" is feasible and bounded by $\gamma$, so its dual "minimize $\lambda c$ subject to $\lambda M = w$, $\lambda \ge 0$" has an optimal solution with the same value, at most $\gamma$; in (2), with $w = 0$, the dual is feasible ($\lambda = 0$) and the primal is infeasible, so the dual is unbounded below. The data are rational and an optimal or unbounded direction can be taken at a basic solution, so $\lambda$ is rational. This is [Farkas' lemma](/farkas-lemma/) in affine form. $\square$

## Theorem 1: soundness

**Claim.** If $(\lambda_1, \lambda_2)$ solves $(\ast)$, then $\rho = \lambda_2 A'$ is a linear ranking function with $\delta_0 = -\lambda_1 b$ and $\delta = -\lambda_2 b \ge 1$.

**Proof.** From $\lambda_2 (A + A') = 0$, $\rho = \lambda_2 A' = -\lambda_2 A$. From $(\lambda_1 - \lambda_2) A = 0$, also $\rho = -\lambda_1 A$. Let $(x, x') \in R$, so $A x + A' x' \le b$.

(B): $\rho \cdot x = -\lambda_1 A x = -\lambda_1 A x - \lambda_1 A' x' = -\lambda_1 (A x + A' x') \ge -\lambda_1 b = \delta_0$. The second step adds $\lambda_1 A' x' = 0$, and the inequality uses $\lambda_1 \ge 0$.

(D): $\rho \cdot x - \rho \cdot x' = -\lambda_2 A x - \lambda_2 A' x' = -\lambda_2 (A x + A' x') \ge -\lambda_2 b = \delta \ge 1$, using $\lambda_2 \ge 0$ and the last row of $(\ast)$. $\square$

## Theorem 2: completeness over the rationals

**Claim.** If the loop has a linear ranking function $(\rho, \delta_0, \delta)$, then $(\ast)$ has a solution.

**Proof.** Treat $(x, x')$ as one vector of $2n$ unknowns, so $R$ is the solution set of $[A \;\, A'] (x, x') \le b$.

*Case $R$ empty.* By Lemma 1, part 2, there is $\lambda \ge 0$ with $\lambda A = 0$, $\lambda A' = 0$ and $\lambda b < 0$. Scale it by $-1/(\lambda b)$, so that $\lambda b = -1$, and take $\lambda_1 = \lambda_2 = \lambda$. Every row of $(\ast)$ holds: the three products are 0 and $\lambda_2 b = -1$.

*Case $R$ not empty.* Condition (B) says that every point of $R$ satisfies $(-\rho) \cdot x + 0 \cdot x' \le -\delta_0$. By Lemma 1, part 1, there is $\lambda_1 \ge 0$ with $\lambda_1 A = -\rho$, $\lambda_1 A' = 0$ and $\lambda_1 b \le -\delta_0$. Condition (D) says that every point of $R$ satisfies $(-\rho) \cdot x + \rho \cdot x' \le -\delta$. By Lemma 1, part 1, there is $\lambda_2 \ge 0$ with $\lambda_2 A = -\rho$, $\lambda_2 A' = \rho$ and $\lambda_2 b \le -\delta$. Then $\lambda_1 A' = 0$; $(\lambda_1 - \lambda_2) A = -\rho + \rho = 0$; $\lambda_2 (A + A') = -\rho + \rho = 0$; and $\lambda_2 b \le -\delta < 0$. Multiply both $\lambda_1$ and $\lambda_2$ by $s = 1/\min(\delta, 1) > 0$. The equalities are homogeneous and stay true, the multipliers stay nonnegative, and $\lambda_2 b \le -s\delta \le -1$. $\square$

## Corollary: the decision procedure

The algorithm returns a function exactly when a linear ranking function exists over $\mathbb{Q}$ (Theorems 1 and 2), and the exact simplex method decides whether $(\ast)$ has a solution. The system has $2m$ unknowns and $3n$ equalities and one inequality, so by the polynomial algorithms for [linear programming](/linear-programming-problem/) the existence of a linear ranking function over the rationals is decidable in polynomial time.

## Theorem 3: a ranking function proves termination

**Claim.** If $(\rho, \delta_0, \delta)$ is a linear ranking function, every run from $x_0$ has at most $\lfloor (\rho \cdot x_0 - \delta_0) / \delta \rfloor + 1$ steps, over $\mathbb{Q}^n$ and over $\mathbb{Z}^n$.

**Proof.** Let $x_0, \ldots, x_t$ be a run with $t \ge 1$ steps. By (D), $\rho \cdot x_{t-1} \le \rho \cdot x_0 - (t - 1) \delta$, and by (B) applied to the step $(x_{t-1}, x_t)$, $\rho \cdot x_{t-1} \ge \delta_0$. So $(t - 1) \delta \le \rho \cdot x_0 - \delta_0$. An integer run is a rational run, so the bound also holds over $\mathbb{Z}^n$. $\square$

## What the theorems do not give

**Termination does not imply a linear ranking function.** The loop $x \ge 0$, $x' = x + y$, $y' = y - 1$ terminates from every rational state. The value of $y$ after $j$ steps is $y_0 - j$. So after $j_0 = \max(0, \lceil y_0 \rceil + 1)$ steps $y \le -1$, and from then on each step adds $y \le -1$ to $x$. Since a step needs $x \ge 0$, at most $x_{j_0} + 1$ more steps follow. But no $\rho = (p, q)$ works. For (D), $\rho \cdot x - \rho \cdot x' = -p y + q$ must be at least $\delta > 0$ for every $y$, since $y$ is free; so $p = 0$ and $q > 0$. For (B), $\rho \cdot x = q y$ must be bounded below for all $y$, which fails for $q > 0$. So $(\ast)$ has no solution, and the tests check it.

**A rational answer is about rational runs.** Theorem 2 is completeness over $\mathbb{Q}$. A loop can terminate over $\mathbb{Z}$, and even have an integer linear ranking function, while it does not terminate over $\mathbb{Q}$. For the guard $2x \ge 1 \wedge 2x \le 1$ with $x' = x$, no integer state enters the loop, so every function is a ranking function over $\mathbb{Z}$, but the rational state $x = 1/2$ loops for ever. So "none" from this algorithm does not mean that an integer program fails to terminate, and it does not even mean that it has no integer linear ranking function. Theorem 1 does transfer: a rational ranking function is also one for the integer runs. $\blacksquare$
