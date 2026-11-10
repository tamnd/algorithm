---
tag: 9SBD59
kind: algorithm
slug: bernoulli-sampling
name: Bernoulli sampling
aliases:
- Bernoulli sampling with probability p
- geometric skip sampling
area: randomized/sampling
level: intro
summary: Include each item independently with probability p, so the sample size is random.
model: real-ram
complexity:
  vars: {n: the number of items, p: the inclusion probability}
  time: {expected: Θ(1 + n p), worst: O(n)}
  space: {extra: O(1)}
properties: {deterministic: false, exact: true, online: true, recursive: false}
prereqs: [bernoulli-trials, geometric-distribution, independent-random-variables]
see_also: [random-sampling, binomial-distribution, reservoir-sampling, uniform-random-subset, probability-proportional-to-size-sampling, stream-sampling, erdos-renyi-model, inverse-transform-sampling]
sources:
  - book: isbn:9780387975283
    title: Carl-Erik Särndal, Bengt Swensson and Jan Wretman, Model Assisted Survey Sampling, Springer, 1992
    locator: Chapter 3 (Bernoulli sampling and its Horvitz-Thompson estimator)
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter II, Section 2 (inversion), and Chapter X (the geometric distribution)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.4.1 (the geometric distribution by inversion of a uniform deviate)
  - paper: doi:10.1103/PhysRevE.71.036113
    title: Vladimir Batagelj and Ulrik Brandes, Efficient generation of large random networks, Physical Review E 71, 036113, 2005
    locator: the algorithm for the Erdős-Rényi model G(n, p) with geometric skips
  - paper: "Karl Bringmann and Tobias Friedrich, Exact and efficient generation of geometric random variates and random graphs, ICALP 2013, Lecture Notes in Computer Science 7965, Springer, 2013"
    locator: pages 267 to 278
---

Bernoulli sampling keeps each of $n$ items independently with the same probability $p$. The sample size is random, with the [binomial distribution](/binomial-distribution/) $\mathrm{Bin}(n, p)$, and each set $A$ of items is the sample with probability $p^{|A|}(1-p)^{n-|A|}$. The direct method flips one biased coin for each item, in $\Theta(n)$ time. The skip method jumps from one kept item to the next by a [geometric](/geometric-distribution/) number of places, in $\Theta(1 + np)$ expected time, and gives exactly the same law.

## In plain words

Walk along a row of items. For each item, flip a biased coin that shows heads with a fixed chance, for example one in four. Keep the item if the coin shows heads. The items are kept or dropped each on its own, so you do not know in advance how many you keep.

When the chance is small, most flips show tails, and you waste time on them. You can skip them. The number of tails before the next heads follows a known law, and one random number gives it. So you draw that number, jump over that many items, and keep the item where you land. Then you draw again. This keeps exactly the same items in law as the coin flips, but it does work only for the items that you keep.

## The problem

The input is the number of items $n$ and a rate $p \in [0, 1]$. The output is a random set $S \subseteq \{0, \ldots, n-1\}$ with

$$\Pr[S = A] = p^{|A|} (1-p)^{n - |A|} \quad \text{for each } A \subseteq \{0, \ldots, n-1\}.$$

So the events $\{i \in S\}$ are [independent](/independent-random-variables/), each with probability $p$. In survey language, it is a sampling design with inclusion probability $\pi_i = p$ for each unit and $\pi_{ij} = p^2$ for each pair. A sample of fixed size $k$ is a different design: see [uniform random subset](/uniform-random-subset/) and [reservoir sampling](/reservoir-sampling/).

Notation: $n$ is the number of items, $p$ the rate, $q = 1 - p$. The skip method runs on the [real RAM](/real-ram/) with uniform reals in $(0, 1]$ and exact logarithms. The direct method for a rational $p = a/b$ needs only uniform integers.

## The algorithm

```pseudo id=main
BERNOULLI-SAMPLE(n, p)                   ▷ 0 < p < 1
L1  S ← empty list;  i ← −1              ▷ i is the last position visited
L2  loop
L3      G ← GEOMETRIC(p)                 ▷ the number of items to skip
L4      i ← i + G + 1                    ▷ the next kept position
L5      if i ≥ n then return S
L6      append i to S

GEOMETRIC(p)                             ▷ Pr[G = g] = (1 − p)^g p, g = 0, 1, 2, ...
L7  U ← a uniform real in (0, 1]
L8  return ⌊ ln U / ln(1 − p) ⌋
```

GEOMETRIC is [inverse transform sampling](/inverse-transform-sampling/) for the number of failures before the first success in [Bernoulli trials](/bernoulli-trials/). The loop of BERNOULLI-SAMPLE replays those trials: after the last kept position $i$, the next $G$ items fail and item $i + G + 1$ succeeds. When the jump passes the end, the trials of all the remaining items have failed, and the sample is complete. The cases $p = 0$ (return nothing) and $p = 1$ (return everything) are handled before the loop.

**The exact direct method.** For a rational $p = a/b$, keep item $i$ when an independent uniform integer $t_i \in \{0, \ldots, b-1\}$ satisfies $t_i < a$. This has no rounding at all, and it costs $n$ integer draws.

## Example

Take $n = 20$ and $p = 1/4$, so $\ln(1 - p) = \ln 0.75 \approx -0.2877$. One run with a seeded generator gives:

| $U$ | $\ln U / \ln 0.75$ | $G$ | $i$ | action |
|---|---|---|---|---|
| 0.2067 | 5.481 | 5 | $-1 + 5 + 1 = 5$ | keep 5 |
| 0.1780 | 5.999 | 5 | $5 + 5 + 1 = 11$ | keep 11 |
| 0.5150 | 2.307 | 2 | $11 + 2 + 1 = 14$ | keep 14 |
| 0.7384 | 1.054 | 1 | $14 + 1 + 1 = 16$ | keep 16 |
| 0.9995 | 0.002 | 0 | $16 + 0 + 1 = 17$ | keep 17 |
| 0.3372 | 3.779 | 3 | $17 + 3 + 1 = 21$ | stop, $21 \ge 20$ |

The sample is $\{5, 11, 14, 16, 17\}$. The run used 6 uniforms, where the direct method uses 20. The sample size 5 equals the mean $np = 5$ here, but in general it varies: $\Pr[|S| = 5] = \binom{20}{5} 0.25^5\, 0.75^{15} \approx 0.2023$.

## Correctness

GEOMETRIC is correct because $\lfloor \ln U / \ln q \rfloor \ge g$ holds exactly when $U \le q^g$, so $\Pr[G \ge g] = q^g$. For the loop, fix a set $A = \{a_1 < \cdots < a_k\}$ and write $a_0 = -1$. The loop returns $A$ exactly when the skips are $a_j - a_{j-1} - 1$ for $j = 1, \ldots, k$ and the last skip is at least $n - 1 - a_k$. The probability is a product, and the exponents of $q$ telescope to $n - k$. So $\Pr[S = A] = p^k q^{n-k}$, which is the law of independent coins. The full proof is below.

The law is exact in exact arithmetic. With floats, see the pitfalls.

## Complexity

- **Expected time.** The loop runs once for each kept item and once more to stop, so $|S| + 1$ times. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}|S| = np$, so the expected time is $\Theta(1 + np)$, with $1 + np$ uniforms in expectation. The direct method takes $\Theta(n)$ time and $n$ draws.
- **Worst case.** Each skip moves at least one place, so the loop runs at most $n + 1$ times: $O(n)$ for every random string.
- **Concentration.** $|S|$ is a sum of $n$ independent indicators, so the [Chernoff bound](/chernoff-bound/) gives $\Pr[\,|\,|S| - np\,| \ge \delta np\,] \le 2 e^{-\delta^2 np/3}$ for $0 < \delta \le 1$.
- **Space.** $O(1)$ besides the output.

## Properties

- **Exact** in exact arithmetic (skip method) and exactly with integer draws for rational $p$ (direct method).
- **Online.** The kept positions come out in increasing order, and the method needs only the next position. It works on a stream of unknown length: draw a skip and wait for that item. See [stream sampling](/stream-sampling/).
- **Random size.** The size is $\mathrm{Bin}(n, p)$, with variance $np(1-p)$. For a fixed size, use a different design.
- **Unbiased totals.** For values $y_i$, the [Horvitz-Thompson](/probability-proportional-to-size-sampling/) estimator $\frac{1}{p} \sum_{i \in S} y_i$ is an unbiased estimate of $\sum_i y_i$.

## Variants and improvements

- **Poisson sampling.** Each item $i$ has its own probability $\pi_i$. Skips no longer apply directly, but the items can be grouped by probability. This is the design behind [probability proportional to size sampling](/probability-proportional-to-size-sampling/) with a random size.
- **Random graphs.** The [Erdős-Rényi model](/erdos-renyi-model/) $G(n, p)$ is Bernoulli sampling of the $\binom{n}{2}$ possible edges. Batagelj and Brandes generate it in $O(n + m)$ expected time, where $m$ is the number of edges, by geometric skips over the list of pairs.
- **Exact geometric skips.** For a rational $p$, the geometric variate itself can be drawn exactly from random bits, without logarithms. Bringmann and Friedrich (2013) gave such a method with an expected time close to the float one.
- **Conditioning on the size.** Bernoulli sampling conditioned on $|S| = k$ is a [uniform random subset](/uniform-random-subset/) of size $k$.

## When to use it

Use Bernoulli sampling when the items must be kept independently, for example to thin a stream, to keep a fixed fraction of log lines, or to build a random graph. Use the skip method when $p$ is small, since its cost depends on the sample size and not on $n$. Use the direct method with integer draws when $p$ is a simple fraction and exactness matters more than speed, or when $p$ is large. When the sample must have exactly $k$ items, use [reservoir sampling](/reservoir-sampling/) or [Floyd's method](/floyd-sampling/) instead.

## Pitfalls

- **The start of the walk.** Line L1 must start at $i = -1$. With $i = 0$, the first jump of line L4 lands at 1 or later, and item 0 is never kept.
- **$\ln(1 - p)$ for a small $p$.** For $p = 10^{-17}$, the float $1 - p$ rounds to 1, so `log(1 - p)` is 0 and line L8 divides by zero. Compute $\ln(1-p)$ as `log1p(-p)`.
- **$U = 0$.** Many generators return values in $[0, 1)$, and $\ln 0 = -\infty$. Line L7 needs $U \in (0, 1]$: use $1 - U$.
- **The float grid.** With 53-bit uniforms, $U \ge 2^{-53}$, so a skip is never longer than $53 \ln 2 / (-\ln(1-p))$. For $p = 10^{-6}$ this is about $3.7 \cdot 10^7$ items. Such long skips have probability about $2^{-53}$, so the error is of that order, but the method is exact only in exact arithmetic.
- **Rounding $p$.** The direct method with `random() < p` uses the float nearest to $p$, so it is not exact for $p = 1/3$. Use integer draws for a rational $p$.

## Implementations

## History

Bernoulli sampling is one of the basic designs of survey sampling, where Särndal, Swensson and Wretman treat it with its estimators. The geometric law by inversion of a uniform is in Knuth's Volume 2 and in Devroye's book. Skipping over the failures with geometric variates is used for random graphs by Batagelj and Brandes (2005).

## References
