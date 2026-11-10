---
tag: H30QN2
kind: definition
slug: min-entropy
name: Min-entropy
aliases:
- H_infinity entropy
- guessing entropy
- k-source
area: randomized/derandomization
level: advanced
summary: The negative log of the largest probability of any single outcome; the entropy measure used by extractors.
prereqs: [shannon-entropy, total-variation-distance, convex-combination]
see_also: [randomness-extractor, seeded-extractor, leftover-hash-lemma, santha-vazirani-source, two-source-extractor, disperser, systematic-sampling, von-neumann-debiasing]
sources:
  - paper: doi:10.1137/0217015
    title: Benny Chor and Oded Goldreich, Unbiased bits from sources of weak randomness and probabilistic communication complexity, SIAM Journal on Computing 17(2), 1988
    locator: pages 230 to 261 (sources in which every string has probability at most 2^(-k), and the reduction to flat sources)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1-3), 2012
    locator: Chapter 6, Section 6.1 (min-entropy, k-sources, flat sources and the convex combination lemma)
  - paper: "Alfréd Rényi, On measures of entropy and information, Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability, volume 1, 1961, pages 547 to 561"
    locator: the family of entropies of order alpha, which includes min-entropy as the limit of infinite order and collision entropy as order 2
---

The **min-entropy** of a random variable is $-\log_2$ of the probability of its most likely value. It measures randomness by the worst case: a source with min-entropy $k$ never takes any single value with probability above $2^{-k}$, so even the best guess of its value is right with probability at most $2^{-k}$. This is the measure that [randomness extractors](/randomness-extractor/) need, because a source can have high [Shannon entropy](/shannon-entropy/) and still be constant half of the time. Every distribution with min-entropy at least $k$ is a mixture of uniform distributions on sets of size $2^k$, which lets proofs about extractors consider only those flat sources.

## Definition

Notation. $X$ is a random variable with a finite set of values; $p_x = \Pr[X = x]$. $U_S$ is the uniform distribution on a finite set $S$. $\Delta(X, Y) = \frac{1}{2}\sum_z |\Pr[X = z] - \Pr[Y = z]|$ is the [total variation distance](/total-variation-distance/). Logarithms are base 2.

**Definition.** The min-entropy of $X$ is

$$H_\infty(X) = -\log_2 \max_x p_x = \min_x \log_2 \frac{1}{p_x}.$$

$X$ is a *$k$-source* if $H_\infty(X) \ge k$, that is, $p_x \le 2^{-k}$ for every $x$. A source on $\{0,1\}^n$ has *min-entropy rate* $H_\infty(X)/n$. $X$ is *flat* if it is uniform on its support $S$; then $H_\infty(X) = \log_2 |S|$.

**Comparison with other entropies.** The collision entropy is $H_2(X) = -\log_2 \sum_x p_x^2$, and the Shannon entropy is $H(X) = \sum_x p_x \log_2(1/p_x)$. They satisfy

$$H_\infty(X) \le H_2(X) \le H(X) \le \log_2 |\mathrm{supp}(X)|, \qquad H_2(X) \le 2 H_\infty(X).$$

The first bound holds since $\sum_x p_x^2 \le \max_x p_x \cdot \sum_x p_x = \max_x p_x$. The second and third follow from Jensen's inequality for the concave function $\log_2$: $-H(X) = \mathrm{E}[\log_2 p_X] \le \log_2 \mathrm{E}[p_X] = -H_2(X)$, and $H(X) = \mathrm{E}[\log_2(1/p_X)] \le \log_2 \mathrm{E}[1/p_X] = \log_2|\mathrm{supp}(X)|$. The last follows from $\sum_x p_x^2 \ge (\max_x p_x)^2$. All of them are equal for a flat source. They are the Rényi entropies of orders $\infty$, $2$ and $1$.

**Theorem (convex combination of flat sources).** Let $K \ge 1$ be an integer and let $X$ satisfy $p_x \le 1/K$ for every $x$. Then $X$ is a [convex combination](/convex-combination/) of flat distributions on sets of exactly $K$ values. In particular, every $k$-source with an integer $k$ is a convex combination of flat $k$-sources.

*Proof.* List the values $x_1, x_2, \ldots$ and cut $[0, 1)$ into consecutive half-open intervals $I_j$ of lengths $p_{x_j}$. For $\theta \in [0, 1/K)$ let $P_\theta = \{\theta, \theta + 1/K, \ldots, \theta + (K - 1)/K\}$, a set of $K$ points in $[0, 1)$ with spacing $1/K$, and let $S_\theta$ be the set of values $x_j$ whose interval $I_j$ contains a point of $P_\theta$.

*Each $S_\theta$ has $K$ elements.* Each point lies in exactly one interval. An interval is half-open with length at most $1/K$, so it contains at most one point. Hence the $K$ points lie in $K$ different intervals.

*The mixture is $X$.* Each $t \in [0, 1)$ lies in $P_\theta$ for exactly one $\theta$, namely $\theta = t \bmod 1/K$. Since $I_j$ is half-open with length at most $1/K$, the map $t \mapsto t \bmod 1/K$ is one-to-one on $I_j$. So the set of $\theta$ with $x_j \in S_\theta$ has measure $p_{x_j}$, and for $\theta$ uniform in $[0, 1/K)$, $\Pr[x_j \in S_\theta] = K p_{x_j}$. Pick $\theta$ uniformly and then a uniform element of $S_\theta$. The result is $x_j$ with probability $K p_{x_j} \cdot \frac{1}{K} = p_{x_j}$. So $X = \mathrm{E}_\theta[U_{S_\theta}]$.

*The mixture is finite.* As $\theta$ moves, $S_\theta$ changes only when a point crosses an end of an interval, so only finitely many sets occur. $\square$

This is [systematic sampling](/systematic-sampling/) with $K$ draws: one random start $\theta$ and a fixed step $1/K$.

**Facts.**

1. **Flat sources are enough.** If a function $E$ (with or without a seed) gives output within distance $\varepsilon$ of uniform for every flat $k$-source, it does so for every $k$-source. If $X = \sum_j \alpha_j X_j$ with flat $X_j$, the output distribution is $\sum_j \alpha_j$ times the output distributions for $X_j$, and the triangle inequality gives distance at most $\sum_j \alpha_j \varepsilon = \varepsilon$. Most proofs about [seeded extractors](/seeded-extractor/) and [dispersers](/disperser/) use this.
2. **Operational meaning.** $2^{-H_\infty(X)}$ is the probability that the best single guess of $X$ is right. So min-entropy is the right measure when an adversary gets one guess, for example a guess of a key.
3. **No more than $k$ bits.** If $X$ is flat on $2^k$ values and $f$ maps into $\{0,1\}^m$, then $f(X)$ takes at most $2^k$ values, so $\Delta(f(X), U_{\{0,1\}^m}) \ge 1 - 2^{k - m}$. With a seed of $d$ uniform bits, the same count gives at most $2^{k+d}$ values. So nearly uniform output has at most about $k + d$ bits.
4. **No deterministic extractor for all $k$-sources.** For every $f : \{0,1\}^n \to \{0,1\}$ one preimage has at least $2^{n-1}$ elements. The flat source on $2^{n-1}$ of them is an $(n-1)$-source on which $f$ is constant. This is why extractors for general $k$-sources need a seed or several independent sources.
5. **Conditioning costs at most the length.** For any random variable $Y$ with at most $2^\ell$ values, $\Pr_y\big[H_\infty(X \mid Y = y) \ge H_\infty(X) - \ell - s\big] \ge 1 - 2^{-s}$ for every $s > 0$. Proof: $\Pr[X = x \mid Y = y] \le 2^{-H_\infty(X)}/\Pr[Y = y]$, and the values $y$ with $\Pr[Y = y] < 2^{-\ell - s}$ have total probability less than $2^\ell \cdot 2^{-\ell - s} = 2^{-s}$.

## Examples and non-examples

- **Uniform $n$ bits.** $H_\infty = H_2 = H = n$.
- **High Shannon entropy, low min-entropy.** On $\{0,1\}^4$, put probability $1/2$ on $0000$ and spread the other $1/2$ uniformly over all 16 strings. Then $\Pr[0000] = 17/32$ and every other string has $1/32$. So $H_\infty = \log_2(32/17) \approx 0.9125$, $H_2 = \log_2(1024/304) \approx 1.7521$ and $H \approx 2.8285$. In the same construction on $\{0,1\}^n$, $H$ is about $n/2 + 1$, but every function of $X$ equals its value at $0^n$ with probability at least $1/2$, so no function gives even one almost fair bit. Shannon entropy is an average over many samples; min-entropy speaks about one sample.
- **Flat decomposition.** The distribution $(1/4, 1/4, 1/6, 1/6, 1/12, 1/12)$ on $\{0, \ldots, 5\}$ has $H_\infty = 2$. With $K = 4$, the proof gives the sets $\{0, 1, 2, 3\}$ for $\theta \in [0, 1/12)$, $\{0, 1, 2, 4\}$ for $\theta \in [1/12, 1/6)$ and $\{0, 1, 3, 5\}$ for $\theta \in [1/6, 1/4)$, each with weight $1/3$. Check: value 2 gets $\frac{1}{3}\cdot\frac{1}{4} + \frac{1}{3}\cdot\frac{1}{4} = \frac{1}{6}$, and value 5 gets $\frac{1}{3}\cdot\frac{1}{4} = \frac{1}{12}$.
- **Bit-fixing source.** $n$ bits of which $k$ are uniform and independent and the rest are fixed: a flat $k$-source.
- **Santha-Vazirani source.** A [$\delta$-SV source](/santha-vazirani-source/) on $n$ bits has min-entropy at least $n\log_2\frac{1}{1-\delta}$.
- **Biased coins.** $n$ independent bits with $\Pr[1] = p \le 1/2$ have $H_\infty = n\log_2\frac{1}{1-p}$, which is less than the Shannon entropy $nH(p)$; for $p = 0.1$ these are about $0.152n$ and $0.469n$. Over many samples, [von Neumann debiasing](/von-neumann-debiasing/) and its improvements extract about $nH(p)$ bits, more than the min-entropy, because they use the independence of the bits.
- **Non-example: a large support is not enough.** Let $X$ be $0$ with probability $1/2$ and uniform on $\{1, \ldots, 2^{200}\}$ otherwise. Its support has more than $2^{200}$ values and its Shannon entropy is about 101, but $H_\infty(X) = 1$. An attacker who guesses $0$ is right half of the time, so $X$ cannot serve as a 128-bit key, nor can any function of $X$.

## Related definitions

- [Shannon entropy](/shannon-entropy/): the average of $\log_2(1/p_X)$. It governs compression and long runs of independent samples; min-entropy governs a single sample.
- **Collision entropy** $H_2$: the measure used in the [leftover hash lemma](/leftover-hash-lemma/), where the output of a universal hash is close to uniform if $H_2$, and hence $H_\infty$, is large.
- **Smooth min-entropy**: the largest min-entropy of a distribution within distance $\varepsilon$ of $X$. It is used in cryptography because it changes little under small changes of the distribution.
- **Average conditional min-entropy**: $-\log_2 \mathrm{E}_y[\max_x \Pr[X = x \mid Y = y]]$, where the expectation is the probability of guessing $X$ when $Y$ is known. It drops by at most $\ell$ when $Y$ has $2^\ell$ values (Dodis, Ostrovsky, Reyzin and Smith, 2008).
- [Randomness extractor](/randomness-extractor/), [seeded extractor](/seeded-extractor/) and [two-source extractor](/two-source-extractor/): functions that turn $k$-sources into almost uniform bits. [Dispersers](/disperser/) are their one-sided relatives.
- [Santha-Vazirani source](/santha-vazirani-source/): a special class of sources with linear min-entropy, for which deterministic extraction still fails.

## References
