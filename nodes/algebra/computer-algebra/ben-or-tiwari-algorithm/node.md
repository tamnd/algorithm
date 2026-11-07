---
tag: RHYB1V
kind: algorithm
slug: ben-or-tiwari-algorithm
name: Ben-Or and Tiwari algorithm
aliases:
- Ben-Or-Tiwari interpolation
- Ben-Or-Tiwari sparse interpolation
area: algebra/computer-algebra
level: research
summary: Recovers a sparse polynomial from 2t evaluations at geometric points via Prony-style linear recurrences.
model: blum-shub-smale-machine
complexity:
  vars: {T: the given bound on the number of terms, t: the actual number of terms}
  time: {worst: O(T^2), best: O(T^2)}
  space: {extra: O(T)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [berlekamp-massey, vandermonde-matrix, polynomial-interpolation]
see_also: [sparse-polynomial-interpolation, prony-method, zippel-sparse-interpolation, straight-line-program, reed-solomon-decoding, polynomial-identity-testing, hensel-lifting, schwartz-zippel-lemma]
sources:
  - paper: doi:10.1145/62212.62241
    title: Michael Ben-Or and Prasoon Tiwari, A deterministic algorithm for sparse multivariate polynomial interpolation, Proceedings of the 20th ACM Symposium on Theory of Computing (STOC), 301-309, 1988
    locator: the evaluation at powers of primes, the reduction to a linear recurrence, the use of the Berlekamp-Massey step and the transposed Vandermonde system
  - paper: "Erich Kaltofen and Lakshman Yagati, Improved sparse multivariate polynomial interpolation algorithms, Proceedings of ISSAC 1988, Lecture Notes in Computer Science 358, Springer, 1989, pages 467 to 474"
    locator: the solution of the transposed Vandermonde system in O(t^2) operations and the fast versions of the linear algebra steps
  - paper: "Erich Kaltofen and Wen-shin Lee, Early termination in sparse interpolation algorithms, Journal of Symbolic Computation 36(3-4), 365-400, 2003"
    locator: the version that does not need the bound T and stops when the recurrence stabilizes at a random point
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.9 (rational function reconstruction) and Section 12.3 (minimal polynomials of linearly recurrent sequences and Wiedemann's algorithm)
  - paper: "Gaspard de Prony, Essai expérimental et analytique, Journal de l'École Polytechnique 1(22), 24-76, 1795"
    locator: the method of recovering a sum of exponentials from equally spaced samples through a linear recurrence
---

The Ben-Or and Tiwari algorithm reconstructs a multivariate polynomial with at most $T$ terms from its values at the $2T$ points $(p_1^i, \ldots, p_n^i)$, $i = 0, \ldots, 2T - 1$, where $p_1, \ldots, p_n$ are distinct primes. The polynomial is only available as a black box that returns values. The values form a sequence that satisfies a linear recurrence whose characteristic polynomial has the monomial values $p_1^{e_1} \cdots p_n^{e_n}$ as roots. The algorithm finds the recurrence with [Berlekamp-Massey](/berlekamp-massey/), finds the roots, reads the exponents off their prime factorizations, and gets the coefficients from a transposed [Vandermonde](/vandermonde-matrix/) system. Ben-Or and Tiwari published it in 1988. It was the first deterministic algorithm whose number of evaluations depends on the number of terms and not on the degree, and it is the template for [sparse interpolation](/sparse-polynomial-interpolation/) in computer algebra.

## In plain words

Some polynomials have huge degree but only a few terms. Classical interpolation would need as many values as there are possible terms, which can be astronomically many. This method needs only twice the number of terms.

It feeds the unknown polynomial very special inputs: powers of 2 for the first variable, powers of 3 for the second, powers of 5 for the third, and so on. Each term then turns into a fixed number raised to the step number. A short calculation finds those fixed numbers. Each one is a product of small primes, and the count of each prime in it tells the exponent of the matching variable. A last small system of equations gives the coefficients.

## The problem

Let $K = \mathbb{Q}$, a field of characteristic 0, and $K[x_1, \ldots, x_n]$ the polynomial ring. Write $x^e = x_1^{e_1} \cdots x_n^{e_n}$ for $e \in \mathbb{N}^n$. The unknown polynomial is

$$f = \sum_{j=1}^{t} c_j x^{e_j}, \qquad c_j \in K \setminus \{0\}, \quad e_j \text{ distinct},$$

with $t$ terms and total degree at most $d$. The algorithm does not use a monomial order; for display, the terms are listed in lex order with $x_1 > \cdots > x_n$, and $\operatorname{LT}$, $\operatorname{LM}$ and $\operatorname{LC}$ refer to that order.

**Input:** the number of variables $n$, a bound $T \ge t$, and a black box that returns $f(a)$ for any $a \in K^n$.
**Output:** the list of pairs $(c_j, e_j)$.

The cost is counted in two parts: black-box probes, and operations in $K$. Because the evaluation points are large integers, the bit size of the numbers matters as well, and the [complexity](#complexity) section gives it. $M(d)$ denotes the cost of multiplying two polynomials of degree $d$ over $K$.

## The algorithm

Let $p_1 < \cdots < p_n$ be the first $n$ primes and $m_j = p_1^{e_{j1}} \cdots p_n^{e_{jn}}$ the value of $x^{e_j}$ at $(p_1, \ldots, p_n)$. Then

$$a_i = f(p_1^i, \ldots, p_n^i) = \sum_{j=1}^{t} c_j m_j^i .$$

Let $\Lambda(z) = \prod_{j=1}^{t} (z - m_j) = z^t + \lambda_{t-1} z^{t-1} + \cdots + \lambda_0$. For every $s \ge 0$, $\sum_{k=0}^{t} \lambda_k a_{s+k} = \sum_j c_j m_j^s \Lambda(m_j) = 0$, with $\lambda_t = 1$. So $(a_i)$ is a linear recurrent sequence with characteristic polynomial $\Lambda$.

```pseudo id=main
BEN-OR-TIWARI(f, n, T)               ▷ f a black box with at most T terms
L1  p_1, ..., p_n ← the first n primes
L2  a_i ← f(p_1^i, ..., p_n^i) for i = 0, ..., 2T - 1
L3  Λ ← minimal polynomial of (a_0, ..., a_{2T-1}) by Berlekamp-Massey; t ← deg Λ
L4  if t = 0 then return the zero polynomial
L5  m_1, ..., m_t ← the integer roots of Λ
L6  e_j ← the exponent of p_k in m_j, for k = 1, ..., n and j = 1, ..., t
L7  solve c_1 m_1^i + ... + c_t m_t^i = a_i for i = 0, ..., t - 1
L8  return the sum of c_j x^(e_j)
```

Line L3 returns the connection polynomial $C(z) = 1 + \lambda_{t-1} z + \cdots + \lambda_0 z^t$ of the shortest recurrence; $\Lambda$ is its reversal. Line L5 finds the roots of a polynomial that is known to split over $\mathbb{Z}$ with distinct roots: the implementation finds the roots modulo a small prime $q$ for which $\Lambda$ has $t$ distinct roots, and lifts each one by Newton iteration modulo $q^{2^k}$ until the modulus exceeds twice Cauchy's root bound. Line L7 is solved in $O(t^2)$ operations with the identity that comes from $\Lambda_j(z) = \Lambda(z)/(z - m_j) = \sum_i q_{ji} z^i$:

$$\sum_{i=0}^{t-1} q_{ji} a_i = \sum_k c_k \Lambda_j(m_k) = c_j \Lambda'(m_j).$$

## Example

Let $f = 3x^2y - 2y^3 + 5 \in \mathbb{Q}[x, y]$, so $n = 2$, and take $T = 3$. The points are $(2^i, 3^i)$. The monomial values are $m = 4 \cdot 3 = 12$ for $x^2 y$, $27$ for $y^3$ and $1$ for the constant. The trace, from the implementation:

| step | line | result |
|---|---|---|
| 1 | L2 | $a = (6, -13, -1021, -34177, -1000669, -27951313)$ from the points $(1,1), (2,3), (4,9), (8,27), (16,81), (32,243)$ |
| 2 | L3 | the recurrence length grows $1, 1, 2, 2, 3, 3$ over the prefixes; the final connection polynomial is $1 - 40z + 363z^2 - 324z^3$ |
| 3 | L3 | $\Lambda(z) = z^3 - 40z^2 + 363z - 324$, $t = 3$ |
| 4 | L5 | roots $1, 12, 27$ |
| 5 | L6 | $1 \mapsto (0, 0)$, $12 = 2^2 \cdot 3 \mapsto (2, 1)$, $27 = 3^3 \mapsto (0, 3)$ |
| 6 | L7 | $c_1 + c_2 + c_3 = 6$, $c_1 + 12c_2 + 27c_3 = -13$, $c_1 + 144c_2 + 729c_3 = -1021$ give $c = (5, 3, -2)$ |

The output is $3x^2y - 2y^3 + 5$. One can check the recurrence by hand: $40 a_2 - 363 a_1 + 324 a_0 = -40840 + 4719 + 1944 = -34177 = a_3$.

## Correctness

The full proof is in the correctness file. The $m_j$ are distinct because the exponent vectors are distinct and factorization into primes is unique. The Hankel matrix $H = (a_{i+k})_{0 \le i, k < t}$ factors as $V^{\mathsf T} \operatorname{diag}(c) V$ with the Vandermonde matrix $V = (m_j^k)$, so it is nonsingular and no recurrence of order less than $t$ holds. Hence $\Lambda$ is the minimal polynomial of the sequence, and Berlekamp-Massey finds it from $2t \le 2T$ terms, since it returns the unique shortest recurrence of length $L$ whenever at least $2L$ terms are given. Its roots are the $m_j$, which give the exponents. The system of line L7 has the nonsingular matrix $V^{\mathsf T}$, so the coefficients are unique.

## Complexity

- **Probes:** exactly $2T$, proved. No method with fixed points can do better when $d \ge 2T - 1$: for any $2T - 1$ points in $K$, the linear system for the coefficients of a polynomial supported on $1, x, \ldots, x^{2T-1}$ that vanishes at them has a nonzero solution, and splitting that solution into two halves of $T$ terms gives two different $T$-sparse polynomials with the same values.
- **Operations in $K$:** $O(T^2)$ for Berlekamp-Massey and $O(t^2)$ for the transposed Vandermonde system with the identity above, proved. With fast polynomial arithmetic, both drop to $O(M(T) \log T)$, the first by the half-gcd form of Berlekamp-Massey and the second by Kaltofen and Lakshman's method.
- **Root finding:** $\Lambda$ splits into linear factors over $\mathbb{Z}$, so the roots can be found in time polynomial in $t$ and the bit size of $\Lambda$, for example by $q$-adic lifting as in the implementation, or Loos's method used by Ben-Or and Tiwari.
- **Bit size:** $|m_j| \le p_n^d$, so $a_i$ has $O(i\, d \log p_n)$ digits plus the size of the coefficients, and the numbers in the computation have $O(T d \log n)$ digits since $p_n = O(n \log n)$. The total bit complexity is polynomial in $n$, $T$, $d$ and the coefficient size, proved; the large numbers are the main practical cost, observed.
- **Space:** $O(T)$ elements of $K$, of the sizes above, plus the $O(t)$ roots.

## Properties

- **Deterministic and nonadaptive.** The evaluation points do not depend on $f$ or on earlier answers, so the $2T$ probes can be made in parallel.
- **Degree independent.** The number of probes does not depend on $d$ or $n$; only the bit sizes grow with $d$.
- **Exact.** All arithmetic is in $\mathbb{Q}$; the coefficients and exponents are recovered exactly.
- **Needs a term bound.** Without $T$, a wrong guess gives a wrong answer with no warning, unless an extra check is made.

## Variants and improvements

- **Early termination** (Kaltofen and Lee 2003). Evaluate at powers of a random point and stop as soon as the recurrence found by Berlekamp-Massey stops changing; with high probability this happens after $2t + 1$ probes, without knowing $T$.
- **Modular versions.** Work over $\mathbb{Z}/p\mathbb{Z}$ with a generator $\omega$ and evaluate at $(\omega^{i}, \omega^{i r_2}, \ldots)$ for a packing of exponents in base $d + 1$, so that each $m_j$ is a power of $\omega$. The exponents are then discrete logarithms, cheap when $p - 1$ has only small prime factors. This avoids the growth of numbers and needs $p > (d + 1)^n$.
- **Coefficient recovery by fast algorithms.** Kaltofen and Lakshman (1988) solve the transposed Vandermonde system in $O(M(t) \log t)$ operations.
- **Zippel's algorithm** is a probabilistic alternative that interpolates one variable at a time and needs $O(n d t)$ probes; it works over small fields where Ben-Or and Tiwari's points are not available. See [Zippel's algorithm](/zippel-sparse-interpolation/).
- **Numerical sparse interpolation.** Over $\mathbb{C}$, evaluate at powers of roots of unity of different orders, to keep the Vandermonde system well conditioned (Giesbrecht, Labahn and Lee 2009). This is close to [Prony's method](/prony-method/).
- **Supersparse polynomials.** When $d$ is huge, the modular versions need very large primes; newer methods reduce the exponents modulo several small primes and combine them.

## When to use it

Use it when $f$ is given by a black box or a [straight-line program](/straight-line-program/), the number of terms is much smaller than the number of possible monomials, and exact rational arithmetic is acceptable: for example, to recover the result of a determinant or a resultant with symbolic entries from its values. For a dense polynomial, ordinary interpolation is cheaper. When the values must be computed modulo a prime, use a modular variant or Zippel's algorithm. When no term bound is known, use early termination.

## Pitfalls

- **A wrong term bound.** If $T < t$, Berlekamp-Massey still returns a polynomial, and its roots need not be integers or products of the chosen primes. Check the result at one extra point; the implementation raises an error when a root does not factor over $p_1, \ldots, p_n$.
- **Number growth.** The value $a_{2T-1}$ has about $2T d \log_2 p_n$ bits. For large $d$ or $T$, the exact computation is dominated by these numbers; use the modular variant.
- **Small characteristic.** Over a small finite field the $m_j$ can collide or vanish. The method needs characteristic 0 or a prime larger than every $m_j$, or the discrete logarithm variant.
- **Floating point.** The Vandermonde system with nodes $m_j$ of very different sizes is badly conditioned. Do not run the method in floating point at prime powers.
- **Zero coefficients.** A black box that returns a polynomial with cancelled terms has fewer terms than expected; this is harmless, since $t = \deg \Lambda$ is computed, not assumed.

## Implementations

## History

Prony (1795) recovered a sum of exponentials from equally spaced samples by the same linear recurrence. Ben-Or and Tiwari (1988) applied the idea to polynomials, with prime-power points so that the roots encode the exponents, and gave the first deterministic sparse interpolation whose number of probes does not depend on the degree. In the same year Kaltofen and Lakshman made the linear algebra fast, and Zippel's probabilistic algorithm (1979, 1990) offered an alternative. The connection to Reed-Solomon decoding was noted later: Berlekamp-Massey was designed for decoding BCH and Reed-Solomon codes, and sparse interpolation with errors is a decoding problem. Kaltofen and Lee's early termination (2003) removed the need for the term bound.

## References
