---
tag: M0T5ZN
kind: data-structure
slug: cube-map
name: Cube map
aliases:
- cubemap
- cube environment map
area: graphics-and-signals/real-time-rendering
level: intro
summary: Six square textures on the faces of a cube that store a function of direction. A lookup picks the face of the largest component of the direction and divides the other two by it.
model: real-ram
complexity:
  vars: {n: the number of texels along one edge of a face}
  time: {lookup: Θ(1), store: Θ(1), texel_direction: Θ(1), fill: Θ(n^2)}
  space: {total: Θ(n^2)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1986
  people: [Ned Greene]
  note: Greene proposed in 1986 to store the world as seen from one point on the six faces of a cube, as a better projection for environment maps than the sphere and latitude maps used before. Graphics hardware and APIs added cube map textures in the late 1990s.
prereqs: [texture-mapping, bilinear-filtering]
see_also: [environment-mapping, image-based-lighting, mipmap, irradiance-environment-map, split-sum-approximation, shadow-mapping, texture-mapping, g-buffer]
sources:
  - paper: doi:10.1109/MCG.1986.276658
    title: Ned Greene, Environment mapping and other applications of world projections, IEEE Computer Graphics and Applications 6(11), 1986, 21 to 29
    locator: the cube projection of the environment, its six perspective faces, and its comparison with other world projections
  - url: https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf
    title: Mark Segal and Kurt Akeley, The OpenGL Graphics System, A Specification, version 4.6 (core profile), Khronos Group
    locator: the section on cube map texture selection (the table of the major axis and of sc, tc and ma for each face) and the seamless cube map filtering rule
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 10, Local Illumination (the part on cube mapping and environment map projections)
---

A cube map stores a function of direction, for example the radiance of the environment seen from one point, on the six faces of a cube centered at that point. Each face is a square texture of $n \times n$ texels. To read the value for a direction $d$, the lookup picks the face of the axis where $|d|$ is largest, divides the other two components by that largest one, and maps them to texture coordinates on the face. The mapping costs a few comparisons and one division, needs no trigonometry, and has no singular point like the poles of a latitude and longitude map. Greene proposed it in 1986, and every graphics API supports it in hardware. A cube map is the usual storage for [environment mapping](/environment-mapping/), [image-based lighting](/image-based-lighting/) and point light shadows; those pages describe what is stored, and this page describes the storage.

## In plain words

Stand in the middle of a room shaped like a cube, and paint on each of its six sides (four walls, the floor and the ceiling) what you see through it. Every direction you can look in hits one side, at one point. To find the color for a direction, find the side it points at most, then find the spot on that side. The sides are flat pictures, so the hardware can store and filter them like any other texture. The price is that texels near the corners of a side cover a smaller part of the view than texels in the middle, and the edges between sides need extra care when you blend nearby texels.

## The abstract type

A cube map is a map from directions in $\mathbb{R}^3 \setminus \{0\}$ (only the direction matters, not the length) to values, with a fixed resolution. Its operations:

- `lookup(d)`: the value stored for the direction $d$, with nearest or bilinear filtering.
- `store(f, i, j, v)`: set the value of texel $(i, j)$ of face $f$.
- `texel_direction(f, i, j)`: the unit direction of the center of a texel, which is the inverse of the lookup.
- `texel_solid_angle(f, i, j)`: the solid angle that the texel covers, needed for integrals over the sphere.
- `fill(g)`: store $g(d)$ at the center direction of every texel.

## Representation

The cube map holds six arrays of $n \times n$ values, one per face, in the OpenGL order $+x, -x, +y, -y, +z, -z$. Texel $(i, j)$ of a face covers the face coordinates $s \in [i/n, (i+1)/n]$ and $t \in [j/n, (j+1)/n]$ and is stored in row $j$, column $i$. The face coordinates come from this table, which the page takes from the OpenGL specification:

| face | major axis $ma$ | $sc$ | $tc$ |
|---|---|---|---|
| $+x$ | $d_x$ | $-d_z$ | $-d_y$ |
| $-x$ | $d_x$ | $+d_z$ | $-d_y$ |
| $+y$ | $d_y$ | $+d_x$ | $+d_z$ |
| $-y$ | $d_y$ | $+d_x$ | $-d_z$ |
| $+z$ | $d_z$ | $+d_x$ | $-d_y$ |
| $-z$ | $d_z$ | $-d_x$ | $-d_y$ |

with $s = (sc / |ma| + 1)/2$ and $t = (tc / |ma| + 1)/2$. Other APIs flip some of these signs or order the faces differently, so code that moves cube maps between APIs has to remap the faces. The invariant is simple: six faces of $n \times n$ values, and texel $(f, i, j)$ is the region above. The page uses a right handed frame with $y$ up, as in OpenGL.

## Operations

```pseudo id=main
CUBE-LOOKUP(C, d)
L1  face ← the axis of the largest |d_k|, with its sign   ▷ ties: x, then y, then z
L2  (sc, tc, ma) ← the row of face in the table
L3  s ← (sc / |ma| + 1) / 2;  t ← (tc / |ma| + 1) / 2
L4  i ← min(⌊s · n⌋, n - 1);  j ← min(⌊t · n⌋, n - 1)
L5  return C.face[face][j][i]
```

**Lookup.** Line L1 finds the face that the ray from the center crosses: it leaves the cube where its largest component reaches 1. Line L2 takes the other two components with the signs of the table. Line L3 is a central projection onto the face plane, followed by the map from $[-1, 1]$ to $[0, 1]$. Line L4 picks the texel for the nearest filter; the minimum keeps $s = 1$ inside the last texel. The direction need not be normalized, because line L3 divides by $|ma|$. Cost: $O(1)$. A bilinear lookup replaces lines L4 and L5 by the weighted mean of the four texels around $(s n - 1/2, t n - 1/2)$, see [bilinear filtering](/bilinear-filtering/).

```pseudo id=direction
TEXEL-DIRECTION(C, f, i, j)
L6  s ← (i + 1/2) / n;  t ← (j + 1/2) / n
L7  sc ← 2s - 1;  tc ← 2t - 1
L8  p ← the point of face f with these sc and tc, for example (1, -tc, -sc) on +x
L9  return p / |p|
```

**Texel direction.** This inverts lines L2 and L3: the face fixes one coordinate of $p$ at $\pm 1$, and the table, read backwards, gives the other two. Cost: $O(1)$. `fill` calls it for each texel, $\Theta(n^2)$ calls per face.

**Store.** Write the value at row $j$, column $i$ of the face. Cost: $O(1)$.

**Solid angle.** A point $(x, y)$ of the face plane, with $x, y \in [-1, 1]$, sees the center at distance $r = \sqrt{1 + x^2 + y^2}$, so $d\omega = dA / r^3$. Its integral over a texel $[x_0, x_1] \times [y_0, y_1]$ is $F(x_1, y_1) - F(x_0, y_1) - F(x_1, y_0) + F(x_0, y_0)$ with $F(x, y) = \arctan(xy / \sqrt{1 + x^2 + y^2})$ (a proved formula). Cost: $O(1)$.

## Example

A cube map with $n = 4$ starts with every texel at 0.

| step | operation | work | result |
|---|---|---|---|
| 1 | `store(-y, 2, 0, 5.0)` | write row 0, column 2 of face $-y$ | face $-y$ has one texel with 5 |
| 2 | `lookup((0.3, -0.8, 0.5))` | L1: $|d_y| = 0.8$ is largest, face $-y$; L2: $sc = 0.3$, $tc = -0.5$; L3: $s = 0.6875$, $t = 0.1875$; L4: $i = 2$, $j = 0$ | 5.0 |
| 3 | `lookup((1, 0, 0))` | face $+x$, $s = t = 0.5$, $i = j = 2$ | 0.0 |
| 4 | `lookup((0.5, 0.5, 0.5))` | a tie of all three axes, so face $+x$ by the tie order; $s = 0$, $t = 0$ | 0.0, from texel $(0, 0)$ of $+x$ |
| 5 | `texel_direction(-y, 2, 0)` | $s = 0.625$, $t = 0.125$, $sc = 0.25$, $tc = -0.75$, $p = (0.25, -1, 0.75)$ | $(0.1961, -0.7845, 0.5883)$ |
| 6 | `texel_solid_angle(-y, 2, 0)` | the formula above with $x \in [0, 0.5]$, $y \in [-1, -0.5]$ | 0.1204 sr |

Step 5 returns a direction that step 2 would map to the same texel. In step 6, the four center texels of a face have 0.2014 sr, the edge texels 0.1204 sr and the corner texels 0.0815 sr; the 96 texels add up to $4\pi$. A uniform split would give $4\pi / 96 = 0.1309$ sr to each.

## Correctness

The invariant is that the six arrays have $n \times n$ entries and that texel $(f, i, j)$ is the region of the face given by the table; only `store` changes an entry, and it changes one. The [proof](proofs/correctness.md) shows that line L1 selects the face where the ray leaves the cube, that $s$ and $t$ are in $[0, 1]$, that `texel_direction` inverts lines L2 and L3, that the center of a texel maps back to that texel, that a lookup returns the last value stored in its texel, and that the solid angle formula holds and sums to $4\pi$. All of these are proved properties. The tests compare the face with a brute force intersection of the ray with the six face planes, and the operations with a dict model.

## Complexity

The model is the real RAM.

| operation | time | note |
|---|---|---|
| `lookup` (nearest) | $\Theta(1)$ | 3 comparisons, 2 divisions, 1 read |
| `lookup` (bilinear, one face) | $\Theta(1)$ | 4 reads |
| `store` | $\Theta(1)$ | 1 write |
| `texel_direction` | $\Theta(1)$ | 1 square root |
| `texel_solid_angle` | $\Theta(1)$ | 4 arctangents |
| `fill` | $\Theta(n^2)$ | one function call per texel |
| space | $\Theta(n^2)$ | $6 n^2$ values; a full mipmap chain adds a third |

The cost of a lookup does not depend on $n$, because the face and the texel are computed, not searched.

## Variants

- **Mipmapped cube maps.** A [mipmap](/mipmap/) chain per face gives filtered lookups. For prefiltered environments, each level stores a blur for one roughness, as in the [split sum approximation](/split-sum-approximation/).
- **Seamless filtering.** Bilinear filtering inside one face, as in the code of this page, clamps at the edges and leaves a visible seam. Seamless filtering takes the texels across the edge from the neighbor face. OpenGL has it as the seamless cube map mode, and newer APIs such as Vulkan always filter this way.
- **Cube map arrays.** Several cube maps in one texture, indexed by a layer, for many [light probes](/irradiance-volume/).
- **Other parameterizations.** A latitude and longitude map is easy to paint but wastes texels near the poles. A sphere map, the first form of [environment mapping](/environment-mapping/), depends on the view. Octahedral maps fold the sphere onto one square with less distortion than the cube. Dual paraboloid maps use two textures.
- **Equal area or warped cubes.** A remap of $s$ and $t$ on each face makes the texel solid angles more even, at the cost of a little arithmetic per lookup.
- **Depth cube maps.** For a point light, each face stores the distance to the nearest surface, for omnidirectional [shadow mapping](/shadow-mapping/).

## When to use it

Use a cube map whenever a value depends on a direction from one point: environment reflection, sky and irradiance maps, light probes and point light shadows. It is native to the hardware, it has no singularities, and its texels differ in solid angle by a factor of only about $3\sqrt 3 \approx 5.2$ between the center and the corners in the limit of fine texels. Choose a latitude and longitude map for storage and editing of captured panoramas, and convert to a cube map for rendering. Choose an octahedral map when six faces are inconvenient, for example in an atlas of many small probes.

## Pitfalls

- **Wrong face table.** Using the table of another API, or a $y$ down image convention, mirrors or rotates faces. Line L2 must match the table of the API that samples the texture, and the test of the round trip should run on the real data.
- **Equal weights in integrals.** A sum over texels that ignores `texel_solid_angle` overweights the corners. The projection of an [irradiance environment map](/irradiance-environment-map/) needs the solid angle at each texel.
- **Seams.** A per face bilinear filter, or a blur that runs on each face alone, gives a visible line at the edges, worst in prefiltered maps at high roughness. Use seamless filtering, or filter in direction space across faces.
- **Texel centers.** The center of texel $i$ is at $s = (i + 1/2)/n$. Using $i/n$ in line L6 shifts every texel by half a texel and breaks the round trip.
- **Ties at edges and corners.** On an edge, two faces hold the same direction. Line L1 must use one fixed tie rule; mixing $>$ and $\ge$ between code paths gives two different texels for the same direction.
- **Gamma.** Store linear values for lighting, or decode sRGB faces before any filtering, see [gamma correction](/gamma-correction/).

## Implementations

## History

Blinn and Newell (1976) indexed a reflection map by the two angles of the reflected direction. Miller and Hoffman (1984) noted that a map can be stored as six perspective views, and Greene (1986) worked out the cube as a projection of the world, with its sampling and filtering, and used it for environment mapping. Hardware cube map textures arrived around 1999 and became part of OpenGL 1.3 and Direct3D 7. Since then the cube map has been the common way to store environments, prefiltered reflections and probes in real-time rendering.

## References
