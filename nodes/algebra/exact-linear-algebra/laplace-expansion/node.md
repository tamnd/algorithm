---
tag: 5K370Y
kind: theorem
slug: laplace-expansion
name: Laplace expansion
aliases: [cofactor expansion, expansion by minors, Laplace's formula]
area: algebra/exact-linear-algebra
level: core
summary: A formula computing a determinant by expanding along any row or column as a sum of entries times determinants of smaller minors.
prereqs: [determinant, permutation]
see_also: [cramers-rule, matrix-inversion, determinant-computation, bareiss-algorithm, berkowitz-algorithm, hadamard-bound, characteristic-polynomial]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition, Prentice Hall, 1971
    locator: Chapter 5, Determinants (the expansion by minors along a row or a column, the classical adjoint and the identity adj(A) A = det(A) I, over a commutative ring with identity)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 0.3, Determinants (Laplace expansion by minors along a row or column, and the adjugate)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.5, Modular determinant computation (the size bound for the determinant and the minors of an integer matrix, and the modular method that avoids expansion)
  - book: "Thomas Muir, The Theory of Determinants in the Historical Order of Development, Volume 1, Macmillan, 1906"
    locator: the account of Laplace's memoir of 1772 and its expansion by complementary minors
---

The Laplace expansion writes the [determinant](/determinant/) of an $n \times n$ matrix as a signed sum, along one row or one column, of each entry times the determinant of the $(n-1) \times (n-1)$ matrix left when its row and column are deleted. It holds over every commutative ring, uses no division, and gives the adjugate identity $A \operatorname{adj}(A) = \det(A) I$, from which [Cramer's rule](/cramers-rule/) and the formula for the inverse follow. As an algorithm it costs about $(e - 1) \, n!$ multiplications, so it is used for small or very sparse matrices and for proofs, while [elimination](/determinant-computation/) is used to compute.

## Statement

**Notation.** $R$ is a commutative ring with $1$ (for example $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{Z}/p\mathbb{Z}$ or a polynomial ring), and $A = (a_{ij})$ is an $n \times n$ matrix over $R$ with $n \ge 1$. $A_{ij}$ is the $(n-1) \times (n-1)$ matrix obtained by deleting row $i$ and column $j$ of $A$; its determinant is a *minor*, and $C_{ij} = (-1)^{i+j} \det A_{ij}$ is the *cofactor* of $a_{ij}$. The determinant is defined by the Leibniz formula

$$\det A = \sum_{\sigma \in S_n} \operatorname{sgn}(\sigma) \prod_{k=1}^{n} a_{k \sigma(k)}, \qquad \operatorname{sgn}(\sigma) = (-1)^{\operatorname{inv}(\sigma)},$$

where $\operatorname{inv}(\sigma)$ is the number of pairs $k < l$ with $\sigma(k) > \sigma(l)$, and the $0 \times 0$ matrix has determinant $1$.

**Theorem.** For each row $i$ and each column $j$,

$$\det A = \sum_{j=1}^{n} a_{ij} C_{ij} \quad \text{(expansion along row } i\text{)}, \qquad \det A = \sum_{i=1}^{n} a_{ij} C_{ij} \quad \text{(expansion along column } j\text{)}.$$

**Expansion by alien cofactors.** For rows $i \neq k$, $\sum_{j} a_{kj} C_{ij} = 0$, and for columns $j \neq l$, $\sum_{i} a_{il} C_{ij} = 0$. With the *adjugate* $\operatorname{adj}(A) = (C_{ji})_{i,j}$, the transpose of the matrix of cofactors, these statements together say

$$A \operatorname{adj}(A) = \operatorname{adj}(A) A = \det(A) \, I_n.$$

**Generalized form.** For a set $I$ of $k$ rows, $\det A = \sum_{J} (-1)^{\sum I + \sum J} \det A[I, J] \det A[\bar I, \bar J]$, where $J$ runs over the sets of $k$ columns, $A[I, J]$ is the submatrix in rows $I$ and columns $J$, and $\bar I$, $\bar J$ are the complements. The case $k = 1$ is the row expansion. This form is stated for reference and is not proved on this page; see Muir and Horn and Johnson.

## In plain words

A determinant of a big square table of numbers can be reduced to determinants of smaller tables. Pick one row. For each number in that row, cross out its row and its column, and take the determinant of what is left. Multiply it by the number, give it a plus or minus sign by a checkerboard pattern, and add everything up.

You can pick any row or any column, and the answer is the same. A row with many zeros is the best choice, because each zero removes a whole smaller determinant from the sum. The rule needs only multiplication, addition and subtraction, so it works for integers, for polynomials and for remainders, with no fractions.

## Proof

**Row expansion.** Fix the row $i$. Group the terms of the Leibniz formula by the value $j = \sigma(i)$:

$$\det A = \sum_{j=1}^{n} a_{ij} \, S_j, \qquad S_j = \sum_{\sigma \in S_n,\, \sigma(i) = j} \operatorname{sgn}(\sigma) \prod_{k \neq i} a_{k \sigma(k)}.$$

It remains to show $S_j = (-1)^{i+j} \det A_{ij}$. Number the rows of $A_{ij}$ by the rows $k \neq i$ of $A$ in their order, and its columns by the columns $l \neq j$ of $A$ in their order. A permutation $\sigma$ with $\sigma(i) = j$ is the same as a bijection from the rows $k \neq i$ to the columns $l \neq j$, and with the numbering above this is a permutation $\pi \in S_{n-1}$. The map $\sigma \mapsto \pi$ is a bijection from $\{\sigma : \sigma(i) = j\}$ to $S_{n-1}$, and $\prod_{k \neq i} a_{k \sigma(k)}$ is exactly the Leibniz product of $\pi$ in $A_{ij}$.

Now compare the inversions. A pair $k < l$ with $k, l \neq i$ is an inversion of $\sigma$ if and only if the corresponding pair is an inversion of $\pi$, because the renumbering keeps the order of rows and of columns. The other inversions of $\sigma$ are the pairs that contain $i$. Let $a$ be the number of $k < i$ with $\sigma(k) > j$. Then $(i - 1) - a$ of the $k < i$ have $\sigma(k) < j$. Exactly $j - 1$ indices $k \neq i$ have $\sigma(k) < j$, so $(j-1) - (i-1) + a = j - i + a$ of the indices $k > i$ have $\sigma(k) < j$. The pairs that contain $i$ and are inversions are the $a$ pairs $(k, i)$ with $k < i$, $\sigma(k) > j$, and the $j - i + a$ pairs $(i, k)$ with $k > i$, $\sigma(k) < j$. So

$$\operatorname{inv}(\sigma) = \operatorname{inv}(\pi) + (j - i) + 2a, \qquad \operatorname{sgn}(\sigma) = (-1)^{i+j} \operatorname{sgn}(\pi).$$

Summing over $\pi \in S_{n-1}$ gives $S_j = (-1)^{i+j} \det A_{ij}$, which proves the row expansion. For $n = 1$ it reads $\det A = a_{11} \cdot 1$.

**Column expansion.** The map $\sigma \mapsto \sigma^{-1}$ is a bijection of $S_n$ with $\operatorname{inv}(\sigma^{-1}) = \operatorname{inv}(\sigma)$ (a pair of positions $k < l$ with $\sigma(k) > \sigma(l)$ corresponds to the pair of values $\sigma(l) < \sigma(k)$ inverted by $\sigma^{-1}$), and $\prod_k a_{k \sigma(k)} = \prod_l a_{\sigma^{-1}(l) l}$. So $\det A^T = \det A$. The column expansion of $A$ is the row expansion of $A^T$, since $(A^T)_{ji} = (A_{ij})^T$.

**Alien cofactors.** Let $k \neq i$ and let $B$ be $A$ with row $i$ replaced by row $k$. Then $B_{ij} = A_{ij}$ for each $j$, so the row expansion of $B$ along row $i$ is $\sum_j a_{kj} C_{ij}$. The matrix $B$ has two equal rows $i$ and $k$, and its determinant is $0$: with the transposition $\tau = (i \; k)$, the map $\sigma \mapsto \sigma \tau$ pairs the permutations of $S_n$ without fixed points of the pairing, the two terms of a pair have the same product because rows $i$ and $k$ of $B$ are equal, and their signs are opposite. So the terms cancel in pairs, with no division by $2$, over every commutative ring. This gives $\sum_j a_{kj} C_{ij} = 0$, and the column statement follows from it for $A^T$. Entry $(k, i)$ of $A \operatorname{adj}(A)$ is $\sum_j a_{kj} C_{ij}$, which is $\det A$ for $k = i$ and $0$ otherwise; the same for $\operatorname{adj}(A) A$ with columns. $\blacksquare$

The sign rule used here is $\operatorname{sgn}(\sigma \tau) = -\operatorname{sgn}(\sigma)$ for a transposition $\tau = (i \; k)$ with $i < k$. The permutation $\sigma \tau$ swaps the values at the positions $i$ and $k$. Pairs of positions that avoid $i$ and $k$ keep their status. The pair $(i, k)$ changes status. For a position $l$ outside the range from $i$ to $k$, the pairs $(l, i)$ and $(l, k)$ exchange their values, so their number of inversions does not change. For a position $l$ with $i < l < k$, both pairs $(i, l)$ and $(l, k)$ change status when $\sigma(l)$ lies between $\sigma(i)$ and $\sigma(k)$, and they exchange their status otherwise. So the number of inversions changes by an odd number. $\square$

## Consequences

**A worked expansion.** Let

$$A = \begin{pmatrix} 2 & 0 & 1 & 3 \\ 1 & -1 & 0 & 2 \\ 0 & 4 & 1 & 1 \\ 3 & 0 & 2 & -1 \end{pmatrix}.$$

Column $2$ has two zeros, so expand along it. The cofactor signs in column $2$ are $-, +, -, +$. The two nonzero terms are $a_{22} C_{22} = (-1) \cdot \det \begin{pmatrix} 2 & 1 & 3 \\ 0 & 1 & 1 \\ 3 & 2 & -1 \end{pmatrix} = (-1)(-12) = 12$ and $a_{32} C_{32} = 4 \cdot (-1) \cdot \det \begin{pmatrix} 2 & 1 & 3 \\ 1 & 0 & 2 \\ 3 & 2 & -1 \end{pmatrix} = -4 \cdot 5 = -20$. So $\det A = 12 - 20 = -8$, the same value as the Leibniz sum over all $24$ permutations.

**Inverse and Cramer's rule.** If $\det A$ is a unit of $R$, the adjugate identity gives $A^{-1} = \det(A)^{-1} \operatorname{adj}(A)$. So a square matrix over $R$ is invertible over $R$ if and only if its determinant is a unit; over $\mathbb{Z}$ this is the definition of a [unimodular matrix](/unimodular-matrix/). Applied to $A x = b$, it gives [Cramer's rule](/cramers-rule/), $x_j = \det A^{(j)} / \det A$, where $A^{(j)}$ is $A$ with column $j$ replaced by $b$. Over $\mathbb{Z}$ this shows that the solution of a nonsingular integer system has the common denominator $\det A$ and numerators that are minors, so by the [Hadamard bound](/hadamard-bound/) both have at most about $n (b + \tfrac12 \log_2 n)$ binary digits when the entries have $b$ digits. This bound is what [matrix inversion](/matrix-inversion/), [Dixon lifting](/dixon-p-adic-lifting/) and the [multimodular determinant](/multimodular-determinant/) rely on.

**Triangular and block triangular matrices.** Expansion along the first column of an upper triangular matrix leaves one term, so by induction its determinant is the product of the diagonal. The same induction, expanding along the first column $k$ times, gives $\det \begin{pmatrix} B & C \\ 0 & D \end{pmatrix} = \det B \det D$ for square blocks $B$ and $D$.

**Linearity in each row.** The row expansion shows that $\det A$ is a linear function of row $i$ when the other rows are fixed, because the cofactors $C_{ij}$ do not depend on row $i$. This linearity is one of the axioms that characterize the determinant.

**Characteristic polynomial.** Expanding $\det(x I - A)$ shows that it is a monic polynomial of degree $n$ in $x$ with coefficients in $R$; see [characteristic polynomial](/characteristic-polynomial/).

**As an algorithm.** Recursive expansion along the first row with no reuse does $M(n)$ multiplications, where $M(1) = 0$ and $M(n) = n (M(n-1) + 1)$. This gives $M(2) = 2$, $M(3) = 9$, $M(4) = 40$, $M(5) = 205$, and in general $M(n) = n! \sum_{k=1}^{n-1} 1/k!$, which tends to $(e - 1) \, n!$. If the minors are stored by their set of columns (expanding row $1$, then row $2$ of each minor, and so on), each subset $S$ of columns appears once, and the cost falls to $\sum_{s} s \binom{n}{s} = n 2^{n-1}$ multiplications, still exponential. Over $\mathbb{Z}$ all intermediate values are minors of $A$, so they obey the Hadamard bound, and there is no growth of numbers beyond it. For comparison, [Gaussian elimination](/determinant-gaussian-elimination/) uses $O(n^3)$ field operations, the [Bareiss algorithm](/bareiss-algorithm/) $O(n^3)$ operations with exact division, and the division-free [Berkowitz algorithm](/berkowitz-algorithm/) $O(n^4)$ ring operations. Expansion is still the practical choice for $n \le 4$ or so, for matrices with a few nonzeros in each row, and for symbolic entries where division is costly.

## Tightness

The expansion is an identity, so the only question is its cost as an algorithm. Each of the $n!$ terms of the Leibniz formula appears exactly once in the full recursive expansion of a matrix with no zero entries, so plain expansion cannot avoid factorial time. The memoized version is limited by the $2^n$ subsets of columns. Both are far above the cost of elimination, $O(n^3)$, or $O(n^\omega)$ field operations with fast matrix multiplication, where $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/); see [determinant computation](/determinant-computation/).

## History

Pierre-Simon Laplace gave the expansion of a determinant by complementary minors, the generalized form above, in a memoir of 1772; the account is in Muir's history. The row and column expansion is its case of one row.

## References
