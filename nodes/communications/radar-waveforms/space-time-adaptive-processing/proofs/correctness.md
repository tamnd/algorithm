---
title: SMI space-time adaptive processing solves R w = v, the weight R^-1 v gives the largest output SINR, the AMF statistic has a constant false alarm rate when R is known, and Brennan's rule gives the clutter rank for an integer beta
proves: [correctness]
status: full
---

The notation is that of the page. An array of $M$ elements receives $P$ pulses, and a snapshot is a vector of length $D = MP$, indexed by $pM + m$ for pulse $p$ and element $m$. The steering vector of the target is $v \ne 0$. Line L1 forms $\hat{R} = \frac{1}{T}\sum_{t=1}^{T} x_t x_t^H$ from $T$ training snapshots, line L2 adds $\delta I$ with $\delta \ge 0$, line L3 factors $\hat{R} + \delta I = G G^H$ with $G$ lower triangular, line L4 solves for $w$, line L5 forms $y = w^H x$ for the cell under test, and line L6 forms $\Lambda = |y|^2 / (v^H w)$.

**Lemma 1 (the matrix of line L3 is positive definite).** $\hat{R}$ is Hermitian and positive semidefinite. $\hat{R} + \delta I$ is positive definite if $\delta > 0$, or if $\delta = 0$ and the training snapshots span $\mathbb{C}^D$, which needs $T \ge D$.

*Proof.* Each $x_t x_t^H$ is Hermitian, and $u^H x_t x_t^H u = |x_t^H u|^2 \ge 0$. So $u^H \hat{R} u = \frac{1}{T} \sum_t |x_t^H u|^2 \ge 0$. With $\delta > 0$, $u^H(\hat{R} + \delta I)u \ge \delta \|u\|^2 > 0$ for $u \ne 0$. With $\delta = 0$, the sum is zero only if $u$ is orthogonal to every $x_t$, which for spanning snapshots means $u = 0$. $T$ vectors span at most $T$ dimensions. $\square$

So the Cholesky factor $G$ of line L3 exists, with a positive real diagonal, and the implementation raises an error when the matrix is not positive definite.

**Lemma 2 (line L4).** The forward substitution $a_i = (v_i - \sum_{k<i} G_{ik} a_k)/G_{ii}$ and the back substitution $w_i = (a_i - \sum_{k>i} \overline{G_{ki}}\, w_k)/\overline{G_{ii}}$ give the unique $w$ with $(\hat{R} + \delta I) w = v$.

*Proof.* Row $i$ of $Ga = v$ is $\sum_{k \le i} G_{ik} a_k = v_i$, and the forward step solves it for $a_i$ once $a_0, \dots, a_{i-1}$ are known; $G_{ii} \ne 0$. $G^H$ is upper triangular with $(G^H)_{ik} = \overline{G_{ki}}$, and row $i$ of $G^H w = a$ is $\sum_{k \ge i} \overline{G_{ki}}\, w_k = a_i$, solved in the order $i = D-1, \dots, 0$. Then $G G^H w = G a = v$. $G$ is invertible, so the solution is unique. $\square$

**Theorem 1 (the optimum weight).** Let $R$ be a Hermitian positive definite covariance of the interference plus noise, and define the output SINR of a weight $u \ne 0$ for a target $v$ of unit power as $\mathrm{SINR}(u) = |u^H v|^2 / (u^H R u)$. Then

$$\mathrm{SINR}(u) \le v^H R^{-1} v,$$

with equality if and only if $u$ is a nonzero multiple of $R^{-1} v$.

*Proof.* $\langle a, b \rangle_R = a^H R b$ is an inner product. Put $g = R^{-1} v$, so $u^H v = u^H R g = \langle u, g \rangle_R$. The Cauchy-Schwarz inequality gives $|u^H v|^2 \le (u^H R u)(g^H R g) = (u^H R u)(v^H R^{-1} v)$, with equality exactly when $u$ and $g$ are proportional. $\square$

By Lemma 2, SMI returns the optimum weight for the matrix $\hat{R} + \delta I$ that it estimates. Its SINR in the true $R$ is $\mathrm{SINR}(w)$, and the ratio $\rho = \mathrm{SINR}(w) / (v^H R^{-1} v) \le 1$ is the loss of the estimate. For $\delta = 0$, $T \ge D$ and Gaussian training data with covariance $R$, Reed, Mallett and Brennan (1974) showed that $\rho$ has a beta distribution with mean $(T + 2 - D)/(T + 1)$. We do not reprove that result here. The tests check the mean by simulation.

**Theorem 2 (the AMF statistic with a known covariance).** Let $w = R^{-1} v$ for the true $R$, and let the cell under test hold only interference, $x \sim \mathcal{CN}(0, R)$. Then $\Lambda = |w^H x|^2 / (v^H w)$ is exponential with mean 1, so $P(\Lambda > \eta) = e^{-\eta}$ for every $R$.

*Proof.* $y = w^H x$ is a linear function of a circular Gaussian vector, so $y \sim \mathcal{CN}(0, w^H R w)$ and $w^H R w = v^H R^{-1} R R^{-1} v = v^H R^{-1} v = v^H w$. So $\Lambda = |y|^2 / E|y|^2$, and the squared magnitude of a $\mathcal{CN}(0, 1)$ variable is exponential with mean 1. $\square$

$\Lambda$ does not change when $w$ is multiplied by a nonzero constant, so the scale of the weight does not matter.

**Theorem 3 (Brennan's rule for an integer beta).** Let the clutter patches $c = 1, \dots, Q$ have spatial frequencies $f_c$, distinct modulo 1, the Doppler $\beta f_c$ with an integer $1 \le \beta \le M$, and powers $\gamma_c > 0$. The steering vector of patch $c$ is $v_c[pM + m] = e^{j 2\pi f_c (\beta p + m)}$. Then $R_c = \sum_c \gamma_c v_c v_c^H$ has rank $\min(Q, K)$ with $K = M + \beta(P - 1)$.

*Proof.* The entry $pM + m$ of $v_c$ depends only on $q = \beta p + m$, which runs over $0, \dots, K - 1$. Let $e_c[q] = e^{j 2\pi f_c q}$ for $q = 0, \dots, K-1$, and let $S$ be the $D \times K$ matrix with $S[pM + m][\beta p + m] = 1$ and zeros elsewhere, so $v_c = S e_c$. Each $q$ in $0, \dots, K-1$ is $\beta p + m$ for some valid $p$ and $m$: if $q \le \beta(P-1)$, take $p = \lfloor q/\beta \rfloor$ and $m = q - \beta p < \beta \le M$; otherwise take $p = P - 1$ and $m = q - \beta(P - 1) \le M - 1$. So each column of $S$ has a 1, the columns have disjoint supports, and $S$ has rank $K$. Then $R_c = S V \Gamma V^H S^H$, where $V$ is the $K \times Q$ matrix with columns $e_c$ and $\Gamma = \mathrm{diag}(\gamma_c)$. $V$ is a Vandermonde matrix in the distinct nodes $e^{j 2\pi f_c}$, so its rank is $\min(Q, K)$. $V \Gamma V^H = (V\Gamma^{1/2})(V\Gamma^{1/2})^H$ has the rank of $V$, and multiplying by $S$ on the left and $S^H$ on the right keeps the rank, because $S$ has full column rank. $\square$

For a non-integer $\beta$ the rank is close to $M + \beta(P-1)$ in the sense that the other eigenvalues are small, which is the form of Brennan's rule used in practice. Theorem 3 covers only the exact case. $\blacksquare$
