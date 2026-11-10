---
tag: TN0BMK
kind: problem
slug: frequency-moment-problem
name: Frequency moment estimation problem
aliases:
- F_k estimation
- moments of the frequency vector
- F_p estimation
- L_p norm estimation in streams
area: online-and-streaming/streaming-sketches
level: core
summary: Estimate F_k, the sum of the k-th powers of the item counts; F_0 is distinct elements and F_2 is the second moment.
prereqs: [streaming-model, frequency-vector, epsilon-delta-guarantee]
see_also: [ams-sketch, indyk-p-stable-sketch, frequency-moment-lower-bounds, distinct-elements-problem, hyperloglog, join-size-estimation-problem, entropy-estimation-problem, morris-counter]
sources:
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999 (STOC 1996)
    locator: the definition of F_k, the sampling algorithm for F_k, the F_2 sketch, and the lower bounds for F_k with k > 5, for F_∞ and for deterministic algorithms (to check)
  - paper: doi:10.1145/1060590.1060621
    title: Piotr Indyk and David Woodruff, Optimal approximations of the frequency moments of data streams, Proceedings of the 37th ACM Symposium on Theory of Computing (STOC), 2005
    locator: the main theorem, a one-pass algorithm for F_k with k > 2 in n^(1 − 2/k) times polylogarithmic space (to check)
  - paper: doi:10.1016/j.jcss.2003.11.006
    title: Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar and D. Sivakumar, An information statistics approach to data stream and communication complexity, Journal of Computer and System Sciences 68(4), 2004
    locator: the lower bound for F_k with k > 2 through multi-party set disjointness (to check)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 3, Summaries for multisets (F_2 and the AMS sketch, distinct counts), and Chapter 10, Lower bounds for summaries
  - paper: doi:10.1561/0400000002
    title: S. Muthukrishnan, Data Streams, Algorithms and Applications, Foundations and Trends in Theoretical Computer Science 1(2), 2005
    locator: the sections on frequency moments and on norms of streams
---

The frequency moment problem asks for an estimate of $F_p = \sum_i |f_i|^p$, where $f$ is the [frequency vector](/frequency-vector/) of a stream. The cases $p = 0$, $1$, $2$ and $\infty$ are the number of distinct items, the stream length, the self-join size and the largest count. Alon, Matias and Szegedy (1996) posed the problem and started the theory of streaming algorithms with it. The space needed changes sharply at $p = 2$. For $0 \le p \le 2$, a $(1 \pm \varepsilon)$ estimate needs only $O(\varepsilon^{-2} \log(1/\delta))$ words, or polylogarithmic space for fixed $\varepsilon$ and $\delta$. For $p > 2$ it needs $n^{1 - 2/p}$ space up to polylogarithmic factors (Indyk and Woodruff 2005, with matching lower bounds). For $F_\infty$, it needs $\Omega(n)$ space. Here $m$ is the stream length and $n$ the universe size.

## In plain words

Count how often each item occurs in a stream. Now raise every count to some power and add the results. With power zero you get the number of different items. With power one you get the length of the stream. With power two, items that occur often count much more than rare ones, so the sum tells you how skewed the data is. With a very large power, only the most common item matters.

You want a good guess of this sum after one pass, with much less memory than one tally for each item. For powers up to two, a few hundred numbers are enough. For larger powers, the memory must grow with the number of possible items, and for the largest count alone you need memory close to one tally for each item.

## Definition

The input is a stream $\sigma$ of updates $(i, c)$ with $i \in [n] = \{1, \ldots, n\}$, which add $c$ to $f_i$. In the insertion-only (cash register) model every $c = 1$, so the stream is a sequence $a_1, \ldots, a_m$ of items. In the [turnstile model](/turnstile-model/), $c$ can be any integer.

For a real number $p > 0$, the $p$-th frequency moment is
$$ F_p = \sum_{i=1}^n |f_i|^p , $$
and the related norm is $\|f\|_p = F_p^{1/p}$. The limit cases are
$$ F_0 = |\{ i : f_i \ne 0 \}| , \qquad F_\infty = \max_i |f_i| = \lim_{p \to \infty} \|f\|_p . $$
For $F_0$ the convention is $0^0 = 0$. In an insertion-only stream, $F_1 = m$.

The task is to output $\hat F_p$ with
$$ \Pr\left[ (1 - \varepsilon) F_p \le \hat F_p \le (1 + \varepsilon) F_p \right] \ge 1 - \delta , $$
the relative form of the [epsilon-delta guarantee](/epsilon-delta-guarantee/), in one pass and in space much smaller than $n$. The cost is the space in bits, as a function of $n$, $m$, $\varepsilon$ and $\delta$, and the update time.

## Variants

- **The norm or the moment.** An estimate of $\|f\|_p$ within $1 \pm \varepsilon$ gives one of $F_p$ within $1 \pm O(p \varepsilon)$, and the reverse.
- **Insertion only or turnstile.** In the insertion-only model, $F_1 = m$ is one counter. In the turnstile model, $F_1 = \|f\|_1$ needs a sketch, for example a [p-stable sketch](/indyk-p-stable-sketch/) with $p = 1$. The strict turnstile model, with all $f_i \ge 0$ at the end, allows some extra methods.
- **Exact or approximate, deterministic or randomized.** Exact computation of $F_p$ for $p \ne 1$, and any deterministic approximation within a small constant factor, need $\Omega(n)$ bits (Alon, Matias and Szegedy). So the interesting version is randomized and approximate.
- **Several passes.** With $q$ passes, the space for $F_\infty$ drops to $\Theta(n/q)$, and for $p > 2$ the lower bounds also hold with a factor $1/q$.
- **Additive error.** For some uses, $|\hat F_p - F_p| \le \varepsilon \cdot m^p$ is enough, and this is easier.

## Examples

Take the stream $a, b, a, c, a, b$, with $m = 6$ and $f = (f_a, f_b, f_c) = (3, 2, 1)$.

| $p$ | $F_p$ | meaning |
|---|---|---|
| 0 | 3 | three distinct items |
| 1 | $3 + 2 + 1 = 6$ | the stream length |
| 2 | $9 + 4 + 1 = 14$ | the self-join size, the number of equal pairs $(s, t)$ of positions |
| 3 | $27 + 8 + 1 = 36$ | dominated by the most common item |
| $\infty$ | 3 | the largest count |

For a stream where all $m$ items are distinct, $F_2 = m$. For a stream of one item repeated $m$ times, $F_2 = m^2$. So $F_2 / m$ ranges from 1 to $m$ and measures the skew. $F_2$ counts the ordered pairs of positions with the same item, which is the size of the self-join of the stream on the item attribute.

## Known algorithms

- **$F_0$, distinct elements.** See the [distinct elements problem](/distinct-elements-problem/): the [Flajolet-Martin algorithm](/flajolet-martin-algorithm/), [HyperLogLog](/hyperloglog/), and the [KMV sketch](/kmv-sketch/). Kane, Nelson and Woodruff (2010) gave an algorithm with the optimal $O(\varepsilon^{-2} + \log n)$ bits for constant $\delta$.
- **$F_1$.** One counter in the insertion-only model, or $O(\log \log m)$ bits for a constant factor with the [Morris counter](/morris-counter/). In the turnstile model, the Cauchy sketch, the case $p = 1$ of the p-stable sketch.
- **$F_2$.** The [AMS sketch](/ams-sketch/): $O(\varepsilon^{-2} \log(1/\delta))$ counters, each $Z = \sum_i s(i) f_i$ with 4-wise independent signs. Its fast form is a [count sketch](/count-sketch/) with 4-wise independent signs.
- **$0 < p \le 2$.** The [Indyk p-stable sketch](/indyk-p-stable-sketch/) (Indyk 2000, journal 2006) projects $f$ onto vectors of [p-stable](/p-stable-distribution/) random values and takes a median. It uses $O(\varepsilon^{-2} \log(1/\delta))$ counters. Kane, Nelson and Woodruff (2010) reached the optimal bit complexity.
- **$p > 2$.** The AMS sampling estimator picks a random position, counts the later copies $R$ of its item, and outputs $m(R^p - (R - 1)^p)$, which has mean $F_p$; it needs $O(p \, n^{1 - 1/p} \varepsilon^{-2})$ copies. Indyk and Woodruff (2005) gave the first algorithm with $n^{1 - 2/p}$ times polylogarithmic space, by estimating the sizes of the level sets $\{i : |f_i| \approx (1 + \varepsilon)^k\}$ with heavy hitter sketches. Later work, such as the precision sampling of Andoni, Krauthgamer and Onak (2011), simplified it and reduced the polylogarithmic factors.
- **$F_\infty$.** Exact counters for all items, $O(n \log m)$ bits, are optimal up to the $\log m$ factor. For a weaker goal, heavy hitter summaries find the items with $f_i \ge \varepsilon \|f\|_1$ or $\ge \varepsilon \|f\|_2$; see the [frequent items problem](/frequent-items-problem/).

## Bounds

All bounds are for randomized one-pass algorithms with constant $\delta$, unless stated.

| $p$ | upper bound | lower bound |
|---|---|---|
| 0 | $O(\varepsilon^{-2} + \log n)$ bits (Kane, Nelson, Woodruff 2010) | $\Omega(\varepsilon^{-2} + \log n)$ bits |
| $(0, 2]$ | $O(\varepsilon^{-2} \log(mn))$ bits | $\Omega(\varepsilon^{-2} + \log n)$ bits |
| $p > 2$ | $n^{1 - 2/p} \cdot \mathrm{poly}(\varepsilon^{-1} \log n)$ (Indyk, Woodruff 2005) | $\Omega(n^{1 - 2/p})$ (Bar-Yossef et al. 2004; Chakrabarti, Khot, Sun 2003; tight form by Gronemeier 2009 and Jayram 2009) |
| $\infty$ | $O(n \log m)$ bits | $\Omega(n)$ bits (Alon, Matias, Szegedy 1996) |
| any $p \ne 1$, deterministic | $O(n \log m)$ bits | $\Omega(n)$ bits (Alon, Matias, Szegedy 1996) |

The $\Omega(\varepsilon^{-2})$ terms come from the gap Hamming problem (Indyk and Woodruff 2003, Woodruff 2004). The $\Omega(n^{1-2/p})$ bound comes from multi-party set disjointness; see [frequency moment lower bounds](/frequency-moment-lower-bounds/), which also proves the $\Omega(n)$ bound for $F_\infty$ in full. The bounds in the table for $p \in (0, 2]$ and $p = 0$ are cited, not proved here. The threshold at $p = 2$ is sharp: for $p \le 2$ the space does not grow with $n$ beyond logarithmic factors, and for every $p > 2$ it grows polynomially.

## Reductions

- **From set disjointness to $F_\infty$.** Alice holds $A \subseteq [n]$ and Bob holds $B \subseteq [n]$. They stream $A$ and then $B$. The largest count is 2 if $A \cap B \ne \emptyset$ and at most 1 otherwise. So a streaming algorithm that tells $F_\infty \ge 2$ from $F_\infty \le 1$ solves [disjointness](/disjointness-problem/), which needs $\Omega(n)$ bits of [randomized communication](/randomized-communication-complexity/). The same streams give $F_p \ge 2^p$ against $F_p \le n$ after a promise that $|A \cap B| \le 1$, and with $t$ players instead of two this gives the bound for $p > 2$.
- **From exact counts to distinct elements.** With the [INDEX problem](/index-problem-lower-bound/), an exact $F_0$ algorithm needs $\Omega(n)$ bits: Alice streams her set, Bob adds his index, and $F_0$ grows by one only if the index is not in Alice's set.
- **Inner products to $F_2$.** For two vectors, $\langle f, g \rangle = \frac{1}{4}(F_2(f + g) - F_2(f - g))$. So a linear $F_2$ sketch gives estimates of [join sizes](/join-size-estimation-problem/), with an additive error in terms of $F_2(f) + F_2(g)$.
- **Entropy to moments near $p = 1$.** The Shannon entropy of $f/m$ is $-\frac{d}{dp} \log \|f/m\|_p^p$ at $p = 1$, so estimates of $F_p$ for $p$ close to 1 give estimates of the [entropy](/entropy-estimation-problem/).

## Applications

- **Databases.** $F_2$ is the self-join size, used by query optimizers to choose join orders, which was the motivation of Alon, Matias and Szegedy. $F_0$ is the number of distinct values of an attribute.
- **Skew and repeat rate.** $F_2 / m^2$ is the probability that two random positions hold the same item, the repeat rate or collision probability of the data.
- **Network monitoring.** $F_0$ counts distinct flows or sources, $F_2$ and higher moments signal heavy flows and attacks, and $\|f - g\|_2$ between two time windows detects change.
- **Similarity of streams.** With the turnstile model, $\|f - g\|_p$ for the difference of two streams measures how far apart two data sets are, without storing either.

## References
