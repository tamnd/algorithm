---
tag: 6P3FW5
kind: algorithm
slug: faddeev-leverrier-algorithm
name: Faddeev-LeVerrier algorithm
aliases:
- LeVerrier algorithm
- Faddeev-Souriau algorithm
- Souriau-Frame algorithm
- Leverrier-Faddeev method
area: algebra/exact-linear-algebra
level: advanced
summary: Computes the characteristic polynomial through a recurrence on matrix powers, dividing by integers.
solves: [characteristic-polynomial-computation, matrix-inversion, determinant-computation]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix, b: the maximum binary length of an entry of an integer input}
  time: {worst: Θ(n^4), best: Θ(n^4)}
  space: {extra: Θ(n^2)}
  field_operations: {worst: 2n^4 + O(n^3)}
  bit_operations: {worst: O(n^5 b (b + log n))}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [characteristic-polynomial, cramers-rule]
see_also: [berkowitz-algorithm, characteristic-polynomial-computation, cayley-hamilton-theorem, matrix-inversion, determinant-computation, nc, matrix-multiplication-exponent, hessenberg-reduction]
sources:
  - paper: doi:10.1137/0205040
    title: L. Csanky, Fast parallel matrix inversion algorithms, SIAM Journal on Computing 5(4), 1976
    locator: pp. 618 to 623 (the characteristic polynomial from the traces of powers by Newton's identities, in parallel depth O(log^2 n), with the division by integers that restricts it to characteristic 0)
  - book: "D. K. Faddeev and V. N. Faddeeva, Computational Methods of Linear Algebra, W. H. Freeman, 1963"
    locator: the chapter on the computation of eigenvalues, the sections on the method of Leverrier and its modification by D. K. Faddeev
  - book: "F. R. Gantmacher, The Theory of Matrices, volume 1, Chelsea, 1959"
    locator: Chapter IV, the section on methods of computing the coefficients of the characteristic polynomial and the adjoint matrix (the method of D. K. Faddeev)
  - paper: "Urbain Le Verrier, Sur les variations seculaires des elements elliptiques des sept planetes principales, Journal de Mathematiques Pures et Appliquees, first series, 5, 1840"
    locator: pp. 220 to 254 (the coefficients of the secular equation from the sums of powers of its roots)
  - paper: "J. S. Frame, A simple recursion formula for inverting a matrix, Bulletin of the American Mathematical Society 55, 1949, abstract"
    locator: p. 1045 (the recursion M_(k+1) = A M_k + p_k I with the inverse as a by-product)
---

The Faddeev-LeVerrier algorithm computes the coefficients of the [characteristic polynomial](/characteristic-polynomial/) $\det(xI - A)$ with $n$ matrix products and $n$ traces. It keeps a matrix $M_k$, multiplies by $A$, reads the next coefficient from the trace divided by $k$, and adds that coefficient to the diagonal. The last matrix $M_n$ is, up to sign, the adjugate of $A$, so the inverse and the determinant come out of the same loop. The divisions by $1, 2, \dots, n$ restrict the method to fields of characteristic $0$ or larger than $n$; over the integers the divisions are exact. It costs about $2n^4$ field operations, four times the [Berkowitz algorithm](/berkowitz-algorithm/), but it is short, made of matrix products, and the basis of the first $\mathrm{NC}$ algorithm for the determinant.

Notation: $K$ is a field of characteristic $0$ or greater than $n$, or the ring $\mathbb{Z}$. $A$ is an $n \times n$ matrix, $\chi_A(x) = \det(xI - A) = \sum_{k=0}^{n} p_k x^{n-k}$ with $p_0 = 1$, so $p_k$ is the coefficient of $x^{n-k}$. $\operatorname{tr}$ is the trace, and $\omega$ is the exponent of matrix multiplication. For an integer input, $b$ is the maximum binary length of an entry. Costs are given in field operations and in bit operations with schoolbook integer arithmetic.

## In plain words

Start with the identity matrix. Multiply it by the input matrix and look at the sum of the diagonal: dividing it by one and changing the sign gives the first coefficient. Put that coefficient on the diagonal, multiply by the input matrix again, and divide the new diagonal sum by two to get the next coefficient. Keep going, dividing by three, four, and so on. After as many rounds as the size of the matrix, all coefficients are known, and the matrix kept along the way gives the inverse almost for free.

## The problem

Input: an $n \times n$ matrix $A$ over a field of characteristic $0$ or greater than $n$, or over $\mathbb{Z}$. Output: the coefficients $p_0, \dots, p_n$ of $\chi_A$, and the matrix $M_n$ with $A M_n = -p_n I$. From them, $\det A = (-1)^n p_n$, $\operatorname{adj}(A) = (-1)^{n-1} M_n$, and $A^{-1} = -M_n / p_n$ when $p_n \ne 0$.

## The algorithm

The matrices are $M_1 = I$ and $M_{k+1} = A M_k + p_k I$, and the coefficients are $p_k = -\operatorname{tr}(A M_k)/k$. The pseudocode keeps $N = A M_{k-1}$ so that each step needs one matrix product.

```pseudo id=main
FADDEEV-LEVERRIER(A)                         ▷ A is n × n, with 1, ..., n invertible
L1  p_0 ← 1; N ← the n × n zero matrix
L2  for k ← 1 to n do
L3      M ← N + p_{k−1} I                       ▷ M = M_k
L4      N ← A · M
L5      p_k ← −tr(N) / k
L6  return (p_0, ..., p_n), M                 ▷ M = M_n and A M_n = −p_n I
```

At the end, $N = A M_n$ is $-p_n I$, a free check: if it is not a multiple of the identity, the arithmetic went wrong. The last product is needed only for its trace, so an implementation can compute just the diagonal of $A M_n$, which saves one product.

## Example

For $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$:

| $k$ | $M_k$ (rows) | $\operatorname{tr}(A M_k)$ | $p_k$ |
| --- | --- | --- | --- |
| 1 | (1 0 0), (0 1 0), (0 0 1) | 9 | $-9/1 = -9$ |
| 2 | (−7 1 0), (1 −6 1), (0 1 −5) | −48 | $48/2 = 24$ |
| 3 | (11 −4 1), (−4 8 −2), (1 −2 5) | 54 | $-54/3 = -18$ |

So $\chi_M(x) = x^3 - 9x^2 + 24x - 18$ and $\det M = (-1)^3 p_3 = 18$. The product $A M_2$ has rows $(-13, -4, 1)$, $(-4, -16, -2)$, $(1, -2, -19)$, and $M_3 = A M_2 + 24 I$. The last product $A M_3 = 18 I$, as predicted. Since $n = 3$ is odd, $M_3 = \operatorname{adj}(M)$ and $M^{-1} = M_3/18$, the same inverse as on the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) page. Every division in the table is exact, because the input has integer entries.

The implementation checks this example, and tests random integer, rational and mod-$101$ matrices against the coefficients computed as sums of principal minors, the adjugate against cofactors, and $A A^{-1} = I$.

## Correctness

The proof compares two formulas for the adjugate $B(x) = \operatorname{adj}(xI - A)$. First, $(xI - A)B(x) = \chi_A(x) I$ by [Cramer's rule](/cramers-rule/); comparing coefficients shows $B(x) = \sum_{k=1}^{n} M_k x^{n-k}$, with exactly the recurrence $M_1 = I$, $M_{k+1} = A M_k + p_k I$, and $A M_n + p_n I = 0$. This is the computation inside the proof of the Cayley-Hamilton theorem. Second, the derivative of a determinant is the trace of the adjugate: $\chi_A'(x) = \operatorname{tr} B(x)$. Comparing coefficients gives $\operatorname{tr} M_k = (n - k + 1) p_{k-1}$. Taking the trace of the recurrence then gives $k\, p_k = -\operatorname{tr}(A M_k)$, which determines $p_k$ when $k$ is invertible. Over $\mathbb{Z}$, the same values are computed in $\mathbb{Q}$, and they are integers, so each division is exact. The [full proof](proofs/correctness.md) gives the details.

## Complexity

**Field operations.** Each of the $n$ products on line L4 costs $n^2$ inner products of length $n$, that is $2n^3 - n^2$ operations. Lines L3 and L5 cost $O(n)$ each. The total is $2n^4 + O(n^3)$, and $2n^4 - 2n^3 + O(n^2)$ if the last product is replaced by its trace. The work does not depend on the entries. With fast matrix multiplication, the cost is $O(n^{\omega + 1})$.

**Bit operations over $\mathbb{Z}$.** Let $|a_{ij}| \le B < 2^b$. Each $M_k$ is a coefficient of $\operatorname{adj}(xI - A)$, so its entries are signed sums of minors of order at most $n - 1$ of $A$; by the [Hadamard bound](/hadamard-bound/), they and the $p_k$ have $O(n(b + \log n))$ bits. In each product $A M_k$, one factor of every multiplication has only $b$ bits, so a product costs $O(n^3 \cdot n b (b + \log n))$ bit operations with schoolbook arithmetic. The $n$ products give $O(n^5 b (b + \log n))$, and the divisions by $k$ cost less. These bounds are proved.

**Space.** The algorithm keeps the matrices $M$ and $N$, so $\Theta(n^2)$ extra field elements, and over $\mathbb{Z}$ $O(n^3 (b + \log n))$ bits.

## Properties

- **Needs $1, \dots, n$ invertible.** Over $\mathbb{Q}$, $\mathbb{R}$, $\mathbb{C}$ and $\mathbb{Z}/p\mathbb{Z}$ with $p > n$ the method works. Over $\mathbb{Z}/p\mathbb{Z}$ with $p \le n$, the step $k = p$ divides by $0$, and the identity $p \cdot p_p = -\operatorname{tr}(A M_p)$ says nothing about $p_p$.
- **Integer-preserving.** On an integer matrix every $M_k$ and every $p_k$ is an integer, and each division by $k$ is exact, as in the [Bareiss algorithm](/bareiss-algorithm/).
- **Inverse and adjugate as by-products.** $\operatorname{adj}(A) = (-1)^{n-1} M_n$ is defined for every $A$, singular or not, and $A^{-1} = -M_n / p_n$.
- **No pivoting, no branching on the data.** The sequence of operations is the same for every input of size $n$.
- **Built from matrix products**, so it uses fast matrix multiplication and parallel hardware directly.
- **Numerically unstable.** In floating point the traces suffer from cancellation, and the computed coefficients can be badly wrong already for moderate $n$. The method is for exact arithmetic.

## Variants and improvements

- **LeVerrier's original form.** Compute the power sums $s_k = \operatorname{tr}(A^k)$ for $k = 1, \dots, n$ and solve Newton's identities $k\, p_k = -(s_k + p_1 s_{k-1} + \cdots + p_{k-1} s_1)$. This gives the same coefficients, without the adjugate.
- **Csanky's parallel algorithm.** Compute all powers $A^k$ by a parallel prefix product and solve Newton's identities, a triangular system, in parallel. This gives depth $O(\log^2 n)$ with polynomially many processors, so the characteristic polynomial, the determinant and the inverse over a field of characteristic $0$ are in [NC](/nc/). The [Berkowitz algorithm](/berkowitz-algorithm/) removed the condition on the characteristic.
- **Baby steps and giant steps.** The traces $\operatorname{tr}(A^{i + jm})$ for $m \approx \sqrt n$ need only the powers $A^i$ and $A^{jm}$ for $i, j < m$, about $2\sqrt n$ matrix products, and then $n$ traces of products, each $O(n^2)$ since $\operatorname{tr}(XY) = \sum_{i,j} X_{ij} Y_{ji}$. That gives the characteristic polynomial in characteristic $0$ in $O(n^{\omega + 1/2} + n^3)$ field operations; Preparata and Sarwate used this idea to reduce the processor count of Csanky's algorithm.
- **Small characteristic.** Over $\mathbb{Z}/p\mathbb{Z}$ with $p \le n$, run the integer version on a lift of the matrix and reduce at the end, or use Berkowitz or [Hessenberg reduction](/hessenberg-reduction/).
- **Faster sequential methods.** Over a field, Hessenberg reduction costs $O(n^3)$, and Keller-Gehrig's method $O(n^\omega \log n)$; see [characteristic polynomial computation](/characteristic-polynomial-computation/).

## When to use it

Use it for small exact matrices over $\mathbb{Q}$ or a large prime field when the characteristic polynomial and the inverse or adjugate are wanted together, when a short branch-free method built from matrix products is convenient, or in a parallel setting. It is also a classic tool for symbolic work, where entries are rational functions in parameters and pivoting would need zero tests. For large $n$, Hessenberg reduction is faster, and in small characteristic or over rings with zero divisors, Berkowitz is the division-free choice.

## Pitfalls

- **Dividing by $k$ in small characteristic.** Modulo a prime $p \le n$, the step $k = p$ divides by zero. Check the characteristic first.
- **Floating point.** The method is unstable in floating point; do not use it for numerical eigenvalue problems.
- **The sign of the adjugate.** $\operatorname{adj}(A) = (-1)^{n-1} M_n$, not $M_n$. For even $n$ the signs flip.
- **Off-by-one in the recurrence.** The coefficient added on line L3 is $p_{k-1}$, the one just computed, and the first step adds $p_0 = 1$ to the zero matrix. Starting with $M = A$ instead skips a coefficient.
- **Integer division that is not exact.** Over $\mathbb{Z}$, a nonzero remainder on line L5 means a bug in the products; the implementation asserts that the remainder is $0$.

## Implementations

## History

Urbain Le Verrier, the astronomer who predicted Neptune, computed the coefficients of a characteristic ("secular") equation from the sums of powers of its roots in 1840, which is the power-sum form of the method. In the 1940s several authors found the recurrence that also produces the adjugate: Jean-Marie Souriau in 1948, J. S. Frame in 1949, and D. K. Faddeev and I. S. Sominsky in 1949, hence the names Faddeev-LeVerrier and Souriau-Frame. In 1976 L. Csanky turned the power-sum form into the first parallel algorithm with depth $O(\log^2 n)$ for the determinant and the inverse.

## References
