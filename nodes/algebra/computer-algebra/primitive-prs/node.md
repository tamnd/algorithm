---
tag: 1021Z1
kind: algorithm
slug: primitive-prs
name: Primitive polynomial remainder sequence algorithm
aliases: [primitive PRS, primitive polynomial GCD, primitive Euclidean algorithm]
area: algebra/computer-algebra
level: advanced
summary: Polynomial GCD over Z by pseudo-division with removal of content at each step.
solves: [polynomial-gcd]
model: blum-shub-smale-machine
complexity:
  vars: {m: the larger of the degrees of f and g}
  time: {worst: O(m^2)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [pseudo-division, primitive-polynomial, gauss-lemma, polynomial-euclidean-algorithm]
see_also: [subresultant-gcd, subresultant-prs, subresultant, brown-modular-gcd, polynomial-gcd, hadamard-bound, sylvester-matrix, resultant]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of Polynomials (Algorithm E, the gcd over a unique factorization domain with primitive parts, and the example pair u, v)
  - paper: doi:10.1145/321371.321381
    title: George E. Collins, Subresultants and reduced polynomial remainder sequences, Journal of the ACM 14(1), 1967
    locator: pp. 128 to 142 (polynomial remainder sequences, the primitive sequence, and its relation to subresultants)
  - paper: doi:10.1145/321662.321664
    title: W. S. Brown, On Euclid's algorithm and the computation of polynomial greatest common divisors, Journal of the ACM 18(4), 1971
    locator: pp. 478 to 504 (the Euclidean, primitive and reduced sequences compared, and the cost of content computations)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 7, Polynomial GCD Computation (polynomial remainder sequences, the primitive PRS and coefficient growth)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 6 (pseudodivision and the primitive Euclidean algorithm) and Section 11.2, Subresultants
---

The primitive PRS algorithm computes the [gcd](/polynomial-gcd/) of two polynomials with integer coefficients, or more generally over a unique factorization domain, by the Euclidean algorithm with [pseudo-division](/pseudo-division/), and replaces each pseudo-remainder by its [primitive part](/primitive-polynomial/). This gives the smallest coefficients that any sequence of remainders in $\mathbb{Z}[x]$ can have, because every member is primitive. The price is one gcd of all the coefficients at each step. It is the simplest correct gcd method over $\mathbb{Z}[x]$, and the reference against which the [subresultant algorithm](/subresultant-gcd/) and the [modular algorithm](/brown-modular-gcd/) are measured.

## In plain words

The school method for the greatest common divisor of two polynomials divides one by the other again and again. With integer coefficients, the division brings in fractions. One way out is to multiply first by a power of the leading number, so that the division stays in the integers. But then the numbers grow very fast from step to step.

The primitive method stops this growth in the most direct way. After each division it finds the largest whole number that divides all the coefficients of the remainder, and it divides that number out. The remainders keep the same roots, and their numbers stay as small as they can be. The cost is that this common divisor of all the coefficients must be found again at every step.

## The problem

**Notation.** $R$ is a unique factorization domain, usually $\mathbb{Z}$, with field of fractions $K$. For $f \in R[x]$, $f \ne 0$, $\operatorname{LC}(f)$ is the leading coefficient and the content $\operatorname{cont}(f)$ is a gcd of the coefficients. Over $\mathbb{Z}$ we choose the sign of $\operatorname{LC}(f)$, so the primitive part $\operatorname{pp}(f) = f / \operatorname{cont}(f)$ has a positive leading coefficient. $\operatorname{prem}(A, B) = \operatorname{LC}(B)^{\deg A - \deg B + 1} A \bmod B$ is the [pseudo-remainder](/pseudo-division/), which lies in $R[x]$.

**Input.** $f, g \in R[x]$. **Output.** $\gcd(f, g)$ in $R[x]$, normalized (over $\mathbb{Z}$, with positive leading coefficient), and the primitive PRS: the sequence $P_1 = \operatorname{pp}(f)$, $P_2 = \operatorname{pp}(g)$, $P_{i+1} = \operatorname{pp}(\operatorname{prem}(P_{i-1}, P_i))$, for $\deg f \ge \deg g$, up to the last nonzero member.

## The algorithm

```pseudo id=main
PRIMITIVE-PRS(f, g)
L1  if f = 0 and g = 0 then return 0
L2  if deg f < deg g then swap f and g          ▷ deg 0 = -∞
L3  if g = 0 then return f, normalized
L4  c ← gcd(cont(f), cont(g)); A ← pp(f); B ← pp(g)
L5  while deg B > 0 do
L6      r ← prem(A, B)
L7      if r = 0 then return c · B
L8      A ← B; B ← pp(r)
L9  return c                                     ▷ B is a nonzero constant
```

Line L4 splits off the contents: by [Gauss's lemma](/gauss-lemma/), $\gcd(f, g) = \gcd(\operatorname{cont} f, \operatorname{cont} g) \cdot \gcd(\operatorname{pp} f, \operatorname{pp} g)$. Line L6 is pseudo-division, so no fractions appear. Line L8 removes the content of the remainder. When the loop reaches a remainder 0, the last $B$ is primitive and is the gcd of the primitive parts. When it reaches a nonzero constant, the primitive parts are coprime.

## Example

Take Knuth's pair $u = x^8 + x^6 - 3x^4 - 3x^3 + 8x^2 + 2x - 5$ and $v = 3x^6 + 5x^4 - 4x^2 - 9x + 21$, both primitive. So $c = 1$.

| pass | $A$ | $B$ | $\operatorname{prem}(A, B)$ | content | new $B$ |
|---|---|---|---|---|---|
| 1 | $u$ | $v$ | $-15x^4 + 3x^2 - 9$ | $-3$ | $5x^4 - x^2 + 3$ |
| 2 | $v$ | $5x^4 - x^2 + 3$ | $-585x^2 - 1125x + 2205$ | $-45$ | $13x^2 + 25x - 49$ |
| 3 | $5x^4 - x^2 + 3$ | $13x^2 + 25x - 49$ | $-233150x + 307500$ | $-50$ | $4663x - 6150$ |
| 4 | $13x^2 + 25x - 49$ | $4663x - 6150$ | $143193869$ | $143193869$ | $1$ |

The loop stops with the constant $B = 1$, so $\gcd(u, v) = 1$. The primitive PRS is $u, v, 5x^4 - x^2 + 3, 13x^2 + 25x - 49, 4663x - 6150, 1$. Knuth writes the third member as $-5x^4 + x^2 - 3$, with the other sign convention for the content. For the same pair, the [subresultant algorithm](/subresultant-gcd/) gives the members $-15x^4 + \ldots$, $65x^2 + \ldots$, $-9326x + \ldots$ and $260708$, which differ from these by integer factors. Without the content step, pseudo-division alone ends with a constant of 35 digits.

## Correctness

Over $K$, $\operatorname{prem}(A, B)$ is a nonzero constant times the remainder $A \bmod B$, and $\operatorname{pp}$ divides by a nonzero constant. So each pass replaces $(A, B)$ by $(B, \lambda (A \bmod B))$ with $\lambda \in K^*$, which keeps the set of common divisors in $K[x]$, and the degree of $B$ falls. The loop ends with $B$ an associate in $K[x]$ of $\gcd(\operatorname{pp} f, \operatorname{pp} g)$. Every $B$ is primitive, and a primitive polynomial that is an associate in $K[x]$ of the gcd of two primitive polynomials is their gcd in $R[x]$, by Gauss's lemma. The full proof is in the proof file below.

## Complexity

**Cost model.** Ring operations in $R$ and gcds of elements of $R$, each counted as one step. Over $\mathbb{Z}$ the bit cost also depends on the sizes of the integers, bounded below.

- **Pseudo-divisions.** Pass $i$ divides a polynomial of degree $n_i$ by one of degree $n_{i+1}$ in $O((\delta_i + 1) \, n_i)$ ring operations, with $\delta_i = n_i - n_{i+1}$. The sum over all passes is $O(m^2)$.
- **Contents.** Each pass takes the gcd of at most $m + 1$ coefficients, so $O(m)$ gcds per pass and $O(m^2)$ in total, plus $O(m)$ exact divisions per pass.
- **Sizes.** Each member of the primitive PRS is, up to sign, the primitive part of a [subresultant](/subresultant/) of $f$ and $g$, because both are associates in $K[x]$ of the same Euclidean remainder. A primitive part has coefficients no larger than the polynomial itself. So by the [Hadamard bound](/hadamard-bound/) on the minors of the [Sylvester matrix](/sylvester-matrix/), every coefficient in the sequence is at most $\|f\|_2^{\,n} \|g\|_2^{\,m}$ in absolute value, with $m = \deg f$ and $n = \deg g$. For coefficients of $L$ digits this is $O(m (L + \log m))$ digits, and the total bit cost is polynomial.

These bounds are proved. In practice the primitive members are often much smaller than the subresultants, but the content gcds dominate the running time, and the subresultant algorithm is usually faster because it divides by a factor known in advance. For large dense inputs over $\mathbb{Z}$, the modular algorithm is faster than both; this is observed by measurement, as in Brown 1971.

## Properties

- Every member is primitive, so no remainder sequence in $R[x]$ with the same degrees has smaller coefficients up to units: each member is the smallest $R[x]$ multiple of the Euclidean remainder.
- The degrees $n_1 \ge n_2 > n_3 > \cdots$ are those of the Euclidean algorithm over $K$.
- It works over any unique factorization domain where gcds of elements can be computed, for example $\mathbb{Z}[y]$, which gives a recursive gcd for multivariate polynomials.
- It is deterministic and uses no randomness or primes.

## Variants and improvements

- **Euclidean PRS.** Pseudo-division with no reduction. It is simplest, but the coefficient sizes grow exponentially with the number of passes.
- **Reduced PRS.** Collins divides each pseudo-remainder by $\operatorname{LC}^{\delta + 1}$ of the member two steps before. It is correct, but it can still grow when the degree drops by more than one.
- **Subresultant PRS.** Divide by a factor $\gamma h^\delta$ known in advance. The members are the subresultants, with linear size growth and no content gcds. See [subresultant PRS](/subresultant-prs/) and [subresultant gcd](/subresultant-gcd/).
- **Monic PRS over $\mathbb{Q}$.** Make each remainder monic. The numbers are then fractions whose numerators and denominators also grow, and they are kept in lowest terms by gcds, so this has the same kind of cost.
- **Modular and heuristic gcd.** Compute the gcd modulo many primes, or at one large integer point, and reconstruct; see [Brown's modular gcd](/brown-modular-gcd/).

## When to use it

Use the primitive PRS when the remainders themselves are needed in their smallest form, for example to show them or to feed a [Sturm sequence](/sturm-sequence/) where only signs matter, and for small or sparse inputs where the content gcds are cheap. For a gcd of large dense polynomials over $\mathbb{Z}$, use the modular algorithm, and for a deterministic method with no coefficient gcds, use the subresultant algorithm.

## Pitfalls

- **Forgetting the contents of the input.** The gcd of $2x + 4$ and $6x^2 - 24$ is $2(x + 2)$, not $x + 2$. Line L4 keeps $\gcd(\operatorname{cont} f, \operatorname{cont} g)$ for the result.
- **The sign of the content.** If the content is always taken positive, the members can have negative leading coefficients and the gcd must be normalized at the end. Choose one convention and use it in the output.
- **Constant remainder.** A nonzero constant remainder means that the primitive parts are coprime. The gcd is then $c$, not the constant itself.
- **Zero inputs.** $\gcd(f, 0) = f$ normalized, and $\gcd(0, 0) = 0$. Pseudo-division by the zero polynomial is not defined, so line L3 must come before the loop.
- **Degree order.** Pseudo-division needs $\deg A \ge \deg B$; line L2 swaps the inputs when they come in the other order.

## Implementations

## History

Euclid's algorithm for polynomials goes back to Stevin in the sixteenth century. The use of primitive parts to keep the computation in $\mathbb{Z}[x]$ follows from Gauss's lemma. In the 1960s Collins studied polynomial remainder sequences for computer algebra and showed in 1967 that the reduced and subresultant sequences avoid the exponential growth of the Euclidean sequence without the content gcds of the primitive sequence. Brown in 1971 compared the Euclidean, primitive, reduced and subresultant sequences with the modular algorithm, and Knuth gave the primitive form as Algorithm E of Section 4.6.1.

## References
