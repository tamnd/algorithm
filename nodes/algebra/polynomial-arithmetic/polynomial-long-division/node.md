---
tag: 0Q78BZ
kind: algorithm
slug: polynomial-long-division
name: Polynomial long division
aliases:
- classical polynomial division
- schoolbook polynomial division
area: algebra/polynomial-arithmetic
level: intro
summary: Repeatedly subtracts multiples of the divisor to eliminate leading terms; quadratic in the degrees.
solves: [polynomial-division]
model: blum-shub-smale-machine
complexity:
  vars: {m: the degree of the dividend f, n: the degree of the divisor g}
  time: {worst: Θ((m - n + 1) n + m)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [polynomial-division, polynomial-degree, loop-invariant]
see_also: [polynomial-division, fast-polynomial-division, pseudo-division, horner-rule, polynomial-remainder-theorem, polynomial-euclidean-algorithm, long-division, monic-polynomial]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 2.4, Division with remainder (pp. 37 to 41), the classical algorithm and its cost
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of Polynomials (Algorithm D, division of polynomials over a field)
---

Polynomial long division computes the quotient $q$ and the remainder $r$ of $f$ divided by $g$, with $f = qg + r$ and $\deg r < \deg g$, by removing the top term of the running remainder with one multiple $c\, x^k g$ at a time. It solves [polynomial division](/polynomial-division/) over any commutative ring in which the leading coefficient of $g$ is a unit, in particular over every field. For $m = \deg f \ge n = \deg g$ it uses at most $(2n + 1)(m - n + 1)$ operations in the ring and one inversion. It is the method of choice for small degrees and is the base case of [fast division](/fast-polynomial-division/).

## In plain words

You divide one polynomial by another the way you divide numbers on paper. Look at the highest term of the dividend. Find the single term that, times the highest term of the divisor, gives it. Write that term into the quotient. Multiply the divisor by that term and subtract the result from the dividend. The highest term is now gone.

Repeat with what is left. Each round removes one top term, so the rounds stop when what is left is shorter than the divisor. That last piece is the remainder.

Unlike long division of numbers, there are no carries and no guessing: each quotient term is found by one division of two coefficients.

## The problem

Given a commutative ring $R$, $f = \sum_{i=0}^{m} f_i x^i$ and $g = \sum_{j=0}^{n} g_j x^j$ in $R[x]$ with $g_n$ a unit of $R$, find $q, r \in R[x]$ with $f = qg + r$ and $\deg r < n$. The solution exists and is unique; see [polynomial division](/polynomial-division/). Polynomials are stored densely, as coefficient arrays with the lowest degree first.

## The algorithm

```pseudo id=main
LONG-DIVISION(f, g)                ▷ f = (f_0, ..., f_m), g = (g_0, ..., g_n), g_n a unit
L1  strip the zero top coefficients of f and of g; if g = 0 then error
L2  if deg f < deg g then return (0, f)
L3  u ← g_n^(−1)
L4  r ← a copy of f; q ← an array of m − n + 1 coefficients
L5  for k ← m − n downto 0 do
L6      c ← r_(n+k) · u                ▷ the coefficient that cancels the top term
L7      q_k ← c
L8      for j ← 0 to n − 1 do
L9          r_(j+k) ← r_(j+k) − c · g_j
L10     r_(n+k) ← 0                    ▷ r_(n+k) − c · g_n is 0 because u · g_n = 1
L11 return (q, r_0 + r_1 x + ... + r_(n−1) x^(n−1)) with zero top coefficients stripped
```

Line L1 makes $m$ and $n$ the true degrees. A stored array can have zero top coefficients, for example after a subtraction or a reduction modulo $p$, and the loop must not divide by such a zero. Line L3 inverts the leading coefficient once, so the loop needs no division. The loop of line L5 runs from the top: at the step for $k$, the running remainder $r$ has degree at most $n + k$, and line L6 picks the multiple $c\, x^k g$ that has the same top coefficient. Lines L8 to L10 subtract $c\, x^k g$ from $r$. Line L10 writes the zero that the subtraction would produce, which saves one multiplication.

Over $\mathbb{Z}$, the precondition means $g_n = \pm 1$. For any other $g_n$, use [pseudo-division](/pseudo-division/) or work over $\mathbb{Q}$.

## Example

Divide $f = 2x^4 + 3x^3 - x + 5$ by $g = x^2 + x + 1$ over $\mathbb{Z}$. Here $m = 4$, $n = 2$, $u = 1$, and the remainder array is $r = [r_0, \ldots, r_4]$.

| step | $c$ | subtract | $r$ after the step | $q$ so far |
|---|---|---|---|---|
| start | | | $[5, -1, 0, 3, 2]$ | |
| $k = 2$ | $r_4 = 2$ | $2x^2 g = 2x^4 + 2x^3 + 2x^2$ | $[5, -1, -2, 1, 0]$ | $2x^2$ |
| $k = 1$ | $r_3 = 1$ | $x g = x^3 + x^2 + x$ | $[5, -2, -3, 0, 0]$ | $2x^2 + x$ |
| $k = 0$ | $r_2 = -3$ | $-3 g = -3x^2 - 3x - 3$ | $[8, 1, 0, 0, 0]$ | $2x^2 + x - 3$ |

The result is $q = 2x^2 + x - 3$ and $r = x + 8$. Over $\mathbb{F}_7$ with the non-monic divisor $g = 2x^2 + 3$, the same loop with $u = 2^{-1} = 4$ divides $f = 4x^5 + x^4 + 3x^2 + 1$ into $q = 2x^3 + 4x^2 + 4x + 6$ and $r = 2x + 4$.

## Correctness

The loop keeps this [invariant](/loop-invariant/): before the step for $k$,

$$f = \Big(\sum_{i = k + 1}^{m - n} q_i x^i\Big) g + r \qquad\text{and}\qquad r_i = 0 \text{ for all } i > n + k .$$

A step subtracts exactly $c\, x^k g$ from $r$ and adds $c\, x^k$ to the quotient, so the identity stays true, and the choice of $c$ clears the coefficient $r_{n+k}$. After the step for $k = 0$, $r$ has degree less than $n$, so $(q, r)$ is the unique solution. The full proof is below.

## Complexity

The cost counts operations in $R$, each at unit cost, as in [polynomial ring](/polynomial-ring/).

- **Time.** If $m < n$, the algorithm does no arithmetic. Otherwise line L3 does one inversion, and each of the $m - n + 1$ steps of line L5 does one multiplication in line L6 and $n$ multiplications and $n$ subtractions in line L9. The total is $(2n + 1)(m - n + 1)$ operations and one inversion. If $g$ is monic, the multiplication by $u = 1$ can be skipped, which leaves $2n(m - n + 1)$. Lines L1 and L4 copy and scan $O(m)$ coefficients. So the time is $\Theta((m - n + 1) n + m)$ in every case, which is $\Theta(n^2)$ for $m = 2n$ and $\Theta(m)$ for constant $n$.
- **Space.** $O(m)$ extra for the copy $r$ and the quotient.
- **Bit cost over $\mathbb{Q}$.** The arithmetic count does not show the growth of the numbers. Over $\mathbb{Q}$ the coefficients of $q$ and $r$ can have numerators and denominators much larger than those of $f$ and $g$; the denominators divide $g_n^{m-n+1}$, which is the reason for [pseudo-division](/pseudo-division/).

The operation counts are proved. The point at which [Newton division](/fast-polynomial-division/) with $O(M(m))$ operations becomes faster is observed by measurement and depends on the ring, the multiplication algorithm and the machine.

## Properties

- **Exact.** No rounding: over $\mathbb{Q}$ or $\mathbb{F}_p$ the result is exact.
- **One inversion.** Only $g_n$ is inverted. Over $\mathbb{F}_p$ this is one modular inverse; over $\mathbb{Z}$ with a monic $g$ there is none.
- **Online in the quotient.** The quotient comes out from the top coefficient down, and each coefficient $q_k$ depends only on the top $m - n - k + 1$ coefficients of $f$.
- **Not in place as written.** The copy $r$ can overwrite $f$ when $f$ is no longer needed. Then $q_k$ can be stored in $r_{n+k}$, the slot that line L10 clears, so the whole division runs in the space of $f$.

## Variants and improvements

- **Synthetic division.** For $g = x - a$, the loop becomes [Horner's rule](/horner-rule/): $q_{k} = r_{k+1}$ and the remainder is $f(a)$, the [remainder theorem](/polynomial-remainder-theorem/).
- **Remainder only.** Drop line L7. This is the reduction step of arithmetic in $F[x]/(g)$ and of the [Euclidean algorithm](/polynomial-euclidean-algorithm/).
- **Pseudo-division.** Multiply $r$ by $g_n$ instead of dividing by it, to stay in an integral domain. See [pseudo-division](/pseudo-division/).
- **Fast division.** Compute the quotient from the reversals with [power series inversion](/power-series-inversion/) and [Newton iteration](/newton-iteration/), in $O(M(m))$ operations: [fast polynomial division](/fast-polynomial-division/).
- **Division modulo a fixed $g$ with a sparse $g$.** When $g$ has $t$ nonzero terms, line L8 runs only over them, and the cost is $O((m - n + 1) t)$. Trinomials and pentanomials are chosen as moduli of binary fields for this reason.

## When to use it

Use long division for small degrees, for divisors of small degree, and for quotients of small degree, where its $\Theta((m - n + 1) n)$ cost is close to linear. Use it as the base case of Newton division and of the fast Euclidean algorithm. For large balanced divisions, use [Newton division](/fast-polynomial-division/), which costs $O(M(m))$. Over $\mathbb{Z}$ with a non-monic divisor, use [pseudo-division](/pseudo-division/) or a modular method.

## Pitfalls

- **Zero top coefficients.** If line L1 is skipped and the stored $g$ ends with a zero, line L3 inverts $0$. If the stored $f$ ends with zeros, the quotient gets spurious zero top coefficients. Strip both first.
- **Integer division over $\mathbb{Z}$.** Replacing line L3 by an integer division, as in $c \leftarrow \lfloor r_{n+k} / g_n \rfloor$, gives a wrong result when $g_n \ne \pm 1$: the top term is not cancelled and the remainder has the wrong degree. The precondition is that $g_n$ is a unit.
- **Floating-point coefficients.** With floats, line L10 hides the rounding error in the top coefficient, but the other coefficients of $r$ carry it. Exact arithmetic or a careful error analysis is needed when the remainder is small compared with $f$.
- **Wrong loop direction.** The loop of line L5 must run from $k = m - n$ down to $0$. Going up uses the top coefficient before it is final.

## Implementations

## History

Division of polynomials with remainder is as old as algebra written with symbols. Knuth (Section 4.6.1) gives it as Algorithm D and traces the related algorithm for the gcd to the 16th century, to Simon Stevin. Von zur Gathen and Gerhard (Section 2.4) give the classical algorithm with the count used here.

## References
