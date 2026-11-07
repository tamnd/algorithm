---
tag: YEET6X
kind: data-structure
slug: dense-polynomial-representation
name: Dense polynomial representation
aliases:
- coefficient array
- coefficient vector
- coefficient list
area: algebra/polynomial-arithmetic
level: intro
summary: Stores all coefficients of degree 0 to n in an array; fast for dense polynomials.
implements: [polynomial]
model: blum-shub-smale-machine
complexity:
  vars: {m: the length of the first coefficient array, n: the length of the second coefficient array}
  time: {worst: Θ(m + n), best: Θ(m + n)}
  space: {extra: Θ(m + n)}
prereqs: [polynomial, monic-polynomial]
see_also: [sparse-polynomial-representation, point-value-representation, dense-polynomial, horner-rule, polynomial-long-division, polynomial-multiplication, kronecker-substitution, multiprecision-integer]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 2.2, Representation and addition of polynomials; Section 2.3, Multiplication; Section 2.4, Division with remainder
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6, Polynomial arithmetic (the coefficient representation), Section 4.6.1, Division of polynomials (Algorithm D), and Section 4.6.4, Evaluation of polynomials
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 17.1, Basic arithmetic (coefficient vectors and the cost of addition, multiplication and division with remainder)
---

The dense representation stores a [polynomial](/polynomial/) of degree less than $n$ as the array of its $n$ coefficients, lowest degree first, with the zero coefficients included. It is normalized: the top entry is never zero, and the zero polynomial is the empty array, so each polynomial has exactly one representation and the degree is the length minus one. Addition takes $\Theta(m + n)$ ring operations, schoolbook multiplication $\Theta(mn)$, and evaluation by [Horner's rule](/horner-rule/) $\Theta(n)$. All fast polynomial algorithms, from [FFT multiplication](/fft-polynomial-multiplication/) to [fast division](/fast-polynomial-division/), work on this array.

## In plain words

A polynomial is a list of numbers, one for each power of x: the constant, then the number in front of x, then the number in front of x squared, and so on. The dense form stores this list in order, and it stores a zero for each power that is missing. The list starts at the constant, so position i holds the number in front of x to the power i.

The list never ends with a zero. So each polynomial has only one list, and the length of the list tells the degree. The zero polynomial is the empty list. To add two polynomials, add the lists position by position, then remove zeros from the end. This form is best when most of the numbers are not zero.

## The abstract type

The representation implements the [polynomial](/polynomial/) abstract type over a commutative ring $R$: the values are all of $R[x]$, with `add`, `sub`, `neg`, scalar multiplication, `mul`, `evaluate`, `degree`, the leading coefficient, the formal derivative, and division with remainder by a polynomial whose leading coefficient is a unit of $R$. Over a field $F$ this last condition holds for each nonzero divisor. The cost of each operation is counted in ring operations of $R$, in the algebraic complexity model (the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $R$: each addition, subtraction, multiplication and zero test of ring elements costs 1, and so does each inversion of a unit). Array access and loop control are free in this model; on a real machine they add $O(1)$ time per ring operation.

## Representation

A value is a list $a = [a_0, a_1, \ldots, a_{n-1}]$ of $n \ge 0$ elements of $R$. It stands for

$$\operatorname{val}(a) = \sum_{i=0}^{n-1} a_i x^i \in R[x].$$

**Invariant (N).** If $n > 0$ then $a_{n-1} \ne 0$.

Each $f \in R[x]$ has exactly one list that meets (N): if $f = 0$ it is the empty list, and otherwise it is the list of the coefficients of $x^0, \ldots, x^{\deg f}$. So two values are equal exactly when the lists are equal, and $\deg \operatorname{val}(a) = n - 1$, with $-1$ standing for the degree $-\infty$ of the zero polynomial. The leading coefficient is $a_{n-1}$.

Over $\mathbb{Z}/p\mathbb{Z}$ or any ring with a chosen normal form, the entries must be stored in that normal form, for example as integers in $[0, p)$. A zero test is then a comparison with $0$. Without a normal form for the entries, (N) cannot be checked, and the length no longer gives the degree.

In libraries the list is a record with a pointer to the coefficients, the number of allocated entries and the number of entries in use. FLINT's `fmpz_poly_t` and NTL's `ZZX` work this way, and both restore (N) after each operation that can lower the degree.

## Operations

```pseudo id=main
NORMALIZE(c)
L1  while c is not empty and the last entry of c is 0 do
L2      remove the last entry of c
L3  return c

ADD(a, b)                                  ▷ normalized; m = |a|, n = |b|
L4  c ← a list of max(m, n) zeros
L5  for i ← 0 to max(m, n) − 1 do
L6      c[i] ← (a[i] if i < m else 0) + (b[i] if i < n else 0)
L7  return NORMALIZE(c)

MUL(a, b)                                  ▷ the schoolbook product
L8  if m = 0 or n = 0 then return [ ]
L9  c ← a list of m + n − 1 zeros
L10 for i ← 0 to m − 1 do
L11     for j ← 0 to n − 1 do
L12         c[i + j] ← c[i + j] + a[i] · b[j]
L13 return NORMALIZE(c)

EVALUATE(a, u)                             ▷ Horner's rule
L14 s ← 0
L15 for i ← m − 1 down to 0 do
L16     s ← s · u + a[i]
L17 return s

DIVMOD(a, b)                               ▷ n ≥ 1; lc(b) = b[n − 1] is a unit
L18 r ← a copy of a; q ← a list of max(m − n + 1, 0) zeros
L19 v ← b[n − 1]⁻¹
L20 for k ← m − n down to 0 do
L21     t ← r[k + n − 1] · v
L22     q[k] ← t
L23     for j ← 0 to n − 1 do
L24         r[k + j] ← r[k + j] − t · b[j]
L25 return (NORMALIZE(q), NORMALIZE(r[0 .. n − 2]))
```

Subtraction is ADD with the negated second operand, scalar multiplication $s \cdot a$ multiplies each entry and then calls NORMALIZE, and the derivative of $a$ is the list $[1 \cdot a_1, 2 \cdot a_2, \ldots, (n-1) \cdot a_{n-1}]$, normalized, where $i \cdot a_i$ is the sum of $i$ copies of $a_i$.

NORMALIZE (lines L1 to L3) is the only place where (N) is restored, and every operation whose result can have a smaller degree than the length suggests ends with it. ADD can lose any number of top entries through cancellation. MUL can lose its top entry only when $R$ has zero divisors, because the top entry is $a_{m-1} b_{n-1}$; over $\mathbb{Z}/4\mathbb{Z}$, $(2x + 1)^2 = 4x^2 + 4x + 1 = 1$ loses two. Scalar multiplication by a zero divisor and the derivative over a ring of positive characteristic can also lose entries.

DIVMOD is [long division](/polynomial-long-division/). Step $k$ of line L20 makes the entry $r[k + n - 1]$ zero: line L24 with $j = n - 1$ subtracts $t \cdot b[n-1] = r[k + n - 1] \cdot v \cdot b[n-1] = r[k + n - 1]$. So after the loop all entries of $r$ from position $n - 1$ up are zero, and line L25 keeps the first $n - 1$ entries. When $b$ is [monic](/monic-polynomial/), $v = 1$ and no inversion is needed; this is why division by a monic polynomial works over every commutative ring.

## Example

**A product.** Over $\mathbb{Z}$, take $a = 1 + x + 3x^3$, stored as $[1, 1, 0, 3]$, and $b = 2 - x$, stored as $[2, -1]$. Line L9 makes $c = [0, 0, 0, 0, 0]$, and the loop of lines L10 to L12 runs as follows.

| $i$ | $a_i$ | updates | $c$ after row $i$ |
|---|---|---|---|
| 0 | 1 | $c_0 \mathrel{+}= 2$, $c_1 \mathrel{+}= -1$ | $[2, -1, 0, 0, 0]$ |
| 1 | 1 | $c_1 \mathrel{+}= 2$, $c_2 \mathrel{+}= -1$ | $[2, 1, -1, 0, 0]$ |
| 2 | 0 | $c_2 \mathrel{+}= 0$, $c_3 \mathrel{+}= 0$ | $[2, 1, -1, 0, 0]$ |
| 3 | 3 | $c_3 \mathrel{+}= 6$, $c_4 \mathrel{+}= -3$ | $[2, 1, -1, 6, -3]$ |

The top entry $-3$ is nonzero, so NORMALIZE changes nothing, and $ab = 2 + x - x^2 + 6x^3 - 3x^4$. The stored zero $a_2$ still costs two multiplications: the dense form does not skip zeros.

**A sum with cancellation.** $(1 + 2x + x^2) + (4 - 2x - x^2)$ gives the list $[5, 0, 0]$ at line L6, and NORMALIZE removes two entries, so the result is $[5]$, of degree 0.

**A division over $\mathbb{F}_7$.** Divide $a = x^3 + 2x + 5$, stored as $[5, 2, 0, 1]$, by $b = 3x + 1$, stored as $[1, 3]$. Here $m = 4$, $n = 2$, and line L19 sets $v = 3^{-1} = 5$, since $3 \cdot 5 = 15 \equiv 1$.

| $k$ | $t = r[k+1] \cdot 5$ | $r$ after line L24 |
|---|---|---|
| 2 | $1 \cdot 5 = 5$ | $[5, 2, 2, 0]$ |
| 1 | $2 \cdot 5 = 10 \equiv 3$ | $[5, 6, 0, 0]$ |
| 0 | $6 \cdot 5 = 30 \equiv 2$ | $[3, 0, 0, 0]$ |

So $q = [2, 3, 5] = 5x^2 + 3x + 2$ and $r = [3]$. Check: $(5x^2 + 3x + 2)(3x + 1) + 3 = 15x^3 + 14x^2 + 9x + 5 \equiv x^3 + 2x + 5 \pmod 7$.

## Correctness

Each operation maps normalized lists to normalized lists, and its value is the exact result in $R[x]$. For ADD and MUL this is a direct comparison of coefficients, plus the fact that NORMALIZE removes only zero entries. For EVALUATE the loop invariant is $s = \sum_{j=i}^{m-1} a_j u^{j-i}$ at line L15. For DIVMOD the invariant is that $a = (\sum_{j > k} q_j x^j)\, b + \operatorname{val}(r)$ with $r_j = 0$ for $j \ge k + n$ before step $k$. The full proof, with the uniqueness of the quotient and the remainder, is in the proof file.

## Complexity

All costs are ring operations of $R$, in the algebraic complexity model described in the abstract type. The front matter states the cost of ADD. Write $m = |a|$ and $n = |b|$, both normalized.

| operation | ring operations | notes |
|---|---|---|
| `add`, `sub` | $\max(m, n)$ additions, plus at most $\max(m, n)$ zero tests | $\Theta(m + n)$; the result must be written |
| `neg`, scalar multiple | $n$ | plus zero tests in NORMALIZE for a zero divisor |
| `mul` | $mn$ multiplications and $(m - 1)(n - 1)$ additions | $\Theta(mn)$; the fast methods give $M(n)$ |
| `evaluate` | $m$ multiplications and $m$ additions | $m - 1$ of each if $s$ starts at $a_{m-1}$, which is optimal |
| `divmod` | 1 inversion, $(m - n + 1) n$ multiplications and as many subtractions | $\Theta((m - n + 1) n)$ for $m \ge n$; 0 for $m < n$ |
| `degree`, leading coefficient | 0 | $O(1)$ time, by (N) |
| space | $m + n$ | a sum has at most $\max(m, n)$ entries, a product $m + n - 1$ |

The counts follow from the loops: lines L5 to L6 run $\max(m, n)$ times; lines L10 to L12 run $mn$ times, and the first update of each $c_k$ adds to a zero, so $mn - (m + n - 1)$ additions are real; lines L20 to L24 run $(m - n + 1)$ times $n$. NORMALIZE removes each entry at most once. The addition bound is tight, since each of the $\max(m, n)$ output entries depends on an input entry. The bounds for `mul` and `divmod` are those of the schoolbook methods. With [Karatsuba](/karatsuba-multiplication/) or [FFT](/fft-polynomial-multiplication/) multiplication in place of MUL, the cost is $M(n)$, and with [Newton division](/fast-polynomial-division/) the division costs $O(M(m))$. The representation itself does not change.

On a real machine each ring operation on $\mathbb{Z}/p\mathbb{Z}$ with $p$ below the word size takes $O(1)$ time, so the costs above are also time bounds on the [word RAM](/word-ram/). Over $\mathbb{Z}$ or $\mathbb{Q}$ the coefficients grow, and the time of each ring operation depends on their size; then the bit cost must be analyzed apart, as in von zur Gathen and Gerhard, Section 8.4.

## Variants

- **Highest degree first.** Some texts and systems store $[a_{n-1}, \ldots, a_0]$, the order in which a polynomial is printed and in which Horner's rule reads it. The algorithms are the same with reversed indices. The low-first order makes the index equal to the exponent and makes the [reversal](/fast-polynomial-division/) used by fast division an explicit operation.
- **Fixed length with a degree field.** A buffer of capacity $N$ and a separate degree $d \le N - 1$. This avoids reallocation in loops, such as the Euclidean algorithm, where degrees only fall.
- **Packed coefficients over small fields.** Over $\mathbb{F}_2$, store one coefficient per bit, so that a machine word holds 64 coefficients and addition is a bitwise exclusive or of words. Over $\mathbb{F}_p$ with small $p$, several coefficients can share a word in the same way. [Kronecker substitution](/kronecker-substitution/) is the same idea used for multiplication: pack the coefficients into one big integer.
- **Sparse representation.** Store only the pairs (exponent, nonzero coefficient), sorted by exponent. See [sparse polynomial representation](/sparse-polynomial-representation/).
- **Point-value representation.** Store the values at $n$ fixed points instead of the coefficients. Multiplication then takes $O(n)$ ring operations, but evaluation at a new point and division are harder. See [point-value representation](/point-value-representation/).
- **Multivariate dense.** A polynomial in $x_1, \ldots, x_k$ with $\deg_{x_i} < d_i$ is stored as a $k$-dimensional array of $d_1 \cdots d_k$ entries, or recursively as a dense polynomial in $x_k$ whose coefficients are dense polynomials in the other variables.

## When to use it

Use the dense form for univariate polynomials in which most coefficients are nonzero, and for all fast algorithms, which need the coefficients at known positions. Polynomials over finite fields that arise in factoring, coding and cryptography are dense in this sense, and so are products and remainders of random polynomials. Use the [sparse form](/sparse-polynomial-representation/) when the number of nonzero terms $t$ is much smaller than the degree, as in $x^{1000000} + 1$: the dense form needs $10^6 + 1$ entries and the sparse form needs 2. A common rule is to use the dense form when at least a fixed fraction of the coefficients are nonzero, but the exact crossover depends on the ring, the operation and the machine.

## Pitfalls

- **Not normalizing.** Without line L13 or line L7, the product $(2x + 1)^2$ over $\mathbb{Z}/4\mathbb{Z}$ is stored as $[1, 0, 0]$, and the degree function reports 2 for a constant. Every later algorithm that reads the leading coefficient, such as DIVMOD, then divides by zero or loops on a zero top entry.
- **Entries not in normal form.** Over $\mathbb{Z}/3\mathbb{Z}$, the list $[0, 1, 3]$ stands for $x$, but a test `3 == 0` on plain integers fails, so NORMALIZE keeps the top entry. Reduce entries before the zero test, or use a coefficient type whose equality is the equality of $R$.
- **The degree of zero.** The zero polynomial has degree $-\infty$, stored here as $-1$. Code that computes `len(a) + len(b) - 1` for a product with an empty operand gets a negative or wrong length; line L8 handles this case first.
- **Division by a nonunit.** Over $\mathbb{Z}$, DIVMOD by $2x + 1$ would need $\tfrac{1}{2}$. Either divide over $\mathbb{Q}$, or use [pseudo-division](/pseudo-division/), which multiplies $a$ by a power of $\operatorname{lc}(b)$ first. The implementation below raises an error for an integer leading coefficient other than $\pm 1$.
- **Aliasing.** If an in-place ADD writes into $a$ while $b$ is the same list, the result is $2a$ only by accident of the order of reads. Copy, or document which arguments may share storage.
- **Coefficient growth.** Over $\mathbb{Z}$ the dense form is still dense in the integers: each coefficient can be large, and the cost model that counts ring operations hides this. A product of two polynomials with $k$-digit coefficients has coefficients of up to about $2k + \log_{10} n$ digits.

## Implementations

## History

The coefficient array is the representation of Knuth's Section 4.6 and of the first chapters of von zur Gathen and Gerhard. Dense arrays with a normalized length are the base representation of current libraries for univariate polynomials, such as NTL and FLINT. The early general computer algebra systems, which worked mostly with multivariate polynomials, used sparse lists of terms, and dense univariate arrays became the standard for fast univariate arithmetic.

## References
