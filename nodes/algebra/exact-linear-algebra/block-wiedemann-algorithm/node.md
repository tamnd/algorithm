---
tag: 0EQBTW
kind: algorithm
slug: block-wiedemann-algorithm
name: Block Wiedemann algorithm
aliases:
- block Wiedemann
- Coppersmith's block Wiedemann algorithm
area: algebra/exact-linear-algebra
level: research
summary: Block version of Wiedemann's method that exploits parallel matrix-vector products for sparse matrices over finite fields.
solves: [nullspace-computation]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix, w: the number of nonzero entries, s: the block width}
  time: {worst: O(n w + s n^2)}
  space: {extra: O(n s)}
  field_operations: {worst: 3 n w + O(s n^2)}
properties: {deterministic: false, in_place: false, recursive: false}
prereqs: [wiedemann-algorithm, black-box-matrix, matrix-minimal-polynomial]
see_also: [block-lanczos-algorithm, wiedemann-algorithm, black-box-matrix, structured-gaussian-elimination, general-number-field-sieve, index-calculus, berlekamp-massey, krylov-subspace]
sources:
  - paper: doi:10.1090/S0025-5718-1994-1192970-7
    title: Don Coppersmith, Solving homogeneous linear equations over GF(2) via block Wiedemann algorithm, Mathematics of Computation 62(205), 1994
    locator: pp. 333 to 350 (the blocked sequence, the matrix generalization of Berlekamp-Massey, and the parallel use over GF(2))
  - paper: doi:10.1109/TIT.1986.1057137
    title: Douglas H. Wiedemann, Solving sparse linear equations over finite fields, IEEE Transactions on Information Theory 32(1), 1986
    locator: pp. 54 to 62 (the scalar method that the block version generalizes)
  - paper: "Erich Kaltofen, Analysis of Coppersmith's block Wiedemann algorithm for the parallel solution of sparse linear systems, Mathematics of Computation 64(210), 1995"
    locator: pp. 777 to 806 (the probability of success over large fields and the cost analysis)
  - paper: "Gilles Villard, Further analysis of Coppersmith's block Wiedemann algorithm for the solution of sparse linear systems, ISSAC 1997"
    locator: pp. 32 to 39 (the analysis over small fields, and the link with matrix minimal polynomials)
  - paper: "Pascal Giorgi, Claude-Pierre Jeannerod and Gilles Villard, On the complexity of polynomial matrix computations, ISSAC 2003"
    locator: pp. 135 to 142 (the M-Basis and PM-Basis algorithms for minimal approximant bases)
  - paper: "Emmanuel Thome, Subquadratic computation of vector generating polynomials and improvement of the block Wiedemann algorithm, Journal of Symbolic Computation 33(5), 2002"
    locator: pp. 757 to 775 (a subquadratic matrix generator step)
---

The block Wiedemann algorithm finds vectors in the kernel of a large sparse matrix over a finite field, using only products of the matrix with blocks of vectors. It runs [Wiedemann's method](/wiedemann-algorithm/) on $s$ vectors at once: the scalar sequence $u^T A^i v$ becomes a sequence of $s \times s$ matrices $X^T A^i Y$, and the Berlekamp-Massey step becomes the computation of a matrix generator. The sequence is $s$ times shorter, so the expensive part, about $3n$ products of $A$ with a vector, splits into $s$ independent streams that can run on different machines with no communication. Over $\mathbb{F}_2$, a block of $64$ vectors fits in one machine word per row. Don Coppersmith introduced the method in 1994, and it is the standard linear algebra step of record factorizations with the number field sieve.

Notation: $A$ is an $n \times n$ matrix over a finite field $\mathbb{F}_p$ with $w$ nonzero entries, given as a [black box](/black-box-matrix/) for products $v \mapsto Av$. $s$ is the block width, and $X, Z$ are $n \times s$ matrices with random entries. Coppersmith uses two widths, $m$ for $X$ and $n$ for $Y$; this page takes both equal to $s$. Costs count operations in $\mathbb{F}_p$; for a prime $p$ of $\beta$ bits, each costs $O(\beta^2)$ bit operations with schoolbook arithmetic. $\omega$ is the exponent of matrix multiplication.

## In plain words

Some systems of equations are huge but have only a few nonzero numbers in each equation, as in the last step of factoring large numbers. Elimination would fill them with nonzeros and run out of memory, so the method only ever multiplies the matrix by vectors. From a few hundred such products it learns a short rule that the products obey, and the rule gives a vector that the matrix sends to zero. The block version runs many such product chains side by side, which lets many computers share the work, and then combines their results in one smaller step.

## The problem

Input: a singular $n \times n$ matrix $A$ over $\mathbb{F}_p$, as a black box, and a block width $s$. Output: a nonzero vector $u$ with $Au = 0$. The same method solves $Bx = b$ for a nonsingular $B$, by taking a kernel vector of $[B \mid -b]$ completed to a square matrix, and it gives the rank and the minimal polynomial with more work. Cost is measured in black-box products and in field operations.

## The algorithm

```pseudo id=main
BLOCK-WIEDEMANN(A, s)                        ▷ A is n × n over F_p
L1  choose random X, Z ∈ F_p^{n×s}; Y ← A Z
L2  L ← 2⌈n/s⌉ + 4
L3  for i ← 0 to L − 1 do
L4      S_i ← X^T (A^i Y)                        ▷ an s × s matrix; keep only A^i Y
L5  F ← right generators of S_0, …, S_{L−1}: pairs (d, f) with Σ_j S_{i+j} f_j = 0 for i < L − d
L6  for each (d, f) in F with d ≤ L − ⌈n/s⌉, by increasing d, do
L7      e ← the least j with f_j ≠ 0; u ← Σ_{j ≥ e} A^{j−e} Z f_j
L8      repeat at most e + 2 times while u ≠ 0
L9          if A u = 0 then return u
L10         u ← A u
L11 return FAIL
```

Lines L3 and L4 are the sequence phase. The $s$ columns of $Y$ give $s$ independent sequences $A^i y_c$, and $S_i$ needs only the dot products of $X$ with the current block, so each column can run on its own machine.

Line L5 is the matrix generalization of the [Berlekamp-Massey algorithm](/berlekamp-massey/). The implementation computes an approximant basis: polynomial rows $(a \mid b)$ with $a(x) S(x)^T \equiv b(x) \pmod{x^L}$ and $\deg b < \deg a$, which is a matrix [Padé approximation](/pade-approximation/) problem, solved by the iterative M-Basis method of Giorgi, Jeannerod and Villard. A row of degree $d$, read backwards, gives a vector polynomial $f(x) = \sum_j f_j x^j$ with $\sum_j S_{i+j} f_j = 0$, which says that $X^T A^i (\sum_j A^j Y f_j) = 0$ for all small $i$. With high probability this means $\sum_j A^j Y f_j = 0$, that is, $A \cdot \sum_j A^j Z f_j = 0$.

Lines L7 to L10 extract a kernel vector. If $f = x^e g$, then $A^{e+1} g(A) Z = 0$, so among $u = g(A)Z, Au, A^2 u, \dots$ the last nonzero vector is in the kernel. The products on line L7 recompute the blocks $A^j Z$; storing them would cost $O(n^2)$ memory.

## Example

Over $\mathbb{F}_7$, take $s = 2$ and

$$
A = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & 1 & 3 & 0 \\ 1 & 3 & 3 & 1 \\ 2 & 0 & 0 & 1 \end{pmatrix},
$$

which is singular, since row $3$ is the sum of rows $1$ and $2$. To keep the example readable, $X = (e_1, e_2)$ and $Z = (e_3, e_4)$ are made of unit vectors instead of random blocks. Then $Y = AZ$ has rows $(0, 1)$, $(3, 0)$, $(3, 1)$, $(0, 1)$, and $L = 2 \cdot 2 + 4 = 8$. The first terms of the sequence are

$$
S_0 = \begin{pmatrix} 0 & 1 \\ 3 & 0 \end{pmatrix}, \quad S_1 = \begin{pmatrix} 6 & 2 \\ 5 & 3 \end{pmatrix}, \quad S_2 = \begin{pmatrix} 2 & 4 \\ 3 & 4 \end{pmatrix}, \quad S_3 = \begin{pmatrix} 6 & 5 \\ 4 & 0 \end{pmatrix}.
$$

The generator of least degree has $d = 1$, $f_0 = (6, 1)^T$ and $f_1 = (5, 2)^T$. For $i = 0$, $S_0 f_0 + S_1 f_1 = (1, 4)^T + (6, 3)^T = (0, 0)^T$ modulo $7$, and the same holds for $i = 1, \dots, 6$. Here $e = 0$, so line L7 gives

$$
u = Z f_0 + A Z f_1 = (0, 0, 6, 1)^T + (2, 1, 3, 2)^T = (2, 1, 2, 3)^T,
$$

and $Au = (7, 7, 14, 7)^T \equiv 0$. So line L9 returns $u$ at once. The tests check this run.

## Correctness

The algorithm is Las Vegas: line L9 returns a vector only after checking $u \ne 0$ and $Au = 0$, so every answer is correct, and on a nonsingular matrix it always fails. The approximant basis keeps the invariant $P(x) G(x) \equiv 0 \pmod{x^k}$ for the stacked matrix $G = [S^T; -I]$, with degree counters that bound $\deg a$ and $\deg b + 1$; at the end each row with $a \ne 0$ reads backwards as a generator of the projected sequence. If such a generator also annihilates the unprojected blocks, that is $\sum_j A^j Y f_j = 0$, then $A^{e+1} u = 0$ and the loop of line L8 finds a kernel vector. The [full proof](proofs/correctness.md) gives these steps. That a generator of the projected sequence is, with high probability, a generator of the blocks themselves is a theorem of Kaltofen (1995) for large fields and of Villard (1997) for small ones, which this page does not prove.

## Complexity

**Black-box products.** Line L1 takes one block product, lines L3 and L4 take $L = 2\lceil n/s \rceil + 4$, and lines L6 and L7 about $\lceil n/s \rceil$ more for the first candidate. Each block product is $s$ products of $A$ with a vector, $s w$ multiplications, so the total is about $3 n w$ field operations, the same as scalar Wiedemann. The gain is that the $s$ streams are independent: on $s$ machines the wall-clock time of this phase drops by a factor of $s$.

**Projections.** Each $S_i$ costs $n s^2$ operations, so the sequence costs $2 n^2 s$ in total. Over $\mathbb{F}_2$ with $s = 64$, a row of a block is one machine word, and the dot products are word operations.

**Generator.** The iterative M-Basis method does $L$ rounds on a $2s \times 2s$ polynomial matrix, $O(s^3 L^2) = O(s n^2)$ operations. With fast polynomial matrix multiplication (PM-Basis, or Thomé's subquadratic method) this step costs $O(s^{\omega - 1} n)$ up to logarithmic factors. All these counts are proved bounds for one try.

**Success.** For a field with many more than $n$ elements, one try succeeds with probability close to $1$ (Kaltofen 1995). Over small fields a larger $s$ helps. In runs of the implementation on random singular sparse $40 \times 40$ matrices with $4$ nonzero entries per row, one try succeeded in $60$, $87$, $98$ and $100$ of $100$ cases over $\mathbb{F}_2$ for $s = 1, 2, 4, 8$, and in every singular case over $\mathbb{F}_{65521}$ for every $s$ (between $96$ and $99$ of the $100$ random matrices of each run were singular). These rates are observations, not bounds.

**Space.** The algorithm stores $A$, a few $n \times s$ blocks and the $L$ matrices $S_i$, which is $O(w + ns)$.

## Properties

- **Las Vegas.** Every answer is checked; the randomness affects only the time.
- **Black box.** Only products $Av$ are needed, so $A$ can be sparse, structured or implicit, and it is never modified. No fill-in occurs.
- **Parallel with little communication.** The sequence phase is $s$ independent jobs, which exchange only $O(L s^2)$ field elements at the end.
- **Better over small fields than scalar Wiedemann.** With $s > 1$, the random projections have more chances to see the whole Krylov space, as the measured rates over $\mathbb{F}_2$ show.

## Variants and improvements

- **Two block widths.** Coppersmith uses $m$ columns for $X$ and $n$ for $Y$, with sequence length about $N/m + N/n$ for an $N \times N$ matrix. A larger $m$ shortens the sequence; the generator step grows.
- **Solving a system.** For $Bx = b$, kernel vectors of $[B \mid b]$ with a nonzero last entry give solutions. One can also put $b$ as a column of $Y$ and look for a generator whose coefficient at that column is nonzero.
- **Rank, determinant and minimal polynomial.** The matrix generator gives the minimal polynomial of the sequence; with preconditioners, as in the [black box](/black-box-matrix/) model, it gives the rank and determinant.
- **Distributed record computations.** The factorizations of RSA-768 and later records used block Wiedemann on matrices with hundreds of millions of rows over $\mathbb{F}_2$, splitting the sequence phase across clusters.
- **Block Lanczos.** The [block Lanczos algorithm](/block-lanczos-algorithm/) uses about the same number of products, needs no generator step, but needs communication at every iteration.

## When to use it

Use block Wiedemann for the kernel of a very large sparse matrix over a finite field, when elimination would fill in, and especially when several machines are available but fast communication between them is not. This is the linear algebra step of the [number field sieve](/general-number-field-sieve/), the [quadratic sieve](/quadratic-sieve/) and [index calculus](/index-calculus/) for discrete logarithms. Shrink the matrix first with [structured Gaussian elimination](/structured-gaussian-elimination/). For a small or dense matrix, use plain elimination.

## Pitfalls

- **Taking $Y$ random instead of $AZ$.** A generator of $A^i Y$ gives $f(A)Y = 0$, which says nothing about the kernel. With $Y = AZ$ it gives $A f(A) Z = 0$.
- **Reading the generator with the wrong degree.** The reversal must use the degree counter $d$ of the approximant row, not the degree of its $a$ part, or the condition $\deg b < d$ is lost.
- **Too short a sequence.** With $L$ below about $2n/s$, the generator of the projected sequence need not annihilate the blocks. Every candidate must be checked.
- **Small fields with $s = 1$.** Over $\mathbb{F}_2$, scalar Wiedemann often fails. Use $s \ge 4$, or many retries.
- **Memory for the blocks $A^j Z$.** Keeping them all costs $O(n^2)$; recompute them in the extraction phase instead.
- **Trivial kernel vectors.** If $A$ has zero columns, the kernel contains unit vectors, and in factoring these are useless dependencies. Remove empty columns and singletons first.

## Implementations

## History

Douglas Wiedemann published the scalar method in 1986. Don Coppersmith gave the block version in 1994, aimed at GF(2) matrices from factoring, with a matrix version of the Berlekamp-Massey algorithm. Erich Kaltofen analysed its success probability and cost for large fields in 1995, and Gilles Villard extended the analysis in 1997. Later work by Thomé, and by Giorgi, Jeannerod and Villard, made the generator step fast with polynomial matrix multiplication, and the method became the standard linear algebra step of record integer factorizations and discrete logarithm computations.

## References
