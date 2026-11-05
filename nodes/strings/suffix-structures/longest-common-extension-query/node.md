---
tag: QQ0R59
kind: problem
slug: longest-common-extension-query
name: Longest common extension query
aliases:
- LCE query
area: strings/suffix-structures
level: advanced
summary: Given two positions, return the length of the longest common prefix of their suffixes.
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: O(1)}
  space: {extra: O(n)}
prereqs: [lcp-array, lcp-rmq-reduction, range-minimum-query]
see_also: [lcp-rmq-reduction, lcp-array, substring-equality-queries, polynomial-rolling-hash, lowest-common-ancestor, suffix-tree, range-minimum-query, sparse-table]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 9.1 (longest common extension, a bridge to inexact matching), with the maximal palindromes of Section 9.2 and the k-mismatch problem of Section 9.4
  - paper: doi:10.1016/j.jda.2010.08.004
    title: Lucian Ilie, Gonzalo Navarro and Liviu Tinta, The longest common extension problem revisited and applications to approximate string searching, Journal of Discrete Algorithms 8(4), 2010
    locator: the comparison of the direct scan with the constant-time methods, and the finding that the direct scan is fast on typical texts
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948, the suffix array and the Lcp values
---

The longest common extension (LCE) query asks, for a fixed text $T$ of length $n$ and two positions $p$ and $q$, for the length of the longest common prefix of the suffixes $T[p \ldots]$ and $T[q \ldots]$: how far the text reads the same from both places. After $O(n)$ preprocessing, the query takes $O(1)$ time with the [suffix array](/suffix-array/), the [LCP array](/lcp-array/) and a [range minimum query](/range-minimum-query/) structure, by the [LCP-RMQ reduction](/lcp-rmq-reduction/), or with a [suffix tree](/suffix-tree/) and [lowest common ancestor](/lowest-common-ancestor/) queries. LCE queries are the inner step of many algorithms for approximate matching, palindromes and repeats.

## In plain words

Put two fingers on a text, at two places. Move both fingers to the right, one letter at a time, as long as they point to the same letter. How many steps can you take? That number is the answer to the query.

Moving the fingers takes as many steps as the answer, and some algorithms ask this question millions of times. With some work done once on the text, each question can be answered in one step: sort all endings of the text, write down how much each ending shares with its neighbor in the sorted list, and look up the smallest such number between the two endings.

## Definition

**Input.** A text $T = T[0 \ldots n-1]$ over an ordered alphabet, given once for preprocessing. Positions are 0-based. Then queries, each a pair of positions $0 \le p, q \le n$.

**Output.** For each query,

$$\mathrm{LCE}(p, q) = \max \{\, \ell \ge 0 : T[p \ldots p + \ell - 1] = T[q \ldots q + \ell - 1] \,\},$$

where both ranges must lie inside $T$. So $\mathrm{LCE}(p, p) = n - p$, and $\mathrm{LCE}(p, n) = 0$. No sentinel is needed: the end of the text stops the extension.

**The standard solution.** Build the suffix array $SA$, its inverse $RANK$, the LCP array and a range minimum structure on it. For $p \ne q$ with $p, q < n$, let $i < j$ be $RANK[p]$ and $RANK[q]$ in order. Then $\mathrm{LCE}(p, q) = \min LCP[i+1 \ldots j]$, by the LCP-RMQ lemma.

## Variants

- **Two strings.** $\mathrm{LCE}_{X,Y}(i, j)$ for a position $i$ of $X$ and $j$ of $Y$: solve it on $X \# Y$ with a separator $\#$ that occurs in neither string; the separator stops each extension.
- **Backward extension.** The longest common suffix of $T[0 \ldots p]$ and $T[0 \ldots q]$ is an LCE query on the reversed text.
- **With mismatches.** $\mathrm{LCE}_k(p, q)$ allows $k$ mismatches. It is $k + 1$ plain LCE queries, each jumping over one mismatch: the *kangaroo* method.
- **Substring equality.** Is $T[p \ldots p + \ell - 1] = T[q \ldots q + \ell - 1]$? This is the test $\mathrm{LCE}(p, q) \ge \ell$; see [substring equality queries](/substring-equality-queries/).
- **Space-bounded and dynamic.** Answer LCE with less than $n$ words of extra space, or on a text that changes; these have their own trade-offs between space and query time.

## Examples

For $T = \texttt{mississippi}$:

| query | suffixes | answer |
|---|---|---|
| $\mathrm{LCE}(1, 4)$ | ississippi, issippi | 4 (`issi`) |
| $\mathrm{LCE}(2, 5)$ | ssissippi, ssippi | 3 (`ssi`) |
| $\mathrm{LCE}(3, 6)$ | sissippi, sippi | 2 (`si`) |
| $\mathrm{LCE}(0, 7)$ | mississippi, ppi | 0 |
| $\mathrm{LCE}(1, 1)$ | the same suffix | 10 |

With $SA = [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$ and $LCP = [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]$, the query $\mathrm{LCE}(2, 5)$ maps to the ranks $RANK[5] = 9$ and $RANK[2] = 10$, and returns $\min LCP[10 \ldots 10] = 3$.

**Kangaroo jumps.** Find the places where $P = \texttt{abd}$ occurs in $T = \texttt{abcabdabcaba}$ with at most $k = 1$ mismatch. At each alignment $i$, an LCE query between $P$ and $T[i \ldots]$ jumps over the matching part; a mismatch costs one step; then the next LCE query continues. At $i = 0$, the first jump is 2 (`ab`), then the mismatch `c` against `d`, then $P$ ends: 1 mismatch, a match. At $i = 3$ one jump of 3 covers $P$: an exact match. At $i = 1$ the jumps are 0, mismatch, 0, mismatch: more than 1, so no match. The matches are at 0, 3, 6 and 9. Each alignment costs at most $k + 1$ LCE queries, so the whole search takes $O(nk)$ time after the preprocessing.

**Palindromes.** Let $R$ be $T$ reversed. For a center $c$, the LCE of $T[c \ldots]$ and $R[n-1-c \ldots]$ is the number of symbols that read the same going right and left from $c$. For $T = \texttt{abacabaa}$ and $c = 3$, it is 4, so `abacaba` of length $2 \cdot 4 - 1 = 7$ is the longest odd palindrome with center 3. All $n$ centers take $O(n)$ time in total.

## Known algorithms

| method | preprocessing | query | notes |
|---|---|---|---|
| direct scan | none | $O(\ell)$ | fast in practice, since most answers are small on typical text (Ilie, Navarro and Tinta) |
| suffix array, LCP array and a [sparse table](/sparse-table/) | $O(n \log n)$ | $O(1)$ | simple; $\Theta(n \log n)$ words |
| suffix array, LCP array and a linear [RMQ](/range-minimum-query/) structure, such as [Fischer-Heun](/fischer-heun-rmq/) | $O(n)$ for an integer alphabet | $O(1)$ | the [LCP-RMQ reduction](/lcp-rmq-reduction/) |
| [suffix tree](/suffix-tree/) with constant-time [LCA](/lowest-common-ancestor/) | $O(n)$ for an integer alphabet | $O(1)$ | the string depth of the lowest common ancestor of the two leaves (Gusfield, Section 9.1) |
| [polynomial rolling hash](/polynomial-rolling-hash/) of the prefixes, with [binary search](/binary-search/) on $\ell$ | $O(n)$ | $O(\log \ell)$ by exponential then binary search | Monte Carlo: a hash collision can give a wrong answer |

For a general ordered alphabet, add the $O(n \log n)$ time to sort the symbols to the preprocessing of the suffix array methods.

## Bounds

- **Upper bound.** $O(n)$ preprocessing, $O(n)$ words and $O(1)$ query time in the [word RAM](/word-ram/), for an integer alphabet of size $n^{O(1)}$.
- **Lower bound.** The preprocessing must read the text, so it takes $\Omega(n)$ time, and each query takes $\Omega(1)$. The standard solution meets both.
- **Space.** In the standard solution, the suffix array, its inverse and the LCP array take $3n$ words. Compressed indexes trade query time for space.

## Reductions

- **To range minimum.** By the [LCP-RMQ reduction](/lcp-rmq-reduction/), an LCE query is one inverse lookup and one range minimum query on the LCP array.
- **To lowest common ancestor.** In the suffix tree, $\mathrm{LCE}(p, q)$ is the string depth of the lowest common ancestor of the leaves of $T[p \ldots]$ and $T[q \ldots]$.
- **To suffix comparison.** $T[p \ldots] < T[q \ldots]$ if and only if, with $\ell = \mathrm{LCE}(p, q)$, either $p + \ell = n$ and $q + \ell < n$, or both are less than $n$ and $T[p + \ell] < T[q + \ell]$. So LCE gives $O(1)$ suffix comparison.

## Applications

- **Matching with $k$ mismatches.** The kangaroo method above, $O(nk)$ time (Gusfield, Section 9.4).
- **Matching with $k$ differences.** The method of Landau and Vishkin extends each diagonal of the edit distance table with one LCE query, for $O(nk)$ time.
- **Palindromes.** All maximal palindromes in $O(n)$ time (Gusfield, Section 9.2).
- **Tandem repeats and runs.** Algorithms that find all squares and all maximal repetitions extend each candidate to the left and to the right with LCE queries.
- **Wild cards.** Matching with wild cards in the pattern jumps over each wild card, as in the kangaroo method.
- **Sparse suffix sorting and suffix comparison.** Sorting a chosen set of suffixes by comparing them with LCE queries.

## References
