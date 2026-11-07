---
tag: PAZPAT
kind: problem
slug: rational-canonical-form
name: Rational canonical form
aliases: [Frobenius form, Frobenius normal form, invariant factor form]
area: algebra/exact-linear-algebra
level: advanced
summary: Find a similarity transformation to block companion matrices, valid over any field.
prereqs: [matrix-minimal-polynomial, characteristic-polynomial, smith-normal-form]
see_also: [jordan-normal-form, minimal-polynomial-computation, characteristic-polynomial-computation, krylov-subspace, cayley-hamilton-theorem, companion-matrix-method, primary-decomposition, linear-feedback-shift-register]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition, Prentice Hall, 1971
    locator: Section 7.2, Cyclic Decompositions and the Rational Form, and Section 7.4, Computation of Invariant Factors (the Smith form of xI - A)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 3.3, The minimal polynomial and the companion matrix
  - paper: "Mark Giesbrecht, Nearly optimal algorithms for canonical matrix forms, SIAM Journal on Computing 24(5), 1995"
    locator: pp. 948 to 969 (randomized computation of the Frobenius form and a transform with about as many field operations as matrix multiplication, up to logarithmic factors)
  - paper: "Arne Storjohann, An O(n^3) algorithm for the Frobenius normal form, ISSAC 1998"
    locator: pp. 101 to 104 (a deterministic algorithm in O(n^3) field operations)
  - paper: "Arne Storjohann, Deterministic computation of the Frobenius form, 42nd IEEE Symposium on Foundations of Computer Science (FOCS), 2001"
    locator: pp. 368 to 377 (the Frobenius form deterministically in O(n^ω log n log log n) field operations)
---

The rational canonical form, or Frobenius form, of an $n \times n$ matrix $A$ over a field $K$ is the unique block diagonal matrix $F = \operatorname{diag}(C(f_1), \ldots, C(f_k))$ similar to $A$, where each $C(f_i)$ is the companion matrix of a monic polynomial and $f_1 \mid f_2 \mid \cdots \mid f_k$. The problem asks for $F$ and often for an invertible $P$ with $P^{-1} A P = F$. Unlike the [Jordan normal form](/jordan-normal-form/), it needs no eigenvalues and no field extension, so it can be computed exactly with field operations only, and it decides whether two matrices are similar.

## In plain words

A square table of numbers describes a linear map, and a change of coordinates gives another table for the same map. The question is which tables describe the same map. The rational canonical form is one standard table for each map: a chain of blocks along the diagonal, each block a simple pattern built from the coefficients of a polynomial, with each polynomial dividing the next.

Two tables describe the same map in different coordinates exactly when they have the same standard table. The form is built with ordinary arithmetic, without finding roots of polynomials.

## Definition

**Notation.** $K$ is a field and $A$ an $n \times n$ matrix over $K$. For a monic $f = x^d + c_{d-1} x^{d-1} + \cdots + c_0$, the *companion matrix* $C(f)$ is the $d \times d$ matrix with ones just below the diagonal, last column $(-c_0, \ldots, -c_{d-1})^T$, and zeros elsewhere. It has [minimal polynomial](/matrix-minimal-polynomial/) and [characteristic polynomial](/characteristic-polynomial/) both equal to $f$. $\omega$ is the exponent of matrix multiplication.

**Input.** An $n \times n$ matrix $A$ over $K$.

**Output.** Monic nonconstant polynomials $f_1 \mid f_2 \mid \cdots \mid f_k$, the *invariant factors* of $A$, such that $A$ is similar to $F = \operatorname{diag}(C(f_1), \ldots, C(f_k))$; and, in the version with transform, an invertible $P$ over $K$ with $P^{-1} A P = F$.

**Theorem.** Every $A$ has exactly one such sequence. The $f_i$ are the nonconstant diagonal entries of the [Smith normal form](/smith-normal-form/) of $x I - A$ over $K[x]$, $f_k = \mu_A$ is the minimal polynomial, and $f_1 f_2 \cdots f_k = \chi_A$. Two matrices over $K$ are similar if and only if they have the same invariant factors.

*Sketch.* $K^n$ becomes a $K[x]$-module with $x \cdot v = A v$, and $x I - A$ is a presentation matrix of it. The structure theorem for finitely generated modules over the principal ideal domain $K[x]$ gives $K^n \cong \bigoplus_i K[x] / (f_i)$ with $f_1 \mid \cdots \mid f_k$, unique, and read from the Smith form of $x I - A$. In the basis $v, x v, \ldots, x^{d-1} v$ of a cyclic summand $K[x]/(f)$ of degree $d$, multiplication by $x$ has matrix $C(f)$. Similar matrices give isomorphic modules, and conversely. Hoffman and Kunze, Sections 7.2 and 7.4, give the full proof. $\square$

The form does not change when $K$ is enlarged: the Smith form over $K[x]$ is also the Smith form over $L[x]$, because the gcds of the minors, which determine it, are the same.

## Variants

- **Invariant factors only.** Return $f_1, \ldots, f_k$ without $P$. This already decides similarity and gives $\chi_A$ and $\mu_A$.
- **With transform.** Return $P$. Its columns are Krylov bases $v, A v, \ldots, A^{d - 1} v$ of the cyclic summands.
- **Primary rational form.** Factor each $f_i$ into powers of irreducible polynomials (the *elementary divisors*) and use one companion block per prime power. This needs polynomial factorization over $K$.
- **Jordan form.** When every $f_i$ splits into linear factors over $K$, the primary form can be refined to the [Jordan normal form](/jordan-normal-form/).
- **Similarity test.** Decide whether $A$ and $B$ are similar, and find $P$ with $P^{-1} A P = B$ if so.
- **Over $\mathbb{Q}$ by bits.** The $f_i$ have integer coefficients when $A$ is an integer matrix, and multimodular algorithms compute them modulo many primes.

## Examples

**Diagonal with a repeated eigenvalue.** $A = \operatorname{diag}(2, 2, 3)$ has $\chi_A = (x - 2)^2 (x - 3)$ and $\mu_A = (x - 2)(x - 3) = x^2 - 5 x + 6$, so $f_1 = x - 2$ and $f_2 = x^2 - 5 x + 6$. With $P$ whose columns are $e_1$, $v = (0, 1, 1)$ and $A v = (0, 2, 3)$,

$$P = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 2 \\ 0 & 1 & 3 \end{pmatrix}, \qquad P^{-1} A P = \begin{pmatrix} 2 & 0 & 0 \\ 0 & 0 & -6 \\ 0 & 1 & 5 \end{pmatrix} = \operatorname{diag}(C(x - 2), C(x^2 - 5 x + 6)).$$

**No eigenvalues in $K$.** Over $\mathbb{Q}$, $R = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ is already $C(x^2 + 1)$. It has no Jordan form over $\mathbb{Q}$, but its Frobenius form exists and is the same over $\mathbb{Q}$, $\mathbb{R}$ and $\mathbb{C}$.

**Similarity.** $J = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ and $I_2$ have the same characteristic polynomial $(x - 1)^2$, but the invariant factors are $(x - 1)^2$ for $J$ and $x - 1$, $x - 1$ for $I_2$, so they are not similar.

**Scalar and nonderogatory extremes.** $c I_n$ has $n$ invariant factors, all $x - c$. A matrix with $\mu_A = \chi_A$ has one invariant factor and is similar to the single companion matrix $C(\chi_A)$.

**Edge cases.** The $0 \times 0$ matrix has no invariant factors ($k = 0$), and a $1 \times 1$ matrix $(a)$ has the single factor $x - a$.

## Known algorithms

- **Smith form of $x I - A$.** Elimination over $K[x]$ with polynomial gcds gives the invariant factors in polynomially many field operations, but the intermediate polynomials can have degree up to $n$ in $n^2$ entries.
- **Krylov and cyclic decomposition methods.** Build Krylov subspaces $\langle v, A v, \ldots \rangle$ to split off cyclic summands one after another, with elimination on the Krylov matrices; these give the transform as well.
- **Storjohann (1998):** a deterministic algorithm in $O(n^3)$ field operations.
- **Giesbrecht (1995):** randomized (Las Vegas) algorithms for the Frobenius form and a transform in about as many field operations as matrix multiplication, up to logarithmic factors, over sufficiently large fields.
- **Storjohann (2001):** deterministic in $O(n^\omega \log n \log \log n)$ field operations.
- **Over $\mathbb{Z}$ and $\mathbb{Q}$.** Compute the form modulo several primes and reconstruct the coefficients with the [Chinese remainder theorem](/chinese-remainder-theorem/); a prime is bad only if the degrees of the invariant factors change modulo $p$, which happens for finitely many primes.

## Bounds

**Algebraic model.** The best deterministic bound is $O(n^\omega \log n \log \log n)$ field operations (Storjohann, 2001), and since $\chi_A = f_1 \cdots f_k$ costs only a few polynomial products, the problem is at least as hard as [characteristic polynomial computation](/characteristic-polynomial-computation/), up to $O(n^2)$ operations. No lower bound better than $\Omega(n^2)$ is proved for computation trees with branching.

**Bit sizes over $\mathbb{Z}$.** For an integer matrix, each $f_i$ is a monic factor of $\chi_A$ in $\mathbb{Z}[x]$ (Gauss's lemma, as for the minimal polynomial). The coefficient of $x^{n - j}$ in $\chi_A$ is a sum of $\binom{n}{j}$ principal minors of order $j$, each bounded by the Hadamard bound $j^{j/2} 2^{j b}$, so all coefficients of $\chi_A$ have $O(n (b + \log n))$ binary digits, and Mignotte's factor bound gives the same order for its factors. The transform $P$ is not unique, and its entries can be much larger. These bounds are proved.

**Reduction modulo primes.** For all but finitely many primes $p$, the invariant factors of $A \bmod p$ are the reductions of those of $A$. At a bad prime the degrees of the invariant factors change, as for $\operatorname{diag}(1, 3)$, whose single invariant factor $(x - 1)(x - 3)$ splits modulo $2$ into the two factors $x + 1$, $x + 1$.

## Reductions

- **To the Smith form over $K[x]$.** The invariant factors are the nonconstant Smith form entries of $x I - A$.
- **To it: characteristic and minimal polynomials.** Both are read off: $\chi_A = \prod_i f_i$ and $\mu_A = f_k$. See [minimal polynomial computation](/minimal-polynomial-computation/).
- **To it: similarity testing.** $A \sim B$ if and only if their Frobenius forms are equal, and then $P_A P_B^{-1}$ conjugates one to the other.
- **To it: matrix functions.** In Frobenius form, the powers and polynomials of $A$ are cheap to compute, block by block.

## Applications

- **Similarity and conjugacy.** Deciding whether two matrices describe the same linear map, for instance in the classification of linear dynamical systems or of representations of cyclic groups.
- **Linear recurrences and shift registers.** A [linear feedback shift register](/linear-feedback-shift-register/) is a companion matrix acting on its state, and the cyclic decomposition of a general linear map splits it into such registers.
- **Matrix powers and exponentials.** The form reduces $A^N$ or $f(A)$ to computations modulo the invariant factors, as in [Kitamasa-style linear recurrence evaluation](/linear-recurrence-nth-term/).
- **Structure of modules.** The form describes $K^n$ as a $K[x]$-module, and the dimension of the centralizer of $A$ is determined by the degrees of the $f_i$.

## References
