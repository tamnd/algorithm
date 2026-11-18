---
tag: N3KQ0C
kind: technique
slug: geomorphing
name: Geomorphing
aliases:
- geomorph
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Interpolate the vertex positions between two levels of detail over several frames so that switching levels causes no visible pop.
prereqs: [level-of-detail, progressive-mesh]
see_also: [view-dependent-refinement, roam-terrain, geometry-clipmaps, mesh-simplification, mipmap, alpha-blending, bilinear-interpolation]
sources:
  - paper: doi:10.1145/237170.237216
    title: Hugues Hoppe, Progressive meshes, SIGGRAPH 1996, 99 to 108
    locator: the section on geomorphs (the linear blend of vertex positions between two meshes of a progressive mesh)
  - paper: doi:10.1145/1015706.1015799
    title: Frank Losasso and Hugues Hoppe, Geometry clipmaps, terrain rendering using nested regular grids, ACM Transactions on Graphics 23(3), SIGGRAPH 2004, 769 to 776
    locator: the transition regions, in which the heights of a level are blended toward the next coarser level
  - paper: "Arul Asirvatham and Hugues Hoppe, Terrain rendering using GPU-based geometry clipmaps, in Matt Pharr (editor), GPU Gems 2, Addison-Wesley, 2005, Chapter 2"
    locator: the morph z' = (1 - alpha) z_f + alpha z_c in the vertex shader, with the transition width w = n/10 (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: the part on level of detail and the switching between levels in the chapter on acceleration algorithms (general locator)
---

A geomorph moves the vertices of a finer mesh, over a short time or a short range of distance, from the places they have on the coarser mesh to their own places. The [level of detail](/level-of-detail/) switch then happens in small steps that the eye does not see as a pop. It differs from a blend of two images with [alpha blending](/alpha-blending/): only one mesh is drawn, the finer one, and its geometry changes. Hoppe introduced the term for [progressive meshes](/progressive-mesh/); terrain methods such as [geometry clipmaps](/geometry-clipmaps/) use the same blend on heights.

## In plain words

When a game switches a mountain from a rough model to a detailed one, new bumps appear in one frame. That jump is easy to see.

A geomorph hides it. Draw the detailed model, but at first put every new point exactly on the surface of the rough model, so the picture does not change. Then, over a second or over a few meters of travel, slide each new point to where it should be. At the end the detailed model is in place, and at no time did anything jump.

The same trick runs backward when the model gets simpler: slide the extra points onto the rough surface first, then switch.

## When it applies

- Two levels of detail of the same surface, where every vertex of the finer level has a natural place on the coarser one: its parent vertex in a [progressive mesh](/progressive-mesh/), or a point of the coarse surface below it in a height field.
- The finer level has the same or more vertices, and its connectivity is used during the morph. The coarse mesh need not be drawn.
- The switch is driven by a parameter that changes smoothly: time after the switch, or the distance to the viewer.
- The error to hide is in the positions. A change in the outline of a mesh with a different topology, or in the texture, needs another method, such as a cross-fade.

## The template

The holes are the *coarse place* $c(v)$ of each vertex $v$ of the fine mesh, the *fine place* $f(v)$, and the *blend factor* $\alpha \in [0, 1]$.

```pseudo id=main
GEOMORPH(fine mesh, c, f, α)                     ▷ holes: c(v), f(v), α
L1  for each vertex v of the fine mesh do
L2      if v keeps its place in the coarse mesh then g(v) ← f(v)
L3      else g(v) ← (1 - α) c(v) + α f(v)
L4  return the fine mesh with the vertex places g
```

The steps of the method are:

1. Choose the two levels and the fine mesh that is drawn during the morph.
2. For each vertex of the fine mesh, compute its coarse place $c(v)$ once, when the switch starts. In a progressive mesh it is the position of the vertex that the split came from. In a height grid it is the height of the coarse surface at the vertex, the mean of the two ends of the coarse edge that the vertex lies on.
3. Each frame, compute $\alpha$ from the time since the switch, or from the distance of each vertex to the viewer, and clamp it to $[0, 1]$.
4. Run lines L1 to L4, on the CPU or in the vertex shader, and draw the fine mesh. Normals and texture coordinates can be blended in the same way.
5. When $\alpha$ reaches 1, drop $c(v)$ and use the fine mesh as it is. For a switch to the coarse level, run $\alpha$ from 1 to 0 and then draw the coarse mesh.

On a regular height grid, as in the code, the coarse mesh uses every other vertex and the same diagonal direction, so each coarse triangle is the union of four fine triangles. Line L2 keeps the coarse vertices, and line L3 moves each other vertex from the midpoint height of its coarse edge to its own height.

## Classic examples

**A height grid.** The fine grid has $3 \times 3$ vertices, and the coarse grid has the four corners with the heights 0, 2, 4 and 6 at $(0, 0)$, $(2, 0)$, $(0, 2)$ and $(2, 2)$. The other fine heights are 3 at $(1, 0)$, 1 at $(0, 1)$, 5 at $(1, 1)$, 4 at $(2, 1)$ and 7 at $(1, 2)$.

| vertex | $c(v)$ | $\alpha = 0$ | $\alpha = 1/2$ | $\alpha = 1$ |
|---|---|---|---|---|
| $(1, 0)$ | $(0 + 2)/2 = 1$ | 1 | 2 | 3 |
| $(0, 1)$ | $(0 + 4)/2 = 2$ | 2 | 3/2 | 1 |
| $(1, 1)$ | $(0 + 6)/2 = 3$ | 3 | 4 | 5 |
| $(2, 1)$ | $(2 + 6)/2 = 4$ | 4 | 4 | 4 |
| $(1, 2)$ | $(4 + 6)/2 = 5$ | 5 | 6 | 7 |

At the domain point $(0.5, 0.5)$ the drawn surface has the height $3/2$ at $\alpha = 0$, which is the height of the coarse surface there, then 2 at $\alpha = 1/2$, and $5/2$ at $\alpha = 1$, the fine surface. Without the morph the vertex $(1, 1)$ would jump by 2 in one frame.

**Progressive meshes.** Hoppe (1996) defines a geomorph between any two meshes of a [progressive mesh](/progressive-mesh/): a vertex split makes two vertices from one, and both start at the position of the parent and move to their own positions. A sequence of splits then becomes one smooth change, so a renderer can move between any two meshes of the sequence without a pop.

**Geometry clipmaps.** In [geometry clipmaps](/geometry-clipmaps/), each level has a transition region near its outer border. There $\alpha$ grows from 0 to 1 with the distance from the viewer, so the heights of a level equal those of the next coarser level at the border, and the levels meet without a crack and without a jump when the viewer moves. Asirvatham and Hoppe use a region of width $n/10$ for a grid of $n \times n$ vertices; this width is a tuning.

**The same blend on textures.** Trilinear filtering of a [mipmap](/mipmap/) blends two levels by the fraction of the level of detail, so a texture also changes level without a pop. It is the same template, with texels in place of vertices.

## Variations

- **Time or distance.** A morph over time starts at the switch and runs for a fixed number of frames. A morph over distance gives each vertex its own $\alpha$ from its distance to the viewer, so the mesh is the same for a given view, and a still camera gives a still image.
- **Vertical only.** For terrain, only the height changes and the $(x, y)$ of each vertex stays fixed, which keeps the grid and its texture coordinates.
- **In the vertex shader.** Store $c(v)$ as a second attribute or read it from the coarse level, and compute line L3 on the GPU.
- **Selective refinement.** [View-dependent refinement](/view-dependent-refinement/) and [ROAM](/roam-terrain/) change the mesh in many places each frame. A morph per split or per merge needs a state per vertex; many systems use a small error threshold instead, so that each change is below a pixel.
- **Morph of attributes.** Normals, colors and texture coordinates are blended with the same $\alpha$, and normals are normalized after the blend.

## Pitfalls

- **A coarse place that is not on the coarse surface.** If line L3 starts from a value that the coarse mesh does not show (for example the fine height of a neighbor), the first frame of the morph already differs from the coarse mesh, and the pop is still there.
- **Different diagonals.** On a grid, if the coarse cells and the fine cells use different diagonal directions, a coarse triangle is not a union of fine triangles. Then $\alpha = 0$ in line L3 does not reproduce the coarse surface, even with the right midpoints.
- **Moving the coarse vertices.** Line L2 must keep the places of the vertices that the coarse mesh shares. If they move too, the neighbors at a border with an unmorphed region open a crack.
- **A jump in alpha.** If $\alpha$ is computed from the position of the viewer with a clamp at a level border that differs from the border of the morph region, then $\alpha$ jumps there, and the surface jumps with it.
- **Morphing in screen space only.** Blending projected positions in place of world positions gives a surface that changes when the camera turns, and shading that does not match the geometry.

## Exercises

1. Show that on the grid of the code, at $\alpha = 0$, the drawn surface equals the coarse surface at every point, not only at the vertices. Use the fact that each coarse triangle is the union of four fine triangles.
2. Show that the height at each domain point is an affine function of $\alpha$. What does this say about the largest speed of a surface point during a morph over $k$ frames?
3. For the $3 \times 3$ example, find the domain point in the cell $[1, 2] \times [0, 1]$ whose height changes the most from $\alpha = 0$ to $\alpha = 1$, and compute that change.
4. In a geometry clipmap with $n = 255$ and the transition width $n/10$, $\alpha$ goes from 0 to 1 over 25.5 cells of the level. A viewer moves toward the border of the level by one cell of that level per frame. Over about how many frames does a vertex in the region complete its morph, and what is the largest change of $\alpha$ per frame?
5. Give a progressive mesh split in which both new vertices start at the parent's position, and show that the faces $f_l$ and $f_r$ that the split creates have zero area at $\alpha = 0$.

## References
