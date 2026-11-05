---
tag: QYBSZD
kind: problem
slug: lcp-array-construction
name: LCP array construction
aliases:
- computing the LCP array
area: strings/suffix-structures
level: core
summary: Compute the LCP array from a string and its suffix array.
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: Θ(n)}
prereqs: [lcp-array, suffix-array]
see_also: [kasai-algorithm, suffix-array-construction, lcp-rmq-reduction, suffix-tree-from-suffix-array, burrows-wheeler-transform, longest-common-extension-query]
sources:
  - paper: doi:10.1007/3-540-48194-X_17
    title: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, CPM 2001, LNCS 2089
    locator: pages 181 to 192, the problem statement and the O(n) algorithm
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948, the computation of the Lcp values during the sort
  - paper: Juha Kärkkäinen, Giovanni Manzini and Simon J. Puglisi, Permuted longest-common-prefix array, CPM 2009, LNCS 5577
    locator: the PLCP array, the Phi algorithm and its experimental comparison
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press, 2015
    locator: Chapter 8 (Classical indexes), and Chapter 9 (Burrows-Wheeler indexes) for the construction of the LCP array from the BWT
---

LCP array construction is the problem of computing the [LCP array](/lcp-array/) of a text: given a text $T$ of length $n$ and its [suffix array](/suffix-array/), output for each rank $i \ge 1$ the length of the longest common prefix of the suffixes of ranks $i - 1$ and $i$. [Kasai's algorithm](/kasai-algorithm/) solves it in $\Theta(n)$ time with equality tests on symbols, which is optimal because the output has $n$ entries. The problem matters because the suffix array alone supports only pattern search, while the suffix array with its LCP array can do most of what a [suffix tree](/suffix-tree/) does.

## In plain words

Sort all endings of a text. For each ending in the sorted list, count how many first letters it shares with the ending just before it. The problem is to compute all these counts.

You can compare each pair of neighbors letter by letter. That is correct, but a text with long repeats, such as a long run of one letter, makes this slow, because the same letters are compared again and again. The good methods compare each letter only a few times in total, so the work grows only in proportion to the length of the text.

## Definition

**Input.** A text $T = T[0 \ldots n-1]$, $n \ge 0$, over an alphabet whose symbols can be tested for equality, and its suffix array $SA[0 \ldots n-1]$. Indices are 0-based. No sentinel is appended: $SA$ lists the start positions of the $n$ nonempty suffixes $T_p = T[p \ldots n-1]$ in increasing lexicographic order, where a proper prefix sorts first.

**Output.** The array $LCP[0 \ldots n-1]$ with

$$LCP[0] = 0, \qquad LCP[i] = \mathrm{lcp}(T_{SA[i-1]}, T_{SA[i]}) \quad (1 \le i \le n-1),$$

where $\mathrm{lcp}(x, y) = \max\{ h \ge 0 : x[0 \ldots h-1] = y[0 \ldots h-1] \}$. For $n = 0$ the output is empty.

The order on the alphabet is needed to build $SA$, but not to compute $LCP$ from it: equal symbols are all that matter.

## Variants

- **The permuted LCP array.** Output $PLCP[p] = LCP[RANK[p]]$ in text order instead. It has the property $PLCP[p+1] \ge PLCP[p] - 1$, so it fits in $2n$ bits.
- **With a sentinel.** For $T\$$ the suffix array has $n + 1$ entries with the empty suffix first, and the output has one more entry, $LCP[1] = 0$.
- **A collection of strings.** For a [generalized suffix array](/generalized-suffix-tree/) of several strings joined with separators, the separators must not match each other, so that no common prefix runs across the end of a string.
- **Together with the suffix array.** Compute both in one pass of a suffix sorting algorithm, as [prefix doubling](/prefix-doubling/) or an induced sorting method can do.
- **Sparse or external.** Compute LCP values only for a subset of suffixes, or for a text that does not fit in memory.

## Examples

| text | $SA$ | $LCP$ | $\sum LCP$ |
|---|---|---|---|
| `banana` | $[5, 3, 1, 0, 4, 2]$ | $[0, 1, 3, 0, 0, 2]$ | 6 |
| `mississippi` | $[10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$ | $[0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]$ | 13 |
| `aaaaa` | $[4, 3, 2, 1, 0]$ | $[0, 1, 2, 3, 4]$ | 10 |
| `abababab` | $[6, 4, 2, 0, 7, 5, 3, 1]$ | $[0, 2, 4, 6, 0, 1, 3, 5]$ | 21 |
| `abcd` | $[0, 1, 2, 3]$ | $[0, 0, 0, 0]$ | 0 |

The texts $\texttt{a}^n$ and $(\texttt{ab})^{n/2}$ are the bad cases for the direct method. The sum of the LCP values is $\binom{n}{2}$ for $\texttt{a}^n$, so a comparison of each adjacent pair from scratch does $\Theta(n^2)$ work. The text `abcd` with all symbols distinct is the best case for every method.

## Known algorithms

All bounds are in the [word RAM](/word-ram/) and assume that $SA$ is given.

| algorithm | time | working space beyond $T$, $SA$ and the output | notes |
|---|---|---|---|
| compare each adjacent pair directly | $\Theta(n + \sum_i LCP[i])$, so $O(n^2)$ worst case | $O(1)$ | fast on random text, where the values are small |
| [Kasai's algorithm](/kasai-algorithm/) | $\Theta(n)$ | $n$ words for the inverse suffix array | the standard method |
| $\Phi$ algorithm (Kärkkäinen, Manzini and Puglisi, 2009) | $\Theta(n)$ | $n$ words | computes the permuted array with sequential access to the text, faster in practice |
| hashing of prefixes and binary search | $O(n \log n)$ expected | $n$ words of hash values | uses [substring equality queries](/substring-equality-queries/) by [polynomial hashing](/polynomial-rolling-hash/) |
| from the [suffix tree](/suffix-tree/) | $\Theta(n)$ | the tree | $LCP[i]$ is the string depth of the lowest common ancestor of the leaves of ranks $i - 1$ and $i$ |
| from the [Burrows-Wheeler transform](/burrows-wheeler-transform/) | $O(n \log \sigma)$ | succinct | for indexes that keep only the BWT |
| during suffix sorting ([Manber and Myers](/manber-myers-algorithm/)) | $O(n \log n)$ | $O(n)$ words | the LCP values come out of the doubling steps |

## Bounds

- **Upper bound.** $O(n)$ time when $SA$ is given, by Kasai's algorithm, with equality tests on the symbols. If only $T$ is given, the cost is that of [suffix array construction](/suffix-array-construction/) plus $O(n)$: $O(n)$ for an integer alphabet of size $n^{O(1)}$, and $O(n \log n)$ for a general ordered alphabet.
- **Lower bound.** Each algorithm writes $n$ entries, so it needs $\Omega(n)$ time. Kasai's algorithm is optimal up to a constant factor.
- **Comparisons.** Kasai's algorithm makes at most $2n$ equal comparisons and at most $n$ unequal ones.

## Reductions

- **To the suffix tree and back.** From $SA$ and $LCP$ the suffix tree is built in $O(n)$ time with a stack ([suffix tree from suffix array](/suffix-tree-from-suffix-array/)). From the suffix tree, $SA$ is the order of the leaves in a depth-first walk with sorted children, and $LCP$ comes from the same walk in $O(n)$ time. So, given the suffix array, the two structures are equivalent up to linear time.
- **To range minimum queries.** With the LCP array and a [range minimum query](/range-minimum-query/) structure, the LCP of any two suffixes is one query ([LCP-RMQ reduction](/lcp-rmq-reduction/)). This gives [longest common extension queries](/longest-common-extension-query/) in $O(1)$ time.
- **From LCE queries.** Conversely, an LCE structure answers each $LCP[i]$ with one query, so $n$ queries give the array.

## Applications

- The [longest repeated substring](/longest-repeated-substring/) is a prefix of length $\max_i LCP[i]$ of $T_{SA[i]}$ at the maximum.
- The [number of distinct substrings](/count-distinct-substrings/) is $n(n+1)/2 - \sum_i LCP[i]$.
- The [longest common substring](/longest-common-substring/) of two strings is a maximum of $LCP$ over adjacent suffixes from different strings.
- The [enhanced suffix array](/enhanced-suffix-array/) and the [LCP interval tree](/lcp-interval-tree/) use the array to simulate suffix tree walks, for example to find [maximal repeats](/maximal-repeats/).
- The search of Manber and Myers in $O(m + \log n)$ time uses LCP values to avoid comparing the pattern again from its start.
- In a [compressed suffix tree](/compressed-suffix-tree/), the LCP array is stored as the $2n$-bit PLCP vector.

## References
