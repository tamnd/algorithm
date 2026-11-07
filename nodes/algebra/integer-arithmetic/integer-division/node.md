---
tag: Q6G6RA
kind: problem
slug: integer-division
name: Integer division
aliases:
- divide with remainder
area: algebra/integer-arithmetic
level: intro
summary: Compute quotient and remainder of two n-digit integers.
model: word-ram
complexity:
  vars: {n: the number of limbs of the divisor, M: the cost of a product of two n-limb numbers (a function of n)}
  time: {worst: O(M(n))}
prereqs: [division-with-remainder, integer-multiplication, positional-number-system]
see_also: [long-division, newton-raphson-division, burnikel-ziegler-division, division-by-constant, floor-division, restoring-division, non-restoring-division, barrett-reduction]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, The classical algorithms (Algorithm D, the normalization, and Theorems A and B on the trial quotient), and Section 4.3.3 (division in the time of multiplication)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.4, Division (1.4.1 naive division, Algorithm 1.6 BasecaseDivRem and Theorem 1.3; 1.4.3 divide and conquer division, Theorem 1.4; 1.4.4 Newton's method; 1.4.5 exact division; 1.4.7 division by a single word)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 9, Newton iteration (division with remainder in the time of multiplication, for polynomials and integers)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Part IV, Division (Chapter 13, basic division schemes, restoring and nonrestoring division, division by constants, SRT division)
---

Integer division is the problem of computing, for integers $A$ and $B \ne 0$, the quotient and the remainder of the [division with remainder](/division-with-remainder/) $A = QB + R$. For $A$ of $2n$ limbs and $B$ of $n$ limbs, the school method ([long division](/long-division/)) takes $\Theta(n^2)$ limb operations, and [Newton's method](/newton-raphson-division/) takes $O(M(n))$, where $M(n)$ is the cost of a [multiplication](/integer-multiplication/) of two $n$-limb numbers. Division and multiplication have the same cost up to a constant factor. In practice division is still several times slower than a product of the same size, and a program that divides many numbers by the same divisor uses a precomputed reciprocal instead ([division by a constant](/division-by-constant/)).

## In plain words

Division asks how many times one number fits into another, and what is left over. You learned the long method at school: you look at the first few digits, guess the next digit of the answer, multiply, subtract, and go on to the next digit. If the guess was too large, you correct it.

A computer does the same with machine words as digits. The guess comes from the first one or two words, and a small trick makes sure that the guess is almost always right and is never off by more than two.

For very long numbers there is a faster way. You first compute one over the divisor to enough places by a method that doubles the number of correct digits at each step, and then you multiply. This makes division about as fast as multiplication.

## Definition

**Input.** Integers $A \ge 0$ and $B > 0$, given in the base $\beta = 2^w$ as limb arrays of $m + n$ and $n$ limbs, with $b_{n-1} \ne 0$.

**Output.** The unique integers $Q$ and $R$ with

$$A = QB + R, \qquad 0 \le R < B .$$

So $Q = \lfloor A/B \rfloor$ and $R = A - QB$. The page [division with remainder](/division-with-remainder/) proves that $Q$ and $R$ exist and are unique. Since $Q \le A/B < \beta^{m+n}/\beta^{n-1}$, the quotient has at most $m + 1$ limbs, and $R$ has at most $n$ limbs.

**Cost.** $D(m + n, n)$ is the cost of this problem, and $D(n) = D(2n, n)$ for the balanced case.

**Signed operands.** For $A$ or $B$ negative, the quotient is rounded by a rule that the problem must state. *Truncated* division rounds $A/B$ toward zero, and $R$ has the sign of $A$ (C, Java, GMP's `tdiv`). *Floored* division rounds toward $-\infty$, and $R$ has the sign of $B$ ([floor division](/floor-division/): Python, Ruby). *Euclidean* division keeps $0 \le R < |B|$. The three rules agree when $A \ge 0$ and $B > 0$, and all of them reduce to that case with $O(n)$ extra work.

## Variants

- **Division by one limb.** $B < \beta$. One pass from the top limb down, with one division of a two-limb number by a limb at each step: $\Theta(m)$ limb operations ([long division](/long-division/), short form).
- **Only the quotient, or only the remainder.** The remainder alone is the *reduction modulo* $B$, the step of [modular arithmetic](/modular-multiplication/). [Barrett reduction](/barrett-reduction/) and [Montgomery multiplication](/montgomery-multiplication/) do it with products only, after a precomputation that depends on $B$.
- **Exact division.** It is known that $R = 0$. Then $Q$ can be computed from the low limbs with an inverse of $B$ modulo $\beta$ (Jebelean's method, Brent and Zimmermann Section 1.4.5), which is faster than a general division.
- **Many divisions by one divisor.** [Division by a constant](/division-by-constant/) replaces each division by a multiplication by a precomputed reciprocal and a shift. The [Granlund-Montgomery method](/granlund-montgomery-division/) does this for machine words.
- **Bit-level hardware division.** [Restoring division](/restoring-division/), [non-restoring division](/non-restoring-division/) and SRT division produce one or a few quotient bits per cycle.
- **Unbalanced division.** For $m > n$, cut the dividend into blocks of $n$ limbs and divide block by block, which costs about $\lceil m/n \rceil D(n)$.

## Examples

**Base 10.** For $A = 7007652$ and $B = 1234$, $Q = 5678$ and $R = 1000$, since $1234 \cdot 5678 = 7006652$.

**Normalization and the trial quotient.** Knuth's Algorithm D first multiplies both operands by a factor $d$ so that the top digit of the divisor is at least $\beta/2$. Here $\beta = 10$, and $d = 5$ gives $B' = 6170$ and $A' = 35038260$. Then each quotient digit is guessed from the top two digits of the current remainder and the top digit 6 of $B'$, capped at 9:

| step | current part of the remainder | guess $\hat q$ | true digit $q$ |
|---|---|---|---|
| 1 | 35038 | $\lfloor 35/6 \rfloor = 5$ | 5 |
| 2 | 41882 | $\lfloor 41/6 \rfloor = 6$ | 6 |
| 3 | 48626 | $\lfloor 48/6 \rfloor = 8$ | 7 |
| 4 | 54360 | $\lfloor 54/6 \rfloor = 9$ | 8 |

The quotient is 5678 and the final remainder is $5000 = d \cdot R$, so $R = 5000/5 = 1000$. The guess is too large twice, by one each time. Knuth's Theorems A and B in Section 4.3.1 prove that, after normalization, $q \le \hat q \le q + 2$ always holds.

**Base $2^8$.** $A = \text{0x1234567890}$ (5 limbs) and $B = \text{0x0345}$ (2 limbs) give $Q = \text{0x5916252} = 93413970$ and $R = \text{0x276} = 630$. To normalize, both are shifted left by 6 bits, so that $B$ becomes $\text{0xD140}$ with a top limb $\ge 128$.

**Signs.** For $A = -7$ and $B = 2$: truncated division gives $(-3, -1)$, floored and Euclidean division give $(-4, 1)$. For $A = 7$ and $B = -2$: truncated gives $(-3, 1)$, floored gives $(-4, -1)$, and Euclidean gives $(-3, 1)$.

## Known algorithms

| algorithm | cost for $D(n)$ | notes |
|---|---|---|
| [long division](/long-division/) (Knuth's Algorithm D) | $\Theta(n^2)$ limb operations | the base case of all others; the trial quotient is off by at most 2 |
| [restoring division](/restoring-division/), [non-restoring division](/non-restoring-division/) | $\Theta(N^2)$ bit operations for $N$ bits | one quotient bit per step, in hardware |
| [Burnikel-Ziegler division](/burnikel-ziegler-division/) | $2M(n/2)$ per level; about $2K(n)$ with Karatsuba | recursive long division with two-limb digits of size $n/2$ |
| [Newton-Raphson division](/newton-raphson-division/) | $O(M(n))$ | reciprocal by Newton iteration, then one product and a correction |
| [Barrett reduction](/barrett-reduction/) | two products of $n$ limbs after a precomputation | for many reductions modulo one $B$ |
| [Granlund-Montgomery division](/granlund-montgomery-division/) | one product of words and a few shifts | for a fixed word-size divisor |

Brent and Zimmermann (Theorem 1.4) show that the recursive method satisfies $D(n) = 2D(n/2) + 2M(n/2) + O(n)$, which gives $D(n) \sim 2M(n)$ when $M$ is Karatsuba and $D(n) = O(M(n) \log n)$ when $M(n)$ is quasi-linear. Newton's method removes the factor $\log n$ in that range. Which method is fastest at a given size is a measured fact of each library and machine, not a theorem.

## Bounds

**Upper bound.** $D(n) = O(M(n))$, if $M(n)/n$ does not decrease. The proof is the Newton iteration $x_{k+1} = x_k + x_k(1 - B x_k)$ for $1/B$, which doubles the number of correct limbs at each step. Step $k$ works at precision about $2^k$ limbs and costs $O(M(2^k))$, and $\sum_k M(2^k) \le 2M(n)$ under the condition on $M$. With the bounds of [integer multiplication](/integer-multiplication/), division takes $O(N \log N)$ bit operations.

**Lower bound by reduction.** Multiplication is not harder than division, up to a constant factor. A square follows from reciprocals by

$$x^2 = \frac{1}{\frac{1}{x} - \frac{1}{x + 1}} - x ,$$

with enough precision in each reciprocal, and a product follows from two squares. So $M(n) = O(D(n))$, and division and multiplication have the same order of cost. Cook's thesis of 1966 used Newton's method to divide in the time of a multiplication, and Knuth Section 4.3.3 gives the reciprocal algorithm.

**Trivial lower bound.** $\Omega(n)$ limb operations, because each limb of $A$ and $B$ can change the result.

## Reductions

- **To multiplication.** Division with remainder costs $O(M(n))$ by the Newton iteration above, and squaring reduces to division as shown, so the two problems are equivalent up to constant factors.
- **From the greatest common divisor.** The [Euclidean algorithm](/euclidean-algorithm/) is a sequence of divisions, and the fast [half-gcd](/half-gcd/) method uses the same divide-and-conquer pattern as fast division.
- **From radix conversion.** Conversion of an $n$-limb number to decimal divides by powers of 10, which costs $O(D(n) \log n)$ by divide and conquer ([radix conversion](/radix-conversion/)).
- **From modular exponentiation.** Each step of [modular exponentiation](/modular-exponentiation/) is a product followed by a reduction modulo $B$.

## Applications

- Conversion of numbers to decimal for output, and the parsing of decimal input.
- Modular arithmetic in cryptography and number theory, where each product is reduced.
- Rational arithmetic, where each fraction is reduced by a gcd, and the gcd itself runs divisions.
- Address and index computation with a divisor that is known only at run time, such as hash tables with a prime size.

## References
