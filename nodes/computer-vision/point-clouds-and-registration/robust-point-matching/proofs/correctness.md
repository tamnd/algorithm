---
title: Softassign and the pose step each minimize the same energy at a fixed temperature
proves: [correctness]
status: full
---

We use the notation of the page and of the reference code. $X$ has $n$ points $x_j$ and $Y$ has $m$ points $y_k$. The map is $y \mapsto A y + t$, and $d_{jk} = |x_j - A y_k - t|^2$. The match matrix $M$ has the real entries $M_{jk}$, a slack column with entries $s_j$ for the rows, and a slack row with entries $r_k$ for the columns. The constraints are

$$\sum_k M_{jk} + s_j = 1 \ \text{ for each } j, \qquad \sum_j M_{jk} + r_k = 1 \ \text{ for each } k, \qquad M, s, r > 0 .$$

Call this set $\mathcal{C}$. With $\phi(v) = v \log v - v$, the energy at the inverse temperature $\beta > 0$ is

$$E_\beta(M, A, t) = \sum_{j,k} M_{jk} (d_{jk} - \alpha) + \lambda \|A - I\|_F^2 + \frac{1}{\beta} \Bigl( \sum_{j,k} \phi(M_{jk}) + \sum_j \phi(s_j) + \sum_k \phi(r_k) \Bigr).$$

Line L5 sets $M_{jk} = \exp(\beta(\alpha - d_{jk}))$ and $s_j = r_k = 1$, up to a common factor in each row. Lines L6 and L7 divide each row, then each column, by its sum, and repeat. Line L8 computes the pose step.

## Lemma 1: Sinkhorn keeps the scaling form

After line L5 and any number of sweeps of lines L6 and L7, there are numbers $u_j$ and $v_k$ such that

$$M_{jk} = e^{\beta(\alpha - d_{jk})}\, e^{-u_j - v_k}, \qquad s_j = e^{-u_j}, \qquad r_k = e^{-v_k}.$$

After a row step, every row sums to 1; after a column step, every column sums to 1.

*Proof.* At line L5 this holds with $v_k = 0$ and $u_j$ the common factor of row $j$ (zero, or the shift that the code subtracts to avoid overflow). A row step divides $M_{j1}, \ldots, M_{jm}$ and $s_j$ by the same positive number $c$, which adds $\log c$ to $u_j$. A column step divides $M_{1k}, \ldots, M_{nk}$ and $r_k$ by the same number, which adds to $v_k$. The slack column entry $s_j$ is changed only by the row step of row $j$, and the slack row entry $r_k$ only by the column step of column $k$, so the form holds after every step. The sums are 1 right after their own step by construction. $\square$

## Lemma 2: a converged softassign minimizes the energy over the match matrix

Fix $A$, $t$ and $\beta$. If a matrix of the form of Lemma 1 lies in $\mathcal{C}$, then it is the unique minimizer of $E_\beta(\cdot, A, t)$ over $\mathcal{C}$.

*Proof.* Over $\mathcal{C}$, the energy is a linear function of $(M, s, r)$ plus $\frac{1}{\beta}$ times a sum of the strictly convex functions $\phi$, so it is strictly convex, and the constraints are linear. For such a problem, a feasible point at which the gradient of the energy is a linear combination of the gradients of the constraints is the unique minimizer (the Karush-Kuhn-Tucker conditions are sufficient for a convex problem, and the inequality constraints $M > 0$ are not active). With multipliers $\mu_j$ for the rows and $\nu_k$ for the columns, the conditions read

$$d_{jk} - \alpha + \tfrac{1}{\beta} \log M_{jk} = \mu_j + \nu_k, \qquad \tfrac{1}{\beta} \log s_j = \mu_j, \qquad \tfrac{1}{\beta} \log r_k = \nu_k ,$$

since $\phi'(v) = \log v$. The form of Lemma 1 satisfies them with $\mu_j = -u_j / \beta$ and $\nu_k = -v_k / \beta$. $\square$

## Lemma 3: the pose step minimizes the energy over the map

Fix $M$ with $w = \sum_{j,k} M_{jk} > 0$, and let $\lambda > 0$. Then $E_\beta(M, \cdot, \cdot)$ has a unique minimizer over $(A, t)$, and line L8 returns it.

*Proof.* Only the terms $\sum M_{jk} d_{jk} + \lambda \|A - I\|_F^2$ depend on $(A, t)$. They split into two independent problems, one for each row $r$ of $A$ with the matching entry $t_r$: minimize

$$\sum_{j,k} M_{jk} (x_{jr} - a_r \cdot y_k - t_r)^2 + \lambda |a_r - e_r|^2 ,$$

where $e_r$ is row $r$ of $I$. This is a quadratic in $z = (a_r, t_r) \in \mathbb{R}^3$ with the matrix

$$S = \begin{pmatrix} \sum M_{jk} y_k y_k^\top + \lambda I & \sum M_{jk} y_k \\ \sum M_{jk} y_k^\top & w \end{pmatrix}.$$

With $\bar y = \sum M_{jk} y_k / w$, the Schur complement of $w$ is $\sum M_{jk} (y_k - \bar y)(y_k - \bar y)^\top + \lambda I$, which is positive definite. So $S$ is positive definite, the quadratic is strictly convex, and its unique minimizer solves $S z = b$ with $b = (\sum M_{jk} x_{jr} y_k + \lambda e_r,\ \sum M_{jk} x_{jr})$. Line L8 forms exactly $S$ and $b$ and solves the system by Gaussian elimination. $\square$

## Theorem

At a fixed $\beta$ and a fixed $\lambda$, if Sinkhorn converges at each step of the inner loop of line L3, then the energy $E_\beta$ never rises from one step of the inner loop to the next.

*Proof.* Let $(M, A, t)$ be the state after one step. The next step first replaces $M$ by $M'$, the minimizer over $\mathcal{C}$ for the fixed $(A, t)$ (Lemmas 1 and 2), so $E_\beta(M', A, t) \le E_\beta(M, A, t)$. Then it replaces $(A, t)$ by the minimizer for the fixed $M'$ (Lemma 3), so $E_\beta(M', A', t') \le E_\beta(M', A, t)$. $\square$

This is block coordinate descent on one energy. The test `test_energy_never_rises_at_fixed_beta` checks it with Sinkhorn run to a tolerance of $10^{-13}$.

## What this does not prove

- **Convergence of Sinkhorn.** The theorem assumes that the sweeps reach $\mathcal{C}$. The row and column steps are alternating projections onto the two sets of constraints in the Kullback-Leibler sense. Sinkhorn (1964) proved that the iteration converges for a square positive matrix scaled to doubly stochastic form; the form with slacks here is a related case, and we do not prove its convergence. The reference code stops after a fixed number of sweeps, so at large $\beta$ it uses a matrix that is only close to $\mathcal{C}$.
- **Annealing.** When $\beta$ grows, or when $\lambda$ shrinks, the energy itself changes, so the energy of the whole run need not decrease. The hope behind deterministic annealing is that the minimum at a small $\beta$, where $E_\beta$ is nearly convex in $M$, leads by small changes to a good minimum at a large $\beta$. This is a heuristic, not a theorem; the test `test_fixed_small_penalty_can_fail` shows a case where a different schedule fails.
- **Global optimum.** The joint energy is not convex in $(M, A, t)$, so the method can stop in a local minimum.
- **Hard matches.** At a finite $\beta$ the matrix is soft. The rule that the code uses to read off the matches, the largest entry of both its row and its column and above the slacks, is a choice of this code.
