---
tag: 3RSRW5
kind: technique
slug: trochoidal-milling
name: Trochoidal milling
aliases:
- trochoidal toolpath
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Moves the tool on circles that advance along a slot or path, so the radial engagement stays small, which allows high cutting speeds and long tool life.
prereqs: [toolpath-planning, pocket-machining]
see_also: [constant-engagement-toolpath, contour-parallel-toolpath, fermat-spiral-toolpath, feedrate-scheduling, cutter-location-data, scallop-height]
sources:
  - paper: doi:10.1016/j.ijmachtools.2006.08.002
    title: Murat Otkur and Ismail Lazoglu, Trochoidal milling, International Journal of Machine Tools and Manufacture 47(9), 1324-1332, 2007
    locator: the model of the contact between the tool and the workpiece, the engagement angle along a trochoidal path, and the dual trochoidal path
  - paper: doi:10.1016/j.ijmachtools.2008.12.006
    title: Matthieu Rauch, Emmanuel Duc and Jean-Yves Hascoet, Improving trochoidal tool paths generation and implementation using process constraints modelling, International Journal of Machine Tools and Manufacture 49(5), 375-383, 2009
    locator: the choice of the trochoidal parameters, the maximum radial depth of cut, and the execution of the path on CNC machines
  - paper: "J. A. Stori and P. K. Wright, Constant engagement tool path generation for convex geometries, Journal of Manufacturing Systems 19(3), 172-184, 2000"
    locator: the engagement angle as the measure of tool load in high-speed milling
---

Trochoidal milling cuts a slot, or the material along any path, by moving the tool center on a sequence of small circles that advance a little along the path at each turn. The tool never cuts the full width of the slot at once. In each loop it takes a thin, crescent-shaped bite from the front of the cut and then returns through the empty slot. The radial engagement stays small, so the tool can run at a high cutting speed and a high feed with a long tool life, and the slot can be wider than the tool. The price is a long path: most of each loop moves through air. Trochoidal milling is a pattern laid on a path, not a search. Its two parameters, the loop radius and the advance per loop, decide the slot width, the largest engagement and the ridges left on the wall. This page gives the formulas for these and shows how to choose the parameters.

## In plain words

Cutting a groove in one straight pass makes the cutter bite with half its edge at once. That is a heavy load, and in hard metal it breaks or wears the cutter fast.

Instead, move the cutter round in small circles, and move the circles slowly forward. Each circle shaves only a thin sliver off the front of the groove, and then the cutter swings back through the empty groove before the next sliver.

Each bite is small, so the cutter can spin and move much faster. The groove can also be wider than the cutter. The cost is that the cutter travels a long way, and much of that travel cuts nothing.

## When it applies

- **Slots and narrow channels in hard materials.** Full slotting gives the engagement $180°$, which is the worst case for heat and tool wear. Trochoidal milling bounds the engagement by the choice of the pitch.
- **High-speed machines.** The method needs a machine that keeps a high feed on small circles. Its benefit comes from cutting speed and tool life, and the long path makes it slower than slotting on a slow machine or in a soft material.
- **Rest material and corners.** Where a [contour-parallel path](/contour-parallel-toolpath/) would bury the tool in a corner, a few trochoidal loops clear it with a bounded load.
- **A slot wider than the tool.** The slot width is $2(\rho + R)$, so a tool of radius $R$ can cut any width above $2R$ by the choice of the loop radius $\rho$.
- **Not useful** for open areas with no walls on both sides. There a [constant engagement path](/constant-engagement-toolpath/) cuts on most of its length and wastes less time in air.

## The template

The spine is the path along which the slot runs, given by arc length $u \in [0, \ell]$, with unit tangent $T(u)$ and left normal $N(u)$. The loop radius is $\rho$, the pitch (the advance per loop) is $p$, and each loop is cut into $k$ moves.

```pseudo id=main
TROCHOIDAL-PATH(spine, ℓ, ρ, p, k)
L1  θ ← 0;  path ← empty
L2  while pθ/(2π) ≤ ℓ
L3      u ← pθ/(2π)                         ▷ the spine advances by p per loop
L4      T, N ← unit tangent and left normal of the spine at u
L5      append spine(u) + ρ (cos θ · T + sin θ · N) to path
L6      θ ← θ + 2π/k
L7  return path
```

On a straight spine along the $x$ axis, line L5 gives the trochoid
$$
c(\theta) = \Big(\frac{p\theta}{2\pi} + \rho\cos\theta,\; \rho\sin\theta\Big),
$$
which is a circle of radius $\rho$ whose center moves forward at the rate $p$ per turn.

**Slot width.** The tool reaches $y = \rho + R$ at $\theta = 90°$ and $y = -(\rho + R)$ at $\theta = 270°$, and the center never goes farther from the spine than $\rho$. So the slot has the width $2(\rho + R)$.

**Engagement at the front.** Treat each loop as a circle of radius $\rho$, and the previous loop as one $p$ behind it. The previous loop has cut all points within $\rho + R$ of its center. At the front of the new loop the tool center is at the distance $\rho + p$ from that center and moves at right angles to the line between them. The engagement there is
$$
\cos\alpha_{\text{front}} = \frac{(\rho + R)^2 - (\rho + p)^2 - R^2}{2(\rho + p)R}.
$$
This is the formula for a tool on a circle of radius $\rho + p$ that cuts material outside the radius $\rho + R$. Its proof is on the [constant engagement](/constant-engagement-toolpath/) page. The largest engagement in a loop is a little higher, and it comes a little before the front. The example gives numbers.

**Wall ridges.** In the same circle model, the wall is a row of arcs of radius $\rho + R$, $p$ apart, so the ridges on the wall have the height $h = (\rho + R) - \sqrt{(\rho + R)^2 - p^2/4}$. This is the same formula as the [scallop height](/scallop-height/) of a ball between passes.

**Example.** Take $R = 5$, $\rho = 3$ and $p = 1$. The slot is 16 wide. The front formula gives $\cos\alpha = (64 - 16 - 25)/40 = 0.575$, so $\alpha_{\text{front}} = 54.90°$. A scan of the loop in the circle model, with $0.5°$ samples, finds the largest engagement $60.0°$ at $\theta \approx 314°$, which is $46°$ before the front. A direct computation on the true trochoid, with the material removed by all earlier positions of the tool, gives $56°$ at the front, a largest value of $59°$ at $\theta \approx 318°$, and zero engagement on 46% of the loop, from about $100°$ to $260°$. The loop is 18.86 long, against $2\pi\rho = 18.85$ for a circle. The wall ridges are $0.0156$ high in the circle model and $0.0163$ on the true trochoid. The table shows how the pitch trades the load against the material removed per unit length of the path, which is $2(\rho + R)p$ divided by the loop length.

| pitch $p$ | $\alpha_{\text{front}}$ | largest $\alpha$ in a loop (circle model) | area removed per unit of path | wall ridge $h$ |
|---|---|---|---|---|
| 0.5 | $40.16°$ | $42.0°$ | 0.424 | 0.0039 |
| 1 | $54.90°$ | $60.0°$ | 0.848 | 0.0156 |
| 2 | $73.74°$ | $86.0°$ | 1.693 | 0.0627 |
| 3 | $87.13°$ | $107.5°$ | 2.530 | 0.1419 |

For comparison, a straight side cut with the same tool and the engagement $60°$ has the radial depth 2.5 and removes 2.5 per unit of path, three times as much as the trochoid with $p = 1$. Full slotting removes the whole width of the cut at $180°$. Trochoidal milling buys a bounded load in a slot at the cost of most of the path length.

## Classic examples

- **Slotting in hardened steel and titanium.** Narrow slots in dies and in aircraft parts are cut with trochoidal loops so that the tool takes a small radial bite at a high speed.
- **Pocket corners and rest material.** CAM systems switch to trochoidal loops where the engagement of a pocket path would rise, for example at inner corners and in narrow parts of a pocket.
- **Dual trochoidal paths.** Otkur and Lazoglu analyzed the contact between the tool and the workpiece and proposed a path with two trochoidal parts to cut more efficiently.
- **Process-based parameter choice.** Rauch, Duc and Hascoet chose the pitch and loop radius from the maximum radial depth of cut and studied how the machine executes the small circles.

## Variations

- **Circle and line loops.** Many CAM systems replace each loop by a circular arc for the cut and a straight return, which shortens the time in air.
- **Curved spines.** Along a curved spine, the loops on the outside of the bend are farther apart than $p$ and those on the inside are closer. The engagement then rises on the side that bends toward the material, by the circular formula of the [constant engagement](/constant-engagement-toolpath/) page. A planner can reduce $p$ on such bends.
- **Variable pitch.** The pitch can change along the spine to hold the largest engagement, from the table above or from a stock model.
- **Feed control in the loop.** The feed can be higher on the empty return and lower in the cut, by [feedrate scheduling](/feedrate-scheduling/).
- **Spiral and Fermat paths.** For open pockets, spiral paths such as the [Fermat spiral](/fermat-spiral-toolpath/) keep the tool in the cut and avoid the empty returns.

**Difference from constant engagement.** A trochoidal path is a fixed geometric pattern with the same shape in every loop, chosen before cutting from $R$, $\rho$ and $p$. It bounds the largest engagement, but within each loop the engagement still goes from zero to the largest value and back. A [constant engagement path](/constant-engagement-toolpath/) is computed from the remaining stock, its shape follows the material, and it tries to hold the engagement at one value along the whole path. The two are often used together: constant engagement in open regions and trochoidal loops in slots and narrow passages.

## Pitfalls

- **Too large a pitch.** The largest engagement grows fast with $p$. In the example it passes $100°$ at $p = 3$, and the method then gives no benefit over slotting.
- **The front formula is not the largest value.** The largest engagement in a loop comes before the front and is several degrees higher. Use a scan of the loop, as in the example, to set the pitch.
- **Machine dynamics.** Small circles at a high feed need a high centripetal acceleration, $v^2/\rho$. If the machine cannot follow, it slows down, and the high speed that the method relies on is lost. Check the feed against the limits of the machine.
- **Speed of the center.** The center of the tool moves with the speed $\rho\omega \pm p\omega/(2\pi)$ along a trochoid, so a constant rate of loops does not give a constant feed. Program the feed along the path, not the loop rate.
- **Islands in the middle.** If $\rho > R$, a single loop leaves an uncut island of radius $\rho - R$ in its center. Later loops cut it, but the first and last loops of a slot need care.
- **Air time.** Nearly half of each loop cuts nothing. On a slow machine or in a soft material, slotting or a [contour-parallel path](/contour-parallel-toolpath/) is faster.

## Exercises

1. Derive the front engagement formula from the distance of a point of the tool circle to the center of the previous loop.
2. Show that the speed of the center along the straight trochoid lies between $\rho\omega - p\omega/(2\pi)$ and $\rho\omega + p\omega/(2\pi)$, where $\omega$ is the loop rate.
3. For $R = 5$ and $\rho = 3$, find the pitch at which the front engagement is $45°$, and compare the removal per unit of path with a straight side cut at $45°$.
4. Explain why the circle model and the true trochoid give slightly different wall ridges, and which one is larger.

## References
