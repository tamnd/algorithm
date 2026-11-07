---
tag: Q52APH
kind: problem
slug: matrix-inversion
name: Matrix inversion
aliases: [computing the inverse, computing the inverse of a matrix, inverse matrix computation]
area: algebra/exact-linear-algebra
level: core
summary: Compute the inverse of a nonsingular square matrix exactly.
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix}
  time: {worst: Θ(n^ω)}
prereqs: [determinant, gaussian-elimination]
see_also: [gauss-jordan-elimination, lu-decomposition, matrix-multiplication-inversion-equivalence, laplace-expansion, cramers-rule, unimodular-matrix, dixon-p-adic-lifting, strassen-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 28.2, Inverting matrices (inversion from LUP decomposition, and the proofs that inversion and multiplication have the same asymptotic cost)
  - paper: doi:10.1007/BF02165411
    title: Volker Strassen, Gaussian elimination is not optimal, Numerische Mathematik 13, 1969
    locator: pp. 354 to 356 (matrix multiplication with 7 products of half size, and inversion by blocks in O(n^(log2 7)) operations)
  - paper: doi:10.1090/S0025-5718-1974-0331751-8
    title: James R. Bunch and John E. Hopcroft, Triangular factorization and inversion by fast matrix multiplication, Mathematics of Computation 28(125), 1974
    locator: pp. 231 to 236 (inversion of every nonsingular matrix in O(n^ω), with row pivoting)
  - book: isbn:9783540605829
    title: Peter Burgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer, 1997
    locator: Chapter 16, Problems Related to Matrix Multiplication (inversion, determinant and multiplication have the same exponent; the Baur-Strassen theorem on partial derivatives)
  - paper: "Arne Storjohann, The shifted number system for fast linear algebra on integer matrices, Journal of Complexity 21(4), 2005"
    locator: the inverse of a nonsingular integer matrix in about n^3 b bit operations up to logarithmic factors, which is near the size of the output
---

Matrix inversion asks, for a square matrix $A$ over a field, for the matrix $A^{-1}$ with $A A^{-1} = A^{-1} A = I$, or for the answer that $A$ is singular. In the algebraic model it has the same cost as [matrix multiplication](/matrix-multiplication-exponent/), $\Theta(n^\omega)$ field operations up to constants. For an integer matrix the exact inverse is the adjugate divided by the [determinant](/determinant/), and its output alone has about $n^3$ times the length of an entry, which sets the bit complexity.

## In plain words

The inverse of a square table of numbers is the table that undoes it: multiply the two and you get the identity, the table with ones on the diagonal and zeros elsewhere. It exists exactly when the table does not squash any nonzero vector to zero.

To compute it, you solve one system of equations for each column of the identity. Elimination does all of them together. With exact numbers, such as fractions, the answer has a common denominator, which is the determinant, and the numerators can be long, because they are determinants of smaller tables.

## Definition

**Notation.** $K$ is a field, $R$ an integral domain with field of fractions $K$ (usually $R = \mathbb{Z}$ and $K = \mathbb{Q}$), and $A$ an $n \times n$ matrix. $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/). For an integer matrix, $b$ is the maximum binary length of an entry.

**Input.** An $n \times n$ matrix $A$ over $K$.

**Output.** The matrix $A^{-1}$ over $K$ with $A A^{-1} = I_n$, if $\det A \neq 0$; otherwise the answer "singular". By the [rank-nullity theorem](/rank-nullity-theorem/) a one-sided inverse of a square matrix is two-sided, so $A X = I$ is enough.

**Over a ring.** For $A$ over a commutative ring $R$, the [Laplace expansion](/laplace-expansion/) gives $A \operatorname{adj}(A) = \det(A) I$. So $A$ has an inverse with entries in $R$ if and only if $\det A$ is a unit of $R$, and then $A^{-1} = \det(A)^{-1} \operatorname{adj}(A)$. Over $\mathbb{Z}$ this means $\det A = \pm 1$, a [unimodular matrix](/unimodular-matrix/). Over $\mathbb{Z}/N\mathbb{Z}$ it means $\gcd(\det A, N) = 1$.

**Size of the output over $\mathbb{Q}$.** For an integer $A$ with $\det A \neq 0$, $A^{-1} = \operatorname{adj}(A) / \det A$. Each entry of $\operatorname{adj}(A)$ is a minor of order $n - 1$ and $\det A$ is a minor of order $n$, so by the [Hadamard bound](/hadamard-bound/) all of them have at most $n (b + \tfrac12 \log_2 n)$ binary digits. The output is $n^2$ such numbers, $O(n^3 (b + \log n))$ binary digits in total, and for random matrices this size is reached up to a constant factor (an observation, not a proved bound).

## Variants

- **Decision.** Is $A$ invertible? This is $\det A \neq 0$, or $\operatorname{rank}(A) = n$; see [rank computation](/rank-computation/).
- **Solve instead of invert.** To get $A^{-1} B$ for a few columns $B$, solve $A X = B$ with an [LU decomposition](/lu-decomposition/); forming $A^{-1}$ first costs more and, over $\mathbb{Q}$, produces larger numbers.
- **Inverse modulo $N$.** Over $\mathbb{Z}/N\mathbb{Z}$, for example in the Hill cipher, invert $\det A$ modulo $N$ with the [extended Euclidean algorithm](/extended-euclidean-algorithm/) and multiply the adjugate, or eliminate directly when $N$ is prime.
- **Integer output format.** Over $\mathbb{Z}$, the output is the pair $(\operatorname{adj}(A), \det A)$, or the inverse as fractions in lowest terms.
- **Structured matrices.** The inverse of a Toeplitz matrix is determined by $O(n)$ numbers and can be found in $O(n^2)$ field operations; see [Toeplitz system solving](/toeplitz-system-solving/).
- **Generalized inverses.** For a singular or rectangular matrix, the Moore-Penrose [pseudoinverse](/pseudoinverse/) replaces the inverse.

## Examples

**A unimodular matrix.** For

$$A = \begin{pmatrix} 2 & 1 & 1 \\ 1 & 3 & 2 \\ 1 & 0 & 0 \end{pmatrix}, \qquad \det A = -1, \qquad A^{-1} = \begin{pmatrix} 0 & 0 & 1 \\ -2 & 1 & 3 \\ 3 & -1 & -5 \end{pmatrix}.$$

Expansion along row $3$ gives $\det A = 1 \cdot \det \begin{pmatrix} 1 & 1 \\ 3 & 2 \end{pmatrix} = -1$. The inverse has integer entries because $\det A$ is a unit of $\mathbb{Z}$, and $\operatorname{adj}(A) = \det(A) A^{-1} = -A^{-1}$.

**A rational inverse.** For $B = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$, $\det B = 5$ and $B^{-1} = \tfrac15 \begin{pmatrix} 3 & -1 \\ -1 & 2 \end{pmatrix}$. The denominator $5$ is the determinant and the numerators are the cofactors.

**The same matrix modulo primes.** Modulo $7$, $5^{-1} = 3$, so $B^{-1} \equiv 3 \begin{pmatrix} 3 & -1 \\ -1 & 2 \end{pmatrix} \equiv \begin{pmatrix} 2 & 4 \\ 4 & 6 \end{pmatrix}$, and indeed $B \begin{pmatrix} 2 & 4 \\ 4 & 6 \end{pmatrix} = \begin{pmatrix} 8 & 14 \\ 14 & 22 \end{pmatrix} \equiv I \pmod 7$. Modulo $5$, $B$ is singular.

**Singular input.** The matrix with rows $(1, 2, 3)$, $(4, 5, 6)$, $(7, 8, 9)$ has determinant $0$, and Gauss-Jordan elimination of $(A \mid I)$ meets a zero row in the left half, which is the certificate.

## Known algorithms

- [Gauss-Jordan elimination](/gauss-jordan-elimination/) of $(A \mid I_n)$ to $(I_n \mid A^{-1})$: $n^3 + O(n^2)$ multiplications over a field when the identity part is not stored in full.
- [LU decomposition](/lu-decomposition/) followed by $n$ solves: $O(n^3)$ field operations, and the factorization can be kept for later solves.
- Inversion by blocks with fast multiplication (Strassen, 1969, with the pivoting of Bunch and Hopcroft, 1974): $O(n^\omega)$ field operations, so $O(n^{2.81})$ with [Strassen's algorithm](/strassen-algorithm/).
- The adjugate from cofactors, by [Laplace expansion](/laplace-expansion/): division-free but exponential, useful for $n \le 4$.
- Division-free methods through the characteristic polynomial: if $\chi_A(x) = x^n + c_{n-1} x^{n-1} + \cdots + c_0$, the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) gives $A^{-1} = -c_0^{-1} (A^{n-1} + c_{n-1} A^{n-2} + \cdots + c_1 I)$. The [Faddeev-LeVerrier algorithm](/faddeev-leverrier-algorithm/) builds the inverse this way.
- Over $\mathbb{Z}$: elimination with fractions or the [Bareiss algorithm](/bareiss-algorithm/) costs $O(n^5 (b + \log n)^2)$ bit operations with schoolbook arithmetic. [Dixon lifting](/dixon-p-adic-lifting/) of each column costs about $n^4 b$ bit operations up to logarithmic factors, and Storjohann's algorithm of 2005 (Las Vegas) costs about $n^3 b$ up to logarithmic factors.

## Bounds

**Algebraic model.** Over a field, inversion costs $\Theta(n^\omega)$ field operations up to constant factors: an algorithm for multiplication in $O(n^\alpha)$ with $\alpha > 2$ gives inversion in $O(n^\alpha)$, and conversely; see [the equivalence of multiplication and inversion](/matrix-multiplication-inversion-equivalence/). The direction "multiplication is not harder" uses

$$\begin{pmatrix} I & X & 0 \\ 0 & I & Y \\ 0 & 0 & I \end{pmatrix}^{-1} = \begin{pmatrix} I & -X & X Y \\ 0 & I & -Y \\ 0 & 0 & I \end{pmatrix},$$

so one inversion of size $3n$ gives the product $X Y$ of two $n \times n$ matrices. The best known bound on $\omega$ is below $2.372$, and the only proved lower bound in general is the trivial $\Omega(n^2)$. These are proved results.

**Bit complexity over $\mathbb{Z}$.** The output has $\Theta(n^3 b)$ binary digits for typical inputs, which is a lower bound for any algorithm that writes the inverse in full. Storjohann's algorithm reaches this up to logarithmic factors.

## Reductions

- **To multiplication and back.** As above, in both directions with a constant factor, for $\omega > 2$.
- **From the determinant.** By the Baur-Strassen theorem, a straight-line program for $\det A$ of length $L$ gives one for all partial derivatives $\partial \det A / \partial a_{ij} = C_{ij}$ of length $O(L)$, and so for $\operatorname{adj}(A)$ and $A^{-1}$. So the inverse is at most a constant factor harder than the determinant in the algebraic model.
- **To solving.** Inversion is $n$ linear solves with the same matrix; conversely one solve is a matrix-vector product with $A^{-1}$.

## Applications

- **Change of basis and dual bases.** The [dual lattice](/dual-lattice/) of a lattice with basis matrix $B$ has basis matrix $B^{-T}$.
- **Unimodular transforms.** Normal form algorithms over $\mathbb{Z}$ return transforms $U$ and need $U^{-1}$, which is integral when $\det U = \pm 1$; see [Smith normal form](/smith-normal-form/) and [Hermite normal form](/hermite-normal-form/).
- **Cryptography.** The Hill cipher decrypts with the inverse of the key matrix modulo $26$.
- **Computer algebra.** Exact inverses of matrices with rational or polynomial entries appear in the solution of parametric linear systems and in the transformation of differential systems.

## References
