---
tag: WR8F9R
kind: definition
slug: determinant
name: Determinant
aliases: [det]
area: algebra/exact-linear-algebra
level: intro
summary: Alternating multilinear function of the columns of a square matrix that is nonzero exactly when the matrix is invertible.
prereqs: [permutation, linear-independence]
see_also: [determinant-computation, determinant-gaussian-elimination, cramers-rule, laplace-expansion, characteristic-polynomial, rank, hadamard-bound, unimodular-matrix]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition
    locator: Chapter 5, Determinants (Sections 5.2 to 5.4, determinant functions, uniqueness through permutations, and the product rule)
  - book: isbn:9783319110790
    title: Sheldon Axler, Linear Algebra Done Right, third edition
    locator: Chapter 10, Trace and Determinant (Section 10.B, Determinant)
  - book: isbn:9780980232714
    title: Gilbert Strang, Introduction to Linear Algebra, fourth edition
    locator: Chapter 5, Section 5.1, The properties of determinants
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.3, Computing determinants
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 1979
    locator: "the #P-completeness of the permanent of a 0-1 matrix"
---

The determinant of a square matrix $A$ over a field or a commutative ring is the signed sum, over all permutations, of products of one entry from each column and each row. Read as a function of the columns, it is the only function that is linear in each column, is zero when two columns are equal, and is $1$ on the identity matrix. It is nonzero exactly when $A$ is invertible, it is multiplicative, $\det(AB) = \det A \det B$, and it gives the [characteristic polynomial](/characteristic-polynomial/), [Cramer's rule](/cramers-rule/) and the volume of a parallelepiped.

Notation on these pages: $K$ is a field and $R$ is a commutative ring, usually an integral domain such as $\mathbb{Z}$. $A$ is an $n \times n$ matrix with entries $a_{ij}$, where $i$ is the row and $j$ the column, and $[n] = \{1, \dots, n\}$.

## Definition

A [permutation](/permutation/) of $[n]$ is a bijection $\sigma : [n] \to [n]$, and $S_n$ is the set of all $n!$ of them. A transposition swaps two elements and fixes the others. Each permutation is a product of transpositions; the number $k$ of factors is not fixed, but its parity is, and $\operatorname{sgn}(\sigma) = (-1)^k$ is the *sign* of $\sigma$. The sign is multiplicative, $\operatorname{sgn}(\sigma\tau) = \operatorname{sgn}(\sigma)\operatorname{sgn}(\tau)$, and a transposition has sign $-1$. We use these facts about permutations without proof. Equivalently, $\operatorname{sgn}(\sigma) = (-1)^{\operatorname{inv}(\sigma)}$, where $\operatorname{inv}(\sigma)$ is the number of pairs $i < j$ with $\sigma(i) > \sigma(j)$.

For vectors $v_1, \dots, v_n \in K^n$, write $(v)_i$ for coordinate $i$ of $v$, and define

$$
D(v_1, \dots, v_n) = \sum_{\sigma \in S_n} \operatorname{sgn}(\sigma) \prod_{j=1}^{n} (v_j)_{\sigma(j)}.
$$

If $a_1, \dots, a_n$ are the columns of $A$, the **determinant** of $A$ is

$$
\det A = D(a_1, \dots, a_n) = \sum_{\sigma \in S_n} \operatorname{sgn}(\sigma)\, a_{\sigma(1)1}\, a_{\sigma(2)2} \cdots a_{\sigma(n)n}.
$$

This is the Leibniz formula. It uses only $+$, $-$ and $\times$, so it defines $\det A$ for a matrix over any commutative ring $R$, for example $\mathbb{Z}$ or a polynomial ring $K[x]$. For $n = 0$ the sum has one term, the empty product, so the $0 \times 0$ matrix has determinant $1$.

A function $E$ of $n$ vectors in $K^n$ is **multilinear** when it is linear in each argument while the others stay fixed. It is **alternating** when $E(v_1, \dots, v_n) = 0$ whenever two arguments are equal. Let $e_1, \dots, e_n$ be the standard unit vectors.

**Theorem.** Let $K$ be a field and $n \ge 1$.

- (a) $D$ is multilinear and alternating, and $D(e_1, \dots, e_n) = 1$.
- (b) Each multilinear alternating function $E$ with $E(e_1, \dots, e_n) = 1$ satisfies $E(a_1, \dots, a_n) = \det A$ for each matrix $A$ with columns $a_1, \dots, a_n$.
- (c) $\det(AB) = \det A \cdot \det B$ for all $n \times n$ matrices $A$ and $B$.
- (d) $\det A \ne 0$ if and only if $A$ is invertible.
- (e) $\det A^T = \det A$.

Parts (a), (b), (c) and (e) hold over each commutative ring with the same proofs. Over a commutative ring, (d) becomes: $A$ is invertible exactly when $\det A$ is a unit, by (c) and the adjugate formula on the [Cramer's rule](/cramers-rule/) page.

**Lemma.** Let $E$ be multilinear and alternating, let $w_1, \dots, w_n \in K^n$, let $X = (x_{kj})$ be an $n \times n$ matrix, and let $u_j = \sum_{k=1}^{n} x_{kj} w_k$ for each $j$. Then $E(u_1, \dots, u_n) = \det X \cdot E(w_1, \dots, w_n)$.

*Proof.* First, swapping two arguments changes the sign of $E$. Put $x + y$ in positions $p \ne q$, with the other arguments fixed. The value is $0$ since $E$ is alternating. By linearity it splits into four terms; the two with the same vector in both positions are $0$, so the other two, $E(\dots, x, \dots, y, \dots)$ and $E(\dots, y, \dots, x, \dots)$, add to $0$.

Second, $E(w_{\sigma(1)}, \dots, w_{\sigma(n)}) = \operatorname{sgn}(\sigma)\, E(w_1, \dots, w_n)$ for each $\sigma \in S_n$. Write $\sigma$ as a product of $k$ transpositions and use induction on $k$. For $k = 0$, $\sigma$ is the identity. For $k \ge 1$, let $\sigma = \sigma'\tau$, where $\sigma'$ is a product of $k-1$ transpositions and $\tau$ swaps $i$ and $j$. Then $\sigma(i) = \sigma'(j)$, $\sigma(j) = \sigma'(i)$, and $\sigma(t) = \sigma'(t)$ for the other $t$. So the tuple $(w_{\sigma(t)})_t$ is the tuple $(w_{\sigma'(t)})_t$ with positions $i$ and $j$ swapped. By the first step and the induction hypothesis, the value is $-\operatorname{sgn}(\sigma') E(w_1, \dots, w_n) = \operatorname{sgn}(\sigma) E(w_1, \dots, w_n)$.

Third, expand $E(u_1, \dots, u_n)$ by linearity in each argument:

$$
E(u_1, \dots, u_n) = \sum_{k_1 = 1}^{n} \cdots \sum_{k_n = 1}^{n} \Big( \prod_{j=1}^{n} x_{k_j j} \Big) E(w_{k_1}, \dots, w_{k_n}).
$$

A term in which two indices $k_j$ are equal has two equal arguments, so it is $0$. The tuples with distinct indices are $(\sigma(1), \dots, \sigma(n))$ for $\sigma \in S_n$, and by the second step their terms are $\operatorname{sgn}(\sigma) \prod_j x_{\sigma(j) j} \cdot E(w_1, \dots, w_n)$. Their sum is $\det X \cdot E(w_1, \dots, w_n)$. $\square$

*Proof of (a).* Multilinear: the vector $v_j$ occurs in each product only in the factor $(v_j)_{\sigma(j)}$, and a coordinate is linear in its vector. Alternating: let $v_j = v_k$ with $j < k$, and let $\tau$ swap $j$ and $k$. The map $\sigma \mapsto \sigma\tau$ is its own inverse and has no fixed point, so it splits $S_n$ into pairs $\{\sigma, \sigma\tau\}$. In a pair, the factor of $\sigma\tau$ at position $j$ is $(v_j)_{\sigma(k)} = (v_k)_{\sigma(k)}$, the factor of $\sigma$ at position $k$; in the same way the factor at position $k$ matches the factor of $\sigma$ at position $j$, and the other factors agree. So the two products are equal and the signs are opposite, and each pair adds to $0$. Normalization: the factor $(e_j)_{\sigma(j)}$ is $0$ unless $\sigma(j) = j$, so only the identity contributes, with value $1$. $\square$

*Proof of (b).* Column $j$ of $A$ is $a_j = \sum_k a_{kj} e_k$. The lemma with $w_k = e_k$ and $X = A$ gives $E(a_1, \dots, a_n) = \det A \cdot E(e_1, \dots, e_n) = \det A$. $\square$

*Proof of (c).* Column $j$ of $AB$ is $\sum_k b_{kj} a_k$, since its entry $i$ is $\sum_k a_{ik} b_{kj}$. The lemma with $E = D$, $w_k = a_k$ and $X = B$ gives $\det(AB) = \det B \cdot D(a_1, \dots, a_n) = \det B \cdot \det A$. $\square$

*Proof of (d).* If $A$ is invertible, (c) gives $\det A \cdot \det A^{-1} = \det I = 1$, so $\det A \ne 0$. If $A$ is not invertible, then by the [rank-nullity theorem](/rank-nullity-theorem/) its columns are linearly dependent, so some column is a combination of the others: $a_j = \sum_{i \ne j} c_i a_i$. Expand $D(a_1, \dots, a_n)$ by linearity in position $j$. Each term has some $a_i$, $i \ne j$, in position $j$ and also in position $i$, so it is $0$. Hence $\det A = 0$. $\square$

*Proof of (e).* $\det A^T = \sum_\sigma \operatorname{sgn}(\sigma) \prod_j a_{j\sigma(j)}$. Put $i = \sigma(j)$: the same factors give $\prod_i a_{\sigma^{-1}(i)\, i}$. Since $\operatorname{sgn}(\sigma^{-1}) = \operatorname{sgn}(\sigma)$ and $\sigma \mapsto \sigma^{-1}$ is a bijection of $S_n$, the sum is $\sum_\tau \operatorname{sgn}(\tau) \prod_i a_{\tau(i)\, i} = \det A$. $\blacksquare$

**Corollary (row and column operations).** By (e), every statement about columns holds for rows.

- Swapping two rows multiplies $\det A$ by $-1$ (first step of the lemma).
- Multiplying one row by $c$ multiplies $\det A$ by $c$ (linearity).
- Adding $c$ times one row to another row does not change $\det A$: by linearity the change is $c$ times a determinant with two equal rows, which is $0$.
- If $A$ is triangular, $\det A = a_{11} a_{22} \cdots a_{nn}$. For an upper triangular $A$, a nonzero term needs $\sigma(j) \le j$ for each $j$; then $\sigma(1) = 1$, and by induction $\sigma(j) = j$ for each $j$, since $\sigma(j) \le j$ and the values $1, \dots, j-1$ are taken.

These rules are the base of [determinant by Gaussian elimination](/determinant-gaussian-elimination/), which needs $O(n^3)$ field operations instead of the $n!$ terms of the Leibniz formula. The page [determinant computation](/determinant-computation/) surveys the faster and the exact methods.

## Examples and non-examples

- A $1 \times 1$ matrix $(a)$ has determinant $a$. For $n = 2$, $\det \begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$: the identity gives $+ad$ and the swap gives $-bc$. So $\det \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} = -2$.
- For $M = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 4 \end{pmatrix}$, the permutations $(\sigma(1), \sigma(2), \sigma(3))$ give $(1,2,3)$: $+2 \cdot 3 \cdot 4 = 24$; $(2,1,3)$: $-1 \cdot 1 \cdot 4 = -4$; $(1,3,2)$: $-2 \cdot 1 \cdot 1 = -2$; the other three contain a zero entry. So $\det M = 18$ and $M$ is invertible over $\mathbb{Q}$. Over $\mathbb{Z}$ it is not invertible, because $18$ is not a unit, and over $\mathbb{Z}/3\mathbb{Z}$ it is singular, because $18 \equiv 0$.
- The identity $I_n$ has determinant $1$, and $\det(cI_n) = c^n$.
- $\begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$ has determinant $0$: its second column is twice the first.
- A [unimodular matrix](/unimodular-matrix/) is an integer matrix with determinant $\pm 1$, for example $\begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$.

Non-examples, which show what the definition excludes:

- The determinant is not linear in the whole matrix: $\det(2I_2) = 4$, but $\det I_2 + \det I_2 = 2$.
- The product of the diagonal entries is not the determinant in general: $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ has diagonal product $0$ and determinant $-1$.
- The permanent $\operatorname{per} A = \sum_\sigma \prod_j a_{\sigma(j) j}$ drops the sign and is not alternating: the all-ones $2 \times 2$ matrix has permanent $2$. Unlike the determinant, no polynomial-time algorithm for the permanent is known; over $\mathbb{Z}$ computing it is #P-hard (Valiant 1979).
- A matrix that is not square has no determinant.

Over $\mathbb{R}$, $|\det A|$ is the volume of the parallelepiped spanned by the columns, and $\det A < 0$ exactly when $A$ reverses orientation. The [Hadamard bound](/hadamard-bound/) turns this into the inequality $|\det A| \le \prod_j \|a_j\|_2$, which bounds the size of the determinant of an integer matrix.

## Related definitions

- [Characteristic polynomial](/characteristic-polynomial/): $\chi_A(x) = \det(xI - A)$, a determinant over $K[x]$. Its roots in $K$ are the [eigenvalues](/eigenvalue/) of $A$.
- [Rank](/rank/): a square matrix has rank $n$ exactly when its determinant is nonzero. In general the rank is the largest size of a nonzero minor.
- [Laplace expansion](/laplace-expansion/): the determinant as a signed sum of smaller determinants along one row or column.
- [Cramer's rule](/cramers-rule/): when $\det A \ne 0$, the solution of $Ax = b$ is a vector of quotients of determinants.
- [Unimodular matrix](/unimodular-matrix/): a square integer matrix with determinant $\pm 1$; these are the integer matrices with an integer inverse.
- [Linear independence](/linear-independence/): the columns of $A$ are independent exactly when $\det A \ne 0$.
- [Lattice determinant](/lattice-determinant/): the volume of a fundamental domain of a lattice, equal to $|\det B|$ for a basis matrix $B$.

## References
