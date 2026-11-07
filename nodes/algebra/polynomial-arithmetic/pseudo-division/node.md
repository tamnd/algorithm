---
tag: XBNRYF
kind: algorithm
slug: pseudo-division
name: Pseudo-division
aliases:
- pseudo-remainder
- pseudo-quotient
- prem
area: algebra/polynomial-arithmetic
level: advanced
summary: Division over an integral domain after multiplying f by a power of the leading coefficient, avoiding fractions.
solves: [polynomial-division]
model: blum-shub-smale-machine
complexity:
  vars: {m: the degree of the dividend f, n: the degree of the divisor g}
  time: {worst: Θ((m - n + 1) (m + n))}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [polynomial-long-division, primitive-polynomial]
see_also: [polynomial-long-division, primitive-prs, subresultant-prs, subresultant-gcd, polynomial-division, primitive-polynomial, resultant, bareiss-algorithm]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of Polynomials (Algorithm R, pseudo-division of polynomials, and its use in the gcd algorithms over a unique factorization domain)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 6.12, Pseudodivision and primitive Euclidean Algorithms (p. 190)
  - paper: doi:10.1145/321371.321381
    title: George E. Collins, Subresultants and reduced polynomial remainder sequences, Journal of the ACM 14(1), 1967
    locator: pp. 128 to 142 (remainder sequences built from pseudo-remainders)
  - paper: doi:10.1145/321662.321664
    title: W. S. Brown, On Euclid's algorithm and the computation of polynomial greatest common divisors, Journal of the ACM 18(4), 1971
    locator: pp. 478 to 504
---

Pseudo-division divides a polynomial $f$ by a polynomial $g \ne 0$ over a commutative ring $R$ in which the leading coefficient $\ell = \operatorname{lc}(g)$ need not be invertible. It returns $q, r \in R[x]$ with $\ell^{m - n + 1} f = q g + r$ and $\deg r < n$, where $m = \deg f \ge n = \deg g$, and it uses only additions, subtractions and multiplications in $R$. Over $\mathbb{Z}$ it gives the remainder of $f$ by $g$ without fractions, multiplied by a known factor. It is the step of the fraction-free [primitive](/primitive-prs/) and [subresultant](/subresultant-prs/) remainder sequences.

## In plain words

Long division of polynomials needs to divide by the top coefficient of the divisor. With integer coefficients, that division is often not exact, and fractions appear.

Pseudo-division avoids this. Before each step, it multiplies everything by the top coefficient of the divisor. Then the next quotient term needs no division: the top coefficient of the running remainder can be used as it is. After all steps, the original polynomial has been multiplied by a known power of the top coefficient, and the result is a quotient and a remainder for this multiple. If you divide the result by the same power, you get the usual quotient and remainder over the fractions. All the numbers stay integers.

## The problem

Let $R$ be a commutative ring, and let $f, g \in R[x]$ with $g \ne 0$, $m = \deg f$, $n = \deg g$ and $\ell = \operatorname{lc}(g)$. Let $\delta = \max(m - n + 1, 0)$. Compute $q, r \in R[x]$ with

$$\ell^{\delta} f = q g + r, \qquad \deg r < n.$$

$q$ is the *pseudo-quotient* $\operatorname{pquo}(f, g)$ and $r$ is the *pseudo-remainder* $\operatorname{prem}(f, g)$. If $\ell$ is not a zero divisor, for example if $R$ is an integral domain, then $q$ and $r$ are unique (see Properties). Polynomials are dense coefficient arrays, lowest degree first, as in [long division](/polynomial-long-division/).

## The algorithm

```pseudo id=main
PSEUDO-DIVIDE(f, g)                        ▷ R a commutative ring; m = deg f, n = deg g
L1  if g = 0 then error
L2  if m < n then return (0, f)
L3  ℓ ← lc(g); r ← a copy of f; d ← m − n
L4  for k ← d down to 0 do
L5      t[k] ← r[n + k]                     ▷ the top coefficient, used as it is
L6      for j ← 0 to n + k − 1 do r[j] ← ℓ · r[j]
L7      for j ← 0 to n − 1 do r[j + k] ← r[j + k] − t[k] · g[j]
L8      r[n + k] ← 0                        ▷ ℓ · t[k] − t[k] · ℓ = 0
L9  q[k] ← t[k] · ℓ^k for k = 0, …, d       ▷ the powers of ℓ computed one after the other
L10 return (q, r[0 .. n − 1]), with zero top coefficients stripped
```

At step $k$, lines L6 to L8 replace $r$ by $\ell r - t_k x^k g$. Line L6 multiplies all coefficients below position $n + k$ by $\ell$, and line L7 subtracts $t_k x^k g$, whose top coefficient $t_k \ell$ cancels $\ell \cdot r[n + k]$. Line L8 writes this zero without computing it. The coefficient $t_k$ found at step $k$ is multiplied by $\ell$ in each of the $k$ later steps, so its final value in $q$ is $t_k \ell^k$, which line L9 computes once at the end. This is Knuth's Algorithm R in Section 4.6.1.

## Example

Over $\mathbb{Z}$, take Knuth's pair from Section 4.6.1:

$$f = x^8 + x^6 - 3x^4 - 3x^3 + 8x^2 + 2x - 5, \qquad g = 3x^6 + 5x^4 - 4x^2 - 9x + 21.$$

Here $m = 8$, $n = 6$, $d = 2$, $\ell = 3$ and $\ell^{d + 1} = 27$.

| $k$ | $t_k$ | $r$ after lines L6 to L8 |
|---|---|---|
| 2 | $1$ | $-2x^6 - 5x^4 + 3x^2 + 6x - 15$ |
| 1 | $0$ | $-6x^6 - 15x^4 + 9x^2 + 18x - 45$ |
| 0 | $-6$ | $-15x^4 + 3x^2 - 9$ |

Line L9 gives $q = 1 \cdot 3^2\, x^2 + 0 \cdot 3\, x + (-6) = 9x^2 - 6$. So $27 f = (9x^2 - 6)\, g + (-15x^4 + 3x^2 - 9)$. Over $\mathbb{Q}$, the ordinary remainder is $f \operatorname{rem} g = -\tfrac59 x^4 + \tfrac19 x^2 - \tfrac13$, and $27$ times it is the pseudo-remainder, as Properties states. Step $k = 1$ found $t_1 = 0$ and only multiplied $r$ by $3$; the variant that skips such steps would return $-5x^4 + x^2 - 3$ with the factor $\ell^2 = 9$ in place of $27$.

## Correctness

The proof is a [loop invariant](/loop-invariant/). Before step $k$ of line L4, write $Q_k = \sum_{i > k} t_i \ell^{i - k - 1} x^i$ for the quotient so far, scaled to the current step. Then

$$\ell^{d - k} f = Q_k\, g + r \quad\text{and}\quad r[j] = 0 \text{ for } j > n + k.$$

It holds before the first step, with $k = d$, $Q_d = 0$ and $r = f$ of degree $m = n + d$. Step $k$ multiplies both sides by $\ell$ and moves $t_k x^k g$ from $r$ to the quotient, which keeps the equation and makes $r[n + k] = 0$. After step $0$, $\ell^{d + 1} f = (\sum_i t_i \ell^i x^i)\, g + r$ with $\deg r < n$, which is the output of lines L9 and L10. The full proof is below.

## Complexity

The cost counts ring operations at unit cost, as in [polynomial ring](/polynomial-ring/). Let $d = m - n \ge 0$.

- **The loop.** Step $k$ makes $n + k$ multiplications in line L6, and $n$ multiplications and $n$ subtractions in line L7. Over all steps this is $\sum_{k=0}^{d} (2n + k) = (d + 1)\, 2n + d(d + 1)/2$ multiplications and $(d + 1)\, n$ subtractions.
- **The quotient.** Line L9 makes $d - 1$ multiplications for $\ell^2, \ldots, \ell^d$ and $d$ for the products, so fewer than $2d$.
- **Total.** At most $(d + 1)(3n + d/2) + 2d$ operations and no inversion, which is $\Theta((m - n + 1)(m + n))$. When $m \le 2n$, as in every step of a remainder sequence after the first, this is $O((m - n + 1)\, n)$, the order of [long division](/polynomial-long-division/), which uses at most $(2n + 1)(m - n + 1)$ operations and one inversion.
- **Space.** $O(m)$ for $r$, $t$ and $q$.
- **Bit cost over $\mathbb{Z}$.** The operation counts hide the growth of the integers. Write $\|h\|$ for the largest absolute value of a coefficient of $h$. Step $k$ replaces $r$ by $\ell r - t_k x^k g$ with $|t_k| \le \|r\|$, so $\|r\|$ grows at most by the factor $|\ell| + \|g\| \le 2 \|g\|$ per step, and $\|\operatorname{prem}(f, g)\| \le \|f\|\, (2 \|g\|)^{d + 1}$. The digits of the remainder are thus at most those of $f$ plus $d + 1$ times those of $2 \|g\|$. In a remainder sequence this growth compounds from step to step, which is why the [primitive](/primitive-prs/) and [subresultant](/subresultant-prs/) sequences divide out known factors after each pseudo-division.

The operation counts are proved. The relative speed of pseudo-division and of division over $\mathbb{Q}$ on real inputs is observed by measurement, and depends on the sizes of the coefficients.

## Properties

- **No inversions.** The algorithm works over every commutative ring, including $\mathbb{Z}$, $\mathbb{Z}[y]$ and rings with zero divisors, such as $\mathbb{Z}/8\mathbb{Z}$. The identity $\ell^{\delta} f = q g + r$ with $\deg r < n$ always holds.
- **Uniqueness.** If $\ell$ is not a zero divisor, then $q$ and $r$ are unique. *Proof.* If $\ell^{\delta} f = q g + r = q' g + r'$, then $(q - q') g = r' - r$ has degree less than $n$. Since $\ell$ is not a zero divisor, $\deg ((q - q') g) = \deg(q - q') + n$ when $q \ne q'$, which is at least $n$. So $q = q'$ and then $r = r'$. $\square$
- **Relation to division over the fraction field.** If $R$ is an integral domain with fraction field $K$, then $\operatorname{pquo}(f, g) = \ell^{\delta} (f \operatorname{quo} g)$ and $\operatorname{prem}(f, g) = \ell^{\delta} (f \operatorname{rem} g)$, where the right sides are the quotient and remainder in $K[x]$. *Proof.* Multiply $f = (f \operatorname{quo} g)\, g + f \operatorname{rem} g$ by $\ell^{\delta}$ and use uniqueness in $K[x]$. $\square$ In particular $\operatorname{prem}(f, g)$ and $f \operatorname{rem} g$ differ by a nonzero constant, so they have the same roots and the same gcd with $g$ up to a unit of $K$.
- **Monic divisors.** If $\ell = 1$, pseudo-division is ordinary [long division](/polynomial-long-division/).
- **Divisibility.** Over an integral domain, $g$ divides $\ell^{\delta} f$ in $R[x]$ exactly when $\operatorname{prem}(f, g) = 0$. So $\operatorname{prem}(f, g) = 0$ shows that $g$ divides $f$ in $K[x]$, but not always in $R[x]$: $\operatorname{prem}(x, 2x) = 0$ over $\mathbb{Z}$, and $2x$ does not divide $x$ in $\mathbb{Z}[x]$.

## Variants and improvements

- **Sparse pseudo-division.** Multiply by $\ell$ only at the steps where $t_k \ne 0$. The result satisfies $\ell^{e} f = q g + r$, where $e \le \delta$ is the number of nonzero quotient coefficients, and the remainder is smaller by the factor $\ell^{\delta - e}$. The example above shows the saving.
- **Lazy scaling.** The coefficients of $r$ below position $k$ are only multiplied by $\ell$ at step $k$. Multiplying each coefficient once by the right power of $\ell$ when it first enters the window $r[k .. n + k]$ lowers the cost to $O((m - n + 1)\, n + m)$, the cost of long division.
- **Division over the fraction field.** Over $\mathbb{Q}$ or $\mathbb{Q}(y)$, compute $f \operatorname{rem} g$ with fractions and multiply by $\ell^{\delta}$. This gives the same result, but the intermediate fractions need gcd computations to stay reduced.
- **Remainder sequences.** The [primitive PRS](/primitive-prs/) takes the [primitive part](/primitive-polynomial/) of each pseudo-remainder. The [subresultant PRS](/subresultant-prs/) divides each pseudo-remainder by a factor known in advance, which keeps the coefficients of the size of [subresultants](/subresultant/) without content computations. See [subresultant gcd](/subresultant-gcd/).
- **Fast pseudo-division.** Since $\operatorname{pquo}(f, g) = \ell^{\delta} (f \operatorname{quo} g)$, [fast division](/fast-polynomial-division/) over the fraction field $K$, followed by a multiplication by $\ell^{\delta}$, gives the pseudo-quotient in $O(M(m))$ operations in $K$.

## When to use it

Use pseudo-division when the coefficients lie in an integral domain that is not a field, such as $\mathbb{Z}$ or a polynomial ring $\mathbb{Z}[y]$, and the next step only needs the remainder up to a constant factor: gcd computations by remainder sequences, [resultants](/resultant/), and Sturm-type sequences. Use plain [long division](/polynomial-long-division/) over a field or when $g$ is monic. For gcds of large polynomials over $\mathbb{Z}$, [modular methods](/brown-modular-gcd/) are usually faster in practice than any remainder sequence.

## Pitfalls

- **Using prem as a remainder in $R[x]$.** $\operatorname{prem}(f, g) = 0$ does not mean that $g$ divides $f$ in $R[x]$; it means that $g$ divides $\ell^{\delta} f$. Test exact divisibility with an exact division in $R$.
- **The factor in the identity.** Different texts use $\ell^{m - n + 1}$ or the sparse exponent $e$. Code that combines pseudo-remainders, such as the subresultant algorithm, must use the same convention as its proof.
- **Signs.** For [Sturm sequences](/sturm-sequence/) the sign of the remainder matters. $\ell^{\delta}$ is negative when $\ell < 0$ and $\delta$ is odd, which flips the sign of the remainder. Use $|\ell|^{\delta}$, or check the sign.
- **The case $m < n$.** Then $\delta = 0$ and the result is $(0, f)$; do not multiply by $\ell^{m - n + 1}$ with a negative exponent.
- **Coefficient growth.** Repeated pseudo-division without removing contents makes the coefficient sizes grow exponentially in the number of steps, as Knuth's example of the Euclidean algorithm on the [polynomial GCD](/polynomial-gcd/) page shows over $\mathbb{Q}$.

## Implementations

## History

Pseudo-division is the step of the polynomial remainder sequences that Collins (1967) and Brown (1971) used to compute gcds and resultants over $\mathbb{Z}$ without fractions. Knuth, Section 4.6.1, gives it as Algorithm R and uses it in his gcd algorithms over a unique factorization domain. Von zur Gathen and Gerhard treat it in Section 6.12 together with the primitive Euclidean algorithm.

## References
