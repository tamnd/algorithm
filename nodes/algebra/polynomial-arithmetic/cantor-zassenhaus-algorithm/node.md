---
tag: 1P1SGK
kind: algorithm
slug: cantor-zassenhaus-algorithm
name: Cantor-Zassenhaus algorithm
aliases:
- Cantor-Zassenhaus splitting
- equal-degree factorization
- equal-degree splitting
- Cantor-Zassenhaus factorization
area: algebra/polynomial-arithmetic
level: advanced
summary: Randomized factorization over finite fields by square-free, distinct-degree and random gcd splitting.
solves: [polynomial-factorization-over-finite-fields]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of f, p: the size of the prime field, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {expected: O(n M(n) log(n p))}
  space: {extra: O(n)}
  splitting_attempts: {expected: O(n)}
properties: {deterministic: false, in_place: false, recursive: false, online: false}
history:
  year: 1981
  people: [David G. Cantor, Hans Zassenhaus]
  note: Cantor and Zassenhaus combined distinct-degree factorization with a random splitting by gcd(a^((q^d - 1)/2) - 1, f), which gave a simple randomized factoring method for large finite fields.
prereqs: [square-free-factorization, distinct-degree-factorization, equal-degree-factorization, irreducible-polynomial, polynomial-gcd]
see_also: [polynomial-factorization-over-finite-fields, berlekamp-factorization, yun-square-free-factorization, rabin-irreducibility-test, zassenhaus-algorithm, polynomial-factorization-over-integers, square-free-polynomial, brent-kung-composition]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 14, Factoring polynomials over finite fields; Sections 14.2, 14.3, 14.4 and 14.6
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.4, Factoring polynomials modulo a prime p
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Chapter 20, Algorithms for finite fields; Sections 20.3 and 20.4
  - paper: doi:10.1090/S0025-5718-1981-0606517-5
    title: David G. Cantor and Hans Zassenhaus, A new algorithm for factoring polynomials over finite fields, Mathematics of Computation 36(154), 587-592, 1981
    locator: the complete algorithm
---

The Cantor-Zassenhaus algorithm factors a polynomial $f$ over a prime field $\mathbb{F}_p$ into monic irreducible factors with multiplicities. It works in three stages: [square-free factorization](/square-free-factorization/) separates the factors by multiplicity, [distinct-degree factorization](/distinct-degree-factorization/) separates them by degree, and [equal-degree factorization](/equal-degree-factorization/) splits each part with random gcds. Only the last stage uses randomness, and the output is always correct.

Notation: $p$ is a prime and $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$, so the coefficient ring must be a field. $f \in \mathbb{F}_p[x]$ is nonzero of degree $n$, and $\mathrm{lc}(f)$ is its leading coefficient. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$. Costs count operations in $\mathbb{F}_p$ in the algebraic complexity model, and the algorithm can draw uniform random elements of $\mathbb{F}_p$.

## In plain words

To break a polynomial over a finite field into unbreakable pieces, sort the pieces in two ways before you separate them. First, group the pieces by how often they occur, using the common part of the polynomial and its derivative. Second, group the pieces in each group by size, using a fixed polynomial for each size that contains every piece of that size. Now each group holds distinct pieces of one size. Third, separate the pieces in a group with random tests that split the group in two about half of the time, and repeat until every part is one piece.

## The problem

**Input:** a prime $p$ and a nonzero $f \in \mathbb{F}_p[x]$.

**Output:** $c = \mathrm{lc}(f)$ and the pairs $(q_1, e_1), \ldots, (q_k, e_k)$ of distinct monic irreducible $q_i$ and exponents $e_i \ge 1$ with $f = c\, q_1^{e_1} \cdots q_k^{e_k}$.

This is [polynomial factorization over finite fields](/polynomial-factorization-over-finite-fields/). The factorization exists and is unique because $\mathbb{F}_p[x]$ is a Euclidean domain.

## The algorithm

The pseudocode does the square-free factorization of lines L2 to L10 with the derivative $u'$ and $p$-th roots, and calls DISTINCT-DEGREE and EQUAL-DEGREE from their pages.

```pseudo id=main
CANTOR-ZASSENHAUS(f)
L1  c ← lc(f);  result ← [];  work ← [(f / c, 1)]
L2  while work is not empty do
L3      (u, k) ← pop(work);  v ← gcd(u, u');  w ← u / v;  i ← 1
L4      while w ≠ 1 do                  ▷ w: the factors of u of multiplicity ≥ i and not divisible by p
L5          y ← gcd(w, v);  s ← w / y   ▷ s: the factors of multiplicity exactly i
L6          if s ≠ 1 then
L7              for each (g, d) in DISTINCT-DEGREE(s) do
L8                  for each q in EQUAL-DEGREE(g, d) do append (q, i k) to result
L9          w ← y;  v ← v / y;  i ← i + 1
L10     if v ≠ 1 then push (the p-th root of v, p k) onto work
L11 return c and result, sorted
```

Over $\mathbb{F}_p$, $a^p = a$ for every coefficient $a$, so a polynomial whose exponents are all multiples of $p$ is $\left(\sum_j a_{jp} x^j\right)^p$; line L10 takes this root. A factor $q^e$ with $p \mid e$ has derivative $e\, q^{e-1} q' = 0$, so it divides $u'$ to its full power and stays in $v$ until line L10. For odd $p$, EQUAL-DEGREE uses the power $a^{(p^d - 1)/2}$; for $p = 2$ it uses the trace $a + a^2 + \cdots + a^{2^{d-1}}$.

## Example

Take $p = 3$ and $f = 2x^9 + x^8 + x^7 + x^6 + 2x^4 + 2x^3 + 2x^2 + x$, which is $2 \cdot x (x + 2)(x + 1)^3 (x^2 + 1)^2$. Line L1 gives $c = 2$ and $u = f/2 = x^9 + 2x^8 + 2x^7 + 2x^6 + x^4 + x^3 + x^2 + 2x$. Line L3 gives $v = \gcd(u, u') = x^5 + x^3 + x^2 + 1$ and $w = x^4 + 2x^3 + x^2 + 2x$.

| step | $y = \gcd(w, v)$ | $s = w / y$ | DISTINCT-DEGREE$(s)$ | factors out | $v$ after |
|---|---|---|---|---|---|
| $k = 1$, $i = 1$ | $x^2 + 1$ | $x^2 + 2x$ | $(x^2 + 2x, 1)$ | $(x, 1)$, $(x + 2, 1)$ | $x^3 + 1$ |
| $k = 1$, $i = 2$ | $1$ | $x^2 + 1$ | $(x^2 + 1, 2)$ | $(x^2 + 1, 2)$ | $x^3 + 1$ |
| $k = 3$, $i = 1$ | $1$ | $x + 1$ | $(x + 1, 1)$ | $(x + 1, 3)$ | $1$ |

After the second step $w = 1$, and $v = x^3 + 1$ has only exponents divisible by $3$, so line L10 pushes its cube root $x + 1$ with $k = 3$. In the first step, EQUAL-DEGREE splits $x^2 + 2x$ with $d = 1$ and exponent $(3 - 1)/2 = 1$; for example $a = x + 1$ gives $\gcd(a - 1, x^2 + 2x) = x$. The result is $f = 2 \cdot x \cdot (x + 1)^3 (x + 2) (x^2 + 1)^2$. A script checked every entry.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Write $u = \prod_q q^{e_q}$. Then $\gcd(u, u') = \prod_{p \nmid e_q} q^{e_q - 1} \prod_{p \mid e_q} q^{e_q}$, so $w$ at line L3 is the product of the $q$ with $p \nmid e_q$. The loop invariant at line L4 is that $w$ is the product of the $q$ with $p \nmid e_q$ and $e_q \ge i$, and $v = \prod_{p \nmid e_q,\, e_q \ge i} q^{e_q - i} \prod_{p \mid e_q} q^{e_q}$. Then $s$ at line L5 is the product of the $q$ with $e_q = i$, which is square-free, so the pages on distinct-degree and equal-degree factorization show that lines L7 and L8 output exactly these $q$. At line L10, $v = \prod_{p \mid e_q} q^{e_q}$ is a $p$-th power, and its root has the multiplicities $e_q / p$. Each push divides the degree by at least $p$, so the work list empties after at most $\log_p n + 1$ rounds.

## Complexity

The bounds are proved, count operations in $\mathbb{F}_p$, and are expected values over the random choices in EQUAL-DEGREE.

- **Square-free stage.** At most $2n$ gcds and exact divisions of degree at most $n$, so $O(n M(n) \log n)$ with fast gcds, and $O(n^3)$ classically. The $p$-th roots cost $O(n)$. Yun's method lowers the count, see [Yun's algorithm](/yun-square-free-factorization/).
- **Distinct-degree stage.** $O(n M(n) \log(n p))$ in total over all parts, which dominates.
- **Equal-degree stage.** $O((d \log p + \log n) M(n) \log r)$ for a part of degree $n$ with $r$ factors of degree $d$, and at most $2$ attempts per split on average, so $O(n)$ attempts in all.
- **Total.** $O(n M(n) \log(n p))$ expected, as in von zur Gathen and Gerhard, Chapter 14. With schoolbook arithmetic, as in the implementation, $O(n^3 \log(n p))$.
- **Space.** $O(n)$ field elements.

**In practice (observed).** For random $f$, the distinct-degree stage takes most of the time, because it computes $x^{p^i} \bmod f$ for $i$ up to about $n/2$. A random polynomial is usually square-free and has few factors, so the other two stages are cheap. For small $p$ and moderate $n$, Berlekamp's algorithm is a competitive alternative, since its splitting does not depend on $\log p$; which one is faster depends on the implementation and the machine.

## Properties

- **Las Vegas.** The output is always correct; only the time is random.
- **Any characteristic.** The power map works for odd $p$; for $p = 2$ the trace map replaces it, as on the page on equal-degree factorization.
- **Gives multiplicities.** The multiplicity of each factor comes from the square-free stage, as the product $i k$ at line L8.
- **Iterative.** The work list and the stacks inside the stages replace recursion; the depth of the work list is at most $\log_p n + 1$.

## Variants and improvements

- **Yun's square-free factorization.** [Yun's algorithm](/yun-square-free-factorization/) replaces lines L3 to L9 with fewer and smaller gcds.
- **Root finding.** For the roots in $\mathbb{F}_p$ only, compute $\gcd(x^p - x, f)$ and split it with equal-degree factorization for $d = 1$.
- **Faster distinct-degree stage.** The methods of von zur Gathen and Shoup, of Kaltofen and Shoup, and of Kedlaya and Umans use [modular composition](/brent-kung-composition/) and baby-step giant-step to bring the cost below $n^2$ operations for fixed $p$.
- **Deterministic alternative.** [Berlekamp's algorithm](/berlekamp-factorization/) replaces the last two stages with linear algebra on the matrix of the Frobenius map, deterministically for small $p$.
- **Larger fields.** Over $\mathbb{F}_q$ with $q = p^m$, replace $p$ by $q$ in the two last stages; the $p$-th root at line L10 then also takes $p$-th roots of the coefficients.

## When to use it

Use the Cantor-Zassenhaus algorithm to factor polynomials over prime fields with large $p$, where Berlekamp's deterministic splitting would cost a factor $p$. It is the modular step of [the Zassenhaus algorithm](/zassenhaus-algorithm/) for [factoring over the integers](/polynomial-factorization-over-integers/), and its root-finding variant finds the roots of polynomials over large prime fields.

## Pitfalls

- **Skipping the square-free stage.** Distinct-degree factorization misses repeated factors, and equal-degree factorization may never separate two equal factors.
- **Zero derivative.** If $u' = 0$, then $\gcd(u, u') = u$ and $w = 1$; the factors then all come from the $p$-th root at line L10. Code that assumes $u' \ne 0$ loops or fails.
- **Wrong multiplicity.** The multiplicity is $i k$, not $i$; forgetting $k$ loses the factor $p$ for factors from the root at line L10.
- **Power map in characteristic two.** $(2^d - 1)/2$ is not an integer; use the trace.
- **Seeding.** A fixed random seed gives reproducible runs; a bad generator that repeats values can make the equal-degree stage loop.

## Implementations

## History

Berlekamp gave the first polynomial-time factoring algorithm for small finite fields in 1967, and in 1970 a randomized variant for large fields. Rabin analyzed random splitting in 1980. Cantor and Zassenhaus published their method in 1981; its distinct-degree stage followed known practice, and its splitting stage was a simple random gcd. Later work by von zur Gathen, Kaltofen, Shoup, Kedlaya and Umans made the distinct-degree stage asymptotically faster.

## References
