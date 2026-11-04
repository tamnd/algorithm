---
tag: BQ5NDK
kind: definition
slug: bernoulli-trials
name: Bernoulli trials
aliases:
- Bernoulli random variable
area: foundations/probabilistic-analysis
level: intro
summary: Independent experiments each succeeding with fixed probability p.
prereqs: [random-variable, independent-events]
see_also: [binomial-distribution, geometric-distribution, poisson-distribution, indicator-random-variable, monte-carlo-algorithm, skip-list, chernoff-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.4, The geometric and binomial distributions (Bernoulli trials)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.2, The Bernoulli and Binomial Random Variables; Section 4.2.1, Chernoff Bounds for the Sum of Poisson Trials
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter VI, The Binomial and the Poisson Distributions, Section 1, Bernoulli Trials
---

Bernoulli trials are a sequence of experiments, each with two outcomes, success and failure, in which each trial succeeds with the same probability $p$ and the trials are mutually [independent](/independent-events/). One trial is described by a Bernoulli random variable, which is 1 with probability $p$ and 0 with probability $1 - p$. Coin flips in a [skip list](/skip-list/), repeated runs of a [Monte Carlo algorithm](/monte-carlo-algorithm/), and independent retries of a request are all Bernoulli trials, and the [binomial](/binomial-distribution/), [geometric](/geometric-distribution/) and [Poisson](/poisson-distribution/) distributions all come from them.

## Definition

**A Bernoulli random variable** with parameter $p \in [0, 1]$ is a [random variable](/random-variable/) $X$ with

$$\Pr(X = 1) = p, \qquad \Pr(X = 0) = 1 - p.$$

We write $q = 1 - p$. The outcome 1 is called success and 0 failure. The [indicator](/indicator-random-variable/) of an event with probability $p$ is a Bernoulli random variable with parameter $p$.

**Bernoulli trials** with success probability $p$ are random variables $X_1, X_2, \ldots$ (finitely or infinitely many) such that each $X_i$ is Bernoulli with parameter $p$ and the $X_i$ are mutually independent: for each finite set $I$ of indices and each choice of values $b_i \in \{0, 1\}$,

$$\Pr(X_i = b_i \text{ for all } i \in I) = \prod_{i \in I} \Pr(X_i = b_i).$$

When the $X_i$ are independent but $X_i$ has its own parameter $p_i$, they are called **Poisson trials** (Mitzenmacher and Upfal, Section 4.2.1). For an infinite sequence, a probability space that carries it exists: it is the product measure on $\{0, 1\}^{\mathbb{N}}$, see the infinite coin flips on the [probability space](/probability-space/) page.

### Properties

**(a) Moments of one trial.** Since $X \in \{0, 1\}$, $X^k = X$ for each $k \ge 1$. So $\mathbb{E}[X^k] = 0 \cdot q + 1 \cdot p = p$. The [variance](/variance/) is $\mathbb{E}[X^2] - \mathbb{E}[X]^2 = p - p^2 = pq$. As a function of $p$, $pq = \frac14 - (p - \frac12)^2$, so the variance is at most $1/4$, with equality only at $p = 1/2$.

**(b) The probability of one sequence.** For $b_1, \ldots, b_n \in \{0, 1\}$ with $k = \sum_i b_i$ ones,

$$\Pr(X_1 = b_1, \ldots, X_n = b_n) = p^k q^{n-k}.$$

This is the product rule, with a factor $p$ for each 1 and $q$ for each 0. Each sequence with the same number of successes has the same probability, whatever the order.

**(c) The number of successes.** $S_n = X_1 + \cdots + X_n$ has the [binomial distribution](/binomial-distribution/): there are $\binom{n}{k}$ sequences with $k$ ones, each of probability $p^k q^{n-k}$ by (b). By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[S_n] = np$. Independence makes the variances add, so $\mathrm{Var}(S_n) = npq$.

**(d) The first success.** For $0 < p \le 1$, the index $T$ of the first success has $\Pr(T = k) = \Pr(X_1 = \cdots = X_{k-1} = 0, X_k = 1) = q^{k-1} p$ by (b). This is the [geometric distribution](/geometric-distribution/). $T$ is finite with probability 1, because $\Pr(T > k) = q^k \to 0$.

**(e) No memory.** The trials after any fixed index $j$, that is $X_{j+1}, X_{j+2}, \ldots$, are again Bernoulli trials with parameter $p$, and they are independent of $X_1, \ldots, X_j$. In particular, $\Pr(X_{j+1} = 1 \mid X_1 = \cdots = X_j = 0) = p$ by independence. A run of failures does not make a success more likely.

## Examples and non-examples

**Skip list levels.** In a [skip list](/skip-list/), each key flips a coin with $\Pr(\text{heads}) = 1/2$ and moves up one level for each heads, until the first tails. The flips of all keys are Bernoulli trials with $p = 1/2$. By (d), the level of a key is geometric, and by (c) the number of keys that reach level 2 or higher among $n$ keys is binomial with mean $n/2$.

**Keys in one bucket.** Under [simple uniform hashing](/simple-uniform-hashing/) with $m$ buckets, let $X_i$ be the indicator that key $i$ hashes to bucket 0. Then $X_1, \ldots, X_n$ are Bernoulli trials with $p = 1/m$, and the load of bucket 0 is binomial$(n, 1/m)$. The loads of different buckets are not independent, since they sum to $n$.

**Amplifying a Monte Carlo test.** A test that, for a "no" input, wrongly says "yes" with probability at most $1/2$, and never errs on "yes" inputs, can be run $t$ times with fresh random bits, answering "no" if any run says "no". For a "no" input, the runs are independent trials, each erring with probability at most $1/2$, so all $t$ runs err with probability at most $2^{-t}$. For $t = 20$ this is $2^{-20} \approx 9.54 \times 10^{-7}$. [Freivalds' algorithm](/freivalds-algorithm/) is a test of this kind.

**A fair coin from a biased coin.** Flip a coin with unknown heads probability $p \in (0, 1)$ in pairs. Output heads on the pair HT, tails on TH, and flip a new pair on HH or TT. By (b), $\Pr(HT) = \Pr(TH) = pq$, so given that the pair is unequal, each output has conditional probability $1/2$. Each pair stops with probability $2pq$, so by (e) and (d) the number of pairs is geometric with mean $1/(2pq)$. For $p = 0.3$: $2pq = 0.42$, the expected number of pairs is $2.381$, and the expected number of flips is $4.762$.

**Non-example: draws without replacement.** A batch of 10 requests holds 3 that will fail. Test them one at a time in random order, and let $X_i$ indicate that the $i$-th tested request fails. Each $X_i$ has $\Pr(X_i = 1) = 3/10$, but $\Pr(X_2 = 1 \mid X_1 = 1) = 2/9 \ne 3/10$. The trials are dependent, and the number of failures in the first $k$ tests is hypergeometric, not binomial. With replacement (each test picks any of the 10), the trials would be Bernoulli.

**Non-example: probes in linear probing.** In [linear probing](/linear-probing/), the event "slot $i$ is full" and "slot $i + 1$ is full" are positively correlated, because full slots form runs. The probes of one search are not Bernoulli trials, which is why the analysis of [linear probing](/linear-probing-analysis/) differs from that of [uniform hashing](/uniform-hashing-assumption/).

### Pitfalls

- **The gambler's fallacy.** After many failures, the next trial still succeeds with probability $p$, by (e). A retry loop does not become more likely to succeed with each failure, unless the cause of the failure changes.
- **Pseudo-random bits are not independent.** The analysis assumes true independence. A poor generator, or a seed reused across trials, breaks it. Repeated runs of a Monte Carlo test must use fresh random bits for the bound $2^{-t}$ to hold.
- **Same parameter is part of the definition.** With different $p_i$ the sum is not binomial. The mean is still $\sum_i p_i$ and the variance $\sum_i p_i q_i$, and Chernoff bounds still apply, but the formulas of the [binomial distribution](/binomial-distribution/) page do not.

## Related definitions

- The [binomial distribution](/binomial-distribution/) is the law of the number of successes in $n$ trials.
- The [geometric distribution](/geometric-distribution/) is the law of the index of the first success.
- The [Poisson distribution](/poisson-distribution/) is the limit of the binomial when $n \to \infty$ and $np \to \lambda$.
- The [Chernoff bound](/chernoff-bound/) and [binomial tail bounds](/binomial-tail-bounds/) bound the probability that the number of successes is far from $np$.
- An [indicator random variable](/indicator-random-variable/) is a Bernoulli variable attached to an event.

## References
