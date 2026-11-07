---
tag: 97XDKH
kind: problem
slug: polynomial-evaluation
name: Polynomial evaluation
aliases:
- evaluating a polynomial at a point
- polynomial evaluation at a point
area: algebra/polynomial-arithmetic
level: intro
summary: Given coefficients and x, compute f(x) with few arithmetic operations.
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the polynomial f}
  time: {worst: Θ(n)}
prereqs: [polynomial-ring, polynomial-degree]
see_also: [horner-rule, horners-rule-optimality, estrin-scheme, paterson-stockmeyer-algorithm, multipoint-evaluation, polynomial-remainder-theorem, discrete-fourier-transform, polynomial-composition]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of Polynomials (Horner's rule, adaptation of coefficients, and the lower bounds of Ostrowski, Motzkin and Pan)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.2, Evaluation and interpolation, and Section 10.1, Fast multipoint evaluation (p. 295)
  - paper: "doi:10.1137/0202007"
    title: Michael S. Paterson and Larry J. Stockmeyer, On the number of nonscalar multiplications necessary to evaluate polynomials, SIAM Journal on Computing 2(1), 1973
    locator: pp. 60 to 66
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 5, Polynomials (rounding error analysis of Horner's method)
---

Polynomial evaluation is the problem of computing the value $f(u)$ of a polynomial $f = a_0 + a_1 x + \cdots + a_n x^n$, given by its coefficients, at a point $u$. [Horner's rule](/horner-rule/) solves it with $n$ multiplications and $n$ additions, and no method that treats the coefficients as unknown inputs can do with fewer. The problem has many forms: the point can be a matrix or a polynomial, the coefficients can be fixed in advance, or there can be many points. Evaluation is the inner loop of root finding, hashing, coding and the [evaluation-interpolation paradigm](/evaluation-interpolation-paradigm/).

## In plain words

You have the list of numbers that defines a polynomial, and you want its value at one number. The direct way computes each power of the number, multiplies it by its coefficient, and adds the results. That takes about twice as many multiplications as needed.

The usual way starts from the top coefficient. Multiply by the number, add the next coefficient, and repeat until the last one. Each coefficient costs one multiplication and one addition, and it is known that you cannot do better in general.

The problem becomes harder and more interesting when the number is replaced by something expensive to multiply, such as a matrix, or when you need the value at many numbers at once.

## Definition

**Input.** A commutative ring $R$, the coefficients $a_0, \ldots, a_n \in R$ of $f = \sum_{i=0}^{n} a_i x^i$, and a point $u$. The point is in $R$, or more generally in a ring $S$ that contains $R$ in its center, for example a matrix ring over $R$ or the polynomial ring $R[y]$.

**Output.** $f(u) = \sum_{i=0}^{n} a_i u^i \in S$.

**Cost.** Operations in $R$ (or in $S$) at unit cost, as in [polynomial ring](/polynomial-ring/). Since the operations differ in cost when $S$ is large, the count separates additions, multiplications by elements of $R$ (scalar multiplications) and products of two elements of $S$ (nonscalar multiplications). Over $\mathbb{R}$ with floating-point numbers, the accuracy of the result is a second measure.

## Variants

- **One point, general coefficients.** The basic problem. [Horner's rule](/horner-rule/) is optimal.
- **Preconditioning.** The coefficients are fixed and known in advance, and only $u$ is the input; a one-time computation on the coefficients is free. Then about $n/2$ multiplications suffice (Knuth, Section 4.6.4, adaptation of coefficients).
- **Point in an algebra.** $u$ is a matrix, a power series or an element of $R[y]/(g)$, where a product of two elements of $S$ is much more costly than a scalar operation. The [Paterson-Stockmeyer algorithm](/paterson-stockmeyer-algorithm/) uses $O(\sqrt n)$ nonscalar multiplications. With $S = R[y]$, the problem is [polynomial composition](/polynomial-composition/).
- **Many points.** Evaluate $f$ at $u_1, \ldots, u_k$. With $k = n + 1$ points this is [multipoint evaluation](/multipoint-evaluation/), in $O(M(n) \log n)$ operations by a [subproduct tree](/subproduct-tree/); at the powers of a root of unity it is the [discrete Fourier transform](/discrete-fourier-transform/).
- **Value and derivatives.** Compute $f(u), f'(u), \ldots$ together, as Newton's method needs. Repeated synthetic division gives the Taylor coefficients at $u$.
- **Parallel evaluation.** Minimize the depth of the computation. The [Estrin scheme](/estrin-scheme/) has depth $O(\log n)$.
- **Sparse polynomials.** $f$ has $t$ nonzero terms of large degree. Evaluate each term by [binary exponentiation](/binary-exponentiation/), in $O(t \log n)$ operations.

## Examples

- **Horner over $\mathbb{Z}$.** For $f = 2x^4 + 3x^3 - x + 5$ at $u = 2$: $2 \cdot 2 + 3 = 7$, $7 \cdot 2 + 0 = 14$, $14 \cdot 2 - 1 = 27$, $27 \cdot 2 + 5 = 59$. That is $4$ multiplications and $4$ additions. The direct method computes $2^2, 2^3, 2^4$ ($3$ multiplications), then $2 \cdot 16$, $3 \cdot 8$, $-1 \cdot 2$ ($3$ more), and adds.
- **A root modulo 7.** The same $f$ at $u = 3$ gives $245 = 5 \cdot 7^2$, so $f(3) = 0$ in $\mathbb{F}_7$, and $x - 3$ divides $f$ over $\mathbb{F}_7$ by the [remainder theorem](/polynomial-remainder-theorem/).
- **All points of a cyclic group.** Over $\mathbb{F}_5$, $2$ has order $4$, with powers $1, 2, 4, 3$. The same $f$, reduced modulo $5$, takes the values $4, 4, 0, 0$ at these points. These four values are the length 4 [discrete Fourier transform](/discrete-fourier-transform/) of its coefficient vector over $\mathbb{F}_5$.
- **A matrix point.** For $f = x^2 + 1$ and the rotation matrix $u = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$ over $\mathbb{Z}$, $u^2 = -I$, so $f(u) = 0$. Here $1$ means the identity matrix, and $f(u)$ costs one matrix product.
- **A polynomial point.** For $f = x^2 + 1$ and $u = y^3 - y \in \mathbb{Z}[y]$, $f(u) = y^6 - 2y^4 + y^2 + 1$. This is composition.

## Known algorithms

| algorithm | multiplications | additions | notes |
|---|---|---|---|
| direct, power by power | $2n - 1$ | $n$ | computes $u^2, \ldots, u^n$ first |
| [Horner's rule](/horner-rule/) | $n$ | $n$ | optimal for general coefficients; also gives $f/(x - u)$ |
| [Estrin scheme](/estrin-scheme/) | $O(n)$ | $n$ | depth $O(\log n)$; suits SIMD and parallel hardware |
| adaptation of coefficients (preconditioning) | about $n/2$ | about $n$ | the coefficients are fixed; Knuth, Section 4.6.4 |
| [Paterson-Stockmeyer](/paterson-stockmeyer-algorithm/) | $O(\sqrt n)$ nonscalar, $O(n)$ scalar | $O(n)$ | for $u$ in an algebra, such as matrices |
| [multipoint evaluation](/multipoint-evaluation/) | $O(M(n) \log n)$ for $n + 1$ points | | subproduct tree; von zur Gathen and Gerhard, Section 10.1 |

The operation counts in the table are proved. Which method is fastest on a given machine is observed in practice: on modern processors, Horner's rule has a long chain of dependent operations, and the Estrin scheme or a split into even and odd parts can run faster for moderate $n$ even though it does more work.

**Accuracy.** In floating-point arithmetic, Horner's rule is backward stable: the computed value is the exact value of a polynomial whose coefficients differ from the $a_i$ by a relative error of at most about $2n$ units of rounding (Higham, Chapter 5). The forward error can still be large near a root of $f$ or when the terms $a_i u^i$ cancel.

## Bounds

- **Lower bound for general coefficients.** Every algorithm that takes $a_0, \ldots, a_n$ and $u$ as inputs needs at least $n$ additions or subtractions and at least $n$ multiplications or divisions. Ostrowski (1954) asked whether Horner's rule is optimal and proved it for small $n$, and Pan (1966) proved the bound on multiplications for all $n$. Knuth, Section 4.6.4, proves both bounds, which make Horner's rule optimal; see [optimality of Horner's rule](/horners-rule-optimality/).
- **With preconditioning.** About $n/2$ multiplications are necessary and sufficient for most coefficient vectors; Knuth, Section 4.6.4, gives the schemes and the lower bound.
- **Nonscalar multiplications.** For $u$ in an algebra, Paterson and Stockmeyer (1973) proved that $\Theta(\sqrt n)$ nonscalar multiplications are necessary and sufficient for most polynomials.
- **Trivial bound.** $\Omega(n)$ operations in any model in which the output must depend on every coefficient.

## Reductions

- **Evaluation is a remainder.** $f(u) = f \operatorname{rem} (x - u)$, by the [polynomial remainder theorem](/polynomial-remainder-theorem/). So evaluation reduces to [division](/polynomial-division/) by a linear polynomial, and Horner's rule is long division by $x - u$.
- **Many points reduce to remainders in a tree.** $f \operatorname{rem} \prod_i (x - u_i)$ is computed down a [subproduct tree](/subproduct-tree/) until the leaves $x - u_i$.
- **At roots of unity it is the DFT.** Evaluating at $1, \omega, \ldots, \omega^{n-1}$ for a primitive $n$-th root of unity $\omega$ is the [discrete Fourier transform](/discrete-fourier-transform/), computed by the [fast Fourier transform](/fast-fourier-transform/) in $O(n \log n)$ operations.
- **Composition is evaluation at a polynomial.** $f(g)$ is $f$ evaluated at $u = g \in R[x]$.

## Applications

- [Root finding](/polynomial-root-finding/): [Newton's method](/newton-raphson-method/) needs $f(u)$ and $f'(u)$ at each step, and synthetic division [deflates](/polynomial-deflation/) a root once it is found.
- Hashing: the [polynomial rolling hash](/polynomial-rolling-hash/) of a string is a polynomial evaluated at a fixed base modulo a prime, as in [Rabin-Karp](/rabin-karp/) search.
- Identity testing: by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), evaluating at a random point tests whether a polynomial given by a formula is zero, the base of [polynomial identity testing](/polynomial-identity-testing/).
- Coding and secret sharing: [Reed-Solomon codes](/reed-solomon-code/) encode a message as the values of a polynomial, and [Shamir secret sharing](/shamir-secret-sharing/) hands out values of a random polynomial.
- [Radix conversion](/radix-conversion/): a number with digits $d_0, \ldots, d_n$ in base $b$ is $f(b)$ for $f = \sum d_i x^i$, and Horner's rule converts it.
- The [evaluation-interpolation paradigm](/evaluation-interpolation-paradigm/) for multiplication and for modular algorithms.

## References
