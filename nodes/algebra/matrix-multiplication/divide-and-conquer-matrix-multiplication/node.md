---
tag: 4CTYKM
kind: algorithm
slug: divide-and-conquer-matrix-multiplication
name: Divide-and-conquer matrix multiplication
aliases:
- recursive matrix multiplication
- block recursive matrix multiplication
- MATRIX-MULTIPLY-RECURSIVE
- Simple divide-and-conquer matrix multiplication
area: algebra/matrix-multiplication
level: core
summary: Split each matrix into four blocks and form the product from eight recursive block products; the recurrence T(n) = 8T(n/2) + Θ(1) gives Θ(n^3), the same work as the triple loop.
model: algebraic-computation-tree
complexity:
  vars: {n: the number of rows of A, m: the number of columns of A (the rows of B), p: the number of columns of B}
  time: {worst: Θ(n m p), average: Θ(n m p), best: Θ(n m p)}
  space: {extra: O(log(n m p))}
properties: {deterministic: true, recursive: true, in_place: false}
prereqs: [naive-matrix-multiplication, divide-and-conquer-paradigm, master-theorem]
see_also: [strassen-algorithm, cache-oblivious-matrix-multiplication, blocked-matrix-multiplication, parallel-matrix-multiplication, recursion-tree-method]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.1, Multiplying square matrices (the procedure MATRIX-MULTIPLY-RECURSIVE and the recurrence T(n) = 8T(n/2) + Θ(1))
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms
    locator: Chapter 6, Matrix multiplication and related operations (block partitions of matrices)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition
    locator: Section 1.3, Block matrices and algorithms
---

Divide-and-conquer matrix multiplication cuts each of $A$ and $B$ into four blocks and computes the four blocks of $C = AB$ from eight products of blocks, each done by the same method. Its recurrence $T(n) = 8T(n/2) + \Theta(1)$ solves to $\Theta(n^3)$, so it does exactly the multiplications of the [triple loop](/naive-matrix-multiplication/). Its value is in its shape: it is the starting point of [Strassen's algorithm](/strassen-algorithm/), which replaces the eight products by seven, and of [cache-oblivious](/cache-oblivious-matrix-multiplication/) and [parallel](/parallel-matrix-multiplication/) versions.

## In plain words

Cut each table into four smaller tables: top left, top right, bottom left and bottom right. The top left part of the answer is the top left part of the first table times the top left part of the second, plus the top right part of the first times the bottom left part of the second. The other three parts of the answer follow the same rule. So the answer needs eight products of smaller tables, and each of these is done by cutting again.

The cutting stops when a table has a single number. This method does the same multiplications as the simple method, only in another order. That order keeps the work on small pieces, which fit in fast memory.

## The problem

The input is an $n \times m$ matrix $A$ and an $m \times p$ matrix $B$ over a ring $R$ (commutativity is not needed, and a semiring also works). The output is $C = AB$, with $C[i][j] = \sum_{k} A[i][k] B[k][j]$. The cost counts ring operations; $MM(n)$ is the cost for $n \times n$ matrices. We describe the method as $C \leftarrow C + AB$ on a zero matrix $C$, so that the two products of each block add into the same place.

## The algorithm

Write a matrix with $r$ rows and $c$ columns in blocks with $\lceil r/2 \rceil$ and $\lfloor r/2 \rfloor$ rows and $\lceil c/2 \rceil$ and $\lfloor c/2 \rfloor$ columns:

$$A = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}, \quad B = \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}, \quad C_{rs} = A_{r1} B_{1s} + A_{r2} B_{2s}.$$

The blocks are views: index ranges into the original arrays, so no entry is copied.

```pseudo id=main
DC-MULTIPLY-ADD(A, B, C)                  ▷ C ← C + A·B; A is n × m, B is m × p, C is n × p
L1  if n = 0 or m = 0 or p = 0 then return
L2  if n = 1 and m = 1 and p = 1 then
L3      C[0][0] ← C[0][0] + A[0][0] · B[0][0]
L4      return
L5  split the rows of A and C at ⌈n/2⌉, the columns of A and rows of B at ⌈m/2⌉, the columns of B and C at ⌈p/2⌉
L6  for r ← 1 to 2 do
L7      for s ← 1 to 2 do
L8          DC-MULTIPLY-ADD(A_r1, B_1s, C_rs)
L9          DC-MULTIPLY-ADD(A_r2, B_2s, C_rs)
```

The call DC-MULTIPLY-ADD$(A, B, 0)$ returns $AB$. Line L1 stops on an empty block, which comes from a side of length 1 (its second half is empty). Lines L2 to L4 multiply two single entries. Line L5 makes the block views. Lines L6 to L9 make the eight calls, two for each block of $C$. The first call of each pair handles the first half of the inner index $k$, and the second call the second half, so each entry receives its products in increasing order of $k$.

The split at $\lceil \cdot / 2 \rceil$ handles every size: a side of odd length gives one block one row longer than the other. So the method needs no padding to a power of two.

## Example

Let $A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}$ and $B = \begin{pmatrix} 9 & 8 & 7 \\ 6 & 5 & 4 \\ 3 & 2 & 1 \end{pmatrix}$. Each side has length 3, so line L5 splits it as $2 + 1$. The top level makes these eight calls, in the order of lines L6 to L9.

| call | block product | shape | value |
|---|---|---|---|
| 1 | $A_{11} B_{11}$ | $2 \times 2$ | $\begin{pmatrix} 21 & 18 \\ 66 & 57 \end{pmatrix}$ |
| 2 | $A_{12} B_{21}$ | $2 \times 2$ | $\begin{pmatrix} 9 & 6 \\ 18 & 12 \end{pmatrix}$ |
| 3 | $A_{11} B_{12}$ | $2 \times 1$ | $\begin{pmatrix} 15 \\ 48 \end{pmatrix}$ |
| 4 | $A_{12} B_{22}$ | $2 \times 1$ | $\begin{pmatrix} 3 \\ 6 \end{pmatrix}$ |
| 5 | $A_{21} B_{11}$ | $1 \times 2$ | $(111, 96)$ |
| 6 | $A_{22} B_{21}$ | $1 \times 2$ | $(27, 18)$ |
| 7 | $A_{21} B_{12}$ | $1 \times 1$ | $(81)$ |
| 8 | $A_{22} B_{22}$ | $1 \times 1$ | $(9)$ |

Adding the pairs gives $C_{11} = \begin{pmatrix} 30 & 24 \\ 84 & 69 \end{pmatrix}$, $C_{12} = \begin{pmatrix} 18 \\ 54 \end{pmatrix}$, $C_{21} = (138, 114)$ and $C_{22} = (90)$, so

$$AB = \begin{pmatrix} 30 & 24 & 18 \\ 84 & 69 & 54 \\ 138 & 114 & 90 \end{pmatrix}.$$

Call 1 itself splits its $2 \times 2$ blocks into $1 \times 1$ blocks and makes eight calls of lines L2 to L4. In all, the run makes $27 = 3^3$ base multiplications, one for each triple $(i, j, k)$.

## Correctness

The method is correct by strong induction on $n + m + p$. Block multiplication gives $C_{rs} = A_{r1} B_{1s} + A_{r2} B_{2s}$, because the inner index $k$ of $\sum_k A[i][k] B[k][j]$ runs first over the columns of $A_{r1}$ and then over the columns of $A_{r2}$. Each recursive call has a smaller value of $n + m + p$, so by the hypothesis it adds the right block product to $C_{rs}$. A cleaner way to say it: the eight calls split the set of index triples $\{(i, j, k)\}$ into eight disjoint boxes, and each base call adds the product of one triple. The full proof is in the proofs section.

## Complexity

**Exact count.** Each triple $(i, j, k)$ with $0 \le i < n$, $0 \le k < m$, $0 \le j < p$ reaches line L3 exactly once (this is the partition of the proof). So the method does exactly $nmp$ multiplications and $nmp$ additions, the same as the triple loop.

**Recurrence.** For $n = m = p = 2^t$, the views of line L5 take $\Theta(1)$ time, so

$$T(n) = 8\,T(n/2) + \Theta(1), \qquad T(1) = \Theta(1).$$

Here $a = 8$, $b = 2$ and $n^{\log_b a} = n^3$ grows faster than the $\Theta(1)$ term, so case 1 of the [master theorem](/master-theorem/) gives $T(n) = \Theta(n^3)$. The number of calls is $\sum_{t'=0}^{t} 8^{t'} = (8n^3 - 1)/7$.

**Copies instead of views.** If line L5 copies the blocks into new arrays, and the block sums are formed in new arrays, the recurrence becomes $T(n) = 8T(n/2) + \Theta(n^2)$. This still gives $\Theta(n^3)$, since $n^2$ is polynomially smaller than $n^3$, but the constant grows.

**Space.** The recursion depth is $\lceil \lg \max(n, m, p) \rceil + 1$, and each frame holds $O(1)$ data, so the extra space is $O(\log \max(n, m, p))$ beyond the output.

**General shapes.** For any $n$, $m$, $p$, the time is $\Theta(nmp)$ plus the number of calls. A call either is a base case or has a side of length at least 2, so the number of calls is $O(nmp + 1)$ and the total time is $\Theta(nmp)$ when $nmp > 0$.

## Properties

- **Same arithmetic as the triple loop.** The products and the order in which each entry adds them are the same, so the result is bit for bit the same, even in floating point.
- **No subtraction.** It works over semirings, such as the Boolean and min-plus semirings.
- **Good locality.** At depth $d$, a call works on blocks with about $n/2^d$ rows. Once these fit in a cache, the call runs without further misses. This is the base of the [cache-oblivious](/cache-oblivious-matrix-multiplication/) method.
- **Parallel.** The four blocks of $C$ are independent. Running them in parallel, with the two calls of each block in sequence, gives span $\Theta(n)$ and work $\Theta(n^3)$ in the [work-span model](/work-span-model/).

## Variants and improvements

- **Seven products.** [Strassen's algorithm](/strassen-algorithm/) uses 7 block products and 18 block additions and subtractions, for $\Theta(n^{\log_2 7})$. It needs a ring with subtraction.
- **A cutoff.** Stop the recursion at blocks of, say, 32 to 128 rows and use the [triple loop](/naive-matrix-multiplication/) there. Calls of size 1 cost far more than one multiplication.
- **Split only the longest side.** For rectangular inputs, split only the largest of $n$, $m$, $p$ in two. This keeps the blocks close to square and is the version of Frigo, Leiserson, Prokop and Ramachandran, see [cache-oblivious matrix multiplication](/cache-oblivious-matrix-multiplication/).
- **Parallel with a temporary.** Compute the two products of each block of $C$ into $C$ and a temporary $T$ in parallel, then add. The span drops to $\Theta(\log^2 n)$ at the cost of $\Theta(n^2)$ extra memory at the top level, see [parallel matrix multiplication](/parallel-matrix-multiplication/).

## When to use it

Use it as a step toward Strassen's algorithm, as a cache-friendly order for the classical product without tuning to a cache size, and as a simple parallel product. For speed on one core with known cache sizes, a [blocked](/blocked-matrix-multiplication/) loop with a tuned kernel is faster, since recursion costs time.

## Pitfalls

- **Padding instead of splitting.** Padding an $n \times n$ matrix to the next power of two can almost double each side and multiply the work by almost 8. Split at $\lceil n/2 \rceil$ as in line L5, or peel off one row and column.
- **Overwriting in place of adding.** If line L3 writes $C[0][0] \leftarrow A[0][0] B[0][0]$, the second call of each pair (line L9) erases the first. Each call must add into $C$.
- **No empty-block test.** Without line L1, a side of length 1 gives a block with 0 rows, and the base test of line L2 never holds for it. The recursion then does not stop.
- **Swapped block indices.** $C_{rs}$ needs $A_{r1} B_{1s} + A_{r2} B_{2s}$. Writing $A_{1r}$ or $B_{s1}$ gives a wrong product that still passes tests on symmetric matrices.

## Implementations

## History

The block form of the product is as old as matrix algebra. The recursive method appears in textbooks as the step before Strassen's algorithm; CLRS gives it as MATRIX-MULTIPLY-RECURSIVE. Strassen's 1969 paper showed that the eight block products of this scheme can be replaced by seven.

## References
