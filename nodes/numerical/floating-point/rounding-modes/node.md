---
tag: RJRH3Z
kind: concept
slug: rounding-modes
name: Rounding modes
aliases:
- rounding direction
- rounding-direction attributes
- directed rounding
area: numerical/floating-point
level: intro
summary: The rules that map a real result to a float. IEEE 754 defines round to nearest (ties to even or away from zero), toward zero, toward plus infinity and toward minus infinity.
prereqs: [floating-point-arithmetic, ulp]
see_also: [round-to-nearest-even, ieee-754, interval-arithmetic, stochastic-rounding, machine-epsilon, double-rounding, floating-point-model, special-floating-point-values]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 4.3, Rounding-direction attributes (4.3.1 rounding to nearest with the overflow rule, 4.3.2 directed rounding, 4.3.3 rounding attribute requirements); Clause 6.3, The sign bit (the sign of an exact zero sum)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.2, Rounding (the rounding functions RN, RD, RU, RZ, faithful rounding, and their properties such as monotonicity)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.1 (rounding and the unit roundoff for chopping), Section 2.3 (IEEE arithmetic and its rounding modes) and Section 2.8 (statistical distribution of rounding errors)
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 1.5, Exactly Rounded Operations (round to even and the drift example); Section 2.3, the part on the rounding modes of the IEEE standard
---

A rounding mode is the rule that chooses which [floating-point](/floating-point-arithmetic/) number stands for a real result that the format cannot hold. The [IEEE 754](/ieee-754/) standard defines five: round to nearest with ties to even (the default), round to nearest with ties away from zero, and the three *directed* roundings toward $+\infty$, toward $-\infty$ and toward zero. Each basic operation must return the exact result rounded by the active mode, so the mode decides the last bit of each result, the error bound $u$, and the bias of the errors.

## In plain words

A float has a fixed number of digits, so most exact results fall between two floats. The computer must pick one of the two neighbours. Rounding to nearest picks the closer one, and needs a rule for an exact tie: the standard default picks the neighbour whose last digit is even. Rounding up always picks the larger neighbour, rounding down the smaller one, and rounding toward zero the one with the smaller size.

Rounding to nearest makes the smallest errors, and its errors cancel on average. Rounding up and down make larger errors, but always on a known side. That is what you need to compute a guaranteed lower and upper bound for a result.

## The idea

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64 ($\beta = 2$, $p = 53$). The unit roundoff is $u = \tfrac12 \beta^{1-p}$, which is $2^{-53}$ for binary64 with rounding to nearest. $\Omega = (\beta - \beta^{1-p})\beta^{e_{\max}}$ is the largest finite float, and $\mathrm{ulp}$ is as in Muller et al., Section 2.3.2 (see [ulp](/ulp/)).

**The five rounding functions.** For a real $x$ with $|x| \le \Omega$:

| IEEE 754 name | symbol | value |
|---|---|---|
| roundTowardNegative | $\mathrm{RD}(x)$ | the largest float $\le x$ |
| roundTowardPositive | $\mathrm{RU}(x)$ | the smallest float $\ge x$ |
| roundTowardZero | $\mathrm{RZ}(x)$ | $\mathrm{RD}(x)$ if $x \ge 0$, $\mathrm{RU}(x)$ if $x < 0$ |
| roundTiesToEven | $\mathrm{RN}(x)$ | the float nearest to $x$; on a tie, the one with an even last digit |
| roundTiesToAway | $\mathrm{RNA}(x)$ | the float nearest to $x$; on a tie, the one with the larger magnitude |

If $x \in \mathbb{F}$, all five return $x$. Otherwise $\mathrm{RD}(x) < x < \mathrm{RU}(x)$ are the two neighbours, and $\mathrm{RU}(x) - \mathrm{RD}(x) = \mathrm{ulp}(x)$. Each mode returns one of them. A rounding that returns one of the two neighbours by any rule is called *faithful*; IEEE 754 does not offer that as a mode, but some algorithms only need it. See [round to nearest, ties to even](/round-to-nearest-even/) for the tie rule.

**Beyond the largest float (Clause 4.3).** For $x > \Omega$: $\mathrm{RU}(x) = +\infty$ and $\mathrm{RD}(x) = \mathrm{RZ}(x) = \Omega$. Round to nearest returns $+\infty$ when $x \ge \beta^{e_{\max}}(\beta - \tfrac12\beta^{1-p})$, that is $\Omega + \tfrac12\mathrm{ulp}(\Omega)$, and $\Omega$ below it. In binary64 the threshold is $2^{1024}(1 - 2^{-54})$. Negative values are symmetric.

**Properties (proved from the definitions; Muller et al., Section 2.2).**

- *Monotone.* If $x \le y$, then $\circ(x) \le \circ(y)$ for each of the five modes $\circ$. This is the property that [interval arithmetic](/interval-arithmetic/) and many proofs about floats use.
- *Symmetry.* $\mathrm{RN}(-x) = -\mathrm{RN}(x)$, $\mathrm{RNA}(-x) = -\mathrm{RNA}(x)$, $\mathrm{RZ}(-x) = -\mathrm{RZ}(x)$, and $\mathrm{RD}(-x) = -\mathrm{RU}(x)$.
- *Error bounds.* In the normal range, $|\mathrm{RN}(x) - x| \le \tfrac12\mathrm{ulp}(x)$ and $|\mathrm{RD}(x) - x|, |\mathrm{RU}(x) - x|, |\mathrm{RZ}(x) - x| < \mathrm{ulp}(x)$. As relative errors, $\circ(x) = x(1 + \delta)$ with $|\delta| \le u$ for the two nearest modes and $|\delta| < 2u$ for the directed modes, when there is no underflow and no overflow (Higham, Theorem 2.2, and the [machine epsilon](/machine-epsilon/) page).
- *The sign of the error.* $\mathrm{RD}(x) - x \le 0$ and $\mathrm{RU}(x) - x \ge 0$ always. This is the reason the directed modes exist.

**The sign of an exact zero (Clause 6.3).** When the exact result of $x + y$ or $x - y$ is zero and the operands are not both zeros of the same sign, the result is $+0$ in each mode except roundTowardNegative, where it is $-0$. So `1.0 - 1.0` is `0.0` in the default mode. See [signed zero](/special-floating-point-values/).

**Requirements.** An implementation must provide roundTiesToEven and the three directed modes. roundTiesToAway is required for decimal formats only (Clause 4.3.3). The default for binary formats is roundTiesToEven. In C the mode is set with `fesetround` from `<fenv.h>`, with the values `FE_TONEAREST`, `FE_UPWARD`, `FE_DOWNWARD` and `FE_TOWARDZERO`. Python has no way to change the mode of its `float` operations; its `decimal` module has its own modes, such as `ROUND_HALF_EVEN`, `ROUND_CEILING`, `ROUND_FLOOR` and `ROUND_DOWN`.

**Bias.** Over many roundings, round toward zero makes errors of one sign for inputs of one sign, so a sum of many truncated values drifts toward zero by about half an ulp per operation. Round to nearest makes errors of both signs; with ties to even, the errors on exact ties also cancel on average (Goldberg, Theorem 5, shows that ties to even stops a drift that ties away can cause). [Stochastic rounding](/stochastic-rounding/) is a further rule, not in IEEE 754, that picks a neighbour at random so that the error has expectation zero.

## Examples

The values below are for binary64, computed from exact rationals.

| real $x$ | $\mathrm{RD}(x)$ | $\mathrm{RU}(x)$ | $\mathrm{RZ}(x)$ | $\mathrm{RN}(x)$ | $\mathrm{RNA}(x)$ |
|---|---|---|---|---|---|
| $1/10$ | `0x1.9999999999999p-4` | `0x1.999999999999ap-4` | `0x1.9999999999999p-4` | `0x1.999999999999ap-4` | `0x1.999999999999ap-4` |
| $-1/10$ | `-0x1.999999999999ap-4` | `-0x1.9999999999999p-4` | `-0x1.9999999999999p-4` | `-0x1.999999999999ap-4` | `-0x1.999999999999ap-4` |
| $1/3$ | `0x1.5555555555555p-2` | `0x1.5555555555556p-2` | `0x1.5555555555555p-2` | `0x1.5555555555555p-2` | `0x1.5555555555555p-2` |
| $1 + 2^{-53}$ (a tie) | $1$ | $1 + 2^{-52}$ | $1$ | $1$ | $1 + 2^{-52}$ |
| $2^{53} + 1$ (a tie) | $2^{53}$ | $2^{53} + 2$ | $2^{53}$ | $2^{53}$ | $2^{53} + 2$ |
| $2^{53} + 3$ (a tie) | $2^{53} + 2$ | $2^{53} + 4$ | $2^{53} + 2$ | $2^{53} + 4$ | $2^{53} + 4$ |

For $1/10$, round to nearest rounds up, because the bits of $0.1$ continue as $1001\,1001\ldots$ after the last kept bit. For $2^{53} + 1$ and $2^{53} + 3$, the two ties go in opposite directions under ties to even, so that the last bit of the result is 0 both times.

**Python's `round`.** The built-in `round` rounds to nearest with ties to even: `round(0.5) == 0`, `round(1.5) == 2`, `round(2.5) == 2` and `round(-2.5) == -2`. The call `round(2.675, 2)` gives `2.67`, not `2.68`: the literal 2.675 is stored as $3011782250804019/2^{50}$, which is below $2.675$, so there is no tie.

**Overflow.** $2^{1024}(1 - 2^{-54}) - 1$ rounds to nearest as $\Omega$ = `0x1.fffffffffffffp+1023`, and $2^{1024}(1 - 2^{-54})$ itself rounds to $+\infty$ (Python's exact conversion `float(Fraction(...))` raises `OverflowError` for it).

## Where it is used

- **The default.** Almost all code runs in roundTiesToEven. It gives the bound $|\delta| \le u$ of the [standard model](/floating-point-model/), and the [error-free transformations](/error-free-transformations/) such as [TwoSum](/two-sum/) need it.
- **Interval arithmetic.** [Interval arithmetic](/interval-arithmetic/) computes the lower end of each result with $\mathrm{RD}$ and the upper end with $\mathrm{RU}$, so that the true value is always inside.
- **A test of sensitivity.** Running a program in the four modes and comparing the results is a cheap test of how much rounding errors affect it. It is a heuristic, not a bound: a program can give the same wrong result in all four modes.
- **Conversion to integers.** A cast from `double` to `int` in C rounds toward zero. `math.floor` and `math.ceil` round down and up to an integer.
- **Exact rounding of other operations.** A correctly rounded result in one mode can be built from the result in another mode, for example $\mathrm{RU}(x) = -\mathrm{RD}(-x)$. Libraries use this to provide all modes from one code path.
- **Decimal money.** Financial rules often require round half up or half even on decimal amounts; the decimal formats of [IEEE 754](/ieee-754/) and Python's `decimal` module support them.

## References
