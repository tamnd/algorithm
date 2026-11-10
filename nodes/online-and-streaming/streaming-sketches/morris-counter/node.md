---
tag: V4GE3S
kind: algorithm
slug: morris-counter
name: Morris counter
aliases:
- Morris approximate counter
- Morris algorithm
- probabilistic counter
area: online-and-streaming/streaming-sketches
level: intro
summary: Stores only the exponent of the count and increments it with probability 2^-x.
solves: [approximate-counting-problem]
model: word-ram
complexity:
  vars: {n: the number of increments}
  time: {worst: O(1), average: O(1)}
  space: {extra: O(log log n)}
properties: {online: true, deterministic: false}
history:
  year: 1978
  people: [Robert Morris]
  note: Morris published the counter in Communications of the ACM in 1978. Flajolet gave a full analysis of its distribution in 1985.
prereqs: [approximate-counting-problem, expected-value, variance, chebyshev-inequality, median-trick]
see_also: [epsilon-delta-guarantee, cash-register-model, streaming-model, markov-inequality, flajolet-martin-algorithm, loglog-counting, approximate-counting, geometric-distribution]
sources:
  - paper: doi:10.1145/359619.359627
    title: Robert Morris, Counting large numbers of events in small registers, Communications of the ACM 21(10), 1978
    locator: pp. 840 to 842 (the counter, the base change and the variance)
  - paper: doi:10.1007/BF01934993
    title: Philippe Flajolet, Approximate counting, a detailed analysis, BIT 25(1), 1985
    locator: pp. 113 to 134 (the exact distribution of the register and its moments)
  - paper: doi:10.1145/3517804.3526225
    title: Jelani Nelson and Huacheng Yu, Optimal bounds for approximate counting, PODS 2022
    locator: pp. 119 to 127 (the optimal space Θ(log log n + log(1/ε) + log log(1/δ)))
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 2, Section 2.1, Morris Approximate Counter
---

The Morris counter counts up to $n$ events in $O(\log \log n)$ bits instead of the $\lceil \log_2 (n+1) \rceil$ bits of an exact counter. It keeps only a small register $X$, which is about $\log_2 n$, and adds 1 to it with probability $2^{-X}$ at each event. The estimate $2^X - 1$ is unbiased, with variance $n(n-1)/2$. It solves the [approximate counting problem](/approximate-counting-problem/) and is the oldest streaming sketch: Robert Morris wrote it at Bell Labs to count many kinds of events in 8-bit registers. On this page $n$ is the number of increments so far, and the stream is a sequence of increments with no deletions ([cash register model](/cash-register-model/) with unit updates).

## In plain words

An exact counter must be able to hold every number up to the count, so it needs about as many bits as the count has binary digits. The Morris counter keeps only the number of digits. When an event comes, it flips coins. If all of the coins come up heads, it moves the register up by one. The number of coins is the value of the register, so each step up is half as likely as the last one. After many events the register is near the number of digits of the true count, and the counter reports the number that has that many digits on average. A single counter is often off by a large factor, so in practice you run many copies and take the average or the median.

## The problem

The input is a stream of $n$ events, with $n$ not known in advance. At any time, a query must return an estimate $\hat n$ of the number of events so far. The goal is a small state, with a guarantee in the form of the [(ε, δ) guarantee](/epsilon-delta-guarantee/): $\Pr[|\hat n - n| > \varepsilon n] < \delta$. An exact counter uses $\lceil \log_2(n+1) \rceil$ bits, and each deterministic counter needs that many (see the problem page).

## The algorithm

```pseudo id=main
MORRIS(σ)                                  ▷ σ is a stream of events
L1  X ← 0
L2  for each event of σ do
L3      b ← X fresh random bits
L4      if b = 0 then X ← X + 1            ▷ all X bits are 0: probability 2^(−X)
L5  return 2^X − 1
```

The query of line L5 can run at any time; it does not change $X$. Line L3 draws $X$ bits, but it can stop at the first 1 bit. Then an event costs at most 2 random bits on average.

**Morris(a), the base change.** Morris also gave a version with a parameter $a \in (0, 1]$. Line L4 adds 1 with probability $(1+a)^{-X}$, and line L5 returns $((1+a)^X - 1)/a$. The base 2 version is $a = 1$. A smaller $a$ gives a smaller error and a larger register.

**Morris+ and Morris++.** Morris+ runs $s$ independent copies and returns the mean of their estimates. Morris++ runs $t$ independent copies of Morris+, with $t$ odd, and returns the median. This is the [median trick](/median-trick/).

## Example

Three increments. The first event raises $X$ to 1 with probability $2^0 = 1$. The second raises it to 2 with probability $1/2$. The third raises it from 1 to 2 with probability $1/2$, or from 2 to 3 with probability $1/4$.

| $X$ after 3 events | probability | estimate $2^X - 1$ |
|---|---|---|
| 1 | 1/4 | 1 |
| 2 | 5/8 | 3 |
| 3 | 1/8 | 7 |

The mean is $1/4 + 15/8 + 7/8 = 3$, the true count. The mean square is $1/4 + 45/8 + 49/8 = 12$, so the variance is $12 - 9 = 3 = 3 \cdot 2/2$.

After four events the distribution of $X = 1, 2, 3, 4$ is $1/8, 19/32, 17/64, 1/64$, with estimates $1, 3, 7, 15$. The mean is 4 and the variance is $22 - 16 = 6 = 4 \cdot 3/2$.

## Correctness

The key fact is that one event raises $2^X$ by exactly 1 in expectation: with probability $2^{-X}$ the value $2^X$ grows by $2^X$, and otherwise it stays. So $\mathbb{E}[2^{X_n}] = n + 1$ and the estimate of line L5 is unbiased. The same step for $4^X$ gives $\mathbb{E}[4^{X_n}] = 1 + 3n(n+1)/2$, so the variance is $n(n-1)/2$. For Morris(a) the estimate is again unbiased, with variance $a\,n(n-1)/2$. The proofs are below, with the bounds for Morris+, Morris++ and the size of $X$.

## Complexity

All the bounds in this section are proved on the proof page, except the optimal bound of Nelson and Yu, which is cited.

- **Update time.** $O(1)$ word operations per event: draw the bits of line L3 and compare. With the early stop, the expected number of random bits per event is less than 2.
- **Query time.** $O(1)$: one power of 2.
- **Space of one counter.** $\Pr[X_n \ge \log_2(n+1) + c] \le 2^{-c}$ for each $c \ge 0$, by [Markov's inequality](/markov-inequality/) on $2^X$. So with probability $1 - 2^{-c}$ the register fits in $\lceil \log_2(\log_2(n+1) + c + 1) \rceil = O(\log \log n)$ bits. There are no hash seeds; the random bits are fresh at each event and are not stored.
- **One counter is weak.** By [Chebyshev's inequality](/chebyshev-inequality/), $\Pr[|\hat n - n| \ge \varepsilon n] \le (n-1)/(2 \varepsilon^2 n) < 1/(2\varepsilon^2)$. This is useful only for $\varepsilon > 1/\sqrt 2$.
- **Morris+.** With $s = \lceil 3/(2\varepsilon^2) \rceil$ copies the failure probability is below $1/3$.
- **Morris++.** With $t = O(\log(1/\delta))$ copies of Morris+, the failure probability is below $\delta$. The space is $O(\varepsilon^{-2} \log(1/\delta) \log\log(n/(\varepsilon\delta)))$ bits with probability $1 - \delta$.
- **Morris(a).** With $a = 2\varepsilon^2\delta$, Chebyshev gives a failure probability below $\delta$ from one counter, and the register needs $O(\log\log n + \log(1/\varepsilon) + \log(1/\delta))$ bits with probability $1 - \delta$.
- **Optimal space (cited).** Nelson and Yu (2022) prove that $\Theta(\log\log n + \log(1/\varepsilon) + \log\log(1/\delta))$ bits are necessary and sufficient, and that a small change of Morris(a) reaches the bound.

## Properties

- **Unbiased at each time.** $\mathbb{E}[2^{X_n} - 1] = n$ for each $n$, not only in the limit.
- **Randomized, not deterministic.** A deterministic counter with a constant relative error still needs $\log_2 n - O(1)$ bits (proof on the [problem page](/approximate-counting-problem/)). The saving comes only from the coins.
- **Online.** The state after each event is a valid counter for the prefix.
- **Monotone.** $X$ never goes down. The estimate takes only the values $2^k - 1$.
- **Increments only.** There is no decrement. A turnstile counter needs other methods.

## Variants and improvements

- **Base change.** Morris(a) of the algorithm section. Morris already proposed it, to trade register size for accuracy.
- **Averaging and the median.** Morris+ and Morris++ give any $(\varepsilon, \delta)$ from the base 2 counter.
- **Flajolet's analysis.** Flajolet (1985) found the exact distribution of $X_n$ and the asymptotic mean and variance of $X_n$, with small periodic terms.
- **Adding $k$ at once.** To add $k$ events, draw the gap to the next raise from a [geometric distribution](/geometric-distribution/) with parameter $2^{-X}$, and repeat. The cost is $O(1)$ per raise, not per event. The implementation has this as `increment_by`.
- **Optimal counters.** The counter of Nelson and Yu (2022) reaches the lower bound in $\delta$.
- **Related sketches.** The same idea, keep only the position of a rare event, is the base of the [Flajolet-Martin algorithm](/flajolet-martin-algorithm/) and of [LogLog counting](/loglog-counting/) for distinct items.

## When to use it

Use a Morris counter when you keep very many counters at the same time and each one can be large, for example per-key event counts in a router, a cache or a database. Then 8 or 16 bits per counter in place of 32 or 64 bits is a real saving. For one counter, a 64-bit integer is cheaper and exact.

## Pitfalls

- **A single base 2 counter.** Its relative standard deviation is about $1/\sqrt 2$. Average many copies, or use a smaller base, before you trust the value.
- **Reusing random bits.** The bits of line L3 must be fresh and independent at each event. A fixed pseudo-random sequence restarted for each counter makes the copies of Morris+ dependent, and then the average does not reduce the variance.
- **Wrong estimate for Morris(a).** If you change the probability of line L4 to $(1+a)^{-X}$, you must also change line L5 to $((1+a)^X - 1)/a$. With $2^X - 1$ the estimate is biased.
- **Biased median.** The median of Morris++ is not unbiased. Use the mean when you need an unbiased value, and the median when you need a tail bound.

## Implementations

## History

Robert Morris wrote the counter at Bell Labs, to count events in 8-bit registers, and published it in 1978. Philippe Flajolet gave the full analysis of the distribution of the register in 1985, with the methods of analytic combinatorics. Nelson and Yu proved the optimal space bound in 2022, and showed that a Morris counter with a small change reaches it.

## References
