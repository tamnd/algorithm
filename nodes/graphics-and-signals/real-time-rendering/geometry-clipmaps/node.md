---
tag: 03429S
kind: data-structure
slug: geometry-clipmaps
name: Geometry clipmaps
aliases:
- terrain clipmaps
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Render terrain as nested regular grids centered on the viewer. Each coarser level has half the resolution of the level inside it, and the levels update incrementally as the viewer moves.
model: real-ram
complexity:
  vars: {n: the number of vertices along each side of a level, L: the number of levels, d: "the number of cells by which the windows move, summed over the levels"}
  time: {build: Θ(L n^2), move: O(n d), mesh: Θ(L n^2)}
  space: {total: Θ(L n^2)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2004
  people: [Frank Losasso, Hugues Hoppe]
  note: Losasso and Hoppe presented geometry clipmaps at SIGGRAPH 2004, after the texture clipmaps of Tanner, Migdal and Jones (1998). Asirvatham and Hoppe moved the method to the GPU in GPU Gems 2 (2005).
prereqs: [level-of-detail, mipmap]
see_also: [texture-clipmap, roam-terrain, view-dependent-refinement, geomorphing, circular-buffer, virtual-texturing, frustum-culling, z-fighting]
sources:
  - paper: doi:10.1145/1015706.1015799
    title: Frank Losasso and Hugues Hoppe, Geometry clipmaps, terrain rendering using nested regular grids, ACM Transactions on Graphics 23(3), SIGGRAPH 2004, 769 to 776
    locator: the nested grids centered on the viewer, the incremental update of the levels as the viewer moves, the transition regions and the zero-area triangles at the level borders (general locator)
  - paper: "Arul Asirvatham and Hugues Hoppe, Terrain rendering using GPU-based geometry clipmaps, in Matt Pharr (editor), GPU Gems 2, Addison-Wesley, 2005, Chapter 2"
    locator: the levels of n = 255 vertices with the block size m = 64, the 12 blocks of m x m, the 4 fix-ups of m x 3 and the L-shaped trim, the degenerate triangles to avoid T-junctions, the morph with w = n/10, and the toroidal update (general locator)
  - paper: doi:10.1145/280814.280855
    title: Christopher C. Tanner, Christopher J. Migdal and Michael T. Jones, The clipmap, a virtual mipmap, SIGGRAPH 98, 151 to 158
    locator: the clipped levels of a mipmap centered on a point of interest, and their toroidal update (general locator)
---

A geometry clipmap keeps a terrain as a stack of $L$ regular grids of the same size $n \times n$, all centered on the viewer, where each level has twice the spacing of the level inside it. Each frame the renderer draws the finest grid and, for each coarser level, the ring that the finer level does not cover. As the viewer moves, each level writes only the new rows and columns into a wraparound array. [ROAM](/roam-terrain/) and [view-dependent refinement](/view-dependent-refinement/) decide per triangle each frame; here the layout is fixed by the viewer position alone, and the GPU draws large regular blocks. The [texture clipmap](/texture-clipmap/) is the same structure for the levels of a texture.

## In plain words

Lay a fine square net over the ground under the viewer. Around it lay a net with holes twice as large, which covers four times the area, and cut out its middle, where the fine net already is. Repeat this a few times. Near the viewer the ground has small triangles, and far away it has large ones, and a far triangle looks about as large on the screen as a near one.

When the viewer walks, every net moves with them, but only in whole steps of its own size. A move adds a strip of new points on one side and drops a strip on the other side. The new points go into the places of the old ones, so nothing else is copied.

Where two nets meet, the fine net bends its heights toward the coarse net, so the two fit without a gap or a step.

## The abstract type

A geometry clipmap of a height function $h$ is a value that depends on the viewer position $v$ in the plane, with these operations.

- **build(v)**: make the $L$ levels for the viewer $v$, with the heights of $h$ at their vertices.
- **move(v)**: change the viewer to $v$, so that every level holds the heights of its new window.
- **mesh(v)**: give the triangles and the heights that cover the window of the coarsest level, from fine near $v$ to coarse far from it, with no cracks.
- **get(l, p)**: the stored height of the vertex $p$ of level $l$.

After build or move, get$(l, p) = h(p)$ for each vertex $p$ of the window of level $l$.

## Representation

Domain points are integer pairs in units of the finest grid. Level $l$ has the spacing $s_l = 2^l$ and $n \times n$ vertices with $n$ odd, so its *window* is a square of side $(n - 1) s_l$. Its lower corner, the *origin* $o_l$, is a multiple of $s_{l+1}$, so that the vertices of level $l + 1$ in the window are every other vertex of level $l$. Each level stores its heights in an $n \times n$ array $T_l$ with *toroidal* addressing: the vertex $p$ goes to the slot $(\lfloor p_x / s_l \rfloor \bmod n, \lfloor p_y / s_l \rfloor \bmod n)$, as in a [circular buffer](/circular-buffer/) in two dimensions. The slot of a vertex depends only on the vertex, not on the window, so a vertex that stays in the window keeps its slot.

## Operations

```pseudo id=main
ORIGIN(v, l)
L1  o_l ← the multiple of s_(l+1) nearest to v - (n - 1) s_l / 2, in each coordinate

MOVE(l, o)                                       ▷ the new origin o from line L1
L2  for each vertex p of the new window of level l that is not in the old window do
L3      T_l[(p_x / s_l) mod n, (p_y / s_l) mod n] ← h(p)
L4  o_l ← o

MESH(v)
L5  for each level l and each cell of its window that is not inside the window of level l - 1 do emit its two triangles
L6  for each level l ≥ 1 and each edge (a, b) of level l on the border of the window of level l - 1 do emit the zero-area triangle (a, b, o) with o the midpoint
L7  each vertex p of level l < L - 1 gets z' = (1 - alpha) h(p) + alpha (h(a) + h(c))/2, with alpha = clamp(1 - b_p / w, 0, 1)
```

In line L7, $a$ and $c$ are the ends of the edge of level $l + 1$ through $p$ ($a = c = p$ when $p$ is a vertex of level $l + 1$), and $b_p$ is the distance of $p$ from the border of its window in cells of level $l$. So $\alpha = 1$ on the border and 0 at $w$ cells or more inside it, and the heights of the level blend into the coarser level over a *transition region* of width $w$. This is the [geomorph](/geomorphing/) of the method. The coarsest level keeps $h$.

Line L5 gives the *ring* of each level. In the GPU version of Asirvatham and Hoppe, with $n = 255$ and $m = (n + 1)/4 = 64$, the ring is made of 12 blocks of $m \times m$ vertices, 4 fix-ups of $m \times 3$ and an L-shaped trim, and the same few vertex buffers are drawn at every level with a scale and an offset. The trim is needed because the origin of line L1 is a multiple of $s_{l+1}$, so the fine window is not at the exact center of the coarse one. The code emits the ring cell by cell, which gives the same surface.

## Example

Take $n = 15$, $L = 4$ levels, $w = 1.5$ and the viewer at $(0, 0)$. Line L1 gives these windows.

| level | spacing | window $(x_0, y_0)$ to $(x_1, y_1)$ | side | ring width in cells, low and high side |
|---|---|---|---|---|
| 0 | 1 | $(-6, -6)$ to $(8, 8)$ | 14 | all cells |
| 1 | 2 | $(-12, -12)$ to $(16, 16)$ | 28 | 3 and 4 |
| 2 | 4 | $(-24, -24)$ to $(32, 32)$ | 56 | 3 and 4 |
| 3 | 8 | $(-48, -48)$ to $(64, 64)$ | 112 | 3 and 4 |

Each ring is at least $(n - 1)/4 - 3/2 = 2$ cells wide by the bound of the proof, and here it is 3 or 4 because the origin is rounded to a multiple of the coarser spacing. Level 0 draws its $14 \times 14 = 196$ cells, and each ring draws $196 - 7 \times 7 = 147$ cells, so the mesh has $2 (196 + 3 \cdot 147) = 1274$ triangles. Each finer window has 28 coarse edges on its border, so line L6 adds $3 \cdot 28 = 84$ zero-area triangles. For the $n = 255$ of the GPU version the bound is 62 cells.

**A move.** At level 1 the vertex columns have $p_x / s_1$ from $-6$ to 8, in the slots 9 to 14 and 0 to 8. A move of the viewer that moves the origin by $s_2 = 4$ in $x$ gives the columns $-4$ to 10. The two new columns 9 and 10 go into the slots 9 and 10, which held the dropped columns $-6$ and $-5$. So the move writes $2n = 30$ heights and copies nothing.

**The morph.** With $w = 1.5$, a vertex on the border of its window has $\alpha = 1$ and takes the mean of the two coarse vertices around it, one cell inside has $\alpha = 1 - 1/1.5 = 1/3$, and two cells inside has $\alpha = 0$.

## Correctness

The proof file gives the arguments, and the tests check them for 10 random viewers and 40 random moves.

- **Nesting.** If $(n - 1)/4 > 3/2$, each window lies strictly inside the next coarser one, its corners are vertices of the coarser level, and the ring is at least $(n - 1)/4 - 3/2$ coarse cells wide on each side (a proved property).
- **Tiling.** The triangles of line L5 for all levels cover the coarsest window once, with disjoint interiors (a proved property; the test sums the areas).
- **Closed edges.** With the triangles of line L6, every directed edge is paired with its reverse, except on the outer border (a proved property; the test counts the directed edges).
- **No cracks.** If $0 < w \le (n - 1)/4 - 3/2$, a point shared by two levels has the same height in both, and the three corners of each zero-area triangle are collinear in space (a proved property). The width $w = n/10$ of Asirvatham and Hoppe meets the condition for $n \ge 35/3$; the value $n/10$ is a tuning.
- **The update.** The toroidal slot is one to one on a window, and after line L4 the array equals a fresh fill of the new window; the move writes exactly the new vertices, $n^2 - (n - |d_x|)(n - |d_y|)$ of them for a move by $(d_x, d_y)$ cells (a proved property).

The proof covers the surface of one frame. It does not show that the surface is continuous in time when an origin moves, and the tests do not check it.

## Complexity

| operation | time | note |
|---|---|---|
| build | $\Theta(L n^2)$ | one height per vertex of each level |
| move | $O(n d)$ | a level that moves by $(d_x, d_y)$ cells makes $n^2 - (n - d_x)(n - d_y) \le n(d_x + d_y)$ writes |
| mesh | $\Theta(L n^2)$ | each ring has $O(n^2)$ cells; on the GPU it is a fixed set of draws |
| get | $O(1)$ | one slot |

The space is $\Theta(L n^2)$: $L$ arrays of $n^2$ heights, against the $\Theta(4^L n^2)$ of a full grid at the finest spacing over the coarsest window. The code finds the new vertices with a set difference, which costs $\Theta(n^2)$ per move; the bound above is for writing the strips directly, as the paper does.

## Variants

- **GPU blocks.** The footprints of Asirvatham and Hoppe draw each ring from a few shared vertex buffers, and the vertex shader reads the heights from the level texture and computes the morph.
- **Compression and synthesis.** Losasso and Hoppe keep the full terrain in a compressed pyramid and fill new strips by decompression, and they can add detail beyond the data for the finest levels.
- **Morph from the viewer.** The code computes $\alpha$ from the distance to the window border. Computing it from the distance to the viewer, as a renderer would do in the vertex shader, makes $\alpha$ change smoothly when the viewer moves, not in steps when an origin moves.
- **Clipmaps for textures.** The [texture clipmap](/texture-clipmap/) uses the same nested windows and toroidal update for the levels of a [mipmap](/mipmap/).
- **Culling.** Blocks of a ring that are outside the view frustum can be skipped, which [frustum culling](/frustum-culling/) of the block bounds does at a small cost.

## When to use it

Use geometry clipmaps for a large height field that is seen from a viewer near the ground, such as a flight or a driving simulator, when the GPU should draw large regular blocks and the CPU should do little work per frame. The error is not adapted to the shape of the terrain: a flat plain gets as many triangles as a mountain range, so for very uneven terrain [ROAM](/roam-terrain/) or [view-dependent refinement](/view-dependent-refinement/) can need fewer triangles. For a mesh that is not a height field, the method does not apply.

## Pitfalls

- **An origin on the fine spacing.** If line L1 rounds to a multiple of $s_l$ in place of $s_{l+1}$, the corners of the window of level $l$ are not vertices of level $l + 1$, the ring of line L5 cuts through coarse cells, and the levels do not tile.
- **A slot relative to the origin.** If line L3 uses the slot $((p_x - o_x) / s_l, (p_y - o_y) / s_l)$, the slot of a vertex changes when the origin moves, and each move must copy all $n^2$ heights to their new slots.
- **Rewriting the window.** If line L2 runs over every vertex of the new window, the result is right, but each move writes $n^2$ heights in place of a strip.
- **No zero-area triangles.** Without line L6, the midpoint of each coarse edge on a level border is a T-junction. Even when the heights agree, rounding in the rasterizer can leave single-pixel holes along it.
- **A transition region that is too wide.** If $w$ in line L7 is larger than the ring, a vertex of the coarser level on the inner border of its ring has $\alpha > 0$, its height differs from the height of the same point in the finer level, and a crack opens.
- **A morph toward the wrong heights.** If line L7 blends toward the mean of two fine neighbors in place of the two coarse vertices $a$ and $c$, the border of the level does not match the coarse edge, and the zero-area triangles are no longer flat.

## Implementations

## History

Tanner, Migdal and Jones introduced the clipmap for textures at SIGGRAPH 98: a mipmap whose fine levels are clipped to a window around a point of interest and updated with wraparound addressing. Losasso and Hoppe applied the same idea to terrain geometry at SIGGRAPH 2004, with nested grids around the viewer, transition regions between the levels, and a compressed terrain pyramid. A year later Asirvatham and Hoppe described a version for the GPU in GPU Gems 2, which draws the rings from a few shared blocks and keeps the levels in textures. The method became a common way to draw large terrains in real time.

## References
