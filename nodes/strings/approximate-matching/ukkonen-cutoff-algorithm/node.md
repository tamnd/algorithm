---
tag: V58QHM
kind: algorithm
slug: ukkonen-cutoff-algorithm
name: Ukkonen's cutoff algorithm
aliases:
- Ukkonen cutoff heuristic
area: strings/approximate-matching
level: advanced
summary: Computes each column of the Sellers table only down to its last cell with a value at most k, in O(kn) expected time on random text.
solves: [k-differences-problem, approximate-string-matching]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, k: the error bound}
  time: {worst: Θ(m n), average: O(k n)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1985
  people: [Esko Ukkonen]
  note: Ukkonen described the cut-off in a short note at the end of his 1985 paper on approximate patterns and conjectured the O(kn) average time, which Chang and Lampe proved in 1992.
prereqs: [sellers-algorithm, k-differences-problem]
see_also: [landau-vishkin-algorithm, myers-bit-parallel-algorithm, wu-manber-approximate-matching, galil-park-algorithm, wagner-fischer-algorithm, levenshtein-automaton]
sources:
  - paper: "Esko Ukkonen, Finding approximate patterns in strings, Journal of Algorithms 6(1), 1985, pages 132 to 137"
    locator: the note at the end of the paper on the last cell with a value at most k
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 5.3, Improving the average case (the paragraph on Ukkonen 1985, the cut-off heuristic)
  - paper: "William I. Chang and Jordan Lampe, Theoretical and empirical comparisons of approximate string matching algorithms, Combinatorial Pattern Matching (CPM 1992), LNCS 644, pages 172 to 181"
    locator: the proof that the cut-off runs in O(kn) expected time on random text
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 6, Approximate matching (the dynamic programming algorithm and its last active cell)
---

Ukkonen's cut-off algorithm is [Sellers' algorithm](/sellers-algorithm/) for the [k-differences problem](/k-differences-problem/) with one change: it computes each column of the table only down to the last cell whose value is at most $k$, the last active cell. Cells below that cell can never lead to a match, so their exact values do not matter. On random text the last active cell stays near row $k$, so the expected time drops from $\Theta(mn)$ to $O(kn)$ for a pattern of length $m$ and a text of length $n$. The worst case stays $\Theta(mn)$, and the output is the same as Sellers' output.

## In plain words

Sellers' method fills a grid: the pattern down the side, the text along the top, and one column for each text letter. A cell holds the number of errors of the best match of the pattern's beginning that ends there. Only matches with few errors matter.

Down a column the numbers grow fast when the text does not look like the pattern. Once a number passes the error limit, the cells below it in that column cannot help any match. So the program remembers the last cell in the column that is still within the limit, and in the next column it stops one row below that cell.

Most places in a text do not look like the pattern, so the work for each column is small on average. The answers are the same as with the full grid.

## The problem

The input is a text $T = T[0 \ldots n-1]$, a pattern $P = P[0 \ldots m-1]$ and an integer $k \ge 0$. Indices are 0-based. The edit model is the Levenshtein distance: unit-cost insertion, deletion and substitution, with no transpositions. The output is the set of end positions $j \in \{0, \ldots, n\}$ such that $d(P, T[h \ldots j)) \le k$ for some $h \le j$, in increasing order.

## The algorithm

Let $C[i][j]$ be the Sellers table. A cell is *active* when its value is at most $k$. The last active row of column $j$ is

$$\ell_j = \max\{\, i : C[i][j] \le k \,\},$$

which exists because $C[0][j] = 0$. Column $j$ has a match exactly when $\ell_j = m$. The values along a diagonal never decrease, so $C[i][j] \le k$ implies $C[i-1][j-1] \le k$, which gives $\ell_j \le \ell_{j-1} + 1$. So column $j$ needs only the rows up to $\min(\ell_{j-1} + 1, m)$.

```pseudo id=main
UKKONEN-CUTOFF(P, T, k)                    ▷ |P| = m, |T| = n
L1  for i ← 0 to m do C[i] ← i             ▷ column 0
L2  lact ← min(k, m)                       ▷ the last active row of column 0
L3  if lact = m then report 0
L4  for j ← 1 to n do
L5      top ← min(lact + 1, m)
L6      prev ← C[0]                        ▷ C[0] stays 0
L7      for i ← 1 to top do
L8          new ← min(C[i] + 1, C[i − 1] + 1, prev + [P[i − 1] ≠ T[j − 1]]), prev ← C[i], C[i] ← new
L9      lact ← top, then while C[lact] > k do lact ← lact − 1
L10     if lact = m then report j
L11     else C[lact + 1] ← k + 1           ▷ a stand-in for an inactive value
```

Lines L6 to L8 are the column update of Sellers' algorithm, restricted to the rows 1 to $top$. The cells below $top$ keep old values, and the next column never reads them. Line L11 writes $k + 1$ into the one row below the last active row, because the next column reads that row and its stored value can be old. The stand-in is safe because a value above $k$ can only feed values above $k$.

## Example

Let $P = \texttt{GATAA}$, $T = \texttt{CAGATAAGAGAA}$ and $k = 1$. The table shows the cells that the algorithm computes, and a dot for each cell it skips.

| | $j = 0$ | C | A | G | A | T | A | A | G | A | G | A | A |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\varepsilon$ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| G | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| A | 2 | 2 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 |
| T | 3 | · | · | 2 | 1 | 0 | 1 | 2 | 2 | 1 | 1 | 1 | 1 |
| A | 4 | · | · | · | · | 1 | 0 | 1 | 2 | 2 | 2 | 1 | 1 |
| A | 5 | · | · | · | · | · | 1 | 0 | 1 | 2 | · | · | 1 |

The last active rows are $\ell_0, \ldots, \ell_{12} = 1, 1, 2, 2, 3, 4, 5, 5, 5, 3, 3, 4, 5$. Column 9 ends at row 5 with the value 2, so the loop of line L9 goes up to row 3, and columns 10 and 11 stop at row 4. The rows equal to 5 give the ends 6, 7, 8 and 12. The algorithm computes 47 cells, while Sellers' algorithm computes all $5 \cdot 12 = 60$.

## Correctness

Call a stored value *valid* for a true value $v$ when it equals $v$ if $v \le k$, and is greater than $k$ if $v > k$. The proof shows by induction over the columns that after column $j$, the stored values of rows 0 to $\min(\ell_j + 1, m)$ are valid, and that $lact = \ell_j$. The minimum of line L8 over valid inputs is valid, because a true term at most $k$ comes from an exact input, and a stand-in above $k$ only gives a term above $k$. The rows below $top$ hold true values above $k$, by the diagonal bound $\ell_j \le \ell_{j-1} + 1$. So line L10 reports $j$ exactly when $C[m][j] \le k$. The full proof is below.

## Complexity

- **Worst case.** Column $j$ costs $O(top_j + 1)$ for the update, plus the steps of the loop of line L9. That loop moves $lact$ down by one at each step, and $lact$ goes up by at most 1 in each column, so all its steps together cost at most $n + k$. For a text that matches the pattern everywhere, such as $P = \texttt{a}^m$ and $T = \texttt{a}^n$ with $m \le n$, almost all cells are active, and the time is $\Theta(mn)$.
- **Average case.** For a text of independent uniform random characters, Chang and Lampe proved that the expected time is $O(kn)$, as Ukkonen had conjectured. Baeza-Yates and Navarro gave a refined proof.
- **Space.** One column of $m + 1$ cells, $\Theta(m)$. The text is read once from left to right.

## Properties

- **Same output as Sellers.** The skipped cells are exactly those that cannot lead to a match.
- **Online.** Each text character is read once, and a match is reported when its end is read.
- **Adaptive.** The work for a column is about the length of the longest pattern prefix that nearly matches there. Texts with few near matches are fast.

## Variants and improvements

- **Transpositions.** With the transposition of two adjacent characters as an operation, Navarro's survey points out that the cut must use $k + 2$ instead of $k + 1$.
- **Blocks of bits.** [Myers' bit-parallel algorithm](/myers-bit-parallel-algorithm/) in its blocked form updates only the words up to the last active block, which gives $O(\lceil k / w \rceil\, n)$ expected time.
- **Diagonal methods.** [Landau and Vishkin](/landau-vishkin-algorithm/) and [Galil and Park](/galil-park-algorithm/) reach $O(kn)$ in the worst case, but with larger constants. Myers' algorithm of 1986 computes the diagonal strokes by direct comparison and reaches $O(kn)$ on average.
- **Edit distance of two strings.** For the distance of two strings with a bound $k$, a band of $2k + 1$ diagonals around the main diagonal suffices, which is a different cut.

## When to use it

Use it whenever Sellers' algorithm is used and $k$ is small compared with $m$: the change is a few lines, and on natural text and on DNA it saves most of the work. It is also a good verifier for filters. When the pattern fits in a machine word, a bit-parallel method is faster, and for a guaranteed bound use a diagonal method.

## Pitfalls

- **Stale cells.** A cell below the computed part holds a value from an older column. Reading it as if it were current gives false matches. Line L11 prevents this.
- **The first column.** Column 0 has $C[i][0] = i$, so its last active row is $\min(k, m)$, not 0.
- **Stand-in values.** The stand-in must be greater than $k$. A stand-in of 0 or of an old value can create false active cells.
- **No worst-case gain.** On periodic texts and patterns, such as runs of one letter, the algorithm does all the work of Sellers' algorithm.

## Implementations

## History

Ukkonen described the cut-off in a short note at the end of his 1985 paper "Finding approximate patterns in strings", and conjectured that it runs in $O(kn)$ time on average. Navarro's survey counts it as the first improvement to the average case of the search problem. Chang and Lampe proved the conjecture at CPM 1992, and Baeza-Yates and Navarro refined the proof in 1996.

## References
