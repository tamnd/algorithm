---
tag: A5KM8D
kind: algorithm
slug: consistent-mesh-orientation
name: Consistent mesh orientation
aliases:
- face orientation propagation
area: cad/mesh-processing
level: intro
summary: Orients all faces of a connected mesh alike by a traversal that flips each neighbour whose shared edge runs the same way, then fixes outward normals by volume sign.
solves: [mesh-repair-problem]
model: real-ram
complexity:
  vars: {c: "the number of corners, the sum of the face sizes"}
  time: {worst: O(c) expected}
  space: {extra: Θ(c)}
properties: {deterministic: true, recursive: false, exact: true}
prereqs: [manifold-mesh, breadth-first-search]
see_also: [indexed-face-set, bipartite-graph, connected-components, generalized-winding-number, mesh-repair-problem, corner-table, ray-casting, euler-poincare-formula]
sources:
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 8, Model Repair (inconsistent orientation as a type of artifact, and its repair)
  - paper: doi:10.1145/2431211.2431214
    title: Marco Attene, Marcel Campen and Leif Kobbelt, Polygon mesh repairing, an application perspective, ACM Computing Surveys 45(2), Article 15, 2013
    locator: the parts on orientation defects and on the methods that fix them
  - url: http://jcgt.org/published/0003/04/02/
    title: Kenshi Takayama, Alec Jacobson, Ladislav Kavan and Olga Sorkine-Hornung, A simple method for correcting facet orientations in polygon meshes based on ray casting, Journal of Computer Graphics Techniques 3(4), 2014, 53 to 63
    locator: the method of visibility sampling by rays, for meshes where the traversal of this page does not apply
---

Consistent mesh orientation gives all faces of a [manifold mesh](/manifold-mesh/) the same orientation, so that the two faces of each inner edge go along it in opposite directions, and then turns each closed part so that its normals point out. It is a [breadth-first search](/breadth-first-search/) over the faces: a face keeps its vertex order, and a neighbour is reversed when the shared edge runs the same way in both. If the search reaches a face a second time with the opposite demand, the part is not orientable, like a Möbius strip. For a closed part, the exact sign of the signed volume decides between the two orientations. The time is linear in the size of the mesh. It is one of the first steps of [mesh repair](/mesh-repair-problem/).

## In plain words

Each face of a mesh lists its corners in some order, and the order tells which side is the front. Two faces next to each other agree when they walk their shared side in opposite directions, like two gears that turn together.

Start at any face and trust it. Look at each neighbour. If it walks the shared side the same way, reverse its corner list. Then do the same from the neighbours, until every face of the piece is done. If you come back to a face that you already fixed and it now needs the other order, no fix exists: the piece is one-sided.

At the end the whole piece agrees, but it may face inward. For a closed piece, add up the signed volume that its faces enclose. If the sum is negative, reverse every face of the piece.

## The problem

The input is a mesh as an [indexed face set](/indexed-face-set/): vertex positions and faces, where each face is a list of distinct vertex indices. Each edge has one or two faces. The output reverses some faces, so that for each edge-connected part:

- if the part is orientable, the two faces of each inner edge use it in opposite directions, and
- if the part is also closed and bounds a region, the outward normal of each face follows the right-hand rule for its vertex order.

If a part is not orientable, the output says so. Three or more faces on one edge make the question ill-posed, so the algorithm rejects such a mesh; [mesh repair](/mesh-repair-problem/) must split the edge first.

## The algorithm

For an edge $e = \{u, v\}$ with $u < v$, a face $f$ has the direction $d_f(e) = +1$ if it goes from $u$ to $v$, and $-1$ if it goes from $v$ to $u$. The bit $s_f$ is 1 when face $f$ will be reversed.

```pseudo id=main
ORIENT(F, P)
L1  E ← map from each edge {u, v} to its uses (f, d_f(e)); fail if an edge has 3 or more uses
L2  s_f ← unset for every face f
L3  for each face r with s_r unset do                ▷ a new component K
L4      s_r ← 0; Q ← [r]; K ← [r]
L5      while Q is not empty do
L6          f ← the first face of Q, removed
L7          for each edge e of f with a second face g do
L8              want ← s_f xor [d_f(e) = d_g(e)]     ▷ reverse g when it runs the same way
L9              if s_g is unset then s_g ← want; append g to Q and to K
L10             else if s_g ≠ want then mark K not orientable
L11     if K is orientable and has no border edge then
L12         W ← Σ det(p_a, p_b, p_c) over the fan triangles (a, b, c) of the faces of K, as oriented by s
L13         if W < 0 then s_f ← 1 − s_f for every f in K
L14 return each face f, reversed if s_f = 1
```

Line L8 is the whole rule. If $f$ is not reversed, $g$ must be reversed exactly when it runs the same way as $f$. If $f$ is reversed, the demand is the opposite. Line L12 is six times the signed volume of the part, computed with the [determinant](/determinant/) of each triangle and the origin.

**The predicate and its failure.** Lines L1 to L10 use only vertex indices, so they are exact on any input. Line L13 is a sign test. In floating point, $W$ is a sum of many terms of both signs, and for a thin or far-from-the-origin part the rounding errors can be larger than the result, through [catastrophic cancellation](/catastrophic-cancellation/). The code of this page uses integer or rational coordinates, so the sign is exact. With floating point input, an exact sum of the products, as in [Shewchuk's expansion arithmetic](/shewchuk-expansion-sum/), gives the true sign. Moving the origin to a vertex of the part also makes the terms smaller.

## Example

Take the tetrahedron $0 = (0,0,0)$, $1 = (1,0,0)$, $2 = (0,1,0)$, $3 = (0,0,1)$ with the faces $f_0 = (0, 1, 2)$, $f_1 = (0, 1, 3)$, $f_2 = (1, 2, 3)$, $f_3 = (0, 2, 3)$. The faces $f_0$ and $f_3$ point inward, and $f_1$ and $f_2$ point outward.

| step | face | edge | directions | result |
|---|---|---|---|---|
| L4 | $f_0$ | | | $s_0 = 0$ |
| L8 | $f_0 \to f_1$ | $\{0, 1\}$ | both $0 \to 1$, the same | $s_1 = 1$ |
| L8 | $f_0 \to f_2$ | $\{1, 2\}$ | both $1 \to 2$, the same | $s_2 = 1$ |
| L8 | $f_0 \to f_3$ | $\{0, 2\}$ | $2 \to 0$ and $0 \to 2$, opposite | $s_3 = 0$ |
| L10 | $f_1, f_2, f_3$ | the other 3 edges | | no conflict |

Now the oriented faces are $(0, 1, 2)$, $(3, 1, 0)$, $(3, 2, 1)$, $(0, 2, 3)$, all pointing inward. In line L12 every term with the vertex 0 at the origin is zero, so $W = \det(p_3, p_2, p_1) = -1$. The sign is negative, so line L13 reverses all four faces. The result is $(2, 1, 0)$, $(0, 1, 3)$, $(1, 2, 3)$, $(3, 2, 0)$ with $W = 1$, six times the volume $1/6$ of the tetrahedron.

For the Möbius strip with the five triangles $(i, i+1, i+2)$, indices mod 5, the search sets the bits around the band in both directions. The band has five inner edges, and the five labels $\lambda$ have an odd sum, so the last check of an edge that closes the band asks for the opposite bit. Line L10 marks the strip as not orientable.

## Correctness

Write the condition for an inner edge $e$ between $f$ and $g$ as $s_f \oplus s_g = \lambda(e)$, where $\lambda(e) = 1$ when the two faces run the same way along $e$. This is a system of equations over the bits, one for each edge of the dual graph, the graph with a node for each face and an edge for each inner edge. The search sets the bits along a spanning tree of each component so that the tree equations hold. Each other edge is then checked. If a check fails, no assignment works, because the tree forces every bit once the first bit is chosen. If no check fails, the assignment works, and its complement is the only other one. This is the same parity argument as the test of a [bipartite graph](/bipartite-graph/). For a closed part that bounds a region, $W/6$ is the volume of the region when the normals point out, by the divergence theorem, and minus the volume when they point in. The full proof is below.

## Complexity

Let $c$ be the number of corners, the sum of the face sizes. Line L1 builds a hash map of the edges in $O(c)$ expected time. The search puts each face in the queue once and looks at each edge of each face once, so lines L3 to L10 take $O(c)$ time. Line L12 adds $c - 2m$ determinants for $m$ faces. The total is $O(c)$ expected time and $\Theta(c)$ space. With exact arithmetic on integer coordinates of $b$ bits, each determinant has about $3b$ bits, and the sum of $c$ of them has $O(b + \log c)$ more.

## Properties

- **Exact.** The combinatorial part uses no arithmetic on coordinates. The volume sign is exact with exact arithmetic.
- **Unique up to the outward choice.** An orientable connected part has exactly two consistent orientations, and the volume picks one.
- **Detects non-orientable parts.** A Möbius strip or a Klein bottle gives a conflict in line L10.
- **Per component.** Parts that share only a vertex, not an edge, are separate components and are oriented separately.

## Variants and improvements

- **Union-find.** The same equations can be solved with a [disjoint-set](/disjoint-set/) structure with a parity bit on each link, which also works when the faces arrive one at a time.
- **Ray casting.** For meshes with holes, inner walls and parts that only touch, the outward side is not defined by a volume. Takayama and others cast many rays from each face and choose the side that is seen more often from outside. This is a heuristic: it is measured on a large set of models, not proved, and the [ray casting](/ray-casting/) costs much more than the search.
- **Winding numbers.** The [generalized winding number](/generalized-winding-number/) tells, for any point, how many times the mesh wraps around it, even for a mesh with holes. It can choose the outward side of each part after the search.
- **Non-manifold edges.** Some programs first cut the mesh at each edge with three or more faces, and then orient each piece. The result depends on how the faces at the edge are paired.

## When to use it

Use it after [vertex welding](/vertex-welding/) and before any step that needs normals, such as rendering with back-face culling, offsetting, [mesh Boolean operations](/mesh-boolean-operations/), or building a [corner table](/corner-table/) or a half-edge structure, which need a consistent orientation. The traversal is the right tool when the mesh is manifold and closed. If the mesh has holes or self-intersections, orient each part with the traversal and decide the outward side with a winding number or with rays.

## Pitfalls

- **Nested shells.** A solid with a cavity has an outer shell and an inner shell. The normals of the inner shell must point into the cavity, away from the material, so the inner shell has negative volume. The rule of line L13 makes both shells positive, and so it turns the inner shell the wrong way. Decide the side of each shell by how deeply it is nested inside the others.
- **Open parts.** A part with a border bounds no region, so $W$ has no meaning and depends on the origin. Do not flip open parts by the volume sign.
- **Self-intersecting parts.** If a closed part crosses itself, $W$ is a sum of volumes weighted by winding numbers, and its sign can be wrong for some regions.
- **Floating point volume.** A sum of many floating point determinants can have the wrong sign for a thin part far from the origin. Use exact arithmetic, or at least move the origin into the part.
- **Duplicate vertices.** Faces that should be neighbours but use different copies of a vertex are not joined, and each one is oriented alone. Weld first.

## Implementations

## History

The traversal is folklore of mesh processing and of solid modeling, and it is part of the repair steps that Botsch and others and Attene, Campen and Kobbelt describe. The parity argument is the same one that tells whether a graph is bipartite. In 2014 Takayama, Jacobson, Kavan and Sorkine-Hornung gave a method based on rays for the many models in online collections where the traversal does not apply, because the meshes are not manifold or not closed.

## References
