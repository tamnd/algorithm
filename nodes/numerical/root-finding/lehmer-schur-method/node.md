---
tag: GXZ3FQ
kind: algorithm
slug: lehmer-schur-method
name: Lehmer-Schur method
aliases:
- Lehmer-Schur algorithm
- Lehmer's method
- Lehmer's disc method
area: numerical/root-finding
level: research
summary: Bisection in the plane for polynomial zeros. Keep a disc known to hold a zero and test its half-radius disc and eight covering discs exactly; each pass cuts the radius to at most 33/64.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: the degree, B: "the starting radius, a power of 2 above the Cauchy bound", δ: the target radius}
  time: {worst: "O(n^2 log(B/δ))"}
  space: {extra: "O(n)"}
  evaluations: {per_step: "9", worst: "45 log(B/δ)/log(64/33)"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: true, local: false}
history:
  year: 1961
  people: [D. H. Lehmer]
  note: Lehmer described the method in 1961 as a machine method for polynomial equations, using the Schur-Cohn test to decide whether a disc contains a zero.
prereqs: [schur-cohn-test, bisection-method, cauchy-root-bound]
see_also: [schur-cohn-test, bisection-method, polynomial-root-finding, real-root-counting, laguerre-method, muller-method, cauchy-root-bound, polynomial-deflation]
sources:
  - paper: doi:10.1145/321062.321064
    title: "D. H. Lehmer, A machine method for solving polynomial equations, Journal of the ACM 8 (1961) 151-162"
    locator: the disc search, the covering of the annulus by eight discs and the Schur-Cohn decision
  - book: "P. Henrici, Applied and Computational Complex Analysis, Volume 1, Wiley, 1974"
    locator: Chapter 6, Polynomials (the Schur-Cohn algorithm and the method of Lehmer)
  - book: "M. Marden, Geometry of Polynomials, second edition, Mathematical Surveys 3, American Mathematical Society, 1966"
    locator: Chapter X, the Schur-Cohn criterion for the number of zeros in a circle
  - paper: doi:10.1137/S0036144595288554
    title: "V. Y. Pan, Solving a polynomial equation: some history and recent progress, SIAM Review 39 (1997) 187-220"
    locator: the sections on subdivision methods (Weyl's quadtree and Lehmer's method) and their complexity
---

The Lehmer-Schur method locates a zero of a complex polynomial $p$ the way [bisection](/bisection-method/) locates a real root, but in the plane, with discs instead of intervals and with a zero-counting test instead of a sign test. It keeps a disc $D(c, r)$ that is known to contain a zero. In each pass it asks the [Schur-Cohn test](/schur-cohn-test/) whether the disc of half the radius contains a zero; if so, that disc becomes the new one. If not, every zero of the old disc lies in an annulus, which is covered by eight smaller discs, and the first of them that contains a zero becomes the new disc. The radius shrinks by a fixed factor in each pass, so the method converges linearly from any start, for every polynomial, to a disc of any prescribed radius, and with exact arithmetic the final disc is certified to contain a zero. D. H. Lehmer proposed it in 1961.

## In plain words

Draw a large circle that surely contains a root, for example from a bound on the size of the roots. Ask an exact test whether the circle of half the size around the same centre contains a root. If it does, move to it. If it does not, the root lies in the ring between the two circles, so place eight smaller circles around the ring that together cover it, and ask each whether it contains a root; move to the first one that does. Every move makes the circle at least about half as big, so after forty moves the circle is a trillion times smaller.

## The problem

Given a complex polynomial $p(z) = a_n z^n + \cdots + a_0$ with $a_n \ne 0$ and $n \ge 1$, and a radius $\delta > 0$, find a centre $c$ and a radius $r \le \delta$ such that the open disc $D(c, r)$ contains at least one zero of $p$, and report how many zeros it contains.

Notation on the root-finding pages: $D(c, r) = \{z : |z - c| < r\}$; $\operatorname{COUNT}(p, c, r)$ is the number of zeros of $p$ in $D(c, r)$ given by the Schur-Cohn test, which may be "singular"; $\rho = \frac{13}{16}$ and $\beta = \frac{7}{16}$ are the distance and the radius of the covering discs, in units of $r$; $\omega_0, \ldots, \omega_7$ are the eight directions at angles $k\pi/4$, with $\frac{\sqrt2}{2}$ replaced by $\frac{181}{256}$ so that all centres are dyadic; the cost is counted in Schur-Cohn tests.

## The algorithm

```pseudo id=main
LEHMER-SCHUR(p, δ, kmax)
L1  if deg p = 0 then return "no roots"; B ← least power of 2 with B ≥ 1 + max_i |a_i/a_n|; (c, r) ← (0, B)
L2  for k ← 1 to kmax do
L3      if r ≤ δ then return (c, r, count, "converged")
L4      (m, r') ← COUNT(p, c, r/2)            ▷ COUNT retries with radius factors 33/32, 31/32, 65/64, 63/64 when singular
        if m is singular then return "singular"; if m ≥ 1 then (r, count) ← (r', m); continue
L5      for j ← 0 to 7 do                     ▷ no zero in D(c, r'), so the zeros of D(c, r) lie in r' ≤ |z − c| < r
L6          c_j ← c + ρ r ω_j; (m, r_j) ← COUNT(p, c_j, β r); if m ≥ 1 then (c, r, count) ← (c_j, r_j, m); break
L7      if no c_j was accepted then return "failure"
L8  return (c, r, count, "kmax reached")
```

Line L1 starts from a disc that contains every zero: by the [Cauchy bound](/cauchy-root-bound/), every zero satisfies $|z| < 1 + \max_i |a_i/a_n|$. The implementation bounds $|a_i/a_n|$ by the sum of the absolute values of its real and imaginary parts and rounds up to a power of 2. Line L3 is the stopping test. Line L4 is the inner test. A singular Schur-Cohn step, which happens when a zero lies on the test circle, is retried with a radius changed by $\frac{1}{32}$ or $\frac{1}{64}$, and the radius actually used is kept. Lines L5 and L6 test the eight covering discs in turn. Line L7 can only be reached when a covering test was singular for all five radii (proved). Every centre and radius is a dyadic rational, so each test is exact.

## Example

For $p(z) = z^5 - z - 1$, whose only real zero is $1.1673039782614187$, line L1 gives $B = 2$. The first inner test, on $D(0, 1)$, is singular, since $|a_0| = |a_5|$, and the retry with radius $\frac{33}{32}$ finds one zero. So $r = \frac{33}{32}$. The next inner test finds none, and the covering disc in the direction $\omega_0$, with centre $\frac{13}{16} \cdot \frac{33}{32}$ and radius $\frac{7}{16} \cdot \frac{33}{32} = \frac{231}{512}$, contains the zero. With $\delta = 2^{-40}$ the method stops after 39 passes and 80 Schur-Cohn tests with
$$c = 1.1673039782613113, \qquad r = 4.43 \times 10^{-13}, \qquad |c - x^*| = 1.07 \times 10^{-13},$$
and the final disc holds exactly one zero. Of the 38 radius ratios, 22 are $\frac12$ (inner tests) and the others are $\frac{7}{16}$ or the first $\frac{33}{64}$; their geometric mean is $0.474$. For $z^3 - z - 2$ ($B = 4$) the same tolerance takes 39 passes and 88 tests, ending at $1.5213797068049184$ with $r = 7.5 \times 10^{-13}$. For $(z - 1)^2$ the final disc reports 2 zeros: the method sees the multiplicity.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **Invariant (proved).** At the start of every pass, $D(c, r)$ contains at least one zero of $p$, and $\mathrm{count}$ is the exact number of zeros in it.
- **Covering (proved).** If $D(c, r)$ contains a zero and $D(c, r')$ with $r' \ge \frac{31}{64} r$ contains none, then that zero lies in one of the eight discs $D(c + \rho r\omega_j, \beta f r)$ for every factor $f \in [\frac{31}{32}, \frac{33}{32}]$.
- **Shrinking (proved).** Each pass multiplies $r$ by at most $\frac{33}{64}$. So the method returns "converged" after at most $\lceil \log(B/\delta)/\log(64/33) \rceil$ passes, unless a test is singular for all five radii.
- **Result (proved).** On "converged", $|c - z| < r \le \delta$ for some zero $z$, and the number of zeros in $D(c, r)$ is exactly $\mathrm{count}$.
- **Speed (observed).** The ratio per pass is $\frac12$ or about $\frac{7}{16}$, with a geometric mean near $0.47$ in the examples: linear convergence, of order 1.

## Complexity

The cost model is the number of Schur-Cohn tests, each of which costs $O(n^2)$ arithmetic operations on exact numbers (the Taylor shift to the disc and at most $n$ Schur transforms). The method never evaluates $p$ at a point.

- **Per pass.** One inner test, plus up to eight covering tests, each retried up to five times when singular. In the examples there were about 2.1 tests per pass.
- **Passes.** At most $\lceil \log(B/\delta)/\log(64/33) \rceil$, that is about $1.05 \log_2(B/\delta)$ passes; in practice about $\log_2(B/\delta)/1.08$.
- **Order and efficiency.** The convergence is linear, of order $q = 1$, so the efficiency index $q^{1/w}$ is 1 for every $w$, the same as bisection. The method trades speed for its global guarantee.
- **Arithmetic.** $O(n^2)$ operations per test, $O(n^2 \log(B/\delta))$ in all. The sizes of the exact numbers grow linearly with the number of passes, because the centres are dyadic with growing denominators.
- **Space.** $O(n)$ numbers.

### Floating point

The implementation uses exact rationals, so the inclusion tests are exact for the polynomial whose coefficients are the given numbers, and the stopping rule is a radius test that always ends: the radius shrinks geometrically, and $k_{\max}$ bounds the loop in any case. A floating point version would face the difficulties of the Schur-Cohn test in floating point: a test disc whose circle passes close to a zero gives tiny constant terms whose signs are unreliable, and the method could then follow a disc that contains no zero. Even with exact tests, rounded input data limit the meaning of the answer to the [conditioning](/root-conditioning/) of the zeros.

## Properties

- **Global.** It converges for every polynomial from the Cauchy disc; no starting guess is needed.
- **Certified.** In exact arithmetic the final disc provably contains exactly $\mathrm{count}$ zeros.
- **Derivative free and evaluation free.** Only coefficient arithmetic, through the shift and the Schur-Cohn test.
- **Bracketing in two dimensions.** The disc plays the role of the bracket of bisection.
- **Not sensitive to multiplicity.** Multiple and clustered zeros do not slow it down; the final count reports them.
- **Slow.** Linear convergence with ratio about $\frac12$ per pass and two or more tests per pass.

## Variants and improvements

- **Polishing.** Use the Lehmer-Schur method to reach a disc with one zero and well separated from the others, then switch to Newton's or [Laguerre's method](/laguerre-method/) for quadratic or cubic convergence.
- **All zeros.** Run it with [deflation](/polynomial-deflation/) in floating point, or, keeping certification, explore all covering discs that contain zeros, a tree search like Weyl's quadtree subdivision.
- **Other inclusion tests.** Weyl's method and its successors use squares and cheaper tests based on Turán's or Pellet's inequalities, with complexity analysed by Pan and others; Renegar and Pan used such subdivision in near-optimal algorithms.
- **Other coverings.** Lehmer's original covering of the annulus used eight discs as well; the constants here are chosen to be dyadic, and other choices give slightly different ratios.

## When to use it

Use it when a certified enclosure of a zero is needed regardless of the polynomial, when no good starting value is known, or as a robust first phase before a fast local method. For computing all zeros of a moderate degree polynomial quickly in floating point, eigenvalue methods, the Jenkins-Traub method or Aberth's iteration are better.

## Pitfalls

- **Singular tests.** A test circle through a zero makes the Schur-Cohn test singular; without the radius retries the method would stop.
- **Coverage must include margins.** The covering discs must cover the whole annulus even after the inner radius and their own radii are changed by the retries; the proof checks this for the constants used.
- **Growing numbers.** Exact arithmetic with nested dyadic centres slows down as the disc shrinks; stop at a modest radius and polish with a fast local method.
- **Floating point tests.** Rounding can change a count near the boundary of a disc, after which the "certified" disc may hold no zero.
- **Which zero.** The method finds some zero, not a prescribed one; the order of the eight directions decides which.

## Implementations

## History

D. H. Lehmer published the method in 1961 as a machine method for polynomial equations, building on the counting test of Schur (1917) and Cohn (1922); it is described in Henrici's *Applied and Computational Complex Analysis* (1974). Weyl had proposed a subdivision method based on exclusion tests in 1924. The approach became the template for later subdivision algorithms with complexity guarantees, surveyed by Pan (1997).

## References
