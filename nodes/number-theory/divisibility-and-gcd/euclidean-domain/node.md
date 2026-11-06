---
tag: 9YR55N
kind: definition
slug: euclidean-domain
name: Euclidean domain
aliases:
- Euclidean ring
area: number-theory/divisibility-and-gcd
level: advanced
summary: An integral domain with a Euclidean function, so that a Euclid-style gcd and Bézout identity hold.
prereqs: [euclidean-algorithm, bezouts-identity, euclids-lemma, polynomial-ring]
see_also: [polynomial-gcd, extended-euclidean-algorithm, fundamental-theorem-of-arithmetic, greatest-common-divisor, gcd-recursion-theorem, polynomial-ideal, euclidean-algorithm, euclids-lemma]
sources:
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition
    locator: Section 8.1, Euclidean domains; Section 8.2, Principal ideal domains; Section 8.3, Unique factorization domains (including the example of Z[(1 + sqrt(-19))/2])
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition
    locator: Chapter 1, Sections 1.3 and 1.4 (unique factorization in a principal ideal domain, and the rings k[x], Z[i] and Z[omega])
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 12, The fundamental theorem of arithmetic in k(1), k(i) and k(rho), and Chapter 14 (quadratic fields, Euclidean fields)
  - paper: "Theodore Motzkin, The Euclidean algorithm, Bulletin of the American Mathematical Society 55(12), 1949"
    locator: pages 1142 to 1146
---

A Euclidean domain is an integral domain in which division with remainder is possible: there is a size function $N$ such that any $a$ can be written as $a = qb + r$ with $r = 0$ or $N(r) < N(b)$. This is the one property the [Euclidean algorithm](/euclidean-algorithm/) needs, so in every Euclidean domain the algorithm computes a [greatest common divisor](/greatest-common-divisor/), [Bézout's identity](/bezouts-identity/) holds, and factorization into primes is unique. The integers, polynomials over a field, the Gaussian integers $\mathbb{Z}[i]$ and the Eisenstein integers are the standard examples. Every Euclidean domain is a principal ideal domain, but not conversely.

## Definition

Let $R$ be an **integral domain**: a commutative ring with $1 \ne 0$ in which $ab = 0$ implies $a = 0$ or $b = 0$. A **Euclidean function** on $R$ is a function $N : R \setminus \{0\} \to \mathbb{Z}_{\ge 0}$ such that for all $a, b \in R$ with $b \ne 0$ there exist $q, r \in R$ with

$$a = qb + r, \qquad r = 0 \text{ or } N(r) < N(b).$$

$R$ is a **Euclidean domain** if it has at least one Euclidean function. The $q$ and $r$ need not be unique, and $N$ is not part of the structure: a ring can have many Euclidean functions. Some authors also require $N(a) \le N(ab)$ for $a, b \ne 0$; every Euclidean domain has a function with this extra property, so the class of rings is the same.

**The Euclidean algorithm works.** Given $a, b$, repeat $(a, b) \leftarrow (b, r)$ with $a = qb + r$ until $b = 0$. Each step lowers $N(b)$, a non-negative integer, so the loop stops. Each step keeps the set of common divisors, because $r = a - qb$; so the last non-zero value divides $a$ and $b$, and every common divisor divides it. It is a gcd, unique up to multiplication by a unit. The [extended Euclidean algorithm](/extended-euclidean-algorithm/) also works and writes the gcd as $ax + by$.

**Theorem (Euclidean implies principal ideal domain).** Every ideal $I$ of a Euclidean domain $R$ is principal, $I = (b)$ for one $b$.

*Proof.* If $I = \{0\}$, take $b = 0$. Otherwise let $b \in I \setminus \{0\}$ have the smallest value $N(b)$, which exists by the well-ordering of $\mathbb{Z}_{\ge 0}$. For $a \in I$, write $a = qb + r$. Then $r = a - qb \in I$. If $r \ne 0$, then $N(r) < N(b)$, against the choice of $b$. So $r = 0$, $a \in (b)$, and $I = (b)$. $\square$

**Consequences.** In a principal ideal domain, the ideal $(a, b)$ equals $(g)$ for a gcd $g$, which is Bézout's identity. An irreducible element $p$ then satisfies [Euclid's lemma](/euclids-lemma/): if $p \mid ab$ and $p \nmid a$, then $(p, a) = (1)$, so $1 = px + ay$, and $b = pbx + aby$ is divisible by $p$. With the fact that factorization into irreducibles exists in a principal ideal domain, this gives unique factorization, the analogue of the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/). So

$$\text{Euclidean domain} \;\Rightarrow\; \text{principal ideal domain} \;\Rightarrow\; \text{unique factorization domain},$$

and neither arrow can be reversed.

**Units and the minimum.** If $N(u)$ is the smallest value of $N$ on $R \setminus \{0\}$ and $N(a) \le N(ab)$ holds, then the elements with that smallest value are exactly the units. Motzkin (1949) showed that every Euclidean domain has a smallest Euclidean function, built by transfinite recursion from the units.

## Examples and non-examples

**The integers.** $\mathbb{Z}$ with $N(a) = |a|$: for $b \ne 0$, take $q = \lfloor a/b \rfloor$ when $b > 0$, so $0 \le r < |b|$. Choosing the nearest integer instead gives $|r| \le |b|/2$, another valid choice of $r$.

**Polynomials over a field.** $k[x]$ with $N(f) = \deg f$, for any field $k$: long division of polynomials gives $f = qg + r$ with $r = 0$ or $\deg r < \deg g$. For example $\gcd(x^3 - 1, x^2 - 1) = x - 1$ over $\mathbb{Q}$: $x^3 - 1 = x(x^2 - 1) + (x - 1)$ and $x^2 - 1 = (x + 1)(x - 1)$. See [polynomial GCD](/polynomial-gcd/).

**The Gaussian integers.** $\mathbb{Z}[i] = \{x + yi : x, y \in \mathbb{Z}\}$ with the norm $N(x + yi) = x^2 + y^2$. To divide $a$ by $b$, compute $a/b$ in $\mathbb{Q}(i)$ and round each coordinate to the nearest integer to get $q$. The error $a/b - q$ has both coordinates at most $1/2$ in absolute value, so $N(r) = N(b) \, N(a/b - q) \le N(b)/2$. Example: $\gcd(11 + 3i, 1 + 8i)$:

$$11 + 3i = (1 - i)(1 + 8i) + (2 - 4i), \quad 1 + 8i = (-1 + i)(2 - 4i) + (-1 + 2i), \quad 2 - 4i = -2 \cdot (-1 + 2i).$$

The norms of the remainders drop $65 \to 20 \to 5 \to 0$. The gcd is $-1 + 2i$, an associate of $2 + i$: indeed $11 + 3i = (2 + i)(5 - i)$ and $1 + 8i = (2 + i)(2 + 3i)$.

**Other quadratic rings.** $\mathbb{Z}[\sqrt{-2}]$, the Eisenstein integers $\mathbb{Z}[\omega]$ with $\omega = (-1 + \sqrt{-3})/2$, and the rings of integers of $\mathbb{Q}(\sqrt{-7})$ and $\mathbb{Q}(\sqrt{-11})$ are Euclidean for the norm. Among imaginary quadratic fields these five, $d = -1, -2, -3, -7, -11$, are the only Euclidean ones. Some real quadratic rings are Euclidean too, such as $\mathbb{Z}[\sqrt 2]$ with $N(x + y\sqrt 2) = |x^2 - 2y^2|$.

**Fields and power series.** A field is Euclidean with $N$ constant, since every division is exact. The formal power series $k[[x]]$ are Euclidean with $N(f)$ the order of $f$, the index of its first non-zero coefficient.

**Non-example: $\mathbb{Z}[x]$.** The ideal $(2, x)$, the polynomials with even constant term, is not principal: a generator would divide $2$ and $x$, so it would be $\pm 1$, but $1 \notin (2, x)$. So $\mathbb{Z}[x]$ is not a principal ideal domain and not Euclidean, although it has unique factorization. Bézout's identity fails: $\gcd(2, x) = 1$, but $2f + xg$ always has an even constant term.

**Non-example: $\mathbb{Z}[\sqrt{-5}]$.** Here $6 = 2 \cdot 3 = (1 + \sqrt{-5})(1 - \sqrt{-5})$ gives two different factorizations into irreducibles, so the ring is not a unique factorization domain and not Euclidean.

**Non-example: a principal ideal domain that is not Euclidean.** The ring $\mathbb{Z}[(1 + \sqrt{-19})/2]$ is a principal ideal domain, but it has no Euclidean function at all, for any choice of $N$. The proof uses a *universal side divisor*: every Euclidean domain that is not a field has an element $u$, not zero or a unit, such that every element is congruent modulo $u$ to $0$ or a unit; this ring has none.

**Non-example: $k[x, y]$.** Polynomials in two variables over a field have unique factorization, but $(x, y)$ is not principal, so the ring is not Euclidean.

## Related definitions

- **Principal ideal domain (PID).** An integral domain in which every ideal is generated by one element. Every Euclidean domain is a PID; gcds exist and Bézout's identity holds, but there may be no algorithm to compute them by division.
- **Unique factorization domain (UFD).** An integral domain in which every non-zero non-unit is a product of irreducibles, unique up to order and units. Every PID is a UFD; $\mathbb{Z}[x]$ and $k[x, y]$ are UFDs that are not PIDs.
- **Norm-Euclidean.** A ring of integers of a number field that is Euclidean with the absolute value of the field norm as $N$. The five imaginary quadratic cases above are norm-Euclidean.
- **[Polynomial ring](/polynomial-ring/).** $k[x]$ over a field is the main Euclidean domain after $\mathbb{Z}$; its gcd algorithms are [polynomial GCD](/polynomial-gcd/), the subresultant and modular methods.
- **Ideal generated by elements.** $(a_1, \ldots, a_k)$, the set of combinations $\sum r_i a_i$. In a Euclidean domain it equals $(\gcd(a_1, \ldots, a_k))$; in general rings of polynomials it is studied with [polynomial ideals](/polynomial-ideal/) and Gröbner bases.

## References
