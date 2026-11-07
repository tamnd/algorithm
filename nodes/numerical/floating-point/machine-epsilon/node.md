---
tag: DERCNY
kind: definition
slug: machine-epsilon
name: Machine epsilon
aliases:
- unit roundoff
- machine precision
- DBL_EPSILON
area: numerical/floating-point
level: intro
summary: The gap between 1 and the next larger floating-point number, ε = β^(1-p); half of it is the unit roundoff u that bounds the relative error of rounding to nearest.
prereqs: [floating-point-arithmetic, ulp]
see_also: [ulp, relative-error, floating-point-model, ieee-754, round-to-nearest-even, rounding-modes, rounding-error-analysis, subnormal-numbers]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.1, Floating Point Number System (the machine epsilon ε_M = β^(1-t), Lemma 2.1 on the spacing, Theorem 2.2 with the unit roundoff u)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.3.1, Relative error due to rounding (the unit roundoff u and the bound u/(1 + u)); Chapter 4, Section 4.1 on testing the computational environment
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 1.2, Relative Error and Ulps (the machine epsilon and the wobble of a factor β)
  - paper: "M. A. Malcolm, Algorithms to reveal properties of floating-point arithmetic, Communications of the ACM 15(11) (1972), 949-951"
    title: M. A. Malcolm, Algorithms to reveal properties of floating-point arithmetic
    locator: the loops that find the base and the precision of the arithmetic at run time
  - paper: "W. J. Cody, Algorithm 665: MACHAR, a subroutine to dynamically determine machine parameters, ACM Transactions on Mathematical Software 14(4) (1988), 303-311"
    title: W. J. Cody, MACHAR, a subroutine to dynamically determine machine parameters
    locator: the computation of eps, epsneg and the other parameters
---

Machine epsilon is the distance $\varepsilon = \beta^{1-p}$ from 1 to the next larger number of a [floating-point](/floating-point-arithmetic/) system. Half of it, the *unit roundoff* $u = \varepsilon/2$, bounds the [relative error](/relative-error/) of each rounding to nearest, and it is the constant in the [standard model](/floating-point-model/) of error analysis. For binary64, $\varepsilon = 2^{-52} \approx 2.22 \times 10^{-16}$ and $u = 2^{-53} \approx 1.11 \times 10^{-16}$. The two names are used with both meanings in the literature, so a text must say which one it means.

## Definition

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$. The default is binary64: $\beta = 2$, $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$. $\mathrm{fl}(x)$ is the value of the real $x$ rounded to $\mathbb{F}$. The [ulp](/ulp/) follows Muller et al., Section 2.3.2: for $\beta^{e} \le |x| < \beta^{e+1}$, $\mathrm{ulp}(x) = \beta^{\max(e, e_{\min}) - p + 1}$.

**Machine epsilon.**

$$\varepsilon = \beta^{1-p} = \mathrm{ulp}(1).$$

The numbers of $\mathbb{F}$ in $[1, \beta)$ are $1, 1 + \varepsilon, 1 + 2\varepsilon, \ldots$, so $\varepsilon$ is the gap between 1 and its successor. This is Higham's $\varepsilon_M$, C's `DBL_EPSILON`, and Python's `sys.float_info.epsilon`.

**Unit roundoff.**

$$u = \tfrac12 \beta^{1-p} = \frac{\varepsilon}{2} \quad \text{(rounding to nearest)}, \qquad u = \beta^{1-p} = \varepsilon \quad \text{(directed rounding)}.$$

On this site $u$ means the first value, $2^{-53}$ for binary64, unless a page says that it uses a directed rounding.

**The bound that $u$ gives (proved).** Let $x$ be a real number with $\beta^{e_{\min}} \le |x| \le \max \mathbb{F}$, and let $\mathrm{fl}$ round to nearest (any tie rule). Then

$$\mathrm{fl}(x) = x(1 + \delta), \qquad |\delta| \le \frac{u}{1 + u} < u.$$

*Proof.* Let $\beta^{e} \le |x| < \beta^{e+1}$ with $e \ge e_{\min}$. The floats in $[\beta^{e}, \beta^{e+1}]$ are spaced $\beta^{e-p+1}$ apart, and both ends are floats (the upper end may be the overflow threshold, but $|x| \le \max\mathbb{F}$ keeps the nearest float finite). So $|\mathrm{fl}(x) - x| \le \tfrac12 \beta^{e-p+1} = u \beta^{e}$. If $|x| \ge \beta^{e}(1 + u)$, then $|\delta| \le u\beta^{e}/|x| \le u/(1+u)$. If $\beta^{e} \le |x| < \beta^{e}(1 + u)$, then the nearest float is $\beta^{e}$, because $\beta^{e}(1+u)$ is the midpoint of $\beta^{e}$ and $\beta^{e}(1 + 2u)$. So $|\mathrm{fl}(x) - x| = |x| - \beta^{e}$ and $|\delta| = 1 - \beta^{e}/|x| < 1 - 1/(1+u) = u/(1+u)$. $\square$

The simpler bound $|\delta| \le u$ is Higham's Theorem 2.2. The sharper $u/(1+u)$ is in Muller et al., Section 2.3.1. Below $\beta^{e_{\min}}$ the relative error is not bounded by $u$: see [subnormal numbers](/subnormal-numbers/). With a directed rounding the same argument gives $|\delta| < \varepsilon$.

**Relative spacing.** For a normal $x \in \mathbb{F}$, the gap between $|x|$ and the next float above it is $\mathrm{ulp}(x)$. If $\beta^{e} \le |x| < \beta^{e+1}$, then $\mathrm{ulp}(x) = \beta^{e}\varepsilon$, so

$$\frac{\varepsilon}{\beta} |x| < \mathrm{ulp}(x) \le \varepsilon |x|,$$

with equality on the right exactly when $|x|$ is a power of $\beta$ (Higham, Lemma 2.1, states the spacing bounds with $\le$ on both sides). So the relative gap changes by a factor of up to $\beta$ inside each binade. Goldberg calls this factor the *wobble*. It is one reason to prefer $\beta = 2$.

### The other definition

Some books define machine epsilon as the smallest positive float $x$ with $\mathrm{fl}(1 + x) > 1$. This is a different number. With round to nearest, ties to even in binary64, $1 + 2^{-53}$ is a tie between 1 and $1 + 2^{-52}$, and it rounds to 1, the even one. The smallest float above $2^{-53}$ is $2^{-53} + 2^{-105}$, and $1$ plus it rounds up. So this definition gives $2^{-53} + 2^{-105}$, which is $u$ plus a tiny amount, not $\varepsilon$. It depends on the rounding mode, which the definition $\beta^{1-p}$ does not.

## Examples and non-examples

**Values for the common formats.**

| format | $p$ | $\varepsilon = 2^{1-p}$ | $u = 2^{-p}$ |
|---|---|---|---|
| bfloat16 | 8 | $2^{-7} = 0.0078125$ | $2^{-8} = 0.00390625$ |
| binary16 | 11 | $2^{-10} \approx 9.77 \times 10^{-4}$ | $2^{-11} \approx 4.88 \times 10^{-4}$ |
| binary32 | 24 | $2^{-23} \approx 1.19 \times 10^{-7}$ | $2^{-24} \approx 5.96 \times 10^{-8}$ |
| binary64 | 53 | $2^{-52} \approx 2.22 \times 10^{-16}$ | $2^{-53} \approx 1.11 \times 10^{-16}$ |
| binary128 | 113 | $2^{-112} \approx 1.93 \times 10^{-34}$ | $2^{-113} \approx 9.63 \times 10^{-35}$ |

So binary64 holds a little less than 16 significant decimal digits: $-\log_{10} u \approx 15.95$.

**In Python.** `sys.float_info.epsilon == 2**-52` is true, and so is `math.ulp(1.0) == 2**-52`. The test `1.0 + 2**-53 == 1.0` is true (the tie goes to even), while `1.0 + math.nextafter(2**-53, 1) > 1.0` is true. Below 1 the gap is smaller: `math.nextafter(1.0, 0) == 1 - 2**-53`, because $[1/2, 1)$ has spacing $\varepsilon/2$.

**The bound $u/(1+u)$ is attained in the limit.** Take $x = 1 + u = 1 + 2^{-53}$. It rounds to 1, and the relative error is $u/(1 + u)$, which is $0.99999999999999989 \cdot u$. For $x = 1/3$, the stored value is $\mathrm{fl}(1/3) = 1/3 - 1/54043195528445952$, and the relative error is $2^{-54} = u/2$.

**The classic loop.** The loop `e = 1.0; while 1.0 + e/2 > 1.0: e /= 2` stops with `e == 2**-52` in binary64. It finds $\varepsilon$ because it only tries powers of 2, and $1 + 2^{-53}$ rounds down. On an x87 unit that keeps `1.0 + e/2` in an 80-bit register, the same loop can stop at $2^{-63}$, the epsilon of the extended format. Malcolm (1972) and Cody's MACHAR (1988) are careful versions of such loops.

**Non-examples.**

- $\varepsilon$ is not the smallest positive float. The smallest normal binary64 number is $2^{-1022}$ and the smallest subnormal is $2^{-1074}$, both far below $2^{-52}$.
- $\varepsilon$ is not the absolute error of a rounding. The absolute error near $x$ is up to $\tfrac12 \mathrm{ulp}(x)$, which is about $u|x|$; for $x = 10^{20}$ it is $8192$.
- $u$ does not bound the error of a computation of many operations. It bounds one rounding. The errors of $n$ operations add up to bounds such as $\gamma_n = nu/(1 - nu)$: see [rounding error analysis](/rounding-error-analysis/).

## Related definitions

- [Unit in the last place](/ulp/): $\varepsilon = \mathrm{ulp}(1)$, and $\mathrm{ulp}(x) \approx \varepsilon |x|$ for a normal $x$.
- [Relative error](/relative-error/): the measure that $u$ bounds.
- [Standard model of floating-point arithmetic](/floating-point-model/): $\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta)$, $|\delta| \le u$.
- [Rounding modes](/rounding-modes/) and [round to nearest, ties to even](/round-to-nearest-even/): the mode decides whether $u = \varepsilon/2$ or $u = \varepsilon$.
- [IEEE 754](/ieee-754/): fixes $p$, and so $\varepsilon$, for each format.
- [Rounding error analysis](/rounding-error-analysis/): builds bounds from $u$.

## References
