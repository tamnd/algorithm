---
tag: XSAGXT
kind: problem
slug: approximate-membership
name: Approximate membership problem
aliases:
- approximate set membership
- set membership with false positives
area: data-structures/probabilistic-structures
level: intro
summary: Store a set so that membership queries may return false positives but never false negatives.
prereqs: [dictionary, hash-function, one-sided-error]
see_also: [bloom-filter, false-positive-rate, bloom-filter-lower-bound, cuckoo-filter, xor-filter, quotient-filter, bloomier-filter, perfect-hashing]
sources:
  - paper: doi:10.1145/800133.804332
    title: Larry Carter, Robert Floyd, John Gill, George Markowsky and Mark Wegman, Exact and approximate membership testers, Proceedings of the 10th ACM Symposium on Theory of Computing (STOC 1978)
    locator: pages 59 to 65 (the definition of an approximate membership tester and the space lower bound)
  - paper: doi:10.1145/362686.362692
    title: Burton H. Bloom, Space/time trade-offs in hash coding with allowable errors, Communications of the ACM 13(7), 1970
    locator: pages 422 to 426 (the problem with allowable errors and the two hash-coding methods)
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2 (the false positive rate, the space lower bound and the comparison with exact methods)
  - paper: doi:10.1007/978-3-540-70575-8_32
    title: Martin Dietzfelbinger and Rasmus Pagh, Succinct data structures for retrieval and approximate membership, ICALP 2008
    locator: pages 385 to 396 (retrieval structures and the filters built from them)
  - paper: doi:10.1109/90.851975
    title: Li Fan, Pei Cao, Jussara Almeida and Andrei Z. Broder, Summary cache, a scalable wide-area Web cache sharing protocol, IEEE/ACM Transactions on Networking 8(3), 2000
    locator: pages 281 to 293 (filters as summaries of the contents of cache servers)
  - paper: doi:10.1137/120867044
    title: Shachar Lovett and Ely Porat, A space lower bound for dynamic approximate membership data structures, SIAM Journal on Computing 42(6), 2013
    locator: pages 2182 to 2196 (the lower bound for the dynamic version)
---

The approximate membership problem asks for a compact representation of a set $S$ of $n$ keys that answers "is $x$ in $S$?" with [one-sided error](/one-sided-error/): a key of $S$ always gets "yes", and a key outside $S$ gets "yes" with probability at most a fixed $\varepsilon$, the [false positive rate](/false-positive-rate/). In exchange for these errors, the space drops from about $\log_2 \binom{u}{n}$ bits, which depends on the size $u$ of the universe, to about $n \log_2(1/\varepsilon)$ bits, which does not. The [Bloom filter](/bloom-filter/) is the classic solution; cuckoo, quotient, xor and ribbon filters are newer ones.

## In plain words

You keep a list of the bad web addresses, and you check each address that a user types. The list is too large to keep in fast memory. So you keep a small summary of it instead. The summary answers "maybe in the list" or "surely not in the list".

When it says "surely not", it is right, and you are done fast. When it says "maybe", you look in the full list on the disk. Sometimes the summary says "maybe" for a good address. This costs one slow look on the disk, but it never gives a wrong final answer. The smaller the chance of a wrong "maybe", the more space the summary needs. A summary with a one percent chance of a wrong "maybe" needs fewer than ten bits for each address, however long the addresses are.

## Definition

Let $U$ be a universe of $u$ keys, let $n \le u$, and let $0 < \varepsilon < 1$. A *filter* for $S \subseteq U$ with $|S| = n$ is a pair of procedures. BUILD takes $S$ and random bits $\rho$ and makes a string $F$. QUERY takes $F$ and a key $x \in U$ and returns yes or no. It must meet two conditions.

- **No false negatives.** For each $S$, each $\rho$ and each $x \in S$, QUERY$(F, x) = $ yes.
- **Few false positives.** For each $S$ and each fixed $x \in U \setminus S$, $\Pr_\rho[\text{QUERY}(F, x) = \text{yes}] \le \varepsilon$.

The probability is over the random bits of BUILD, which in practice are the choice of the [hash functions](/hash-function/). It is not over the queries. The cost measures are the length of $F$ in bits (the space), and the time of BUILD and QUERY, usually in the [word RAM](/word-ram/) model.

Carter, Floyd, Gill, Markowsky and Wegman (1978) used a deterministic form. A *tester* maps each $S$ to a string $F(S)$ whose set of accepted keys $A(F(S))$ satisfies $S \subseteq A(F(S))$ and $|A(F(S)) \setminus S| \le \varepsilon (u - n)$. The two forms give the same space bound up to lower-order terms, as the [space lower bound](/bloom-filter-lower-bound/) page shows.

## Variants

- **Static.** $S$ is given at once and never changes. [Xor filters](/xor-filter/), [binary fuse filters](/binary-fuse-filter/) and [ribbon filters](/ribbon-filter/) solve this version with the least space.
- **Incremental.** Keys can be inserted one at a time, up to a capacity fixed in advance. The [Bloom filter](/bloom-filter/) is the standard solution. The [scalable Bloom filter](/scalable-bloom-filter/) removes the capacity limit.
- **Dynamic.** Keys can be inserted and deleted. [Counting Bloom filters](/counting-bloom-filter/), [cuckoo filters](/cuckoo-filter/) and [quotient filters](/quotient-filter/) solve it. A delete of a key that was never inserted is not allowed, because no filter can tell it apart from a false positive.
- **Retrieval with membership.** Each key of $S$ has a value, and a query for a key of $S$ returns its value. A query for other keys may return anything, or "absent" with probability at least $1 - \varepsilon$. This is the [Bloomier filter](/bloomier-filter/).
- **Multiplicities.** The input is a multiset, and a query estimates the count of a key. See the [spectral Bloom filter](/spectral-bloom-filter/) and the [frequency estimation problem](/frequency-estimation/).
- **Sliding windows and streams.** Only the recent keys of an unbounded stream count. Here false negatives for old keys are allowed, as in the [stable Bloom filter](/stable-bloom-filter/).
- **Exact membership.** The case $\varepsilon = 0$ is the static [dictionary](/dictionary/) problem with only membership queries.

## Examples

**A small universe.** Let $U = \{0, 1, \ldots, 15\}$, so $u = 16$, and let $S = \{3, 7, 12\}$. A tester that accepts $A = \{3, 5, 7, 12\}$ is valid for each $\varepsilon \ge 1/13$: it accepts all of $S$, and one of the 13 keys outside $S$. A tester that accepts $\{3, 5, 12\}$ is not valid for any $\varepsilon$, because it rejects $7 \in S$. The tester that accepts all of $U$ is valid for $\varepsilon = 1$ and needs no space.

**Counting the space.** There are $\binom{16}{3} = 560$ sets $S$, so an exact representation needs $\lceil \log_2 560 \rceil = 10$ bits. With $\varepsilon = 1/13$, each accepted set of size 4 contains $\binom{4}{3} = 4$ of the sets $S$. So at least $560 / 4 = 140$ different strings are needed, and $\lceil \log_2 140 \rceil = 8$ bits suffice to name them. The counting argument of the [lower bound](/bloom-filter-lower-bound/) turns this into a general bound.

**A realistic size.** Take $n = 10^6$ keys from the universe of 32-bit integers, $u = 2^{32}$. An exact set needs $\log_2 \binom{2^{32}}{10^6}$ bits, which is 13.51 bits per key. A filter with $\varepsilon = 0.01$ needs at least $\log_2 100 = 6.64$ bits per key, and a Bloom filter with the best number of hash functions uses 9.59 bits per key. For keys that are 100-byte strings, the exact bound grows to about 780 bits per key, while the filter bounds stay the same.

**Fingerprints.** Choose a hash function $h : U \to \{0, \ldots, n/\varepsilon - 1\}$ from a [universal family](/universal-hash-family/), and store the set $h(S)$ exactly. A key $x \notin S$ is accepted only if $h(x) = h(y)$ for some $y \in S$. By the [union bound](/union-bound/), this has probability at most $n \cdot \varepsilon / n = \varepsilon$. This solves the problem with about $n \log_2(e/\varepsilon)$ bits if $h(S)$ is stored as a compressed sorted list.

## Known algorithms

| structure | operations | bits per key, about | query probes |
|---|---|---|---|
| [Bloom filter](/bloom-filter/) | insert, query | $1.44 \log_2(1/\varepsilon)$ | $\log_2(1/\varepsilon)$ random bits |
| [counting Bloom filter](/counting-bloom-filter/) | insert, delete, query | 4 times the Bloom filter | as Bloom |
| [cuckoo filter](/cuckoo-filter/) | insert, delete, query | $(\log_2(1/\varepsilon) + 3)/0.955$ | 2 buckets |
| [quotient filter](/quotient-filter/) | insert, delete, query, merge, resize | $(\log_2(1/\varepsilon) + 3)/\alpha$ at load $\alpha$ | one cluster of adjacent slots |
| [xor filter](/xor-filter/) | static | $1.23 \log_2(1/\varepsilon)$ | 3 cells |
| [binary fuse filter](/binary-fuse-filter/) | static | $1.13 \log_2(1/\varepsilon)$ for large $n$ | 3 cells in a short window |
| [ribbon filter](/ribbon-filter/) | static | $(1 + \delta) \log_2(1/\varepsilon)$, small $\delta$ | one band of about 64 cells |

The figures for the cuckoo filter are for buckets of 4 entries and a load of 95 percent. The xor, binary fuse and ribbon filters need $\log_2(1/\varepsilon)$ to be an integer number of fingerprint bits.

## Bounds

- **Lower bound.** Each filter for sets of size $n$ from a universe of size $u$ needs at least $n \log_2 \frac{1}{\varepsilon + (1-\varepsilon)n/u}$ bits in the worst case, which tends to $n \log_2(1/\varepsilon)$ when $u/n \to \infty$ (Carter et al. 1978). The proof is a [counting argument](/counting-argument/) on the [lower bound](/bloom-filter-lower-bound/) page.
- **Static upper bound.** Filters built from retrieval structures use $(1 + o(1))\, n \log_2(1/\varepsilon)$ bits with constant query time when $\log_2(1/\varepsilon)$ is an integer (Dietzfelbinger and Pagh 2008). So the static problem is solved up to lower-order terms.
- **Dynamic lower bound.** If the filter must support inserts without knowing $S$ in advance and $u$ is large enough, then $C(\varepsilon) \cdot n \log_2(1/\varepsilon)$ bits are needed for a constant $C(\varepsilon) > 1$ that depends on $\varepsilon$ (Lovett and Porat 2013). So a dynamic filter cannot match the static bound exactly.
- **Bloom filters.** The best Bloom filter uses $\log_2 e \approx 1.44$ times the lower bound, see the [optimal number of hash functions](/bloom-filter-optimal-hash-count/).

## Reductions

- **To retrieval.** Pick a hash $g : U \to \{0,1\}^r$ and store a static function $f$ with $f(x) = g(x)$ for each $x \in S$. Accept $x$ if $f(x) = g(x)$. For $x \notin S$ the stored value $f(x)$ does not depend on $g(x)$, so the false positive rate is $2^{-r}$. This is how the [Bloomier](/bloomier-filter/), [xor](/xor-filter/) and [ribbon](/ribbon-filter/) filters work. The cost is the size of the retrieval structure, about $r$ bits per key.
- **To exact membership.** Store $h(S)$ for a hash $h$ into a range of size $n/\varepsilon$, as in the fingerprint example. Any exact [dictionary](/dictionary/) or [hash table](/hash-table/) on these fingerprints is a filter. The cuckoo and quotient filters refine this reduction.
- **From exact membership.** A filter in front of an exact set lets the slow exact set answer only the "yes" queries. The expected number of slow lookups on a key outside $S$ is at most $\varepsilon$.

## Applications

- **Avoiding slow lookups.** A [log-structured merge tree](/log-structured-merge-tree/) keeps one filter for each file on disk, so that a read skips each file that cannot hold the key. Distributed databases send filters over the network in a [Bloom join](/bloom-join/).
- **Web caches.** Each cache server sends the others a filter of its contents. A server asks a neighbour for a page only if the neighbour's filter says yes (Fan, Cao, Almeida and Broder 2000). Deletes from the cache need a [counting Bloom filter](/counting-bloom-filter/).
- **Dictionaries with rare errors.** Bloom's own example was a hyphenation dictionary in which most words follow simple rules: a filter of the exceptions sends only a few words to the slow table on disk.
- **Model checking.** [Bitstate hashing](/bitstate-hashing/) records the visited states of a program in a bit array and accepts that some states are missed.
- **Set reconciliation and networking.** Two parties compare sets by sending filters, see [set reconciliation](/set-reconciliation/).

## References
