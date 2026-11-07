---
tag: T0YM2W
kind: algorithm
slug: berlekamp-factorization
name: Berlekamp's factorization algorithm
aliases:
- Berlekamp factorization
- Berlekamp's algorithm
- Berlekamp Q-matrix method
area: algebra/polynomial-arithmetic
level: advanced
summary: Factors a square-free polynomial over GF(p) by finding the null space of the Berlekamp matrix.
solves: [polynomial-factorization-over-finite-fields]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of f, p: the size of the prime field, r: the number of irreducible factors of f, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(n^3 + p r n^2 + M(n) log p)}
  random_splitting: {expected: O(n^3 + M(n) log(n p) log r)}
  space: {extra: O(n^2)}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1967
  people: [Elwyn R. Berlekamp]
  note: Berlekamp reduced factoring over a finite field to linear algebra on the matrix of the map v to v^p - v, which gave the first factoring algorithm polynomial in n and p; in 1970 he gave a randomized form for large fields.
prereqs: [irreducible-polynomial, square-free-factorization, polynomial-gcd, chinese-remainder-theorem, gaussian-elimination-modular, nullspace, fermat-little-theorem]
see_also: [cantor-zassenhaus-algorithm, distinct-degree-factorization, equal-degree-factorization, polynomial-factorization-over-finite-fields, zassenhaus-algorithm, wiedemann-algorithm, binary-exponentiation]
sources:
  - paper: doi:10.1002/j.1538-7305.1967.tb03174.x
    title: Elwyn R. Berlekamp, Factoring polynomials over finite fields, Bell System Technical Journal 46(8), 1853-1859, 1967
    locator: the matrix Q and the splitting by gcd(v - s, f)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 14.8, Algorithms based on linear algebra
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of polynomials (factoring modulo p, Berlekamp's method)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 20.5, Factoring polynomials, Berlekamp's algorithm
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.4, Factoring polynomials modulo a prime p (Berlekamp's method)
---

Berlekamp's algorithm factors a monic square-free polynomial $f$ over a prime field $\mathbb{F}_p$ with linear algebra. The polynomials $v$ of degree less than $n$ with $v^p \equiv v \pmod f$ form a vector space over $\mathbb{F}_p$, the Berlekamp algebra, whose dimension is the number $r$ of irreducible factors of $f$. It is the null space of $Q - I$, where $Q$ is the matrix of the map $v \mapsto v^p \bmod f$. Each such $v$ is a constant modulo each factor, so the gcds of $f$ with $v - s$ for $s \in \mathbb{F}_p$ split $f$.

Notation: $p$ is a prime and $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$, so the coefficient ring must be a field. $f \in \mathbb{F}_p[x]$ is monic and square-free of degree $n$, the product of $r$ distinct monic irreducibles $q_1, \ldots, q_r$. Vectors of length $n$ stand for polynomials of degree less than $n$, low degree first. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$. Costs count operations in $\mathbb{F}_p$ in the algebraic complexity model.

## In plain words

Work with remainders modulo the polynomial you want to factor. Some remainders do not change when you raise them to the power given by the field size, and these form a flat space that you can find by solving linear equations. The size of this space tells you how many pieces the polynomial has. Every remainder in the space looks like a plain number when seen from each piece, but the numbers differ from piece to piece. So for each possible number, the common part of the polynomial and that remainder minus the number picks out a group of pieces. Doing this for each direction of the space separates all the pieces.

## The problem

**Input:** a prime $p$ and a monic square-free $f \in \mathbb{F}_p[x]$ of degree $n \ge 1$.

**Output:** the monic irreducible factors $q_1, \ldots, q_r$ of $f$.

A general polynomial is first made monic and split into square-free parts by [square-free factorization](/square-free-factorization/), as in the [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/). The full problem is [polynomial factorization over finite fields](/polynomial-factorization-over-finite-fields/).

## The algorithm

```pseudo id=main
BERLEKAMP(f)
L1  n ← deg f;  build the n × n matrix Q whose row i holds the coefficients of x^(p i) mod f
L2  v_1, ..., v_r ← a basis of the left null space of Q - I, with v_1 = 1
L3  factors ← [f]
L4  for j ← 2 to r while |factors| < r do
L5      new ← []
L6      for each h in factors do
L7          for s ← 0 to p - 1 do
L8              g ← gcd(v_j - s, h);  if deg g > 0 then append g to new
L9      factors ← new
L10 return factors
```

Line L1 computes $x^p \bmod f$ by [binary exponentiation](/binary-exponentiation/) and each further row by one product modulo $f$. A row vector $v$ satisfies $v Q = v$ exactly when $v^p \equiv v \pmod f$, since $v(x)^p = \sum_i v_i x^{p i}$ over $\mathbb{F}_p$. Line L2 is [Gaussian elimination modulo p](/gaussian-elimination-modular/) on $(Q - I)^T$; row $0$ of $Q - I$ is zero, so $1$ is always in the [null space](/nullspace/). The implementation keeps factors of degree $1$ without further gcds.

For large $p$, lines L4 to L9 cost a factor $p$. The implementation then splits as in [equal-degree factorization](/equal-degree-factorization/): take a random $a = \sum_j c_j v_j$, and split each piece $h$ with $\gcd(a^{(p-1)/2} - 1, h)$.

## Example

Take $p = 3$ and $f = x^4 + x^3 + x + 2 = (x^2 + 1)(x^2 + x + 2)$; both quadratics have no root modulo $3$. Here $x^3 \bmod f = x^3$, so the rows of $Q$ are $x^0$, $x^3$, $x^6$ and $x^9$ modulo $f$.

| $i$ | $x^{3i} \bmod f$ | row $i$ of $Q$ | row $i$ of $Q - I$ |
|---|---|---|---|
| 0 | $1$ | $(1, 0, 0, 0)$ | $(0, 0, 0, 0)$ |
| 1 | $x^3$ | $(0, 0, 0, 1)$ | $(0, 2, 0, 1)$ |
| 2 | $x^3 + 2x^2 + x + 1$ | $(1, 1, 2, 1)$ | $(1, 1, 1, 1)$ |
| 3 | $x$ | $(0, 1, 0, 0)$ | $(0, 1, 0, 2)$ |

The left null space of $Q - I$ has the basis $v_1 = 1$ and $v_2 = x + x^3$, so $r = 2$ and $f$ has two irreducible factors. For $v_2$: $\gcd(v_2, f) = x^2 + 1$, $\gcd(v_2 - 1, f) = 1$ and $\gcd(v_2 - 2, f) = x^2 + x + 2$. Indeed $v_2 = x(x^2 + 1)$ is $0$ modulo $x^2 + 1$ and $2$ modulo $x^2 + x + 2$. A script checked every entry.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). By the [Chinese remainder theorem](/chinese-remainder-theorem/), $\mathbb{F}_p[x]/(f) \cong \prod_i \mathbb{F}_p[x]/(q_i)$, a product of fields $K_i$ with $p^{\deg q_i}$ elements. In a field $K_i$, the solutions of $y^p = y$ are exactly the $p$ elements of $\mathbb{F}_p$, by [Fermat's little theorem](/fermat-little-theorem/) and because $y^p - y$ has at most $p$ roots. So the Berlekamp algebra corresponds to $\mathbb{F}_p^r$, has dimension $r$, and each $v$ in it is congruent to a constant $s_i(v)$ modulo $q_i$. Then $h = \prod_s \gcd(v - s, h)$ for every piece $h$, so line L8 replaces $h$ by a partition of its factors. Two distinct factors $q_a, q_b$ are separated by the basis vector $v_j$ with $s_a(v_j) \ne s_b(v_j)$, which exists because the basis spans $\mathbb{F}_p^r$. So after the loop every piece is irreducible.

## Complexity

The bounds are proved and count operations in $\mathbb{F}_p$.

- **The matrix.** $O(M(n) \log p)$ for $x^p \bmod f$ and $O(n M(n))$ for the other rows.
- **The null space.** $O(n^3)$ by Gaussian elimination, or $O(n^\omega)$ with fast matrix multiplication.
- **Deterministic splitting.** At most $r - 1$ basis vectors, each with $p$ gcds per piece; the pieces have total degree $n$, so this is $O(p r n^2)$ with classical gcds.
- **Total.** $O(n^3 + p r n^2 + M(n) \log p)$, polynomial in $n$ and $p$ but not in $\log p$. With random splitting, the expected cost is $O(n^3 + M(n) \log(n p) \log r)$; von zur Gathen and Gerhard, Section 14.8, analyze the method with fast linear algebra.
- **Space.** $O(n^2)$ for the matrix.

**In practice (observed).** For small $p$ and moderate $n$ the linear algebra is cheap and the method is fast and deterministic; the matrix of size $n^2$ limits it for large $n$. For large $p$ the deterministic loop over $s$ is too slow, and random splitting or the Cantor-Zassenhaus algorithm is used instead. The crossover between the two methods depends on the implementation and the machine.

## Properties

- **Deterministic for small $p$.** Lines L1 to L10 use no randomness; the random splitting for large $p$ is Las Vegas.
- **Counts factors first.** The rank of $Q - I$ is $n - r$, so the number of factors, and whether $f$ is irreducible, comes before any splitting.
- **Needs square-free input.** If $q^2 \mid f$, the null space still has dimension equal to the number of distinct factors, but $q^2$ cannot be split into $q \cdot q$ by gcds with $v - s$.
- **Iterative.** No recursion.

## Variants and improvements

- **Large fields.** Berlekamp's 1970 method, and the random splitting above, avoid the factor $p$ by using powers $(p - 1)/2$ of random elements of the algebra.
- **Fast linear algebra.** The null space can be computed with fast matrix multiplication, or with black-box methods such as the [Wiedemann algorithm](/wiedemann-algorithm/), as in the method of Kaltofen and Lobo.
- **Niederreiter's method.** A related linear system built from a differential equation gives another deterministic reduction to linear algebra.
- **Over $\mathbb{F}_q$.** For $q = p^m$, the map $v \mapsto v^q$ is $\mathbb{F}_q$-linear, and the same method works with $q$ in place of $p$.

## When to use it

Use Berlekamp's algorithm to factor square-free polynomials over small prime fields, where a deterministic method is wanted and $n$ is small enough for an $n \times n$ matrix, for example in coding theory over $\mathbb{F}_2$ and in the modular step of [the Zassenhaus algorithm](/zassenhaus-algorithm/) with a small prime. For large $p$, use the random splitting or the [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/).

## Pitfalls

- **Row versus column.** The algebra is the left null space of $Q - I$, the vectors $v$ with $v (Q - I) = 0$. Solving $(Q - I) v = 0$ instead gives a different space in general.
- **Not square-free.** Run square-free factorization first.
- **Stopping too early or too late.** Stop when there are $r$ pieces; continuing wastes gcds, and stopping at fewer leaves products.
- **Random combinations.** In the random splitting, draw one scalar $c_j$ per basis vector and multiply the whole vector by it; drawing a scalar per coefficient leaves the algebra.

## Implementations

## History

Elwyn Berlekamp published the method in 1967, in the Bell System Technical Journal; it was the first factoring algorithm over $\mathbb{F}_p$ with cost polynomial in $n$ and $p$. In 1970 he gave a randomized form for large fields, using the same algebra. In 1981 Cantor and Zassenhaus gave a random splitting that needs no matrix.

## References
