---
tag: NDCZEW
kind: algorithm
slug: newton-raphson-division
name: Newton-Raphson division
aliases:
- Newton reciprocal division
- Newton division
- division by reciprocal approximation
area: algebra/integer-arithmetic
level: advanced
summary: Computes the reciprocal of the divisor by Newton iteration, then multiplies by the dividend.
solves: [integer-division]
model: word-ram
complexity:
  vars: {n: the number of limbs of the divisor (the dividend has at most 2n limbs), M: the cost M(k) of multiplying two integers of k limbs}
  time: {worst: O(M(n)), average: O(M(n)), best: O(M(n))}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, in_place: false}
prereqs: [newton-raphson-method, long-division, karatsuba-multiplication]
see_also: [long-division, burnikel-ziegler-division, goldschmidt-division, newton-integer-root, barrett-reduction, srt-division, division-by-constant, newton-iteration]
sources:
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.4.4, Newton's method (division at the cost of a constant number of multiplications), and Section 3.4, Reciprocal and division (Sections 3.4.1 and 3.4.2, the reciprocal with precision doubling, its error analysis, and division from it)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.3, How fast can we multiply? (Algorithm R, high-precision reciprocal, and division in O(M(n)))
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 16, Division by convergence (Newton-Raphson reciprocal iteration and Goldschmidt division in hardware)
  - paper: S. A. Cook, On the minimum computation time of functions, PhD thesis, Harvard University, 1966
    title: Stephen A. Cook, On the minimum computation time of functions
    locator: the reduction of division to multiplication by Newton's method
---

Newton-Raphson division computes $\lfloor A / D \rfloor$ by first computing an approximation of $1/D$ and then multiplying it by $A$. The reciprocal comes from Newton's method for $f(x) = 1/x - D$, whose step $x \leftarrow x + x(1 - Dx)$ uses only multiplications and subtractions and squares the relative error: from an approximation with $h$ correct binary digits it gives about $2h$. Starting from a reciprocal of the top half of $D$, computed the same way, one step gives a reciprocal of all of $D$, so the work at the full precision is a few multiplications and the work at lower precisions is a geometric series. A short correction with additions makes the reciprocal exact, and a quotient from it is off by at most 1. On the [word RAM](/word-ram/), dividing a $2n$-limb number by an $n$-limb number costs $O(M(n))$ limb operations, where $M(n)$ is the cost of an $n$-limb product: division is as fast as multiplication, up to a constant factor. With [Schönhage-Strassen](/schonhage-strassen-multiplication/) or faster products, this is the division of the fastest big-number libraries for very large sizes, and the same iteration is used for division in floating-point hardware.

## In plain words

Dividing by 7 is the same as multiplying by $1/7$. If we had $1/7 = 0.142857\ldots$ to enough digits, a division would be one multiplication.

Newton's method finds the reciprocal with multiplications only. Take a guess $x$ for $1/D$. Then $D \cdot x$ is close to 1, and the miss is $e = 1 - Dx$. The improved guess is $x + x \cdot e$. The new miss is $e^2$: if the first guess was right to 3 digits, the next is right to 6, then 12, then 24. So a few steps are enough, and the early steps can work with short numbers, because they only need a few digits. The final step at full length costs about as much as a few multiplications.

## The problem

The input is integers $A \ge 0$ and $D > 0$ as arrays of limbs in radix $\beta = 2^w$, the divisor $D$ of $n$ limbs and $A$ of at most $2n$ limbs. The output is the quotient $q = \lfloor A/D \rfloor$ and the remainder $r = A - qD$, with $0 \le r < D$; see [integer division](/integer-division/) and [division with remainder](/division-with-remainder/). A longer dividend is divided in blocks of $n$ limbs, as in [long division](/long-division/). The algorithm is written with $B$ binary digits of $D$, so $2^{B-1} \le D < 2^B$, and the reciprocal $R = \lfloor 4^B / D \rfloor$, which has $B + 1$ binary digits.

**Cost model.** Word RAM with $w$-bit words. Costs are in limb operations, and $M(n)$ is the cost of an $n$-limb product, assumed to satisfy $M(2n) \ge 2M(n)$. The bound $O(M(n))$ and the correction bounds are proved; the constants and the counts of corrections are also measured.

## The algorithm

```pseudo id=main
RECIPROCAL(D)                              ▷ D of B binary digits; returns ⌊4^B / D⌋
L1  if B ≤ B0 then return ⌊4^B / D⌋ by a short division
L2  h ← ⌈B/2⌉;  D_h ← ⌊D / 2^(B − h)⌋            ▷ the top h binary digits of D
L3  X_h ← RECIPROCAL(D_h)                          ▷ ⌊4^h / D_h⌋
L4  X ← X_h · 2^(B − h)                            ▷ about h correct digits
L5  E ← 4^B − D·X                                  ▷ the residual, may be negative
L6  X ← X + ⌊X·E / 4^B⌋   (rounded toward −∞)      ▷ one Newton step
L7  E ← 4^B − D·X;  while E ≥ D do X ← X + 1, E ← E − D
L8  return X

DIVIDE(U, D, R)                            ▷ 0 ≤ U < D·2^B, R = RECIPROCAL(D)
L9  q ← ⌊U·R / 4^B⌋;  r ← U − q·D
L10 while r ≥ D do q ← q + 1, r ← r − D;  return (q, r)
```

The divisions by $4^B$ and $2^{B-h}$ are shifts. Line L6 rounds toward $-\infty$, so that the new $X$ never exceeds $4^B / D$; then line L7 only has to count up. Line L9 is one product of a $2B$-digit number by a $(B + 1)$-digit number, and only its top half is needed. A dividend of more than $2B$ digits is divided by applying DIVIDE to blocks of $B$ digits from the top, carrying the remainder into the next block, with the same $R$ each time.

## Example

**The reciprocal of $D = 50000$.** $D$ has $B = 16$ binary digits, so $h = 8$ and $D_h = \lfloor 50000 / 2^8 \rfloor = 195$. The recursive call gives $X_h = \lfloor 4^8 / 195 \rfloor = 336$, so $X = 336 \cdot 2^8 = 86016$. Line L5 gives $E = 2^{32} - 50000 \cdot 86016 = -5832704$: the start is a bit too large. Line L6 subtracts $\lceil 86016 \cdot 5832704 / 2^{32} \rceil = \lceil 116.81 \rceil = 117$ and gives $X = 85899$. Line L7 finds $E = 2^{32} - 50000 \cdot 85899 = 17296 < D$, so no correction is needed, and indeed $\lfloor 2^{32}/50000 \rfloor = 85899$.

**A division.** For $A = 3141592653$, line L9 gives $q = \lfloor 3141592653 \cdot 85899 / 2^{32} \rfloor = 62831$, and $r = 3141592653 - 62831 \cdot 50000 = 42653 < D$: no correction, and $3141592653 = 62831 \cdot 50000 + 42653$.

**The error squares.** In real numbers, for $d = 0.76$ and $x_0 = 1$, the misses $1 - dx_k$ are $0.24$, $0.0576$, $0.00332$, $1.10 \cdot 10^{-5}$ and $1.21 \cdot 10^{-10}$: each is the square of the previous one. All values were computed by script, and the integer ones are checked by the test of this page.

## Correctness

Write $R^* = 4^B/D$, a real number, and $X^*$ for the exact Newton step of line L6 without rounding. The key identity is that a Newton step squares the residual: if $E = 4^B - DX$, then $X^* = X + XE/4^B$ satisfies $4^B - DX^* = E^2/4^B \ge 0$. So $X^* \le R^*$ whatever the start, and $R^* - X^* = E^2/(4^B D)$. Line L3 gives a start whose error is less than $4 \cdot 2^{B-h}$ in absolute value, so $E$ is less than $4D \cdot 2^{B-h}$ in absolute value, and $R^* - X^* < 16 \cdot D 4^{B-h}/4^B \le 16$ since $2h \ge B$. Rounding toward $-\infty$ in line L6 loses less than 1, so after line L6, $R^* - 17 < X \le R^*$, and line L7 adds at most 16 to reach $\lfloor R^* \rfloor$; its loop ends exactly at $X = \lfloor 4^B/D \rfloor$, because $0 \le E < D$ characterizes the floor. For line L9, $R > R^* - 1$ gives $q > U/D - U/4^B - 1 > U/D - 2$, since $U < D 2^B \le 4^B$, and $R \le R^*$ gives $q \le U/D$; so the integer $q$ is $\lfloor U/D \rfloor$ or $\lfloor U/D \rfloor - 1$, and line L10 adds at most 1. The full proof is below.

## Complexity

**The reciprocal.** At precision $B$, lines L5 to L7 make three products of numbers of about $B$ binary digits and $O(B)$ further work, since line L7 runs at most 16 times. With $n$ limbs and $M(2n) \ge 2M(n)$, the cost satisfies $T(n) = T(\lceil n/2 \rceil) + 3M(n) + O(n)$, so

$$T(n) \le 3M(n)\Big(1 + \tfrac12 + \tfrac14 + \cdots\Big) + O(n) \le 6M(n) + O(n) = O(M(n)) .$$

The recursion has depth $\lceil \log_2 (B/B_0) \rceil$, logarithmic. Careful implementations reduce the constant: line L5 needs only the middle part of the product $DX$, which is known to be close to $4^B$, and line L6 needs only the top half of $XE$; Brent and Zimmermann analyze such versions in Section 3.4.

**The division.** Lines L9 and L10 add two products, so dividing $2n$ limbs by $n$ limbs costs $O(M(n))$, proved. For a dividend of $m \ge 2n$ limbs there are $m/n$ blocks, and the cost is $O((m/n) M(n))$ with one reciprocal for all blocks.

**Measured.** For random divisors of $B = 1024$, $4096$ and $16384$ binary digits, the implementation made 21, 27 and 33 products, with a total length of the factors of about $7B$, and recursion depths 7, 9 and 11. Over many random and extreme divisors, line L7 never needed more than 7 corrections, against the proved 16. These counts are observations. Which division method is fastest at a given size depends on the multiplication code; GMP, for example, switches from divide and conquer division to a Newton-based method at sizes of the order of a thousand limbs or more, by tuned thresholds.

## Properties

- **Division as fast as multiplication.** $O(M(n))$, with any multiplication algorithm, including FFT methods.
- **Multiplications and subtractions only.** No trial quotient digits and no normalization loop, unlike long division.
- **Self-correcting.** Errors of the early steps are squared away by the later ones; only the final result needs a correction, and it is bounded.
- **Reusable reciprocal.** Many divisions by the same $D$ cost one reciprocal and two products each, the idea behind [Barrett reduction](/barrett-reduction/) and [division by a constant](/division-by-constant/).
- **Recursive, logarithmic depth.** One level per doubling of the precision.

## Variants and improvements

- **Floating-point hardware.** Processors without a divider, or with a fused multiply-add, compute $1/d$ from a table and two or three Newton steps $x \leftarrow x(2 - dx)$; the Cray-1 divided this way, and later designs with a fused multiply-add, such as IBM POWER and Intel Itanium, compute a correctly rounded quotient from such steps.
- **Goldschmidt division.** Multiply numerator and denominator by the same factors $2 - d_k$ until the denominator is 1; the two products of a step are independent and can run in parallel. It is the same convergence in another order, used in the IBM System/360 Model 91 and in later floating-point units; see [Goldschmidt division](/goldschmidt-division/).
- **Karp-Markstein.** Fold the multiplication by $A$ into the last Newton step, which saves about one product.
- **Divide and conquer division.** [Burnikel-Ziegler division](/burnikel-ziegler-division/) recurses on blocks with Karatsuba products and is faster than the Newton method in the middle range of sizes.
- **Other Newton iterations.** The same idea gives the [integer square root and $k$-th roots](/newton-integer-root/) and power series reciprocals of polynomials; see [Newton iteration](/newton-iteration/).
- **Exact division.** When $D$ is known to divide $A$, Hensel's method computes $A/D$ from the low end with a 2-adic Newton inverse.

## When to use it

Use Newton-Raphson division for very large operands, where multiplication is subquadratic and division should follow it, as in computing digits of constants and in fast [radix conversion](/radix-conversion/). Use it also when many numbers are divided by the same divisor, by computing the reciprocal once. For small and medium sizes, [long division](/long-division/) and Burnikel-Ziegler division are faster, and a library should switch between them by measured thresholds.

## Pitfalls

- **Rounding the wrong way.** If line L6 rounds up or to nearest, $X$ can exceed $\lfloor 4^B/D \rfloor$, and a correction loop that only counts up never fixes it. Either round down or correct in both directions.
- **Too few digits in the start.** The step doubles the number of correct digits only if the start already has about half; a start with only a few correct digits needs several steps at full precision.
- **Forgetting the final correction.** The reciprocal and the quotient are each too small by a bounded amount; without lines L7 and L10, quotients are occasionally off by one, rarely enough to pass casual tests.
- **Division by zero and unnormalized divisors.** $B$ is the exact length of $D$; a divisor with leading zero limbs must be trimmed first, and $D = 0$ must be rejected.
- **Dividends too long for one block.** Line L9 is valid only for $U < D 2^B$; a longer dividend must be split into blocks.

## Implementations

## History

Newton (1669) and Raphson (1690) gave the iteration for roots of equations, and its use for reciprocals is old: early computers without division hardware divided by subroutines, and a reciprocal iteration was one of the standard ones. In the theory of computation, Cook's thesis of 1966 showed that division costs a constant number of multiplications, by Newton's method with increasing precision, and Knuth's Volume 2 gave the method as Algorithm R. In hardware, the IBM System/360 Model 91 (1967) used Goldschmidt's form, and many floating-point units since then compute reciprocals by a table lookup and Newton steps. In big-number libraries, Newton division with FFT multiplication gives the fastest division for very large numbers, with constants studied in detail by Brent and Zimmermann and others.

## References
