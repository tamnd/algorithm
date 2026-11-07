---
tag: H77D0W
kind: algorithm
slug: equal-degree-factorization
name: Equal-degree factorization
aliases:
- EDF
- equal degree splitting
area: algebra/polynomial-arithmetic
level: advanced
summary: Splits a product of irreducibles of one common degree into its factors, given that degree.
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of f, d: the common degree of the irreducible factors, r: the number of factors n/d, p: the size of the prime field, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {expected: O((d log p + log n) M(n) log r)}
  space: {extra: O(n)}
  attempts_per_split: {expected: 2}
properties: {deterministic: false, in_place: false, recursive: false, online: false}
history:
  year: 1981
  people: [David G. Cantor, Hans Zassenhaus]
  note: Cantor and Zassenhaus split a product of irreducibles of equal degree with gcd(a^((q^d - 1)/2) - 1, f) for random a, after earlier random splitting methods of Berlekamp and of Rabin.
prereqs: [distinct-degree-factorization, irreducible-polynomial, polynomial-gcd, binary-exponentiation, chinese-remainder-theorem, euler-criterion]
see_also: [cantor-zassenhaus-algorithm, berlekamp-factorization, polynomial-factorization-over-finite-fields, quadratic-residue, tonelli-shanks, cipolla-algorithm, square-free-factorization]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 14.3, Equal-degree factorization, Cantor and Zassenhaus' algorithm; Section 14.5, Application, root finding
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.4.4, Final splitting
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 20.4, Factoring polynomials, the Cantor-Zassenhaus algorithm (the equal degree stage)
  - paper: doi:10.1090/S0025-5718-1981-0606517-5
    title: David G. Cantor and Hans Zassenhaus, A new algorithm for factoring polynomials over finite fields, Mathematics of Computation 36(154), 587-592, 1981
    locator: the random splitting of a product of irreducibles of equal degree
---

Equal-degree factorization splits a polynomial $f$ over $\mathbb{F}_p$ that is a product of distinct irreducible polynomials of one known degree $d$ into those factors. It picks a random polynomial $a$ and computes $b = a^{(p^d - 1)/2} \bmod f$. Modulo each irreducible factor, $b$ is $0$, $1$ or $-1$, each nonzero value with probability about one half, so $\gcd(b - 1, f)$ is a proper factor with probability at least one half. Repeating on the pieces gives all factors. It is the second stage of the [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/), after [distinct-degree factorization](/distinct-degree-factorization/).

Notation: $p$ is a prime, $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$, and $f \in \mathbb{F}_p[x]$ is monic of degree $n = r d$, the product of $r$ distinct monic irreducibles of degree $d$. Arithmetic is modulo $f$ in $\mathbb{F}_p[x]$, so $\mathbb{F}_p$ must be a field. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$. Costs count operations in $\mathbb{F}_p$ in the algebraic complexity model, and the algorithm can draw uniform random elements of $\mathbb{F}_p$.

## In plain words

Suppose a polynomial is a product of several unbreakable pieces that all have the same size, and you want the pieces. Pick a random polynomial and raise it to a large, carefully chosen power, keeping only remainders modulo the input. Seen from each piece, the result is plus one or minus one, like a coin toss, and the tosses for different pieces are independent. The common part of the input and the result minus one collects the pieces whose coin came up plus one. Unless all coins agree, this splits the input. Repeat on each part until every part has the known size.

## The problem

**Input:** a prime $p$, a degree $d \ge 1$, and a monic square-free $f \in \mathbb{F}_p[x]$ whose irreducible factors all have degree $d$.

**Output:** the $r = n/d$ monic irreducible factors of $f$.

Such an $f$ is exactly what each part $g_d$ of [distinct-degree factorization](/distinct-degree-factorization/) is. For $d = 1$, the problem is to find all roots of a polynomial that splits into distinct linear factors.

## The algorithm

For odd $p$, let $e = (p^d - 1)/2$. For $p = 2$, the power is replaced by the trace $T(a) = a + a^2 + a^4 + \cdots + a^{2^{d-1}}$.

```pseudo id=main
EQUAL-DEGREE(f, d)
L1  stack ← [f];  out ← []
L2  while stack is not empty do
L3      h ← pop(stack)
L4      if deg h = d then append h to out;  continue
L5      choose a ∈ F_p[x] at random with deg a < deg h;  if a is constant, go to L5
L6      g ← gcd(a, h);  if g ≠ 1 then push g and h/g;  continue
L7      b ← a^e mod h                       ▷ for p = 2: b ← T(a) mod h
L8      g ← gcd(b - 1, h)
L9      if g ≠ 1 and g ≠ h then push g and h/g else push h
L10 return out
```

Line L7 uses [binary exponentiation](/binary-exponentiation/) modulo $h$, with about $d \log_2 p$ squarings, and the trace for $p = 2$ uses $d - 1$ squarings. An explicit stack replaces recursion. A failed attempt draws a new $a$ for the same $h$.

## Example

Take $p = 7$, $d = 2$, and $f = (x^2 + 1)(x^2 + 4)(x^2 + x + 3) = x^6 + x^5 + x^4 + 5x^3 + 5x^2 + 4x + 5$. All three quadratics are irreducible over $\mathbb{F}_7$, since their discriminants $-4$, $-16$ and $-11$ are not squares modulo $7$. Here $e = (49 - 1)/2 = 24$.

| attempt | $h$ | $a$ | $b = a^{24} \bmod h$ | $b$ modulo the factors | $\gcd(b - 1, h)$ |
|---|---|---|---|---|---|
| 1 | $f$ | $x^2$ | $1$ | $1, 1, 1$ | $f$: no split |
| 2 | $f$ | $x$ | $6x^4 + 2x^2 + 4$ | $1, 1, -1$ | $x^4 + 5x^2 + 4$ |
| 3 | $x^4 + 5x^2 + 4$ | $x + 1$ | $3x^2 + 4$ | $1, -1$ | $x^2 + 1$ |

Attempt 1 fails because $x^2$ is a square modulo every factor. Attempt 2 separates $x^2 + x + 3$ from the other two, and attempt 3 separates $x^2 + 1$ from $x^2 + 4$. The output is $x^2 + 1$, $x^2 + 4$ and $x^2 + x + 3$. A script checked every entry.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). By the [Chinese remainder theorem](/chinese-remainder-theorem/), $\mathbb{F}_p[x]/(f) \cong \mathbb{F}_{p^d}^r$, and a random $a$ maps to $r$ independent uniform elements $a_1, \ldots, a_r$. For odd $p$, $a_j^e$ is $0$ if $a_j = 0$, and otherwise $1$ or $-1$ as $a_j$ is a square or not in $\mathbb{F}_{p^d}$, by the generalization of [Euler's criterion](/euler-criterion/). So $\gcd(b - 1, h)$ is the product of the factors where $a_j$ is a nonzero square. Every piece that is pushed is a product of some of the factors, and every piece that is output has degree $d$, so it is one factor. Each attempt splits with probability at least $1/2$ when $h$ has at least two factors, so the algorithm stops with probability $1$.

## Complexity

The bounds are proved, count operations in $\mathbb{F}_p$, and are expected values over the random choices.

- **One attempt on $h$ of degree $m$.** $O(d \log p)$ products modulo $h$ for line L7 and two gcds, so $O((d \log p) M(m) + M(m) \log m)$.
- **Success probability.** At least $1/2$ for each attempt on an $h$ with two or more factors, so at most $2$ attempts per split on average.
- **Total.** The pieces form a splitting tree whose levels have total degree at most $n$, and its expected depth is $O(\log r)$. With $M$ superlinear, the total is $O((d \log p + \log n) M(n) \log r)$, as in von zur Gathen and Gerhard, Section 14.3. With schoolbook arithmetic, as in the implementation, $O(n^2 (d \log p + n) \log r)$.
- **Space.** $O(n)$ field elements.

**In practice (observed).** The power $a^e \bmod h$ dominates. In the trials of the test file, the number of attempts per split is close to $2$ for two factors and smaller for many factors, as the analysis predicts. Implementations reuse the powers $x^{p^i} \bmod f$ from distinct-degree factorization to compute $a^e$ faster, since $e = (p - 1)/2 \cdot (1 + p + \cdots + p^{d-1})$.

## Properties

- **Las Vegas.** The output is always correct; only the running time is random.
- **Needs equal degrees and square-freeness.** If the factors had different degrees, a piece of degree $d$ could be a product of smaller factors. If $f$ had a repeated factor, $\gcd(b - 1, h)$ could never separate the two copies, and the loop would not end.
- **Characteristic two.** The power map does not work for $p = 2$, since $(p^d - 1)/2$ is not an integer; the trace map plays its role.
- **Iterative.** An explicit stack, no recursion.

## Variants and improvements

- **Root finding.** For $d = 1$, apply the method to $\gcd(x^p - x, f)$ to find all roots in $\mathbb{F}_p$; von zur Gathen and Gerhard, Section 14.5. Square roots modulo $p$ are the case $f = x^2 - c$, which is close to [Cipolla's algorithm](/cipolla-algorithm/).
- **Deterministic splitting for small $p$.** [Berlekamp's algorithm](/berlekamp-factorization/) splits with $\gcd(v - s, f)$ for all $s \in \mathbb{F}_p$ and basis elements $v$ of the Berlekamp algebra, which needs no randomness and costs a factor $p$.
- **Faster powering.** Write $a^e$ with the trace of $a$ and the Frobenius powers $x^{p^i} \bmod f$, computed by [modular composition](/brent-kung-composition/); this lowers the cost to about $M(n)$ times a power of $\log n$ for each attempt, as in the methods of von zur Gathen, Kaltofen and Shoup.
- **Larger fields.** Over $\mathbb{F}_q$ with odd $q$, use $e = (q^d - 1)/2$; for $q = 2^k$, use the trace from $\mathbb{F}_{q^d}$ to $\mathbb{F}_2$.

## When to use it

Use equal-degree factorization after [distinct-degree factorization](/distinct-degree-factorization/) to finish factoring over a finite field, in particular when $p$ is large, where the deterministic splitting of Berlekamp would cost a factor $p$. For $d = 1$ it is the standard method to find roots of polynomials over large prime fields.

## Pitfalls

- **Using $\gcd(b, h)$ instead of $\gcd(b - 1, h)$.** For odd $p$, $b$ is $0$ only modulo factors that divide $a$, so $\gcd(b, h)$ is almost always $1$.
- **Constant $a$.** A constant $a$ has the same value modulo every factor and never splits; draw $a$ again.
- **Wrong exponent.** The exponent is $(p^d - 1)/2$, not $(p - 1)/2$; with the smaller exponent, $b$ is not $\pm 1$ modulo factors of degree $d > 1$.
- **Deep recursion.** Splitting recursively on both parts gives depth up to $r$ in bad runs; an explicit stack avoids it.
- **Squared factors.** Run [square-free factorization](/square-free-factorization/) first; otherwise the algorithm may loop forever.

## Implementations

## History

Elwyn Berlekamp gave a randomized method for finding roots over large prime fields in 1970, and Michael Rabin analyzed random splitting for factoring and root finding in 1980. David Cantor and Hans Zassenhaus published the splitting by $\gcd(a^{(q^d - 1)/2} - 1, f)$ in 1981, in the paper that combined it with distinct-degree factorization into a complete algorithm. Since then the stage has been made faster with Frobenius powers and modular composition by von zur Gathen, Kaltofen and Shoup.

## References
