---
tag: NTQA57
kind: problem
slug: polynomial-division
name: Polynomial division
aliases:
- division with remainder
- polynomial division with remainder
area: algebra/polynomial-arithmetic
level: intro
summary: Given f and nonzero g, find q and r with f = qg + r and deg r < deg g.
model: blum-shub-smale-machine
complexity:
  vars: {m: the degree of the dividend f, n: the degree of the divisor g, M: the multiplication time (M(k) operations to multiply two polynomials of degree less than k)}
  time: {worst: O(M(m))}
prereqs: [polynomial-ring, polynomial-degree, polynomial-multiplication]
see_also: [polynomial-long-division, fast-polynomial-division, pseudo-division, polynomial-remainder-theorem, power-series-inversion, polynomial-euclidean-algorithm, monic-polynomial, division-with-remainder]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 2.4, Division with remainder (pp. 37 to 41), and Section 9.1, Division with remainder using Newton iteration (pp. 257 to 264)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of Polynomials
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.4, Division (the integer analogues, with 1.4.4 on Newton's method and 1.4.8 on Hensel's division)
  - paper: "arXiv:cs/0301016"
    title: Peter Bürgisser and Martin Lotz, Lower bounds on the bounded coefficient complexity of bilinear maps, Journal of the ACM 51(3), 2004
    locator: pp. 464 to 482 (the Omega(n log n) bound for division with remainder in bounded coefficient circuits)
---

Polynomial division is the problem of writing a polynomial $f$ as $f = qg + r$ for a given nonzero divisor $g$, with a remainder $r$ of degree less than $\deg g$. It has a unique solution when the leading coefficient of $g$ is a unit of the coefficient ring $R$, in particular for every nonzero $g$ over a field. [Long division](/polynomial-long-division/) solves it with $O((m - n + 1) n)$ operations in $R$, and [Newton iteration](/fast-polynomial-division/) with $O(M(m))$, the cost of one [multiplication](/polynomial-multiplication/). Division is the step of the [Euclidean algorithm](/polynomial-euclidean-algorithm/), of arithmetic in $F[x]/(g)$ and of evaluation.

## In plain words

Dividing one polynomial by another works like dividing one number by another at school. You look at the highest term of what is left, find the term that makes the divisor match it, write that term into the answer and subtract. Each round removes the highest term, so what is left gets shorter. You stop when it is shorter than the divisor. What is left then is the remainder.

The method needs one thing: you must be able to divide by the top number of the divisor. With fractions or with arithmetic modulo a prime this always works. With whole numbers it works only when the top number of the divisor is one or minus one. For other cases there is a variant that first multiplies the dividend by a suitable number.

## Definition

**Input.** A commutative ring $R$ with $1$, a polynomial $f \in R[x]$, and a nonzero $g \in R[x]$ whose leading coefficient $\operatorname{lc}(g)$ is a unit of $R$. Write $m = \deg f$ and $n = \deg g$.

**Output.** Polynomials $q, r \in R[x]$ with

$$f = q g + r \qquad\text{and}\qquad \deg r < \deg g .$$

We write $q = f \operatorname{quo} g$ and $r = f \operatorname{rem} g$ (or $f \bmod g$). Then $q = 0$ when $m < n$, and $\deg q = m - n$ otherwise (rule 3 of [degree of a polynomial](/polynomial-degree/)).

**Existence.** By strong induction on $\deg f$. If $\deg f < n$, take $q = 0$ and $r = f$. Otherwise let $c = \operatorname{lc}(f)\operatorname{lc}(g)^{-1}$ and $f_1 = f - c\, x^{m - n} g$. The coefficient of $x^m$ in $f_1$ is $\operatorname{lc}(f) - c \operatorname{lc}(g) = 0$, so $\deg f_1 < m$. By the hypothesis, $f_1 = q_1 g + r$ with $\deg r < n$, and then $f = (q_1 + c x^{m-n}) g + r$. $\square$

**Uniqueness.** Let $qg + r = q'g + r'$ with $\deg r, \deg r' < n$. Then $(q - q') g = r' - r$. If $q \ne q'$, the left side has degree $\deg(q - q') + n \ge n$, because $\operatorname{lc}(g)$ is a unit and so not a zero divisor; but the right side has degree less than $n$. So $q = q'$, and then $r = r'$. $\square$

**When $\operatorname{lc}(g)$ is not a unit.** A solution can fail to exist. In $\mathbb{Z}[x]$, take $f = x^2$ and $g = 2x$: any $q$ with $\deg(x^2 - 2xq) < 1$ needs $2 \operatorname{lc}(q) = 1$, which has no solution in $\mathbb{Z}$. The uniqueness proof still works when $\operatorname{lc}(g)$ is not a zero divisor. Over an integral domain, [pseudo-division](/pseudo-division/) divides $\operatorname{lc}(g)^{m - n + 1} f$ by $g$ instead, which always succeeds.

**Cost.** Operations in $R$ at unit cost, and one inversion of $\operatorname{lc}(g)$, as in [polynomial ring](/polynomial-ring/). $M(n)$ is the cost of multiplying two polynomials of degree less than $n$.

## Variants

- **Remainder only, or quotient only.** $f \operatorname{rem} g$ is the reduction in $R[x]/(g)$, the step of modular arithmetic and of the Euclidean algorithm. The quotient alone is the top part of $f/g$ and needs only the top $m - n + 1$ coefficients of $f$.
- **Exact division.** It is known that $g \mid f$, so $r = 0$. The quotient can be computed from the low end, as $f \cdot g^{-1} \bmod x^{m - n + 1}$ when $g(0)$ is a unit, which is the polynomial form of Hensel's division.
- **Division by a linear polynomial.** $g = x - a$. Then $r = f(a)$ by the [remainder theorem](/polynomial-remainder-theorem/), and the quotient comes from [Horner's rule](/horner-rule/) (synthetic division) with $m$ multiplications and $m$ additions.
- **Many divisions by one fixed $g$.** Precompute the inverse of $\operatorname{rev}_n(g)$ modulo $x^{m - n + 1}$ once; then each division costs two multiplications. This is the polynomial form of Barrett reduction.
- **Pseudo-division.** Over an integral domain $D$ that is not a field, compute $\operatorname{lc}(g)^{m-n+1} f = qg + r$ with $q, r \in D[x]$. See [pseudo-division](/pseudo-division/).
- **Power series division.** $f/g$ in $R[[x]]$ to precision $x^k$, when $g(0)$ is a unit: [power series inversion](/power-series-inversion/) and one product.
- **Several variables.** Division by a set of polynomials with respect to a monomial order; the remainder is unique only for a Gröbner basis. See the [multivariate division algorithm](/multivariate-division-algorithm/).

## Examples

- **Over $\mathbb{Q}$ with a monic divisor.** $f = 2x^4 + 3x^3 - x + 5$ and $g = x^2 + x + 1$ give $q = 2x^2 + x - 3$ and $r = x + 8$. Check: $(2x^2 + x - 3)(x^2 + x + 1) = 2x^4 + 3x^3 - 2x - 3$, and adding $x + 8$ gives $f$.
- **Over $\mathbb{F}_7$ with a non-monic divisor.** $f = 4x^5 + x^4 + 3x^2 + 1$ and $g = 2x^2 + 3$. Here $\operatorname{lc}(g)^{-1} = 2^{-1} = 4$. The result is $q = 2x^3 + 4x^2 + 4x + 6$ and $r = 2x + 4$.
- **A divisor of larger degree.** $f = x + 1$ and $g = x^3$: $q = 0$ and $r = x + 1$.
- **A constant divisor.** $g = 3$ over $\mathbb{Q}$: $q = f/3$ and $r = 0$, since $\deg r < 0$ forces $r = 0$.
- **No solution over $\mathbb{Z}$.** $x^2$ divided by $2x$ has no solution in $\mathbb{Z}[x]$, as shown above. Over $\mathbb{Q}$ the answer is $q = x/2$, $r = 0$.
- **CRC checksums.** A cyclic redundancy check of a message of bits $b_0, \ldots, b_{k-1}$ is the remainder of $x^n \sum b_i x^i$ divided by a fixed generator polynomial of degree $n$ over $\mathbb{F}_2$.

## Known algorithms

| algorithm | operations in $R$ | notes |
|---|---|---|
| [Long division](/polynomial-long-division/) | $(2n + 1)(m - n + 1)$ at most, plus one inversion | the school method; best for small degrees or small $m - n$ |
| [Fast division](/fast-polynomial-division/) by Newton iteration | $O(M(m))$ | uses [power series inversion](/power-series-inversion/) of $\operatorname{rev}_n(g)$ |
| [Horner's rule](/horner-rule/) for $g = x - a$ | $m$ multiplications and $m$ additions | synthetic division |
| [Pseudo-division](/pseudo-division/) | $O((m - n + 1) n)$ in an integral domain | no inversions; coefficients grow |

The count for long division: the quotient has $m - n + 1$ coefficients; each one costs one multiplication by $\operatorname{lc}(g)^{-1}$ and then $n$ multiplications and $n$ subtractions to update the remainder below the cancelled top term. These bounds are proved. Which method is faster for a given size is observed in practice, and the crossover from long division to Newton division depends on the ring, the multiplication algorithm and the machine.

## Bounds

- **Upper bound.** $O(M(m))$ operations in $R$, so $O(m \log m \log \log m)$ over any ring with the method of Cantor and Kaltofen, and $O(m \log m)$ when $R$ supports the FFT. The constant in front of $M$ for Newton division is analysed in von zur Gathen and Gerhard, Section 9.1.
- **Lower bound.** $\Omega(m)$ in general, since the remainder depends on every coefficient of $f$. In bounded coefficient circuits over $\mathbb{C}$, Bürgisser and Lotz (2004) proved an $\Omega(n \log n)$ bound for division with remainder of polynomials of degree $O(n)$.

## Reductions

- **To power series inversion.** Substitute $x \mapsto 1/x$ and multiply by $x^m$: $\operatorname{rev}_m(f) = \operatorname{rev}_{m-n}(q)\operatorname{rev}_n(g) + x^{m-n+1}\operatorname{rev}_{n-1}(r)$. So $\operatorname{rev}_{m-n}(q) = \operatorname{rev}_m(f) \cdot \operatorname{rev}_n(g)^{-1} \bmod x^{m-n+1}$, an inversion of a power series whose constant term $\operatorname{lc}(g)$ is a unit. Then $r = f - qg$ costs one more product. This is the method of [fast polynomial division](/fast-polynomial-division/).
- **Evaluation reduces to division.** $f(a) = f \operatorname{rem} (x - a)$, and [multipoint evaluation](/multipoint-evaluation/) reduces $f$ modulo the products in a [subproduct tree](/subproduct-tree/).
- **Gcd reduces to a sequence of divisions.** The [Euclidean algorithm](/polynomial-euclidean-algorithm/) is a sequence of divisions with remainder.

## Applications

- Arithmetic in $F[x]/(g)$: the finite fields $\mathbb{F}_{p^k} = \mathbb{F}_p[x]/(g)$ for an [irreducible](/irreducible-polynomial/) $g$ of degree $k$, used in AES (over $\mathbb{F}_2$, degree 8) and in elliptic curve cryptography over binary fields.
- The [Euclidean algorithm](/polynomial-euclidean-algorithm/), [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/) and [gcd](/polynomial-gcd/).
- Evaluation of a polynomial at a point and at many points.
- Error-detecting and error-correcting codes: CRC checksums, and the encoding of cyclic codes such as BCH and Reed-Solomon codes.
- The factorization algorithms over finite fields, which compute powers $x^{q^i} \bmod f$.

## References
