---
tag: NP7V4M
kind: algorithm
slug: karp-miller-rosenberg-algorithm
name: Karp-Miller-Rosenberg algorithm
aliases:
- KMR algorithm
area: strings/suffix-structures
level: advanced
summary: Assigns equal integer names to equal substrings of doubling length, giving an O(n log n) suffix sort.
solves: [suffix-array-construction, longest-repeated-substring]
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n log n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 1972
  people: [Richard M. Karp, Raymond E. Miller, Arnold L. Rosenberg]
  note: Presented at STOC 1972 as a method to find repeated patterns in strings, trees and arrays by naming their parts.
prereqs: [radix-sort, counting-sort, suffix-array]
see_also: [prefix-doubling, manber-myers-algorithm, larsson-sadakane-algorithm, substring-equality-queries, longest-repeated-substring, sparse-table, polynomial-rolling-hash, circular-suffix-array]
sources:
  - paper: doi:10.1145/800152.804905
    title: Richard M. Karp, Raymond E. Miller and Arnold L. Rosenberg, Rapid identification of repeated patterns in strings, trees and arrays, STOC 1972
    locator: pages 125 to 136, the naming of substrings of length 2^k from the names of length 2^(k-1) and its use to find repeats
  - url: https://cp-algorithms.com/string/suffix-array.html
    title: cp-algorithms, Suffix Array
    locator: sections Construction (the O(n log n) approach) and Comparing two substrings of a string
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948, the sort of the suffixes in rounds of doubling length
---

The Karp-Miller-Rosenberg (KMR) algorithm gives each substring of length $2^j$ of a text an integer *name*, its rank among the distinct substrings of that length, for $j = 0, 1, 2, \ldots$. The names of length $2^{j+1}$ come from pairs of names of length $2^j$ with one [radix sort](/radix-sort/), so all levels take $\Theta(n \log n)$ time. The table of names, the *dictionary of basic factors*, compares or tests for equality any two substrings of the same length in $O(1)$ time, and the same doubling idea sorts the suffixes, as in [prefix doubling](/prefix-doubling/). It is the oldest of the doubling methods behind [suffix array construction](/suffix-array-construction/).

## In plain words

Give each letter of a text a number, its place in the alphabet. Now look at all pieces of two letters. Each piece is a pair of numbers, the number of its first letter and the number of its second letter. Sort the pairs and give each different pair a new number, so that equal pieces get the same number. Do the same for pieces of four letters, made of two pieces of two letters, then eight, and so on.

After about $\log n$ rounds you know a number for every piece whose length is a power of two. Two pieces of any length can then be compared with two lookups, because a piece is covered by two power-of-two pieces that may overlap. Pieces with the same number are repeats, which is what Karp, Miller and Rosenberg were looking for.

## The problem

**Input.** A text $T = T[0 \ldots n-1]$ over a general ordered alphabet. The symbols are only compared, once, to give them ranks. Positions are 0-based and no sentinel is appended.

**Output.** For each level $j$ with $2^j \le n$, the array $NAME_j[0 \ldots n - 2^j]$, where $NAME_j[i]$ is the rank of the *basic factor* $T[i \ldots i + 2^j - 1]$ among the distinct factors of length $2^j$. So equal factors get equal names, and names compare as the factors do.

From these names the same method answers the classic questions on the text: the [suffix array](/suffix-array/), the comparison of two factors, and the [longest repeated substring](/longest-repeated-substring/).

## The algorithm

```pseudo id=main
KMR(T)                                   ▷ n = |T|; NAME_j[i] for 0 ≤ i ≤ n − 2^j
L1  NAME_0[i] ← rank of T[i] among the distinct symbols of T
L2  j ← 0
L3  while 2^(j+1) ≤ n do
L4      pair[i] ← (NAME_j[i], NAME_j[i + 2^j]) for 0 ≤ i ≤ n − 2^(j+1)
L5      order ← the positions sorted by pair, with a two-pass radix sort
L6      r ← −1; for each position i in order do
L7          if i is the first or pair[i] differs from the pair before then r ← r + 1
L8          NAME_(j+1)[i] ← r
L9      j ← j + 1
L10 return NAME_0, .., NAME_j
```

A factor of length $2^{j+1}$ is the concatenation of two factors of length $2^j$, so its name is fixed by the pair of their names (line L4). Line L5 sorts the pairs with two stable [counting sorts](/counting-sort/), on the second component and then on the first; the names are below $n$, so each pass has $n$ buckets. Lines L6 to L8 give consecutive names to the distinct pairs in sorted order.

**Comparing two factors.** To compare $T[p \ldots p + \ell - 1]$ with $T[q \ldots q + \ell - 1]$, let $k = \lfloor \log_2 \ell \rfloor$. Each factor is covered by its two windows of length $2^k$ at offsets $0$ and $\ell - 2^k$, which overlap. Compare the pairs $(NAME_k[p], NAME_k[p + \ell - 2^k])$ and $(NAME_k[q], NAME_k[q + \ell - 2^k])$. This is the same covering trick as the [sparse table](/sparse-table/) for range minima, and it gives [substring equality queries](/substring-equality-queries/) and lexicographic comparisons in $O(1)$ time.

**Suffix array.** Name the prefixes of length $2^j$ of the suffixes instead of the factors: a suffix shorter than $2^j$ is its own prefix, and a missing second half gets a name smaller than all others. After the round where all names differ, or $2^j \ge n$, the order of the names is the suffix array. This is [prefix doubling](/prefix-doubling/), as in the [Manber-Myers algorithm](/manber-myers-algorithm/), and the same loop on cyclic factors gives the [circular suffix array](/circular-suffix-array/).

**Longest repeat.** A factor that occurs twice has all its prefixes occur twice, so the property "some factor of length $L$ repeats" is monotone in $L$. Build $L$ from the highest power of two down: try $L + 2^j$, name its factors by the pairs (name of length $L$ at $i$, $NAME_j[i + L]$), and keep the step if two names are equal. This gives the longest repeated factor in $O(n \log n)$ time.

## Example

The text is $T = \texttt{abaababa}$, $n = 8$.

| level $j$ | length | factors at $i = 0, 1, \ldots$ | $NAME_j$ |
|---|---|---|---|
| 0 | 1 | a b a a b a b a | 0 1 0 0 1 0 1 0 |
| 1 | 2 | ab ba aa ab ba ab ba | 1 2 0 1 2 1 2 |
| 2 | 4 | abaa baab aaba abab baba | 1 3 0 2 4 |
| 3 | 8 | abaababa | 0 |

At level 2, the factor at $i = 3$ is `abab`, and line L4 forms the pair $(NAME_1[3], NAME_1[5]) = (1, 1)$, the names of `ab` and `ab`. The pairs of level 2 are $(1, 0), (2, 1), (0, 1), (1, 1), (2, 2)$, and their ranks in sorted order are $1, 3, 0, 2, 4$.

**Comparing.** To compare $T[1 \ldots 3] = \texttt{baa}$ with $T[4 \ldots 6] = \texttt{bab}$, take $\ell = 3$ and $k = 1$. The pairs are $(NAME_1[1], NAME_1[2]) = (2, 0)$ and $(NAME_1[4], NAME_1[5]) = (2, 1)$, so `baa` < `bab`. For $T[0 \ldots 2]$ and $T[3 \ldots 5]$ both pairs are $(1, 2)$: both factors are `aba`.

**Longest repeat.** At level 3 there is only one factor. At level 2 all five names differ, so no factor of length 4 repeats. At level 1 the name 1 repeats, so $L = 2$. Then $L + 1 = 3$: the names of the factors of length 3 are the pairs $(NAME_1[i], NAME_0[i + 2])$, and `aba` occurs at 0, 3 and 5. So the longest repeat is `aba`, of length 3.

The suffix array of `abaababa` is $[7, 2, 5, 0, 3, 6, 1, 4]$.

## Correctness

The invariant is that $NAME_j[i]$ is the number of distinct factors of length $2^j$ that are smaller than the factor at $i$. It holds for $j = 0$ by line L1. A factor of length $2^{j+1}$ compares with another of the same length as the pair of its halves, so the pairs of line L4 compare as the factors. The radix sort orders them, and lines L6 to L8 count the distinct pairs before each one, which is the invariant for $j + 1$. For the comparison of two factors of length $\ell$, the two windows of length $2^k$ cover the factor and overlap, so if the first windows are equal, the first difference lies in the second windows. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| quantity | value |
|---|---|
| time, all levels | $\Theta(n \log n)$ |
| space, all levels | $\Theta(n \log n)$ words |
| space, last level only | $\Theta(n)$ words |
| compare or test two factors | $O(1)$ |
| suffix array | $O(n \log n)$ |
| longest repeat | $O(n \log n)$ |

Each of the $\lfloor \log_2 n \rfloor$ rounds takes $O(n)$ time: line L4 is one pass, line L5 is two counting sorts with $n$ buckets, and lines L6 to L8 are one pass. The initial ranks of the symbols cost $O(n \log n)$ comparisons for a general ordered alphabet and $O(n)$ for integers in a range of size $O(n)$. The cost is the same on every input, since the number of rounds depends only on $n$. The implementation of the longest repeat uses library sorts and hashing for the trial lengths, which adds a factor of $\log n$ in the worst case.

## Properties

- **Not comparison based after line L1.** The rounds use only counting sorts on integer names.
- **Deterministic and exact.** Names never collide, unlike the fingerprints of [Rabin and Karp](/rabin-karp/), which find the same repeats faster in expectation but can err.
- **Order preserving.** The names are ranks, so they give the lexicographic order and not only equality. Names given by a hash table, as in some versions, give only equality.
- **Not recursive.** The levels are computed one after the other in a loop.

## Variants and improvements

- **Prefix doubling for suffixes.** The [Manber-Myers algorithm](/manber-myers-algorithm/) and the version on cyclic shifts sort the suffixes in $O(n \log n)$ time with one array of names, so $\Theta(n)$ space.
- **Skipping finished groups.** The [Larsson-Sadakane algorithm](/larsson-sadakane-algorithm/) refines only the groups of suffixes that still have equal names and runs in $O(n \log n)$ time with a much smaller constant on real data.
- **Linear time.** The [DC3 algorithm](/dc3-skew-algorithm/) and [SA-IS](/sa-is/) sort suffixes in $O(n)$ time; the naming of triples in DC3 is a KMR step on a sample of positions.
- **Arbitrary lengths.** The factors of any one length $\ell$ get names in $O(n \log \ell)$ time by combining the levels of the binary representation of $\ell$; this is how KMR finds the repeats of a given length.
- **Trees and arrays.** The original paper names paths in trees and subarrays of two-dimensional arrays in the same way.

## When to use it

Use the dictionary of basic factors when an algorithm must compare many pairs of substrings, in order and not only for equality, and $O(n \log n)$ words of memory are acceptable. It is simpler than a [suffix array](/suffix-array/) with an LCP range-minimum structure and gives exact answers, unlike hashing. For a suffix array alone, use a prefix-doubling or a linear construction, which need only $O(n)$ words.

## Pitfalls

- **Levels beyond the text.** Level $j$ has $n - 2^j + 1$ names. Code that reads $NAME_j[i + 2^j]$ for $i > n - 2^{j+1}$ reads past the end; for factors there is no padding, and for suffixes the missing half needs the smallest name.
- **Sorting with comparisons.** Sorting the pairs with a comparison sort makes each round $O(n \log n)$ and the total $O(n \log^2 n)$. The two counting sorts keep each round linear.
- **Equal names, not equal positions.** Two factors with the same name are equal strings, even when they overlap, as `aba` at positions 3 and 5 above.
- **Memory.** All levels together take $n \log_2 n$ words, which for $n = 10^8$ is several gigabytes. Keep only the levels that the queries need.

## Implementations

The Python function `kmr` returns the list of levels, with an explicit two-pass radix sort. The module also has `substring_compare`, `suffix_array` and `longest_repeat`, all iterative.

## History

Karp, Miller and Rosenberg presented the naming method at STOC in 1972, to find repeated patterns in strings, trees and arrays. The same doubling idea is the basis of the suffix array construction of Manber and Myers (1990, journal version 1993) and of the faster suffix sort of Larsson and Sadakane. Crochemore and Rytter later named the table of names the dictionary of basic factors and used it as a general tool in text algorithms.

## References
