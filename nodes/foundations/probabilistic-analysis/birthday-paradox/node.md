---
tag: ZWA9KR
kind: theorem
slug: birthday-paradox
name: Birthday paradox
aliases:
- Birthday bound
- birthday bound
- birthday paradox bound
- birthday problem
area: foundations/probabilistic-analysis
level: intro
summary: About sqrt(n) random draws from n values yield a repeat with constant probability.
prereqs: [probability-space, independent-events, indicator-random-variable, linearity-of-expectation, union-bound]
see_also: [hash-collision, birthday-attack, pollard-rho, balls-into-bins, coupon-collector-problem, hash-table, cryptographic-hash-function, uniform-hashing-assumption]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Section 5.4 (The birthday paradox, with the analysis by indicator random variables)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5, Section 5.1 (Example, the birthday paradox)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 3, Section 3.1 (Occupancy problems)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.3, Some asymptotic calculations (the function Q(n) and its expansion)
---

The birthday paradox is the fact that among $k$ values drawn uniformly and independently from $n$ possible values, two are equal with probability about $1 - e^{-k^2/(2n)}$, so a repeat becomes likely already at $k \approx 1.18\sqrt n$ draws. For $n = 365$ birthdays, 23 people are enough for a shared birthday with probability $0.5073$. The result bounds the [collisions](/hash-collision/) of a [hash table](/hash-table/), sets the cost of the [birthday attack](/birthday-attack/) on a [cryptographic hash function](/cryptographic-hash-function/), and drives [Pollard's rho method](/pollard-rho/).

## Statement

Let $n \ge 1$ and $k \ge 0$ be integers, let $D_1, \ldots, D_k$ be independent and uniform on a set of $n$ values, and let
$$ p(n, k) = \Pr[D_1, \ldots, D_k \text{ are all distinct}]. $$

**Theorem.**

1. *Exact value.* $p(n,k) = \prod_{i=1}^{k-1}\left(1 - \frac in\right) = \frac{n!}{(n-k)!\,n^k}$ for $k \le n$, and $p(n,k) = 0$ for $k > n$.
2. *Two-sided bound.* For each $k \ge 0$,
$$ 1 - \frac{k(k-1)}{2n} \le p(n,k) \le e^{-k(k-1)/(2n)}. $$
3. *The bound is sharp when $k = o(n^{2/3})$.* If $k - 1 \le n/2$, then
$$ p(n,k) \ge \exp\left(-\frac{k(k-1)}{2n} - \frac{k^3}{3n^2}\right). $$
4. *Threshold.* A repeat has probability at least $1/2$ as soon as $k(k-1) \ge 2n\ln 2$, that is for $k \ge \frac12\bigl(1 + \sqrt{1 + 8n\ln 2}\bigr) \approx 1.1774\sqrt n$. It has probability at most $k^2/(2n)$, so $\Omega(\sqrt n)$ draws are needed for a constant probability.
5. *Pairs.* The expected number of pairs $i < j$ with $D_i = D_j$ is exactly $\binom k2 / n$.

## In plain words

Put people in a room one at a time. The first person cannot share a birthday with anyone. The second must avoid one day, the third two days, and so on. Each new person has only a small chance to match, but the chances add up, because each new person can match any of the people already there. With twenty-three people there are 253 pairs, and each pair matches with a chance of one in 365. So a match is about as likely as not.

The general rule: a repeat becomes likely once the number of draws is about the square root of the number of possible values. It is not likely when the number of draws is a small fraction of that square root.

## Proof

**Part 1.** The event that all $k$ values are distinct is the intersection, for $i = 1, \ldots, k-1$, of the events $A_i$ that $D_{i+1}$ differs from $D_1, \ldots, D_i$. Given that $D_1, \ldots, D_i$ are distinct, they take $i$ values, and $D_{i+1}$ is independent of them and uniform, so $\Pr[A_i \mid A_1 \cap \cdots \cap A_{i-1}] = 1 - i/n$. The chain rule of [conditional probability](/conditional-probability/) gives the product. For $k > n$ some factor is $1 - n/n = 0$.

**Part 2, upper bound.** For each real $x$, $1 - x \le e^{-x}$, because $e^{-x}$ is convex and $1 - x$ is its tangent at $0$. Each factor satisfies $0 \le 1 - i/n \le e^{-i/n}$ when $i \le n$, so
$$ p(n,k) \le \exp\left(-\sum_{i=1}^{k-1}\frac in\right) = e^{-k(k-1)/(2n)}. $$
For $k > n$ the bound is trivial since $p = 0$.

**Part 2, lower bound.** The event that some pair is equal is the union of the $\binom k2$ events $\{D_i = D_j\}$, each of probability $1/n$. By the [union bound](/union-bound/), $1 - p(n,k) \le \binom k2 / n = k(k-1)/(2n)$.

**Part 3.** For $0 \le x \le 1/2$, $\ln(1 - x) \ge -x - x^2$. To see this, let $f(x) = \ln(1-x) + x + x^2$. Then $f(0) = 0$ and $f'(x) = -\frac{1}{1-x} + 1 + 2x = \frac{x(1 - 2x)}{1 - x} \ge 0$ on $[0, \frac12]$. Each $i/n$ with $i \le k - 1 \le n/2$ is in this range, so
$$ \ln p(n,k) \ge -\sum_{i=1}^{k-1}\frac in - \sum_{i=1}^{k-1}\frac{i^2}{n^2} \ge -\frac{k(k-1)}{2n} - \frac{k^3}{3n^2}, $$
because $\sum_{i=1}^{k-1} i^2 = \frac{(k-1)k(2k-1)}{6} \le \frac{k^3}{3}$.

**Part 4.** By Part 2, $p(n,k) \le e^{-k(k-1)/(2n)} \le \frac12$ when $k(k-1) \ge 2n\ln 2$. The quadratic $k^2 - k - 2n\ln 2 \ge 0$ holds for $k \ge \frac12(1 + \sqrt{1 + 8n\ln 2})$. The upper bound $1 - p(n,k) \le k(k-1)/(2n) < k^2/(2n)$ is Part 2 again; it is below a constant $\delta$ when $k < \sqrt{2\delta n}$.

**Part 5.** Let $X_{ij}$ be the indicator of $D_i = D_j$. Given $D_i$, the independent uniform $D_j$ equals it with probability $1/n$, so $\mathbb{E}[X_{ij}] = 1/n$. By [linearity of expectation](/linearity-of-expectation/), the expected number of equal pairs is $\binom k2 / n$. $\square$

## Consequences

**The classical numbers.** For $n = 365$, the table gives the exact probability of a shared birthday $1 - p(365, k)$, the estimate $1 - e^{-k(k-1)/730}$ from Part 2, and the union bound $k(k-1)/730$.

| $k$ | $1 - p(365, k)$ | $1 - e^{-k(k-1)/730}$ | $k(k-1)/730$ |
| --- | --- | --- | --- |
| 5 | 0.0271 | 0.0270 | 0.0274 |
| 10 | 0.1169 | 0.1160 | 0.1233 |
| 20 | 0.4114 | 0.4058 | 0.5205 |
| 22 | 0.4757 | 0.4689 | 0.6329 |
| 23 | 0.5073 | 0.5000 | 0.6932 |
| 30 | 0.7063 | 0.6963 | 1.1918 |
| 41 | 0.9032 | 0.8942 | 2.2466 |
| 57 | 0.9901 | 0.9874 | 4.3726 |
| 70 | 0.9992 | 0.9987 | 6.6164 |

The smallest $k$ with a shared birthday more likely than not is 23; the smallest $k$ for probability $0.9$, $0.99$ and $0.999$ are 41, 57 and 70. Part 4 gives $\lceil \frac12(1 + \sqrt{1 + 2920\ln 2})\rceil = 23$ as well. In a simulation of 200000 groups of 23 random birthdays (seed 3), 50.72 percent of the groups had a shared birthday.

**The expected number of pairs.** Part 5 is the form of CLRS, Section 5.4. The expected number of pairs with the same birthday is at least 1 when $k(k-1) \ge 2 \cdot 365$, that is for $k \ge 28$. This threshold is higher than 23, because the expected count of pairs and the probability of at least one pair are different quantities.

**The first repeat.** Let $R$ be the index of the first draw that repeats an earlier value. Then $R > k$ exactly when the first $k$ draws are distinct, so $\mathbb{E}[R] = \sum_{k=0}^{n}p(n,k) = 1 + Q(n)$, where $Q(n) = \sum_{k \ge 1} \frac{n!}{(n-k)!\,n^k}$ is Ramanujan's function. Knuth, Volume 1, Section 1.2.11.3, gives $Q(n) = \sqrt{\pi n/2} - \frac13 + \frac{1}{12}\sqrt{\pi/(2n)} + O(1/n)$. For $n = 365$, $\mathbb{E}[R] = 24.6166$; for $n = 10^6$ it is $1253.98$.

**Hash values.** For $k$ keys hashed by a uniformly random function into $2^b$ values, the chance of a collision is about $1 - e^{-k^2/2^{b+1}}$. With 64-bit hashes:

| keys | $2^{16}$ | $2^{24}$ | $2^{28}$ | $2^{32}$ | $5.06 \times 10^9$ |
| --- | --- | --- | --- | --- | --- |
| collision probability | $1.2 \times 10^{-10}$ | $7.6 \times 10^{-6}$ | $0.0020$ | $0.3935$ | $0.5004$ |

So a 64-bit hash is safe as a unique identifier for a few million keys but not for four billion. A $b$-bit hash gives only about $b/2$ bits of security against a [birthday attack](/birthday-attack/), which finds a collision in about $2^{b/2}$ evaluations.

**Algorithms that use it.** [Pollard's rho method](/pollard-rho/) finds a factor $p$ of a number after about $\sqrt p$ steps, because a pseudorandom sequence modulo $p$ repeats after $\Theta(\sqrt p)$ steps. In a [hash table](/hash-table/) of $m$ slots, a collision is likely once about $\sqrt m$ keys are inserted, so a hash table must handle collisions even when it is almost empty.

## Tightness

Part 3 shows that the upper bound of Part 2 is the true value up to a factor $e^{-k^3/(3n^2)}$, which tends to 1 when $k = o(n^{2/3})$. In particular the threshold of Part 4 is asymptotically exact: for $k \sim c\sqrt n$, $p(n,k) \to e^{-c^2/2}$, and the probability of a repeat tends to $1/2$ exactly when $c = \sqrt{2\ln 2} = 1.1774\ldots$.

The union bound of Part 2 is sharp for small $k$, and off by at most the factor $1 - 1/e$ while $k(k-1) \le 2n$. Indeed, $1 - e^{-x} \ge (1 - e^{-1})x$ for $0 \le x \le 1$, because $1 - e^{-x}$ is concave and the two sides agree at $x = 0$ and $x = 1$. So for $x = k(k-1)/(2n) \le 1$,
$$ 0.632\,\frac{k(k-1)}{2n} \le 1 - p(n,k) \le \frac{k(k-1)}{2n}. $$

**Non-uniform values.** If the values are not uniform, a repeat is more likely, not less. With probabilities $q_1, \ldots, q_n$, the expected number of equal pairs is $\binom k2\sum_v q_v^2$, and $\sum_v q_v^2 \ge 1/n$ by the Cauchy-Schwarz inequality. Real birthdays are not uniform, so for real data the expected number of shared pairs is at least the uniform value $\binom k2/365$.

### Pitfalls

- **A match with a given person.** The chance that someone in a group of $k - 1$ others shares *your* birthday is $1 - (364/365)^{k-1}$, which reaches $1/2$ only at $k - 1 = 253$. The paradox is about any pair, not a fixed person.
- **Expected pairs versus probability.** The two thresholds 28 and 23 answer different questions. Do not equate "at least one pair is expected" with "a pair has probability $1/2$".
- **$k$ versus $k^2$.** The load of a hash table grows linearly with the number of keys, but the chance of a collision grows with its square while it is small. Doubling the number of keys multiplies a small collision chance by about 4.
- **The square root of the space, not of the key length.** A 128-bit hash has birthday bound $2^{64}$ evaluations, not 64. A 32-bit checksum collides with probability $0.39$ already among $2^{16} = 65536$ random inputs.
- **Computing the product.** For large $n$ and $k$, compute $\ln p(n,k) = \sum_i \ln(1 - i/n)$ with a function such as `log1p`, or use log-gamma. Do not form $n!$.

## History

The standard textbook treatment, with the exact product and the exponential bound, is in CLRS, Section 5.4, in Mitzenmacher and Upfal, Section 5.1, and in Motwani and Raghavan, Section 3.1.

## References
