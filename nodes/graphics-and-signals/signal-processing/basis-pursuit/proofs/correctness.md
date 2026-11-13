---
title: Correctness of basis pursuit
proves: [correctness]
status: full
---

We prove that the linear program of lines L1 to L5 solves $(P_1)$, that its vertex solution has at most $m$ nonzero entries, and that $(P_1)$ recovers every $s$-sparse vector exactly if and only if $A$ has the null space property of order $s$. We then show that the coherence condition $\mu < 1/(2s - 1)$ implies the null space property.

## Lemma 1 (the linear program is $(P_1)$)

Let $M = [\,A \;\; {-A}\,]$ and let $(\mathrm{LP})$ be: minimize $\mathbf 1^{\mathsf T} z$ subject to $Mz = y$, $z \ge 0$, with $z = (u, v)$. Then $(\mathrm{LP})$ is feasible exactly when $Ax = y$ has a solution, the two problems have the same optimal value, and $x = u - v$ is a minimizer of $(P_1)$ for every optimal $(u, v)$.

*Proof.* If $Ax = y$, let $u_j = \max(x_j, 0)$ and $v_j = \max(-x_j, 0)$. Then $u, v \ge 0$, $u - v = x$, so $Mz = A(u - v) = y$, and $\mathbf 1^{\mathsf T} z = \sum_j |x_j| = \|x\|_1$. So the value of $(\mathrm{LP})$ is at most the value of $(P_1)$. Conversely, if $z = (u, v)$ is feasible, then $x = u - v$ satisfies $Ax = Mz = y$, and $|x_j| = |u_j - v_j| \le u_j + v_j$, so $\|x\|_1 \le \mathbf 1^{\mathsf T} z$. So the value of $(P_1)$ is at most the value of $(\mathrm{LP})$. The values are equal, and for an optimal $z$, $\|u - v\|_1 \le \mathbf 1^{\mathsf T} z$, which is the common optimal value, so $u - v$ is optimal for $(P_1)$. $\square$

The objective of $(\mathrm{LP})$ is at least $0$, so when it is feasible it has an optimal solution, and the simplex method of lines L3 and L4, with Bland's rule, ends at an optimal basic solution.

## Lemma 2 (sparse vertices)

Let $z = (u, v)$ be an optimal basic solution of $(\mathrm{LP})$. Then $x = u - v$ has at most $m$ nonzero entries.

*Proof.* A basic solution has at most $m$ nonzero entries, one for each basic column, after redundant rows are dropped. If both $u_j > 0$ and $v_j > 0$ for some $j$, subtract $t = \min(u_j, v_j)$ from both. Columns $j$ and $n + j$ of $M$ are $a_j$ and $-a_j$, so $Mz$ does not change, and the cost drops by $2t > 0$, which contradicts optimality. So for each $j$ at most one of $u_j, v_j$ is nonzero, $x_j \ne 0$ only if one of them is, and $x$ has at most as many nonzero entries as $z$. $\square$

## Theorem 1 (null space property)

Say that $A$ has the null space property of order $s$ if

$$\|v_S\|_1 < \|v_{\bar S}\|_1 \quad \text{for every } v \ne 0 \text{ with } Av = 0 \text{ and every } S \subseteq \{1, \ldots, n\} \text{ with } |S| \le s,$$

where $v_S$ keeps the entries of $v$ on $S$ and $\bar S$ is the complement. Then the following are equivalent:

1. For every $s$-sparse $x_0$, the vector $x_0$ is the unique minimizer of $\|x\|_1$ subject to $Ax = Ax_0$.
2. $A$ has the null space property of order $s$.

*Proof that 2 implies 1.* Let $x_0$ be $s$-sparse with support inside $S$, $|S| \le s$, and let $x \ne x_0$ satisfy $Ax = Ax_0$. Then $v = x_0 - x \ne 0$ and $Av = 0$. Since $x_0$ is zero off $S$, $x_{\bar S} = -v_{\bar S}$ and $x_S = x_{0,S} - v_S$. By the triangle inequality,

$$\|x_0\|_1 = \|x_{0,S}\|_1 \le \|x_{0,S} - v_S\|_1 + \|v_S\|_1 = \|x_S\|_1 + \|v_S\|_1 < \|x_S\|_1 + \|v_{\bar S}\|_1 = \|x_S\|_1 + \|x_{\bar S}\|_1 = \|x\|_1.$$

The strict step is the null space property. So every other feasible $x$ has a larger norm. $\square$

*Proof that 1 implies 2.* Let $v \ne 0$ with $Av = 0$, and $|S| \le s$. The vector $v_S$ is $s$-sparse, and $A v_S = A(-v_{\bar S})$ since $A(v_S + v_{\bar S}) = 0$. Also $-v_{\bar S} \ne v_S$, because $v_S - (-v_{\bar S}) = v \ne 0$. By 1, $v_S$ is the unique minimizer for the measurements $Av_S$, so $\|v_S\|_1 < \|{-v_{\bar S}}\|_1 = \|v_{\bar S}\|_1$. $\square$

## Theorem 2 (coherence)

Let the columns of $A$ have norm $1$ and let $\mu = \max_{i \ne j} |\langle a_i, a_j \rangle|$. If $\mu < 1/(2s - 1)$, then $A$ has the null space property of order $s$. So basis pursuit recovers every $s$-sparse vector.

*Proof.* Let $Av = 0$ with $v \ne 0$. For each $i$, take the inner product of $\sum_j v_j a_j = 0$ with $a_i$:

$$v_i = -\sum_{j \ne i} \langle a_i, a_j \rangle v_j, \qquad \text{so} \qquad |v_i| \le \mu \big(\|v\|_1 - |v_i|\big), \qquad |v_i| \le \frac{\mu}{1 + \mu}\|v\|_1.$$

For $|S| \le s$, summing over $i \in S$ gives $\|v_S\|_1 \le \frac{s\mu}{1 + \mu}\|v\|_1$. The condition $\mu(2s - 1) < 1$ is the same as $2s\mu < 1 + \mu$, so $\|v_S\|_1 < \tfrac12 \|v\|_1 = \tfrac12(\|v_S\|_1 + \|v_{\bar S}\|_1)$, which gives $\|v_S\|_1 < \|v_{\bar S}\|_1$. $\square$

The condition $\mu < 1/(2s - 1)$ can also be written as $s < \tfrac12(1 + 1/\mu)$, which is the form of Donoho and Elad (2003).

## Theorem 3 (correctness of BASIS-PURSUIT)

If $Ax = y$ has no solution, line L3 reports it. Otherwise line L5 returns a minimizer $\hat x$ of $(P_1)$ with at most $m$ nonzero entries. If moreover $y = Ax_0$ for an $s$-sparse $x_0$ and $A$ has the null space property of order $s$, then $\hat x = x_0$.

*Proof.* Phase 1 minimizes the sum of the artificial variables, which is $0$ exactly when $Mz = y$ has a solution with $z \ge 0$, and by Lemma 1 this is exactly when $Ax = y$ has a solution. Phase 2 ends at an optimal basic solution, and Lemmas 1 and 2 give the first claim. Under the null space property, Theorem 1 says $x_0$ is the only minimizer of $(P_1)$, so $\hat x = x_0$. $\square$
