---
title: The MMSE filter minimizes the mean squared error, maximizes the SINR of each stream among linear filters, and has the bias 1 - (N0/Es) P_kk
proves: [correctness]
status: full
---

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$, $w \sim \mathcal{CN}(0, N_0 I_m)$ independent of $x$, and $E[x] = 0$, $E[x x^H] = E_s I_n$. Let $a = N_0 / E_s > 0$, $G = H^H H + a I_n$, $P = G^{-1}$ and $W = P H^H$, as in lines L1 and L2. Let $h_k$ be column $k$ of $H$. $G$ is Hermitian positive definite, because $u^H G u = \|H u\|^2 + a \|u\|^2 > 0$ for $u \ne 0$, so $P$ exists and is Hermitian positive definite.

**Theorem 1 (minimum mean squared error).** For every $n \times m$ matrix $V$, $E\|V y - x\|^2 \ge E\|W y - x\|^2 = N_0\, \mathrm{tr}(P)$, and the error covariance of $W$ is $E[(W y - x)(W y - x)^H] = N_0 P$.

*Proof.* The second moments are $R_{yy} = E[y y^H] = E_s H H^H + N_0 I$ and $R_{xy} = E[x y^H] = E_s H^H$. The error $e = W y - x$ is orthogonal to the data: $E[e\, y^H] = W R_{yy} - R_{xy} = E_s (P H^H H H^H + a P H^H) - E_s H^H = E_s P (H^H H + a I) H^H - E_s H^H = 0$. For any $V$, write $V y - x = e + (V - W) y$. The cross term $E[e^H (V - W) y] = \mathrm{tr}((V - W) E[y e^H]) = 0$, so $E\|V y - x\|^2 = E\|e\|^2 + E\|(V - W) y\|^2 \ge E\|e\|^2$. For the covariance, $E[e e^H] = E[e (W y - x)^H] = -E[e x^H]$ by the orthogonality, and $-E[e x^H] = R_{xx} - W R_{yx} = E_s I - E_s P H^H H = E_s P (G - H^H H) = E_s a P = N_0 P$. $\square$

**Lemma 2 (push-through).** $W = H^H (H H^H + a I_m)^{-1}$.

*Proof.* $(H^H H + a I) H^H = H^H (H H^H + a I)$. Multiply on the left by $P$ and on the right by $(H H^H + a I)^{-1}$. $\square$

Let $R = E_s H H^H + N_0 I_m = E_s (H H^H + a I)$, the covariance of $y$, and let $R_k = R - E_s h_k h_k^H$, the covariance of the interference and the noise seen by stream $k$. By Lemma 2, $W = E_s H^H R^{-1}$, so row $k$ of $W$ is $w_k^H = E_s h_k^H R^{-1}$.

**Theorem 3 (maximum SINR, bias and SINR formula).** Let $s_k = E_s h_k^H R_k^{-1} h_k$. Then:
1. Row $k$ of $W$ is a positive multiple of $h_k^H R_k^{-1}$.
2. Among all row vectors $v^H \ne 0$, the SINR $E_s |v^H h_k|^2 / (v^H R_k v)$ of the output $v^H y$ is at most $s_k$, with equality for $v^H \propto h_k^H R_k^{-1}$. So row $k$ of $W$ maximizes the SINR.
3. $\beta_k = (W H)_{kk} = s_k / (1 + s_k) = 1 - a P_{kk}$, and so $s_k = 1 / (a P_{kk}) - 1$.

*Proof.* (1) By the Sherman-Morrison formula, $R^{-1} h_k = R_k^{-1} h_k / (1 + s_k)$, since $R = R_k + E_s h_k h_k^H$ and $R_k$ is positive definite. So $w_k^H = E_s h_k^H R_k^{-1} / (1 + s_k)$.

(2) Write $u = R_k^{1/2} v$. By the Cauchy-Schwarz inequality, $|v^H h_k|^2 = |u^H R_k^{-1/2} h_k|^2 \le \|u\|^2\, h_k^H R_k^{-1} h_k = (v^H R_k v)\, s_k / E_s$, with equality if and only if $u \propto R_k^{-1/2} h_k$, that is, $v \propto R_k^{-1} h_k$.

(3) By (1), $(W H)_{kk} = w_k^H h_k = E_s h_k^H R_k^{-1} h_k / (1 + s_k) = s_k / (1 + s_k)$. On the other side, $W H = P H^H H = P (G - a I) = I - a P$, so $(W H)_{kk} = 1 - a P_{kk}$. Solving $1 - a P_{kk} = s_k / (1 + s_k)$ gives $1 + s_k = 1 / (a P_{kk})$. $\square$

The scale of a filter row does not change its SINR, so dividing by $\beta_k$ in line L6 keeps the SINR $s_k$ and makes the output unbiased: $E[z_k / \beta_k \mid x_k] = x_k$, because the other streams and the noise have mean zero. For a constellation with more than one amplitude, the decision regions of the nearest point rule are built for the points $x_k$ themselves, so the unbiased output is the right input to the slicer. For PSK, the regions are cones from the origin and a positive scale does not change the decision.

**Corollary 4 (never worse than ZF in SINR).** If $H$ has full column rank, $s_k \ge (E_s/N_0) / [(H^H H)^{-1}]_{kk}$, the ZF post-detection SNR of stream $k$.

*Proof.* Row $k$ of the ZF filter is a linear filter with no interference and the SNR $(E_s/N_0)/[(H^H H)^{-1}]_{kk}$. By Theorem 3(2), no linear filter has a larger SINR than $s_k$. $\square$

**Theorem 5 (ZF limit, exact without noise).** If $H$ has full column rank, $W \to (H^H H)^{-1} H^H$ and $\beta_k \to 1$ as $N_0 \to 0$. With $w = 0$ and $N_0$ small enough, the decisions of lines L4 to L6 equal $x$.

*Proof.* Matrix inversion is continuous at the invertible matrix $H^H H$, so $P \to (H^H H)^{-1}$ and $W \to (H^H H)^{-1} H^H$, and $a P_{kk} \to 0$. With $w = 0$, $z / \beta_k \to x_k$ for each $k$ because $(H^H H)^{-1} H^H H x = x$. Each $x_k$ is at distance at least $d_{\min} / 2 > 0$ from the boundary of its decision region, so for $N_0$ small enough every output lies in the right region. $\square$

The tests check Theorem 1 by a simulated MSE with 16-QAM against $N_0 P_{kk}$, Lemma 2 on random channels with $n > m$ and $n \le m$, Theorem 3 against the direct SINR formula, Theorem 5 against the ZF filter, and the numbers of the example on the page.
