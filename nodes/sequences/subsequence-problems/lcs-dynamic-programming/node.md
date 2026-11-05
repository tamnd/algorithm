---
tag: 31FDB1
kind: algorithm
slug: lcs-dynamic-programming
name: LCS dynamic programming
aliases:
- Wagner-Fischer LCS table
- Needleman-Wunsch-style LCS table
area: sequences/subsequence-problems
level: intro
summary: Fills an O(nm) table of prefix LCS lengths and traces back an optimal subsequence.
solves: [longest-common-subsequence]
model: word-ram
complexity:
  vars: {m: the length of X, n: the length of Y}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [lcs-optimal-substructure, tabulation, traceback]
see_also: [longest-common-subsequence, hirschberg-lcs, hunt-szymanski, bit-parallel-lcs, myers-diff, wagner-fischer-algorithm, needleman-wunsch, rolling-array-space-reduction]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.4, the procedures LCS-LENGTH and PRINT-LCS, the worked table, and the exercises on reconstruction without the b table and on space
  - paper: "Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974, 168-173"
    locator: the table algorithm for the cost of a cheapest edit sequence and the recovery of the edit sequence
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 6.3, Edit distance (the same table, filled in row order, as a DAG of subproblems)
---

The LCS dynamic program computes a [longest common subsequence](/longest-common-subsequence/) of two sequences $X$ and $Y$ of lengths $m$ and $n$. It fills a table $c[0 \ldots m, 0 \ldots n]$ where $c[i, j]$ is the LCS length of the prefixes $X_i$ and $Y_j$, from the three-case recurrence of the [optimal substructure theorem](/lcs-optimal-substructure/), and then walks back through the table to read off one LCS. It does exactly $mn$ equality tests and takes $\Theta(mn)$ time and space; the length alone needs only two rows. It is the same table as the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) for edit distance, with the costs of LCS.

## In plain words

Write the first sequence down the side of a grid and the second along the top. The cell in row $i$ and column $j$ will hold the length of the best common part of the first $i$ items of the side word and the first $j$ items of the top word. The top row and the left column hold zero.

Fill the other cells row by row. If the two items of a cell are equal, take the value of the cell up and to the left, plus one. If they are not equal, take the larger of the cell above and the cell to the left. The bottom right cell holds the answer. To get the common part itself, start at that cell and walk back: on a match, write down the item and go up and left; else go to the neighbour that has the same value.

## The problem

The input is two sequences $X = \langle x_1, \ldots, x_m \rangle$ and $Y = \langle y_1, \ldots, y_n \rangle$ over a set with an equality test. The output is a common subsequence of maximum length. This is the [longest common subsequence](/longest-common-subsequence/) problem.

## The algorithm

```pseudo id=main
LCS-LENGTH(X[1 .. m], Y[1 .. n])
L1  for i ← 0 to m do c[i, 0] ← 0
L2  for j ← 0 to n do c[0, j] ← 0
L3  for i ← 1 to m do
L4      for j ← 1 to n do
L5          if X[i] = Y[j] then c[i, j] ← c[i − 1, j − 1] + 1
L6          else if c[i − 1, j] ≥ c[i, j − 1] then c[i, j] ← c[i − 1, j]
L7          else c[i, j] ← c[i, j − 1]
L8  return c

LCS-TRACEBACK(c, X, Y)
L9  i ← m, j ← n, Z ← empty sequence
L10 while i > 0 and j > 0 do
L11     if X[i] = Y[j] then put X[i] at the front of Z, i ← i − 1, j ← j − 1
L12     else if c[i − 1, j] ≥ c[i, j − 1] then i ← i − 1
L13     else j ← j − 1
L14 return Z
```

Lines L5 to L7 are the recurrence. When each cell $(i, j)$ is computed, the three cells it reads are in an earlier row or earlier in the same row, so they are final. CLRS stores an arrow table $b$ next to $c$; LCS-TRACEBACK recomputes each arrow from $c$ and the two items, so the arrow table is not needed. The tie rule of line L12 must be the same as that of line L6 if you want the traceback to follow the arrows of the fill; any rule that moves to a neighbour with the value $c[i, j]$ gives a correct LCS, but different rules give different LCSs.

## Example

Take $X = \text{ABCBDAB}$ and $Y = \text{BDCABA}$, the example of CLRS Section 14.4. The [longest common subsequence](/longest-common-subsequence/) page shows the full table; its last cell is $c[7, 6] = 4$. The traceback visits these cells:

| cell $(i, j)$ | $x_i$, $y_j$ | test | move |
| --- | --- | --- | --- |
| (7, 6) | B, A | $c[6,6] = 4 \ge c[7,5] = 4$ | up |
| (6, 6) | A, A | match | output A, diagonal |
| (5, 5) | D, B | $c[4,5] = 3 \ge c[5,4] = 2$ | up |
| (4, 5) | B, B | match | output B, diagonal |
| (3, 4) | C, A | $c[2,4] = 1 < c[3,3] = 2$ | left |
| (3, 3) | C, C | match | output C, diagonal |
| (2, 2) | B, D | $c[1,2] = 0 < c[2,1] = 1$ | left |
| (2, 1) | B, B | match | output B, diagonal |

The walk stops at $(1, 0)$. Reading the outputs from the last to the first gives the LCS BCBA. With the opposite tie rule ($>$ in lines L6 and L12) the same table gives BDAB.

## Correctness

LCS-LENGTH is correct by induction over the cells in row order: line L1 and L2 set the cells with $i = 0$ or $j = 0$ to their true value 0, and lines L5 to L7 compute $c[i, j]$ from cells that are already correct, by the recurrence, which the [optimal substructure theorem](/lcs-optimal-substructure/) proves. LCS-TRACEBACK keeps this [loop invariant](/loop-invariant/): $Z$ is a common subsequence of $x_{i+1} \cdots x_m$ and $y_{j+1} \cdots y_n$, and $|Z| + c[i, j] = c[m, n]$. When the loop stops, $i = 0$ or $j = 0$, so $c[i, j] = 0$ and $|Z| = c[m, n]$. The full proof is in the proof file.

## Complexity

- **Time.** Lines L1 and L2 take $\Theta(m + n)$. The double loop runs $mn$ times, with one equality test and $O(1)$ other work each time. So LCS-LENGTH takes $\Theta(mn)$ time on every input, with exactly $mn$ equality tests. Each iteration of the traceback loop lowers $i + j$ by 1 or 2, so it runs at most $m + n$ times and takes $O(m + n)$ time.
- **Space.** The table has $(m+1)(n+1)$ entries, each at most $\min(m, n)$, so $\Theta(mn)$ words.
- **The length in less space.** Row $i$ needs only row $i - 1$. With two rows, or one row and one extra variable, the length takes $\Theta(\min(m, n))$ extra space if the shorter sequence is put along the row. This is the [rolling array](/rolling-array-space-reduction/) trick. It loses the traceback; [Hirschberg's algorithm](/hirschberg-lcs/) gets an LCS in linear space at about twice the time.
- **Lower bound.** In the model of equal and unequal tests, $\Omega(mn)$ tests are necessary when the alphabet is not bounded (Aho, Hirschberg and Ullman 1976, see the [LCS](/longest-common-subsequence/) page). So for such inputs the table is optimal in that model.

For $m = n = 10^4$ the table has about $10^8$ cells. With 4-byte entries this is 400 MB, which is why the linear-space methods matter.

## Properties

- **Deterministic and oblivious.** The cells are filled in the same order on each input, and the number of tests does not depend on the input.
- **Equality only.** The items need an equality test, not an order. So the method works for lines of text, tokens or records.
- **Not adaptive.** Two equal inputs of length $n$ still cost $n^2$ steps. The [Myers algorithm](/myers-diff/) and [Hunt-Szymanski](/hunt-szymanski/) are faster on similar or sparse inputs.
- **Parallel by anti-diagonals.** The cells with the same $i + j$ do not depend on each other, so a wavefront can compute each anti-diagonal in parallel.

## Variants and improvements

- **Rolling rows.** Length only, in linear space, as above.
- **[Hirschberg's algorithm](/hirschberg-lcs/).** One LCS in $\Theta(m + n)$ space by divide and conquer on the middle row.
- **[Bit-parallel LCS](/bit-parallel-lcs/).** Store the 0 and 1 differences of a row in words, and update a whole word at a time.
- **Banded table.** If the LCS is known to be at least $\max(m, n) - k$, only cells with $|i - j| \le k$ can be on an optimal path, which gives $O(k \max(m, n))$ time; see [banded alignment](/banded-alignment/).
- **Weighted costs.** Replace $+1$ and $\max$ with scores and gap costs to get [Needleman-Wunsch](/needleman-wunsch/) [global alignment](/global-alignment/), or with edit costs to get the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/).
- **Memoized recursion.** The recurrence with [memoization](/memoization/) computes only the cells it reaches, which can be fewer, but it uses recursion depth up to $m + n$.

## When to use it

Use the table when the inputs are short enough that $mn$ cells fit in memory and time, or when you need the full table (for example, to list all LCSs or to answer questions for all prefix pairs). For long similar files, use [Myers' algorithm](/myers-diff/). For an LCS of long inputs in small memory, use [Hirschberg's algorithm](/hirschberg-lcs/). For the length of short strings over a small alphabet, use the [bit-parallel](/bit-parallel-lcs/) method.

## Pitfalls

- **Off by one.** The table has $m + 1$ rows and $n + 1$ columns. The item of row $i$ is $X[i]$ in 1-based code and `x[i - 1]` in 0-based code.
- **The last row is not an LCS.** The values in the last row are lengths of different LCSs of different prefixes; the subsequence comes only from the traceback.
- **Plain recursion.** The recurrence without a table takes exponential time, for example about $\binom{m+n}{m}$ calls when $X$ and $Y$ have no common item.
- **Recursion in the traceback.** A recursive PRINT-LCS has depth up to $m + n$, which can overflow the stack in languages with a small stack. The loop of lines L10 to L13 does not.
- **Memory.** A full table of $10^4 \times 10^4$ entries does not fit in a small machine. Use rolling rows for the length.

## Implementations

## History

Wagner and Fischer (1974) gave the table algorithm for the string-to-string correction problem, which includes the LCS as a special case. CLRS presents the LCS version with the arrow table $b$ and the recursive PRINT-LCS, and leaves the reconstruction from $c$ alone as an exercise.

## References
