---
tag: 71QAG0
kind: technique
slug: gauss-complex-multiplication
name: Gauss's complex multiplication trick
aliases:
- Complex number multiplication with three real multiplications
- 3M method
area: algebra/integer-arithmetic
level: core
summary: A trick that multiplies two complex numbers using three real multiplications instead of four, the idea behind Karatsuba multiplication.
prereqs: [integer-multiplication, asymptotic-notation]
see_also: [karatsuba-multiplication, toom-cook-multiplication, strassen-algorithm, fast-fourier-transform, polynomial-multiplication, tensor-rank, master-theorem]
sources:
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms, McGraw-Hill, 2008
    locator: Chapter 2, Divide-and-conquer algorithms, Section 2.1, Multiplication (Gauss's trick and its use in the divide-and-conquer integer product)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.3, How fast can we multiply? (the identity behind the three-product scheme)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 4, Divide-and-conquer, Section 4.2, Strassen's algorithm for matrix multiplication (the exercise on multiplying complex numbers with three real multiplications)
  - paper: doi:10.1137/0613043
    title: Nicholas J. Higham, Stability of a method for multiplying complex matrices with three real matrix multiplications, SIAM Journal on Matrix Analysis and Applications 13(3), 1992
    locator: pp. 681 to 687 (the 3M method for complex matrices and its error bounds)
---

Gauss's complex multiplication trick computes the product $(a + bi)(c + di) = (ac - bd) + (ad + bc)i$ with three real multiplications instead of four, at the price of extra additions. The trick is the identity

$$ad + bc = (a + b)(c + d) - ac - bd,$$

which gets the cross term from one product of sums and the two products $ac$ and $bd$ that are needed anyway. Saving one product out of four does not matter much for one complex product of machine numbers, but it matters a great deal when the "numbers" are themselves large: applied recursively to the two halves of a long integer it is [Karatsuba multiplication](/karatsuba-multiplication/), and applied to matrices it is the 3M method for complex matrix products. The same pattern, more products of sums and fewer products overall, is the core of [Toom-Cook](/toom-cook-multiplication/) and [Strassen's algorithm](/strassen-algorithm/).

## In plain words

To multiply two complex numbers you need four products of their parts: real times real, imaginary times imaginary, and the two mixed ones. But you only need two answers, the real part and the imaginary part, and the imaginary part is just the sum of the two mixed products.

There is a shortcut for that sum. Add the two parts of the first number, add the two parts of the second number, and multiply the two sums. That big product contains the two mixed products you want, plus the two plain products, which you have already computed. Subtract them, and the sum of the mixed products is left. Three multiplications instead of four.

The trick pays when multiplying is far more costly than adding, as it is for very long numbers.

## When it applies

The signals are:

- **Two pairs and a symmetric cross term.** A computation needs $ac$, $bd$ and the sum $ad + bc$, but not $ad$ and $bc$ separately. Products of complex numbers, of linear polynomials $(a + bx)(c + dx)$, and of two-part numbers $(a\beta^k + b)(c\beta^k + d)$ all have this form.
- **Products cost much more than sums.** The operands are long integers, polynomials, or matrices, so a product costs $M(n) \gg n$ and an addition costs $\Theta(n)$. For one multiplication of hardware floating-point numbers, the trick rarely helps.
- **The structure repeats.** If the parts are themselves split in the same way, the saving compounds, from a factor $3/4$ to an exponent: $n^{\log_2 3}$ instead of $n^2$.
- **Commutativity is not needed.** The identity $(a + b)(c + d) - ac - bd = ad + bc$ holds in each ring, so it works for matrices, where Strassen-type savings need more care.

## The template

```pseudo id=main
THREE-PRODUCTS(a, b, c, d, MULT)            ▷ returns ac, bd and ad + bc
L1  p ← MULT(a, c)                           ▷ the hole MULT: the costly product
L2  q ← MULT(b, d)
L3  s ← MULT(a + b, c + d)                   ▷ equals ac + ad + bc + bd
L4  return (p, q, s − p − q)

COMPLEX-MULT(a + bi, c + di, MULT)
L5  (p, q, m) ← THREE-PRODUCTS(a, b, c, d, MULT)
L6  return (p − q) + m · i                   ▷ the hole COMBINE: how the three results are used
```

The two holes are MULT, the product of the parts, which can be a machine product, a recursive call, or a matrix product, and COMBINE, which assembles the answer. For complex numbers COMBINE is $(p - q) + mi$. For a number split at $\beta^k$, it is $p\beta^{2k} + m\beta^k + q$; for a linear polynomial, $p + mx + qx^2$.

Counting operations, COMPLEX-MULT does 3 products and 5 additions or subtractions (two in L3, two in L4, one in L6), against 4 products and 2 additions for the direct formula. A second form, $k_1 = c(a + b)$, $k_2 = a(d - c)$, $k_3 = b(c + d)$, with real part $k_1 - k_3$ and imaginary part $k_1 + k_2$, also uses 3 products and 5 additions, but if $c + di$ is fixed, the values $c$, $d - c$ and $c + d$ can be computed once, and each product then costs 3 products and 3 additions.

**Example.** $(3 + 4i)(5 + 6i)$: $p = 15$, $q = 24$, $s = 7 \cdot 11 = 77$, so $m = 77 - 15 - 24 = 38$ and the product is $(15 - 24) + 38i = -9 + 38i$. The direct formula gives $15 - 24 = -9$ and $18 + 20 = 38$.

**Why three is the minimum.** Call an algorithm *bilinear* if each product it makes is a linear form in $(a, b)$ times a linear form in $(c, d)$, and the outputs are linear combinations of the products. Over the reals, no bilinear algorithm computes $ac - bd$ and $ad + bc$ with two products. *Proof.* The two outputs are the bilinear forms $(a, b) A (c, d)^T$ and $(a, b) B (c, d)^T$ with

$$A = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \qquad B = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} .$$

A product of a linear form $u \cdot (a, b)$ and a linear form $v \cdot (c, d)$ is the bilinear form of the rank-one matrix $u v^T$. If two products suffice, then $A$ and $B$ lie in the span of two rank-one matrices $u_1 v_1^T$ and $u_2 v_2^T$. Since $A$ and $B$ are linearly independent, that span equals the span of $A$ and $B$, so it contains the nonzero matrix $u_1 v_1^T$ of rank at most one. But for each $(x, y) \ne (0, 0)$, $\det(xA + yB) = -x^2 - y^2 \ne 0$, so each nonzero matrix of the span of $A$ and $B$ has rank 2. This is a contradiction. $\blacksquare$ In the language of [tensor rank](/tensor-rank/), complex multiplication has rank 3 over $\mathbb{R}$. Over $\mathbb{C}$ it has rank 2, since it splits into the two products $(a + bi)(c + di)$ and $(a - bi)(c - di)$; the proof uses that $x^2 + y^2 \ne 0$ for real $(x, y) \ne 0$.

## Classic examples

- **[Karatsuba multiplication](/karatsuba-multiplication/).** Split $x = x_1\beta^k + x_0$ and $y = y_1\beta^k + y_0$, and get $x_1 y_1$, $x_0 y_0$ and $x_1 y_0 + x_0 y_1$ from three half-size products, recursively. The recurrence $T(n) = 3T(n/2) + O(n)$ gives $O(n^{\log_2 3}) = O(n^{1.585})$ by the [master theorem](/master-theorem/).
- **[Polynomial multiplication](/polynomial-multiplication/).** The same split by the degree, $f = f_1 x^k + f_0$, gives Karatsuba for polynomials, with the same exponent.
- **Complex products in the [fast Fourier transform](/fast-fourier-transform/).** Each butterfly multiplies by a fixed twiddle factor $\omega = c + di$, so the second form with precomputed $c$, $d - c$ and $c + d$ uses 3 real products and 3 additions. Whether it is faster than 4 products depends on the machine; with fused multiply-add units the direct form usually wins.
- **The 3M method for complex matrices.** $(A + iB)(C + iD)$ with three real matrix products $AC$, $BD$ and $(A + B)(C + D)$ saves a quarter of the work of a large complex matrix product, at some cost in accuracy (Higham, 1992).
- **[Toom-Cook](/toom-cook-multiplication/) and [Strassen](/strassen-algorithm/).** Toom-3 gets 5 products of thirds instead of 9 by evaluating at more points, and Strassen gets 7 products of $2 \times 2$ blocks instead of 8. Both generalize the same exchange of products for additions.

## Variations

- **The Karatsuba form and the subtractive form.** The cross term can be computed as $(a + b)(c + d) - ac - bd$ or as $ac + bd - (a - b)(c - d)$. The second form keeps the operands from growing: $|a - b|$ fits in the same number of digits as $a$ and $b$, while $a + b$ may need one more, at the cost of handling signs.
- **Squaring.** $(a + bi)^2 = (a + b)(a - b) + 2ab\, i$ uses two real products instead of three.
- **Precomputed operand.** If one factor is fixed, as in the FFT, the form with $k_1, k_2, k_3$ moves two of the additions into the precomputation.
- **More parts.** Splitting into $r$ parts and evaluating at $2r - 1$ points gives $2r - 1$ products instead of $r^2$, which is Toom-Cook; the trick here is the case $r = 2$, with the evaluation points $0$, $1$ and $\infty$.

## Pitfalls

- **Using it where products are cheap.** For one product of two `double` complex numbers, three multiplications and five additions are no faster than four multiplications and two additions on current processors, and are often slower. The trick is for costly products.
- **Loss of accuracy in floating point.** The imaginary part $s - p - q$ is a difference of large numbers when $ad + bc$ is small compared with $ac$ and $bd$, so its rounding error is bounded by a multiple of $|a||c| + |b||d| + |a + b||c + d|$, not of $|ad + bc|$. For integers and exact arithmetic there is no such issue.
- **Operand growth.** $a + b$ and $c + d$ can have one more digit than the parts, so a recursive integer version must handle half-size products of $k + 1$ limbs, not $k$. Forgetting the extra carry gives wrong results only for inputs whose top limbs are large, such as all limbs equal to $\beta - 1$.
- **Assuming it is optimal in every sense.** Three is the minimum number of products for bilinear algorithms over the reals, as proved above, but the trick does not minimize additions, and over the complex numbers two products of a different kind suffice.

## Exercises

1. Check that $k_1 = c(a + b)$, $k_2 = a(d - c)$ and $k_3 = b(c + d)$ give $ac - bd = k_1 - k_3$ and $ad + bc = k_1 + k_2$. How many additions are left per product when $c + di$ is fixed?
2. Show that the product of two linear polynomials, that is, the three coefficients $ac$, $ad + bc$ and $bd$ of $(a + bx)(c + dx)$, also needs three products in every bilinear algorithm. (Hint: write the matrices of the three outputs as bilinear forms and show that they are linearly independent.) Then show that three products suffice, which is Karatsuba's step.
3. Apply THREE-PRODUCTS recursively to multiply two $n$-digit integers, with $n$ a power of 2. Write the recurrence for the number of one-digit products, solve it exactly, and compare it with $n^2$ for $n = 1024$. (Answer: $3^{\log_2 n} = n^{\log_2 3}$, which is $59049$ against $1048576$.)
4. Multiply two complex matrices of size $n \times n$ by the 3M method and by the direct method with schoolbook matrix products. Count the real multiplications and the real additions of each method as functions of $n$.

## References
