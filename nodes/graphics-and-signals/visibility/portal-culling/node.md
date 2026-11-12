---
tag: 52EA3Z
kind: algorithm
slug: portal-culling
name: Portal culling
aliases:
- portal rendering
- cell-and-portal culling
- cell-and-portal visibility
area: graphics-and-signals/visibility
level: advanced
summary: Split the scene into cells joined by portals. Walk from the eye's cell through the portals, narrowing the view cone at each one, and draw only the cells reached.
solves: [visibility-culling]
model: real-ram
complexity:
  vars: {S: "the number of (cell, cone) pairs that the walk pushes", d: the largest number of portals of a cell}
  time: {worst: O(S d), average: O(S d), best: Θ(d)}
  space: {extra: O(S)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1995
  people: [David Luebke, Chris Georges]
  note: Luebke and Georges computed the cells seen through portals at run time, with the screen rectangle of each portal as a narrowing view frustum. Airey and Teller had used cells and portals to precompute visibility.
prereqs: [visibility-culling, frustum-culling, depth-first-search, orientation-test]
see_also: [potentially-visible-set, occlusion-culling, back-face-culling, visibility-polygon, bsp-tree, hidden-surface-removal, graph, convex-polygon]
sources:
  - paper: doi:10.1145/199404.199422
    title: David P. Luebke and Chris Georges, Portals and mirrors, simple, fast evaluation of potentially visible sets, Proceedings of the 1995 Symposium on Interactive 3D Graphics, pages 105 to 106
    locator: the whole paper
  - paper: doi:10.1145/122718.122725
    title: Seth J. Teller and Carlo H. Séquin, Visibility preprocessing for interactive walkthroughs, Proceedings of SIGGRAPH 1991, pages 61 to 70
    locator: the sections on the subdivision into cells and portals, and the eye-to-cell visibility
  - paper: doi:10.1145/91385.91416
    title: John M. Airey, John H. Rohlf and Frederick P. Brooks Jr., Towards image realism with interactive update rates in complex virtual building environments, Proceedings of the 1990 Symposium on Interactive 3D Graphics, Computer Graphics 24(2), pages 41 to 50
    locator: the whole paper
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 19, Section 19.5 (Portal Culling), page 837
---

Portal culling finds the parts of an indoor scene that the eye can see through doors and windows. The scene is split into *cells*, such as rooms, and the openings between cells are *portals*. The walk starts in the cell of the eye with the view cone. For each portal of the cell, it cuts the cone down to the part that passes through the portal, and if some of the cone is left, it goes on into the next cell with the narrower cone. Only the cells reached are drawn, and their objects can be culled against the narrowed cone. The walk never misses a cell that the eye can see. In the plane with exact cones it also reaches only cells that the eye can see; in 3D the cones are usually widened to screen rectangles, and the result is a conservative superset. It is a form of [visibility culling](/visibility-culling/) for architectural scenes.

## In plain words

In a house, from the kitchen you can see into the hall only through the kitchen door. From the hall you can see into a bedroom only through the bedroom door, and only through the part of that door that you can see through the kitchen door.

So the renderer starts in your room, with the field of view of the camera. For each door of the room, it asks: which part of my view passes through this door? If no part does, the room behind the door is not seen through it. If some part does, the room is marked as seen, and the question is asked again for its doors, with only that part of the view.

The view gets narrower at each door. After a few doors nothing is left, so the walk stops. Rooms far away, or around corners, are never visited.

## The problem

The scene is in the plane; the same idea works in 3D, as the variants describe. It is split into convex *cells*. The boundary of each cell consists of *walls*, which block sight, and *portals*, segments through which the next cell is seen. For a cell $c$, its portals are listed as $(p, q, c')$, with $p \to q$ counterclockwise around $c$, so $c$ is on the left of $p \to q$, and $c'$ is the cell on the other side.

The eye $E$ is in the interior of a cell $c_0$, and the view is a *cone* $K_0$ of directions from $E$, given by two vectors $a, b$ with $\operatorname{cross}(a, b) > 0$: the angle from $a$ counterclockwise to $b$. A cell $c$ is *visible* when some point $X$ in its interior is in the open view cone and the closed segment $EX$ meets no wall. The output is a set of cells that contains each visible cell. The coordinates are real numbers; the implementation uses exact fractions.

## The algorithm

```pseudo id=main
PORTAL-CULL(cells, start cell c0, eye E, view cone K0)
L1  V ← {c0}; stack ← [(c0, K0)]
L2  while stack is not empty do
L3      pop (c, K) from stack
L4      for each portal (p, q, c′) of c do
L5          if cross(p − E, q − E) ≤ 0 then continue     ▷ E is not strictly on the side of c: the portal faces away
L6          K′ ← K ∩ cone(p − E, q − E)                 ▷ the part of K that passes through the portal
L7          if K′ is empty or a single ray then continue
L8          add c′ to V; push (c′, K′)
L9  return V
```

Line L5 is an [orientation test](/orientation-test/). It keeps only portals that the eye sees from the side of the current cell. It stops the walk from going back through the portal it came in by. It is the [back-face test](/back-face-culling/) for portals. Line L6 cuts the cone. The intersection of two cones of less than 180 degrees is a cone. Its two sides are among the four sides of the two cones. Line L7 drops a cone that has no interior. The stack is explicit, so the walk is a [depth-first search](/depth-first-search/) over paths of portals, not over cells. A cell can be reached on more than one path, with a different cone each time.

## Example

The grid has $4 \times 3$ unit cells $(x, y)$. The eye is at $E = (\tfrac12, \tfrac32)$ in cell $(0, 1)$ and looks along $+x$, with the cone from $(4, -1)$ to $(4, 1)$, about $\pm 14$ degrees. The doors are the vertical edges at $x = 1$ and $x = 2$ in row 1, at $x = 3$ in row 1 and at $x = 2$ in row 0. The horizontal doors are between $(1, 1)$ and $(1, 2)$, between $(2, 0)$ and $(2, 1)$, and between $(3, 1)$ and $(3, 2)$. Every other edge is a wall.

| push | cell | cone after line L6 | reason |
|---|---|---|---|
| 1 | $(0, 1)$ | $(4, -1)$ to $(4, 1)$ | start |
| 2 | $(1, 1)$ | $(4, -1)$ to $(4, 1)$ | the door spans $(\tfrac12, -\tfrac12)$ to $(\tfrac12, \tfrac12)$, wider than the view |
| 3 | $(2, 1)$ | $(4, -1)$ to $(4, 1)$ | the door spans $(\tfrac32, -\tfrac12)$ to $(\tfrac32, \tfrac12)$, still wider |
| 4 | $(2, 0)$ | $(4, -1)$ to $(\tfrac52, -\tfrac12)$ | the floor door spans $(\tfrac32, -\tfrac12)$ to $(\tfrac52, -\tfrac12)$ |
| 5 | $(3, 1)$ | $(\tfrac52, -\tfrac12)$ to $(\tfrac52, \tfrac12)$ | the door at $x = 3$ |
| 6 | $(3, 2)$ | $(\tfrac72, \tfrac12)$ to $(\tfrac52, \tfrac12)$ | the ceiling door of $(3, 1)$, about 8 to 11 degrees |

Two cells that the doors connect are not reached. The door from $(1, 1)$ up to $(1, 2)$ spans the directions from $(\tfrac32, \tfrac12)$ to $(\tfrac12, \tfrac12)$, 18 to 45 degrees, outside the view, so line L7 drops it. The door from $(2, 0)$ to $(1, 0)$ is at $x = 2$, and the eye is to the left of it, on the side of $(1, 0)$, so line L5 drops it. The output is 6 of the 8 cells that the doors connect. For each push, the tests find a point of the cell that the eye sees along a direction in the cone.

## Correctness

Take a visible point $X$ in a cell $c$. The segment from $E$ to $X$ passes from $c_0$ to $c$ through a sequence of portals, because it meets no wall. A small change of $X$ keeps it visible, so we can take the segment through the relative interiors of the portals and through no endpoint. By induction along the segment, the direction of $X - E$ is inside each narrowed cone, each portal passes line L5, and each cone has an interior. So the walk pushes each cell of the sequence, and $c \in V$. Conversely, in the plane each pushed cone has an interior, and a direction inside it gives a ray that crosses the portals in order, so the pushed cell is visible. Line L5 makes the walk finite: along a ray each convex cell is met once, so no path of the walk repeats a cell. The full proofs are below. The tests check both directions on 500 random grids, with exact segment tests against the walls.

## Complexity

Each pushed pair $(c, K)$ costs one test per portal of $c$, and a cone intersection is $O(1)$. So the time is $O(S d)$, where $S$ is the number of pushes and $d$ the largest number of portals of a cell. The best case is $\Theta(d)$, when no portal of the start cell is seen. $S$ depends on the scene: a cell seen through two doors is pushed twice. In the plane, a path of the walk is fixed by the rays in its cone, so the cones of the paths of one length do not overlap. This keeps $S$ small for building plans. The stack holds $O(S)$ pairs. The walk needs no preprocessing except the cells and portals, so it works when the eye moves and when doors open and close.

## Properties

- **Conservative.** No visible cell is missed.
- **Exact in the plane.** With exact cones, each cell reached is visible, as the tests check. In 3D with screen rectangles the result is a superset.
- **From the point of the eye.** The answer is for the current eye position. A [potentially visible set](/potentially-visible-set/) answers for a whole region of eye positions, computed before the run.
- **Depends on the scene structure.** The method needs cells and portals, which are natural for buildings, caves and ships and poor for open terrain or forests.
- **Online.** Each frame does a new walk, so moving doors and moving eyes need no precomputation.

## Variants and improvements

- **3D with screen rectangles.** Luebke and Georges project each portal to the screen and keep the axis-aligned rectangle of its projection. The cone is the rectangle, narrowed by intersection with the rectangle of each portal on the path. Rectangles are cheap to intersect and give a conservative result. The objects of each cell are then [frustum culled](/frustum-culling/) against the narrowed frustum.
- **Mirrors.** A mirror is a portal into a reflected copy of the cell, seen with the reflected eye.
- **Exact 3D portals.** Clip the frustum by the portal polygon, so that the cone is a general convex pyramid. This is tighter and costs more.
- **Precomputed cell-to-cell visibility.** Airey and Teller find, for each cell, the cells that some point of it can see through the portals. Teller and Séquin find these with a test for a line that passes through a sequence of portals. The result is a [potentially visible set](/potentially-visible-set/), and the run-time walk is then restricted to it.
- **Automatic cells.** The cells can be the leaves of a [BSP tree](/bsp-tree/) of the walls, and the portals the parts of the splitting planes that are not wall.

## When to use it

Use portal culling for indoor scenes, where walls hide most of the scene and doors and windows are small. It is cheap, it needs little preprocessing, and it allows moving doors. For open scenes use [occlusion culling](/occlusion-culling/). For a static scene where a precomputation is acceptable, a [potentially visible set](/potentially-visible-set/) gives the answer with a table lookup, and the portal walk can make it tighter at run time.

## Pitfalls

- **No orientation test.** If a portal is taken with its endpoints in either order, the walk can go back through the door it came in by, then forward again, without end. The tests show this. Orient each portal around its cell and keep the test of line L5.
- **Visiting cells once.** Marking a cell as done at the first visit is wrong. A cell seen first through a narrow cone can be seen later through a wider one, and the cells behind it depend on the cone. The walk is over paths, not cells.
- **Cells that are not convex.** The proof needs each cell to be convex, so that the part of a ray in the cell is one segment. In a cell that is not convex, objects inside the cell can hide each other and the cell can hide parts of its own portals.
- **An eye on a portal.** If the eye is on the boundary between two cells, the start cell is ambiguous. Start in both cells, or move the eye a little.
- **Portals that are too big.** A door modelled as the whole wall gives no culling. Make portals tight around the openings.

## Implementations

## History

Airey, Rohlf and Brooks in 1990 split building models into cells and used the openings between them to estimate which cells are visible from each cell, before the walkthrough. Teller and Séquin in 1991 computed the cells visible from each cell with a test for a line of sight through a sequence of portals, and stored the result as a potentially visible set. Luebke and Georges in 1995 did the walk at run time, from the eye, with the screen rectangles of the portals. Their method needs almost no preprocessing and became the common form of portal rendering in games.

## References
