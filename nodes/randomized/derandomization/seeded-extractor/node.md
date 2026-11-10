---
tag: FNWM9D
kind: definition
slug: seeded-extractor
name: Seeded extractor
aliases:
- strong seeded extractor
- strong extractor
area: randomized/derandomization
level: advanced
summary: An extractor that takes a short uniform seed as a second input. A strong one keeps its output close to uniform even when the seed is revealed.
prereqs: [randomness-extractor, min-entropy, total-variation-distance]
see_also: [randomness-extractor, randomness-extraction, leftover-hash-lemma, trevisan-extractor, two-source-extractor, disperser, nisan-wigderson-generator, list-decoding]
sources:
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 6 (strong extractors, constructions and their parameters) and Chapter 7 (Trevisan's extractor)
  - paper: doi:10.1145/502090.502099
    title: Luca Trevisan, Extractors and pseudorandom generators, Journal of the ACM 48(4), 2001
    locator: the extractor from a list-decodable code and a design, and its parameters
  - paper: doi:10.1145/1538902.1538904
    title: Venkatesan Guruswami, Christopher Umans and Salil Vadhan, Unbalanced expanders and randomness extractors from Parvaresh-Vardy codes, Journal of the ACM 56(4), 2009
    locator: the extractor with seed O(log n + log(1/ε)) and output (1 - α)k
  - paper: doi:10.1137/S0895480197329508
    title: Jaikumar Radhakrishnan and Amnon Ta-Shma, Bounds for dispersers, extractors, and depth-two superconcentrators, SIAM Journal on Discrete Mathematics 13(1), 2000
    locator: the lower bounds on the seed length and on the entropy loss
  - paper: doi:10.1006/jcss.1996.0004
    title: Noam Nisan and David Zuckerman, Randomness is linear in space, Journal of Computer and System Sciences 52(1), 1996
    locator: the first extractors with a seed much shorter than the source
---

A seeded extractor is a function $\mathrm{Ext}(x, s)$ that turns a sample $x$ of a weak random source and a short uniform seed $s$ into almost uniform bits. It is *strong* if the output stays close to uniform even to someone who sees the seed. Strong extractors are the version used in practice: in privacy amplification the seed is sent in public, and in many constructions one seed is used for many purposes. The main goal of the theory is an explicit extractor with a seed of $O(\log n + \log(1/\varepsilon))$ bits that keeps almost all the [min-entropy](/min-entropy/). Guruswami, Umans and Vadhan (2009) came within a constant factor of this goal in the output length. This page states the definition, the facts that make strong extractors convenient, and the main constructions; the general definition and its bounds are on [randomness extractor](/randomness-extractor/).

## Definition

Let $X$ be a random variable on $\{0,1\}^n$ with min-entropy at least $k$, that is, $\Pr[X = x] \le 2^{-k}$ for every $x$; such an $X$ is an *$(n, k)$-source*. Let $U_d$ be uniform on $\{0,1\}^d$ and independent of $X$, and let $\Delta$ be the statistical distance.

**Definition.** A function $\mathrm{Ext} : \{0,1\}^n \times \{0,1\}^d \to \{0,1\}^m$ is a *strong $(k, \varepsilon)$-extractor* if for every $(n, k)$-source $X$,

$$\Delta\big((U_d, \mathrm{Ext}(X, U_d)),\ (U_d, U_m)\big) \le \varepsilon.$$

It is a *(seeded) $(k, \varepsilon)$-extractor* if only $\Delta(\mathrm{Ext}(X, U_d), U_m) \le \varepsilon$ is required. An extractor family is *explicit* if $\mathrm{Ext}(x, s)$ can be computed in time polynomial in $n$ and $d$.

**Equivalent form.** The left side of the strong condition equals $\mathbb{E}_s\big[\Delta(\mathrm{Ext}(X, s), U_m)\big]$, the average over seeds of the distance for the fixed seed. So a strong extractor is one for which, for every source, the output is close to uniform for a typical seed. It is not required, and not possible, that the output is close to uniform for every fixed seed: for a fixed $s$, the map $x \mapsto \mathrm{Ext}(x, s)$ is a deterministic function, and some $(n, n-1)$-source makes its first bit constant.

**From strong to ordinary.** If $\mathrm{Ext}$ is a strong $(k, \varepsilon)$-extractor, then $\mathrm{Ext}'(x, s) = (s, \mathrm{Ext}(x, s))$ is a $(k, \varepsilon)$-extractor with output length $d + m$. So the entropy loss $k - m$ of a strong extractor is the same quantity as the loss $k + d - m'$ of an ordinary one.

**Extracting twice from the same source.** Strong extractors compose. Let $\mathrm{Ext}_1$ be a strong $(k, \varepsilon_1)$-extractor with output length $m_1$, and $\mathrm{Ext}_2$ a strong $(k - m_1 - \log_2(1/\delta), \varepsilon_2)$-extractor with output length $m_2$. Then

$$\mathrm{Ext}(x, (s_1, s_2)) = \big(\mathrm{Ext}_1(x, s_1),\ \mathrm{Ext}_2(x, s_2)\big)$$

is a strong $(k, \varepsilon_1 + \varepsilon_2 + \delta)$-extractor with output length $m_1 + m_2$.

*Proof.* Let $X$ be an $(n, k)$-source, $S_1, S_2$ independent uniform seeds, $Y = \mathrm{Ext}_1(X, S_1)$ and $Z = \mathrm{Ext}_2(X, S_2)$.

1. *Conditioning costs at most $m_1 + \log_2(1/\delta)$ bits.* Fix $s_1$. Call an output $y$ *rare* if $\Pr[Y = y \mid S_1 = s_1] < \delta 2^{-m_1}$. There are at most $2^{m_1}$ outputs, so $\Pr[Y \text{ rare} \mid S_1 = s_1] < \delta$. If $y$ is not rare, then for every $x$, $\Pr[X = x \mid S_1 = s_1, Y = y] \le 2^{-k} / (\delta 2^{-m_1})$, because $X$ is independent of $S_1$. So given $(s_1, y)$, $X$ has min-entropy at least $k - m_1 - \log_2(1/\delta)$.
2. *The second output.* $S_2$ is independent of $(X, S_1, Y)$. For each $(s_1, y)$ that is not rare, the strong property of $\mathrm{Ext}_2$ gives that $(S_2, Z)$ given $(s_1, y)$ is $\varepsilon_2$-close to $(S_2, U_{m_2})$. Averaging, and paying at most $\delta$ for the rare pairs, $(S_1, Y, S_2, Z)$ is $(\varepsilon_2 + \delta)$-close to $(S_1, Y, S_2, U_{m_2})$.
3. *The first output.* $(S_1, Y)$ is $\varepsilon_1$-close to $(S_1, U_{m_1})$, and appending an independent $(S_2, U_{m_2})$ does not change the distance.

By the triangle inequality, $(S_1, S_2, Y, Z)$ is $(\varepsilon_1 + \varepsilon_2 + \delta)$-close to $(S_1, S_2, U_{m_1}, U_{m_2})$. $\square$

This lets an extractor that outputs only a fraction of the entropy be used several times to output almost all of it, at the cost of a longer seed.

## Examples and non-examples

**Constructions.** In the table, $\alpha > 0$ is any constant, $\varepsilon$ is the error, and the bounds hold for the ranges of $k$ and $\varepsilon$ stated in the sources.

| construction | strong | seed length $d$ | output length $m$ | explicit |
|---|---|---|---|---|
| lower bound (Radhakrishnan and Ta-Shma 2000) | | $\log_2(n - k) + 2\log_2(1/\varepsilon) - O(1)$ | at most $k + d - 2\log_2(1/\varepsilon) + O(1)$ | |
| random function | yes | $\log_2(n - k) + 2\log_2(1/\varepsilon) + O(1)$ | $k + d - 2\log_2(1/\varepsilon) - O(1)$ | no |
| [leftover hash lemma](/leftover-hash-lemma/), Toeplitz matrices | yes | $n + m - 1$ | $k - 2\log_2(1/\varepsilon) + 2$ | yes |
| [Trevisan](/trevisan-extractor/) (2001) | yes | $O(\log^2(n/\varepsilon) / \log k)$ | $k^{1 - \alpha}$ | yes |
| Guruswami, Umans and Vadhan (2009) | see the source | $O(\log n + \log(1/\varepsilon))$ | $(1 - \alpha)k$ | yes |

For $k = n^{\Omega(1)}$ and $\varepsilon = 1/\mathrm{poly}(n)$, Trevisan's seed is $O(\log n)$, but the output keeps only $k^{1-\alpha}$ of the $k$ bits. The construction of Guruswami, Umans and Vadhan first applies a lossless condenser built from Parvaresh-Vardy codes, which maps the source to a string of length $O(k)$ that keeps almost all the min-entropy, and then extracts from this source of high min-entropy rate.

**The inner product with the seed.** $\mathrm{Ext}(x, s) = \langle x, s\rangle \bmod 2$ with $d = n$ is a strong $(k, \varepsilon)$-extractor with one output bit and $\varepsilon = \frac12\sqrt{2^{1-k}}$, by the leftover hash lemma. For $n = 3$ and the flat source on $\{000, 001, 010, 100\}$, the 8 seeds give the outputs: $s = 000$ gives four 0s (distance $\frac12$); the seeds of weight 1 give three 0s and one 1 (distance $\frac14$ each); the seeds of weight 2 give two 0s and two 1s (distance 0); $s = 111$ gives one 0 and three 1s (distance $\frac14$). The average is $(\frac12 + 3 \cdot \frac14 + \frac14)/8 = \frac3{16}$, below the bound $\frac12\sqrt{2^{-1}} \approx 0.354$ for $k = 2$.

**Non-example: a strong extractor needs the seed to mix with the source.** $\mathrm{Ext}(x, s) = s$ is an ordinary $(k, 0)$-extractor with $m = d$, but as a strong extractor its error is $1 - 2^{-d}$.

**Non-example: a seed that only selects bits.** $\mathrm{Ext}(x, s) = x_s$ with $d = \log_2 n$ has error $\frac{n-k}{2n}$ on the source whose first $n - k$ bits are 0. Sampling a few bits of the source works only if the source spreads its entropy over the bits, which a general $(n, k)$-source need not do.

## Related definitions

- **[Randomness extractor](/randomness-extractor/).** The general definition, the graph view, existence by the probabilistic method and the lower bounds.
- **[Two-source extractor](/two-source-extractor/).** The uniform seed is replaced by a second independent weak source. If the second source is $\gamma$-close to uniform, a seeded $(k, \varepsilon)$-extractor with that source as its seed has error at most $\varepsilon + \gamma$.
- **[Disperser](/disperser/).** The one-sided analogue: the output must hit almost every string, not be close to uniform.
- **[Pseudorandom generator](/pseudorandom-generator/).** Trevisan's extractor is the [Nisan-Wigderson generator](/nisan-wigderson-generator/) with the source, encoded by a [list-decodable code](/list-decoding/), in place of the hard function.
- **[Leftover hash lemma](/leftover-hash-lemma/).** The simplest strong extractor, with optimal entropy loss and a long seed.
- **Condenser.** A function whose output is close to a source of higher min-entropy rate. A lossless condenser keeps all the min-entropy of the input and the seed.

## References
