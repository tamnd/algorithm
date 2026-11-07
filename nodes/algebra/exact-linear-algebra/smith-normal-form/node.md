---
tag: 6QGYB8
kind: problem
slug: smith-normal-form
name: Smith normal form
aliases: [Smith canonical form, Smith form, Smith normal form algorithm, invariant factors of an integer matrix]
area: algebra/exact-linear-algebra
level: advanced
summary: Find unimodular U and V so that UAV is diagonal with each diagonal entry dividing the next.
prereqs: [unimodular-matrix, hermite-normal-form, greatest-common-divisor]
see_also: [kannan-bachem-algorithm, linear-diophantine-system, rational-canonical-form, matrix-tree-theorem, hadamard-bound, rank-computation, extended-euclidean-algorithm, lattice-determinant]
sources:
  - paper: doi:10.1098/rstl.1861.0016
    title: Henry J. S. Smith, On systems of linear indeterminate equations and congruences, Philosophical Transactions of the Royal Society of London 151, 1861
    locator: pp. 293 to 326 (the diagonal form of an integer matrix and its invariants, the quotients of the gcds of the minors)
  - paper: doi:10.1137/0208040
    title: Ravindran Kannan and Achim Bachem, Polynomial algorithms for computing the Smith and Hermite normal forms of an integer matrix, SIAM Journal on Computing 8(4), 1979
    locator: pp. 499 to 507 (the first Smith form algorithm with polynomially bounded intermediate numbers, by alternating Hermite forms of the matrix and its transpose)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer
    locator: Section 2.4.4, The Smith normal form and applications (existence and uniqueness, the modular Algorithm 2.4.14, and the structure of finite abelian groups)
  - paper: "Arne Storjohann, Algorithms for Matrix Canonical Forms, PhD thesis, ETH Zurich, 2000"
    locator: the chapters on the Smith form over principal ideal rings and of integer matrices (the Smith form with small transforms, and deterministic bounds with fast matrix multiplication)
  - paper: "Stavros Birmpilis, George Labahn and Arne Storjohann, A Las Vegas algorithm for computing the Smith form of a nonsingular integer matrix, ISSAC 2020"
    locator: the Smith form of a nonsingular n by n integer matrix in about n^ω b bit operations up to logarithmic and subpolynomial factors
---

The Smith normal form of an $m \times n$ matrix $A$ over the integers (or over another principal ideal domain such as $K[x]$) is the unique diagonal matrix $S = \operatorname{diag}(s_1, \ldots, s_r, 0, \ldots, 0)$ with $s_1 \mid s_2 \mid \cdots \mid s_r$, positive $s_i$, and unimodular $U$, $V$ with $U A V = S$. The problem asks for $S$, and often for $U$ and $V$ too. The $s_i$ are the *invariant factors* of $A$; they describe the finite abelian group $\mathbb{Z}^m / A \mathbb{Z}^n$, the integer solutions of $A x = c$, and, over $K[x]$, the similarity class of a matrix.

## In plain words

You may add a whole-number multiple of one row to another, swap rows, flip the sign of a row, and do the same with columns. These moves can be undone with whole numbers. With them, every table of whole numbers can be brought to a diagonal shape in which each diagonal number divides the next one, and that final shape is the same however you reach it.

The diagonal numbers are what is left of the table once all the choices of coordinates are removed. They say, for example, which group of remainders the table defines, and which right-hand sides give whole-number solutions.

## Definition

**Notation.** $R$ is a principal ideal domain, usually $\mathbb{Z}$ or $K[x]$ for a field $K$. $A$ is an $m \times n$ matrix over $R$ of rank $r$. A [unimodular matrix](/unimodular-matrix/) is a square matrix over $R$ whose determinant is a unit. For an integer matrix, $b$ is the maximum binary length of an entry, and $\omega$ is the exponent of matrix multiplication.

**Input.** An $m \times n$ matrix $A$ over $R$.

**Output.** The matrix $S = \operatorname{diag}(s_1, \ldots, s_r, 0, \ldots, 0)$, of shape $m \times n$, with nonzero $s_i$ normalized (positive over $\mathbb{Z}$, monic over $K[x]$) and $s_i \mid s_{i+1}$ for $1 \le i < r$; and, in the version with transforms, unimodular $U$ ($m \times m$) and $V$ ($n \times n$) with $U A V = S$.

**Theorem (existence and uniqueness).** Let $d_k(A)$ be the greatest common divisor of all $k \times k$ minors of $A$, with $d_0 = 1$. Then $d_k(A) \ne 0$ exactly for $k \le r$, and the Smith form exists and is unique, with

$$s_k = \frac{d_k(A)}{d_{k-1}(A)}, \qquad 1 \le k \le r.$$

*Proof.* Invariance: by the Cauchy-Binet formula, each $k \times k$ minor of $U A$ is an $R$-linear combination of $k \times k$ minors of $A$, so $d_k(A)$ divides $d_k(U A)$; applying this to $U^{-1}$ gives the converse, and the same holds for columns. So $d_k(U A V) = d_k(A)$. For a diagonal $S$ with $s_1 \mid \cdots \mid s_r$, the nonzero $k \times k$ minors are products of $k$ distinct $s_i$, and the one that divides all others is $s_1 \cdots s_k$, so $d_k(S) = s_1 \cdots s_k$. This gives the formula and uniqueness. Existence, over $\mathbb{Z}$: if $A = 0$ we are done. Otherwise move an entry of least nonzero absolute value to position $(1, 1)$. Divide every other entry of row $1$ and column $1$ by it with remainder, and subtract multiples of column $1$ and row $1$; if a nonzero remainder is left, it is smaller, so move it to $(1, 1)$ and repeat. If row $1$ and column $1$ are cleared but some entry $a_{ij}$ is not divisible by $a_{11}$, add row $i$ to row $1$ and repeat. Each round decreases $|a_{11}|$, so this stops with $a_{11}$ dividing every entry, and the process continues on the remaining $(m - 1) \times (n - 1)$ block, whose entries stay multiples of $a_{11}$. Over $K[x]$ the same works with the degree in place of the absolute value. $\square$

## Variants

- **Diagonal only.** Return $S$ without $U$ and $V$. Many applications need only the invariant factors, and the fastest algorithms compute only those.
- **With small transforms.** Return $U$ and $V$ with entries bounded by a polynomial in the [Hadamard bound](/hadamard-bound/). Naive elimination gives correct but huge transforms.
- **Elementary divisors.** The prime power factors of the $s_i$; over $\mathbb{Z}$ they need integer factorization, and the local Smith form at one prime $p$ needs only arithmetic modulo a power of $p$.
- **Over $K[x]$.** The Smith form of $x I - B$ for a square $B$ over $K$ gives its invariant factors and hence the [rational canonical form](/rational-canonical-form/) of $B$.
- **Sparse and large matrices.** Boundary matrices of simplicial complexes are huge and very sparse; black box methods compute the invariant factors with modular rank computations.
- **Over $\mathbb{Z}/N\mathbb{Z}$.** A Smith form exists over this principal ideal ring as well, with the $s_i$ divisors of $N$.

## Examples

**A diagonal matrix that is not in Smith form.** $\operatorname{diag}(2, 3)$ has $d_1 = \gcd(2, 3) = 1$ and $d_2 = 6$, so its Smith form is $\operatorname{diag}(1, 6)$. Both describe the group $\mathbb{Z}/2 \oplus \mathbb{Z}/3 \cong \mathbb{Z}/6$.

**With transforms.** For $A = \begin{pmatrix} 6 & 4 \\ 4 & 6 \end{pmatrix}$, $d_1 = 2$ and $d_2 = |\det A| = 20$, so $S = \operatorname{diag}(2, 10)$. Subtracting column $2$ from column $1$, adding row $1$ to row $2$, and subtracting twice column $1$ from column $2$ gives

$$\begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} 6 & 4 \\ 4 & 6 \end{pmatrix} \begin{pmatrix} 1 & -2 \\ -1 & 3 \end{pmatrix} = \begin{pmatrix} 2 & 0 \\ 0 & 10 \end{pmatrix}.$$

So $\mathbb{Z}^2 / A \mathbb{Z}^2 \cong \mathbb{Z}/2 \oplus \mathbb{Z}/10$, a group of order $20$ that is not cyclic.

**A $3 \times 3$ example.** $\begin{pmatrix} 2 & 4 & 4 \\ -6 & 6 & 12 \\ 10 & -4 & -16 \end{pmatrix}$ has $d_1 = 2$, $d_2 = 12$, $d_3 = 144$, so its Smith form is $\operatorname{diag}(2, 6, 12)$.

**The critical group of a graph.** The Laplacian of the complete graph $K_4$ (diagonal $3$, all other entries $-1$) has Smith form $\operatorname{diag}(1, 4, 4, 0)$. The torsion part $\mathbb{Z}/4 \oplus \mathbb{Z}/4$ is the sandpile group of $K_4$, and its order $16$ is the number of spanning trees, as the [matrix-tree theorem](/matrix-tree-theorem/) predicts.

**Edge cases.** The zero matrix is its own Smith form, with $r = 0$; a $1 \times n$ row $(a_1, \ldots, a_n)$ has Smith form $(\gcd(a_1, \ldots, a_n), 0, \ldots, 0)$, for example $(1, 0, 0)$ for $(4, 6, 9)$.

## Known algorithms

- **Elimination with gcd steps** (Smith, 1861), as in the existence proof: correct, but the entries of the working matrix and of the transforms grow very fast in practice; for the closely related integer elimination, Fang and Havas (1997) proved exponential growth on explicit families.
- **Kannan and Bachem (1979):** alternate [Hermite normal forms](/hermite-normal-form/) of the matrix and its transpose, reducing entries at every step, with all intermediate numbers bounded by a polynomial in $n$ and $b$, so polynomial time. See the [Kannan-Bachem algorithm](/kannan-bachem-algorithm/).
- **Modulo the determinant** (Iliopoulos, 1989; Cohen, Algorithm 2.4.14): for a nonsingular $A$, the Smith form can be computed modulo $|\det A|$, which bounds every number by the [Hadamard bound](/hadamard-bound/).
- **Storjohann (1996, and his thesis):** deterministic algorithms with fast matrix multiplication, about $n^{\omega + 1} b$ bit operations for the Smith form of a nonsingular $n \times n$ integer matrix, up to logarithmic factors, and transforms with small entries.
- **Randomized algorithms:** Eberly, Giesbrecht and Villard (2000) find the largest invariant factor by solving random linear systems, and the whole form in about $n^{3.5}$ bit operations up to factors polynomial in $b$ and $\log n$; Birmpilis, Labahn and Storjohann (2020) reach about $n^\omega b$ for a nonsingular matrix (Las Vegas).
- **Over $K[x]$:** the same elimination with polynomial division, and fast randomized algorithms that use about $n^\omega d$ field operations, up to logarithmic factors, for an $n \times n$ matrix of degree $d$ (Storjohann, 2003, by high-order lifting).

## Bounds

**Size of the answer.** For a nonsingular $n \times n$ integer matrix, $s_1 \cdots s_n = |\det A|$, which is at most $n^{n/2} 2^{n b}$ by the Hadamard bound. So $S$ has at most $n (b + \tfrac12 \log_2 n) + n$ binary digits in total, about the size of one entry of $A^{-1}$: a small output, which is why algorithms for $S$ alone can beat $n^3 b$. In general the same holds with $d_r(A)$ in place of $|\det A|$. These are proved.

**Size of the transforms.** $U$ and $V$ are not unique, and there are choices with entries polynomially bounded in the Hadamard bound (Storjohann's thesis), while naive choices can be exponentially larger. The $n^2$ entries of the transforms make the version with transforms at least as expensive as writing $n^2$ such numbers.

**Algebraic lower bound.** Over a field the Smith form is $\operatorname{diag}(1, \ldots, 1, 0, \ldots, 0)$ with $r$ ones, so computing it includes [rank computation](/rank-computation/). No lower bound better than the size of the input is known for integer matrices.

## Reductions

- **To Hermite normal forms.** The Smith form is reached by alternately computing the row Hermite form of $A$ and of its transpose until the matrix is diagonal, then fixing divisibility with gcd steps on pairs of diagonal entries: $\operatorname{diag}(a, b)$ is equivalent to $\operatorname{diag}(\gcd(a, b), \operatorname{lcm}(a, b))$.
- **Linear Diophantine systems.** With $U A V = S$, the system $A x = c$ over $\mathbb{Z}$ becomes $S y = U c$ with $x = V y$, which is solved one coordinate at a time: $s_i y_i = (U c)_i$ needs $s_i \mid (U c)_i$, and the coordinates with $i > r$ are free. See [linear Diophantine systems](/linear-diophantine-system/).
- **Similarity of matrices.** Two matrices $B$, $B'$ over $K$ are similar if and only if $x I - B$ and $x I - B'$ have the same Smith form over $K[x]$.
- **Determinant and rank.** $d_r(A)$ and $r$ are read off from $S$, so the Smith form computes the [rank](/rank-computation/) and, for square $A$, $|\det A|$.

## Applications

- **Finitely generated abelian groups.** A group given by $m$ generators and the relations in the columns of $A$ is $\bigoplus_i \mathbb{Z}/s_i \oplus \mathbb{Z}^{m - r}$; class group computations in number fields end with such a Smith form.
- **Homology.** The torsion coefficients of simplicial homology groups are the invariant factors greater than $1$ of the boundary matrices.
- **Integer linear algebra.** Solvability of linear Diophantine systems, the index of a sublattice ($|\det A| = s_1 \cdots s_n$; see [lattice determinant](/lattice-determinant/)), and the structure of $\mathbb{Z}^n / L$ for a lattice $L$.
- **Control theory and polynomial matrices.** The Smith form over $K[x]$ and its rational analogue, the Smith-McMillan form, describe the poles and zeros of multivariable linear systems.
- **Combinatorics.** Critical groups of graphs, as in the $K_4$ example, and Smith forms of incidence matrices of designs.

## References
