---
tag: RAY63F
kind: algorithm
slug: inverse-tool-offset
name: Inverse tool offset
aliases:
- ITO method
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Computes cutter locations on a grid that do not gouge the sampled part, as the highest inverted tool placed at each sample, after Kishinami, Kondo and Saito.
solves: [toolpath-planning]
model: real-ram
complexity:
  vars: {n: number of grid points, k: number of grid points in the tool footprint}
  time: {worst: "O(n k)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1988
  people: [Takeshi Kishinami, Tsukasa Kondo, Katsumasa Saito]
  note: Kondo, Kishinami and Saito described a machining system built on the inverse offset method, which places the inverted tool at every point of the part and keeps the upper envelope as the cutter location surface.
prereqs: [cutter-location-data, z-buffer, morphological-dilation]
see_also: [z-map-model, gouge-detection, offset-surface, dexel-representation, iso-planar-toolpath, scallop-height, mathematical-morphology, nc-verification]
sources:
  - paper: doi:10.2493/jjspe.54.971
    title: Tsukasa Kondo, Takeshi Kishinami and Katsumasa Saito, Machining system based on inverse offset method, Journal of the Japan Society for Precision Engineering 54(5), 971-976, 1988
    locator: the inverse offset of the tool over the part and the cutter location surface built from it
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: the chapters on the computation of cutter location data for sculptured surfaces, where the inverse tool offset method is presented
---

The inverse tool offset (ITO) method computes the [cutter location](/cutter-location-data/) of a tool that moves straight down onto a part, at every point of a grid. It does not ask where the tool touches the part. Instead it turns the tool upside down, puts this inverted tool at every sample point of the part, and keeps the highest of all these shapes at each grid point. The upper envelope is the surface on which the tool tip can move without cutting into any sample, which is the cutter location surface of three-axis machining. The method works the same for every part, however many patches, holes or steep walls it has, because it only needs heights. This is a manufacturing method of mechanical CAD: placement and routing here mean where a cutter goes and how it moves, not the placement and routing of a circuit. The code computes the envelope on a height grid by scattering, as a [z-buffer](/z-buffer/) does, and it checks it against a direct maximum over all samples.

## In plain words

Press a ball down onto a bumpy surface until it rests on the bumps. The height of the lowest point of the ball is where the tool tip may go. Doing this at every grid point one by one is slow, because at each point the ball has to be compared with all the bumps under it.

Turn the question around. Each bump pushes the ball up when the ball is near. If you hang an upside-down ball under each bump, the height that a bump forces on the tip at a nearby point is the height of that hanging ball there. So hang one upside-down ball under every bump and take, at each point, the highest one.

The result is a smooth surface over the part. The tool tip runs along it and never pushes into a bump.

## The problem

The part is a height field $f$ sampled on a grid with spacing $d$. The tool points down, and its shape is a function $T(o) \ge 0$ on a disk of offsets $o$: the height of the tool surface above its tip at the horizontal offset $o$. A ball end mill of radius $r$ has $T(o) = r - \sqrt{r^2 - |o|^2}$, and a flat end mill has $T = 0$ on its disk. The tool tip at grid point $p$ must be at least as high as
$$
Z(p) = \max_{q \in N(p)} \big(f(q) - T(q - p)\big),
$$
where $N(p)$ is the set of samples under the tool. This is the lowest tip height that leaves every sample at or under the tool surface. For a ball end mill on a smooth part, the tool center is at height $Z + r$, and the surface of centers is the [offset surface](/offset-surface/) of the part, cut at the points where the offset folds.

In terms of [mathematical morphology](/mathematical-morphology/), $Z$ is the grayscale [dilation](/morphological-dilation/) of $f$ by the structuring function $-T$.

## The algorithm

```pseudo id=main
INVERSE-TOOL-OFFSET(f, T)
L1  Z[p] ← −∞ for every grid point p
L2  for each sample q of the part do
L3      for each offset o in the footprint of the tool do
L4          p ← q + o; skip p if it is off the grid
L5          Z[p] ← max(Z[p], f(q) − T(o))         ▷ the inverted tool at q, as in a z-buffer
L6  return Z
```

The value $f(q) - T(o)$ is the height of the inverted tool, hung at the sample $q$, above the point $q + o$. For a symmetric tool, $T(o) = T(-o)$, so this is the same as $f(q) - T(q - p)$ in the formula for $Z(p)$. The inverted tool is computed once, as a small table of heights over the footprint.

## Example

Take a $5 \times 5$ grid with spacing $d = 0.5$, a flat floor at height 0, and one pin of height 1 at the middle sample. The tool is a ball end mill with $r = 1$. Its footprint has the 13 offsets with $|o| \le 1$, and $T$ is 0 at the center, $1 - \sqrt{0.75} = 0.1340$ at distance 0.5, $1 - \sqrt{0.5} = 0.2929$ at distance 0.707 and 1 at distance 1.

| grid point on the middle row | $x = -1$ | $x = -0.5$ | $x = 0$ | $x = 0.5$ | $x = 1$ |
|---|---|---|---|---|---|
| highest inverted tool | floor 0, pin $1 - 1 = 0$ | pin $1 - 0.1340$ | pin $1$ | pin $1 - 0.1340$ | floor 0, pin 0 |
| $Z$ | 0 | 0.8660 | 1 | 0.8660 | 0 |

The tip rides over the pin on a dome of radius 1, which is the inverted ball hung under the pin. At the diagonal neighbour $(0.5, 0.5)$, $Z = 0.7071$. Elsewhere the floor wins and $Z = 0$.

## Correctness

**Theorem.** INVERSE-TOOL-OFFSET returns, at each grid point $p$, $Z[p] = \max_{q \in N(p)} (f(q) - T(q - p))$. With the tip at $Z[p]$, the tool is at or above every sample under it and touches at least one, and every lower tip height leaves a sample above the tool.

The scatter loop sends the value $f(q) - T(o)$ to the point $q + o$. For a fixed $p$, the pairs that reach it are exactly the samples $q$ in its footprint, by the symmetry of the footprint, with the same values as in the formula, and the maximum does not depend on the order. The sample that attains the maximum touches the tool, and any lower tip cuts into it. The full proof is in the proof file.

The claim is about the samples only. The tests compare the scatter with a direct maximum over all samples for exact equality, with Fractions for the flat tool, and they check the ball on the tilted plane $z = mx$ against the continuous answer $mx + r(\sqrt{1 + m^2} - 1)$. The grid value is never above it, and in the tests it is below it by at most 0.0056 for $d = 0.25$ and $r = 2$, which is a measurement.

## Complexity

The footprint of a tool of radius $r$ has $k \approx \pi r^2/d^2$ grid points. Lines L2 to L5 run $nk$ times for $n$ samples, so the time is $O(nk)$, and $Z$ takes $O(n)$ space. Halving the grid spacing multiplies $n$ by 4 and $k$ by 4, so the time grows by 16. Each step is a table lookup, a subtraction and a comparison, which suits graphics hardware: drawing the inverted tool at every sample with a depth test is a [z-buffer](/z-buffer/) rendering.

## Properties

- **Robust.** The method needs only heights, so gaps, overlaps and bad patches of the model do not stop it.
- **Gouge-free at the samples.** No sample lies above the tool surface. Between samples the part can rise above the tool.
- **Any tool shape.** Ball, flat, bull-nose and tapered tools all work by their height table $T$.
- **Order-free.** The maximum is the same in any order of the samples, so the loop can run in parallel.
- **Three-axis only.** The tool axis is fixed and vertical.

## Variants and improvements

- **Rendering on graphics hardware.** Drawing the inverted tool as a mesh at every sample with a depth buffer computes $Z$ at the speed of the graphics card.
- **Gather form.** At each grid point, take the maximum over the samples in the footprint. This gives the same values and suits a parallel machine.
- **Paths from the surface.** Tool paths are read from $Z$ along grid rows, which gives [iso-planar](/iso-planar-toolpath/) passes, or along level sets of $Z$, which gives waterline passes.
- **Verification.** The same grid is used to simulate the cut and check it, as in the [z-map model](/z-map-model/) and in [NC verification](/nc-verification/).

## When to use it

Use the inverse tool offset for three-axis machining of complex parts given as meshes or as many patches, such as dies and molds, where robustness matters more than exact geometry. Use an exact method on the surface model, with [gouge detection](/gouge-detection/), when the part has thin features or when a fine grid is too costly.

## Pitfalls

- **Features between samples.** A rib thinner than the grid spacing can fall between samples and get cut. The grid spacing must be smaller than the smallest feature.
- **Grid error.** The grid value is below the continuous answer by an amount that grows with the spacing, so a finished surface can show small cuts below the true part. In the tests on a tilted plane the error was below $0.006$ for spacing 0.25. The error depends on the spacing and the slope, so choose the spacing from the tolerance of the part.
- **Edges of the grid.** Near the edge of the grid, the footprint holds fewer samples, and the tool can drop over the edge. Pad the grid with the stock height or with the part outside the machining area.
- **Memory.** A fine grid over a large part needs much memory, and the time grows with the fourth power of the inverse spacing.

## Implementations

## History

Kishinami, Kondo and Saito developed the inverse offset method in Japan in the late 1980s, and Kondo, Kishinami and Saito (1988) described a machining system based on it. The method spread with the z-map model and graphics hardware, and Choi and Jerard (1998) present it as a standard way to compute cutter location data for sculptured surfaces.

## References
