---
title: The EM step of MLESAC never lowers the likelihood, and MLESAC keeps the sampled model of best score
proves: [correctness]
status: full
---

We use the notation of the page. For a fixed model $\theta$, write $a_i = \phi_\sigma(r(\theta, x_i)) > 0$ and $b = 1/v > 0$, and let $D_i(\gamma) = \gamma a_i + (1 - \gamma) b$ and $\ell(\gamma) = \sum_{i=1}^n \log D_i(\gamma) = -L(\theta, \gamma)$ for $\gamma \in [0, 1]$. The model of computation is the real RAM with $\exp$ and $\log$ as exact operations.

**Claim.** (a) $\ell$ is concave on $[0, 1]$. (b) For $0 < \gamma < 1$, the EM step of lines L10 and L11, $\gamma' = \frac{1}{n} \sum_i \gamma a_i / D_i(\gamma)$, satisfies $0 < \gamma' < 1$, $\gamma' = \gamma + \gamma (1 - \gamma) \ell'(\gamma) / n$ and $\ell(\gamma') \ge \ell(\gamma)$. A $\gamma \in (0, 1)$ is a fixed point of the step if and only if it maximizes $\ell$ on $[0, 1]$. (c) At each test of line L2, $\theta^*$ has the least score $L$ among the models of the samples drawn so far, where each score uses the $\gamma$ of $m$ EM steps from $1/2$, and the loop ends after at most $k_{\max}$ rounds.

**Lemma 1 (concavity).** Part (a) holds.

*Proof.* $D_i$ is affine in $\gamma$ and positive on $[0, 1]$, so $\ell''(\gamma) = -\sum_i (a_i - b)^2 / D_i(\gamma)^2 \le 0$. $\square$

**Lemma 2 (the step as a gradient step).** For $0 < \gamma < 1$, $\gamma' - \gamma = \gamma (1 - \gamma) \ell'(\gamma) / n$, and $0 < \gamma' < 1$.

*Proof.* $\gamma a_i - \gamma D_i(\gamma) = \gamma (1 - \gamma)(a_i - b)$, so $\gamma' - \gamma = \frac{1}{n} \sum_i \frac{\gamma a_i - \gamma D_i(\gamma)}{D_i(\gamma)} = \frac{\gamma (1 - \gamma)}{n} \sum_i \frac{a_i - b}{D_i(\gamma)}$, and the sum is $\ell'(\gamma)$. Each posterior $z_i = \gamma a_i / D_i(\gamma)$ lies strictly between 0 and 1 because $\gamma a_i > 0$ and $(1 - \gamma) b > 0$, so their mean $\gamma'$ does too. $\square$

**Lemma 3 (ascent).** For $0 < \gamma < 1$, $\ell(\gamma') - \ell(\gamma) \ge n \big(\gamma' \log \frac{\gamma'}{\gamma} + (1 - \gamma') \log \frac{1 - \gamma'}{1 - \gamma}\big) \ge 0$.

*Proof.* With $z_i = \gamma a_i / D_i(\gamma)$ and $1 - z_i = (1 - \gamma) b / D_i(\gamma)$,
$$\frac{D_i(\gamma')}{D_i(\gamma)} = z_i \frac{\gamma'}{\gamma} + (1 - z_i) \frac{1 - \gamma'}{1 - \gamma}.$$
The logarithm is concave, so by Jensen's inequality with the weights $z_i$ and $1 - z_i$, $\log \frac{D_i(\gamma')}{D_i(\gamma)} \ge z_i \log \frac{\gamma'}{\gamma} + (1 - z_i) \log \frac{1 - \gamma'}{1 - \gamma}$. Summing over $i$ and using $\sum_i z_i = n \gamma'$ gives the first inequality. The right side is $n$ times the Kullback-Leibler divergence between the Bernoulli laws with parameters $\gamma'$ and $\gamma$, which is nonnegative by Gibbs' inequality. $\square$

**Lemma 4 (fixed points).** A $\gamma \in (0, 1)$ is a fixed point of the step if and only if it maximizes $\ell$ on $[0, 1]$.

*Proof.* By Lemma 2, $\gamma' = \gamma$ if and only if $\ell'(\gamma) = 0$, since $\gamma (1 - \gamma) > 0$. By Lemma 1, $\ell$ is concave, so an interior point with $\ell'(\gamma) = 0$ is a maximum on $[0, 1]$, and an interior maximum has $\ell'(\gamma) = 0$. $\square$

Lemmas 2 to 4 prove (b). Lines L8 to L11 start at $\gamma = 1/2$ and apply the step $m$ times, so by Lemma 2 every value stays in $(0, 1)$ and by Lemma 3 the likelihood does not decrease along the way.

**Proof of (c).** Before the first round, $L^* = \infty$. In a round, either line L6 skips the sample and nothing changes, or line L12 computes the score $L$ of the new model with its own $\gamma$. Line L13 replaces $\theta^*$ exactly when $L < L^*$, so after line L14 $L^*$ is the least score among the old models and the new one. The value $k$ starts at $k_{\max}$ and line L15 sets it only to values at most $k_{\max}$; each round increases $t$ by 1, so after $k_{\max}$ rounds the test of line L2 fails. $\square$

**Remark (sampling).** If a model of least score is the model of every sample inside its set of likely inliers $I$, and the samples are independent, then $K$ rounds find it with probability at least $1 - (1 - q)^K$, where $q$ is the probability that a sample lies in $I$, by the argument for MSAC. The count of line L15 uses the estimate $\gamma$ of the best model so far, which is not a bound on the inlier ratio of the best model overall, so the stopping rule is a heuristic.
