---
tag: 4T16NS
kind: definition
slug: subnormal-numbers
name: Subnormal numbers
aliases:
- denormal numbers
- gradual underflow
- denormalized numbers
area: numerical/floating-point
level: core
summary: The floats below the smallest normal magnitude, with a leading digit 0 and the minimum exponent. They fill the gap near zero with even spacing, at the cost of fewer significant digits.
prereqs: [ieee-754, ulp]
see_also: [special-floating-point-values, floating-point-exceptions, sterbenz-lemma, ulp, machine-epsilon, floating-point-model, rounding-error-analysis, ieee-754]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 2.1 (definition of subnormal number), Clause 3.3 and 3.4 (subnormal values and their encoding with biased exponent 0), Clause 7.5 (underflow, tininess before or after rounding, default handling)
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 2.2, Special Quantities, the part on denormalized numbers (gradual underflow and the property that x ≠ y implies x ⊖ y ≠ 0)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.1 (subnormal numbers in the number system), Section 2.2 (the model with an absolute error term for underflow) and Section 2.3 (gradual underflow in IEEE arithmetic)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 2 (normal and subnormal numbers, and underflow) and Section 4.2 (exact operations, including additions whose result is subnormal)
  - paper: "James Demmel, Underflow and the reliability of numerical software, SIAM Journal on Scientific and Statistical Computing 5(4) (1984), 887-919"
    title: James Demmel, Underflow and the reliability of numerical software
    locator: the comparison of gradual underflow with flush to zero, and the error model with an absolute term
---

A subnormal number (formerly *denormal*) is a nonzero [floating-point](/floating-point-arithmetic/) number whose magnitude is below the smallest normal number $\beta^{e_{\min}}$: its significand has a leading digit 0, and its exponent is the minimum $e_{\min}$. The subnormals fill the interval between zero and $\beta^{e_{\min}}$ with the same spacing as the binade just above, which is called *gradual underflow*. They give up significant digits as they get smaller, so the relative error bound $u$ fails for them, but they keep useful properties such as "$x \neq y$ implies $x - y \neq 0$", which a format that flushes small results to zero does not have.

## Definition

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64 ($\beta = 2$, $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$). The unit roundoff is $u = \tfrac12\beta^{1-p}$ ($2^{-53}$). $\mathrm{fl}(\cdot)$ is the rounded result, and $\mathrm{ulp}$ is as in Muller et al., Section 2.3.2.

**Definition.** A *subnormal number* of $\mathbb{F}$ is a number

$$x = \pm\, 0.d_1 d_2 \ldots d_{p-1} \times \beta^{e_{\min}} = \pm\, M \beta^{e_{\min} - p + 1}, \qquad 1 \le M \le \beta^{p-1} - 1,$$

with integer $M$. So $0 < |x| < \beta^{e_{\min}}$. The *normal* numbers have $\beta^{e_{\min}} \le |x| \le \Omega$, where $\Omega$ is the largest float. Zero is neither normal nor subnormal.

In binary64 the subnormals are $k \cdot 2^{-1074}$ for $1 \le k \le 2^{52} - 1$, from $2^{-1074} \approx 4.94 \times 10^{-324}$ to $2^{-1022} - 2^{-1074}$. Their encoding has biased exponent field $E = 0$ and trailing significand $T = k$ (Clause 3.4); the stored exponent 0 stands for $e_{\min}$, not for $e_{\min} - 1$.

**Gradual underflow.** The numbers $M\beta^{e_{\min} - p + 1}$ for $0 \le M < \beta^{p}$ are the subnormals, zero and the normal numbers of the lowest binade, all spaced $\beta^{e_{\min} - p + 1}$ apart. So the gap between zero and the smallest normal number is filled with the spacing of the lowest binade, and $\mathrm{ulp}(x) = \beta^{e_{\min}-p+1}$ for each $|x| < \beta^{e_{\min} + 1}$. Without subnormals, the gap between 0 and $\beta^{e_{\min}}$ would be $\beta^{p-1}$ times the gap just above $\beta^{e_{\min}}$.

**Precision.** A subnormal $M\beta^{e_{\min}-p+1}$ has only as many significant digits as $M$ has: in binary64, $\lfloor \log_2 k \rfloor + 1$ bits for $x = k \cdot 2^{-1074}$. Its relative spacing is $1/k$, much larger than $2u$ for small $k$.

**Underflow (Clause 7.5).** A nonzero result is *tiny* when its magnitude is below $\beta^{e_{\min}}$. The standard lets a binary implementation detect tininess before rounding (the exact result is below $\beta^{e_{\min}}$) or after rounding (the result rounded with an unbounded exponent range is below $\beta^{e_{\min}}$). In the default handling, the underflow flag is raised only when the result is both tiny and inexact; the result is the correctly rounded value, which may be subnormal or zero.

### Properties (proved, round to nearest)

1. **Error model.** For each real $x$ with $|x| \le \Omega$, $\mathrm{fl}(x) = x(1 + \delta) + \eta$ with $|\delta| \le u$, $|\eta| \le \tfrac12\beta^{e_{\min}-p+1}$ and $\delta\eta = 0$. *Proof.* If $|x| \ge \beta^{e_{\min}}$, the relative bound holds with $\eta = 0$ (see [machine epsilon](/machine-epsilon/)). Otherwise $x$ lies in the grid of spacing $\beta^{e_{\min}-p+1}$, so $|\mathrm{fl}(x) - x|$ is at most half of it; take $\delta = 0$. This is the model of Higham, Section 2.2, for underflow.
2. **Exact subnormal sums.** If $x, y \in \mathbb{F}$ and $|x + y| < \beta^{e_{\min}}$ (in particular if $\mathrm{fl}(x + y)$ is subnormal), then $\mathrm{fl}(x + y) = x + y$. *Proof.* Every float is an integer multiple of $\beta^{e_{\min}-p+1}$, so $x + y = N\beta^{e_{\min}-p+1}$ with an integer $N$, and $|x + y| < \beta^{e_{\min}}$ gives $|N| < \beta^{p-1}$. So $x + y$ is zero or subnormal, hence in $\mathbb{F}$. So $\eta = 0$ for addition and subtraction in property 1.
3. **No false zero.** If $x, y \in \mathbb{F}$ and $x \neq y$, then $\mathrm{fl}(x - y) \neq 0$. *Proof.* If $|x - y| < \beta^{e_{\min}}$, then $x - y$ is computed exactly by property 2, and it is not zero. Otherwise $|x - y| \ge \beta^{e_{\min}}$, a float, and rounding is monotone, so $|\mathrm{fl}(x - y)| \ge \beta^{e_{\min}}$. So the test `if x != y: z = 1 / (x - y)` never divides by zero.
4. **The [Sterbenz lemma](/sterbenz-lemma/)** holds in the whole range only with subnormals.

### Flush to zero

Many processors have modes that replace subnormal results by zero (FTZ, flush to zero) and treat subnormal inputs as zero (DAZ, denormals are zero). These modes do not conform to [IEEE 754](/ieee-754/), and properties 2 to 4 fail in them. They exist for speed: on many processors an operation with a subnormal input or output takes a slow path, often tens to hundreds of cycles instead of a few. The size of the slowdown depends on the processor and is a measured fact, not a property of the format; some recent designs handle subnormals at full speed.

## Examples and non-examples

**The extremes in Python (binary64).**

| value | `float.hex` | note |
|---|---|---|
| `5e-324` | `0x0.0000000000001p-1022` | $2^{-1074}$, the smallest subnormal, 1 significant bit |
| `2.225073858507201e-308` | `0x0.fffffffffffffp-1022` | $2^{-1022} - 2^{-1074}$, the largest subnormal, 52 bits |
| `2.2250738585072014e-308` | `0x1.0000000000000p-1022` | $2^{-1022}$, the smallest normal, 53 bits |

`math.ulp(5e-324)`, `math.ulp(0.0)` and `math.ulp(2.0**-1022)` are all `5e-324`, and `math.nextafter(2.0**-1022, 1) - 2.0**-1022 == 5e-324`.

**Rounding in the subnormal range.** With $t = 2^{-1074}$: `t / 2` gives `0.0` (a tie between 0 and $t$, rounded to the even 0), `t * 0.75 == t`, `t * 1.5 == 2*t` (a tie, rounded to the even $2t$), and `t * 2.5 == 2*t`. The product $2^{-1022}(1 - 2^{-53})$ is a tie between the largest subnormal and $2^{-1022}$, and it rounds to $2^{-1022}$, the one with the even significand.

**Lost precision.** `1e-310` is the subnormal $20240225330731 \cdot 2^{-1074}$, with 45 significant bits instead of 53. The quotient `1e-310 / 3` is the subnormal nearest to the exact value, and its relative error is $4.94 \times 10^{-14}$, about 445 times $u$: the result has only 43 significant bits. Property 1 still holds, with $|\eta| \le 2^{-1075}$.

**No false zero.** For `x = 1e-300` and `y = 1e-300 * (1 + 2**-52)`, the difference `y - x` is `1.6578092e-316`, a subnormal, and it is the exact difference. With flush to zero it would be `0.0` although `x != y`.

**Non-examples.**

- `0.0` is not subnormal. Its encoding also has $E = 0$, but $T = 0$.
- $2^{-1022}$ is normal, although `math.ulp` returns the same value for it as for the subnormals.
- The x87 80-bit format has an explicit leading bit, and a value with leading bit 0 and a nonzero exponent field is an *unnormal*, not a subnormal. Modern processors treat such words as invalid.
- A bound "relative error at most $u$" for a product is not true when the product is subnormal: `1e-310 / 3` above has a relative error of $445u$.

## Related definitions

- [IEEE 754](/ieee-754/): the standard that requires gradual underflow.
- [Infinities, NaN and signed zero](/special-floating-point-values/): the other values at the ends of the range; a result that underflows past the subnormals is a signed zero.
- [Floating-point exceptions](/floating-point-exceptions/): the underflow exception and its flag.
- [Unit in the last place](/ulp/): constant in the subnormal range.
- [Standard model of floating-point arithmetic](/floating-point-model/) and [rounding error analysis](/rounding-error-analysis/): the model with the absolute term $\eta$ for underflow.
- [Sterbenz lemma](/sterbenz-lemma/): needs the subnormals near zero.

## References
