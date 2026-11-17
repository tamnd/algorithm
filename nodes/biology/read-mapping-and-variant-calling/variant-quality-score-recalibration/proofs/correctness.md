---
title: EM never lowers the likelihood, and the threshold keeps the target share of the truth set
proves: [correctness]
status: full
---

A call is a vector $x \in \mathbb{R}^d$ of annotation values. A diagonal Gaussian mixture with $K$ components has weights $w_k \ge 0$ with $\sum_k w_k = 1$, means $\mu_k$ and variances $v_{kj} > 0$, and density

$$p(x) = \sum_{k=1}^{K} w_k \prod_{j=1}^{d} \frac{1}{\sqrt{2 \pi v_{kj}}} \exp\Bigl(-\frac{(x_j - \mu_{kj})^2}{2 v_{kj}}\Bigr).$$

The procedure has three parts: fit a mixture $p_+$ to the training calls (line L1), fit a mixture $p_-$ to the calls that $p_+$ scores worst (lines L2 to L4), and score each call by $\lambda(x) = \ln p_+(x) - \ln p_-(x)$ (line L5). Then it picks the threshold (line L6) and filters (line L7). Lines L2, L3, L5 and L7 compute what they say, with `log_density` evaluating $\ln p(x)$ by the log-sum-exp identity $\ln \sum_k e^{a_k} = a + \ln \sum_k e^{a_k - a}$ with $a = \max_k a_k$. What needs proof is the fitting step and the threshold.

## The fitting step

`fit_gmm` runs EM on data $y_1, \ldots, y_n$, with each variance kept at least at a floor $\varepsilon > 0$. Let $\ell(\theta) = \sum_i \ln p_\theta(y_i)$.

**Theorem 1.** Each EM round gives $\ell(\theta^{t+1}) \ge \ell(\theta^t)$.

*Proof.* The E step computes the responsibilities $\gamma_{ik} = w_k \phi_k(y_i) / p_{\theta^t}(y_i)$, where $\phi_k$ is the density of component $k$. For any $\theta$, write $\ell(\theta) = \sum_i \ln \sum_k \gamma_{ik} \frac{w_k' \phi_k'(y_i)}{\gamma_{ik}}$, with primes for the parameters $\theta$. By Jensen's inequality for the concave logarithm,

$$\ell(\theta) \ge \sum_i \sum_k \gamma_{ik} \ln \frac{w_k' \phi_k'(y_i)}{\gamma_{ik}} =: \mathcal{L}(\theta),$$

with equality at $\theta = \theta^t$, where the ratio inside is $p_{\theta^t}(y_i)$ for every $k$. So if the M step gives $\theta^{t+1}$ with $\mathcal{L}(\theta^{t+1}) \ge \mathcal{L}(\theta^t)$, then $\ell(\theta^{t+1}) \ge \mathcal{L}(\theta^{t+1}) \ge \mathcal{L}(\theta^t) = \ell(\theta^t)$.

The M step maximizes $\mathcal{L}$ over the allowed parameters. With $N_k = \sum_i \gamma_{ik}$, the terms in the weights are $\sum_k N_k \ln w_k'$, which under $\sum_k w_k' = 1$ is largest at $w_k' = N_k / n$ (Gibbs' inequality). The terms of component $k$ and coordinate $j$ are

$$-\frac12 \sum_i \gamma_{ik} \Bigl(\ln(2\pi v) + \frac{(y_{ij} - \mu)^2}{v}\Bigr).$$

For fixed $v$ this is largest at the weighted mean $\mu = \sum_i \gamma_{ik} y_{ij} / N_k$. With that mean and $S = \sum_i \gamma_{ik} (y_{ij} - \mu)^2$, the function $v \mapsto -\frac12 (N_k \ln v + S / v)$ increases for $v < S / N_k$ and decreases after, so its largest value under $v \ge \varepsilon$ is at $v = \max(\varepsilon, S / N_k)$. These are the updates of the code. A component with $N_k$ below $10^{-12}$ gets weight 0 and keeps its old mean and variance; its terms in $\mathcal{L}$ are then $N_k$ times bounded numbers, which the code drops, and the change in $\mathcal{L}$ is of the order of $10^{-12}$ times the size of the terms. $\square$

The test of the implementation checks that the traced log-likelihood never drops by more than a relative $10^{-7}$. Theorem 1 does not say that EM finds the global maximum. The result depends on the start, which the code draws from a seeded random generator.

**Corollary.** With $K = 1$, the M step after the first round gives the sample mean and the sample variance with divisor $n$ (floored at $\varepsilon$), and no later round changes them. These are the maximum likelihood estimates of one diagonal Gaussian.

*Proof.* With one component, $\gamma_{i1} = 1$ for every $i$, and the updates are the plain mean and variance. They do not depend on $\theta^t$, so the next round gives the same values. $\square$

## The threshold

For a list $s_1, \ldots, s_T$ of scores of the truth-set calls and a target $\tau \in (0, 1]$, let $\nu = \lceil \tau T \rceil$ and let $s_{(1)} \ge s_{(2)} \ge \cdots \ge s_{(T)}$ be the scores in decreasing order.

**Theorem 2.** `tranche_threshold` returns $s_{(\nu)}$, which is the largest $t$ such that at least $\nu$ of the scores are $\ge t$. So the filter of line L7 keeps at least the share $\tau$ of the truth-set calls, and no higher threshold does.

*Proof.* The code sorts the scores in decreasing order and returns entry $\nu$. The scores $\ge s_{(\nu)}$ include $s_{(1)}, \ldots, s_{(\nu)}$, so there are at least $\nu$ of them. For $t > s_{(\nu)}$, every score $\ge t$ is among $s_{(1)}, \ldots, s_{(\nu - 1)}$, since the others are at most $s_{(\nu)} < t$, so there are at most $\nu - 1$ of them. The kept share is at least $\nu / T \ge \tau$. $\square$

The code subtracts $10^{-12}$ inside the ceiling so that a product such as $0.99 \times 100$ that comes out a little above 99 in floating point still gives $\nu = 99$.

**What the guarantee covers.** Theorem 2 is about the truth set, and it holds for any scores. The share of all true variants that pass, and the share of false calls that pass, depend on how well the two mixtures separate the calls, which no theorem here bounds. In the simulation test the two kinds of calls come from separated clusters, and both shares come out as wanted.

## Cost

One EM round costs $O(n K d)$ for $n$ points, so fitting costs $O(I n K d)$ for $I$ rounds. Scoring all $N$ calls costs $O(N (K_+ + K_-) d)$, and the sorts cost $O(N \log N)$.
