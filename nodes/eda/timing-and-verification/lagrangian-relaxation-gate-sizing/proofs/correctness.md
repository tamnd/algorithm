---
title: The Lagrangian relaxation of gate sizing reduces to flow-conserving multipliers, its local resizing is optimal, and there is no duality gap
proves: [flow conservation, weak duality, local resizing, strong duality, complexity]
status: full
---

**Model.** The circuit is a DAG of gates $0, \dots, n - 1$ with $m$ edges. Gate $i$ has a size $x_i \in [\ell_i, h_i]$ with $0 < \ell_i \le h_i$ and constants $p_i \ge 0$, $r_i, c_i, a_i > 0$ and $f_i \ge 0$, and its delay is
$$ D_i(x) = p_i + \frac{r_i}{x_i} \Big( f_i + \sum_{j \in \mathrm{out}(i)} c_j x_j \Big). $$
The timing graph adds a source $s$ with an edge to each gate without fanins and a sink $t$ with an edge from each gate without fanouts; let $E$ be all its edges. With arrival variables $A_i$ and $A_s = 0$, the problem (P) is
$$ \min \sum_i a_i x_i \quad \text{subject to} \quad A_u + D_v(x) \le A_v \ \ ((u, v) \in E,\ v \ne t), \qquad A_u \le T \ \ ((u, t) \in E), \qquad \ell \le x \le h. $$
(P) is the same as asking that the latest arrival time be at most $T$: given $x$, the arrival times of static timing analysis are the least $A$ that meet the first constraints.

**Lemma 1 (flow conservation).** For multipliers $\mu \ge 0$ on $E$, let $\mathcal L(x, A, \mu)$ be the Lagrangian of the timing constraints. Its infimum over the free variables $A$ is $-\infty$ unless, at every gate $i$, $\sum_{e \text{ into } i} \mu_e = \sum_{e \text{ out of } i} \mu_e$. Under this condition
$$ \mathcal L(x, A, \mu) = \sum_i a_i x_i + \sum_i \lambda_i D_i(x) - T \sum_{(u, t) \in E} \mu_{ut}, \qquad \lambda_i = \sum_{e \text{ into } i} \mu_e. $$

*Proof.* $\mathcal L = \sum_i a_i x_i + \sum_{(u, v), v \ne t} \mu_{uv} (A_u + D_v - A_v) + \sum_{(u, t)} \mu_{ut} (A_u - T)$. The coefficient of $A_i$ is the flow out of $i$ minus the flow into $i$. A linear function of an unbounded variable has infimum $-\infty$ unless its coefficient is 0. With all coefficients 0 the $A$ terms vanish, and each $D_v$ appears with the sum of the multipliers into $v$. $\square$

So the dual function is $Q(\mu) = \min_{\ell \le x \le h} \Phi_\lambda(x) - T \sum_{(u, t)} \mu_{ut}$ with $\Phi_\lambda(x) = \sum_i a_i x_i + \sum_i \lambda_i D_i(x)$, on the set $\Omega$ of nonnegative flow-conserving $\mu$. The inner problem is the *local resizing subproblem*.

**Lemma 2 (weak duality).** For every $\mu \in \Omega$, $Q(\mu) \le \mathrm{OPT}(P)$.

*Proof.* For a feasible $(x, A)$, every multiplier term is $\mu_e$ times a number at most 0, so $\mathcal L(x, A, \mu) \le \sum_i a_i x_i$. Take the minimum over $x$ on the left and over feasible points on the right. $\square$

**Lemma 3 (one gate in closed form).** Fix $\lambda \ge 0$ and all sizes except $x_i$. Then $\Phi_\lambda$ as a function of $x_i$ is $\alpha x_i + \beta / x_i + \text{const}$ with
$$ \alpha = a_i + c_i \sum_{k \in \mathrm{in}(i)} \frac{\lambda_k r_k}{x_k} > 0, \qquad \beta = \lambda_i r_i \Big( f_i + \sum_{j \in \mathrm{out}(i)} c_j x_j \Big) \ge 0, $$
and its minimum over $[\ell_i, h_i]$ is at $x_i = \min(h_i, \max(\ell_i, \sqrt{\beta / \alpha}))$.

*Proof.* $x_i$ appears in $a_i x_i$, in $\lambda_i D_i$ as $\lambda_i r_i (\cdots) / x_i$, and in $\lambda_k D_k$ for each fanin $k$ through the load $c_i x_i$, which gives $\lambda_k r_k c_i x_i / x_k$. The function $\alpha z + \beta / z$ is convex on $z > 0$ with its unconstrained minimum at $\sqrt{\beta / \alpha}$ (at $z \to 0$ if $\beta = 0$), so its minimum over an interval is that point clamped into the interval. $\square$

**Lemma 4 (a fixed point of local resizing solves the subproblem).** With $y_i = \log x_i$, $\Psi(y) = \Phi_\lambda(e^y)$ is convex, differentiable and strictly convex, so the subproblem has a unique minimizer. A point at which every $x_i$ satisfies the formula of Lemma 3 is that minimizer.

*Proof.* Every term of $\Phi_\lambda$ is a positive constant times a monomial $\prod_k x_k^{\alpha_k}$, which is $\exp$ of an affine function of $y$, hence convex in $y$. The terms $a_i e^{y_i}$ are strictly convex in $y_i$, and their sum is strictly convex in $y$. The box $\ell \le x \le h$ is a box in $y$. At a point where each coordinate is optimal on its interval, each partial derivative $\partial \Psi / \partial y_i$ is 0, or is $\ge 0$ at the lower end, or is $\le 0$ at the upper end. These are the KKT conditions of a differentiable convex function on a box, which are sufficient for a global minimum. $\square$

**Theorem 1 (no duality gap).** If some sizes in the box have latest arrival time below $T$, then $\max_{\mu \in \Omega} Q(\mu) = \mathrm{OPT}(P)$, the maximum is attained at some $\mu^*$, and the unique minimizer $x(\mu^*)$ of the local resizing subproblem is the unique optimal sizing.

*Proof.* In the variables $(y, A)$, problem (P) has the convex objective $\sum_i a_i e^{y_i}$, the constraints $A_u + D_v(e^y) - A_v \le 0$, whose left sides are convex by the argument of Lemma 4, the affine constraints $A_u \le T$ and a box on $y$. Sizes with latest arrival below $T$, with $A$ slightly above the arrival times, meet all the timing constraints strictly, so Slater's condition holds. Hence the Lagrangian dual has the same value and a dual optimum $\mu^*$ is attained; by Lemma 1, $\mu^* \in \Omega$. For an optimal $(y^*, A^*)$ and $\mu^*$, the saddle point property says that $y^*$ minimizes $\mathcal L(\cdot, A^*, \mu^*) = \Psi(\cdot) + \text{const}$ over the box. By Lemma 4 this minimizer is unique, so it is $x(\mu^*)$. The primal optimum is unique because the objective is strictly convex in $y$ and the feasible set is convex. $\square$

**Corollary (certificate).** For every $\mu \in \Omega$ and every sizing $x$ that meets the target, $Q(\mu) \le \mathrm{OPT}(P) \le \sum_i a_i x_i$. So a pair whose two values are close proves that $x$ is close to optimal. The tests check this bound for the computed pair.

**Theorem 2 (cost of one round).** One sweep of local resizing, one timing pass, the update of all multipliers and the projection each take $O(n + m)$ time. A round with $S$ sweeps takes $O(S (n + m))$ time.

*Proof.* In a sweep, gate $i$ needs its load and the sum over its fanins, in $O(1 + |\mathrm{in}(i)| + |\mathrm{out}(i)|)$, which sums to $O(n + m)$. Static timing is one pass in topological order. The projection visits the gates in reverse topological order and touches each edge twice. $\square$

**What is not proved here.** The multiplier update of the implementation, which scales each edge by the ratio of the arrival time through it to the arrival time at its head (or to $T$ for an edge into the sink) and then restores flow conservation by proportional scaling, is not proved to converge. The tests measure that it reaches the grid optimum and the dual bound within a relative $10^{-3}$ on small circuits.
