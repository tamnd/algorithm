---
title: Each CPD iteration does not increase the negative log-likelihood
proves: [correctness]
status: full
---

We use the notation of the page. The data points are $X = (x_1, \ldots, x_n)$ and the centroids are $Y = (y_1, \ldots, y_K)$, all in $\mathbb{R}^D$. For a transformation $T$ and a variance $\sigma^2 > 0$, the mixture density is

$$p(x \mid T, \sigma^2) = \frac{w}{n} + \frac{1 - w}{K} \sum_{k=1}^{K} g_k(x), \qquad g_k(x) = (2\pi\sigma^2)^{-D/2} \exp\!\left(-\frac{|x - T(y_k)|^2}{2\sigma^2}\right),$$

with a fixed outlier weight $0 \le w < 1$. The negative log-likelihood is $E(T, \sigma^2) = -\sum_{i} \log p(x_i \mid T, \sigma^2)$. We assume exact arithmetic.

**Claim.** Let $(T_j, \sigma_j^2)$ be the parameters before one iteration of the rigid loop (lines L3 to L8) and $(T_{j+1}, \sigma_{j+1}^2)$ the parameters after it. If the weight sum $N_P = \sum_{k,i} P_{ki}$ is positive, the new scale $s$ is positive and the new variance is positive, then $E(T_{j+1}, \sigma_{j+1}^2) \le E(T_j, \sigma_j^2)$. The same holds for the affine M-step, and for the non-rigid M-step when $E$ is replaced by $E + \frac{\lambda}{2} \operatorname{tr}(W^{\mathsf T} G W)$ and $G$ is positive definite.

**Lemma 1 (the EM bound).** Fix the old parameters $\theta_j = (T_j, \sigma_j^2)$ and let $P_{ki}$ be the posteriors of line L3, that is $P_{ki} = \frac{1 - w}{K} g_k(x_i) / p(x_i \mid \theta_j)$ evaluated at $\theta_j$, and $P_{0i} = \frac{w}{n} / p(x_i \mid \theta_j)$ for the outlier component. Define

$$Q(\theta) = \frac{1}{2\sigma^2} \sum_{k,i} P_{ki} |x_i - T(y_k)|^2 + \frac{N_P D}{2} \log \sigma^2 .$$

Then $E(\theta) - E(\theta_j) \le Q(\theta) - Q(\theta_j)$ for every $\theta$.

*Proof.* For each $i$, the posteriors $P_{0i}, P_{1i}, \ldots, P_{Ki}$ are positive and sum to 1. Write $a_{ki}(\theta)$ for the term of component $k$ in $p(x_i \mid \theta)$, so $p(x_i \mid \theta) = \sum_{k=0}^{K} a_{ki}(\theta)$ and $P_{ki} = a_{ki}(\theta_j) / p(x_i \mid \theta_j)$. By the concavity of the logarithm ([Jensen's inequality](/jensens-inequality/)),

$$\log \frac{p(x_i \mid \theta)}{p(x_i \mid \theta_j)} = \log \sum_{k=0}^{K} P_{ki} \frac{a_{ki}(\theta)}{a_{ki}(\theta_j)} \ge \sum_{k=0}^{K} P_{ki} \log \frac{a_{ki}(\theta)}{a_{ki}(\theta_j)} .$$

The outlier term $a_{0i} = w/n$ does not depend on $\theta$, so its log ratio is 0. For $k \ge 1$, $\log a_{ki}(\theta) = \log\frac{1-w}{K} - \frac{D}{2} \log(2\pi\sigma^2) - \frac{|x_i - T(y_k)|^2}{2\sigma^2}$. Sum over $i$ and change the sign. The constants cancel, and what is left is $E(\theta) - E(\theta_j) \le Q(\theta) - Q(\theta_j)$. $\square$

So any step that does not increase $Q$ does not increase $E$. It remains to show that each M-step does not increase $Q$.

**Lemma 2 (the rigid M-step).** Lines L5 to L8 return a global minimizer of $Q$ over $R \in SO(D)$, $s > 0$, $t \in \mathbb{R}^D$ and $\sigma^2 > 0$, when $N_P > 0$, the new $s$ is positive and the new $\sigma^2$ is positive.

*Proof.* Fix $R$ and $s$. The sum $\sum_{k,i} P_{ki} |x_i - s R y_k - t|^2$ is a convex quadratic in $t$. Its gradient is zero at $t = \mu_x - s R \mu_y$, with the weighted means of line L5, so this $t$ is optimal for every $R$ and $s$. Put it in. With the centered points $\hat x_i = x_i - \mu_x$ and $\hat y_k = y_k - \mu_y$, the sum becomes

$$S(R, s) = \sum_i (P^{\mathsf T}\mathbf 1)_i |\hat x_i|^2 - 2 s \operatorname{tr}(A^{\mathsf T} R) + s^2 \sum_k (P \mathbf 1)_k |\hat y_k|^2, \qquad A = \hat X^{\mathsf T} P^{\mathsf T} \hat Y,$$

because $|R \hat y_k| = |\hat y_k|$. For every fixed $s > 0$, $S$ is least when $\operatorname{tr}(A^{\mathsf T} R)$ is greatest. With the SVD $A = U \Sigma V^{\mathsf T}$, the maximum of $\operatorname{tr}(A^{\mathsf T} R)$ over $SO(D)$ is attained at $R = U C V^{\mathsf T}$ with $C = \operatorname{diag}(1, \ldots, 1, \det(U V^{\mathsf T}))$. This is the theorem of Umeyama (1991), proved on the [Kabsch algorithm](/kabsch-algorithm/) page. Line L7 computes this $R$, and it does not depend on $s$. For this $R$, $S$ is a quadratic in $s$ with a positive leading term, least at $s = \operatorname{tr}(A^{\mathsf T} R) / \sum_k (P\mathbf 1)_k |\hat y_k|^2$, which is the $s$ of line L7. (With the scale fixed to 1, this step is skipped and $s = 1$ is the only choice.) Finally, for a fixed value $S > 0$, the function $S / (2\sigma^2) + (N_P D / 2) \log \sigma^2$ has the derivative $-S/(2\sigma^4) + N_P D/(2\sigma^2)$, which is negative below $\sigma^2 = S/(N_P D)$ and positive above it. Line L8 sets $\sigma^2 = S/(N_P D)$ with the least value of $S$. For every fixed $\sigma^2$, $Q$ increases with $S$, so no other choice of $(R, s, t, \sigma^2)$ gives a smaller $Q$. $\square$

**Lemma 3 (the affine M-step).** The step $B = A (\hat Y^{\mathsf T} \operatorname{d}(P\mathbf 1) \hat Y)^{-1}$, $t = \mu_x - B \mu_y$, $\sigma^2 = S(B)/(N_P D)$ minimizes $Q$ over all $B$, $t$ and $\sigma^2$, when $\hat Y^{\mathsf T} \operatorname{d}(P\mathbf 1) \hat Y$ is invertible.

*Proof.* The translation is eliminated as in Lemma 2. What is left, $\sum_{k,i} P_{ki} |\hat x_i - B \hat y_k|^2$, is a convex quadratic in $B$ whose gradient $-2(A - B \hat Y^{\mathsf T} \operatorname{d}(P\mathbf 1)\hat Y)$ vanishes at the stated $B$. The variance step is as in Lemma 2. $\square$

**Lemma 4 (the non-rigid M-step).** Let $G$ be positive definite and let $\sigma^2$ be fixed. The $W$ that solves $(\operatorname{d}(P\mathbf 1) G + \lambda \sigma^2 I) W = P X - \operatorname{d}(P\mathbf 1) Y$ minimizes $Q(Y + G W, \sigma^2) + \frac{\lambda}{2} \operatorname{tr}(W^{\mathsf T} G W)$ over $W$.

*Proof.* The function is $\frac{1}{2\sigma^2}\sum_{k,i} P_{ki}|x_i - y_k - (GW)_k|^2 + \frac{\lambda}{2}\operatorname{tr}(W^{\mathsf T} G W)$ plus a constant. It is convex in $W$: the first part is a convex quadratic of the linear map $W \mapsto GW$, and the second part is convex because $G$ is positive semidefinite. Its gradient is $G \left[ \frac{1}{\sigma^2}(\operatorname{d}(P\mathbf 1)(Y + GW) - P X) + \lambda W \right]$. The stated $W$ makes the bracket zero, so the gradient is zero, and a stationary point of a convex function is a global minimizer. $\square$

The non-rigid loop then sets $\sigma^2$ to the minimizer for the new $W$, as in Lemma 2. Two steps that each do not increase $Q + \frac{\lambda}{2}\operatorname{tr}(W^{\mathsf T} G W)$ give a total step that does not increase it. The penalty does not depend on $\sigma^2$ or on $P$, so Lemma 1 holds with the penalty added to both $E$ and $Q$.

*Proof of the claim.* The old parameters are one candidate of each M-step, so by Lemmas 2, 3 and 4, $Q(\theta_{j+1}) \le Q(\theta_j)$ (with the penalty in the non-rigid case). By Lemma 1, $E(\theta_{j+1}) - E(\theta_j) \le Q(\theta_{j+1}) - Q(\theta_j) \le 0$. $\square$

**What the claim does not say.** The values of $E$ do not increase, and they are bounded below while $\sigma^2$ stays away from 0, so they converge. This does not mean that the parameters converge to the global minimum of $E$. EM can stop at a local minimum or a saddle point, and the result depends on the start, as the example on the page shows. When the data fit exactly, $\sigma^2$ goes to 0 and $E$ goes to $-\infty$; the code stops at the floor sigma2_min.

**Floating point.** The code computes the sums of line L3 with a shift by the least squared distance, so the posteriors are finite even when all the Gaussian terms underflow. The tests check the nonincreasing property with a relative slack of $10^{-9}$.
