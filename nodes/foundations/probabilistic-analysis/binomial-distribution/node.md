---
tag: MXGQM4
kind: definition
slug: binomial-distribution
name: Binomial distribution
aliases:
- binomial random variable
area: foundations/probabilistic-analysis
level: intro
summary: The number of successes in n independent Bernoulli trials.
prereqs: [bernoulli-trials, binomial-coefficient, binomial-theorem]
see_also: [binomial-tail-bounds, chernoff-bound, poisson-distribution, geometric-distribution, balls-into-bins, chaining-analysis, variance]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.4, The geometric and binomial distributions, and Section C.5, The tails of the binomial distribution
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.2, The Bernoulli and Binomial Random Variables; Section 3.2.1, Example, Variance of a Binomial Random Variable
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter VI, The Binomial and the Poisson Distributions, Sections 2 and 3
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 4, Tail Inequalities
---

The binomial distribution with parameters $n$ and $p$ is the law of the number of successes in $n$ [Bernoulli trials](/bernoulli-trials/) with success probability $p$. Its mass function is $\binom{n}{k} p^k (1-p)^{n-k}$, its mean is $np$ and its variance is $np(1-p)$. In algorithms it is the law of the number of keys in one bucket of a [hash table](/hash-table/), of the number of nodes at a level of a [skip list](/skip-list/), and of the number of failed requests in a batch.

## Definition

Let $n \ge 0$ be an integer and $p \in [0, 1]$, and write $q = 1 - p$. A [random variable](/random-variable/) $X$ has the **binomial distribution** $\mathrm{Bin}(n, p)$ when

$$\Pr(X = k) = b(k; n, p) = \binom{n}{k} p^k q^{n-k} \quad \text{for } k = 0, 1, \ldots, n.$$

The name $b(k; n, p)$ is the one of CLRS. If $X_1, \ldots, X_n$ are Bernoulli trials with parameter $p$, then $X = X_1 + \cdots + X_n$ is $\mathrm{Bin}(n, p)$: the event $X = k$ is the disjoint union of the $\binom{n}{k}$ outcome sequences with $k$ ones, and each of them has probability $p^k q^{n-k}$.

### Properties

**(a) It is a distribution.** Each term is nonnegative, and by the [binomial theorem](/binomial-theorem/), $\sum_{k=0}^n \binom{n}{k} p^k q^{n-k} = (p + q)^n = 1$.

**(b) Mean $np$.** Two proofs. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[X] = \sum_i \mathbb{E}[X_i] = np$; this needs no independence. Directly, with $k \binom{n}{k} = n \binom{n-1}{k-1}$ for $k \ge 1$:

$$\mathbb{E}[X] = \sum_{k=1}^{n} k \binom{n}{k} p^k q^{n-k} = np \sum_{k=1}^{n} \binom{n-1}{k-1} p^{k-1} q^{n-k} = np (p + q)^{n-1} = np.$$

**(c) Variance $npq$.** With $k(k-1)\binom{n}{k} = n(n-1)\binom{n-2}{k-2}$ for $k \ge 2$, the same steps give $\mathbb{E}[X(X-1)] = n(n-1)p^2$. So $\mathbb{E}[X^2] = n(n-1)p^2 + np$, and

$$\mathrm{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = n(n-1)p^2 + np - n^2 p^2 = np(1 - p) = npq.$$

Equivalently, the $X_i$ are independent, so their [variances](/variance/) add, and each is $pq$.

**(d) Shape and mode.** For $1 \le k \le n$ and $0 < p < 1$,

$$\frac{b(k; n, p)}{b(k-1; n, p)} = \frac{(n - k + 1)\,p}{k\,q}.$$

This ratio is greater than 1 exactly when $(n - k + 1)p > kq$, that is $k < (n + 1)p$, and equal to 1 exactly when $k = (n+1)p$. So the terms increase while $k < (n + 1)p$ and decrease after. The largest term is at $k = \lfloor (n + 1)p \rfloor$. When $(n + 1)p$ is an integer, the terms at $(n + 1)p$ and $(n + 1)p - 1$ tie. CLRS, Section C.4, gives the same shape.

**(e) Sums.** If $X \sim \mathrm{Bin}(n_1, p)$ and $Y \sim \mathrm{Bin}(n_2, p)$ are independent, then $X + Y \sim \mathrm{Bin}(n_1 + n_2, p)$. Proof: realize $X$ as the sum of $n_1$ trials and $Y$ as the sum of $n_2$ further trials, all mutually independent; then $X + Y$ counts the successes of $n_1 + n_2$ Bernoulli trials. The law of $X + Y$ depends only on the laws of $X$ and $Y$ and their independence, so this realization gives the answer in general.

**(f) Symmetry.** $n - X$ counts failures, so $n - X \sim \mathrm{Bin}(n, q)$.

**(g) A simple upper tail.** For $0 \le k \le n$, $\Pr(X \ge k) \le \binom{n}{k} p^k$. Proof: if at least $k$ trials succeed, then some set $S$ of exactly $k$ trials all succeed. For each fixed $S$ that has probability $p^k$, and there are $\binom{n}{k}$ sets, so the [union bound](/union-bound/) gives the claim. CLRS, Section C.5, proves this bound. Much sharper bounds are on the pages [binomial tail bounds](/binomial-tail-bounds/) and [Chernoff bound](/chernoff-bound/).

## Examples and non-examples

**A small table.** For $n = 10$ and $p = 0.3$ the mass function, to four places, is

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $b(k; 10, 0.3)$ | 0.0282 | 0.1211 | 0.2335 | 0.2668 | 0.2001 | 0.1029 | 0.0368 | 0.0090 | 0.0014 | 0.0001 | 0.0000 |

The mode is $\lfloor 11 \cdot 0.3 \rfloor = 3$, as (d) predicts. The mean is 3 and the variance is $2.1$.

**Load of one bucket.** Hash $n$ keys into $m$ buckets with [simple uniform hashing](/simple-uniform-hashing/). The load of a fixed bucket is $\mathrm{Bin}(n, 1/m)$, with mean $n/m$, the load factor. For $n = m = 1000$: the bucket is empty with probability $(1 - 1/1000)^{1000} \approx 0.3677$, so about $367.7$ buckets are empty in expectation. By (g), the bucket holds 10 or more keys with probability at most $\binom{1000}{10} / 1000^{10} \approx 2.63 \times 10^{-7}$ (the exact value is about $1.07 \times 10^{-7}$). The union bound over the 1000 buckets gives that some bucket holds 10 or more keys with probability at most $2.64 \times 10^{-4}$. See [chaining analysis](/chaining-analysis/) and [balls into bins](/balls-into-bins/).

**Levels of a skip list.** In a [skip list](/skip-list/) with 1024 keys and promotion probability $1/2$, a key reaches level 3 or higher with probability $1/4$. The number of such keys is $\mathrm{Bin}(1024, 1/4)$, with mean 256, variance 192 and standard deviation about $13.86$.

**Failures in a batch.** A batch of 100 requests, each failing independently with probability $0.02$. The number of failures is $\mathrm{Bin}(100, 0.02)$. No request fails with probability $0.98^{100} \approx 0.1326$, and at most 2 fail with probability about $0.6767$. The mean is 2.

**Non-example: dependent trials.** The loads $L_0, \ldots, L_{m-1}$ of the $m$ buckets are each binomial, but they are not independent, since they sum to $n$. Their joint law is multinomial. For example, with $n = m = 2$, $\Pr(L_0 = 2, L_1 = 2) = 0$, but $\Pr(L_0 = 2)\Pr(L_1 = 2) = 1/16$.

**Non-example: sampling without replacement.** The number of defective items in $k$ draws without replacement from a lot with a fixed number of defects is hypergeometric, not binomial: the draws are dependent (see [Bernoulli trials](/bernoulli-trials/)).

### Pitfalls

- **Mean, mode and median differ.** The mode is $\lfloor (n+1)p \rfloor$, which can differ from $np$ by up to 1. Do not use one for another in an exact argument.
- **Overflow and underflow.** $\binom{2000}{1000}$ is about $10^{600}$, beyond the range of a double, while $p^k$ underflows to 0. Compute $\log b(k; n, p)$ with the log-gamma function, or step from $b(k-1)$ to $b(k)$ with the ratio in (d).
- **Rounding in $(1 - p)^n$.** For $p = 10^{-17}$, $1 - p$ rounds to $1.0$ in double precision, so $1 - (1 - p)^n$ comes out as 0 for any $n$. For $n = 10^6$ the true value is about $10^{-11}$. Use $1 - \exp(n \cdot \mathrm{log1p}(-p))$.
- **The normal approximation is poor in the tails.** The binomial is close to a normal law near its mean when $npq$ is large (Feller, Chapter VII), but the relative error far in the tails can be large. For tail probabilities use exact sums or [Chernoff bounds](/chernoff-bound/).

## Related definitions

- [Bernoulli trials](/bernoulli-trials/) are the trials that a binomial variable counts.
- The [Poisson distribution](/poisson-distribution/) is the limit of $\mathrm{Bin}(n, \lambda/n)$ as $n \to \infty$.
- The [geometric distribution](/geometric-distribution/) is the waiting time for the first success in the same trials.
- The [Chernoff bound](/chernoff-bound/) and [binomial tail bounds](/binomial-tail-bounds/) bound $\Pr(X \ge (1 + \delta)np)$ and $\Pr(X \le (1 - \delta)np)$.

## References
