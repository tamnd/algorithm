---
tag: FZ993N
kind: algorithm
slug: winograd-inner-product-algorithm
name: Winograd's inner product algorithm
aliases:
- Winograd's commutative trick
- Winograd 1968 algorithm
- Winograd's inner product method
area: algebra/matrix-multiplication
level: advanced
summary: Over a commutative ring, compute the matrix product with about n^3/2 multiplications instead of n^3 by pairing terms of each inner product and precomputing one correction per row and per column.
model: algebraic-computation-tree
complexity:
  vars: {n: the number of rows of A, m: the number of columns of A (the rows of B), p: the number of columns of B}
  time: {worst: Θ(n m p), average: Θ(n m p), best: Θ(n m p)}
  space: {extra: Θ(n + p)}
  multiplications: {worst: (n p + n + p) m/2 + O(n p)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1968
  people: [Shmuel Winograd]
  note: Winograd published the pairing identity for inner products, which halves the multiplications of a matrix product when the entries commute.
prereqs: [naive-matrix-multiplication, dot-product]
see_also: [strassen-algorithm, laderman-algorithm, bilinear-complexity, matrix-multiplication-exponent, matrix-vector-multiplication, karatsuba-multiplication]
sources:
  - paper: doi:10.1109/TC.1968.227420
    title: Shmuel Winograd, A new algorithm for inner product, IEEE Transactions on Computers C-17(7) (1968)
    locator: pp. 693 to 694 (the identity for inner products with a precomputed term per vector, and its use for matrix products)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.4, Evaluation of polynomials (the discussion of Winograd's inner product scheme and the number of multiplications for matrix products)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition
    locator: Chapter 23, Fast Matrix Multiplication (Winograd's method, its error bound, and scaling to make it stable)
---

Winograd's inner product algorithm computes the product of an $n \times m$ and an $m \times p$ matrix over a commutative ring with about $nmp/2$ multiplications instead of the $nmp$ of the [triple loop](/naive-matrix-multiplication/). It pairs the terms of each inner product, so that one multiplication covers two terms plus two error terms, and it removes the error terms with one correction per row of $A$ and one per column of $B$, each computed once and used $p$ or $n$ times. The number of additions grows by about the same amount that the multiplications drop, so the total cost stays $\Theta(nmp)$; the method helps when multiplications cost much more than additions. Because it needs the entries to commute, it cannot be applied to blocks, and so, unlike [Strassen's algorithm](/strassen-algorithm/), it gives no recursion and no lower exponent.

## In plain words

Each entry of a matrix product is a sum of products of pairs of numbers. Take two of these products at a time. Add the first number of one pair to the second number of the other, do the same with the remaining two numbers, and multiply the two sums. The result has the two products you want, plus two unwanted products: one made only from row numbers and one made only from column numbers.

The unwanted products depend on the row alone or on the column alone. So compute them once for each row and once for each column, and subtract them at the end. Each entry then needs about half as many multiplications.

## The problem

The input is $A \in R^{n \times m}$ and $B \in R^{m \times p}$ over a commutative ring $R$. The output is $C = AB$ with $C[i][j] = \sum_{k} A[i][k] B[k][j]$. The cost is counted in ring operations, and the main interest is the number of multiplications. Subtraction is needed, so the method does not work over semirings such as Boolean or min-plus.

## The algorithm

Let $h = \lfloor m/2 \rfloor$. The method rests on the identity, for commuting $x_1, x_2, y_1, y_2$,

$$(x_1 + y_2)(x_2 + y_1) = x_1 y_1 + x_2 y_2 + x_1 x_2 + y_1 y_2.$$

With $x_1 = A[i][2t]$, $x_2 = A[i][2t+1]$, $y_1 = B[2t][j]$ and $y_2 = B[2t+1][j]$, the first two terms are the wanted products, $x_1 x_2$ depends only on row $i$, and $y_1 y_2$ only on column $j$.

```pseudo id=main
WINOGRAD-PRODUCT(A, B)                     ▷ A is n × m, B is m × p, R commutative
L1  h ← ⌊m / 2⌋
L2  for i ← 0 to n − 1 do ξ_i ← Σ_(t<h) A[i][2t] · A[i][2t+1]
L3  for j ← 0 to p − 1 do η_j ← Σ_(t<h) B[2t][j] · B[2t+1][j]
L4  for i ← 0 to n − 1 do for j ← 0 to p − 1 do
L5      s ← −ξ_i − η_j
L6      for t ← 0 to h − 1 do s ← s + (A[i][2t] + B[2t+1][j]) · (A[i][2t+1] + B[2t][j])
L7      if m is odd then s ← s + A[i][m−1] · B[m−1][j]
L8      C[i][j] ← s
L9  return C
```

Lines L2 and L3 compute the corrections: $\xi_i$ for each row of $A$ and $\eta_j$ for each column of $B$. Lines L5 and L6 compute the paired sum for entry $(i, j)$, starting from the negated corrections. Line L7 adds the unpaired last term when $m$ is odd.

## Example

Let $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ and $B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}$, so $m = 2$ and $h = 1$. Line L2 gives $\xi_0 = 1 \cdot 2 = 2$ and $\xi_1 = 3 \cdot 4 = 12$. Line L3 gives $\eta_0 = 5 \cdot 7 = 35$ and $\eta_1 = 6 \cdot 8 = 48$. Then

| entry | paired product (L6) | minus $\xi_i + \eta_j$ | $C[i][j]$ |
|---|---|---|---|
| $(0, 0)$ | $(1 + 7)(2 + 5) = 56$ | $2 + 35 = 37$ | $19$ |
| $(0, 1)$ | $(1 + 8)(2 + 6) = 72$ | $2 + 48 = 50$ | $22$ |
| $(1, 0)$ | $(3 + 7)(4 + 5) = 90$ | $12 + 35 = 47$ | $43$ |
| $(1, 1)$ | $(3 + 8)(4 + 6) = 110$ | $12 + 48 = 60$ | $50$ |

So $C = \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix}$, which is $AB$. Here the method uses $4 + 2 + 2 = 8$ multiplications, the same as the triple loop: the corrections pay off only for larger sizes. For $n = m = p = 4$ it uses $32 + 8 + 8 = 48$ instead of $64$, and for $n = m = p = 100$ it uses $510000$ instead of $10^6$.

## Correctness

Fix $i$ and $j$. Summing the identity over $t < h$ gives

$$\sum_{t<h} (A[i][2t] + B[2t+1][j])(A[i][2t+1] + B[2t][j]) = \sum_{k < 2h} A[i][k] B[k][j] + \xi_i + \eta_j,$$

where commutativity is used to write $B[2t+1][j] A[i][2t+1]$ as $A[i][2t+1] B[2t+1][j]$ and $B[2t+1][j] B[2t][j]$ as $B[2t][j] B[2t+1][j]$. Lines L5 and L6 subtract $\xi_i + \eta_j$, and line L7 adds the term $k = m - 1$ when $m$ is odd, so $s = C[i][j]$. All loops are bounded, so the method stops. The full proof is in the proofs section.

## Complexity

- **Multiplications.** Line L2 makes $nh$, line L3 makes $ph$, line L6 makes $nph$, and line L7 makes $np$ when $m$ is odd. The total is $(np + n + p) \lfloor m/2 \rfloor + np\,(m \bmod 2)$. For $n = m = p$ even it is $n^3/2 + n^2$, against $n^3$ for the triple loop.
- **Additions and subtractions.** Line L6 makes $3$ per term, lines L2 and L3 make $h - 1$ per row or column, line L5 makes $2$ per entry, and line L7 one more when $m$ is odd. For $n = m = p$ even this is $\frac{3}{2} n^3 + O(n^2)$, against $n^3 - n^2$ for the triple loop.
- **Total.** About $2n^3$ ring operations, the same as the triple loop, so the time is $\Theta(nmp)$ in every case. The method moves work from multiplications to additions.
- **Space.** $\Theta(n + p)$ for the corrections, besides the output.

## Properties

- **Needs commutativity.** The proof swaps factors twice. Over matrices of matrices, or quaternions, the method gives wrong results, so it cannot be used inside a block recursion.
- **Not bilinear.** The products in line L6 multiply sums that mix entries of $A$ and $B$, and those of lines L2 and L3 multiply two entries of the same matrix. So it is a quadratic algorithm, not a bilinear one, and it does not bound the [tensor rank](/tensor-rank/) of matrix multiplication.
- **Deterministic and exact** over each commutative ring.

## Variants and improvements

- **Matrix-vector and single inner products.** For one inner product the correction terms cost as much as the saving, so the method helps only when each correction is reused, that is, for many inner products with the same vectors, as in a matrix product.
- **Why many inner products are needed.** Winograd (1970) proved that the classical count of $nm$ multiplications is optimal for a single matrix-vector product with independent entries, so a saving needs many inner products that share their vectors, as in a matrix product.
- **Use inside fast methods.** At the base of a recursion of Strassen's kind, the blocks are scalars, so Winograd's method can be applied at the base level on scalars only.
- **Fixed-point arithmetic and hardware.** The method suits settings where multiplication is much more expensive than addition, such as arithmetic on long integers or some digital signal processors.

## When to use it

Use it over commutative rings where a multiplication costs much more than an addition, for example matrices of large integers or of polynomials, and when $n$ and $p$ are not tiny, so that the corrections are reused. Do not use it with floating-point numbers of very different sizes in $A$ and $B$ without scaling, and do not use it for blocks of matrices.

## Pitfalls

- **Block matrices.** The method is wrong for matrices whose entries do not commute. It cannot replace the scalar multiplications inside a recursion on blocks.
- **Odd inner dimension.** Without line L7, the last term is lost when $m$ is odd.
- **Rounding.** In floating-point arithmetic, the sum $A[i][2t] + B[2t+1][j]$ mixes entries of the two matrices. If they differ greatly in size, the small one is lost and the error bound depends on $\max |A| \cdot \max |B|$ through the products of sums, not on $|A| |B|$ entrywise. Scaling $B$ by a power of two so that the two matrices have similar norms restores a usable bound.
- **Overflow.** The paired products and the corrections can be much larger than the entries of $C$, which matters for fixed-width integers.

## Implementations

## History

Winograd published the method in 1968, a year before Strassen's algorithm, as a way to compute inner products with about half the multiplications when many of them share their vectors. It was the first algorithm for matrix products with fewer than $n^3$ multiplications, but it needs commutativity and so does not lower the exponent. Its numerical behavior and the effect of scaling were studied later, and Higham's book summarizes the analysis.

## References
