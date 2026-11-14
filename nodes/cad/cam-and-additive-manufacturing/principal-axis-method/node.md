---
tag: WFBXPX
kind: algorithm
slug: principal-axis-method
name: Principal axis method
aliases:
- Rao-Ismail-Bedi method
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Five-axis method of Rao, Bedi and coauthors that tilts a toroidal or flat end mill in the minimum curvature plane so its effective radius matches the maximum curvature.
solves: [five-axis-tool-orientation]
model: real-ram
complexity:
  vars: {m: number of cutter contact points}
  time: {worst: "O(m)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, recursive: false}
history:
  year: 1996
  people: [N. Rao, Sanjeev Bedi, Ralph O. Buchal, Fathy Ismail]
  note: Rao, Bedi and Buchal described an implementation of the method in 1996, and Rao, Ismail and Bedi studied how the feed direction changes the result in 1997.
prereqs: [surface-curvature, cutter-location-data, gouge-detection]
see_also: [five-axis-tool-orientation, scallop-height, iso-scallop-toolpath, lines-of-curvature, offset-surface, flank-milling, collision-free-tool-orientation, accessibility-cone]
sources:
  - paper: doi:10.1016/S0890-6955(96)00046-6
    title: N. Rao, F. Ismail and S. Bedi, Tool path planning for five-axis machining using the principal axis method, International Journal of Machine Tools and Manufacture 37(7), 1025-1040, 1997
    locator: the principal axis method and the comparison of tool paths with different feed directions
  - paper: "N. Rao, S. Bedi and R. Buchal, Implementation of the principal-axis method for machining of complex surfaces, The International Journal of Advanced Manufacturing Technology 11(4), 249-257, 1996"
    locator: the tilt of the tool in the plane of minimum curvature and the effective radius of the tool in the plane of maximum curvature
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: the material on tool positioning for five-axis machining with flat and toroidal end mills
---

The principal axis method (PAM) chooses the [tool orientation](/five-axis-tool-orientation/) of a flat or toroidal end mill at each cutter contact point in five-axis milling. It tilts the tool axis away from the surface normal in the plane of minimum curvature, by the smallest angle at which the tilted tool, seen along the feed direction, curves as much as the surface does in the plane of maximum curvature. The tilted flat bottom then fits the surface across the feed much more closely than a ball end mill of the same size, so each pass cuts a wider strip and fewer passes are needed for a given [scallop height](/scallop-height/). This is a manufacturing method of mechanical CAD: it decides how a cutter is held against a part. It is not about the placement and routing of a circuit. The tilt comes from one formula in the [principal curvatures](/surface-curvature/), and on a concave cylinder the formula is exact: it gives the smallest tilt that does not gouge, and the closest fit.

## In plain words

A flat-bottomed cutter held straight up against a curved hollow touches it with its sharp rim and leaves deep ridges. A round-ended cutter fits better, but it cuts only a narrow band at a time.

Tip the flat cutter forward a little, in the direction along which the surface is nearly straight. Seen from the front, its round bottom edge now looks like a flat oval. For a small tip the oval is very flat, and its bottom is a wide, gentle curve.

The method picks the tip at which the bottom of the oval curves exactly as much as the hollow does across. Tip less and the oval digs in at the sides. Tip more and it stands away from the surface and leaves more material. At the right tip the cutter hugs the hollow over a wide band.

## The problem

At a cutter contact point $p$ the surface has the unit normal $n$, pointing to the tool, the principal directions $e_{\min}$ and $e_{\max}$, and the normal curvatures $\kappa_{\min} \le \kappa_{\max}$, with a positive curvature where the surface bends toward the tool (a concave part). The tool is a toroidal end mill: its center circle, the circle of the centers of the corner arcs, has radius $R$ and lies at height $r$ above the tip, where $r$ is the corner radius. A flat end mill is the case $r = 0$. The task is to choose the tool axis $a$ and the tip position $c$ so that the tool touches $p$ with normal $n$, does not cut into the surface near $p$, and leaves as little material as possible across the feed. This is one case of the [five-axis tool orientation](/five-axis-tool-orientation/) problem, solved locally at each point.

The key quantity is the effective radius of the tool. Tilt the axis by the angle $\lambda$ from $n$ toward $e_{\min}$, and look along $e_{\min}$. The center circle projects to an ellipse with semi axes $R$ and $R\sin\lambda$, whose radius of curvature at its lowest point is $R^2/(R\sin\lambda) = R/\sin\lambda$. The corner adds $r$, so the tool cuts a profile with the radius
$$
R_{\text{cut}}(\lambda) = \frac{R}{\sin\lambda} + r
$$
in the plane of maximum curvature. A profile with a smaller radius than the surface, $1/\kappa_{\max}$, leaves a small gap. A profile with a larger radius gouges the sides.

## The algorithm

```pseudo id=main
PRINCIPAL-AXIS-METHOD(p, n, e_min, κ_max, R, r, λ_min)
L1  if κ_max ≤ 0 then                          ▷ convex or flat across the feed
L2      λ ← λ_min
L3  else ρ ← 1/κ_max                            ▷ radius of the surface across the feed
L4      if R > ρ − r then fail: no tilt avoids a gouge
L5      λ ← max(arcsin(R/(ρ − r)), λ_min)       ▷ R/sin λ + r = ρ
L6  a ← cos λ · n + sin λ · e_min               ▷ tilt in the plane of minimum curvature
L7  e ← cos λ · e_min − sin λ · n               ▷ in the tip plane, toward the contact
L8  c ← p + r n − r a − R e                     ▷ tip center; the corner touches p
L9  return (λ, a, c)
```

Line L5 solves $R_{\text{cut}}(\lambda) = \rho$. Line L8 puts the lowest corner center at $p + r n$, so the corner arc touches $p$ with normal $n$. The tool feeds along $e_{\min}$ in the basic method, so the swept cross-section is the effective profile in the plane of $n$ and $e_{\max}$. The lower bound $\lambda_{\min}$ keeps the center of the flat bottom, where the cutting speed is zero, off the surface, and it is the tilt used on convex parts, where any tilt is free of local gouges.

## Example

A toroidal end mill of diameter 20 mm has $R = 8$ and $r = 2$. It cuts the inside of a cylinder of radius $\rho = 50$, feeding along the axis. At the bottom, $n = (0, 0, 1)$, $e_{\min} = (1, 0, 0)$ and $\kappa_{\max} = 0.02$.

| line | value |
|---|---|
| L3 | $\rho = 50$, and $R = 8 \le \rho - r = 48$ |
| L5 | $\sin\lambda = 8/48 = 1/6$, $\lambda = 9.594°$ |
| L6 | $a = (0.1667, 0, 0.9860)$ |
| L7 | $e = (0.9860, 0, -0.1667)$ |
| L8 | $c = (-8.2214, 0, 1.3613)$ |

The effective radius is $R/\sin\lambda = 48$, and with the corner the cut profile has radius 50, equal to the surface. The table below gives the width of the strip across the feed in which the vertical gap between the tool and the surface is at most $h = 0.01$, computed by sampling the swept profile.

| tool and tilt | strip width for $h = 0.01$ |
|---|---|
| toroidal, $\lambda = 9.594°$ (PAM) | 8.06 |
| toroidal, $\lambda = 12°$ | 3.98 |
| toroidal, $\lambda = 15°$ | 2.74 |
| toroidal, $\lambda = 20°$ | 2.02 |
| ball end mill of radius 10 | 1.00 |

A tilt below $9.594°$ gouges the sides. For the ball, the effective radius against the concave surface is $1/(1/10 - 1/50) = 12.5$, and the strip is $2\sqrt{2 \cdot 12.5 \cdot 0.01} \approx 1.00$ wide. The PAM strip is eight times wider. The reason is the order of contact: at the PAM tilt the clearance grows like the fourth power of the distance from the contact, and at any other tilt it grows like the square.

## Correctness

**Theorem.** Take a concave circular trough of radius $\rho$, feed along its axis with a fixed tool axis, and a toroidal end mill with $2R + 2r < \rho$. The tool placed by lines L6 to L8 at tilt $\lambda$ makes no gouge if and only if $\sin\lambda \ge R/(\rho - r)$. At every point of the cutting edge the clearance to the surface grows with $\lambda$, so the tilt of line L5 is the smallest tilt without a gouge and the closest fit at every point of the edge. At that tilt the cut profile has the radius $\rho$ at the contact, and the clearance is of fourth order in the distance from it.

The proof is in the proof file. The distance of a tool point from the axis of the trough decides a gouge, and by the triangle inequality the worst point is a corner center plus $r$. For the corner center at angle $t$, with $u = 1 - \cos t$ and $b = R\sin\lambda$,
$$
D(t)^2 - (\rho - r)^2 = u\big[\,2\big(R^2 - (\rho - r) b\big) - u (R^2 - b^2)\big],
$$
which is at most 0 for all $t$ exactly when $(\rho - r) b \ge R^2$. The derivative in $b$ is negative, which gives the monotone clearance. At equality the first term vanishes, and the clearance is $u^2 (R^2 - b^2)/(2(\rho - r))$ to leading order.

The model is stated in full: a cylinder, a feed along the zero-curvature direction, and a tool axis that does not turn during the pass. On a general surface the formula only matches the second-order shape of the surface at $p$, and nothing is proved about points away from $p$. The tests check the theorem by a grid search over tilts that uses a direct 3D test of the placed tool in the trough and no curvature formula, and by exact rational arithmetic at the tilt $\sin\lambda = 7/25$, where the tool touches the trough at one point of its edge and nowhere goes in.

## Complexity

Each contact point costs $O(1)$ arithmetic after the principal curvatures and directions are known, which for a parametric surface is also $O(1)$ from the first and second derivatives. A path of $m$ contact points takes $O(m)$ time and $O(1)$ extra space. The real cost of a PAM tool path is elsewhere: in the global gouge and collision checks that the local formula does not cover, and in choosing the paths and the step between them.

## Properties

- **Local.** The tilt depends only on the curvature at the contact point.
- **Exact on cylinders.** On a concave cylinder with the feed along the axis, the tilt is the smallest that does not gouge and gives the closest fit.
- **Wide strips.** At the matched tilt the clearance is of fourth order across the feed, so the strip for a given scallop height is much wider than for a ball end mill.
- **Needs concavity across the feed.** On convex or flat parts there is nothing to match, and the method falls back to the minimum tilt.

## Variants and improvements

- **Inclined tool method.** The older inclined tool method tilts a flat or toroidal end mill by a fixed angle in the feed direction. PAM replaces the fixed angle by the curvature-matched one and ties the tilt to the principal directions.
- **Feed direction.** Rao, Ismail and Bedi (1997) compared tool paths with different feed directions while the tilt follows the principal axes. Feeding along the minimum curvature direction makes the swept section equal to the effective profile of the theorem.
- **Multi-point machining.** Later methods tilt and rotate the tool so that it touches the surface at two points instead of one, which gives a still wider strip on some surfaces.
- **Rolling ball and arc-intersect methods.** These methods of the same school choose the axis from a circle that fits the surface, and they target global gouges as well as local ones.
- **Iso-scallop paths.** The effective radius gives the scallop height between passes, so PAM can feed an [iso-scallop](/iso-scallop-toolpath/) path planner.

## When to use it

Use PAM for five-axis finishing of large, gently curved parts that are concave across the feed, such as dies, molds and turbine passages, with a flat or toroidal end mill. Use a ball end mill, or a gouge-checked method such as a multi-point method, where the curvature changes fast or where the part is small compared with the tool.

## Pitfalls

- **Matching only at one point.** The formula matches the curvature at $p$. If the curvature changes within the width of the tool, the tool can gouge at the edge of the strip. Check the result with [gouge detection](/gouge-detection/).
- **Global gouges and collisions.** The tilted tool and its holder can hit other parts of the surface. PAM does not see this, so an [accessibility](/accessibility-cone/) or [collision-free orientation](/collision-free-tool-orientation/) step is still needed.
- **Too wide a tool.** If $R > 1/\kappa_{\max} - r$, no tilt avoids a gouge. Use a smaller tool or a ball end mill there.
- **Umbilic points.** Where $\kappa_{\min} = \kappa_{\max}$, the principal directions are not defined, and the tilt direction can jump. Smooth the directions or fix the feed direction near such points.
- **Sign of curvature.** The formula needs the curvature with the sign that is positive for a concave part, as seen from the tool. With the other sign the method tilts on a convex part and wastes the fit.
- **Feed curvature.** The theorem assumes zero curvature along the feed. A curved feed direction also bends the swept volume, and the effective profile changes.

## Implementations

## History

The inclined tool method of the 1980s tilted a flat end mill by a fixed angle so that its rim fitted the surface better than a ball. Rao, Bedi and Buchal (1996) described an implementation of the principal axis method, which ties the tilt to the principal curvature directions and matches the effective radius to the maximum curvature, and Rao, Ismail and Bedi (1997) used it to study how the feed direction changes five-axis tool paths, with machining tests on two surfaces. The group at the University of Waterloo later developed the multi-point, rolling ball and arc-intersect methods from the same idea of fitting the tool to the local shape of the part.

## References
