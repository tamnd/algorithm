---
tag: Q8APKG
kind: problem
slug: determinant-computation
name: Determinant computation
aliases:
- computing the determinant
- determinant problem
area: algebra/exact-linear-algebra
level: core
summary: Compute the determinant of a square matrix exactly, as a rational or integer.
prereqs: [determinant]
see_also: [determinant-gaussian-elimination, bareiss-algorithm, multimodular-determinant, berkowitz-algorithm, hadamard-bound, wiedemann-algorithm, characteristic-polynomial-computation, permanent-computation]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 5, Section 5.5, Modular determinant computation (elimination over Q, its cost, the Hadamard bound and the small primes and big prime methods); Section 12.4, Wiedemann's algorithm and black box linear algebra
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.3, Computing determinants (Gaussian elimination over a field, the Gauss-Bareiss method over Z, and the modular method)
  - paper: doi:10.1090/S0025-5718-1974-0331751-8
    title: James R. Bunch and John E. Hopcroft, Triangular factorization and inversion by fast matrix multiplication, Mathematics of Computation 28(125), 1974
    locator: pp. 231 to 236 (LUP decomposition, and so the determinant, in O(n^ω) field operations)
  - paper: doi:10.1016/0304-3975(83)90110-X
    title: Walter Baur and Volker Strassen, The complexity of partial derivatives, Theoretical Computer Science 22(3), 1983
    locator: the derivative theorem and its corollary that the inverse costs at most a constant times the determinant
  - paper: doi:10.1090/S0025-5718-1968-0226829-0
    title: Erwin H. Bareiss, Sylvester's identity and multistep integer-preserving Gaussian elimination, Mathematics of Computation 22(103), 1968
    locator: pp. 565 to 578 (fraction-free elimination; every intermediate entry is a minor)
  - paper: doi:10.1016/0020-0190(84)90018-8
    title: Stuart J. Berkowitz, On computing the determinant in small parallel time using a small number of processors, Information Processing Letters 18(3), 1984
    locator: pp. 147 to 150 (a division-free algorithm over any commutative ring, in NC^2)
  - paper: doi:10.1109/TIT.1986.1057137
    title: Douglas H. Wiedemann, Solving sparse linear equations over finite fields, IEEE Transactions on Information Theory 32(1), 1986
    locator: pp. 54 to 62 (the determinant of a sparse matrix from the minimal polynomial of a preconditioned matrix)
  - paper: "Arne Storjohann, The shifted number system for fast linear algebra on integer matrices, Journal of Complexity 21(4), 2005"
    locator: the Las Vegas algorithm for the determinant of an integer matrix in about n^ω b bit operations, up to logarithmic factors
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 1979
    locator: "pp. 189 to 201 (the permanent, with the same formula without signs, is #P-complete)"
---

Determinant computation asks for the exact value of $\det A$ for a square matrix $A$ over a field or a commutative ring, most often over $\mathbb{Z}$ or $\mathbb{Q}$. The defining Leibniz formula has $n!$ terms, but elimination needs only $O(n^3)$ field operations, and with fast matrix multiplication $O(n^\omega)$, which is optimal up to a constant factor because the determinant and matrix multiplication have the same algebraic cost. Over $\mathbb{Z}$, the problem has a second side: the determinant can have about $n(b + \tfrac12 \log_2 n)$ bits, and the methods differ mainly in how they keep the intermediate numbers small. The main approaches are elimination over $\mathbb{Q}$, fraction-free elimination, modular methods with the Chinese remainder theorem, division-free methods for rings, and black-box methods for sparse matrices.

Notation: $R$ is a commutative ring, $K$ a field, $A = (a_{ij})$ an $n \times n$ matrix, $\omega$ the exponent of matrix multiplication ($2 \le \omega < 2.372$), and for an integer matrix $b$ is the maximum binary length of an entry, so $|a_{ij}| < 2^b$. Costs are given in operations of $R$ or $K$ (the arithmetic model, as in an [algebraic computation tree](/algebraic-computation-tree/) or a [straight-line program](/straight-line-program/)) and, over $\mathbb{Z}$, in bit operations.

## In plain words

The determinant of a square table of numbers is one number that says, among other things, whether the table can be inverted. Its formula has a term for every way to pick one entry from each row and each column, which is far too many terms for a big table. So the problem is to find the exact value much faster. Row operations do it with a number of steps that grows like the cube of the size. For whole numbers there is an extra difficulty: the numbers met on the way can get very long, and good methods prevent that, for example by working with remainders.

## Definition

**Input:** an $n \times n$ matrix $A$ over a commutative ring $R$, given by its $n^2$ entries.

**Output:** $\det A = \sum_{\sigma \in S_n} \operatorname{sgn}(\sigma) \prod_{i=1}^{n} a_{i \sigma(i)} \in R$, as defined on the [determinant](/determinant/) page. For $n = 0$ the output is $1$.

Two cost measures are standard. In the *arithmetic* model, each operation of $R$ costs $1$, and divisions are allowed only where $R$ is a field or where the division is known to be exact. In the *bit* model over $R = \mathbb{Z}$, the cost is the number of bit operations, and the output itself has up to $n(b + \tfrac12 \log_2 n)$ bits by the [Hadamard bound](/hadamard-bound/).

## Variants

- **Over a field $K$.** Divisions are allowed. Over a finite field, every operation has constant size. Over $\mathbb{Q}$, the input is an integer matrix after clearing denominators.
- **Over $\mathbb{Z}$, bit complexity.** The input has $n^2$ entries of $b$ bits, and the target is a bound in $n$ and $b$.
- **Over a ring without divisions.** For a commutative ring that is not a domain, such as $\mathbb{Z}/m\mathbb{Z}$ with composite $m$, or for symbolic entries, the algorithm may use only $+$, $-$ and $\times$.
- **Polynomial matrices.** Over $K[x]$, the output is a polynomial of degree at most the sum of the row degrees. Evaluation at enough points and [interpolation](/polynomial-interpolation/) reduces this to determinants over $K$.
- **Sign only.** Geometric predicates such as the [orientation test](/orientation-test/) need only the sign of a small determinant, but exactly.
- **Singularity.** Decide whether $\det A = 0$. Over a field this is equivalent to $\operatorname{rank} A < n$.
- **Sparse or structured matrices.** For a matrix given only by the map $v \mapsto Av$, a [black-box](/black-box-matrix/) method such as [Wiedemann's algorithm](/wiedemann-algorithm/) finds $\det A$ without storing $A$.

## Examples

- $\det \begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$.
- The matrix $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$ has $\det M = 18$. The Hadamard bound gives $|\det M| \le \sqrt{5 \cdot 11 \cdot 17} < 31$, so the residues modulo $7$ and $11$, which are $4$ and $7$, determine it: the Chinese remainder theorem gives $18$ modulo $77 > 2 \cdot 30$.
- The matrix with rows $(0, 1, 2, 3)$, $(1, 0, 1, 2)$, $(2, 1, 0, 1)$, $(3, 2, 1, 0)$ has determinant $-12$; the trace of [elimination](/determinant-gaussian-elimination/) shows one row swap and the pivots $1, 1, -4, -3$.
- The [Vandermonde matrix](/vandermonde-matrix/) of the points $1, 2, 3, 4$ has determinant $\prod_{i<j}(x_j - x_i) = 1 \cdot 2 \cdot 3 \cdot 1 \cdot 2 \cdot 1 = 12$.
- The Hadamard matrix of order $4$ with rows $(1, 1, 1, 1)$, $(1, -1, 1, -1)$, $(1, 1, -1, -1)$, $(1, -1, -1, 1)$ has determinant $16 = 4^{4/2}$, which is the largest possible for entries of absolute value $1$. So the Hadamard bound on the output size is attained.

## Known algorithms

| Algorithm | Ring | Arithmetic cost | Bit cost over $\mathbb{Z}$ |
| --- | --- | --- | --- |
| Leibniz formula | any commutative | $\Theta(n \cdot n!)$ | |
| [Laplace expansion](/laplace-expansion/) with memoization over column sets | any commutative | $O(n 2^n)$ | |
| [Gaussian elimination](/determinant-gaussian-elimination/) | field | $2n^3/3 + O(n^2)$ | $O(n^5 (b + \log n)^2)$, proved |
| [Kraut (LU) method](/kraut-determinant/) | field | $2n^3/3 + O(n^2)$ | as elimination |
| [Bareiss algorithm](/bareiss-algorithm/) | integral domain, exact division | $O(n^3)$ | $O(n^5 (b + \log n)^2)$ with schoolbook arithmetic, proved |
| [Multimodular determinant](/multimodular-determinant/) | $\mathbb{Z}$ | | $O(n^4 (b + \log n))$ word operations for the eliminations with word-size primes, plus reduction and Chinese remaindering |
| [Berkowitz algorithm](/berkowitz-algorithm/) | any commutative, no division | $O(n^4)$ | |
| [Faddeev-LeVerrier algorithm](/faddeev-leverrier-algorithm/) | field of characteristic $0$ or $> n$ | $O(n^4)$, or $O(n^{\omega + 1})$ | |
| LUP by fast multiplication (Bunch and Hopcroft) | field | $O(n^\omega)$ | |
| [Wiedemann's algorithm](/wiedemann-algorithm/) | field, randomized | $O(n)$ products $Av$ plus $O(n^2)$ | |
| Storjohann's shifted number system | $\mathbb{Z}$, Las Vegas | | $O(n^\omega b)$ up to logarithmic factors |

The proved bit bounds for elimination and Bareiss come from the fact that every intermediate number is a minor of $A$, or a quotient of two minors, and so has $O(n(b + \log n))$ bits by the Hadamard bound. In practice, the determinant is often much smaller than the Hadamard bound, and multimodular codes with early termination stop when the reconstructed value does not change for a few more primes; that saves primes, but its correctness is then probabilistic.

## Bounds

- **Output size.** $|\det A| \le \prod_i \|a_i\|_2 \le n^{n/2} 2^{bn}$ for an integer matrix with rows $a_i$, so the output has at most $n(b + \tfrac12 \log_2 n) + 1$ bits. Hadamard matrices, with entries $\pm 1$, attain $n^{n/2}$, so the term $\tfrac12 n \log_2 n$ cannot be removed, and scaling such a matrix by $2^{b-1}$ shows that the term $n(b-1)$ is needed too.
- **Arithmetic upper bound.** $O(n^\omega)$ field operations, by LUP decomposition with fast multiplication. With Strassen's algorithm this is $O(n^{\log_2 7}) = O(n^{2.81})$.
- **Arithmetic lower bound.** Only $\Omega(n^2)$ is known for general algorithms, since each entry must be read. The exponent of the determinant equals $\omega$ (see Reductions), so a better lower bound on the determinant would be a lower bound on matrix multiplication.
- **Division-free.** Without divisions, $O(n^4)$ ring operations suffice by Berkowitz, and with fast matrix multiplication the exponent is below $3$ (Kaltofen and Villard).
- **Parallel time.** The determinant is in $\mathrm{NC}^2$: Berkowitz's algorithm runs in $O(\log^2 n)$ parallel time with a polynomial number of processors over any commutative ring.
- **Contrast with the permanent.** The permanent has the same formula without the signs, but computing it is #P-complete (Valiant 1979), even for $0$-$1$ matrices. See [permanent computation](/permanent-computation/).

## Reductions

- **Determinant to LUP decomposition to multiplication.** Bunch and Hopcroft compute $PA = LU$ in $O(n^\omega)$ field operations, and $\det A = \pm \prod_i u_{ii}$.
- **Inversion to determinant.** By the theorem of Baur and Strassen, a [straight-line program](/straight-line-program/) of length $L$ for $\det A$ gives one of length at most a constant times $L$ for all $n^2$ partial derivatives. Since $\partial \det A / \partial a_{ij}$ is the cofactor $(\operatorname{adj} A)_{ji}$, this computes $\operatorname{adj} A$ and $A^{-1} = \operatorname{adj} A / \det A$.
- **Multiplication to inversion.** For $n \times n$ matrices $X$ and $Y$, the $3n \times 3n$ block matrix with block rows $(I, X, 0)$, $(0, I, Y)$, $(0, 0, I)$ has the inverse with block rows $(I, -X, XY)$, $(0, I, -Y)$, $(0, 0, I)$. So a product costs one inversion of a matrix three times as large.

  Together these show that the determinant, the inverse and the product have the same exponent $\omega$.
- **Determinant and characteristic polynomial.** $\det A = (-1)^n \chi_A(0)$, so a [characteristic polynomial](/characteristic-polynomial-computation/) algorithm gives the determinant. Conversely, $\chi_A(x)$ has degree $n$, so its values $\det(x_k I - A)$ at $n + 1$ points determine it by interpolation.
- **Solving.** By [Cramer's rule](/cramers-rule/), $n + 1$ determinants solve a nonsingular system. Over $\mathbb{Z}$ the reverse direction is also used: the common denominator of the solution of $Ax = b$ for a random $b$ is, with high probability, the largest invariant factor of the [Smith normal form](/smith-normal-form/), a large divisor of $\det A$.

## Applications

- **Counting.** The [matrix-tree theorem](/matrix-tree-theorem/) counts spanning trees by a determinant, the [Kasteleyn method](/kasteleyn-method/) counts perfect matchings of planar graphs, and the [Lindstrom-Gessel-Viennot lemma](/lindstrom-gessel-viennot-lemma/) counts families of disjoint lattice paths.
- **Polynomial algebra.** The [resultant](/resultant/) of two polynomials is the determinant of their [Sylvester matrix](/sylvester-matrix/).
- **Randomized tests.** The [Tutte matrix](/tutte-matrix/) of a graph has a nonzero determinant exactly when the graph has a [perfect matching](/perfect-matching/). Evaluating it at random points, by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), gives a randomized test.
- **Geometry.** Orientation and in-circle tests are signs of small determinants, and the volume of a simplex is a determinant divided by $n!$.
- **Lattices.** The [determinant of a lattice](/lattice-determinant/) with a square basis matrix $B$ is $|\det B|$.
- **Invertibility.** An integer matrix has an integer inverse exactly when $\det A = \pm 1$; see [unimodular matrix](/unimodular-matrix/).

## References
