---
tag: MF7VJW
kind: problem
slug: sparse-polynomial-interpolation
name: Sparse polynomial interpolation
aliases: [sparse interpolation, black-box interpolation, sparse multivariate interpolation]
area: algebra/computer-algebra
level: advanced
summary: Recover a sparse polynomial from black-box evaluations.
prereqs: [sparse-polynomial, polynomial-interpolation, schwartz-zippel-lemma]
see_also: [zippel-sparse-interpolation, ben-or-tiwari-algorithm, prony-method, berlekamp-massey, polynomial-identity-testing, kronecker-substitution, straight-line-program, vandermonde-matrix]
sources:
  - paper: doi:10.1007/3-540-09519-5_73
    title: Richard Zippel, Probabilistic algorithms for sparse polynomials, EUROSAM 1979, Lecture Notes in Computer Science 72
    locator: pp. 216 to 226 (the probabilistic variable by variable interpolation and the zero test)
  - paper: doi:10.1016/S0747-7171(08)80018-1
    title: Richard Zippel, Interpolating polynomials from their values, Journal of Symbolic Computation 9(3), 1990
    locator: pp. 375 to 403
  - paper: doi:10.1145/62212.62241
    title: Michael Ben-Or and Prasoon Tiwari, A deterministic algorithm for sparse multivariate polynomial interpolation, STOC 1988
    locator: pp. 301 to 309
  - paper: doi:10.1007/3-540-51084-2_44
    title: Erich Kaltofen and Lakshman Yagati, Improved sparse multivariate polynomial interpolation algorithms, ISSAC 1988, Lecture Notes in Computer Science 358
    locator: pp. 467 to 474 (fast transposed Vandermonde solving and the cost of the Ben-Or and Tiwari method)
  - paper: doi:10.1016/S0747-7171(08)80015-6
    title: Erich Kaltofen and Barry M. Trager, Computing with polynomials given by black boxes for their evaluations, Journal of Symbolic Computation 9(3), 1990
    locator: pp. 301 to 320 (the black-box model, with greatest common divisors and factorization)
  - paper: doi:10.1137/0219073
    title: Dima Grigoriev, Marek Karpinski and Michael F. Singer, Fast parallel algorithms for sparse multivariate polynomial interpolation over finite fields, SIAM Journal on Computing 19(6), 1990
    locator: pp. 1059 to 1063
  - paper: doi:10.1016/S0747-7171(03)00088-9
    title: Erich Kaltofen and Wen-shin Lee, Early termination in sparse interpolation algorithms, Journal of Symbolic Computation 36(3-4), 2003
    locator: pp. 365 to 400
  - paper: doi:10.1145/345542.345629
    title: Erich Kaltofen, Wen-shin Lee and Austin A. Lobo, Early termination in Ben-Or/Tiwari sparse interpolation and a hybrid of Zippel's algorithm, ISSAC 2000
    locator: pp. 192 to 201
  - paper: doi:10.1016/0304-3975(91)90157-W
    title: Michael Clausen, Andreas Dress, Johannes Grabmeier and Marek Karpinski, On zero-testing and interpolation of k-sparse multivariate polynomials over finite fields, Theoretical Computer Science 84(2), 1991
    locator: pp. 151 to 164
  - paper: doi:10.1006/jsco.1996.0020
    title: Hirokazu Murao and Tetsuro Fujise, Modular algorithm for sparse multivariate polynomial interpolation and its parallel implementation, Journal of Symbolic Computation 21(4-6), 1996
    locator: pp. 377 to 396 (the Ben-Or and Tiwari method over Z/pZ with discrete logarithms)
  - paper: doi:10.1016/j.tcs.2009.03.030
    title: Sanchit Garg and Éric Schost, Interpolation of polynomials given by straight-line programs, Theoretical Computer Science 410(27-29), 2009
    locator: pp. 2659 to 2662
  - paper: doi:10.1016/j.jsc.2015.11.005
    title: Andrew Arnold, Mark Giesbrecht and Daniel S. Roche, Faster sparse multivariate polynomial interpolation of straight-line programs, Journal of Symbolic Computation 75, 2016
    locator: pp. 4 to 24
  - paper: doi:10.1016/j.jsc.2008.11.003
    title: Mark Giesbrecht, George Labahn and Wen-shin Lee, Symbolic-numeric sparse interpolation of multivariate polynomials, Journal of Symbolic Computation 44(8), 2009
    locator: pp. 943 to 959
---

## In plain words

Sometimes a polynomial is known only through a procedure that computes its value at any point we choose. Examples are a determinant of a matrix whose entries contain variables, or the result of a long computation. The polynomial can have many variables and a high degree, but only a few terms. Writing it out in full, with every possible term, would take far too long.

Sparse interpolation asks for the few terms directly, from as few evaluations as possible. A good method uses a number of evaluations that depends on the number of terms and the number of variables, and not on the number of all possible terms. Such methods choose the evaluation points with care: random points, so that unlucky cancellations are improbable, or powers of fixed numbers, so that the values form a pattern that reveals the exponents.

## Definition

**Notation.** $K$ is a field, and $K[x_1, \ldots, x_n]$ is the polynomial ring. A polynomial is written $f = \sum_{j=1}^{t} c_j x^{e_j}$ with $c_j \in K \setminus \{0\}$ and distinct exponent vectors $e_j \in \mathbb{N}^n$, so $t$ is the number of terms. $d$ is a degree bound: either on each partial degree, $\deg_{x_i} f \le d$, or on the total degree, and each statement says which. $M(d)$ is the cost of multiplying two univariate polynomials of degree $d$ in field operations.

**Input.**

- A *black box* for $f$: a procedure that, given $a \in L^n$ for a field $L \supseteq K$ (often $L = K$, or a finite extension of $K$ when $K$ is a small finite field), returns $f(a)$. One call is a *probe*.
- The number $n$ of variables and a degree bound $d$.
- Usually a term bound $T \ge t$. Methods with *early termination* do not need $T$.

**Output.** The list of pairs $(c_j, e_j)$, $j = 1, \ldots, t$.

**Cost.** Three measures are used, and a method is judged on all of them:

- the number of probes;
- the number of field operations in $K$ (or $L$) besides the probes;
- for $K = \mathbb{Q}$, the bit operations, which depend on the size of the values $f(a)$, and these grow with $d$ and with the coordinates of $a$.

The output has size about $t (n \log d + \text{size of a coefficient})$, so the target is a cost polynomial in $n$, $t$ and $\log d$, or at least polynomial in $n$, $t$ and $d$. The dense size $(d + 1)^n$ is exponential in $n$.

**A necessary condition.** The answer must be unique given the data. Over a finite field $\mathbb{F}_q$ this needs $d < q - 1$ for each variable, or points in an extension field: $x^{q-1}$ and $1$ give the same value at every nonzero point of $\mathbb{F}_q$.

## Variants

- **Probabilistic or deterministic.** Monte Carlo methods use random points and fail with a probability that is bounded by a ratio of the form (polynomial in $n$, $d$, $T$) divided by the size of the sample set. Deterministic methods use fixed points, such as powers of the first $n$ primes.
- **Black box or straight-line program.** A [straight-line program](/straight-line-program/) of length $L$ can be evaluated in any ring, not only in $K$. For example it can be evaluated modulo $x^p - 1$, which maps every exponent to its residue modulo $p$. This extra power gives methods with cost polynomial in $\log d$, which a pure black box over $\mathbb{Q}$ cannot give without large numbers.
- **Univariate or multivariate.** [Kronecker substitution](/kronecker-substitution/) $x_i \mapsto z^{(d+1)^{i-1}}$ turns $n$ variables with partial degrees at most $d$ into one variable of degree less than $(d+1)^n$, with the same $t$ terms. So a univariate method whose cost is polynomial in $t$ and $\log(\text{degree})$ solves the multivariate problem in cost polynomial in $t$, $n$ and $\log d$.
- **Known or unknown term bound.** With early termination, the method stops when its output stops changing as more probes arrive, and it uses about $2t$ probes plus a few extra, without knowing $T$.
- **Exact or numerical.** Over $\mathbb{C}$ with floating point values, the problem becomes a structured eigenvalue problem, close to the [Prony method](/prony-method/), and the main question is the conditioning.
- **Other bases.** Sparsity in a Chebyshev, Pochhammer or shifted power basis, or for rational functions given by a black box.

## Examples

**Why the term bound matters.** For $n = 1$ and one probe at $x = 2$, the polynomials $x^2$ and $2x$ both give $4$. Both have one term. In general, for any $2t - 1$ points and any $2t$ monomials, the linear system "a combination of these monomials vanishes at the points" has $2t - 1$ equations and $2t$ unknowns, so it has a nonzero solution $g$. Split the $2t$ terms of $g$ into two halves $g = g_1 - g_2$; then $g_1 \ne g_2$ have at most $t$ terms each and agree at all the points. So a method that fixes its points in advance needs at least $2t$ probes, and the Ben-Or and Tiwari method below uses exactly $2t$.

**Ben-Or and Tiwari on a small input.** Let $K = \mathbb{Q}$, $n = 2$, $T = 3$ and $f = 3x^2y + 5xy^3 - 2$, unknown to the algorithm.

1. Probe at $(2^i, 3^i)$ for $i = 0, \ldots, 5$. A term $c\, x^{u} y^{v}$ gives $c\, m^i$ with $m = 2^u 3^v$, so $a_i = f(2^i, 3^i) = 3 \cdot 12^i + 5 \cdot 54^i - 2 \cdot 1^i$. The values are $a = (6, 304, 15010, 792502, 42577486, 2296571614)$.
2. The sequence $a_i$ satisfies a linear recurrence whose characteristic polynomial has the monomial values as roots. The [Berlekamp-Massey](/berlekamp-massey/) algorithm on the six values gives $\Lambda(z) = z^3 - 67 z^2 + 714 z - 648$, that is, $a_{i+3} = 67 a_{i+2} - 714 a_{i+1} + 648 a_i$. For $i = 0$: $67 \cdot 15010 - 714 \cdot 304 + 648 \cdot 6 = 792502$.
3. The integer roots of $\Lambda$ are $1$, $12$ and $54$. By unique factorization, $12 = 2^2 \cdot 3$ gives $x^2 y$, $54 = 2 \cdot 3^3$ gives $x y^3$, and $1$ gives the constant term.
4. The coefficients solve the transposed [Vandermonde](/vandermonde-matrix/) system $\sum_j c_j m_j^i = a_i$ for $i = 0, 1, 2$, with $m = (12, 54, 1)$. The solution is $c = (3, 5, -2)$, which gives $f$ back.

**Collision over a finite field.** Over $\mathbb{F}_7$, $3^6 = 1$, and $x^6$ takes the value $1$ at every nonzero point. So with $d = 6$ the monomials $x^6$ and $1$ cannot be told apart from probes in $\mathbb{F}_7$, and probes in an extension field are needed.

## Known algorithms

| Method | Probes | Other cost | Kind |
|---|---|---|---|
| Dense interpolation, variable by variable | $(d+1)^n$ | $O(n (d+1)^{n-1} M(d) \log d)$ field operations | deterministic |
| [Zippel](/zippel-sparse-interpolation/) (1979, 1990) | $O(n d T)$ | $O(n d T^2)$ field operations for the Vandermonde systems | Monte Carlo |
| [Ben-Or and Tiwari](/ben-or-tiwari-algorithm/) (1988) | $2T$ | Berlekamp-Massey, root finding over $\mathbb{Z}$, one transposed Vandermonde solve | deterministic over $\mathbb{Q}$ |
| Kaltofen and Lakshman (1988) | $2T$ | $O(M(T) \log T)$ operations for the recurrence and the Vandermonde step | deterministic over $\mathbb{Q}$ |
| Modular Ben-Or and Tiwari (Murao and Fujise 1996, and others) | $2T$ | discrete logarithms in $\mathbb{F}_p$ with $p - 1$ smooth, after Kronecker substitution | deterministic per prime |
| Early termination (Kaltofen, Lee and Lobo 2000; Kaltofen and Lee 2003) | $2t + O(1)$ | as Ben-Or and Tiwari, or as Zippel in the hybrid | Monte Carlo |
| Straight-line programs (Garg and Schost 2009; Arnold, Giesbrecht and Roche 2016) | evaluations modulo $x^p - 1$ | polynomial in $L$, $t$, $n$ and $\log d$ | deterministic or Monte Carlo |

**Zippel's method.** It introduces the variables one at a time. When $f(x_1, \ldots, x_{k}, a_{k+1}, \ldots, a_n)$ is known, it assumes that its support in $x_1, \ldots, x_{k}$ is the support of the next stage as well, for random $a$. It then finds the coefficients for $d + 1$ values of $x_{k+1}$ by solving Vandermonde systems of size at most $T$, and it interpolates each coefficient in $x_{k+1}$ by dense univariate interpolation. The assumption fails only if a random choice makes a coefficient vanish, which the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) bounds.

**Ben-Or and Tiwari's method.** It probes at powers of a point whose coordinates are pairwise coprime integers (the first $n$ primes), so that each monomial value $m_j = p_1^{e_{j1}} \cdots p_n^{e_{jn}}$ encodes its exponent vector. It is the exact form of [Prony's method](/prony-method/), and step 2 is the same computation as in decoding [Reed-Solomon codes](/reed-solomon-decoding/). Its weakness over $\mathbb{Q}$ is the size of the numbers: $m_j$ can be as large as $p_n^{D}$ for total degree $D$, so the values $a_i$ have size $O(T D \log p_n)$ digits, and the bit cost grows with $D$ and $T$ together. The modular forms avoid this by working in $\mathbb{F}_p$ and reading $e_j$ from a discrete logarithm of $m_j$, which is cheap with the [Pohlig-Hellman](/pohlig-hellman/) method when $p - 1$ has only small prime factors.

## Bounds

- **Probes.** For any fixed set of fewer than $2t$ points there are two different polynomials with at most $t$ terms that agree on it (Examples). So $2t$ probes are needed by methods that choose all points in advance, and Ben-Or and Tiwari attain this. This is a proved bound.
- **Zero testing.** A nonzero $f$ of total degree $D$ vanishes at a random point of $S^n$ with probability at most $D / |S|$ (Schwartz-Zippel). A nonzero $f$ with at most $T$ terms over $\mathbb{Q}$ does not vanish at all of the points $(p_1^i, \ldots, p_n^i)$, $i = 0, \ldots, T - 1$, because the matrix $(m_j^i)$ is Vandermonde with distinct $m_j$. So zero testing with a term bound is deterministic with $T$ probes.
- **Field size.** Over a small finite field $\mathbb{F}_q$ the probes may have to be taken in an extension field. Grigoriev, Karpinski and Singer (1990) and Clausen, Dress, Grabmeier and Karpinski (1991) give algorithms and bounds for this case.
- **Bit cost over $\mathbb{Q}$.** For a pure black box the values $f(a)$ themselves can have size proportional to $d$, so cost polynomial in $\log d$ is not possible over $\mathbb{Q}$ without reducing modulo primes. The polynomial bounds in $\log d$ above are for straight-line programs or for modular black boxes.
- **In practice.** Zippel's method is the method of choice in systems for sparse GCD and for polynomial system solving, because its probes have small values. The Ben-Or and Tiwari method uses far fewer probes and is preferred when probes are expensive, for example in parallel and distributed settings. These are observations, not proved bounds.

## Reductions

- **Multivariate to univariate.** By Kronecker substitution, as in Variants, at the cost of degree $(d+1)^n$. Randomized substitutions $x_i \mapsto z^{s_i}$ with small $s_i$ keep the degree lower, at the risk of collisions between terms.
- **From interpolation to zero testing.** A sparse interpolation algorithm with a term bound tests whether $f = 0$; this is [polynomial identity testing](/polynomial-identity-testing/) for sparse polynomials. Conversely, Zippel's method uses zero tests to decide when each stage is complete.
- **Equivalent to recurrence finding.** The Ben-Or and Tiwari step is: given $2T$ terms of a sequence that satisfies a linear recurrence of order $t \le T$, find the recurrence and its roots. This is the problem that Prony, Berlekamp-Massey and BCH or Reed-Solomon decoding solve.
- **Black-box algebra on top.** Kaltofen and Trager (1990) compute GCDs and factors of polynomials given by black boxes, and return black boxes. A sparse interpolation step at the end turns such a black box into the list of terms.

## Applications

- **Sparse GCD and factorization.** Zippel introduced the method for the GCD of sparse multivariate polynomials, where a dense modular method would need far too many images. See [polynomial GCD](/polynomial-gcd/).
- **Determinants and resultants with variables.** A determinant of a matrix with polynomial entries is easy to evaluate at points by Gaussian elimination but has a sparse expanded form; interpolation recovers it without symbolic elimination.
- **Black-box linear algebra.** Wiedemann-style methods on a [black-box matrix](/black-box-matrix/) produce values that are then interpolated.
- **Polynomial systems.** Modern solvers compute Gröbner bases or triangular sets of a parametric system at many specialized parameter values and recover the parametric answer by sparse rational interpolation.
- **Signal processing and exponential sums.** The same step recovers frequencies and amplitudes of a sum of exponentials from samples, as in the Prony method and in the [sparse Fourier transform](/sparse-fourier-transform/).

## References
