---
tag: 7JPXK4
kind: algorithm
slug: z-algorithm
name: Z-algorithm
aliases:
- Z-function
- Z-array
area: strings/exact-matching
level: core
summary: Computes the longest common prefix of each suffix with the string; linear-time matching.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [string-matching, border, loop-invariant]
see_also: [prefix-function, knuth-morris-pratt, longest-common-extension-query, boyer-moore, good-suffix-rule, lcp-array]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 1, Exact matching (the values Z_i, Z-boxes, the fundamental preprocessing in linear time, and matching by the Z values of P$T), pages 5-15
  - url: https://cp-algorithms.com/string/z-function.html
    title: CP-Algorithms, Z-function and its calculation
    locator: the definition, the efficient algorithm with the segment [l, r), the proof of linear time, and the search application
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node14.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Boyer-Moore algorithm (the function suffixes, the mirror image of the Z array, used to build the good-suffix table)
---

The Z-algorithm computes, for a string $S$ of length $N$ and every position $k$, the value $Z[k]$: the length of the longest common prefix of $S$ and its suffix $S[k \ldots N-1]$. It runs in $\Theta(N)$ time with at most $2N$ character comparisons, by reusing the rightmost segment that is known to match a prefix. Applied to the pattern, a separator and the text, it solves [string matching](/string-matching/) in $\Theta(n + m)$ time, and its table is the base of many other string algorithms, such as the preprocessing of [Boyer-Moore](/boyer-moore/).

## In plain words

For each place in a word, ask: how many letters, starting here, are the same as the start of the word? That count is the Z value of the place.

Counting from scratch at each place is slow. Instead, remember the piece, already known to copy the start of the word, that reaches farthest to the right. Inside that piece, the letters are a copy of the start, so the answer at a place inside it is already known from an earlier place, at least up to the end of the piece. Only letters beyond its end need new comparisons, and each one pushes the end further right.

To search for a word in a text, glue the word, a mark that is never a letter, and the text. Places in the text whose count equals the length of the word are the matches.

## The problem

The input is a string $S[0 \ldots N-1]$ over a general alphabet: only equality tests between characters are used. Indices are 0-based. The output is the Z array, $Z[k] = \max\{\, \ell : S[0 \ldots \ell-1] = S[k \ldots k+\ell-1] \,\}$ for $1 \le k < N$, and $Z[0] = N$ by convention. (Gusfield leaves $Z_1$ undefined and CP-Algorithms sets $z[0] = 0$; nothing below uses $Z[0]$.)

For [string matching](/string-matching/), the input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$, and the output is every shift $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, all shifts $0, \ldots, n$ are output; if $m > n$, nothing is output.

## The algorithm

The algorithm keeps the segment $S[l \ldots r-1]$, called the Z-box, with $l < k$ and $S[l \ldots r-1] = S[0 \ldots r-l-1]$, whose right end $r$ is the largest found so far. If $k < r$, then $S[k \ldots r-1] = S[k-l \ldots r-l-1]$, so the prefix match at $k$ is the match at $k - l$, cut at $r - k$.

```pseudo id=main
Z-ARRAY(S)
L1  N ← |S|, Z[0] ← N, l ← 0, r ← 0      ▷ return the empty array if N = 0
L2  for k ← 1 to N − 1 do
L3      if k < r then Z[k] ← min(r − k, Z[k − l]) else Z[k] ← 0
L4      while k + Z[k] < N and S[Z[k]] = S[k + Z[k]] do
L5          Z[k] ← Z[k] + 1
L6      if k + Z[k] > r then l ← k, r ← k + Z[k]
L7  return Z

Z-MATCH(T, P)
L8  m ← |P|, n ← |T|
L9  if m = 0 then output 0, 1, …, n and return
L10 Z ← Z-ARRAY(P $ T)                    ▷ $ is a separator not in the alphabet
L11 for s ← 0 to n − m do                 ▷ no iteration when m > n
L12     if Z[m + 1 + s] = m then output s
```

Line L3 copies the known value. Lines L4 and L5 compare new characters. If $Z[k-l] < r - k$, the first comparison of line L4 fails at once, because the character after the match at $k - l$ differs from the next pattern character, and that character also lies inside the box. Line L6 moves the box when the match at $k$ reaches past $r$. In Z-MATCH, no value at a text position can exceed $m$, because the separator matches nothing, so $Z[m+1+s] = m$ means exactly that $T[s \ldots s+m-1] = P$.

## Example

Search for $P$ = aab in $T$ = baabaaab, so $S$ = aab\$baabaaab and $N = 12$. The column "start" is the value set by line L3, and "comparisons" counts the tests of line L4.

| $k$ | $S[k]$ | box $[l, r)$ before | start | comparisons | $Z[k]$ |
|---|---|---|---|---|---|
| 1 | a | [0, 0) | 0 | 2 | 1 |
| 2 | b | [1, 2) | 0 | 1 | 0 |
| 3 | \$ | [1, 2) | 0 | 1 | 0 |
| 4 | b | [1, 2) | 0 | 1 | 0 |
| 5 | a | [1, 2) | 0 | 4 | 3 |
| 6 | a | [5, 8) | 1 | 1 | 1 |
| 7 | b | [5, 8) | 0 | 1 | 0 |
| 8 | a | [5, 8) | 0 | 3 | 2 |
| 9 | a | [8, 10) | 1 | 2 | 3 |
| 10 | a | [9, 12) | 1 | 1 | 1 |
| 11 | b | [9, 12) | 0 | 1 | 0 |

The array is $Z$ = 12 1 0 0 0 3 1 0 2 3 1 0. The value $m = 3$ appears at $k = 5$ and $k = 9$, so the output is $s = 5 - 4 = 1$ and $s = 9 - 4 = 5$. At $k = 6$, line L3 copies $Z[1] = 1$ from inside the box aab, and one failed comparison confirms it. At $k = 9$, the copied value $\min(10 - 9, Z[1]) = 1$ reaches the end of the box, so line L4 goes on comparing past $r$ and finds $Z[9] = 3$. The total is 18 comparisons, within $2N = 24$.

Another array: for $S$ = aabxaabxay, $Z$ = 10 1 0 0 5 1 0 0 1 0. For $S = a^N$, $Z[k] = N - k$.

## Correctness

The loop of line L2 keeps the [loop invariant](/loop-invariant/): $Z[1], \ldots, Z[k-1]$ are correct, and $r$ is the largest value of $j + Z[j]$ over $1 \le j < k$ (or 0), reached at $j = l$, so $S[l \ldots r-1] = S[0 \ldots r-l-1]$. If $k < r$, the copy at line L3 is a lower bound on $Z[k]$, and it is exact when $Z[k-l] < r - k$. Lines L4 and L5 then extend the value to the true one. The full proof is below.

## Complexity

- **Comparisons.** In line L4, each comparison either succeeds or ends the loop. Each iteration of line L2 has at most one failed comparison, so at most $N - 1$ in total. A successful comparison at position $k + Z[k]$ happens only when $k + Z[k] \ge r$: if line L3 copied a value smaller than $r - k$, the first comparison fails, and otherwise the comparisons start at $r$ or after. After the loop, line L6 sets $r$ past every position compared successfully. So each successful comparison moves $r$ by at least 1, and $r \le N$, so there are at most $N$ of them. The total is at most $2N - 1$ comparisons and $O(N)$ time.
- **Matching.** Z-MATCH builds a string of length $n + m + 1$, so it takes $O(n + m)$ time. Each text character is read at least once, so the time is $\Theta(n + m)$ in the best and the worst case.
- **Space.** $\Theta(N)$ for the array; $\Theta(n + m)$ for matching, for $S$ and $Z$.

| claim | value |
|---|---|
| comparisons for Z-ARRAY | at most $2N - 1$ |
| time for matching | $\Theta(n + m)$ |
| extra space for matching | $\Theta(n + m)$, or $\Theta(m)$ with the variant below |

## Properties

- **General alphabet.** Only equality tests are used. The separator must be a symbol that equals no character; in code, a fresh object or an out-of-range integer.
- **Not online.** The value at a position is fixed only after reading the characters that follow it, so an occurrence is found after its last character is read, but the matcher looks ahead and stores the text.
- **Exact LCP values.** Unlike the [prefix function](/prefix-function/), the Z array gives at each position the full length of the match with the pattern, not only whether it is complete. This gives, for free, the longest prefix of $P$ starting at each text position.
- **Equivalent information.** The Z array and the prefix function of a string can each be computed from the other in $O(N)$ time.

## Variants and improvements

- **No concatenation.** Compute $Z$ for $P$ only, then run the same loop over $T$ with a box in $T$ and values copied from the Z array of $P$. This gives, for each text position, the longest prefix of $P$ starting there, with $\Theta(m)$ extra space and at most $2n$ comparisons in the scan. Gusfield calls this computation of the values for $T$ the matching phase.
- **Reverse Z array.** Applied to the reversed strings, it gives at each position the longest common suffix with $P$: the table $N_j$ of Gusfield, or suffixes in Charras and Lecroq, from which the [good-suffix rule](/good-suffix-rule/) of [Boyer-Moore](/boyer-moore/) is built.
- **Circular and approximate matching.** Combining the forward and the reverse values at each text position gives [circular pattern matching](/circular-pattern-matching/) and matching with one mismatch in linear time.
- **Longest common extensions.** The Z array answers [longest common extension](/longest-common-extension-query/) queries in which one of the two positions is 0. For arbitrary pairs, use a [suffix array](/suffix-array/) with an [LCP array](/lcp-array/).

## When to use it

Use the Z-algorithm when you need the length of the match with the pattern at every text position, not just the full occurrences: for example, to combine prefix and suffix matches, or to build Boyer-Moore tables. It is as fast as [KMP](/knuth-morris-pratt/) for plain matching and many people find it easier to write correctly. Use KMP or the [string-matching automaton](/string-matching-automaton/) when the text is a stream that must not be stored.

## Pitfalls

- **No separator.** Without the separator, a value at a text position can exceed $m$, because the match runs from the pattern into the text, and the test `= m` misses occurrences. The test `test_separator_not_matched` searches aa in aaaa.
- **A separator inside the alphabet.** If \$ can occur in the text, it can match the separator. Use a value outside the alphabet, as the implementation does with a fresh object.
- **Copying without the cut.** Line L3 needs $\min(r - k, Z[k-l])$. Copying $Z[k-l]$ alone claims matches beyond $r$ that were never compared; on $S$ = aaa it gives $Z[2] = 2$, past the end of the string, instead of 1. The test `test_z_array_against_definition` checks every value against the definition.
- **The box test.** The condition is $k < r$ with $r$ exclusive. Writing $k \le r$ reads $Z[k - l]$ for a position outside the box.
- **The empty string.** Line L1 must not write $Z[0]$ when $N = 0$.

## Implementations

## History

The Z values and the Z-box method were presented by Gusfield in his 1997 book as the fundamental preprocessing for exact matching, from which he derives the tables of [Boyer-Moore](/boyer-moore/) and of [Knuth-Morris-Pratt](/knuth-morris-pratt/). The same table appears in other texts under other names, such as the prefix table or the function suffixes of Charras and Lecroq computed on the reversed pattern. In competitive programming it is known as the Z-function.

## References
