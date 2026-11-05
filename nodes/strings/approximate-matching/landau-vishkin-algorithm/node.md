---
tag: 2PT2TT
kind: algorithm
slug: landau-vishkin-algorithm
name: Landau-Vishkin algorithm
aliases:
- Landau-Vishkin diagonal algorithm
area: strings/approximate-matching
level: advanced
summary: Computes furthest reaching diagonal points with longest-common-extension queries in O(kn) time.
solves: [k-differences-problem, approximate-string-matching]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, k: the error bound}
  time: {worst: "O((k + 1) n)"}
  space: {extra: O(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1986
  people: [Gad M. Landau, Uzi Vishkin]
  note: Landau and Vishkin gave an O(k^2 n) algorithm in 1985 and the O(k n) algorithm with a suffix tree and constant-time lowest common ancestors in 1986, the first worst-case improvements for the k-differences problem.
prereqs: [sellers-algorithm, k-differences-problem, longest-common-extension-query]
see_also: [galil-park-algorithm, ukkonen-cutoff-algorithm, suffix-tree, lowest-common-ancestor, myers-bit-parallel-algorithm, cole-hariharan-algorithm, k-mismatch-problem]
sources:
  - paper: "Gad M. Landau and Uzi Vishkin, Fast parallel and serial approximate string matching, Journal of Algorithms 10(2), 1989, pages 157 to 169"
    locator: the serial O(kn) algorithm with the suffix tree of the text and the pattern and constant-time lowest common ancestor queries
  - paper: "Gad M. Landau and Uzi Vishkin, Fast string matching with k differences, Journal of Computer and System Sciences 37, 1988, pages 63 to 78"
    locator: the diagonal method with O(k^2 n) time and O(m) space
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 5.2, Improving the worst case (the recurrence for the furthest rows of the diagonals, and its history)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 9 (longest common extension with a suffix tree) and Chapter 12 (inexact matching with a bounded number of differences)
---

The Landau-Vishkin algorithm solves the [k-differences problem](/k-differences-problem/): it finds every end position in a text of a substring at Levenshtein distance at most $k$ from a pattern, in $O(kn)$ time for a text of length $n$. It computes, for each diagonal of the [Sellers](/sellers-algorithm/) table and each error count $e \le k$, the furthest row that the diagonal reaches with at most $e$ errors. Each such point takes $O(1)$ time, because a [longest common extension](/longest-common-extension-query/) query jumps over a run of equal characters in one step. Landau and Vishkin found it in 1986, and it was the first algorithm for the problem that beats $O(mn)$ in the worst case for small $k$.

## In plain words

Take the grid that Sellers' method fills: the pattern down the side, the text along the top. Each diagonal line of cells pairs the pattern with one fixed shift of the text. Along such a line, the numbers never drop, and they grow by at most one at each step.

So the places where a diagonal's number grows describe it fully. The algorithm finds these places in order of the number of errors. For zero errors, it follows each diagonal while the pattern and the text agree. Then, for one error, each diagonal starts one step past the best of itself and its two neighbours with zero errors, and again follows the agreement as far as it goes. And so on, up to the error limit.

A diagonal that reaches the last pattern letter marks a match. With a suffix tree, each run of agreement is measured in one step.

## The problem

The input is a text $T = T[0 \ldots n-1]$, a pattern $P = P[0 \ldots m-1]$ and an integer $k \ge 0$. Indices are 0-based. The edit model is the Levenshtein distance: unit-cost insertion, deletion and substitution, with no transpositions. The output is the set of end positions

$$\{\, j \in \{0, \ldots, n\} : d(P, T[h \ldots j)) \le k \text{ for some } h \le j \,\},$$

reported in increasing order, the same output as [Sellers' algorithm](/sellers-algorithm/).

## The algorithm

Let $C[i][j]$, for $0 \le i \le m$ and $0 \le j \le n$, be the Sellers table: the least distance from $P[0 \ldots i)$ to a substring of $T$ that ends at $j$. The cell $(i, j)$ lies on diagonal $d = j - i$, and diagonal $d$ holds the rows $i$ from $\max(0, -d)$ to $\min(m, n - d)$. Its first cell has the value $\max(0, -d)$: it is $C[0][d] = 0$ for $d \ge 0$ and $C[-d][0] = -d$ for $d < 0$. Along a diagonal the values never decrease and grow by at most 1 at each step. So for each $e \ge 0$ the rows with $C[i][i + d] \le e$ form an initial run of the diagonal, and

$$L[d][e] = \max\{\, i : C[i][i + d] \le e \,\}$$

describes it. $L[d][e]$ exists exactly when $e \ge \max(0, -d)$. Write $L[d][e] = -\infty$ when it does not exist, and $\mathrm{LCE}(i, j)$ for the length of the longest common prefix of $P[i \ldots m)$ and $T[j \ldots n)$.

```pseudo id=main
LANDAU-VISHKIN(P, T, k)                     ▷ |P| = m, |T| = n
L1  build the LCE structure for P and T
L2  for e ← 0 to k do
L3      for d ← max(−e, −m) to n do
L4          r ← max(0, −d)                  ▷ the first cell of diagonal d
L5          r ← max(r, L[d][e−1] + 1, L[d−1][e−1], L[d+1][e−1] + 1)
L6          r ← min(r, m, n − d)            ▷ stay on the diagonal
L7          L[d][e] ← r + LCE(r, r + d)     ▷ LCE is 0 when r = m or r + d = n
L8  report m + d for each d with L[d][k] = m, in increasing order of d
```

Line L5 has one term for each operation that can end in a cell with $e$ errors. The term $L[d][e-1] + 1$ is a substitution: one step down the same diagonal. The term $L[d-1][e-1]$ is an insertion of a text character: one step to the right, from diagonal $d - 1$ to diagonal $d$, in the same row. The term $L[d+1][e-1] + 1$ is a deletion of a pattern character: one step down, from diagonal $d + 1$ to diagonal $d$. A term with $L = -\infty$ does not count. Line L6 moves a candidate that falls past the end of the diagonal back to its last cell, and line L7 slides along the diagonal over equal characters. Each row $e$ needs only row $e - 1$, so two arrays of length $n + m + 1$ suffice.

The original algorithm answers each LCE query in $O(1)$ time with a [suffix tree](/suffix-tree/) of $P$ and $T$ and constant-time [lowest common ancestor](/lowest-common-ancestor/) queries. The implementation below uses a [suffix array](/suffix-array/), the [LCP array](/lcp-array/) of [Kasai](/kasai-algorithm/) and a [sparse table](/sparse-table/), which also answer a query in $O(1)$ time.

## Example

Let $P = \texttt{GATAA}$, $T = \texttt{CAGATAAGAGAA}$, $m = 5$, $n = 12$ and $k = 1$. Only diagonals $d$ from $-1$ to $n - m = 7$ can reach row 5. The table gives $L[d][e]$.

| $d$ | $-1$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|
| $e = 0$ | | 0 | 0 | **5** | 0 | 0 | 0 | 0 | 2 |
| $e = 1$ | 1 | 2 | **5** | **5** | **5** | 2 | 2 | 3 | **5** |

For $e = 0$, each diagonal starts at row 0 and slides. Diagonal 2 pairs $P$ with $T[2 \ldots 7) = \texttt{GATAA}$ and slides to row 5, an exact match that ends at 7. Diagonal 7 pairs $\texttt{GA}$ with $T[7 \ldots 9) = \texttt{GA}$ and stops at row 2, because $P[2] = \texttt{T} \ne T[9] = \texttt{G}$.

For $e = 1$, diagonal 7 takes the maximum of $L[7][0] + 1 = 3$, $L[6][0] = 0$ and $L[8][0] + 1 = 1$, so $r = 3$, and the LCE of $P[3 \ldots) = \texttt{AA}$ and $T[10 \ldots) = \texttt{AA}$ is 2. So $L[7][1] = 5$: the substitution of $\texttt{T}$ by $\texttt{G}$ gives a match that ends at 12. Diagonal 1 takes $L[2][0] + 1 = 6$, which line L6 cuts to row 5: $T[2 \ldots 6) = \texttt{GATA}$ is the pattern with its last $\texttt{A}$ deleted, a match that ends at 6. Diagonal 3 takes $L[2][0] = 5$: $T[2 \ldots 8) = \texttt{GATAAG}$ is the pattern with one $\texttt{G}$ inserted, a match that ends at 8. The diagonals with $L[d][1] = 5$ are 1, 2, 3 and 7, so the output is the ends 6, 7, 8 and 12, the same as Sellers' table gives.

## Correctness

The proof first shows three facts on the Sellers table: two adjacent cells in a row or a column differ by at most 1, and along a diagonal each step adds 0 or 1. Then it shows by induction on $e$ that line L7 stores the true $L[d][e]$. Each candidate of lines L4 to L6 is a cell with a value at most $e$, and each step of the slide keeps the value, so the result is at most the true furthest row. For the other direction, take the true furthest row and go back along its diagonal over equal characters to the start of the run. The cell there is the first cell of the diagonal, or it gets its value from a neighbour with $e - 1$ errors, and that neighbour gives a candidate at least as far as the start of the run. The slide then reaches the true furthest row. The full proof is below.

## Complexity

- **Time.** Row $e$ handles at most $n + e + 1$ diagonals, each with $O(1)$ work and one LCE query. With $O(1)$ queries this is $O((k + 1)(n + k))$, which is $O((k + 1) n)$ when $k < m \le n$. For $k \ge m$ every end is a match, so this case needs no work.
- **Preprocessing.** A suffix tree of $P$ and $T$ with lowest common ancestor queries takes $O(n + m)$ time over an alphabet of constant size. The suffix array in the implementation takes $O((n + m) \log^2 (n + m))$ time with prefix doubling, and the sparse table $O((n + m) \log (n + m))$ time and space.
- **Space.** Two rows of $L$ need $O(n + m)$ words, besides the LCE structure. The text must be stored in full, so the method does not run on a stream.

Landau and Vishkin's earlier algorithm of 1985 takes $O(k^2 n)$ time and $O(m)$ space: it uses the self-similarity of the pattern instead of a suffix tree of the text. Galil and Giancarlo reached $O(kn)$ time in $O(m)$ space, with suffix trees of overlapping pieces of the text of length $O(m)$.

## Properties

- **Diagonal transition.** The values on a diagonal grow by 0 or 1 at each step, so $k + 1$ numbers describe the part of a diagonal with values at most $k$. The algorithm computes only these numbers, never the cells.
- **Worst case, not average.** The bound $O(kn)$ holds for every input. For random text, simpler methods such as [Ukkonen's cut-off](/ukkonen-cutoff-algorithm/) reach $O(kn)$ on average with smaller constants.
- **Offline.** The LCE structure covers the whole text, so the text must be known in advance. A match is at most $m + k$ characters long, so pieces of the text of length $2m + k$ that overlap by $m + k$ can be searched one at a time.
- **Same output as Sellers.** It reports ends, and the row of furthest points tells the number of errors of each match: the least $e$ with $L[d][e] = m$ is $C[m][m + d]$.

## Variants and improvements

- **Edit distance of two strings.** With the first row of the table as $C[0][j] = j$, only the diagonals $-k$ to $k$ matter, and $O(k^2)$ LCE queries test whether $d(x, y) \le k$. This is Ukkonen's diagonal method, the origin of the idea. Myers used the same furthest points for his difference algorithm.
- **Galil and Park.** [Galil and Park](/galil-park-algorithm/) replace the suffix tree of the text by a table of the pattern against itself, for $O(kn)$ time and $O(m^2)$ space.
- **Hamming distance.** For the [k-mismatch problem](/k-mismatch-problem/), only the substitution term remains, and each alignment needs at most $k + 1$ LCE queries, for $O(kn)$ time. This is the "kangaroo" method.
- **Cole and Hariharan.** For $m$ large compared with $k$, [Cole and Hariharan](/cole-hariharan-algorithm/) reduce the number of alignments that need the full diagonal work and reach $O(n + n k^4 / m)$ time.
- **Parallel version.** The 1989 paper of Landau and Vishkin also gives a parallel form of the algorithm.

## When to use it

Use it when a worst-case bound linear in $n$ for fixed $k$ matters, for example when an adversary can choose the text. In practice the constants of the suffix tree are large: for short patterns, [Myers' bit-parallel algorithm](/myers-bit-parallel-algorithm/) or the cut-off is faster, and for long patterns with a small error level, filters such as [q-gram filtering](/q-gram-filtering/) are faster on average. The diagonal idea is useful on its own for the edit distance of two similar strings.

## Pitfalls

- **Negative diagonals.** A match can start before the first text character and lose its first pattern characters, so diagonals $-k$ to $-1$ count. Their first cell is $(-d, 0)$ with the value $-d$, not 0.
- **The end of a diagonal.** A candidate can fall past the last cell. Clip it to $\min(m, n - d)$, as line L6 does. The clipped cell always has a value at most $e$.
- **Index base of the LCE.** The query compares $P[r]$ with $T[r + d]$, the characters after the cell $(r, r + d)$, not the characters at the cell.
- **Sentinels.** Join $P$ and $T$ with distinct separator symbols before the suffix structure is built, so that no common prefix runs from $P$ into $T$.

## Implementations

## History

Ukkonen published the diagonal method for the edit distance of two strings in 1983, with the full paper in 1985. In 1985 Landau and Vishkin adapted it to search in a text, with $O(k^2 n)$ time, and the paper appeared in 1988. In 1986 they reached $O(kn)$ time with a suffix tree and constant-time lowest common ancestors, and this paper appeared in 1989 together with a parallel version. Navarro's survey counts these as the first worst-case improvements for the search problem. The same diagonal idea appears in later work by Galil and Giancarlo, Galil and Park, Myers, and Cole and Hariharan.

## References
