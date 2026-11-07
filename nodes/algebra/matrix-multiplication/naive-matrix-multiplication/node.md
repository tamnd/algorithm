---
tag: F9X6P7
kind: algorithm
slug: naive-matrix-multiplication
name: Naive matrix multiplication
aliases:
- schoolbook matrix multiplication
- triple-loop matrix multiplication
- classical matrix multiplication
- definition-based matrix multiplication
area: algebra/matrix-multiplication
level: intro
summary: Compute each entry of the product AB as the dot product of a row of A and a column of B, with three nested loops and n m p multiplications.
model: algebraic-computation-tree
complexity:
  vars: {n: the number of rows of A, m: the number of columns of A (the rows of B), p: the number of columns of B}
  time: {worst: Θ(n m p), average: Θ(n m p), best: Θ(n m p)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1858
  people: [Arthur Cayley]
  note: Cayley defined the product of two matrices by this rule in his memoir on the theory of matrices.
prereqs: [dot-product, asymptotic-notation, loop-invariant]
see_also: [strassen-algorithm, divide-and-conquer-matrix-multiplication, blocked-matrix-multiplication, matrix-vector-multiplication, winograd-inner-product-algorithm, matrix-multiplication-exponent, matrix-multiplication-quadratic-lower-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.1, Multiplying square matrices (the procedure MATRIX-MULTIPLY and its Θ(n^3) bound)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition
    locator: Section 1.1, Basic algorithms and notation (the dot product and saxpy forms and the six loop orders), and Section 1.5, Vectorization and locality
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.4, Evaluation of polynomials (the part on matrix multiplication and bilinear forms)
  - paper: doi:10.1098/rstl.1858.0002
    title: Arthur Cayley, A memoir on the theory of matrices, Philosophical Transactions of the Royal Society of London 148, 1858
    locator: pp. 17 to 37 (the definition of the product of two matrices)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition
    locator: Section 3.5, Matrix multiplication (the rounding error bound of the classical product)
---

Naive matrix multiplication computes the product $C = AB$ of an $n \times m$ matrix $A$ and an $m \times p$ matrix $B$ straight from the definition: the entry $C[i][j]$ is the [dot product](/dot-product/) of row $i$ of $A$ and column $j$ of $B$. Three nested loops do $nmp$ multiplications and $nmp$ additions, so two $n \times n$ matrices take $\Theta(n^3)$ ring operations. It works over any ring, it needs no subtraction, and it works unchanged over semirings such as the Boolean and the min-plus semiring. It is the reference against which every faster method, such as [Strassen's algorithm](/strassen-algorithm/), is checked.

## In plain words

Write the first matrix as a stack of rows and the second as a row of columns. To fill one cell of the answer, take the matching row of the first matrix and the matching column of the second. Multiply the first number of the row by the first number of the column, the second by the second, and so on, and add up these products. Do this for each cell.

Each cell needs one pass along a row and a column. For two square tables with the same number of rows, the work grows with the cube of that number: twice as many rows means eight times the work.

## The problem

**Notation used on all matrix multiplication pages.** $R$ is a ring with $0$ and $1$. It need not be commutative unless a page says so. $A$ is an $n \times m$ matrix and $B$ is an $m \times p$ matrix over $R$, with entries $A[i][k]$ for $0 \le i < n$, $0 \le k < m$. The product is the $n \times p$ matrix

$$C[i][j] = \sum_{k=0}^{m-1} A[i][k] \, B[k][j], \qquad 0 \le i < n,\ 0 \le j < p.$$

For square matrices, $MM(n)$ is the number of ring operations that a method needs for $n \times n$ matrices, and $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/). The cost model counts ring operations ($+$, $-$, $\times$) as one step each, as in a [straight-line program](/straight-line-program/), which is an [algebraic computation tree](/algebraic-computation-tree/) with no branch nodes. Reading and writing entries is free in this model. On a real machine with fixed-width numbers, the same count is the time on the [word RAM](/word-ram/) up to a constant factor.

When $m = 0$, each sum is empty, so $C$ is the $n \times p$ zero matrix.

## The algorithm

```pseudo id=main
MATRIX-MULTIPLY(A, B)                    ▷ A is n × m, B is m × p
L1  C ← a new n × p matrix
L2  for i ← 0 to n − 1 do
L3      for j ← 0 to p − 1 do
L4          s ← 0
L5          for k ← 0 to m − 1 do
L6              s ← s + A[i][k] · B[k][j]
L7          C[i][j] ← s
L8  return C
```

Lines L2 and L3 visit each cell $(i, j)$ of the result. Lines L4 to L6 compute the dot product of row $i$ of $A$ and column $j$ of $B$ in the variable $s$. Line L7 stores it. The order of the factors in line L6 matters when $R$ is not commutative: the entry of $A$ comes first.

The three loops can run in any of the six orders $ijk$, $ikj$, $jik$, $jki$, $kij$, $kji$. Each order does the same multiplications and gives the same result, because each order adds the same products into each $C[i][j]$, in increasing order of $k$. The orders differ only in the way they access memory (see Variants).

## Example

Let

$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix}, \qquad B = \begin{pmatrix} 7 & 8 \\ 9 & 10 \\ 11 & 12 \end{pmatrix}.$$

Here $n = 2$, $m = 3$ and $p = 2$. The table gives, for each cell, the three products of line L6 and the value of $s$ after each step of the loop of line L5.

| cell $(i, j)$ | products $A[i][k] B[k][j]$ for $k = 0, 1, 2$ | $s$ after each step | $C[i][j]$ |
|---|---|---|---|
| (0, 0) | 7, 18, 33 | 7, 25, 58 | 58 |
| (0, 1) | 8, 20, 36 | 8, 28, 64 | 64 |
| (1, 0) | 28, 45, 66 | 28, 73, 139 | 139 |
| (1, 1) | 32, 50, 72 | 32, 82, 154 | 154 |

So $AB = \begin{pmatrix} 58 & 64 \\ 139 & 154 \end{pmatrix}$. The method did $2 \cdot 3 \cdot 2 = 12$ multiplications and 12 additions.

## Correctness

The loop of line L5 keeps the [loop invariant](/loop-invariant/) $s = \sum_{t=0}^{k-1} A[i][t] B[t][j]$. At the start $k = 0$ and $s = 0$, the empty sum. Line L6 adds the term for $t = k$. When the loop ends, $k = m$ and $s$ is the full sum, so line L7 stores the correct value of $C[i][j]$. Lines L2 and L3 reach each pair $(i, j)$ exactly one time, so each entry of $C$ is correct. All loops have fixed bounds, so the procedure stops. The full proof is in the proofs section.

The proof uses only the ring laws for addition ($0$ is neutral, $+$ is associative). It never uses commutativity of $\times$ or subtraction. So the same procedure is correct over any semiring, with $+$ and $\cdot$ replaced by the semiring operations and $0$ by the neutral element of the semiring addition.

## Complexity

Line L6 runs once for each triple $(i, j, k)$, so it runs $nmp$ times. Each run does one multiplication and one addition. Lines L4 and L7 run $np$ times. So the method does exactly $nmp$ multiplications and $nmp$ additions. If line L4 starts $s$ with the first product, the additions drop to $np(m - 1)$. For $n \times n$ matrices this gives $n^3$ multiplications and $n^3 - n^2$ additions, $2n^3 - n^2$ operations in all.

- The time is $\Theta(nmp)$ in each case: the work does not depend on the values. For square matrices this is $MM(n) = \Theta(n^3)$.
- The extra space is $\Theta(1)$ beyond the output $C$: the variables $i$, $j$, $k$ and $s$.
- The output has $np$ entries, and the input has $nm + mp$ entries, so no method can take less than $\Omega(nm + mp + np)$ time on a RAM. For square matrices the gap between $n^2$ and $n^3$ is where all fast methods live (see the [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/)).

The count of multiplications is optimal for some formats. A $1 \times m$ times $m \times 1$ product (a dot product) over a ring where the algorithm cannot use commutativity needs $m$ multiplications. But for $n \times n$ matrices with $n \ge 2$, [Strassen's algorithm](/strassen-algorithm/) shows that $n^3$ is not optimal.

## Properties

- **Any ring, any semiring.** No subtraction, no division and no commutativity is used. This is why the Boolean product and the min-plus product, which have no subtraction, can always use this method.
- **Not in place.** $C$ must not share memory with $A$ or $B$: line L7 writes $C[i][j]$ while later steps still read row $i$ of $A$ and column $j$ of $B$.
- **Data-oblivious.** The sequence of operations depends only on $n$, $m$ and $p$, not on the values.
- **Exact over the integers.** Over $\mathbb{Z}$ the result is exact. Over floating point numbers, each entry has the error bound of a dot product of length $m$: $|\hat C - C| \le \gamma_m |A||B|$ entrywise, with $\gamma_m = m u / (1 - m u)$ and unit roundoff $u$.

## Variants and improvements

- **Loop order.** In a row-major array, the order $ikj$ (fix $a = A[i][k]$, then add $a \cdot B[k][j]$ to $C[i][j]$ for all $j$) reads $B$ and writes $C$ row by row. The order $ijk$ reads $B$ down a column, which jumps in memory. On a cached machine $ikj$ is often several times faster than $ijk$ for large $n$, though both do the same arithmetic.
- **Blocking.** Cut the matrices into tiles that fit in the cache and multiply tile by tile. This is [blocked matrix multiplication](/blocked-matrix-multiplication/). The [cache-oblivious](/cache-oblivious-matrix-multiplication/) version gets the same effect by recursion.
- **Recursive form.** The [divide and conquer](/divide-and-conquer-matrix-multiplication/) method splits each matrix into four blocks and does 8 recursive products. It does the same $n^3$ multiplications.
- **Fewer multiplications for commutative rings.** [Winograd's inner product algorithm](/winograd-inner-product-algorithm/) uses about $n^3/2$ multiplications, at the cost of more additions.
- **Fewer operations in total.** [Strassen's algorithm](/strassen-algorithm/) uses 7 products of half size instead of 8, for $O(n^{\log_2 7})$ operations. It needs subtraction.
- **Sparse matrices.** When most entries are zero, skip the zero products. See [sparse matrix multiplication](/sparse-matrix-multiplication/).

## When to use it

Use it for small matrices, for rectangular matrices with one small side, for semirings without subtraction, and as the base case of the recursive methods. Tuned libraries (BLAS routines such as GEMM) still do the $\Theta(n^3)$ operations of this method, with blocking, vector instructions and many cores, and on current machines they beat Strassen-type methods for small and medium sizes. Use a fast method only when $n$ is large, the ring has subtraction, and the numerical or overflow effects are acceptable.

## Pitfalls

- **Writing into an input.** Calling the procedure with $C$ equal to $A$ (for example to square a matrix in place) changes row $i$ of $A$ while line L6 still reads it. Allocate a new matrix in line L1.
- **Wrong factor order.** Writing $B[k][j] \cdot A[i][k]$ in line L6 is wrong when $R$ is not commutative, for example when the entries are themselves matrices, as in a blocked product.
- **Wrong shapes.** The number of columns of $A$ must equal the number of rows of $B$. When $m = 0$ the result is the $n \times p$ zero matrix, and the code must still know $p$.
- **Overflow.** With 64-bit integers, an entry of $C$ can reach $m \cdot \max|A| \cdot \max|B|$. Reduce modulo $q$ after each step of line L6 when working in $\mathbb{Z}/q\mathbb{Z}$.
- **Slow loop order.** The order $ijk$ on row-major arrays is slow on large inputs. Use $ikj$, or block the loops.

## Implementations

## History

Arthur Cayley defined the product of two matrices by this rule in 1858, as the matrix of the composition of two linear maps. For more than a century, the definition was also taken as the way to compute the product. In 1969 Volker Strassen showed with his [algorithm](/strassen-algorithm/) that $\Theta(n^3)$ operations are not necessary.

## References
