---
tag: WKGNRC
kind: technique
slug: interval-arithmetic
name: Interval arithmetic
aliases:
- interval analysis
- verified computing
area: numerical/floating-point
level: advanced
summary: Computes guaranteed bounds by propagating intervals through operations with directed rounding.
prereqs: [rounding-modes, rounding-error-analysis, floating-point-arithmetic]
see_also: [forward-error-analysis, condition-number, catastrophic-cancellation, newton-raphson-method, bisection-method, interval-branch-and-bound, automatic-differentiation, global-optimization]
sources:
  - book: isbn:9780898716696
    title: Ramon E. Moore, R. Baker Kearfott and Michael J. Cloud, Introduction to Interval Analysis, SIAM, 2009
    locator: Chapters 2 to 6 (interval arithmetic, the fundamental theorem of inclusion, interval extensions, the dependency problem, the interval Newton method)
  - paper: doi:10.1017/S096249291000005X
    title: Siegfried M. Rump, Verification methods, rigorous results using floating-point arithmetic, Acta Numerica 19 (2010), 287-449
    locator: the sections on interval arithmetic with directed rounding, overestimation, and verified solution of nonlinear systems
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 26.4, interval analysis
  - url: https://doi.org/10.1109/IEEESTD.2015.7140721
    title: IEEE Std 1788-2015, IEEE Standard for Interval Arithmetic
    locator: the set-based interval model, the required operations and their enclosure requirements
  - url: https://ieeexplore.ieee.org/document/8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 4.3.2, directed rounding attributes roundTowardPositive and roundTowardNegative
  - paper: doi:10.1007/s002080010018
    title: Warwick Tucker, A rigorous ODE solver and Smale's 14th problem, Foundations of Computational Mathematics 2 (2002), 53-117
    locator: the interval-based computer-assisted proof that the Lorenz attractor exists
---

Interval arithmetic replaces each number by an interval $[\underline x, \overline x]$ known to contain it, and each operation by one whose result contains every possible result of the operation on members of its operands. Computing the lower ends with rounding toward $-\infty$ and the upper ends with rounding toward $+\infty$ makes the enclosure hold in floating point too, so the final interval is a proof that the true answer lies inside, whatever the rounding errors and the data uncertainty were. The price is overestimation: intervals can grow much wider than the true range, most of all when a variable occurs more than once in a formula.

## In plain words

Instead of computing with a single number that is probably slightly wrong, compute with a lower bound and an upper bound that are certainly right. To add two ranges, add the lows and add the highs. To multiply, try the four combinations of ends and keep the smallest and largest.

Every time a computer rounds, round the low end down and the high end up, so the true value can never escape. At the end you get a range that is guaranteed to contain the exact answer. If the range is narrow, you have a proof of an accurate result. If it is wide, either the problem is sensitive or the formula needs rearranging.

## When it applies

- The result must be **certain**, not just probably accurate: computer-assisted proofs, safety bounds, verified roots and optima.
- The inputs are **uncertain** within known bounds (measurements, tolerances), and the output range is wanted.
- One wants an **automatic error bound** for a floating-point computation without a hand [rounding error analysis](/rounding-error-analysis/).
- A search must **exclude regions** rigorously, as in [interval branch-and-bound](/interval-branch-and-bound/) [global optimization](/global-optimization/) and root isolation: if $0 \notin F(X)$, then $f$ has no zero in $X$.

It does not apply well to long iterations where every variable depends on every other, such as naive Gaussian elimination on intervals, where widths grow exponentially with the dimension.

## The template

An interval is $X = [\underline x, \overline x]$ with $\underline x \le \overline x$. Write $\nabla$ and $\Delta$ for rounding toward $-\infty$ and $+\infty$ (IEEE 754-2019, Clause 4.3.2). The basic operations are

$$X + Y = [\nabla(\underline x + \underline y),\ \Delta(\overline x + \overline y)], \qquad X - Y = [\nabla(\underline x - \overline y),\ \Delta(\overline x - \underline y)],$$

$$X \cdot Y = [\nabla \min S,\ \Delta \max S], \quad S = \{\underline x\underline y, \underline x\overline y, \overline x\underline y, \overline x\overline y\},$$

$$X / Y = X \cdot [1/\overline y, 1/\underline y] \text{ with outward rounding, when } 0 \notin Y.$$

Monotone functions map ends to ends ($\exp X = [\nabla \exp \underline x, \Delta \exp \overline x]$), and others such as $\sin$ or $x^2$ use their known extremes. Then:

1. Replace each input by an enclosing interval; a decimal constant such as $0.1$ becomes $[0.09999999999999999, 0.1]$, the two binary64 neighbours of $1/10$.
2. Evaluate the formula with interval operations. This is the **natural interval extension** $F$ of $f$.
3. Read off the result. By the **fundamental theorem of interval arithmetic** (Moore), if every operation is inclusion isotone, then $\{f(x) : x \in X\} \subseteq F(X)$ for every box $X$ on which $F$ is defined. The proof is induction on the expression: each operation's result contains every result on members of its operands, and outward rounding only enlarges it.
4. If the result is too wide, reduce dependency (rewrite so each variable occurs once), use a centred form, or split $X$ into pieces and take the union.

What is proved: the enclosure, for any finite expression, assuming the elementary functions used are themselves enclosed correctly. What is not: any bound on how much $F(X)$ overestimates the true range, beyond the first-order results below.

## Classic examples

- **The dependency problem.** On $X = [1, 2]$, $X - X = [-1, 1]$, not $\{0\}$: interval arithmetic does not know the two operands are the same number. On $X = [0, 1]$, $x(1 - x)$ evaluates to $[0, 1]$ and the algebraically equal $x - x^2$ to $[-1, 1]$, while the true range is $[0, 1/4]$.
- **A sum with rounding.** Adding $0.1$ ten times in binary64 gives $1.0$. The interval version, started from $[0.09999999999999999, 0.1]$ and widened by one ulp outward per operation, returns an interval of width about $1.7 \times 10^{-15}$ that contains $1$. It encloses both the exact sum of ten tenths and the exact sum of ten copies of the binary64 number nearest $0.1$.
- **Rump's example.** $f(a, b) = 333.75 b^6 + a^2(11a^2b^2 - b^6 - 121b^4 - 2) + 5.5b^8 + a/(2b)$ at $a = 77617$, $b = 33096$ is about $-0.8274$, but binary64 evaluation returns $-1.1805916207174113 \times 10^{21}$. Interval evaluation in binary64 returns an enclosure about $7 \times 10^{22}$ wide: useless as an answer, but honest. It shows that the floating-point result cannot be trusted, which the single number did not. (Values computed with the one-ulp outward emulation described under Pitfalls, and checked in exact rationals.)
- **Interval Newton.** For $f(x) = x^2 - 2$ on $X_0 = [1, 2]$, iterate $N(X) = m - f(m)/F'(X)$, $X_{k+1} = X_k \cap N(X_k)$ with $m$ the midpoint. The widths are $0.0625$, $3.6 \times 10^{-4}$, $6.7 \times 10^{-9}$ and $8.9 \times 10^{-16}$ after four steps: quadratic convergence to an enclosure of $\sqrt 2$ a few ulps wide. If $N(X) \subseteq X$, a zero in $X$ is proved to exist and to be unique; if $X \cap N(X) = \emptyset$, there is none.
- **Computer-assisted proofs.** Interval bounds certified the inequalities in Hales's proof of the Kepler conjecture, and Tucker's 2002 proof that the Lorenz equations have a strange attractor (Smale's 14th problem) used a rigorous interval ODE solver.

## Variations

- **Centred and mean-value forms.** $F(X) = f(m) + F'(X)(X - m)$ overestimates the range by $O(w^2)$ for width $w$, against $O(w)$ for the natural extension; combine with [automatic differentiation](/automatic-differentiation/) to get $F'$.
- **Subdivision.** Splitting $X$ into $k$ pieces cuts the overestimation of the natural extension by about a factor $k$; it is the core of interval branch-and-bound.
- **Affine arithmetic and Taylor models.** Track linear (or polynomial) dependence on the inputs symbolically, with an interval remainder, which removes most of the dependency problem.
- **Midpoint-radius form.** Represent $\langle m, r \rangle$; Rump's INTLAB uses it for fast verified linear algebra with rounding-mode switches around whole BLAS calls.
- **Extended and set-based intervals.** IEEE 1788-2015 standardizes intervals as sets, including unbounded ones and division by intervals containing 0 (giving a union of two half-lines), with decorations that record whether a function was defined and continuous on the input.
- **Verified linear systems.** Krawczyk's operator and Rump's method enclose the solution of $Ax = b$ by an a posteriori residual argument instead of interval Gaussian elimination.

## Pitfalls

- **Rounding modes.** Changing the hardware rounding mode can be slow, compilers may reorder or constant-fold across mode changes, and many math libraries are not correct in directed modes. A portable fallback is to round to nearest and then step one ulp outward with `nextafter`, which is valid because a rounded-to-nearest result is within one ulp of the exact one; it costs a little width. The examples above use this fallback.
- **Dependency.** Each occurrence of a variable is treated independently. Rewrite to use each variable once where possible: $x(1-x)$ is better than $x - x^2$, and $1/4 - (x - 1/2)^2$, with a single occurrence and an interval square, gives the exact range $[0, 1/4]$.
- **Wrapping in iterations.** Iterating an interval map, such as an ODE step or a matrix power, can grow widths exponentially even when the true set stays small; this is the wrapping effect, and it needs coordinate changes or Taylor models.
- **Elementary functions.** The enclosure is only as good as the enclosures of $\exp$, $\sin$ and the rest. A library function that is merely accurate, not correctly rounded or bounded, must be widened by its documented error.
- **Input conversion.** Writing `0.1` in source code gives the rounded binary64 number, not an enclosure of $1/10$; inputs must be enclosed at conversion time.
- **Division by intervals containing zero.** Plain interval arithmetic must stop or return the whole line; the set-based extension returns two pieces, which complicates code.

## Exercises

1. Prove the multiplication rule: for $X = [\underline x, \overline x]$ and $Y = [\underline y, \overline y]$, $\{xy : x \in X, y \in Y\} = [\min S, \max S]$. Then list the nine sign cases that let an implementation use only two multiplications in most of them.
2. Show that interval addition and multiplication are associative and commutative, that $X(Y + Z) \subseteq XY + XZ$ (subdistributivity), and find intervals for which the inclusion is strict.
3. For $f(x) = x(1-x)$ on $X = [0, 1]$, compute the natural extension, the mean-value form centred at $1/2$, and the natural extension after splitting $X$ into $k$ equal pieces. How fast does each approach the true range $[0, 1/4]$?
4. Prove that if $N(X) \subseteq X$ for the interval Newton operator and $0 \notin F'(X)$, then $f$ has exactly one zero in $X$.
5. Explain why rounding to nearest followed by one `nextafter` step outward always gives a valid enclosure of an exact sum or product, and when it gives the same interval as directed rounding.

## References
