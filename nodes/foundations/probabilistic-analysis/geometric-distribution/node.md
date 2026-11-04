---
tag: 0K6G57
kind: definition
slug: geometric-distribution
name: Geometric distribution
aliases:
- geometric random variable
area: foundations/probabilistic-analysis
level: intro
summary: The number of trials until the first success; its expectation is 1/p.
prereqs: [bernoulli-trials, geometric-series]
see_also: [binomial-distribution, coupon-collector-problem, las-vegas-algorithm, skip-list, exponential-backoff, uniform-hashing-assumption, expected-value]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.4, The geometric and binomial distributions; Section 11.4, Open addressing (the probe count under uniform hashing)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.4, The Geometric Distribution, and Section 2.4.1, Example, Coupon Collector's Problem
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 8, Data Structures (skip lists); Appendix C, Basic Probability Theory
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter VI, The Binomial and the Poisson Distributions (waiting times in Bernoulli trials), and Chapter XI, Integral Valued Variables. Generating Functions
---

The geometric distribution with parameter $p$ is the law of the number of [Bernoulli trials](/bernoulli-trials/) up to and including the first success, when each trial succeeds with probability $p$. Its mass function is $(1-p)^{k-1} p$ for $k \ge 1$, its mean is $1/p$ and its variance is $(1-p)/p^2$. It is the law of the number of runs of a [Las Vegas algorithm](/las-vegas-algorithm/) that restarts on failure, of the number of attempts of a retry loop, and of the level of a node in a [skip list](/skip-list/).

## Definition

Let $0 < p \le 1$ and $q = 1 - p$. A [random variable](/random-variable/) $X$ has the **geometric distribution** with parameter $p$ when

$$\Pr(X = k) = q^{k-1} p \quad \text{for } k = 1, 2, 3, \ldots$$

If $X_1, X_2, \ldots$ are Bernoulli trials with parameter $p$, then the index $X$ of the first success has this law: $X = k$ means $k - 1$ failures and then a success, with probability $q^{k-1} p$ by independence. This is the convention of CLRS and of Mitzenmacher and Upfal. Some books count the failures before the first success, $Y = X - 1$ with $\Pr(Y = j) = q^j p$ for $j \ge 0$ and mean $q/p$. Always check which one a formula uses.

### Properties

**(a) It is a distribution.** The terms are nonnegative, and by the [geometric series](/geometric-series/) $\sum_{k \ge 1} q^{k-1} p = p \cdot \frac{1}{1 - q} = 1$ for $0 < p \le 1$.

**(b) Tail.** $\Pr(X > k) = q^k$ for $k \ge 0$: $X > k$ exactly when the first $k$ trials fail. So $\Pr(X \ge k) = q^{k-1}$, and $\Pr(X > t/p) \le (1-p)^{t/p} \le e^{-t}$ for $t \ge 0$, by $1 - p \le e^{-p}$.

**(c) Mean $1/p$.** For a random variable with values in $\{0, 1, 2, \ldots\}$, $\mathbb{E}[X] = \sum_{k \ge 0} \Pr(X > k)$ (proved on the [expected value](/expected-value/) page). With (b),

$$\mathbb{E}[X] = \sum_{k \ge 0} q^k = \frac{1}{1 - q} = \frac{1}{p}.$$

**(d) Variance $q/p^2$.** For $|x| < 1$ the power series $\sum_{k \ge 0} x^k = \frac{1}{1-x}$ can be differentiated term by term, so $\sum_{k \ge 2} k(k-1) x^{k-2} = \frac{2}{(1-x)^3}$. With $x = q$:

$$\mathbb{E}[X(X-1)] = \sum_{k \ge 2} k(k-1) q^{k-1} p = pq \cdot \frac{2}{p^3} = \frac{2q}{p^2}.$$

Then $\mathbb{E}[X^2] = \frac{2q}{p^2} + \frac{1}{p}$ and $\mathrm{Var}(X) = \frac{2q}{p^2} + \frac{1}{p} - \frac{1}{p^2} = \frac{2q + p - 1}{p^2} = \frac{q}{p^2}$. For $p = 1$ this is 0, as it must be: then $X = 1$ always.

**(e) No memory.** For integers $s, t \ge 0$, by (b),

$$\Pr(X > s + t \mid X > s) = \frac{q^{s+t}}{q^s} = q^t = \Pr(X > t)$$

(for $p < 1$, so that $\Pr(X > s) > 0$). Conversely, it is the only law on $\{1, 2, \ldots\}$ with this property. Let $G(k) = \Pr(X > k)$, with $G(0) = 1$ and $0 < G(1) < 1$. If $G(s + t) = G(s) G(t)$ for all $s, t \ge 0$, then $G(k) = G(1)^k$ by induction on $k$, so $X$ is geometric with $q = G(1)$.

**(f) Median.** The median is the least $k$ with $1 - q^k \ge 1/2$, that is $k = \lceil \ln 2 / (-\ln q) \rceil$, which is about $(\ln 2)/p \approx 0.69/p$ for small $p$. The mean $1/p$ is larger than the median.

**(g) Waiting for the $r$-th success.** The number of trials up to the $r$-th success is a sum of $r$ independent geometric variables with parameter $p$: after each success, the trials that follow are again Bernoulli trials, independent of the past (property (e) of [Bernoulli trials](/bernoulli-trials/)). So its mean is $r/p$ by [linearity of expectation](/linearity-of-expectation/), and its variance is $rq/p^2$. Its law is $\Pr(T_r = k) = \binom{k-1}{r-1} p^r q^{k-r}$ for $k \ge r$ (the negative binomial law): the $k$-th trial succeeds, and $r - 1$ of the first $k - 1$ trials succeed.

## Examples and non-examples

**Retries.** Each attempt succeeds with probability $0.9$, independently. The number of attempts is geometric with $p = 0.9$: its mean is $1/0.9 \approx 1.111$, its variance is $0.1/0.81 \approx 0.1235$, and more than 3 attempts are needed with probability $0.1^3 = 0.001$.

**Restarting a Las Vegas algorithm.** A [Las Vegas algorithm](/las-vegas-algorithm/) whose single run succeeds with probability at least $1/4$, and which restarts with fresh random bits on failure, needs at most 4 runs in expectation. If one run costs at most $T$, the expected total cost is at most $4T$. By (b), more than $4t$ runs are needed with probability at most $(3/4)^{4t} \le e^{-t}$.

**Rejection sampling.** To draw a uniform value in $\{0, \ldots, m-1\}$ from 32-bit uniform words, reject words at or above the largest multiple of $m$ that is at most $2^{32}$, and reduce the others mod $m$ (this removes the modulo bias of the [discrete distribution](/discrete-probability-distribution/) page). The number of words used is geometric with $p = \lfloor 2^{32}/m \rfloor m / 2^{32}$. For $m = 3 \cdot 2^{30}$ this is $p = 3/4$, so the mean is $4/3$ words. For small $m$, $p$ is close to 1.

**Skip list levels.** A key in a [skip list](/skip-list/) moves up one level while its coin, with heads probability $r$, comes up heads. Its level is geometric with success probability $1 - r$ (a tails ends it), so its mean is $1/(1 - r)$. For $r = 1/2$ the mean is 2, and for $r = 1/4$ it is $4/3$. Summed over $n$ keys, the expected number of nodes is $n/(1 - r)$. Motwani and Raghavan, Chapter 8, analyze skip lists with these levels.

**Open addressing.** Under the [uniform hashing assumption](/uniform-hashing-assumption/) with load factor $\alpha < 1$, the $i$-th probe of an unsuccessful search finds an occupied slot, given that the probes before did, with probability at most $\alpha$. So the number of probes $P$ has $\Pr(P > k) \le \alpha^k$, and $\mathbb{E}[P] \le \sum_{k \ge 0} \alpha^k = 1/(1 - \alpha)$: the tail of a geometric law with $p = 1 - \alpha$. For $\alpha = 0.9$ the bound is 10 probes. CLRS, Section 11.4, proves this bound.

**The coupon collector.** To see all $n$ values of a uniform hash at least once, the wait for the $i$-th new value is geometric with $p = (n - i + 1)/n$. The total has mean $\sum_{i=1}^n \frac{n}{n - i + 1} = n H_n$. See [coupon collector problem](/coupon-collector-problem/).

**Non-example: a growing success chance.** If attempt $k$ succeeds with probability $1 - 2^{-k}$ (say, a server that recovers), the number of attempts is not geometric: $\Pr(X > 1 + 1 \mid X > 1) = 1/4 \ne \Pr(X > 1) = 1/2$, so the law has memory.

### Pitfalls

- **Off by one.** Trials up to the first success (mean $1/p$) or failures before it (mean $q/p$)? A skip list with level 0 at the bottom uses the second.
- **The mean hides a long tail when $p$ is small.** For $p = 0.01$, the mean is 100 but the median is 69, and $\Pr(X > 300) = 0.99^{300} \approx 0.049$. A retry loop with a small success probability needs a cap, or a bound in probability rather than in expectation.
- **The mean of $1/X$ is not $p$.** $\mathbb{E}[1/X] = \sum_k \frac{q^{k-1}p}{k} = \frac{p}{q} \ln \frac{1}{p}$ for $p < 1$, which is larger than $p$, see the pitfalls of [expected value](/expected-value/).
- **Independence is needed.** If failures are correlated (the server stays down), the count is not geometric, and the mean $1/p$ can be far too small. See [independent events](/independent-events/).

## Related definitions

- [Bernoulli trials](/bernoulli-trials/) are the trials whose first success it counts.
- The [binomial distribution](/binomial-distribution/) counts the successes in a fixed number of the same trials. $\Pr(X > k) = \Pr(\mathrm{Bin}(k, p) = 0)$.
- The exponential law is its continuous analogue, and $\lceil E \rceil$ is geometric for an exponential $E$, see [probability density function](/probability-density-function/).
- The [coupon collector problem](/coupon-collector-problem/) and [Wald's equation](/walds-equation/) use sums of geometric variables.

## References
