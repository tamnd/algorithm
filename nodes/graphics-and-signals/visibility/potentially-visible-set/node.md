---
tag: 3GQ0A8
kind: concept
slug: potentially-visible-set
name: Potentially visible set
area: graphics-and-signals/visibility
level: advanced
summary: A precomputed superset of the objects visible from a region, used for fast runtime culling.
prereqs: [visibility-culling, portal-culling, bsp-tree]
see_also: [occlusion-culling, frustum-culling, bsp-tree-visibility, visibility-coherence, occlusion-query, visibility-polygon, hidden-surface-removal, ray-casting]
sources:
  - paper: doi:10.1145/91385.91416
    title: John M. Airey, John H. Rohlf and Frederick P. Brooks Jr., Towards image realism with interactive update rates in complex virtual building environments, Proceedings of the 1990 Symposium on Interactive 3D Graphics, Computer Graphics 24(2), pages 41 to 50
    locator: the subdivision of a building into cells and the precomputed set of potentially visible polygons for each cell
  - paper: doi:10.1145/122718.122725
    title: Seth J. Teller and Carlo H. Séquin, Visibility preprocessing for interactive walkthroughs, Proceedings of SIGGRAPH 1991, Computer Graphics 25(4), pages 61 to 70
    locator: the cell-to-cell and cell-to-object visibility through portal sequences, and the eye-to-cell culling at run time
  - paper: doi:10.1109/TVCG.2003.1207447
    title: Daniel Cohen-Or, Yiorgos L. Chrysanthou, Cláudio T. Silva and Frédo Durand, A survey of visibility for walkthrough applications, IEEE Transactions on Visualization and Computer Graphics 9(3), 2003
    locator: the from-region methods, and the classification into exact, conservative, aggressive and approximate visibility
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 19 (culling techniques, portal culling and occlusion culling)
---

A *potentially visible set* (PVS) of a region $R$ of viewpoints is a set of objects that contains each object visible from some point of $R$. The renderer computes it before run time, for each cell of a subdivision of the space where the viewer can move. At run time it finds the cell that contains the eye and draws only the objects in that cell's PVS. The set may contain some objects that are never visible from $R$. It must not leave out a visible object, or the image is wrong. Airey, Rohlf and Brooks introduced the idea in 1990 for walkthroughs of buildings, and Airey's PhD thesis at the University of North Carolina in the same year developed it. Teller and Séquin in 1991 computed it exactly at the level of cells, with lines through sequences of [portals](/portal-culling/). PVS is a form of [visibility culling](/visibility-culling/) that moves almost all of the work from run time into a preprocess.

## In plain words

In a building, from any place in one room you can see only a few other rooms: the rooms next to it, and some rooms farther away when the doors line up. That list does not change while the building stays the same. So you can make the list once, before anyone walks through, and keep one list for each room. When the viewer is in a room, you draw only the rooms and objects on its list.

The list may say "maybe visible" for something that you never actually see. That costs a little extra drawing. But the list must never miss something that you can see, because then it disappears from the picture.

## The idea

**From-point and from-region visibility.** The visible set of a single eye point changes each time the eye moves. The idea of the PVS is to compute the union of these sets over a whole region $R$:
$$V(R) = \{\, o : \text{some segment from a point of } R \text{ to a point of } o \text{ meets no other object} \,\}.$$
A PVS is a set $S(R)$ with $V(R) \subseteq S(R)$. It is *exact* when $S(R) = V(R)$, and it is *conservative* when it can be larger. A method that can return a set smaller than $V(R)$ is *aggressive* or *approximate*, and it can make visible objects disappear. Cohen-Or and others use this classification in their 2003 survey.

**Cells.** The regions are the cells of a subdivision of the space where the viewer can be. In buildings the natural cells are the rooms. A [BSP tree](/bsp-tree/) of the walls gives convex cells, and its leaves give a fast way to find the cell of the eye. The openings between cells, such as doors and windows, are the portals.

**Computing the set.** Different methods trade cost against exactness.

- *Sampling.* Cast many rays from points of the cell and add each object that a ray hits first. This is simple, but it can miss small or thin objects, so it is aggressive. Airey's method used sampling of this kind.
- *Portal sequences.* A cell $B$ is visible from a cell $A$ only if a line goes through each portal of a chain of cells from $A$ to $B$. Teller and Séquin found these chains with a depth-first search over the graph of cells and portals. In the plane, the test for a line through a sequence of portal segments is a small linear program. The result at the level of cells is exact. It is conservative at the level of objects when each object in a visible cell is listed.
- *Occluder fusion and conservative tests.* For open scenes without natural portals, a set of large occluders hides the cells behind them. A conservative method must prove that an object is hidden from all points of the cell, not just from some sample points.

**Use at run time.** The renderer finds the cell of the eye, takes its PVS, and then applies the cheap culling of each frame to that set: [frustum culling](/frustum-culling/), and often [portal culling](/portal-culling/) or [occlusion culling](/occlusion-culling/) on the set. A [z-buffer](/z-buffer/) resolves the rest. So the PVS replaces the per-frame visibility work of distant parts of the scene by a table lookup.

**Costs.** The preprocess can take hours for a large scene. For $c$ cells, a PVS for each cell as a bit vector over the cells takes $c^2$ bits: for $c = 10\,000$ cells, that is $10^8$ bits, or $12.5$ MB, before compression. Most bits are zero, so run-length codes and similar codes make the table much smaller. The PVS is valid only for static occluders. Moving objects are culled with the PVS of the cells that they overlap, and they cannot hide other objects in the table.

## Examples

**Four rooms in a row.** The rooms $A$, $B$, $C$ and $D$ are the unit-width strips $0 \le x \le 1$, $1 \le x \le 2$, $2 \le x \le 3$ and $3 \le x \le 4$, with $0 \le y \le 3$. The walls between them are at $x = 1$, $2$ and $3$. Each wall has one door: the door $AB$ is at $x = 1$, $0 \le y \le 1$; the door $BC$ is at $x = 2$, $2 \le y \le 3$; the door $CD$ is at $x = 3$, $0 \le y \le 1$.

- $A$ sees $B$ through one door.
- $A$ sees $C$ if a line passes through the doors $AB$ and $BC$. The line through $(1, 1)$ and $(2, 2)$ does, so $C$ is in the PVS of $A$.
- $A$ sees $D$ only if a line $y = \alpha + \beta x$ satisfies $y(1) \le 1$, $y(2) \ge 2$ and $y(3) \le 1$. But $y(2) = \tfrac12\big(y(1) + y(3)\big) \le 1$, so there is no such line, and $D$ is not in the PVS of $A$.
- $B$ sees $D$ through the doors $BC$ and $CD$, for example on the line through $(2, 2)$ and $(3, 1)$.

| cell | PVS (cells) |
|---|---|
| $A$ | $A, B, C$ |
| $B$ | $A, B, C, D$ |
| $C$ | $A, B, C, D$ |
| $D$ | $B, C, D$ |

The table is symmetric, because a segment that joins two cells can be walked in both directions. If room $C$ holds a lamp near the floor at $y < 1$, the lamp is in the PVS of $A$ at the object level, because $C$ is. But no line from $A$ through both doors reaches it: such a line has $y(1) \le 1$ and $y(2) \ge 2$, so its slope is at least 1, and in $C$ it is at heights $y \ge 2$. So the lamp is a false positive of a cell-level PVS. A cell-to-object test, as in Teller and Séquin, removes it.

**A street scene.** In a city model, the cells are parts of the streets. From a street, the buildings next to it and the buildings at the ends of the street are visible, and the buildings behind the street fronts are hidden from all points of the street. A conservative PVS for each street segment lists the visible buildings. It is valid for each eye position along the street.

**The cost of an error.** Suppose a sampling method casts 1000 rays from a cell and none hits a thin pole in a far room, which is visible through a narrow gap. The pole is not in the PVS, and it does not appear when the viewer stands where the gap lines up. This is why conservative methods test regions, not samples.

## Where it is used

- **Indoor games.** Games with levels made of rooms and corridors stored a PVS for each leaf of the BSP tree of the level, as compressed bit vectors, from id Software's Quake in 1996 on. The tool that computed it ran at build time.
- **Architectural walkthroughs.** The original use, by Airey and by Teller and Séquin: interactive frame rates in building models whose total polygon count is far beyond what the hardware could draw in each frame.
- **Open worlds and streaming.** Precomputed visibility between regions also decides which parts of a large world to load into memory near the viewer, and which parts to send over a network.
- **With other culling.** PVS is a precomputed, coarse layer. The run-time methods [portal culling](/portal-culling/), [occlusion culling](/occlusion-culling/) and [frustum culling](/frustum-culling/) cut its sets down further in each frame.

## References
