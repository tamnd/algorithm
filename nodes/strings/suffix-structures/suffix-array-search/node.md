---
tag: VMB6DY
kind: algorithm
slug: suffix-array-search
name: Suffix array pattern search
aliases:
- binary search in a suffix array
- binary search on suffix array
area: strings/suffix-structures
level: core
summary: Finds a pattern by binary search over the suffix array, in O(m log n) time, or O(m + log n) with LCP values.
solves: [string-matching]
model: comparison-model
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: O(m + log n), plain: O(m log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: true}
prereqs: [suffix-array, binary-search]
see_also: [suffix-array-construction, lcp-array, enhanced-suffix-array, fm-index, suffix-tree, manber-myers-algorithm, range-minimum-query, string-matching]
sources:
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948; the search section (binary search with the values l and r, and the precomputed Llcp and Rlcp for O(P + log N) time)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 7, the section on suffix arrays (the mlr accelerant and the use of Lcp values for O(n + log m) search)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 6, Context, the section on suffix arrays (rank by binary search over the sorted suffixes)
  - paper: doi:10.1016/S1570-8667(03)00065-0
    title: Mohamed I. Abouelhoda, Stefan Kurtz and Enno Ohlebusch, Replacing suffix trees with enhanced suffix arrays, Journal of Discrete Algorithms 2(1), 2004
    locator: pages 53 to 86; the child table and the search for a pattern in O(m) time for a constant alphabet
---

Suffix array pattern search finds all occurrences of a pattern $P$ of length $m$ in a text $S$ of length $n$ from the [suffix array](/suffix-array/) of $S$. The suffixes that start with $P$ form one contiguous block of the array, and two [binary searches](/binary-search/) find its ends. A plain binary search costs $O(m \log n)$ symbol comparisons; with two arrays of [LCP](/lcp-array/) values precomputed from the text, Manber and Myers bring this to $O(m + \log n)$, so the search reads each pattern symbol about once.

## In plain words

A suffix array lists all endings of a text in dictionary order. All endings that begin with the pattern sit next to each other in this list, as all words that begin with "ca" sit together in a dictionary. To find them, open the list in the middle, compare the pattern with the ending there, and keep the half where the pattern must be. Repeat until one place is left. Do this twice, once for the first ending of the block and once for the place just after the last one. The block between the two places tells how many times the pattern occurs and where.

The slow part is the comparison of the pattern with an ending. A clever version remembers how much of the pattern already matched the endings at both sides, and starts the next comparison from there.

## The problem

**Input.** A text $S = S[0 \ldots n-1]$ over a general ordered alphabet (symbols are only compared, with $=$ and $<$), its suffix array $SA$, and a pattern $P = P[0 \ldots m-1]$ with $m \ge 1$. Indices are 0-based, and ranks run from 0 to $n - 1$. No [sentinel](/sentinel-character/) is appended. For the fast version, the LCP array is also given: $LCP[r]$ is the length of the longest common prefix of the suffixes of ranks $r - 1$ and $r$.

**Output.** The half-open rank interval $[lb, ub)$ of the suffixes that have $P$ as a prefix. Then $occ = ub - lb$, and the occurrences of $P$ are the positions $SA[lb], \ldots, SA[ub - 1]$.

Write $S_i = S[i \ldots n-1]$ and $S_i^m$ for its prefix of length $\min(m, n - i)$. Since $SA$ sorts the suffixes, it also sorts their $m$-prefixes (Lemma 2 of the suffix array proof). So $lb$ is the number of ranks $q$ with $S_{SA[q]}^m < P$, and $ub$ is the number of ranks with $S_{SA[q]}^m \le P$. These are the lower bound and the upper bound of $P$ in a sorted list.

## The algorithm

Add two virtual ranks, $-1$ and $n$, whose suffixes are smaller and larger than every string. The binary search keeps the interval $(lo, hi)$ with the suffix of rank $lo$ below $P$ and the suffix of rank $hi$ not below $P$. It also keeps

- $l$, the length of the longest common prefix of $P$ and the suffix of rank $lo$, and
- $r$, the same for the suffix of rank $hi$.

For each midpoint $mid$ that the search can visit, the values $Llcp[mid] = lcp(lo, mid)$ and $Rlcp[mid] = lcp(mid, hi)$ are computed once, before the searches, where $lcp(a, b)$ is the longest common prefix of the suffixes of ranks $a$ and $b$, and 0 when one of them is virtual. The intervals $(lo, hi)$ of the search do not depend on $P$, so there are at most $n$ midpoints. For $0 \le a < b < n$, $lcp(a, b) = \min(LCP[a+1], \ldots, LCP[b])$, and one bottom-up pass over the tree of intervals computes all the values in $O(n)$ time.

```pseudo id=main
SA-BOUND(S, SA, Llcp, Rlcp, P, strict)    ▷ the lower bound, or the upper bound if strict
L1  lo ← −1; hi ← n
L2  l ← 0; r ← 0
L3  while hi − lo > 1 do
L4      mid ← ⌊(lo + hi) / 2⌋
L5      if l ≥ r then
L6          if Llcp[mid] > l then lo ← mid; continue
L7          if Llcp[mid] < l then hi ← mid; r ← Llcp[mid]; continue
L8          k ← l
        else
L9          if Rlcp[mid] > r then hi ← mid; continue
L10         if Rlcp[mid] < r then lo ← mid; l ← Rlcp[mid]; continue
L11         k ← r
L12     while k < m and SA[mid] + k < n and P[k] = S[SA[mid] + k] do k ← k + 1
L13     right ← strict if k = m, else (SA[mid] + k = n or S[SA[mid] + k] < P[k])
L14     if right then lo ← mid; l ← k
L15     else hi ← mid; r ← k
L16 return hi
```

The search for $P$ is $lb = $ SA-BOUND$(\ldots, P, \text{false})$ and $ub = $ SA-BOUND$(\ldots, P, \text{true})$. With strict set, the suffixes that start with $P$ count as "below", so the search goes past them.

Lines L6, L7, L9 and L10 decide the side without reading the text. Take $l \ge r$. If the suffix at $mid$ agrees with the suffix at $lo$ on more than $l$ symbols, it compares with $P$ as the suffix at $lo$ does, so it is below $P$. If it agrees with the suffix at $lo$ on fewer than $l$ symbols, it differs from $P$ at the position $Llcp[mid]$, where it has a larger symbol than the suffix at $lo$, and so a larger symbol than $P$. Only when $Llcp[mid] = l$ does line L12 read the text, and it starts at position $l$, not at 0. The case $l < r$ is symmetric, with $Rlcp$.

**The plain version.** Without $Llcp$ and $Rlcp$, delete lines L5 to L11 and start line L12 with $k \leftarrow \min(l, r)$. This is the *mlr* heuristic of Manber and Myers. It is correct because the suffixes between $lo$ and $hi$ share their first $\min(l, r)$ symbols with $P$. Its worst case stays at $O(m \log n)$, but it is fast on most texts. Starting at $k = 0$ gives the textbook binary search with full string comparisons.

## Example

Take $S = \texttt{mississippi}$, $n = 11$. Then $SA = [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$ and $LCP = [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]$. The intervals of the search give

| $mid$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $Llcp[mid]$ | 0 | 1 | 0 | 4 | 0 | 0 | 1 | 0 | 0 | 1 | 3 |
| $Rlcp[mid]$ | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |

The search for the lower bound of $P = \texttt{ssi}$:

| $(lo, hi)$ | $l, r$ | $mid$ | suffix at $mid$ | action |
|---|---|---|---|---|
| $(-1, 11)$ | 0, 0 | 5 | pi | compare from 0: $\texttt{p} < \texttt{s}$, go right, $l = 0$ |
| $(5, 11)$ | 0, 0 | 8 | sissippi | compare from 0: match s, then $\texttt{i} < \texttt{s}$, go right, $l = 1$ |
| $(8, 11)$ | 1, 0 | 9 | ssippi | $Llcp[9] = 1 = l$; compare from 1: match s, i, all of $P$, go left, $r = 3$ |

The result is $lb = 9$. The upper bound search takes the same first two steps, goes right at $mid = 9$ because the suffix starts with $P$, and at $(9, 11)$ with $l = 3$ it meets $mid = 10$, the suffix $\texttt{ssissippi}$, with $Llcp[10] = 3 = l$: line L12 reads nothing, since $k = m$ already, and the search goes right. So $ub = 11$, $occ = 2$, and $\texttt{ssi}$ occurs at $SA[9] = 5$ and $SA[10] = 2$.

The lower bound of $P = \texttt{issip}$ shows the shortcut. At $(-1, 11)$, $mid = 5$ ($\texttt{pi}$) is above $P$, so $hi = 5$, $r = 0$. At $(-1, 5)$, $mid = 2$ ($\texttt{issippi}$) matches all 5 symbols, so $hi = 2$, $r = 5$. Now $l = 0 < r = 5$. At $(-1, 2)$, $mid = 0$ has $Rlcp[0] = 1 < 5$, so the suffix $\texttt{i}$ is below $P$ and $l = 1$, with no text read. At $(0, 2)$, $mid = 1$ has $Rlcp[1] = 1 < 5$, so $\texttt{ippi}$ is below $P$ too. The result is $lb = 2$, after 6 symbol comparisons in all.

## Correctness

SA-BOUND keeps three facts at the test of line L3: (1) the suffix at $lo$ has its $m$-prefix below $P$ (at most $P$ if strict), or $lo = -1$; (2) the suffix at $hi$ has its $m$-prefix at least $P$ (above $P$ if strict), or $hi = n$; (3) $l$ and $r$ are the exact LCP lengths of $P$ with these two suffixes. The shortcut lines use only that the suffixes are sorted: for ranks $lo < mid$, the first position where the suffix at $mid$ differs from the suffix at $lo$ has a larger symbol at $mid$, or the suffix at $lo$ ends there. Line L12 is correct because the suffix at $mid$ shares its first $k$ symbols with $P$ when it starts. Since the $m$-prefixes are sorted, the ranks with "below" form a prefix of $0, \ldots, n-1$, and the invariant puts $lo$ and $hi$ on the two sides of its end; when $hi = lo + 1$, $hi$ is that end. The proof file gives the details.

## Complexity

**Iterations.** Each pass of line L3 at least halves $hi - lo$, rounded up, so there are at most $\lceil \lg(n + 1) \rceil$ passes.

**Symbol comparisons.** The value $\max(l, r)$ never decreases: lines L6 and L9 keep $l$ and $r$, lines L7 and L10 lower the smaller of the two only, and line L12 starts at $\max(l, r)$ and stores its end into $l$ or $r$. Each successful test $P[k] = S[\ldots]$ in line L12 raises $\max(l, r)$ by one, and $\max(l, r) \le m$, so there are at most $m$ successful tests in all. Each pass adds at most one failed equality test and one order test. So one bound search uses at most $m + 2 \lceil \lg(n + 1) \rceil$ symbol comparisons, and the pair of searches $O(m + \log n)$ time. Reporting adds $O(occ)$.

| version | time of one search | extra space |
|---|---|---|
| full comparisons from 0 | $O(m \log n)$ | none |
| mlr heuristic | $O(m \log n)$ worst, often near $O(m + \log n)$ | none |
| $Llcp$ and $Rlcp$ | $O(m + \log n)$ worst | $2n$ integers, built in $O(n)$ from $LCP$ |

The plain worst case is real: for $S = \texttt{a}^n$ and $P = \texttt{a}^{m-1}\texttt{b}$, each probe at a suffix of length at least $m - 1$ matches $m - 1$ symbols when it starts from 0, and most probes are at such suffixes when $n \ge 2m$.

## Properties

- **Comparison-based.** Only $=$ and $<$ on symbols are used, so the search works over a general ordered alphabet, and the same code works for byte strings, integer arrays or lists of words.
- **Independent of the alphabet size.** Unlike a [suffix tree](/suffix-tree/) with child maps, the cost has no factor of $|\Sigma|$ and no hashing.
- **Static.** The suffix array and the $Llcp$ and $Rlcp$ tables are for one fixed text.
- **Pattern-independent probes.** The intervals visited depend on $P$ only through the left or right choices, which is why $Llcp$ and $Rlcp$ can be precomputed for all of them.

## Variants and improvements

- **One search for both bounds.** Run the lower bound search; while it runs, record the first interval where the suffix at $mid$ starts with $P$, and start the upper bound search from that interval. This saves the common steps.
- **Enhanced suffix array.** Abouelhoda, Kurtz and Ohlebusch add a child table to $SA$ and $LCP$, which lets the search walk the implicit [suffix tree](/suffix-tree/) top-down in $O(m)$ time for a constant alphabet. See the [enhanced suffix array](/enhanced-suffix-array/).
- **Backward search.** The [FM-index](/fm-index/) finds the same interval $[lb, ub)$ by reading $P$ from right to left, with rank queries on the [Burrows-Wheeler transform](/burrows-wheeler-transform/), in $O(m)$ rank queries and compressed space.
- **LCP by range minimum.** Instead of the fixed tables, compute $lcp(lo, mid)$ on demand with a [range minimum query](/range-minimum-query/) over $LCP$. This allows other search orders, for example an exponential search from one end.
- **Prefix table.** Store the interval of each string of length $q$ in a table with $|\Sigma|^q$ entries, and start the binary search inside that interval.

## When to use it

Use it with a suffix array when the text is fixed and the alphabet is large or unknown, or when the memory of a suffix tree is too much: the array takes $n$ words and the plain search no more. For a constant alphabet and short patterns, the plain or mlr search is enough in practice, because $\log n$ is small next to the cache misses of each probe. When memory is very tight, an [FM-index](/fm-index/) gives the same interval from a compressed text. For one pattern and one text without an index, use a linear-time [string matching](/string-matching/) algorithm such as [Knuth-Morris-Pratt](/knuth-morris-pratt/) instead.

## Pitfalls

- **A suffix shorter than the pattern.** When the suffix at $mid$ ends before $P$ does, it is a proper prefix of $P$ and so smaller than $P$. Code that reads $S[SA[mid] + k]$ without the test $SA[mid] + k < n$ reads past the end, or compares with a wrong symbol.
- **One bound, two meanings.** The lower bound is the first suffix whose $m$-prefix is at least $P$; the upper bound is the first one whose $m$-prefix is above $P$. Comparing whole suffixes with $P$ for the upper bound is wrong: $\texttt{ssissippi} > \texttt{ssi}$ as strings, but it starts with $\texttt{ssi}$.
- **The mlr start from max.** Starting line L12 at $\max(l, r)$ without the $Llcp$ and $Rlcp$ tests is wrong: the suffix at $mid$ need not share $\max(l, r)$ symbols with $P$. Only $\min(l, r)$ is safe without the tables.
- **The tables follow one search shape.** $Llcp$ and $Rlcp$ are correct only for the intervals of the exact search of lines L1 and L4. Changing the start interval, or the rounding of $mid$, needs new tables.
- **The empty pattern.** All $n$ suffixes start with the empty string, so the answer is $[0, n)$. The code handles it, but some callers expect "not found".

## Implementations

## History

Manber and Myers introduced the suffix array in 1990 (published in SIAM Journal on Computing in 1993) as a smaller alternative to the suffix tree, and gave the search together with the array: the binary search with the mlr heuristic, and the precomputed Llcp and Rlcp values that give $O(m + \log n)$ time. Gonnet, Baeza-Yates and Snider described the same sorted array of text positions, the PAT array, at about the same time. Abouelhoda, Kurtz and Ohlebusch removed the $\log n$ term for constant alphabets in 2004 with the enhanced suffix array. Textbooks such as Gusfield's present the search with the same two accelerants.

## References
