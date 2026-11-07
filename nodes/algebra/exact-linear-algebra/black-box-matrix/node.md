---
tag: SDPPKB
kind: model
slug: black-box-matrix
name: Black-box matrix model
aliases:
- black-box model
- black box linear algebra
- matrix-vector product oracle
area: algebra/exact-linear-algebra
level: advanced
summary: Model in which the matrix is accessed only through matrix-vector products, enabling sparse and structured methods.
prereqs: [matrix-vector-multiplication, matrix-minimal-polynomial]
see_also: [wiedemann-algorithm, block-wiedemann-algorithm, block-lanczos-algorithm, structured-gaussian-elimination, krylov-subspace, berlekamp-massey, straight-line-program, sparse-matrix-vector-multiplication]
sources:
  - paper: doi:10.1109/TIT.1986.1057137
    title: Douglas H. Wiedemann, Solving sparse linear equations over finite fields, IEEE Transactions on Information Theory 32(1), 1986
    locator: pp. 54 to 62 (systems, determinants and minimal polynomials from O(n) products with the matrix and O(n^2) further field operations)
  - paper: "Erich Kaltofen and B. David Saunders, On Wiedemann's method of solving sparse linear systems, Proceedings of AAECC-9, Lecture Notes in Computer Science 539, Springer, 1991"
    locator: pp. 29 to 38 (Toeplitz preconditioners, the rank of a black-box matrix, and singular systems)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 12, Section 12.4, Wiedemann's algorithm and black box linear algebra
  - paper: doi:10.1090/S0025-5718-1994-1192970-7
    title: Don Coppersmith, Solving homogeneous linear equations over GF(2) via block Wiedemann algorithm, Mathematics of Computation 62(205), 1994
    locator: pp. 333 to 350 (blocks of vectors, so that several products are computed at once)
  - paper: "Li Chen, Wayne Eberly, Erich Kaltofen, B. David Saunders, William J. Turner and Gilles Villard, Efficient matrix preconditioners for black box linear algebra, Linear Algebra and its Applications 343-344, 2002"
    locator: pp. 119 to 146 (diagonal, Toeplitz and butterfly preconditioners and the probabilities that they work)
  - paper: "Jean-Guillaume Dumas, Thierry Gautier, Mark Giesbrecht, Pascal Giorgi, Bradford Hovinen, Erich Kaltofen, B. David Saunders, Will J. Turner and Gilles Villard, LinBox: a generic library for exact linear algebra, Proceedings of ICMS 2002, World Scientific"
    locator: pp. 40 to 50 (the black-box interface as a software design, and its implementations)
---

In the black-box matrix model, an algorithm does not see the entries of the matrix $A$. It may only ask for products: give a vector $v$, get back $Av$, and sometimes $A^T u$ as well. Everything else is ordinary field arithmetic on a few vectors. The model fits sparse matrices, structured matrices such as Toeplitz matrices, and matrices given as products or sums of simpler ones, where a product $Av$ is much cheaper than $n^2$ operations and where elimination would destroy the structure by fill-in. [Wiedemann's algorithm](/wiedemann-algorithm/) showed in 1986 that systems, determinants and minimal polynomials over a finite field need only $O(n)$ products and $O(n^2)$ more operations in this model, with storage for $O(n)$ field elements.

Notation: $K$ is a field, often a finite field $\mathbb{F}_q$. $A$ is an $m \times n$ matrix over $K$, square with $m = n$ unless said otherwise, and $\mu(A)$ is the cost, in field operations, of one product $v \mapsto Av$. For a sparse matrix with $N$ nonzero entries, $\mu(A) \le 2N$. $\omega$ is the exponent of matrix multiplication.

## The machine

The machine has three parts.

- **The black box.** An oracle that holds $A$ and, on input $v \in K^n$, returns $Av \in K^m$. A *transpose* black box also returns $A^T u$ for $u \in K^m$. The algorithm cannot read entries, test the structure, or modify $A$.
- **A field processor.** The algorithm performs $+$, $-$, $\times$ and $\div$ in $K$, tests for zero, and keeps a working memory of field elements. Over a finite field each operation has constant cost; over $\mathbb{Q}$ the model is used with a bit cost and with the same operations modulo primes.
- **Random elements.** The algorithm may draw elements uniformly from a finite subset $S \subseteq K$, or from an extension field when $K$ is small. Most results are randomized: Monte Carlo (the answer may be wrong with small probability) or Las Vegas (the answer is checked, and the algorithm may report failure).

Black boxes compose. If $A$ and $B$ are black boxes, then so are $AB$, $A + B$, $A^T$ when the transpose is available, $DA$ for a diagonal $D$, and $T A$ for a Toeplitz $T$. This is how preconditioners are applied: the algorithm runs on the composed box $\tilde A = T_1 A T_2 D$ without ever forming it.

## What it counts

The cost of an algorithm is given by three numbers:

- the number of black-box calls, so the time spent in the box is that number times $\mu(A)$;
- the number of further field operations, outside the box;
- the extra storage, in field elements, beyond what the box itself uses.

A typical bound reads $O(n)$ calls, $O(n^2)$ further operations and $O(n)$ storage, for a total time of $O(n \mu(A) + n^2)$. For a sparse matrix with $N \ge n$ nonzero entries this is $O(nN)$, against $O(n^3)$ for dense elimination, and the storage stays $O(N)$ instead of the $O(n^2)$ that fill-in can cause. The probability of failure is part of the result, and it depends on the size of the set $S$, typically like $n^2/|S|$ for a single run.

## Relation to other models

- **Dense matrices.** $n$ calls with the unit vectors $e_1, \dots, e_n$ return the columns of $A$, so a black box can always be turned into an explicit matrix and any dense algorithm can then be used. This costs $n \mu(A)$ time and $n^2$ storage, which is what the model is meant to avoid. Conversely, an explicit matrix is a black box with $\mu(A) = O(n^2)$, or $O(N)$ in a sparse format.
- **Straight-line programs.** A black box computed by a linear [straight-line program](/straight-line-program/) of length $L$ has $\mu(A) \le L$. By the transposition principle, a linear straight-line program for $v \mapsto Av$ can be turned into one for $u \mapsto A^T u$ of the same length up to a constant (and the number of inputs and outputs). So a transpose box is often free in practice, but the model keeps the two separate.
- **Structured matrices.** Toeplitz, Hankel, circulant and [Vandermonde](/vandermonde-matrix/) matrices have products in $O(n \log n)$ or $O(n \log^2 n)$ operations with fast polynomial arithmetic, so they are natural black boxes. Sparse products are treated on the [sparse matrix-vector multiplication](/sparse-matrix-vector-multiplication/) page.
- **Krylov methods in floating point.** Conjugate gradients, [Lanczos](/lanczos-algorithm/) and GMRES use the same access to $A$, through the [Krylov subspace](/krylov-subspace/) $\operatorname{span}\{v, Av, A^2 v, \dots\}$. The exact methods of this model replace orthogonality and convergence by the minimal polynomial and the [Berlekamp-Massey algorithm](/berlekamp-massey/).
- **Elimination-based sparse methods.** [Structured Gaussian elimination](/structured-gaussian-elimination/) reads the entries and eliminates carefully to limit fill-in. It is often used first to shrink a sparse system, and a black-box method finishes the smaller, denser system.

## Known results in the model

The core tool is the scalar sequence $a_i = u^T A^i v$ for random $u$ and $v$. By the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/), it satisfies a linear recurrence whose characteristic polynomial divides the [minimal polynomial](/matrix-minimal-polynomial/) $\mu_A$, and for random $u, v$ it is equal to $\mu_A$ with good probability. Computing $a_0, \dots, a_{2n-1}$ takes $2n$ calls, and the Berlekamp-Massey algorithm finds the recurrence with $O(n^2)$ operations.

**A small example.** Over $\mathbb{F}_7$ take $A$ with rows $(2, 3, 1)$, $(4, 1, 5)$, $(1, 6, 3)$ and $u = v = e_1$. Five calls give $a_0, \dots, a_5 = 1, 2, 3, 2, 4, 2$. Berlekamp-Massey returns the recurrence $a_{i+3} + a_{i+2} + 3a_{i+1} + 3a_i = 0$, which holds for $i = 0, 1, 2$; for example $2 + 3 + 6 + 3 = 14 \equiv 0$. So $\mu_A$ is $x^3 + x^2 + 3x + 3$, which has degree $3$ and so equals $\chi_A \bmod 7$, and $\det A \equiv (-1)^3 \cdot 3 \equiv 4 \pmod 7$. Indeed $\det A = -52 \equiv 4$.

- **Minimal polynomial.** Monte Carlo with $2n$ calls and $O(n^2)$ operations; Las Vegas by repeating with new vectors and taking the least common multiple (Wiedemann 1986).
- **Nonsingular systems.** If $\mu_A(x) = x\, g(x) + c_0$ with $c_0 \ne 0$, then $x = -c_0^{-1} g(A) b$ solves $Ax = b$, with $n$ more calls. The result is checked by one more product, so the solver is Las Vegas (Wiedemann 1986).
- **Determinant.** With a random diagonal preconditioner $D$, the minimal polynomial of $DA$ equals its characteristic polynomial with good probability, so $\det(DA)$ is its constant term up to sign and $\det A = \det(DA)/\det D$. Cost $O(n)$ calls and $O(n^2)$ operations.
- **Rank and singular systems.** Kaltofen and Saunders (1991) precondition with random triangular Toeplitz matrices and a diagonal matrix, so that the leading $r \times r$ block of $\tilde A$ is nonsingular for $r = \operatorname{rank} A$; the rank is then read from the degree of the minimal polynomial of $\tilde A$. The same preconditioning gives random solutions of consistent singular systems, and a basis of the kernel by repetition. Cost $O(n)$ calls per answer and $O(n^2 \log n)$ further operations.
- **Small fields.** Over $\mathbb{F}_2$ the random choices fail too often, so the vectors and preconditioners are taken in an extension field $\mathbb{F}_{2^k}$, or blocks of vectors are used. The [block Wiedemann algorithm](/block-wiedemann-algorithm/) (Coppersmith 1994) uses blocks of $w$ vectors, computes $w$ products at once with word operations over $\mathbb{F}_2$, and parallelizes over several machines. The [block Lanczos algorithm](/block-lanczos-algorithm/) (Montgomery 1995) needs a transpose box and is the other standard method for the huge sparse systems of integer factoring.
- **Integer matrices.** For a black box over $\mathbb{Z}$, the same methods run modulo primes and are combined by the Chinese remainder theorem, or by $p$-adic lifting in the style of [Dixon](/dixon-p-adic-lifting/), and give determinants and rational solutions of sparse integer systems.
- **Preconditioners.** Chen, Eberly, Kaltofen, Saunders, Turner and Villard (2002) collected the preconditioners for these tasks, including butterfly networks with $O(n \log n)$ cost, and proved the probabilities with which they work.

These results are proved, with explicit failure probabilities over a large enough field. In practice the probabilities are much better than the bounds, and one run with a well-chosen preconditioner usually succeeds. The LinBox library implements this model as a programming interface.

## References
