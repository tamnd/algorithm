---
tag: MFPT9A
kind: problem
slug: characteristic-polynomial-computation
name: Characteristic polynomial computation
aliases:
- computing the characteristic polynomial
- charpoly computation
area: algebra/exact-linear-algebra
level: advanced
summary: Compute the characteristic polynomial det(xI - A) of a square matrix exactly.
prereqs: [characteristic-polynomial]
see_also: [characteristic-polynomial, berkowitz-algorithm, faddeev-leverrier-algorithm, hessenberg-reduction, determinant-computation, matrix-minimal-polynomial, rational-canonical-form, krylov-subspace]
sources:
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.4, Computing the characteristic polynomial (the Hessenberg method over a field, and the modular approach for integer matrices)
  - paper: "Walter Keller-Gehrig, Fast algorithms for the characteristic polynomial, Theoretical Computer Science 36, 1985"
    locator: pp. 309 to 317 (the characteristic polynomial over a field in O(n^ω log n) operations, from Krylov bases computed with fast matrix multiplication)
  - paper: "Clement Pernet and Arne Storjohann, Faster algorithms for the characteristic polynomial, Proceedings of ISSAC 2007, ACM"
    locator: pp. 307 to 314 (a Las Vegas algorithm in O(n^ω) field operations over a sufficiently large field)
  - paper: doi:10.1016/0020-0190(84)90018-8
    title: Stuart J. Berkowitz, On computing the determinant in small parallel time using a small number of processors, Information Processing Letters 18(3), 1984
    locator: pp. 147 to 150 (the division-free characteristic polynomial over any commutative ring, in NC^2)
  - paper: doi:10.1137/0205040
    title: L. Csanky, Fast parallel matrix inversion algorithms, SIAM Journal on Computing 5(4), 1976
    locator: pp. 618 to 623 (the characteristic polynomial from power sums by Newton's identities, in parallel, in characteristic 0)
  - paper: "Erich Kaltofen and Gilles Villard, On the complexity of computing determinants, Computational Complexity 13(3-4), 2004"
    locator: the division-free algorithms for the determinant and the characteristic polynomial with exponent below 3, and the bit complexity for integer matrices
---

Characteristic polynomial computation asks for the coefficients of $\chi_A(x) = \det(xI - A)$ for a square matrix $A$, exactly. The [characteristic polynomial](/characteristic-polynomial/) contains the determinant, the trace and every sum of principal minors, and its roots are the eigenvalues, so the problem is at least as hard as the determinant. Over a field it can still be solved with $O(n^3)$ operations by reduction to Hessenberg form, and with $O(n^\omega)$ by randomized fast methods; without division, the [Berkowitz algorithm](/berkowitz-algorithm/) needs $O(n^4)$ ring operations over any commutative ring. Over $\mathbb{Z}$ the output has $n$ coefficients of $O(n(b + \log n))$ bits each, and modular methods are the practical choice.

Notation: $R$ is a commutative ring, $K$ a field, $A = (a_{ij})$ an $n \times n$ matrix, $\chi_A(x) = \sum_{k=0}^{n} c_k x^k$ with $c_n = 1$, and $E_k(A)$ the sum of the principal minors of order $k$, so that $c_{n-k} = (-1)^k E_k(A)$. $\omega$ is the exponent of matrix multiplication, and for an integer matrix $b$ is the maximum binary length of an entry. Costs are counted in operations of $R$ or $K$ and, over $\mathbb{Z}$, in bit operations.

## In plain words

Every square table of numbers has a characteristic polynomial, whose degree is the size of the table and whose roots are the eigenvalues. Its first coefficient after the leading one is minus the sum of the diagonal, and its last is the determinant, up to sign. The task is to find all of its coefficients exactly. The formula from the definition is far too slow, so methods either transform the table into a simpler shape with the same polynomial or build the polynomial step by step.

## Definition

**Input:** an $n \times n$ matrix $A$ over a commutative ring $R$, given by its entries.

**Output:** the coefficients $c_0, \dots, c_{n-1} \in R$ of $\chi_A(x) = \det(xI - A) = x^n + c_{n-1}x^{n-1} + \cdots + c_0$. For $n = 0$ the output is the polynomial $1$.

In the *arithmetic* model each operation of $R$ or $K$ costs $1$; divisions are allowed only over a field, or where they are known to be exact. In the *bit* model over $\mathbb{Z}$, the coefficient $c_{n-k} = (-1)^k E_k(A)$ is a sum of $\binom{n}{k}$ minors of order $k$, so by the [Hadamard bound](/hadamard-bound/) $|c_{n-k}| \le \binom{n}{k} k^{k/2} B^k$ when $|a_{ij}| \le B$. Each coefficient has $O(n(b + \log n))$ bits, and the whole output has $O(n^2 (b + \log n))$ bits.

## Variants

- **Over a field $K$.** Divisions are allowed, and similarity transformations $A \mapsto P^{-1} A P$ keep $\chi_A$.
- **Over a ring without division.** For $\mathbb{Z}/m\mathbb{Z}$ with composite $m$, polynomial rings in several variables or symbolic entries, only $+$, $-$ and $\times$ may be used.
- **Over $\mathbb{Z}$, bit complexity.** The target is a bound in $n$ and $b$. Since $\chi_{A \bmod p} = \chi_A \bmod p$, the problem splits into problems over prime fields.
- **The minimal polynomial.** Find the monic generator of $\{f : f(A) = 0\}$ instead. It divides $\chi_A$ and equals it when $A$ is nonderogatory; see [minimal polynomial](/matrix-minimal-polynomial/).
- **The Frobenius form.** Find the invariant factors, whose product is $\chi_A$, and a transformation; see [rational canonical form](/rational-canonical-form/).
- **Sparse and black-box matrices.** When $A$ is given by the map $v \mapsto Av$, [Wiedemann's algorithm](/wiedemann-algorithm/) finds the minimal polynomial with $O(n)$ products; the characteristic polynomial needs extra work for the multiplicities of the factors.
- **A few coefficients.** The trace $-c_{n-1}$ costs $n - 1$ additions, and $c_{n-2} = \tfrac12((\operatorname{tr} A)^2 - \operatorname{tr}(A^2))$ in characteristic other than $2$ costs $O(n^2)$, since $\operatorname{tr}(A^2) = \sum_{i,j} a_{ij} a_{ji}$. The constant term is the [determinant](/determinant-computation/).

## Examples

- For $n = 2$, $\chi_A(x) = x^2 - (a_{11} + a_{22})x + (a_{11}a_{22} - a_{12}a_{21})$.
- $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$ has $\chi_M(x) = x^3 - 9x^2 + 24x - 18$. Its values at $x = 0, 1, 2, 3$ are $-18, -2, 2, 0$, so $3$ is an eigenvalue, and $\chi_M(x) = (x - 3)(x^2 - 6x + 6)$. The four values also determine $\chi_M$ by interpolation.
- The companion matrix with rows $(0, 0, -5)$, $(1, 0, 2)$, $(0, 1, 0)$ has $\chi = x^3 - 2x + 5$. So computing eigenvalues includes finding the roots of any monic polynomial.
- Graphs. The adjacency matrix of the path on three vertices has $\chi = x^3 - 2x$, and that of the triangle has $\chi = x^3 - 3x - 2 = (x - 2)(x + 1)^2$. For any simple graph, $c_{n-2}$ is minus the number of edges and $c_{n-3}$ is minus twice the number of triangles.
- Over $\mathbb{Z}/6\mathbb{Z}$, $A = \begin{pmatrix} 2 & 3 \\ 3 & 2 \end{pmatrix}$ has $\chi_A = x^2 - 4x - 5 \equiv x^2 + 2x + 1$. No pivot is invertible modulo $6$, so elimination cannot start; Berkowitz computes the answer with ring operations only.

## Known algorithms

| Algorithm | Ring | Arithmetic cost | Notes |
| --- | --- | --- | --- |
| Sums of principal minors | any commutative | exponential ($2^n$ minors) | the definition; a test reference |
| Interpolation of $\det(x_k I - A)$ | field with $\ge n + 1$ elements | $O(n^4)$, or $O(n^{\omega + 1})$ | $n + 1$ determinants |
| [Faddeev-LeVerrier algorithm](/faddeev-leverrier-algorithm/) | characteristic $0$ or $> n$, or $\mathbb{Z}$ | $2n^4 + O(n^3)$, or $O(n^{\omega+1})$ | gives the adjugate too |
| [Berkowitz algorithm](/berkowitz-algorithm/) | any commutative | $n^4/2 + O(n^3)$, or $O(n^{\omega+1} \log n)$ | division-free, $\mathrm{NC}^2$ |
| [Hessenberg reduction](/hessenberg-reduction/) and a recurrence | field | $O(n^3)$ | Cohen's Algorithm in Section 2.2.4 |
| Danilevsky's method, reduction to companion form | field | $O(n^3)$ | needs restarts when a pivot is $0$ |
| Keller-Gehrig, Krylov bases with fast multiplication | field | $O(n^\omega \log n)$ | deterministic |
| Pernet and Storjohann | field with enough elements | $O(n^\omega)$ | Las Vegas |
| Multimodular | $\mathbb{Z}$ | $O(n^3)$ per prime, $O(n(b + \log n))$ primes | Chinese remaindering of $\chi_{A \bmod p}$ |

The Hessenberg method transforms $A$ by similarity, with elimination steps that pivot like [Gaussian elimination](/gaussian-elimination/), to a matrix $H$ that is zero below the first subdiagonal. The characteristic polynomials of the leading blocks of $H$ then satisfy a recurrence with $O(n^2)$ terms in total, so the second stage costs $O(n^3)$ as well.

Over $\mathbb{Z}$, the multimodular method computes $\chi_A$ modulo word-size primes by the Hessenberg method and combines the coefficients by the Chinese remainder theorem, with a symmetric residue for the signs. The coefficient bound above fixes how many primes are needed, so the method is deterministic with $O(n^4 (b + \log n))$ word operations for the modular stage; this bound is proved. Many implementations stop early when the reconstruction stays stable for a few more primes, which is faster in practice but correct only with high probability.

## Bounds

- **Output size.** Over $\mathbb{Z}$, $|c_{n-k}| \le \binom{n}{k} k^{k/2} B^k$, so each coefficient has at most $n(b + \tfrac12 \log_2 n) + n$ bits. For Hadamard matrices the constant term attains $n^{n/2}$, so the bound on the size of the largest coefficient cannot be much improved.
- **Arithmetic upper bounds.** $O(n^3)$ deterministic by Hessenberg reduction, $O(n^\omega \log n)$ deterministic by Keller-Gehrig, and $O(n^\omega)$ Las Vegas by Pernet and Storjohann.
- **Arithmetic lower bound.** The constant term is $\pm \det A$, so the problem is at least as hard as the determinant, whose exponent is $\omega$. With Pernet and Storjohann's upper bound, the characteristic polynomial has the same exponent $\omega$ as matrix multiplication for randomized algorithms. No lower bound beyond $\Omega(n^2)$ is known.
- **Division-free.** $O(n^4)$ ring operations by Berkowitz, $O(n^{\omega+1} \log n)$ with fast multiplication, and less by the algorithms of Kaltofen and Villard.
- **Parallel time.** Depth $O(\log^2 n)$ over any commutative ring by Berkowitz, and in characteristic $0$ by Csanky, so the problem is in $\mathrm{NC}^2$.

## Reductions

- **Determinant from the characteristic polynomial.** $\det A = (-1)^n c_0$.
- **Characteristic polynomial from determinants.** Over a field with at least $n + 1$ elements, evaluate $\det(x_k I - A)$ at $n + 1$ points and [interpolate](/polynomial-interpolation/). Over a small field, work in an extension field.
- **Krylov sequences.** If $u, Au, \dots, A^{n-1}u$ are linearly independent, the coefficients of $\chi_A$ are the solution of the linear system $\sum_{k<n} c_k A^k u = -A^n u$. Keller-Gehrig computes such a [Krylov](/krylov-subspace/) basis with $O(\log n)$ matrix products by doubling; when no vector generates the whole space, $\chi_A$ is a product of the polynomials of several Krylov blocks.
- **From the Frobenius form.** $\chi_A$ is the product of the invariant factors of $xI - A$, so an algorithm for the [rational canonical form](/rational-canonical-form/) gives $\chi_A$.
- **Eigenvalues and roots.** The eigenvalues are the roots of $\chi_A$, and each monic polynomial is the characteristic polynomial of its companion matrix. So exact eigenvalue computation and polynomial root finding are equivalent up to the cost of $\chi_A$.
- **Integer to modular.** $\chi_{A \bmod m} = \chi_A \bmod m$ for every modulus $m$, which reduces the problem over $\mathbb{Z}$ to prime fields, and over $\mathbb{Z}/m$ to the integer problem.

## Applications

- **Exact eigenvalues.** Factor $\chi_A$ over $\mathbb{Q}$ or a number field to get the eigenvalues exactly, as in the example above, and then the [Jordan normal form](/jordan-normal-form/).
- **Powers and inverses.** By the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/), $A^k$ is the remainder of $x^k$ modulo $\chi_A$ evaluated at $A$, and $A^{-1}$ is a polynomial in $A$.
- **Similarity tests.** Similar matrices have the same characteristic polynomial; a difference proves that two matrices are not similar.
- **Spectral graph theory.** The characteristic polynomial of an adjacency matrix counts edges and triangles in its coefficients, and closed walks in the power sums of its roots.
- **Linear recurrences.** The sequence $u^T A^k v$ satisfies the recurrence with the coefficients of $\chi_A$, which is the basis of [linear recurrence](/linear-recurrence-nth-term/) methods and of Wiedemann's algorithm.

## References
