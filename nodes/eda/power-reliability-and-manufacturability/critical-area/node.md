---
tag: PJPMSC
kind: definition
slug: critical-area
name: Critical area
aliases:
- critical area for shorts and opens
area: eda/power-reliability-and-manufacturability
level: core
summary: The area of the layout where the centre of a spot defect of given size causes a short or open; integrated over the defect size distribution it gives the yield loss.
prereqs: [minkowski-sum]
see_also: [voronoi-critical-area-extraction, poisson-yield-model, murphy-yield-model, negative-binomial-yield-model, redundant-via-insertion, dummy-fill-problem, order-k-voronoi-diagram, design-rule-checking]
sources:
  - paper: doi:10.1147/rd.276.0549
    title: C. H. Stapper, Modeling of integrated circuit defect sensitivities, IBM Journal of Research and Development 27(6), 549 to 557, November 1983
    locator: the definition of the critical area of a pattern for a defect of given size, and its average over the defect size distribution as the quantity that multiplies the defect density in the yield formula
  - paper: "C. H. Stapper, Modeling of defects in integrated circuit photolithographic patterns, IBM Journal of Research and Development 28(4), 461 to 475, July 1984"
    locator: the critical areas of dense arrays of parallel lines for shorts and opens, and the defect size distribution that falls as the inverse cube of the size above its peak
  - paper: "Evanthia Papadopoulou and D. T. Lee, Critical area computation via Voronoi diagrams, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 18(4), 463 to 474, April 1999"
    locator: the square defect model, the critical radius of a point as its distance to the second nearest polygon, and the critical area for shorts as the area where that radius is at most the defect radius
---

The critical area of a layout layer, for a spot defect of radius $r$, is the area of the set of points where the centre of the defect must fall for the defect to cause a fault: a *short* when extra conducting material joins two different nets, an *open* when missing material cuts a net. It is a function $A(r)$ of the defect size, and its average $\bar A$ over the size distribution, times the defect density, is the expected number of faults on the chip. That expected number is the input of the [Poisson](/poisson-yield-model/), [Murphy](/murphy-yield-model/) and [negative binomial](/negative-binomial-yield-model/) yield models, and the area itself is the [Minkowski sum](/minkowski-sum/) of the layout with the defect shape, cut down to the positions that join or break nets.

## Definition

**Layout and defects.** A layer is a finite set of closed polygons $P_1, \dots, P_m$ in a window $W \subset \mathbb{R}^2$ of finite area, and each polygon has a net label $\nu(P_i)$. Polygons with the same label are connected elsewhere, so touching them together does no harm. Let $B$ be a closed unit ball that is symmetric about the origin: the disk $\{z : \|z\|_2 \le 1\}$ or the square $\{z : \|z\|_\infty \le 1\}$. A *spot defect* of radius $r \ge 0$ centred at $c$ is the set $c + rB$. The square model of [Papadopoulou and Lee](/voronoi-critical-area-extraction/) makes every distance an $L_\infty$ distance and every region a union of polygons.

**Expansion.** Because $B = -B$, the defect $c + rB$ meets a polygon $P$ if and only if $c \in P \oplus rB$, the Minkowski sum of $P$ and $rB$. For a net $N$ let $E_N(r) = \bigcup_{\nu(P) = N} P \oplus rB$.

**Critical area for shorts.** An extra-material defect causes a short when it meets polygons of at least two different nets:

$$ A_{\mathrm{s}}(r) \;=\; \operatorname{area}\Big( W \cap \bigcup_{N \ne N'} \big( E_N(r) \cap E_{N'}(r) \big) \Big). $$

Equivalently, let $t(c)$ be the distance from $c$ to the second nearest net, with distance measured in the norm of $B$ and the nearest polygon of each net taken. Then a defect at $c$ shorts two nets if and only if $r \ge t(c)$, so $A_{\mathrm{s}}(r) = \operatorname{area}\{c \in W : t(c) \le r\}$. The value $t(c)$ is the *critical radius* of $c$.

**Critical area for opens.** A missing-material defect causes an open when the set $\bigcup_{\nu(P)=N} P \setminus (c + r\,\mathrm{int}\,B)$ has two terminals of net $N$ in different connected pieces. $A_{\mathrm{o}}(r)$ is the area of the set of such centres $c$ in $W$, over all nets. For a long straight wire of width $w$, away from its ends, this happens exactly when the defect covers a full cross section of the wire.

**Average critical area.** Let $f$ be the [probability density](/probability-density-function/) of the defect radius and $D$ the number of defects per unit area. The average critical area and the expected number of faults are

$$ \bar A \;=\; \int_0^\infty A(r)\, f(r)\, dr, \qquad \lambda \;=\; D\, \bar A. $$

Since $A(r) \le \operatorname{area}(W)$ for all $r$, the integral is finite. The ratio $A(r)/\operatorname{area}(W)$ is the *probability of failure* of a defect of radius $r$ whose centre is uniform on $W$.

**Size distribution.** Stapper's distribution, written for the radius with peak $r_0$, is

$$ f(r) = \begin{cases} r / r_0^2 & 0 \le r \le r_0, \\ r_0^2 / r^3 & r > r_0. \end{cases} $$

Each piece has mass $1/2$, so $f$ is a density. Since $x = 2r$ maps it to the same form in the diameter $x$ with peak $x_0 = 2r_0$, the radius and diameter conventions give the same model. The tail exponent 3 and the peak $r_0$ are fitted to defect monitor data of a fab, not derived.

## Examples and non-examples

**Two parallel wires, square defects.** Let the wires be $[0, L] \times [-w, 0]$ and $[0, L] \times [s, s + w]$, of different nets, with spacing $s > 0$ and nothing else in the window. A square $c + r[-1,1]^2$ meets an axis-parallel rectangle if and only if its $x$ range meets the rectangle's $x$ range and its $y$ range meets the rectangle's $y$ range. So $E_1(r) = [-r, L + r] \times [-w - r, r]$ and $E_2(r) = [-r, L + r] \times [s - r, s + w + r]$. Their intersection is $[-r, L + r] \times [s - r, r]$, which is empty when $2r < s$. Hence

$$ A_{\mathrm{s}}(r) \;=\; (L + 2r)\,(2r - s)^{+}, $$

where $(u)^{+} = \max(u, 0)$. For $L = 100$, $s = 1$ and $r = 1$ this is $102 \cdot 1 = 102$; for $r = 0.75$ it is $101.5 \cdot 0.5 = 50.75$.

**Two parallel wires, disk defects.** Same wires, Euclidean disks. For $0 \le x \le L$ the distance from $(x, y)$ to the lower wire is at most $r$ exactly when $-w - r \le y \le r$, and to the upper wire exactly when $s - r \le y \le s + w + r$, so the strip $0 \le x \le L$ contributes $L(2r - s)$. For $x < 0$ and $0 \le y \le s$ the nearest points of the two wires are the corners $(0, 0)$ and $(0, s)$. For $x < 0$ and $y < 0$, a point within $r$ of $(0, s)$ is within $r$ of $(0, 0)$ too, because $|y| < s - y$, and $(0,0)$ lies on the lower wire; the case $y > s$ is symmetric. So the part with $x < 0$ is the half of the lens $\{z : \|z\|_2 \le r,\ \|z - (0, s)\|_2 \le r\}$ on the side $x < 0$. The right end gives the other half. The lens of two disks of radius $r$ whose centres are $s$ apart has area $2r^2 \arccos\frac{s}{2r} - \frac{s}{2}\sqrt{4r^2 - s^2}$, so for $2r \ge s$

$$ A_{\mathrm{s}}(r) \;=\; L(2r - s) + 2r^2 \arccos\frac{s}{2r} - \frac{s}{2}\sqrt{4r^2 - s^2}, $$

and $A_{\mathrm{s}}(r) = 0$ for $2r < s$. For $L = 100$, $s = 1$ and $r = 1$ this is $100 + 2\pi/3 - \sqrt{3}/2 \approx 101.228$; for $r = 0.75$ it is $50.387$. The disk gives less than the square at each $r$, because the disk lies inside the square of the same radius.

**Average for a long pair.** Ignore the two ends, so $A_{\mathrm{s}}(r) = L(2r - s)^{+}$ for both shapes, and take $r_0 \le s/2$. Only the tail of $f$ contributes:

$$ \bar A_{\mathrm{s}} \;=\; \int_{s/2}^{\infty} L(2r - s)\,\frac{r_0^2}{r^3}\, dr \;=\; L r_0^2 \Big[ -\frac{2}{r} + \frac{s}{2r^2} \Big]_{s/2}^{\infty} \;=\; L r_0^2 \Big( \frac{4}{s} - \frac{2}{s} \Big) \;=\; \frac{2 L r_0^2}{s}. $$

For $L = 100$, $s = 1$ and $r_0 = 0.25$ this gives $\bar A_{\mathrm{s}} = 12.5$, about $1/8$ of the drawn area of the gap. In diameters it reads $L x_0^2 / (2s)$. Halving the spacing doubles the average critical area.

**Opens of one wire.** For a long wire $[0, L] \times [0, w]$, a square defect covers a full cross section exactly when its $y$ range contains $[0, w]$, that is $w - r \le c_y \le r$. A disk covers the cross section at $x = c_x$ under the same condition, and if $c_y > r$ or $c_y < w - r$ the band of the wire below or above the disk stays free and joins both sides. So, away from the ends, $A_{\mathrm{o}}(r) = L(2r - w)^{+}$ and $\bar A_{\mathrm{o}} = 2 L r_0^2 / w$ when $r_0 \le w/2$. Wide wires resist opens and wide spaces resist shorts, which is the trade that [dummy fill](/dummy-fill-problem/) and wire spreading work with.

**Non-example: the sum over pairs.** Three parallel wires of width $w = 1$ at spacing $s = 1$, on three nets, at $y \in [-1, 0]$, $[1, 2]$ and $[3, 4]$. Per unit length, for square defects of radius $r = 2$, the pairs (1,2), (2,3) and (1,3) have critical intervals $[-1, 2]$, $[1, 4]$ and $[1, 2]$ in $y$, of lengths 3, 3 and 1. Their sum, 7, is not the critical area. The critical area is the length of the union, $[-1, 4]$, which is 5. A centre that shorts three nets is one fault for the yield model, so the definition takes the union.

**Non-example: same net.** A defect that touches two polygons of the same net is not a short, even though it joins two shapes. A defect of radius $r < s/2$ between the two wires above touches at most one of them, so it is not critical at all.

**Non-example: the pair formula with its ends, over all sizes.** The square formula $(L + 2r)(2r - s)$ has the term $4r^2$, and $\int^{R} 4r^2 \cdot r_0^2 r^{-3}\, dr = 4 r_0^2 \ln R + \text{const}$ grows without bound. With $L = 100$, $s = 1$, $r_0 = 0.25$ and the integral stopped at $R = 1000$ the result is $14.14$, not $12.5$, and it keeps growing with $R$. The pair formula is valid for a pair alone in the plane; in a real window $A(r) \le \operatorname{area}(W)$ caps the integrand. An average computed from per-pair formulas needs either a largest defect size or the window cap.

## Related definitions

- The yield models turn $\lambda = D \bar A$ into a yield. The [Poisson yield model](/poisson-yield-model/) gives $e^{-\lambda}$ when the defect density is the same on every chip; the [Murphy](/murphy-yield-model/) and [negative binomial](/negative-binomial-yield-model/) models average that over a varying density.
- The critical radius $t(c)$ is a second-nearest-site distance, so $A_{\mathrm{s}}$ is read off the second order [Voronoi diagram](/voronoi-diagram/) of the polygons (an [order-k Voronoi diagram](/order-k-voronoi-diagram/) with $k = 2$, with nets as sites). [Voronoi critical area extraction](/voronoi-critical-area-extraction/) computes $A_{\mathrm{s}}(r)$ for all $r$ and $\bar A_{\mathrm{s}}$ from it.
- The minimum spacing rule of [design rule checking](/design-rule-checking/) sets the smallest $s$, so it bounds the smallest defect that can cause a short. Critical area extends that pass or fail rule to a measure of how much yield each spacing costs.
- A *via open* is the open of a single cut, whose critical area is the area where a defect removes the whole cut. [Redundant via insertion](/redundant-via-insertion/) adds a second cut so that one defect no longer opens the net.

## References
