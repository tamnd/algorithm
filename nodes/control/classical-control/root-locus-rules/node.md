---
tag: V7FWWP
kind: algorithm
slug: root-locus-rules
name: Root locus construction rules
aliases:
- Evans rules
area: control/classical-control
level: core
summary: Computes the features that fix the shape of a root locus from the open-loop poles and zeros, the real axis segments, asymptotes, breakaway points, departure angles and axis crossings.
model: real-ram
complexity:
  vars: {n: the number of open-loop poles, m: the number of open-loop zeros, t: the number of iterations of the polynomial root finder}
  time: {worst: "O((n + m)^3 + t (n + m)^2)"}
  space: {extra: "O(n + m)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1948
  people: [Walter R. Evans]
  note: "Evans gave the angle and magnitude conditions and the rules for sketching the locus in 1948, and their use for the design of compensators in 1950."
prereqs: [root-locus, poles-and-zeros, polynomial-root-finding]
see_also: [root-locus, routh-hurwitz-criterion, routh-array, polynomial-root-finding, root-conditioning, gain-margin, lead-lag-compensator, ziegler-nichols-tuning]
sources:
  - paper: doi:10.1109/T-AIEE.1948.5059708
    title: W. R. Evans, Graphical analysis of control systems, Transactions of the American Institute of Electrical Engineers 67(1) (1948) 547-551
    locator: the whole paper (the angle and magnitude conditions and the rules for the graphical construction)
  - paper: doi:10.1109/T-AIEE.1950.5060121
    title: W. R. Evans, Control system synthesis by root locus method, Transactions of the American Institute of Electrical Engineers 69(1) (1950) 66-69
    locator: the whole paper (the use of the locus to choose the gain and the compensation)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 5, The Root-Locus Design Method (the guidelines for sketching a root locus)
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Chapter 6, on the analysis and design of control systems by the root locus method (the general rules for constructing root loci)
---

The root locus construction rules compute, from the poles and zeros of the open-loop transfer function $G(s) = N(s)/D(s)$ alone, the features that fix the shape of the [root locus](/root-locus/): the set of points where the closed-loop characteristic polynomial $D(s) + K N(s)$ has a root for some gain $K > 0$. The rules give the parts of the real axis on the locus, the straight lines that the branches approach at high gain, the points where branches meet and leave the real axis, the directions in which branches leave the poles and arrive at the zeros, and the gains at which branches cross the imaginary axis. Evans stated them in 1948 for drawing by hand. Each rule follows from one fact: $s$ is on the locus if and only if $G(s)$ is a negative real number.

## In plain words

A feedback loop has a gain knob. As you turn it up, the closed-loop poles move, and the root locus is the map of their paths. You can compute the paths by solving a polynomial for many gains, but a few rules tell you the shape of the map with little work. Some pieces of the real line are on the map and the others are not. The paths that go to infinity follow straight lines from one common center. Two paths that meet on the real line split off it at a point you can compute. Each path leaves its start point in a direction you can compute, and it ends at a fixed point of the plant or at infinity. The rules also give the gain at which a path crosses into the unstable half of the plane. This page computes all of these features and proves them.

## The problem

**Input.** The open-loop poles $p_1, \ldots, p_n$ and zeros $z_1, \ldots, z_m$, complex numbers with repetition, with $n \ge 1$ and $m \le n$. The two lists are closed under complex conjugation, so that $G$ has real coefficients, and no pole equals a zero. Write

$$D(s) = \prod_{i=1}^n (s - p_i), \qquad N(s) = \prod_{k=1}^m (s - z_k), \qquad \chi_K(s) = D(s) + K N(s).$$

Both $D$ and $N$ are monic, so $G = N/D$ and the loop transfer function is $L = K G$ with $K > 0$. The closed loop with unity negative feedback has the characteristic polynomial $\chi_K$. The locus is the set $\mathcal{L} = \{ s \in \mathbb{C} : \chi_K(s) = 0 \text{ for some } K > 0 \}$.

**Output.**

- the real axis segments, the closure of $\mathcal{L} \cap \mathbb{R}$, as a union of closed intervals;
- if $n > m$, the centroid $\sigma$ and the $n - m$ asymptote angles;
- the breakaway and break-in points, the points $s$ where $\chi_K$ has a multiple root for some $K > 0$, with that $K$;
- for each distinct pole of multiplicity $\mu$, the $\mu$ departure angles, and for each distinct zero of multiplicity $\nu$, the $\nu$ arrival angles;
- the imaginary axis crossings, the pairs $(\omega, K)$ with $\omega \ge 0$, $K > 0$ and $\chi_K(j\omega) = 0$; or a flag when $K(j\omega)$ is real for every $\omega$, so that whole intervals of the imaginary axis lie on the locus.

Angles are in degrees in $[0, 360)$, measured from the positive real axis.

## The algorithm

```pseudo id=main
ROOT-LOCUS-RULES(p_1..p_n, z_1..z_m)
L1  check n ≥ 1, m ≤ n, both lists closed under conjugation, no pole equal to a zero; D ← ∏(s − p_i), N ← ∏(s − z_k)
L2  segments ← the closed real intervals with an odd number of real poles and zeros, with multiplicity, to their right
L3  if n > m then σ ← (Σ p_i − Σ z_k)/(n − m); angles ← (2k + 1) · 180/(n − m) for k = 0, ..., n − m − 1
L4  W ← Σ_i w_i ∏_{j ≠ i} (s − r_j)   ▷ r_i: the distinct poles and zeros; w_i: the multiplicity, negative for a zero
L5  breakaways ← the pairs (s, K) with W(s) = 0 and K = −D(s)/N(s) real and positive
L6  for each distinct pole p of multiplicity μ: θ_j ← (180 + 360 j + Σ_k ∠(p − z_k) − Σ_{q ≠ p} ∠(p − q))/μ, j = 0, ..., μ − 1
L7  for each distinct zero z of multiplicity ν: φ_j ← (180 + 360 j + Σ_i ∠(z − p_i) − Σ_{y ≠ z} ∠(z − y))/ν, j = 0, ..., ν − 1
L8  R ← the polynomial with Im D(jω) N(−jω) = ω R(ω²); crossings ← the pairs (ω, K), ω = 0 or ω = √u for a real root u > 0 of R, with K = −D(jω)/N(jω) > 0; if R = 0 then set the flag
L9  return segments, σ, angles, breakaways, departures, arrivals, crossings, flag
```

Line L1 rejects the inputs for which the rules are false: a pole equal to a zero is a fixed root of $\chi_K$ for every $K$, and a list that is not closed under conjugation gives a $G$ with complex coefficients, for which the real axis rule fails. Line L2 sweeps the distinct real poles and zeros from right to left and keeps a running count; an interval between two of them is on the locus when the count is odd, and two such intervals that meet at a point of even multiplicity are merged. In line L3 the sums of the complex values are real, because the lists are closed under conjugation.

Line L4 builds $W = Q \sum_i w_i/(s - r_i)$, where $Q = \prod_i (s - r_i)$ and the sum is the logarithmic derivative $D'/D - N'/N$. Its roots are the critical points of $K(s) = -D(s)/N(s)$ away from the poles and zeros, and line L5 keeps the ones where $K$ is a positive real number. The other roots of $W$ belong to the locus for negative gain. Lines L6 and L7 add the angles of the vectors from all other poles and zeros, as the angle condition asks. In line L8, $K(j\omega)$ is real exactly when $D(j\omega) \overline{N(j\omega)}$ is real, and the imaginary part of that product is an odd polynomial in $\omega$. The point $\omega = 0$ is tested on its own, with $K = -D(0)/N(0)$.

The implementation works in floating point and finds the roots of $W$ and $R$ with the Durand-Kerner method of the shared helper module. It treats a value as real when its imaginary part is at most $10^{-9}(1 + |x|)$, two poles or zeros as equal when they differ by at most $10^{-9}(1 + |x|)$, and a gain as real when its imaginary part is at most $10^{-6}(1 + |K|)$.

## Example

**A third-order loop.** Take $G(s) = 1/(s(s + 1)(s + 2))$, so $n = 3$, $m = 0$, $D = s^3 + 3 s^2 + 2 s$ and $N = 1$.

| line | computation | result |
|---|---|---|
| L2 | real values from the right: $0$ (count 1), $-1$ (count 2), $-2$ (count 3) | segments $[-1, 0]$ and $(-\infty, -2]$ |
| L3 | $\sigma = (0 - 1 - 2)/3$, angles $(2k + 1) \cdot 60$ | $\sigma = -1$; 60, 180, 300 |
| L4 | $W = (s + 1)(s + 2) + s(s + 2) + s(s + 1)$ | $3 s^2 + 6 s + 2$ |
| L5 | roots $-1 \pm 1/\sqrt 3$; $K = -D(s)$ | $-0.42265$ with $K = 0.38490$ kept; $-1.57735$ with $K = -0.38490$ rejected |
| L6 | at 0: $180 - 0 - 0$; at $-1$: $180 - 180 - 0$; at $-2$: $180 - 180 - 180$ | 180, 0, 180 |
| L8 | $D(j\omega) = -3\omega^2 + j(2\omega - \omega^3)$, so $R(u) = 2 - u$ | $\omega = \sqrt 2 = 1.41421$, $K = 6$ |

At $\omega = 0$ the gain $-D(0)/N(0) = 0$ is not positive, so the origin is a start point and not a crossing. The two branches from 0 and $-1$ move toward each other on $[-1, 0]$, meet at $-0.42265$, and leave the axis. They follow the asymptotes at 60 and 300 degrees and cross the imaginary axis at $\pm j\sqrt 2$ for $K = 6$; at that gain $\chi_6 = (s + 3)(s^2 + 2)$. The third branch runs from $-2$ to $-\infty$. The value $K = 6$ is the [gain margin](/gain-margin/) of the loop with $K = 1$, the same value that the [Routh array](/routh-array/) of $s^3 + 3 s^2 + 2 s + K$ gives.

**Complex poles and a zero.** Take $G(s) = (s + 2)/(s^2 + 2 s + 2)$, with poles $-1 \pm j$ and the zero $-2$. Line L2 gives the segment $(-\infty, -2]$. Line L3 gives $n - m = 1$ and the single angle 180. Line L4 gives $W = (s + 2)(2 s + 2) - (s^2 + 2 s + 2) = s^2 + 4 s + 2$, with roots $-2 \pm \sqrt 2$. At $-2 - \sqrt 2 = -3.41421$ the gain is $2 + 2\sqrt 2 = 4.82843$, a break-in point; at $-2 + \sqrt 2$ the gain is $-0.82843$ and the root is rejected. Line L6 at $-1 + j$ gives $180 + \angle(1 + j) - \angle(2j) = 180 + 45 - 90 = 135$ degrees, and 225 at $-1 - j$. Line L7 at $-2$ gives $180 + \angle(-1 - j) + \angle(-1 + j) = 180 + 225 + 135 = 540$, that is 180 degrees. In line L8, $D(j\omega) N(-j\omega) = (2 - \omega^2 + 2 j\omega)(2 - j\omega)$ has the imaginary part $\omega(2 + \omega^2)$, so $R(u) = 2 + u$ has no positive root, and $-D(0)/N(0) = -1$: no crossings, and the loop is stable for every $K > 0$. The complex branch is an arc of the circle $|s + 2| = \sqrt 2$.

**Complex breakaway points.** Take $G(s) = 1/(s(s + 4)(s^2 + 4 s + 20))$. With $u = s^2 + 4 s$ the polynomial is $D = u (u + 20)$, and $W$ is a multiple of $D' = (2u + 20)(2 s + 4)$. The roots are $s = -2$ with $K = 64$, and the roots $-2 \pm j\sqrt 6 = -2 \pm 2.44949 j$ of $u = -10$ with $K = 100$. At $K = 100$ the closed loop is $(s^2 + 4 s + 10)^2$, so the four branches meet in pairs at two complex points. The departure angle at $-2 + 4j$ is 270 degrees. The Routh array of $s^4 + 8 s^3 + 36 s^2 + 80 s + K$ gives the crossing at $\omega = \sqrt{10}$ for $K = 260$, which line L8 also returns.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md). Each statement holds in exact arithmetic, with exact roots of $W$ and $R$.

- **Angle and magnitude conditions (proved).** For $s$ not a pole or zero, $s \in \mathcal{L}$ if and only if $G(s) < 0$, that is $\angle G(s) = 180$ degrees modulo 360; then $K = 1/|G(s)|$. Poles and zeros are not in $\mathcal{L}$; they are the limits of the branches as $K \to 0$ and $K \to \infty$.
- **Real axis segments (proved).** A real $x$ that is not a pole or zero is on the locus if and only if the number of real poles and zeros, with multiplicity, greater than $x$ is odd. Line L2 returns the closure of these points.
- **Asymptotes (proved).** If $q = n - m \ge 1$, then for large $K$ the closed loop has $m$ roots near the zeros and $q$ roots $s_k(K) = \sigma + K^{1/q} e^{j\theta_k} + o(1)$, with $\theta_k = (2k + 1)180/q$. If $q \ge 2$, the mean of these $q$ roots tends to $\sigma$.
- **Breakaway points (proved).** $\chi_K$ has a multiple root at $s_0$ for some $K > 0$ if and only if $W(s_0) = 0$ and $-D(s_0)/N(s_0)$ is a positive real number. Branches can meet, and real roots can leave the real axis, only at such points.
- **Departure and arrival angles (proved).** For small $K$ there are exactly $\mu$ roots near a pole of multiplicity $\mu$, and their directions from the pole tend to the angles of line L6. For large $K$ the same holds at a zero with the angles of line L7.
- **Crossings (proved).** For $\omega > 0$, $j\omega \in \mathcal{L}$ if and only if $R(\omega^2) = 0$ and $-D(j\omega)/N(j\omega) > 0$, unless $R$ is the zero polynomial. The number of closed-loop poles in the open right half plane can change only at a gain in the list of crossings.

## Complexity

Let $d \le n + m$ be the number of distinct poles and zeros, and $t$ the number of iterations of the polynomial root finder. The cost is counted in arithmetic operations on complex numbers.

- **Line L1.** The conjugation check and the comparisons of poles with zeros take $O((n + m)^2)$ operations; the products $D$ and $N$ take $O(n^2 + m^2)$.
- **Lines L2 and L3.** Grouping equal values takes $O((n + m)^2)$ and the sort $O(d \log d)$; the centroid takes $O(n + m)$.
- **Line L4.** The implementation forms each of the $d$ products of $d - 1$ linear factors in $O(d^2)$, so $O(d^3)$ in all. The sum has degree at most $d - 1$.
- **Line L5.** Durand-Kerner on $W$ costs $O(d^2)$ per iteration, so $O(t d^2)$; each candidate needs one evaluation of $D$ and $N$, $O(n + m)$.
- **Lines L6 and L7.** Each distinct pole or zero adds $n + m$ angles: $O(d (n + m))$.
- **Line L8.** The coefficients of $D(j\omega) N(-j\omega)$ take $O(n m + n)$ operations. $R$ has degree at most $(n + m - 1)/2$, and its roots cost $O(t (n + m)^2)$.

The total is $O((n + m)^3 + t (n + m)^2)$ operations and $O(n + m)$ extra space. In practice $n + m$ is below 20 and the cost is negligible next to drawing the locus by computing the roots of $\chi_K$ on a grid of gains, which costs $O(t n^2)$ per gain.

## Properties

- **Local information from the poles and zeros.** Every rule uses only the poles, the zeros and their multiplicities; the gain enters only through the magnitude condition.
- **Exact rules, approximate numbers.** In exact arithmetic the output is exact. In floating point the angles, the centroid and the segments are accurate to rounding, while the breakaway points and the crossings carry the errors of the root finder and the tolerances of line L5 and line L8.
- **Not a full locus.** The rules fix the shape near the poles, near the zeros, near infinity, on the real axis and on the imaginary axis. Between these places the branches must be computed or sketched.
- **Deterministic.** The same input gives the same output.

## Variants and improvements

- **Negative gain.** For $K < 0$ the condition is $G(s) > 0$, and the rules change: a real point is on the locus when an even number of real poles and zeros lie to its right, the asymptote angles are $k \cdot 360/(n - m)$, the 180 in lines L6 and L7 becomes 0, and line L5 keeps the roots of $W$ with negative $K$. The roots that line L5 rejects are the breakaway points of this complementary locus.
- **Routh array for the crossings.** Textbooks find the crossing gain from the row of $s^1$ in the [Routh array](/routh-array/) of $\chi_K$, and $\omega$ from the auxiliary polynomial of the row of $s^2$. This gives the same pairs as line L8 and also proves stability between the crossings, by the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/).
- **A cheaper W.** Dividing $Q$ by each factor $s - r_i$ with [Horner's rule](/horner-rule/) gives each product of line L4 in $O(d)$, so $O(d^2)$ in all. Another way is to form $N D' - N' D$ and divide it by the repeated factors.
- **Exact counts.** With rational poles and zeros, a [Sturm sequence](/sturm-sequence/) of $W$ counts the real breakaway candidates in an interval without rounding errors (see [real root counting](/real-root-counting/)).
- **Discrete time.** For a sampled loop $K G(z)$, lines L2 to L7 hold unchanged in the $z$ plane, and the stability boundary is the unit circle. Line L8 then becomes the search for the $\theta$ with $K = -D(e^{j\theta})/N(e^{j\theta})$ real and positive.
- **Numerical locus.** Design tools compute the roots of $\chi_K$ on a grid of gains and join them into branches; the rules give the start and end directions, and the breakaway and crossing gains tell where the grid must be fine.

## When to use it

Use the rules to sketch a locus by hand, to check a computed root locus plot, or to answer the questions a plot answers only approximately: the gain at which the loop becomes unstable, the gain at which a pair of real poles becomes complex, and the effect of one added pole or zero of a [lead-lag compensator](/lead-lag-compensator/). The crossing gain and frequency are the ultimate gain and frequency of [Ziegler-Nichols tuning](/ziegler-nichols-tuning/). For a full picture, compute the roots of $\chi_K$ on a grid of gains with a [polynomial root finder](/polynomial-root-finding/) and use the rules to place the grid. The rules need a rational $G$ and one gain that enters linearly; for a time delay, use a [Padé approximation](/pade-approximation/) first.

## Pitfalls

- **Rejected candidates.** Not every root of $W$ is a breakaway point. A real root of $W$ outside the real axis segments has $K < 0$, and a complex root is a breakaway point only if its $K$ is real and positive, as in the third example.
- **Double roots are ill-conditioned.** At a breakaway gain the closed loop has a double root, and a computed double root splits by about the square root of the unit roundoff, near $10^{-8}$ relative (see [root conditioning](/root-conditioning/)). A test of a breakaway point must use a tolerance of this size, not $10^{-15}$.
- **Asymptotes are limits.** The branches approach the asymptotes only as $K \to \infty$, and they can cross the asymptotes on the way. A branch near an asymptote is not on it.
- **Multiple poles and zeros.** A pole of multiplicity $\mu$ has $\mu$ departure angles spaced by $360/\mu$ degrees; using the formula for a simple pole gives one angle and loses the others.
- **Cancellation.** A pole equal to a zero is rejected in line L1. If the cancellation is only approximate, the rules hold, but a short branch from the pole to the nearby zero carries a slow closed-loop pole, and for an unstable pole this pole stays unstable.
- **Signs.** The rules assume monic $N$ and $D$ and $K > 0$. A plant with a negative leading coefficient, such as $(1 - s)/(s + 1)^2$, needs the negative gain rules.
- **The imaginary axis on the locus.** If $D(j\omega) \overline{N(j\omega)}$ is real for every $\omega$, as for $G = 1/(s^2 + 1)$, line L8 sets the flag instead of listing points. Then whole intervals of the axis are on the locus.

## Implementations

## History

Walter R. Evans published the graphical analysis of control systems by the paths of the closed-loop roots in 1948, with the angle and magnitude conditions and the rules for sketching the paths from the open-loop poles and zeros. In 1950 he showed how to use the locus to choose the gain and the compensation. Before the method, designers found closed-loop poles by factoring the characteristic polynomial for each gain, or worked in the frequency domain with the Nyquist and Bode methods. After computers took over the computation of the roots, the rules stayed in use to read and check root locus plots.

## References
