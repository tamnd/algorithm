---
tag: JVN17A
kind: problem
slug: multipoint-evaluation
name: Multipoint evaluation
aliases:
- evaluating a polynomial at many points
- multipoint polynomial evaluation
area: algebra/polynomial-arithmetic
level: advanced
summary: Evaluate a degree-n polynomial at n given points, in quasi-linear time with the subproduct tree.
prereqs: [polynomial, horner-rule, point-value-representation, factor-theorem]
see_also: [fast-multipoint-evaluation, subproduct-tree, fast-interpolation, fast-polynomial-division, fast-fourier-transform, bluestein-fft, evaluation-interpolation-paradigm, pollard-strassen]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 10.1, Fast multipoint evaluation; Section 10.2, Fast interpolation; Section 10.3, Fast Chinese remaindering
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of polynomials
  - paper: doi:10.1145/860854.860870
    title: Alin Bostan, Gregoire Lecerf and Eric Schost, Tellegen's principle into practice, Proceedings of ISSAC 2003, 37-44
    locator: transposed multiplication and division, and the faster multipoint evaluation and interpolation built from them
---

Multipoint evaluation asks for the values $f(u_0), \ldots, f(u_{n-1})$ of one polynomial $f$ of degree less than $n$ at $n$ given points. Horner's rule at each point solves it with $\Theta(n^2)$ ring operations. The subproduct tree solves it with $O(M(n) \log n)$, which is $O(n \log^2 n)$ when fast Fourier multiplication is available, and special points such as roots of unity allow $O(n \log n)$. The best lower bound known for general points is $\Omega(n \log n)$, so the exact complexity is open.

Notation: $R$ is a commutative ring with $1$, $f = \sum_{k<n} f_k x^k \in R[x]$, and $M(n)$ is the cost of multiplying two polynomials of degree less than $n$ over $R$. Costs count ring operations in the algebraic complexity model.

## In plain words

You have one polynomial and a long list of numbers. You want the value of the polynomial at each number. The direct way works on one number at a time and uses about as many steps as the degree for each, so the total grows with the square of the list length. A faster way works on many numbers at once. It splits the list in two halves and replaces the polynomial by two smaller polynomials, one that gives the right values on each half. Then it splits each half again, and so on, until each piece holds one number and the small polynomial is just its value.

## Definition

**Input:** $f \in R[x]$ with $\deg f < n$, given by its coefficients, and points $u_0, \ldots, u_{n-1} \in R$.

**Output:** the values $f(u_0), \ldots, f(u_{n-1}) \in R$.

The points need not be distinct. In matrix form, the output is $V c$, where $c = (f_0, \ldots, f_{n-1})^T$ and $V = (u_i^j)_{0 \le i, j < n}$ is the [Vandermonde matrix](/vandermonde-matrix/) of the points. The inverse problem, from $n$ values at $n$ points whose differences are units back to the coefficients, is [interpolation](/fast-interpolation/), and the two together convert between the coefficient form and the [point-value form](/point-value-representation/).

The key identity is the [factor theorem](/factor-theorem/) in its remainder form: $f(u) = f \bmod (x - u)$. More generally, if $m = \prod_{i \in S} (x - u_i)$, then $f$ and $f \bmod m$ have the same value at every $u_i$ with $i \in S$, since $f - (f \bmod m)$ is a multiple of $m$.

## Variants

- **$N$ points and degree less than $n$, with $N \ne n$.** If $N > n$, split the points into $\lceil N/n \rceil$ groups of $n$ and solve each. If $N < n$, first reduce $f$ modulo $\prod (x - u_i)$, at a cost of $O(M(n))$ for the division plus $O(M(N) \log N)$ for the product, and then solve a problem of size $N$.
- **Fixed points, many polynomials.** When the points are known in advance, the [subproduct tree](/subproduct-tree/) and the inverses needed for the divisions can be computed once, and each polynomial then costs a smaller constant times $M(n) \log n$.
- **Roots of unity.** If $u_i = \omega^i$ for a principal $n$-th root of unity $\omega$, the problem is the discrete Fourier transform, and the [fast Fourier transform](/fast-fourier-transform/) solves it with $O(n \log n)$ operations.
- **Geometric progressions.** If $u_i = a q^i$, the identity $ij = \binom{i+j}{2} - \binom{i}{2} - \binom{j}{2}$ turns the problem into one polynomial product, so it costs $O(M(n))$ when $q$ is a unit. This is the chirp z-transform, and [Bluestein's FFT](/bluestein-fft/) is its form at roots of unity.
- **The transposed problem.** Given $c_0, \ldots, c_{n-1}$ and the points, compute the power sums $\sum_i c_i u_i^j$ for $0 \le j < n$, that is $V^T c$. By the transposition principle it has the same cost as multipoint evaluation up to a constant factor, and transposed algorithms give the fastest known constants for evaluation itself.
- **Several variables.** Evaluating a polynomial in $r$ variables at many points is much harder; for bounded $r$ over finite fields, Kedlaya and Umans gave nearly linear algorithms, which also give fast modular composition.
- **Approximate evaluation.** Over $\mathbb{R}$ or $\mathbb{C}$ with floating point numbers, the subproduct tree method is numerically unstable for general points. Methods related to the fast multipole method trade exactness for stability.

## Examples

**Horner at four points.** For $f = x^3 - 2x + 1$ at $0, 1, 2, 3$, Horner's rule gives the values $1, 0, 5, 22$, with three multiplications and three additions per point.

**The subproduct tree on the same input.** The two halves of the points have the products $m_0 = x(x - 1) = x^2 - x$ and $m_1 = (x - 2)(x - 3) = x^2 - 5x + 6$. Modulo $m_0$, $x^2 \equiv x$ and $x^3 \equiv x$, so $f \bmod m_0 = 1 - x$, whose values at $0$ and $1$ are $1$ and $0$. Modulo $m_1$, $x^2 \equiv 5x - 6$ and $x^3 \equiv 19x - 30$, so $f \bmod m_1 = 17x - 29$, whose values at $2$ and $3$ are $5$ and $22$. The values agree with Horner's rule. A script checked both computations.

**Roots of unity.** For $f = 1 + 2x + 3x^2 + 4x^3$ at the fourth roots of unity $1, i, -1, -i$ over $\mathbb{C}$, the values are $10$, $-2 - 2i$, $-2$ and $-2 + 2i$. The radix-2 FFT computes them from the two half-size polynomials $1 + 3y$ and $2 + 4y$ at $y = \pm 1$.

**A point repeated.** At the points $1, 1$ the problem is still defined and the answer is $f(1), f(1)$. The subproduct tree uses $(x - 1)^2$ and still works for evaluation, but interpolation at these points is not defined.

## Known algorithms

| algorithm | cost in ring operations | conditions |
|---|---|---|
| [Horner's rule](/horner-rule/) at each point | $n^2 - n$ multiplications and as many additions | any ring |
| [Fast multipoint evaluation](/fast-multipoint-evaluation/) with the [subproduct tree](/subproduct-tree/) | $O(M(n) \log n)$ | any ring |
| the same with FFT multiplication | $O(n \log^2 n)$ | roots of unity of suitable order in $R$ |
| [FFT](/fast-fourier-transform/) | $O(n \log n)$ | the points are the powers of a principal root of unity |
| chirp z-transform | $O(M(n))$ | the points are a geometric progression with unit ratio |
| transposed remainder tree (Bostan, Lecerf and Schost) | $O(M(n) \log n)$ with a smaller constant | any ring |

All the bounds in the table are proved. Which method is fastest for a given $n$ is observed in practice and depends on the ring and the machine: Horner's rule is the fastest for small $n$, and the size above which the subproduct tree wins must be found by measurement.

## Bounds

- **Upper bound.** $O(M(n) \log n)$ ring operations for general points, that is $O(n \log^2 n)$ with FFT multiplication, and $O(n \log^2 n \log\log n)$ over every commutative ring with the multiplication of Cantor and Kaltofen (von zur Gathen and Gerhard, Section 10.1).
- **Lower bound.** Every algorithm must read the $2n$ inputs, which gives $\Omega(n)$. Strassen showed in 1973, with his degree bound, that a straight-line program which computes the values from indeterminate coefficients and points needs $\Omega(n \log n)$ nonscalar multiplications.
- **The gap.** No algorithm with $o(M(n) \log n)$ operations is known for general points, and no lower bound larger than $\Omega(n \log n)$ is known. For points known in advance, with free preprocessing, the question is also open.

## Reductions

- **To division.** By the identity $f(u) = f \bmod (x - u)$, multipoint evaluation is a tree of divisions with remainder by the products of the points. With [fast polynomial division](/fast-polynomial-division/) each level of the tree costs $O(M(n))$, and there are $\lceil \log_2 n \rceil$ levels.
- **From multiplication.** Multiplication of polynomials of degree less than $n$ reduces to evaluation at $2n - 1$ points, $2n - 1$ products in $R$, and interpolation. This is the [evaluation-interpolation paradigm](/evaluation-interpolation-paradigm/).
- **Interpolation reduces to evaluation.** Lagrange interpolation needs the values $m'(u_i)$ of the derivative of $m = \prod (x - u_i)$, which is one multipoint evaluation, and then a linear combination that the subproduct tree computes in $O(M(n) \log n)$.
- **Transposition.** Multipoint evaluation, the product by $V$, and the power sum problem, the product by $V^T$, have the same algebraic complexity up to a constant factor, by the transposition principle for linear straight-line programs.
- **Chinese remaindering.** Multipoint evaluation is the special case of computing $f \bmod m_i$ for many moduli $m_i$, where all $m_i$ have degree 1. The same tree handles moduli of any degree, which is the first half of fast Chinese remaindering.

## Applications

- **Fast interpolation and Chinese remaindering.** Both use multipoint evaluation as a step, and both are in [fast interpolation](/fast-interpolation/).
- **Deterministic integer factoring.** The [Pollard-Strassen](/pollard-strassen/) method finds a factor of $N$ with about $N^{1/4}$ times a polylogarithmic number of operations, by evaluating a product of linear factors at many points modulo $N$.
- **Factorials modulo a prime.** [$n! \bmod p$](/factorial-modulo-prime/) can be computed in about $\sqrt{n}$ times a polylogarithmic number of operations, by grouping the product into blocks and evaluating one polynomial at many points.
- **Codes.** Encoding a [Reed-Solomon code](/reed-solomon-code/) is the evaluation of the message polynomial at the code locators, and decoding uses interpolation.
- **Modular algorithms.** Evaluation at many points is the first step of evaluation-interpolation algorithms for determinants, resultants and gcds over $F[x]$.
- **Root finding over small fields.** Over $\mathbb{F}_q$ with small $q$, evaluating $f$ at all elements finds its roots directly.

## References
