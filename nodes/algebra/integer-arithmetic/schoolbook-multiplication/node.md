---
tag: 7VTRV2
kind: algorithm
slug: schoolbook-multiplication
name: Schoolbook multiplication
aliases:
- grade-school multiplication
- long multiplication
- basecase multiplication
area: algebra/integer-arithmetic
level: intro
summary: Multiply digit by digit and sum shifted partial products in Theta(n^2) digit operations.
solves: [integer-multiplication]
model: word-ram
complexity:
  vars: {m: the number of limbs of the first operand, n: the number of limbs of the second operand}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m + n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [multiprecision-integer, integer-multiplication, loop-invariant]
see_also: [karatsuba-multiplication, toom-cook-multiplication, lattice-multiplication, russian-peasant-multiplication, array-multiplier, long-division, integer-addition]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, Algorithm M (multiplication of nonnegative integers) and its analysis; Section 4.3.3 for the faster methods
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3.1, Naive multiplication, and Section 1.3.6, Squaring
  - url: https://gmplib.org/manual/Multiplication-Algorithms
    title: The GNU Multiple Precision Arithmetic Library manual, Multiplication Algorithms
    locator: Section 15.1.1, Basecase Multiplication, and Section 15.1.2, Karatsuba Multiplication (the threshold MUL_TOOM22_THRESHOLD)
  - paper: A. A. Karatsuba, The complexity of computations, Proceedings of the Steklov Institute of Mathematics 211, 1995
    locator: pp. 169 to 183 (the account of Kolmogorov's n^2 conjecture and its refutation)
---

Schoolbook multiplication computes the product of two integers given as limb arrays by multiplying each limb of one operand by each limb of the other and adding the partial products at their positions, with carries. For operands of $m$ and $n$ limbs in the radix $\beta = 2^w$ it does exactly $mn$ limb products and $\Theta(mn)$ limb operations on the [word RAM](/word-ram/), in every case. It is the method taught in school, Knuth's Algorithm M, and the base case under which every fast method of [integer multiplication](/integer-multiplication/) switches back to it for small sizes.

## In plain words

To multiply 4093 by 199 on paper, you multiply 4093 by each digit of 199 and write each row one place further to the left. Then you add the rows. The computer does the same, but each "digit" is a whole machine word.

The computer does not write all rows first. It keeps one result array and adds each small product into the right place at once, moving the carry to the next place. Each digit of the first number meets each digit of the second number exactly one time. So the work grows with the product of the two lengths: twice as long numbers take four times as long.

## The problem

The input is two nonnegative integers in the radix $\beta = 2^w$, $A = \sum_{i=0}^{m-1} a_i \beta^i$ and $B = \sum_{j=0}^{n-1} b_j \beta^j$, as limb arrays $a$ and $b$ with $0 \le a_i, b_j < \beta$. The output is the array $c$ of $m + n$ limbs with $\sum_k c_k \beta^k = AB$. It exists because $AB \le (\beta^m - 1)(\beta^n - 1) < \beta^{m+n}$. This is the problem [integer multiplication](/integer-multiplication/). For signed operands, multiply the magnitudes and set the sign by the rule $\operatorname{sign}(AB) = \operatorname{sign}(A)\operatorname{sign}(B)$, with the sign $+$ for a zero product, as in the [multiprecision integer](/multiprecision-integer/) representation.

**Cost model.** Costs are in limb operations on the word RAM with $w$-bit words: a product of two limbs into two limbs, an addition of limbs with a carry, a shift or a mask. $M(n)$ is the cost of a product of two $n$-limb numbers; for the schoolbook method this page shows $M(n) = \Theta(n^2)$, with exactly $n^2$ limb products.

## The algorithm

```pseudo id=main
SCHOOLBOOK-MUL(a[0 .. m − 1], b[0 .. n − 1])
L1  c ← an array of m + n zero limbs
L2  for i ← 0 to m − 1 do
L3      carry ← 0
L4      for j ← 0 to n − 1 do
L5          t ← c[i + j] + a[i] · b[j] + carry      ▷ 0 ≤ t ≤ β² − 1, two limbs
L6          c[i + j] ← t mod β                    ▷ the low limb
L7          carry ← ⌊t / β⌋                        ▷ the high limb
L8      c[i + n] ← carry
L9  return c
```

Row $i$ adds the partial product $a_i \cdot B$, shifted by $i$ limbs, into $c$. Line L5 is one limb product and two limb additions, and its result fits in two limbs because

$$t \le (\beta - 1) + (\beta - 1)^2 + (\beta - 1) = \beta^2 - 1 .$$

This bound is the reason why the method works with a $2w$-bit product and no wider sum: the carry of a step is at most $\beta - 1$, one limb. Line L8 needs no addition: position $i + n$ has not been written by an earlier row, because row $i' < i$ writes only positions up to $i' + n < i + n$. So $c[i + n]$ is still 0 when row $i$ ends.

If both inputs are normalized, the top limb $c_{m+n-1}$ can be 0, and a normalized result drops it. The product has $m + n - 1$ or $m + n$ significant limbs, since $AB \ge \beta^{m-1}\beta^{n-1}$.

## Example

Take $w = 4$, so $\beta = 16$. Let $A = 4093$, the limbs $a = [13, 15, 15]$, and $B = 199$, the limbs $b = [7, 12]$ (least significant first). Each row of the table is one run of line L5.

| $i$ | $j$ | $a_i$ | $b_j$ | $c_{i+j}$ before | carry in | $t$ | $c_{i+j}$ after | carry out |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 13 | 7 | 0 | 0 | 91 | 11 | 5 |
| 0 | 1 | 13 | 12 | 0 | 5 | 161 | 1 | 10 |
| 1 | 0 | 15 | 7 | 1 | 0 | 106 | 10 | 6 |
| 1 | 1 | 15 | 12 | 10 | 6 | 196 | 4 | 12 |
| 2 | 0 | 15 | 7 | 4 | 0 | 109 | 13 | 6 |
| 2 | 1 | 15 | 12 | 12 | 6 | 198 | 6 | 12 |

After row 0, line L8 sets $c_2 = 10$, so $c = [11, 1, 10, 0, 0]$, which is $13 \cdot 199 = 2587$. After row 1, $c = [11, 10, 4, 12, 0]$. After row 2, $c = [11, 10, 13, 6, 12]$, that is $\text{0xC6DAB} = 814507 = 4093 \cdot 199$. The product has $m + n = 5$ limbs.

## Correctness

The invariant of the outer loop is: before row $i$, $\sum_k c_k \beta^k = (\sum_{i' < i} a_{i'} \beta^{i'}) \cdot B$, and $c_k = 0$ for $k \ge i + n$. The inner loop adds $a_i B \beta^i$ to $c$ with the carry invariant of [integer addition](/integer-addition/). At the end, $i = m$ gives $\sum_k c_k\beta^k = AB$. The full proof, with the bound on $t$ and the inner invariant, is below.

## Complexity

Line L5 runs exactly $mn$ times, and each run is one limb product, two limb additions, and the split into two limbs. Lines L3 and L8 run $m$ times, and line L1 writes $m + n$ limbs. So the time is $\Theta(mn)$ limb operations, the same for all inputs: the loops do not depend on the values. For $m = n$ this is $M(n) = \Theta(n^2)$. The extra space is the output array of $m + n$ limbs.

**Unbalanced inputs.** The cost $mn$ is linear in the longer operand when the shorter one has a fixed length. For example, multiplying an $n$-limb number by one limb costs $\Theta(n)$. The fast methods gain only when both operands are long.

**Squaring.** For $A^2$, each cross product $a_i a_j$ with $i \ne j$ appears twice. Computing the $n(n-1)/2$ products with $i < j$ once, doubling their sum by a one-bit shift, and adding the $n$ squares $a_i^2$ costs $n(n+1)/2$ limb products instead of $n^2$, so squaring is about twice as fast for large $n$.

**Proved and observed.** The bound $\Theta(n^2)$ is proved. The size where a faster method wins is observed, and depends on the machine and the code. The GMP manual says that the switch to Karatsuba, MUL_TOOM22_THRESHOLD, can be as low as 10 limbs, and that the threshold for squaring is usually about twice that; GMP measures both on each machine with its tuning program. Below the threshold, schoolbook multiplication is faster because its inner loop has no extra additions and maps to one multiply-accumulate instruction per limb pair.

## Properties

- **Exact count.** The number of limb products is $mn$ for each input, so the time does not leak the values of the limbs, only the lengths. For cryptographic code this is a useful property, if each limb product itself takes constant time.
- **Not in place.** The output needs its own $m + n$ limbs; it cannot overwrite an input that is still being read.
- **Sequential access.** Row $i$ reads $b$ from left to right and writes a window of $c$. This makes the inner loop fast in cache and easy to vectorize.
- **Online in one operand.** Row $i$ uses only $a_i$, so the limbs of $A$ can arrive one at a time.

## Variants and improvements

- **Product scanning (by columns).** Compute $c_k = \sum_{i + j = k} a_i b_j$ for $k = 0, 1, \ldots$ in a three-limb accumulator, then emit the low limb and shift. This is the [lattice multiplication](/lattice-multiplication/) order. It writes each output limb once, which helps in hardware and in some cryptographic code.
- **Multiply and add rows.** GMP's base case calls one routine for the first row (multiply a limb array by one limb) and another for each later row (multiply by a limb and add into the result). Each is one tight loop.
- **Squaring** with half the products, as above.
- **Short products.** If only $AB \bmod \beta^n$ is needed, skip all $(i, j)$ with $i + j \ge n$: about $n^2 / 2$ products. This is used inside Newton iterations for division.
- **Hardware.** The [array multiplier](/array-multiplier/) is the same method as a circuit. The [Wallace tree](/wallace-tree-multiplier/) adds the same partial products in a tree of depth $O(\log n)$.
- **Faster methods.** [Karatsuba multiplication](/karatsuba-multiplication/) replaces four half-size products by three, and [Toom-Cook](/toom-cook-multiplication/) and the [Schönhage-Strassen algorithm](/schonhage-strassen-multiplication/) go further; each of them calls this method below its threshold.

## When to use it

Use schoolbook multiplication for small operands, up to the measured threshold of about ten to a few tens of limbs, for unbalanced products where one operand has only a few limbs, and as the base case of the recursive methods. For a few hundred limbs and more, use Karatsuba or Toom-Cook, and for tens of thousands of limbs an FFT method.

## Pitfalls

- **Overflow of the sum.** In line L5 the sum is up to $\beta^2 - 1$. In C with $w = 64$, `a[i] * b[j]` must be a 128-bit product, and the two additions must propagate their carries into the high limb; adding `c[i+j] + carry` in 64 bits first loses the carry when it overflows.
- **Adding instead of storing in line L8.** Writing `c[i + n] += carry` is correct but hides the fact that the position is fresh. Writing `c[i + n] = carry` into a buffer that was not cleared at line L1 is wrong: line L1 must zero all $m + n$ limbs, or row 0 must store instead of add.
- **The length of the result.** Allocating $\max(m, n) + 1$ or $m + n - 1$ limbs for the product loses the top limb. The product of $[15]$ and $[15]$ in radix 16 is $[1, 14]$, two limbs.
- **Normalization.** The top limb $c_{m+n-1}$ can be 0, for example for $1 \cdot 1$. Drop it before the result is used as a normalized number; a zero product must also get the sign $+$.
- **Aliasing.** If $c$ shares memory with $a$ or $b$, the writes of line L6 change limbs that later rows still read. Use a separate output buffer.

## Implementations

## History

Long multiplication with rows of partial products is the method of written arithmetic, and it is far older than computers; [lattice multiplication](/lattice-multiplication/) is an old layout of the same computation. Knuth gives it as Algorithm M in Section 4.3.1. In the 1950s Kolmogorov conjectured that each method for multiplying $n$-digit numbers needs on the order of $n^2$ digit operations. In 1960 Karatsuba found a faster method, published in 1962, as he recounts in his 1995 paper; see [Karatsuba multiplication](/karatsuba-multiplication/).

## References
