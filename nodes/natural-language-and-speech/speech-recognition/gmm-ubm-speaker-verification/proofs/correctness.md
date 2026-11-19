---
title: GMM-UBM enrollment is a MAP step and the score is the average log likelihood ratio
proves: [correctness]
status: full
---

We use the notation of the page. The universal background model (UBM) is a mixture of $M$ Gaussians with weights $c_m > 0$, means $\mu_m \in \mathbb{R}^d$ and diagonal covariances $\Sigma_m$. All logs are natural logs. For a mixture $\lambda$ write $p(x \mid \lambda) = \sum_m c_m \mathcal{N}(x; \mu_m(\lambda), \Sigma_m)$, and $a_m(x, \lambda) = \log\big(c_m \mathcal{N}(x; \mu_m(\lambda), \Sigma_m)\big)$ for the terms in log form.

**Lemma 1 (log-sum-exp is exact).** For real numbers $a_1, \ldots, a_M$ with maximum $a^*$, $\log \sum_m e^{a_m} = a^* + \log \sum_m e^{a_m - a^*}$, and the inner sum lies in $[1, M]$.

*Proof.* Multiply and divide the sum by $e^{a^*}$. Each term $e^{a_m - a^*}$ is in $(0, 1]$, and the term of the largest $a_m$ is 1. $\square$

So the code evaluates $\log p(x \mid \lambda)$ without forming the densities, whose values can be below the smallest double. The posterior of line L1 is $\gamma_m(t) = e^{a_m - z}$ with $z = \log p(x_t \mid \text{UBM})$, which is the exact posterior $c_m \mathcal{N}(x_t; \mu_m, \Sigma_m) / p(x_t \mid \text{UBM})$.

**Theorem 2 (enrollment is one MAP-EM step).** Put the prior $\mu^{s}_m \sim \mathcal{N}(\mu_m, \Sigma_m / r)$, independent over $m$, on the means of the speaker model, and keep its weights and covariances equal to those of the UBM. Start MAP-EM at the UBM. Then lines L1 to L4 compute the means after one MAP-EM step, and this step does not lower $\log p(X \mid \lambda) + \log p(\lambda)$ for the enrollment frames $X$.

*Proof.* At the start, the current model is the UBM, so the E-step posteriors are the $\gamma_m(t)$ of line L1, and $n_m$ and $E_m$ of line L2 are the occupancy and the data mean. With $\alpha_m = n_m / (n_m + r)$, line L4 gives

$$\hat\mu_m = \alpha_m E_m + (1 - \alpha_m) \mu_m = \frac{\sum_t \gamma_m(t) x_t + r \mu_m}{n_m + r},$$

and for $n_m = 0$ it keeps $\mu_m$, which is the same formula. This is the maximizer of the penalized auxiliary function with $\tau = r$, by Lemma 1 of the proof on the [MAP speaker adaptation](/map-speaker-adaptation/) page, and that page's Theorem 2 gives the monotonicity. $\square$

**Theorem 3 (the score).** Under the assumption that the frames are independent given the model, line L6 computes

$$\Lambda(Y) = \frac{1}{T} \log \frac{p(y_1, \ldots, y_T \mid \text{speaker})}{p(y_1, \ldots, y_T \mid \text{UBM})},$$

the log likelihood ratio of the two hypotheses divided by the number of frames.

*Proof.* With independent frames, $\log p(Y \mid \lambda) = \sum_t \log p(y_t \mid \lambda)$, and by Lemma 1 each term is computed exactly in real arithmetic. The difference of two sums is the sum of the differences, and line L6 divides it by $T$. $\square$

**Corollary 4 (the decision rule).** If the speaker model and the UBM were the true distributions of the target speaker and of the impostors, then for a fixed $T$ the test "accept when $\Lambda(Y) \ge \theta$" is a likelihood ratio test with the threshold $e^{T\theta}$ on the ratio. By the [Neyman-Pearson lemma](/neyman-pearson-lemma/), no other test with the same false alarm rate has a lower miss rate.

*Proof.* $\Lambda(Y) \ge \theta$ if and only if $p(Y \mid \text{speaker}) / p(Y \mid \text{UBM}) \ge e^{T \theta}$, because $x \mapsto e^{T x}$ is increasing. $\square$

The models are only estimates and the frames are not independent, so in practice the optimality is not exact, and the threshold is set on development data. The division by $T$ makes the scores of utterances of different lengths more comparable, but it is a heuristic: the true log likelihood ratio grows with $T$.

**Proposition 5 (fast scoring).** Let $S_t$ be the set of the $C$ components with the largest $a_m(y_t, \text{UBM})$. If $C = M$, the top-$C$ score equals $\Lambda(Y)$. For any $C$, the UBM term of the top-$C$ score is within $\log(M / C)$ of the exact term: $\log p(y_t \mid \text{UBM}) - \log(M/C) \le \log \sum_{m \in S_t} e^{a_m(y_t, \text{UBM})} \le \log p(y_t \mid \text{UBM})$.

*Proof.* For $C = M$ every sum is over all components. For $C < M$, the upper bound holds because the terms are positive. The $C$ largest of $M$ positive numbers have at least the fraction $C/M$ of their sum, which gives the lower bound. $\square$

There is no such bound for the speaker term: a speaker component that moved far from its UBM component can be large at a frame where the UBM component is not among the top $C$. So the top-$C$ score can be above or below $\Lambda(Y)$. The method relies on MAP adaptation keeping each speaker component close to its UBM component, which holds when $n_m$ is small next to $r$ or the data mean is close to $\mu_m$.
