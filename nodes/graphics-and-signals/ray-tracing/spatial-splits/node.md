---
tag: C37NSZ
kind: technique
slug: spatial-splits
name: Spatial splits
aliases: [spatial split BVH]
area: graphics-and-signals/ray-tracing
level: advanced
summary: Let a BVH builder also cut space at a plane and clip the primitives that cross it, so one reference can be in both children, and keep the cut when its SAH cost beats the best object split.
prereqs: [bvh-construction, surface-area-heuristic]
see_also: [bounding-volume-hierarchy, kd-tree-traversal, bvh-traversal, lbvh-construction, bounding-interval-hierarchy, axis-aligned-bounding-box, sutherland-hodgman, polygon-window-clipping]
sources:
  - paper: doi:10.1145/1572769.1572771
    title: Martin Stich, Heiko Friedrich and Andreas Dietrich, Spatial splits in bounding volume hierarchies, High Performance Graphics 2009, 7 to 13
    locator: the SBVH, with the spatial split candidates, the chopped binning of references, the overlap threshold alpha, and reference unsplitting
  - paper: doi:10.1109/RT.2007.4342588
    title: Ingo Wald, On fast construction of SAH-based bounding volume hierarchies, IEEE Symposium on Interactive Ray Tracing 2007, 33 to 40
    locator: the binned SAH object split that the SBVH extends
  - paper: doi:10.1109/RT.2006.280216
    title: Ingo Wald and Vlastimil Havran, On building fast kd-trees for ray tracing, and on doing that in O(N log N), IEEE Symposium on Interactive Ray Tracing 2006, 61 to 69
    locator: the clipping of triangles to the cells of a kd-tree to get tight boxes for the SAH, the same split clipping that spatial splits use
---

**Spatial splits** add to a [BVH builder](/bvh-construction/) a second kind of split. An object split puts each primitive into one of two groups, so the two child boxes can overlap. A spatial split cuts the box of the node at a plane, as a kd-tree does; a primitive that crosses the plane is clipped, and a reference to it with the box of its part goes into each child. The builder rates both kinds with the [surface area heuristic](/surface-area-heuristic/) and keeps the cheaper. Stich, Friedrich and Dietrich (2009) called the result the split BVH (SBVH). It gives the tight, nonoverlapping nodes of a kd-tree where they help, and keeps the bounded size of a BVH elsewhere, since spatial splits are only tried when the object split overlaps.

## In plain words

Some scenes have long, thin triangles that cross the whole scene, such as a long wire or a slanted floor. A normal BVH must put each triangle into one box. The box that gets the long triangle becomes as big as the scene, and every ray has to look into it.

A spatial split cuts the scene into a left half and a right half with a wall. A long triangle that crosses the wall goes into both halves, but each half only records the part of the triangle on its side, so each half keeps a small box. The cost is that the triangle is now listed twice. The builder counts both costs and only cuts when it pays.

## When it applies

- The structure is a [BVH](/bounding-volume-hierarchy/) of boxes built top down with the SAH.
- The scene has primitives that are large compared with their neighbors, or long and slanted, so that the best object split leaves two child boxes that overlap a lot.
- The primitives can be clipped by an axis-aligned plane and the box of a part can be computed. For triangles this is [polygon clipping](/polygon-window-clipping/) by [Sutherland-Hodgman](/sutherland-hodgman/) against the six planes of a box.
- More memory per primitive is acceptable, since a primitive can be in many leaves, and a build two to a few times slower than a binned build is acceptable. The traversal is the plain [BVH traversal](/bvh-traversal/); nothing changes in it.

## The template

A reference is a pair (primitive, box of the part of the primitive in the current node). At the root each reference has the full box of its primitive. The holes are OBJECT-SPLIT, the object split search of the builder; CLIP, which gives the box of the part of a primitive inside a box; the number $K$ of spatial bins; and the threshold $\alpha$.

```pseudo id=main
SPLIT-NODE(R, B)                                 ▷ R: the references of the node, B: their box
L1  (c_o, L_o, R_o) ← OBJECT-SPLIT(R)
L2  if A(B(L_o) ∩ B(R_o)) > α · A(root box) then
L3      for each axis a, cut B into K equal bins; for each reference r, add CLIP(r, bin k) to the box of bin k for each bin k that r spans, count an entry in its first bin and an exit in its last bin
L4      sweep the planes j between the bins: B(L) = union of bins below j, N(L) = entries below j; B(R) = union of bins from j on, N(R) = exits from j on
L5      (c_s, a, plane) ← the least SAH cost c_t + c_i (A(B(L)) N(L) + A(B(R)) N(R)) / A(B) with N(L) < |R| and N(R) < |R|
L6  take the cheaper of the object split and the spatial split; make a leaf if that is cheaper still and |R| is small
L7  for a spatial split, give each reference that spans the plane two new references, CLIP(r, below the plane) and CLIP(r, above the plane)
```

Line L2 is the guard of Stich et al.: spatial splits are tried only when the two boxes of the best object split overlap in an area that is more than the fraction $\alpha$ of the area of the root. With $\alpha = 1$ no spatial split is ever tried and the builder is a plain SAH builder; with $\alpha = 0$ they are tried at every node whose object split overlaps at all. Line L3 is the *chopped binning*: a reference is added to every bin it spans, with the box of its part in that bin, and is counted once on each side by its first and last bin, so the sweep of line L4 gives the exact counts and boxes of the two children of every plane. Line L5 accepts a plane only if each child has fewer references than the node, which keeps the build finite even when many primitives meet at one point.

The implementation clips triangles exactly with rational numbers and checks on random scenes that each reference box lies inside its leaf box, that the parts of each triangle cover it, that the logged cost of each split is the SAH cost of the children it made, and that closest-hit and any-hit answers equal a brute force over all triangles.

**Example.** Three triangles: a long one $(0, 0, 0)$, $(16, 8, 0)$, $(16, 8, 1)$ across the scene, a small one $(0, 0, 0)$, $(2, 0, 0)$, $(0, 2, 1)$ near the origin, and a small one $(14, 8, 0)$, $(16, 8, 0)$, $(16, 6, 1)$ in the far corner. The root box is $[0, 16] \times [0, 8] \times [0, 1]$ with area 304; $c_t = c_i = 1$, $K = 4$, $\alpha = 0$.

| split at the root | left box | right box | $A(L) N(L) + A(R) N(R)$ | SAH cost |
|---|---|---|---|---|
| leaf | | | | 3 |
| best object split: {small near 0} against {long, far small} | $[0, 2] \times [0, 2] \times [0, 1]$, area 16 | the whole root box, area 304 | $16 \cdot 1 + 304 \cdot 2 = 624$ | $1 + 624/304 \approx 3.05$ |
| spatial split at $x = 4$ | $[0, 4] \times [0, 2] \times [0, 1]$, area 28 | $[4, 16] \times [2, 8] \times [0, 1]$, area 180 | $28 \cdot 2 + 180 \cdot 2 = 416$ | $\approx 2.37$ |
| spatial split at $x = 8$ | $[0, 8] \times [0, 4] \times [0, 1]$, area 88 | $[8, 16] \times [4, 8] \times [0, 1]$, area 88 | $88 \cdot 2 + 88 \cdot 2 = 352$ | $1 + 352/304 \approx 2.16$ |

The object split must put the long triangle on one side, and that side's box is the whole root box. The spatial split at $x = 8$ clips the long triangle into the part $[0, 8] \times [0, 4] \times [0, 1/2]$ on the left and $[8, 16] \times [4, 8] \times [0, 1]$ on the right, so both children are small. With leaves of one reference, the SBVH has 4 references and the SAH cost $169/76 \approx 2.22$, against 3 references and $59/19 \approx 3.11$ for the tree with object splits only.

## Classic examples

- The SBVH of Stich, Friedrich and Dietrich (2009) is the template above on top of the [binned SAH build](/bvh-construction/).
- SAH kd-trees, walked by [kd-tree traversal](/kd-tree-traversal/), use only spatial splits: every split is a plane, each primitive that crosses it goes to both sides, and Wald and Havran (2006) clip triangles to the cells for tight boxes in the [SAH](/surface-area-heuristic/).
- Early split clipping (Ernst and Greiner 2007) splits large triangles before the build into several references with smaller boxes, and then runs a plain object-split builder. It is the same idea done once, globally, without the SAH choice at each node.
- The [bounding interval hierarchy](/bounding-interval-hierarchy/) goes the other way: it keeps object splits only, but chooses its planes like a kd-tree.

## Variations

- **Reference unsplitting.** For a reference that spans the chosen plane, Stich et al. also test whether putting the whole reference into the left child, or into the right child, gives a lower cost than putting it into both, and do so if it does. This removes many duplicates.
- **Spatial splits without clipping.** A cheaper builder bins only the box of each reference and splits the box at the plane, without clipping the primitive. The boxes are larger but the build is faster.
- **Presplitting.** Split the largest triangles before the build, as in early split clipping, or by a fixed edge length, and use any builder.
- **Bounding the duplication.** Many builders stop spatial splits when the number of references exceeds a fixed multiple of the number of primitives, or below a certain depth.
- **Parallel and GPU builders.** The chopped binning of line L3 is a parallel loop over references, and GPU builders apply spatial splits to the top levels of a tree.

## Pitfalls

- **Clipping the triangle to the bin and not to the reference box.** In line L3 the part must be the primitive clipped to the intersection of the bin and the current reference box. Clipping the whole primitive to the bin brings back parts that an earlier split already moved to the other child, and the boxes grow.
- **Counting a spanning reference once.** Line L4 must count a reference that spans the plane on both sides, by its entry bin and its exit bin. Counting it once makes spatial splits look cheaper than they are.
- **No progress.** If line L5 accepts a plane with $N(L) = |R|$ or $N(R) = |R|$, the child can have the same references as the node, and a fan of triangles around one vertex makes the builder cut forever toward that vertex.
- **Boxes from float clipping.** In floating point, a clipped part can be rounded to a box that is slightly smaller than the true part. The box of a part must be rounded outward, or intersected with the reference box after a conservative clip, so that no part of the primitive falls outside every leaf.
- **Testing the part in the leaf.** The leaf must test the whole primitive, not the clipped part. A hit found in a leaf can then lie outside the leaf box, which is correct for the closest-hit query, as the proof of [BVH traversal](/bvh-traversal/) allows any number of leaves per primitive.
- **Too small an $\alpha$ and too many bins.** Spatial splits at every node and many bins multiply the build time and the memory. The guard in line L2 keeps them where they pay.

## References
