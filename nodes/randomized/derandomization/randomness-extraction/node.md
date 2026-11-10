---
tag: 7BW5PT
kind: problem
slug: randomness-extraction
name: Randomness extraction
aliases:
- randomness purification
- debiasing
area: randomized/derandomization
level: core
summary: Given samples from a weak random source, output bits that are close to uniform. No single function works for all sources, so extractors use a short seed or several independent sources.
prereqs: [min-entropy, total-variation-distance, randomized-algorithm]
see_also: [randomness-extractor, seeded-extractor, two-source-extractor, leftover-hash-lemma, von-neumann-debiasing, santha-vazirani-source, entropy-source, disperser]
sources:
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 6 (weak sources, min-entropy, the impossibility of deterministic extraction, seeded extractors and their uses)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 21 (weak random sources and randomness extractors)
  - paper: doi:10.1006/jcss.1996.0004
    title: Noam Nisan and David Zuckerman, Randomness is linear in space, Journal of Computer and System Sciences 52(1), 1996
    locator: the definition of extractors with a short seed and the first uses for simulation with weak sources
  - paper: doi:10.1137/0217015
    title: Benny Chor and Oded Goldreich, Unbiased bits from sources of weak randomness and probabilistic communication complexity, SIAM Journal on Computing 17(2), 1988
    locator: the model of sources by min-entropy, and extraction from two independent sources
  - paper: doi:10.1137/S0895480197329508
    title: Jaikumar Radhakrishnan and Amnon Ta-Shma, Bounds for dispersers, extractors, and depth-two superconcentrators, SIAM Journal on Discrete Mathematics 13(1), 2000
    locator: the lower bounds on the seed length and the entropy loss of extractors
---

Randomness extraction is the problem of turning the output of a weak random source into bits that are almost uniform. Physical sources, such as noise in a circuit or the timing of key presses, are random but biased and correlated. Randomized algorithms and cryptography need uniform bits. The standard measure of the randomness in a source is its [min-entropy](/min-entropy/). No fixed function extracts even one bit from every source of min-entropy $n - 1$, so the problem splits into variants: special classes of sources, a short uniform seed ([seeded extractors](/seeded-extractor/)), or several independent sources ([two-source extractors](/two-source-extractor/)).

## In plain words

Imagine a coin that is bent, or a noise meter whose readings depend on each other. Each reading has some randomness, but it is not a fair coin. The goal is to turn many such readings into a smaller number of fair coin flips.

For some sources this is easy. For a bent coin with independent tosses, look at pairs: heads then tails gives 0, tails then heads gives 1, and equal pairs are thrown away. For a general source this is impossible with a fixed rule, because an adversary who knows the rule can pick a source that makes the output constant. The fix is to use a few truly random bits as a catalyst, or two sources that do not depend on each other.

## Definition

**Sources.** A *source* on $\{0,1\}^n$ is a random variable $X$. It has min-entropy $k$ if $\Pr[X = x] \le 2^{-k}$ for every $x$, and it is *flat* if it is uniform on a set of size $2^k$. Such an $X$ is an *$(n, k)$-source*.

**Closeness.** $Y$ is *$\varepsilon$-close* to $Z$ if the statistical distance $\Delta(Y, Z) = \max_T |\Pr[Y \in T] - \Pr[Z \in T]|$ is at most $\varepsilon$.

**The problem.** Given a class $\mathcal{C}$ of sources on $\{0,1\}^n$, an output length $m$ and an error $\varepsilon$, find an efficiently computable function whose output is $\varepsilon$-close to $U_m$ for every source in $\mathcal{C}$. The variants differ in the class and in the extra inputs:

- *deterministic:* $\mathrm{Ext} : \{0,1\}^n \to \{0,1\}^m$ with $\mathrm{Ext}(X)$ $\varepsilon$-close to $U_m$ for every $X \in \mathcal{C}$;
- *seeded:* $\mathrm{Ext} : \{0,1\}^n \times \{0,1\}^d \to \{0,1\}^m$ with $\mathrm{Ext}(X, U_d)$ $\varepsilon$-close to $U_m$ for every $(n, k)$-source $X$; this is a [$(k, \varepsilon)$-extractor](/randomness-extractor/);
- *multi-source:* $\mathrm{Ext}(X_1, \ldots, X_t)$ close to uniform for independent sources $X_i$ of min-entropy $k_i$.

## Variants

| variant | sources | extra input | example |
|---|---|---|---|
| independent identical bits | $X_i$ independent with the same bias | none | [von Neumann debiasing](/von-neumann-debiasing/) |
| bit-fixing sources | some bits uniform, the others fixed | none | parity of all bits, for one output bit |
| [Santha-Vazirani sources](/santha-vazirani-source/) | each bit has bias at most $\delta$ given the past | none is possible; a seed or a second source works | impossible for one fixed function |
| general $(n, k)$-sources | min-entropy $k$ | a uniform seed of $d$ bits | [leftover hash lemma](/leftover-hash-lemma/), [Trevisan](/trevisan-extractor/), GUV |
| two independent sources | min-entropy $k_1$ and $k_2$ | none | [inner product](/two-source-extractor/), Chattopadhyay and Zuckerman |
| one-sided version | min-entropy $k$ | seed | [disperser](/disperser/): output hits every large set |
| computational | source with pseudoentropy | seed or key | [HKDF](/hkdf/), [HILL](/hill-prg-from-one-way-functions/) |

A *strong* seeded extractor keeps the output close to uniform even when the seed is revealed; most uses need this.

## Examples

**Von Neumann debiasing.** Let $X_1, X_2, \ldots$ be independent bits, each 1 with probability $p$. Read them in pairs. Output 0 for the pair 10 and 1 for the pair 01, and output nothing for 00 and 11. Both useful pairs have probability $p(1-p)$, so each output bit is exactly uniform, and the outputs are independent. For $p = 0.7$ a pair gives a bit with probability $2 \cdot 0.7 \cdot 0.3 = 0.42$, so 100 tosses give 21 bits on average. The method fails if the tosses are not independent.

**Deterministic extraction is impossible.** Let $f : \{0,1\}^n \to \{0,1\}$ be any function. One of the sets $f^{-1}(0)$ and $f^{-1}(1)$ has at least $2^{n-1}$ elements. The uniform distribution on $2^{n-1}$ of its elements is an $(n, n-1)$-source, and $f$ is constant on it. So no fixed function extracts one bit with error less than $\frac12$ from all $(n, n-1)$-sources.

**A seed fixes this.** With $d$ uniform seed bits, the [leftover hash lemma](/leftover-hash-lemma/) gives, for every $(n, k)$-source, $m = k - 2\log_2(1/\varepsilon) + 2$ output bits that are $\varepsilon$-close to uniform, with a seed of about $n$ bits. The seed must be independent of the source.

## Known algorithms

| construction | type | seed or sources | output | source |
|---|---|---|---|---|
| von Neumann | deterministic, i.i.d. bits | none | about $np(1-p)$ bits | von Neumann 1951 |
| [leftover hash lemma](/leftover-hash-lemma/) | strong seeded | $d \approx n$ | $k - 2\log(1/\varepsilon) + O(1)$ | Impagliazzo, Levin and Luby 1989 |
| [Trevisan](/trevisan-extractor/) | strong seeded | $O(\log^2(n/\varepsilon)/\log k)$ | $k^{1-\alpha}$ | Trevisan 2001 |
| Guruswami, Umans and Vadhan | seeded | $O(\log n + \log(1/\varepsilon))$ | $(1 - \alpha)k$ | Guruswami, Umans and Vadhan 2009 |
| [inner product](/two-source-extractor/) | two sources | $k_1 + k_2 > n + 2\log(1/\varepsilon)$ | 1 bit | Chor and Goldreich 1988 |
| Chattopadhyay and Zuckerman | two sources | $k_1, k_2 \ge \log^C n$ | 1 bit | Chattopadhyay and Zuckerman 2016 |

## Bounds

- **Output length.** If $X$ is flat on $2^k$ points, then $\mathrm{Ext}(X, U_d)$ takes at most $2^{k+d}$ values, so its distance from $U_m$ is at least $1 - 2^{k+d-m}$. Error $\varepsilon$ therefore needs $m \le k + d + \log_2(1/(1 - \varepsilon))$, roughly $m \le k + d$. Shannon entropy is not enough: a source that is $0^n$ with probability $\frac12$ and uniform otherwise has Shannon entropy about $n/2$ but min-entropy only 1.
- **Lower bounds for seeded extraction (Radhakrishnan and Ta-Shma 2000).** For $k \le n - 1$ and $\varepsilon \le \frac12$, every $(k, \varepsilon)$-extractor with $m > d$ has seed length $d \ge \log_2(n - k) + 2\log_2(1/\varepsilon) - O(1)$ and entropy loss $k + d - m \ge 2\log_2(1/\varepsilon) - O(1)$.
- **Existence.** A random function is a $(k, \varepsilon)$-extractor with $d = \log_2(n - k) + 2\log_2(1/\varepsilon) + O(1)$ and $m = k + d - 2\log_2(1/\varepsilon) - O(1)$, matching the lower bounds; see [randomness extractor](/randomness-extractor/).

## Reductions

**Simulating BPP with a weak source.** Let $A$ be a randomized algorithm that uses $m$ random bits and errs with probability at most $\frac13$ on each input. Let $\mathrm{Ext}$ be a $(k, \varepsilon)$-extractor with $\varepsilon < \frac16$. Given one sample $x$ from an $(n, k')$-source with $k' > k$, run $A$ with $\mathrm{Ext}(x, s)$ for all $2^d$ seeds $s$ and take the majority.

*Claim.* For each input, the majority is wrong with probability less than $2^{k - k'}$ over $x$.

*Proof.* Fix an input and let $B$ be the set of $x$ for which at least half of the seeds give a wrong answer. If $|B| \ge 2^k$, the uniform distribution on any $2^k$ elements of $B$ is a $(n, k)$-source on which $A(\mathrm{Ext}(X, U_d))$ is wrong with probability at least $\frac12$, while $A(U_m)$ is wrong with probability at most $\frac13$. The test "is $A$ wrong on these random bits?" then tells $\mathrm{Ext}(X, U_d)$ from $U_m$ with advantage at least $\frac16 > \varepsilon$, which is impossible. So $|B| < 2^k$, and $\Pr[X \in B] < 2^k \cdot 2^{-k'}$. $\square$

With $d = O(\log n)$ this costs only a polynomial factor in time. The same argument shows that an extractor is a sampler: the seeds $s$ with input $x$ give points $\mathrm{Ext}(x, s)$ whose average estimates the average of any test, for all but few $x$.

**Extractors and other objects.** A $(k, \varepsilon)$-extractor is a bipartite graph in which every set of $2^k$ left vertices has neighbors close to uniform on the right; a [disperser](/disperser/) only asks that the neighbors cover most of the right side. Trevisan showed that a [pseudorandom generator](/pseudorandom-generator/) proof by reconstruction gives an extractor. Two-source extractors with low error give explicit [Ramsey graphs](/ramsey-theorem/).

## Applications

- **Random number generators.** Operating systems and [cryptographically secure generators](/cryptographically-secure-prng/) collect bits from [entropy sources](/entropy-source/) and condense them with hash functions before use.
- **Cryptography.** Privacy amplification turns a partly secret shared key into a shorter key that is almost uniform for the adversary. Key derivation functions such as [HKDF](/hkdf/) follow an extract-then-expand plan.
- **Derandomization.** Extractors give samplers with few random bits, simulations of BPP with weak sources, and Nisan and Zuckerman's generator for space-bounded machines.
- **Combinatorics.** Extractors give explicit graphs with strong expansion, and two-source extractors give Ramsey graphs.

## References
