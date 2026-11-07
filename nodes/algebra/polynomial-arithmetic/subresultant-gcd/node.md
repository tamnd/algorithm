---
tag: DB9KV8
kind: algorithm
slug: subresultant-gcd
name: Subresultant GCD algorithm
aliases:
- subresultant pseudo-remainder sequence
- subresultant algorithm
- Collins subresultant algorithm
area: algebra/polynomial-arithmetic
level: advanced
summary: Computes gcds over integral domains with controlled coefficient growth, using subresultant sequences.
solves: [polynomial-gcd]
model: blum-shub-smale-machine
complexity:
  vars: {m: the larger of the degrees of f and g}
  time: {worst: O(m^2)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [pseudo-division, resultant, primitive-polynomial, polynomial-euclidean-algorithm]
see_also: [subresultant, subresultant-prs, primitive-prs, pseudo-division, brown-modular-gcd, resultant, polynomial-gcd, gauss-lemma]
sources:
  - paper: doi:10.1145/321371.321381
    title: George E. Collins, Subresultants and reduced polynomial remainder sequences, Journal of the ACM 14(1), 1967
    locator: pp. 128 to 142
  - paper: doi:10.1145/321662.321665
    title: W. S. Brown and J. F. Traub, On Euclid's algorithm and the theory of subresultants, Journal of the ACM 18(4), 1971
    locator: pp. 505 to 514 (the fundamental theorem of subresultants)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of Polynomials (the gcd over a unique factorization domain by subresultants, and the example pair u, v used below)
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.3, The sub-resultant algorithm
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 11.2, Subresultants (p. 327)
  - paper: doi:10.1145/321662.321664
    title: W. S. Brown, On Euclid's algorithm and the computation of polynomial greatest common divisors, Journal of the ACM 18(4), 1971
    locator: pp. 478 to 504
  - paper: doi:10.1016/S0022-4049(98)00081-4
    title: Lionel Ducos, Optimizations of the subresultant algorithm, Journal of Pure and Applied Algebra 145(2), 2000
    locator: pp. 149 to 163
---

The subresultant gcd algorithm computes the [gcd](/polynomial-gcd/) of two polynomials with integer coefficients, or more generally over a unique factorization domain, by the Euclidean algorithm with [pseudo-division](/pseudo-division/), and divides each pseudo-remainder by a factor $\gamma h^{\delta}$ that is known in advance. The division is always exact, and the polynomials it produces are, up to sign, the [subresultants](/subresultant/) of the inputs. So their coefficients are determinants of the [Sylvester matrix](/sylvester-matrix/) and grow only linearly with the degree, not exponentially. It takes $O(m^2)$ ring operations for degree $m$ and needs no gcd of coefficients inside the loop.

## In plain words

The Euclidean algorithm over the integers makes fractions. Pseudo-division avoids fractions by multiplying by the top coefficient first, but then the numbers grow very fast, because each step multiplies again.

Most of this growth is a common factor that can be divided out. One way is to divide each remainder by the gcd of its coefficients, but that costs many integer gcds. The subresultant algorithm instead divides by a number that it computes from earlier top coefficients. A theorem of Collins, Brown and Traub says that this division is always exact. The numbers that remain are determinants of a matrix built from the input coefficients, so their size grows only slowly.

## The problem

Given $f, g \in \mathbb{Z}[x]$, compute $\gcd(f, g)$ in $\mathbb{Z}[x]$, normalized to a positive leading coefficient, with $\gcd(0, 0) = 0$. The same algorithm works over every unique factorization domain $R$, such as $\mathbb{Z}[y]$ or $F[y]$, with the normal form of the [content](/primitive-polynomial/) chosen in $R$. The cost model counts operations in $R$ at unit cost, including exact divisions, as in the algebraic model of [polynomial ring](/polynomial-ring/). Polynomials are dense coefficient arrays.

## The algorithm

```pseudo id=main
SUBRESULTANT-GCD(f, g)                     ▷ f, g in Z[x], or R[x] for a UFD R
L1  if deg f < deg g then swap f and g
L2  if g = 0 then return f, with a positive leading coefficient
L3  c ← gcd(cont f, cont g); A ← pp(f); B ← pp(g); γ ← 1; h ← 1
L4  loop
L5      δ ← deg A − deg B
L6      R ← prem(A, B)                         ▷ lc(B)^(δ+1) A = q B + R
L7      if R = 0 then return c · pp(B)
L8      if deg R = 0 then return c
L9      (A, B) ← (B, R / (γ h^δ))              ▷ the division is exact
L10     γ ← lc(A); h ← γ^δ / h^(δ − 1)         ▷ exact; h stays the same when δ = 0
```

Line L6 is [pseudo-division](/pseudo-division/). Line L9 divides each coefficient of $R$ by $\gamma h^{\delta}$, where $\gamma$ is the leading coefficient of the polynomial before $A$ and $h$ is computed in line L10 from earlier leading coefficients. In the normal case, where every $\delta$ after the first is $1$, line L10 gives $h = \gamma$, and the divisor in line L9 is $\gamma^2$ for every step after the second. Lines L3, L7 and L8 handle the [contents](/primitive-polynomial/): the gcd of $f$ and $g$ in $\mathbb{Z}[x]$ is the gcd of the contents times the gcd of the primitive parts. This is Cohen's form of the algorithm (Section 3.3).

## Example

Knuth's pair from Section 4.6.1:

$$u = x^8 + x^6 - 3x^4 - 3x^3 + 8x^2 + 2x - 5, \qquad v = 3x^6 + 5x^4 - 4x^2 - 9x + 21.$$

Both are primitive, so $c = 1$, $A = u$ and $B = v$.

| pass | $\delta$ | $\gamma$ | $h$ | $\gamma h^{\delta}$ | new $B$ |
|---|---|---|---|---|---|
| 1 | 2 | 1 | 1 | 1 | $-15x^4 + 3x^2 - 9$ |
| 2 | 2 | 3 | 9 | 243 | $65x^2 + 125x - 245$ |
| 3 | 2 | $-15$ | 25 | $-9375$ | $-9326x + 12300$ |
| 4 | 1 | 65 | 169 | 10985 | (line L8) |

In pass 2, the pseudo-remainder is $15795x^2 + 30375x - 59535$, and $243$ divides it exactly. In pass 4, the pseudo-remainder is the constant $2863877380 = 10985 \cdot 260708$, so line L8 returns $c = 1$: $u$ and $v$ are coprime. The sequence $v, -15x^4 + \ldots, 65x^2 + \ldots, -9326x + \ldots, 260708$ is, up to sign, Knuth's subresultant sequence for this pair. Over $\mathbb{Q}$, the Euclidean algorithm on the same pair ends with the fraction $-1288744821/543589225$; see [polynomial GCD](/polynomial-gcd/).

## Correctness

Two facts give correctness; the full proof is below.

1. **The degrees and the gcd are those of Euclid.** Over the fraction field $K$, $\operatorname{prem}(A, B)$ is a nonzero constant times $A \operatorname{rem} B$ (see [pseudo-division](/pseudo-division/)). So line L9 replaces $(A, B)$ by $(B, \text{a constant times } A \operatorname{rem} B)$, which keeps the common divisors in $K[x]$, and the degrees fall at each pass. When $R = 0$, $B$ is a gcd of $f$ and $g$ in $K[x]$; when $R$ is a nonzero constant, the gcd in $K[x]$ is $1$. By [Gauss's lemma](/gauss-lemma/), the gcd in $\mathbb{Z}[x]$ is then $c \cdot \operatorname{pp}(B)$ or $c$.
2. **The divisions are exact.** By the fundamental theorem of subresultants (Brown and Traub, 1971; von zur Gathen and Gerhard, Section 11.2), each new $B$ of line L9 equals, up to sign, the subresultant $S_{j}(\operatorname{pp} f, \operatorname{pp} g)$ with $j = \deg A - 1$ for the new $A$. The coefficients of a subresultant are determinants of integer matrices, so they lie in $\mathbb{Z}$, and the same theorem shows that each $h$ of line L10 lies in $\mathbb{Z}$; it is, up to sign, a leading coefficient of a subresultant.

## Complexity

The cost counts operations in $R$ at unit cost, including exact divisions. Let $m \ge n$ be the degrees, $n_1 = m$, $n_2 = n$, and $n_3 > n_4 > \cdots$ the degrees of the new $B$, with $\delta_i = n_i - n_{i+1}$.

- **The pseudo-divisions.** Pass $i$ divides a polynomial of degree $n_i$ by one of degree $n_{i+1}$, which costs $O((\delta_i + 1)(n_i + n_{i+1}))$ operations (see [pseudo-division](/pseudo-division/)). Since $n_i \le m$ and $\sum_i (\delta_i + 1) \le m + n + 1$, the total is $O(m(m + n)) = O(m^2)$.
- **The divisions and the powers.** Line L9 makes at most $n_{i+1}$ exact divisions per pass, and line L10 makes $O(\delta_i)$ multiplications and one division. Over all passes this is $O(m)$ besides the divisions of line L9, which add $O(n^2)$.
- **Contents.** Line L3 and the final primitive part take $O(m)$ gcds in $R$.
- **Space.** $O(m)$ elements of $R$.

The operation counts are proved. The sizes of the integers are what makes the method useful. Every new $B$ is, up to sign, a subresultant, and each of its coefficients is a determinant of order at most $m + n$ whose rows are coefficient vectors of $f$ and $g$; by the [Hadamard bound](/hadamard-bound/) it is at most $\|f\|_2^{\,n} \|g\|_2^{\,m}$ in absolute value. So for inputs with coefficients of $L$ digits, every member of the sequence has coefficients of $O(m (L + \log m))$ digits. With the plain Euclidean algorithm over $\mathbb{Q}$, or with pseudo-division and no reduction, the sizes can grow exponentially in the number of passes. Which of the subresultant algorithm, the [primitive PRS](/primitive-prs/) and the [modular algorithm](/brown-modular-gcd/) is fastest for given inputs is observed by measurement; for large dense inputs over $\mathbb{Z}$ the modular algorithm is usually faster in practice.

## Properties

- **Fraction-free.** All values stay in $R$; no content of a remainder is computed inside the loop.
- **The members are subresultants.** With the sign conventions of Collins and of Brown and Traub, the members of the sequence are exactly the subresultants $S_{n_i - 1}$; the variant here differs from them only in signs. In the normal case, where the degrees fall by one at each step and the last member has degree $0$, the last member is $\pm \operatorname{Res}(f, g)$, the [resultant](/resultant/); the variant that tracks the signs gives the resultant with its sign.
- **Compared with the primitive PRS.** On Knuth's pair, the [primitive PRS](/primitive-prs/) gives $5x^4 - x^2 + 3$, $13x^2 + 25x - 49$, $4663x - 6150$, $1$, with smaller numbers, but each step needs the content of the remainder, a gcd of all its coefficients. The subresultant sequence has larger numbers but no content computations.
- **Integral domains.** The sequence of line L9, without lines L3, L7 and L8, works over every integral domain, not only over a UFD. The exactness theorem needs only that $R$ is an integral domain.

## Variants and improvements

- **Subresultant PRS with exact signs.** Track the signs as Brown and Traub do, so that each member is exactly the subresultant. This gives the resultant and the subresultants themselves, as needed in [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) and in [Sturm sequences](/sturm-sequence/) over $\mathbb{Z}$; see [subresultant PRS](/subresultant-prs/).
- **Ducos' optimization.** Ducos (2000) computes the members after a degree gap of $\delta \ge 2$ with smaller intermediate values, avoiding the large power $h^{\delta}$.
- **Primitive PRS.** Replace the division by $\gamma h^{\delta}$ with the division by the content of $R$: smallest numbers, more gcds. See [primitive PRS](/primitive-prs/).
- **Modular gcd.** Compute the gcd modulo several primes and reconstruct: [Brown's modular gcd](/brown-modular-gcd/). It avoids the growth of intermediate values altogether.
- **Fast subresultants.** Over a field, all subresultants can be computed by a divide-and-conquer version of the Euclidean algorithm in $O(M(m) \log m)$ operations (von zur Gathen and Gerhard, Chapter 11).

## When to use it

Use it for gcds and resultants of polynomials over $\mathbb{Z}$, $\mathbb{Z}[y]$ or other domains without a fast modular method, for small and medium degrees, and whenever the subresultants themselves are needed. Use the [modular algorithm](/brown-modular-gcd/) for large dense inputs over $\mathbb{Z}$, and the plain [Euclidean algorithm](/polynomial-euclidean-algorithm/) over finite fields.

## Pitfalls

- **Order of updates.** In line L10, $\gamma$ is the leading coefficient of the new $A$, the old $B$, and $\delta$ is the value of line L5 for the pass that just ended. Mixing old and new values gives divisions that are not exact.
- **The power $h^{\delta - 1}$.** For $\delta = 0$ it is $h^{-1}$, and the formula $h^{1 - \delta} \gamma^{\delta}$ gives $h$ again. Code that computes $\gamma^{\delta} / h^{\delta - 1}$ literally must treat $\delta = 0$ apart.
- **Inexact division as a bug detector.** If a division in line L9 or L10 leaves a remainder, the code is wrong. Make the exact division raise an error rather than round.
- **Contents.** The algorithm is correct without taking primitive parts at line L3, but then the contents of $f$ and $g$ enter the subresultants and the numbers are larger. The output must still be multiplied by the gcd of the contents.
- **Signs.** The sequence of this page differs from the true subresultants by signs. For resultants and Sturm sequences use the signed version.
- **Over a field.** The algorithm works, but it does useless multiplications; use the Euclidean algorithm with monic remainders.

## Implementations

## History

Collins (1967) introduced the subresultant remainder sequence and showed that its coefficients stay small. Brown (1971) and Brown and Traub (1971) gave the fundamental theorem of subresultants, which explains the exact divisions and covers the case of degree gaps. Knuth, Section 4.6.1, presents the subresultant gcd algorithm over a unique factorization domain, and Ducos (2000) later reduced the size of the intermediate values.

## References
