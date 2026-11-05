---
tag: 6RWY4Y
kind: data-structure
slug: lcp-array
name: LCP array
aliases:
- longest common prefix array
- longest-common-prefix array
area: strings/suffix-structures
level: core
summary: For each adjacent pair in the suffix array, the length of their longest common prefix.
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix-array, suffix]
see_also: [kasai-algorithm, lcp-array-construction, lcp-rmq-reduction, longest-common-extension-query, lcp-interval-tree, enhanced-suffix-array, longest-repeated-substring, count-distinct-substrings]
sources:
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948, the Lcp information and its use in the O(m + log n) search
  - paper: doi:10.1007/3-540-48194-X_17
    title: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, CPM 2001, LNCS 2089
    locator: pages 181 to 192, the linear-time construction and the lemma on consecutive text positions
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press, 2015
    locator: Chapter 8 (Classical indexes), suffix arrays and the LCP array
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, Cambridge University Press, 2016
    locator: Chapter 11 (Texts), the compressed representation of the LCP array by the PLCP bit vector
---

The LCP array of a text $T$ of length $n$ is the array $LCP[0 \ldots n-1]$ in which $LCP[i]$ is the length of the longest common prefix of the two [suffixes](/suffix/) that are adjacent at ranks $i-1$ and $i$ of the [suffix array](/suffix-array/), and $LCP[0] = 0$. Together with the suffix array, it holds the full shape of the [suffix tree](/suffix-tree/): the LCP of any two suffixes is a range minimum of it, and its maximum is the length of the [longest repeated substring](/longest-repeated-substring/). It takes $n$ integers and is built in $\Theta(n)$ time from the text and the suffix array by [Kasai's algorithm](/kasai-algorithm/).

## In plain words

Write all endings of a word in sorted order, one under the other, like the words of a dictionary. Neighbors in this list often start with the same letters. For each line, count how many first letters it shares with the line above it. That list of counts is the LCP array.

The counts tell a lot about the text. A large count means that some piece of text occurs twice. The largest count is the length of the longest piece that repeats. Two lines that are far apart in the list share as many first letters as the smallest count between them, because the list is sorted. So with one quick "smallest number in this stretch" lookup, you can compare any two endings of the text.

## The abstract type

The LCP array is a static array of integers, so its basic operation is `get(i)`. It is used with the suffix array as part of a [full-text index](/full-text-index/), and it adds these operations on the suffixes of $T$:

- `lcp_ranks(i, j)`: the length of the longest common prefix of the suffixes of ranks $i$ and $j$;
- `lce(p, q)`: the length of the longest common prefix of the suffixes that start at text positions $p$ and $q$. This is the [longest common extension query](/longest-common-extension-query/).

Both reduce to a [range minimum query](/range-minimum-query/) on the LCP array, by the [LCP-RMQ reduction](/lcp-rmq-reduction/).

## Representation

The text is $T[0 \ldots n-1]$ over an ordered alphabet; the symbols are only compared. Positions and ranks are 0-based. No sentinel is appended: the suffix array $SA$ lists the $n$ nonempty suffixes $T_p = T[p \ldots n-1]$ in increasing lexicographic order, where a proper prefix sorts before the longer string. $RANK$ is the inverse permutation, $RANK[SA[i]] = i$. For two strings $x$ and $y$, $\mathrm{lcp}(x, y)$ is the largest $h$ with $x[0 \ldots h-1] = y[0 \ldots h-1]$.

**Invariant.** For $n \ge 1$:

- **(L1)** $LCP[0] = 0$.
- **(L2)** $LCP[i] = \mathrm{lcp}(T_{SA[i-1]}, T_{SA[i]})$ for $1 \le i \le n - 1$.

For the queries, a [sparse table](/sparse-table/) $M$ stores $M[k][i] = \min LCP[i \ldots i + 2^k - 1]$ for each $k \ge 0$ and $0 \le i \le n - 2^k$.

Some sources index the array from 1, or store the value of the pair $(i, i+1)$ at index $i$. Others append a sentinel $\$$, which adds the empty suffix at rank 0 and one more entry. These conventions shift the indices, and code that mixes them is a common bug. The *permuted* LCP array $PLCP[p] = LCP[RANK[p]]$ stores the same values in text order.

## Operations

```pseudo id=main
LCP-BUILD(T, SA)                         ▷ n = |T|; makes RANK and LCP[0 .. n − 1]
L1  for i ← 0 to n − 1 do RANK[SA[i]] ← i
L2  h ← 0
L3  for p ← 0 to n − 1 do                ▷ text positions in increasing order
L4      if RANK[p] = 0 then LCP[0] ← 0, h ← 0, continue
L5      q ← SA[RANK[p] − 1]               ▷ the suffix just before T_p in sorted order
L6      while p + h < n and q + h < n and T[p + h] = T[q + h] do h ← h + 1
L7      LCP[RANK[p]] ← h
L8      if h > 0 then h ← h − 1

LCP-RANKS(i, j)                          ▷ 0 ≤ i < j < n
L9  k ← ⌊lg(j − i)⌋
L10 return min(M[k][i + 1], M[k][j − 2^k + 1])

LCE(p, q)                                ▷ 0 ≤ p, q < n
L11 if p = q then return n − p
L12 i ← min(RANK[p], RANK[q]), j ← max(RANK[p], RANK[q])
L13 return LCP-RANKS(i, j)
```

**Build.** Lines L1 to L8 are [Kasai's algorithm](/kasai-algorithm/). It visits the suffixes in text order $T_0, T_1, \ldots$ and compares each one with the suffix just before it in the suffix array. The key fact is that the LCP value drops by at most 1 from $T_p$ to $T_{p+1}$, so line L8 keeps $h - 1$ matched symbols and line L6 starts after them. The [Kasai's algorithm](/kasai-algorithm/) page has the trace and the proof that the loop of line L6 runs fewer than $2n$ times in total. Then the sparse table is filled row by row with $M[k][i] = \min(M[k-1][i], M[k-1][i + 2^{k-1}])$.

**Query by rank.** The suffixes of ranks $i < j$ share a prefix of length $\min LCP[i+1 \ldots j]$ (the [LCP-RMQ reduction](/lcp-rmq-reduction/)). Lines L9 and L10 cover the range $[i+1, j]$ with two ranges of length $2^k$ that may overlap, which is safe for a minimum.

**Query by position.** LCE maps the two text positions to ranks with $RANK$ and calls LCP-RANKS. For $p = q$, the answer is the length of the suffix. A position $p = n$ (the empty suffix) gives 0.

## Example

The text is $T = \texttt{banana}$, $n = 6$.

| $i$ | $SA[i]$ | suffix $T_{SA[i]}$ | $LCP[i]$ |
|---|---|---|---|
| 0 | 5 | a | 0 |
| 1 | 3 | ana | 1 |
| 2 | 1 | anana | 3 |
| 3 | 0 | banana | 0 |
| 4 | 4 | na | 0 |
| 5 | 2 | nana | 2 |

So $LCP = [0, 1, 3, 0, 0, 2]$, $RANK = [3, 2, 5, 1, 4, 0]$ and $PLCP = [0, 3, 2, 1, 0, 0]$. The $PLCP$ values in text order show the property that LCP-BUILD uses: from position $p$ to $p + 1$ the value drops by at most 1 ($3, 2, 1, 0$), and it can rise by any amount ($0$ to $3$).

Read off three facts. The largest value, $LCP[2] = 3$, is the [longest repeated substring](/longest-repeated-substring/) `ana`. The sum of the values is $6$, and $\binom{7}{2} - 6 = 21 - 6 = 15$ is the number of distinct nonempty substrings of `banana` (the [count of distinct substrings](/count-distinct-substrings/)). And $\mathrm{lce}(1, 3) = \mathrm{lcp}(\texttt{anana}, \texttt{ana}) = 3$, which LCE finds as the minimum of $LCP[2 \ldots 2] = 3$, since $RANK[1] = 2$ and $RANK[3] = 1$.

For $T = \texttt{mississippi}$, $SA = [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$ and $LCP = [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]$. The query LCE(1, 4) compares `ississippi` with `issippi`. The ranks are $RANK[1] = 3$ and $RANK[4] = 2$, so it returns $\min LCP[3 \ldots 3] = 4$. LCP-RANKS(0, 3) returns $\min(1, 1, 4) = 1$: `i` and `ississippi` share only `i`.

## Correctness

After LCP-BUILD, (L1) and (L2) hold. The proof rests on one lemma: if $p \ge 1$ and $LCP[RANK[p-1]] = h > 0$, then $LCP[RANK[p]] \ge h - 1$. The suffix before $T_{p-1}$ in sorted order shares $h$ symbols with it; drop the first symbol of both, and you get a suffix that is smaller than $T_p$ and shares $h - 1$ symbols with it, so the suffix just before $T_p$ shares at least $h - 1$. So line L6 can start at $h - 1$ and still find the exact value. The query lines are correct by the LCP-RMQ lemma and by the sparse table invariant. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/), with $n$ and the positions in a word, and a symbol comparison in $O(1)$ time.

| operation | time | extra space |
|---|---|---|
| LCP-BUILD from $T$ and $SA$ | $\Theta(n)$ worst case | $n$ words for $RANK$ |
| sparse table for the queries | $\Theta(n \log n)$ | $\Theta(n \log n)$ words |
| `get(i)` | $O(1)$ | |
| LCP-RANKS, LCE | $O(1)$ | |

**Build.** Lines L1 to L5, L7 and L8 run $O(1)$ times for each $p$. Each successful test of line L6 increases $h$. The value $h$ never exceeds $n$, and it drops by at most 1 in each of the $n$ rounds, so the total number of increases is at most $2n$. With mismatches, line L6 makes fewer than $3n$ symbol comparisons.

**Queries in less space.** The sparse table is the simple choice. A linear-space [range minimum query](/range-minimum-query/) structure, such as that of [Fischer and Heun](/fischer-heun-rmq/), keeps $O(1)$ query time with $O(n)$ preprocessing.

**Space of the array.** The LCP array takes $n$ words. The values are at most $n - 1$, so it fits in $n \lceil \log_2 n \rceil$ bits, but most values are small, and compact codings are common (see Variants).

## Variants

- **PLCP bit vector.** Because $PLCP[p+1] \ge PLCP[p] - 1$, the values $PLCP[p] + p$ never decrease, and they are at most $n$. So the sequence can be stored as a bit vector of at most $2n$ bits, with a 1 at position $PLCP[p] + 2p$ for each $p$. Then $LCP[i] = \mathrm{select}_1(SA[i] + 1) - 2\,SA[i]$, where $\mathrm{select}_1(k)$ is the position of the $k$-th 1, found with a [rank and select](/rank-select-dictionary/) structure. This is the LCP part of a [compressed suffix tree](/compressed-suffix-tree/).
- **Byte array with an exception list.** Store values below 255 in one byte, and the rare larger values in a separate sorted list. On DNA and natural-language text most values are small.
- **The LCP array with a sentinel.** With $T\$$ there are $n + 1$ suffixes, the empty suffix comes first, and the array has $n + 1$ entries. The values for the nonempty suffixes are the same.
- **Pairs of arbitrary suffixes.** With the sparse table, the structure answers `lcp_ranks` and `lce` in $O(1)$. This is the basis of the [enhanced suffix array](/enhanced-suffix-array/) and of the [LCP interval tree](/lcp-interval-tree/).

Other ways to build it, such as the $\Phi$ method and the construction from the [Burrows-Wheeler transform](/burrows-wheeler-transform/), are on the [LCP array construction](/lcp-array-construction/) page.

## When to use it

Build the LCP array whenever you have a suffix array and need more than pattern search. Many classic questions on one string become a scan of the LCP array: the longest repeated substring, the number of distinct substrings, the [maximal repeats](/maximal-repeats/), and, with a separator, the [longest common substring](/longest-common-substring/) of two strings. A bottom-up walk of the [suffix tree](/suffix-tree/) can be simulated with the LCP array and a stack, so the pair of arrays replaces a suffix tree in most uses and takes much less memory. If you need only pattern search, the suffix array alone is enough.

## Pitfalls

- **Comparing the wrong neighbor.** $LCP[i]$ belongs to the pair at ranks $i - 1$ and $i$. Code that compares $T_{SA[i]}$ with $T_{SA[i+1]}$ but writes to index $i$ shifts the whole array by one. Line L7 writes to $RANK[p]$, the larger rank of the pair.
- **Resetting $h$ to 0 in each round.** If line L8 sets $h \leftarrow 0$, the result is still correct, but the time becomes $\Theta(n^2)$ on $T = \texttt{a}^n$. The decrement by 1 is what makes it linear.
- **Reading past the end.** Line L6 must test $p + h < n$ and $q + h < n$ before it reads $T$. Without a sentinel, the end of the text is the only stop for a suffix that is a prefix of another, such as `ana` and `anana`.
- **Range off by one.** The LCP of ranks $i < j$ is the minimum of $LCP[i+1 \ldots j]$, not of $LCP[i \ldots j]$. Line L10 starts at $i + 1$.

## Implementations

The Python class takes the text and, if given, its suffix array. Without a suffix array it builds one by sorting with doubled keys. It stores $SA$, $RANK$, $LCP$ and the sparse table, and all loops are iterative.

## History

Manber and Myers introduced the suffix array in 1990, with the journal version in 1993, and they also stored the LCP values of adjacent suffixes and of the pairs that a binary search compares, to search in $O(m + \log n)$ time. Their construction found the LCP values in $O(n \log n)$ time as part of the sort. Kasai, Lee, Arimura, Arikawa and Park gave the simple linear-time construction from the text and the suffix array in 2001, and used the LCP array to simulate the bottom-up walk of a suffix tree.

## References
