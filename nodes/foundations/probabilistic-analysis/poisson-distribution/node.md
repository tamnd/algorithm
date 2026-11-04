---
tag: HTJF9T
kind: definition
slug: poisson-distribution
name: Poisson distribution
aliases:
- Poisson random variable
area: foundations/probabilistic-analysis
level: intro
summary: The limit of the binomial distribution for many trials with small success probability.
prereqs: [binomial-distribution, bernoulli-trials]
see_also: [balls-into-bins, chaining-analysis, total-variation-distance, geometric-distribution, chernoff-bound, hash-table]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 5.3, The Poisson Distribution, with Section 5.3.1, Limit of the Binomial Distribution; Section 5.4, The Poisson Approximation; Section 5.5.1, Chain Hashing; Section 8.4, The Poisson Process
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter VI, The Binomial and the Poisson Distributions, Sections 5 to 7
  - paper: doi:10.2140/pjm.1960.10.1181
    title: Lucien Le Cam, An approximation theorem for the Poisson binomial distribution, Pacific Journal of Mathematics 10(4), 1960, pages 1181 to 1197
    locator: the bound on the distance between a sum of independent Bernoulli variables and the Poisson law with the same mean
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 3, Moments and Deviations (occupancy problems)
---

The Poisson distribution with mean $\lambda$ is the law on $\{0, 1, 2, \ldots\}$ with mass function $e^{-\lambda} \lambda^k / k!$. It is the limit of the [binomial distribution](/binomial-distribution/) $\mathrm{Bin}(n, p)$ when the number of trials $n$ grows, the success probability $p$ falls, and $np$ stays near $\lambda$, and the error of this limit is at most $np^2$ in [total variation distance](/total-variation-distance/). In algorithms it describes the load of a bucket in a large [hash table](/hash-table/), the number of balls in a bin in [balls into bins](/balls-into-bins/), and the number of requests that arrive in a short time window.

## Definition

Let $\lambda > 0$. A [random variable](/random-variable/) $X$ has the **Poisson distribution** $\mathrm{Poi}(\lambda)$ when

$$\Pr(X = k) = \frac{e^{-\lambda} \lambda^k}{k!} \quad \text{for } k = 0, 1, 2, \ldots$$

### Properties

**(a) It is a distribution.** The terms are positive and $\sum_{k \ge 0} \lambda^k / k! = e^{\lambda}$, so they sum to 1.

**(b) Mean $\lambda$.** $\mathbb{E}[X] = \sum_{k \ge 1} k \frac{e^{-\lambda}\lambda^k}{k!} = \lambda \sum_{k \ge 1} \frac{e^{-\lambda}\lambda^{k-1}}{(k-1)!} = \lambda$.

**(c) Variance $\lambda$.** The same shift by two gives $\mathbb{E}[X(X-1)] = \lambda^2$, so $\mathrm{Var}(X) = \lambda^2 + \lambda - \lambda^2 = \lambda$. The mean and the variance are equal.

**(d) Shape.** $\Pr(X = k) / \Pr(X = k - 1) = \lambda / k$ for $k \ge 1$. So the terms increase while $k < \lambda$ and decrease when $k > \lambda$. The mode is $\lfloor \lambda \rfloor$, and when $\lambda$ is an integer, the terms at $\lambda - 1$ and $\lambda$ tie.

**(e) Sums.** If $X \sim \mathrm{Poi}(\lambda)$ and $Y \sim \mathrm{Poi}(\mu)$ are independent, then $X + Y \sim \mathrm{Poi}(\lambda + \mu)$. By independence and the [binomial theorem](/binomial-theorem/),

$$\Pr(X + Y = k) = \sum_{j=0}^{k} \frac{e^{-\lambda}\lambda^j}{j!} \cdot \frac{e^{-\mu}\mu^{k-j}}{(k-j)!} = \frac{e^{-(\lambda + \mu)}}{k!} \sum_{j=0}^k \binom{k}{j} \lambda^j \mu^{k-j} = \frac{e^{-(\lambda+\mu)}(\lambda + \mu)^k}{k!}.$$

By induction, a sum of $n$ independent Poisson variables is Poisson with the sum of the means.

### The binomial limit

**Theorem (pointwise limit).** Let $p_n \in [0, 1]$ with $n p_n \to \lambda > 0$ as $n \to \infty$. Then for each fixed $k \ge 0$,

$$\binom{n}{k} p_n^k (1 - p_n)^{n-k} \to \frac{e^{-\lambda}\lambda^k}{k!}.$$

*Proof.* For $n \ge k$ write the left side as

$$\frac{n(n-1)\cdots(n-k+1)}{n^k} \cdot \frac{(n p_n)^k}{k!} \cdot (1 - p_n)^{n} \cdot (1 - p_n)^{-k}.$$

The first factor is a product of $k$ terms $1 - j/n$, each tending to 1. The second tends to $\lambda^k / k!$. Since $p_n = (np_n)/n \to 0$, the fourth tends to 1. For the third, $\ln(1 - x) = -x - r(x)$ with $0 \le r(x) \le x^2$ for $0 \le x \le 1/2$, so for large $n$, $n \ln(1 - p_n) = -np_n - n\,r(p_n)$, where $0 \le n\,r(p_n) \le n p_n^2 = (np_n) p_n \to 0$. Hence $n \ln(1 - p_n) \to -\lambda$ and $(1 - p_n)^n \to e^{-\lambda}$. $\square$

Mitzenmacher and Upfal, Section 5.3.1, and Feller, Chapter VI, prove this limit.

**Theorem (error bound).** Let $X_1, \ldots, X_n$ be independent with $\Pr(X_i = 1) = p_i$ and $\Pr(X_i = 0) = 1 - p_i$, let $S = \sum_i X_i$ and $\lambda = \sum_i p_i$. Then for every set $A$ of integers,

$$\left|\Pr(S \in A) - \Pr(\mathrm{Poi}(\lambda) \in A)\right| \le \sum_{i=1}^n p_i^2.$$

In particular, $d_{TV}(\mathrm{Bin}(n, p), \mathrm{Poi}(np)) \le np^2 = \lambda^2 / n$. Le Cam (1960) proved this inequality. The proof below is by coupling.

*Proof.* **Step 1: one trial.** Fix $p \in [0, 1]$. Let $Y \sim \mathrm{Poi}(p)$, and let $V$ be uniform on $[0, 1]$, independent of $Y$. Define $X = 1$ if $Y \ge 1$; if $Y = 0$, define $X = 1$ when $V < c$ and $X = 0$ otherwise, where $c = (p - 1 + e^{-p})/e^{-p}$. Since $1 - p \le e^{-p} \le 1$ and $p \le 1$, $0 \le c \le 1$. Then $\Pr(X = 1) = (1 - e^{-p}) + e^{-p} c = p$, so $X$ is Bernoulli$(p)$. The two disagree when $Y \ge 2$, or when $Y = 0$ and $X = 1$:

$$\Pr(X \ne Y) = (1 - e^{-p} - p e^{-p}) + (p - 1 + e^{-p}) = p(1 - e^{-p}) \le p^2,$$

by $1 - e^{-p} \le p$. (When $Y = 1$, $X = 1 = Y$.)

**Step 2: all trials.** Build such a pair $(X_i, Y_i)$ for each $i$ with parameter $p_i$, with the $n$ pairs independent. Then $S = \sum_i X_i$ has the law of the theorem, and $T = \sum_i Y_i \sim \mathrm{Poi}(\lambda)$ by property (e). If $S \ne T$, then $X_i \ne Y_i$ for some $i$, so by the [union bound](/union-bound/), $\Pr(S \ne T) \le \sum_i p_i^2$.

**Step 3: from coupling to distance.** For each set $A$, $\Pr(S \in A) - \Pr(T \in A) \le \Pr(S \in A, T \notin A) \le \Pr(S \ne T)$, and the same holds with $S$ and $T$ swapped. $\square$

The bound is useful when $p$ is small. It gives nothing for $\mathrm{Bin}(100, 0.1)$, where $np^2 = 1$, although there the true distance is about $0.026$.

## Examples and non-examples

**Bucket loads in a hash table.** Hash $n = 1000$ keys into $m = 1000$ buckets with [simple uniform hashing](/simple-uniform-hashing/). The load of one bucket is $\mathrm{Bin}(1000, 0.001)$, and the Poisson limit uses $\lambda = 1$:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $\Pr(\mathrm{Bin} = k)$ | 0.36770 | 0.36806 | 0.18403 | 0.06128 | 0.01529 | 0.00305 |
| $\Pr(\mathrm{Poi}(1) = k)$ | 0.36788 | 0.36788 | 0.18394 | 0.06131 | 0.01533 | 0.00307 |

The total variation distance between the two laws is about $0.00028$, below the bound $np^2 = 0.001$. The expected number of empty buckets is $1000 (0.999)^{1000} \approx 367.7$, and the Poisson value is $1000 e^{-1} \approx 367.9$. In general, with load factor $\alpha = n/m$ and large $m$, a bucket holds $k$ keys with probability near $e^{-\alpha}\alpha^k/k!$ (Mitzenmacher and Upfal, Section 5.5.1).

**The largest bucket.** With $n = m$, the expected load is 1, but the largest load among the $m$ buckets grows: it is $\Theta(\ln n / \ln \ln n)$ with high probability. The Poisson tail $e^{-1}/k!$ explains the order: $m \cdot e^{-1}/k!$ falls below 1 when $k!$ passes $m$. See [balls into bins](/balls-into-bins/).

**Arrivals of requests.** A server gets requests from many independent clients, each of which sends one in a short window with a small probability. The number of requests in the window is close to Poisson. At a rate of 200 requests per second, a 10 millisecond window has $\lambda = 2$: it is empty with probability $e^{-2} \approx 0.1353$, and it has 5 or more requests with probability about $0.0527$. The model of arrivals at random times is the Poisson process (Mitzenmacher and Upfal, Section 8.4).

**Non-example: large success probability.** $\mathrm{Bin}(100, 1/2)$ has mean 50 and variance 25. A Poisson law with mean 50 has variance 50, so it does not fit. The limit needs small $p$, not only large $n$.

**Non-example: a bounded count.** The number of keys in a bucket is at most $n$, and a Poisson variable is unbounded. For $n = 2$ keys, $\Pr(\text{load} = 3) = 0$, while $\Pr(\mathrm{Poi}(\lambda) = 3) > 0$. The Poisson law is an approximation, with the error of the theorem.

### Pitfalls

- **The loads of different buckets are not independent.** They sum to $n$. The Poisson law approximates the load of one bucket. To treat all loads at once as independent Poisson variables, use the Poisson approximation of Mitzenmacher and Upfal, Section 5.4: there, an event that has probability $p$ in the model with independent Poisson loads has probability at most $e\sqrt{m}\,p$ with the true loads, and the factor improves to 2 for events of a monotone kind.
- **Pointwise convergence alone gives no error bound.** For a statement about a fixed $n$, use the bound $\sum_i p_i^2$, or compute the binomial values exactly.
- **Mean equal to variance is a check, not a proof.** Data whose variance is far from its mean is not Poisson. Data whose variance equals its mean need not be Poisson.
- **Independent trials are needed.** The theorem assumes independent trials. With dependence, for example correlated client failures, the count can be far from Poisson.

## Related definitions

- The [binomial distribution](/binomial-distribution/) is the exact law that the Poisson law approximates.
- [Bernoulli trials](/bernoulli-trials/), and Poisson trials with different $p_i$, are the trials behind the limit.
- The [total variation distance](/total-variation-distance/) is the metric of the error bound.
- [Balls into bins](/balls-into-bins/) and [chaining analysis](/chaining-analysis/) use the Poisson approximation.
- The exponential law of the [probability density function](/probability-density-function/) page is the law of the gaps between arrivals of a Poisson process.

## References
