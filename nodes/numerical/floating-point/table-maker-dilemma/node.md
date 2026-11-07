---
tag: 3QB409
kind: problem
slug: table-maker-dilemma
name: Table-maker's dilemma
aliases:
- Table maker's dilemma
- TMD
- hardest-to-round cases
- worst cases for correct rounding
area: numerical/floating-point
level: research
summary: Deciding how many extra digits are needed to round a function value correctly in all cases.
prereqs: [correctly-rounded-functions, rounding-modes, ulp]
see_also: [correctly-rounded-elementary-functions, payne-hanek-argument-reduction, cody-waite-range-reduction, round-to-nearest-even, double-rounding, lll-algorithm, coppersmith-method, continued-fraction]
sources:
  - book: "Jean-Michel Muller, Elementary Functions, Algorithms and Implementation, third edition, Birkhauser, 2016"
    title: Jean-Michel Muller, Elementary Functions, Algorithms and Implementation, third edition (2016)
    locator: Chapter 12, Solving the Table Maker's Dilemma (the problem, the probabilistic estimate, Ziv's strategy, Lefèvre's and the SLZ worst-case searches, bounds from transcendental number theory, and tables of worst cases in binary64)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 10, Evaluating Floating-Point Elementary Functions (correct rounding and the table maker's dilemma)
  - paper: doi:10.1145/114697.116813
    title: Abraham Ziv, Fast evaluation of elementary mathematical functions with correctly rounded last bit, ACM Transactions on Mathematical Software 17(3) (1991), 410-423
    locator: the strategy of evaluating with increasing precision until the rounding is decided
  - paper: doi:10.1109/12.736435
    title: Vincent Lefèvre, Jean-Michel Muller and Arnaud Tisserand, Toward correctly rounded transcendentals, IEEE Transactions on Computers 47(11) (1998), 1235-1243
    locator: the probabilistic model of the bits after the rounding position, and the first exhaustive worst-case searches
  - paper: doi:10.1109/TC.2005.55
    title: Damien Stehlé, Vincent Lefèvre and Paul Zimmermann, Searching worst cases of a one-variable function using lattice reduction, IEEE Transactions on Computers 54(3) (2005), 340-346
    locator: the SLZ algorithm, which uses Coppersmith's method to find the inputs where a polynomial approximation of f is close to a breakpoint
  - paper: doi:10.1109/ARITH.2001.930109
    title: Tomas Lang and Jean-Michel Muller, Bounds on runs of zeros and ones for algebraic functions, 15th IEEE Symposium on Computer Arithmetic (ARITH 2001), 13-20
    locator: worst cases for square root, reciprocal, division and other algebraic functions, which need about 2p bits
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 9.2, Additional mathematical operations (recommended correctly rounded functions)
---

The table-maker's dilemma is the problem of computing $\circ(f(x))$, the correctly rounded value of a function such as $\exp$, $\log$ or $\sin$, when $f(x)$ can only be approximated. An approximation with error $\varepsilon$ gives the right rounded result unless $f(x)$ lies within $\varepsilon$ of a rounding breakpoint. Then the approximation cannot tell which way to round. The dilemma is to find how small $\varepsilon$ has to be so that this never happens for any input of a given format, or else to decide each hard case some other way. The name recalls the makers of printed tables of logarithms, who had to choose how many extra digits to compute. W. Kahan popularized the term.

## In plain words

To round a number correctly, you have to know which side of a halfway point it falls on. Most values are far from such a point, and a few extra digits are enough to settle it. But some values come extremely close to a halfway point, and you need many digits to see which side they are on. The dilemma is that you do not know in advance how close the worst value comes. You either search all inputs to find the worst one, or you keep computing more digits until the answer becomes clear.

## Definition

Let $\mathbb{F}$ be a floating-point format with radix 2 and precision $p$, and let $\circ$ be a rounding function: round to nearest, or a directed rounding. The **breakpoints** of $\circ$ are the reals at which $\circ$ is discontinuous. For round to nearest they are the midpoints between consecutive floats. For directed roundings they are the floats themselves. Let $f$ be a real function, and let $x \in \mathbb{F}$ be an input with $f(x)$ in the normal range.

- **The rounding problem.** Given $x$, compute $\circ(f(x))$, using an oracle that returns, for any $m$, an approximation $y_m$ with $|y_m - f(x)| \le 2^{-m}|f(x)|$.
- **Hardness of an input.** Write $f(x) = 2^{E}\,\tau$ with $1 \le \tau < 2$, and let $\varphi$ be the distance from $2^{p-1}\tau$ to the nearest point of $\mathbb{Z} + \tfrac12$ (for round to nearest) or of $\mathbb{Z}$ (for directed rounding). Here $\varphi$ is measured in ulps of $f(x)$. The hardness of $x$ is $k(x) = -\log_2 \varphi$, with $k(x) = \infty$ when $f(x)$ is a breakpoint. In binary, the bits of $f(x)$ after the rounding position begin with a run of about $k(x)$ equal bits, $1000\ldots$ or $0111\ldots$ for round to nearest.
- **The dilemma.** Find $k^{\ast} = \max_{x} k(x)$ over all inputs $x \in \mathbb{F}$ in the domain whose image is not a breakpoint. Treat the exact cases, where $f(x)$ is a breakpoint, separately. Then any approximation with relative error below about $2^{-(p + k^{\ast} + 1)}$ rounds correctly for every input.

The value $k^{\ast}$, together with the inputs attaining it, is called the **worst case** of $f$ for that format and rounding.

## Variants

- **Rounding mode.** Round to nearest and the directed roundings have different breakpoints, and hence different worst cases. Libraries that support all modes need both.
- **Exact cases.** Some inputs give breakpoints exactly, for example $\exp(0) = 1$, $\log_2(2^{n}) = n$, $\sqrt{x^2} = |x|$ and $x^{y}$ with small integer results. They have infinite hardness, and they must be detected and returned directly.
- **Algebraic functions.** For $\sqrt{x}$, $1/x$, $x/y$ and $\sqrt[3]{x}$, the worst cases can be described and bounded by number theory, as shown under bounds.
- **Functions of two variables.** For $x^{y}$ and $\operatorname{atan2}(y, x)$ there are about $2^{2p}$ inputs. Exhaustive search is then infeasible in binary64, and only partial results are known.
- **Decimal and other radixes.** The same problem arises for [decimal floating point](/decimal-floating-point/), with breakpoints in radix 10.

## Examples

**One rounding in binary64.** Suppose a library computes $\exp(x)$ with relative error $2^{-70}$ for some $x$. If the bits of $\exp(x)$ after bit 53 are `0110...`, the error cannot move the value across the midpoint `1000...`, and rounding the approximation is safe. If they are `0111 1111 1111 1111 1111 1111 1111 1101...`, the true value is within $2^{-30}$ ulps of the midpoint, and an error of $2^{-70}$ relative is still enough. But if the run of ones were 80 bits long, the approximation would not decide the rounding.

**Worst cases in binary16.** We evaluated $\exp$ and $\log$ at every positive normal binary16 input, with 80 significant decimal digits using Python's `decimal` module, and measured $k(x)$ for round to nearest. These are observed values from our own computation:

| function | inputs checked | $\log_2$ of the count | worst $k$ | at $x$ |
|---|---|---|---|---|
| $\exp$, $-17 < x < 11$ | 17792 | 14.12 | 16.42 | `0x1.de4p-8` |
| $\log$, $x \ne 1$ | 30719 | 14.91 | 15.79 | `0x1.17cp-3` |

For both functions, an approximation with error well below $2^{-17}$ ulps, that is, about $11 + 18 = 29$ bits of relative accuracy, rounds every binary16 input correctly. A random sample of 200000 binary32 inputs to $\exp$ in $[1, 2)$ gave a worst $k$ of 16.45, against $\log_2 200000 = 17.6$. That is what the probabilistic model below predicts for a sample of that size.

**Square root.** For $x \in [1, 4)$ in binary64, $\sqrt{x}$ is never a midpoint, and it is never closer than $2^{-108}$ to one. This is the bound proved below. So 108 bits of absolute accuracy always suffice for $\sqrt{x}$, and hardware square root never faces the dilemma.

## Known algorithms

- **Ziv's strategy.** Evaluate $f(x)$ with an error bound $\varepsilon_1$, and round if the interval $[y - \varepsilon_1, y + \varepsilon_1]$ contains no breakpoint. Otherwise recompute with a much smaller error $\varepsilon_2$, and so on (Ziv 1991). The method terminates for every input that is not an exact case, because $f(x)$ is then not a breakpoint, so some finite precision separates it. It needs no knowledge of the worst case. Its running time is unbounded a priori, but the expected time is close to that of the first step, because the probability of a retry is about $2\varepsilon_1/\mathrm{ulp}$. Libraries such as IBM's libultim and MPFR use it.
- **Exhaustive search over linear approximations (Lefèvre).** Cut a binade into small intervals on which $f$ is close to a line. On each interval, finding the inputs that land near a breakpoint is a problem of the form "find $t$ in $[0, T)$ with $\{at + b\}$ small", which continued fractions and the three-distance theorem solve quickly. The total cost is about $2^{2p/3}$ per binade. This made the binary64 worst cases of the common functions computable around the year 2000.
- **SLZ.** Stehlé, Lefèvre and Zimmermann (2005) use polynomial approximations of higher degree and find their near-breakpoint integer points with [Coppersmith's method](/coppersmith-method/), which relies on [lattice reduction](/lll-algorithm/). The heuristic cost per binade is asymptotically lower than Lefèvre's. It is the method of choice for wider formats.
- **Brute force.** For binary32 there are only $2^{32}$ inputs. Evaluating each one in high precision is feasible, and the CORE-MATH project uses exhaustive checks to validate its correctly rounded binary32 functions.
- **Once the worst case is known.** A library evaluates $f$ with a fast step accurate to a little more than $p$ bits. It tests whether the result is safely away from a breakpoint, and otherwise uses a slow step accurate to $p + k^{\ast} + 1$ bits. Since $k^{\ast}$ is known, the slow step is guaranteed to succeed. CRlibm uses this design, and [correctly rounded elementary functions](/correctly-rounded-elementary-functions/) in general follow it.

## Bounds

1. **Termination for transcendental functions (proved, by classical theorems).** By the Lindemann-Weierstrass theorem, $e^{x}$ is transcendental for every algebraic $x \ne 0$. Every float is rational, so $\exp(x)$ is irrational and is never a breakpoint for $x \ne 0$. The same holds for $\log x$ with $x \ne 1$, and for $\sin x$ and $\cos x$ with $x \ne 0$. So Ziv's strategy terminates on all inputs except the listed exact cases.
2. **Square root (proved here).** Let $x \in [1, 4)$ be a float with precision $p$, so $x = X 2^{1-p}$ for an integer $X$. A midpoint in $[1, 2)$ has the form $m = (2M + 1)2^{-p}$. Then $x - m^2 = \bigl(X 2^{p+1} - (2M + 1)^2\bigr) / 2^{2p}$, and the numerator is odd, so it is not 0. Hence $|x - m^2| \ge 2^{-2p}$, and $|\sqrt{x} - m| = |x - m^2|/(\sqrt{x} + m) > 2^{-2p}/4 = 2^{-2p-2}$. So $\sqrt{x}$ is never a midpoint, and an absolute accuracy of $2^{-2p-2}$ always suffices. Similar arguments cover directed rounding, where exact squares are the exact cases, and the reciprocal and division. Lang and Muller (2001) give such bounds for many algebraic functions, all of about $2p$ bits.
3. **Probabilistic estimate (heuristic, not proved).** Model the bits after the rounding position as independent fair coin flips. Then $\Pr[k(x) \ge k] = 2^{1-k}$ for one input, and among $N$ inputs the largest $k$ is about $\log_2 N + 1$. For a function on $n_e$ binades of binary64, $N \approx n_e 2^{52}$, which predicts $k^{\ast} \approx 53 + \log_2 n_e$. So the needed accuracy is about $2p + \log_2 n_e$ bits, a little more than 2p. Our binary16 table agrees with this estimate, with $k^{\ast}$ about $\log_2 N + 1$ to $\log_2 N + 2.3$. Muller (2016, Chapter 12) reports that the published binary64 worst cases also agree with it.
4. **Provable bounds from transcendence theory.** Effective versions of the Lindemann-Weierstrass theorem, such as the bounds of Nesterenko and Waldschmidt, give a provable precision that always suffices for $\exp$ and $\log$. For binary64 these bounds run to millions of bits, far beyond what is needed in practice. They show that the problem is finite, but they do not solve it in practice (Muller 2016, Chapter 12).
5. **The exact worst cases (computed).** For binary64 and the common univariate functions, the worst cases have been found by exhaustive search with Lefèvre's and the SLZ algorithms, and they are tabulated by Muller (2016, Chapter 12). In each case the measured $k^{\ast}$ is close to the probabilistic estimate.

## Reductions

- **From correct rounding to the worst-case search.** If the worst case $k^{\ast}$ of $f$ is known, correctly rounded evaluation of $f$ reduces to evaluating $f$ with relative error about $2^{-(p + k^{\ast} + 1)}$ and rounding the result. That is a fixed-precision approximation problem with no dilemma.
- **From the worst-case search to Diophantine approximation.** On a short interval, $f(x_0 + t\,\mathrm{ulp}) \approx P(t)$ for a polynomial $P$. Inputs near a breakpoint are integers $t$ with $2^{s}P(t)$ close to a half-integer. For $\deg P = 1$ this is inhomogeneous Diophantine approximation, solved with [continued fractions](/continued-fraction/). For higher degree it is a small-roots problem for a modular polynomial, solved with Coppersmith's method.
- **Relation to argument reduction.** Finding the floats closest to multiples of $\pi/2$, which bounds the accuracy that [Payne-Hanek reduction](/payne-hanek-argument-reduction/) needs, is the same kind of question. Kahan solved it with continued fractions of $\pi/2$.
- **Relation to double rounding.** Computing in a wider format and then rounding to a narrower one is correct unless the wider result lies on a narrower breakpoint. That is a table-maker's dilemma with $k^{\ast}$ bounded by the extra width, which is why [double rounding](/double-rounding/) can go wrong.

## Applications

- **Correctly rounded libraries.** CRlibm, the CORE-MATH project and the correctly rounded functions recommended by IEEE 754-2019 (Clause 9.2) all rely on known worst cases or on Ziv's strategy.
- **Reproducibility.** Correctly rounded functions give the same results on every platform. That supports portable and reproducible numerical software, and it lets compilers evaluate constant expressions with the same answers as the run-time library.
- **Testing libraries.** Lists of worst cases are the inputs most likely to expose a library that claims correct rounding but has a slightly too inaccurate slow path.
- **Hardware design.** The bounds for algebraic functions show that division and square root units need only a fixed number of extra bits, or a final remainder check, to be correctly rounded.

## References
