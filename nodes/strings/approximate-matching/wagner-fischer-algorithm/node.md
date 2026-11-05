---
tag: ZX8DFX
kind: algorithm
slug: wagner-fischer-algorithm
name: Wagner-Fischer algorithm
aliases:
- Wagner-Fischer dynamic program
- Levenshtein dynamic program
area: strings/approximate-matching
level: intro
summary: O(nm) dynamic program filling the edit-distance table row by row.
solves: [edit-distance]
model: word-ram
complexity:
  vars: {m: the length of the first string, n: the length of the second string}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m n), distance_only: "Θ(min(m, n))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1974
  people: [Robert A. Wagner, Michael J. Fischer]
  note: Wagner and Fischer published the dynamic program for the string-to-string correction problem with general costs. The same table was found independently several times around that time.
prereqs: [edit-distance, edit-operations, tabulation]
see_also: [sellers-algorithm, needleman-wunsch, hirschberg-lcs, lcs-dynamic-programming, ukkonen-cutoff-algorithm, myers-bit-parallel-algorithm, damerau-levenshtein-distance, traceback]
sources:
  - paper: doi:10.1145/321796.321811
    title: Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974
    locator: pages 168 to 173 (traces, the recurrence and the algorithm)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11 (the edit distance recurrence, the tabular computation and the traceback)
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 5.1.1, Computing edit distance (and the list of independent discoveries in Section 5.1)
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 7, Alignments
---

The Wagner-Fischer algorithm computes the [edit distance](/edit-distance/) of two strings by [tabulation](/tabulation/): it fills a table whose cell $(i, j)$ holds the distance between the first $i$ characters of one string and the first $j$ characters of the other. Each cell is the minimum of three neighbours plus a cost, so the table of $(m+1)(n+1)$ cells fills in $\Theta(mn)$ time. A walk back through the table, the [traceback](/traceback/), gives an optimal alignment. The edit model on this page is the Levenshtein distance: unit-cost insertion, deletion and substitution, without transpositions.

## In plain words

You want the fewest changes that turn one word into another. Break the job into smaller jobs: how many changes turn the first few letters of one word into the first few letters of the other word?

Write these answers in a grid. A row stands for a start of the first word, and a column for a start of the second word. The top row and the left column are easy: to make a word from nothing, you add each letter.

Any other cell looks at three cells that are already filled: the cell above, the cell to the left and the cell up and to the left. The last change is then a removal, an addition, or a change of one letter. The cell keeps the cheapest choice. The cell in the bottom right corner is the answer.

## The problem

The input is two strings $x = x[0 \ldots m-1]$ and $y = y[0 \ldots n-1]$ over an [alphabet](/alphabet/) $\Sigma$. Indices are 0-based. The output is the Levenshtein distance $d(x, y)$, the least number of insertions, deletions and substitutions of single characters that turn $x$ into $y$. A second procedure outputs an optimal alignment, a list of columns $(a, b)$ in which $(a, a)$ is a match, $(a, b)$ with $a \ne b$ is a substitution, $(a, -)$ is a deletion and $(-, b)$ is an insertion.

## The algorithm

The table $D[0 \ldots m][0 \ldots n]$ holds $D[i][j] = d(x[0 \ldots i), y[0 \ldots j))$.

```pseudo id=main
WAGNER-FISCHER(x, y)                       ▷ |x| = m, |y| = n
L1  for i ← 0 to m do D[i][0] ← i
L2  for j ← 0 to n do D[0][j] ← j
L3  for i ← 1 to m do
L4      for j ← 1 to n do
L5          c ← 0 if x[i − 1] = y[j − 1], else 1
L6          D[i][j] ← min(D[i − 1][j] + 1, D[i][j − 1] + 1, D[i − 1][j − 1] + c)
L7  return D[m][n]

TRACEBACK(x, y, D)                         ▷ an optimal alignment
L8  i ← m, j ← n, S ← empty list
L9  while i > 0 or j > 0 do
L10     if i > 0 and j > 0 and D[i][j] = D[i − 1][j − 1] + [x[i − 1] ≠ y[j − 1]] then put (x[i − 1], y[j − 1]) in front of S, i ← i − 1, j ← j − 1
L11     else if i > 0 and D[i][j] = D[i − 1][j] + 1 then put (x[i − 1], −) in front of S, i ← i − 1
L12     else put (−, y[j − 1]) in front of S, j ← j − 1
L13 return S
```

Lines L1 and L2 fill the first column and the first row: a prefix of length $i$ needs $i$ deletions to become empty, and $j$ insertions make a prefix of length $j$ from nothing. Line L6 takes the best of the three possible last columns of an alignment. The term $D[i-1][j] + 1$ deletes $x[i-1]$, the term $D[i][j-1] + 1$ inserts $y[j-1]$, and the term $D[i-1][j-1] + c$ matches or substitutes $x[i-1]$ with $y[j-1]$. The loops visit the cells row by row, so the three neighbours of a cell are ready when the cell is computed. TRACEBACK starts at the corner $(m, n)$ and moves to a neighbour that gives the minimum in line L6, so it follows one optimal path back to $(0, 0)$.

## Example

Let $x = \texttt{kitten}$ ($m = 6$) and $y = \texttt{sitting}$ ($n = 7$). Row $i$ is the prefix of $x$ of length $i$, and column $j$ the prefix of $y$ of length $j$.

| | $\varepsilon$ | s | i | t | t | i | n | g |
|---|---|---|---|---|---|---|---|---|
| $\varepsilon$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| k | 1 | **1** | 2 | 3 | 4 | 5 | 6 | 7 |
| i | 2 | 2 | **1** | 2 | 3 | 4 | 5 | 6 |
| t | 3 | 3 | 2 | **1** | 2 | 3 | 4 | 5 |
| t | 4 | 4 | 3 | 2 | **1** | 2 | 3 | 4 |
| e | 5 | 5 | 4 | 3 | 2 | **2** | 3 | 4 |
| n | 6 | 6 | 5 | 4 | 3 | 3 | **2** | **3** |

So $d(\texttt{kitten}, \texttt{sitting}) = 3$. The bold cells are the path of TRACEBACK. From $(6, 7)$, line L10 fails because $\texttt{n} \ne \texttt{g}$ and $D[5][6] + 1 = 4$, and line L11 fails because $D[5][7] + 1 = 5$, so line L12 inserts $\texttt{g}$. Then the path takes the diagonal six times: a match of $\texttt{n}$, a substitution $\texttt{e} \to \texttt{i}$, matches of $\texttt{t}$, $\texttt{t}$ and $\texttt{i}$, and a substitution $\texttt{k} \to \texttt{s}$. The alignment is

```
k i t t e n -
s i t t i n g
```

with two substitutions and one insertion.

## Correctness

The proof has two parts. First, $D[i][j]$ is the least cost of an alignment of the two prefixes, by induction on $i + j$: the last column of an alignment is a match or substitution, a deletion or an insertion, and line L6 takes the best of the three. Second, the least cost of an alignment equals the least number of operations of an edit script. An alignment gives a script with one operation for each column that costs 1. Conversely, the alignment cost satisfies the [triangle inequality](/triangle-inequality/), so a script of $L$ operations gives an alignment of cost at most $L$, even when the script changes one position several times. TRACEBACK keeps the invariant that its columns cost $D[m][n] - D[i][j]$. The full proof is below.

## Complexity

- **Time.** Lines L5 and L6 run $mn$ times, each in $O(1)$ time, and lines L1 and L2 take $O(m + n)$. So the time is $\Theta(mn)$ in each case, for $m, n \ge 1$. TRACEBACK takes $O(m + n)$ time, because $i + j$ drops in each step.
- **Space.** The full table has $(m+1)(n+1)$ cells, so it takes $\Theta(mn)$ space. Row $i$ needs only row $i - 1$. With two rows, and with the shorter string along the rows, the distance needs $O(\min(m, n))$ extra space. The traceback needs the full table, or the divide and conquer of Hirschberg.

In the model where an algorithm only tests two characters for equality, Wong and Chandra show that $\Omega(mn)$ tests are necessary for an alphabet without a bound on its size. For a finite alphabet, the [Four Russians method](/four-russians-method/) of Masek and Paterson reaches $O(n^2 / \log n)$ for $m = n$.

## Properties

- **Exact.** It computes the distance, not an estimate.
- **Data-oblivious.** The cells and their order do not depend on the characters, only on $m$ and $n$.
- **Symmetric.** $D$ for $(y, x)$ is the transpose of $D$ for $(x, y)$, because the recurrence is symmetric.
- **All prefix distances.** The table gives $d(x[0 \ldots i), y[0 \ldots j))$ for each $i$ and $j$, not only the final distance.
- **Many optimal alignments.** Several paths can reach the minimum. The order of the tests in lines L10 to L12 picks one of them.

## Variants and improvements

- **General costs.** Replace the 1 in line L6 by the cost of a deletion or an insertion, and $c$ by the cost of a substitution. This is the form of Wagner and Fischer, the [weighted edit distance](/weighted-edit-distance/), and in biology the [Needleman-Wunsch](/needleman-wunsch/) algorithm.
- **Transpositions.** One more term, $D[i-2][j-2] + 1$ when $x[i-2 \ldots i)$ and $y[j-2 \ldots j)$ are swapped, gives the optimal string alignment distance. The true [Damerau-Levenshtein distance](/damerau-levenshtein-distance/) needs the algorithm of Lowrance and Wagner.
- **Search in a text.** A first row of zeros gives [Sellers' algorithm](/sellers-algorithm/) for [approximate string matching](/approximate-string-matching/).
- **A band.** If the distance is at most $k$, only the cells with $|i - j| \le k$ matter. This gives $O(k \min(m, n))$ time, and with doubling of $k$, $O(d \min(m, n))$ for $d = d(x, y)$ (Ukkonen, 1985). See [banded alignment](/banded-alignment/).
- **Bit-parallel rows.** [Myers' algorithm](/myers-bit-parallel-algorithm/) stores the differences between adjacent cells as bit vectors, and updates a column of $w$ cells with a few word operations.
- **Linear space with an alignment.** The divide and conquer of [Hirschberg](/hirschberg-lcs/) finds the middle cell of an optimal path with two half tables, and recurses. The time stays $O(mn)$ and the space drops to $O(m + n)$.

## When to use it

Use it to compute the distance of two strings of moderate length, or when you need an alignment and the table fits in memory. It is short, it has no special cases, and it adapts to other costs. For a small bound $k$ on the distance, use a band. For long strings over a small alphabet, use the bit-parallel form. To search a pattern in a text, use [Sellers' algorithm](/sellers-algorithm/) or its faster relatives.

## Pitfalls

- **Off by one.** The table has $m + 1$ rows and $n + 1$ columns. Cell $(i, j)$ compares the characters $x[i-1]$ and $y[j-1]$.
- **A shortcut on a match.** Some texts take $D[i-1][j-1]$ at once when $x[i-1] = y[j-1]$. This is correct for unit costs, because $D[i-1][j-1] \le D[i-1][j] + 1$ and $D[i-1][j-1] \le D[i][j-1] + 1$. With general costs it can be wrong.
- **Traceback with two rows.** The two-row version gives only the distance. An alignment needs the full table or Hirschberg's method.
- **Memory.** For two strings of length $10^5$, the full table has $10^{10}$ cells. Use two rows or a band.
- **Unicode.** A user-visible character can be several code points. Compare the units that the application means, for example grapheme clusters.

## Implementations

## History

Levenshtein defined the distance in 1965 for the study of codes that correct insertions, deletions and substitutions of bits. The table method was found several times in different fields: Navarro lists Vintsyuk (1968, speech recognition), Needleman and Wunsch (1970, biology), Sankoff (1972), Sellers (1974), Wagner and Fischer (1974) and Lowrance and Wagner (1975). Wagner and Fischer stated the string-to-string correction problem with general costs, proved the recurrence through traces, and gave the algorithm in the form that most textbooks use.

## References
