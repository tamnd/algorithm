---
title: Why the selection by binary subdivision draws each sample with its weight, why one step of CONDENSATION is factored sampling of the posterior, and what the contour observation model gives
proves: [correctness]
status: full
---

Notation as on the page. The sample set at time $t - 1$ is $\{(s_j, \pi_j, c_j)\}_{j=1}^N$ with weights $\pi_j \ge 0$ and cumulative weights $c_0 = 0$, $c_j = c_{j-1} + \pi_j$. The claims say what one step computes. Whether the tracked contour follows the object depends on the dynamical model and the observation model, which are assumptions.

## Claim 1: selection draws index j with probability proportional to its weight, in O(log N)

Let $r$ be uniform on $[0, c_N]$ with $c_N > 0$, and let $j$ be the smallest index with $c_j \ge r$ (lines L1 and L2). Then $\Pr(j = k) = \pi_k / c_N$ for every $k$, and binary subdivision finds $j$ with at most $\lceil \log_2 (N + 1) \rceil$ comparisons.

*Proof.* The cumulative weights are non-decreasing, so $j = k$ holds exactly when $c_{k-1} < r \le c_k$. This is an interval of length $c_k - c_{k-1} = \pi_k$ inside $[0, c_N]$, so it has probability $\pi_k / c_N$ (the single point $r = 0$, which selects the first index with $c_j \ge 0$, has probability 0). Because the sequence is sorted, the set of indices with $c_j \ge r$ is a suffix $\{j, \ldots, N\}$, and bisection on this monotone predicate halves the candidate range at each comparison. $\square$

A sample with weight 0 is never chosen, except for the event $r = 0$ of probability 0. The implementation clamps the index to $N$, which covers rounding when $r$ equals $c_N$. The test checks the definition on 500 random values and the frequencies on 20,000 draws.

## Claim 2: one step is factored sampling of the posterior

Assume the old set represents the density $p(x_{t-1} \mid Z_{t-1})$ by the weighted empirical measure $\sum_j \pi_j \delta_{s_j}$ with $\sum_j \pi_j = 1$. Let

$$
q(x_t) = \sum_j \pi_j\, p(x_t \mid x_{t-1} = s_j)
$$

be the predicted prior. Then, given the old set:

(a) after lines L1 to L3, the new samples $s_1, \ldots, s_N$ are independent with density $q$;

(b) after lines L4 to L6, for every bounded function $g$,

$$
\sum_n \pi_n\, g(s_n) = \frac{\frac1N \sum_n g(s_n)\, p(z_t \mid s_n)}{\frac1N \sum_n p(z_t \mid s_n)} \longrightarrow \frac{\int g(x)\, p(z_t \mid x)\, q(x)\, dx}{\int p(z_t \mid x)\, q(x)\, dx}
$$

almost surely as $N \to \infty$, provided $\int p(z_t \mid x) q(x) dx > 0$. The right side is the expectation of $g$ under the posterior that Bayes' rule gives from the prior $q$ and the observation density.

*Proof.* (a) Each new sample uses its own uniform $r$ and its own noise $w$, independent of the others. By Claim 1 its parent is $s_k$ with probability $\pi_k$, and given the parent it has density $p(x_t \mid s_k)$, so its density is the mixture $q$. (b) The weights of line L4 are $p(z_t \mid s_n)$, and line L5 divides them by their sum, which gives the first equality. The numerator and the denominator are means of $N$ independent copies of $g(X) p(z_t \mid X)$ and $p(z_t \mid X)$ with $X \sim q$. These have finite means because $g$ is bounded and $p(z_t \mid x)$ is bounded (Claim 4 shows it for the model of the page). By the strong law of large numbers each mean converges almost surely to its expectation, and the quotient converges because the limit of the denominator is positive. $\square$

This is the factored sampling of Section 3 of Isard and Blake, applied once per frame. Line L7, the weighted mean, is (b) with $g(x) = x$ on the bounded image region. The claim is conditional on the old set. That the error does not grow over many frames is a result about particle filters in general, which needs conditions on the model that are not proved here; the [particle filter](/particle-filter/) page treats it.

## Claim 3: the prediction is the second-order autoregressive model

With the state $(x_{t-1}, x_t)$ and the damping $a$, line L3 computes

$$
x_{t+1} = x_t + a (x_t - x_{t-1}) + B w_t, \qquad w_t \sim N(0, I),
$$

which is $X_{t+1} - \bar X = A (X_t - \bar X) + B' w_t$ for the stacked state $X_t = (x_{t-1}, x_t)$ with $\bar X = 0$ and

$$
A = \begin{pmatrix} 0 & I \\ -a I & (1 + a) I \end{pmatrix}, \qquad B' = \begin{pmatrix} 0 \\ B \end{pmatrix}.
$$

With $B = 0$ and $a = 1$, a sample that moves by $v$ between $x_{t-1}$ and $x_t$ moves by $v$ again: the model holds a constant velocity. With $|a| < 1$ and $B = 0$ the velocity is multiplied by $a$ at each step and goes to 0.

*Proof.* The second block row of $A X_t$ is $-a x_{t-1} + (1 + a) x_t = x_t + a (x_t - x_{t-1})$, and the first block row copies $x_t$ into the new first slot. The velocity $v_{t+1} = x_{t+1} - x_t = a (x_t - x_{t-1}) = a v_t$ when $B = 0$. $\square$

This is the form of equations (10) and (11) of the paper, with $A$ fixed by hand instead of learned. The test checks the constant velocity case with zero noise.

## Claim 4: the observation density of one normal, and what it does with no features

Along one normal, let the features be at signed offsets $\nu_1, \ldots, \nu_K$ from the hypothesized contour point. The density used for that normal is

$$
p_1(\nu_1, \ldots, \nu_K) \propto 1 + \frac{1}{\sqrt{2\pi}\, \sigma \alpha} \sum_{k=1}^K \exp\Big( -\frac{\nu_k^2}{2 \sigma^2} \Big),
$$

and the density of a contour is the product over its $M$ normals (line L4). Then:

(a) The density is at least 1 and at most $1 + K / (\sqrt{2\pi} \sigma \alpha)$ per normal, so it is bounded and positive.

(b) If no normal of any hypothesis has a feature, every sample has weight $1/N$ after line L5, and the step only moves the samples by the dynamics.

(c) It comes from this model: with probability $q$ the object is not seen and all features on the normal are clutter; otherwise exactly one feature is the true edge, displaced by a normal error with standard deviation $\sigma$, and each feature is the true one with the same probability $p$. The clutter is a Poisson process with density $\lambda$ along the normal.

*Proof.* (a) Each term of the sum is in $(0, 1]$. (b) With $K = 0$ on every normal, the density is 1 for every hypothesis, so all weights are equal before and after normalization. (c) For a Poisson process with density $\lambda$ on a window of length $W$, the density of $K$ given points is $e^{-\lambda W} \lambda^K$. If the object is not seen, the $K$ features are clutter, which gives $q\, e^{-\lambda W} \lambda^K$. If feature $k$ is the true one, the other $K - 1$ are clutter, which gives $p\, e^{-\lambda W} \lambda^{K-1} \frac{1}{\sqrt{2\pi} \sigma} e^{-\nu_k^2 / (2 \sigma^2)}$. Sum over the $K + 1$ cases and divide by $q\, e^{-\lambda W} \lambda^K$, which does not depend on the hypothesis:

$$
1 + \frac{p}{q \lambda} \cdot \frac{1}{\sqrt{2\pi} \sigma} \sum_k e^{-\nu_k^2 / (2 \sigma^2)}.
$$

This is the stated form with one constant in front of the sum. Isard and Blake write it as $1 / (\sqrt{2\pi} \sigma \alpha)$ with $\alpha = q \lambda$, equation (13). $\square$

Part (b) is the "tunnelling" of the paper: when the object is hidden, the samples keep moving with the dynamics and spread, so they can find the object when it appears again. Equation (16) of the paper replaces the sum by the nearest feature only, $\exp(-\sum_m f(\nu_1(m); \mu) / (2 r M))$ with $f(\nu; \mu) = \min(\nu^2, \mu^2)$. Its logarithm is also bounded, between $-\mu^2 / (2 r)$ and 0, so Claim 2 applies to it too.

## Cost

Line L2 costs $O(\log N)$ by Claim 1, line L3 costs $O(d^2)$ for a state of dimension $d$, and line L4 costs $O(M L)$ for $M$ normals that are each probed at $2 L + 1$ points. Lines L5 to L7 cost $O(N)$ in all. So a step costs $\Theta(N (\log N + d^2 + M L))$ and holds $\Theta(N d)$ numbers.

## What is not claimed

The observation model is an assumption. Its sharpness decides how many samples survive a step: in the example on the page, moving a hypothesis by one pixel lowers its log-likelihood by about 7, so its weight falls by a factor near 1000. With so sharp a density, a sample set can lose one of two equally good modes within a few steps by chance, and Claim 2 does not prevent this for a fixed $N$. The convergence in Claim 2 is for $N \to \infty$ and says nothing about the error for a given $N$.
