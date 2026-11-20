---
title: SVD precoding turns the channel into parallel scalar channels, water-filling picks the best powers, and the result reaches the MIMO capacity
proves: [correctness]
status: full
---

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$, $w \sim \mathcal{CN}(0, N_0 I_m)$ and the power constraint $\mathrm{tr}(Q) \le P$ on the input covariance $Q = E[x x^H]$. Line L1 computes $H = U \Sigma V^H$ with $U \in \mathbb{C}^{m \times m}$ and $V \in \mathbb{C}^{n \times n}$ unitary and $\Sigma$ an $m \times n$ matrix with the singular values $s_1 \ge s_2 \ge \cdots \ge s_r > 0$ on its diagonal, where $r$ is the rank of $H$. Let $u_i$ and $v_i$ be column $i$ of $U$ and $V$. Line L4 sets $F = [\sqrt{p_1} v_1, \ldots, \sqrt{p_r} v_r]$, and the transmitter sends $x = F d$ with $E[d d^H] = I_r$.

**Theorem 1 (parallel channels).** $U_r^H H F = \mathrm{diag}(s_1 \sqrt{p_1}, \ldots, s_r \sqrt{p_r})$, where $U_r = [u_1, \ldots, u_r]$. So the output of line L6 is $z_i = s_i \sqrt{p_i}\, d_i + \nu_i$ for $i = 1, \ldots, r$, with $\nu \sim \mathcal{CN}(0, N_0 I_r)$. Also $\|F\|_F^2 = \sum_i p_i$.

*Proof.* $H v_i = U \Sigma V^H v_i = U \Sigma e_i = s_i u_i$, because the columns of $V$ are orthonormal. So $H F$ has column $i$ equal to $s_i \sqrt{p_i}\, u_i$, and $u_k^H u_i = \delta_{ki}$ gives the diagonal form. The noise term is $\nu = U_r^H w$, a linear map of a circularly symmetric Gaussian vector, with covariance $N_0 U_r^H U_r = N_0 I_r$. Finally $\|F\|_F^2 = \sum_i p_i \|v_i\|^2 = \sum_i p_i$. $\square$

So the receiver sees $r$ independent scalar channels with the gains $g_i = s_i^2 / N_0$, and the rate with Gaussian $d$ is $\sum_i \log_2(1 + g_i p_i)$. Also $F F^H = V_r \,\mathrm{diag}(p)\, V_r^H$, and $\det(I + H F F^H H^H / N_0) = \prod_i (1 + g_i p_i)$ by Theorem 1 and $\det(I + A B) = \det(I + B A)$.

**Lemma 1 (water-filling).** For gains $g_1 \ge \cdots \ge g_r > 0$ and $P > 0$, the problem "maximize $\sum_i \log_2(1 + g_i p_i)$ subject to $p_i \ge 0$ and $\sum_i p_i = P$" has the unique solution $p_i = (\mu - 1/g_i)^+$, where $\mu$ solves $\sum_i (\mu - 1/g_i)^+ = P$. The loop of `water_fill` finds this $\mu$.

*Proof.* The objective is strictly concave and the constraints are linear, so the [KKT conditions](/kkt-conditions/) are necessary and sufficient and the solution is unique. With a multiplier $\lambda$ for the sum and $\eta_i \ge 0$ for $p_i \ge 0$, stationarity reads $g_i / (1 + g_i p_i) = \lambda \ln 2 - \eta_i$. Write $\mu = 1/(\lambda \ln 2)$. If $p_i > 0$, then $\eta_i = 0$ and $p_i = \mu - 1/g_i$. If $p_i = 0$, then $g_i \le \lambda \ln 2$, that is $1/g_i \ge \mu$. Both cases give $p_i = (\mu - 1/g_i)^+$.

Now the loop. Let $a_i = 1/g_i$, so $a_1 \le \cdots \le a_r$, and let $f(t) = \sum_i (t - a_i)^+$. The function $f$ is continuous, $f(a_1) = 0$, and $f$ increases strictly for $t > a_1$ without bound, so there is a unique $\mu$ with $f(\mu) = P$, and $\mu > a_1$. Let $\mu_k = (P + a_1 + \cdots + a_k)/k$. Then $\mu_k > a_k$ holds exactly when $P > \sum_{i \le k} (a_k - a_i) = f(a_k)$, that is when $a_k < \mu$. Since the $a_i$ increase, the set of such $k$ is $\{1, \ldots, k^*\}$, where $k^*$ is the number of channels with $a_i < \mu$. The loop starts at $k = r$ and stops at the first $k$ with $\mu_k > a_k$, which is $k^*$; the case $k = 1$ always passes because $P > 0$. On the set $i \le k^*$, $\mu_{k^*}$ solves $f(t) = P$, so $\mu_{k^*} = \mu$. $\square$

**Lemma 2 (Hadamard's inequality).** For a Hermitian positive semidefinite matrix $A$, $\det A \le \prod_i A_{ii}$, with equality for a positive definite $A$ only if $A$ is diagonal.

*Proof.* If some $A_{ii} = 0$, then row $i$ and column $i$ of $A$ are zero (a $2 \times 2$ principal minor would be negative otherwise), so $\det A = 0$. Otherwise let $D = \mathrm{diag}(A_{11}, \ldots, A_{nn})$ and $B = D^{-1/2} A D^{-1/2}$. $B$ is positive semidefinite with unit diagonal, so its eigenvalues $\lambda_i \ge 0$ add up to $n$. By the inequality of arithmetic and geometric means, $\det B = \prod_i \lambda_i \le 1$, with equality only if every $\lambda_i = 1$, that is $B = I$. Then $\det A = \det D \det B \le \prod_i A_{ii}$. $\square$

**Theorem 2 (capacity).** For every $Q \succeq 0$ with $\mathrm{tr}(Q) \le P$,

$$\log_2 \det\Bigl(I_m + \frac{H Q H^H}{N_0}\Bigr) \le \sum_{i=1}^{r} \log_2(1 + g_i p_i),$$

with the water-filling powers $p_i$ of Lemma 1. The SVD precoder reaches the right side, so it reaches the capacity of the channel with $H$ known at both ends.

*Proof.* Let $\tilde Q = V^H Q V$. It is positive semidefinite with $\mathrm{tr}(\tilde Q) = \mathrm{tr}(Q) \le P$. By $\det(I + A B) = \det(I + B A)$,

$$\det\Bigl(I + \frac{U \Sigma \tilde Q \Sigma^H U^H}{N_0}\Bigr) = \det\Bigl(I + \frac{\Sigma \tilde Q \Sigma^H}{N_0}\Bigr).$$

The matrix $\Sigma \tilde Q \Sigma^H$ is zero outside its leading $r \times r$ block, and that block is $S \tilde Q_r S$ with $S = \mathrm{diag}(s_1, \ldots, s_r)$ and $\tilde Q_r$ the leading block of $\tilde Q$. Lemma 2 applied to $I + S \tilde Q_r S / N_0$ gives the bound $\prod_{i \le r} (1 + g_i \tilde Q_{ii})$. The numbers $q_i = \tilde Q_{ii}$ are nonnegative with $\sum_{i \le r} q_i \le P$, and the rate grows with each $q_i$, so by Lemma 1 the bound is at most the water-filling value. By Theorem 1 the precoder of line L4 reaches it. $\square$

The tests check Theorem 1 by $U_r^H H F$ against the diagonal and by the power $\|F\|_F^2 = P$, Theorem 2 against random covariances of trace $P$ and the log-det formula, Lemma 1 by its KKT conditions and by a fine grid over the power split of two modes, and the check values 5.1699 and 2.1699 of the area.
