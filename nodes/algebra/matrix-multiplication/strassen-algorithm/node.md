---
tag: MZ8PBV
kind: algorithm
slug: strassen-algorithm
name: Strassen's algorithm
aliases:
- Strassen multiplication
- Strassen matrix multiplication
- Strassen's method
area: algebra/matrix-multiplication
level: core
summary: Multiply 2 by 2 block matrices with seven recursive block products instead of eight, which gives n^(log2 7) multiplications and O(n^(log2 7)) ring operations, about n^2.807.
model: algebraic-computation-tree
complexity:
  vars: {n: the order of the matrices}
  time: {worst: Θ(n^(log2 7)), average: Θ(n^(log2 7)), best: Θ(n^(log2 7))}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: true, in_place: false}
history:
  year: 1969
  people: [Volker Strassen]
  note: Strassen published the seven-product scheme in a short paper titled Gaussian elimination is not optimal.
prereqs: [divide-and-conquer-matrix-multiplication, master-theorem]
see_also: [naive-matrix-multiplication, matrix-multiplication-exponent, bilinear-complexity, tensor-rank, laderman-algorithm, parallel-strassen, coppersmith-winograd-algorithm, alphatensor]
sources:
  - paper: doi:10.1007/BF02165411
    title: Volker Strassen, Gaussian elimination is not optimal, Numerische Mathematik 13, 1969
    locator: pp. 354 to 356 (the seven products, the bound 4.7 n^(log2 7), and the consequences for inversion and determinants)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.2, Strassen's algorithm for matrix multiplication
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition
    locator: Chapter 23, Fast matrix multiplication (the operation counts, the Winograd variant and the normwise error bounds)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.4, Evaluation of polynomials (Strassen's scheme, the Winograd form with 15 additions, and tensor rank)
  - paper: "Shmuel Winograd, On multiplication of 2 × 2 matrices, Linear Algebra and its Applications 4 (1971)"
    locator: pp. 381 to 388 (7 multiplications are necessary, and the variant with 15 additions)
  - paper: "John E. Hopcroft and Leslie R. Kerr, On minimizing the number of multiplications necessary for matrix multiplication, SIAM Journal on Applied Mathematics 20(1), 1971"
    locator: pp. 30 to 36 (7 multiplications are necessary for 2 by 2 matrices without commutativity)
  - paper: "Robert L. Probert, On the additive complexity of matrix multiplication, SIAM Journal on Computing 5(2), 1976"
    locator: pp. 187 to 203 (15 additions are necessary for a 7-product scheme for 2 by 2 matrices)
  - paper: "Elaye Karstadt and Oded Schwartz, Matrix multiplication, a little faster, Journal of the ACM 67(1), 2020"
    locator: the alternative basis method and the leading coefficient 5 (first in SPAA 2017)
---

Strassen's algorithm multiplies two $n \times n$ matrices over a ring by splitting each into four blocks and forming the product from 7 block products instead of the 8 of the [divide-and-conquer method](/divide-and-conquer-matrix-multiplication/). The recurrence $T(n) = 7T(n/2) + \Theta(n^2)$ gives $\Theta(n^{\log_2 7}) = O(n^{2.8074})$ ring operations, so it was the first method to beat $\Theta(n^3)$. It needs subtraction, so it works over rings but not over the Boolean or the min-plus semiring. It started the search for the [matrix multiplication exponent](/matrix-multiplication-exponent/) $\omega$, and it is the only fast method of that search that is in common practical use.

## In plain words

To multiply two tables that are cut into four parts each, the simple method needs eight products of the parts. Strassen found a clever set of seven products. Each of the seven multiplies a sum or difference of parts of the first table by a sum or difference of parts of the second. Adding and subtracting these seven results in the right way gives the four parts of the answer.

One product is saved at each level of cutting, and the saving repeats at every level. Additions are cheap compared with products of large parts. So for large tables the total work grows more slowly than with the simple method: doubling the size multiplies the work by about seven, not eight.

## The problem

The input is two matrices $A$, $B$ over a ring $R$. The ring must have subtraction (an additive inverse for each element), but it need not be commutative: the entries can themselves be matrices, which is what the recursion uses. The output is $C = AB$. The cost counts ring operations, and $MM(n)$ is the cost for $n \times n$ matrices. The page describes square matrices; the same scheme works for $n \times m$ times $m \times p$ when all three sides are even, and the implementation handles all shapes.

## The algorithm

Split each matrix into four blocks of half size:

$$A = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}, \qquad B = \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}.$$

```pseudo id=main
STRASSEN(A, B)                            ▷ A is n × m, B is m × p
L1  if min(n, m, p) ≤ n0 then return MATRIX-MULTIPLY(A, B)
L2  if n, m or p is odd then pad each odd side with one zero row or column, multiply, and remove the padding
L3  split A and B into four blocks of half size each
L4  M1 ← STRASSEN(A11 + A22, B11 + B22)
L5  M2 ← STRASSEN(A21 + A22, B11)
L6  M3 ← STRASSEN(A11, B12 − B22)
L7  M4 ← STRASSEN(A22, B21 − B11)
L8  M5 ← STRASSEN(A11 + A12, B22)
L9  M6 ← STRASSEN(A21 − A11, B11 + B12)
L10 M7 ← STRASSEN(A12 − A22, B21 + B22)
L11 C11 ← M1 + M4 − M5 + M7
L12 C12 ← M3 + M5
L13 C21 ← M2 + M4
L14 C22 ← M1 − M2 + M3 + M6
L15 return the matrix with blocks C11, C12, C21, C22
```

Line L1 switches to the [triple loop](/naive-matrix-multiplication/) for small inputs; $n_0 \ge 1$ is the cutoff. Line L2 makes all sides even. Padding with zeros does not change the product: a zero row of $A$ gives a zero row of $C$, and a zero column of $A$ meets a zero row of $B$. Lines L4 to L10 form the seven products. Ten additions or subtractions form their operands. Lines L11 to L14 combine the products with eight more additions or subtractions, 18 in all. In each product, the factor that comes from $A$ is on the left, so the scheme is correct without commutativity.

## Example

Let $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ and $B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}$, with $n_0 = 1$, so the blocks are single numbers.

| product | operands | value |
|---|---|---|
| $M_1$ | $(1 + 4)(5 + 8)$ | 65 |
| $M_2$ | $(3 + 4) \cdot 5$ | 35 |
| $M_3$ | $1 \cdot (6 - 8)$ | $-2$ |
| $M_4$ | $4 \cdot (7 - 5)$ | 8 |
| $M_5$ | $(1 + 2) \cdot 8$ | 24 |
| $M_6$ | $(3 - 1)(5 + 6)$ | 22 |
| $M_7$ | $(2 - 4)(7 + 8)$ | $-30$ |

Then $C_{11} = 65 + 8 - 24 - 30 = 19$, $C_{12} = -2 + 24 = 22$, $C_{21} = 35 + 8 = 43$ and $C_{22} = 65 - 35 - 2 + 22 = 50$. So $AB = \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix}$, the same as the triple loop gives, with 7 multiplications instead of 8.

For a $3 \times 3$ product with $n_0 = 1$, line L2 pads both matrices to $4 \times 4$ with a zero last row and column, the recursion makes 7 products of $2 \times 2$ blocks and 49 scalar products, and the $3 \times 3$ top left part of the $4 \times 4$ result is $AB$.

## Correctness

The core is four identities of block matrices, which hold in any ring:

$$\begin{aligned} M_1 + M_4 - M_5 + M_7 &= A_{11} B_{11} + A_{12} B_{21}, \\ M_3 + M_5 &= A_{11} B_{12} + A_{12} B_{22}, \\ M_2 + M_4 &= A_{21} B_{11} + A_{22} B_{21}, \\ M_1 - M_2 + M_3 + M_6 &= A_{21} B_{12} + A_{22} B_{22}. \end{aligned}$$

Each one follows by expanding the products with the distributive laws, keeping the $A$ factor on the left, and cancelling. For example, $M_3 + M_5 = A_{11} B_{12} - A_{11} B_{22} + A_{11} B_{22} + A_{12} B_{22}$. With these identities, the method is correct by induction on the size, since each recursive call returns the true block product. The full proof, with all four expansions and the padding step, is in the proofs section.

## Complexity

**Multiplications.** With $n = 2^k$ and $n_0 = 1$, line L1 is reached $7^k$ times, each with one scalar multiplication. So the method does exactly $7^k = n^{\log_2 7}$ multiplications, with $\log_2 7 = 2.80735\ldots$

**All operations.** Each level does 18 additions of blocks of size $n/2$, so

$$T(n) = 7\,T(n/2) + 18\,(n/2)^2, \qquad T(1) = 1.$$

The solution has the form $T(n) = \alpha n^{\log_2 7} + \beta n^2$. Putting it into the recurrence gives $\beta n^2 = \tfrac{7}{4} \beta n^2 + \tfrac{18}{4} n^2$, so $\beta = -6$, and $T(1) = 1$ gives $\alpha = 7$. So $T(n) = 7 n^{\log_2 7} - 6 n^2$ exactly. By case 1 of the [master theorem](/master-theorem/), $T(n) = \Theta(n^{\log_2 7})$, and this does not depend on the values, so it holds in each case.

**Comparison with the classical count.** The triple loop does $2n^3 - n^2$ operations. The exact counts give:

| $n$ | classical $2n^3 - n^2$ | Strassen to $1 \times 1$ | Strassen with cutoff $n_0 = 8$ |
|---|---|---|---|
| 16 | 7 936 | 15 271 | 7 872 |
| 64 | 520 192 | 798 967 | 436 416 |
| 1024 | 2 146 435 072 | 1 971 035 287 | 1 100 550 336 |

So the full recursion has fewer operations than the classical method only from $n = 1024$ on, while a cutoff at $n_0 = 8$ wins already at $n = 16$. With a cutoff $n_0 = 2^c$ and $n = 2^k \ge n_0$, the same method of solution gives $T(n) = \alpha\, n^{\log_2 7} - 6n^2$ with $\alpha = (2n_0^3 + 5n_0^2)/7^c$. The values of $\alpha$ for $n_0 = 1, 2, 4, 8, 16$ are $7$, $5.14$, $4.24$, $3.92$ and $3.95$ (rounded), so among cutoffs that are powers of two, $n_0 = 8$ gives the smallest count for each $n \ge 16$. One level of Strassen followed by the classical method costs $7(2(n/2)^3 - (n/2)^2) + 18(n/2)^2 = \tfrac{7}{4} n^3 + \tfrac{11}{4} n^2$, which is less than $2n^3 - n^2$ exactly when $n > 15$.

These are counts of ring operations, and they are proved. The time on a real machine also depends on memory traffic, the speed of the additions, vector units and parallelism. The size at which a Strassen implementation beats a tuned classical library is found by measurement on each machine, and it is usually much larger than 16.

**Padding.** With the dynamic padding of line L2, each level adds at most one row and one column, so the sides at depth $d$ are at most $n/2^d + 2$, and the bound $O(n^{\log_2 7})$ still holds for all $n$.

**Space.** The operands and products of one level take $\Theta(n^2)$ space, and the levels below use a geometric series of smaller amounts, so the extra space is $\Theta(n^2)$. The recursion depth is $O(\log n)$.

## Properties

- **Needs subtraction.** The products $M_3$, $M_4$, $M_6$ and $M_7$ use differences. Over a semiring without subtraction, such as Boolean or min-plus matrices, the method is not defined. Boolean matrices can still use it by computing over $\mathbb{Z}$ and testing each entry for being nonzero, see [Boolean matrix multiplication](/boolean-matrix-multiplication/).
- **No commutativity needed.** This is what allows the recursion: the blocks are matrices, which do not commute.
- **Numerical stability.** In floating point, Strassen's algorithm satisfies a normwise error bound $\|\hat C - C\| \le c_n u \|A\| \|B\| + O(u^2)$, but not the entrywise bound $|\hat C - C| \le \gamma_n |A| |B|$ of the classical method. The constant $c_n$ grows faster with $n$ than the classical one. Small entries of $C$ can therefore have large relative errors when $A$ or $B$ has entries of very different sizes.
- **Exact over the integers and finite fields.** Over $\mathbb{Z}$ or $\mathbb{Z}/q\mathbb{Z}$ there is no error, and the method is used in exact linear algebra libraries.

## Variants and improvements

- **Winograd's variant.** Seven products and 15 additions, by reusing sums. The count becomes $6 n^{\log_2 7} - 5 n^2$. Probert (1976) showed that 15 additions are the minimum for any 7-product scheme for $2 \times 2$ matrices in the standard basis.
- **Alternative basis.** Karstadt and Schwartz (2017) changed the basis of the blocks at the start and the end, and lowered the leading coefficient to 5, for $5 n^{\log_2 7}$ plus lower terms.
- **More than 2 by 2.** A scheme for $k \times k$ blocks with $r$ products gives exponent $\log_k r$. [Laderman's algorithm](/laderman-algorithm/) uses 23 products for $3 \times 3$, which gives $\log_3 23 \approx 2.854$, worse than Strassen. Pan's schemes for large blocks and the later methods up to [Coppersmith and Winograd](/coppersmith-winograd-algorithm/) give smaller exponents, but they are galactic: their gains appear only for matrices far larger than any computer can hold.
- **Parallel Strassen.** The seven products are independent, see [parallel Strassen](/parallel-strassen/).
- **Search for schemes.** [AlphaTensor](/alphatensor/) searched for low-rank schemes of small formats with reinforcement learning and found, among others, a scheme with 47 products for $4 \times 4$ matrices over $\mathbb{Z}/2\mathbb{Z}$, where two levels of Strassen give 49.

## When to use it

Use it for large dense matrices over $\mathbb{Z}$, finite fields or other exact rings, where the saving of one product in eight at each level pays off and there is no rounding error. In floating point, use it when a normwise error bound is enough. Keep a cutoff and a tuned classical kernel for the small blocks. Do not use it over semirings without subtraction, for small matrices, or when the memory for the temporaries is not available.

## Pitfalls

- **Recursing to 1 by 1.** With $n_0 = 1$ the method does more operations than the classical one for all $n < 1024$ (see the table). Set the cutoff of line L1 to a measured value.
- **Padding to the next power of two at the top.** Padding $n = 2^k + 1$ to $2^{k+1}$ multiplies the work by about 7. Pad one row and column at each level, as in line L2, or peel off the extra row and column and fix up with matrix-vector products.
- **A sign error in the combination.** $C_{11}$ is $M_1 + M_4 - M_5 + M_7$ and $C_{22}$ is $M_1 - M_2 + M_3 + M_6$. A swapped sign gives wrong results that a test on symmetric or diagonal matrices can miss. Test against the triple loop on random non-symmetric matrices.
- **Swapping the factors.** Writing $M_3 = (B_{12} - B_{22}) A_{11}$ is correct for numbers but wrong for blocks, since block products do not commute.
- **Overflow.** The operand sums of lines L4 to L10 double the size of the entries at each level. With fixed-width integers, reduce modulo the prime at each step or use wider words.

## Implementations

## History

Volker Strassen published the method in 1969 in a paper of three pages titled *Gaussian elimination is not optimal*. He also showed that inversion and determinants can be computed with $O(n^{\log_2 7})$ operations. In 1971 Winograd, and independently Hopcroft and Kerr, proved that 7 multiplications are necessary for $2 \times 2$ matrices, so Strassen's scheme is optimal for this format. Winograd also gave the variant with 15 additions. The exponent $\log_2 7$ stood until Pan's work in 1978, see the [matrix multiplication exponent](/matrix-multiplication-exponent/).

## References
