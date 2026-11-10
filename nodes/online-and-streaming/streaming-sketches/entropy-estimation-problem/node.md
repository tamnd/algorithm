---
tag: MZC8SS
kind: problem
slug: entropy-estimation-problem
name: Entropy estimation problem
aliases:
- empirical entropy of a stream
- streaming entropy estimation
area: online-and-streaming/streaming-sketches
level: advanced
summary: Estimate the empirical Shannon entropy of the item frequencies in a stream.
prereqs: [shannon-entropy, frequency-vector, streaming-model, epsilon-delta-guarantee]
see_also: [frequency-moment-problem, indyk-p-stable-sketch, ams-sketch, reservoir-sampling, boyer-moore-majority, disjointness-problem, gap-hamming-distance, conditional-entropy]
sources:
  - paper: doi:10.1145/1798596.1798604
    title: Amit Chakrabarti, Graham Cormode and Andrew McGregor, A near-optimal algorithm for estimating the entropy of a stream, ACM Transactions on Algorithms 6(3), 2010 (SODA 2007)
    locator: the estimator g(R) − g(R − 1), the special handling of an item with more than half the stream, the space bound, and the lower bound (to check)
  - paper: "Nicholas J. A. Harvey, Jelani Nelson and Krzysztof Onak, Sketching and streaming entropy via approximation theory, Proceedings of the 49th IEEE Symposium on Foundations of Computer Science (FOCS), 2008"
    locator: the reduction to F_p for p near 1, Rényi and Tsallis entropies, and the turnstile algorithms for additive and multiplicative error (to check)
  - paper: doi:10.1145/1140277.1140295
    title: Ashwin Lall, Vyas Sekar, Mitsunori Ogihara, Jun Xu and Hui Zhang, Data streaming algorithms for estimating entropy of network traffic, Proceedings of ACM SIGMETRICS 2006
    locator: the sampling estimator built on the AMS method and its use on network traces (DOI to check)
  - paper: "Amit Chakrabarti, Khanh Do Ba and S. Muthukrishnan, Estimating entropy and entropy norm on data streams, Proceedings of STACS 2006"
    locator: the entropy norm sum_i f_i log f_i and the first sublinear multiplicative bounds (to check)
  - paper: "Sudipto Guha, Andrew McGregor and Suresh Venkatasubramanian, Streaming and sublinear approximation of entropy and information distances, Proceedings of the 17th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2006"
    locator: multiplicative approximation of entropy and information distances in streams (to check)
---

The entropy estimation problem asks for the empirical Shannon entropy of a stream: with $f_i$ the number of times item $i$ occurs and $m$ the stream length, $H = \sum_i \frac{f_i}{m} \log_2 \frac{m}{f_i}$. The entropy is 0 when one item fills the stream and $\log_2 n$ when $n$ items occur equally often, so it measures how spread out the data is. Exact computation needs space linear in the number of items. Chakrabarti, Cormode and McGregor (2007) gave a one-pass $(1 \pm \varepsilon)$ estimate in $O(\varepsilon^{-2}\log(1/\delta))$ words times a logarithmic factor, from an unbiased estimator in the style of the [AMS sampling method](/ams-sketch/). Harvey, Nelson and Onak (2008) solved the problem in the turnstile model through the [frequency moments](/frequency-moment-problem/) $F_p$ for $p$ close to 1.

## In plain words

Count how often each item occurs in a stream, and turn the counts into shares of the whole. The entropy is one number that says how mixed the stream is. If one item fills the whole stream, it is zero. If many items have equal shares, it is large. In bits, it is about how many yes-or-no questions you need on average to guess the next item.

Network operators watch this number for the addresses and ports of their traffic. An attack or a scan changes the mix of addresses suddenly, and the number jumps.

You want a close guess after one pass, without one tally for each item. A random position in the stream, and the count of its item from there on, give a guess that is right on average. Many such guesses, combined with care, give a close answer.

## Definition

The input is a stream $a_1, \ldots, a_m$ of items from $[n]$, with [frequency vector](/frequency-vector/) $f$. The *empirical entropy* is
$$ H(f) = \sum_{i : f_i > 0} \frac{f_i}{m} \log_2 \frac{m}{f_i} = \log_2 m - \frac{1}{m}\sum_i f_i \log_2 f_i , $$
the [Shannon entropy](/shannon-entropy/) of the distribution $(f_i / m)_i$. The sum $\sum_i f_i \log_2 f_i$ is the *entropy norm*. Always $0 \le H \le \log_2 \min(n, m)$.

- **Additive version.** Output $\hat H$ with $|\hat H - H| \le \varepsilon$ with probability at least $1 - \delta$.
- **Multiplicative version.** Output $\hat H$ with $(1 - \varepsilon) H \le \hat H \le (1 + \varepsilon) H$ with probability at least $1 - \delta$. This is harder when $H$ is close to 0, which happens when one item has almost all of the stream.

## Variants

- **Turnstile streams.** Updates $(i, c)$ with $c$ of any sign, and $H$ defined from the final $f \ge 0$ with $m = \sum_i f_i$. Sampling methods fail here; linear sketches work.
- **Rényi and Tsallis entropies.** $H_p = \frac{1}{1 - p}\log_2 \sum_i (f_i/m)^p$ and $T_p = \frac{1 - \sum_i (f_i/m)^p}{p - 1}$. As $p \to 1$, $H_p$ tends to the Shannon entropy in bits and $T_p$ tends to it in natural units. Both are functions of $F_p$ and $m$.
- **Sliding windows.** The entropy of the last $W$ items, for traffic monitoring.
- **Conditional and joint entropy, and information distances.** For pairs $(x, y)$ in the stream, the empirical [conditional entropy](/conditional-entropy/) $H(Y \mid X) = H(X, Y) - H(X)$ needs two entropy estimates. Guha, McGregor and Venkatasubramanian (2006) studied such distances.
- **Higher-order entropy of a string.** The $k$-th order empirical entropy, the average entropy of the next symbol given the $k$ previous ones, measures how well a string compresses.
- **Entropy of an unknown distribution from samples.** Here the items are independent samples from a distribution, and the goal is the entropy of the distribution, not of the sample. This is a statistics problem with its own bounds (Paninski 2003; Valiant and Valiant 2011, with about $n / \log n$ samples), and it is different from the streaming problem.

## Examples

**A small stream.** For $\texttt{abacab}$, $m = 6$ and $f = (3, 2, 1)$ for $a, b, c$. Then
$$ H = \tfrac{3}{6}\log_2 2 + \tfrac{2}{6}\log_2 3 + \tfrac{1}{6}\log_2 6 \approx 0.5 + 0.5283 + 0.4308 = 1.4591 \text{ bits}. $$
The entropy norm is $3\log_2 3 + 2\log_2 2 = 6.7549$, and $\log_2 6 - 6.7549/6 = 1.4591$ as well.

**The sampling estimator.** Let $g(r) = r \log_2 (m / r)$ with $g(0) = 0$. Pick a position $J$ uniformly at random, and let $R$ be the number of positions $j \ge J$ with $a_j = a_J$. Output $X = g(R) - g(R - 1)$. For $\texttt{abacab}$:

| $J$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $a_J$ | a | b | a | c | a | b |
| $R$ | 3 | 2 | 2 | 1 | 1 | 1 |
| $X$ | $-0.1699$ | $0.5850$ | $0.5850$ | $2.5850$ | $2.5850$ | $2.5850$ |

The mean over the six positions is $8.7549 / 6 = 1.4591 = H$. This is no accident: for each item $i$, its $f_i$ positions give $R = f_i, f_i - 1, \ldots, 1$, so their values of $X$ telescope to $g(f_i) - g(0) = g(f_i)$, and
$$ \mathbb{E}[X] = \frac{1}{m}\sum_i g(f_i) = \sum_i \frac{f_i}{m}\log_2\frac{m}{f_i} = H . $$
The position $J$ is chosen in one pass with [reservoir sampling](/reservoir-sampling/), and $R$ is counted after it. If $m$ is not known in advance, the estimator is computed for the final $m$ at the end, because $R$ does not depend on $m$. The same telescoping idea gives the AMS estimator for $F_k$.

**Extreme cases.** A stream with one item repeated $m$ times has $H = 0$. A stream of $m$ distinct items has $H = \log_2 m$. A stream where one item has $m - 1$ positions and another has one has $H = \frac{m-1}{m}\log_2\frac{m}{m-1} + \frac{1}{m}\log_2 m \approx \frac{\log_2 m + \log_2 e}{m}$, which is close to 0: a multiplicative estimate must see the one rare item.

## Known algorithms

| algorithm | model | guarantee and space |
|---|---|---|
| Exact counting | any | exact, $O(n \log m)$ bits |
| Lall, Sekar, Ogihara, Xu, Zhang 2006 | insertion-only | the sampling estimator above, averaged and combined with medians; good when $H$ is not too small |
| Chakrabarti, Do Ba, Muthukrishnan 2006 | insertion-only | multiplicative estimates of $H$ and of the entropy norm in sublinear space |
| Guha, McGregor, Venkatasubramanian 2006 | insertion-only | multiplicative estimates of $H$ and of information distances |
| Chakrabarti, Cormode, McGregor 2007 | insertion-only | $(1 \pm \varepsilon)$ multiplicative, $O(\varepsilon^{-2}\log(1/\delta))$ words times a $\log m$ factor (exact form to check) |
| Harvey, Nelson, Onak 2008 | turnstile | additive and multiplicative, from estimates of $F_p$ at several $p$ near 1, in $\tilde O(\varepsilon^{-2})$ space |

The algorithm of Chakrabarti, Cormode and McGregor runs many copies of the sampling estimator. Its main new idea handles a stream with one item $i^*$ above half of $m$, where $H$ is small and the estimator has a large variance relative to $H$. It finds $i^*$ with a majority algorithm such as [Boyer-Moore](/boyer-moore-majority/), keeps a backup sample from the stream without $i^*$, and computes the contribution of $i^*$ separately from its estimated count.

The algorithm of Harvey, Nelson and Onak uses the fact that $F_p$ near $p = 1$ determines $H$. It estimates $F_p$ with [stable sketches](/indyk-p-stable-sketch/) at a few values of $p$ close to 1, and interpolates the Rényi or Tsallis entropy with a polynomial at Chebyshev points, where the interpolation error is controlled.

## Bounds

**Exact computation needs $\Omega(n)$ bits.** This follows from a reduction from [set disjointness](/disjointness-problem/), proved below. An additive error below $\frac{1}{2n}$ needs $\Omega(n)$ bits too.

**The error needs $\Omega(\varepsilon^{-2})$ space up to logarithmic factors.** Chakrabarti, Cormode and McGregor proved a lower bound of order $\varepsilon^{-2}$ divided by a power of $\log(1/\varepsilon)$ for the multiplicative version, by a reduction from [gap Hamming distance](/gap-hamming-distance/) (exact form to check). So their algorithm is optimal up to logarithmic factors.

**Polylogarithmic upper bounds.** For fixed $\varepsilon$ and $\delta$, both the insertion-only and the turnstile versions take space polylogarithmic in $n$ and $m$. So entropy is in the easy range of the [frequency moment problem](/frequency-moment-problem/), like $F_p$ for $p \le 2$, and unlike $F_p$ for $p > 2$.

## Reductions

**From set disjointness (exact entropy).** Alice holds $A \subseteq [n]$ and Bob holds $B \subseteq [n]$. Alice streams the elements of $A$ and sends the memory state and $|A|$ to Bob, who streams $B$; so $m = |A| + |B|$ is known to Bob. Let $t = |A \cap B|$. Then $t$ items have count 2 and $m - 2t$ items have count 1, so
$$ H = \frac{m - 2t}{m}\log_2 m + \frac{2t}{m}\log_2\frac{m}{2} = \log_2 m - \frac{2t}{m} . $$
So $H = \log_2 m$ when the sets are disjoint and $H \le \log_2 m - \frac{2}{m}$ when they meet. An estimate with additive error below $\frac1m$, and in particular below $\frac{1}{2n}$ since $m \le 2n$, decides disjointness. Disjointness needs $\Omega(n)$ bits of communication with randomness, so a one-pass algorithm needs $\Omega(n)$ bits of memory, and a $q$-pass algorithm $\Omega(n/q)$, as in the [frequency moment lower bounds](/frequency-moment-lower-bounds/).

**To frequency moments near $p = 1$.** Let $q_i = f_i / m$. Then $\frac{d}{dp}\sum_i q_i^p = \sum_i q_i^p \ln q_i$, which at $p = 1$ is $-H$ in natural units. So
$$ H_{\ln} = -\frac{d}{dp}\Big(\frac{F_p}{m^p}\Big)\Big|_{p=1}, \qquad H_{\ln} = \lim_{p \to 1}\frac{1 - F_p / m^p}{p - 1} . $$
Estimates of $F_p$ for a few $p$ near 1, and of $m = F_1$, give $H$ by numerical differentiation or interpolation. The difficulty is that the difference quotient divides by $p - 1$, so the estimates of $F_p$ must have relative error much smaller than $|p - 1|$; Harvey, Nelson and Onak chose the points and the error so that the total space is $\tilde O(\varepsilon^{-2})$.

**To and from heavy hitters.** If no item has more than half the stream, then every $f_i/m \le \frac12$, so $H \ge \sum_i \frac{f_i}{m}\log_2 2 = 1$ bit, and an additive error of $\varepsilon$ is a multiplicative error of $O(\varepsilon)$. So the multiplicative version reduces to the additive one plus the case of one heavy item, which a majority algorithm finds.

## Applications

- **Network anomaly detection.** The entropy of source addresses, destination addresses and ports changes sharply under denial-of-service attacks, port scans and worms. Lakhina, Crovella and Diot (2005) used these entropies to find anomalies, and Lall et al. (2006) gave streaming estimates for line-rate monitoring.
- **Database and data summaries.** Entropy and conditional entropy of attributes help to choose indexes, find functional dependencies, and select features.
- **Compression.** The empirical entropy, and its higher-order versions, bound how well a stream compresses with entropy coding.
- **Testing and comparing distributions.** Information distances between two streams, such as the Jensen-Shannon divergence, reduce to entropies of mixtures.

## References
