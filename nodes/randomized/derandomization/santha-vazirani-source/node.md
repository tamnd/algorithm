---
tag: RZ8CZ6
kind: definition
slug: santha-vazirani-source
name: Santha-Vazirani source
aliases:
- SV source
- weak random source
- semi-random source
- slightly random source
area: randomized/derandomization
level: advanced
summary: A bit source in which each bit has conditional probability bounded away from 0 and 1 given all previous bits.
prereqs: [conditional-expectation, min-entropy, randomness-extractor]
see_also: [von-neumann-debiasing, seeded-extractor, two-source-extractor, entropy-source, bpp, randomness-amplification]
sources:
  - paper: doi:10.1016/0022-0000(86)90044-9
    title: Miklos Santha and Umesh V. Vazirani, Generating quasi-random sequences from semi-random sources, Journal of Computer and System Sciences 33(1), 1986
    locator: pages 75 to 87 (the definition of semi-random sources, the impossibility of deterministic extraction of one bit, and the XOR of independent sources)
  - paper: doi:10.1109/sfcs.1985.45
    title: Umesh V. Vazirani and Vijay V. Vazirani, Random polynomial time is equal to slightly-random polynomial time, FOCS 1985
    locator: pages 417 to 428 (simulation of randomized polynomial time algorithms with one semi-random source)
  - paper: doi:10.1137/0217015
    title: Benny Chor and Oded Goldreich, Unbiased bits from sources of weak randomness and probabilistic communication complexity, SIAM Journal on Computing 17(2), 1988
    locator: pages 230 to 261 (probability-bounded sources, which contain the SV sources, and extraction from two independent sources)
---

A **Santha-Vazirani source** with parameter $\delta$ is a random string of bits in which every bit is 1 with probability between $\delta$ and $1 - \delta$, given any values of the bits before it. It models a physical source whose bits are somewhat random but may depend on the past in an unknown, even adversarial, way. Santha and Vazirani (1986) proved that no deterministic function can extract even one almost fair bit from all such sources: for every function there is a source that makes it no better than a single bit of the source. Randomized algorithms can still use SV sources, with tools that are not deterministic extractors.

## Definition

Notation. $X = (X_1, \ldots, X_n)$ is a random variable on $\{0,1\}^n$, and $X_{<i} = (X_1, \ldots, X_{i-1})$. $\delta \in (0, 1/2]$. For a bit $Z$, $\mathrm{bias}(Z) = |\Pr[Z = 1] - \Pr[Z = 0]|$.

**Definition.** $X$ is a *$\delta$-SV source* if for every $i \in \{1, \ldots, n\}$ and every prefix $y \in \{0,1\}^{i-1}$ with $\Pr[X_{<i} = y] > 0$,

$$\delta \le \Pr[X_i = 1 \mid X_{<i} = y] \le 1 - \delta.$$

For $\delta = 1/2$ this is the uniform distribution. Some authors write the condition as $\frac{1}{2} - \gamma \le \Pr[X_i = 1 \mid X_{<i} = y] \le \frac{1}{2} + \gamma$, so $\gamma = \frac{1}{2} - \delta$. The source is a class of distributions: an algorithm that uses an SV source must work for every distribution in the class.

**Facts.**

1. **Min-entropy.** Every string has probability at most $(1 - \delta)^n$, since its probability is a product of $n$ conditional probabilities, each at most $1 - \delta$. So the [min-entropy](/min-entropy/) of a $\delta$-SV source is at least $n \log_2 \frac{1}{1 - \delta}$, a constant fraction of $n$. SV sources are a special case of sources with high min-entropy.

2. **No deterministic extractor (Santha and Vazirani 1986).** For every $n \ge 1$, every $\delta \in (0, 1/2)$ and every function $f : \{0,1\}^n \to \{0,1\}$, there is a $\delta$-SV source $X$ and a bit $b$ with $\Pr[f(X) = b] \ge 1 - \delta$, so $\mathrm{bias}(f(X)) \ge 1 - 2\delta$. The bound is tight: the function $f(x) = x_1$ has bias at most $1 - 2\delta$ on every $\delta$-SV source. So no function of the whole string beats the first bit alone.

   *Proof.* Let $b$ be a value with $|f^{-1}(b)| \ge 2^{n-1}$; one exists because the two preimages partition $\{0,1\}^n$. Let $\lambda = (1 - \delta)/\delta > 1$. Give each $x \in f^{-1}(b)$ the weight $w(x) = \lambda$ and every other $x$ the weight $w(x) = 1$, and let $\Pr[X = x] = w(x)/W$ with $W = \sum_x w(x)$.

   *$X$ is a $\delta$-SV source.* Fix $i$ and a prefix $y$ of length $i - 1$. For $c \in \{0, 1\}$, let $A_c$ be the total weight of the $2^{n-i}$ strings that start with $y c$. Each weight lies in $[1, \lambda]$, so $2^{n-i} \le A_c \le \lambda 2^{n-i}$, and $A_0/A_1 \le \lambda$ and $A_1/A_0 \le \lambda$. Hence
   $$\Pr[X_i = 1 \mid X_{<i} = y] = \frac{A_1}{A_0 + A_1} = \frac{1}{1 + A_0/A_1} \ge \frac{1}{1 + \lambda} = \delta,$$
   and in the same way $\Pr[X_i = 0 \mid X_{<i} = y] \ge \delta$. Every prefix has positive probability, since all weights are positive.

   *$f(X)$ is biased.* Let $s = |f^{-1}(b)| \ge 2^{n-1}$. Then
   $$\Pr[f(X) = b] = \frac{\lambda s}{\lambda s + (2^n - s)}.$$
   This increases with $s$, so it is at least its value at $s = 2^{n-1}$, which is $\lambda/(\lambda + 1) = 1 - \delta$.

   *Tightness.* $\Pr[X_1 = 1] \in [\delta, 1 - \delta]$ by the definition with $i = 1$, so $\mathrm{bias}(X_1) \le 1 - 2\delta$. $\square$

   The source in the proof depends on $f$. That is the whole point: the class of SV sources is rich enough to defeat each fixed function. The same argument works for a function with $m$ output bits, since its first output bit is a function of $X$.

3. **XOR of independent sources (Santha and Vazirani 1986).** If $X^{(1)}, \ldots, X^{(k)}$ are independent $\delta$-SV sources of length $n$, the bitwise XOR $Z = X^{(1)} \oplus \cdots \oplus X^{(k)}$ is a $\delta'$-SV source with $1 - 2\delta' = (1 - 2\delta)^k$.

   *Proof.* Condition on all the bits before position $i$ of all $k$ sources. Since the sources are independent, the bits $X^{(1)}_i, \ldots, X^{(k)}_i$ are then independent, and $X^{(j)}_i = 1$ with some probability $p_j \in [\delta, 1 - \delta]$. So $\mathrm{E}[(-1)^{Z_i}] = \prod_j (1 - 2p_j)$, which has absolute value at most $(1 - 2\delta)^k$, and $\Pr[Z_i = 1]$ lies in $[\delta', 1 - \delta']$. Conditioning only on $Z_{<i}$ averages these conditional probabilities, so they stay in the interval. $\square$

4. **Randomized algorithms can use one SV source.** Vazirani and Vazirani (1985) showed that every [BPP](/bpp/) algorithm can be simulated in polynomial time with one $\delta$-SV source for any constant $\delta > 0$. Later results with [seeded extractors](/seeded-extractor/) give a simpler route: since the min-entropy is $\Omega(n)$, run the algorithm on the output of the extractor for every one of the $\mathrm{poly}(n)$ seeds and take the majority vote. This simulates the algorithm; it does not extract random bits.

## Examples and non-examples

- **Majority, $n = 3$, $\delta = 1/4$.** Here $\lambda = 3$, $b = 1$, the four strings $000, 001, 010, 100$ get probability $1/16$ and the four strings $011, 101, 110, 111$ get $3/16$. The conditional probabilities of a 1 are $5/8$ for the first bit; $2/3$ and $3/5$ for the second bit after $0$ and $1$; and $1/2, 3/4, 3/4, 1/2$ for the third bit after $00, 01, 10, 11$. All lie in $[1/4, 3/4]$, and $\Pr[\mathrm{MAJ}(X) = 1] = 12/16 = 3/4 = 1 - \delta$. The min-entropy is $\log_2(16/3) \approx 2.415$.
- **Parity.** For $f(x) = x_1 \oplus \cdots \oplus x_n$, each preimage has exactly $2^{n-1}$ strings, so the proof gives $\Pr[f(X) = 1] = 1 - \delta$ exactly. Parity removes bias for independent coins, but not for SV sources. A check over all 256 functions $f : \{0,1\}^3 \to \{0,1\}$ with $\delta = 1/4$ confirms that the source of the proof is a valid SV source and gives $\Pr[f(X) = b] \ge 3/4$ in every case.
- **Biased independent coins.** Independent bits with $\Pr[X_i = 1] = p_i \in [\delta, 1 - \delta]$ form a $\delta$-SV source. If all $p_i$ are equal, [von Neumann debiasing](/von-neumann-debiasing/) extracts exact bits; the impossibility result shows that this must fail for some other SV sources.
- **A Markov chain** on $\{0, 1\}$ whose four transition probabilities lie in $[\delta, 1 - \delta]$, with a first bit in the same range, is a $\delta$-SV source.
- **XOR of three sources.** With $\delta = 1/4$ and $k = 3$, $1 - 2\delta' = (1/2)^3 = 1/8$, so the XOR is a $7/16$-SV source.
- **Non-example: a fixed bit.** A source in which some bit is a fixed constant, or a fixed function of the earlier bits, is not an SV source for any $\delta > 0$, even when the other bits are uniform. The uniform distribution on the even-weight strings is an example: its last bit is determined by the others. Such sources can still have high min-entropy.
- **Non-example: $\delta = 0$.** With $\delta = 0$ the condition says nothing, and the source can be a constant string.

## Related definitions

- [Min-entropy](/min-entropy/): the general measure of randomness of a source. Every $\delta$-SV source has min-entropy at least $n\log_2\frac{1}{1-\delta}$, but most sources with that min-entropy are not SV sources.
- [Randomness extractor](/randomness-extractor/): a function that turns a weak source into almost uniform bits. Fact 2 shows that deterministic extractors do not exist for SV sources.
- [Seeded extractor](/seeded-extractor/): uses a short independent uniform seed, and works for all sources of high min-entropy, including SV sources.
- [Two-source extractor](/two-source-extractor/): uses two independent weak sources and no seed. The inner product function extracts from two independent sources of min-entropy above $n/2$ (Chor and Goldreich 1988).
- **Probability-bounded sources and block sources** (Chor and Goldreich 1988): sources in which each block of bits has high min-entropy given the earlier blocks. They generalize SV sources from single bits to blocks.
- [Entropy source](/entropy-source/): the engineering view of physical randomness, where the model of the source must be justified by tests and analysis.

## References
