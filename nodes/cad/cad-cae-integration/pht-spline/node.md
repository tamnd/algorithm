---
tag: BQ9V8S
kind: data-structure
slug: pht-spline
name: Polynomial spline over hierarchical T-mesh
aliases:
- PHT-spline
area: cad/cad-cae-integration
level: research
summary: Deng and coauthors' C1 bicubic splines on a hierarchical T-mesh built from vertex basis functions, with simple local refinement for adaptive analysis.
model: real-ram
complexity:
  vars: {V: the number of vertices after the step, L: the number of levels, n: the number of basis functions before the step, r: the number of cells split in the step}
  time: {worst: O(V L + n r), average: O(V L + n r), best: O(V L + n r)}
  space: {extra: O(V + n r)}
properties: {deterministic: true, recursive: false}
history:
  year: 2008
  people: [Jiansong Deng, Falai Chen, Xin Li, Changqi Hu, Weihua Tong, Zhouwang Yang, Yuyu Feng]
  note: Deng, Chen, Li, Hu, Tong, Yang and Feng defined PHT-splines in 2008, after Deng, Chen and Feng's 2006 dimension formula for spline spaces over T-meshes. Nguyen-Thanh and coauthors used them for isogeometric analysis in 2011.
prereqs: [b-spline, tensor-product-surface, parametric-continuity, partition-of-unity]
see_also: [hierarchical-b-spline, truncated-hierarchical-b-spline, t-spline, lr-b-spline, analysis-suitable-t-spline, isogeometric-analysis, bezier-patch, de-casteljau-algorithm]
sources:
  - paper: doi:10.1016/j.gmod.2008.03.001
    title: Jiansong Deng, Falai Chen, Xin Li, Changqi Hu, Weihua Tong, Zhouwang Yang and Yuyu Feng, Polynomial splines over hierarchical T-meshes, Graphical Models 70(4) (2008), 76 to 86
    locator: the hierarchical T-mesh, the basis vertices, the level by level construction of the basis with modification of the old functions, and its properties (general locator)
  - paper: doi:10.1016/j.cam.2005.07.009
    title: Jiansong Deng, Falai Chen and Yuyu Feng, Dimensions of spline spaces over T-meshes, Journal of Computational and Applied Mathematics 194(2) (2006), 267 to 283
    locator: the dimension formula for spline spaces over T-meshes, which gives 4(V_b + V_+) for C1 bicubic splines on hierarchical T-meshes (general locator)
  - paper: doi:10.1016/j.cagd.2019.07.001
    title: Qian Ni, Xuhui Wang and Jiansong Deng, Modified PHT-splines, Computer Aided Geometric Design 73 (2019), 37 to 53
    locator: Section 2.3, formula (1), the dimension formula; Definition 4, modification by setting the Bezier ordinates of the new basis vertices to zero; Definition 5 and Theorem 6, the basis and its properties, for meshes that also allow splits in half
  - paper: doi:10.1016/j.cma.2011.01.018
    title: N. Nguyen-Thanh, H. Nguyen-Xuan, S. P. A. Bordas and T. Rabczuk, Isogeometric analysis using polynomial splines over hierarchical T-meshes for two-dimensional elastic solids, Computer Methods in Applied Mechanics and Engineering 200(21-22) (2011), 1892 to 1908
    locator: adaptive isogeometric analysis of plane elasticity with PHT-splines (general locator)
  - paper: doi:10.1016/j.gmod.2015.06.011
    title: Hongmei Kang, Jinlan Xu, Falai Chen and Jiansong Deng, A new basis for PHT-splines, Graphical Models 82 (2015), 149 to 159
    locator: the decay of the original basis functions under some refinements, and a basis of tensor B-splines on 2 by 2 submeshes (general locator)
---

A PHT-spline is a function that is a bicubic polynomial on each cell of a hierarchical T-mesh and has continuous first derivatives. The mesh starts as a grid, and each refinement step splits some cells of the finest level into four by a cross. Deng, Chen, Li, Hu, Tong, Yang and Feng introduced the space and its basis in 2008. The space has dimension $4(V_b + V_+)$, where $V_b$ is the number of boundary vertices and $V_+$ the number of interior crossing vertices. Each such *basis vertex* carries four basis functions, so the spline is fixed by its value, its two first derivatives and its mixed derivative at the basis vertices. Because the continuity is only $C^1$, the T-junctions do not spread through the mesh, and refinement is simple and local. This makes PHT-splines a natural choice for adaptive [isogeometric analysis](/isogeometric-analysis/).

## In plain words

Lay a grid over a square and put a cubic patch on each cell, so that the surface and its slopes match across every edge. Where you need more detail, cut a cell into four by a cross. A new corner in the middle of a side can touch the side of a neighbour that was not cut. That is a T-junction.

Describe the surface by four numbers at each corner: the height, the two slopes and the twist. At a T-junction these numbers must be what the big neighbour cell has at that point, or the surface breaks. At the other corners they are free.

So each free corner gets four bumps. When you cut cells, the old bumps are set to zero at the new free corners, and four new small bumps are added there.

## The abstract type

A PHT-spline space on $[0, n]^2$ stores a hierarchical T-mesh and a basis of $S(3, 3, 1, 1, T)$, the $C^1$ functions that are bicubic on each leaf cell. The operations are:

- REFINE$(R)$: split each cell of $R$, which must be leaf cells of the finest level, into four by a cross, and update the basis.
- EVALUATE$(b, x, y)$: the value, the two first derivatives and the mixed derivative of a function at a point.
- COEFFICIENTS$(f)$: the coefficients on the basis of a spline given by its data at the basis vertices.

A vertex is a *boundary vertex* if it lies on the boundary of the square. An interior vertex is a *T-junction* if it lies inside a side of a leaf cell; this cell is its *host*. The other interior vertices are *crossings*. The basis vertices are the boundary vertices and the crossings.

## Representation

A cell $(\ell, i, j)$ is the square of side $h = 2^{-\ell}$ with lower left corner $(ih, jh)$. The leaves are a hash set. Every function is a sparse map from vertices to its *Hermite data* $(f, f_x, f_y, f_{xy})$ there. On each leaf cell the function is the bicubic Hermite interpolant of the data at its four corners, the tensor product of the cubic Hermite shapes in $x$ and $y$. So EVALUATE locates the leaf that contains the point and sums 16 products.

The basis has four functions for each basis vertex $v$, one for each pair $(\alpha, \beta) \in \{0, 1\}^2$. Let $\ell$ be the level at which $v$ became a basis vertex and $h = 2^{-\ell}$. In one direction, the two $C^1$ cubic [B-splines](/b-spline/) of $v$ have the knots $(v - h, v - h, v, v, v + h)$ and $(v - h, v, v, v + h, v + h)$; at the boundary the outside knots are replaced by $v$. With $h_-$ and $h_+$ the spacings on the two sides of $v$, $0$ at the boundary, and $H = h_- + h_+$, their values and slopes at $v$ are

$$\Bigl(\frac{h_+}{H}, -\frac{3}{H}\Bigr) \text{ and } \Bigl(\frac{h_-}{H}, \frac{3}{H}\Bigr).$$

The data of the function $(v, \alpha, \beta)$ at $v$ are the products of the pair $\alpha$ in $x$ and the pair $\beta$ in $y$: value times value, slope times value, value times slope, and slope times slope. Its data at every other basis vertex are zero. Its data at T-junctions are stored too, so that every leaf can be evaluated from its own corners.

## Operations

```pseudo id=main
REFINE(R)                                           ▷ R: leaf cells of the finest level K
L1  split each cell of R into four by a cross; K ← K + 1; classify the vertices
L2  N ← the basis vertices that were not basis vertices before; their level is K
L3  for each basis function b do
L4      for each new vertex w of a split cell P where b is not zero: data_b(w) ← (f, f_x, f_y, f_xy) of b on P at w
L5      for each v in N: data_b(v) ← 0
L6  for each v in N and (α, β) ∈ {0, 1}²: add the function with data D_v(α, β) at v and 0 elsewhere
```

Line L4 is the subdivision of the old polynomial on the split cell, the Hermite form of [de Casteljau](/de-casteljau-algorithm/) subdivision of a [Bézier patch](/bezier-patch/). Line L5 is the modification of Deng and coauthors: the old function keeps its data at the old vertices and gets zero data at the new basis vertices. The classification in line L1 tests, for each vertex and each level, whether the cells of that level to its left and right, or below and above, are leaves that contain the vertex inside a side.

COEFFICIENTS uses the dual functionals of the B-splines: at a basis vertex with data $(f, f_x, f_y, f_{xy})$, the coefficient of $(v, \alpha, \beta)$ is $f + s_\alpha f_x + t_\beta f_y + s_\alpha t_\beta f_{xy}$, with $s_0 = -h_-/3$ and $s_1 = h_+/3$ in $x$, and $t_0, t_1$ the same in $y$.

## Example

Take $n = 2$. The level 0 mesh has 9 vertices, all basis vertices, and 36 basis functions, the tensor products of the $C^1$ cubic B-splines on the knots $0, 0, 0, 0, 1, 1, 2, 2, 2, 2$. The function of the centre $(1, 1)$ with $\alpha = \beta = 0$ has the knots $(0, 0, 1, 1, 2)$ in both directions and the data $(\tfrac14, -\tfrac34, -\tfrac34, \tfrac94)$ at $(1, 1)$.

Split the cell $[0, 1]^2$. The centre $(\tfrac12, \tfrac12)$ is a crossing, and $(\tfrac12, 0)$ and $(0, \tfrac12)$ are boundary vertices, so there are 12 basis vertices and 48 functions. The midpoints $(1, \tfrac12)$ and $(\tfrac12, 1)$ lie inside sides of the cells $[1, 2] \times [0, 1]$ and $[0, 1] \times [1, 2]$, so they are T-junctions. The function of $(1, 1)$ above had the value $\tfrac{49}{256}$ at $(\tfrac12, \tfrac12)$. After the step its data there are zero, its value at $(\tfrac34, \tfrac34)$ falls from $\tfrac{6561}{16384}$ to $\tfrac{649}{2048}$, and its value at $(\tfrac32, \tfrac32)$ stays $\tfrac{1}{256}$. Its data at the T-junction $(1, \tfrac12)$ are $(\tfrac{7}{32}, -\tfrac{21}{32}, \tfrac{9}{16}, -\tfrac{27}{16})$, which are the values of the host cell's polynomial there.

Now split $[\tfrac12, 1]^2$. Only its centre is a new basis vertex; its four side midpoints are T-junctions. The mesh has 13 basis vertices and 6 T-junctions, and the space has dimension 52. A direct count of all piecewise bicubics with the $C^1$ conditions across every shared edge also gives 52.

## Correctness

The proof rests on one fact about hierarchical T-meshes. Every T-junction lies inside a side of exactly one leaf cell, its host, and the corners of the host appeared at an earlier step than the T-junction. A $C^1$ piecewise bicubic has well defined Hermite data at every vertex, including the mixed derivative. On each cell it is the Hermite interpolant of its corner data, and the data at a T-junction are those of the host's polynomial. By induction over the steps, the data at the basis vertices fix all data, and any data at the basis vertices extend to a $C^1$ function. So the map to the data at the basis vertices is a bijection and the dimension is $4(V_b + V_+)$.

The constructed functions are in the space, because lines L4 and L5 keep the T-junction data equal to the host's. Each function has data only at its own basis vertex, given by an invertible $4 \times 4$ block, so the functions are a basis. The blocks of one vertex sum to $(1, 0, 0, 0)$, so the functions sum to 1. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Let $V$ be the number of vertices after the step, $L$ the number of levels, $n$ the number of basis functions before the step and $r$ the number of split cells. The classification in line L1 does $O(L)$ hash lookups per vertex, so $O(V L)$. Lines L3 to L5 test each old function against each split cell and compute at most five new data per cell, so $O(n r)$; with an index of the functions by cell, only the $O(r)$ functions near the split cells do work. Line L6 adds $O(r)$ functions. The extra space is $O(V)$ for the classification and $O(n r)$ for the new data in the worst case. EVALUATE takes $O(L)$ time to locate the cell and $O(1)$ to evaluate.

## Variants

- **Modified PHT-splines.** Ni, Wang and Deng also allow a cell to be split in half, horizontally or vertically, and build the basis in the same way.
- **Bases without decay.** Under some refinements the modified old functions become very small, which hurts the condition number. Kang, Xu, Chen and Deng proposed a basis of tensor B-splines on $2 \times 2$ submeshes, at the cost of partition of unity, and later work restores partition of unity with weights.
- **Other degrees.** Spline spaces over T-meshes with bidegree $(m, n)$ and smoothness $(\alpha, \beta)$ have a simple dimension formula when $m \ge 2\alpha + 1$ and $n \ge 2\beta + 1$, by Deng, Chen and Feng. Bicubic $C^1$ is the case used in practice.
- **Related local refinement.** [Hierarchical](/hierarchical-b-spline/) and [truncated hierarchical B-splines](/truncated-hierarchical-b-spline/), [T-splines](/t-spline/) and [LR B-splines](/lr-b-spline/) keep $C^2$ cubic splines, so a refinement affects a larger region.

## When to use it

Use PHT-splines for adaptive analysis and surface fitting where $C^1$ continuity is enough, for example second order problems in [isogeometric analysis](/isogeometric-analysis/), and where you want a refinement that only touches the split cells and their neighbours. Their Hermite data also make interpolation of given values and derivatives at the vertices direct. For problems that need $C^2$ continuity or the higher smoothness of B-splines, use [truncated hierarchical B-splines](/truncated-hierarchical-b-spline/) or [analysis-suitable T-splines](/analysis-suitable-t-spline/).

## Pitfalls

- **Free data at T-junctions.** The data at a T-junction must be those of the host's polynomial. Setting them freely gives a function that is not $C^1$, and the tests show the jump in the slope.
- **Splitting a coarse cell late.** The construction assumes that each step splits leaf cells of the finest level. Splitting an older cell can turn a T-junction into a crossing, and then the basis update needs extra care.
- **Decay of the basis.** Repeated refinement around the same region can make modified old functions very small. Watch the condition number, or use a basis that does not decay.
- **Lower smoothness.** The functions are only $C^1$, so the continuity across cells is lower than for cubic B-splines with simple knots, and the number of functions per cell is higher.

## Implementations

The Python module stores the leaves in a hash set and each basis function as exact Hermite data at the vertices, classifies the vertices, refines by lines L1 to L6, evaluates by bicubic Hermite interpolation, and computes the coefficients of a spline from its data. The tests check that level 0 gives the tensor $C^1$ cubic B-splines of a Cox-de Boor reference, the counts of the example, that the number of functions equals $4(V_b + V_+)$ and the dimension of a brute force system of all piecewise bicubics with $C^1$ conditions, linear independence by exact rank, partition of unity, $C^1$ continuity across every T-junction by one-sided finite differences fitted exactly with cubics, that wrong T-junction data break it, that one step equals the subtraction formula of Deng and coauthors with B-splines of the new level, nested spaces, and nonnegativity at sample points.

## History

Deng, Chen and Feng gave the dimension of spline spaces over T-meshes in 2006. In 2008 Deng, Chen, Li, Hu, Tong, Yang and Feng defined PHT-splines on hierarchical T-meshes, with the level by level basis and its use for surface fitting. Nguyen-Thanh, Nguyen-Xuan, Bordas and Rabczuk used them for isogeometric analysis of elastic solids in 2011. Later work changed the basis to avoid decay and allowed splits in half.

## References
