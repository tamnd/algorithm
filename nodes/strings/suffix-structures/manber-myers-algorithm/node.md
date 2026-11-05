---
tag: D2EGK8
kind: algorithm
slug: manber-myers-algorithm
name: Manber-Myers algorithm
aliases:
- Manber-Myers suffix array construction
- prefix doubling
- prefix doubling suffix sort
- suffix array by doubling
area: strings/suffix-structures
level: core
summary: Builds the suffix array by prefix doubling in O(n log n) time.
solves: [suffix-array-construction]
model: comparison-model
complexity:
  vars: {n: the length of the text}
  time: {worst: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: true}
prereqs: [suffix-array, prefix-doubling, counting-sort]
see_also: [suffix-array-construction, larsson-sadakane-algorithm, karp-miller-rosenberg-algorithm, sa-is, dc3-skew-algorithm, suffix-array-search, lcp-array]
sources:
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948; the sorting section (the h-stages, the buckets and the move of each suffix i − h to the next free place of its bucket)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.5, Suffix arrays (the doubling construction with sorting of rank pairs)
  - paper: doi:10.1145/1242471.1242472
    title: Simon J. Puglisi, W. F. Smyth and Andrew H. Turpin, A taxonomy of suffix array construction algorithms, ACM Computing Surveys 39(2), 2007
    locator: the section on prefix-doubling algorithms (Manber and Myers, and Larsson and Sadakane)
---

The Manber-Myers algorithm builds the [suffix array](/suffix-array/) of a string of length $n$ in $O(n \log n)$ time by [prefix doubling](/prefix-doubling/). Each round takes the suffixes sorted by their first $h$ symbols and sorts them by their first $2h$ symbols, in $O(n)$ time and without comparing symbols: the suffix $S_{i}$ is moved by the rank of $S_{i+h}$. It was the construction of the paper that introduced suffix arrays, and it works over a general ordered alphabet, where $O(n \log n)$ is optimal.

## In plain words

First sort the endings of the text by their first letter. Endings with the same first letter form a group. Then refine each group to sort by the first two letters, then four, then eight.

The trick is how to refine. The ending that starts at place $i$ is, for its first $2h$ letters, its first $h$ letters followed by the first $h$ letters of the ending at place $i + h$. The order of the second part is already known from the last round. So walk through the endings in their current order. For each ending at place $j$, take the ending at place $j - h$ and put it in the next free seat of its group. Inside each group, the endings then come out in the right order for twice the length. When every group has one ending, the sort is done.

## The problem

The input is a string $S = S[0 \ldots n-1]$ over a general ordered alphabet: symbols are only compared, and only in the first step. Indices are 0-based, and no [sentinel](/sentinel-character/) is appended. The output is the permutation $SA$ with $S_{SA[0]} < \cdots < S_{SA[n-1]}$, where $S_i = S[i \ldots n-1]$. This is [suffix array construction](/suffix-array-construction/).

Write $S_i^{h}$ for the prefix of length $\min(h, n - i)$ of $S_i$. An *$h$-bucket* is a maximal run of ranks $r$ in $SA$ on which $S_{SA[r]}^{h}$ is the same string.

## The algorithm

The array $B[i]$ holds the first rank of the bucket of position $i$, so two positions are in the same bucket if and only if they have the same $B$ value, and $B$ orders the buckets.

```pseudo id=main
MANBER-MYERS(S)
L1  SA ← the positions 0 … n − 1, sorted by S[i]
L2  B[SA[0]] ← 0; for r ← 1 to n − 1: B[SA[r]] ← B[SA[r − 1]] if S[SA[r]] = S[SA[r − 1]], else r
L3  h ← 1
L4  while h < n and B has fewer than n distinct values do
L5      next[x] ← x for each rank x                ▷ the next free slot of the bucket that starts at x
L6      for i ← n − 1 down to n − h do             ▷ S[i + h ..] is empty: first in its bucket
            new[next[B[i]]] ← i; next[B[i]] ← next[B[i]] + 1
L7      for r ← 0 to n − 1 do                      ▷ in the order of S[j + h ..]
            j ← SA[r] − h
            if j ≥ 0 then new[next[B[j]]] ← j; next[B[j]] ← next[B[j]] + 1
L8      SA ← new
L9      B'[SA[0]] ← 0; for r ← 1 to n − 1: with p = SA[r − 1], q = SA[r],
            B'[q] ← B'[p] if B[p] = B[q] and B[p + h] = B[q + h] (−1 past the end), else r
L10     B ← B'; h ← 2h
L11 return SA
```

**Walk-through.** Lines L1 and L2 form the 1-buckets. In a round, each bucket is filled from its first slot. The suffixes $S_i$ with $i + h \ge n$ have an empty second half, so they are placed first (line L6). Only $i = n - h$ can share its bucket with others: a suffix shorter than $h$ is its own $h$-prefix, so its bucket has one member. Line L7 then scans $SA$ in the order of the $h$-prefixes and places $j = SA[r] - h$ in its bucket. So the members of one $h$-bucket arrive in the order of the $h$-prefixes of their second halves, which is their order by $2h$-prefix. Line L9 splits the buckets where the pair (first half, second half) changes. The loop stops when all buckets have one member, or when $h \ge n$.

The paper of Manber and Myers keeps the buckets as bit marks in the array and updates them in place; the version here keeps a second array $B'$ for clarity, with the same $O(n)$ cost per round.

## Example

Take $S = \texttt{mississippi}$, $n = 11$. Bars separate the buckets.

| after | $SA$ | the $h$-prefixes, by bucket | buckets |
|---|---|---|---|
| L2, $h = 1$ | 1 4 7 10 \| 0 \| 8 9 \| 2 3 5 6 | i \| m \| p \| s | 4 |
| round $h = 1$ | 10 \| 7 \| 1 4 \| 0 \| 9 \| 8 \| 3 6 \| 2 5 | i \| ip \| is \| mi \| pi \| pp \| si \| ss | 8 |
| round $h = 2$ | 10 \| 7 \| 1 4 \| 0 \| 9 \| 8 \| 6 \| 3 \| 5 \| 2 | i \| ippi \| issi \| miss \| pi \| ppi \| sipp \| siss \| ssip \| ssis | 10 |
| round $h = 4$ | 10 7 4 1 0 9 8 6 3 5 2 | all 11 different | 11 |

In the round $h = 1$, the $\texttt{i}$-bucket has slots 0 to 3. Line L6 puts $i = 10$ in slot 0, because $S_{10} = \texttt{i}$ has nothing after its first symbol. Line L7 scans the old $SA = [1, 4, 7, 10, 0, 8, 9, 2, 3, 5, 6]$ and places $j = SA[r] - 1$: it places 0 in the $\texttt{m}$-bucket, 3 and 6 in the $\texttt{s}$-bucket (second halves $\texttt{i}$), 9 in the $\texttt{p}$-bucket, then 7 in the $\texttt{i}$-bucket (second half $\texttt{p}$), 8, then 1 and 4 in the $\texttt{i}$-bucket (second half $\texttt{s}$), and 2 and 5 in the $\texttt{s}$-bucket. In the round $h = 4$, positions 1 and 4 (both $\texttt{issi}$) are split by their second halves $S_5^4 = \texttt{ssip}$ and $S_8^4 = \texttt{ppi}$, so 4 comes first. The output is the suffix array $[10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$ after three rounds.

## Correctness

The invariant of the loop is: before the round with value $h$, $SA$ lists the positions in non-decreasing order of $S_i^h$, and $B[i] = B[j]$ if and only if $S_i^h = S_j^h$, with $B$ ordering the buckets. A round places each position in its own $h$-bucket, in the order of the $h$-prefix of $S_{i+h}$ (the empty string first), which by the split $S_i^{2h} = S_i^h \cdot S_{i+h}^h$ is the order of $S_i^{2h}$. Line L9 then gives equal $B'$ exactly to equal $2h$-prefixes. When all buckets are singletons, the order of the prefixes is the order of the suffixes. The full proof is in the proof file.

## Complexity

- **Time.** Line L1 is a comparison sort, $O(n \log n)$ comparisons in the [comparison model](/comparison-model/). Each round of lines L5 to L10 does $O(n)$ integer work, with no symbol comparison. After the round with value $h$, two positions share a bucket only if their $2h$-prefixes are equal, and two different suffixes are different once $2h \ge n$. So there are at most $\lceil \lg n \rceil$ rounds, and the time is $O(n \log n)$ in the worst case.
- **Lower bound and tightness.** Over a general ordered alphabet, each suffix sorting algorithm needs $\Omega(n \log n)$ comparisons, because the suffix array of a string of distinct symbols sorts them. Over an integer alphabet, line L1 becomes a counting sort, and the $\lceil \lg n \rceil$ rounds still cost $\Theta(n \log n)$ on strings such as $\texttt{a}^n$, where the buckets become singletons only when $h \ge n/2$. So the algorithm is $\Theta(n \log n)$ in the worst case and on $\texttt{a}^n$. On random text over $\sigma \ge 2$ letters, the longest repeated substring has length $O(\log n)$ with high probability, so only $O(\log \log n)$ rounds are needed, but line L1 still costs $\Theta(n \log n)$ comparisons on distinct symbols.
- **Space.** The arrays $SA$, $B$, $B'$, $next$ and $new$ take $5n$ integers here. The paper uses fewer arrays, with bit marks for the bucket boundaries in place of $B'$.

## Properties

- **Comparison-based only at the start.** After line L1 the algorithm never reads $S$ again, so it handles any ordered alphabet.
- **Produces the inverse array.** At the end, $B[i] = rank[i]$, the inverse suffix array, which [Kasai's algorithm](/kasai-algorithm/) needs for the [LCP array](/lcp-array/).
- **Not recursive and not online.** Each round needs the whole text.

## Variants and improvements

- **Doubling with sorts of pairs.** Replace lines L5 to L7 by a comparison sort of the pairs $(B[i], B[i+h])$. This is simpler and costs $O(n \log^2 n)$. It is the version in CLRS and in the [suffix array](/suffix-array/) page.
- **Larsson-Sadakane.** Sort only the buckets that are not yet singletons, with ternary-split quicksort, and use the current bucket of $S_{i+h}$, which may be finer than the old one. The worst case is the same, $O(n \log n)$, and it is several times faster in practice. See [Larsson-Sadakane](/larsson-sadakane-algorithm/).
- **Linear time.** For an integer alphabet, [SA-IS](/sa-is/) and [DC3](/dc3-skew-algorithm/) sort the suffixes in $O(n)$ time.
- **Search with the same paper.** Manber and Myers also give the search in $O(m + \log n)$ time with the LCP of the bounds of the binary search. See [suffix array search](/suffix-array-search/).

## When to use it

Use Manber-Myers when the alphabet is large or only comparable, when you want a short program with a guaranteed $O(n \log n)$ bound, or when you need the inverse suffix array as well. For long texts over small integer alphabets, [SA-IS](/sa-is/) or a library such as libdivsufsort is faster by a large factor. For a quick program in a contest, the $O(n \log^2 n)$ version with a library sort is often enough.

## Pitfalls

- **Forgetting the suffix $n - h$.** If line L6 is left out, the position $n - h$, whose second half is empty, is never placed, because line L7 places $j$ only from $SA[r] = j + h < n$. Its slot keeps a stale value and the result is not a permutation.
- **Placing $n - h$ last.** Line L6 must run before line L7. An empty second half is the smallest, so $n - h$ must take the first slot of its bucket. For $\texttt{aa}$, putting it last gives $[0, 1]$ instead of $[1, 0]$.
- **Using the new buckets for the second half.** Line L9 must compare $B[p + h]$ and $B[q + h]$ of the old round. Mixing new and old values while $B'$ is being written splits buckets on half-computed data.
- **Testing $h < n$ only.** The test of line L4 for $n$ distinct buckets is what makes the algorithm fast on most inputs; without it, it does all $\lceil \lg n \rceil$ rounds. Both versions are correct.

## Implementations

## History

Udi Manber and Gene Myers presented suffix arrays and this construction at the first ACM-SIAM Symposium on Discrete Algorithms in 1990, and published the journal version in the SIAM Journal on Computing in 1993. The doubling idea comes from the naming technique of Karp, Miller and Rosenberg (1972). Larsson and Sadakane gave the faster variant in a 1999 report, published in 2007.

## References
