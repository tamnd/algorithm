---
tag: QT4WGM
kind: algorithm
slug: wu-manber-approximate-matching
name: Wu-Manber algorithm
aliases:
- Wu-Manber approximate matching
area: strings/approximate-matching
level: advanced
summary: Bit-parallel approximate matching with k errors, using one bit vector per error level.
solves: [k-differences-problem, approximate-string-matching]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, k: the error bound, w: the word length, σ: the alphabet size}
  time: {worst: "O((k + 1) ⌈m / w⌉ n)", average: "O((k + 1) ⌈m / w⌉ n)"}
  space: {extra: "O((σ + k) ⌈m / w⌉)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1992
  people: [Sun Wu, Udi Manber]
  note: Wu and Manber extended the shift-and method to k errors with one bit vector for each error count, and built the search tool agrep on it.
prereqs: [bitap-algorithm, sellers-algorithm, bit-parallelism]
see_also: [myers-bit-parallel-algorithm, k-differences-problem, nondeterministic-finite-automaton, shift-or, levenshtein-automaton, pigeonhole-filtering, ukkonen-cutoff-algorithm]
sources:
  - paper: doi:10.1145/135239.135244
    title: Sun Wu and Udi Manber, Fast text searching allowing errors, Communications of the ACM 35(10), 1992
    locator: pages 83 to 91 (the k + 1 bit vectors for insertions, deletions and substitutions, and the extensions to classes and wild cards)
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 7.2, Parallelizing non-deterministic automata (the paragraph on Wu and Manber 1992 and its update formula)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 6, Approximate matching (the bit-parallel simulation of the automaton by rows)
---

The Wu-Manber algorithm solves the [k-differences problem](/k-differences-problem/) with [bit-parallelism](/bit-parallelism/): it keeps $k + 1$ bit vectors of length $m$, one for each number of errors, and updates all of them with a few word operations for each text character. Vector $R_e$ marks the pattern prefixes that match a substring ending at the current position with at most $e$ errors, so it is row $e$ of the [nondeterministic automaton](/nondeterministic-finite-automaton/) for approximate matching. For a pattern that fits in a machine word, the time is $O((k + 1) n)$ for a text of length $n$. Wu and Manber published it in 1992 as an extension of the [shift-and method](/bitap-algorithm/), and it is the core of the search tool agrep.

## In plain words

The exact shift method keeps one row of bits, one bit for each pattern letter. A bit says: the pattern up to this letter matches the text that ends here. For each text letter, the program shifts the row by one place and keeps the bits whose pattern letter equals the text letter.

For approximate matching, keep one row for each number of errors: a row for no errors, a row for at most one error, and so on. A bit in the row for one error can become true in four ways: by a matching letter, as before, or by one error added to the row above. The error can replace a letter, skip a text letter, or skip a pattern letter. Each way is a shift or an OR of whole rows.

A match ends here when the last bit of the last row is set.

## The problem

The input is a text $T = T[0 \ldots n-1]$, a pattern $P = P[0 \ldots m-1]$ and an integer $k \ge 0$. Indices are 0-based. The edit model is the Levenshtein distance: unit-cost insertion, deletion and substitution, with no transpositions. The output is the set of end positions $j \in \{0, \ldots, n\}$ such that $d(P, T[h \ldots j)) \le k$ for some $h \le j$, in increasing order, the same output as [Sellers' algorithm](/sellers-algorithm/).

## The algorithm

Let $C[i][j]$ be the Sellers table. After column $j$, bit $i - 1$ of $R_e$, for $1 \le i \le m$, is 1 exactly when $C[i][j] \le e$. Row 0 has $C[0][j] = 0$ and is always active, so it is not stored: a shift by one place brings in a 1 for it. The mask $B[c]$ has bit $i$ set when $P[i] = c$. The operations are on $m$-bit vectors: $\ll$ is a shift toward higher bits, $|$ is OR and $\&$ is AND.

```pseudo id=main
WU-MANBER(P, T, k)                          ▷ |P| = m, |T| = n
L1  for each symbol c, B[c] ← the vector with bit i set when P[i] = c
L2  for e ← 0 to k do R[e] ← the vector with bits 0 to min(e, m) − 1 set
L3  if m = 0 or bit m − 1 of R[k] is set then report 0
L4  for j ← 1 to n do
L5      b ← B[T[j − 1]], old ← R[0], R[0] ← ((R[0] ≪ 1) | 1) & b
L6      for e ← 1 to k do
L7          prev ← old, old ← R[e], R[e] ← (((old ≪ 1) | 1) & b) | (prev ≪ 1) | 1 | prev | (R[e − 1] ≪ 1), cut to m bits
L8      if m = 0 or bit m − 1 of R[k] is set then report j
```

Line L2 sets the column $j = 0$: $C[i][0] = i$, so the prefixes of length 1 to $\min(e, m)$ are within $e$ errors. In line L7, $old$ is $R_e$ of column $j - 1$, $prev$ is $R_{e-1}$ of column $j - 1$, and $R[e-1]$ is already the new vector of column $j$. The four parts of line L7 are:

- $((old \ll 1) \,|\, 1) \,\&\, b$: a matching character, with no new error.
- $(prev \ll 1) \,|\, 1$: a substitution, one step down and right from $e - 1$ errors.
- $prev$: an insertion, a text character that the pattern skips, one step right in the same row.
- $R[e-1] \ll 1$: a deletion, a pattern character that the text skips, one step down in the new column.

## Example

Let $P = \texttt{GATAA}$, $T = \texttt{CAGATAAGAGAA}$ and $k = 1$. The table writes each vector as a string of the bits for the rows $i = 1, \ldots, 5$ from left to right, so the left digit is the bit for the prefix $\texttt{G}$ and the right digit the bit for the whole pattern.

| $j$ | $T[j-1]$ | $R_0$ | $R_1$ | match |
|---|---|---|---|---|
| 0 | | 00000 | 10000 | |
| 1 | C | 00000 | 10000 | |
| 2 | A | 00000 | 11000 | |
| 3 | G | 10000 | 11000 | |
| 4 | A | 01000 | 11100 | |
| 5 | T | 00100 | 11110 | |
| 6 | A | 00010 | 11111 | 6 |
| 7 | A | 00001 | 11011 | 7 |
| 8 | G | 10000 | 11001 | 8 |
| 9 | A | 01000 | 11100 | |
| 10 | G | 10000 | 11100 | |
| 11 | A | 01000 | 11110 | |
| 12 | A | 00000 | 11111 | 12 |

$R_0$ is the exact shift-and run: the single 1 moves right while the text spells $\texttt{GATAA}$, and the last bit at $j = 7$ is the exact occurrence. $R_1$ has its first bit set in every column, because with one error the prefix $\texttt{G}$ matches any single character, or the empty string. At $j = 6$, the last bit of $R_1$ comes from the deletion part: $R_0$ of column 6 has the bit for $\texttt{GATA}$, so $\texttt{GATA}$ with the last $\texttt{A}$ deleted matches. The output is 6, 7, 8 and 12, the last row of Sellers' table at most 1.

## Correctness

The proof shows that the vectors hold exactly the sets $\{i \ge 1 : C[i][j] \le e\}$. From the Sellers recurrence, $C[i][j] \le e$ holds exactly when $P[i-1] = T[j-1]$ and $C[i-1][j-1] \le e$, or when one of $C[i-1][j-1]$, $C[i][j-1]$ and $C[i-1][j]$ is at most $e - 1$. These four conditions are the four parts of line L7, with row 0 always present. An induction over $j$, and inside a column over $e$, gives the claim, and line L8 tests $C[m][j] \le k$. The full proof is below.

## Complexity

- **Time.** Line L7 runs $kn$ times and line L5 runs $n$ times. Each is a constant number of operations on $m$-bit vectors, which take $\lceil m / w \rceil$ word operations each on a [word RAM](/word-ram/) with words of $w$ bits. The time is $O((k + 1) \lceil m / w \rceil\, n)$ in the worst case and on average, and $O((k + 1) n)$ when $m \le w$.
- **Preprocessing.** The masks take $O(\sigma \lceil m / w \rceil + m)$ time for an alphabet of $\sigma$ symbols.
- **Space.** $k + 1$ vectors and $\sigma$ masks, so $O((\sigma + k) \lceil m / w \rceil)$ words. A hash map of masks stores only the symbols of $P$.

## Properties

- **Online.** The text is read once from left to right, and a match is reported when its end is read.
- **Flexible.** Each row is an exact shift-and search, so anything that shift-and handles, such as classes of characters and wild cards, works with errors by the same four extra parts.
- **Ends, not starts.** The algorithm reports where matches end.
- **Independent of the text.** The cost per character does not depend on the text, so there is no bad case and no good case.

## Variants and improvements

- **Shift-or form.** The original paper and agrep use the complemented vectors, with 0 for an active state, as in [shift-or](/shift-or/). This saves the OR with 1 after each shift.
- **Bit-parallel by diagonals.** Baeza-Yates and Navarro packed the automaton by diagonals instead of rows, which removes the dependence of each row on the new value of the row above.
- **Column differences.** [Myers' algorithm](/myers-bit-parallel-algorithm/) packs the differences between adjacent cells of a column, for $O(\lceil m / w \rceil\, n)$ time, independent of $k$.
- **Partition into pieces.** For a long pattern, Wu and Manber cut the pattern into $k + 1$ pieces and searched them exactly, the idea of [pigeonhole filtering](/pigeonhole-filtering/), then checked the candidates.
- **Weights and classes.** The paper also handles patterns with sets of characters, parts that must match exactly, and integer costs for the operations.

## When to use it

Use it for short patterns and small $k$, when the pattern fits in one or two machine words, and when the pattern can be more than a plain string: classes, wild cards or regular expressions. For plain strings and larger $k$, [Myers' algorithm](/myers-bit-parallel-algorithm/) is faster, because its cost does not grow with $k$. For long patterns with few errors, filters are faster on average.

## Pitfalls

- **Old and new rows.** The deletion part uses the new $R_{e-1}$ of the same column, while the substitution and insertion parts use the old one. Mixing them up gives wrong matches. Save the old value before overwriting it, as line L7 does.
- **The initial vectors.** At $j = 0$, $R_e$ has its lowest $\min(e, m)$ bits set, not 0. With 0, matches that start with deletions of pattern characters are lost at the start of the text.
- **The bit for row 0.** The substitution part needs the 1 for the empty prefix, which is always within $e - 1$ errors for $e \ge 1$.
- **Overflow.** Cut the vectors to $m$ bits after each shift, or the bits above $m - 1$ grow without bound in a language with unbounded integers.

## Implementations

## History

Baeza-Yates and Gonnet published the shift-and method for exact matching and for the Hamming distance in 1992. In the same issue of the Communications of the ACM, Wu and Manber extended it to the Levenshtein distance with one vector for each number of errors, and to classes, wild cards and regular expressions. They built the search tool agrep on these ideas. Navarro's survey describes their row-wise scheme as a perfect speedup over a serial simulation of the automaton for short patterns.

## References
