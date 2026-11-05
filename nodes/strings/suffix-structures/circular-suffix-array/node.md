---
tag: DE34MK
kind: data-structure
slug: circular-suffix-array
name: Circular suffix array
aliases:
- sorted rotations array
- cyclic suffix array
area: strings/suffix-structures
level: core
summary: Sorted array of the cyclic rotations of a string, used by the Burrows-Wheeler transform.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix-array, counting-sort, lexicographic-order]
see_also: [burrows-wheeler-transform, suffix-array, prefix-doubling, minimal-rotation, booth-algorithm, fm-index, lyndon-word, sentinel-character]
sources:
  - url: https://cp-algorithms.com/string/suffix-array.html
    title: cp-algorithms, Suffix Array
    locator: sections Construction (the O(n log n) approach on cyclic shifts) and Finding the smallest cyclic shift
  - paper: Michael Burrows and David J. Wheeler, A block-sorting lossless data compression algorithm, Digital Systems Research Center, Research Report 124, 1994
    locator: the sort of the n rotations of the block and the output of the last column with the index of the original string
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press, 2015
    locator: Chapter 9 (Burrows-Wheeler indexes), the Burrows-Wheeler transform as the last column of the sorted rotations
---

The circular suffix array of a string $T$ of length $n$ is the array $CA[0 \ldots n-1]$ of the start positions of the $n$ cyclic rotations of $T$, listed in increasing lexicographic order of the rotations. Its last column is the [Burrows-Wheeler transform](/burrows-wheeler-transform/), and its first entry is the [least rotation](/minimal-rotation/) of $T$. It is built in $O(n \log n)$ time by [prefix doubling](/prefix-doubling/) with two [counting sorts](/counting-sort/) per round. When $T$ ends with a unique smallest [sentinel](/sentinel-character/), it is equal to the [suffix array](/suffix-array/).

## In plain words

Write a word on a ring, so that its end joins its start. You can read it starting at any letter and go once around the ring. Each starting point gives a rotation of the word. For "banana" the rotations are "banana", "ananab", "nanaba", and so on.

Sort the rotations as in a dictionary and keep, for each one, the letter where it starts. That list of start points is the circular suffix array. The last letters of the sorted rotations form the Burrows-Wheeler transform, the first step of the bzip2 compressor. The first line is the rotation that comes first in the dictionary.

To sort fast, compare the rotations on their first letter, then on their first 2 letters, then 4, then 8. Each new round reuses the order of the round before.

## The abstract type

The structure is static. It is built once from $T$ and supports these operations:

- `get(r)`: the start position $CA[r]$ of the rotation of rank $r$;
- `rotation(r)`: the rotation of rank $r$;
- `bwt()`: the last column $L[r] = T[(CA[r] - 1) \bmod n]$ and the primary index, the rank of rotation 0;
- `least_rotation()`: the smallest position whose rotation is least;
- `find(P)`: the positions $i$ where the rotation $R_i$ starts with $P$, for $|P| \le n$. These are the occurrences of $P$ in $T$ read on the ring, which include matches that wrap from the end to the start.

## Representation

The text $T = T[0 \ldots n-1]$ is over a general ordered alphabet. The symbols are only compared: the build maps them first to the integer codes $0, \ldots, \sigma - 1$, in their order. Positions and ranks are 0-based, and position arithmetic is modulo $n$. No sentinel is appended. The rotation at $i$ is $R_i = T[i \ldots n-1]\,T[0 \ldots i-1]$; all rotations have length $n$, so no rotation is a proper prefix of another.

**Invariant.** $CA$ is a permutation of $0, \ldots, n-1$, and for $1 \le r < n$, either $R_{CA[r-1]} < R_{CA[r]}$, or $R_{CA[r-1]} = R_{CA[r]}$ and $CA[r-1] < CA[r]$.

Two rotations are equal only when $T$ is a power $w^k$ of a shorter word with $k \ge 2$, as in `abab`. Then the order of the equal rotations is a convention; this page orders them by position.

The build also keeps the class array $cls$: $cls[i]$ is the rank of $R_i$ among the distinct rotations.

## Operations

```pseudo id=main
CYCLIC-SORT(T)                           ▷ n = |T|; returns CA and the classes cls
L1  if n = 0 then return the empty array
L2  cls[i] ← code of T[i]; p ← positions 0 .. n − 1 sorted by cls with a counting sort
L3  ℓ ← 1
L4  while ℓ < n do                       ▷ p is sorted by the cyclic prefixes of length ℓ
L5      pn[r] ← (p[r] − ℓ) mod n for each r   ▷ sorted by the second half
L6      p ← stable counting sort of pn by cls       ▷ now sorted by the first half too
L7      cls′[p[0]] ← 0; cls′[p[r]] ← cls′[p[r − 1]] + [pair of p[r] ≠ pair of p[r − 1]]; cls ← cls′
L8      ℓ ← 2ℓ
L9  CA ← stable counting sort of 0, 1, .., n − 1 by cls   ▷ equal rotations by position
    return CA, cls
```

**Build.** For $\ell \ge 1$, let $R_i^{(\ell)}$ be the first $\ell$ symbols of the infinite word $R_i R_i \cdots$, the *cyclic prefix* of length $\ell$. Each round turns the order of the cyclic prefixes of length $\ell$ into the order of those of length $2\ell$, because $R_i^{(2\ell)} = R_i^{(\ell)} R_{i+\ell}^{(\ell)}$ is a pair of two known classes. Line L5 is the trick that saves one of the two sorts of a radix sort on pairs: if $p$ is sorted by the class of the second half, then shifting each position back by $\ell$ gives a list sorted by the second half of the new pair. Line L6 sorts it stably by the first half. Line L7 gives equal pairs equal classes. After $\lceil \log_2 n \rceil$ rounds, $\ell \ge n$ and the cyclic prefixes are the full rotations. Line L9 fixes the order of equal rotations, which the rounds leave in an arbitrary order.

**BWT.** $L[r] = T[(CA[r] - 1) \bmod n]$, the symbol before the start of the rotation of rank $r$, which is the last symbol of that rotation. The primary index is the rank $r$ with $CA[r] = 0$; it lets the inverse transform start.

**Find.** The rotations that start with $P$ form one interval of ranks, because the array is sorted. Two binary searches find its ends, comparing the first $|P|$ symbols of a rotation with $P$, as in [suffix array search](/suffix-array-search/). The cost is $O(m \log n)$.

**Least rotation.** $CA[0]$. With the tie rule of line L9, it is the smallest position of a least rotation, the answer that [Booth's algorithm](/booth-algorithm/) gives in $O(n)$ time.

## Example

The text is $T = \texttt{banana}$, $n = 6$, with the codes a = 0, b = 1, n = 2. Each row shows the order $p$ and the classes $cls$ after the round, and the cyclic prefixes in the order $p$.

| after | $\ell$ | $p$ | $cls$ by position $0..5$ | cyclic prefixes in order $p$ |
|---|---|---|---|---|
| L2 | 1 | 1, 3, 5, 0, 2, 4 | 1, 0, 2, 0, 2, 0 | a a a b n n |
| round 1 | 2 | 5, 1, 3, 0, 2, 4 | 2, 1, 3, 1, 3, 0 | ab an an ba na na |
| round 2 | 4 | 5, 3, 1, 0, 4, 2 | 3, 2, 5, 1, 4, 0 | aban anab anan bana naba nana |
| round 3 | 8 | 5, 3, 1, 0, 4, 2 | 3, 2, 5, 1, 4, 0 | the full rotations |

In round 2, line L5 shifts $p = [5, 1, 3, 0, 2, 4]$ back by 2 and gives $pn = [3, 5, 1, 4, 0, 2]$, a list sorted by the class of the second half. Line L6 sorts it stably by the first half. Then all six classes differ, and the order no longer changes.

| rank $r$ | $CA[r]$ | rotation | $L[r]$ |
|---|---|---|---|
| 0 | 5 | abanan | n |
| 1 | 3 | anaban | n |
| 2 | 1 | ananab | b |
| 3 | 0 | banana | a |
| 4 | 4 | nabana | a |
| 5 | 2 | nanaba | a |

So $CA = [5, 3, 1, 0, 4, 2]$, the BWT is `nnbaaa` and the primary index is 3. Here $CA$ is equal to the suffix array, but that is not true in general.

**Equal rotations.** For $T = \texttt{abab}$, the rounds give $p = [0, 2, 1, 3]$, then $[0, 2, 3, 1]$, then $[2, 0, 1, 3]$, and the classes stay $[0, 1, 0, 1]$: rotations 0 and 2 are both `abab`. The final sort of line L9 gives $CA = [0, 2, 1, 3]$ with the tie broken by position. The suffix array of `abab` is $[2, 0, 3, 1]$, because the suffix `ab` is a proper prefix of `abab`.

**Rotations and suffixes differ.** For $T = \texttt{baa}$, the suffix array is $[2, 1, 0]$ (`a`, `aa`, `baa`), but the rotations sort as `aab`, `aba`, `baa`, so $CA = [1, 2, 0]$. With a sentinel, $T\$ = \texttt{baa\$}$ has $CA = SA = [3, 2, 1, 0]$.

For $T = \texttt{abracadabra}$, $CA = [10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]$, the BWT is `rdarcaaaabb` with primary index 2, and `find("abra")` returns the positions 0 and 7. The query `find("aa")` returns position 10: the rotation $R_{10}$ is `aabracadabr`, a match that wraps around the end.

## Correctness

The invariant of the loop is: at each test of line L4, $p$ is sorted by the cyclic prefixes of length $\ell$, and $cls[i]$ is the rank of $R_i^{(\ell)}$ among the distinct cyclic prefixes of length $\ell$. Lines L5 and L6 sort by the pair (first half, second half), because a stable sort by the first key of a list sorted by the second key sorts by the pair. Line L7 then gives the classes of length $2\ell$. When $\ell \ge n$, two cyclic prefixes compare as the two rotations, so line L9 gives the order of the invariant. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/), with positions and classes in a word.

| operation | time | extra space |
|---|---|---|
| CYCLIC-SORT | $O(n \log n)$ worst case, after the symbol codes | $\Theta(n)$ words |
| symbol codes | $O(n \log n)$ comparisons for a general ordered alphabet, $O(n)$ for integers in $0 .. n^{O(1)}$ | $O(\sigma)$ |
| `get(r)`, BWT symbol $L[r]$ | $O(1)$ | |
| `find(P)` | $O(m \log n)$ plus the output | |
| `least_rotation()` | $O(1)$ | |

Each round is $O(n)$: two counting sorts with $n$ buckets and one scan. There are $\lceil \log_2 n \rceil$ rounds. The loop can stop early when all classes differ. On random text over $\sigma \ge 2$ symbols, the cyclic prefixes become distinct at a length of about $2 \log_\sigma n$, so $O(\log \log n)$ rounds are enough. For $T = \texttt{a}^n$ all classes stay 0 and all rounds run. The arrays $p$, $pn$, $cls$, the new classes and the counts take $O(n)$ words.

## Variants

- **Suffix array through a sentinel.** Append a symbol $\$$ that is smaller than all others and occurs once. Then $R_i$ of $T\$$ compares as the suffix $T_i\$$, so the circular suffix array of $T\$$ is the suffix array of $T\$$. This is the common way to build a suffix array with the same code.
- **Bijective BWT.** Factor $T$ into [Lyndon words](/lyndon-word/) and sort the rotations of all factors together in the order of infinite periodic words. The result needs no sentinel and no primary index.
- **Linear time.** The circular suffix array of $T$ can be found in $O(n)$ time for an integer alphabet: build the suffix array of $TT$ with a linear [suffix array construction](/suffix-array-construction/) and keep the suffixes that start before $n$, in order. Equal rotations need care.
- **Early stop.** Stop the loop when the largest class is $n - 1$. Only periodic texts run all rounds.
- **Least rotation only.** If only $CA[0]$ is needed, [Booth's algorithm](/booth-algorithm/) or the Lyndon factorization finds it in $O(n)$ time and $O(1)$ extra space.

## When to use it

Use it to compute the [Burrows-Wheeler transform](/burrows-wheeler-transform/) of a block of data, as in a block-sorting compressor, when the input has no sentinel. Use it for problems on a cyclic string, such as the least rotation, the number of distinct rotations, or a pattern search on a ring, as in circular DNA. The prefix-doubling build is short and fast enough for $n$ up to some millions in contest code. For a [suffix array](/suffix-array/) of a large text, use a linear construction such as [SA-IS](/sa-is/).

## Pitfalls

- **Rotations are not suffixes.** Without a sentinel, the circular order and the suffix order differ, as for `baa`. Code that uses the circular array as a suffix array gives wrong searches and a wrong LCP array.
- **Ties of equal rotations.** For a periodic $T$, the rounds leave equal rotations in an order that depends on the earlier rounds, as the `abab` trace shows. Tests that compare with a sort of `(rotation, position)` fail without the final sort of line L9.
- **Negative modulo.** Line L5 needs $(p[r] - \ell) \bmod n$ in $0 .. n-1$. In C and Java, `%` of a negative number is negative; add $n$ first.
- **Stable sort.** Line L6 must be stable, or the order by the second half is lost.
- **The empty text.** $n = 0$ has no rotation, and the BWT has no primary index; line L1 returns at once.

## Implementations

The Python function `cyclic_sort` returns the array and the final classes, with all loops iterative. The class adds the BWT, the least rotation and the rotation search.

## History

Burrows and Wheeler sorted the rotations of a block in their 1994 report on block-sorting compression, the basis of bzip2. Prefix doubling goes back to the naming method of Karp, Miller and Rosenberg in 1972 and to the suffix array construction of Manber and Myers in 1990. The variant on cyclic shifts with two counting sorts per round, of which one is saved by the shift of line L5, is the standard contest version.

## References
