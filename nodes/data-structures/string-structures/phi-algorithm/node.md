---
tag: 46X4G6
kind: algorithm
slug: phi-algorithm
name: PHI algorithm
aliases:
- Kärkkäinen-Manzini-Puglisi algorithm
area: data-structures/string-structures
level: research
summary: Compute the LCP array in linear time using the predecessor array without the inverse suffix array.
solves: [lcp-array-construction]
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 2009
  people: [Juha Kärkkäinen, Giovanni Manzini, Simon J. Puglisi]
  note: Kärkkäinen, Manzini and Puglisi computed the permuted LCP array in text order through the predecessor array Φ, and derived space-saving variants from it.
prereqs: [suffix-array, lcp-array, kasai-algorithm]
see_also: [kasai-algorithm, lcp-array, lcp-array-construction, suffix-array, locality-of-reference, succinct-data-structures, suffix-tree-from-suffix-array, enhanced-suffix-array]
sources:
  - paper: Juha Kärkkäinen, Giovanni Manzini and Simon J. Puglisi, Permuted longest-common-prefix array, Combinatorial Pattern Matching (CPM 2009), LNCS 5577, doi:10.1007/978-3-642-02441-2_17
    locator: pages 181 to 192, the arrays Φ and PLCP, the linear algorithm in text order, irreducible lcp values, and the sparse variant
  - paper: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, Combinatorial Pattern Matching (CPM 2001), LNCS 2089, doi:10.1007/3-540-48194-X_17
    locator: pages 181 to 192, the lemma that the lcp of a suffix with its predecessor drops by at most one from one text position to the next, and the linear algorithm with the inverse suffix array
  - paper: Giovanni Manzini, Two space saving tricks for linear time LCP array computation, Scandinavian Workshop on Algorithm Theory (SWAT 2004), LNCS 3111, doi:10.1007/978-3-540-27810-8_32
    locator: pages 372 to 383, reducing the working space of Kasai's algorithm by reusing arrays
---

The PHI algorithm computes the [LCP array](/lcp-array/) of a text from its [suffix array](/suffix-array/) in linear time. It is a reorganization of [Kasai's algorithm](/kasai-algorithm/): instead of the inverse suffix array, it uses the array $\Phi$, which gives for each suffix the suffix just before it in sorted order, and first computes the *permuted* LCP array $PLCP$, indexed by text position rather than by rank. Kärkkäinen, Manzini and Puglisi (2009) showed that this order of work has better memory locality, needs one working array that is first $\Phi$ and then $PLCP$, and leads to compact and sparse variants. This page covers $\Phi$, $PLCP$ and these variants; the page of Kasai's algorithm covers the original.

## In plain words

The LCP array says, for each suffix in sorted order, how many letters it shares with the suffix just before it. Computing each value from scratch can take quadratic time.

The trick, already in Kasai's algorithm, is to go through the suffixes in text order: the suffix at position $i + 1$ is the one at $i$ without its first letter. If the suffix at $i$ shares $h$ letters with its sorted predecessor, the suffix at $i + 1$ shares at least $h - 1$ with its own. So each comparison starts where the last one almost ended.

The PHI algorithm stores, for each text position, the position of the sorted predecessor. It fills a table of answers by text position, and only at the end puts them in sorted order.

## The problem

Given a text $t$ of length $n$ and its suffix array $SA$, compute $LCP[r] = lcp(t[SA[r-1] \ldots], t[SA[r] \ldots])$ for $1 \le r < n$, with $LCP[0] = 0$ ([LCP array construction](/lcp-array-construction/)). Define $\Phi[SA[r]] = SA[r-1]$ for $r \ge 1$ and $\Phi[SA[0]] = -1$, and $PLCP[i] = lcp(t[i \ldots], t[\Phi[i] \ldots])$, with $PLCP[SA[0]] = 0$. Then $LCP[r] = PLCP[SA[r]]$.

## The algorithm

```pseudo id=main
PHI-LCP(t, SA)
L1  for r ← 1 to n − 1: A[SA[r]] ← SA[r − 1];  A[SA[0]] ← −1          ▷ A holds Φ
L2  h ← 0
L3  for i ← 0 to n − 1:                                                ▷ text order
        j ← A[i]; if j = −1 then A[i] ← 0; h ← 0; continue
L4      while i + h < n and j + h < n and t[i + h] = t[j + h]: h ← h + 1
L5      A[i] ← h; h ← max(h − 1, 0)                                     ▷ A[i] now holds PLCP[i]
L6  for r ← 0 to n − 1: LCP[r] ← A[SA[r]]
```

Line L1 fills $\Phi$ by one scan of the suffix array. Lines L2 to L5 compute $PLCP$ in text order, overwriting $\Phi[i]$ by $PLCP[i]$ as soon as it has been used. The key fact is $PLCP[i + 1] \ge PLCP[i] - 1$: if the suffix at $i$ and its predecessor at $\Phi[i]$ share $h \ge 1$ symbols, then the suffixes at $i + 1$ and $\Phi[i] + 1$ share $h - 1$ symbols, and $\Phi[i] + 1$ comes before $i + 1$ in sorted order, so the predecessor of $i + 1$ shares at least as much. Line L6 permutes $PLCP$ into rank order. If only $PLCP$ is needed, line L6 is skipped.

## Example

For $t = $ banana, the suffix array is $[5, 3, 1, 0, 4, 2]$ (a, ana, anana, banana, na, nana).

| i | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| suffix | banana | anana | nana | ana | na | a |
| Φ[i] | 1 | 3 | 4 | 5 | 0 | −1 |
| predecessor | anana | ana | na | a | banana | none |
| h at the start | 0 | 0 | 2 | 1 | 0 | 0 |
| PLCP[i] | 0 | 3 | 2 | 1 | 0 | 0 |

At $i = 1$, anana against ana matches 3 symbols. At $i = 2$, the comparison of nana with na starts with $h = 2$ and stops at once because na ends; at $i = 3$, ana against a starts with $h = 1$ and stops at once. The comparisons made 3 matching steps in total. Line L6 gives

$$LCP = [PLCP[5], PLCP[3], PLCP[1], PLCP[0], PLCP[4], PLCP[2]] = [0, 1, 3, 0, 0, 2].$$

## Correctness

The value of $h$ at the start of iteration $i$ is a lower bound on $PLCP[i]$, and the loop of line L4 extends it to the exact value. The lower bound holds by the key fact $PLCP[i + 1] \ge PLCP[i] - 1$, which follows from the order of the suffixes. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Line L4 increments $h$ at most $2n$ times in total, since $h \le n$ at all times and it decreases by at most 1 per iteration; the other lines are scans. So the time is $\Theta(n)$. The working space is one array of $n$ integers, $A$, besides the text, the suffix array and the output; computing $PLCP$ alone needs nothing else.

**Memory access.** Kasai's algorithm also works in text order, but at each step it looks up the rank of $i$ in the inverse suffix array and then reads $SA$ at a neighboring rank, two random accesses. The PHI algorithm replaces these by one sequential read of $\Phi[i]$ and one random access to the text at $\Phi[i] + h$. Kärkkäinen, Manzini and Puglisi report that this makes the PHI algorithm faster than Kasai's in practice; line L6, the permutation, is a separate scan with random reads.

## Properties

- **Two passes over the suffix array.** Line L1 and line L6 are the only accesses to $SA$, both sequential.
- **PLCP is compressible.** Since $PLCP[i + 1] \ge PLCP[i] - 1$, the values $PLCP[i] + i$ never decrease and are at most $n$, so $PLCP$ can be stored as a bit vector of at most $2n$ bits, writing each increment in unary. Compressed suffix trees use this representation, where $LCP[r]$ is read as $PLCP[SA[r]]$.
- **Not in place.** The output $LCP$ is a second array; the in-place trick only merges $\Phi$ and $PLCP$.

## Variants and improvements

- **Irreducible lcp values.** A value $PLCP[i]$ is *reducible* when $t[i - 1] = t[\Phi[i] - 1]$, and then $PLCP[i] = PLCP[i - 1] - 1$ without any comparison. Computing only the irreducible values by direct comparison gives an algorithm whose worst case is $O(n \log n)$, because the paper shows that the sum of the irreducible values is $O(n \log n)$, but which is fast in practice.
- **Sparse PLCP.** Storing $PLCP$ only at every $q$-th text position, and computing these values with $\Phi$ restricted to them, uses $O(n / q)$ words of working space at the cost of more time; the other values are recovered from the samples when needed.
- **Space tricks for Kasai's algorithm.** Manzini (2004) reduced the space of Kasai's algorithm by reusing the arrays; the PHI algorithm reaches a similar effect with a simpler data flow.
- **Kasai's algorithm.** The original uses the inverse suffix array $ISA$ and computes $LCP[ISA[i]]$ in text order; see the page of [Kasai's algorithm](/kasai-algorithm/).

## When to use it

Use the PHI algorithm when building the LCP array for a large text, where memory locality matters, or when the permuted LCP array, or a compressed form of it, is what you need, as in compressed suffix trees. For small inputs, Kasai's algorithm is equally good and more often shown in textbooks.

## Pitfalls

- **The first suffix.** $SA[0]$ has no predecessor. Give it a sentinel value in $\Phi$ and set $PLCP[SA[0]] = 0$; also reset $h$, since the lower bound does not carry over a position without a predecessor.
- **Off-by-one in the permutation.** $LCP[r]$ compares $SA[r - 1]$ with $SA[r]$, so it is $PLCP[SA[r]]$, not $PLCP[SA[r - 1]]$.
- **Text bounds.** Without an end marker, the comparison of line L4 must stop at the end of the text for both positions.
- **Decreasing $h$ below 0.** After a value of 0, $h$ stays 0, not $-1$.

## Implementations

The Python module fills one list with $\Phi$, overwrites it with $PLCP$ in text order, and permutes it into the LCP array. It works for strings and for lists of integers. The tests replay the example, check the property $PLCP[i + 1] \ge PLCP[i] - 1$, and compare 600 random texts against a direct computation of each LCP value.

## History

Kasai, Lee, Arimura, Arikawa and Park (2001) gave the first linear-time LCP construction from the suffix array, based on the drop-by-at-most-one lemma. Manzini (2004) reduced its space. Kärkkäinen, Manzini and Puglisi (2009) introduced the names $\Phi$ and PLCP for this computation in text order, showed that it is faster in practice, and derived the irreducible and sparse variants.

## References
