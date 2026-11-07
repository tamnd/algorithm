---
tag: PAGM5P
kind: problem
slug: nullspace-computation
name: Nullspace computation
aliases: [kernel computation, kernel basis computation, solving a homogeneous linear system]
area: algebra/exact-linear-algebra
level: core
summary: Compute a basis of the set of vectors x with Ax = 0.
model: algebraic-computation-tree
complexity:
  vars: {m: the number of rows, n: the number of columns, r: the rank of A}
  time: {worst: "O(m n r^(ω-2))"}
prereqs: [nullspace, gaussian-elimination]
see_also: [reduced-row-echelon-form, rank-computation, linear-diophantine-system, hermite-normal-form, wiedemann-algorithm, block-lanczos-algorithm, linear-system-modulo-2, lll-algorithm]
sources:
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer
    locator: Section 2.3.1, Kernel and image (the kernel over a field by elimination), and Section 2.4.3, Applications of the Hermite normal form (the kernel of an integer matrix as a Z-module)
  - paper: "Arne Storjohann, Algorithms for Matrix Canonical Forms, PhD thesis, ETH Zurich, 2000"
    locator: Chapter 2, echelon forms over fields (a transforming matrix and the reduced echelon form in O(n m r^(ω-2)) field operations, from which a nullspace basis is read)
  - paper: doi:10.1109/TIT.1986.1057137
    title: Douglas H. Wiedemann, Solving sparse linear equations over finite fields, IEEE Transactions on Information Theory 32(1), 1986
    locator: pp. 54 to 62 (random nullspace vectors of a sparse singular matrix from its minimal polynomial)
  - paper: doi:10.1007/3-540-54522-0_93
    title: Erich Kaltofen and B. David Saunders, On Wiedemann's method of solving sparse linear systems, AAECC-9, Lecture Notes in Computer Science 539, 1991
    locator: pp. 29 to 38 (preconditioners that make Wiedemann's method compute the rank and sample uniformly from the nullspace)
---

Nullspace computation asks, for an $m \times n$ matrix $A$ over a field $K$, for a basis of the [nullspace](/nullspace/) $\{x : A x = 0\}$, that is, a full description of all solutions of a homogeneous linear system. Over a field, elimination to [reduced row echelon form](/reduced-row-echelon-form/) solves it in $O(m n \min(m, n))$ field operations, and $O(m n r^{\omega - 2})$ with fast matrix multiplication, where $r$ is the rank. Over the integers the problem changes: the integer solutions form a lattice, and a basis of it needs normal form or lattice reduction methods.

## In plain words

You have a set of linear equations that all equal zero, and you want every way to satisfy them. The answers form a flat space through the origin, and a basis is a short list of answers from which every answer can be built by adding and scaling.

Elimination finds it: bring the equations to a staircase form, let the variables that are not at a step be free, and solve for the others. Each free variable gives one basis vector. With whole numbers only, scaling is limited, so the problem is harder and needs extra care.

## Definition

**Notation.** $K$ is a field and $A$ an $m \times n$ matrix over $K$ of [rank](/rank/) $r$. $\omega$ is the exponent of matrix multiplication. For an integer matrix, $b$ is the maximum binary length of an entry.

**Input.** An $m \times n$ matrix $A$ over $K$.

**Output.** An $n \times (n - r)$ matrix $N$ over $K$ whose columns form a basis of $\ker A = \{x \in K^n : A x = 0\}$. Equivalently: $A N = 0$, and $N$ has rank $n - r$. By the [rank-nullity theorem](/rank-nullity-theorem/) the number of columns is forced to be $n - r$.

**The canonical basis.** If $E$ is the reduced row echelon form of $A$ with pivot columns $p_1 < \cdots < p_r$, then for each free column $f$ there is one basis vector $x^{(f)}$: $x^{(f)}_f = 1$, $x^{(f)}_{f'} = 0$ for the other free columns $f'$, and $x^{(f)}_{p_i} = -E_{i f}$. These vectors are a basis, and this basis depends only on $A$, because the RREF is unique.

**Over the integers.** For an integer matrix $A$, the integer solutions $\Lambda = \{x \in \mathbb{Z}^n : A x = 0\}$ form a [lattice](/lattice/) of rank $n - r$, and the problem asks for a $\mathbb{Z}$-basis of $\Lambda$. A $\mathbb{Q}$-basis scaled to integer vectors spans a sublattice of $\Lambda$ that can have index greater than $1$, so it is not an answer.

## Variants

- **Left nullspace.** The vectors $y$ with $y^T A = 0$, which is the nullspace of $A^T$. Factoring algorithms want this form: the rows of $A$ are relations, and a left kernel vector is a set of relations that combine to a square.
- **One vector.** Find a single nonzero $x$ with $A x = 0$, or a uniformly random one. For sparse matrices this is what [Wiedemann's algorithm](/wiedemann-algorithm/) and [block Lanczos](/block-lanczos-algorithm/) do.
- **Over $\mathbb{F}_2$.** The setting of [linear systems modulo 2](/linear-system-modulo-2/), with bit-packed rows.
- **Over $\mathbb{Z}/N\mathbb{Z}$ with $N$ composite.** There is no field, and the solution set is a module, described by the [Smith normal form](/smith-normal-form/) of $A$ over $\mathbb{Z}$ or by a Howell form over $\mathbb{Z}/N\mathbb{Z}$.
- **Integer kernel.** A $\mathbb{Z}$-basis of $\Lambda$, found with the [Hermite normal form](/hermite-normal-form/) of $A^T$ with its transform, or a reduced (short) basis, found with the [LLL algorithm](/lll-algorithm/).
- **Polynomial matrices.** For $A$ over $K[x]$, a kernel basis of minimal degrees (a minimal approximant or kernel basis), used for syzygies and for block Wiedemann.

## Examples

**Over $\mathbb{Q}$.** Let

$$A = \begin{pmatrix} 1 & 2 & 0 & 3 \\ 2 & 4 & 1 & 1 \\ 3 & 6 & 1 & 4 \end{pmatrix}, \qquad E = \begin{pmatrix} 1 & 2 & 0 & 3 \\ 0 & 0 & 1 & -5 \\ 0 & 0 & 0 & 0 \end{pmatrix}.$$

The pivot columns are $1$ and $3$, so $r = 2$ and the free columns are $2$ and $4$. The canonical basis is $(-2, 1, 0, 0)$ and $(-3, 0, 5, 1)$, and both satisfy $A x = 0$, for example $3 \cdot (-3) + 1 \cdot 5 + 4 \cdot 1 = 0$ in row $3$.

**An integer kernel.** For $A = (4 \;\; 6 \;\; 9)$, the RREF gives the $\mathbb{Q}$-basis $(-\tfrac32, 1, 0)$, $(-\tfrac94, 0, 1)$. Clearing denominators gives $u = (-3, 2, 0)$ and $w = (-9, 0, 4)$, but these span only a sublattice of index $2$: the integer kernel has the basis $u$ and $v = (0, 3, -2)$, and $w = 3u - 2v$, with $\det \begin{pmatrix} 1 & 0 \\ 3 & -2 \end{pmatrix} = -2$. The vector $v$ is in the kernel, but it is not an integer combination of $u$ and $w$.

**Balancing a chemical equation.** For $a\,\mathrm{H_2} + b\,\mathrm{O_2} \to c\,\mathrm{H_2O}$, count each element: hydrogen gives $2a - 2c = 0$ and oxygen $2b - c = 0$. The kernel of $\begin{pmatrix} 2 & 0 & -2 \\ 0 & 2 & -1 \end{pmatrix}$ has the integer basis $(2, 1, 2)$, which is $2 \mathrm{H_2} + \mathrm{O_2} \to 2 \mathrm{H_2O}$.

**Edge cases.** A full column rank matrix has the empty basis ($n - r = 0$), the zero matrix has the basis $e_1, \ldots, e_n$, and an $m \times 0$ matrix has the empty basis of $K^0$.

## Known algorithms

- **Gauss-Jordan elimination** to the RREF, then the canonical basis: $O(m n \min(m, n))$ field operations; see [Gauss-Jordan elimination](/gauss-jordan-elimination/).
- **Elimination with a transform.** Compute an invertible $U$ with $U A^T$ in echelon form; the last $n - r$ rows of $U$ span the kernel of $A$. Over $\mathbb{Z}$, the same with a unimodular $U$ from the [Hermite normal form](/hermite-normal-form/) gives a $\mathbb{Z}$-basis of $\Lambda$ (Cohen, Section 2.4.3).
- **Fast elimination.** Storjohann's thesis (Chapter 2) gives the RREF with a transform in $O(m n r^{\omega - 2})$ field operations.
- **Black box methods.** For a sparse $A$, [Wiedemann's algorithm](/wiedemann-algorithm/) with the preconditioners of Kaltofen and Saunders (1991) samples a random kernel vector with $O(n)$ products $v \mapsto A v$ and $O(n^2)$ further field operations; [block Lanczos](/block-lanczos-algorithm/) and [block Wiedemann](/block-wiedemann-algorithm/) find several kernel vectors at once over $\mathbb{F}_2$.
- **Structured elimination.** For very sparse matrices from factoring, [structured Gaussian elimination](/structured-gaussian-elimination/) shrinks the matrix first.
- **Over $\mathbb{Z}$ or $\mathbb{Q}$ by bits.** Fraction-free elimination in the style of the [Bareiss algorithm](/bareiss-algorithm/) keeps every intermediate entry equal to a minor of $A$ of order at most $r$; [multimodular](/gaussian-elimination-modular/) and [p-adic](/dixon-p-adic-lifting/) methods avoid large intermediate numbers.

## Bounds

**Algebraic model.** $O(m n r^{\omega - 2})$ field operations suffice (Storjohann's thesis), which for square full-size input is $O(n^\omega)$. Computing the canonical basis is also at least as hard as matrix multiplication: for $n \times n$ matrices $X$ and $Y$, the $2n \times 3n$ matrix

$$\begin{pmatrix} I & -X & 0 \\ 0 & I & -Y \end{pmatrix} \quad \text{has the RREF} \quad \begin{pmatrix} I & 0 & -X Y \\ 0 & I & -Y \end{pmatrix},$$

so its canonical kernel basis is the $3n \times n$ matrix with blocks $X Y$, $Y$ and $I$, and contains the product $X Y$. The trivial lower bound is $\Omega(m n)$ to read the input, and no better general lower bound is known. These statements are proved.

**Bit sizes over $\mathbb{Q}$.** By Cramer's rule, each entry $-E_{i f}$ of the canonical basis is a quotient of two $r \times r$ minors of $A$, with the same denominator for all of them. Scaling by that denominator gives an integer basis whose entries are minors of order $r$, so by the [Hadamard bound](/hadamard-bound/) they have at most $r (b + \tfrac12 \log_2 r)$ binary digits, and the output has $O(n (n - r) \, r (b + \log r))$ digits. This is a proved bound. Fraction-free elimination keeps every intermediate entry within the same bound, so it costs $O(m n r)$ operations on integers of that length, $O(m n r^3 (b + \log r)^2)$ bit operations with schoolbook multiplication. Elimination over $\mathbb{Q}$ with fractions reduced at every step stays within a constant factor of these sizes, but without reduction the numerators can double in length at each step.

**Integer kernel.** A $\mathbb{Z}$-basis of $\Lambda$ with entries bounded by a polynomial in the Hadamard bound exists, and the Hermite normal form methods find one in polynomial time ([Kannan and Bachem](/kannan-bachem-algorithm/), 1979). Naive integer elimination without care for entry growth can produce exponentially long entries, an observed phenomenon that motivated those methods.

## Reductions

- **Solving to kernel.** $A x = c$ is solvable if and only if $\ker (A \mid -c)$ contains a vector with last entry $1$, and then $x$ is read from it.
- **Kernel to echelon form.** A kernel basis is read from the RREF, or from the transform of an echelon form of $A^T$.
- **Rank from kernel.** $r = n - \dim \ker A$; see [rank computation](/rank-computation/).
- **Multiplication to kernel.** As in the bound above, a canonical kernel basis of a $2n \times 3n$ matrix contains a product of $n \times n$ matrices.

## Applications

- **Integer factoring.** The [quadratic sieve](/quadratic-sieve/) and the [number field sieve](/general-number-field-sieve/) find a congruence of squares from a left kernel vector of a large sparse matrix over $\mathbb{F}_2$.
- **Discrete logarithms.** [Index calculus](/index-calculus/) solves a sparse linear system modulo the group order, and kernel vectors give the logarithms of the factor base.
- **Polynomial factoring.** The [Berlekamp factorization algorithm](/berlekamp-factorization/) splits a squarefree polynomial over $\mathbb{F}_q$ with a basis of the kernel of $Q - I$, where $Q$ is the matrix of the Frobenius map.
- **Integer relations and syzygies.** Integer kernels describe the integer linear relations among vectors, and kernels of polynomial matrices describe syzygies.
- **Chemistry and network flows.** Balancing reactions and finding conserved quantities are integer kernel problems.

## References
