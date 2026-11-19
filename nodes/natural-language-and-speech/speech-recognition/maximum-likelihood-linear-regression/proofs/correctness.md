---
title: The MLLR update maximizes the EM auxiliary function and never lowers the likelihood
proves: [correctness]
status: full
---

We use the notation of the page. There are $M$ Gaussians with speaker independent means $\mu_m \in \mathbb{R}^n$, diagonal covariances $\Sigma_m = \mathrm{diag}(\sigma^2_{m,1}, \ldots, \sigma^2_{m,n})$ with $\sigma^2_{m,i} > 0$, and mixture weights $c_m$. Gaussian $m$ belongs to the regression class $r(m)$. The extended mean is $\xi_m = (1, \mu_m)^\top \in \mathbb{R}^{n+1}$. A set of transforms $\mathcal{W} = (W_1, \ldots, W_R)$, each of size $n \times (n+1)$, gives the adapted means $\hat\mu_m = W_{r(m)} \xi_m$. Row $i$ of $W_r$ is $w_{r,i}^\top$, so $\hat\mu_{m,i} = w_{r(m),i}^\top \xi_m$. All logs are natural logs. Write $p(O \mid \mathcal{W})$ for the likelihood of the frames $o_1, \ldots, o_T$ under the mixture with the adapted means; the weights and covariances do not change.

Fix the current transforms $\mathcal{W}^{\mathrm{old}}$ and let $\gamma_m(t)$ be the posterior of Gaussian $m$ at frame $t$ under them, as in line L4. Let $\mathrm{occ}_m = \sum_t \gamma_m(t)$ and $s_m = \sum_t \gamma_m(t) o_t$, as in line L5. The auxiliary function is

$$\mathcal{Q}(\mathcal{W}) = \sum_{t=1}^{T} \sum_{m=1}^{M} \gamma_m(t) \log \big( c_m\, \mathcal{N}(o_t; W_{r(m)} \xi_m, \Sigma_m) \big).$$

**Lemma 1 (the auxiliary function separates by rows).** There is a constant $K$ that does not depend on $\mathcal{W}$ such that

$$\mathcal{Q}(\mathcal{W}) = K - \frac{1}{2} \sum_{r=1}^{R} \sum_{i=1}^{n} \big( w_{r,i}^\top G_{r,i}\, w_{r,i} - 2\, w_{r,i}^\top k_{r,i} \big),$$

with $G_{r,i} = \sum_{m: r(m) = r} (\mathrm{occ}_m / \sigma^2_{m,i})\, \xi_m \xi_m^\top$ and $k_{r,i} = \sum_{m: r(m) = r} (s_{m,i} / \sigma^2_{m,i})\, \xi_m$, the matrices of line L7.

*Proof.* With a diagonal covariance,

$$\log \mathcal{N}(o_t; \hat\mu_m, \Sigma_m) = -\frac{1}{2} \sum_{i=1}^{n} \Big( \log(2\pi\sigma^2_{m,i}) + \frac{(o_{t,i} - \hat\mu_{m,i})^2}{\sigma^2_{m,i}} \Big).$$

The terms $\log c_m$, $\log(2\pi\sigma^2_{m,i})$ and $o_{t,i}^2 / \sigma^2_{m,i}$ do not depend on $\mathcal{W}$; they go into $K$. What is left is

$$-\frac{1}{2} \sum_m \sum_i \frac{1}{\sigma^2_{m,i}} \sum_t \gamma_m(t) \big( \hat\mu_{m,i}^2 - 2 o_{t,i} \hat\mu_{m,i} \big) = -\frac{1}{2} \sum_m \sum_i \frac{\mathrm{occ}_m\, \hat\mu_{m,i}^2 - 2 s_{m,i}\, \hat\mu_{m,i}}{\sigma^2_{m,i}}.$$

Put $\hat\mu_{m,i} = w_{r(m),i}^\top \xi_m$, so $\hat\mu_{m,i}^2 = w_{r(m),i}^\top \xi_m \xi_m^\top w_{r(m),i}$, and group the Gaussians by class. $\square$

Each pair $(r, i)$ owns its own vector $w_{r,i}$, and no other term of the sum depends on it. So $\mathcal{Q}$ is a sum of $nR$ quadratic functions in disjoint variables, and it is maximized by maximizing each one alone.

**Lemma 2 (when the system has one solution).** Each $G_{r,i}$ is symmetric and positive semidefinite. It is positive definite if and only if the extended means $\xi_m$ of the Gaussians of class $r$ with $\mathrm{occ}_m > 0$ span $\mathbb{R}^{n+1}$. This holds if and only if these Gaussians include $n+1$ means that are affinely independent.

*Proof.* For $v \in \mathbb{R}^{n+1}$, $v^\top G_{r,i} v = \sum_m (\mathrm{occ}_m / \sigma^2_{m,i}) (v^\top \xi_m)^2 \ge 0$, and each weight is positive when $\mathrm{occ}_m > 0$. The sum is 0 exactly when $v$ is orthogonal to every $\xi_m$ with $\mathrm{occ}_m > 0$. Such a nonzero $v$ exists if and only if these $\xi_m$ do not span $\mathbb{R}^{n+1}$. Finally, the vectors $(1, \mu_m)$ span $\mathbb{R}^{n+1}$ if and only if the points $\mu_m$ are not all in one affine hyperplane, that is, if and only if $n+1$ of them are affinely independent. $\square$

The condition does not depend on $i$. If it fails, line L8 meets a singular system, and the code raises an error. A recognizer then uses a smaller set of classes, so that each class has enough data.

**Theorem 1 (the M-step).** If every $G_{r,i}$ is positive definite, the transforms of line L8, $w_{r,i} = G_{r,i}^{-1} k_{r,i}$, are the unique maximizer of $\mathcal{Q}$.

*Proof.* By Lemma 1 it is enough to maximize $f(w) = -\frac{1}{2}(w^\top G w - 2 w^\top k)$ for each pair, with $G$ positive definite by Lemma 2. Let $w^* = G^{-1} k$. For any $w$, with $d = w - w^*$,

$$f(w) = f(w^*) - \frac{1}{2} d^\top G d,$$

which one checks by expanding both sides and using $G w^* = k$. The last term is negative unless $d = 0$. $\square$

**Theorem 2 (the likelihood does not decrease).** Let $\mathcal{W}^{\mathrm{new}}$ be the transforms of line L8, computed from the statistics of $\mathcal{W}^{\mathrm{old}}$. Then $\log p(O \mid \mathcal{W}^{\mathrm{new}}) \ge \log p(O \mid \mathcal{W}^{\mathrm{old}})$.

*Proof.* Write $p(o_t, m \mid \mathcal{W}) = c_m \mathcal{N}(o_t; W_{r(m)} \xi_m, \Sigma_m)$. For each frame, $\gamma_m(t) = p(o_t, m \mid \mathcal{W}^{\mathrm{old}}) / p(o_t \mid \mathcal{W}^{\mathrm{old}})$ is a probability distribution over $m$. For any $\mathcal{W}$, by the concavity of log (Jensen's inequality),

$$\log \frac{p(o_t \mid \mathcal{W})}{p(o_t \mid \mathcal{W}^{\mathrm{old}})} = \log \sum_m \gamma_m(t) \frac{p(o_t, m \mid \mathcal{W})}{p(o_t, m \mid \mathcal{W}^{\mathrm{old}})} \ge \sum_m \gamma_m(t) \log \frac{p(o_t, m \mid \mathcal{W})}{p(o_t, m \mid \mathcal{W}^{\mathrm{old}})}.$$

Sum over $t$: $\log p(O \mid \mathcal{W}) - \log p(O \mid \mathcal{W}^{\mathrm{old}}) \ge \mathcal{Q}(\mathcal{W}) - \mathcal{Q}(\mathcal{W}^{\mathrm{old}})$. The old transforms are one of the candidates over which line L8 maximizes, because the old means are $W^{\mathrm{old}}_{r(m)} \xi_m$ with the same $\xi_m$. So $\mathcal{Q}(\mathcal{W}^{\mathrm{new}}) \ge \mathcal{Q}(\mathcal{W}^{\mathrm{old}})$ by Theorem 1, and the right side is at least 0 for $\mathcal{W} = \mathcal{W}^{\mathrm{new}}$. $\square$

The argument needs that each iteration estimates the transform from the speaker independent means $\xi_m$, with the posteriors of the current adapted model. It is the same in an HMM system, where $\gamma_m(t)$ is the posterior of state and Gaussian $m$ from the forward-backward algorithm and the sum over $m$ in the proof is a sum over state sequences and Gaussians.

**Remark (what is not claimed).** EM converges to a stationary point of the likelihood, which need not be the global maximum. With full covariances, the rows do not separate, because the quadratic form couples all coordinates of $\hat\mu_m$; the maximizer then solves one linear system in all $n(n+1)$ entries of $W_r$ at once. In floating point, Gaussian elimination with partial pivoting gives the solution of a nearby system, so the computed $W$ satisfies Theorem 1 only up to rounding.
