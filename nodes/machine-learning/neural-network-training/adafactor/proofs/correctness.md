---
title: The factored second moment is the best rank one fit, keeps the row and column sums, and is exact for rank one matrices
proves: [correctness]
status: full
---

**Setting.** $V$ is an $n \times m$ matrix with positive entries, $R = V1_m$ its row sums, $C = 1_n^\top V$ its column sums, and $S = 1_n^\top R = C1_m$ the sum of all entries. The factored estimate is $\hat{V} = RC/S$, the matrix with entries $R_iC_j/S$. The I-divergence (generalized Kullback-Leibler divergence) between positive matrices is $D(V \Vert W) = \sum_{i,j} \bigl(V_{ij}\log(V_{ij}/W_{ij}) - V_{ij} + W_{ij}\bigr)$.

**Claim 1 (best rank one fit).** Over all matrices $W = rc^\top$ with $r \in \mathbb{R}_{>0}^n$, $c \in \mathbb{R}_{>0}^m$, the I-divergence $D(V \Vert W)$ is minimized exactly when $W = \hat{V}$.

*Proof.* Write $r_i = e^{a_i}$ and $c_j = e^{b_j}$. Then
$$D = \sum_{i,j}\bigl(V_{ij}\log V_{ij} - V_{ij}(a_i + b_j) - V_{ij} + e^{a_i + b_j}\bigr),$$
a sum of affine functions of $(a, b)$ and of exponentials of affine functions, so $D$ is convex in $(a, b)$ and every stationary point is a global minimum. The derivatives are $\partial D/\partial a_i = -R_i + r_i\sum_j c_j$ and $\partial D/\partial b_j = -C_j + c_j\sum_i r_i$. The choice $r = R$, $c = C/S$ makes both zero, because $\sum_j c_j = 1$ and $\sum_i r_i = S$. So $\hat{V} = RC^\top/S$ is a minimizer. Conversely, at any stationary point $r_i = R_i/\sum_j c_j$ and $c_j = C_j/\sum_i r_i$; adding the first equations over $i$ gives $(\sum_i r_i)(\sum_j c_j) = S$, so $r_ic_j = R_iC_j/S$. Every minimizer gives the same matrix $\hat{V}$. $\square$

**Claim 2 (sums are kept).** $\hat{V}1_m = R$ and $1_n^\top\hat{V} = C$.

*Proof.* $\sum_j R_iC_j/S = R_i S/S = R_i$, and in the same way $\sum_i R_iC_j/S = C_j$. $\square$

**Claim 3 (exact for rank one).** If $V = uw^\top$ with positive $u, w$, then $\hat{V} = V$.

*Proof.* $R = u(\sum_j w_j)$, $C = (\sum_i u_i)w^\top$ and $S = (\sum_i u_i)(\sum_j w_j)$, so $R_iC_j/S = u_iw_j$. $\square$

**Claim 4 (the running averages).** Let $V_t$ be the exponential average that an unfactored method would keep, $V_t = \hat{\beta}_{2t}V_{t-1} + (1 - \hat{\beta}_{2t})(G_t^2 + \epsilon_1 1_n1_m^\top)$ with $V_0 = 0$. Then the $R_t$ and $C_t$ of Algorithm 4 are the row and column sums of $V_t$, so $\hat{V}_t$ of the algorithm is the factored estimate of $V_t$. If $\hat{\beta}_{21} = 0$, as with $\hat{\beta}_{2t} = 1 - t^{-0.8}$, the weights of the average add to $1$ at every $t \ge 1$, so no bias correction is needed.

*Proof.* Row and column sums are linear, and $R_t$, $C_t$ follow the same recurrence as $V_t1_m$ and $1_n^\top V_t$ from the same start $0$. For the weights: $G_i^2$ gets weight $(1 - \hat{\beta}_{2i})\prod_{k=i+1}^t\hat{\beta}_{2k}$, and these add to $1 - \prod_{k=1}^t\hat{\beta}_{2k}$, which is $1$ when $\hat{\beta}_{21} = 0$. $\square$

**Claim 5 (update clipping).** $\hat{U} = U/\max(1, \operatorname{RMS}(U)/d)$ satisfies $\operatorname{RMS}(\hat{U}) = \min(\operatorname{RMS}(U), d)$ and has the direction of $U$.

*Proof.* RMS is positively homogeneous: if $\operatorname{RMS}(U) \le d$ the divisor is $1$; otherwise $\operatorname{RMS}(\hat{U}) = \operatorname{RMS}(U)\,d/\operatorname{RMS}(U) = d$. $\square$

**Consequences.** Claims 1 and 4 say that Adafactor divides by the rank one matrix closest, in I-divergence, to the second moment estimate that Adam without momentum would keep, and Claim 3 says that nothing is lost when that matrix is rank one. In particular, on the first step $\hat{\beta}_{21} = 0$, so if the gradient is a rank one matrix $G = ab^\top$, then $\hat{V}_1 = G^2 + \epsilon_1$ up to the $\epsilon_1$ term, and with $\epsilon_1 = 0$ the update direction is $\operatorname{sign}(G)$. The state is the $n + m$ numbers of $R$ and $C$. Claim 1 is a statement about the fit, not about convergence of the optimizer; the paper gives no convergence theorem.
