---
tag: CE3Y53
kind: data-structure
slug: irradiance-volume
name: Irradiance volume
aliases:
- light probe grid
area: graphics-and-signals/real-time-rendering
level: advanced
summary: A 3D grid of light probes that store the incoming irradiance by direction, interpolated to light moving objects with baked global illumination.
model: real-ram
complexity:
  vars: {n: the number of probes in the grid}
  time: {sample: Θ(1), set_probe: Θ(1), bake: Θ(n)}
  space: {total: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1998
  people: [Gene Greger, Peter Shirley, Philip M. Hubbard, Donald P. Greenberg]
  note: Greger, Shirley, Hubbard and Greenberg sampled the irradiance at the points of a grid in space and for many directions at each point, so that a moving object could get the diffuse light of a precomputed scene at any position. Games later stored nine spherical harmonic coefficients per probe.
prereqs: [irradiance-environment-map, uniform-grid]
see_also: [light-mapping, cube-map, spherical-harmonic-lighting, precomputed-radiance-transfer, ambient-occlusion, irradiance-caching, global-illumination, octree]
sources:
  - paper: doi:10.1109/38.656788
    title: Gene Greger, Peter Shirley, Philip M. Hubbard and Donald P. Greenberg, The irradiance volume, IEEE Computer Graphics and Applications 18(2), 1998, 32 to 43
    locator: the definition of the irradiance at all points and directions of space, its sampling on a grid and its interpolation for moving objects
  - url: http://jcgt.org/published/0008/02/01/
    title: Zander Majercik, Jean-Philippe Guertin, Derek Nowrouzezahrai and Morgan McGuire, Dynamic Diffuse Global Illumination with Ray-Traced Irradiance Fields, Journal of Computer Graphics Techniques 8(2), 2019, 1 to 30
    locator: the probe grid that ray tracing updates each frame, and the per probe visibility data against light leaks
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 11, Global Illumination (the part on precomputed lighting stored in probes)
---

An irradiance volume stores the diffuse lighting of a scene at the points of a regular 3D grid. Each grid point, called a probe, holds the irradiance that arrives there as a function of the surface normal, usually as nine [spherical harmonic](/spherical-harmonic-lighting/) coefficients per color channel, the same encoding as an [irradiance environment map](/irradiance-environment-map/). To light a point of a moving object, the renderer finds the grid cell around it, blends the coefficients of the 8 corner probes with trilinear weights, and evaluates the blend at the normal. The probes are baked offline by a global illumination renderer, or updated at run time by ray tracing. A query costs the same for any grid size. The weakness is that the blend ignores walls: a probe on the far side of a thin wall still contributes, so light leaks into dark rooms.

## In plain words

Before the game runs, place many small light meters in a 3D lattice through the level. Each meter records how bright the light is from every direction around it, in a compact form of a few numbers. When a character walks through the level, look at the eight meters around it, mix their records by how close the character is to each, and read the mix in the direction its surface faces. The character then gets the bounced light of the room, the colors of nearby walls and the darkness of corners, without any ray tracing at run time. Meters on the other side of a wall do not know about the wall, which is the main source of errors.

## The abstract type

An irradiance volume is a map from a point $p$ in a box of space and a unit normal $n$ to an irradiance $E(p, n)$, with these operations:

- `set_probe(i, j, k, c)`: store the coefficients $c$ of the irradiance at probe $(i, j, k)$.
- `bake(f)`: call `set_probe` with $f(\text{position})$ for every probe, for example the projection of the radiance that a renderer computes there.
- `sample(p, n)`: the interpolated irradiance at $p$ for the normal $n$.
- `sample_coeffs(p)`: the interpolated coefficients at $p$, for shaders that evaluate many normals at one point.

The defined result of `sample` is the trilinear interpolation of the probe irradiance functions, with points outside the box clamped to the box. How close that is to the true irradiance depends on the scene and on the spacing, not on the data structure.

## Representation

The grid has $X \times Y \times Z$ probes, at least 2 along each axis, with an origin $o$ and a spacing $h$; probe $(i, j, k)$ is at $o + h(i, j, k)$. Each probe holds nine numbers $E_{lm}$ per color channel: the spherical harmonic coefficients of the radiance, already multiplied by the clamped cosine factors $\pi$, $2\pi/3$ and $\pi/4$ of bands 0, 1 and 2, so that $E(n) = \sum_{lm} E_{lm} Y_{lm}(n)$. The invariant is that the array has $X Y Z$ entries of nine numbers each, and that entry $(i, j, k)$ belongs to the probe at that position. On the GPU, the coefficients usually go into a few 3D textures, so that the hardware does the trilinear blend in one fetch per texture.

## Operations

```pseudo id=main
SAMPLE(V, p, n)
L1  g ← clamp((p - o) / h, 0, (X, Y, Z) - 1)   ▷ per axis, in probe units
L2  i ← min(⌊g⌋, (X, Y, Z) - 2);  f ← g - i      ▷ per axis: the cell and the place in it
L3  c ← nine zeros
L4  for each corner (a, b, d) in {0, 1}^3
L5      w ← (f_x or 1 - f_x) · (f_y or 1 - f_y) · (f_z or 1 - f_z)   ▷ f if the bit is 1
L6      c ← c + w · V.probe[i_x + a][i_y + b][i_z + d]
L7  return Σ_m c_m Y_m(n)
```

**Sample.** Line L1 converts the point to grid units and clamps it to the box. Line L2 finds the lowest corner of the cell; the minimum keeps a point on the last plane inside the last cell. Lines L4 to L6 blend the 8 corner probes with the trilinear weights, which are nonnegative and add up to 1. Line L7 evaluates the blended coefficients at the normal, nine multiplications per channel. Cost: $O(1)$.

**Set probe and bake.** `set_probe` writes nine numbers per channel. `bake` calls it once per probe, $\Theta(n)$ calls for $n$ probes; the cost of the renderer that computes each probe is separate and dominates in practice.

## Example

A $2 \times 2 \times 2$ grid with origin $(0, 0, 0)$ and spacing 2 m. The four probes at $x = 0$ see a uniform sky of radiance 1, so their irradiance is $\pi$ for every normal. The four probes at $x = 2$ see only a point light of unit power straight above, so their irradiance is $17/16$ for the normal $+z$, $3/32$ for $+x$ and $1/16$ for $-z$ (the nine coefficient values of the [irradiance environment map](/irradiance-environment-map/) page). Sample at $p = (0.5, 1, 1)$:

| step | line | work | result |
|---|---|---|---|
| 1 | L1 | $g = (0.25, 0.5, 0.5)$ | inside the box |
| 2 | L2 | $i = (0, 0, 0)$, $f = (0.25, 0.5, 0.5)$ | the only cell |
| 3 | L4, L5 | the 4 corners with $a = 0$ get $0.75 \cdot 0.5 \cdot 0.5 = 0.1875$, the 4 with $a = 1$ get $0.0625$ | weights add up to 1 |
| 4 | L6 | $c = 0.75\, c_{\text{sky}} + 0.25\, c_{\text{light}}$ | nine numbers |
| 5 | L7, $n = +z$ | $0.75 \pi + 0.25 \cdot 17/16$ | 2.6218 |
| 6 | L7, $n = -z$ | $0.75 \pi + 0.25 \cdot 1/16$ | 2.3718 |
| 7 | L7, $n = +x$ | $0.75 \pi + 0.25 \cdot 3/32$ | 2.3796 |

The result is linear in the probe data, so the sky and the light could be baked into separate volumes and added. Now put a wall at $x = 1$ and keep the probes: a point at $x = 0.8$, on the sky side of the wall, still gets $40\%$ of the light probes, because line L5 does not know about the wall. That is the light leak, shown in the tests as a measurement of the failure.

## Correctness

The invariant is that the probe array has $X Y Z$ entries of nine numbers, and only `set_probe` changes an entry. The [proof](proofs/correctness.md) shows that line L2 always gives a valid cell with fractions in $[0, 1]$, that lines L3 to L6 equal the sum over all probes of their coefficients times a product of three hat functions, that the weights are nonnegative and add up to 1, that the sample at a probe is that probe, that fields of coefficients that are affine in position are reproduced exactly, and that the result is linear in the probe data. All of these are proved properties. The tests check each of them, and compare random sequences of stores and samples with a dict model and a brute force sum over all probes.

Whether the sample equals the true irradiance is a different question. The true irradiance field is smooth in open space but can change sharply at shadow edges and across occluders, and a grid with spacing $h$ cannot represent changes on a scale smaller than $h$. That error is a property of the scene, and the usual fix is a finer grid or visibility data, not a change to the blend.

## Complexity

The model is the real RAM, with $n = XYZ$ probes and nine coefficients per channel.

| operation | time | note |
|---|---|---|
| `sample` | $\Theta(1)$ | 8 probes, 72 multiply-adds per channel, 9 more for the evaluation |
| `sample_coeffs` | $\Theta(1)$ | the same without line L7 |
| `set_probe` | $\Theta(1)$ | 9 writes per channel |
| `bake` | $\Theta(n)$ | calls to the probe renderer, which cost far more than the writes |
| space | $\Theta(n)$ | $27 n$ numbers for three color channels |

For scale, a grid of $32 \times 16 \times 32 = 16384$ probes with 27 half precision numbers each needs $884736$ bytes, under 1 MB. A light map of the same level would need texels on every surface, and still could not light objects that move.

## Variants

- **Other probe encodings.** Two bands of spherical harmonics (four numbers per channel) for a smaller grid, an ambient cube of six colors along the axes, or a small octahedral map per probe for sharper directional detail.
- **Visibility-aware blending.** Store with each probe some statistics of the distance to nearby surfaces, and lower the weight of probes that the shaded point cannot see. Majercik and coauthors do this in DDGI and update the probes each frame with ray tracing.
- **Adaptive grids.** An [octree](/octree/) or a two-level grid puts more probes where the lighting changes fast, at the cost of a search per query and of seams between levels.
- **Irregular probes.** Probes placed by hand or by a tool, with a tetrahedral mesh between them and barycentric weights; the query first finds the tetrahedron that contains the point.
- **Radiance probes.** Store radiance instead of irradiance, as [cube maps](/cube-map/), for glossy reflections. These are usually fewer and placed by hand, and they need parallax correction.
- **Moving the sample point.** Offset the point along the normal, or toward the viewer, by a part of the spacing before line L1, which reduces leaks and self-shadowing (a heuristic).

## When to use it

Use an irradiance volume for the diffuse light on dynamic objects in a scene whose lighting is baked or slowly changing, and as the diffuse term of whole levels when the geometry or the time of day changes too much for [light maps](/light-mapping/). It is cheap to query and to store, and it needs no unique texture layout. Avoid it alone where sharp contact shadows or thin walls matter, unless the probes carry visibility data; combine it with [ambient occlusion](/ambient-occlusion/) for small scale darkening. For static surfaces with fine detail, light maps give sharper results.

## Pitfalls

- **Light leaks.** Line L5 gives weight to probes behind a wall. Thin walls, floors between stories and probes inside geometry give bright spots in dark rooms. Keep probes out of solid geometry, use visibility data, or make walls thicker than the spacing.
- **Probes inside geometry.** A probe baked inside a wall sees only back faces and stores black or garbage. It then darkens everything around it through line L6. Detect such probes during the bake and move or disable them.
- **Clamping at the box.** Line L1 clamps points outside the box to its faces, so an object that leaves the volume keeps the light of the boundary. Give the volume a margin or blend to a fallback.
- **Ringing.** Strong, small lights give spherical harmonic coefficients whose evaluation in line L7 can go negative for normals away from the light. Window the coefficients, or clamp the result at zero, and test with the brightest light of the scene.
- **Cell index at the far edge.** Without the minimum in line L2, a point exactly on the last plane reads one probe past the end of the array.
- **Blending in the wrong space.** Blend linear radiometric values. Blending after [tone mapping](/tone-mapping/) or [gamma](/gamma-correction/) encoding does not give the interpolated irradiance.

## Implementations

## History

Greger, Shirley, Hubbard and Greenberg (1998) defined the irradiance volume: they extended the irradiance from points on surfaces to all points and directions of space, sampled it at the points of a grid, and interpolated it to light objects that move through a precomputed scene. Ramamoorthi and Hanrahan (2001) showed that nine spherical harmonic coefficients represent irradiance well, and probe grids in games then moved to that encoding or to similar small bases such as six color ambient cubes. Majercik, Guertin, Nowrouzezahrai and McGuire (2019) added per probe visibility and ray traced updates, which made dynamic probe grids practical on hardware with ray tracing.

## References
