---
tag: PM8CKR
kind: algorithm
slug: berkowitz-algorithm
name: Berkowitz algorithm
aliases:
- Samuelson-Berkowitz algorithm
- Berkowitz's method
area: algebra/exact-linear-algebra
level: advanced
summary: Division-free algorithm for the characteristic polynomial, valid over any commutative ring.
solves: [characteristic-polynomial-computation, determinant-computation]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix, b: the maximum binary length of an entry of an integer input}
  time: {worst: Θ(n^4), best: Θ(n^4)}
  space: {extra: Θ(n)}
  ring_operations: {worst: n^4/2 + O(n^3)}
  bit_operations: {worst: O(n^5 (b + log n)^2)}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [characteristic-polynomial, cayley-hamilton-theorem]
see_also: [characteristic-polynomial-computation, faddeev-leverrier-algorithm, determinant-computation, bareiss-algorithm, gaussian-elimination-modular, hessenberg-reduction, nc, matrix-multiplication-exponent]
sources:
  - paper: doi:10.1016/0020-0190(84)90018-8
    title: Stuart J. Berkowitz, On computing the determinant in small parallel time using a small number of processors, Information Processing Letters 18(3), 1984
    locator: pp. 147 to 150 (the division-free reduction of the characteristic polynomial to products of Toeplitz matrices, and the parallel version in depth O(log^2 n))
  - paper: "Paul A. Samuelson, A method of determining explicitly the coefficients of the characteristic equation, Annals of Mathematical Statistics 13(4), 1942"
    locator: pp. 424 to 429 (the bordering recurrence that expresses the characteristic polynomial of a matrix through that of its trailing block)
  - paper: "Erich Kaltofen, On computing determinants of matrices without divisions, Proceedings of ISSAC 1992, ACM"
    locator: pp. 342 to 349 (division-free determinant with fewer ring operations than Berkowitz, and a comparison with it)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.4, Computing the characteristic polynomial (the Hessenberg method over a field, the usual alternative when divisions are allowed)
---

The Berkowitz algorithm computes the [characteristic polynomial](/characteristic-polynomial/) $\det(xI - A)$ of an $n \times n$ matrix, and with it the determinant, using only additions, subtractions and multiplications. It works over every commutative ring: the integers, polynomial rings, and rings with zero divisors such as $\mathbb{Z}/6\mathbb{Z}$ or the 64-bit machine integers, where elimination fails because pivots cannot be inverted. It builds the polynomial from the bottom right corner up, adding one row and column at a time, and each step multiplies by a small Toeplitz matrix of numbers $\rho S^j \gamma$. The cost is about $n^4/2$ ring operations, one power of $n$ more than elimination, and the method parallelizes to depth $O(\log^2 n)$.

Notation: $R$ is a commutative ring with $1$, $A$ is an $n \times n$ matrix over $R$, indexed from $0$, and $\chi_A(x) = \det(xI - A)$. $A_r$ is the trailing principal block in rows and columns $r, \dots, n-1$. Polynomials are coefficient lists, highest degree first. $\omega$ is the exponent of matrix multiplication. For an integer input, $b$ is the maximum binary length of an entry. Costs are given in ring operations and in bit operations with schoolbook integer arithmetic.

## In plain words

Most ways to find a determinant divide by a pivot, and that fails when the numbers cannot be divided, for example when they are remainders modulo a number like 6 that is not prime. This method never divides. It starts with the smallest square in the bottom corner and grows it one row and column at a time. To grow it, it multiplies the new row by powers of the old square and then by the new column, and mixes the results into the old answer. At the end it has the full characteristic polynomial, and the determinant is its last number, up to sign.

## The problem

Input: an $n \times n$ matrix $A$ over a commutative ring $R$. Output: the coefficients of $\chi_A(x) = \det(xI - A)$, a monic polynomial of degree $n$, and from it $\det A = (-1)^n \chi_A(0)$. Only ring operations are allowed: no division, no zero test. Over $\mathbb{Z}$, the cost of interest is in bit operations.

## The algorithm

Write $A_r = \begin{pmatrix} a & \rho \\ \gamma & S \end{pmatrix}$, where $a = A[r, r]$, $\rho$ is the rest of row $r$, $\gamma$ the rest of column $r$, and $S = A_{r+1}$ has size $s = n - r - 1$. Samuelson's formula says

$$
\chi_{A_r}(x) = (x - a)\,\chi_S(x) - \rho \operatorname{adj}(xI - S)\, \gamma,
$$

and the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) writes the adjugate as a polynomial in $S$. The result is a product: the coefficient list of $\chi_{A_r}$ is $T \cdot p$, where $p$ lists $\chi_S$ and $T$ is the $(s+2) \times (s+1)$ lower triangular Toeplitz matrix with first column

$$
q = (1,\; -a,\; -\rho\gamma,\; -\rho S \gamma,\; \dots,\; -\rho S^{s-1}\gamma).
$$

Equivalently, $T p$ is the product of the polynomials $q$ and $p$, cut after $s + 2$ coefficients.

```pseudo id=main
BERKOWITZ(A)                                 ▷ A is n × n over a commutative ring R
L1  if n = 0 then return (1)
L2  p ← (1, −A[n − 1, n − 1])                   ▷ χ of the last 1 × 1 block
L3  for r ← n − 2 down to 0 do
L4      s ← n − r − 1; a, ρ, γ, S ← the parts of the block A_r
L5      q ← (1, −a); v ← ρ
L6      for k ← 0 to s − 1 do
L7          append −v · γ to q                    ▷ −ρ S^k γ
L8          if k < s − 1 then v ← v S
L9      p ← the first s + 2 coefficients of q · p ▷ the Toeplitz product T p
L10 return p
```

Line L9 is the polynomial product $p'_i = \sum_t q_t\, p_{i-t}$ for $0 \le i \le s + 1$, with only the terms where both indices are in range. Line L8 skips the last product $vS$, which would not be used. The determinant is $(-1)^n$ times the last entry of the result.

## Example

For $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$, line L2 gives $p = (1, -4)$, the polynomial $x - 4$.

- $r = 1$: $a = 3$, $\rho = (1)$, $\gamma = (1)$, $S = (4)$, $s = 1$. Then $q = (1, -3, -1)$, and $p' = (1,\; -3 - 4,\; -1 + 12) = (1, -7, 11)$, which is $\chi$ of $\begin{pmatrix} 3 & 1 \\ 1 & 4 \end{pmatrix}$: trace $7$, determinant $11$.
- $r = 0$: $a = 2$, $\rho = (1, 0)$, $\gamma = (1, 0)^T$, $S = \begin{pmatrix} 3 & 1 \\ 1 & 4 \end{pmatrix}$, $s = 2$. Then $\rho\gamma = 1$, $v = \rho S = (3, 1)$ and $v\gamma = 3$, so $q = (1, -2, -1, -3)$. The product gives

$$
p' = (1,\; -7 - 2,\; 11 + 14 - 1,\; -22 + 7 - 3) = (1, -9, 24, -18).
$$

So $\chi_M(x) = x^3 - 9x^2 + 24x - 18$ and $\det M = (-1)^3 \cdot (-18) = 18$, as in the example of the [characteristic polynomial](/characteristic-polynomial/) page.

**A ring with zero divisors.** Over $\mathbb{Z}/6\mathbb{Z}$, take $A = \begin{pmatrix} 2 & 3 \\ 3 & 2 \end{pmatrix}$. Elimination is stuck: neither $2$ nor $3$ is invertible modulo $6$, and the [modular elimination](/gaussian-elimination-modular/) page shows how this goes wrong. Berkowitz starts with $p = (1, -2)$, forms $q = (1, -2, -9)$, and returns $(1, -4, -5) \equiv (1, 2, 1)$. So $\chi_A = x^2 + 2x + 1$ and $\det A = -5 \equiv 1 \pmod 6$, which matches $4 - 9 = -5$.

The implementation checks both examples, and tests random matrices over $\mathbb{Z}$, $\mathbb{Z}/4$, $\mathbb{Z}/6$, $\mathbb{Z}/12$ and $\mathbb{Z}/2^{64}$ against the coefficients computed as sums of principal minors with the Leibniz formula.

## Correctness

The invariant is that after the iteration with index $r$, the list $p$ holds $\chi_{A_r}$. Two identities give the step. First, for a bordered matrix, $\det \begin{pmatrix} \alpha & \beta \\ \gamma & D \end{pmatrix} = \alpha \det D - \beta \operatorname{adj}(D) \gamma$; it is a polynomial identity with integer coefficients, so it is enough to prove it for a matrix of indeterminates, where the Schur complement gives it. Applied to $xI - A_r$, it gives Samuelson's formula. Second, $\operatorname{adj}(xI - S) = \sum_{k=1}^{s} c_k \sum_{j<k} x^{k-1-j} S^j$, where $c_k$ are the coefficients of $\chi_S$. Multiplying by $xI - S$ telescopes to $\chi_S(x)I - \chi_S(S) = \chi_S(x) I$ by Cayley-Hamilton, and a monic polynomial is not a zero divisor, so the adjugate is this sum. Collecting the coefficients of $x$ gives the Toeplitz product. No step divides, so the proof works over every commutative ring. The [full proof](proofs/correctness.md) does the index bookkeeping.

## Complexity

**Ring operations.** In the step with block size $s$, line L7 costs $2s$ operations and line L8 costs $s(2s - 1)$, so the loop of line L6 costs $2s^3 + O(s^2)$, and line L9 costs $O(s^2)$. The sum over $s = 1, \dots, n - 1$ is $\tfrac12 n^4 + O(n^3)$ ring operations. A count with an instrumented ring gives $0.477\, n^4$ for $n = 40$, approaching $\tfrac12$. The work does not depend on the entries, so the best case is also $\Theta(n^4)$. Elimination over a field needs only $\tfrac23 n^3$ for the determinant; the extra factor $n$ is the price of having no division.

**Bit operations over $\mathbb{Z}$.** Let $|a_{ij}| \le B < 2^b$. An entry of $S^j$ is at most $s^{j-1}B^j$, so every $\rho S^j \gamma$ has at most $n(b + \log_2 n)$ bits. Every coefficient of every $\chi_{A_r}$ is a signed sum of at most $2^n$ principal minors, each bounded by the [Hadamard bound](/hadamard-bound/), so it also has $O(n(b + \log n))$ bits. In line L8 one factor of each product is an entry of $S$, with $b$ bits, so the vector-matrix products cost $O(n^5 b (b + \log n))$ in total. Line L9 multiplies two large numbers $O(n^3)$ times in total, for $O(n^5 (b + \log n)^2)$. The total is $O(n^5 (b + \log n)^2)$ bit operations with schoolbook arithmetic, the same order as the [Bareiss algorithm](/bareiss-algorithm/). These bounds are proved; they are not tight for random matrices, whose minors are usually much smaller than the Hadamard bound.

**Space.** Besides the input, the algorithm keeps the lists $p$, $q$ and $v$, of length at most $n + 1$: $\Theta(n)$ ring elements.

**With fast matrix multiplication.** The vectors $\rho S^k$ for $k < s$ can be computed by doubling: from the rows $\rho, \rho S, \dots, \rho S^{t-1}$, one product with $S^t$ gives the next $t$ rows, and $S^{2t}$ is one squaring. That is $O(\log s)$ matrix products per step, and $O(n^{\omega + 1} \log n)$ ring operations in total.

## Properties

- **Division-free.** Only $+$, $-$ and $\times$ are used, and no element is tested for zero. The algorithm is a straight-line program, the same sequence of operations for every input of size $n$.
- **Any commutative ring.** The proof needs only commutativity and $1$. Over $\mathbb{Z}/m\mathbb{Z}$ with composite $m$, the result is the reduction of the integer characteristic polynomial; over $\mathbb{Z}/2^{64}$ it runs directly on machine words with wrap-around.
- **All the coefficients at once.** The characteristic polynomial gives $\det A$, $\operatorname{tr} A$ and every sum of principal minors, and the characteristic polynomial of every trailing block $A_r$ appears on the way.
- **Deterministic and data-independent.** No pivoting, so no branching on the data, which suits hardware and constant-time code.
- **Parallel.** The quantities $\rho S^j \gamma$ for all $j$ and all blocks come from powers of matrices, and the product of the $n$ Toeplitz matrices is a balanced product tree. Both take depth $O(\log^2 n)$ with polynomially many processors, so the determinant over any commutative ring is in [NC](/nc/) $^2$.

## Variants and improvements

- **Parallel Berkowitz.** The 1984 paper organizes the computation as above: compute all needed powers by repeated squaring and multiply the Toeplitz matrices in a tree, for depth $O(\log^2 n)$ and $O(n^{\omega+1})$ processors up to logarithmic factors. Csanky's 1976 parallel method has the same depth but divides by $1, 2, \dots, n$, so it needs characteristic $0$ or larger than $n$.
- **Fast matrix multiplication.** With the doubling step above, the sequential cost is $O(n^{\omega+1} \log n)$.
- **Faster division-free determinants.** Kaltofen (1992) gave a division-free determinant with about $n^{3.5}$ ring operations, by running Wiedemann's method over a polynomial ring with baby steps and giant steps. Kaltofen and Villard later lowered the exponent below $3$. These methods are much more complex.
- **Chistov's algorithm** is another division-free method with $O(n^4)$ ring operations, which writes $\det(I - xA)$ through power series modulo $x^{n+1}$ attached to the leading principal blocks; it also parallelizes.
- **Divisions allowed.** Over a field, reduction to [Hessenberg form](/hessenberg-reduction/) followed by a recurrence gives $\chi_A$ in $O(n^3)$ field operations, and over $\mathbb{Z}$ a multimodular version is faster than Berkowitz for large $n$. See [characteristic polynomial computation](/characteristic-polynomial-computation/).
- **Characteristic $0$ alternative.** The [Faddeev-LeVerrier algorithm](/faddeev-leverrier-algorithm/) also avoids pivoting, but divides by $1, \dots, n$.

## When to use it

Use Berkowitz when the entries lie in a ring where division is impossible or expensive: residues modulo a composite number or a power of $2$, polynomials in several variables, symbolic entries, or a ring given only by its operations. It is also a good choice for small $n$ when a short, branch-free and exact method is wanted, and as the base of parallel determinant algorithms. For large matrices over a field or over $\mathbb{Z}$, the $O(n^3)$ methods with divisions are faster.

## Pitfalls

- **The sign of the determinant.** The last coefficient is $\chi_A(0) = (-1)^n \det A$. Forgetting the factor $(-1)^n$ gives the wrong sign for odd $n$.
- **Row and column of the border.** The step needs $\rho S^j \gamma$ with $\rho$ the row and $\gamma$ the column of the border. Using the row twice computes the characteristic polynomial of a different matrix; the tests with non-symmetric matrices catch this.
- **The Toeplitz shape.** The matrix $T$ has $s + 2$ rows and $s + 1$ columns. Keeping only $s + 1$ coefficients of the product drops the constant term, and keeping the full product of length $2s + 2$ gives a polynomial of the wrong degree.
- **Intermediate growth.** Over $\mathbb{Z}$ the vectors $\rho S^k$ have entries up to $n(b + \log_2 n)$ bits even when the result is small. Use big integers, or work modulo primes and combine.
- **The empty matrix.** For $n = 0$ the answer is the polynomial $1$, and the determinant is $1$.

## Implementations

## History

Paul Samuelson gave the bordering recurrence in 1942, as a way to compute the coefficients of the characteristic equation directly. Stuart Berkowitz showed in 1984 that it uses no division and that it can be organized as an iterated product of Toeplitz matrices, which put the determinant over every commutative ring in $\mathrm{NC}^2$. The method is often called the Samuelson-Berkowitz algorithm, and computer algebra systems such as SymPy provide it as a division-free method.

## References
