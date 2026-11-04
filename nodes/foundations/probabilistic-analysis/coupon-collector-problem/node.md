---
tag: TBMM12
kind: problem
slug: coupon-collector-problem
name: Coupon collector's problem
aliases:
- coupon collector
area: foundations/probabilistic-analysis
level: intro
summary: Expected number of random draws to collect all n coupons is about n ln n.
prereqs: [geometric-distribution, linearity-of-expectation, harmonic-series, union-bound, chebyshev-inequality]
see_also: [balls-into-bins, birthday-paradox, hiring-problem, streaks, variance, poisson-distribution, random-load-balancing, high-probability-bounds]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Section 5.4 (Balls and bins, the expected number of tosses until every bin holds a ball)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.4 (the geometric distribution and the coupon collector's problem), Section 3.3 (the variance and Chebyshev's inequality for the coupon collector), Section 5.4 (the coupon collector's problem revisited, the sharp threshold)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 3, Section 3.6 (The coupon collector's problem)
  - paper: "P. Erdős and A. Rényi, On a classical problem of probability theory, Magyar Tudományos Akadémia Matematikai Kutató Intézetének Közleményei 6 (1961)"
    locator: pp. 215 to 220, the limit law Pr[T > n ln n + cn] tends to 1 − exp(−e^(−c))
---

The coupon collector's problem asks how many uniformly random draws, with replacement, from $n$ types of coupon are needed until every type has been seen at least once. The number of draws $T$ has mean exactly $nH_n = n\ln n + \gamma n + O(1)$, where $H_n$ is the $n$-th [harmonic number](/harmonic-series/), and it is concentrated: $T = n\ln n + O(n)$ with probability close to 1. The problem is the model behind the time to fill every bin in [balls into bins](/balls-into-bins/), the time for a random process to visit every state, and many [high-probability bounds](/high-probability-bounds/) of randomized algorithms.

## In plain words

A cereal box holds one of several kinds of toy, each kind equally likely. You buy boxes until you have every kind. The first few boxes almost always give a new toy. When you miss only one kind, each box has a small chance of giving it, so you wait a long time. The last few kinds take most of the boxes.

The answer is the number of kinds times the sum of the first that many reciprocals, which grows like the number of kinds times its natural logarithm. With six kinds you expect to buy about fifteen boxes. The real count rarely strays from this value by more than a few times the number of kinds.

## Definition

**Input.** An integer $n \ge 1$. Draws $D_1, D_2, \ldots$ are independent and each is uniform on $\{1, \ldots, n\}$.

**Quantity.** The collection time
$$ T = \min\{t : \{D_1, \ldots, D_t\} = \{1, \ldots, n\}\}. $$
The problem asks for the distribution of $T$: its mean, its variance and its tails.

**Answer in brief.** For each $n \ge 1$ and each real $c \ge 0$:
$$ \mathbb{E}[T] = nH_n, \qquad \operatorname{Var}[T] = n^2 H_n^{(2)} - nH_n < \frac{\pi^2}{6}n^2, $$
$$ \Pr[T > n\ln n + cn] \le e^{-c}, \qquad \Pr[T \le n\ln n - cn] \le 2e^{-c} \quad (n \ge 2), $$
where $H_n^{(2)} = \sum_{k=1}^n 1/k^2$. The proofs are in the Bounds section.

## Variants

- **Collecting $k$ of the $n$ types.** The expected number of draws to see $k$ distinct types is $\sum_{i=0}^{k-1} \frac{n}{n-i} = n(H_n - H_{n-k})$. For $k = n/2$ this is about $n\ln 2 \approx 0.69\,n$, so the first half is cheap and the last half is expensive.
- **Unequal probabilities.** If type $i$ has probability $p_i$, then $\mathbb{E}[T] = \int_0^\infty \bigl(1 - \prod_{i}(1 - e^{-p_i x})\bigr)\,dx$. The formula comes from the Poisson version of the process, in which draws arrive at rate 1, and the two versions have the same mean.
- **Several complete sets (double dixie cup).** Waiting for $m$ copies of each type takes $n\ln n + (m-1)n\ln\ln n + O(n)$ draws. Erdős and Rényi found the limit law of this count.
- **A fixed subset.** Waiting until each of $k$ given types has appeared takes $nH_k$ draws on average, by the same argument with success probabilities $(k - i + 1)/n$.

## Examples

**A die.** For $n = 6$, $\mathbb{E}[T] = 6H_6 = 6 \cdot \frac{49}{20} = 14.7$ throws, with standard deviation $6.24$. The exact distribution, from inclusion and exclusion, gives $\Pr[T \le 6] = 6!/6^6 = 0.0154$, $\Pr[T \le 13] = 0.514$ and $\Pr[T \le 27] = 0.957$. So the median is 13, below the mean, because the distribution has a long right tail.

**Growth with $n$.** The table gives the exact mean $nH_n$, the leading term $n\ln n$, the standard deviation from the exact variance, and the mean of a simulation with numpy (seed 7; 100000, 10000 and 1000 runs).

| $n$ | $nH_n$ | $n\ln n$ | standard deviation | $\text{std}/n$ | simulated mean |
| --- | --- | --- | --- | --- | --- |
| 6 | 14.70 | 10.75 | 6.24 | 1.041 | 14.71 |
| 10 | 29.29 | 23.03 | 11.21 | 1.121 | |
| 100 | 518.74 | 460.52 | 125.82 | 1.258 | 518.73 |
| 365 | 2364.65 | 2153.46 | 465.21 | 1.275 | |
| 1000 | 7485.47 | 6907.76 | 1279.24 | 1.279 | 7503.48 |
| $10^6$ | 14392726.72 | 13815510.56 | 1282543.83 | 1.283 | |

The ratio $\text{std}/n$ tends to $\pi/\sqrt6 = 1.2825$. So the spread is of order $n$ while the mean is of order $n\ln n$.

**The tails at $n = 100$.** The exact tail $\Pr[T > n\ln n + cn]$ from inclusion and exclusion, its limit $1 - e^{-e^{-c}}$, and the bound $e^{-c}$:

| $c$ | $t = \lceil n\ln n + cn \rceil$ | $\Pr[T > t]$ | limit $1 - e^{-e^{-c}}$ | bound $e^{-c}$ |
| --- | --- | --- | --- | --- |
| 0 | 461 | 0.6321 | 0.6321 | 1 |
| 1 | 561 | 0.3024 | 0.3078 | 0.3679 |
| 2 | 661 | 0.1227 | 0.1266 | 0.1353 |
| 3 | 761 | 0.0467 | 0.0486 | 0.0498 |

On the lower side, $\Pr[T \le 360] = 0.0568$ and $\Pr[T \le 260] = 1.8 \times 10^{-4}$, both far below the bound $2e^{-c}$.

## Known algorithms

The problem is a question about a random process, not a task with input and output, so it has no algorithm in the usual sense. Two computations are standard.

- **The exact distribution.** By inclusion and exclusion over the set of types not yet seen,
$$ \Pr[T \le t] = \sum_{k=0}^{n} (-1)^k \binom nk \left(1 - \frac kn\right)^t. $$
The sum has alternating terms that are much larger than the result, so compute it with exact rationals or high precision, not with floating point for large $n$.
- **Simulation.** Keep a boolean array of seen types and a counter of distinct types. Each draw costs $O(1)$, so one run costs $O(n\log n)$ expected time.

## Bounds

All the results follow from one decomposition. Call draw $t$ a *success* when $D_t$ is a type not seen before. Let $T_i$ be the number of draws made while exactly $i - 1$ types are known, for $i = 1, \ldots, n$. Then $T = T_1 + \cdots + T_n$. While $i - 1$ types are known, each draw is new with probability $p_i = \frac{n - i + 1}{n}$, independently of the past. So $T_i$ has the [geometric distribution](/geometric-distribution/) with parameter $p_i$, and $T_1, \ldots, T_n$ are independent.

**The mean, $\mathbb{E}[T] = nH_n$.** A geometric variable with parameter $p$ has mean $1/p$. By [linearity of expectation](/linearity-of-expectation/),
$$ \mathbb{E}[T] = \sum_{i=1}^{n} \frac{n}{n-i+1} = n\sum_{j=1}^{n}\frac1j = nH_n. $$
Since $\ln n < H_n \le \ln n + 1$, this is $n\ln n + \Theta(n)$, and more precisely $nH_n = n\ln n + \gamma n + \frac12 + O(1/n)$.

**The variance.** A geometric variable with parameter $p$ has variance $(1-p)/p^2$. The $T_i$ are independent, so the variances add:
$$ \operatorname{Var}[T] = \sum_{i=1}^{n}\frac{1 - p_i}{p_i^2} = \sum_{j=1}^{n}\frac{1 - j/n}{(j/n)^2} = n^2\sum_{j=1}^{n}\frac{1}{j^2} - n\sum_{j=1}^n\frac1j = n^2H_n^{(2)} - nH_n, $$
where $j = n - i + 1$. This is less than $\frac{\pi^2}{6}n^2$. By [Chebyshev's inequality](/chebyshev-inequality/), $\Pr[|T - nH_n| \ge \lambda n] \le \frac{\pi^2}{6\lambda^2}$ for each $\lambda > 0$.

**Upper tail, $\Pr[T > n\ln n + cn] \le e^{-c}$.** Let $t \ge n\ln n + cn$ be an integer. The event $T > t$ means that some type is missing after $t$ draws. Type $i$ is missing with probability $(1 - 1/n)^t \le e^{-t/n}$. By the [union bound](/union-bound/),
$$ \Pr[T > t] \le n\left(1 - \frac1n\right)^t \le n e^{-t/n} \le n e^{-\ln n - c} = e^{-c}. $$
So $T \le n\ln n + cn$ with probability at least $1 - e^{-c}$, and $T \le 2n\ln n$ with probability at least $1 - 1/n$.

**Lower tail, $\Pr[T \le n\ln n - cn] \le 2e^{-c}$ for $n \ge 2$.** Let $t \le n\ln n - cn$ be a nonnegative integer, and let $X$ be the number of types missing after $t$ draws, so that $T \le t$ exactly when $X = 0$. Write $X = \sum_i I_i$ with $I_i$ the indicator that type $i$ is missing. Then $\Pr[I_i = 1] = q_1 = (1 - 1/n)^t$ and, for $i \ne j$, $\Pr[I_i = I_j = 1] = q_2 = (1 - 2/n)^t$. Since $1 - 2/n \le (1 - 1/n)^2$, we have $q_2 \le q_1^2$, so each covariance $q_2 - q_1^2$ is at most 0 and
$$ \operatorname{Var}[X] \le \sum_i \operatorname{Var}[I_i] \le n q_1 = \mathbb{E}[X]. $$
By Chebyshev's inequality, $\Pr[X = 0] \le \Pr[|X - \mathbb{E}X| \ge \mathbb{E}X] \le \operatorname{Var}[X]/(\mathbb{E}X)^2 \le 1/\mathbb{E}[X]$. Now $\ln(1 - 1/n) = -\ln(1 + \frac{1}{n-1}) \ge -\frac{1}{n-1}$, so
$$ \mathbb{E}[X] = n\left(1 - \frac1n\right)^t \ge n e^{-t/(n-1)} \ge n e^{-\frac{n}{n-1}(\ln n - c)} = n^{-1/(n-1)} e^{cn/(n-1)} \ge \frac{e^{c}}{2}, $$
using $n^{1/(n-1)} \le 2$ for $n \ge 2$ and $c \ge 0$. Hence $\Pr[T \le t] \le 2e^{-c}$.

**Concentration.** Together, for each $c \ge 0$ and $n \ge 2$, $\Pr[|T - n\ln n| > cn] \le 3e^{-c}$. So for each $\varepsilon > 0$ the constant $c = \ln(3/\varepsilon)$ gives $|T - n\ln n| \le cn$ with probability at least $1 - \varepsilon$, whatever $n$ is, and $T/(n\ln n) \to 1$ in probability.

**The sharp threshold.** The two bounds are not tight. Erdős and Rényi (1961) proved that for each fixed real $c$,
$$ \lim_{n\to\infty}\Pr[T > n\ln n + cn] = 1 - e^{-e^{-c}}. $$
So $(T - n\ln n)/n$ converges in distribution to the Gumbel law. Mitzenmacher and Upfal, Section 5.4, prove this with the Poisson approximation of the number of missing types. The lower tail is therefore $e^{-e^{c}}$ in the limit, much smaller than the bound $2e^{-c}$.

## Reductions

- **Balls into bins.** Throwing balls uniformly into $n$ bins until no bin is empty is the same process: the bins are the types. So the expected number of balls is $nH_n$, which is CLRS's form of the question.
- **Random walks and cover times.** A walk on the complete graph with a loop at each vertex moves to a uniformly random vertex at each step. Its cover time is a coupon collector time in which the start vertex is already seen, so its mean is $\sum_{j=1}^{n-1} n/j = nH_{n-1}$.
- **The hiring problem.** The number of hires in the [hiring problem](/hiring-problem/) is also a sum of independent pieces, there indicators with means $1/i$, and its mean is $H_n$. Here the pieces are geometric with means $n/j$, and the mean is $nH_n$.

## Applications

- **Testing and sampling.** To see each of $n$ equally likely outcomes at least once, plan for about $n\ln n + 3n$ samples; then the chance of missing one is at most $e^{-3} \approx 5\%$.
- **Random load balancing.** In [random load balancing](/random-load-balancing/) with $n$ servers, $n\ln n$ requests are needed before every server has received one. Below that, some servers sit idle.
- **Analysis of randomized algorithms.** The bound $\Pr[T > n\ln n + cn] \le e^{-c}$ is a model for many high-probability bounds: the expected time and a tail that is exponentially small in the excess.

## References
