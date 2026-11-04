---
tag: BF0TJV
kind: technique
slug: rolling-array-space-reduction
name: Rolling-array space reduction
aliases:
- space-optimised dynamic programming
area: techniques/dynamic-programming
level: intro
summary: Keep only the last few rows of a DP table when each row depends only on the previous ones.
prereqs: [tabulation, subproblem-graph]
see_also: [traceback, hirschberg-algorithm, lcs-dynamic-programming, knapsack-dynamic-programming, unbounded-knapsack, fibonacci-numbers, edit-distance, floyd-warshall]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.4 (longest common subsequence) and Exercise 14.4-4 (LCS length with 2 min(m, n) entries, then min(m, n) entries, plus O(1) extra space)
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Section 6.7 (sequence alignment in linear space via divide and conquer)
  - paper: doi:10.1145/360825.360861
    title: Daniel S. Hirschberg, A linear space algorithm for computing maximal common subsequences, Communications of the ACM 18(6), 1975
    locator: pp. 341 to 343
---

Rolling-array space reduction is a way to run a [tabulated](/tabulation/) dynamic program in less memory: when each row of the table depends only on the previous $k$ rows, the program keeps only $k + 1$ rows and reuses them in turn, or even a single row that it updates in place in the right direction. It cuts the space of a table with $n$ rows of width $w$ from $\Theta(nw)$ to $\Theta(kw)$, and the time stays the same. The price is that the full table is gone, so the optimal value is easy to get but a [traceback](/traceback/) of the optimal solution is not. The standard fix for alignment problems is [Hirschberg's algorithm](/hirschberg-algorithm/).

## In plain words

Some tables are filled one row at a time, and each new row reads only the row just above it. Once a row is done and the next row is done, nobody will read the old row again. So you can throw it away.

Keep two rows: the old one and the new one. When the new row is full, it becomes the old row, and you start a new one in the space of the row you threw away. A table with a million rows now needs the memory of two rows.

Sometimes one row is enough. You overwrite the cells of the row one by one, as long as you never overwrite a cell that you still need to read. The direction in which you walk along the row decides this.

## When it applies

Look for these signals.

- The program fills a table $T[i][j]$ in increasing order of $i$, and the formula for $T[i][j]$ reads only cells $T[i'][j']$ with $i - k \le i' \le i$, for a small fixed $k$. In the [subproblem graph](/subproblem-graph/), each edge goes back at most $k$ rows.
- The problem asks for the optimal value, or the value is enough for the next step of an algorithm.
- The table is large: $n w$ cells do not fit in memory, or the memory traffic makes the program slow.

## The template

The holes are the number $k$ of rows that a row reads, the width $w$ of a row, the base rows, the formula $F$, and the order of the columns inside a row.

```pseudo id=main
ROLLING-FILL(n, k, w)
L1  R[0 .. k][0 .. w] ← an array of k + 1 rows      ▷ ring buffer: row i lives in R[i mod (k + 1)]
L2  for i ← 0 to k − 1 do R[i] ← base row i
L3  for i ← k to n do
L4      cur ← R[i mod (k + 1)]                      ▷ this slot held row i − k − 1, which is no longer needed
L5      for j in the column order do
L6          cur[j] ← F(i, j, R[(i − 1) mod (k + 1)], …, R[(i − k) mod (k + 1)], cur[earlier columns])
L7  return R[n mod (k + 1)]
```

Line L4 is where the space is saved. Row $i$ reads rows $i - 1$ to $i - k$, which live in the other $k$ slots, and it overwrites the slot of row $i - k - 1$, which no later row reads. So the values that line L6 reads are the same values that the full table would hold, and the result is the same. Line L6 must write every cell of the row, or reset it first, because the slot still holds the cells of an old row.

**One row in place.** When $k = 1$ and $T[i][j]$ reads $T[i-1][j']$ only for $j' \le j$, a single row $f$ is enough if the columns go from right to left: when the program writes $f[j]$, the cells $f[j']$ with $j' < j$ still hold row $i - 1$. When $T[i][j]$ reads $T[i-1][j']$ only for $j' \ge j$, the columns must go from left to right. If the formula also reads the current row, the direction must satisfy both needs, or the program keeps one or two old cells in variables.

**The cost.** The time is the same as for the full table. The space is $(k + 1)(w + 1)$ cells, or $w + 1$ cells for the one-row form, plus $O(1)$ variables. When the table has two dimensions of different size, choose the shorter one as the width.

## Classic examples

### Fibonacci numbers

The recurrence $F_i = F_{i-1} + F_{i-2}$ has $k = 2$ and width 1. Two variables are enough: replace $(a, b)$ with $(b, a + b)$ at each step. After 50 steps from $(F_0, F_1) = (0, 1)$, the first variable is $F_{50} = 12586269025$. The space drops from $\Theta(n)$ numbers to two. See [Fibonacci numbers](/fibonacci-numbers/).

### Longest common subsequence length

The table $c[i][j]$ of [LCS](/lcs-dynamic-programming/) reads $c[i-1][j-1]$, $c[i-1][j]$ and $c[i][j-1]$. So two rows of length $\min(m, n) + 1$ are enough: make the shorter string the one along the row. For $X = \mathrm{ABCBDAB}$ and $Y = \mathrm{BDCABA}$, the two-row program returns 4, the same as the full table. With one row, the cell $c[i-1][j-1]$ is overwritten before $c[i][j]$ needs it, so keep it in one extra variable that is saved before each write. This is the $\min(m, n)$ plus $O(1)$ space of CLRS Exercise 14.4-4. The same scheme computes the [edit distance](/edit-distance/) in $O(\min(m, n))$ space.

### 0/1 knapsack with one row

The [knapsack table](/knapsack-dynamic-programming/) is $K[i][c] = \max(K[i-1][c],\ K[i-1][c - w_i] + v_i)$ for $c \ge w_i$. It reads row $i - 1$ at $c$ and at $c - w_i \le c$. So one array $f$ is enough if the capacity goes **down**, from $W$ to $w_i$: when the program writes $f[c]$, the cell $f[c - w_i]$ still holds row $i - 1$.

Take the items $(w, v) = (2, 3), (3, 4), (4, 5)$ and $W = 6$. The array after each item, with the capacity going down:

| after item | $f[0..6]$ |
|---|---|
| $(2, 3)$ | 0, 0, 3, 3, 3, 3, 3 |
| $(3, 4)$ | 0, 0, 3, 4, 4, 7, 7 |
| $(4, 5)$ | 0, 0, 3, 4, 5, 7, 8 |

The answer is 8, from the first and the third item. The space is $W + 1$ cells instead of $(n+1)(W+1)$.

### Unbounded knapsack with one row

If the capacity goes **up** instead, $f[c - w_i]$ already holds row $i$ when $f[c]$ reads it. The loop then computes $K[i][c] = \max(K[i-1][c],\ K[i][c - w_i] + v_i)$, which is the recurrence of the [unbounded knapsack](/unbounded-knapsack/), where each item can be taken again. On the same items, the upward loop gives 0, 0, 3, 3, 6, 6, 9 after the first item and ends with $f[6] = 9$, three copies of $(2, 3)$. The only change between the two problems is the direction of one loop.

### Floyd-Warshall

[Floyd-Warshall](/floyd-warshall/) computes a matrix $D^{(k)}$ from $D^{(k-1)}$ for $k = 1, \ldots, n$. The update of $D^{(k)}[i][j]$ reads $D^{(k-1)}[i][k]$ and $D^{(k-1)}[k][j]$, and these two cells do not change in round $k$ when there is no negative cycle, since a path from $i$ to $k$ does not get shorter through $k$. So one matrix updated in place is enough, and the space is $\Theta(n^2)$ instead of $\Theta(n^3)$.

## Variations

- **Ring buffer of k + 1 rows.** The template above, for a recurrence that reads $k$ rows back, such as $T[i]$ from $T[i-1]$ and $T[i-2]$.
- **Two rows with a swap.** For $k = 1$, keep `prev` and `cur` and swap the two references after each row. Swap the references, do not copy the rows.
- **One row and saved cells.** Overwrite in place and keep in variables the few old cells that the order would destroy, as in LCS.
- **Diagonals.** For [interval DP](/interval-dp/), where the cell $(i, j)$ reads shorter ranges, the natural rows are the diagonals of equal length $j - i$. A range can read ranges much shorter than itself, so this case often does not reduce well.
- **Divide and conquer for the solution.** To get the solution in linear space, run the rolling program forward on the first half of one string and backward on the second half, find the cell where an optimal path crosses the middle row, and recurse on the two parts. This is [Hirschberg's algorithm](/hirschberg-algorithm/) (Hirschberg 1975). Kleinberg and Tardos, Section 6.7, prove that it aligns two strings of lengths $m$ and $n$ in $O(mn)$ time and $O(m + n)$ space. See also [Hirschberg for LCS](/hirschberg-lcs/).
- **Checkpoints.** Keep every $\sqrt{n}$-th row. To trace back, recompute the rows between two checkpoints from the nearer one. This uses $O(\sqrt{n}\, w)$ space and about twice the time.

## Pitfalls

- **No traceback.** The rows that the [traceback](/traceback/) needs are gone. Plan for the solution before you remove the table: keep a compact table of choices, use checkpoints, or use Hirschberg's method.
- **The wrong loop direction.** In the 0/1 knapsack, the upward loop computes the unbounded knapsack. On the items above it returns 9 instead of 8. The bug gives a plausible number, so test against the full table on small inputs.
- **Stale cells.** A reused slot still holds an old row. If the base column, for example $c[i][0] = 0$ in LCS or $D[i][0] = i$ in edit distance, is not written again for each row, the program reads a value from row $i - 2$.
- **Aliasing.** In Python, `prev = cur` makes both names refer to one list. Then the next row overwrites the row it reads. Build a new list, or swap two lists.
- **Rows that read further back than you think.** A recurrence such as $T[i] = \max(T[i-1], T[i - w] + v)$ reads $w$ rows back, not one. Check the largest distance of each edge in the subproblem graph before you choose $k$.
- **The wrong dimension as the width.** Rolling over the longer string keeps rows of the longer length. Put the shorter string along the row.

## Exercises

1. Write the LCS length program with one row of length $\min(m, n) + 1$ and one extra variable. Prove, with a loop invariant on $j$, that before the write of cell $j$ the row holds $c[i][0..j-1]$ and $c[i-1][j..n]$.
2. The bounded knapsack lets item $i$ be taken up to $b_i$ times. Explain why neither loop direction alone gives a one-row program, and give one that is correct.
3. Compute the edit distance of two strings in $O(\min(m, n))$ space. Then show how to output only the *last column* of the full table with the same space, which is what Hirschberg's algorithm needs.
4. For the recurrence $T[i] = T[i-1] + T[i-3]$, how many values must the program keep? Write the ring buffer.
5. Count the number of paths that move right or down through a grid with blocked cells, using one row. In which direction must the columns go? See [grid paths with obstacles](/grid-paths-with-obstacles/).
6. Show that the checkpoint method with $s$ checkpoints rebuilds a traceback of the full table with $O((n/s + s) w)$ space and $O(nw)$ extra time.

## References
