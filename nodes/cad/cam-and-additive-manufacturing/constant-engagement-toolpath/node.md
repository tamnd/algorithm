---
tag: X9MBE5
kind: algorithm
slug: constant-engagement-toolpath
name: Constant engagement toolpath
aliases:
- adaptive clearing
- engagement angle control
area: cad/cam-and-additive-manufacturing
level: research
summary: Stori and Wright's and later toolpaths that bound the angle of tool engagement with the material by curved paths and medial axis spirals, for high-speed roughing.
solves: [pocket-machining]
model: real-ram
complexity:
  vars: {m: number of tool moves, n: number of samples on the front half circle, k: number of pixels in the box around one move}
  time: {worst: "O(m (n + k))"}
  space: {extra: "O(m)"}
properties: {deterministic: true, recursive: false}
history:
  year: 2000
  people: [J. A. Stori, P. K. Wright]
  note: Stori and Wright generated toolpaths with a constant engagement angle for convex pockets in 2000. Later methods use medial axis spirals and a simulated stock.
prereqs: [pocket-machining, toolpath-planning]
see_also: [trochoidal-milling, contour-parallel-toolpath, fermat-spiral-toolpath, voronoi-pocket-machining, medial-axis, feedrate-scheduling, z-map-model, nc-verification]
sources:
  - paper: "J. A. Stori and P. K. Wright, Constant engagement tool path generation for convex geometries, Journal of Manufacturing Systems 19(3), 172-184, 2000"
    locator: the engagement angle of a tool on a curved path and the construction of offsets that keep it constant
  - paper: doi:10.1016/j.cad.2004.05.008
    title: Gershon Elber, Elaine Cohen and Sam Drake, MATHSM, medial axis transform toward high speed machining of pockets, Computer-Aided Design 37(2), 241-250, 2005
    locator: the spiral paths built on the medial axis that limit the change of engagement in a pocket
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: the material on pocket machining and the stock models used for simulation
---

A constant engagement toolpath is a roughing path for [pocket machining](/pocket-machining/) along which the angle of the tool circle that is in contact with the material stays near a chosen value. The engagement angle sets the load on the tool and the chip thickness. An ordinary [contour-parallel path](/contour-parallel-toolpath/) keeps the distance between passes constant, so the engagement jumps at inner corners and grows on curves that bend toward the material, and the feed must be set for the worst case. A constant engagement path changes the distance between passes instead, so the tool can run at a high feed everywhere. Stori and Wright gave the first construction in 2000, for convex shapes. Commercial systems call the idea adaptive clearing. The version here grows the path step by step: it keeps a pixel model of the stock and, at each step, turns the tool until the measured engagement equals the target.

## In plain words

A cutter that moves through a block of metal touches the uncut metal along part of its edge. The size of that part is the engagement. A big engagement is a heavy load, and a small one wastes time.

If the cutter goes round a pocket in rings that are always the same distance apart, the load is not steady. In a corner or on a bend the cutter suddenly bites much more.

So the method does not fix the distance. It keeps a picture of the metal that is left. Before each small move, it looks at how much of the cutter edge would touch metal in each direction it could go. Then it steers toward the metal or away from it until the touch is just right, makes the move, and erases the metal it cut from the picture.

## The problem

The tool is a disk of radius $R$ that moves in the plane. At the center $c$ with the feed direction $\psi$, the front half circle is the set of points $c + R(\cos t, \sin t)$ with $|t - \psi| \le 90°$. The engagement angle $\theta(c, \psi)$ is the measure of the part of the front half circle that lies in the remaining material. Given the initial material, a start point, a start heading and a target $\theta^*$, the task is to produce a sequence of tool moves along which $\theta$ stays close to $\theta^*$ and the material is removed.

Two closed forms set the scale. For a straight cut that leaves a wall at the radial depth $a$ inside the tool,
$$
\theta = \arccos(1 - a/R).
$$
For a tool on a circle of radius $\rho$ that cuts into material outside the radius $R_b$ about the same center,
$$
\cos\theta = \frac{R_b^2 - \rho^2 - R^2}{2\rho R}.
$$
So for a fixed stepover $s$, with $R_b = \rho - s + R$, the engagement on a circle is larger than on a straight line, and it grows as $\rho$ falls. To keep $\theta = \theta^*$, the stepover must be
$$
s = \rho + R - \sqrt{\rho^2 + R^2 + 2\rho R\cos\theta^*},
$$
which is smaller on tight curves. Both formulas are proved in the proof file.

## The algorithm

The generator below moves the tool by a fixed step $\sigma$. The material lies on the side `side` of the path, $+1$ for the left and $-1$ for the right. Let $E(\varphi)$ be the engagement, sampled at $n$ points of the front half circle in the pixel stock, at the point $c + \sigma(\cos\varphi, \sin\varphi)$ with the heading $\varphi$.

```pseudo id=main
CONSTANT-ENGAGEMENT-PATH(stock, c, ψ, R, θ*, σ, Δ, m, side)
L1  repeat m times
L2      E(φ) ← sampled engagement at c + σ(cos φ, sin φ) with heading φ
L3      toward ← ψ + side·Δ;  away ← ψ − side·Δ   ▷ the turn limits
L4      if E(away) ≥ θ* then φ ← away            ▷ too much material even when turning away
L5      else if E(toward) ≤ θ* then φ ← toward   ▷ too little even when turning in
L6      else bisect φ between toward and away 12 times so that E crosses θ*
L7      remove the capsule of radius R around the segment c to c + σ(cos φ, sin φ) from the stock
L8      append (c + σ(cos φ, sin φ), φ, E(φ)) to the path; c, ψ ← that point, φ
L9  return the path
```

Turning toward the material raises the engagement, and turning away lowers it. Line L6 keeps a bracket $\ell, h$ with $E(\ell) > \theta^* \ge E(h)$. The stock is a grid of pixels of side $d$. A pixel is cut when its center is within $R$ of the move segment, so the stock always equals the initial material minus the swept capsules, at pixel resolution.

## Example

The tool has $R = 5$, and the target is $60°$. On a straight wall, $60°$ needs the depth $a = R(1 - \cos 60°) = 2.5$. On a circle of radius $\rho = 10$, the same angle needs the stepover $s = 15 - \sqrt{175} = 1.771$, and the stepover 2.5 gives $\arccos(0.3125) = 71.79°$ instead. The table compares the pixel engagement, with $d = 0.2$ and $n = 60$ samples of $3°$, with the closed form for some circles.

| $\rho$ | $s$ | pixel | closed form | straight cut with the same $s$ |
|---|---|---|---|---|
| 8 | 1 | $48°$ | $46.57°$ | $36.87°$ |
| 10 | 2 | $63°$ | $63.90°$ | $53.13°$ |
| 15 | 2 | $60°$ | $60.44°$ | $53.13°$ |
| 25 | 3 | $72°$ | $71.58°$ | $66.42°$ |

In the test run, the stock is the square $[-26, 26]^2$ with a round hole of radius 8 cut in the middle, and the tool starts at $(3, 0)$, heading up, with the material on its right. The step is $\sigma = 0.5$ and the turn limit is $\Delta = 15°$. In 600 steps the tool spirals out from the radius 5.64 to 13.33, and from step 100 on the engagement stays between $60°$ and $63°$. An Archimedean spiral with the fixed pitch 2.5, the straight-cut stepover for $60°$, cut to the same radius in the same stock, has engagements from $63°$ to $78°$ after the same warm-up. Started on a straight wall at the depth 1, the generator turns into the material and settles at the depth 2.5.

## Correctness

The proof file proves the straight and circular closed forms and the stepover formula. For the generator it proves what a single step does. The stock invariant holds: after each step the pixel stock is exactly the initial material minus the pixels within $R$ of the segments cut so far. The new heading is within $\Delta$ of the old one. When the target lies between $E(\text{away})$ and $E(\text{toward})$, the bisection returns a heading inside an interval of width $2\Delta/2^{12}$ on which the sampled engagement crosses the target. The generator stops after $m$ steps.

**What is proved and what is measured.** The step is proved, but the path as a whole is not. No result here says that the engagement stays near the target over many steps, that the path leaves no islands of material, or that it clears the pocket. The tests measure these things. The generator holds $60°$ to $63°$ after a warm-up, which is within one sample of the target. It does more than twice as well as a fixed-pitch spiral. The pixel engagement is within two samples of an engagement computed with exact rational arithmetic from the true union of the cut capsules. It is within one sample plus $2°$ of the closed forms on straight and circular cuts.

## Complexity

One evaluation of $E$ looks at $n$ points, each in $O(1)$ time. Each step evaluates $E$ at most 15 times and cuts one capsule, which visits the $k$ pixels in a box around the segment, about $(2R + \sigma)(2R)/d^2$ of them. So $m$ steps take $O(m(n + k))$ time. The stock takes the space of its pixel grid, which the caller provides, and the path takes $O(m)$ space. In practice the stock is the main cost. A finer grid gives a more accurate engagement and costs quadratically more per cut.

## Properties

- **Steady load.** The engagement stays close to the target wherever the turn limit allows the path to follow the material.
- **Variable stepover.** The distance between passes is not constant. It shrinks on curves that bend toward the material and in corners.
- **Stock driven.** The path depends on the actual remaining material, so it handles rest material and partly cut regions.
- **Local and greedy.** Each step looks only at the next move. Nothing in the method plans the whole pocket.

## Variants and improvements

- **Offset construction.** Stori and Wright built each pass as a curve at the stepover of the stepover formula from the previous one, for convex shapes, with no stock model.
- **Medial axis spirals.** Elber, Cohen and Drake grow a spiral out from the [medial axis](/medial-axis/) of the pocket, so that the passes change slowly and the engagement does not jump. [Fermat spiral](/fermat-spiral-toolpath/) and [Voronoi](/voronoi-pocket-machining/) paths are related.
- **Stock models.** A pixel grid is the simplest stock. A [z-map](/z-map-model/), a polygon model of the stock boundary, or a [distance transform](/distance-transform/) gives the engagement faster or more accurately.
- **Feed adjustment.** Instead of changing the path, a planner can keep the path and change the feed to keep the chip thickness constant. This is a case of [feedrate scheduling](/feedrate-scheduling/).
- **Trochoidal moves.** Where the stepover would have to be very small, for example in a narrow slot, many systems switch to [trochoidal milling](/trochoidal-milling/).

## When to use it

Use a constant engagement path for roughing of pockets and open regions in hard materials at high speed, where tool load decides the tool life, and the machine can follow smooth curves at a high feed. In a soft material at a low speed, a simple contour-parallel or zigzag path is shorter and often faster.

**Difference from trochoidal milling.** [Trochoidal milling](/trochoidal-milling/) is a fixed geometric pattern: a circle of loops that moves forward along a slot, with the same shape everywhere. It bounds the engagement by making the loops small, and the engagement still varies within each loop, from zero on the return to its highest value as the tool comes round to the front. A constant engagement path is computed from the stock, so its shape changes with the material, and it aims to keep the engagement at one value along the whole path.

## Pitfalls

- **Islands of material.** A greedy path can leave thin islands or uncut regions between passes. A real system needs a final check of the stock and clean-up moves.
- **Pixel noise.** The sampled engagement moves in steps of $180°/n$, and a coarse grid shifts the boundary by up to a pixel. Choose $d$ much smaller than the stepover.
- **The turn limit.** A small $\Delta$ keeps the path smooth but cannot follow sharp corners, so the engagement rises there. A large $\Delta$ gives a path that zigzags, which the machine cannot follow at full feed.
- **Engagement is not the only load.** The axial depth, the chip thinning at small angles and the machine dynamics also matter. A constant angle does not mean a constant force.
- **Air moves.** Where there is no material, the engagement is zero, and the generator turns toward the material at the turn limit. It needs a rule to link to the next region.

## Implementations

## History

High-speed machining in the 1990s made tool load a main concern of roughing. Stori and Wright (2000) defined the constant engagement problem for pockets and gave an offset construction for convex shapes. Elber, Cohen and Drake (2005) used the medial axis to build spirals whose passes change slowly. Through the 2000s CAM systems added roughing strategies that compute the path from a model of the remaining stock and keep the engagement or the chip thickness within bounds. They are sold under names such as adaptive clearing.

## References
