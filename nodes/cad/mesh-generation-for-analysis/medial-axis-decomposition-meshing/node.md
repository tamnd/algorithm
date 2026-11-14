---
tag: NAAF85
kind: technique
slug: medial-axis-decomposition-meshing
name: Medial axis decomposition meshing
aliases:
- Tam-Armstrong decomposition
area: cad/mesh-generation-for-analysis
level: advanced
summary: Tam and Armstrong's method that splits a domain at its medial axis into simple subdomains, then meshes each with mapped quadrilaterals or hexahedra.
prereqs: [medial-axis, hexahedral-mesh-generation, transfinite-interpolation-grid, mixed-integer-programming]
see_also: [hexahedral-sweeping, structured-grid-generation, paving, polycube-hex-meshing, quadtree-mesh-generation, hexahedral-mesh-existence-theorem, straight-skeleton, mesh-quality-measures]
sources:
  - paper: "T. K. H. Tam and C. G. Armstrong, 2D finite element mesh generation by medial axis subdivision, Advances in Engineering Software 13, 1991"
    locator: the decomposition of a planar domain at its medial axis and the meshing of the parts by templates (general locator)
  - paper: "T. S. Li, R. M. McKeag and C. G. Armstrong, Hexahedral meshing using midpoint subdivision and integer programming, Computer Methods in Applied Mechanics and Engineering 124(1-2), 1995, 171 to 193"
    locator: midpoint subdivision of simple polygons and polyhedra, and the assignment of the numbers of intervals by integer programming (general locator)
  - paper: "M. A. Price, C. G. Armstrong and M. A. Sabin, Hexahedral mesh generation by medial surface subdivision, part I, solids with convex edges, International Journal for Numerical Methods in Engineering 38(19), 1995, 3335 to 3359"
    locator: the 3D method for solids with convex edges (general locator)
  - paper: "M. A. Price and C. G. Armstrong, Hexahedral mesh generation by medial surface subdivision, part II, solids with flat and concave edges, International Journal for Numerical Methods in Engineering 40(1), 1997, 111 to 136"
    locator: the extension to flat and concave edges (general locator)
  - paper: "Alla Sheffer, Michal Etzion, Ari Rappoport and Michel Bercovier, Hexahedral mesh generation using the embedded Voronoi graph, Engineering with Computers 15(3), 1999, 248 to 262"
    locator: the decomposition into sweepable parts from a simpler Voronoi structure (general locator)
  - paper: "Nico Pietroni, Marcel Campen, Alla Sheffer, Gianmarco Cherchi, David Bommes, Xifeng Gao, Riccardo Scateni, Franck Ledoux, Jean-François Remacle and Marco Livesu, Hex-mesh generation and processing, a survey, arXiv 2202.12670, 2022"
    locator: the paragraph on medial descriptors in the section on domain decomposition, with the limits of the approach
---

Medial axis decomposition meshing cuts a domain into simple parts along its [medial axis](/medial-axis/), the set of centers of the largest disks or balls that fit inside, and meshes each part with a fixed pattern of quads or hexes. Tam and Armstrong gave the method for planar domains in 1991. Price, Armstrong and Sabin extended it to solids in 1995 and 1997, with the medial surface in place of the medial axis. The parts are chosen so that each one is a triangle, a quadrilateral, a pentagon or a simple polyhedron that midpoint subdivision can fill. The numbers of mesh intervals on all edges are then chosen together, by an integer program, so that the parts match.

This page is one method for [hexahedral mesh generation](/hexahedral-mesh-generation/), and it fills a solid only when its medial surface cuts it into parts with known patterns, while that page states the general problem and its limits.

## In plain words

The medial axis is the skeleton of a shape. For a long thin plate it is a line down the middle, and at a T joint the skeleton has a branch point. Each piece of the skeleton tells you a region of the shape that is like a strip, and each branch point a region where strips meet.

So you cut the shape along lines from the skeleton to the boundary. Strips become four-sided parts, which a grid fills. Branch points become three-sided or five-sided parts, which you split from a center point into one four-sided part per corner. Then you decide how many elements go along each edge. Neighbouring parts must agree, and each part has its own rules, such as an even total. A small integer program finds counts close to the wanted element size that obey all rules.

## When it applies

- The domain is a planar region or a solid whose medial axis or medial surface can be computed and is stable: small bumps of the boundary must be removed first, because each bump adds a new branch.
- The parts that the medial axis gives have a known pattern. For planar domains this is almost always so. For solids, Price and others treat convex edges first and then flat and concave edges. The survey of Pietroni and others notes that boundary vertices of high valence have no pattern.
- A structured look is wanted: long strips of regular elements along thin parts, as in sheet metal, ribs and blades.
- It does not apply well to shapes with many small features, or to organic shapes, where the medial surface has many branches and the parts become tiny.

## The template

Each part $P$ of the decomposition has sides, and a side of $P$ is either a curve of the boundary or a cut. Let $n_e$ be the number of mesh intervals on each side $e$, a positive integer, and let $t_e$ be the target $\operatorname{length}(e) / h$ for the element size $h$.

```pseudo id=main
MEDIAL-DECOMPOSITION-MESH(Ω, h)
L1  M ← the medial axis of Ω in 2D, or its medial surface in 3D
L2  cut Ω along curves (or surfaces) from the branch points of M to the boundary points that their disks (or balls) touch
L3  for each part P do choose a pattern by the number of sides: mapped grid, or midpoint subdivision
L4  for each part P do add the linear equations of its pattern on the counts n_e
L5  for each cut shared by two parts do use one count n_e for both
L6  solve min Σ_e w_e |n_e − t_e| subject to L4 and L5, with each n_e a positive integer
L7  for each part P do mesh P by its pattern with the counts n_e, filling each grid by transfinite interpolation
L8  smooth the inner vertices and check the element quality
```

The holes are the rules of L2 and L3, which differ from paper to paper, the weights $w_e$ of L6, and the smoothing of L8.

**The patterns of L3 and L4 in 2D.** A four-sided part is meshed by an $m \times n$ grid, which needs the counts of opposite sides to be equal. A part with $k = 3$ or $k \ge 5$ sides is split by midpoint subdivision: a new point $G$ inside, a new point $M_i$ on each side $i$, and the segments $G M_i$. This makes $k$ four-sided parts, one at each corner, and each is filled by a grid.

**Claim (the triangle).** A triangle with counts $a$, $b$ and $c$ on its three sides has a midpoint subdivision into three grids if and only if $a + b + c$ is even and $a < b + c$, $b < c + a$ and $c < a + b$.

**Proof.** Number the sides $1$, $2$ and $3$ with counts $a$, $b$ and $c$, and let $s_i$ be the count on the spoke $G M_i$. The corner part between the sides $i$ and $j$ is the four-sided part with corners $v$, $M_i$, $G$ and $M_j$, where $v$ is the shared vertex. Its side $v M_i$ is opposite to $G M_j$, and its side $v M_j$ is opposite to $G M_i$. A grid needs equal counts on opposite sides, so the piece of side $i$ next to $v$ has $s_j$ intervals. Side $1$ is made of two such pieces, one at each end, so $a = s_2 + s_3$, and in the same way $b = s_3 + s_1$ and $c = s_1 + s_2$. This linear system has the unique solution

$$s_1 = \frac{b + c - a}{2}, \qquad s_2 = \frac{c + a - b}{2}, \qquad s_3 = \frac{a + b - c}{2}.$$

Each $s_i$ must be a positive integer, because a spoke has at least one interval. The three values are integers exactly when $a + b + c$ is even, since $b + c - a = (a + b + c) - 2a$ and so on. They are positive exactly when the three strict triangle inequalities hold. Conversely, when both conditions hold, these $s_i$ give three grids of sizes $s_2 \times s_3$, $s_3 \times s_1$ and $s_1 \times s_2$ whose counts agree on every spoke and every side, so the subdivision exists. $\square$

The same argument for a part with $k$ sides gives the equations $n_i = s_{i-1} + s_{i+1}$, with indices taken modulo $k$. Adding them shows that the sum of the counts around the part must be even, which is the 2D form of the parity condition on the [existence theorem](/hexahedral-mesh-existence-theorem/) page. In 3D, Li, McKeag and Armstrong give similar equations and inequalities for the midpoint subdivision of tetrahedra, prisms and other simple solids. Collected over all parts, they form the integer program of L6. It is small, because it has one variable for each edge of the decomposition, not for each element.

**What is proved and what is measured.** The claim above and its 3D analogues are proved: when the integer program has a solution, every part has a valid pattern with matching counts. It is not proved that L2 always gives parts with patterns, and in 3D it does not. Nor is the shape of the elements proved: a midpoint subdivision of a thin triangle has a corner part with angles near $180°$. The quality of the final meshes is measured on test parts in the papers.

## Classic examples

- **A plate with a T joint (2D).** The medial axis of a T has three main branches that meet at one point, plus short branches to the convex corners. In the simplest form of the rules, the region around the branch point becomes a three-sided part and each arm becomes a long four-sided strip, which gets a grid along the arm. With counts $a = 4$, $b = 5$ and $c = 3$ on the triangle, the proof gives $s_1 = 2$, $s_2 = 1$ and $s_3 = 3$, so grids of $1 \times 3$, $3 \times 2$ and $2 \times 1$, which is $11$ quads. With $a = b = c = 3$ the sum is odd and the integer program must change one count. With $a = 4$ and $b = c = 1$ the sum is even, but $s_1 = -1$, so the counts must change too.
- **Solids with convex edges (3D).** Price, Armstrong and Sabin cut a solid along its medial surface into parts such as tetrahedra, prisms and cubes in the logical sense, and fill each by midpoint subdivision. The numbers of intervals come from the integer program of Li, McKeag and Armstrong. A tetrahedron splits into 4 hexes, one at each corner, by its edge midpoints, face centres and centroid.
- **Sweepable parts.** Sheffer and others use the embedded Voronoi graph, a simpler structure than the medial surface, to cut a solid into parts that can each be meshed by [hexahedral sweeping](/hexahedral-sweeping/). For tubes such as blood vessels, later methods use the curve skeleton in the same way.
- **Mapped grids.** Each four-sided part is a [structured grid](/structured-grid-generation/) made by [transfinite interpolation](/transfinite-interpolation-grid/). This is why the method gives long rows of regular elements along thin parts.

## Variations

- **The skeleton.** The exact medial axis is hard to compute for curved boundaries and changes a lot under small boundary changes. Methods use an approximation from a Voronoi diagram of boundary samples, the embedded Voronoi graph, or a [straight skeleton](/straight-skeleton/) for polygons.
- **Hex dominant.** Quadros (2014) uses the medial axis transform to guide an advancing front and accepts some elements that are not hexes.
- **Unstructured fill.** Instead of templates, each part can be meshed by [paving](/paving/) in 2D, which accepts any even count.
- **Interval assignment alone.** The integer program of L6 is useful in any block structured method, for example to match swept parts or manual blocks.

## Pitfalls

- **Unstable skeleton.** A small notch in the boundary adds a branch to the medial axis and so a new part. Without a filter on small branches, the decomposition follows noise.
- **Missing patterns.** In 3D some medial configurations, such as boundary vertices with many faces, have no midpoint pattern. Then the method stops or needs manual help.
- **Bad shape from good counts.** The counts can satisfy every equation while the element shape is bad, for example when a corner part of a triangle is long and narrow. Check the quality after L8 with [mesh quality measures](/mesh-quality-measures/).
- **Infeasible program.** If the targets are far from what the equations allow, the integer program changes many counts or has no solution with the bounds set. Relax the bounds or the weights, not the equations.

## Exercises

1. A quadrilateral part is split by midpoint subdivision into four grids. Show that its side counts $n_1, n_2, n_3, n_4$ must satisfy $n_1 = n_3$ and $n_2 = n_4$, so the subdivision gives nothing that a single grid cannot give. *Hint:* the equations are $n_i = s_{i-1} + s_{i+1}$ modulo 4.
2. For a pentagon, solve $n_i = s_{i-1} + s_{i+1}$ modulo 5 for the spokes $s_i$. *Answer:* $s_i = (n_{i-1} + n_i + n_{i+1} - n_{i+2} - n_{i+3})/2$. This is an integer exactly when $n_1 + \dots + n_5$ is even, and the subdivision exists when, in addition, each $s_i$ is positive.
3. Count the quads of the triangle with $a = 6$, $b = 6$ and $c = 4$. *Answer:* the spokes are $2$, $2$ and $4$, so $2 \cdot 4 + 4 \cdot 2 + 2 \cdot 2 = 20$ quads.

## References
