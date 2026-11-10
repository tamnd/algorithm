---
tag: XSTV4C
kind: definition
slug: randomness-extractor
name: Randomness extractor
aliases:
- extractor
- (k, ε)-extractor
area: randomized/derandomization
level: core
summary: A function that turns a weakly random source plus a short uniform seed into an almost uniform output string.
prereqs: [min-entropy, total-variation-distance, randomness-extraction]
see_also: [seeded-extractor, randomness-extraction, leftover-hash-lemma, trevisan-extractor, two-source-extractor, disperser, min-entropy, probabilistic-method]
sources:
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 6 (the definition of extractors, flat sources, the graph view, existence by the probabilistic method, and the lower bounds)
  - paper: doi:10.1006/jcss.1996.0004
    title: Noam Nisan and David Zuckerman, Randomness is linear in space, Journal of Computer and System Sciences 52(1), 1996
    locator: the definition of an extractor with a seed
  - paper: doi:10.1137/S0895480197329508
    title: Jaikumar Radhakrishnan and Amnon Ta-Shma, Bounds for dispersers, extractors, and depth-two superconcentrators, SIAM Journal on Discrete Mathematics 13(1), 2000
    locator: the lower bounds on the seed length and on the entropy loss
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 21 (randomness extractors)
---

A randomness extractor is a function $\mathrm{Ext}(x, s)$ that takes a sample $x$ from a weak random source and a short uniform seed $s$, and outputs a string that is almost uniform. The only promise about the source is a lower bound $k$ on its [min-entropy](/min-entropy/). The seed is needed because no function of the source alone works for all such sources. A random function is an extractor with a seed of about $\log_2(n - k) + 2\log_2(1/\varepsilon)$ bits that keeps all but about $2\log_2(1/\varepsilon)$ bits of the entropy, and Radhakrishnan and Ta-Shma (2000) proved that this is optimal. Explicit constructions, such as the [leftover hash lemma](/leftover-hash-lemma/) and [Trevisan's extractor](/trevisan-extractor/), come close. The general problem is [randomness extraction](/randomness-extraction/).

## Definition

A random variable $X$ on $\{0,1\}^n$ is an *$(n, k)$-source* if $\Pr[X = x] \le 2^{-k}$ for every $x$. It is *flat* if it is uniform on a set of $2^k$ strings. $U_m$ is the uniform distribution on $\{0,1\}^m$. The statistical distance is $\Delta(Y, Z) = \max_T |\Pr[Y \in T] - \Pr[Z \in T]| = \frac12 \sum_z |\Pr[Y = z] - \Pr[Z = z]|$, and $Y$ is *$\varepsilon$-close* to $Z$ if $\Delta(Y, Z) \le \varepsilon$.

**Definition.** A function $\mathrm{Ext} : \{0,1\}^n \times \{0,1\}^d \to \{0,1\}^m$ is a *$(k, \varepsilon)$-extractor* if for every $(n, k)$-source $X$, independent of the uniform seed $U_d$,

$$\Delta\big(\mathrm{Ext}(X, U_d),\ U_m\big) \le \varepsilon.$$

It is a *strong* $(k, \varepsilon)$-extractor if, for every such $X$,

$$\Delta\big((U_d, \mathrm{Ext}(X, U_d)),\ (U_d, U_m)\big) \le \varepsilon,$$

where the same seed appears in both coordinates on the left. The *entropy loss* is $k + d - m$ for an extractor and $k - m$ for a strong extractor. The parameters are the input length $n$, the min-entropy $k$, the seed length $d$, the output length $m$ and the error $\varepsilon$. Write $N = 2^n$, $K = 2^k$, $D = 2^d$ and $M = 2^m$.

**Flat sources are enough.** If $K$ is an integer, every $(n, k)$-source is a convex combination of flat $(n, k)$-sources. *Proof.* The $(n, k)$-sources form the polytope of vectors $p$ with $0 \le p(x) \le 1/K$ and $\sum_x p(x) = 1$. Let $p$ be a vertex. If two coordinates were strictly between $0$ and $1/K$, moving a little mass from one to the other in both directions would stay in the polytope, so $p$ would not be a vertex. So at most one coordinate is strictly between $0$ and $1/K$, and the others are $0$ or $1/K$. Then $\sum_x p(x) = j/K + f$ with $0 \le f < 1/K$, and this equals 1 only if $f = 0$ and $j = K$. So every vertex is flat. $\square$ The distance $\Delta(\mathrm{Ext}(X, U_d), U_m)$ is a convex function of the distribution of $X$, so its maximum over all $(n, k)$-sources is reached at a flat source. The same holds for strong extractors.

**The graph view.** Make a bipartite multigraph with left side $\{0,1\}^n$, right side $\{0,1\}^m$, and an edge from $x$ to $\mathrm{Ext}(x, s)$ for each seed $s$, so each left vertex has degree $D$. Then $\mathrm{Ext}$ is a $(k, \varepsilon)$-extractor if and only if for every set $S$ of $K$ left vertices and every set $T$ of right vertices,

$$\left| \frac{e(S, T)}{KD} - \frac{|T|}{M} \right| \le \varepsilon,$$

where $e(S, T)$ is the number of edges from $S$ to $T$. So an extractor is a graph in which every large enough set on the left sends its edges almost uniformly to the right.

**Strong means most seeds are good.** For a fixed source, $\Delta((U_d, \mathrm{Ext}(X, U_d)), (U_d, U_m))$ is the average over $s$ of $\Delta(\mathrm{Ext}(X, s), U_m)$. So if $\mathrm{Ext}$ is a strong $(k, \varepsilon)$-extractor, Markov's inequality gives, for each $(n, k)$-source and each $\delta > 0$, that at most a fraction $\delta$ of the seeds have $\Delta(\mathrm{Ext}(X, s), U_m) > \varepsilon/\delta$. Which seeds are bad depends on the source.

## Examples and non-examples

**No seed, no extractor.** For $d = 0$, $m \ge 1$ and $k \le n - 1$ there is no $(k, \varepsilon)$-extractor with $\varepsilon < \frac12$. The first output bit is a function $f$ of $x$, one of $f^{-1}(0)$ and $f^{-1}(1)$ has at least $2^{n-1}$ elements, and the uniform distribution on $2^{k}$ of them is an $(n, k)$-source on which $f$ is constant.

**The seed alone is an extractor, but not a strong one.** $\mathrm{Ext}(x, s) = s$ is a $(k, 0)$-extractor with $m = d$ for every $k$, but it extracts nothing from the source: its entropy loss is $k$. As a strong extractor its error is $\Delta((U_d, U_d), (U_d, U_m)) = 1 - 2^{-d}$. This is why the strong definition is the useful one.

**The inner product with the seed.** For $x, s \in \{0,1\}^n$, let $\mathrm{Ext}(x, s) = \langle x, s \rangle = \sum_i x_i s_i \bmod 2$. For $x \ne x'$, $\Pr_s[\langle x, s\rangle = \langle x', s\rangle] = \Pr_s[\langle x \oplus x', s\rangle = 0] = \frac12$, so the family $\{x \mapsto \langle x, s\rangle\}$ is universal. By the [leftover hash lemma](/leftover-hash-lemma/), $\mathrm{Ext}$ is a strong $(k, \varepsilon)$-extractor with $d = n$, $m = 1$ and $\varepsilon = \frac12\sqrt{2^{1-k}}$.

**Universal hashing.** More generally, $\mathrm{Ext}(x, h) = h(x)$ for a universal family of functions $\{0,1\}^n \to \{0,1\}^m$ is a strong $(k, \varepsilon)$-extractor with $m = k - 2\log_2(1/\varepsilon) + 2$. Toeplitz matrices give $d = n + m - 1$.

**Non-example: one bit chosen by the seed.** Let $d = \log_2 n$ and $\mathrm{Ext}(x, s) = x_s$, the bit of $x$ at position $s$. Let $X$ have its first $n - k$ bits equal to 0 and its last $k$ bits uniform; it is a flat $(n, k)$-source. The output is 1 with probability $\frac{k}{n} \cdot \frac12$, so the error is $\frac{n-k}{2n}$, which is $\frac14$ for $k = n/2$. The source chooses where its randomness is, and the seed is too short to find it.

**Non-example: parity of the source.** $\mathrm{Ext}(x) = x_1 \oplus \cdots \oplus x_n$ extracts a perfect bit from every source in which at least one bit is uniform and independent of the others, but it is constant on the $(n, n-1)$-source of all strings with even parity.

**Existence of good extractors.** For all $n$, $k \le n$ and $\varepsilon > 0$, there is a $(k, \varepsilon)$-extractor with

$$d = \left\lceil \log_2(n - k + 2) + 2\log_2(1/\varepsilon) \right\rceil, \qquad m = \left\lfloor k + d - 2\log_2(1/\varepsilon) \right\rfloor.$$

*Proof.* Choose $\mathrm{Ext}$ at random: each of the $ND$ values is uniform in $\{0,1\}^m$ and independent. The choice of $d$ gives $D\varepsilon^2 \ge n - k + 2$, and the choice of $m$ gives $M \le KD\varepsilon^2$. By the flat sources fact it is enough to check flat sources. Fix a set $S$ of $K$ strings and a set $T$ of outputs. The fraction of the $KD$ pairs $(x, s)$ with $x \in S$ and $\mathrm{Ext}(x, s) \in T$ is an average of $KD$ independent indicators with mean $|T|/M$. By Hoeffding's inequality it is more than $\varepsilon$ from its mean with probability at most $2e^{-2\varepsilon^2 KD}$. There are at most $\binom{N}{K} \le (eN/K)^K$ sets $S$ and $2^M$ sets $T$. By the union bound, $\mathrm{Ext}$ fails with probability at most

$$2^M \Big(\frac{eN}{K}\Big)^K \cdot 2 e^{-2\varepsilon^2 KD} = \exp\Big(M \ln 2 + K\big(1 + (n - k)\ln 2\big) + \ln 2 - 2\varepsilon^2 KD\Big).$$

Now $2\varepsilon^2 KD \ge M + K(n - k + 2)$, and $M + K(n - k + 2) > M\ln 2 + K(1 + (n - k)\ln 2) + \ln 2$ because $K \ge 1 > \ln 2$. So the exponent is negative and some choice of $\mathrm{Ext}$ works. $\square$

For example, $n = 20$, $k = 10$ and $\varepsilon = 0.01$ give $D\varepsilon^2 \ge 12$, so $d = 17$ and $m = 13$. The lower bound below gives $d \ge \log_2 10 + 2\log_2 100 - O(1) \approx 16.6 - O(1)$. The proof gives no efficient algorithm: the function is a table with $ND$ entries. With a little more care the same argument gives strong extractors with similar parameters.

**Lower bounds (Radhakrishnan and Ta-Shma 2000, cited).** For $k \le n - 1$ and $\varepsilon \le \frac12$, every $(k, \varepsilon)$-extractor with output longer than its seed has

$$d \ge \log_2(n - k) + 2\log_2(1/\varepsilon) - O(1) \qquad\text{and}\qquad k + d - m \ge 2\log_2(1/\varepsilon) - O(1).$$

So the random extractor above is optimal up to additive constants in both the seed length and the entropy loss. The condition on the output excludes $\mathrm{Ext}(x, s) = s$, which has error 0.

## Related definitions

- **[Seeded extractor](/seeded-extractor/).** The same object, with the emphasis on strong extractors and on explicit constructions with short seeds.
- **[Two-source extractor](/two-source-extractor/).** The seed is replaced by a second independent weak source.
- **[Disperser](/disperser/).** The one-sided version: for every $(n, k)$-source, the output hits all but a fraction $\varepsilon$ of the strings in $\{0,1\}^m$. Every extractor is a disperser.
- **Condenser.** The output is only required to be close to a source of high min-entropy rate, not to uniform. Condensers are a step in the construction of Guruswami, Umans and Vadhan.
- **[Pseudorandom generator](/pseudorandom-generator/).** Trevisan showed that the reconstruction proof of the [Nisan-Wigderson generator](/nisan-wigderson-generator/) gives extractors: the source plays the role of the hard function.
- **[Min-entropy](/min-entropy/).** The measure of randomness used in the definition. Shannon entropy is not enough, because a source can have high Shannon entropy and still put half of its mass on one string.
- **Samplers.** An extractor gives a sampler: from a weak source, the points $\mathrm{Ext}(x, s)$ for all seeds $s$ estimate the mean of every test, for all but few $x$.

## References
