---
tag: 948WA8
kind: technique
slug: surface-area-heuristic
name: Surface area heuristic
aliases: [SAH]
area: graphics-and-signals/ray-tracing
level: advanced
summary: Rate a split of a ray tracing tree by its expected cost for a uniform random ray, a traversal step plus, per child, area ratio times primitive count times test cost, and take the cheapest.
prereqs: [bounding-volume-hierarchy, axis-aligned-bounding-box]
see_also: [bvh-construction, spatial-splits, lbvh-construction, kd-tree-traversal, bvh-refitting, bounding-volume, greedy-algorithm, bounding-interval-hierarchy]
sources:
  - paper: doi:10.1109/MCG.1987.276983
    title: Jeffrey Goldsmith and John Salmon, Automatic creation of object hierarchies for ray tracing, IEEE Computer Graphics and Applications 7(5), 1987, 14 to 20
    locator: the conditional probability that a ray that hits a parent volume hits a child, estimated by the ratio of the surface areas, and the cost of a hierarchy
  - paper: doi:10.1007/BF01911006
    title: J. David MacDonald and Kellogg S. Booth, Heuristics for ray tracing using space subdivision, The Visual Computer 6(3), 1990, 153 to 166
    locator: the cost of a split as a traversal cost plus the area-weighted counts of the two sides, its assumptions, and the greedy choice of the split plane
  - paper: doi:10.1109/RT.2006.280216
    title: Ingo Wald and Vlastimil Havran, On building fast kd-trees for ray tracing, and on doing that in O(N log N), IEEE Symposium on Interactive Ray Tracing 2006, 61 to 69
    locator: the SAH for kd-trees with primitives counted on both sides, the bonus for empty space, and the sweep over sorted events in O(n log n)
  - paper: doi:10.1109/RT.2007.4342588
    title: Ingo Wald, On fast construction of SAH-based bounding volume hierarchies, IEEE Symposium on Interactive Ray Tracing 2007, 33 to 40
    locator: the SAH evaluated only at bin boundaries
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 4, Section 4.3.2 The Surface Area Heuristic, and Section 4.4 Kd-Tree Accelerator for the kd-tree form
  - book: isbn:9780521523448
    title: Luis A. Santaló, Integral Geometry and Geometric Probability, second edition, Cambridge University Press, 2004
    locator: the measure of the lines that meet a convex body in space, which is proportional to its surface area
---

The **surface area heuristic** (SAH) is a cost model for the trees that speed up ray tracing. It estimates how much work a random ray costs when it meets a node: one traversal step $c_t$, plus, for each child, the chance that the ray also meets the child times the number of primitives in it times the cost $c_i$ of one primitive test. The chance is the ratio of the surface areas of the child and the parent, which is exact for uniform random lines and convex volumes. Goldsmith and Salmon (1987) used the area ratio for object hierarchies, and MacDonald and Booth (1990) made it the rule for choosing a split plane. The builder evaluates the cost of a set of candidate splits and takes the cheapest, or makes a leaf when a leaf costs less.

## In plain words

Picture a big box with a small box inside it. Throw straight lines at the big box from all directions, with no favorite direction or position. Some of the lines that hit the big box also hit the small one. The fraction is the surface area of the small box over the surface area of the big one.

So when you split a group of objects into two boxes, you can guess how much work a ray will cost: one step to look at the two boxes, plus for each box the chance to hit it times the number of objects in it. Small boxes with many objects and big boxes with few objects are both fine. A big box with many objects is costly. Try many splits and keep the one with the lowest guess.

## When it applies

- The structure is a tree of convex cells or volumes: a [bounding volume hierarchy](/bounding-volume-hierarchy/) of boxes, a kd-tree of cells, or a [bounding interval hierarchy](/bounding-interval-hierarchy/).
- The rays can be seen as uniform random lines that meet the root. The model assumes that the rays are lines, with no favored direction or origin, and that a ray is not stopped by a hit, so every node it meets is visited.
- The cost of a traversal step $c_t$ and of a primitive test $c_i$ are constants. Only the ratio $c_t/c_i$ changes the choice.
- The builder is greedy: when it rates a split of a node, it treats the two children as leaves. So the SAH gives the best split for one node, not the best tree.

**The probability.** For convex sets $B \subseteq A$ and lines from the measure that is invariant under rotations and translations, $P(\text{the line meets } B \mid \text{it meets } A) = S(B)/S(A)$, where $S$ is the surface area. This is Cauchy's formula of integral geometry: the measure of the lines that meet a convex body is proportional to its surface area. A flat convex set counts both of its sides. The implementation checks the formula by sampling lines for three boxes inside $[0, 4] \times [0, 2] \times [0, 1]$, one of them flat.

**The cost of a tree.** Applying the rule at every node, a tree $T$ has the expected cost

$$C(T) = \frac{1}{S(\text{root})} \Big( \sum_{v \text{ inner}} c_t\, S(v) + \sum_{v \text{ leaf}} c_i\, N(v)\, S(v) \Big),$$

where $N(v)$ is the number of primitives in the leaf $v$. The same value comes from the recurrence $C(v) = c_t + \sum_{w \text{ child of } v} \frac{S(w)}{S(v)} C(w)$ with $C(v) = c_i N(v)$ at a leaf. The implementation checks that both forms agree.

## The template

The holes are CANDIDATES, the set of splits to try; SIDES, which gives the two parts and their volumes; and the constants $c_t$ and $c_i$. The volume of a part is its box for a BVH, or its half of the cell for a kd-tree.

```pseudo id=main
SAH-SPLIT(P, V)                                  ▷ P: the primitives of the node, V: its volume
L1  best ← (leaf, c_i · |P|)
L2  for each split s in CANDIDATES(P, V) do
L3      (L, V_L, R, V_R) ← SIDES(s)
L4      cost ← c_t + c_i · (S(V_L) · |L| + S(V_R) · |R|) / S(V)
L5      if cost < the cost of best then best ← (s, cost)
L6  return best
```

The implementation fills the holes for a BVH. CANDIDATES are the $n - 1$ splits of the primitives sorted by the center of their boxes on each axis, and SIDES gives the boxes of the two parts. A sweep from the right stores the area and count of every right part, and a sweep from the left gives every left part, so all candidates of an axis cost $O(n)$ after an $O(n \log n)$ sort. A test checks the sweep against a direct $O(n^2)$ evaluation.

**Example.** Six unit cubes $[c, c + 1] \times [0, 1] \times [0, 1]$ lie at $c = 0, 1, 2, 3, 4, 18$, with $c_t = c_i = 1$. The root box $[0, 19] \times [0, 1] \times [0, 1]$ has $S = 2(19 + 1 + 19) = 78$. A leaf costs 6. The split after the fifth cube has the boxes $[0, 5]$ with $S = 22$ and the last cube with $S = 6$, so it costs $1 + (22 \cdot 5 + 6 \cdot 1)/78 \approx 2.49$, the least of all candidates. The median split, after the third cube, has the boxes $[0, 3]$ with $S = 14$ and $[3, 19]$ with $S = 66$, and costs $1 + (14 \cdot 3 + 66 \cdot 3)/78 \approx 4.08$.

## Classic examples

- [BVH construction](/bvh-construction/): the binned SAH build of Wald (2007) fills CANDIDATES with the $K - 1$ boundaries of $K$ centroid bins per axis.
- SAH kd-trees, walked by [kd-tree traversal](/kd-tree-traversal/): the candidates are the planes through the faces of the primitive boxes, and a primitive that straddles a plane counts on both sides. Wald and Havran (2006) sweep the sorted events of all three axes once per level, which gives $O(n \log n)$.
- [Spatial splits](/spatial-splits/): the SBVH rates object splits and spatial splits, which clip primitives at a plane, with the same cost, and takes the cheaper.
- [LBVH construction](/lbvh-construction/): the HLBVH builds the top levels of the tree with the SAH over clusters of primitives that share a Morton prefix.
- [BVH refitting](/bvh-refitting/): the SAH cost of the refitted tree, compared with the cost after the last build, tells when to rebuild.

## Variations

- **Binned SAH.** Try only the boundaries of $K$ equal bins, for $O(n)$ work per node. With 8 to 32 bins the trees are close to those of the full sweep.
- **Empty space bonus.** For kd-trees, a split that cuts off an empty cell gets its cost scaled by a factor below 1, so the tree tends to wrap the objects tightly (Wald and Havran 2006).
- **Termination.** Make a leaf when $c_i |P|$ is not more than the best split, or at a fixed size. Some builders also bound the depth.
- **Other ray distributions.** For a known set of rays, such as the camera rays of one view, the area ratio can be replaced by a measured or projected probability. The ray distribution heuristic and occlusion-aware variants are of this kind.
- **Overlap and end points.** Aila, Karras and Laine (2013) found that the SAH cost does not always predict the speed of a BVH well, because real rays start on surfaces and end at hits, and proposed corrections for the overlap of sibling boxes and for the points where rays end.
- **Wide trees.** For trees with 4 or 8 children, the same cost has one term per child, and the builder chooses how to merge a binary SAH tree into wide nodes.

## Pitfalls

- **Volume instead of area.** Line L4 must use the surface area. A flat box, such as the box of triangles in one plane, has volume 0 and would look free, while a ray can still hit it.
- **A parent of area 0.** If all primitives of a node lie on a line or at a point, $S(V) = 0$ and line L4 divides by zero. Compare the sums $S(V_L)|L| + S(V_R)|R|$ directly, since $S(V)$ is the same for all candidates of a node, and make a leaf.
- **An empty side.** A candidate with $L$ or $R$ empty has the cost $c_t + c_i |P|$ and splits nothing. CANDIDATES must not return it, or line L5 must skip it, else the builder can loop on the same set.
- **Straddling primitives in kd-trees.** In a kd-tree, line L3 must count a primitive that crosses the plane in both $L$ and $R$. Counting it once makes splits through dense parts look cheap, and the tree grows without bound.
- **Reading the cost as a time.** The SAH cost is an estimate under uniform random lines. Real rays begin inside the scene and stop at the first hit, so nodes deep inside closed objects are visited less often than the model says. Use it to compare splits, not to predict render times.
- **The wrong ratio of constants.** Only $c_t / c_i$ changes the choice in line L5. A ratio far too low gives deep trees with tiny leaves; a ratio far too high gives large leaves.

## Exercises

1. Unroll the recurrence $C(v) = c_t + \sum_w \frac{S(w)}{S(v)} C(w)$ from the root and show that it gives the closed form of $C(T)$ above.
2. For two concentric spheres of radii $r \le R$, show that a uniform random line that meets the large sphere meets the small one with probability $r^2/R^2$. Check that this is the ratio of the surface areas.
3. Take $n$ unit cubes $[i, i + 1] \times [0, 1] \times [0, 1]$ for $i = 0, \ldots, n - 1$. Show that the split after the first $k$ cubes has $S(V_L) |L| + S(V_R) |R| = (4k + 2)k + (4(n - k) + 2)(n - k)$, and that it is least at $k = \lfloor n/2 \rfloor$ and $k = \lceil n/2 \rceil$.

## References
