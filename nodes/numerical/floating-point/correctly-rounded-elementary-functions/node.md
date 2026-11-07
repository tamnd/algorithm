---
tag: 6JQ4DP
kind: problem
slug: correctly-rounded-elementary-functions
name: Correctly rounded elementary functions
aliases:
- CR-LIBM problem
- correct rounding of elementary functions
- correctly rounded libm
area: numerical/floating-point
level: research
summary: Evaluate exp, log, sin and similar functions with a single correctly rounded result.
prereqs: [correctly-rounded-functions, floating-point-arithmetic, ulp, rounding-modes]
see_also: [table-maker-dilemma, cody-waite-range-reduction, payne-hanek-argument-reduction, double-double-arithmetic, minimax-approximation, interval-arithmetic, ieee-754, arbitrary-precision-arithmetic]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 9.2 (recommended correctly rounded operations such as exp, log, sin, pow and their exceptions)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 10, Evaluating Floating-Point Elementary Functions (range reduction, polynomial approximation, the table maker's dilemma, exact cases and worst cases)
  - book: isbn:9781489979810
    title: Jean-Michel Muller, Elementary Functions, Algorithms and Implementation, third edition, Birkhauser, 2016
    locator: the chapters on range reduction and on final rounding (the table maker's dilemma, Ziv's strategy, worst cases)
  - paper: "Abraham Ziv, Fast evaluation of elementary mathematical functions with correctly rounded last bit, ACM Transactions on Mathematical Software 17(3) (1991), 410-423"
    title: Abraham Ziv, Fast evaluation of elementary mathematical functions with correctly rounded last bit (1991)
    locator: the strategy of evaluating with increasing precision until the rounding test succeeds
  - paper: "Vincent Lefevre and Jean-Michel Muller, Worst cases for correct rounding of the elementary functions in double precision, Proceedings of the 15th IEEE Symposium on Computer Arithmetic (ARITH 15), 2001, 111-118"
    title: Vincent Lefevre and Jean-Michel Muller, Worst cases for correct rounding of the elementary functions in double precision (2001)
    locator: the search algorithm based on linear approximations and the hardest-to-round binary64 inputs it found
  - paper: "Damien Stehle, Vincent Lefevre and Paul Zimmermann, Searching worst cases of a one-variable function using lattice reduction, IEEE Transactions on Computers 54(3) (2005), 340-346"
    title: Stehle, Lefevre and Zimmermann, Searching worst cases of a one-variable function using lattice reduction (2005)
    locator: the SLZ algorithm, which uses higher-degree approximations and Coppersmith's method
  - paper: doi:10.1145/1236463.1236468
    title: Laurent Fousse, Guillaume Hanrot, Vincent Lefevre, Patrick Pelissier and Paul Zimmermann, MPFR, a multiple-precision binary floating-point library with correct rounding, ACM Transactions on Mathematical Software 33(2) (2007)
    locator: correct rounding at arbitrary precision by Ziv loops with proved error bounds
  - paper: doi:10.1145/3747840
    title: "Nicolas Brisebarre, Guillaume Hanrot, Jean-Michel Muller and Paul Zimmermann, Correctly rounded evaluation of a function: why, how, and at what cost?, ACM Computing Surveys (2025)"
    locator: a survey of the problem, the methods (Ziv's strategy, worst-case searches, RLIBM) and the libraries (CRlibm, CORE-MATH)
---

The correctly rounded elementary functions problem asks for an implementation of $\exp$, $\log$, $\sin$, $\mathrm{pow}$ and the other functions of the C mathematical library that returns, for every floating-point input, the exact value rounded once, as IEEE 754 requires of the basic operations. The difficulty is that the exact value is transcendental and can lie extremely close to a rounding boundary, so the required working precision depends on the hardest input, which is the [table-maker's dilemma](/table-maker-dilemma/). It is solved in practice for binary32 and binary64 by fast approximations, a rounding test and a slower accurate fallback whose precision is justified by exhaustive searches for the worst cases.

## In plain words

A computer can store only some numbers, so the answer to a calculation such as the exponential of a number usually falls between two stored numbers. The ideal answer is the stored number nearest to the true value. Addition and multiplication always give that answer on modern hardware. Library functions for exponentials, logarithms and sines usually do, but now and then they return the neighbor instead.

The reason is that the true value can sit almost exactly halfway between two stored numbers. To see which side it is on, the library must compute many more digits than usual, and it does not know in advance how many. The problem is to always get it right while staying fast. The answer is to compute a little more than needed, check whether that is enough, and only for the rare hard inputs compute much more.

## Definition

**Notation.** A binary floating-point system $\mathbb{F}$ with precision $p$ ($p = 53$ for binary64, $p = 24$ for binary32), $\circ$ the rounding function of the current [rounding mode](/rounding-modes/), $u = 2^{-p}$ the unit roundoff for round to nearest, and $\mathrm{ulp}(y)$ as in Muller et al., Section 2.3.2 (the spacing of the floats in the binade of $y$, with $\mathrm{ulp}(y) = 2^{e_{\min} - p + 1}$ below the normal range). See [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**Input.** A function $f$ from a fixed list (in IEEE 754-2019 Clause 9.2, among others: $\exp$, $\exp_2$, $\exp_{10}$, $\mathrm{expm1}$, $\log$, $\log_2$, $\log_{10}$, $\mathrm{log1p}$, $\sin$, $\cos$, $\tan$, their inverses, the hyperbolic functions and their inverses, $\mathrm{pow}$, $\mathrm{hypot}$, $\mathrm{atan2}$), a format $\mathbb{F}$, a rounding mode, and an input $x \in \mathbb{F}$ (two inputs for $\mathrm{pow}$, $\mathrm{hypot}$ and $\mathrm{atan2}$).

**Output.** $\circ(f(x))$, the exact real $f(x)$ rounded once, together with the exceptions a correctly rounded operation signals: overflow when $|f(x)|$ exceeds the overflow threshold of the format, underflow when the result is tiny and inexact, inexact whenever $f(x) \notin \mathbb{F}$, and invalid with a NaN outside the domain.

**Rounding boundaries.** Let $B$ be the set of reals at which $\circ$ changes value: the midpoints between consecutive floats for round to nearest, and the floats themselves for the directed modes. Two reals in the same open interval between consecutive points of $B$ have the same rounding.

**Hardness.** The hardness of an input is $d(x) = \mathrm{dist}(f(x), B)/\mathrm{ulp}(f(x))$, the distance from $f(x)$ to the nearest boundary in ulps. An input is hard to round when $d(x)$ is small.

**Rounding test (proved).** If $y$ satisfies $|y - f(x)| \le \eta$ and the closed interval $[y - \eta, y + \eta]$ contains no point of $B$, then $\circ(y) = \circ(f(x))$, because $f(x)$ and $y$ lie in the same open interval between boundaries. Conversely, any $y$ with $|y - f(x)| < d(x)\,\mathrm{ulp}(f(x))$ rounds correctly, so a relative accuracy of about $2^{-p}\,d_{\min}$, with $d_{\min}$ the minimum of $d$ over all nonexact inputs, decides every case. The assumption is only that $\eta$ is a proved bound; no rounding mode or FMA assumption enters.

## Variants

- **By format.** Binary32 has $2^{32}$ inputs and can be checked exhaustively; binary64 cannot, and needs worst-case searches; binary16, bfloat16 and the 8-bit formats are small enough to tabulate. Decimal formats have the same problem with decimal midpoints.
- **By rounding mode.** Round to nearest, with ties to even or to away, needs the distance to midpoints; the directed modes need the distance to floats. A library may support only round to nearest.
- **One input or two.** Univariate functions have at most $2^{64}$ inputs in binary64; $\mathrm{pow}(x, y)$ has $2^{128}$, so its worst cases are known only on subdomains, and its proofs rely on other arguments.
- **Correct rounding versus faithful rounding.** A weaker goal returns one of the two floats that bracket $f(x)$. This needs no knowledge of hard cases, since an error below $1$ ulp minus the final rounding error suffices; most system libraries aim at errors near $0.5$ ulp without proof.
- **Several formats at once.** One implementation that returns the correctly rounded result for every format up to 32 bits and every rounding mode, as in the RLIBM project of Lim and Nagarakatte.
- **Arbitrary precision.** The precision $p$ is an input, as in MPFR; worst cases cannot be tabulated, and only Ziv's strategy applies.

## Examples

The examples were run with Python 3.14 on macOS 15, whose `math.exp` calls the system math library. References were computed with `decimal` at $60$ significant digits and rounded with `fractions.Fraction`; at that precision a rounding is decided whenever $d(x)$ exceeds about $2^{-140}$, which holds for every case shown.

**A hard case near 1.** For $x = 2^{-53}$ in binary64, the Taylor series gives $e^{x} = 1 + 2^{-53} + 2^{-107} + \dots$. The midpoint between $1$ and its successor $1 + 2^{-52}$ is $1 + 2^{-53}$, and $e^{x}$ is above it by about $2^{-107}$, which is $2^{-55}$ ulp. So $\circ(e^{x}) = 1 + 2^{-52}$ = 0x1.0000000000001p+0 in round to nearest, and an approximation must have a relative accuracy better than about $2^{-107}$ to see it. The system library returned 0x1.0000000000000p+0, the wrong neighbor. For every float $0 < x < 2^{-53}$ the correct result is $1$, so libraries treat tiny arguments with a direct Taylor test.

**How often a cheap test fails.** For $20000$ random $x$ uniform in $[-700, 700]$, the fraction of inputs with $d(x) < 2^{-10}$ was $0.21\%$ and with $d(x) < 2^{-15}$ was $0.01\%$, against $2^{-9} \approx 0.20\%$ and $2^{-14} \approx 0.006\%$ predicted by a uniform distribution of $d$ on $[0, \tfrac12]$. The hardest of the sample, $x$ = 0x1.469137281c77cp+8, had $d(x) \approx 2.2 \times 10^{-5} \approx 2^{-15.5}$. So a first approximation with an error of $2^{-10}$ ulp decides about $99.8\%$ of the inputs.

**An exhaustive binary32 range.** Over all $2^{17}$ binary32 inputs in $[1, 1 + 2^{-6})$, the hardest for $\exp$ is $x$ = 0x1.012e3cp+0, with $d(x) \approx 2.17 \times 10^{-6} \approx 2^{-18.8}$ and $\circ(e^{x})$ = 0x1.5d8c62p+1. The heuristic below predicts a minimum near $1/(2 \cdot 2^{17}) = 2^{-18}$. Since $2^{-18.8}$ is far above the $2^{-28}$ that a binary64 result with error below $1$ binary64 ulp can blur, rounding the binary64 `math.exp` to binary32 is correct on this range, and the check confirmed it for all $131072$ inputs (assuming the library error stays below $1$ binary64 ulp, which is observed, not proved).

**An exact midpoint.** For $\mathrm{pow}(x, 2)$ with $x = 1 - 2^{-27}$ = 0x1.ffffffcp-1, the exact square $1 - 2^{-26} + 2^{-54}$ is a $54$-bit number and lies exactly halfway between the floats $1 - 2^{-26}$ and $1 - 2^{-26} + 2^{-53}$. No precision decides this case; it must be recognized as exact, and ties to even gives 0x1.ffffff8p-1. By contrast $\exp$, $\log$, $\sin$ and $\cos$ have no such inputs apart from trivial ones (see Bounds).

## Known algorithms

- **Ziv's strategy (1991).** Compute $y_1$ with a proved error bound $\eta_1$ in a precision a little above $p$, for example with [double-double arithmetic](/double-double-arithmetic/) or with a fused multiply-add based polynomial; apply the rounding test; if it fails, recompute with a smaller $\eta_2$, and so on. With a first step of $k$ extra digits the expected cost is the cost of the first step plus about $2^{1-k}$ times the cost of the later ones, under the uniform model. Without a known worst case there is no proved bound on the number of steps, only termination for functions without exact boundary cases.
- **Two phases with a known worst case.** CRlibm (Daramy-Loirat, de Dinechin, Defour, Lauter, Muller and others, 2000s) and CORE-MATH (Sibidanov, Zimmermann and others, since 2022) use a quick phase and one accurate phase whose precision, often triple-double, is chosen from the known $d_{\min}$, so the worst-case time is bounded and each phase comes with a proof of its error bound.
- **Range reduction and approximation.** Both phases reduce the argument, by [Cody-Waite](/cody-waite-range-reduction/) for moderate arguments or [Payne-Hanek](/payne-hanek-argument-reduction/) for huge ones in the trigonometric functions, look up tables, and evaluate a [minimax](/minimax-approximation/) polynomial; the error analysis must cover the reduction, the table entries, the polynomial and the reconstruction.
- **Worst-case search by linear approximation.** Lefèvre's algorithm splits the inputs of a binade into intervals on which $f$ is replaced by a degree $1$ polynomial; finding inputs whose image is near a boundary becomes finding integer points close to a line, solved with a continued-fraction method in the style of the three-distance theorem. Lefèvre and Muller (2001) used it to find the binary64 worst cases of $\exp$, $\log$ and related functions on large domains.
- **Worst-case search by lattice reduction (SLZ).** Stehlé, Lefèvre and Zimmermann (2003, 2005) use higher-degree approximations and Coppersmith's method with the [LLL algorithm](/lll-algorithm/) to find the small solutions, with a lower asymptotic cost for large $p$.
- **Exhaustive testing.** For binary32 and smaller formats, every input is evaluated against a multiple-precision reference such as MPFR; this both finds the worst cases and verifies an implementation.
- **Rounding intervals and linear programming (RLIBM).** For each input of a small format, compute the interval of reals that round to the correct result, and fit one polynomial whose values lie in all intervals by [linear programming](/linear-programming-problem/). Using intervals of round to odd in a format two digits wider gives correct results for all smaller formats and all modes.

## Bounds

- **Existence of a finite precision (proved).** By the Hermite-Lindemann theorem, $e^{a}$ is transcendental for every nonzero algebraic $a$. Floats and midpoints are rational, so $\exp(x)$ is never a boundary for a float $x \ne 0$; likewise $\log(x)$ for $x \ne 1$ and $\sin x$, $\cos x$ for $x \ne 0$. Since there are finitely many inputs, $d_{\min} > 0$ and a finite precision suffices. The theorem gives no useful value of $d_{\min}$.
- **Explicit bounds from transcendence measures (proved, unusable).** Results such as those of Nesterenko and Waldschmidt (1996) bound how close $e^{a}$ can be to a rational of given size, giving an explicit precision for each format, but far larger than needed in practice; Muller's books discuss them.
- **Probabilistic estimate (heuristic, not proved).** If $d(x)$ behaved like a uniform variable on $[0, \tfrac12]$ for $N$ inputs, the expected minimum would be about $1/(2N)$ ulp. With $N \approx 2^{p}$ times the number of binades of the domain, a precision of about $2p + \log_2(\text{number of binades})$ digits decides every case. The binary32 range above matches this ($2^{-18.8}$ against $2^{-18}$), and the published binary64 worst cases of Lefèvre and Muller are reported to be consistent with it.
- **Worst cases found (observed).** For binary64, the published worst cases of the univariate functions on their main domains require roughly $2p$ plus a few tens of digits, a little above $100$ binary digits; the exact figures are in Lefèvre and Muller (2001) and in Muller's books. Tiny arguments, where a Taylor expansion such as $e^{x} = 1 + x + \dots$ decides the rounding directly, are excluded from the searches.
- **Cost.** The quick phase costs about the same as a faithful implementation. CORE-MATH and CRlibm report average times within a small factor of the system libraries; the slow phase runs on a fraction of about $2^{1-k}$ of the inputs for $k$ extra digits in the quick phase.

## Reductions

- **Correct rounding reduces to an error bound plus a worst case.** Given $d_{\min}$ for $f$ on $\mathbb{F}$, any approximation with a proved error below $d_{\min}\,\mathrm{ulp}(f(x))$ followed by one rounding is correctly rounded, by the rounding test. The research problem is therefore split into computing $d_{\min}$ (the [table-maker's dilemma](/table-maker-dilemma/)) and proving the error of an approximation.
- **All rounding modes reduce to one search.** The boundaries for round to nearest at precision $p$ and those for the directed modes at precision $p$ together form the floats of precision $p + 1$. A search for inputs whose image is close to a float of precision $p + 1$ covers every mode at once.
- **Round to odd in a wider format.** If $y$ is $f(x)$ rounded to odd in precision $p + 2$ or more, rounding $y$ to precision $p$ in any mode gives $\circ(f(x))$ (Boldo and Melquiond, 2008), which reduces many formats to one target.
- **Worst-case search reduces to Diophantine approximation.** After a degree $1$ approximation on a short interval, the search becomes finding integers $t$ for which $\alpha t + \beta$ is close to an integer, solved with [continued fractions](/continued-fraction/); with degree $d > 1$ it becomes finding small roots of a bivariate polynomial modulo $1$, solved with [Coppersmith's method](/coppersmith-method/).
- **Symmetries.** $\sin(-x) = -\sin x$ and $\cos(-x) = \cos x$ halve the search; $\exp_2$ and $\log_2$ at powers of two are exact; such identities restrict which inputs need the full treatment.

## Applications

- **Reproducibility.** Correctly rounded functions return the same bits on every platform, so simulations, distributed computations and consensus systems can agree bit for bit; this is the main argument of the survey of Brisebarre, Hanrot, Muller and Zimmermann.
- **Standards.** IEEE 754-2019 Clause 9.2 recommends correctly rounded versions of the functions, and C23 reserves names with the prefix `cr_` for them; some C libraries have adopted CORE-MATH code for binary32 functions.
- **Interval arithmetic.** With directed rounding, a correctly rounded function gives the tightest enclosure in [interval arithmetic](/interval-arithmetic/).
- **Testing and verification.** MPFR and other correctly rounded implementations are the reference against which the ulp errors of fast libraries are measured, and they make proofs about numerical programs independent of the library.
- **Properties for free.** Monotonicity, symmetry, exact values such as $\exp(0) = 1$, and the bound $|\delta| \le u$ of the [standard model](/floating-point-model/) all hold automatically; see [correctly rounded functions](/correctly-rounded-functions/).

## References
