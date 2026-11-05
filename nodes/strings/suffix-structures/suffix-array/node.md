---
tag: R5YHHT
kind: data-structure
slug: suffix-array
name: Suffix array
aliases:
- pat array
- suffix array of a string
area: strings/suffix-structures
level: core
summary: The lexicographically sorted list of all starting positions of a string's suffixes.
implements: [full-text-index]
model: comparison-model
complexity:
  vars: {n: the length of the text, m: the length of the pattern, occ: the number of occurrences}
  time: {worst: O(m log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix, lexicographic-order, binary-search]
see_also: [suffix-array-construction, suffix-array-search, lcp-array, suffix-tree, manber-myers-algorithm, sa-is, enhanced-suffix-array, fm-index]
sources:
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948; the definition of Pos, the search in O(P + log N) with the Lcp information, and the sorting by doubling
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.5, Suffix arrays (the definition, the construction by ranks of doubled prefixes, and the LCP array)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 6, Context, the section on suffix arrays (the SuffixArray API, longest repeated substring and keyword in context)
  - paper: doi:10.1145/1242471.1242472
    title: Simon J. Puglisi, W. F. Smyth and Andrew H. Turpin, A taxonomy of suffix array construction algorithms, ACM Computing Surveys 39(2), 2007
    locator: Section 1 (the definition and the history, PAT arrays and suffix arrays)
---

A suffix array of a string $S$ of length $n$ is the list of the start positions of its $n$ nonempty [suffixes](/suffix/), in the [lexicographic order](/lexicographic-order/) of the suffixes. It is a [full-text index](/full-text-index/): all occurrences of a pattern of length $m$ start the suffixes of one contiguous range of the array, and two [binary searches](/binary-search/) find that range with $O(m \log n)$ symbol comparisons. It takes $n$ integers of space, several times less than a [suffix tree](/suffix-tree/), and it can be built in $O(n)$ time for an integer alphabet. With the [LCP array](/lcp-array/) added, it does most of the work of a suffix tree.

## In plain words

Write down every ending of a word: for "banana", these are "banana", "anana", "nana", "ana", "na" and "a". Sort them as a dictionary would: "a", "ana", "anana", "banana", "na", "nana". Do not store the endings themselves. Store only where each one starts in the word. That list of start positions is the suffix array.

Each place where a pattern occurs is the start of an ending that begins with the pattern. In a sorted list, all endings that begin with the same pattern stand next to each other. So you can find all of them by binary search, as you find a word in a dictionary, and the list tells you where each one starts.

## The abstract type

A suffix array implements the static [full-text index](/full-text-index/) of a text $S$: `range(P)` gives the interval of ranks of the suffixes that start with $P$, `count(P)` its size, and `locate(P)` the start positions of the occurrences. The text is fixed after the build.

## Representation

The text is $S = S[0 \ldots n-1]$ over a general ordered alphabet: the algorithms here only compare two symbols. Indices are 0-based. No [sentinel](/sentinel-character/) is appended, so a suffix can be a prefix of another, and then it is the smaller one. Write $S_i = S[i \ldots n-1]$.

- $SA[0 \ldots n-1]$ is a permutation of $\{0, \ldots, n-1\}$.
- $rank[0 \ldots n-1]$, the inverse suffix array, is the inverse permutation. It is optional for search and needed by many construction and LCP algorithms.

**Invariant.** $S_{SA[0]} < S_{SA[1]} < \cdots < S_{SA[n-1]}$, and $rank[SA[r]] = r$ for each $r$.

The order is strict because two different suffixes are different strings. So the suffix array of a string is unique. With a sentinel $\$$ smaller than all symbols, the array of $S\$$ is $n$ followed by the array of $S$, as the page on the [sentinel character](/sentinel-character/) proves.

**The key fact.** For a pattern $P$ of length $m$, the set $\{\, r : P \text{ is a prefix of } S_{SA[r]} \,\}$ is an interval $[lo, hi)$ of ranks. Indeed, write $h(r)$ for the prefix of length $m$ of $S_{SA[r]}$ (shorter if the suffix is shorter). The map $r \mapsto h(r)$ is non-decreasing, because a prefix of the same length cut from sorted strings stays sorted. The ranks with $h(r) = P$ are the ranks where a non-decreasing sequence takes one value, which is an interval.

## Operations

```pseudo id=main
SA-BUILD(S)                              ▷ prefix doubling with a comparison sort
L1  SA ← [0, 1, …, n − 1]
L2  rank[i] ← the rank of S[i] among the distinct symbols of S, for each i
L3  k ← 1; loop
L4      key(i) ← (rank[i], rank[i + k]), with −1 when i + k ≥ n
L5      sort SA by key
L6      give rank[SA[0]] ← 0, and rank[SA[r]] ← rank[SA[r − 1]] + [key(SA[r]) ≠ key(SA[r − 1])]
L7      if rank[SA[n − 1]] = n − 1 then return SA, rank
L8      k ← 2k

SA-BOUND(S, SA, P, strict)               ▷ first r with S[SA[r] .. SA[r] + m − 1] ≥ P, or > P if strict
L9  lo ← 0, hi ← n
L10 while lo < hi do
L11     mid ← lo + ⌊(hi − lo)/2⌋
L12     h ← S[SA[mid] .. min(SA[mid] + m, n) − 1]
L13     if h < P, or strict and h = P then
L14         lo ← mid + 1
L15     else hi ← mid
L16 return lo
```

**Build.** After the round with value $k$, $rank[i]$ is the rank of the prefix of length $2k$ of $S_i$ among all such prefixes, and SA lists the suffixes in the order of these prefixes. The key of line L4 compares the prefix of length $2k$ by its two halves of length $k$, whose ranks the previous round computed. Line L7 stops when all prefixes are different, because then they decide the order of the suffixes. This is the [prefix doubling](/prefix-doubling/) method. With a comparison sort it takes $O(n \log^2 n)$ time; [Manber-Myers](/manber-myers-algorithm/) gets $O(n \log n)$ with bucket sorts, and [SA-IS](/sa-is/) gets $O(n)$.

**Range.** `range(P)` is $[\,$SA-BOUND$(P, \text{false})$, SA-BOUND$(P, \text{true})\,)$. The first search finds the first suffix whose $m$-prefix is at least $P$; the second finds the first whose $m$-prefix is larger than $P$. Between them, the $m$-prefix equals $P$. Then `count(P)` is $hi - lo$ and `locate(P)` reports $SA[lo \ldots hi-1]$. The page [suffix array search](/suffix-array-search/) reduces the cost of the search to $O(m + \log n)$.

## Example

Take $S = \texttt{banana}$, $n = 6$.

| $r$ | $SA[r]$ | suffix $S_{SA[r]}$ | $LCP[r]$ |
|---|---|---|---|
| 0 | 5 | a | 0 |
| 1 | 3 | ana | 1 |
| 2 | 1 | anana | 3 |
| 3 | 0 | banana | 0 |
| 4 | 4 | na | 0 |
| 5 | 2 | nana | 2 |

The inverse array is $rank = [3, 2, 5, 1, 4, 0]$: for example $rank[0] = 3$ because banana has rank 3. The last column is the [LCP array](/lcp-array/), the length of the longest common prefix with the previous row.

**Build by doubling.** Line L2 gives $rank = [1, 0, 2, 0, 2, 0]$ (a = 0, b = 1, n = 2).

| round | keys $(rank[i], rank[i+k])$ for $i = 0, \ldots, 5$ | SA after the sort | new rank |
|---|---|---|---|
| $k = 1$ | (1,0) (0,2) (2,0) (0,2) (2,0) (0,−1) | 5 1 3 0 2 4 | 2 1 3 1 3 0 |
| $k = 2$ | (2,3) (1,1) (3,3) (1,0) (3,−1) (0,−1) | 5 3 1 0 4 2 | 3 2 5 1 4 0 |

After $k = 1$ the ranks sort the prefixes of length 2 (a, an, an, ba, na, na), and the ties $1 = 3$ and $2 = 4$ remain. After $k = 2$ all six ranks are different, so the build stops.

**Search for ana.** SA-BOUND with strict = false finds $lo = 1$: the 3-prefix of row 0 is $\texttt{a} < \texttt{ana}$, and the 3-prefix of row 1 is $\texttt{ana}$. With strict = true it finds $hi = 3$: rows 1 and 2 have the 3-prefix $\texttt{ana}$, and row 3 has $\texttt{ban}$. So $\texttt{ana}$ occurs $3 - 1 = 2$ times, at positions $SA[1] = 3$ and $SA[2] = 1$. For $\texttt{nab}$ both searches return 5, the empty range: $\texttt{na} < \texttt{nab} < \texttt{nan}$.

## Correctness

The build keeps the invariant "after the round with value $k$, $rank$ orders the prefixes of length $2k$ of the suffixes, with equal ranks for equal prefixes", and stops only when all ranks differ, which gives the sorted order of the suffixes. SA-BOUND is a binary search on the non-decreasing sequence $h(r)$ of the key fact, so it returns the first rank where $h(r) \ge P$ (or $> P$), and the ranks in between are exactly those whose suffix starts with $P$. The full proof is in the proof file.

## Complexity

The costs count symbol comparisons and integer operations, in the [comparison model](/comparison-model/) for the symbols.

| operation | cost | case |
|---|---|---|
| build by doubling, comparison sort | $O(n \log^2 n)$ | worst |
| build by [Manber-Myers](/manber-myers-algorithm/) | $O(n \log n)$ | worst |
| build by [SA-IS](/sa-is/) or [DC3](/dc3-skew-algorithm/) | $O(n)$ | worst, integer alphabet |
| range$(P)$, count$(P)$ | $O(m \log n)$ | worst |
| range$(P)$ with LCP information | $O(m + \log n)$ | worst |
| locate$(P)$ | range plus $O(occ)$ | worst |
| space | $n$ integers, plus $n$ for $rank$ | |

**Build.** Each round costs one sort of $n$ keys, $O(n \log n)$ comparisons of integer pairs. After the round with value $k$, two suffixes share a rank only if their prefixes of length $2k$ are equal. Two different suffixes have a common prefix of length at most $n - 1$, so all ranks differ once $2k \ge n$, and there are at most $\lceil \lg n \rceil + 1$ rounds.

**Search.** Each search does $\lceil \lg(n+1) \rceil$ steps, and each step compares at most $m$ symbols. The bound $O(m \log n)$ is reached, for example on $S = \texttt{a}^n$ with $P = \texttt{a}^{m}$.

**Lower bound for the build.** If the symbols of $S$ are pairwise distinct, the suffix array lists the positions in the order of their first symbols, so it sorts the symbols. In the comparison model this needs $\Omega(n \log n)$ comparisons in the worst case, so Manber-Myers is optimal for a general ordered alphabet. Over an integer alphabet $\{0, \ldots, n^{O(1)}\}$, linear time is possible.

**Space.** The array uses $n$ words of $\lceil \lg n \rceil$ binary digits each, against a small constant number of words for each node and edge of a [suffix tree](/suffix-tree/), which has up to $2n$ nodes. The [compressed suffix array](/compressed-suffix-array/) and the [FM-index](/fm-index/) reduce this to about the size of the compressed text.

## Variants

- **With the LCP array.** The [LCP array](/lcp-array/), built in $O(n)$ time by [Kasai's algorithm](/kasai-algorithm/), gives the longest repeated substring, the number of distinct substrings and faster search. With range-minimum structures it becomes the [enhanced suffix array](/enhanced-suffix-array/), which simulates a suffix tree.
- **Sentinel.** Many programs build the array of $S\$$, with $SA[0] = n$. This removes the special case of a suffix that is a prefix of another.
- **Circular suffix array.** Sort the rotations of $S$ instead of its suffixes: the [circular suffix array](/circular-suffix-array/), the order behind the [Burrows-Wheeler transform](/burrows-wheeler-transform/).
- **Sparse suffix array.** Store only the suffixes that start at selected positions, such as word starts, to save space.
- **Compressed suffix array.** Store $SA$ implicitly through the function $\Psi(r) = rank[SA[r] + 1]$ in compressed form: the [compressed suffix array](/compressed-suffix-array/).

## When to use it

Use a suffix array when you need a full-text index of a static text and memory matters: it is a flat integer array, simple to store on disk and fast in cache. Use a [suffix tree](/suffix-tree/) when you need many tree walks, such as [matching statistics](/matching-statistics/), and memory is not a problem. Use the [FM-index](/fm-index/) when the text is large and compressible. For a single search in a text you do not index, a linear-time [string matching](/string-matching/) algorithm such as [Knuth-Morris-Pratt](/knuth-morris-pratt/) is cheaper than any index.

## Pitfalls

- **Comparing full suffixes in a sort.** `sorted(range(n), key=lambda i: S[i:])` is correct but takes $\Theta(n^2)$ space for the keys and $\Theta(n^2 \log n)$ time on $\texttt{a}^n$. Use it only as a test oracle.
- **Comparing the whole suffix in the search.** Line L12 must cut the suffix to length $m$. Comparing $P$ with the whole suffix puts $P$ before every longer suffix that starts with $P$, so the strict search returns the wrong end.
- **The missing sentinel in the doubling key.** Line L4 must give $-1$, a value below every rank, when $i + k \ge n$. Using $0$, the rank of the smallest symbol, makes the key of the last suffix $\texttt{a}$ of $\texttt{a}^n$ equal to the key of each other suffix, all ranks stay equal, and the loop never ends.
- **Refining with the old ranks only.** Line L6 must compare the whole keys of neighbors in the new order. Comparing only the old $rank[i]$ gives back the ranks of the shorter prefixes, nothing is refined, and on $\texttt{a}^n$ the loop never ends.

## Implementations

## History

Manber and Myers introduced suffix arrays in a 1990 conference paper, published in the SIAM Journal on Computing in 1993, with an $O(n \log n)$ construction by doubling and a search in $O(m + \log n)$ time. Gonnet, Baeza-Yates and Snider described the same structure as the PAT array around the same time. In 2003 several groups gave linear-time constructions for integer alphabets, among them the skew algorithm of Kärkkäinen and Sanders. CLRS added a section on suffix arrays in its fourth edition.

## References
