---
tag: F6ST1Z
kind: problem
slug: linear-system-modulo-2
name: System of linear equations modulo 2
aliases: [linear system over GF(2), linear equations over F2, XOR system]
area: algebra/exact-linear-algebra
level: core
summary: Solve a system of linear equations over the field of two elements, where addition is XOR.
complexity:
  vars: {m: the number of equations, n: the number of unknowns, N: the number of nonzero entries of a sparse matrix}
  time: {worst: "O(m n min(m, n))"}
prereqs: [gaussian-elimination, nullspace]
see_also: [xor-gaussian-elimination, bitset-gaussian-elimination, xor-sat, wiedemann-algorithm, block-lanczos-algorithm, structured-gaussian-elimination, quadratic-sieve]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Chapter 6, Subexponential factoring algorithms (the exponent vectors modulo 2 of the quadratic sieve and the number field sieve, and the sparse linear algebra over F2 that finds their dependencies)
  - paper: "Peter L. Montgomery, A block Lanczos algorithm for finding dependencies over GF(2), Advances in Cryptology, EUROCRYPT 95, Lecture Notes in Computer Science 921, Springer, 1995"
    locator: pp. 106 to 120 (dependencies of a large sparse matrix over F2 with word-wide block operations)
  - paper: doi:10.1109/TIT.1986.1057137
    title: Douglas H. Wiedemann, Solving sparse linear equations over finite fields, IEEE Transactions on Information Theory 32(1), 1986
    locator: pp. 54 to 62 (black box solution of sparse systems over a finite field in about n applications of the matrix)
  - paper: doi:10.1109/TIT.1978.1055873
    title: Elwyn R. Berlekamp, Robert J. McEliece and Henk C. A. van Tilborg, On the inherent intractability of certain coding problems, IEEE Transactions on Information Theory 24(3), 1978
    locator: pp. 384 to 386 (finding a solution of a system over F2 of minimum Hamming weight is NP-hard)
---

A system of linear equations modulo $2$ asks for a vector $x$ of bits with $A x = b$, where the arithmetic is in the field $\mathbb{F}_2 = \{0, 1\}$: addition is XOR and multiplication is AND. It is the simplest case of a [linear system](/linear-system-solving/) over a finite field, and [Gaussian elimination](/gaussian-elimination/) solves it with no growth of numbers at all, since each entry is one bit. The large sparse systems of this kind that come from the [quadratic sieve](/quadratic-sieve/) and the [general number field sieve](/general-number-field-sieve/) are solved with [structured Gaussian elimination](/structured-gaussian-elimination/), [block Lanczos](/block-lanczos-algorithm/) or [block Wiedemann](/block-wiedemann-algorithm/).

## In plain words

You have some switches, each on or off, and some lamps. Each lamp is wired to some of the switches, and it is lit when an odd number of its switches are on. You want a given set of lamps to be lit. Which switches do you turn on?

Each lamp gives one equation in which "plus" means "flip". Elimination solves the equations as in school algebra, but no fractions appear, because the only numbers are zero and one, and dividing by one changes nothing. A computer stores each equation as a row of bits and adds two rows with one XOR instruction for each machine word.

## Definition

**Notation.** $\mathbb{F}_2 = \mathbb{Z}/2\mathbb{Z}$. $A$ is an $m \times n$ matrix over $\mathbb{F}_2$ and $b \in \mathbb{F}_2^m$.

**Input.** $A$ and $b$.

**Output.** A vector $x \in \mathbb{F}_2^n$ with $A x = b$, or the answer that there is none. In the search form one often also asks for a basis $u_1, \ldots, u_{n-r}$ of the [nullspace](/nullspace/) of $A$, where $r = \operatorname{rank}(A)$.

**Structure of the solutions.** The system is solvable if and only if $\operatorname{rank}(A) = \operatorname{rank}(A \mid b)$. Then the set of solutions is $x_0 + \operatorname{null}(A)$, and by the [rank-nullity theorem](/rank-nullity-theorem/) it has exactly $2^{\,n - r}$ elements. If the system is not solvable, elimination finds a set of rows whose sum is the zero row while the sum of the corresponding entries of $b$ is $1$: a certificate that no solution exists.

## Variants

- **Decision.** Is there a solution? This is the same as comparing two ranks.
- **Homogeneous system, or dependencies.** Find nonzero $x$ with $A x = 0$, or a basis of all of them. In factoring, $A$ is the transpose of the matrix of exponent vectors, and each nullspace vector is a set of relations whose product is a square.
- **Counting and sampling.** The number of solutions is $0$ or $2^{n-r}$. A uniform random solution is $x_0 + \sum_i c_i u_i$ with independent uniform bits $c_i$.
- **XOR-SAT.** A formula that is a conjunction of XOR clauses is the same problem; see [XOR-SAT](/xor-sat/). SAT solvers mix it with ordinary clauses by [Gaussian elimination on XOR constraints](/xor-gaussian-elimination/).
- **Minimum weight solution.** Find a solution with the fewest ones. This is syndrome decoding of a binary linear code, and its decision version is NP-complete (Berlekamp, McEliece and van Tilborg, 1978).
- **Sparse systems.** $A$ has $N \ll m n$ nonzero entries, and the algorithm may only multiply by $A$ and $A^T$, as a [black box matrix](/black-box-matrix/).

## Examples

**A solvable system.** Over $\mathbb{F}_2$, take

$$A = \begin{pmatrix} 1 & 1 & 0 & 1 \\ 0 & 1 & 1 & 1 \\ 1 & 0 & 1 & 0 \\ 1 & 1 & 1 & 0 \end{pmatrix}, \qquad b = \begin{pmatrix} 1 \\ 0 \\ 1 \\ 1 \end{pmatrix}.$$

The [reduced row echelon form](/reduced-row-echelon-form/) of $(A \mid b)$ has the rows $(1, 0, 0, 1 \mid 1)$, $(0, 1, 0, 0 \mid 0)$, $(0, 0, 1, 1 \mid 0)$ and a zero row. So the rank is $3$, the unknown $x_4$ is free, and the solutions are $x_1 = 1 + x_4$, $x_2 = 0$, $x_3 = x_4$: the two vectors $(1, 0, 0, 0)$ and $(0, 0, 1, 1)$. There are $2^{4 - 3} = 2$ of them, and $(1, 0, 1, 1)$ spans the nullspace.

**An unsolvable system.** In the same $A$, the rows $1$, $2$ and $3$ add up to the zero row. So each solvable right side has $b_1 + b_2 + b_3 = 0$. With $b = (1, 1, 1, 1)^T$ this sum is $1$, and the system has no solution; those three rows are the certificate.

**A dependency in the quadratic sieve.** To factor $1649$, compute $41^2 \bmod 1649 = 32 = 2^5$, $42^2 \bmod 1649 = 115 = 5 \cdot 23$ and $43^2 \bmod 1649 = 200 = 2^3 \cdot 5^2$. Over the primes $2, 3, 5$, the exponent vectors modulo $2$ of $32$ and $200$ are both $(1, 0, 0)$, so their sum is zero: $32 \cdot 200 = 6400 = 80^2$. Then $(41 \cdot 43)^2 \equiv 80^2 \pmod{1649}$, and $\gcd(41 \cdot 43 - 80, 1649) = 17$ is a factor, with $1649 = 17 \cdot 97$. In a real run there are many thousands of such vectors, and the dependency comes from a large sparse system over $\mathbb{F}_2$.

## Known algorithms

- [Gaussian elimination](/gaussian-elimination/) on bit rows: $O(m n \min(m, n))$ bit operations, or $O(m n \min(m, n) / w)$ word operations with $w$-bit words, as in [bitset Gaussian elimination](/bitset-gaussian-elimination/) and [XOR Gaussian elimination](/xor-gaussian-elimination/). No pivoting strategy is needed for correctness: every nonzero entry is $1$.
- Elimination with table lookups (the method of four Russians, as in the M4RI library) saves a factor of about $\log n$ for dense matrices.
- Elimination by blocks with fast matrix multiplication solves an $n \times n$ system with $O(n^\omega)$ bit operations, where $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/); see [LU decomposition](/lu-decomposition/) and [boolean matrix multiplication](/boolean-matrix-multiplication/) for the products used.
- [Structured Gaussian elimination](/structured-gaussian-elimination/) removes most rows and columns of a sparse system cheaply, before a dense or iterative method.
- The [Wiedemann algorithm](/wiedemann-algorithm/) and its block form need $O(n)$ products by $A$, so $O(n N + n^2)$ bit operations for an $n \times n$ matrix with $N$ nonzeros, and $O(n)$ extra space; they are randomized.
- [Block Lanczos](/block-lanczos-algorithm/) (Montgomery, 1995) works on $w$ vectors at once with word operations and needs about $n / (w - 0.76)$ iterations; it is the usual method in factoring programs.

## Bounds

Over $\mathbb{F}_2$ each entry is one bit, so the field operations and the bit operations are the same count: there is no size bound to track, which is the main difference from systems over $\mathbb{Z}$ or $\mathbb{Q}$. Each algorithm must read the input, so $\Omega(m n)$ bit operations are needed for a dense matrix in the worst case and $\Omega(N)$ for a sparse one. The best proved upper bound for a dense $n \times n$ system is $O(n^\omega)$. For sparse systems the best proved bounds are those of the Wiedemann method, $O(n N)$ plus lower-order terms, with a small probability of failure that can be made smaller by repetition. No lower bound above the input size is known for either case. The minimum weight variant is NP-hard, so no polynomial algorithm is expected for it.

## Reductions

- **XOR-SAT to this problem and back.** Each XOR clause $x_{i_1} \oplus \cdots \oplus x_{i_k} = c$ is one row of $A$ and one bit of $b$, in time linear in the size of the formula.
- **Rank and nullspace.** Solving $A x = b$ reduces to an echelon form of $(A \mid b)$, so to [rank computation](/rank-computation/) and [nullspace computation](/nullspace-computation/) over $\mathbb{F}_2$.
- **Products.** The Wiedemann reduction turns a system with a black box $A$ into the [minimal polynomial](/matrix-minimal-polynomial/) of a scalar sequence $u^T A^i b$, found by the [Berlekamp-Massey algorithm](/berlekamp-massey/).

## Applications

- **Factoring.** The quadratic sieve and the number field sieve find a congruence of squares from a dependency among exponent vectors modulo $2$, as in the example above.
- **Coding theory.** Encoding, syndrome computation and erasure decoding of binary linear codes solve systems over $\mathbb{F}_2$.
- **Cryptanalysis.** Algebraic attacks on stream ciphers built from linear feedback shift registers linearize the equations of the key bits and solve a large system over $\mathbb{F}_2$.
- **Puzzles and SAT.** The "lights out" puzzle and XOR constraints in SAT solving are systems over $\mathbb{F}_2$.

## References
