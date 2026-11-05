---
tag: 0F6W2E
kind: algorithm
slug: galil-park-algorithm
name: Galil-Park algorithm
aliases:
- Galil-Park k-differences algorithm
area: strings/approximate-matching
level: advanced
summary: O(nk) algorithm for k-differences that uses constant-time longest-common-extension queries.
solves: [k-differences-problem, approximate-string-matching]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, k: the error bound}
  time: {worst: "O(k n + m^2)"}
  space: {extra: "O(m^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1989
  people: [Zvi Galil, Kunsoo Park]
  note: Galil and Park presented the algorithm at ICALP 1989 and published it in the SIAM Journal on Computing in 1990, building on the reference triples of the first Landau-Vishkin algorithm.
prereqs: [landau-vishkin-algorithm, k-differences-problem, longest-common-extension-query]
see_also: [sellers-algorithm, ukkonen-cutoff-algorithm, suffix-tree, damerau-levenshtein-distance, cole-hariharan-algorithm, myers-bit-parallel-algorithm]
sources:
  - paper: "Zvi Galil and Kunsoo Park, An improved algorithm for approximate string matching, SIAM Journal on Computing 19(6), 1990, pages 989 to 999"
    locator: the O(kn) algorithm with reference triples and the table of longest common prefixes of the pattern with itself
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 5.2, Improving the worst case (the paragraph on Galil and Park, 1989, with Figure 13)
  - paper: "Zvi Galil and Raffaele Giancarlo, Data structures and algorithms for approximate string matching, Technical Report CUCS-299-87, Columbia University, 1987"
    locator: the description of the first Landau-Vishkin algorithm (Algorithm SD2), which derives extensions from a set of triples and a table of the pattern against itself
---

The Galil-Park algorithm solves the [k-differences problem](/k-differences-problem/) in $O(kn)$ time for a text of length $n$, after $O(m^2)$ preprocessing of a pattern of length $m$. It computes the same furthest rows of the diagonals as the [Landau-Vishkin algorithm](/landau-vishkin-algorithm/), but it never builds a [suffix tree](/suffix-tree/) of the text. Each extension of a match between the pattern and the text is derived from a match found earlier, a "reference triple", and a table of [longest common extensions](/longest-common-extension-query/) of the pattern with itself. Galil and Park published it in 1989 and 1990.

## In plain words

The diagonal method slides along the pattern and the text as long as they agree. The Landau-Vishkin algorithm measures each slide in one step with a suffix tree of the pattern and the text together. Galil and Park avoid the text in that structure.

The idea: suppose an earlier slide found that a piece of the text equals a piece of the pattern, and then stopped at a difference. A new slide that starts inside this piece of text compares the pattern with the text. But the text there is a copy of the pattern, so it compares the pattern with itself, and a table built from the pattern alone answers this in one step. Only when the new slide reaches the end of the old piece does it need more work.

The algorithm keeps a few good earlier slides as references, and reads each new text character only once.

## The problem

The input is a text $T = T[0 \ldots n-1]$, a pattern $P = P[0 \ldots m-1]$ and an integer $k \ge 0$. Indices are 0-based. The edit model is the Levenshtein distance: unit-cost insertion, deletion and substitution, with no transpositions. The output is the set of end positions $j \in \{0, \ldots, n\}$ such that $d(P, T[h \ldots j)) \le k$ for some $h \le j$, in increasing order, the same output as [Sellers' algorithm](/sellers-algorithm/).

## The algorithm

As in the Landau-Vishkin algorithm, $L[d][e]$ is the furthest row $i$ of diagonal $d$ with $C[i][i + d] \le e$ in the Sellers table $C$, and $L[d][e] = -\infty$ when no such row exists. The value $L[d][e]$ depends on $L[d][e-1]$, $L[d-1][e-1]$ and $L[d+1][e-1]$, which lie on the anti-diagonals $c = d + e - 1$, $d + e - 2$ and $d + e$. So the algorithm computes the entries in order of $c = d + e$, and inside one anti-diagonal in order of $e$.

Let $PP[a][b]$ be the length of the longest common prefix of $P[a \ldots m)$ and $P[b \ldots m)$. A reference triple $(q, y, f)$ records a maximal match: $T[q \ldots q + f) = P[y \ldots y + f)$, and $q + f = n$, or $y + f = m$, or $T[q + f] \ne P[y + f]$. Each slide of the algorithm gives such a triple. For each $e$ the algorithm keeps in $R[e]$ the triple of the $e$-error slide that reaches furthest in the text. The variable $front$ is the first text position that no comparison has read yet.

```pseudo id=main
GALIL-PARK(P, T, k)                          ▷ |P| = m, |T| = n
L1  compute PP[a][b] for 0 ≤ a, b ≤ m
L2  R[0..k] ← none, front ← 0
L3  for c ← 0 to n + k do                    ▷ the anti-diagonal d + e = c
L4      for e ← 0 to k do, with d ← c − e, skipping d > n and d < −m
L5          r ← max(max(0, −d), L[d][e−1] + 1, L[d−1][e−1], L[d+1][e−1] + 1), then r ← min(r, m, n − d)
L6          r₀ ← r, x ← r + d                ▷ extend: compare P[r..] with T[x..]
L7          while r < m and x < n do
L8              if x ≥ front then compare P[r] with T[x]: if equal, r, x ← r + 1, x + 1 and front ← x, else front ← x + 1 and stop
L9              else if some (q, y, f) in R has q ≤ x < q + f, take the one with the largest q + f: g ← PP[r][y + x − q], h ← q + f − x
L10                 if g ≠ h then r ← r + min(g, h) and stop, else r, x ← r + g, x + g
L11             else compare P[r] with T[x]: if equal, r, x ← r + 1, x + 1, else stop
L12         L[d][e] ← r, and if r > r₀ and r + d > q + f for R[e] = (q, y, f), then R[e] ← (r₀ + d, r₀, r − r₀)
L13         if e = k and r = m then report m + d
```

Line L10 is the core. The triple says that $T[x \ldots q + f)$ equals $P[y' \ldots y' + h)$ with $y' = y + x - q$, and the table says that $P[r \ldots)$ and $P[y' \ldots)$ agree for exactly $g$ characters. If $g < h$, then $P[r \ldots)$ agrees with the text for $g$ characters and then differs, because the text there is a copy of $P[y' \ldots)$. If $g > h$, then $P[r \ldots)$ agrees for $h$ characters, and the character after them differs, because the old match stopped at a difference. Only for $g = h$ is the answer unknown, and the extension goes on at $x + h$. Line L8 reads text that no comparison has read, and line L11 handles a position that no triple covers, such as the difference at the end of a triple. Only three anti-diagonals of $L$ are kept.

## Example

Let $P = \texttt{GATAA}$, $T = \texttt{CAGATAAGAGAA}$ and $k = 1$. The values $L[d][e]$ and the output, the ends 6, 7, 8 and 12, are those of the [Landau-Vishkin example](/landau-vishkin-algorithm/). The table $PP$ of the pattern is:

| $PP[a][b]$ | $b = 0$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $a = 0$ | 5 | 0 | 0 | 0 | 0 |
| 1 | 0 | 4 | 0 | 1 | 1 |
| 2 | 0 | 0 | 3 | 0 | 0 |
| 3 | 0 | 1 | 0 | 2 | 1 |
| 4 | 0 | 1 | 0 | 1 | 1 |

At $c = 2$, the slide for $e = 0$ on diagonal 2 reads $T[2 \ldots 7) = \texttt{GATAA}$ by line L8 and sets $front = 7$ and $R[0] = (2, 0, 5)$.

At $c = 5$, the entry $e = 1$, $d = 4$ starts at $r = 1$, $x = 5$. The position 5 lies in the triple $(2, 0, 5)$, at the pattern position $y' = 3$. Line L9 gives $g = PP[1][3] = 1$ and $h = 7 - 5 = 2$. Since $g < h$, the extension is 1 with no text comparison: $T[5 \ldots) = \texttt{AAGAGAA}$ and $P[1 \ldots) = \texttt{ATAA}$ agree in one character. So $L[4][1] = 2$.

At $c = 6$, the entry $e = 1$, $d = 5$ starts at $r = 1$, $x = 6$, at $y' = 4$ in the same triple. Now $g = PP[1][4] = 1 = h$, so the extension moves on to $r = 2$, $x = 7 = front$, and line L8 compares $P[2] = \texttt{T}$ with $T[7] = \texttt{G}$. They differ, so $L[5][1] = 2$ and $front = 8$.

## Correctness

The values $L[d][e]$ satisfy the recurrence of the Landau-Vishkin algorithm, whose proof shows that the candidate row of line L5 followed by the longest common extension gives the true $L[d][e]$. The anti-diagonal order computes the three inputs of each entry before it. So it suffices that lines L6 to L11 compute the longest common extension of $P[r_0 \ldots)$ and $T[x_0 \ldots)$ exactly. Each stored triple records a maximal match, because each slide stops only at a difference or at the end of a string. The two cases of line L10 then follow from the triple and the table, and the other steps compare characters directly. The full proof is below.

## Complexity

- **Preprocessing.** The table $PP$ takes $\Theta(m^2)$ time and space, by $PP[a][b] = PP[a + 1][b + 1] + 1$ when $P[a] = P[b]$ and 0 otherwise.
- **Search.** There are $(n + k + 1)(k + 1)$ entries. With their choice of reference triples, Galil and Park answer the extensions in $O(k)$ total time for each anti-diagonal, so the search takes $O(kn)$ time in the worst case. Line L8 reads each text character once with a match, so these comparisons cost $O(n)$ in total.
- **Space.** $O(m^2)$ for the table, $O(k)$ for three anti-diagonals and the triples. The text is read from left to right, and only a window of $O(m + k)$ characters behind $front$ is ever compared again.
- **Smaller table.** Galil and Park also show that a suffix tree of the pattern with constant-time lowest common ancestors can replace the table, for $O(m)$ space.

The implementation below scans all $k + 1$ triples at line L9, which costs $O(k)$ for each step of an extension. It is simpler than the bookkeeping of the paper and gives the same values.

## Properties

- **No index of the text.** Only the pattern is preprocessed. The text is read once from left to right, with a small window kept.
- **Worst-case bound.** $O(kn)$ for every input, the same as the Landau-Vishkin algorithm with a suffix tree, and with a smaller structure.
- **Exact.** All matches are found, with no filter and no false positives.
- **Ends of matches.** Like Sellers' algorithm, it reports the end positions.

## Variants and improvements

- **Suffix tree of the pattern.** Replace $PP$ by a suffix tree of $P$ with lowest common ancestor queries: $O(m)$ space, the same time.
- **Transpositions.** Galil and Park show that the method also handles the swap of two adjacent characters, the edit model of the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/), within the same bound.
- **Landau and Vishkin 1985.** The first Landau-Vishkin algorithm used triples of the best previous alignment and the same table of the pattern, for $O(k^2 n)$ time. Galil and Park choose the triples better.
- **Cole and Hariharan.** For $m$ much larger than $k$, [Cole and Hariharan](/cole-hariharan-algorithm/) reach $O(n + n k^4 / m)$ time.

## When to use it

Use it when a worst-case bound of $O(kn)$ is needed but the text is too long or arrives as a stream, so that a suffix tree of the text is not possible. Navarro's survey reports that it is much faster in practice than the $O(m)$-space algorithm of Galil and Giancarlo, but still slow. For a short pattern, [Myers' algorithm](/myers-bit-parallel-algorithm/) or the [cut-off](/ukkonen-cutoff-algorithm/) is a better choice.

## Pitfalls

- **The case $g = h$.** Equal lengths give no answer, because the difference after the triple and the difference in the table can be at the same position with different characters. The extension must go on.
- **Maximal triples only.** A triple that is not maximal, for example one cut at a candidate row, breaks the case $g > h$. Store only full slides, which end at a difference or at the end of a string.
- **The end of the pattern.** When $y + f = m$, the triple tells nothing about the text after it. The case $g > h$ cannot happen then, because $g \le m - y'$.
- **The loop over $e$ runs upward.** The input $L[d+1][e-1]$ lies on the same anti-diagonal as $L[d][e]$, so it must be computed first.

## Implementations

## History

Landau and Vishkin's first algorithm for $k$ differences, from 1985, derived the extensions from the triples of an earlier alignment and from the longest common prefixes of the pattern with itself, in $O(k^2 n)$ time. Their second algorithm reached $O(kn)$ with a suffix tree of the text, and Galil and Giancarlo reached $O(kn)$ in $O(m)$ space with suffix trees of pieces of the text. Galil and Park presented their algorithm at ICALP 1989 and published it in the SIAM Journal on Computing in 1990, with $O(kn)$ time from a better choice of reference triples.

## References
