---
title: Correctness of the statistical model VAD
proves: [correctness]
status: full
---

We prove the three exact statements of the page: the form of the bin ratio and its optimality for known parameters, the meaning of the smoothed statistic $G(n)$ as posterior odds, and the special case without memory.

## Lemma 1 (the bin ratio)

Let $X$ be complex Gaussian with mean 0 and variance $v$, with density $p(X) = \frac{1}{\pi v} e^{-|X|^2 / v}$. Under $H_0$, $v = \lambda$; under $H_1$, $v = \lambda(1 + \xi)$ with $\xi \ge 0$. With $\gamma = |X|^2 / \lambda$,

$$\log \frac{p(X \mid H_1)}{p(X \mid H_0)} = \frac{\gamma \xi}{1 + \xi} - \log(1 + \xi).$$

*Proof.* The ratio is $\frac{\lambda}{\lambda(1 + \xi)} \exp\left(\frac{|X|^2}{\lambda} - \frac{|X|^2}{\lambda(1 + \xi)}\right)$. The exponent is $\gamma (1 - \frac{1}{1 + \xi}) = \gamma \xi / (1 + \xi)$. Take the log. $\square$

Under $H_1$ the variance is $\lambda + \lambda\xi$ because $S$ and $N$ are independent complex Gaussians and their variances add.

**Monotonicity.** For $\xi > 0$ the derivative with respect to $\gamma$ is $\xi / (1 + \xi) > 0$, so $\log \Lambda_k$ increases strictly with $\gamma_k$. For $\xi = 0$ it is identically 0.

## Theorem 1 (the frame test is most powerful for known parameters)

Let $\lambda_k$ and $\xi_k$ be known, and let the bins be independent under both hypotheses. For every level $\epsilon$, the test that decides $H_1$ when $\sum_k \log \Lambda_k > c$, with $c$ chosen so that $P(\text{decide } H_1 \mid H_0) = \epsilon$, has the largest $P(\text{decide } H_1 \mid H_1)$ among all tests with $P(\text{decide } H_1 \mid H_0) \le \epsilon$.

*Proof.* By independence, the likelihood ratio of the whole frame is $\prod_k \Lambda_k$, and its log is the sum. Under $H_0$ the sum has a continuous distribution (it is an affine function of the independent exponential variables $\gamma_k$ with positive coefficients, for the bins with $\xi_k > 0$), so a $c$ with exactly the level $\epsilon$ exists. The Neyman-Pearson lemma states that a test that rejects $H_0$ exactly when the likelihood ratio exceeds a constant, at level $\epsilon$, is most powerful at that level. $\square$

## Theorem 2 (the smoothed statistic is the posterior odds)

Let $q_1, q_2, \dots$ be a Markov chain on $\{0, 1\}$ with transitions $a_{ij}$ ($a_{00} = 1 - a_{01}$, $a_{11} = 1 - a_{10}$, $0 < a_{01}, a_{10} < 1$), started from its stationary law $\pi_1 = a_{01} / (a_{01} + a_{10})$, $\pi_0 = a_{10} / (a_{01} + a_{10})$. Let the frames $X(n)$ be independent given the states, with $X(n)$ depending only on $q_n$, and let $\Lambda(n) = p(X(n) \mid q_n = 1) / p(X(n) \mid q_n = 0)$. Define $G(0) = a_{01} / a_{10}$ and

$$G(n) = \Lambda(n) \frac{a_{01} + a_{11} G(n - 1)}{a_{00} + a_{10} G(n - 1)}.$$

Then for every $n \ge 1$, $G(n) = \frac{P(q_n = 1 \mid X(1), \dots, X(n))}{P(q_n = 0 \mid X(1), \dots, X(n))}$.

*Proof.* Let $f_n(j) = p(X(1), \dots, X(n), q_n = j)$, the forward variables. They satisfy $f_1(j) = \pi_j\, p(X(1) \mid j)$ and $f_n(j) = p(X(n) \mid j) \sum_i f_{n-1}(i)\, a_{ij}$. The posterior odds equal $f_n(1) / f_n(0)$, since both posteriors have the same denominator $p(X(1), \dots, X(n))$. We show $f_n(1) / f_n(0) = G(n)$ by induction.

For $n = 1$: $f_1(1) / f_1(0) = \Lambda(1)\, \pi_1 / \pi_0 = \Lambda(1)\, a_{01} / a_{10}$. The recursion gives $G(1) = \Lambda(1) \frac{a_{01} + a_{11} a_{01} / a_{10}}{a_{00} + a_{01}} = \Lambda(1) \frac{a_{01}(a_{10} + a_{11})}{a_{10}(a_{00} + a_{01})} = \Lambda(1) \frac{a_{01}}{a_{10}}$, since $a_{10} + a_{11} = a_{00} + a_{01} = 1$.

For $n \ge 2$, divide numerator and denominator by $f_{n-1}(0)\, p(X(n) \mid 0)$:

$$\frac{f_n(1)}{f_n(0)} = \frac{p(X(n) \mid 1) (f_{n-1}(0) a_{01} + f_{n-1}(1) a_{11})}{p(X(n) \mid 0) (f_{n-1}(0) a_{00} + f_{n-1}(1) a_{10})} = \Lambda(n) \frac{a_{01} + a_{11} G(n - 1)}{a_{00} + a_{10} G(n - 1)},$$

using $f_{n-1}(1) / f_{n-1}(0) = G(n - 1)$ from the hypothesis. $\square$

So the decision $G(n) > 1$ is the maximum a posteriori decision for frame $n$ given the frames up to $n$, and $G(n) > \eta$ is the Bayes decision when a false alarm costs $\eta$ times as much as a miss. The code uses $\log G$ and computes $\log(a + b\, e^{\ell})$ with a stable log-add, which changes no value.

## Corollary (no memory)

If $a_{01} = a_{10} = 1/2$, then $G(n) = \Lambda(n)$ for all $n$.

*Proof.* All four transitions are $1/2$, so the fraction in the recursion is $(1 + G) / (1 + G) = 1$. $\square$

## Remarks

The tests check Lemma 1 against the two densities computed directly, Theorem 2 against the sum over all $2^n$ state paths for $n \le 6$, and the corollary. The decision-directed $\xi_k$ depends on the data, so Theorem 1 does not apply exactly to the running detector; the page says how this shifts the threshold.
