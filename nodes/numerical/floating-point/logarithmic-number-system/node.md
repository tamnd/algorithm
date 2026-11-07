---
tag: M6XEZA
kind: model
slug: logarithmic-number-system
name: Logarithmic number system
aliases:
- LNS
- sign/logarithm number system
- log-domain arithmetic
area: numerical/floating-point
level: research
summary: Represents a positive number by its logarithm, turning multiplication into addition.
prereqs: [floating-point-model, relative-error]
see_also: [floating-point-arithmetic, log-sum-exp-trick, floating-point-product-error, posit-format, block-floating-point, table-maker-dilemma, correctly-rounded-elementary-functions, real-ram]
sources:
  - paper: "N. G. Kingsbury and P. J. W. Rayner, Digital filtering using logarithmic arithmetic, Electronics Letters 7(2) (1971), 56-58"
    title: N. G. Kingsbury and P. J. W. Rayner, Digital filtering using logarithmic arithmetic
    locator: the proposal to hold filter samples as logarithms and the addition rule through a lookup of log2(1 + 2^z)
  - paper: "Earl E. Swartzlander Jr. and Aristides G. Alexopoulos, The sign/logarithm number system, IEEE Transactions on Computers C-24(12) (1975), 1238-1242"
    title: Earl E. Swartzlander Jr. and Aristides G. Alexopoulos, The sign/logarithm number system
    locator: the sign bit plus fixed-point logarithm format, the four operations, and the comparison of accuracy with floating point
  - paper: "Mark G. Arnold, Thomas A. Bailey, John R. Cowles and Mark D. Winkel, Arithmetic co-transformations in the real and complex logarithmic number systems, IEEE Transactions on Computers 47(7) (1998), 777-786"
    title: Mark G. Arnold, Thomas A. Bailey, John R. Cowles and Mark D. Winkel, Arithmetic co-transformations in the real and complex logarithmic number systems
    locator: the singularity of log2(1 - 2^z) at z = 0 and the co-transformations that avoid large tables near it
  - paper: "J. Nicholas Coleman, Edward I. Chester, Christopher I. Softley and Jiri Kadlec, Arithmetic on the European logarithmic microprocessor, IEEE Transactions on Computers 49(7) (2000), 702-715"
    title: J. Nicholas Coleman, Edward I. Chester, Christopher I. Softley and Jiri Kadlec, Arithmetic on the European logarithmic microprocessor
    locator: the 32-bit format with 23 fractional bits, interpolation with error correction for addition and subtraction, and the measured comparison with binary32
  - paper: "John N. Mitchell Jr., Computer multiplication and division using binary logarithms, IRE Transactions on Electronic Computers EC-11(4) (1962), 512-517"
    title: John N. Mitchell Jr., Computer multiplication and division using binary logarithms
    locator: the approximation log2(1 + m) ≈ m behind cheap logarithmic multipliers
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.2, Model of Arithmetic (the standard model that this page compares against); Section 3.1 (products of n factors and γ_n)
---

A logarithmic number system stores a nonzero real $x$ as a sign bit and a fixed-point approximation of $\log_2 |x|$. Multiplication, division, squaring and reciprocals become additions, subtractions and shifts of fixed-point numbers, so they are exact up to overflow of the logarithm field. Addition and subtraction become the hard operations: they need the functions $\log_2(1 \pm 2^z)$, which hardware gets from tables or interpolation. This page treats LNS as a model of computation next to the [standard model of floating-point arithmetic](/floating-point-model/): which operations are exact, which ones round, and by how much.

## The machine

**Values.** Fix $f$ fractional bits and $k$ integer bits for the logarithm. A value is a pair $(s, L)$ where $s \in \{0, 1\}$ is the sign and $L$ is a two's complement fixed-point number with $k$ integer bits and $f$ fractional bits, so $L \in 2^{-f}\mathbb{Z}$ and $-2^{k-1} \le L < 2^{k-1}$. The pair stands for
$$
x = (-1)^s \, 2^{L}.
$$
Zero has no logarithm, so it gets a reserved bit pattern, usually the most negative $L$ with a flag. The positive values form a geometric grid with constant ratio $\rho = 2^{2^{-f}}$ between neighbours. A floating-point grid is piecewise linear instead: its spacing is constant within each binade and jumps by $\beta$ at each power of the base. That jump is the wobble of the [ulp](/ulp/) relative to $|x|$. The LNS grid has no wobble.

A common 32-bit layout uses $k = 8$ and $f = 23$, plus one sign bit. That gives a range from about $2^{-128}$ to $2^{128}$ and a fraction field the same width as binary32 (Coleman et al. 2000). We take that layout as the default here when a number is needed.

**Rounding a real into the machine.** The rounded value of a real $x \ne 0$ in range is $\mathrm{fl}(x) = \operatorname{sign}(x)\, 2^{\mathrm{rn}_f(\log_2 |x|)}$, where $\mathrm{rn}_f$ rounds to the nearest multiple of $2^{-f}$. Define the LNS unit roundoff
$$
u_L = 2^{2^{-(f+1)}} - 1 \approx 2^{-(f+1)} \ln 2 .
$$
For $f = 23$ this is $u_L \approx 4.13 \times 10^{-8}$. For comparison, binary32 has $u = 2^{-24} \approx 5.96 \times 10^{-8}$.

**Steps.** For $x = (s_x, L_x)$ and $y = (s_y, L_y)$:

- Multiplication: $(s_x \oplus s_y,\ L_x + L_y)$. Division: $(s_x \oplus s_y,\ L_x - L_y)$. Both are one fixed-point addition.
- Square root of a positive value: $(0, L_x / 2)$, a right shift. The shift is exact when the last bit of $L_x$ is 0. Otherwise it drops one bit, which is a tie between two grid points.
- Addition and subtraction of magnitudes: order the operands so that $L_x \ge L_y$ and set $z = L_y - L_x \le 0$. Then
$$
|x| + |y| = 2^{L_x + s_b(z)}, \qquad |x| - |y| = 2^{L_x + d_b(z)},
$$
with the Gaussian logarithms
$$
s_b(z) = \log_2(1 + 2^{z}), \qquad d_b(z) = \log_2(1 - 2^{z}).
$$
The machine computes $L_x + \widehat{s_b}(z)$ or $L_x + \widehat{d_b}(z)$, where the hat marks a value read from a table or interpolated. The sign of the result follows from the signs of $x$ and $y$ and from which magnitude is larger. Equal magnitudes with opposite signs give the reserved zero.
- Comparison of magnitudes is a fixed-point comparison of $L_x$ and $L_y$.

## What it counts

The model counts the same operations as the standard model: one step per $+, -, \times, /$ or $\sqrt{\cdot}$. What changes is the cost of each step and the error each step makes.

- **Cost.** Multiplication and division cost one fixed-point adder, which is cheaper than a floating-point multiplier. Addition and subtraction cost a fixed-point subtraction to form $z$, a function evaluation for $s_b$ or $d_b$, and a fixed-point addition. The function evaluation is the expensive part. So LNS reverses the usual cost order: products are cheap, sums are expensive.
- **Error.** Each step is charged one relative perturbation $\delta$ of the result, as in the standard model. Multiplication and division have $\delta = 0$. Addition and subtraction have $|\delta| \le u_L$ when the result logarithm is rounded to nearest, and a larger bound when $\widehat{s_b}$ and $\widehat{d_b}$ are less accurate. The exact statements are in the section on known results.
- **Exceptions.** Overflow and underflow happen when a logarithm leaves $[-2^{k-1}, 2^{k-1})$. There is no gradual underflow and nothing like [subnormal numbers](/subnormal-numbers/): the grid stays geometric all the way down to the smallest value.

**A worked example.** Take a toy system with $f = 8$, so $u_L = 2^{1/512} - 1 \approx 1.355 \times 10^{-3}$. Store $x = 3$ and $y = 5$:

| quantity | stored $L$ (times $2^8$) | value $2^{L}$ |
|---|---|---|
| $x \approx 3$ | 406 | 3.002028... |
| $y \approx 5$ | 594 | 4.994403... |
| $x \cdot y$ | 406 + 594 = 1000 | 14.993341... |
| $x + y$ | 594 + 174 = 768 | 8 exactly |
| $y - x$ | 594 - 339 = 255 | 1.994592... |

Here $z = (406 - 594)/256 = -0.734375$. Then $s_b(z) = 0.679043...$ rounds to $174/256$, and $d_b(z) = -1.325822...$ rounds to $-339/256$. The product incurs no new error: its error is only that of the stored inputs, which is $|14.99334/15 - 1| \approx 4.4 \times 10^{-4}$. The difference of the two stored values is exactly $4.994403... - 3.002028... = 1.992375...$, and the result $1.994592...$ is within $1.12 \times 10^{-3} \le u_L$ of it in relative terms.

## Relation to other models

**The standard floating-point model.** The [standard model](/floating-point-model/) charges $|\delta| \le u$ to every operation. LNS with correctly rounded addition satisfies the same model with $u$ replaced by $u_L$, so every error bound proved in the standard model carries over with $u \to u_L$. LNS is in fact stronger, since $\delta = 0$ for multiplication and division. Bounds that come from long chains of products therefore improve: the product of $n$ stored numbers has no rounding error beyond its inputs, where [floating-point products](/floating-point-product-error/) accumulate up to $\gamma_{n-1}$. In the other direction, LNS loses the exact properties that IEEE arithmetic has beyond the standard model. Small integers other than powers of 2 are not representable, so integer counting is inexact. [Sterbenz's lemma](/sterbenz-lemma/) fails, because $x - y$ for nearby $x, y$ is not exact. The [error-free transformations](/error-free-transformations/) have no LNS analogue.

**Floating point as a coarse logarithm.** A binary floating-point number $2^{e}(1 + m)$ with $0 \le m < 1$ has $\log_2 = e + \log_2(1 + m)$, and $\log_2(1 + m) \approx m$ to within about $0.086$. So the exponent and fraction field, read as one fixed-point number, is a piecewise linear approximation of the logarithm. Mitchell (1962) used this to build approximate multipliers. The same fact is behind [fast inverse square root](/fast-inverse-square-root/). LNS replaces that approximation with the exact logarithm, rounded to $f$ fractional bits.

**Log-domain arithmetic in software.** Probabilistic models such as [hidden Markov models](/hidden-markov-model/) store probabilities as logarithms to avoid underflow. A product of probabilities is then a sum of logs, and a sum of probabilities is computed with the [log-sum-exp trick](/log-sum-exp-trick/). The function $s_b$ is the base-2 form of $\log(e^a + e^b) = a + \log(1 + e^{b - a})$, so software log-domain code is an unsigned LNS whose $s_b$ is computed by `log1p` and `exp` in floating point. The [Viterbi algorithm](/viterbi-algorithm/) needs only maxima and sums of logs, so in this setting it never needs $s_b$ at all.

**Other number formats.** [Posits](/posit-format/) also have a relative precision that varies smoothly. They have tapered precision, with the most fraction bits near 1 and fewer at the extremes. LNS keeps uniform relative precision over its whole range. [Block floating point](/block-floating-point/) shares one exponent across a vector. LNS shares nothing: each value carries its own full logarithm. The [real RAM](/real-ram/) is the exact limit of all of these as $f \to \infty$.

## Known results in the model

Let $f$ be the number of fractional bits, $u_L = 2^{2^{-(f+1)}} - 1$, and assume no overflow or underflow of the logarithm field.

1. **Representation error (proved).** For every real $x \ne 0$ in range, $\mathrm{fl}(x) = x(1 + \delta)$ with $|\delta| \le u_L$. *Proof.* Let $t = \mathrm{rn}_f(\log_2|x|) - \log_2|x|$, so $|t| \le 2^{-(f+1)}$. Then $\mathrm{fl}(x)/x = 2^{t}$. Over this range of $t$, the largest value of $|2^t - 1|$ is $2^{2^{-(f+1)}} - 1$, reached at the upper end, because $2^{a} - 1 \ge 1 - 2^{-a}$ for $a \ge 0$. The bound is attained in the limit, for $\log_2 |x|$ just below the midpoint of two grid points. Unlike floating point, the worst case is the same in every part of the range.

2. **Exact products and quotients (proved).** For stored $x, y$, the computed $x \times y$ and $x / y$ equal the exact results. *Proof.* $L_x \pm L_y$ is again a multiple of $2^{-f}$, so no rounding happens, and the result is in range by assumption. It follows that $\mathrm{fl}(x_1 x_2 \cdots x_n) = x_1 x_2 \cdots x_n$ exactly for stored $x_i$, in any order. Products of $n$ real inputs that are first rounded into the system satisfy $|\delta| \le (1 + u_L)^n - 1$, and this error comes only from the inputs.

3. **Square root (proved).** $\sqrt{x}$ for stored $x > 0$ is exact when the last bit of $L_x$ is 0. Otherwise $L_x / 2$ lies exactly halfway between two grid points, so a tie rule picks one of them and the result has $|\delta| \le u_L$.

4. **Addition and subtraction (proved, under an assumption on the tables).** If $\widehat{s_b}(z)$ and $\widehat{d_b}(z)$ are rounded to the nearest multiple of $2^{-f}$, then the computed sum or difference of stored $x, y$ is $(x \pm y)(1 + \delta)$ with $|\delta| \le u_L$. *Proof.* $L_x$ is already a multiple of $2^{-f}$. So $L_x + \mathrm{rn}_f(s_b(z)) = \mathrm{rn}_f(L_x + s_b(z)) = \mathrm{rn}_f(\log_2(|x| + |y|))$, and result 1 applies. If the table instead returns values within $\eta$ of the true function, with $\eta \ge 2^{-(f+1)}$, the same argument gives $|\delta| \le 2^{\eta} - 1$. Correct rounding of $s_b$ and $d_b$ is subject to the [table maker's dilemma](/table-maker-dilemma/), as for any transcendental function. Practical designs aim for an error a little above half a unit of the last place of $L$. The ELM paper reports addition accuracy comparable to or better than binary32 (Coleman et al. 2000). That is a measured result, not a proved bound.

5. **The useful domain of $s_b$ (proved).** For $z \le -(f+2)$, $0 < s_b(z) < 2^{-(f+1)}$. So $\mathrm{rn}_f(s_b(z)) = 0$, and $x + y$ rounds to $x$. *Proof.* $\log_2(1 + t) \le t / \ln 2$ for $t > 0$. With $t = 2^{z} \le 2^{-(f+2)}$ this gives $s_b(z) \le 2^{-(f+2)} / \ln 2 \approx 0.72 \cdot 2^{-(f+1)} < 2^{-(f+1)}$. A table for $s_b$ therefore needs only $z \in (-(f+2), 0]$, which is $(f+2) \cdot 2^{f}$ grid points. That is about $2.1 \times 10^{8}$ entries for $f = 23$. So direct lookup is only practical for small $f$, and 32-bit designs interpolate from much smaller tables.

6. **The subtraction singularity (proved).** $d_b(z) \to -\infty$ as $z \to 0^-$, and $d_b'(z) = -2^{z} / (1 - 2^{z})$ is unbounded there. For $z = -2^{-f}$, the closest pair of distinct magnitudes, $d_b(z) \approx \log_2(2^{-f} \ln 2) = -f - 0.53$. For example, $d_b(-2^{-8}) \approx -8.53$ in the toy system. Linear or quadratic interpolation of $d_b$ near $0$ therefore needs very fine tables. *Co-transformation* rewrites $d_b(z)$ for $z$ near 0 as a combination of one value of $d_b$ at a $z$ far from 0 and one entry from a small table indexed by the low bits of $z$, and so removes the problem (Arnold et al. 1998; Coleman et al. 2000). This is the LNS form of [catastrophic cancellation](/catastrophic-cancellation/). The subtraction itself rounds with $|\delta| \le u_L$ as in result 4. What is hard is evaluating $d_b$ accurately and cheaply, and the inputs' representation errors are amplified by the condition number $(|x| + |y|)/|x - y|$ exactly as in floating point.

7. **No wobble (proved).** The relative distance between neighbouring values is $\rho - 1 = 2^{2^{-f}} - 1$ everywhere in range. In binary floating point it varies by a factor of 2 within each binade. So for the same number of fraction bits, the LNS worst-case relative representation error $u_L \approx 0.69 \cdot 2^{-(f+1)}$ is smaller than the floating-point worst case $2^{-(f+1)}$ by the factor $\ln 2$. The floating-point average case is better than its worst case, which narrows the gap (Swartzlander and Alexopoulos 1975 compare the two).

## References
