---
tag: 4ASC1H
kind: algorithm
slug: cohen-sutherland-line-clipping
name: Cohen-Sutherland line clipping
aliases:
- outcode algorithm
area: graphics-and-signals/rasterization
level: intro
summary: Clip a segment to a rectangle with a 4-bit region code per end point. Accept or reject at once when the codes allow it, else cut at one side and repeat.
solves: [line-clipping]
model: real-ram
complexity:
  vars: {n: the number of segments}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1967
  people: [Danny Cohen, Ivan Sutherland]
  note: Cohen and Sutherland made the method in 1967 for flight simulator work. Newman and Sproull described it in their 1973 book.
prereqs: [line-clipping]
see_also: [liang-barsky-line-clipping, polygon-window-clipping, sutherland-hodgman, line-rasterization, bresenham-line-algorithm, ieee-754]
sources:
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Section 3.12, Clipping Lines (the region codes, trivial acceptance and rejection, and the cut at one side at a time)
  - book: "William M. Newman and Robert F. Sproull, Principles of Interactive Computer Graphics, McGraw-Hill, 1973"
    locator: the chapter on clipping (the end point codes of Cohen and Sutherland)
  - paper: doi:10.1145/1476589.1476687
    title: Robert F. Sproull and Ivan E. Sutherland, A clipping divider, AFIPS Fall Joint Computer Conference, 1968
    locator: the hardware clipper by midpoint subdivision, a different method from the same group
  - paper: doi:10.1145/357332.357333
    title: You-Dong Liang and Brian A. Barsky, A new concept and method for line clipping, ACM Transactions on Graphics 3(1), 1 to 22 (1984)
    locator: the comparison of their method with the Cohen-Sutherland method
---

Cohen-Sutherland line clipping solves [line clipping](/line-clipping/) against an axis-aligned rectangle. It gives each end point a 4-bit region code, the outcode, with one bit for each side of the window that the point is outside of. Two bit tests accept a segment with both ends inside, or reject a segment with both ends outside the same side. Any other segment is cut at one side, and the test runs again, at most four times.

## In plain words

Draw the four lines of the window sides across the whole plane. They cut the plane into nine parts: the window in the middle and eight parts around it. Each part gets a short code that says "left", "right", "above", "below", or two of these.

For a segment, look at the codes of its two ends. If both ends are in the window, keep the whole segment. If both ends are left of the window, or both above it, the segment cannot reach the window, so throw it away. These two checks are very cheap.

In any other case, take an end that is outside. Move it along the segment to the side line that it is outside of. Then check the codes again. After a few moves, one of the cheap checks always decides.

## The problem

The input is a segment from $P$ to $Q$ and a window $W = [x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}]$. The output is $\overline{PQ} \cap W$: nothing, one point or one segment, in the direction from $P$ to $Q$. The window is closed, so a point on a side is inside. See [line clipping](/line-clipping/).

The model is the [real RAM](/real-ram/) with exact rational arithmetic; the implementation uses Python integers and fractions, so each decision is exact. The window is in continuous coordinates. When the clipped segment is drawn, the pixels are point samples at the centers $(i + 1/2, j + 1/2)$, as in the OpenGL and Direct3D 10 rules, and not little squares.

## The algorithm

The code of a point $p = (x, y)$ has the bit LEFT $= 1$ if $x < x_{\min}$, RIGHT $= 2$ if $x > x_{\max}$, BOTTOM $= 4$ if $y < y_{\min}$ and TOP $= 8$ if $y > y_{\max}$. A code has at most one bit for each axis, and it is 0 exactly for points of $W$.

```pseudo id=main
COHEN-SUTHERLAND(P, Q, W)                  ▷ W = [xmin, xmax] × [ymin, ymax]
L1  cP ← OUTCODE(P), cQ ← OUTCODE(Q)
L2  loop
L3      if cP = 0 and cQ = 0 then return the segment P Q       ▷ trivial accept
L4      if cP AND cQ ≠ 0 then return empty                     ▷ trivial reject
L5      c ← cP if cP ≠ 0, else cQ                              ▷ an end point outside W
L6      if c has TOP then (x, y) ← (xP + (xQ − xP)(ymax − yP) / (yQ − yP), ymax)
L7      else if c has BOTTOM then (x, y) ← (xP + (xQ − xP)(ymin − yP) / (yQ − yP), ymin)
L8      else if c has RIGHT then (x, y) ← (xmax, yP + (yQ − yP)(xmax − xP) / (xQ − xP))
L9      else (x, y) ← (xmin, yP + (yQ − yP)(xmin − xP) / (xQ − xP))      ▷ c has LEFT
L10     if c = cP then P ← (x, y), cP ← OUTCODE(P) else Q ← (x, y), cQ ← OUTCODE(Q)
```

Line L4 is the AND of the two codes as bit sets. A common bit means that both end points are outside the same side, so the whole segment is outside it. Lines L6 to L9 move the chosen end point to the line of one side that it is outside of, along the segment. The other end point is not outside that side, because the codes have no common bit, so the divisor is never zero. Line L10 keeps the moved point in its place as the start or the end, so the output keeps the direction from $P$ to $Q$.

## Example

Clip the segment from $P = (-3, -1)$ to $Q = (13, 11)$ against $W = [0, 10]^2$. The codes are $c_P = \text{LEFT} \mid \text{BOTTOM} = 5$ and $c_Q = \text{RIGHT} \mid \text{TOP} = 10$. Their AND is 0, so neither cheap test decides.

| Cut | End | Side (line) | New point | New code |
|---|---|---|---|---|
| 1 | $P$ | BOTTOM (L7) | $(-5/3, 0)$ | LEFT |
| 2 | $P$ | LEFT (L9) | $(0, 5/4)$ | 0 |
| 3 | $Q$ | TOP (L6) | $(35/3, 10)$ | RIGHT |
| 4 | $Q$ | RIGHT (L8) | $(10, 35/4)$ | 0 |

Both codes are now 0, and line L3 returns the segment from $(0, 5/4)$ to $(10, 35/4)$. The points $(-5/3, 0)$ and $(35/3, 10)$ are computed and then thrown away. This segment needs the most cuts that any segment can need.

Now clip the segment from $(-2, 8)$ to $(3, 14)$. The codes are LEFT and TOP, with no common bit. The cut at the left side gives $(0, 52/5)$, whose code is TOP. Both codes now have the bit TOP, and line L4 rejects the segment after one cut. The segment passes the upper left corner of the window without touching it.

## Correctness

The proof keeps this invariant: the current segment lies on the input segment in the same direction, and its part inside $W$ is the answer. Line L3 is right because $W$ is convex. Line L4 is right because the region outside one side is convex. A cut removes only points that are strictly outside one side, so the invariant stays true.

For termination, count the set bits of the two codes; there are at most four. The moved point is on a convex combination of the two end points, so it can only have bits that one of the two end points has, and it loses the bit of the side it was moved to. If its new code has a bit in common with the other end, the next test rejects. If not, the count falls by at least one. So there are at most four cuts. The full proof is below.

## Complexity

Each segment takes at most four cuts and five passes of the loop, so it takes $O(1)$ time, with at most four divisions. For $n$ segments the time is $\Theta(n)$, and the extra space is $\Theta(1)$. A segment that is fully inside, or fully outside one side, costs two outcodes and two bit tests, with no division.

## Properties

- The trivial tests decide most segments of a typical scene with no arithmetic beyond comparisons. This was the reason for the method.
- It computes crossing points that it later throws away, as in the example. A segment can need four divisions.
- A segment outside the window can still need one or two cuts before line L4 rejects it, when it passes a corner region.
- With exact arithmetic the output is exact: each coordinate of a new point is a boundary value or the result of one division.
- The output keeps the direction of the segment, and it gives the same set for the reversed segment.

## Variants and improvements

- **Three dimensions.** A 6-bit code, with two bits for the near and far planes, clips against a box. In homogeneous coordinates the tests become $x < -w$, $x > w$ and so on, before the divide.
- **Box culling.** The AND of the outcodes of the eight corners of a bounding box is nonzero exactly when the box is outside one plane. Renderers use this test to skip whole objects.
- **Midpoint subdivision.** The clipping divider of Sproull and Sutherland (1968) finds the crossing point by halving the segment again and again, with only additions and shifts. It was built in hardware.
- **Fewer wasted cuts.** [Liang-Barsky line clipping](/liang-barsky-line-clipping/) computes the parameter of each crossing and does each division at most once. The Nicholl-Lee-Nicholl method (1987) uses the region of one end point to choose the right sides first, so that it computes no point that it throws away.

## When to use it

Use it when most segments are fully inside the window or fully outside one side, as in a large map seen through a small window. The cheap tests then decide almost every segment. When many segments cross the window, [Liang-Barsky line clipping](/liang-barsky-line-clipping/) does less work. For a convex window that is not a rectangle, use the Cyrus-Beck form of the parameter method. For polygons, use [polygon window clipping](/polygon-window-clipping/).

## Pitfalls

- **Floating-point rounding.** In [IEEE 754](/ieee-754/) arithmetic, a computed crossing point can land just outside the window. Its code then has a bit again, and the loop does an extra cut, or in a bad case cuts back and forth. Set the coordinate of the clipped side to the exact boundary value, as lines L6 to L9 do, and compute only the other coordinate. A program can also clamp that coordinate to the window when the segment is accepted, or use exact rational or integer arithmetic.
- **Strict and non-strict tests.** The code uses strict inequalities, so points on a side count as inside. If the codes use $\le$ in some places and $<$ in others, a segment on a side can be rejected or can loop.
- **Division by zero.** The division is safe only because line L4 runs before the cut. If a program changes the order of the tests, a vertical segment can reach line L6 with $y_Q = y_P$.
- **Integer windows.** When the window is in pixel units and the end points are integers, a crossing point is a rational number. Rounding it before [line rasterization](/line-rasterization/) changes the line. A [Bresenham](/bresenham-line-algorithm/) line must start at the exact crossing with the matching error term, so that the clipped line draws the same pixels as the full line inside the window.

## Implementations

## History

Danny Cohen and Ivan Sutherland made the outcode method in 1967, during work on flight simulators. Newman and Sproull described it in their book Principles of Interactive Computer Graphics in 1973, which is the usual source for it. Sproull and Sutherland published "A clipping divider" in 1968. That paper is often cited for the outcode method, but it describes a hardware clipper that finds crossing points by midpoint subdivision. Liang and Barsky gave a parameter method in 1984 that does fewer divisions, and Nicholl, Lee and Nicholl gave a method in 1987 that never computes a point it throws away.

## References
