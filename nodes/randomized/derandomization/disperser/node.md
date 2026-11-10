---
tag: 79AAZ6
kind: definition
slug: disperser
name: Disperser
aliases:
- sampler-disperser
- disperser graph
- two-source disperser
area: randomized/derandomization
level: research
summary: A relaxed extractor that only guarantees the output's support is large, not that it is close to uniform.
prereqs: [min-entropy, randomness-extractor, bipartite-graph]
see_also: [seeded-extractor, hitting-set-generator, expander-walk-sampler, randomness-amplification, two-source-extractor, rp, spectral-gap, ramsey-theorem]
sources:
  - paper: doi:10.1016/0022-0000(88)90035-9
    title: Michael Sipser, Expanders, randomness, or time versus space, Journal of Computer and System Sciences 36(3), 1988
    locator: pages 379 to 383 (dispersers defined as graphs in which every large set of left vertices has a large neighbourhood, and their use for one-sided error)
  - paper: doi:10.1109/sfcs.1989.63449
    title: Aviad Cohen and Avi Wigderson, Dispersers, deterministic amplification, and weak random sources, FOCS 1989
    locator: pages 14 to 19 (dispersers from expanders and deterministic amplification of RP and BPP)
  - paper: doi:10.1137/s0895480197329508
    title: Jaikumar Radhakrishnan and Amnon Ta-Shma, Bounds for dispersers, extractors, and depth-two superconcentrators, SIAM Journal on Discrete Mathematics 13(1), 2000
    locator: pages 2 to 24 (lower bounds on the seed length and the entropy loss of dispersers and extractors, and matching bounds for random constructions)
  - paper: doi:10.4007/annals.2012.176.3.3
    title: Boaz Barak, Anup Rao, Ronen Shaltiel and Avi Wigderson, 2-source dispersers for n^o(1) entropy, and Ramsey graphs beating the Frankl-Wilson construction, Annals of Mathematics 176(3), 2012
    locator: pages 1483 to 1544 (explicit two-source dispersers and bipartite Ramsey graphs)
---

A **disperser** is a function of a weak random source and a short uniform seed whose outputs, over all seeds, cover almost all possible output strings, for every source with enough [min-entropy](/min-entropy/). It is the one-sided relative of a [randomness extractor](/randomness-extractor/): an extractor must make the output close to uniform, while a disperser must only make its support large. In graph terms, a disperser is a [bipartite graph](/bipartite-graph/) of small left degree in which every large set of left vertices has neighbours almost everywhere on the right. That is exactly what an algorithm with one-sided error needs, since one accepting run is enough.

## Definition

Notation. $N = 2^n$, $M = 2^m$, $D = 2^d$, $K = 2^k$, and $\varepsilon \in [0, 1)$. $U_d$ is uniform on $\{0,1\}^d$. A *$k$-source* is a random variable $X$ on $\{0,1\}^n$ with min-entropy at least $k$. $\mathrm{supp}(Z)$ is the set of values that $Z$ takes with positive probability.

**Definition (source form).** A function $\mathrm{Disp} : \{0,1\}^n \times \{0,1\}^d \to \{0,1\}^m$ is a *$(k, \varepsilon)$-disperser* if for every $k$-source $X$,

$$|\mathrm{supp}(\mathrm{Disp}(X, U_d))| \ge (1 - \varepsilon) M.$$

Only the support of $X$ matters, and a $k$-source has at least $K$ values in its support. So it is enough that every set $A \subseteq \{0,1\}^n$ with $|A| = K$ has $|\mathrm{Disp}(A \times \{0,1\}^d)| \ge (1 - \varepsilon)M$.

**Definition (graph form).** Let $G$ be the bipartite multigraph with left vertex set $\{0,1\}^n$, right vertex set $\{0,1\}^m$ and an edge from $x$ to $\mathrm{Disp}(x, y)$ for each seed $y$, so every left vertex has degree $D$. Write $\Gamma(A)$ for the set of neighbours of a set $A$ of left vertices. Then $\mathrm{Disp}$ is a $(k, \varepsilon)$-disperser exactly when

$$|A| \ge K \implies |\Gamma(A)| \ge (1 - \varepsilon) M.$$

Sipser (1988) defined dispersers in this graph form.

**Facts.**

1. **The hitting form.** $\mathrm{Disp}$ is a $(k, \varepsilon)$-disperser if and only if, for every set $T$ of right vertices with $|T| > \varepsilon M$, the set $B_T$ of left vertices with no neighbour in $T$ has $|B_T| < K$.

   *Proof.* Suppose $\mathrm{Disp}$ is a disperser and $|B_T| \ge K$. Take $A \subseteq B_T$ with $|A| = K$. Then $\Gamma(A)$ misses $T$, so $|\Gamma(A)| \le M - |T| < (1 - \varepsilon)M$, a contradiction. Conversely, let $|A| = K$ and let $T$ be the complement of $\Gamma(A)$. Then $A \subseteq B_T$, so $|B_T| \ge K$, and by the hitting form $|T| \le \varepsilon M$, that is, $|\Gamma(A)| \ge (1 - \varepsilon)M$. $\square$

2. **One-sided amplification.** Let $\mathcal{A}$ be an [RP](/rp/) algorithm that uses $m$ random bits and accepts every input in the language with probability more than $\varepsilon$. On input $w$, pick $x \in \{0,1\}^n$ uniformly, run $\mathcal{A}(w, \mathrm{Disp}(x, y))$ for all $D$ seeds $y$, and accept if some run accepts. Inputs outside the language are never accepted. For an input in the language, let $T$ be the set of accepting random strings, so $|T| > \varepsilon M$; the algorithm fails only if $x \in B_T$, which has probability less than $K/N = 2^{k - n}$. So $n$ random bits give error below $2^{-(n-k)}$ with $D$ runs. The same argument with a weak source $X$ of min-entropy $k' > k$ in place of a uniform $x$ gives error below $2^{k - k'}$. This is the use of dispersers in [randomness amplification](/randomness-amplification/) (Sipser 1988; Cohen and Wigderson 1989).

3. **Extractors are dispersers.** A $(k, \varepsilon)$-extractor, whose output $\mathrm{Ext}(X, U_d)$ is $\varepsilon$-close to uniform for every $k$-source, is a $(k, \varepsilon)$-disperser. If the support $S$ of the output had fewer than $(1 - \varepsilon)M$ elements, the uniform distribution would put mass more than $\varepsilon$ outside $S$, so its distance from the output would exceed $\varepsilon$.

4. **Bounds (Radhakrishnan and Ta-Shma 2000).** For $k \le n - 1$ and $\varepsilon$ not too close to 1, every $(k, \varepsilon)$-disperser with $m > d$ has seed length $d \ge \log_2(n - k) + \log_2(1/\varepsilon) - O(1)$ and entropy loss $k + d - m \ge \log_2\log_2(1/\varepsilon) - O(1)$. A random function reaches both bounds up to additive constants. Extractors need more: $d \ge \log_2(n - k) + 2\log_2(1/\varepsilon) - O(1)$ and entropy loss at least $2\log_2(1/\varepsilon) - O(1)$. So the one-sided condition saves about $\log_2(1/\varepsilon)$ seed bits.

5. **Dispersers from expanders.** Let $H$ be a $D$-regular graph on $N$ vertices whose walk matrix has second largest absolute eigenvalue $\lambda$, and let $\mathrm{Disp}(x, y)$ be the $y$-th neighbour of $x$, so $m = n$. By the corollary of the expander mixing lemma proved for the [expander walk sampler](/expander-walk-sampler/), a set of density $\sigma = K/N$ has neighbours in all but a fraction $\tau \le \lambda^2(1 - \sigma)/(\sigma + \lambda^2(1 - \sigma)) < \lambda^2/\sigma$ of the vertices. So $H$ is a $(k, \varepsilon)$-disperser with $\varepsilon = \lambda^2 N/K$. With $\lambda \approx 2/\sqrt{D}$, as for Ramanujan graphs, $D \approx 4 \cdot 2^{n-k}/\varepsilon$, so the seed has about $n - k + \log_2(1/\varepsilon) + 2$ bits. This is short only when $k$ is close to $n$; for small $k$, constructions based on extractors do much better.

## Examples and non-examples

- **The Petersen graph.** It is 3-regular on 10 vertices with walk eigenvalues $1, 1/3, -2/3$, so $\lambda = 2/3$. Use it as a bipartite graph with 10 left and 10 right vertices, and $\Gamma(A)$ the set of neighbours of $A$. The smallest $|\Gamma(A)|$ over all sets of size $K$ is:

  | $K$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | smallest $\lvert\Gamma(A)\rvert$ | 3 | 5 | 6 | 6 | 8 | 9 | 9 | 10 | 10 | 10 |
  | bound from Fact 5 | 2 | 3.6 | 4.9 | 6 | 6.9 | 7.7 | 8.4 | 9 | 9.5 | 10 |

  So every set of 8 left vertices reaches all 10 right vertices ($\varepsilon = 0$), and every set of 5 reaches at least 8 ($\varepsilon = 0.2$). The spectral bound is exact for $K = 4$.
- **Trivial disperser.** $\mathrm{Disp}(x, y) = y$ with $d = m$ reaches every output from every set, so $\varepsilon = 0$. It ignores the source and needs as many seed bits as output bits. The goal is $d$ much smaller than $m$.
- **Non-example: a prefix.** $\mathrm{Disp}(x, y) = (x_1, \ldots, x_m)$ with $d = 0$ is not a disperser for any $k \le n - m$ and $\varepsilon < 1 - 2^{-m}$: the flat source on the $2^{n-m}$ strings that start with $0^m$ has min-entropy $n - m \ge k$, and all its outputs equal $0^m$.
- **Non-example: no seed, one output bit.** With $d = 0$ and $m = 1$, a $(k, 0)$-disperser must be non-constant on every set of $K$ strings. For $k \le n - 1$ this is impossible, since one preimage of $f$ has at least $2^{n-1}$ elements. This is the support version of the fact that deterministic extractors do not exist for general $k$-sources.
- **Two-source dispersers and Ramsey graphs.** A function $f : \{0,1\}^n \times \{0,1\}^n \to \{0,1\}$ is a *two-source disperser* for min-entropy $k$ if $f$ is non-constant on $A \times B$ for all sets $A, B$ of size $K$. This says that the bipartite graph with an edge $(a, b)$ when $f(a, b) = 1$ has no complete and no empty $K \times K$ bipartite subgraph: it is a bipartite Ramsey graph (see [Ramsey's theorem](/ramsey-theorem/)). A random $f$ works for $k = \log_2 n + O(1)$. Explicit constructions are much harder; Barak, Rao, Shaltiel and Wigderson (2012) reached $k = n^{o(1)}$.

## Related definitions

- [Randomness extractor](/randomness-extractor/) and [seeded extractor](/seeded-extractor/): the two-sided notion. Every extractor is a disperser with the same parameters.
- [Hitting set generator](/hitting-set-generator/): the one-sided relative of a pseudorandom generator. A disperser is to an extractor what a hitting set generator is to a pseudorandom generator.
- [Two-source extractor](/two-source-extractor/): the two-sided form of a two-source disperser.
- [Expander walk sampler](/expander-walk-sampler/): the source of the spectral bound used in Fact 5. Expanders are dispersers for sets of large density.
- [Randomness amplification](/randomness-amplification/): the main algorithmic use of dispersers, through the hitting form.
- **Vertex expanders and condensers.** A graph in which every set of at most $K$ left vertices has close to $D$ times as many neighbours is an unbalanced vertex expander; a disperser asks only that sets of size $K$ cover most of the right side.

## References
