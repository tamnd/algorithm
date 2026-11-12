---
title: The UMAP bandwidth equation, the fuzzy union and the SGD steps are correct
proves: [correctness]
status: full
---

We use the notation of the page. UMAP has no theorem about the quality of the map. What can be proved is that each step computes what it says it computes. We prove three facts: the bandwidth search finds the unique $\sigma_i$, the fuzzy union is a symmetric membership in $[0, 1]$, and the SGD steps follow the gradient of the stated cross entropy terms.

## Part 1: the bandwidth search

Fix a point $i$ with neighbor distances $d_1, \ldots, d_k$ and $\rho = \min_j d_j$. Let $\delta_j = d_j - \rho \ge 0$, and let $t$ be the number of $j$ with $\delta_j = 0$ (so $t \ge 1$). Define

$$f(\sigma) = \sum_{j=1}^{k} e^{-\delta_j / \sigma}, \qquad \sigma > 0.$$

**Lemma 1.** If some $\delta_j > 0$, then $f$ is continuous and strictly increasing, with $f(\sigma) \to t$ as $\sigma \to 0^+$ and $f(\sigma) \to k$ as $\sigma \to \infty$. So $f(\sigma) = \log_2 k$ has exactly one solution if and only if $t < \log_2 k < k$.

*Proof.* A term with $\delta_j = 0$ is the constant 1. A term with $\delta_j > 0$ has derivative $(\delta_j/\sigma^2) e^{-\delta_j/\sigma} > 0$, tends to 0 as $\sigma \to 0^+$ and tends to 1 as $\sigma \to \infty$. Add the terms. The intermediate value theorem gives a solution when $\log_2 k$ lies strictly between the two limits, and strict monotonicity makes it unique. Outside that interval no $\sigma$ gives the value. $\square$

Since $t \ge 1$ and $\log_2 k < k$ for all $k \ge 1$, a solution exists when $k \ge 3$ and the nearest distance is not tied: $\log_2 3 \approx 1.585 > 1$. For $k = 2$ the target is $1 = t$, which is reached only in the limit $\sigma \to 0$.

**Lemma 2.** The search on the page finds $\sigma^*$ to any tolerance. While no upper bound is known it doubles $\sigma$; once $f(\sigma) > \log_2 k$ it bisects.

*Proof.* By Lemma 1, $f(\sigma) < \log_2 k$ means $\sigma < \sigma^*$, and $f(\sigma) > \log_2 k$ means $\sigma > \sigma^*$. So the bracket $[\text{lo}, \text{hi}]$ always holds $\sigma^*$. Doubling from 1 passes $\sigma^*$ after at most $\lceil \log_2 \sigma^* \rceil + 1$ steps. After that each step halves the bracket, and $f$ is continuous, so $f(\sigma)$ converges to $\log_2 k$. $\square$

Then $a_{ij} = e^{-\delta_j/\sigma_i} \in (0, 1]$, and $a_{ij} = 1$ for the nearest neighbor. So each point is fully joined to at least one other point. This is the *local connectivity* assumption of the paper.

## Part 2: the fuzzy union

For $a, b \in [0, 1]$ let $a \oplus b = a + b - ab = 1 - (1 - a)(1 - b)$.

**Lemma 3.** $a \oplus b = b \oplus a$, and $\max(a, b) \le a \oplus b \le \min(1, a + b)$. So $w_{ij} = a_{ij} \oplus a_{ji}$ is symmetric, lies in $[0, 1]$, is 0 exactly when $a_{ij} = a_{ji} = 0$, and is 1 when either membership is 1.

*Proof.* Symmetry is clear. $a \oplus b - a = b(1 - a) \ge 0$, and the same for $b$. $a \oplus b \le a + b$ since $ab \ge 0$, and $a \oplus b \le 1$ since $(1-a)(1-b) \ge 0$. The product $(1-a)(1-b)$ is 1 exactly when $a = b = 0$, and 0 when $a = 1$ or $b = 1$. $\square$

If $a_{ij}$ and $a_{ji}$ are read as the probabilities of two independent events, $a_{ij} \oplus a_{ji}$ is the probability that at least one of them happens. This reading motivates the formula. It does not prove that the formula is the right one for the data.

## Part 3: the SGD steps

Let $v(d) = 1/(1 + a\, d^{2b})$ with $a, b > 0$, and write $s = \|y_i - y_j\|^2$, so $d^{2b} = s^b$. The fuzzy cross entropy between the graph and the map is

$$\mathrm{CE} = \sum_{i \ne j} \Big[ w_{ij} \ln \frac{w_{ij}}{v_{ij}} + (1 - w_{ij}) \ln \frac{1 - w_{ij}}{1 - v_{ij}} \Big].$$

The parts that depend on $y$ are $-w_{ij} \ln v_{ij}$ (attraction) and $-(1 - w_{ij}) \ln(1 - v_{ij})$ (repulsion).

**Lemma 4.**

$$\nabla_{y_i} \big[-\ln v\big] = \frac{2ab\, s^{b-1}}{1 + a s^b} (y_i - y_j), \qquad \nabla_{y_i} \big[-\ln(1 - v)\big] = -\frac{2b}{s\,(1 + a s^b)} (y_i - y_j).$$

*Proof.* $-\ln v = \ln(1 + a s^b)$, whose derivative in $s$ is $ab\, s^{b-1}/(1 + a s^b)$. Next, $1 - v = a s^b / (1 + a s^b)$, so $-\ln(1 - v) = -\ln a - b \ln s + \ln(1 + a s^b)$. Its derivative in $s$ is

$$-\frac{b}{s} + \frac{ab\, s^{b-1}}{1 + a s^b} = -\frac{b}{s} \Big(1 - \frac{a s^b}{1 + a s^b}\Big) = -\frac{b}{s\,(1 + a s^b)}.$$

In both cases multiply by $\nabla_{y_i} s = 2(y_i - y_j)$. $\square$

So the attractive step $y_i \leftarrow y_i + \alpha\, c_{\text{attr}} (y_i - y_j)$ with $c_{\text{attr}} = -2ab\, s^{b-1}/(1 + a s^b)$ is a step down the gradient of $-\ln v_{ij}$, and the move of $y_j$ by the opposite vector is the step for $y_j$, since $s$ is symmetric in $y_i$ and $y_j$. The repulsive step with $c_{\text{rep}} = 2b/((\varepsilon + s)(1 + a s^b))$ is a step down the gradient of $-\ln(1 - v_{ic})$ when $\varepsilon = 0$. The constant $\varepsilon = 0.001$ and the clip of each coordinate to $[-4, 4]$ only bound the step near $s = 0$.

**Lemma 5.** If edge $(i, j)$ is used with probability $w_{ij}$, the expected attractive step is $\alpha$ times minus the gradient of the attractive term $-w_{ij} \ln v_{ij}$.

*Proof.* The step is $-\alpha \nabla[-\ln v_{ij}]$ with probability $w_{ij}$ and 0 otherwise. Take the expectation. $\square$

## What is not claimed

- The repulsion uses a few points (5 by default) drawn uniformly for each sampled edge, not the weight $1 - w_{ij}$ on every pair. So the SGD of the reference method is not an unbiased estimate of the gradient of CE. Damrich and Hamprecht (2021) compute the function that it does minimize in expectation, and show that it differs from CE.
- The target $\log_2 k$, the shift by $\rho_i$, the fuzzy union, the curve $1/(1 + a d^{2b})$ and the value of `min_dist` are design choices. The paper motivates them with fuzzy simplicial sets and a functor between categories, but that theory gives no bound on any error of the map and no guarantee that clusters or distances in the map are those of the data.
- The cost is not convex, and the result depends on the start and on the random samples. We do not claim convergence to a minimum.
