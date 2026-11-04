---
tag: V8AHMD
kind: algorithm
slug: smawk-algorithm
name: SMAWK algorithm
aliases:
- SMAWK
- matrix searching algorithm
area: techniques/dynamic-programming
level: research
summary: Find all row minima of a totally monotone n by m matrix in O(n + m) evaluations.
solves: [row-minima-of-totally-monotone-matrices]
model: word-ram
complexity:
  vars: {n: the number of rows, m: the number of columns}
  time: {worst: Θ(n + m), average: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: true}
history:
  year: 1987
  people: [Alok Aggarwal, Maria M. Klawe, Shlomo Moran, Peter Shor, Robert Wilber]
  note: The name is formed from the initials of the five authors of the 1987 paper in Algorithmica.
prereqs: [row-minima-of-totally-monotone-matrices, monge-property]
see_also: [monge-property, divide-and-conquer-optimization, knuth-optimization, optimal-text-wrapping, convex-hull-trick]
sources:
  - paper: doi:10.1007/BF01840359
    title: Alok Aggarwal, Maria M. Klawe, Shlomo Moran, Peter Shor and Robert Wilber, Geometric applications of a matrix-searching algorithm, Algorithmica 2, 195-208, 1987
    locator: the matrix-searching algorithm (the procedure REDUCE and the recursion on half of the rows) and its geometric applications
  - paper: doi:10.1016/0166-218X(95)00103-X
    title: Rainer E. Burkard, Bettina Klinz and Rüdiger Rudolf, Perspectives of Monge properties in optimization, Discrete Applied Mathematics 70(2), 95-161, 1996
    locator: the section on row minima of Monge and totally monotone matrices
  - paper: doi:10.1016/0304-3975(92)90135-3
    title: Zvi Galil and Kunsoo Park, Dynamic programming with convexity, concavity and sparsity, Theoretical Computer Science 92(1), 49-76, 1992
    locator: the use of matrix searching as a subroutine for one-dimensional dynamic programs
---

The SMAWK algorithm finds the leftmost minimum of every row of a totally monotone matrix with $n$ rows and $m$ columns in $O(n + m)$ time. It reads only $O(n + m)$ entries, so it is used when the entries are not stored but computed on demand from a formula. Each [Monge](/monge-property/) matrix is totally monotone, and this makes SMAWK the fastest tool for many [dynamic programs with a Monge cost](/divide-and-conquer-optimization/) and for problems of geometry on convex polygons. It solves the [row minima problem](/row-minima-of-totally-monotone-matrices/) in optimal time.

## In plain words

Think of a large table of numbers that you cannot see at once. You can ask for one cell at a time, and you want the smallest number of each row. In a general table you must ask for every cell. The tables here have a special order: the place of the smallest number moves to the right, never to the left, as you go down the rows. And a stronger rule holds for each pair of rows and each pair of columns.

The method uses two ideas. First, when there are more columns than rows, a quick left-to-right pass throws away columns that cannot hold any answer, until no more columns than rows are left. Second, it solves every second row by the same method. The rows in between then only need a short search, because each answer lies between the answers of the rows above and below it.

## The problem

Let $A$ be an $n \times m$ matrix, $n \ge 1$ and $m \ge 1$, with entries from a totally ordered set, given by a function that returns $A[i][j]$ in $O(1)$ time. For row $i$, let $j(i)$ be the smallest column index $j$ such that $A[i][j]$ is a minimum of row $i$. The matrix is *totally monotone* when for all rows $i < i'$ and columns $j < j'$:

$$A[i][j] > A[i][j'] \implies A[i'][j] > A[i'][j'].$$

In words: if the right column wins strictly in an upper row, it also wins strictly in each lower row. The output is $j(i)$ for every row. See the [problem page](/row-minima-of-totally-monotone-matrices/) for the background and the [Monge property](/monge-property/) for the main source of such matrices.

Two facts follow from the definition. Every submatrix, made of some rows and some columns in their order, is again totally monotone, because its $2 \times 2$ submatrices are among those of $A$. And the leftmost minima are monotone: $j(1) \le j(2) \le \cdots \le j(n)$. For the second fact, take $i < i'$ and suppose $j' = j(i') < j = j(i)$. Then $A[i][j'] > A[i][j]$, because $j$ is the leftmost minimum of row $i$. Total monotonicity gives $A[i'][j'] > A[i'][j]$, so $j'$ is not a minimum of row $i'$, a contradiction.

## The algorithm

Rows and columns are passed as lists of indices in increasing order. A list is indexed from 0. SMAWK$(A, [0, \ldots, n-1], [0, \ldots, m-1])$ returns the map from each row to $j(i)$.

```pseudo id=main
SMAWK(A, R, C)                      ▷ R: rows in order, C: columns in order
L1  if R is empty then return the empty map
L2  C ← REDUCE(A, R, C)              ▷ now |C| ≤ |R|
L3  R′ ← R[1], R[3], R[5], …         ▷ the rows at odd positions
L4  M ← SMAWK(A, R′, C)
L5  k ← 0
L6  for i ← 0, 2, 4, … while i < |R| do
L7      stop ← the position of M[R[i + 1]] in C if i + 1 < |R|, else |C| − 1
L8      M[R[i]] ← the leftmost column c among C[k], …, C[stop] with the least A[R[i]][c]
L9      k ← stop
L10 return M

REDUCE(A, R, C)                     ▷ drop the columns that hold no leftmost minimum
L11 S ← an empty stack
L12 for each column c of C, in order do
L13     while S is not empty and A[R[|S| − 1]][top(S)] > A[R[|S| − 1]][c] do pop S
L14     if |S| < |R| then push c on S
L15 return S, from bottom to top
```

REDUCE keeps a stack $S$ of columns. The column at position $t$ of the stack (from the bottom, starting at 0) is compared on row $R[t]$. When a new column $c$ beats the top column strictly on the row of the top, the top column cannot be the leftmost minimum of that row or of any lower row, by total monotonicity, and it cannot be one of a higher row, by the invariant of the proof. So it is popped. When the stack holds $|R|$ columns and the new column does not beat the top on the last row, the new column loses on the last row and so on each row, and it is dropped. At the end $|S| \le |R|$.

The recursion solves the rows at odd positions on the reduced columns. Then lines L5 to L9 fill in the rows at even positions. By monotonicity, the answer for $R[i]$ lies between the answers of $R[i-1]$ and $R[i+1]$. The search of line L8 starts where the previous one stopped, so the ranges of all even rows overlap only at their ends.

## Example

Take $A[i][j] = (x_i - y_j)^2 + u_j$ with $x = (1, 2, 4, 5, 7)$, $y = (0, 1, \ldots, 6)$ and $u = (9, 4, 6, 0, 7, 3, 5)$. It is a Monge matrix, because $x$ and $y$ are increasing and $u_j$ depends on the column only, so it is totally monotone.

| row | col 0 | col 1 | col 2 | col 3 | col 4 | col 5 | col 6 | $j(i)$ |
|---|---|---|---|---|---|---|---|---|
| 0 | 10 | **4** | 7 | 4 | 16 | 19 | 30 | 1 |
| 1 | 13 | 5 | 6 | **1** | 11 | 12 | 21 | 3 |
| 2 | 25 | 13 | 10 | **1** | 7 | 4 | 9 | 3 |
| 3 | 34 | 20 | 15 | 4 | 8 | **3** | 6 | 5 |
| 4 | 58 | 40 | 31 | 16 | 16 | 7 | **6** | 6 |

Row 0 has the minimum 4 in columns 1 and 3, and the leftmost one, column 1, is the answer.

**REDUCE on rows 0 to 4, all 7 columns.**

| column | test of line L13 | stack after it |
|---|---|---|
| 0 | stack empty | [0] |
| 1 | row 0: $10 > 4$, pop 0 | [1] |
| 2 | row 0: $4 > 7$ is false | [1, 2] |
| 3 | row 1: $6 > 1$, pop 2; row 0: $4 > 4$ is false | [1, 3] |
| 4 | row 1: $1 > 11$ is false | [1, 3, 4] |
| 5 | row 2: $7 > 4$, pop 4; row 1: $1 > 12$ is false | [1, 3, 5] |
| 6 | row 2: $4 > 9$ is false | [1, 3, 5, 6] |

**Recursion on rows 1 and 3, columns [1, 3, 5, 6].** REDUCE pushes 1, pops it for 3 (row 1: $5 > 1$), pushes 5, and drops 6 because the stack is full and row 3 gives $3 > 6$ false. The columns are [3, 5]. The next level, on row 3 alone, keeps column 5 (row 3: $4 > 3$ pops 3), so $j(3) = 5$. Back on rows 1 and 3, row 1 searches columns 3 to 5 of [3, 5] and finds $j(1) = 3$.

**Top level.** Row 0 searches [1, 3], the columns up to $j(1) = 3$, and finds column 1 (the tie with column 3 goes to the left). Row 2 searches from column 3 to $j(3) = 5$, that is [3, 5], and finds 3. Row 4 searches from 5 to the last column, [5, 6], and finds 6. The result is $j = (1, 3, 3, 5, 6)$.

## Correctness

The proof has two parts. REDUCE drops only columns that hold no leftmost minimum. Its invariant is: the column at position $t$ of the stack is not the leftmost minimum of any of the rows $R[0], \ldots, R[t-1]$, because some column to its left has a value at most as large on each of them. The interpolation of lines L5 to L9 is correct because the leftmost minima are monotone and the reduced matrix keeps them. Both parts and the induction on the number of rows are in the proof file below.

## Complexity

Count the entries that the algorithm reads.

- **REDUCE.** Each test of line L13 either pops a column or ends the loop for the current column. Each column is pushed at most once, so there are at most $|C|$ pops, and at most $|C|$ tests end a loop. So REDUCE reads at most $4|C|$ entries and takes $O(|C|)$ time.
- **Interpolation.** For the even position $i$, line L8 reads $stop - k + 1$ entries. The values of $k$ follow on from each other, so the sum over all even positions is at most $|C| + \lceil |R|/2 \rceil$.

After line L2, $|C| \le |R|$. Let $T(r, c)$ be the number of reads on $r$ rows and $c$ columns. Then

$$T(r, c) \le 4c + 2r + T(\lfloor r/2 \rfloor, r),$$

and at the recursion level $\ell \ge 1$ the cost outside the recursive call is at most $5n / 2^{\ell - 1}$. The geometric sum gives $T(n, m) \le 4m + 12n$, which is $O(n + m)$. The derivation is in the complexity proof below. The bound is tight. For $n = 1$, every row of $m$ values is totally monotone, and an unread entry could be the only minimum, so each algorithm must read all $m$ entries. The output has $n$ entries. So the time is $\Theta(n + m)$ in the worst case. The extra space is $O(n + m)$ for the stacks and the map, and the recursion has depth $\lceil \lg n \rceil$ or less.

## Properties

- **Leftmost minima.** The strict test in line L13 and the strict improvement in line L8 give the leftmost minimum of each row. For a Monge matrix, the rightmost minima come from a run on the matrix with both the rows and the columns in reverse order, which is again a Monge matrix.
- **Offline.** All entries must be available when asked for. A dynamic program in which row $i$ needs the answers of rows before $i$ breaks this. The online variants on the [problem page](/row-minima-of-totally-monotone-matrices/) handle that case.
- **Few evaluations.** It reads $O(n + m)$ of the $nm$ entries. When an entry is costly to compute, this is the main gain.
- **Maxima.** The row maxima of $A$ are the row minima of $-A$, so SMAWK finds them when $-A$ is totally monotone.

## Variants and improvements

- **Divide and conquer.** Find the minimum of the middle row by a full scan, then recurse on the upper half with the columns to the left and the lower half with the columns to the right. This takes $O(m \log n + n)$ time and needs only monotone minima, a weaker condition than total monotonicity. It is the method of [divide and conquer optimization](/divide-and-conquer-optimization/).
- **Online searching.** For the concave [least weight subsequence](/optimal-text-wrapping/) problem, the row $i$ becomes known only after the minima of earlier rows. Wilber, Galil and Park, and Larmore and Schieber adapted SMAWK to this case with $O(n)$ total time.
- **Partial matrices.** When some entries are undefined, in a staircase shape, Klawe and Kleitman give an almost linear algorithm.
- **Column minima.** Transposing a Monge matrix gives a Monge matrix, so the same code finds the column minima.

## When to use it

Use SMAWK when the entries are computed on demand, all rows are known in advance, and the matrix is totally monotone, for example a Monge matrix. Typical uses are all farthest neighbors of the vertices of a convex polygon, one layer of a layered dynamic program with a Monge cost, and the inner step of many algorithms on Monge matrices. When the rows are known only one by one, or when the matrix only has monotone minima, use divide and conquer, which is simpler and only a factor $\log n$ slower. For small matrices, the constant factor of SMAWK can make the plain scan faster.

## Pitfalls

- **A non-strict test in REDUCE.** With $\ge$ instead of $>$ in line L13, a tie pops the left column, and a row whose two equal minima are the top and the new column gets the right one. Then line L8 may return a column that is not the leftmost minimum. On the example, row 0 then gets column 3.
- **The wrong row in line L13.** The top of the stack must be compared on row $R[|S| - 1]$, the row of its position, not on the last row or on a fixed row. Another row breaks the invariant.
- **A matrix that is only monotone.** SMAWK needs total monotonicity for every $2 \times 2$ submatrix. Take the rows $(0, 3, 3)$, $(1, 4, 1)$ and $(4, 2, 3)$. The leftmost minima are in columns 0, 0 and 1, which is monotone, but rows 1 and 2 with columns 1 and 2 break total monotonicity. REDUCE drops column 1, and SMAWK returns column 2 for the last row, whose minimum is in column 1. Check the condition, or use the divide and conquer method.
- **The search range of line L8.** The range is from the answer of the row above to the answer of the row below, both included. Searching to $stop - 1$ misses the case where both rows have the same answer.

## Implementations

## History

Alok Aggarwal, Maria Klawe, Shlomo Moran, Peter Shor and Robert Wilber gave the algorithm in a paper in Algorithmica in 1987, with applications to problems of geometry such as all farthest neighbors of a convex polygon. The algorithm is named from the initials of their surnames. Burkard, Klinz and Rudolf survey its role among the algorithms for Monge matrices.

## References
