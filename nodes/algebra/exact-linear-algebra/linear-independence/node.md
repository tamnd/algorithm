---
tag: JA5DBR
kind: concept
slug: linear-independence
name: Linear independence
aliases: [linearly independent, linear dependence]
area: algebra/exact-linear-algebra
level: intro
summary: A set of vectors is independent if no nontrivial linear combination of them is zero.
see_also: [rank, nullspace, rank-nullity-theorem, gaussian-elimination, determinant, reduced-row-echelon-form, xor-gaussian-elimination, lattice-basis]
sources:
  - book: isbn:9783319110790
    title: Sheldon Axler, Linear Algebra Done Right, third edition, Springer, 2015
    locator: Section 2.A, Span and Linear Independence (the definition, the Linear Dependence Lemma, and the fact that an independent list is never longer than a spanning list)
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition, Prentice Hall, 1971
    locator: Section 2.3, Bases and Dimension (independence over an arbitrary field, and the theorem that more than n vectors in a space spanned by n vectors are dependent)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer
    locator: Section 2.3.1, Kernel and image (the elimination algorithm that finds a dependence relation or proves that there is none)
---

A list of vectors $v_1, \ldots, v_k$ over a field $K$ is *linearly independent* when the only combination $c_1 v_1 + \cdots + c_k v_k$ that is the zero vector is the one with $c_1 = \cdots = c_k = 0$. Otherwise the list is *linearly dependent*, and a nonzero coefficient vector $(c_1, \ldots, c_k)$ with sum zero is a *dependence relation*. Independence is the base of [rank](/rank/), of bases and dimension, and of each statement about when a linear system has a unique solution. In exact computation it is tested by [Gaussian elimination](/gaussian-elimination/), and the answer can change when the field changes.

## In plain words

Think of each vector as a direction with a length. A list of vectors is independent when none of them can be built from the others by stretching and adding. If one vector is a mix of the others, it adds nothing new, and the list is dependent.

The test is a question about a system of equations: is there a way to weight the vectors, with at least one weight not zero, so that everything cancels? If the only way is to give every vector the weight zero, the list is independent. Gaussian elimination answers this question exactly.

The answer depends on the kind of numbers you use. Three integer vectors can be independent when you compute with fractions and dependent when you compute with remainders modulo two.

## The idea

**Notation.** $K$ is a field and $R$ is an integral domain with field of fractions $K$ (for example $R = \mathbb{Z}$ and $K = \mathbb{Q}$). For vectors $v_1, \ldots, v_k \in K^m$ let $A$ be the $m \times k$ matrix with columns $v_1, \ldots, v_k$. Then $c_1 v_1 + \cdots + c_k v_k = A c$ for $c = (c_1, \ldots, c_k)^T$.

**Definition.** The list $v_1, \ldots, v_k$ is linearly independent over $K$ when

$$\forall c \in K^k : \quad A c = 0 \implies c = 0.$$

So the list is independent exactly when the [nullspace](/nullspace/) of $A$ is $\{0\}$. The empty list ($k = 0$) is independent, because the only $c \in K^0$ is the empty vector. Independence is a property of a list, not of a set: the list $v, v$ is dependent, since $1 \cdot v + (-1) \cdot v = 0$.

**Equivalent forms.** For $v_1, \ldots, v_k \in K^m$ these statements are equivalent.

1. The list is independent.
2. No $v_j$ is a combination of the others.
3. The [rank](/rank/) of $A$ is $k$.
4. Elimination on $A$ gives a [pivot](/pivot/) in each of the $k$ columns.
5. Some $k \times k$ submatrix of $A$ has a nonzero [determinant](/determinant/).

When $k = m$, statement 5 says $\det A \neq 0$. Statement 2 follows from 1 because a relation $v_j = \sum_{i \neq j} d_i v_i$ gives the dependence relation with $c_j = -1$; for the converse, if $\sum c_i v_i = 0$ with $c_j \neq 0$, divide by $c_j$ to write $v_j$ as a combination of the others. This step uses division, so it needs a field.

**Too many vectors are dependent.** If $k > m$, every list of $k$ vectors in $K^m$ is dependent. Proof: run [Gaussian elimination](/gaussian-elimination/) on $A$. It uses only invertible row operations, so it does not change the solutions of $A c = 0$. The result has at most one pivot in each row, so at most $m < k$ pivot columns. A column without a pivot gives a free unknown. Set it to $1$, set the other free unknowns to $0$, and solve for the pivot unknowns by back substitution. This gives a solution $c \neq 0$. $\square$

**Over an integral domain.** For $v_i \in R^m$, a relation over $K$ becomes a relation over $R$ after multiplication by a common denominator of the $c_i$. So independence over $R$ and over $K$ are the same. Over $\mathbb{Z}$ one can therefore test independence with rational arithmetic, or with fraction-free elimination such as the [Bareiss algorithm](/bareiss-algorithm/).

**Change of field.** Let $v_1, \ldots, v_k \in \mathbb{Z}^m$ be independent over $\mathbb{Q}$, and let $p$ be a prime. The images of the $v_i$ in $(\mathbb{Z}/p\mathbb{Z})^m$ are independent if and only if $p$ does not divide every $k \times k$ minor of $A$. This is statement 5 over $\mathbb{Z}/p\mathbb{Z}$, since a minor of the image is the image of the minor. Because the list is independent over $\mathbb{Q}$, some $k \times k$ minor $\Delta$ is nonzero, and the images stay independent for each prime $p \nmid \Delta$. So only the finitely many primes that divide $\Delta$ can be bad. Modular methods such as the [multimodular determinant](/multimodular-determinant/) and [modular Gaussian elimination](/gaussian-elimination-modular/) rely on this fact. By the [Hadamard bound](/hadamard-bound/), $|\Delta| \le \prod_j \|v_j\|_2$, so at most $\log_2 \prod_j \|v_j\|_2$ primes are bad.

**Cost of the test.** Gaussian elimination decides independence of $k$ vectors in $K^m$ with $O(m k \min(m, k))$ field operations, and returns a dependence relation when there is one. With fast matrix multiplication the cost is $O(m k \min(m,k)^{\omega - 2})$ field operations, where $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/). Over $\mathbb{Z}$ with entries of at most $b$ binary digits, fraction-free elimination keeps each intermediate number a minor of $A$, so by the Hadamard bound it has $O(k (b + \log k))$ digits, and the number of bit operations is polynomial in $m$, $k$ and $b$.

## Examples

**A dependent list over $\mathbb{Q}$.** Take $v_1 = (1, 2, 3)$, $v_2 = (4, 5, 6)$ and $v_3 = (7, 8, 9)$. Then $v_1 - 2 v_2 + v_3 = (1 - 8 + 7, 2 - 10 + 8, 3 - 12 + 9) = (0, 0, 0)$, so the list is dependent. Elimination on the matrix with these columns gives pivots in two columns only, so the rank is $2$. Each two of the three vectors are independent.

**The field matters.** Take $v_1 = (1, 1, 0)$, $v_2 = (0, 1, 1)$ and $v_3 = (1, 0, 1)$. The matrix $A$ with these columns has $\det A = 2$. So the list is independent over $\mathbb{Q}$, and over $\mathbb{Z}/p\mathbb{Z}$ for each odd prime $p$. Over $\mathbb{Z}/2\mathbb{Z}$ the sum $v_1 + v_2 + v_3 = (2, 2, 2)$ is zero, so the list is dependent, and the rank of $A$ modulo $2$ is $2$. The only bad prime is $2$, the only prime that divides $\det A$.

**Standard vectors.** The vectors $e_1, \ldots, e_m$ of $K^m$, where $e_i$ has a $1$ in place $i$ and $0$ elsewhere, are independent: $\sum c_i e_i = (c_1, \ldots, c_m)$, which is zero only if each $c_i$ is zero.

**Lists with a zero vector.** Each list that contains the zero vector is dependent: give the zero vector the coefficient $1$ and the others $0$.

**Monomials.** In the space $K[x]$ of polynomials, the list $1, x, x^2, \ldots, x^d$ is independent, since a combination $\sum c_i x^i$ is the zero polynomial only when each coefficient is zero. Evaluated at $d+1$ distinct points $t_0, \ldots, t_d$, these monomials give the columns of a Vandermonde matrix with determinant $\prod_{i < j} (t_j - t_i) \neq 0$.

**Bit vectors.** Over $\mathbb{Z}/2\mathbb{Z}$ a vector is a string of bits and addition is XOR. The strings $1100$, $0110$ and $1010$ are dependent, because $1100 \oplus 0110 = 1010$. A maximal independent subset of a set of bit strings is an XOR basis, built by [XOR Gaussian elimination](/xor-gaussian-elimination/).

## Where it is used

- **Rank and dimension.** The [rank](/rank/) of a matrix is the largest number of independent columns, and the [rank-nullity theorem](/rank-nullity-theorem/) counts the independent solutions of $A x = 0$.
- **Unique solutions.** A square system $A x = b$ has exactly one solution for each $b$ if and only if the columns of $A$ are independent, that is $\det A \neq 0$. See [determinant](/determinant/) and [matrix inversion](/matrix-inversion/).
- **Echelon forms.** The nonzero rows of an [echelon form](/echelon-form/) or of the [reduced row echelon form](/reduced-row-echelon-form/) are independent, and the pivot columns of the input are a maximal independent set of its columns.
- **Nullspace bases.** A basis of the [nullspace](/nullspace/) is an independent list of solutions; [nullspace computation](/nullspace-computation/) finds one.
- **Lattices.** A [lattice basis](/lattice-basis/) is a list of vectors of $\mathbb{R}^m$ that is independent over $\mathbb{R}$; its integer combinations form the [lattice](/lattice/).
- **Sieve methods.** The [quadratic sieve](/quadratic-sieve/) and [index calculus](/index-calculus/) collect more exponent vectors than their length, so the vectors are dependent modulo $2$ or modulo the group order. A dependence relation, found by the [Wiedemann algorithm](/wiedemann-algorithm/) or [block Lanczos](/block-lanczos-algorithm/), gives the congruence of squares or the logarithm.

## References
