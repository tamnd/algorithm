---
tag: TRTDD8
kind: algorithm
slug: view-dependent-refinement
name: View-dependent refinement of progressive meshes
aliases:
- view-dependent LOD
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Refine or coarsen a progressive mesh locally by legal vertex splits and edge collapses, driven by the view frustum, the surface orientation and screen-space error.
model: real-ram
complexity:
  vars: {a: the number of active vertices, s: the number of vsplits and edge collapses in a pass, N: the number of vsplits of the progressive mesh, n: the number of vertices of the full mesh}
  time: {worst: O(a + s N)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1997
  people: [Hugues Hoppe]
  note: Hoppe presented the selective refinement of progressive meshes at SIGGRAPH 97, one year after progressive meshes. The paper gives the legality conditions, force_vsplit and the screen-space test.
prereqs: [progressive-mesh, level-of-detail]
see_also: [roam-terrain, geomorphing, mesh-simplification, quadric-error-metrics, frustum-culling, geometry-clipmaps, bounding-volume]
sources:
  - paper: doi:10.1145/258734.258843
    title: Hugues Hoppe, View-dependent refinement of progressive meshes, SIGGRAPH 97, 189 to 198
    locator: Section 3 (the vertex hierarchy, vsplit and ecol and their legality), Section 4 (qrefine, the view frustum, the surface orientation and the screen-space geometric error) and Section 5 (adapt_refinement and force_vsplit)
  - paper: doi:10.1145/237170.237216
    title: Hugues Hoppe, Progressive meshes, SIGGRAPH 1996, 99 to 108
    locator: the vertex split and the edge collapse, and the construction of the sequence by simplification
  - paper: "David Luebke, Martin Reddy, Jonathan D. Cohen, Amitabh Varshney, Benjamin Watson and Robert Huebner, Level of Detail for 3D Graphics, Morgan Kaufmann, 2003"
    locator: the chapters on view-dependent level of detail and on the vertex hierarchy (general locator)
---

View-dependent refinement keeps a [progressive mesh](/progressive-mesh/) at a different level of detail in different places: each frame it splits vertices where the surface is near, in view and facing the camera, and collapses edges elsewhere. A plain progressive mesh gives one sequence of meshes with a uniform level of detail, so the whole mesh is coarse or fine at once. The vertex splits here can happen in any order that a small set of conditions allows, and a split that is not yet allowed forces the splits it depends on first. [ROAM](/roam-terrain/) does the same kind of work for a height field on a regular bintree; this method works on any mesh that a progressive mesh can describe.

## In plain words

A detailed model is built by undoing many small simplification steps. Each step turns one point into two points and adds two small triangles. A normal progressive mesh undoes the steps in one fixed order, so the detail grows everywhere at the same time.

This method undoes a step only where the viewer needs it: where the surface is on the screen, faces the viewer and is close enough that the difference shows. It redoes steps where the viewer cannot see the detail. A step can only be undone when its neighbor triangles are there. If they are not, the method first undoes the older steps that make them, and then the step that it wanted.

Each frame it walks over the current points, tests each one, and makes the few changes that the new view needs.

## The problem

The input is a progressive mesh: a base mesh $M^0$ and a sequence of $N$ vertex splits that gives the full mesh $M^N$ with $n$ vertices. Each split $\mathrm{vsplit}(v_s)$ replaces the vertex $v_s$ by its children $v_t$ and $v_u$ and adds the faces $f_l$ and $f_r$, and its record holds the four neighbor faces $f_{n0}, \ldots, f_{n3}$ across the outer edges of $f_l$ and $f_r$. The splits form a binary forest, the *vertex hierarchy*. A selectively refined mesh is given by a *front* $A$ of active vertices that meets each root to leaf path once. The other input is a view, given by the eye $e$, a view frustum and a screen-space tolerance $\tau$, and a test $\mathrm{qrefine}(v)$ that says whether the view needs the detail below $v$. The output, each frame, is a front such that no active vertex has $\mathrm{qrefine}$ true, and no legal collapse has $\mathrm{qrefine}$ of its parent false. Every change is a legal vsplit or a legal edge collapse.

## The algorithm

```pseudo id=main
VSPLIT-LEGAL(v)                                   ▷ v is active and has children
L1  return true if f_n0, f_n1, f_n2 and f_n3 of v are all present
ECOL-LEGAL(v_s)                                   ▷ the children v_t and v_u are active
L2  for each outer edge of f_l and f_r do return false if the face across it is not its f_nj
    return true

FORCE-VSPLIT(v0)
L3  stack ← [v0]
L4  while the stack is not empty do v ← the top of the stack
L5      if v is split then pop v
L6      else if v is not active then push parent(v)
L7      else if VSPLIT-LEGAL(v) then pop v and vsplit(v)
L8      else push the creator of each face f_nj of v that is not present

ADAPT-REFINEMENT(qrefine)                         ▷ one pass per frame
L9  for each active vertex v do
L10     if v has children and qrefine(v) then FORCE-VSPLIT(v)
L11     else if v has a parent p, ECOL-LEGAL(p) and not qrefine(p) then ecol(p)

QREFINE(v)                                        ▷ w = p_v - e, d = |w|
L12 if the sphere of radius r_v around p_v is outside the view frustum then return false
L13 if w · n_v > 0 and (w · n_v)^2 > d^2 sin^2(alpha_v) then return false   ▷ the normal cone faces away
L14 return mu_v^2 ≥ kappa^2 d^2 or delta_v^2 (d^2 - (w · nhat_v)^2) ≥ kappa^2 d^4
```

A face is *present* when the representatives of its three corners on the front are three distinct vertices. A vertex is *split* when it and all its ancestors are off the front, so it lies above the front. The *creator* of a face is the vertex whose vsplit adds it.

Lines L12 to L14 are the three parts of qrefine in Hoppe's Section 4. Line L12 uses a bounding sphere of the leaves below $v$, as on the [frustum culling](/frustum-culling/) page. Line L13 uses a cone of normals around $n_v$ with the half angle $\alpha_v$: when every normal in the cone points away from the eye, the region below $v$ faces away. Line L14 is the screen-space test in squared form, with $\kappa = \tau \tan(\varphi/2)/2$ for the field of view $\varphi$, that is $\kappa^2 = (2 \cot(\varphi/2))^{-2} \tau^2$. The *deviation space* of $v$ is given by $\mu_v$, a deviation in every direction, and $\delta_v$, a deviation along the unit normal $\hat n_v$. The test needs no square root and no division.

In the code the mesh is a height field with $y$ up, built by half-edge collapses, and $\mu_v = 0$. The value $\delta_v$ is the largest height jump of a split below $v$, and $r_v$ and the cone bound the leaves and the full-mesh faces below $v$. These values are heuristics, not the fitted bounds of the paper.

## Example

The test mesh is a $7 \times 7$ grid of heights, with 49 vertices and 72 faces. With the seed 0 the simplification makes 18 half-edge collapses, so the base mesh has 31 vertices and $72 - 2 \cdot 18 = 36$ faces. The vertices of the full mesh are 0 to 48, and the inner vertices of the hierarchy are 49 to 66.

**A forced split.** From the base mesh, FORCE-VSPLIT(50) asks for the split of vertex 50, whose children are the leaves at the domain points $(4, 3)$ and $(5, 4)$.

| step | lines | what happens | stack after, top last |
|---|---|---|---|
| 1 | L6 | 50 is not active; push the parents 56, 58, 66 | 50, 56, 58, 66 |
| 2 | L7 | 66 is a root and its split is legal | 50, 56, 58 |
| 3 | L7 | split 58, then 56 | 50 |
| 4 | L8 | two neighbor faces of 50 are missing; push their creators 54 and 61 | 50, 54, 61 |
| 5 | L6 | 61 is not active; push 62 and 64 | 50, 54, 61, 62, 64 |
| 6 | L8 | 64 needs a face of 65; push 65 | 50, 54, 61, 62, 64, 65 |
| 7 | L7 | split 65, 64, 62, 61, 54 and 50 | empty |

The call makes 9 vsplits in the order 66, 58, 56, 65, 64, 62, 61, 54, 50. The mesh grows from 31 active vertices and 36 faces to 40 vertices and 54 faces. Of the 18 inner vertices of this hierarchy, 50 is the one whose forced split needs the most vsplits.

**A sequence of views.** With the seed 8, six random views and $\tau$ between 0.05 and 0.4, repeated passes of ADAPT-REFINEMENT reach a fixed point. From the base mesh the first view takes 9 passes and 11 changes and ends with 44 active vertices and 62 faces. The next five views take 1, 1, 2, 2 and 2 passes, with 0, 0, 2, 2 and 1 changes. A small change of view needs a small number of changes, which is the reason to keep the front from frame to frame.

## Correctness

The proof file gives the arguments, and the tests check them on random hierarchies.

- **Present faces.** A face of the full mesh is present exactly when it is a base face or its creator is split. So the test of line L1 says that the creators of the four neighbor faces are split, and these creators come earlier in the vsplit order (a proved property).
- **force_vsplit ends.** Each vertex that lines L6 and L8 push is not split and has a smaller index in the vsplit order than the vertex below it. Between two vsplits the indices on top strictly decrease, so the loop makes a vsplit after at most $N$ pushes. A vsplit moves the front down, so there are at most $N$ of them. At the end $v_0$ is split, and every vsplit was legal (a proved property).
- **A fixed point.** If a pass of lines L9 to L11 makes no change, no active vertex asks for a split and no legal collapse is allowed. This is a fixed point, not an optimum: forced splits can leave vertices split that qrefine does not ask for (a proved property).
- **The screen-space test.** The squared test of line L14 holds exactly when $\max(\mu_v,\ \delta_v |\hat n_v \times w| / d) / d \ge \kappa$, the angular size of the deviation space against $\kappa$ (a proved property, by Lagrange's identity).
- **A valid mesh.** On random sequences of legal vsplits and collapses, the tests check that each directed edge occurs once, that the border is a cycle and that the Euler characteristic is 1. This is a measurement, not a proof; the paper gives no proof of it. In 12 of 1200 such states one face of the height field was folded over in the domain, so the legality conditions do not keep the orientation of the faces.

## Complexity

A pass of ADAPT-REFINEMENT tests each of the $a$ active vertices once. Each vsplit or collapse costs $O(1)$ with the face neighbor pointers of the paper, and force_vsplit makes at most $N$ pushes per vsplit, so a pass costs $O(a + s N)$ in the worst case. In practice a forced split needs few ancestors, as in the example. The paper keeps the active vertices in a list and the hierarchy in arrays, which take $\Theta(n)$ space for the $n$ vertices of the full mesh, and it runs one pass per frame. The code is simpler: its collapse test scans the faces, so it shows the logic and not the speed.

## Properties

- **Local.** The mesh is fine only where qrefine asks for it, so the triangle count follows the view, not the size of the model.
- **Legal at every step.** Every change keeps the faces of the mesh in the places that the vsplit records expect (a proved property of the legality tests).
- **Coherent.** The front is kept from one frame to the next, and a small move of the camera gives few changes (a measurement on the example).
- **Not unique.** The result depends on the order of the active vertices and on the history of forced splits, so two runs that reach the same view along different paths can give different meshes.
- **Pops.** A vsplit changes the mesh at once. Hoppe hides this with geomorphs over a few frames, or with a small $\tau$.

## Variants and improvements

- **Geomorphs.** Each vsplit and each collapse can be made a [geomorph](/geomorphing/) over a short time, so that the change does not pop.
- **A face budget.** In place of a fixed $\tau$, a renderer can change $\tau$ from frame to frame so that the number of faces stays near a target (a tuning).
- **Terrain.** Hoppe (1998) applies the same refinement to large terrains in blocks. Regular structures such as [ROAM](/roam-terrain/) and [geometry clipmaps](/geometry-clipmaps/) trade the general hierarchy for simpler data.
- **Other hierarchies.** Xia and Varshney, and Luebke and Erikson, gave view-dependent hierarchies of vertex merges at the same time; the general idea is the same, with other legality conditions.
- **On the GPU.** Later systems refine clusters of triangles in place of single vertices, so that each change is a batch.

## When to use it

Use view-dependent refinement for a single large mesh that is near and far at the same time, such as a terrain, a scanned object or a building seen from inside, when a few discrete levels of detail would be too coarse near the viewer or waste triangles far away. For many small objects, discrete [levels of detail](/level-of-detail/) cost less. For a height field on a grid, [ROAM](/roam-terrain/) or [geometry clipmaps](/geometry-clipmaps/) are simpler and need no vsplit records.

## Pitfalls

- **Splitting without the neighbor test.** If line L7 runs vsplit(v) without line L1, the new faces $f_l$ and $f_r$ attach to faces that are not there, and the mesh gets a hole or overlapping faces.
- **Collapsing without the edge test.** If line L11 collapses $p$ without line L2, a face that a later split expects as a neighbor can be gone, and the next vsplit of a vertex next to it is never legal.
- **The tests in the wrong order.** A split vertex is also not active. If line L6 comes before line L5, it pushes the parent of a split vertex, the loop climbs above the front, and at a split root there is no parent to push.
- **The wrong power of d.** Line L14 compares squares. If the second part uses $\kappa^2 d^2$ in place of $\kappa^2 d^4$, it tests $\delta_v |\hat n_v \times w| / d \ge \kappa$, which does not fall with the distance, so far regions are refined as much as near ones.
- **The wrong side of the cone.** If line L13 tests $w \cdot n_v < 0$, it culls the regions that face the eye and keeps the ones that face away.
- **Bounds that are too small.** If $r_v$ in line L12 bounds only the vertex positions of the current mesh and not the leaves below $v$, a region at the border of the frustum can be culled while some of its faces are still in view.

## Implementations

## History

Hoppe introduced progressive meshes in 1996 and their view-dependent refinement at SIGGRAPH 97. The second paper added the vertex hierarchy, the neighbor faces in each vsplit record that make the legality test local, force_vsplit for splits whose neighbors are missing, and a screen-space test that projects a deviation space with no division. At about the same time Xia and Varshney and Luebke and Erikson published other view-dependent simplification schemes. Hoppe applied the method to large terrains in 1998, and later work moved the refinement to clusters of triangles that suit the GPU.

## References
