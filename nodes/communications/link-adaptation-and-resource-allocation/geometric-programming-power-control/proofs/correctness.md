---
title: The GP forms of power control are convex in log powers, and the condensation loop raises the sum rate to a KKT point
proves: [correctness]
status: full
---

The links, gains $G_{ij}$, noise powers $\sigma_i > 0$, limits $\bar p_i$, the interference plus noise $N_i(p) = \sum_{j \ne i} G_{ij} p_j + \sigma_i$ and $D_i(p) = N_i(p) + G_{ii} p_i$ are as on the page. All powers are positive, and $y = \log p$ entrywise.

## Part 1: the GP forms are convex

**Lemma 1 (log-sum-exp is convex).** Let $f(y) = \log \sum_{m=1}^M e^{z_m}$ with $z_m = b_m + a_m^T y$. Then $\nabla f(y) = \sum_m w_m a_m$ and $\nabla^2 f(y) = \sum_m w_m (a_m - \bar a)(a_m - \bar a)^T \succeq 0$, where $w_m = e^{z_m} / \sum_l e^{z_l}$ and $\bar a = \sum_m w_m a_m$.

*Proof.* $\partial f / \partial y_k = \sum_m e^{z_m} a_{mk} / \sum_l e^{z_l} = \sum_m w_m a_{mk}$. Differentiating $w_m$ gives $\partial w_m / \partial y_r = w_m (a_{mr} - \bar a_r)$, so $\partial^2 f / \partial y_k \partial y_r = \sum_m w_m a_{mk}(a_{mr} - \bar a_r) = \sum_m w_m a_{mk} a_{mr} - \bar a_k \bar a_r$. Since $\sum_m w_m = 1$, this equals $\sum_m w_m (a_{mk} - \bar a_k)(a_{mr} - \bar a_r)$, a weighted covariance matrix with weights $w_m > 0$. For every $v$, $v^T \nabla^2 f\, v = \sum_m w_m ((a_m - \bar a)^T v)^2 \ge 0$. $\square$

A posynomial $P(x) = \sum_m c_m x^{a_m}$ in $x = e^y$ has $\log P(e^y) = \log \sum_m e^{\log c_m + a_m^T y}$, which is convex by Lemma 1.

**Lemma 2 (the three problems are GPs).** For $p > 0$:

1. $\mathrm{SINR}_i(p) \ge \gamma_i$ if and only if $(\gamma_i / G_{ii})\, N_i(p)\, p_i^{-1} \le 1$, and the left side is a posynomial in $p$.
2. $\mathrm{SINR}_i(p) \ge t$ if and only if $t\, N_i(p) / (G_{ii} p_i) \le 1$, a posynomial in $(p, t)$, and maximizing $t$ is minimizing the monomial $t^{-1}$.
3. $-\sum_i \log \mathrm{SINR}_i(p) = \sum_i \log\big(N_i(p) / (G_{ii} p_i)\big)$, a sum of logs of posynomials.

*Proof.* (1) $G_{ii} p_i / N_i(p) \ge \gamma_i$ and $N_i(p) > 0$, $p_i > 0$ give $\gamma_i N_i(p) / (G_{ii} p_i) \le 1$, and the steps reverse. Expanding, $\gamma_i N_i(p) / (G_{ii} p_i) = \sum_{j \ne i} (\gamma_i G_{ij} / G_{ii})\, p_j p_i^{-1} + (\gamma_i \sigma_i / G_{ii})\, p_i^{-1}$, a sum of monomials with positive coefficients (terms with $G_{ij} = 0$ are dropped). (2) is (1) with $\gamma_i$ replaced by the variable $t$, which multiplies each monomial by $t^1$. (3) is the definition of the SINR. The limits $p_i \le \bar p_i$ are the monomial constraints $p_i / \bar p_i \le 1$. $\square$

So in the variable $y$ (and $\log t$), each of the three problems minimizes a convex function, a sum of log-sum-exp functions or a linear function, subject to constraints $f_k(y) \le 0$ with each $f_k$ a log-sum-exp, which is convex. Every local minimum of a convex problem is global.

**Lemma 3 (the barrier method stops within the gap).** Let $f_0$ and $f_1, \ldots, f_m$ be convex and differentiable, and let $y^*(t)$ minimize $\phi_t(y) = f_0(y) - \frac{1}{t} \sum_k \log(-f_k(y))$ over the strictly feasible set. Then $f_0(y^*(t)) - \mathrm{OPT} \le m/t$, where $\mathrm{OPT}$ is the optimal value of $\min f_0$ subject to $f_k \le 0$.

*Proof.* At the minimizer, $\nabla f_0(y^*) + \sum_k \lambda_k \nabla f_k(y^*) = 0$ with $\lambda_k = 1/(t\, (-f_k(y^*))) > 0$. So $y^*$ is a stationary point of the convex function $L(y) = f_0(y) + \sum_k \lambda_k f_k(y)$, hence its minimizer. For every feasible $y$, $f_0(y) \ge f_0(y) + \sum_k \lambda_k f_k(y) = L(y) \ge L(y^*) = f_0(y^*) + \sum_k \lambda_k f_k(y^*) = f_0(y^*) - m/t$. Taking the infimum over feasible $y$ gives $\mathrm{OPT} \ge f_0(y^*) - m/t$. $\square$

The code divides $t f_0 - \sum_k \log(-f_k)$ by $t$, which does not change the minimizer. Each Newton step with backtracking keeps the iterate strictly feasible, since the barrier is $+\infty$ outside, and decreases $\phi_t$; the centering stops when the Newton decrement is below a small tolerance, so $y$ is a minimizer of $\phi_t$ to working accuracy. The outer loop stops when $m/t$ is below the gap tolerance, so by Lemma 3 the returned objective is within that tolerance of the global optimum, up to the centering error.

## Part 2: the condensation loop

**Lemma 4 (condensation).** Fix $p > 0$ and link $i$. Write $D_i(q) = \sum_{m} u_m(q)$ with the terms $u_0(q) = \sigma_i$ and $u_j(q) = G_{ij} q_j$ for the $j$ with $G_{ij} > 0$, and put $\alpha_m = u_m(p) / D_i(p)$. Then $\tilde D_i(q) = \prod_m (u_m(q)/\alpha_m)^{\alpha_m}$ is a monomial, and for all $q > 0$

$$\tilde D_i(q) \le D_i(q), \qquad \tilde D_i(p) = D_i(p), \qquad \nabla_y \log \tilde D_i = \nabla_y \log D_i \text{ at } q = p.$$

*Proof.* Each $u_m$ is a monomial and $\alpha_m > 0$, so the product is a monomial. The weights $\alpha_m$ are positive and sum to 1. Since $\log$ is concave, Jensen's inequality gives $\log \sum_m \alpha_m (u_m/\alpha_m) \ge \sum_m \alpha_m \log(u_m / \alpha_m)$, which is $\log D_i(q) \ge \log \tilde D_i(q)$. At $q = p$, $u_m(p)/\alpha_m = D_i(p)$ for every $m$, so $\tilde D_i(p) = \prod_m D_i(p)^{\alpha_m} = D_i(p)$. In $y$, $\log \tilde D_i(e^y) = \text{const} + \sum_j \alpha_j y_j$, with gradient $(\alpha_j)_j$ (and $\alpha_j = 0$ if $G_{ij} = 0$). By Lemma 1, the gradient of $\log D_i(e^y)$ is $\sum_m w_m a_m$, where $a_m$ is the unit vector $e_j$ for $u_j$ and $0$ for $u_0$, and $w_m = u_m(q)/D_i(q)$; at $q = p$ this is $(\alpha_j)_j$. $\square$

Let $R(q) = \sum_i \log(N_i(q) / D_i(q))$, so the sum rate is $-R(q)/\ln 2$, and let $\tilde R_p(q) = \sum_i \log(N_i(q) / \tilde D_i(q))$ be the objective of line L5 built at $p$. Let $\mathcal F$ be the set of $q > 0$ with $\gamma^{\min}_i N_i(q) / (G_{ii} q_i) \le 1$ and $q_i \le \bar p_i$; by Lemma 2 it is exactly the feasible set of (1).

**Theorem 1 (monotone and feasible).** Let $p \in \mathcal F$, and let $p' \in \mathcal F$ satisfy $\tilde R_p(p') \le \tilde R_p(p)$, which holds for the exact minimizer of line L5 and for any solver output that does not do worse than its start. Then $R(p') \le R(p)$, so the sum rate at $p'$ is at least the sum rate at $p$.

*Proof.* By Lemma 4, $\tilde D_i \le D_i$ everywhere, so $\tilde R_p(q) \ge R(q)$ for all $q$, and $\tilde R_p(p) = R(p)$. Then $R(p') \le \tilde R_p(p') \le \tilde R_p(p) = R(p)$. $\square$

The barrier solver starts line L5 at the current $p$ and only accepts steps that lower $\phi_t$; at the end, $p'$ is within the gap of the minimum of $\tilde R_p$ over $\mathcal F$, which is at most $\tilde R_p(p)$, so the sum rate can fall by at most the gap tolerance in one round. The sum rate is bounded above on $\mathcal F$ (by $\sum_i \log_2(1 + G_{ii} \bar p_i / \sigma_i)$), so the sequence of sum rates converges, and the stopping test of line L6 is met after finitely many rounds.

**Theorem 2 (fixed points are KKT points).** Suppose $p \in \mathcal F$ minimizes $\tilde R_p$ over $\mathcal F$, and a constraint qualification holds for the convex form of $\mathcal F$ at $p$ (for example, $\mathcal F$ has a strictly feasible point, which the algorithm assumes at line L1). Then $p$ satisfies the KKT conditions of (1) in the variables $y$.

*Proof.* In $y$, line L5 is a convex problem, and with a strictly feasible point (Slater's condition) its minimizer satisfies the KKT conditions: there are $\lambda_k \ge 0$ with $\nabla_y \tilde R_p(y) + \sum_k \lambda_k \nabla f_k(y) = 0$ and $\lambda_k f_k(y) = 0$, where $f_k$ are the logs of the constraint posynomials. The constraints of line L5 are those of (1). By Lemma 4, $\nabla_y \log \tilde D_i = \nabla_y \log D_i$ at $p$, and the $N_i$ parts are the same in both objectives, so $\nabla_y \tilde R_p = \nabla_y R$ at $p$. Hence the same $\lambda_k$ satisfy the KKT conditions of (1), written as the minimization of $R$ in $y$ subject to $f_k(y) \le 0$. Since $y = \log p$ is a smooth change of variables with an invertible Jacobian, these are also the KKT conditions of (1) in $p$. $\square$

KKT points of (1) need not be global optima, because $R$ is not convex in $y$. The example on the page with strong coupling has two of them, with sum rates $2.8435$ and $2.8502$.

## The algorithm

Line L1 picks $p \in \mathcal F$ with slack. Lines L3 and L4 build $\tilde D_i$ as in Lemma 4. Line L5 minimizes $\tilde R_p$ over $\mathcal F$ by the barrier method from the start $p$, so by Part 1 its answer is optimal for that GP up to the gap. Line L6 stops when the sum rate rises by at most $\epsilon$, and line L7 moves to the new point. By Theorem 1 the sum rate does not decrease from round to round (up to the gap of the inner solver), every iterate is in $\mathcal F$, and the loop ends. By Theorem 2, a point at which the loop makes no further progress is a KKT point of (1).
