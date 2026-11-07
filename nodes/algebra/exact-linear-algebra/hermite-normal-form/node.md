---
tag: ZYZTRD
kind: problem
slug: hermite-normal-form
name: Hermite normal form
aliases:
- HNF
- HNF algorithm
- Hermite form
- Hermite normal form algorithm
area: algebra/exact-linear-algebra
level: advanced
summary: Find a unimodular transformation that brings an integer matrix to a unique upper triangular echelon form.
prereqs: [unimodular-matrix, echelon-form, extended-euclidean-algorithm]
see_also: [kannan-bachem-algorithm, smith-normal-form, linear-diophantine-system, unimodular-matrix, lattice-basis, lattice-determinant, lll-algorithm, lattice-based-cryptography]
sources:
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.4.2, The Hermite normal form (the definition for columns, existence and uniqueness, Algorithms 2.4.4 and 2.4.5, and the modular Algorithm 2.4.8); Section 2.4.3, Applications of the Hermite normal form
  - paper: doi:10.1137/0208040
    title: Ravindran Kannan and Achim Bachem, Polynomial algorithms for computing the Smith and Hermite normal forms of an integer matrix, SIAM Journal on Computing 8(4), 1979
    locator: pp. 499 to 507 (the first algorithms with a proved polynomial bound on the sizes of all intermediate numbers)
  - paper: "Paul D. Domich, Ravindran Kannan and Leslie E. Trotter, Hermite normal form computation using modulo determinant arithmetic, Mathematics of Operations Research 12(1), 1987"
    locator: pp. 50 to 59 (computing the form of a full-rank matrix modulo a multiple of the lattice determinant)
  - paper: "James L. Hafner and Kevin S. McCurley, Asymptotically fast triangularization of matrices over rings, SIAM Journal on Computing 20(6), 1991"
    locator: pp. 1068 to 1083 (triangular and Hermite forms with fast matrix multiplication)
  - paper: "Arne Storjohann, Algorithms for Matrix Canonical Forms, PhD thesis, ETH Zurich, 2000"
    locator: the chapters on echelon forms over principal ideal rings and on the Hermite form of integer matrices (deterministic algorithms with fast matrix multiplication and bounds on the transform)
  - paper: "Charles Hermite, Sur l'introduction des variables continues dans la theorie des nombres, Journal fur die reine und angewandte Mathematik 41, 1851"
    locator: pp. 191 to 216 (the reduction of integer matrices by unimodular transformations to a triangular form)
---

The Hermite normal form (HNF) is the integer analogue of the reduced row echelon form. For an integer matrix $A$, it is the unique matrix $H = UA$, with $U$ a [unimodular matrix](/unimodular-matrix/), that is in echelon form with positive pivots and with every entry above a pivot reduced modulo that pivot. Row operations over $\mathbb{Z}$ cannot divide, so the pivots are not $1$ in general: they record the structure of the lattice spanned by the rows. Two integer matrices have the same HNF exactly when their rows span the same lattice, which makes the form a canonical description of a subgroup of $\mathbb{Z}^n$. It can be computed in polynomial time, which was first shown by the [Kannan-Bachem algorithm](/kannan-bachem-algorithm/) in 1979; the naive method that runs the Euclidean algorithm on the columns is correct but can create huge numbers.

Notation: $A$ is an $m \times n$ matrix over $\mathbb{Z}$ of rank $r$, with rows $a_1, \dots, a_m$, and $L(A) = \{xA : x \in \mathbb{Z}^m\}$ is the lattice spanned by its rows. For a square matrix, $n$ is its size. $B$ bounds the absolute values of the entries and $b$ is their maximum binary length, and $\omega$ is the exponent of matrix multiplication. This page uses the row convention, $H = UA$ upper triangular; Cohen's book uses the column convention $AU = H$, which is the transpose.

## In plain words

Take a table of whole numbers and allow only row operations that can be undone with whole numbers: swapping rows, changing the sign of a row, and adding a whole multiple of one row to another. The goal is a staircase shape, as in ordinary elimination, but division is not allowed, so the leading numbers of the rows cannot all be made equal to one. The Hermite form fixes all the remaining choices: the leading numbers are positive, and every number above a leading number is smaller than it and not negative. Then the result depends only on the set of all combinations of the rows.

## Definition

**Input:** an $m \times n$ integer matrix $A$.

**Output:** an $m \times n$ integer matrix $H$ and a unimodular $m \times m$ matrix $U$, that is with $\det U = \pm 1$, such that $H = UA$ and $H$ is in Hermite normal form:

1. the first $r$ rows of $H$ are nonzero and the last $m - r$ rows are zero;
2. if the first nonzero entry of row $i \le r$ is in column $j_i$, then $j_1 < j_2 < \cdots < j_r$ (the *pivot columns*);
3. each pivot is positive: $h_{i, j_i} > 0$;
4. each entry above a pivot is reduced: $0 \le h_{k, j_i} < h_{i, j_i}$ for $k < i$.

Entries in the columns that are not pivot columns have no condition. Some sources ask only for $H$, others also for $U$, and $U$ is unique only when $A$ has full row rank $r = m$.

**Theorem (existence and uniqueness).** Every integer matrix has a Hermite normal form $H$, and $H$ depends only on the lattice $L(A)$. In particular, two $m \times n$ matrices $A$ and $A'$ have the same HNF exactly when $A' = VA$ for a unimodular $V$.

*Proof sketch.* Existence: the extended Euclidean algorithm replaces two rows with leading entries $s$ and $t$ by two unimodular combinations with leading entries $\gcd(s, t)$ and $0$. Doing this column by column gives an echelon form, and then more unimodular row operations fix the signs and reduce the entries above the pivots.

Uniqueness: let $H$ and $H'$ be Hermite forms with $L(H) = L(H') = L$. The nonzero rows of each form a basis of $L$. A column $j$ is a pivot column exactly when the projection of $L$ onto the first $j$ coordinates has larger rank than its projection onto the first $j - 1$, so both forms have the same pivot columns $j_1 < \dots < j_r$. Let $L_i$ be the set of vectors of $L$ that are zero in all columns before $j_i$; it is spanned by rows $i, \dots, r$ of $H$, and also by rows $i, \dots, r$ of $H'$. The entries in column $j_i$ of the vectors of $L_i$ form the subgroup $h_{i, j_i}\mathbb{Z} = h'_{i, j_i}\mathbb{Z}$ of $\mathbb{Z}$, so the positive pivots agree. Now let $d$ be row $i$ of $H$ minus row $i$ of $H'$. It lies in $L$ and is zero up to column $j_i$, so $d = \sum_{k > i} x_k h_k$ with integers $x_k$, where $h_k$ is row $k$ of $H$. If some $x_k \ne 0$, take the least such $k$. The entry of $d$ in column $j_k$ is $x_k h_{k, j_k}$, because the rows after $k$ vanish there. It is also the difference of two entries above the pivot $h_{k, j_k} = h'_{k, j_k}$, both in $[0, h_{k, j_k})$, so its absolute value is less than $h_{k, j_k}$. Hence $x_k = 0$, a contradiction, and $d = 0$. Cohen, Section 2.4.2, gives the argument in the column convention. If $A' = VA$, the lattices agree; conversely, if $H = UA = U'A'$, then $A' = U'^{-1}U A$. $\square$

The HNF is defined in the same way over any Euclidean domain, for example $K[x]$, with "positive" replaced by a choice of associates (monic polynomials) and "reduced" by a choice of remainders (degree less than that of the pivot).

## Variants

- **Column HNF.** $AU = H$ with $U$ unimodular acting on columns, with $H$ lower or upper triangular depending on the book. This is the convention of Cohen, and of computations with modules in algebraic number theory.
- **Full-rank square matrices.** For a nonsingular $n \times n$ matrix, $H$ is upper triangular with pivots on the diagonal, $\prod_i h_{ii} = |\det A|$, and $U = HA^{-1}$ is unique.
- **Modular HNF.** For a full-rank lattice, every computation can be done modulo a multiple $D$ of the lattice determinant, because $D\mathbb{Z}^n \subseteq L(A)$ (Domich, Kannan and Trotter 1987; Cohen's Algorithm 2.4.8).
- **With a small transform.** When $A$ has dependent rows, $U$ is not unique; algorithms based on [lattice reduction](/lll-algorithm/) find a $U$ with small entries (Havas, Majewski and Matthews).
- **Over $\mathbb{Z}/N\mathbb{Z}$.** The analogous canonical form for the row span over a ring with zero divisors is the Howell form (Howell 1986).
- **Polynomial matrices.** Over $K[x]$, the HNF has monic pivots; the Popov form is another canonical form of a polynomial matrix, with better degree properties.
- **Smith normal form.** Allowing column operations as well gives the diagonal [Smith normal form](/smith-normal-form/), which describes the quotient $\mathbb{Z}^n / L(A)$ but not the lattice itself.

## Examples

- $A = \begin{pmatrix} 4 & 6 \\ 2 & 2 \end{pmatrix}$ and $A' = \begin{pmatrix} 6 & 4 \\ 4 & 2 \end{pmatrix}$ both have the HNF $\begin{pmatrix} 2 & 0 \\ 0 & 2 \end{pmatrix}$. So both span the lattice $2\mathbb{Z}^2$ of vectors with even coordinates, although no row of one matrix is a row of the other. For $A$, a transform is $U = \begin{pmatrix} -1 & 3 \\ 1 & -2 \end{pmatrix}$, with $\det U = -1$.
- For $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$, the HNF is
  $$
  H = \begin{pmatrix} 1 & 0 & 7 \\ 0 & 1 & 4 \\ 0 & 0 & 18 \end{pmatrix} = \begin{pmatrix} 1 & -1 & 2 \\ 0 & 0 & 1 \\ 1 & -2 & 5 \end{pmatrix} M,
  $$
  and the transform has determinant $1$. The pivots multiply to $18 = \det M$, and $H$ shows at once that $L(M) = \{x \in \mathbb{Z}^3 : x_3 \equiv 7x_1 + 4x_2 \pmod{18}\}$. The reduced row echelon form of $M$ over $\mathbb{Q}$ is the identity, which forgets this structure.
- The $3 \times 4$ matrix with rows $(2, 3, 6, 2)$, $(5, 6, 1, 6)$, $(8, 3, 1, 1)$ has the HNF with rows $(1, 0, 50, -11)$, $(0, 3, 28, -2)$, $(0, 0, 61, -13)$. The pivot columns are $1, 2, 3$, the entries $50$ and $28$ are reduced modulo $61$ and the entry $0$ modulo $3$, and the last column, without a pivot, has negative entries.
- A rank-deficient matrix: rows $(1, 2, 3, 4)$, $(2, 4, 6, 8)$, $(3, 5, 7, 9)$ give the HNF with rows $(1, 0, -1, -2)$, $(0, 1, 2, 3)$, $(0, 0, 0, 0)$. Here the third row of $U$ is a relation among the rows of $A$, for example $(2, -1, 0)$, and any multiple of it can be added to the other rows of $U$, so $U$ is not unique.
- Non-example: $\begin{pmatrix} 2 & 8 \\ 0 & 5 \end{pmatrix}$ is in echelon form with positive pivots, but the entry $8$ above the pivot $5$ is not reduced. Subtracting the second row from the first gives its HNF $\begin{pmatrix} 2 & 3 \\ 0 & 5 \end{pmatrix}$, in which $0 \le 3 < 5$. The entry $2$ has no condition with respect to $5$, and the entry $3$ has no condition with respect to $2$, because it is not above that pivot.

All of these were checked by a script that verifies $H = UA$, $\det U = \pm 1$ and the four conditions.

## Known algorithms

| Algorithm | Cost | Notes |
| --- | --- | --- |
| Euclidean elimination column by column, then reduction | polynomially many operations, but the numbers can grow exponentially | the textbook method; Cohen's Algorithm 2.4.4 |
| [Kannan-Bachem algorithm](/kannan-bachem-algorithm/) (1979) | polynomial in $n$, $m$ and $b$, proved | puts the leading blocks in HNF one at a time and reduces after each step |
| Modular HNF (Domich, Kannan and Trotter 1987; Iliopoulos 1989) | $O(n^3)$ operations on numbers of $O(\log D)$ bits for a full-rank $n \times n$ matrix | works modulo a multiple $D$ of the determinant |
| Hafner and McCurley (1991) | $O(n^\omega)$ operations modulo $D$, up to logarithmic factors | fast matrix multiplication |
| Storjohann (thesis, 2000) | deterministic, about $n^{\omega+1} b$ bit operations up to logarithmic factors for a nonsingular $n \times n$ matrix | also bounds the transform |
| Micciancio and Warinschi (2001), Pernet and Stein (2010) | much faster in practice for random matrices | determinant and system solving by $p$-adic and modular methods, then a correction |

The modular method is the standard choice for full-rank matrices: compute $D = |\det A|$, or a multiple of it, by a [multimodular determinant](/multimodular-determinant/), then run the elimination with every entry reduced modulo $D$, and recover the pivots as gcds with $D$. The sizes of all numbers are then bounded by $\log_2 D \le n(b + \tfrac12 \log_2 n)$ bits, which is a proved bound.

## Bounds

- **Output size, full rank.** For a nonsingular $n \times n$ matrix, $\prod_i h_{ii} = |\det A|$, and every entry of column $i$ lies in $[0, h_{ii}]$. So each entry is at most $|\det A| \le n^{n/2} B^n$ by the [Hadamard bound](/hadamard-bound/), and the whole output has at most $n \log_2 |\det A| + O(n^2)$ bits, which is $O(n^2 (b + \log n))$. For a random matrix the HNF typically has the pivots $1, \dots, 1, |\det A|$, with a last column of entries of the size of $\det A$, so this order is reached.
- **Output size, any rank.** Let $P$ be the pivot columns and $A_{S,P}$ a nonsingular $r \times r$ submatrix of $A$ in those columns. Then $H = H_P A_{S,P}^{-1} A_S$, where $H_P$ is the restriction of $H$ to $P$, and $\det H_P$ divides $\det A_{S,P}$. This gives $|h_{ij}| \le r^2 (r-1)^{(r-1)/2} B^r$ for all entries, so every entry has $O(r(b + \log r))$ bits.
- **The transform.** For a nonsingular square $A$, $U = HA^{-1}$ has entries at most $n$ times the largest cofactor of $A$. For a rank-deficient matrix there are transforms of polynomial size, but the naive one can be much larger.
- **Intermediate growth.** For the naive method, examples with exponential growth of the intermediate numbers are known (Fang and Havas 1997 gave a proof for a version of integer elimination). Kannan and Bachem proved the first polynomial bound.
- **Arithmetic lower bound.** The HNF of a nonsingular matrix gives $|\det A|$ as the product of the pivots, so it is at least as hard as the absolute value of the determinant.

## Reductions

- **Lattice equality and membership.** $L(A) = L(A')$ iff the HNFs agree. A vector $v$ lies in $L(A)$ iff reducing it by the rows of $H$, pivot by pivot, gives $0$; this is a triangular solve over $\mathbb{Z}$.
- **Integer kernel.** For $A$ of rank $r$, the last $m - r$ rows of $U$ form a basis of the integer kernel $\{x \in \mathbb{Z}^m : xA = 0\}$.
- **Linear Diophantine systems.** The HNF of $A^T$, with its transform, gives all integer solutions of $Ax = b$: solve the triangular system for the particular solution, and add the integer kernel. See [linear Diophantine system](/linear-diophantine-system/).
- **Sums and intersections of lattices.** The HNF of the stacked matrix $\begin{pmatrix} A \\ A' \end{pmatrix}$ is a basis of $L(A) + L(A')$, and an integer kernel computation gives $L(A) \cap L(A')$.
- **Smith form.** Alternating row and column HNFs converges to the Smith normal form; Kannan and Bachem used this to give the first polynomial Smith form algorithm too.
- **Determinant.** The modular HNF needs a multiple of $\det A$, so in practice the HNF is computed after a determinant.

## Applications

- **Algebraic number theory.** Ideals and orders of a number field are $\mathbb{Z}$-modules of full rank, and the HNF of a basis matrix is their canonical form; equality, sum, product and intersection of ideals reduce to HNF computations (Cohen, Sections 2.4.3 and 4.7).
- **Integer programming.** The HNF describes all integer points of an affine lattice $\{x : Ax = b\}$, which removes equality constraints from an integer program, and it was Kannan and Bachem's motivation.
- **Lattice-based cryptography.** The HNF of a lattice basis reveals nothing beyond the lattice itself, so it is used as a canonical public basis in [lattice-based cryptography](/lattice-based-cryptography/) (Micciancio 2001).
- **Abelian groups.** A finitely generated subgroup of $\mathbb{Z}^n$ is given by its HNF, and the quotient group is then computed by the Smith form.
- **Compilers.** Loop transformations of nested loops are unimodular matrices, and the HNF is used to compute the new loop bounds and to test dependences.

## References
