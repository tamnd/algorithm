---
tag: TF963B
kind: algorithm
slug: sa-is
name: SA-IS algorithm
aliases:
- Nong-Zhang-Chan induced sorting
- SA-IS
- induced sorting suffix array
area: strings/suffix-structures
level: advanced
summary: Linear-time suffix array construction by induced sorting of LMS suffixes.
solves: [suffix-array-construction]
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, online: false, comparison: false}
prereqs: [suffix-array, counting-sort]
see_also: [suffix-array-construction, dc3-skew-algorithm, manber-myers-algorithm, prefix-doubling, burrows-wheeler-transform, lcp-array-construction, suffix-tree-from-suffix-array, radix-sort]
sources:
  - paper: doi:10.1109/TC.2010.188
    title: Ge Nong, Sen Zhang and Wai Hong Chan, Two efficient algorithms for linear time suffix array construction, IEEE Transactions on Computers 60(10), 2011
    locator: pages 1471 to 1484; the L and S types, the LMS substrings and suffixes, the induced sorting and the reduction lemma
  - paper: doi:10.1109/DCC.2009.42
    title: Ge Nong, Sen Zhang and Wai Hong Chan, Linear suffix array construction by almost pure induced-sorting, Data Compression Conference 2009
    locator: pages 193 to 202
  - paper: doi:10.1007/3-540-44888-8_15
    title: Pang Ko and Srinivas Aluru, Space efficient linear time construction of suffix arrays, CPM 2003
    locator: the L and S types of suffixes and the induced sorting from the S-type suffixes
  - paper: doi:10.1145/1242471.1242472
    title: Simon J. Puglisi, W. F. Smyth and Andrew H. Turpin, A taxonomy of suffix array construction algorithms, ACM Computing Surveys 39(2), 2007
    locator: the induced copying methods (Itoh and Tanaka, Seward, Ko and Aluru)
---

SA-IS builds the [suffix array](/suffix-array/) of a string over an integer alphabet in $O(n)$ time. It classifies each suffix as smaller (S) or larger (L) than the next one, sorts only the leftmost S-type suffixes (LMS suffixes) by recursion on a string of at most half the length, and then *induces* the order of all the other suffixes from them by two scans with bucket pointers. Nong, Zhang and Chan published it in 2009; it is simple, needs little memory beyond the output, and is among the fastest suffix sorters in practice.

## In plain words

Look at each ending of the text and ask: is it smaller or larger, in dictionary order, than the ending that starts one letter later? Call it S if smaller and L if larger. A few special endings, where an L is followed by an S, are the key ones.

Suppose the key endings are already in the right order. Then the others fall into place almost by themselves. Each ending is one letter followed by a shorter ending. If you walk through the list of sorted endings from the smallest, each ending you meet tells where the ending one letter longer must go in its group. Two such walks, one forward and one backward, place every ending. To sort the key endings, the method renames them with short numbers and solves the same problem again on a text at most half as long.

## The problem

**Input.** A string $S = S[0 \ldots n-1]$, 0-based, over an integer alphabet: $S[i] \in \{0, \ldots, K - 1\}$ with $K = O(n)$, or more generally symbols that can be mapped to such ranks in $O(n)$ time, for example by [radix sort](/radix-sort/) when they are below $n^{O(1)}$. The code maps any sortable symbols to ranks first.

**Output.** The suffix array $SA$ of $S$. Inside, the algorithm works on $T = S\$$, where the [sentinel](/sentinel-character/) $\$$ is the symbol 0, smaller than every other symbol, after the symbols of $S$ are shifted up by one. The suffix array of $T$ is $n$ followed by the suffix array of $S$.

## The algorithm

Write $T_i = T[i \ldots n]$. Define the type of each position:

- $i$ is *S-type* if $T_i < T_{i+1}$, and *L-type* if $T_i > T_{i+1}$; position $n$ (the sentinel) is S-type.
- Then $T[i] < T[i+1]$ makes $i$ S-type, $T[i] > T[i+1]$ makes it L-type, and $T[i] = T[i+1]$ gives $i$ the type of $i + 1$. One right-to-left scan computes all types.
- $i$ is *LMS* (leftmost S) if $i$ is S-type and $i - 1$ is L-type. An *LMS substring* is $T[i \ldots j]$ for consecutive LMS positions $i < j$, and $T[n \ldots n]$ alone.

A *bucket* is the range of $SA$ for the suffixes that start with one symbol. Inside the bucket of $c$, the L-type suffixes come before the S-type ones, because an L-type suffix $c\,c^k d \ldots$ with $d < c$ is smaller than an S-type suffix $c\,c^{k'} e \ldots$ with $e > c$.

```pseudo id=main
SA-IS(T)                                  ▷ T[n] = $ is the unique smallest symbol
L1  compute the types S and L of all positions, right to left
L2  P ← the LMS positions, left to right
L3  SA ← all empty; put each LMS position at the end of its bucket
L4  INDUCE-L: for r ← 0 to n: if j = SA[r] − 1 ≥ 0 is L-type, put j at the head of bucket T[j]
L5  INDUCE-S: for r ← n down to 0: if j = SA[r] − 1 ≥ 0 is S-type, put j at the tail of bucket T[j]
L6  name the LMS substrings in the order in which their positions appear in SA;
    equal neighbors (same symbols and types) get the same name
L7  if some names repeat then order ← SA-IS(the names of P, in text order)
L8  else order ← the LMS positions sorted by name
L9  SA ← all empty; put the LMS positions, in the sorted order, at the ends of their buckets
L10 INDUCE-L; INDUCE-S
L11 return SA
```

Lines L3 to L5 sort the LMS substrings, not yet the LMS suffixes: two LMS positions with equal LMS substrings may end up in either order. Line L6 compares each LMS substring with the previous one in $SA$, symbol by symbol and type by type, and gives a new name when they differ. The reduced string $T'$ of the names, read in text order, ends with the name 0 of the sentinel, which is unique, so it has the same form as $T$. Lines L9 and L10 repeat the induction with the LMS suffixes in their true order, and this time every suffix lands at its final rank.

## Example

Take $S = \texttt{mmiissiissiippii}$, $n = 16$, and $T = S\$$. The types, below each symbol, and the LMS positions:

```
position  0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
T         m m i i s s i i s s i  i  p  p  i  i  $
type      L L S S L L S S L L S  S  L  L  L  L  S
LMS           *       *       *                 *
```

The LMS positions are 2, 6, 10 and 16, with the LMS substrings $\texttt{iissi}$, $\texttt{iissi}$, $\texttt{iippii\$}$ and $\$$. The buckets are $\$$ at rank 0, $\texttt{i}$ at ranks 1 to 8, $\texttt{m}$ at 9 and 10, $\texttt{p}$ at 11 and 12, $\texttt{s}$ at 13 to 16.

| step | $SA[0 \ldots 16]$ |
|---|---|
| L3, LMS at bucket ends | 16 - - - - - 2 6 10 - - - - - - - - |
| L4, induce L | 16 15 14 - - - 2 6 10 1 0 13 12 5 9 4 8 |
| L5, induce S | 16 15 14 10 2 6 11 3 7 1 0 13 12 5 9 4 8 |

The LMS positions appear in the order 16, 10, 2, 6. The names are $\$ \to 0$, $\texttt{iippii\$} \to 1$, and $\texttt{iissi} \to 2$ for both 2 and 6. The reduced string, in text order of the positions 2, 6, 10, 16, is $T' = [2, 2, 1, 0]$, with a repeated name, so line L7 recurses. Its suffix array is $[3, 2, 1, 0]$, which gives the LMS suffixes in the order 16, 10, 6, 2.

| step | $SA[0 \ldots 16]$ |
|---|---|
| L9, sorted LMS at bucket ends | 16 - - - - - 10 6 2 - - - - - - - - |
| L10, induce L | 16 15 14 - - - 10 6 2 1 0 13 12 9 5 8 4 |
| L10, induce S | 16 15 14 10 6 2 11 7 3 1 0 13 12 9 5 8 4 |

Dropping the 16 gives the suffix array of $S$. In the first pass the suffixes 6 ($\texttt{iissiippii\$}$) and 2 ($\texttt{iissiissiippii\$}$) were in the wrong order, since their LMS substrings are equal; the recursion decides that $6 < 2$ because the next LMS substring of 6, $\texttt{iippii\$}$, is smaller than that of 2, $\texttt{iissi}$.

## Correctness

Three facts carry the proof. (1) Inside a bucket, L-type suffixes come before S-type ones, so the head and tail pointers of a bucket fill disjoint parts. (2) If the LMS suffixes are at the ends of their buckets in sorted order, then INDUCE-L places all L-type suffixes in sorted order, and then INDUCE-S places all S-type suffixes in sorted order: every L-type $T_j$ is $T[j]$ followed by the smaller suffix $T_{j+1}$, which the left-to-right scan meets before it needs $T_j$, and suffixes in one bucket are ordered by the suffix one position later. The same argument, with LMS substrings in place of LMS suffixes, shows that lines L3 to L5 sort the LMS substrings. (3) The order of the LMS suffixes is the order of the suffixes of the reduced string $T'$, because each LMS suffix is the sequence of its LMS substrings, and comparing LMS substrings by symbols and types never finds one as a proper prefix of another. The proof file gives the details.

## Complexity

**One level.** The type scan, the bucket counts and each induction scan take $O(n + K)$ time. The naming compares each LMS substring with its neighbor; each symbol of $T$ is in at most two LMS substrings, so the total is $O(n)$.

**Recursion.** No two LMS positions are adjacent, and position 0 is never LMS, so there are at most $\lfloor (n+1)/2 \rfloor$ LMS positions, and the reduced string has at most half the length. Its alphabet is the set of names, of size at most its length. So $T(n) \le T(n/2) + O(n)$, which gives $T(n) = O(n)$, and the recursion depth is at most $\lg n$.

**Space.** Beyond the text and the output, the types take $n + 1$ bits and the bucket pointers $K$ words. Nong, Zhang and Chan keep the reduced string and its suffix array inside the output array, so the working space is close to $n$ words; the code here uses separate lists for clarity, $O(n)$ words.

| resource | bound |
|---|---|
| time | $\Theta(n)$ for an integer alphabet with $K = O(n)$ |
| recursion depth | at most $\lceil \lg n \rceil$ |
| extra space | $n$ bits plus $O(K)$ words, in the in-place version |

## Properties

- **Not comparison-based.** It uses symbols as array indices. Over a general ordered alphabet, sort the symbols first in $O(n \log n)$ time; the $\Omega(n \log n)$ lower bound for that model applies to this step only.
- **Recursive, with shallow depth.** The depth is logarithmic, so a recursive implementation is safe; the scans themselves are loops.
- **Deterministic and exact.** No hashing, no randomness.
- **Sequential scans.** The induction scans read $SA$ in order, with random writes into bucket positions; this is cache-friendly compared with the random reads of doubling methods.

## Variants and improvements

- **SA-DS.** The same paper's other algorithm samples fixed-distance substrings instead of LMS substrings.
- **Ko and Aluru (2003).** The first induced-sorting algorithm in linear time, with L and S types, sorting the smaller of the two type classes recursively.
- **BWT and LCP by induction.** The Burrows-Wheeler transform can be induced directly without storing the whole suffix array (Okanohara and Sadakane), and the LCP array can be computed during the induction (Fischer).
- **Constant workspace.** Later work (Goto, and Li, Li and Huo) reduces the extra space to $O(1)$ words beyond the output for integer alphabets.
- **Parallel and external memory.** Induced sorting has been adapted to external memory (eSAIS) and to parallel machines.
- **libdivsufsort.** A widely used library by Yuta Mori uses a related induced copying method, with a worst case of $O(n \log n)$ but fast in practice.

## When to use it

Use SA-IS to build a suffix array, a [Burrows-Wheeler transform](/burrows-wheeler-transform/), or an FM-index from a large text over bytes or small integers. It is linear in the worst case, short to implement, and fast. For short strings, or for teaching, [prefix doubling](/prefix-doubling/) with a library sort is simpler. When the text has a general ordered alphabet with no cheap ranks, sort the distinct symbols first. [DC3](/dc3-skew-algorithm/) is easier to parallelize and to prove, but slower on one core.

## Pitfalls

- **No unique smallest sentinel.** The proof needs $T[n]$ to be smaller than every other symbol and to occur once; with a sentinel equal to a real symbol, the types and the reduced string are wrong.
- **Comparing LMS substrings without types.** Two LMS substrings with equal symbols but different types are different, and naming them equal can give a wrong order. Compare the pairs (symbol, type) and stop at the next LMS position.
- **Bucket heads and tails mixed up.** INDUCE-L writes at bucket heads moving right, INDUCE-S at bucket tails moving left, and each needs fresh pointers. Reusing the tails left by line L3 for INDUCE-S puts S-type suffixes on top of the LMS entries in the wrong places.
- **Keeping the LMS entries of the first pass in step L9.** The array must be cleared before the sorted LMS positions are placed again, or stale entries from the first induction are induced a second time.
- **Recursing when names are unique.** When all names differ, the order follows from the names directly (line L8); recursing anyway still works, but costs time.

## Implementations

## History

Induced sorting goes back to Itoh and Tanaka (1999) and Seward's work on fast BWT computation, which sort a subset of suffixes and derive the others in one scan. Ko and Aluru (2003) turned the idea into a linear-time algorithm with L and S types, in the same year as DC3 by Kärkkäinen and Sanders and the algorithm of Kim, Sim, Park and Park. Nong, Zhang and Chan introduced LMS substrings and the pure induced-sorting algorithm SA-IS at the Data Compression Conference in 2009, with the journal version in IEEE Transactions on Computers in 2011.

## References
