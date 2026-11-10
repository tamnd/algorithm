---
tag: 20AZMB
kind: definition
slug: two-source-extractor
name: Two-source extractor
aliases:
- multi-source extractor
- independent-source extractor
area: randomized/derandomization
level: research
summary: An extractor that takes two independent weak sources and needs no seed. The inner product works when the min-entropies sum to more than n; explicit ones now need only polylog n.
prereqs: [randomness-extractor, min-entropy, walsh-hadamard-transform]
see_also: [randomness-extractor, seeded-extractor, randomness-extraction, ramsey-theorem, hadamard-code, fourier-analysis-of-boolean-functions, probabilistic-method, leftover-hash-lemma]
sources:
  - paper: doi:10.1137/0217015
    title: Benny Chor and Oded Goldreich, Unbiased bits from sources of weak randomness and probabilistic communication complexity, SIAM Journal on Computing 17(2), 1988
    locator: the model of two independent weak sources, the inner product extractor and its proof with Lindsey's lemma
  - paper: doi:10.1145/2897518.2897528
    title: Eshan Chattopadhyay and David Zuckerman, Explicit two-source extractors and resilient functions, 48th ACM Symposium on Theory of Computing (STOC), 2016
    locator: the explicit two-source extractor for polylogarithmic min-entropy and the Ramsey graph corollary
  - paper: doi:10.4007/annals.2019.189.3.1
    title: Eshan Chattopadhyay and David Zuckerman, Explicit two-source extractors and resilient functions, Annals of Mathematics 189(3), 2019
    locator: the journal version of the main theorem
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 6 (deterministic extraction, independent sources and the impossibility for a single source)
---

A two-source extractor is a function $\mathrm{Ext}(x, y)$ that outputs almost uniform bits whenever $x$ and $y$ come from two *independent* weak random sources, each with enough [min-entropy](/min-entropy/). It needs no uniform seed. One weak source is not enough for any fixed function, but two independent ones are. The first example, due to Chor and Goldreich (1988), is the inner product modulo 2, which works when the two min-entropies sum to more than $n$. A random function works with min-entropy only about $\log n$ in each source, and for a long time explicit constructions were far from this. Chattopadhyay and Zuckerman (2016) gave an explicit extractor for min-entropy $\log^C n$, which also gave explicit Ramsey graphs much better than those known before.

## Definition

A random variable $X$ on $\{0,1\}^n$ is an *$(n, k)$-source* if $\Pr[X = x] \le 2^{-k}$ for every $x$. $\Delta$ is the statistical distance and $U_m$ is uniform on $\{0,1\}^m$.

**Definition.** A function $\mathrm{Ext} : \{0,1\}^n \times \{0,1\}^n \to \{0,1\}^m$ is a *$(k_1, k_2, \varepsilon)$ two-source extractor* if for every $(n, k_1)$-source $X$ and every $(n, k_2)$-source $Y$ independent of $X$,

$$\Delta\big(\mathrm{Ext}(X, Y),\ U_m\big) \le \varepsilon.$$

It is *strong in $Y$* if $(Y, \mathrm{Ext}(X, Y))$ is $\varepsilon$-close to $(Y, U_m)$. For one output bit, the distance from a uniform bit is half the *bias* $|\Pr[\mathrm{Ext} = 0] - \Pr[\mathrm{Ext} = 1]|$. A *$t$-source extractor* takes $t$ independent sources in the same way.

As for seeded extractors, every source is a convex combination of flat sources, so it is enough to check $X$ and $Y$ uniform on sets $A$ and $B$ of sizes $2^{k_1}$ and $2^{k_2}$ (see [randomness extractor](/randomness-extractor/)). For one output bit, $\mathrm{Ext}$ is then a $2^n \times 2^n$ matrix of bits, and the condition says that on every rectangle $A \times B$ with $|A| \ge 2^{k_1}$ and $|B| \ge 2^{k_2}$, the fraction of 1s is within $\varepsilon$ of $\frac12$.

**Comparison with a seed.** A [seeded extractor](/seeded-extractor/) is the special case in which $Y$ is uniform, so $k_2 = d$ is the full length of $Y$. A two-source extractor must work even when both inputs are weak.

## Examples and non-examples

**Non-example: one source.** No function $f : \{0,1\}^n \to \{0,1\}$ extracts a bit with error less than $\frac12$ from all $(n, n-1)$-sources: one of $f^{-1}(0)$ and $f^{-1}(1)$ has at least $2^{n-1}$ elements, and the uniform distribution on it is a source on which $f$ is constant. Two independent sources avoid this, because no single set controls the pair.

**The inner product (Chor and Goldreich 1988).** Let $\mathrm{IP}(x, y) = \langle x, y \rangle = \sum_i x_i y_i \bmod 2$.

*Theorem.* For independent $X$ with min-entropy $k_1$ and $Y$ with min-entropy $k_2$, the bias of $\mathrm{IP}(X, Y)$ is at most $2^{(n - k_1 - k_2)/2}$. So $\mathrm{IP}$ is a $(k_1, k_2, \varepsilon)$ two-source extractor with $\varepsilon = 2^{(n - k_1 - k_2)/2 - 1}$, and it is strong in each source with the same bound. The theorem is unconditional.

*Lindsey's lemma.* Let $H$ be the $N \times N$ matrix with $N = 2^n$ and $H_{x,y} = (-1)^{\langle x, y \rangle}$. For all sets $A, B \subseteq \{0,1\}^n$,

$$\Big| \sum_{x \in A,\ y \in B} H_{x,y} \Big| \le \sqrt{|A|\,|B|\,N}.$$

*Proof of the lemma.* The rows of $H$ are orthogonal: for $x \ne x'$, $\sum_y (-1)^{\langle x \oplus x', y \rangle} = 0$, because a nonzero linear function is 0 and 1 equally often. So $H^{\mathsf T} H = N I$, and $\|Hv\|_2^2 = v^{\mathsf T} H^{\mathsf T} H v = N\|v\|_2^2$ for every vector $v$. Let $1_A$ and $1_B$ be the indicator vectors. By the Cauchy-Schwarz inequality,

$$|1_A^{\mathsf T} H 1_B| \le \|1_A\|_2 \, \|H 1_B\|_2 = \sqrt{|A|} \cdot \sqrt{N |B|}. \qquad \square$$

*Proof of the theorem.* Let $p$ and $q$ be the distributions of $X$ and $Y$ as vectors. The bias is

$$\big|\mathbb{E}[(-1)^{\langle X, Y \rangle}]\big| = |p^{\mathsf T} H q| \le \|p\|_2 \, \|H q\|_2 = \sqrt{N}\, \|p\|_2 \, \|q\|_2.$$

Min-entropy $k$ gives $\|p\|_2^2 = \sum_x p(x)^2 \le \max_x p(x) \le 2^{-k}$. So the bias is at most $\sqrt{2^n 2^{-k_1} 2^{-k_2}} = 2^{(n - k_1 - k_2)/2}$. For flat sources this is Lindsey's lemma divided by $|A||B|$. For the strong form, the bias of $\mathrm{IP}(X, y)$ for a fixed $y$ is $|(H p)_y|$, and

$$\mathbb{E}_{y \sim q}\, |(Hp)_y| \le \sqrt{\textstyle\sum_y q(y)(Hp)_y^2} \le \sqrt{2^{-k_2} \|Hp\|_2^2} = \sqrt{2^{-k_2} N \|p\|_2^2} \le 2^{(n - k_1 - k_2)/2}. \qquad \blacksquare$$

**Exact values for $n = 3$.** Enumerating all flat sources on $\{0,1\}^3$, with strings as the integers whose bit $j$ is $x_j$:

| $k_1$ | $k_2$ | largest bias | bound $2^{(n - k_1 - k_2)/2}$ | a worst pair |
|---|---|---|---|---|
| 2 | 2 | $5/8$ | 0.7071 | $A = B = \{0, 1, 2, 4\}$ |
| 2 | 1 | 1 | 1 | $A = \{0, 1, 2, 3\}$, $B = \{0, 4\}$ |
| 3 | 1 | $1/2$ | 0.7071 | |
| 1 | 1 | 1 | 1.414 | |

For $k_1 = k_2 = 2$ the bias is below 1, so the $8 \times 8$ inner product matrix has no constant $4 \times 4$ rectangle. For $k_1 = 2$ and $k_2 = 1$ the bound is reached: on $A \times B$ the first source uses only the low two bits and the second only the top bit, so the inner product is always 0.

**The bound is tight at $k_1 + k_2 = n$.** Let $n$ be even, let $X = (a, 0^{n/2})$ with $a$ uniform and $Y = (0^{n/2}, b)$ with $b$ uniform. Each source has min-entropy $n/2$, and $\langle X, Y \rangle = 0$ always. So the inner product needs $k_1 + k_2 > n$, and the error $2^{(n - k_1 - k_2)/2 - 1}$ is small only when $k_1 + k_2 \ge n + 2\log_2(1/\varepsilon) - 2$.

**A random function is much better.** For $k \ge \log_2(n - k + 2) + 2\log_2(1/\varepsilon)$, a random $f : \{0,1\}^n \times \{0,1\}^n \to \{0,1\}$ is a $(k, k, \varepsilon)$ two-source extractor with positive probability. *Proof.* Let $K = 2^k$, so $\varepsilon^2 K \ge (n - k)\ln 2 + 2$. For fixed sets $A, B$ of size $K$, the fraction of 1s of $f$ on $A \times B$ is an average of $K^2$ independent fair bits, so by Hoeffding's inequality it is more than $\varepsilon$ from $\frac12$ with probability at most $2e^{-2\varepsilon^2 K^2}$. There are at most $(eN/K)^{2K}$ pairs $(A, B)$, and $2K\ln(eN/K) + \ln 2 < 2K\big((n - k)\ln 2 + 2\big) \le 2\varepsilon^2 K^2$. So the union bound over all pairs is less than 1. $\square$ Such a function is not explicit: it is a table of $2^{2n}$ bits.

**Explicit constructions.**

| construction | min-entropy needed | output | error |
|---|---|---|---|
| inner product, Chor and Goldreich (1988) | $k_1 + k_2 > n + 2\log_2(1/\varepsilon) - 2$ | 1 bit | $2^{(n - k_1 - k_2)/2 - 1}$ |
| Bourgain (2005) | both at least $(\frac12 - \alpha)n$ for a small constant $\alpha > 0$ | many bits | $2^{-\Omega(n)}$ |
| Raz (2005) | one source above $n/2$, the other $O(\log n)$ | many bits | small |
| Chattopadhyay and Zuckerman (2016) | both at least $\log^C n$ for a constant $C$ | 1 bit | $n^{-\Omega(1)}$ |
| random function (not explicit) | $\log_2 n + 2\log_2(1/\varepsilon) + O(1)$ | 1 bit | $\varepsilon$ |

**Chattopadhyay and Zuckerman (2016), stated and cited.** There is a constant $C$ and an explicit function $\mathrm{Ext} : \{0,1\}^n \times \{0,1\}^n \to \{0,1\}$, computable in polynomial time, that is a $(k, k, n^{-\Omega(1)})$ two-source extractor for $k \ge \log^C n$. The construction applies a strong seeded extractor to one source with every seed, uses the other source to sample, and combines the results with a resilient function, a function of many bits that no small coalition of bits can control. The error is only polynomially small in $n$; later work improved the min-entropy and the error.

**Ramsey graphs.** For one output bit, an extractor with error less than $\frac12$ for $k_1 = k_2 = k$ is a matrix with no constant $2^k \times 2^k$ rectangle: a bipartite graph on $2^n + 2^n$ vertices with no complete or empty bipartite subgraph on $2^k + 2^k$ vertices. The inner product gives this for $k > n/2$. An extra step turns such a bipartite graph into a graph on one vertex set. Chattopadhyay and Zuckerman obtained explicit graphs on $N$ vertices with no clique and no independent set of size $2^{(\log\log N)^{C}}$; a random graph has none of size $2\log_2 N$, as [Erdős's bound](/ramsey-theorem/) shows by the [probabilistic method](/probabilistic-method/).

## Related definitions

- **[Randomness extractor](/randomness-extractor/) and [seeded extractor](/seeded-extractor/).** The seeded case is the two-source case with one source uniform.
- **[Randomness extraction](/randomness-extraction/).** The general problem and its variants, including sources with special structure.
- **Multi-source extractors.** With more independent sources, each may have lower min-entropy rate. Barak, Impagliazzo and Wigderson used additive combinatorics to extract from a constant number of sources of any constant rate.
- **Affine and bit-fixing extractors.** Deterministic extractors for sources that are uniform on an affine subspace or on a set of coordinates.
- **[Hadamard code](/hadamard-code/).** The rows of the inner product matrix are the codewords of the Hadamard code, and Lindsey's lemma is the statement that they are orthogonal.
- **[Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/).** The bias of $\mathrm{IP}$ on a source is a Fourier coefficient of its distribution.

## References
