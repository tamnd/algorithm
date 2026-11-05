---
tag: TZXPTF
kind: algorithm
slug: sellers-algorithm
name: Sellers algorithm
aliases:
- Sellers' approximate matching
area: strings/approximate-matching
level: core
summary: O(nm) dynamic program for approximate matching, with the first row fixed to zero.
solves: [approximate-string-matching, k-differences-problem]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1980
  people: [Peter H. Sellers]
  note: Sellers turned the edit distance table into a search algorithm by letting a match start at any text position.
prereqs: [wagner-fischer-algorithm, approximate-string-matching]
see_also: [k-differences-problem, ukkonen-cutoff-algorithm, landau-vishkin-algorithm, myers-bit-parallel-algorithm, wu-manber-approximate-matching, semi-global-alignment, levenshtein-automaton]
sources:
  - paper: doi:10.1016/0196-6774(80)90016-4
    title: Peter H. Sellers, The theory and computation of evolutionary distances, pattern recognition, Journal of Algorithms 1(4), 1980
    locator: pages 359 to 373 (the search for the substrings of a text that are close to a pattern)
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 5.1.2, Text searching
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11 (inexact matching of a pattern in a text by dynamic programming with free end spaces)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 6, Approximate matching (the dynamic programming algorithm)
---

Sellers' algorithm solves [approximate string matching](/approximate-string-matching/) under the Levenshtein distance: it finds every position in a text where a substring at [edit distance](/edit-distance/) at most $k$ from the pattern ends. It is the [Wagner-Fischer](/wagner-fischer-algorithm/) table of the pattern against the text, with one change: the first row is zero, so a match can start anywhere in the text. It takes $\Theta(mn)$ time and $\Theta(m)$ space for a pattern of length $m$ and a text of length $n$, and it reads the text once from left to right. It is the base of nearly all faster methods, which compute the same table in less time.

## In plain words

Write the pattern down the side of a grid and the text along the top. Each cell answers one question: how close can the first few letters of the pattern get to some piece of text that ends exactly at this column?

The top row is all zeros: an empty start of the pattern fits anywhere for free. This is the only change from the table for the distance of two words. It lets a match begin at any place in the text.

Each other cell takes the cheapest of three moves from its neighbours, as in the table for two words. The bottom row then gives, for each text position, the best match of the whole pattern that ends there. Each value that is at most the allowed number of errors marks a match. The program keeps only one column at a time.

## The problem

The input is a text $T = T[0 \ldots n-1]$, a pattern $P = P[0 \ldots m-1]$ and an integer $k \ge 0$. Indices are 0-based. The edit model is the Levenshtein distance: unit-cost insertion, deletion and substitution, with no transpositions. The output is the set of end positions

$$\{\, j \in \{0, \ldots, n\} : d(P, T[h \ldots j)) \le k \text{ for some } h \le j \,\},$$

reported in increasing order, where $T[h \ldots j)$ is the substring $T[h] \cdots T[j-1]$. This is the [k-differences problem](/k-differences-problem/).

## The algorithm

Let $C[i][j] = \min_{h \le j} d(P[0 \ldots i), T[h \ldots j))$. Then $C[0][j] = 0$ and $C[i][0] = i$, and the other cells follow the Wagner-Fischer recurrence. The program keeps one column $C[0 \ldots m]$ and updates it for each text character.

```pseudo id=main
SELLERS(P, T, k)                           ▷ |P| = m, |T| = n
L1  for i ← 0 to m do C[i] ← i             ▷ column j = 0
L2  if C[m] ≤ k then report 0
L3  for j ← 1 to n do
L4      prev ← C[0], C[0] ← 0              ▷ the first row is zero
L5      for i ← 1 to m do
L6          c ← 0 if P[i − 1] = T[j − 1], else 1
L7          new ← min(C[i] + 1, C[i − 1] + 1, prev + c)
L8          prev ← C[i], C[i] ← new
L9      if C[m] ≤ k then report j
```

During the update of row $i$ for column $j$, the cell $C[i]$ still holds the value of column $j - 1$, the cell $C[i-1]$ holds the new value of column $j$, and $prev$ holds the old value of row $i - 1$, which is the diagonal neighbour. The term $C[i] + 1$ skips the text character $T[j-1]$ (an insertion into the pattern), the term $C[i-1] + 1$ skips the pattern character $P[i-1]$ (a deletion), and $prev + c$ aligns the two characters. The value $C[m]$ after column $j$ is the best distance of a match that ends at $j$.

## Example

Let $T = \texttt{surgery}$, $P = \texttt{survey}$ and $k = 2$. Rows are pattern prefixes and columns are text positions $j$.

| | $j = 0$ | s | u | r | g | e | r | y |
|---|---|---|---|---|---|---|---|---|
| $\varepsilon$ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| u | 2 | 1 | 0 | 1 | 2 | 2 | 2 | 2 |
| r | 3 | 2 | 1 | 0 | 1 | 2 | 2 | 3 |
| v | 4 | 3 | 2 | 1 | 1 | 2 | 3 | 3 |
| e | 5 | 4 | 3 | 2 | 2 | 1 | 2 | 3 |
| y | 6 | 5 | 4 | 3 | 3 | **2** | **2** | **2** |

The last row is $6, 5, 4, 3, 3, 2, 2, 2$ for $j = 0, \ldots, 7$, so the algorithm reports the ends 5, 6 and 7. For example, the 2 at $j = 5$ belongs to $\texttt{surge}$: substitute $\texttt{g} \to \texttt{v}$ and insert $\texttt{y}$. With $k = 1$ there is no match. The row of $\texttt{s}$ shows the effect of the zero row: $C[1][j] = 0$ wherever $T[j-1] = \texttt{s}$, and 1 elsewhere for $j \ge 1$.

## Correctness

Let $E[i][j]$ be the least distance from $P[0 \ldots i)$ to a substring of $T$ that ends at $j$. Then $E[0][j] = 0$, because the empty substring at $j$ is free, and $E[i][0] = i$. For $i, j \ge 1$, the last column of an optimal alignment is a match or substitution, a deletion or an insertion, so $E$ satisfies the Wagner-Fischer recurrence. The one new case is an empty substring, and the deletion term covers it. An induction over the columns shows that the array holds column $j$ of $E$ at line L9, so the test there is the definition of a match. The full proof is below.

## Complexity

- **Time.** Lines L6 to L8 run $mn$ times with $O(1)$ work each, so the time is $\Theta(mn)$ in every case, for $m, n \ge 1$.
- **Space.** One column of $m + 1$ cells, so $\Theta(m)$ extra space. The text is read once, from left to right, so the algorithm works on a stream.
- **Output.** At most $n + 1$ positions are reported.

When $k$ is small, most cells of a column exceed $k$ and do not matter. [Ukkonen's cut-off](/ukkonen-cutoff-algorithm/) computes only the top part of each column, up to the last cell with a value at most $k$, and runs in $O(kn)$ expected time on random text.

## Properties

- **Online.** Each text character is read once, and a match is reported as soon as its end is read.
- **Exact.** It finds all matches, with no false positives and no misses.
- **Ends, not starts.** The algorithm finds the end of each match. To find a start for a reported end $j$, run the same method backwards from $j$ on the reversed pattern, or keep with each cell the start of its best path.
- **Columns change slowly.** Adjacent cells of one column, and of one row, differ by at most 1. [Myers' algorithm](/myers-bit-parallel-algorithm/) stores these differences as bits.
- **Flexible.** Other costs, character classes and transpositions change only line L7.

## Variants and improvements

- **Weighted costs.** Replace the 1s and $c$ by the costs of a [weighted edit distance](/weighted-edit-distance/). The first row stays zero.
- **Semi-global alignment.** In biology, the same idea with scores instead of costs gives [semi-global alignment](/semi-global-alignment/), with free gaps at the ends of the text.
- **Ukkonen's cut-off.** Compute each column only down to its last active cell. Expected time $O(kn)$.
- **Diagonal methods.** [Landau and Vishkin](/landau-vishkin-algorithm/) and [Galil and Park](/galil-park-algorithm/) follow the diagonals of this table with fast extensions and reach $O(kn)$ in the worst case.
- **Bit-parallel versions.** [Wu and Manber](/wu-manber-approximate-matching/) simulate an automaton with $k + 1$ bit vectors, and [Myers](/myers-bit-parallel-algorithm/) packs the column differences into words, for $O(\lceil m / w \rceil\, n)$ time.
- **Filters.** [Pigeonhole](/pigeonhole-filtering/) and [q-gram](/q-gram-filtering/) filters find candidate areas fast, and Sellers' algorithm verifies them.

## When to use it

Use it as the reference method: it is short, exact and easy to change for other costs. It is fast enough for short patterns and moderate texts, and it is the verifier inside most filters. For long texts with a small $k$, use the cut-off or a bit-parallel method, which compute the same answer much faster.

## Pitfalls

- **The first column.** The first row is zero, but the first column is not: $C[i][0] = i$. A pattern prefix of length $i$ against an empty substring costs $i$ deletions.
- **End positions.** The algorithm reports ends. Several starts can give a match that ends at the same $j$, and adjacent ends usually belong to one region of the text.
- **Cases $k \ge m$.** Then each $j$ is a match, because the empty substring costs $m$. Handle this case first if it is not wanted.
- **Order of updates in one array.** Save the old value of $C[i]$ before overwriting it, because row $i + 1$ needs it as its diagonal neighbour.

## Implementations

## History

The edit distance table was found several times in the 1960s and 1970s. Sellers published the change that turns it into a search in 1980: the first row is zero, so the cost of the part of the text before a match is free. Navarro's survey marks this as the first algorithm for approximate search in a text. Later work kept the table and computed it faster, by cut-offs, diagonals, bit-parallelism and filters.

## References
