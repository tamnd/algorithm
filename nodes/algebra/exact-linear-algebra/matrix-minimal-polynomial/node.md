---
tag: NYWJ4B
kind: definition
slug: matrix-minimal-polynomial
name: Minimal polynomial
aliases: [minimal polynomial of a matrix, minimum polynomial]
area: algebra/exact-linear-algebra
level: core
summary: The monic polynomial of least degree that annihilates a matrix.
prereqs: [characteristic-polynomial, cayley-hamilton-theorem]
see_also: [minimal-polynomial-computation, rational-canonical-form, jordan-normal-form, krylov-subspace, wiedemann-algorithm, berlekamp-massey, black-box-matrix, minimal-polynomial-algebraic-element]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition, Prentice Hall, 1971
    locator: Section 6.3, Annihilating Polynomials (the minimal polynomial, its roots are the characteristic values, and the Cayley-Hamilton theorem)
  - book: isbn:9783319110790
    title: Sheldon Axler, Linear Algebra Done Right, third edition, Springer, 2015
    locator: Section 8.C, Characteristic and Minimal Polynomials
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 3.3, The minimal polynomial and the companion matrix
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 12.3, Linearly recurrent sequences, and Section 12.4, Wiedemann's algorithm and black box linear algebra (the minimal polynomial of a sequence and of a matrix)
---

The *minimal polynomial* $\mu_A$ of a square matrix $A$ over a field $K$ is the monic polynomial of least degree with $\mu_A(A) = 0$. Every polynomial that kills $A$ is a multiple of it, it divides the [characteristic polynomial](/characteristic-polynomial/), and it has the same roots. It is the largest invariant factor of $A$, it tells whether $A$ is diagonalizable, and it is what the [Wiedemann algorithm](/wiedemann-algorithm/) computes from a few matrix-vector products.

## Definition

**Notation.** $K$ is a field and $A$ an $n \times n$ matrix over $K$. For a polynomial $f = \sum_i c_i x^i \in K[x]$, $f(A) = \sum_i c_i A^i$ with $A^0 = I_n$. $\chi_A = \det(x I - A)$ is the characteristic polynomial.

**The annihilator.** The set $\operatorname{Ann}(A) = \{ f \in K[x] : f(A) = 0 \}$ is an ideal of $K[x]$: it is closed under sums, and $(g f)(A) = g(A) f(A) = 0$ when $f(A) = 0$.

**Definition.** The *minimal polynomial* of $A$ is the unique monic generator $\mu_A$ of $\operatorname{Ann}(A)$.

**Why it exists and is unique.** The $n^2 + 1$ matrices $I, A, \ldots, A^{n^2}$ lie in the space $K^{n \times n}$ of dimension $n^2$, so they are [linearly dependent](/linear-independence/), and a dependence is a nonzero $f \in \operatorname{Ann}(A)$. (The [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) gives the better witness $\chi_A$, of degree $n$.) Take a monic $\mu \in \operatorname{Ann}(A)$ of least degree $d$. For any $f \in \operatorname{Ann}(A)$, divide: $f = q \mu + r$ with $\deg r < d$. Then $r(A) = f(A) - q(A) \mu(A) = 0$, so $r = 0$ by the choice of $d$, and $\mu$ divides $f$. Two monic generators divide each other, so they are equal.

**Equivalent description.** $d = \deg \mu_A$ is the least $d$ such that $A^d$ is a linear combination of $I, A, \ldots, A^{d-1}$, and the coefficients of that combination give $\mu_A = x^d - \sum_{i < d} c_i x^i$.

**Minimal polynomial of a vector.** For $v \in K^n$, the monic generator $\mu_{A, v}$ of $\{ f : f(A) v = 0 \}$ is the minimal polynomial of $v$ with respect to $A$. Its degree is the dimension of the [Krylov subspace](/krylov-subspace/) spanned by $v, A v, A^2 v, \ldots$, and $\mu_A = \operatorname{lcm}(\mu_{A, e_1}, \ldots, \mu_{A, e_n})$, since $f(A) = 0$ if and only if $f(A) e_i = 0$ for every unit vector $e_i$.

**Facts.**

1. $\mu_A$ divides $\chi_A$, so $1 \le \deg \mu_A \le n$ for $n \ge 1$. *Proof.* $\chi_A \in \operatorname{Ann}(A)$ by Cayley-Hamilton.
2. $\mu_A$ and $\chi_A$ have the same roots in every extension field $L$ of $K$. *Proof.* If $A v = \lambda v$ with $v \ne 0$, then $0 = \mu_A(A) v = \mu_A(\lambda) v$, so $\mu_A(\lambda) = 0$. Conversely a root of $\mu_A$ is a root of $\chi_A$ by Fact 1. So they have the same irreducible factors over $K$.
3. $\mu_A$ does not change when $K$ is enlarged. *Proof.* $\deg \mu_A$ is the least $d$ for which $I, A, \ldots, A^d$ are dependent, and the dependence of vectors with entries in $K$ is decided by the [rank](/rank/) of a matrix over $K$, which is the same over $L$. The coefficients solve a linear system over $K$ with a unique solution, so they lie in $K$.
4. Similar matrices have the same minimal polynomial, since $f(S^{-1} A S) = S^{-1} f(A) S$.
5. $\mu_A$ is the last (largest) invariant factor of $A$, the last diagonal entry of the Smith form of $x I - A$ over $K[x]$; see the [rational canonical form](/rational-canonical-form/). In the [Jordan normal form](/jordan-normal-form/), the exponent of $x - \lambda$ in $\mu_A$ is the size of the largest Jordan block for $\lambda$.
6. $A$ is diagonalizable over $K$ if and only if $\mu_A$ is a product of distinct linear factors over $K$.
7. For an integer matrix $A$, $\mu_A \in \mathbb{Z}[x]$. *Proof.* $\mu_A$ is monic and divides the monic integer polynomial $\chi_A$, so by Gauss's lemma it has integer coefficients.
8. Reduction modulo a prime can lower the degree: the minimal polynomial of $A \bmod p$ divides $\mu_A \bmod p$, and the division can be proper (Example 5). It is equal for all but finitely many primes.

The conventions for small sizes: for $n = 0$, $K^{0 \times 0}$ has only the zero matrix, which equals $I_0$, so $\mu = 1$. For $n \ge 1$, $\mu_A = 1$ is impossible because $1(A) = I \ne 0$.

## Examples and non-examples

1. **Scalar matrices.** $\mu_{c I_n} = x - c$ for $n \ge 1$, while $\chi = (x - c)^n$. So $\mu_{0} = x$ for the zero matrix of size $n \ge 1$.
2. **A Jordan block.** For $A = \begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 2 \end{pmatrix}$, $\chi_A = (x - 2)^3$ and $\mu_A = (x - 2)^2 = x^2 - 4x + 4$: $A - 2I \ne 0$ but $(A - 2I)^2 = 0$. The largest Jordan block has size $2$, and $A$ is not diagonalizable.
3. **Diagonalizable with a repeated eigenvalue.** $D = \operatorname{diag}(2, 2, 3)$ has $\chi_D = (x - 2)^2 (x - 3)$ and $\mu_D = (x - 2)(x - 3) = x^2 - 5x + 6$. For $v = e_1$, $\mu_{D, v} = x - 2$, and for $v = (1, 0, 1)$, $\mu_{D, v} = \mu_D$.
4. **Irreducible over $\mathbb{Q}$.** $R = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ has $\mu_R = \chi_R = x^2 + 1$. Over $\mathbb{Q}$ it is irreducible and $R$ is not diagonalizable; over $\mathbb{C}$ it splits into distinct factors and $R$ is. Over $\mathbb{F}_2$, $x^2 + 1 = (x + 1)^2$, and $R \equiv \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \ne I$, so the minimal polynomial stays $(x + 1)^2$ and $R$ is not diagonalizable modulo $2$.
5. **Reduction drops the degree.** $A = \operatorname{diag}(1, 3)$ has $\mu_A = (x - 1)(x - 3) = x^2 - 4x + 3$. Modulo $2$, $A \equiv I$, so its minimal polynomial is $x + 1$, a proper divisor of $\mu_A \bmod 2 = x^2 + 1 = (x + 1)^2$.
6. **Companion matrices.** The companion matrix of a monic $f$ of degree $n$ has $\mu = \chi = f$, because $e_1, C e_1, \ldots, C^{n-1} e_1$ are the unit vectors $e_1, \ldots, e_n$, so no polynomial of degree below $n$ kills $e_1$. For example $\begin{pmatrix} 0 & 0 & 2 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$ has $\mu = x^3 - 2$. Matrices with $\mu_A = \chi_A$ are called *nonderogatory*.
7. **Non-example: the characteristic polynomial.** $\chi_A$ always kills $A$ but is not minimal in general, as Examples 1 to 3 show. A random matrix over a large field is nonderogatory with high probability, which is why the two are often confused.
8. **Non-example: the minimal polynomial of an algebraic number.** For an algebraic number $\alpha$, the [minimal polynomial](/minimal-polynomial-algebraic-element/) is always irreducible. For a matrix it need not be, as in Examples 2 and 3. They agree when $A$ is the matrix of multiplication by $\alpha$ on $K(\alpha)$.

## Related definitions

- [Characteristic polynomial](/characteristic-polynomial/): $\det(x I - A)$, a multiple of $\mu_A$ with the same irreducible factors.
- [Rational canonical form](/rational-canonical-form/): the invariant factors $f_1 \mid f_2 \mid \cdots \mid f_r$ with $f_r = \mu_A$ and $f_1 \cdots f_r = \chi_A$.
- [Jordan normal form](/jordan-normal-form/): over an algebraically closed field, the block sizes refine the exponents of $\mu_A$.
- **Minimal polynomial of a sequence.** For a linearly recurrent sequence $(a_i)$, the monic generator of the recurrences it satisfies, found by [Berlekamp-Massey](/berlekamp-massey/). The sequence $a_i = u^T A^i v$ has a minimal polynomial that divides $\mu_{A, v}$, and Wiedemann's method rests on this.
- [Black box matrix](/black-box-matrix/): a matrix known only through $v \mapsto A v$, for which the minimal polynomial is the main tool.
- [Minimal polynomial computation](/minimal-polynomial-computation/): the algorithms that find $\mu_A$.

## References
