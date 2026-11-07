---
tag: 1316R5
kind: concept
slug: fused-multiply-add
name: Fused multiply-add
aliases:
- FMA
- fusedMultiplyAdd
area: numerical/floating-point
level: core
summary: Computes a·b + c with a single rounding, enabling exact error-free products.
prereqs: [floating-point-arithmetic, floating-point-model]
see_also: [two-product, error-free-transformations, double-rounding, horner-rule, newton-raphson-division, accurate-dot-product, floating-point-product-error, ieee-754]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.4.1, Arithmetic operations (fusedMultiplyAdd); Clause 7.2 (the invalid operation case of fusedMultiplyAdd with zero times infinity); Clause 10.4 (literal meaning and value-changing optimizations, contraction)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.4, Fused multiply-add (FMA) instructions; Section 3.4.2, Fused multiply-add; Section 4.4.1, 2MultFMA; Section 4.5, Computation of residuals of division and square root with an FMA; Sections 4.7 and 4.8, Newton-Raphson division and square root with an FMA; Section 7.5, The fused multiply-add instruction
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.6, Fused Multiply-Add Operation (the error model and the effect on inner products and Horner's rule)
  - paper: "Robert K. Montoye, Erdem Hokenek and Sharon L. Runyon, Design of the IBM RISC System/6000 floating-point execution unit, IBM Journal of Research and Development 34(1) (1990), 59-70"
    title: Montoye, Hokenek and Runyon, Design of the IBM RISC System/6000 floating-point execution unit (1990)
    locator: the first commercial fused multiply-add unit
  - paper: "Sylvie Boldo and Guillaume Melquiond, Emulation of FMA and correctly rounded sums: proved algorithms using rounding to odd, IEEE Transactions on Computers 57(4) (2008), 462-471"
    title: Sylvie Boldo and Guillaume Melquiond, Emulation of FMA and correctly rounded sums, proved algorithms using rounding to odd (2008)
    locator: the emulation of a binary64 FMA from operations with rounding to odd
---

The fused multiply-add $\mathrm{fma}(a, b, c)$ computes $ab + c$ exactly and rounds once, where a separate multiplication and addition would round twice. [IEEE 754](/ieee-754/)-2008 made it a required operation, and most processors since about 2010 provide it, often as fast as a single multiplication. Its main gift is exactness: $\mathrm{fma}(a, b, -\mathrm{fl}(ab))$ is exactly the rounding error of the product, which gives the two-instruction [TwoProduct](/two-product/) and, with it, compensated dot products and polynomial evaluation. It also gives exact residuals for division and square root, the basis of fast correctly rounded [Newton-Raphson division](/newton-raphson-division/). Its one danger is that a compiler that uses it silently can break code written for separate roundings.

## In plain words

Many calculations multiply two numbers and add a third. A computer usually rounds the product, then rounds the sum, and each rounding loses a little. A fused multiply-add does the whole thing in one step and rounds only once, at the end.

That saves time, since one instruction does the work of two, and it makes the answer a little more accurate. More surprisingly, it lets a program find exactly how much a multiplication lost to rounding: multiply, then use the fused operation to subtract the rounded product from the exact one. Many accurate algorithms are built on that trick.

## The idea

**Notation.** Binary64 with round to nearest, $p = 53$, $e_{\min} = -1022$, $u = 2^{-53}$, and the [standard model](/floating-point-model/); see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**Definition.** For floats $a, b, c$, $\mathrm{fma}(a, b, c) = \mathrm{fl}(ab + c)$, the correctly rounded value of the exact $ab + c$ in the current rounding mode (IEEE 754-2019, Clause 5.4.1). The exceptions are those of the exact result, except that $\mathrm{fma}(0, \infty, c)$ and $\mathrm{fma}(\infty, 0, c)$ signal invalid operation; when $c$ is a quiet NaN, whether they signal it is implementation-defined (Clause 7.2). In the standard model,

$$\mathrm{fma}(a, b, c) = (ab + c)(1 + \delta), \qquad |\delta| \le u,$$

when there is no underflow or overflow, against $\mathrm{fl}(\mathrm{fl}(ab) + c) = (ab(1 + \delta_1) + c)(1 + \delta_2)$ for the unfused pair.

**Theorem (the error of a product, exactly).** Let $a, b$ be floats, $\pi = \mathrm{fl}(ab)$ with round to nearest, and $\rho = \mathrm{fma}(a, b, -\pi)$. If $e_a + e_b \ge e_{\min} + p - 1$, where $e_a$ and $e_b$ are the exponents of $a$ and $b$ (with no overflow), then $ab = \pi + \rho$ exactly.

*Proof.* Write $a = M_a 2^{e_a - p + 1}$ and $b = M_b 2^{e_b - p + 1}$ with integers $|M_a|, |M_b| < 2^{p}$. Then $ab$ is an integer multiple of $2^{e_a + e_b - 2p + 2}$, and so is $\pi$: the condition on the exponents makes $|ab| \ge 2^{e_a + e_b} \ge 2^{e_{\min} + p - 1}$, so $\pi$ is a normal float of exponent at least $e_a + e_b$, hence a multiple of $2^{e_a + e_b - p + 1}$. So $ab - \pi$ is a multiple of $2^{e_a + e_b - 2p + 2}$. With round to nearest, $|ab - \pi| \le \tfrac12\mathrm{ulp}(ab) \le 2^{e_a + e_b - p + 1}$, since $|ab| < 2^{e_a + e_b + 2}$. An integer multiple of $2^{e_a + e_b - 2p + 2}$ with magnitude at most $2^{e_a + e_b - p + 1}$ has the form $k \cdot 2^{e_a + e_b - 2p + 2}$ with $|k| \le 2^{p - 1}$, which is a float: $|k| < 2^{p}$, and the exponent $e_a + e_b - 2p + 2 \ge e_{\min} - p + 1$ is at least that of the smallest subnormal, so even a subnormal value of this form is representable. Since $ab - \pi$ is a float, the correctly rounded $\mathrm{fma}(a, b, -\pi)$ returns it exactly. $\blacksquare$

This is 2MultFMA (Muller et al., Section 4.4.1); without an FMA the same pair costs 17 operations with [Veltkamp splitting](/veltkamp-splitting/) and Dekker's product.

**Exact residuals.** If $q = \mathrm{fl}(a/b)$ with round to nearest and no underflow, then $r = \mathrm{fma}(-q, b, a) = a - qb$ exactly; similarly $\mathrm{fma}(-s, s, a) = a - s^2$ exactly for $s = \mathrm{fl}(\sqrt{a})$ (Muller et al., Section 4.5). A Newton-Raphson iteration that uses these residuals can then decide the correct rounding of the quotient or the square root.

**Error bounds with FMA.** In an inner product or [Horner's rule](/horner-rule/) written with FMAs, each step $s \leftarrow \mathrm{fma}(x_i, y_i, s)$ has one rounding, so the bound $\gamma_{2n}$ for Horner's rule becomes $\gamma_n$, and $\gamma_n$ for an inner product is unchanged in form but has one rounding per term instead of two (Higham, Section 2.6).

## Examples

Each line was run in Python 3.14, whose `math.fma` (added in Python 3.13) is a correctly rounded FMA, and checked with `fractions.Fraction`.

**The rounding error of a product.** For $a = 1 + 2^{-30}$ and $b = 1 - 2^{-30}$, the exact product is $1 - 2^{-60}$, and $\mathrm{fl}(ab) = 1$. The unfused $\mathrm{fl}(\mathrm{fl}(ab) - 1)$ is $0$. `math.fma(a, b, -1.0)` returns $-2^{-60} \approx -8.67 \times 10^{-19}$, exactly $ab - 1$. For $10000$ random pairs in $[-1000, 1000]$, $\pi + \rho = ab$ held exactly every time, as the theorem requires.

**A division residual.** $q = \mathrm{fl}(1/3)$ = 0x1.5555555555555p-2, and `math.fma(-q, 3.0, 1.0)` returns $2^{-54} \approx 5.55 \times 10^{-17}$, which is exactly $1 - 3q$.

**The underflow condition matters.** For $a = b = 2^{-520}(1 + 2^{-52})$, $e_a + e_b = -1040 < e_{\min} + p - 1 = -970$. The exact product is $2^{-1040}(1 + 2^{-51} + 2^{-104})$, $\pi = 2^{-1040}$ (a subnormal), and the true error $2^{-1091} + 2^{-1144}$ is below half the smallest subnormal, so $\rho = 0$ and $\pi + \rho \ne ab$.

**Contraction can break symmetric code.** For $x$ = 0x1.e36051fe94baap+0 $= 1.8881884810004785$, the expression `x*x - x*x` is $0$ when both products are rounded. If a compiler contracts it to `fma(x, x, -(x*x))`, the result is $-6.93 \times 10^{-17}$, the rounding error of $x^2$, and a following `sqrt` returns NaN. This is Kahan's warning about $\sqrt{a^2 - b^2}$ with $a = b$: with contraction the expression is no longer symmetric in its two products.

## Where it is used

- **[Error-free transformations](/error-free-transformations/).** TwoProduct by FMA is the base of [accurate dot products](/accurate-dot-product/), compensated Horner evaluation and [double-double arithmetic](/double-double-arithmetic/); the [exact product error](/floating-point-product-error/) page treats it as a problem.
- **Division and square root in software.** IA-64 and NVIDIA GPUs have no hardware divider for binary64 and compute quotients and square roots with Newton-Raphson iterations and FMA residuals (Muller et al., Sections 4.7 and 4.8); see also [Goldschmidt division](/goldschmidt-division/).
- **Polynomial evaluation and elementary functions.** Horner's rule with FMAs halves the number of roundings and of instructions; libraries of elementary functions rely on it.
- **Linear algebra and machine learning.** Matrix multiplication units (GPU tensor cores, CPU vector units) are arrays of FMAs; peak floating-point rates are usually counted as two operations per FMA.
- **Emulation.** Without hardware FMA, a correct binary64 FMA cannot be emulated as `(double)((long double)a*b + c)` because of [double rounding](/double-rounding/); a correct emulation uses rounding to odd (Boldo and Melquiond, 2008) or an error-free product and sum.
- **Compiler settings.** C allows contraction of `a*b + c` into an FMA under `#pragma STDC FP_CONTRACT`, and compilers differ in their default (`-ffp-contract`); IEEE 754-2019 Clause 10.4 lists contraction among the value-changing optimizations that a language should let the programmer control. Code that relies on separate roundings, such as the classical TwoSum or the test above, should disable it.

## References
