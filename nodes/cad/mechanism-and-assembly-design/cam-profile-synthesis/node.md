---
tag: 59Q72X
kind: algorithm
slug: cam-profile-synthesis
name: Cam profile synthesis
aliases:
- cam contour generation
- cam layout by inversion
area: cad/mechanism-and-assembly-design
level: core
summary: Computes the cam contour as the envelope of the follower positions for a given displacement law, in closed form for flat-faced and roller followers.
model: real-ram
complexity:
  vars: {N: the number of cam angles sampled, m: the number of segments of the cam program}
  time: {worst: Θ(m + N log m), average: Θ(m + N log m), best: Θ(m + N log m)}
  space: {extra: Θ(N)}
properties: {deterministic: true, recursive: false}
prereqs: [cam-follower-motion-laws, offset-curve]
see_also: [cam-pressure-angle, curve-offsetting, offset-trimming, swept-volume, curvature-comb, transmission-angle, finite-differences, minkowski-sum]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 8.6 (p. 460, sizing the cam, with the pressure angle of translating roller followers on p. 461, the overturning moment of flat-faced followers on p. 465, the radius of curvature of roller followers on p. 466 and of flat-faced followers on p. 470) and Section 8.7 (p. 475, practical design considerations)
  - book: isbn:9780831133672
    title: Robert L. Norton, Cam Design and Manufacturing Handbook, 2nd edition, Industrial Press, 2009
    locator: the chapters on cam size, pressure angle and radius of curvature, and on cam manufacturing (general locator)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the chapter on cam design, the layout of cam profiles by inversion and the analytic profile equations (general locator)
---

Cam profile synthesis computes the outline of a disk cam from the motion that its follower must make. A disk cam is a plate that turns on a shaft. Its follower is a part that slides in a fixed guide and is kept against the edge of the cam by a spring, so the shape of the edge drives the follower. The input is the displacement $s(\theta)$ of the follower as a function of the cam angle, built from [cam follower motion laws](/cam-follower-motion-laws/). The method is inversion: hold the cam still and turn the ground and the follower the other way. The follower then takes one position for each cam angle, and the cam outline is the envelope of these positions, the curve that touches each of them. For a roller follower and for a flat-faced follower the envelope has a closed form, so each point of the outline costs a fixed number of operations, with no search and no root finding.

## In plain words

Draw the cam standing still in the middle of the page. Walk the follower around it, and at each step put the follower where the motion plan says it must be at that angle. The cam edge must touch the follower at each step and must not cut into it. So the edge is the curve that just touches all the drawn followers. For a round roller, the edge is a fixed distance inside the path of the roller center. For a flat foot, the edge is the curve that all the drawn foot lines touch. The same formulas also tell you how steep the push is and how sharp the edge is, so you can see at once if the cam is too small.

## The problem

**Input.**

- A cam program: segments $i = 1, \ldots, m$, each with a motion law $f_i$ on $[0, 1]$ ($f_i(0) = 0$, $f_i(1) = 1$, or $f_i = 0$ for a dwell), a cam angle $\beta_i > 0$ and a lift $L_i$ (negative for a return), with $\sum \beta_i = 2\pi$ and $\sum L_i = 0$.
- The base circle radius $R_b > 0$: the radius of the smallest circle about the cam center that touches the cam profile.
- The follower. A translating roller follower has a roller of radius $R_f \ge 0$, and the line of its motion is at the offset $\varepsilon$ from the cam center. A translating flat-faced follower has a flat face square to its line of motion.
- The number of samples $N \ge 1$.

**Output.** For $\theta = 2\pi k/N$, $k = 0, \ldots, N - 1$, in the frame of the cam: the point of the cam profile that touches the follower, and the checks that decide if the cam works, the pressure angle and the radius of curvature.

For the roller follower, the prime circle has the radius $R_p = R_b + R_f$. It is the circle through the roller center at zero lift. The pitch curve is the path of the roller center relative to the cam. The cam turns counterclockwise. The fixed frame has the cam center at the origin and the follower moving along the line $x = \varepsilon$ in the direction $+y$.

## The algorithm

Here $R(\alpha)$ is the rotation by $\alpha$. A point $p$ fixed to the ground is at $R(-\theta)p$ in the frame of a cam that has turned by $\theta$.

```pseudo id=main
CAM-PROFILE(P, R_b, R_f, ε, N)          ▷ P = segments (f_i, β_i, L_i); translating roller follower
L1  check Σ β_i = 2π and Σ L_i = 0; θ_1 ← 0, h_1 ← 0, θ_{i+1} ← θ_i + β_i, h_{i+1} ← h_i + L_i
L2  R_p ← R_b + R_f, d_0 ← √(R_p² − ε²)
L3  for k ← 0 to N − 1, with θ ← 2πk/N, do
L4      i ← the segment with θ_i ≤ θ < θ_{i+1}, x ← (θ − θ_i)/β_i
L5      s ← h_i + L_i f_i(x), s′ ← L_i f_i′(x)/β_i, s″ ← L_i f_i″(x)/β_i²
L6      u ← d_0 + s, w ← s′ − ε, D ← √(u² + w²)
L7      C ← R(−θ)(ε, u)                              ▷ roller center: a point of the pitch curve
L8      K ← R(−θ)(ε + R_f w/D, u − R_f u/D)          ▷ contact: a point of the cam profile
L9      φ ← atan2(w, u)                              ▷ pressure angle
L10     ρ ← D³/(u² + w(w + s′) − u s″)               ▷ radius of curvature of the pitch curve
L11     output (θ, s, C, K, φ, ρ), marked undercut if 0 < ρ ≤ R_f

FLAT-FACE-PROFILE(P, R_b, N)            ▷ translating follower, flat face square to its axis
L12 for k ← 0 to N − 1, with θ ← 2πk/N, do
L13     s, s′, s″ as in lines L4 and L5
L14     Q ← R(−θ)(s′, R_b + s)                       ▷ contact: a point of the cam profile
L15     ρ ← R_b + s + s″                             ▷ radius of curvature; it must be positive
L16     output (θ, s, Q, ρ); the contact is at the distance s′ from the axis along the face
```

Line L5 is the chain rule on $s = h_i + L_i f_i((\theta - \theta_i)/\beta_i)$. Line L7 is the inversion: in the fixed frame the roller center is at $(\varepsilon, d_0 + s)$, and $d_0$ puts it on the prime circle at zero lift. The pitch curve has the tangent $R(-\theta)(u, w)$. Line L8 steps from the roller center by $R_f$ along the normal toward the cam, so the cam profile is the inner offset of the pitch curve at the distance $R_f$, as on the [offset curve](/offset-curve/) page. Line L9 is the angle between the common normal and the line of motion. Line L10 is the radius of curvature of the pitch curve, positive where the curve is convex. With $\varepsilon = 0$ it is the formula $[(R_p + s)^2 + s'^2]^{3/2}/[(R_p + s)^2 + 2s'^2 - s''(R_p + s)]$ of Norton, Section 8.6. The cam profile then has the radius $\rho - R_f$ at $K$. For the flat face, line L14 is the envelope of the face lines, and line L15 is the radius of the profile itself.

## Example

Take a rise of $20$ mm with the cycloidal law over $90°$, a dwell of $90°$, a return of $20$ mm with the 3-4-5 polynomial over $90°$, and a dwell of $90°$. Take $R_b = 40$ mm, a roller of $R_f = 10$ mm and no offset, so $R_p = d_0 = 50$ mm. In the rise, $\beta = \pi/2$ and the cycloidal law gives $s' = (40/\pi)(1 - \cos 4\theta)$ and $s'' = (160/\pi)\sin 4\theta$. Lengths are in mm, and $s'$, $s''$ are per radian of cam angle.

| $\theta$ | $s$ | $s'$ | $s''$ | pitch point $C$ | cam point $K$ | $\varphi$ | $\rho$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $0°$ | 0 | 0 | 0 | (0, 50) | (0, 40) | $0°$ | 50.00 |
| $22.5°$ | 1.8169 | 12.7324 | 50.9296 | (19.8295, 47.8726) | (18.3178, 37.9875) | $13.81°$ | 410.36 |
| $45°$ | 10 | 25.4648 | 0 | (42.4264, 42.4264) | (38.6799, 33.1548) | $23.00°$ | 56.55 |
| $67.5°$ | 18.1831 | 12.7324 | $-50.9296$ | (62.9930, 26.0925) | (54.6136, 20.6348) | $10.58°$ | 39.51 |
| $90°$ | 20 | 0 | 0 | (70, 0) | (60, 0) | $0°$ | 70.00 |
| $225°$ | 10 | $-23.8732$ | 0 | ($-42.4264$, $-42.4264$) | ($-33.2422$, $-38.4705$) | $-21.70°$ | 56.81 |

At $45°$, line L6 gives $u = 60$, $w = 80/\pi = 25.4648$ and $D = 65.18$, and line L9 gives $\varphi = \arctan(25.4648/60) = 23.00°$. Line L7 turns $(0, 60)$ by $-45°$ to $(42.4264, 42.4264)$. Line L10 gives $65.18^3/(3600 + 1296.91) = 56.55$.

With $N = 3600$ samples, the largest pressure angle is $23.23°$ at $\theta = 41.9°$ in the rise and $-21.94°$ at $228.5°$ in the return. The smallest radius of the pitch curve is $39.42$ mm at $65.9°$, so the cam itself has the radius $29.42$ mm there, and no sample is marked as undercut. An offset of $\varepsilon = 5$ mm lowers the peak in the rise to $19.07°$ but raises the peak in the return to $-26.13°$. An offset helps one direction of motion at the cost of the other.

The same program with a flat-faced follower and $R_b = 40$ mm has the smallest radius $\rho = 7.15$ mm at $66.5°$. The smallest value of $s + s''$ over the cycle is $-32.85$ mm, so line L15 needs $R_b > 32.85$ mm. The contact moves along the face from $s' = -23.87$ mm to $s' = 25.46$ mm, so the face must be at least $49.34$ mm wide.

A small cam shows the undercut. Take a cycloidal rise of $20$ mm over $40°$, a dwell of $140°$, a cycloidal return over $40°$ and a dwell of $140°$, with $R_b = 10$ mm and $R_f = 9$ mm. The pitch curve then has a convex radius of only $6.59$ mm, less than the roller, and line L11 marks 30 of 720 samples, near $30°$ and near $189°$. The pressure angle reaches $64.3°$, far above the usual limits on the [cam pressure angle](/cam-pressure-angle/) page. With $R_b = 60$ mm no sample is marked.

## Correctness

Four facts make the output right. Line L5 gives $s$, $s'$ and $s''$ by the chain rule. In the frame of the cam, the roller center at the angle $\theta$ is the fixed point $(\varepsilon, d_0 + s)$ turned by $-\theta$, which is line L7. The roller circles have the envelope $C \pm R_f n$, where $n$ is the unit normal of the pitch curve, because a point of the envelope satisfies $(p - C)\cdot C' = 0$. The face lines $q\cdot e(\theta) = R_b + s$, with $e = R(-\theta)(0, 1)$, have the envelope $(R_b + s)e + s'e'$, which is line L14.

These facts show that each output point is on the envelope. The proof also shows that the follower does not cut the cam. If $\rho > R_f$ at every angle, the tangent of the profile turns once in one direction, and the whole cam lies on the inner side of the tangent line at each contact point. So the roller is at the distance $R_f$ from the cam, and touches it at $K$. If $0 < \rho < R_f$ at an angle, the roller at nearby angles covers the point $K$, which is the undercut of line L11. For the flat face the same argument works when $R_b + s + s'' > 0$ at every angle. The full proof is below.

## Complexity

Line L1 takes $\Theta(m)$ time. Line L4 finds the segment by binary search on the start angles in $O(\log m)$ time, and lines L5 to L11 take $O(1)$ time, with one square root, one arc tangent and a few products. So the time is $\Theta(m + N\log m)$. The samples come in increasing order of $\theta$, so a pointer that moves forward through the segments replaces the search, and the time drops to $\Theta(m + N)$. The output has $\Theta(N)$ points, and the extra space beyond it is $O(1)$.

The number $N$ follows from the machining tolerance. Between two samples the profile is replaced by a chord, and a chord of length $\ell$ on an arc of radius $r$ is at most $\ell^2/(8r)$ from the arc. For the example, the cam has a perimeter of $320.2$ mm and a smallest radius of $29.42$ mm. With $N = 3600$ the longest chord is $0.1047$ mm, so the bound is $0.1047^2/(8 \cdot 29.42) = 4.7 \times 10^{-5}$ mm, and the largest distance from a chord to the true profile is $3.5 \times 10^{-5}$ mm.

## Properties

- **Exact at the samples.** Each output point is a point of the true profile up to rounding. Only the curve between samples is an approximation.
- **Independent samples.** Each angle is computed alone, so the loop runs in parallel and a single angle can be evaluated on demand.
- **Needs $s''$ but not $s'''$.** The profile needs $s$ and $s'$, and the checks need $s''$. A jump in $s''$, as with the harmonic law next to a dwell, is a jump in the radius of curvature, so the cam has a visible change of curvature there.
- **Deterministic and closed form.** There is no iteration, so there is no convergence test and no tolerance to choose.

## Variants and improvements

- **Oscillating followers.** A follower arm that turns about a fixed pivot needs the same inversion with the arm angle in place of $s$. The formulas change, and the pressure angle is measured against the direction of motion of the roller center, which is square to the arm.
- **The cutter path.** A milling cutter of radius $R_c$ that cuts the cam must follow the offset of the profile by $R_c$. If $R_c = R_f$, the cutter center follows the pitch curve itself. For other cutters, offset the pitch curve by $R_c - R_f$ with [curve offsetting](/curve-offsetting/).
- **General follower shapes.** For a follower of any convex outline, the largest cam that no follower position overlaps is the complement of the union of the follower positions in the cam frame, which is the [swept volume](/swept-volume/) of the follower in two dimensions. The contact points are the points of the follower outline where the relative velocity is square to the normal.
- **Fitted spline cams.** Instead of fixed laws, fit $s$ with a spline that meets the end conditions and limits on $s'$, $s''$ and $s'''$, then run the same loop on the spline.
- **Three-dimensional cams.** Barrel and globoidal cams use the same inversion in space, with an envelope of surfaces in place of curves.

## When to use it

Use it whenever the motion of the follower is known and the cam outline must be made, which is the normal order of cam design. Run the checks of lines L9, L10 and L15 first, at a coarse $N$, and change $R_b$, $\varepsilon$ or the motion laws until the pressure angle and the radius of curvature are acceptable. Then run it at the fine $N$ that the machining tolerance needs.

## Pitfalls

- **The direction of rotation.** The profile for a cam that turns clockwise is the mirror image. Using $R(\theta)$ in place of $R(-\theta)$ gives the profile of a cam that turns the wrong way. The sign of a useful offset $\varepsilon$ also changes with the direction.
- **Derivatives in time or in angle.** Lines L5 to L15 use derivatives with respect to $\theta$, in units of length per radian. The velocity in time is $\omega s'$, not $s'$. Mixing them, or using degrees, gives a wrong pressure angle and a wrong radius.
- **Undercut.** If $0 < \rho \le R_f$, the inner offset forms a cusp and a loop, and a cutter of the roller size removes the loop. The cam then has a sharp corner and the follower does not follow the program. Trimming the loop, as on the [offset trimming](/offset-trimming/) page, does not cure this. Increase $R_b$ or use a smaller roller.
- **The flat face needs a positive radius.** If $R_b + s + s'' \le 0$ somewhere, the envelope folds back, and no flat-faced follower can follow the program. A large negative $s''$ at a high lift causes this. The face must also be wide enough for the full range of $s'$.
- **The offset limit.** The offset needs $|\varepsilon| < R_p$, and the formulas assume $u = d_0 + s > 0$.
- **Too few samples near sharp curvature.** Equal angle steps give long chords where the cam is large and few points where $\rho$ is small. Choose $N$ from the smallest radius, or sample by [arc length](/arc-length-parametrization/).

## Implementations

## History

The layout of a cam by inversion, in which the follower is drawn at each angle around a fixed cam and the cam outline is drawn to touch every position, is the classic graphical method of the mechanism textbooks. The closed forms for the pitch curve, the profile, the pressure angle and the radius of curvature are the analytic form of the same construction. Norton gives the pressure angle and the radius of curvature for translating followers in Section 8.6 of Design of Machinery, and his handbook also treats the manufacture of cams. Uicker, Pennock and Shigley derive the profile equations for flat-faced and roller followers.

## References
