---
tag: 32FCAD
kind: technique
slug: displacement-mapping
name: Displacement mapping
aliases:
- displacement map
area: graphics-and-signals/real-time-rendering
level: core
summary: Move the vertices of a finely tessellated surface along their normals by a height texture, so that the relief changes the geometry and silhouette.
prereqs: [bump-mapping, texture-mapping]
see_also: [normal-mapping, parallax-occlusion-mapping, subdivision-surface, catmull-clark-subdivision, level-of-detail, geomorphing, geometry-clipmaps, fractal-noise]
sources:
  - paper: doi:10.1145/964965.808602
    title: Robert L. Cook, Shade trees, SIGGRAPH 1984
    locator: displacement maps, a shade tree that moves the surface point before it is shaded (general locator)
  - paper: doi:10.1145/37402.37414
    title: Robert L. Cook, Loren Carpenter and Edwin Catmull, The Reyes image rendering architecture, SIGGRAPH 1987
    locator: dicing of surfaces into micropolygons smaller than a pixel, which are displaced and shaded before sampling (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: the material on displacement mapping and hardware tessellation (general locator)
---

Displacement mapping moves the points of a surface along the normal by the value of a height texture. The relief is then real geometry: it changes the outline of the object, it hides parts of itself, it casts and receives shadows, and it writes correct depths into the [z-buffer](/z-buffer/). [Bump mapping](/bump-mapping/) and [normal mapping](/normal-mapping/) change only the shading normal. [Parallax mapping](/parallax-mapping/) applies one offset to the texture coordinate, and [parallax occlusion mapping](/parallax-occlusion-mapping/) marches a ray through the height field in the pixel shader, but both keep the polygon flat. Displacement mapping moves the geometry, so it needs enough vertices to carry the relief, and its cost is the cost of those vertices.

## In plain words

Take a flat sheet of rubber with a grid of many small squares drawn on it. Look up a gray image of heights for each corner of the grid, and push the corner up or down by that height. The sheet now has real bumps. You can see them from the side, they hide what is behind them, and they cast shadows.

The catch is that the bumps can only be as fine as the grid. A bump smaller than one square is lost, so fine relief needs a fine grid, and a fine grid means many triangles. Renderers cut the surface into small pieces only where the camera is close, and use cheaper tricks for the small detail that remains.

## When it applies

- The relief is large enough to show on the outline, or to hide and shadow itself: terrain, rocks, bricks seen from close, wrinkles on a character, ocean waves.
- The renderer can make many vertices: a hardware tessellation stage, a mesh shader, a compute pass that builds the mesh, or a micropolygon renderer such as Reyes.
- The surface has a parametrization, so each new vertex has texture coordinates for the height lookup.
- It does not apply when the detail is smaller than the triangles that the budget allows. Use a normal map or parallax occlusion mapping for that detail, often on top of a coarser displacement.

## The template

The inputs are a base surface with positions $P$, unit normals $n$ and texture coordinates $uv$, a height texture $h$ with values in $[0, 1]$, a scale $s$ and a bias $b$ (the height that means no motion, often $\tfrac12$).

1. Tessellate. Cut the base surface into small triangles, so that the spacing of the vertices in texture space is $\Delta$. Choose $\Delta$ per patch or per edge from the screen size, as in [level of detail](/level-of-detail/). Reyes dices the surface into micropolygons of about one pixel.
2. For each new vertex, interpolate $P$, $n$ and $uv$ from the base surface, or evaluate them on a smooth surface such as a [subdivision surface](/subdivision-surface/).
3. Read the height $h(uv)$. A vertex or domain shader has no pixel derivatives, so choose the [mip level](/mipmap/) by hand from $\Delta$.
4. Move the vertex: $P' = P + s \, (h(uv) - b) \, n$.
5. Compute the new normal. Use the slopes of $h$, as in step 4 of [bump mapping](/bump-mapping/), or read a normal map that was baked with the same height.
6. Rasterize and shade the moved triangles as usual. Depth, outlines and shadow maps now see the relief.

The moved mesh is a piecewise linear copy of the true displaced surface, sampled at the vertices. Let $f = s \, (h - b)$ be the offset. Along one direction, linear interpolation with a step $\Delta$ has an error of at most $\tfrac{\Delta^2}{8} \max |f''|$ in the offset. This is a proved bound, and it sets the spacing for an error $\varepsilon$: $\Delta \le \sqrt{8 \varepsilon / \max |f''|}$. Detail with a period shorter than $2 \Delta$ cannot be shown at all, by the [sampling theorem](/sampling-theorem/). The choice of the error target, and the rule that turns screen size into $\Delta$, are tuning.

## Classic examples

**A trace.** Displace a unit square so that the offset of step 4 is $s \, (h(u) - b) = 0.1 \sin(2 \pi u)$, on a regular grid of $N \times N$ quads, with $\Delta = 1/N$. A grid of $N \times N$ quads has $(N + 1)^2$ vertices and $2 N^2$ triangles. The largest height error is measured on 100001 points along $u$. The bound is $\tfrac{\Delta^2}{8} \cdot 0.1 \cdot (2 \pi)^2$.

| $N$ | vertices | triangles | largest error | bound |
|---|---|---|---|---|
| 4 | 25 | 32 | $0.02105$ | $0.03084$ |
| 8 | 81 | 128 | $0.00704$ | $0.00771$ |
| 16 | 289 | 512 | $0.00188$ | $0.00193$ |
| 32 | 1089 | 2048 | $0.00048$ | $0.00048$ |

With $N = 4$ the vertices fall at heights $0$, $0.1$, $0$ and $-0.1$, and the sine becomes a zigzag. Each doubling of $N$ cuts the error by about 4 and multiplies the triangles by 4. For an error of $0.001$, the bound asks for $\Delta \le 0.045$, about 23 segments per period.

**Film rendering.** Cook's shade trees (1984) included displacement as a shader that moves the surface point. The Reyes architecture (1987) dices every surface into micropolygons smaller than a pixel, so displacement is exact to the pixel and costs no extra machinery.

**Terrain.** A height map, often made with [fractal noise](/fractal-noise/), displaces a regular grid. The grid is refined near the camera by [level of detail](/level-of-detail/) schemes such as [geometry clipmaps](/geometry-clipmaps/), and [geomorphing](/geomorphing/) blends the heights between levels to hide the switch.

**Characters.** A coarse mesh is refined by [Catmull-Clark subdivision](/catmull-clark-subdivision/) and displaced by a map baked from a detailed sculpt. A normal map adds the detail finer than the refined mesh.

## Variations

- **Vector displacement.** Store a 3D offset per texel, not a height along the normal. This allows overhangs, which a height field cannot make.
- **Adaptive tessellation.** Choose the tessellation factor of each edge from its length on the screen, or from the roughness of the height in that region. This is a heuristic.
- **Displacement on the GPU.** Hardware tessellation stages, mesh shaders and compute passes make the vertices on the fly, so the stored mesh stays coarse.
- **Precomputed meshes.** Apply the displacement once offline and store the result as a dense mesh, with level of detail for distance.
- **In the pixel shader.** [Parallax occlusion mapping](/parallax-occlusion-mapping/) finds the displaced surface per pixel by ray marching, with no new vertices but a flat outline.

## Pitfalls

- **Cracks.** Two patches that share an edge must place the same vertices on it, with the same height and normal. Different tessellation factors on the two sides, or different texture coordinates at a UV seam, open gaps. Compute the edge factor from the edge alone, and make the heights match across seams.
- **Undersampling.** Relief finer than $2 \Delta$ aliases into wrong bumps that crawl as the tessellation changes. Read the height from a coarser mip level, matched to $\Delta$.
- **Popping.** A jump in the tessellation level moves vertices from one frame to the next. Use fractional factors or geomorphing.
- **Wrong normals.** The base normal is not the normal of the moved surface. Shading with it makes the relief look flat.
- **Bounds and culling.** The moved surface is larger than the base mesh. Grow the bounding volumes by the largest offset, or the object is culled while it is still visible.
- **Self-intersection.** On concave parts, or with a large scale, the moved surface can fold through itself.
- **Cost.** The triangle count grows with $1/\Delta^2$. Very small triangles also shade badly on GPUs, which work on blocks of 2 by 2 pixels.

## Exercises

1. Prove the bound $\tfrac{\Delta^2}{8} \max |f''|$ for the linear interpolation of a smooth function between two points $\Delta$ apart.
2. For the offset $f = a \sin(2 \pi u / L)$, find the largest $\Delta$ that keeps the height error below $\varepsilon$, and the number of triangles this needs on a square of side $L$.
3. Two patches share an edge, with tessellation factors 3 and 4. Draw the vertices on the edge and show where a crack opens.
4. Explain why the bounding sphere of a displaced mesh must grow by $s \max |h - b|$, and when this is too much.
5. A terrain uses a displacement grid with 1 m spacing, and the height map has detail at 0.5 m. What happens to that detail, and how can a normal map recover part of it?

## References
