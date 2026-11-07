---
tag: W8G6XG
kind: technique
slug: error-free-transformations
name: Error-free transformations
aliases:
- EFT
- error-free transformation
area: numerical/floating-point
level: advanced
summary: Operations that return a floating-point result together with its exact rounding error.
prereqs: [floating-point-model, round-to-nearest-even, fused-multiply-add]
see_also: [two-sum, fast-two-sum, two-product, veltkamp-splitting, kahan-summation, dot2-compensated-dot-product, double-double-arithmetic, shewchuk-expansion-sum]
sources:
  - paper: doi:10.1137/030601818
    title: Takeshi Ogita, Siegfried M. Rump and Shin'ichi Oishi, Accurate sum and dot product, SIAM Journal on Scientific Computing 26(6) (2005), 1955-1988
    locator: the term error-free transformation, TwoSum, TwoProduct and Split as building blocks, and the compensated algorithms Sum2, SumK, Dot2 and DotK built from them
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.2, Exact Operations; Section 4.3, Accurate Computation of the Sum of Two Numbers (4.3.1 Fast2Sum, 4.3.2 2Sum, 4.3.3 if we do not use rounding to nearest); Section 4.4, Accurate Computation of the Product of Two Numbers (4.4.1 2MultFMA, 4.4.2 Veltkamp splitting and Dekker's product); Section 4.12, Evaluation of the error of an FMA; Sections 5.3 to 5.5 (compensated sums, dot products and polynomials)
  - paper: doi:10.1007/BF01397083
    title: Theodorus J. Dekker, A floating-point technique for extending the available precision, Numerische Mathematik 18(3) (1971), 224-242
    locator: Fast2Sum, the splitting of a float into two halves, the exact product, and double-length arithmetic built on them
  - paper: doi:10.1007/BF01975722
    title: Ole Moller, Quasi double-precision in floating point addition, BIT 5 (1965), 37-50
    locator: the branch-free algorithm for the exact error of an addition (TwoSum)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.2.2, Accuracy of Floating Point Arithmetic (the exact error of a rounded addition, computed by the six-operation formula)
---

An error-free transformation turns the result of one floating-point operation into a pair $(x, y)$ of floats such that $x$ is the rounded result and $x + y$ is the exact result. For addition the pair is computed by [TwoSum](/two-sum/) (six operations) or [Fast2Sum](/fast-two-sum/) (three operations, under a condition on the exponents); for multiplication by [TwoProduct](/two-product/) (two operations with an [FMA](/fused-multiply-add/), seventeen with [Veltkamp splitting](/veltkamp-splitting/)). Compensated algorithms apply these transformations at each step, collect the error terms and add them back, so they deliver results as accurate as if computed in twice the working precision, at a few times the cost and with ordinary hardware. The name is from Ogita, Rump and Oishi (2005); the transformations themselves go back to Møller (1965), Kahan (1965) and Dekker (1971).

## In plain words

When a computer adds or multiplies two numbers, the answer is rounded, and the part that was rounded away is lost. Surprisingly, that lost part is itself a number the computer can store exactly, and it can be computed with a few more ordinary operations.

So each addition or multiplication can be turned into two numbers: the usual rounded answer and the exact error. Their sum is the true answer, with nothing lost. Accurate algorithms use this at every step: they keep the errors, add them up on the side, and put them back at the end.

## When it applies

- The arithmetic rounds to nearest (the theorems below assume it; Muller et al., Section 4.3.3, treats other modes), as in IEEE 754 binary arithmetic with the default rounding, and each operation is rounded once to the working format: no extended-precision intermediates, no [double rounding](/double-rounding/).
- No overflow occurs. For addition, underflow does no harm, because an addition with a subnormal result is exact. For multiplication the inputs must satisfy $e_a + e_b \ge e_{\min} + p - 1$, so that the product does not underflow.
- The compiler keeps the operations as written: no reassociation, no value-changing optimizations, and no unwanted contraction into FMAs.
- The problem is ill conditioned enough that the working precision is not sufficient, but a doubled or $K$-fold precision is.

**Notation.** Binary64 with round to nearest, $p = 53$, $u = 2^{-53}$; see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**The basic transformations.** For floats $a$ and $b$:

| name | output | exact relation | cost | condition |
|---|---|---|---|---|
| [Fast2Sum](/fast-two-sum/) (Dekker) | $(s, t)$, $s = \mathrm{fl}(a + b)$ | $a + b = s + t$ | 3 flops | $e_a \ge e_b$ (for example $\lvert a\rvert \ge \lvert b\rvert$) |
| [TwoSum](/two-sum/) (Møller, Knuth) | $(s, t)$, $s = \mathrm{fl}(a + b)$ | $a + b = s + t$ | 6 flops | none |
| [TwoProduct](/two-product/) with FMA | $(\pi, \rho)$, $\pi = \mathrm{fl}(ab)$ | $ab = \pi + \rho$ | 2 flops | $e_a + e_b \ge e_{\min} + p - 1$ |
| TwoProduct, Dekker | $(\pi, \rho)$ | $ab = \pi + \rho$ | 17 flops | as above, and no overflow in the [splitting](/veltkamp-splitting/) |
| ErrFma (Boldo and Muller) | $(r_1, r_2, r_3)$, $r_1 = \mathrm{fma}(a, b, c)$ | $ab + c = r_1 + r_2 + r_3$ | fewer than 30 flops | no underflow |

In each case $|t| \le \tfrac12\mathrm{ulp}(s) \le u|s|$ and $|\rho| \le u|\pi|$, so the error term is small and the pair is *nonoverlapping*. The fact that the error of a rounded sum or product is a float at all is the key theorem: for addition with round to nearest it is always one; for multiplication, when there is no underflow (Muller et al., Sections 4.2 and 4.3).

## The template

```pseudo id=main
COMPENSATED(op, x_1, ..., x_n)
L1  r ← x_1;  c ← 0                         ▷ result and accumulated error
L2  for i ← 2 to n:
L3      (r, e) ← EFT(op, r, x_i)            ▷ hole: TwoSum, TwoProduct, or a pair of them
L4      c ← COMBINE(c, e, i)                 ▷ hole: propagate the old error and add the new one
L5  return fl(r + c)
```

The two holes are the problem-specific parts. Line L3 is the error-free step, and $r$ is exactly the value the plain algorithm would compute. Line L4 is an ordinary floating-point computation: for summation it is $c \leftarrow \mathrm{fl}(c + e)$; for a dot product it adds the errors of the product and of the sum; for [Horner's rule](/horner-rule/) it is $c \leftarrow \mathrm{fl}(c \cdot x + (e_\pi + e_\sigma))$, which propagates the old error through the next multiplication. Line L5 folds the correction in with one rounding.

**Why the result is accurate.** After the loop, the exact relation $\text{exact result} = r + c^{*}$ holds, where $c^{*}$ is the exact value of the error terms propagated without rounding. The only errors are those of line L4, an ordinary computation on terms of size $u$ times the data; its error is $O(nu)$ relative to the size of $c^{*}$, so $O(nu^2)$ relative to the data. The final bound has the shape

$$|\hat r - r_{\text{exact}}| \le u\,|r_{\text{exact}}| + \gamma_n^2 \cdot (\text{the absolute data sum}),$$

the bound of a computation in precision $u^2$ followed by one rounding. This is proved for Sum2, Dot2 and compensated Horner (Ogita, Rump and Oishi, 2005; Muller et al., Sections 5.3 to 5.5).

## Classic examples

- **[Kahan summation](/kahan-summation/)** (1965): line L3 is a Fast2Sum-like step on the corrected term, line L4 keeps one correction. It predates the name and is not exactly error-free when $|x_i| > |r|$; [Neumaier summation](/neumaier-summation/) uses a branch to choose the right Fast2Sum, and Sum2 uses TwoSum.
- **[Dot2](/dot2-compensated-dot-product/)**: TwoProduct on each $x_i y_i$, TwoSum into the running sum, and the two errors summed on the side; see the [accurate dot product](/accurate-dot-product/) problem.
- **Compensated Horner** (Graillat, Louvet and Langlois): TwoProduct and TwoSum at each step of Horner's rule, which evaluates polynomials near multiple roots with doubled-precision accuracy.
- **[Double-double arithmetic](/double-double-arithmetic/)**: a number is a nonoverlapping pair $(x_h, x_l)$, and each operation on pairs is a short sequence of TwoSum, Fast2Sum and TwoProduct steps followed by renormalization.
- **[Expansions](/shewchuk-expansion-sum/)** (Priest, Shewchuk): a number is a sum of any number of nonoverlapping floats, maintained by TwoSum; this gives exact sums and the adaptive geometric predicates.
- **Correctly rounded functions**: the second, accurate step of a library function such as those of CRlibm evaluates in double-double with these building blocks (Muller et al., Section 10.6).

## Variations

- **Vector transformations.** A cascade of TwoSum maps a vector $(x_1, \ldots, x_n)$ to $(t_1, \ldots, t_{n-1}, s)$ with the same exact sum, $s$ the recursive sum; repeating it $K - 1$ times gives SumK, with the accuracy of precision $u^{K}$.
- **Faithful and correctly rounded results.** AccSum (Rump, Ogita and Oishi) repeats the extraction until the result is provably faithful, with a number of passes that depends on the condition number.
- **Residuals of division and square root.** With an FMA, $a - qb$ and $a - s^2$ are exact floats for $q = \mathrm{fl}(a/b)$ and $s = \mathrm{fl}(\sqrt{a})$; they are error-free in the sense that $a/b = q + r/b$ exactly.
- **Other rounding modes.** With directed rounding the error of an addition can fail to be computable by TwoSum; Muller et al., Section 4.3.3, gives what remains true.
- **Augmented operations.** IEEE 754-2019, Clause 9.5, recommends augmentedAddition and augmentedMultiplication, which return the pair in one operation, with roundTiesToZero for the high part so that the result is reproducible.

## Pitfalls

- **Fast2Sum in the wrong order.** Fast2Sum$(2^{-60}, 1)$ returns $(1, 0)$, losing the error $2^{-60}$; TwoSum$(2^{-60}, 1)$ returns $(1, 2^{-60})$. Fast2Sum needs $e_a \ge e_b$, which a comparison of magnitudes guarantees.
- **Optimizing compilers.** Under `-ffast-math` or a similar mode, a compiler can simplify $(s - a) - b$ to $0$ and remove the transformation. Compile these routines with strict IEEE semantics.
- **Extended precision.** On the x87 unit, intermediates in 64-bit precision make $s$ differ from $\mathrm{fl}(a + b)$ in binary64, and the computed $t$ is then not the error.
- **Overflow.** TwoSum$(\Omega, 2^{970})$, with $\Omega$ the largest float, returns $(\infty, \mathrm{NaN})$; Veltkamp splitting overflows for $|a|$ above about $2^{996}$ in binary64.
- **Underflow in products.** For $a = b = 2^{-520}(1 + 2^{-52})$ the error of $\mathrm{fl}(ab)$ is below the smallest subnormal and TwoProduct returns $\rho = 0$, so the relation $ab = \pi + \rho$ fails.

## Exercises

1. Check by hand that TwoSum$(0.1, 0.2)$ in binary64 returns $s = 0.30000000000000004$ and $t = -2.7755575615628914 \times 10^{-17} = -2^{-55}$, and that $\mathrm{fl}(0.1) + \mathrm{fl}(0.2) = s + t$ exactly.
2. Prove that the error $a + b - \mathrm{fl}(a + b)$ of a rounded-to-nearest addition is a float (Muller et al., Section 4.2.1).
3. Show that if $(r, e)$ is computed by TwoSum and then $c \leftarrow \mathrm{fl}(c + e)$, the final $\mathrm{fl}(r + c)$ of the template for summation has error at most $u|s| + \gamma_{n-1}^2 \sum|x_i|$.
4. Write the compensated Horner scheme from the template, and test it on $(x - 1)^{5}$ in expanded form at $x = 1 + 2^{-20}$ against exact rational arithmetic.

## References
