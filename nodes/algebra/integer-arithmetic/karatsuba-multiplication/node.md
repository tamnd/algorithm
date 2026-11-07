---
tag: QWY1MV
kind: algorithm
slug: karatsuba-multiplication
name: Karatsuba multiplication
aliases:
- Karatsuba's algorithm
- Karatsuba-Ofman multiplication
- Toom-2
- Toom-22
area: algebra/integer-arithmetic
level: core
summary: Divide-and-conquer multiplication using three half-size products, running in O(n^(log2 3)) time.
solves: [integer-multiplication]
model: word-ram
complexity:
  vars: {n: the number of limbs of each operand}
  time: {worst: Θ(n^(log2 3)), average: Θ(n^(log2 3)), best: Θ(n^(log2 3))}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, in_place: false}
prereqs: [schoolbook-multiplication, divide-and-conquer-paradigm, master-theorem]
see_also: [toom-cook-multiplication, schonhage-strassen-multiplication, schoolbook-multiplication, polynomial-multiplication, integer-multiplication, kronecker-substitution, multiprecision-integer, burnikel-ziegler-division]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.3, How fast can we multiply? (the identity with three half-size products, the bound O(n^(log2 3)), and the history)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3.2, Karatsuba's algorithm (Algorithm KaratsubaMultiply, the subtractive variant, the threshold), Section 1.3.5, Unbalanced multiplication, and Section 1.3.6, Squaring
  - paper: A. A. Karatsuba, The complexity of computations, Proceedings of the Steklov Institute of Mathematics 211, 1995
    locator: pp. 169 to 183 (Kolmogorov's n^2 conjecture, the seminar of 1960, and the publication of 1962)
  - url: https://gmplib.org/manual/Karatsuba-Multiplication
    title: The GNU Multiple Precision Arithmetic Library manual, Karatsuba Multiplication
    locator: Section 15.1.2 (the formula used by GMP, the threshold MUL_TOOM22_THRESHOLD, and squaring)
---

Karatsuba multiplication multiplies two $n$-limb numbers with three products of half the size instead of four. Split each factor into a high half and a low half, $a = a_1\beta^h + a_0$ and $b = b_1\beta^h + b_0$; then $ab = z_2\beta^{2h} + z_1\beta^h + z_0$ with $z_2 = a_1b_1$, $z_0 = a_0b_0$, and $z_1 = (a_0 + a_1)(b_0 + b_1) - z_0 - z_2$, so the middle term costs one product instead of two. Applied recursively, this gives $M(n) = 3M(n/2) + O(n)$, so $M(n) = \Theta(n^{\log_2 3}) \approx n^{1.585}$ limb operations on the [word RAM](/word-ram/), against $\Theta(n^2)$ for the [schoolbook method](/schoolbook-multiplication/). Found by Karatsuba in 1960 and published in 1962, it was the first method to beat $n^2$, against a conjecture of Kolmogorov. Libraries use it above a machine-dependent threshold of a few dozen limbs, and below the range of [Toom-Cook](/toom-cook-multiplication/) and FFT methods.

## In plain words

To multiply two long numbers, cut each into a front half and a back half. The schoolbook way multiplies every half by every half: four smaller products. Karatsuba saw that three are enough. Multiply the two front halves, and the two back halves. Then add the halves of each number and multiply the two sums. That last product contains the two cross terms you need, plus the two products you already have; subtract those, and the cross terms are left.

Then do the same trick for each of the three smaller products, and again, until the pieces are small. Each level saves a quarter of the work, and the savings add up: for numbers with a thousand digits, splitting down to single digits needs about one seventeenth of the digit products of the schoolbook way, though it adds more additions.

## The problem

The input is two nonnegative integers given as arrays of $n$ limbs in radix $\beta = 2^w$, least significant limb first: $a = \sum_{i<n} a_i\beta^i$ and $b = \sum_{i<n} b_i\beta^i$. The output is the $2n$ limbs of $ab$. Operands of different lengths are handled by padding or by splitting, see Variants. Signed values are multiplied by the sign rule on [sign-magnitude](/sign-magnitude-representation/) [multiprecision integers](/multiprecision-integer/).

**Cost model.** Word RAM with $w$-bit words. A limb operation is the addition or subtraction of two limbs with a carry, or the product of two limbs into two limbs. $M(n)$ is the cost of an $n$-limb product. The exponent $\log_2 3$ is proved. The threshold below which the schoolbook method is faster is observed, and depends on the machine.

## The algorithm

```pseudo id=main
KARATSUBA(a, b)                          ▷ a, b of n limbs; returns 2n limbs
L1  if n ≤ T then return SCHOOLBOOK(a, b)          ▷ T ≥ 1, the threshold
L2  h ← ⌈n/2⌉;  a = a1·β^h + a0;  b = b1·β^h + b0  ▷ a0, b0, a1, b1 of h limbs
L3  z0 ← KARATSUBA(a0, b0)
L4  z2 ← KARATSUBA(a1, b1)
L5  z1 ← KARATSUBA(a0 + a1, b0 + b1) − z0 − z2     ▷ = a0·b1 + a1·b0
L6  return z0 + z1·β^h + z2·β^(2h)
```

Line L2 needs no arithmetic: the halves are slices of the limb arrays, and for odd $n$ the high halves are padded with a zero limb. The sums $a_0 + a_1$ and $b_0 + b_1$ of line L5 can have $h + 1$ limbs. The implementation keeps the recursion on $h$ limbs by splitting off the carry bits: if $a_0 + a_1 = s + c\beta^h$ and $b_0 + b_1 = t + d\beta^h$ with $c, d \in \{0, 1\}$, then $(a_0 + a_1)(b_0 + b_1) = st + (ct + ds)\beta^h + cd\beta^{2h}$, one recursive product and two additions. Line L6 adds three shifted arrays.

## Example

**One level in radix $\beta = 100$.** Multiply $a = 1234$ and $b = 5678$, each of $n = 2$ limbs of two decimal digits, with $h = 1$: $a_1 = 12$, $a_0 = 34$, $b_1 = 56$, $b_0 = 78$.

| quantity | value |
|---|---|
| $z_2 = a_1 b_1$ | $12 \cdot 56 = 672$ |
| $z_0 = a_0 b_0$ | $34 \cdot 78 = 2652$ |
| $(a_0 + a_1)(b_0 + b_1)$ | $46 \cdot 134 = 6164$ |
| $z_1 = 6164 - 2652 - 672$ | $2840 = 34 \cdot 56 + 12 \cdot 78$ |
| $z_0 + z_1\beta + z_2\beta^2$ | $2652 + 284000 + 6720000 = 7006652$ |

Three products of two-digit numbers instead of four, and $1234 \cdot 5678 = 7006652$. The values were checked by script.

**Counting products.** With $T = 1$ and $n = 2^j$, the recursion makes exactly $3^j = n^{\log_2 3}$ limb products, against $4^j = n^2$ for the schoolbook method: 2187 instead of 16384 for $n = 128$. The tests of this page check this count for $j = 0, \ldots, 7$.

## Correctness

The identity behind line L5 is

$$(a_0 + a_1)(b_0 + b_1) - a_0b_0 - a_1b_1 = a_0b_1 + a_1b_0 ,$$

so $z_0 + z_1\beta^h + z_2\beta^{2h} = a_0b_0 + (a_0b_1 + a_1b_0)\beta^h + a_1b_1\beta^{2h} = (a_1\beta^h + a_0)(b_1\beta^h + b_0) = ab$. By strong induction on $n$, with the schoolbook method correct for $n \le T$, each recursive call returns the exact product, since its operands have $h < n$ limbs for $n \ge 2$. The subtraction in line L5 never goes negative, because the result $a_0b_1 + a_1b_0$ is nonnegative, and the final value $ab < \beta^{2n}$ fits in $2n$ limbs. The full proof is below.

## Complexity

**The recurrence.** Splitting and the additions and subtractions in lines L5 and L6 take $O(n)$ limb operations, and there are three recursive products of $h = \lceil n/2 \rceil$ limbs, so

$$M(n) = 3M(\lceil n/2 \rceil) + \Theta(n) \quad (n > T), \qquad M(n) = \Theta(n^2) \quad (n \le T) .$$

By the [master theorem](/master-theorem/) with $a = 3$, $b = 2$ and $f(n) = \Theta(n)$, and since $\log_2 3 > 1$, the solution is $M(n) = \Theta(n^{\log_2 3})$, about $n^{1.585}$, for every input: the recursion does not depend on the values. This bound is proved. Unrolled, level $i$ of the recursion has $3^i$ calls of size $n/2^i$ and costs $\Theta(n(3/2)^i)$, so the levels grow geometrically and the leaves dominate.

**Constants.** Each level does a constant number of additions and subtractions of $O(h)$ limbs, so the number of limb additions is also $\Theta(n^{\log_2 3})$, with a larger constant than the products. The schoolbook method has $n^2$ products and about $2n^2$ additions with simple loops, so it is faster for small $n$. The crossover is observed, not proved: the GMP manual says that its threshold MUL_TOOM22_THRESHOLD can be as small as 10 limbs on some machines, and it is tuned for each processor; the threshold for squaring is usually about twice as large. Brent and Zimmermann discuss the threshold in Section 1.3.2.

**Space.** Each call holds $O(n)$ limbs of temporaries while it recurses, and the sizes halve along the path of the recursion, so the extra space is $O(n) + O(n/2) + \cdots = \Theta(n)$. The recursion depth is $\lceil \log_2 (n/T) \rceil + O(1)$, logarithmic.

## Properties

- **Exact.** Integer arithmetic only, no rounding, unlike the FFT methods.
- **Deterministic and oblivious.** The sequence of operations depends only on $n$, which suits constant-time code for cryptography.
- **Recursive, logarithmic depth.** About $\log_2 (n/T)$ levels.
- **Fewer multiplications, more additions.** It trades one product of size $h$ for a few additions of size $h$ at each level; it wins when products cost more than additions, which for limbs is true only at the scale of whole sub-products.
- **Works over any ring.** The identity uses only addition, subtraction and multiplication, so the same method multiplies polynomials over any commutative ring, see [polynomial multiplication](/polynomial-multiplication/).

## Variants and improvements

- **Subtractive Karatsuba.** Use $z_1 = z_0 + z_2 - (a_0 - a_1)(b_0 - b_1)$. The differences fit in $h$ limbs with a sign, so no carry limb appears; the sign of the product is the product of the signs. Knuth gives this form, and GMP uses it.
- **Unbalanced operands.** For $m \ge 2n$ limbs times $n$ limbs, cut the longer operand into blocks of $n$ limbs and use Karatsuba on each block, for $O((m/n) n^{\log_2 3})$; the implementation does this. Toom-Cook variants such as Toom-32 split the two operands into different numbers of pieces.
- **Squaring.** $(a_0 + a_1)^2 - a_0^2 - a_1^2 = 2a_0a_1$, so a square needs three half-size squares, which are cheaper than products at every level.
- **Toom-Cook.** Splitting into $k$ pieces and evaluating at $2k - 1$ points gives $\Theta(n^{\log_k (2k-1)})$; Karatsuba is the case $k = 2$, evaluation at $0$, $1$ and infinity. See [Toom-Cook multiplication](/toom-cook-multiplication/).
- **Polynomials over $\mathrm{GF}(2)$.** The same identity, with XOR for addition, is used for carry-less multiplication in cryptography and in coding theory.
- **The next steps.** FFT methods ([Schönhage-Strassen](/schonhage-strassen-multiplication/), 1971) reach $O(n \log n \log \log n)$, and Harvey and van der Hoeven (2019, published 2021) reach $O(n \log n)$ in the bit complexity model.

## When to use it

Use Karatsuba from a threshold of some tens of limbs up to a few hundred limbs, where Toom-3 and then FFT methods take over; this is the order of RSA moduli and of many big integer computations. Below the threshold, use the [schoolbook method](/schoolbook-multiplication/) as the base case. The thresholds should be measured on the target machine, as GMP does with its tuning program. Karatsuba is also a good first fast method to implement, because it is short and exact, and it already changes the exponent.

## Pitfalls

- **Infinite recursion on small inputs.** With $h = \lceil n/2 \rceil$, the sums have $h + 1$ limbs, and for $n \le 3$ this is not smaller than $n$. Either use a threshold $T \ge 3$, or split off the carry bits as the implementation does, so that the recursive calls have $h < n$ limbs.
- **Signs in the subtractive variant.** $(a_0 - a_1)(b_0 - b_1)$ can be negative; the sign must be tracked, and $z_1 = z_0 + z_2 - (\ldots)$ must use it.
- **Too small a threshold.** Recursing down to single limbs is correct but slow; the base case should be the schoolbook method for small sizes.
- **Odd sizes.** For odd $n$, the high halves have $n - h = h - 1$ limbs. Either pad them with a zero limb, as the pseudocode does, or handle the unequal halves directly.
- **Unbalanced operands.** Padding a 1-limb operand to $n$ limbs and calling Karatsuba costs $\Theta(n^{\log_2 3})$ instead of $\Theta(n)$. Split the longer operand into blocks instead.
- **Carries in line L6.** The three shifted arrays overlap, and a carry out of $z_1\beta^h$ can run into the part of $z_2\beta^{2h}$; propagate each carry to the end of the buffer. All three terms are nonnegative, so no partial sum exceeds $ab < \beta^{2n}$.

## Implementations

## History

In 1956, and again at a seminar at Moscow State University in 1960, Andrey Kolmogorov conjectured that any method for multiplying two $n$-digit numbers needs a number of operations of order $n^2$. Anatoly Karatsuba, then a student at the seminar, found the method with three half-size products within about a week, and so disproved the conjecture. Kolmogorov presented the result, and it was published in 1962 in Doklady Akademii Nauk SSSR as a paper by A. Karatsuba and Yu. Ofman; Karatsuba later wrote that the paper had been prepared by Kolmogorov and that he learned of it only after it was published. The method was the start of fast multiplication: Toom (1963) and Cook (1966) generalized it to $k$ pieces, Schönhage and Strassen (1971) used the FFT, Fürer (2007) improved the bound further, and Harvey and van der Hoeven (2019, published 2021) reached $O(n \log n)$.

## References
