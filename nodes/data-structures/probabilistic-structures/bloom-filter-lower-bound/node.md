---
tag: XJMVNR
kind: theorem
slug: bloom-filter-lower-bound
name: Approximate membership space lower bound
aliases:
- Carter et al. lower bound
area: data-structures/probabilistic-structures
level: advanced
summary: Any approximate membership structure with false positive rate eps needs about n log(1/eps) bits.
prereqs: [approximate-membership, counting-argument, binomial-coefficient-bounds, markov-inequality]
see_also: [bloom-filter, bloom-filter-optimal-hash-count, xor-filter, binary-fuse-filter, ribbon-filter, false-positive-rate, communication-complexity]
sources:
  - paper: doi:10.1145/800133.804332
    title: Larry Carter, Robert Floyd, John Gill, George Markowsky and Mark Wegman, Exact and approximate membership testers, STOC 1978
    locator: pages 59 to 65 (the counting lower bound for approximate membership testers)
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2.2 (the counting argument and the comparison with Bloom filters)
  - paper: doi:10.1007/978-3-540-70575-8_32
    title: Martin Dietzfelbinger and Rasmus Pagh, Succinct data structures for retrieval and approximate membership, ICALP 2008
    locator: pages 385 to 396 (static filters within a factor 1 + o(1) of the bound)
  - paper: doi:10.1137/120867044
    title: Shachar Lovett and Ely Porat, A space lower bound for dynamic approximate membership data structures, SIAM Journal on Computing 42(6), 2013
    locator: pages 2182 to 2196 (the bound C(eps) n log2(1/eps) with C(eps) > 1 for the dynamic case)
---

Every data structure that stores a set of $n$ keys from a universe of size $u$ and answers membership queries with [false positive rate](/false-positive-rate/) $\varepsilon$ and no false negatives needs at least about $n \log_2(1/\varepsilon)$ bits, when $u$ is much larger than $n$. The bound comes from counting: one memory state can serve only the sets that fit inside its set of accepted keys. It shows that the [Bloom filter](/bloom-filter/), with $1.44 \, n \log_2(1/\varepsilon)$ bits, is 44 percent above the best possible, and it is the target of [xor](/xor-filter/), [binary fuse](/binary-fuse-filter/) and [ribbon](/ribbon-filter/) filters. Carter, Floyd, Gill, Markowsky and Wegman proved it in 1978.

## Statement

Let $1 \le n < u$, let $0 < \varepsilon < 1$, and let a *filter* for the [approximate membership problem](/approximate-membership/) consist of a build map from sets $S \subseteq U$ with $|S| = n$ to memory states of $m$ bits, and a query map from a state and a key to yes or no. Write $A(\sigma)$ for the set of keys that state $\sigma$ accepts.

**Theorem (deterministic form).** Suppose that for each $S$ the state $\sigma = \sigma(S)$ satisfies $S \subseteq A(\sigma)$ and $|A(\sigma) \setminus S| \le \varepsilon(u - n)$. Then
$$ m \ \ge\ \log_2 \frac{\binom{u}{n}}{\binom{L}{n}} \ \ge\ n \log_2 \frac{u}{L} \ =\ n \log_2 \frac{1}{\varepsilon + (1 - \varepsilon) n/u}, \qquad L = n + \varepsilon(u - n). $$

**Theorem (randomized form).** Suppose the build map also uses random bits $\rho$, the query map may depend on $\rho$, and for each $S$ and each $x \notin S$ the probability over $\rho$ that $x$ is accepted is at most $\varepsilon$, while each $x \in S$ is always accepted. Then for each $\eta > 0$,
$$ m \ \ge\ n \log_2 \frac{u}{n + (1 + \eta)\varepsilon(u - n)} - \log_2 \frac{1 + \eta}{\eta}. $$
With $\eta = 1/n$ this is at least $n \log_2 \frac{1}{\varepsilon + n/u} - \log_2 e - \log_2(n + 1)$, so $m \ge n \log_2(1/\varepsilon) - O(\log n)$ when $n/u$ is small compared with $\varepsilon$.

## In plain words

A filter is a short string of bits. Each possible string accepts some keys. When the filter is built for a set, its string must accept all keys of the set and only a few others.

So one string can serve only the sets that fit inside its small group of accepted keys. There are very many possible sets, and each string serves only a few of them. So there must be many different strings, and many strings need many bits.

Counting this gives about one bit per key for each halving of the error rate. A rate of one in a hundred needs at least about six and a half bits per key, however clever the filter is. A Bloom filter needs about nine and a half.

## Proof

**Deterministic form.** Each set $S$ is mapped to a state $\sigma(S)$ with $S \subseteq A(\sigma(S))$ and $|A(\sigma(S))| \le n + \varepsilon(u - n) = L$. Fix a state $\sigma$ that is used for some set. The sets $S$ with $\sigma(S) = \sigma$ are $n$-subsets of $A(\sigma)$, so there are at most $\binom{\lfloor L \rfloor}{n} \le \binom{L}{n}$ of them, where $\binom{L}{n} = L(L-1)\cdots(L - n + 1)/n!$ for real $L \ge n$. There are at most $2^m$ states, and each of the $\binom{u}{n}$ sets has a state, so by the [counting argument](/counting-argument/)
$$ 2^m \binom{L}{n} \ge \binom{u}{n}. $$
For the second inequality,
$$ \frac{\binom{u}{n}}{\binom{L}{n}} = \prod_{i=0}^{n-1} \frac{u - i}{L - i} \ \ge\ \left(\frac{u}{L}\right)^n, $$
because $L \le u$ and so $(u - i)/(L - i) \ge u/L$ for $0 \le i < n$: cross-multiplying gives $uL - iL \ge uL - iu$. Finally $u/L = 1/(\varepsilon + (1 - \varepsilon)n/u)$.

**Randomized form.** Fix $S$ and let $X = |A(\sigma) \setminus S|$ for the state $\sigma$ built from $S$ with random $\rho$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[X] = \sum_{x \notin S} \Pr[x \text{ accepted}] \le \varepsilon(u - n)$. If $\varepsilon(u - n) > 0$, [Markov's inequality](/markov-inequality/) gives
$$ \Pr\big[X > (1+\eta)\varepsilon(u-n)\big] \le \frac{1}{1 + \eta}, $$
so $\Pr[X \le (1 + \eta)\varepsilon(u - n)] \ge \eta/(1 + \eta)$. Call $(S, \rho)$ *good* when this holds. Now choose $S$ uniformly at random as well. Then $\Pr[(S, \rho) \text{ good}] \ge \eta/(1+\eta)$, so there is a fixed value $\rho^*$ with $\Pr_S[(S, \rho^*) \text{ good}] \ge \eta/(1 + \eta)$. With $\rho = \rho^*$ fixed, the build and query maps are deterministic, and they satisfy the hypothesis of the deterministic form with $(1 + \eta)\varepsilon$ in place of $\varepsilon$, but only for a family $\mathcal{F}$ of at least $\frac{\eta}{1+\eta}\binom{u}{n}$ sets. The same count gives
$$ 2^m \binom{L'}{n} \ge \frac{\eta}{1+\eta} \binom{u}{n}, \qquad L' = n + (1+\eta)\varepsilon(u-n), $$
and the product bound gives the claim, if $L' \le u$; if $L' > u$ the right side of the claim is negative and there is nothing to prove.

For $\eta = 1/n$: $\log_2((1 + \eta)/\eta) = \log_2(n + 1)$, and $n + (1 + 1/n)\varepsilon(u - n) \le (1 + 1/n)(\varepsilon u + n)$, so $n \log_2 \frac{u}{L'} \ge n \log_2 \frac{1}{\varepsilon + n/u} - n\log_2(1 + 1/n) \ge n \log_2\frac{1}{\varepsilon + n/u} - \log_2 e$, since $(1 + 1/n)^n \le e$. $\blacksquare$

## Consequences

**Bits per key.** For $u \gg n/\varepsilon$ the bound is $\log_2(1/\varepsilon)$ bits per key, independent of the size of the keys. Exact storage of the set needs $\log_2 \binom{u}{n} \approx n \log_2(eu/n)$ bits, which grows with $u$. For $u = 2^{32}$, $n = 10^6$ and $\varepsilon = 0.01$ the bound is $6.61$ bits per key, against $\log_2(1/\varepsilon) = 6.64$, a Bloom filter's $9.59$, and exact storage at about $13.5$.

**A small case.** Let $u = 16$, $n = 3$ and $\varepsilon = 1/4$. Then $L = 3 + 13/4 = 6.25$, so each state accepts at most 6 keys and serves at most $\binom{6}{3} = 20$ of the $\binom{16}{3} = 560$ sets. So there are at least 28 states and $m \ge 5$ bits, while exact storage needs $\lceil \log_2 560 \rceil = 10$ bits.

**The cost of the Bloom filter.** With the [optimal number of hash functions](/bloom-filter-optimal-hash-count/), a Bloom filter uses $\log_2 e \cdot \log_2(1/\varepsilon) \approx 1.44 \log_2(1/\varepsilon)$ bits per key, so 44 percent above the bound. Xor filters use about $1.23 \log_2(1/\varepsilon)$, and binary fuse and ribbon filters come within a few percent of the bound, for static sets.

**No help from the key size.** The bound does not depend on how keys are represented. A filter of 100-byte URLs and a filter of 4-byte integers need the same space for the same $n$ and $\varepsilon$, if $u$ is large in both cases.

## Tightness

**Hashing to a smaller universe.** Let $h$ map $U$ to $\{0, \ldots, \lceil n/\varepsilon \rceil - 1\}$ at random, and store the set $h(S)$ exactly. A key $x \notin S$ is accepted only if $h(x) \in h(S)$, which has probability at most $n/\lceil n/\varepsilon \rceil \le \varepsilon$. Storing the set of at most $n$ values exactly takes about $\log_2 \binom{n/\varepsilon}{n} \le n \log_2(e/\varepsilon)$ bits, for example with [Elias-Fano encoding](/elias-fano-encoding/) in about $n(\log_2(1/\varepsilon) + 2)$ bits, or with [Golomb coding](/golomb-coding/) of the sorted differences. This is within an additive $O(n)$ bits of the bound, but a query is slow.

**Fast static filters.** Dietzfelbinger and Pagh (2008) store an $r$-bit fingerprint for each key in a retrieval structure of $(1 + o(1)) n r$ bits, which gives a rate of $2^{-r}$ in $(1 + o(1)) n \log_2(1/\varepsilon)$ bits with constant query time. The [ribbon filter](/ribbon-filter/) and the [binary fuse filter](/binary-fuse-filter/) are practical forms of this idea.

**The dynamic case is harder.** Lovett and Porat (2010, 2013) proved that a filter that supports inserts, with the set growing to $n$ keys, needs at least $C(\varepsilon) \, n \log_2(1/\varepsilon)$ bits for a constant $C(\varepsilon) > 1$ that depends only on $\varepsilon$, when $u$ is large enough. So the static bound cannot be reached by an incremental filter.

## History

Carter, Floyd, Gill, Markowsky and Wegman (1978) defined approximate membership testers and proved the counting bound, eight years after Bloom's paper. The bound became the standard measure of the space of filters, and the gap of $\log_2 e$ for Bloom filters is in each survey, such as that of Broder and Mitzenmacher (2004). Dietzfelbinger and Pagh (2008) gave static filters that meet it up to $1 + o(1)$, and Lovett and Porat (2010) proved that dynamic filters cannot.

## References
