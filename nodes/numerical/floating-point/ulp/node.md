---
tag: CFSGM2
kind: definition
slug: ulp
name: Unit in the last place (ulp)
aliases:
- unit in the last place
- unit of least precision
- math.ulp
area: numerical/floating-point
level: intro
summary: The weight of the last significand digit of a number, β^(e-p+1); it is the gap between adjacent floats and the usual unit for rounding errors.
prereqs: [floating-point-arithmetic]
see_also: [machine-epsilon, relative-error, round-to-nearest-even, rounding-modes, subnormal-numbers, ieee-754, floating-point-model, correctly-rounded-functions]
sources:
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.3.2, the ulp function (Goldberg's definition extended to all reals, Harrison's and Kahan's definitions, and the properties of rounding in ulps); Section 2.3.3 on the link between errors in ulps and relative errors
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 1.2, Relative Error and Ulps (the definition of ulps, the wobble, and the relation to relative error)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.1, Floating Point Number System (Lemma 2.1 on the spacing of the floats, and the remark on ulp)
  - url: https://docs.python.org/3/library/math.html#math.ulp
    title: Python documentation, math.ulp and math.nextafter
    locator: the definition of math.ulp(x) for finite, zero, infinite and NaN arguments
---

The *unit in the last place* of a real number $x$, written $\mathrm{ulp}(x)$, is the value that a change of one unit in the last significand digit makes, for the [floating-point](/floating-point-arithmetic/) numbers near $x$. For a float $x$ it is the gap between $|x|$ and the next larger float. Rounding errors are often given in ulps: a correctly rounded operation is off by at most half an ulp, and a good math library is off by less than one ulp. Several definitions exist, and they differ near powers of the base; this site uses the one of Muller et al., which is also the one of Python's `math.ulp`.

## Definition

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$. The default is binary64: $\beta = 2$, $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$. $\mathrm{RN}$, $\mathrm{RD}$ and $\mathrm{RU}$ are rounding to nearest, down and up.

**Definition (Goldberg's, extended to all reals; Muller et al., Section 2.3.2).** For a real $x \neq 0$, let $e$ be the integer with $\beta^{e} \le |x| < \beta^{e+1}$. Then

$$\mathrm{ulp}(x) = \beta^{\max(e, \, e_{\min}) - p + 1}, \qquad \mathrm{ulp}(0) = \beta^{e_{\min} - p + 1}.$$

In binary64, $\mathrm{ulp}(x) = 2^{e - 52}$ for $|x| \ge 2^{-1022}$, and $\mathrm{ulp}(x) = 2^{-1074}$ below it. The value depends on the binade of $x$ only, so $\mathrm{ulp}$ is a step function of $|x|$ that does not decrease.

**Facts (proved, for $\mathbb{F}$ with no upper bound on the exponent; overflow is treated apart).**

1. *Successor.* For $x \in \mathbb{F}$ with $x \ge 0$, the next float above $x$ is $x + \mathrm{ulp}(x)$. *Proof.* Let $x = M \beta^{\max(e, e_{\min}) - p + 1}$ with an integer $M$, $0 \le M < \beta^{p}$. The floats of the same binade are the integer multiples of $\mathrm{ulp}(x)$ in it, and if $M = \beta^{p} - 1$, then $x + \mathrm{ulp}(x) = \beta^{e+1}$, which is the first float of the next binade.
2. *Rounding to nearest.* For each real $x$, $|\mathrm{RN}(x) - x| \le \tfrac12 \mathrm{ulp}(x)$. *Proof.* The floats in $[\beta^{e}, \beta^{e+1}]$ (or in $[0, \beta^{e_{\min}}]$) are spaced $\mathrm{ulp}(x)$ apart, and both ends are floats, so $x$ is within half a gap of one of them.
3. *Directed rounding.* For each real $x$, $|\mathrm{RD}(x) - x| < \mathrm{ulp}(x)$ and $|\mathrm{RU}(x) - x| < \mathrm{ulp}(x)$, by the same argument.
4. *Converse, in base 2.* If $\beta = 2$, $y \in \mathbb{F}$ and $|y - x| < \tfrac12 \mathrm{ulp}(x)$, then $y = \mathrm{RN}(x)$. *Proof.* Let $g = \mathrm{ulp}(x)$ and $2^{e} \le |x| < 2^{e+1}$, with $x > 0$ (the case $x < 0$ is symmetric, and the subnormal range is one grid of spacing $g$). The floats of $[2^{e}, 2^{e+1}]$ are the multiples of $g$ there, and only one of them is within less than $g/2$ of $x$; it is the nearest float of that interval, and so the nearest float, because each float outside the interval is farther than an end. A float $y < 2^{e}$ is at most $2^{e} - g/2$, so $x - y \ge g/2$. A float $y > 2^{e+1}$ is at least $2^{e+1} + 2g$, so $y - x > 2g$. So $y$ is in the interval, and $y = \mathrm{RN}(x)$. $\square$ In base 10 the claim fails just above a power of 10: with $p = 3$, $x = 1.003$ and $y = 0.999$, $|y - x| = 0.004 < \tfrac12 \mathrm{ulp}(x) = 0.005$, but $\mathrm{RN}(x) = 1.00$.
5. *Relative size.* For $|x| \ge \beta^{e_{\min}}$, $\beta^{-p} |x| < \mathrm{ulp}(x) \le \beta^{1-p} |x|$. So an error of $k$ ulps is a [relative error](/relative-error/) between $k\beta^{-p}$ and $k\beta^{1-p}$, and an error of half an ulp is at most $u = \tfrac12\beta^{1-p}$ in relative terms.

**Other definitions.** *Harrison's:* $\mathrm{ulp}(x)$ is the distance between the two closest floats $a \le x \le b$ with $a \neq b$. *Kahan's:* $\mathrm{ulp}(x)$ is the gap between the two floats nearest to $x$, even if $x$ is one of them. For $x$ well inside a binade the three agree. At a power of the base they differ: in binary64, Goldberg's $\mathrm{ulp}(1) = 2^{-52}$, the gap above 1, while Harrison's and Kahan's give $2^{-53}$, the gap below 1. Fact 2 holds for all three. Muller et al. list which of the other facts each definition keeps in each base.

**Ulp distance between floats.** For two finite binary64 values of the same sign, read their 64-bit words as integers. The difference of the integers is the number of floats from one to the other, because the [IEEE 754](/ieee-754/) encoding is monotone in the magnitude. A result that is "within $k$ ulps" in a test suite usually means this distance is at most $k$.

## Examples and non-examples

**Values in binary64.**

| $x$ | $\mathrm{ulp}(x)$ | note |
|---|---|---|
| $1$ | $2^{-52} \approx 2.22 \times 10^{-16}$ | [machine epsilon](/machine-epsilon/) |
| $0.9999999999999999$ (the float below 1) | $2^{-53}$ | the gap is halved below a power of 2 |
| $0.1$ | $2^{-56} \approx 1.39 \times 10^{-17}$ | $2^{-4} \le 0.1 < 2^{-3}$ |
| $3$ | $2^{-51} \approx 4.44 \times 10^{-16}$ | |
| $10^{16}$ | $2$ | odd integers above $2^{53}$ are not floats |
| $2^{53}$ | $2$ | `2.0**53 + 1 == 2.0**53` is true |
| $10^{20}$ | $2^{14} = 16384$ | |
| the largest float $(2 - 2^{-52}) 2^{1023}$ | $2^{971}$ | |
| $2^{-1022}$, the smallest normal | $2^{-1074}$ | |
| $0$ and each [subnormal](/subnormal-numbers/) | $2^{-1074} \approx 4.94 \times 10^{-324}$ | the gap is constant below $2^{-1022}$ |

Python's `math.ulp` returns these values. It returns `inf` for an infinity and `nan` for a NaN, and $\mathrm{ulp}(-x) = \mathrm{ulp}(x)$.

**Half an ulp at a power of two.** Take $x = 1 - 2^{-55}$. Its binade is $[1/2, 1)$, so $\mathrm{ulp}(x) = 2^{-53}$, and $\mathrm{RN}(x) = 1$ with error $2^{-55} \le \tfrac12 \mathrm{ulp}(x)$. The float $1 - 2^{-53}$ is at distance $3 \cdot 2^{-55}$, more than half an ulp.

**Ulp distance.** The word of `0.1 + 0.2` is one more than the word of `0.3`, so the two values are 1 ulp apart. The words of 1.0 and 2.0 differ by $2^{52}$: there are $2^{52}$ floats in $[1, 2)$.

**Non-examples.**

- An ulp is not a relative unit. An error of 1 ulp is a relative error of $2^{-52}$ at $x = 1$ and of about $2^{-53}$ at $x = 2 - 2^{-52}$. Results that cross a power of 2 can change by a factor of 2 in ulps with no change in the relative error.
- The ulp of the result is not always the ulp of the exact value. For $x$ just below $1$, $\mathrm{RN}(x)$ can be $1$, and $\mathrm{ulp}(1) = 2\,\mathrm{ulp}(x)$. A bound "half an ulp of the result" and a bound "half an ulp of the exact value" are different statements; the second is the stronger one here.
- `x * (1 + 2**-52)` is not in general `x + math.ulp(x)`. Use `math.nextafter(x, math.inf)` for the successor.

## Related definitions

- [Machine epsilon](/machine-epsilon/): $\varepsilon = \mathrm{ulp}(1) = \beta^{1-p}$, and the unit roundoff $u = \varepsilon/2$.
- [Relative error](/relative-error/): the measure that fact 5 converts ulps into.
- [Round to nearest, ties to even](/round-to-nearest-even/) and [rounding modes](/rounding-modes/): the roundings in facts 2 and 3.
- [Subnormal numbers](/subnormal-numbers/): the range where the ulp stays constant.
- [Correctly rounded functions](/correctly-rounded-functions/): functions with an error of at most half an ulp.
- [Standard model of floating-point arithmetic](/floating-point-model/): the relative form of fact 2.

## References
