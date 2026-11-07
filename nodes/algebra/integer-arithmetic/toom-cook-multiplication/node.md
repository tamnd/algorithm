---
tag: KFMRJ2
kind: algorithm
slug: toom-cook-multiplication
name: Toom-Cook multiplication
aliases:
- Toom-3
- Toom-Cook-k
- Toom-33
- Toom-Cook algorithm
area: algebra/integer-arithmetic
level: advanced
summary: Splits integers into k parts, evaluates at points and interpolates, generalizing Karatsuba.
solves: [integer-multiplication]
model: word-ram
complexity:
  vars: {n: the number of limbs of each operand}
  time: {worst: Θ(n^(log3 5)), average: Θ(n^(log3 5)), best: Θ(n^(log3 5))}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, in_place: false}
prereqs: [karatsuba-multiplication, evaluation-interpolation-paradigm, lagrange-interpolation]
see_also: [karatsuba-multiplication, schonhage-strassen-multiplication, schoolbook-multiplication, integer-multiplication, polynomial-multiplication, evaluation-interpolation-paradigm, vandermonde-matrix, kronecker-substitution]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.3, How fast can we multiply? (part A, the generalization of Karatsuba's method to r + 1 pieces, Algorithm T, and the bound with k growing with n)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3.3, Toom-Cook multiplication (Algorithm ToomCook3, the choice of points and the interpolation), and Section 1.3.5, Unbalanced multiplication
  - paper: A. L. Toom, The complexity of a scheme of functional elements realizing the multiplication of integers, Soviet Mathematics Doklady 3, 1963
    title: Andrei L. Toom, The complexity of a scheme of functional elements realizing the multiplication of integers
    locator: pp. 714 to 716 (circuits for multiplication by evaluation at many points)
  - paper: S. A. Cook, On the minimum computation time of functions, PhD thesis, Harvard University, 1966
    title: Stephen A. Cook, On the minimum computation time of functions
    locator: the chapter on multiplication (Toom's method as an algorithm for multitape machines)
  - paper: M. Bodrato, Towards optimal Toom-Cook multiplication for univariate and multivariate polynomials in characteristic 2 and 0, WAIFI 2007, Lecture Notes in Computer Science 4547
    title: Marco Bodrato, Towards optimal Toom-Cook multiplication for univariate and multivariate polynomials in characteristic 2 and 0
    locator: pp. 116 to 133 (the evaluation at 0, 1, -1, -2 and infinity and the interpolation sequence used here)
  - url: https://gmplib.org/manual/Toom-3_002dWay-Multiplication
    title: The GNU Multiple Precision Arithmetic Library manual, Toom 3-Way Multiplication
    locator: Section 15.1.3 (the points used by GMP, the interpolation, and the threshold MUL_TOOM33_THRESHOLD)
---

Toom-Cook multiplication cuts each $n$-limb factor into $k$ pieces and reads the pieces as the coefficients of a polynomial of degree $k - 1$, so that $a = A(\beta^h)$ and $b = B(\beta^h)$. The product polynomial $C = AB$ has degree $2k - 2$, so its $2k - 1$ coefficients are fixed by its values at $2k - 1$ points. The method evaluates $A$ and $B$ at those points, multiplies the values with $2k - 1$ recursive products of about $n/k$ limbs, recovers the coefficients of $C$ by interpolation, and adds them with shifts. This gives $M(n) = (2k - 1)M(n/k) + O(n)$, so $M(n) = \Theta(n^{\log_k (2k - 1)})$ limb operations on the [word RAM](/word-ram/). [Karatsuba multiplication](/karatsuba-multiplication/) is the case $k = 2$. The case $k = 3$, Toom-3, uses five products of a third of the size and costs $\Theta(n^{\log_3 5}) \approx n^{1.465}$. Toom described the idea in 1963 and Cook made it an algorithm in his 1966 thesis. Libraries use Toom-3 and larger $k$ in the range between Karatsuba and FFT methods.

## In plain words

Karatsuba cuts each number in two and gets by with three products instead of four. Toom-Cook cuts each number into more pieces. With three pieces each, the schoolbook way needs nine products of pieces, and Toom-3 needs only five.

The trick is to treat the pieces as the coefficients of a quadratic, like $12x^2 + 34x + 56$ for the number 123456 cut into pairs of digits, where $x$ stands for 100. The product of two quadratics is a polynomial of degree four, and such a polynomial is known as soon as its values at five points are known. So put five simple numbers, such as $0, 1, -1, -2$ and "infinity", into both quadratics, multiply the five pairs of values, and solve back for the five coefficients. Finally put $x = 100$ back in. Each of the five products is again done the same way.

## The problem

The input is two nonnegative integers given as arrays of $n$ limbs in radix $\beta = 2^w$, least significant limb first. The output is the $2n$ limbs of their product; see [integer multiplication](/integer-multiplication/).

**Cost model.** Word RAM with $w$-bit words. A limb operation adds, subtracts or multiplies limbs with a carry, or divides two limbs by a small constant. $M(n)$ is the cost of an $n$-limb product. The exponents $\log_k (2k - 1)$ are proved. The thresholds at which one method beats another are observed, and depend on the machine and the code.

## The algorithm

Toom-3, with the evaluation points $0, 1, -1, -2, \infty$ and Bodrato's interpolation sequence. The value of a polynomial "at infinity" is its leading coefficient.

```pseudo id=main
TOOM-3(a, b)                               ▷ a, b of n limbs; returns 2n limbs
L1  if n ≤ T then return SCHOOLBOOK(a, b)            ▷ T ≥ 2, the threshold
L2  k ← ⌈n/3⌉;  a = a2·x^2 + a1·x + a0,  b = b2·x^2 + b1·x + b0  with x = β^k
L3  for c in {a, b}:  p ← c0 + c2;  c(0) ← c0;  c(1) ← p + c1;  c(−1) ← p − c1;
        c(−2) ← 2·(c(−1) + c2) − c0;  c(∞) ← c2
L4  for t in {0, 1, −1, −2, ∞}:  v(t) ← a(t) · b(t)    ▷ five recursive products, signs apart
L5  r0 ← v(0);  r4 ← v(∞);  r3 ← (v(−2) − v(1)) / 3;  r1 ← (v(1) − v(−1)) / 2;  r2 ← v(−1) − v(0)
        r3 ← (r2 − r3) / 2 + 2·r4;  r2 ← r2 + r1 − r4;  r1 ← r1 − r3
L6  return r0 + r1·x + r2·x^2 + r3·x^3 + r4·x^4
```

Line L2 needs no arithmetic: the pieces are slices of $k$ limbs, and the top piece may be shorter. The values of line L3 can be negative and can have $k + 1$ limbs, since $-2\beta^k < c(-2) < 5\beta^k$; line L4 multiplies their magnitudes recursively and attaches the product of the signs. The divisions by 2 and by 3 in line L5 are exact, and each is one pass over the limbs. All five coefficients $r_i$ are nonnegative, because they are the coefficients of $A(x)B(x)$, and line L6 adds them with shifts of $ik$ limbs.

## Example

**One level in radix $\beta = 100$.** Multiply $a = 123456$ and $b = 789012$, each of $n = 3$ limbs of two decimal digits, so $k = 1$ and $x = 100$: $A(x) = 12x^2 + 34x + 56$ and $B(x) = 78x^2 + 90x + 12$.

| point $t$ | $A(t)$ | $B(t)$ | $v(t) = A(t)B(t)$ |
|---|---|---|---|
| $0$ | 56 | 12 | 672 |
| $1$ | 102 | 180 | 18360 |
| $-1$ | 34 | 0 | 0 |
| $-2$ | 36 | 144 | 5184 |
| $\infty$ | 12 | 78 | 936 |

Line L5 computes $r_3 = (5184 - 18360)/3 = -4392$, $r_1 = (18360 - 0)/2 = 9180$ and $r_2 = 0 - 672 = -672$; then $r_3 = (-672 + 4392)/2 + 2 \cdot 936 = 3732$, $r_2 = -672 + 9180 - 936 = 7572$ and $r_1 = 9180 - 3732 = 5448$. So $C(x) = 936x^4 + 3732x^3 + 7572x^2 + 5448x + 672$, which is the schoolbook result: for instance $7572 = 56 \cdot 78 + 34 \cdot 90 + 12 \cdot 12$. With $x = 100$, line L6 gives $97408265472 = 123456 \cdot 789012$. Five products of pieces instead of nine; intermediate values such as $-4392$ are negative, but the final coefficients are not. The values were checked by script, and the test of this page repeats them.

**Counting products.** For $n = 729$ limbs and $T = 8$, the recursion has depth 5 and makes $78125$ limb products, against $531441$ for the schoolbook method; for $n = 2187$ it makes $390625$ against $4782969$. Counted by the implementation.

## Correctness

Let $C(x) = A(x)B(x) = r_0 + r_1x + r_2x^2 + r_3x^3 + r_4x^4$, so that $ab = C(\beta^k)$. Line L3 computes $A$ and $B$ at the five points: $A(-2) = 4a_2 - 2a_1 + a_0 = 2(a_0 - a_1 + a_2 + a_2) - a_0$. By induction on $n$, line L4 gives $v(t) = C(t)$, with $v(\infty) = r_4$. The five values are

$$v(0) = r_0, \quad v(1) = \textstyle\sum_i r_i, \quad v(-1) = \sum_i (-1)^i r_i, \quad v(-2) = \sum_i (-2)^i r_i, \quad v(\infty) = r_4 ,$$

and following line L5 step by step gives $(v(-2) - v(1))/3 = -r_1 + r_2 - 3r_3 + 5r_4$, $(v(1) - v(-1))/2 = r_1 + r_3$ and $v(-1) - v(0) = -r_1 + r_2 - r_3 + r_4$, from which the last three assignments give $r_3$, $r_2$ and $r_1$ exactly. So line L6 returns $C(\beta^k) = ab$. The recursion ends because the operands of line L4 have $k + 1 < n$ limbs for $n \ge 3$. The full proof is below.

## Complexity

**The recurrence.** Lines L2, L3, L5 and L6 cost $O(n)$ limb operations, and line L4 makes five products of $k + 1 = \lceil n/3 \rceil + 1$ limbs, so

$$M(n) = 5M(\lceil n/3 \rceil + 1) + \Theta(n) \quad (n > T) .$$

The extra limb changes only the constant, and the [master theorem](/master-theorem/) with $a = 5$, $b = 3$ and $f(n) = \Theta(n)$ gives $M(n) = \Theta(n^{\log_3 5})$, about $n^{1.465}$, for every input. This bound is proved. The depth of the recursion is $\log_3 (n/T) + O(1)$, logarithmic, and the extra space is $\Theta(n)$, as for Karatsuba.

**Toom-$k$.** With $k$ pieces and $2k - 1$ points, $M(n) = (2k - 1)M(n/k) + O(n)$ for fixed $k$, so $M(n) = \Theta(n^{\log_k (2k - 1)})$: the exponents are $1.585$, $1.465$, $1.404$ and $1.365$ for $k = 2, 3, 4, 5$, and they tend to 1. But the constant in $O(n)$ grows with $k$: the points get larger, so the values get longer, and the interpolation divides by larger numbers. Knuth's Algorithm T lets $k$ grow with $n$ and reaches $O(n \, 2^{\sqrt{2 \log_2 n}} \log n)$, which is $O(n^{1 + \varepsilon})$ for every $\varepsilon > 0$.

**In practice.** The thresholds are observed, not proved. Toom-3 has more additions than Karatsuba, so it wins only from about a hundred limbs; GMP tunes its threshold MUL_TOOM33_THRESHOLD for each processor and uses Toom-4, Toom-6.5 and Toom-8.5 for larger sizes before switching to FFT multiplication. Brent and Zimmermann discuss the thresholds in Section 1.3.

## Properties

- **Exact.** Integer arithmetic only; the divisions in the interpolation are exact.
- **Deterministic and oblivious.** The sequence of operations depends only on $n$, apart from the signs of the values.
- **Recursive, logarithmic depth.** About $\log_3 (n/T)$ levels for Toom-3.
- **Signed intermediates.** Negative points make negative values, and the interpolation passes through negative numbers even when all inputs are positive.
- **Works over many rings.** The same method multiplies polynomials over any ring in which the interpolation divisors (here 2 and 3) are invertible; in characteristic 2 other points are needed.

## Variants and improvements

- **Choice of points.** Any $2k - 1$ distinct points work, including $\infty$. Small points keep the values short, and Bodrato searched for the evaluation and interpolation sequences with the fewest and cheapest operations; the sequence above, with one division by 3 and two by 2, is his choice for Toom-3, also used in GMP.
- **Unbalanced operands.** Toom-32 cuts one operand into three pieces and the other into two and uses four points; Toom-42, Toom-53 and others serve other shape ratios, so that unequal operands are not padded.
- **Squaring.** $A(t)^2$ needs one value per point, and squaring sub-products are cheaper; libraries have separate Toom squaring thresholds.
- **Larger $k$.** Toom-4 uses seven products of quarter size; GMP's Toom-6.5 and Toom-8.5 use half-integer splits, where the two operands are cut into pieces of slightly different sizes.
- **Polynomials.** The same scheme multiplies polynomials; with [Kronecker substitution](/kronecker-substitution/) polynomial products also reduce to integer products and back.
- **The limit of the method.** With $k$ growing, the cost approaches $n^{1+\varepsilon}$ but not $n \log n$; FFT methods such as [Schönhage-Strassen](/schonhage-strassen-multiplication/) (1971), Fürer (2007), and Harvey and van der Hoeven (2019, published 2021) evaluate at roots of unity, where evaluation and interpolation are fast transforms.

## When to use it

Use Toom-3 between the Karatsuba range and the FFT range, roughly from a hundred to a few thousand limbs depending on the machine, and larger $k$ as the sizes grow; measure the thresholds on the target machine. For small sizes use the [schoolbook method](/schoolbook-multiplication/) or [Karatsuba](/karatsuba-multiplication/), and for very large sizes [Schönhage-Strassen](/schonhage-strassen-multiplication/) or other FFT methods. Toom-3 is also a good exercise in the evaluation and interpolation view of multiplication, which the FFT methods take to its limit.

## Pitfalls

- **Infinite recursion on small inputs.** The values have $k + 1$ limbs, which is not smaller than $n$ for $n \le 2$; the threshold must be at least 2.
- **Signs.** $A(-1)$ and $A(-2)$ can be negative, and so can the intermediate values of line L5. Track signs explicitly, or work in two's complement with a guard limb.
- **Inexact division.** The division by 3 is exact only in the order given; dividing a different combination by 3 can leave a remainder, and then the result is wrong without warning.
- **Top piece shorter than the others.** When $3 \nmid n$, the piece $a_2$ has fewer than $k$ limbs; pad it, or treat its length separately, but do not read past the end.
- **Thresholds from another machine.** A threshold copied from elsewhere can make Toom-3 slower than Karatsuba over a wide range of sizes.

## Implementations

## History

In 1963 Andrei Toom showed, for Boolean circuits, that splitting the factors into many pieces and evaluating at many points gives circuits for multiplication of size $O(n^{1+\varepsilon})$ for every $\varepsilon > 0$, a year after Karatsuba's three-product method was published in 1962. Stephen Cook's Harvard thesis of 1966 turned the construction into an algorithm for multitape Turing machines, and the method has carried both names since. Knuth's treatment in Volume 2 made it standard, with the version for growing $k$ as Algorithm T. Schönhage and Strassen (1971) replaced the small integer points by roots of unity, so that evaluation and interpolation became fast Fourier transforms. Later work concentrated on the constants: Bodrato's search for optimal evaluation and interpolation sequences (2007) and the implementations of GMP made Toom-3 to Toom-8.5 practical over a wide range of sizes.

## References
