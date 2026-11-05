---
tag: 0Z6PM0
kind: algorithm
slug: kasai-algorithm
name: Kasai's algorithm
aliases:
- Kasai et al. LCP algorithm
area: strings/suffix-structures
level: core
summary: Computes the LCP array in linear time by reusing the LCP value between consecutive positions.
solves: [lcp-array-construction]
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 2001
  people: [Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa, Kunsoo Park]
  note: Presented at Combinatorial Pattern Matching (CPM) 2001 together with a suffix-tree traversal that uses only the suffix array and the LCP array.
prereqs: [lcp-array, suffix-array]
see_also: [lcp-array-construction, lcp-array, suffix-array-construction, lcp-rmq-reduction, longest-repeated-substring, count-distinct-substrings, suffix-tree-from-suffix-array]
sources:
  - paper: doi:10.1007/3-540-48194-X_17
    title: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, CPM 2001, LNCS 2089
    locator: pages 181 to 192, the algorithm GetHeight and the theorem that it runs in O(n) time
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press, 2015
    locator: Chapter 8 (Classical indexes), the linear-time construction of the LCP array
  - paper: Juha Kärkkäinen, Giovanni Manzini and Simon J. Puglisi, Permuted longest-common-prefix array, CPM 2009, LNCS 5577
    locator: the Phi algorithm and the PLCP array
  - paper: Giovanni Manzini, Two space saving tricks for linear time LCP array computation, SWAT 2004, LNCS 3111
    locator: the space analysis of the algorithm of Kasai and coauthors and the two space-saving variants
---

Kasai's algorithm computes the [LCP array](/lcp-array/) of a text of length $n$ from the text and its [suffix array](/suffix-array/) in $\Theta(n)$ time. It visits the suffixes in text order, not in sorted order, because then the LCP value with the previous suffix in sorted order drops by at most 1 from one suffix to the next. So it never compares again the symbols that it has already matched. The algorithm is ten lines long, uses only equality tests on symbols, and is the standard way to solve [LCP array construction](/lcp-array-construction/).

## In plain words

You have the sorted list of all endings of a text, and you want, for each ending, how many first letters it shares with the ending just above it in the list. Checking each pair from scratch is slow when the text has long repeats.

Kasai's trick is to handle the endings in the order of the text: first the whole text, then the text without its first letter, then without two letters, and so on. Each ending is the previous one with its first letter cut off. If the previous ending shared ten letters with its neighbor above, then this ending shares at least nine letters with its own neighbor above. So the count starts at nine. The count goes up by one for each new match and goes down by at most one in each step, so the total work stays small.

## The problem

The input is a text $T[0 \ldots n-1]$ over an alphabet whose symbols can be tested for equality, and its suffix array $SA$: the $n$ start positions of the nonempty suffixes $T_p = T[p \ldots n-1]$, in increasing lexicographic order, where a proper prefix sorts first. Indices are 0-based and no sentinel is appended. The output is the array $LCP[0 \ldots n-1]$ with $LCP[0] = 0$ and $LCP[i] = \mathrm{lcp}(T_{SA[i-1]}, T_{SA[i]})$ for $1 \le i \le n-1$, where $\mathrm{lcp}(x, y)$ is the length of the longest common prefix of $x$ and $y$.

## The algorithm

```pseudo id=main
KASAI(T, SA)                             ▷ n = |T|; returns LCP[0 .. n − 1]
L1  for i ← 0 to n − 1 do RANK[SA[i]] ← i
L2  h ← 0
L3  for p ← 0 to n − 1 do                ▷ suffixes in text order
L4      if RANK[p] = 0 then LCP[0] ← 0, h ← 0, continue
L5      q ← SA[RANK[p] − 1]               ▷ the suffix just before T_p in sorted order
L6      while p + h < n and q + h < n and T[p + h] = T[q + h] do h ← h + 1
L7      LCP[RANK[p]] ← h
L8      if h > 0 then h ← h − 1
```

Line L1 builds the inverse of the suffix array, so that line L5 finds the sorted neighbor $q$ of the suffix $T_p$. The variable $h$ carries over from one round to the next. At the start of round $p$ it is a lower bound on the answer for $T_p$: the first $h$ symbols of $T_p$ and $T_q$ are known to be equal. Line L6 extends the match from there, and line L7 stores it at the rank of $T_p$. Line L8 prepares the lower bound for $T_{p+1}$.

The suffix of rank 0 has no neighbor before it. Line L4 stores $LCP[0] = 0$ for it. In fact $h$ is already 0 when this round comes, as the proof shows.

## Example

The text is $T = \texttt{mississippi}$, $n = 11$. Its suffix array is $SA = [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$, so $RANK = [4, 3, 10, 8, 2, 9, 7, 1, 6, 5, 0]$. The table gives each round: the value of $h$ at the start, the number of symbol comparisons of line L6 (the matches and the one mismatch, if any), and the value stored.

| $p$ | $T_p$ | $RANK[p]$ | $q$ | $T_q$ | $h$ at start | comparisons | $LCP[RANK[p]]$ |
|---|---|---|---|---|---|---|---|
| 0 | mississippi | 4 | 1 | ississippi | 0 | 1 | 0 |
| 1 | ississippi | 3 | 4 | issippi | 0 | 5 | 4 |
| 2 | ssissippi | 10 | 5 | ssippi | 3 | 1 | 3 |
| 3 | sissippi | 8 | 6 | sippi | 2 | 1 | 2 |
| 4 | issippi | 2 | 7 | ippi | 1 | 1 | 1 |
| 5 | ssippi | 9 | 3 | sissippi | 0 | 2 | 1 |
| 6 | sippi | 7 | 8 | ppi | 0 | 1 | 0 |
| 7 | ippi | 1 | 10 | i | 0 | 1 | 1 |
| 8 | ppi | 6 | 9 | pi | 0 | 2 | 1 |
| 9 | pi | 5 | 0 | mississippi | 0 | 1 | 0 |
| 10 | i | 0 | none | | 0 | 0 | 0 |

The result is $LCP = [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]$. Round 1 finds the match `issi` of length 4. Round 2 then starts at $h = 3$: it knows that `ssi` is shared by $T_2$ and its neighbor, and it needs only one comparison to find the mismatch after it. The rounds 3 and 4 do the same with $h = 2$ and $h = 1$. In total line L6 makes 16 comparisons. In round 7, the match stops because $T_q = \texttt{i}$ ends, not because of a mismatch, so the round makes one comparison and stores 1.

For $T = \texttt{aaaaaaaa}$, round 0 matches 7 symbols, and each later round starts with the right value and makes no comparison at all. The total is 7 comparisons, where the comparison of each sorted pair from scratch would make $0 + 1 + \cdots + 7 = 28$.

## Correctness

The key fact is a lemma on two consecutive text positions. Let $q$ be the sorted neighbor of $T_p$ and $h = \mathrm{lcp}(T_q, T_p) \ge 2$. Then $T_{q+1}$ and $T_{p+1}$ are the same two strings without their equal first symbol, so $T_{q+1} < T_{p+1}$ and they share $h - 1$ symbols. The sorted neighbor of $T_{p+1}$ lies between them in the sorted order, and a string between two strings shares at least their common prefix. So the answer for $T_{p+1}$ is at least $h - 1$.

From this the loop keeps the invariant: at the start of round $p$, the first $h$ symbols of $T_p$ and its neighbor are equal, and all entries for the earlier positions are right. The proof, with the sandwich lemma on sorted strings and the bound on the work, is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/): a position fits in a word, and an equality test of two symbols takes $O(1)$ time.

- **Time.** The value $h$ never exceeds $n$, and line L8 lowers it by 1 at most $n$ times. Each successful test of line L6 raises it by 1, so there are at most $2n$ successful tests, and each round has at most one failed test. The time is $\Theta(n)$ in each case, since lines L1 and L3 always run $n$ times.
- **Space.** The output takes $n$ words and $RANK$ takes $n$ words, in addition to $T$ and $SA$. With 32-bit integers and a byte text, that is $13n$ bytes in all at the peak (Kasai and coauthors report this figure). The variants below lower it.
- **Lower bound.** Each algorithm must write the $n$ entries, so $\Omega(n)$ is a lower bound, and Kasai's algorithm is optimal.

The suffix array itself costs more: $O(n)$ time with an integer alphabet (for example with the [DC3 algorithm](/dc3-skew-algorithm/)), and $O(n \log n)$ time with a comparison-based sort of the symbols. So the LCP array never dominates the cost of a suffix array index.

## Properties

- **Equality tests only.** The algorithm never asks which of two symbols is smaller. It works for any alphabet with an equality test, once the suffix array is known.
- **Random access.** The accesses $T[q + h]$, $SA[RANK[p] - 1]$ and $LCP[RANK[p]]$ jump around in memory. On large texts this costs cache misses, and it is the reason for the $\Phi$ variant.
- **Not online.** It needs the full suffix array before it starts.

## Variants and improvements

- **The $\Phi$ algorithm.** Kärkkäinen, Manzini and Puglisi (2009) store $\Phi[SA[i]] = SA[i-1]$ and compute the permuted array $PLCP[p] = \mathrm{lcp}(T_p, T_{\Phi[p]})$ for $p = 0, 1, \ldots$ with the same reuse of $h$. The scan of $PLCP$ and of $T$ is now sequential, which is faster in practice. A last pass sets $LCP[i] = PLCP[SA[i]]$. The Python file includes this version.
- **Saving space.** Manzini (2004) gave ways to compute the LCP array in less working memory, for example by writing the results over the inverse suffix array.
- **The LCP array from the BWT.** Algorithms that work from the [Burrows-Wheeler transform](/burrows-wheeler-transform/) avoid random access to the text; see [LCP array construction](/lcp-array-construction/).
- **Suffix tree traversal.** The same paper uses the LCP array and a stack to visit the internal nodes of the suffix tree bottom-up; see [suffix tree from suffix array](/suffix-tree-from-suffix-array/) and the [LCP interval tree](/lcp-interval-tree/).

## When to use it

Use Kasai's algorithm whenever you have a suffix array in memory and need its LCP array. It is the simplest correct linear method, and it is fast enough for texts of many millions of symbols. Use the $\Phi$ variant for large texts where cache misses dominate. Use a construction from the BWT or a semi-external method when the text and the arrays do not fit in memory together. If you build the suffix array by [prefix doubling](/prefix-doubling/), you can also get the LCP values as a side product, but in $O(n \log n)$ time.

## Pitfalls

- **Resetting $h$ in each round.** If line L8 is replaced by $h \leftarrow 0$, the output is still right, but the time is $\Theta(n^2)$ on $\texttt{a}^n$. The decrement in line L8 is the whole point.
- **Writing to the wrong index.** The value of round $p$ belongs to the larger rank of the pair, $RANK[p]$ (line L7). Writing it to $RANK[p] - 1$ shifts the array.
- **Missing bounds test.** Without a sentinel, the end of the text stops the match of a suffix that is a prefix of another, as in round 7 of the example. Line L6 must test $p + h < n$ and $q + h < n$ before it reads the symbols.
- **A suffix array of the text with a sentinel.** If $SA$ was built for $T\$$, it has $n + 1$ entries, and the empty suffix is at rank 0. Then line L1 must run over $n + 1$ entries, and the output is one entry longer. Mixing the two conventions gives an array that is shifted by one.

## Implementations

The Python file has the main version, which follows the pseudocode line by line, and the $\Phi$ version. Both take any sequence whose items can be tested for equality.

## History

Manber and Myers (1990, journal version 1993) computed the LCP values of adjacent suffixes while they sorted the suffixes, in $O(n \log n)$ time. Kasai, Lee, Arimura, Arikawa and Park gave the linear algorithm from the finished suffix array at CPM 2001. Their paper also showed how to simulate the bottom-up walk of a suffix tree with the two arrays. Manzini (2004) reduced the working space, and Kärkkäinen, Manzini and Puglisi (2009) gave the faster $\Phi$ formulation.

## References
