---
tag: F82Z8Y
kind: algorithm
slug: bitap-algorithm
name: Bitap algorithm
aliases:
- shift-or with errors
- shift-add algorithm
- Baeza-Yates-Gonnet algorithm
area: strings/approximate-matching
level: core
summary: Bit-parallel shift-and extension that tracks up to k errors per pattern prefix.
solves: [k-mismatch-problem]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, k: the mismatch bound, B: the field width ⌈log2(k + 1)⌉ + 1, w: the machine word length, σ: the alphabet size}
  time: {worst: Θ(n ⌈m B / w⌉), preprocessing: Θ(σ ⌈m B / w⌉ + m)}
  space: {extra: Θ(σ ⌈m B / w⌉)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1989
  people: [Ricardo Baeza-Yates, Gaston H. Gonnet]
  note: Baeza-Yates and Gonnet introduced the shift-or method and its shift-add form for mismatches at SIGIR 1989, with the journal version in Communications of the ACM in 1992.
prereqs: [k-mismatch-problem, shift-or, bit-parallelism]
see_also: [shift-or, wu-manber-approximate-matching, myers-bit-parallel-algorithm, k-mismatch-problem, hamming-string-matching, amir-lewenstein-porat-algorithm, bit-parallel-regex-matching, word-ram]
sources:
  - paper: doi:10.1145/135239.135243
    title: Ricardo Baeza-Yates and Gaston H. Gonnet, A new approach to text searching, Communications of the ACM 35(10), 1992
    locator: pages 74 to 82 (the shift-or method, and the shift-add method with counters and an overflow bit for mismatches)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 4 (the Shift-And method and its extension to errors in agrep)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 2 (Shift-And and Shift-Or) and Chapter 6 (bit-parallel approximate matching)
  - paper: doi:10.1145/135239.135244
    title: Sun Wu and Udi Manber, Fast text searching allowing errors, Communications of the ACM 35(10), 1992
    locator: pages 83 to 91 (the bit-parallel extension to insertions and deletions)
---

The bitap algorithm finds all positions where a pattern occurs in a text with at most $k$ mismatches, by keeping one small counter for each prefix of the pattern in a single machine word. It is the shift-add method of Baeza-Yates and Gonnet, which extends the exact [Shift-Or](/shift-or/) search: after each text character, one shift and one addition update every counter at once. For a pattern that fits in a word, it solves the [k-mismatch problem](/k-mismatch-problem/) in $O(n)$ time on a text of length $n$, with tiny constants. The [Wu-Manber algorithm](/wu-manber-approximate-matching/) extends the same idea to insertions and deletions.

## In plain words

Slide the pattern along the text and, at each place, count the letters that differ. Counting each place from scratch is slow.

Bitap counts all places at once. Think of a row of small counters, one for each start of the pattern: the first letter, the first two letters, and so on. When a new text letter arrives, each counter moves one step down the row, and each counter adds one if its new pattern letter differs from the text letter. The last counter then holds the number of differences for the full pattern, and a small count means a match.

All counters live side by side in one machine word. A single shift moves them all, and a single addition updates them all. A spare bit in each counter remembers that the count got too large, so the counters never spill into each other.

## The problem

The input is a pattern $P = P[0 \ldots m-1]$, a text $T = T[0 \ldots n-1]$ over an alphabet $\Sigma$, and an integer $k \ge 0$. The edit model is the [Hamming distance](/hamming-distance/): only substitutions count, with no insertions, deletions or transpositions. Indices are 0-based. The output is the set of start positions

$$\{\, i \in \{0, \ldots, n - m\} : |\{ q : P[q] \ne T[i + q] \}| \le k \,\}.$$

When $m = 0$, every $i$ in $0, \ldots, n$ is a match. When $m > n$, there is no match. This page reports start positions. The algorithm finds each match at its end position $j = i + m - 1$, so a program can report either one.

## The algorithm

Let $\mathrm{mm}(i, j)$ be the number of mismatches between $P[0 \ldots i]$ and $T[j - i \ldots j]$, for $0 \le i \le j$. The state is a vector of $m$ fields of $B = \lceil \log_2(k + 1) \rceil + 1$ bits each, where field $i$ is bits $iB$ to $iB + B - 1$. The low $B - 1$ bits of a field hold a count, and the top bit is the overflow bit. The choice of $B$ gives $2^{B-1} \ge k + 1$, so any count that reaches the overflow bit is too large for a match. For each character $c$, the vector $M[c]$ has the value 1 in field $i$ when $P[i] \ne c$, and 0 when $P[i] = c$. A second vector $O$ remembers the overflow bits.

```pseudo id=main
BITAP(P, T, k)                             ▷ m = |P| ≥ 1; reports start positions
L1  B ← ⌈log2(k + 1)⌉ + 1; H ← the vector with the top bit of each field set
L2  for each c: M[c] ← Σ { 2^(iB) : 0 ≤ i < m, P[i] ≠ c }
L3  S ← 0; O ← 0
L4  for j ← 0 to n − 1 do
L5      S ← ((S << B) + M[T[j]]) mod 2^(mB)     ▷ move each field up one prefix, add the mismatch
L6      O ← ((O << B) or (S and H)) mod 2^(mB)  ▷ move the old overflow bits, add the new ones
L7      S ← S and not H                         ▷ clear the top bits
L8      if j ≥ m − 1 and field m − 1 of (S or O) ≤ k then report j − m + 1
```

Line L5 shifts each field up by one position, so field $i$ receives the count of field $i - 1$, which is the count for the prefix one shorter that ends one character earlier. The addition of $M[T[j]]$ then adds 1 to field $i$ exactly when $P[i] \ne T[j]$. Field 0 receives 0 from the shift, so it holds $[P[0] \ne T[j]]$. Line L6 records each count that reached $2^{B-1}$, and line L7 clears its top bit, so no field ever carries into the next one. An overflow bit moves up with its field, so it stays attached to the same alignment. Line L8 reads the last field: if the overflow bit is set, the value is at least $2^{B-1} > k$, and otherwise it is the true count $\mathrm{mm}(m-1, j)$.

For $k = 0$, $B = 1$: each field is only an overflow bit, which is set on the first mismatch. This is the Shift-Or method, with the bit set for a mismatch.

## Example

The pattern $P = \texttt{abc}$, the text $T = \texttt{abxabcbc}$ and $k = 1$. Then $B = 2$: each field holds a count of 0 or 1 and an overflow bit. The table shows the field values after each step, with "≥2" for a field whose overflow bit is set, and a blank for a field $i > j$, which has no full alignment yet.

| $j$ | $T[j]$ | field 0 ($\texttt{a}$) | field 1 ($\texttt{ab}$) | field 2 ($\texttt{abc}$) | report |
|---|---|---|---|---|---|
| 0 | a | 0 | | | |
| 1 | b | 1 | 0 | | |
| 2 | x | 1 | ≥2 | 1 | start 0 |
| 3 | a | 0 | ≥2 | ≥2 | |
| 4 | b | 1 | 0 | ≥2 | |
| 5 | c | 1 | ≥2 | 0 | start 3 |
| 6 | b | 1 | 1 | ≥2 | |
| 7 | c | 1 | ≥2 | 1 | start 5 |

At $j = 2$, field 2 is 1, the count for $\texttt{abc}$ against $\texttt{abx}$. At $j = 3$, field 2 receives field 1 of step 2, which has its overflow bit set, so it stays at "≥2": $\texttt{abc}$ against $\texttt{bxa}$ has 3 mismatches. The output is $\{0, 3, 5\}$. With $k = 0$ the output is $\{3\}$, the one exact occurrence.

## Correctness

The invariant after step $j$ is: for each $i \le \min(j, m - 1)$, if the overflow bit of field $i$ in $O$ is 0, then field $i$ of $S$ is $\mathrm{mm}(i, j)$; if it is 1, then $\mathrm{mm}(i, j) \ge 2^{B-1}$. The proof is an induction on $j$, with the identity $\mathrm{mm}(i, j) = \mathrm{mm}(i - 1, j - 1) + [P[i] \ne T[j]]$ and the fact that a field below $2^{B-1}$ plus 1 stays below $2^B$, so no carry crosses a field. Line L8 then reports $j - m + 1$ exactly when $\mathrm{mm}(m - 1, j) \le k$. The full proof is below.

## Complexity

Each step does $O(1)$ shifts, additions and Boolean operations on vectors of $mB$ bits. On a [word RAM](/word-ram/) with words of $w$ bits, a vector takes $\lceil mB / w \rceil$ words, so the search takes $\Theta(n \lceil mB / w \rceil)$ time in the worst case, which is $\Theta(n)$ when $m (\lceil \log_2(k+1) \rceil + 1) \le w$. The table $M$ takes $\Theta(\sigma \lceil mB / w \rceil + m)$ time and $\Theta(\sigma \lceil mB / w \rceil)$ space. A hash table over the pattern characters, with one shared vector for all other characters, reduces this to $O(m)$ entries. The search reads each text character once and keeps no buffer, so it works on a stream.

## Properties

- **Online.** It reads the text once, from left to right, and reports each match as soon as its last character arrives.
- **Counts, not only decisions.** With $B = \lceil \log_2(m + 1) \rceil$ and no overflow bit, the last field holds the exact number of mismatches at every alignment.
- **Independent of the text.** The work per character does not depend on the text or on the number of matches.
- **Wide fields.** The state needs $m$ fields, so a long pattern or a large $k$ needs many words. For a pattern longer than the word, other methods are faster.

## Variants and improvements

- **Shift-And and Shift-Or.** The case $k = 0$, with one bit per prefix. See [Shift-Or](/shift-or/).
- **Classes of characters.** If position $i$ of the pattern accepts a set of characters, set field $i$ of $M[c]$ to 0 for each $c$ in the set. The time does not change.
- **Edits.** The [Wu-Manber algorithm](/wu-manber-approximate-matching/) keeps $k + 1$ bit vectors, one for each number of errors, and adds insertions and deletions. The [Myers bit-parallel algorithm](/myers-bit-parallel-algorithm/) encodes a column of the edit distance table in $O(\lceil m / w \rceil)$ words.
- **Faster for large $k$.** For a long pattern and a large $k$, the [Amir-Lewenstein-Porat algorithm](/amir-lewenstein-porat-algorithm/) solves the [k-mismatch problem](/k-mismatch-problem/) in $O(n \sqrt{k \log k})$ time, and [Hamming string matching](/hamming-string-matching/) with fast Fourier transforms gives all counts.

## When to use it

Use bitap for short patterns, up to about one machine word of fields, with few mismatches. It is simple, has no worst case beyond the linear scan, and suits streams and hardware. The tool agrep uses this family of methods. For patterns longer than a word, or when $k$ is large compared with $m$, use a method based on [the Landau-Vishkin kangaroo jumps](/landau-vishkin-algorithm/) or on convolutions.

## Pitfalls

- **Field width.** $B$ must satisfy $2^{B-1} \ge k + 1$. With $B = \lceil \log_2(k+1) \rceil$ and no overflow bit, a count can carry into the next field and give false matches.
- **Early positions.** Before step $m - 1$, the last field does not stand for a full alignment. Report only from $j = m - 1$ on, or start $S$ with large values in the fields.
- **Characters outside the pattern.** They mismatch every position, so they need the vector with 1 in each field, not 0.
- **End or start.** The algorithm detects a match at its end $j$. The start is $j - m + 1$. Mixing the two shifts the output by $m - 1$.
- **Mismatches only.** The method does not handle insertions or deletions. A pattern with one missing character can have many mismatches at every alignment.

## Implementations

## History

Baeza-Yates and Gonnet presented the shift-or method and the shift-add method for mismatches at SIGIR in 1989, and published the journal version, "A new approach to text searching", in Communications of the ACM in 1992. In the same issue, Wu and Manber extended the bit-parallel approach to insertions and deletions. Their tool agrep made these methods widely used.

## References
