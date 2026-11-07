---
tag: BAZVCR
kind: theorem
slug: polynomial-remainder-theorem
name: Polynomial remainder theorem
aliases:
- remainder theorem
- little Bezout theorem
area: algebra/polynomial-arithmetic
level: intro
summary: The remainder of f divided by x - a is f(a).
prereqs: [polynomial-division, polynomial-degree]
see_also: [factor-theorem, horner-rule, polynomial-long-division, polynomial-evaluation, multipoint-evaluation, chinese-remainder-theorem, lagrange-interpolation, subproduct-tree]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.2, Evaluation and interpolation (evaluation at u is the remainder modulo x - u), and Section 9.2, Generalized Taylor expansion and radix conversion (p. 264)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of Polynomials (Horner's rule gives the quotient by x - x0 as a by-product, and the history of the rule)
---

The polynomial remainder theorem says that dividing a polynomial $f$ by $x - a$ leaves the remainder $f(a)$. It holds over every commutative ring $R$, so evaluation at a point and division by a linear polynomial are the same operation. The quotient comes out of [Horner's rule](/horner-rule/) at no extra cost, and the [factor theorem](/factor-theorem/) is the special case $f(a) = 0$. The same idea with $x - a$ replaced by a product of linear factors is the base of [multipoint evaluation](/multipoint-evaluation/).

## Statement

Let $R$ be a commutative ring with $1$, let $f = \sum_{i=0}^{n} a_i x^i \in R[x]$, and let $a \in R$.

**Theorem.** There is a unique $q \in R[x]$ with

$$f = (x - a)\, q + f(a).$$

So $f \operatorname{rem} (x - a) = f(a)$. If $n \ge 1$ and $a_n \ne 0$, then $\deg q = n - 1$, and the coefficients of $q = \sum_{i=0}^{n-1} b_i x^i$ are

$$b_{n-1} = a_n, \qquad b_{i-1} = a_i + a\, b_i \quad (i = n - 1, \ldots, 1), \qquad f(a) = a_0 + a\, b_0 .$$

**Taylor form.** More generally, for each $k \ge 1$ the remainder of $f$ modulo $(x - a)^k$ is $\sum_{i=0}^{k-1} c_i (x - a)^i$, where $f = \sum_{i=0}^{n} c_i (x - a)^i$ is the expansion of $f$ at $a$. The theorem is the case $k = 1$, since $c_0 = f(a)$. When $n!$ is a unit in $R$, for example over $\mathbb{Q}$, $c_i = f^{(i)}(a)/i!$; in particular $f \operatorname{rem} (x - a)^2 = f(a) + f'(a)(x - a)$ over every commutative ring, since $c_1 = f'(a)$ always.

## In plain words

To find the value of a polynomial at a number, you can divide the polynomial by "the unknown minus that number". The part left over is exactly the value. The other way round also works: to divide by "the unknown minus a number", you can run the usual quick method of evaluation and keep the numbers it makes on the way. They are the coefficients of the quotient.

So the value at a number is zero exactly when the division leaves nothing over. This is the usual test for whether a number is a root.

## Proof

**Existence.** For each $i \ge 1$,

$$x^i - a^i = (x - a)\,(x^{i-1} + a x^{i-2} + \cdots + a^{i-1}),$$

which follows by expanding the right side: the terms telescope. Hence

$$f - f(a) = \sum_{i=1}^{n} a_i (x^i - a^i) = (x - a) \sum_{i=1}^{n} a_i \sum_{j=0}^{i-1} a^{i-1-j} x^j ,$$

and $q = \sum_{i=1}^{n} a_i \sum_{j=0}^{i-1} a^{i-1-j} x^j$ works.

**Uniqueness.** The divisor $x - a$ is monic, so by the uniqueness part of [polynomial division](/polynomial-division/) there is only one pair $(q, r)$ with $f = (x - a) q + r$ and $\deg r < 1$. The constant $f(a)$ has degree less than $1$, so it is that $r$.

**A second proof of $r = f(a)$.** Divide: $f = (x - a) q + r$ with $r \in R$. Since $R$ is commutative, evaluation at $a$ is a ring homomorphism $R[x] \to R$, so $f(a) = (a - a)\, q(a) + r = r$.

**The coefficients of $q$.** The coefficient of $x^j$ in $q$ is $b_j = \sum_{i = j+1}^{n} a_i a^{i-1-j}$. So $b_{n-1} = a_n$, and for $1 \le j \le n - 1$, $b_{j-1} = a_j + \sum_{i=j+1}^{n} a_i a^{i-j} = a_j + a\, b_j$. Finally $a_0 + a\, b_0 = a_0 + \sum_{i=1}^{n} a_i a^i = f(a)$. The degree of $q$ is $n - 1$ because $b_{n-1} = a_n \ne 0$.

**The Taylor form.** The polynomials $(x - a)^i$ are monic of degree $i$, so by induction on $n$ every $f$ of degree $n$ has a unique expansion $f = \sum_{i=0}^{n} c_i (x - a)^i$: take $c_n = a_n$ and expand $f - a_n (x - a)^n$, which has degree less than $n$. The terms with $i \ge k$ are multiples of $(x - a)^k$, and the rest has degree less than $k$, so it is the remainder modulo the monic $(x - a)^k$. Differentiating the expansion $i$ times and setting $x = a$ gives $f^{(i)}(a) = i!\, c_i$, which yields $c_1 = f'(a)$ always and $c_i = f^{(i)}(a)/i!$ when $i!$ is a unit. $\blacksquare$

## Consequences

**Examples.** Let $f = 2x^4 + 3x^3 - x + 5$ over $\mathbb{Z}$.

| divisor | quotient | remainder | how |
|---|---|---|---|
| $x - 2$ | $2x^3 + 7x^2 + 14x + 27$ | $59 = f(2)$ | $b_3 = 2$, $b_2 = 3 + 2 \cdot 2$, $b_1 = 0 + 2 \cdot 7$, $b_0 = -1 + 2 \cdot 14$, $f(2) = 5 + 2 \cdot 27$ |
| $x + 1$ | $2x^3 + x^2 - x$ | $5 = f(-1)$ | the same recurrence with $a = -1$ |
| $(x - 2)^2$ | $2x^2 + 11x + 36$ | $99x - 139 = 59 + 99(x - 2)$ | Taylor form, $f'(2) = 99$ |
| $(x - 2)(x + 1)$ | $2x^2 + 5x + 9$ | $18x + 23$ | the line through $(2, 59)$ and $(-1, 5)$ |

Over $\mathbb{F}_7$ the same $f$ has $f \operatorname{rem} (x - 2) = 59 \bmod 7 = 3$.

- **Factor theorem.** $(x - a) \mid f$ exactly when $f(a) = 0$. This is the [factor theorem](/factor-theorem/), and with it a nonzero polynomial over an integral domain has at most $\deg f$ roots (rule 6 of [degree of a polynomial](/polynomial-degree/)).
- **Synthetic division.** The recurrence $b_{i-1} = a_i + a\, b_i$ is [Horner's rule](/horner-rule/). So one pass of $n$ multiplications and $n$ additions gives both $f(a)$ and $f / (x - a)$. This is the step that deflates a root in [root finding](/polynomial-root-finding/).
- **Evaluation is reduction.** The map $f \mapsto f(a)$ is the map $R[x] \to R[x]/(x - a) \cong R$. For distinct points $u_0, \ldots, u_{n-1}$ in a field, $f \operatorname{rem} \prod_j (x - u_j)$ determines all the values $f(u_j)$, and the [Chinese remainder theorem](/chinese-remainder-theorem/) for $F[x]$ makes this a bijection with $F^n$. [Multipoint evaluation](/multipoint-evaluation/) and [fast interpolation](/fast-interpolation/) work on this isomorphism with a [subproduct tree](/subproduct-tree/); the last row of the table is the case of two points, where the remainder is the [Lagrange interpolant](/lagrange-interpolation/).
- **Differences of values.** For $f \in \mathbb{Z}[x]$ and integers $a, b$: $f(b) - f(a) = (b - a)\, q(b)$ with $q \in \mathbb{Z}[x]$, so $b - a$ divides $f(b) - f(a)$. In the example, $f(2) - f(-1) = 54$ is a multiple of $3$. The same argument gives $f(b) \equiv f(a) \pmod m$ whenever $b \equiv a \pmod m$.
- **Remainders modulo powers.** $f \operatorname{rem} (x - a)^2 = f(a) + f'(a)(x - a)$, so $a$ is a multiple root of $f$ exactly when $f(a) = f'(a) = 0$. This is the base of the test for [square-free polynomials](/square-free-polynomial/).

## Tightness

- **The divisor must be monic, or have a unit leading coefficient.** Over a field, $f \operatorname{rem} (bx - a) = f(a/b)$ for $b \ne 0$, by the theorem applied to $x - a/b$. Over $\mathbb{Z}$ the division by $2x - 1$ need not exist, as for $f = x$; [pseudo-division](/pseudo-division/) gives $2^{n} f = (2x - 1) q + 2^{n} f(1/2)$ instead, with $2^n f(1/2) \in \mathbb{Z}$.
- **Commutativity is used in the second proof.** Over a ring that is not commutative, evaluation $f(a) = \sum a_i a^i$ is not a ring homomorphism. The first proof still gives $f = q\,(x - a) + f(a)$, with the factor $x - a$ on the right. But a left factor does not give a root: over the quaternions, $f = (x - i)\, j = j x - k$ has $f(i) = j i - k = -2k \ne 0$.
- **The Taylor coefficients need $i!$ to be a unit.** Over $\mathbb{F}_p$, $f^{(p)} = 0$ for every $f$, so $c_p$ is not $f^{(p)}(a)/p!$. The expansion and the Taylor form of the remainder still hold; only the formula through derivatives fails. Hasse derivatives, or the radix conversion of von zur Gathen and Gerhard, Section 9.2, compute the $c_i$ in every characteristic.

## History

The scheme that computes $q$ and $f(a)$ together is known as Ruffini's rule, after Paolo Ruffini (1804), and as the core of Horner's method (1819). Knuth, Section 4.6.4, discusses Horner's rule, its use to divide by $x - x_0$, and its history.

## References
