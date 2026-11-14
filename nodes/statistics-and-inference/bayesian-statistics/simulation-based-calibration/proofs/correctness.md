---
title: Uniform ranks under a correct sampler, with ties, and what uniformity tests
proves: [correctness]
status: full
---

**Setting.** A prior $\pi(\theta)$ and a model $p(y \mid \theta)$ define the joint law $\pi(\theta)p(y \mid \theta)$ of $(\theta, y)$, with marginal $p(y)$ and posterior $\pi(\theta \mid y)$. One replication of SBC draws $\tilde\theta \sim \pi$, then $\tilde y \sim p(\cdot \mid \tilde\theta)$, then $\theta_1, \ldots, \theta_L$ from the sampler under test given $\tilde y$. A real function $f$ of the parameter is fixed. Write $\tilde f = f(\tilde\theta)$ and $f_l = f(\theta_l)$. The plain rank is $R_0 = \#\{l : f_l < \tilde f\}$; the randomized rank of L6 is

$$R = \#\{l : f_l < \tilde f\} + U, \qquad U \text{ uniform on } \{0, 1, \ldots, \#\{l : f_l = \tilde f\}\},$$

with $U$ drawn independently given the values.

## Claim 1: the true parameter is a posterior draw given the data

Given $\tilde y = y$, $\tilde\theta$ has the law $\pi(\theta \mid y)$.

*Proof.* The pair $(\tilde\theta, \tilde y)$ has density $\pi(\theta)p(y \mid \theta) = p(y)\pi(\theta \mid y)$ by [Bayes' theorem](/bayes-theorem/), so the conditional density of $\tilde\theta$ given $\tilde y = y$ is $\pi(\theta \mid y)$. $\square$

## Claim 2: rank uniformity without ties

Suppose the sampler returns $\theta_1, \ldots, \theta_L$ independent with law $\pi(\cdot \mid \tilde y)$, independent of $\tilde\theta$ given $\tilde y$, and suppose that for almost every $y$ the law of $f(\theta)$ under $\pi(\cdot \mid y)$ has no atoms. Then $P(R_0 = r) = 1/(L+1)$ for $r = 0, \ldots, L$, and $R = R_0$ almost surely.

*Proof.* Fix $\tilde y = y$. By Claim 1 and the assumption, $\tilde f, f_1, \ldots, f_L$ are $L + 1$ independent values with the same atomless law, so they are distinct with probability one, and $R = R_0$. Write $g_0 = \tilde f$ and $g_l = f_l$, and let $R^{(j)} = \#\{l \ne j : g_l < g_j\}$ be the rank of $g_j$ among the others. The vector $(g_0, \ldots, g_L)$ is exchangeable, so swapping $g_0$ and $g_j$ shows that $R^{(j)}$ has the same law as $R^{(0)} = R_0$. For distinct values, exactly one index has rank $r$, so $\sum_{j=0}^{L}\mathbf{1}\{R^{(j)} = r\} = 1$. Taking expectations, $(L + 1)P(R_0 = r \mid \tilde y = y) = 1$. Averaging over $y$ gives the claim. $\square$

## Claim 3: randomized ranks are uniform even with ties

Under the sampler assumption of Claim 2, but with no condition on atoms, $P(R = r) = 1/(L+1)$ for $r = 0, \ldots, L$. If ties have positive probability, the plain rank is not uniform: $P(R_0 = 0) > 1/(L+1)$ whenever $P(f_1 = \cdots = f_L = \tilde f) > 0$.

*Proof.* Let $V_0, \ldots, V_L$ be independent Uniform(0, 1) values, independent of everything else, and order the pairs $(g_j, V_j)$ lexicographically. Given $\tilde y$ the pairs are independent and identically distributed, and they are distinct with probability one because the $V_j$ are. The argument of Claim 2 shows that the lexicographic rank $R'$ of $(g_0, V_0)$ is uniform on $\{0, \ldots, L\}$. Now fix the values $g_0, \ldots, g_L$. Let $e = \#\{l \ge 1 : g_l = g_0\}$. Then $R' = \#\{l : g_l < g_0\} + \#\{l : g_l = g_0, V_l < V_0\}$, and the second term is the rank of $V_0$ among $e + 1$ independent uniform values, which is uniform on $\{0, \ldots, e\}$. So given the values, $R'$ and $R$ have the same law, hence the same unconditional law, which is uniform.

For the second part, $R_0 \le R$ always, so $P(R_0 = 0) \ge P(R = 0) = 1/(L+1)$, and on the event that all $L + 1$ values are equal, $R_0 = 0$ while $R = U$ is positive with probability $L/(L+1)$. That event has positive probability, which makes the inequality strict. $\square$

*A correction to the usual statement.* Talts and coauthors (2018, Theorem 1) state uniformity of the plain rank for any one-dimensional function. That needs the atomless condition of Claim 2: for a constant $f$, the plain rank is $0$ in every replication. With discrete parameters, or with a function such as an indicator, use the randomized rank of Claim 3.

## Claim 4: what uniform ranks test

Let the sampler return, given $\tilde y = y$, independent draws $\theta_l$ from some law $q(\cdot \mid y)$ such that the distribution function $G_y(t) = q(f(\theta) \le t \mid y)$ is continuous, and let $u = G_{\tilde y}(\tilde f)$. Then

$$P(R = r) = \binom{L}{r}\mathbb{E}\big[u^r(1 - u)^{L - r}\big], \qquad r = 0, \ldots, L,$$

and the rank is uniform on $\{0, \ldots, L\}$ for every $L$ if and only if $u$ is Uniform(0, 1).

*Proof.* Given $\tilde y$ and $\tilde\theta$, each $f_l$ is below $\tilde f$ with probability $u$, independently, and ties have probability zero because $G_y$ is continuous. So $R$ is binomial$(L, u)$ given $u$, which gives the formula. If $u$ is uniform, $\binom{L}{r}\int_0^1 u^r(1-u)^{L-r}\, du = \binom{L}{r}\frac{r!\,(L-r)!}{(L+1)!} = \frac{1}{L+1}$. Conversely, if the rank is uniform for every $L$, then $r = L$ gives $\mathbb{E}[u^L] = 1/(L+1)$ for all $L \ge 1$, which are the moments of Uniform(0, 1). A law on $[0, 1]$ is determined by its moments, so $u$ is uniform. $\square$

So SBC tests whether the value of the computed posterior distribution function at the true parameter, $u$, is uniform. A correct sampler passes by Claim 1, since then $u$ is the probability integral transform of a draw from its own continuous law. A sampler whose posteriors are too narrow puts $u$ near $0$ and $1$, which gives a U-shaped rank histogram; one that is too wide puts $u$ near $1/2$, which gives a hump; one that is shifted up makes $u$ small. A sampler that returns the prior for every $y$ also passes: then $\tilde\theta$ and the draws are independent draws from $\pi$, and $u$ is uniform. Uniform ranks are therefore necessary for a correct sampler but not sufficient.

## What is proved and what is measured

Claims 1 to 4 are exact; the tests check Claim 3 and the prior-sampler remark in exact rational arithmetic on discrete models. Two parts of the method are not proved here. The chi-squared test of the rank counts uses Pearson's approximation of the statistic by the chi-squared law with $B - 1$ degrees of freedom, which holds as the number of replications grows. When the draws come from a Markov chain, they are dependent, Claims 2 to 4 do not apply, and the fact that thinning to about $L$ effective draws restores near-uniform ranks (Talts and coauthors 2018, Algorithm 2) is measured on the page, not proved.
