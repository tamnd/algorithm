---
tag: 3SP5R7
kind: theorem
slug: eisenstein-criterion
name: Eisenstein's criterion
aliases:
- Eisenstein's irreducibility criterion
- Schonemann-Eisenstein criterion
area: algebra/polynomial-arithmetic
level: core
summary: A prime p dividing all non-leading coefficients but not the leading one, with p^2 not dividing the constant term, implies irreducibility.
prereqs: [polynomial, irreducible-polynomial, gauss-lemma]
see_also: [primitive-polynomial, polynomial-irreducibility-testing, polynomial-factorization-over-integers, rational-root-theorem, discriminant, factor-theorem, horner-rule, polynomial-ring]
sources:
  - book: isbn:9780387953854
    title: Serge Lang, Algebra, revised third edition, Graduate Texts in Mathematics 211, Springer, 2002
    locator: Chapter IV, Section 3, Criteria for irreducibility, Theorem 3.1 (Eisenstein's criterion) and the examples after it
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 9.4, Irreducibility criteria (Eisenstein's criterion for Z[x] and for integral domains with a prime ideal, and the cyclotomic example)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 6.2, Gauss' lemma (content, primitive part, and factorization over Z versus Q)
---

Eisenstein's criterion is a quick sufficient test for irreducibility over the rationals. If one prime divides every coefficient of a polynomial except the leading one, and its square does not divide the constant term, then the polynomial does not factor over $\mathbb{Q}$. The test needs only a few divisibility checks, and it gives irreducible polynomials of every degree, such as $x^n - 2$.

## Statement

Let $f = \sum_{k=0}^{n} a_k x^k \in \mathbb{Z}[x]$ with $n \ge 1$, and let $p$ be a prime.

**Theorem (Eisenstein's criterion).** Suppose that

1. $p \nmid a_n$,
2. $p \mid a_k$ for $0 \le k \le n - 1$, and
3. $p^2 \nmid a_0$.

Then $f$ is [irreducible](/irreducible-polynomial/) in $\mathbb{Q}[x]$. If in addition $f$ is primitive (the gcd of its coefficients is $1$), then $f$ is irreducible in $\mathbb{Z}[x]$.

A polynomial that meets the three conditions is called Eisenstein at $p$.

**General form.** Let $D$ be an integral domain, $P$ a prime ideal of $D$, and $f = \sum_{k=0}^{n} a_k x^k \in D[x]$ with $n \ge 1$, $a_n \notin P$, $a_k \in P$ for $k < n$ and $a_0 \notin P^2$. Then $f$ is not a product of two polynomials of positive degree in $D[x]$. If $D$ is a unique factorization domain with fraction field $K$, then $f$ is irreducible in $K[x]$.

## In plain words

Pick a prime number. Check three things about the coefficients of the polynomial. The prime must not divide the top coefficient. It must divide every other coefficient. Its square must not divide the constant term. If all three hold, the polynomial cannot be written as a product of two polynomials of lower degree with rational coefficients. The test is only one way: when it fails, the polynomial may still be irreducible. A common trick is to replace x by x plus a constant first, which does not change whether the polynomial factors, and then try the test again.

## Proof

We prove the general form, and then derive the statement over $\mathbb{Z}$ and $\mathbb{Q}$.

*No factorization in $D[x]$.* Suppose $f = gh$ with $g = \sum_{i=0}^{r} g_i x^i$, $h = \sum_{j=0}^{s} h_j x^j$, $g_r h_s \ne 0$, $r \ge 1$, $s \ge 1$ and $r + s = n$. Since $a_n = g_r h_s \notin P$ and $P$ is an ideal, $g_r \notin P$ and $h_s \notin P$. So the indices

$$u = \min\{ i : g_i \notin P \}, \qquad v = \min\{ j : h_j \notin P \}$$

exist, with $u \le r$ and $v \le s$. The coefficient of $x^{u+v}$ in $gh$ is

$$a_{u+v} = g_u h_v + \sum_{i < u} g_i h_{u+v-i} + \sum_{j < v} g_{u+v-j} h_j,$$

where coefficients with indices out of range are $0$. Every term in the two sums has a factor $g_i$ with $i < u$ or $h_j$ with $j < v$, so it lies in $P$. The product $g_u h_v$ is not in $P$, because $P$ is prime. So $a_{u+v} \notin P$. By condition 2 the only coefficient outside $P$ is $a_n$, so $u + v = n = r + s$. With $u \le r$ and $v \le s$ this gives $u = r \ge 1$ and $v = s \ge 1$. Hence $g_0 \in P$ and $h_0 \in P$, so $a_0 = g_0 h_0 \in P^2$. This contradicts condition 3.

*Over $\mathbb{Q}$.* Suppose $f = GH$ in $\mathbb{Q}[x]$ with $\deg G, \deg H \ge 1$. By [Gauss's lemma](/gauss-lemma/), there are $g, h \in \mathbb{Z}[x]$ with $f = gh$, $\deg g = \deg G$ and $\deg h = \deg H$: write $G = c\, G^*$ and $H = d\, H^*$ with $c, d \in \mathbb{Q}$ and $G^*, H^*$ primitive. The product $G^* H^*$ is primitive, and $f = cd\, G^* H^*$ with $f \in \mathbb{Z}[x]$ forces $cd \in \mathbb{Z}$. Take $g = cd\, G^*$ and $h = H^*$. This is a factorization of $f$ in $\mathbb{Z}[x]$ into two factors of positive degree, which the first part (with $D = \mathbb{Z}$, $P = p\mathbb{Z}$) excludes.

*Over $\mathbb{Z}$.* A factorization of a primitive $f$ in $\mathbb{Z}[x]$ into nonunits has either two factors of positive degree, which the first part excludes, or a constant factor $c \ne \pm 1$, which would divide every coefficient of $f$ and contradict primitivity.

*The general form over $K$.* The same argument works with Gauss's lemma for the unique factorization domain $D$. $\blacksquare$

## Consequences

- **Irreducible polynomials of every degree.** $x^n - 2$ is Eisenstein at $2$, so it is irreducible over $\mathbb{Q}$ for every $n \ge 1$. More generally $x^n - a$ is irreducible whenever some prime divides $a$ exactly once. So $\mathbb{Q}$ has algebraic extensions of every degree, and $\sqrt[n]{2}$ has degree $n$ over $\mathbb{Q}$.
- **Change of variable.** For $c \in \mathbb{Z}$, $f(x)$ is irreducible exactly when $f(x + c)$ is, because $x \mapsto x + c$ is a ring automorphism of $\mathbb{Q}[x]$ that keeps degrees. The shifted coefficients are a Taylor shift, which [Horner's rule](/horner-rule/) computes in $O(n^2)$ ring operations.
- **Cyclotomic polynomials of prime index.** For a prime $p$, $\Phi_p(x) = x^{p-1} + \cdots + x + 1 = (x^p - 1)/(x - 1)$. Then $\Phi_p(x + 1) = ((x + 1)^p - 1)/x = \sum_{k=1}^{p} \binom{p}{k} x^{k-1}$. The leading coefficient is $1$, the binomial coefficients $\binom{p}{k}$ with $0 < k < p$ are divisible by $p$, and the constant term is $\binom{p}{1} = p$. So $\Phi_p(x + 1)$ is Eisenstein at $p$, and $\Phi_p$ is irreducible.
- **Reversed form.** If $p \nmid a_0$, $p \mid a_k$ for $k \ge 1$ and $p^2 \nmid a_n$, then $f$ is irreducible over $\mathbb{Q}$. Apply the theorem to the reversal $x^n f(1/x) = \sum_k a_{n-k} x^k$, which is irreducible exactly when $f$ is, if $a_0 \ne 0$.
- **Use in factoring.** General [factorization over the integers](/polynomial-factorization-over-integers/) and [irreducibility testing](/polynomial-irreducibility-testing/) do not use Eisenstein's criterion, because it is only sufficient. It is a cheap first check, and it is the standard way to produce test inputs that are known to be irreducible.

**Worked examples.** Each of these was checked by a short script.

- $3x^5 - 15$: $p = 5$ divides $-15$ and does not divide $3$, and $25 \nmid 15$. It is irreducible over $\mathbb{Q}$.
- $\Phi_5(x + 1) = x^4 + 5x^3 + 10x^2 + 10x + 5$ is Eisenstein at $5$.
- $x^4 + 1$ meets no prime directly, since its constant term is $1$. But $(x + 1)^4 + 1 = x^4 + 4x^3 + 6x^2 + 4x + 2$ is Eisenstein at $2$, so $x^4 + 1$ is irreducible over $\mathbb{Q}$. It is reducible modulo every prime, so no single reduction modulo $p$ can prove this.
- $x^2 + x + 1$ becomes $x^2 + 3x + 3$ after $x \mapsto x + 1$, which is Eisenstein at $3$.
- $2x^2 + 6$ is Eisenstein at $3$. It is irreducible in $\mathbb{Q}[x]$, but in $\mathbb{Z}[x]$ it is $2 \cdot (x^2 + 3)$, a product of two nonunits, because it is not primitive.

## Tightness

- **Condition 3 is needed.** $x^2 - 4 = (x - 2)(x + 2)$: the prime $2$ divides $0$ and $-4$, does not divide $1$, but $4 \mid 4$.
- **Condition 1 is needed.** $2x^2 + 4x + 2 = (2x + 2)(x + 1)$ meets conditions 2 and 3 for $p = 2$, since $2 \mid 4$, $2 \mid 2$ and $4 \nmid 2$, but $2$ also divides the leading coefficient. It is reducible over $\mathbb{Q}$.
- **The criterion is not necessary.** $x^3 - x - 1$ has no rational root (its values at $\pm 1$ are $-1$), so it is irreducible over $\mathbb{Q}$ by the [rational root theorem](/rational-root-theorem/), since a cubic with a factor has a linear factor. But no shift $f(x + c)$ is Eisenstein at any prime. If $f(x + c)$ is Eisenstein at $p$, then $f \equiv a_n (x - c)^n \pmod p$, so $f$ has a repeated root modulo $p$ and $p$ divides the [discriminant](/discriminant/) of $f$, here $-23$. Modulo $23$, $(x - c)^3 = x^3 - 3c x^2 + 3c^2 x - c^3$ matches $x^3 - x - 1$ only if $3c \equiv 0$, so $c \equiv 0$, and then the coefficient of $x$ is $0$, not $-1$. A script also found no prime below $200$ and shift that works.
- **Degree 1.** Every polynomial of degree $1$ is irreducible over $\mathbb{Q}$, so the criterion says nothing new there.

## History

Theodor Schonemann published the criterion in 1846, in Crelle's journal, and Gotthold Eisenstein published it in 1850 in the same journal; the result is now known by Eisenstein's name, and some texts call it the Schonemann-Eisenstein criterion. Gustave Dumas extended it in 1906 with Newton polygons: if the Newton polygon of $f$ with respect to $p$ has one edge whose lattice points are only its end points, then $f$ is irreducible. Eisenstein's case is the polygon with one edge from $(0, 1)$ to $(n, 0)$.

## References
