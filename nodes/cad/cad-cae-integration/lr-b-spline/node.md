---
tag: G8C6QC
kind: data-structure
slug: lr-b-spline
name: Locally refined B-spline
aliases:
- LR B-spline
- LR-spline
area: cad/cad-cae-integration
level: research
summary: Dokken, Lyche and Pettersen's splines refined by inserting mesh lines that split the supports of B-splines one at a time, keeping a tensor-product flavour.
model: real-ram
complexity:
  vars: {b: the number of LR B-splines before the insertion, s: the number of splits, m: the number of mesh segments, p: the larger of the two degrees}
  time: {worst: O((b + s) m p), average: O((b + s) m p), best: O(b m p)}
  space: {extra: O(b + s)}
properties: {deterministic: true, recursive: false}
history:
  year: 2013
  people: [Tor Dokken, Tom Lyche, Kjell Fredrik Pettersen]
  note: Dokken, Lyche and Pettersen defined LR B-splines on locally refined box partitions in 2013. Bressan studied their linear independence in 2013, and Johannessen, Kvamsdal and Dokken used them for adaptive isogeometric analysis in 2014.
prereqs: [b-spline, tensor-product-surface, boehm-knot-insertion, partition-of-unity]
see_also: [hierarchical-b-spline, truncated-hierarchical-b-spline, t-spline, pht-spline, analysis-suitable-t-spline, isogeometric-analysis, knot-refinement, oslo-algorithm]
sources:
  - paper: doi:10.1016/j.cagd.2012.12.005
    title: Tor Dokken, Tom Lyche and Kjell Fredrik Pettersen, Polynomial splines over locally refined box-partitions, Computer Aided Geometric Design 30(3) (2013), 331 to 356
    locator: the LR mesh, the definition of LR B-splines with weights, the splitting by one-knot insertion, and the refinement by mesh lines (general locator)
  - paper: doi:10.1016/j.cagd.2013.06.004
    title: Andrea Bressan, Some properties of LR-splines, Computer Aided Geometric Design 30(8) (2013), 778 to 794
    locator: linear independence and local linear independence of LR B-splines (general locator)
  - paper: doi:10.1016/j.cma.2013.09.014
    title: Kjetil André Johannessen, Trond Kvamsdal and Tor Dokken, Isogeometric analysis using LR B-splines, Computer Methods in Applied Mechanics and Engineering 269 (2014), 471 to 514
    locator: refinement strategies for analysis and numerical tests of adaptive isogeometric analysis with LR B-splines (general locator)
---

LR B-splines are a way to refine a tensor product [B-spline](/b-spline/) surface locally. You insert one axis-parallel mesh segment at a time. Every B-spline whose support the segment crosses from one side to the other is split in two by the insertion of one knot into its local knot vector, and the split repeats until no mesh line crosses a support without being one of its knots. Each B-spline carries a positive weight, so that the weighted B-splines still sum to 1, and the surface does not change. Dokken, Lyche and Pettersen introduced them in 2013. Each function stays a tensor product B-spline with its own local knots.

## In plain words

Think of a surface made of smooth tiles, one per bump function, laid out on a grid. To add detail in one place, draw a new line on the grid, but only as long as you need.

Each bump that the new line cuts fully from one edge to the other is replaced by two narrower bumps. A bump that the line only touches or reaches into stays as it is. The two new bumps may be cut by lines that were already there, so you keep cutting until no line cuts any bump fully.

Each bump has a weight, and when it is cut, the weight is shared between the two pieces. Two pieces of different bumps can turn out to be the same bump; then you add their weights. The shape of the surface never changes, and the weighted bumps always add up to 1.

## The abstract type

An LR spline of bidegree $(p, q)$ is a set of triples $(B, \gamma, c)$. $B$ is a tensor product B-spline given by its local knot vectors $x_0 \le \cdots \le x_{p+1}$ and $y_0 \le \cdots \le y_{q+1}$, $\gamma > 0$ is its weight, and $c$ is its coefficient, a number or a control point. The spline is

$$s(x, y) = \sum \gamma\, c\, B(x, y), \qquad \sum \gamma\, B(x, y) = 1.$$

The mesh is a set of axis-parallel segments. A segment at $x = a$ *traverses* $B$ if $x_0 < a < x_{p+1}$, $a$ is not one of the $x_i$, and the segment covers $[y_0, y_{q+1}]$; the same with the roles of $x$ and $y$ swapped for a horizontal segment. The operations are:

- INSERT$(\sigma)$: add a segment $\sigma$ to the mesh and split the B-splines until no B-spline is traversed. The segment must traverse at least one B-spline.
- EVALUATE$(x, y)$: the value $s(x, y)$, or $\sum \gamma B(x, y)$.

## Representation

The B-splines are a hash map from the pair of local knot vectors to the pair $(\gamma, c)$. The mesh is a hash map from a direction and a value to a sorted list of disjoint intervals; a new segment is merged with the collinear segments that it overlaps or touches. All mesh lines in this implementation have multiplicity one. The start is a tensor product spline on open knot vectors: every tensor B-spline with weight 1, and every knot line over the whole domain.

The split uses the one-knot rule for a single B-spline. Insert $a$ with $x_0 < a < x_{p+1}$ into the local knots $x_0, \ldots, x_{p+1}$. Let $\tau$ be the $p + 3$ sorted knots, $B_1$ the B-spline on $\tau_0, \ldots, \tau_{p+1}$ and $B_2$ the one on $\tau_1, \ldots, \tau_{p+2}$. Then

$$B = \alpha_1 B_1 + \alpha_2 B_2, \qquad \alpha_1 = \min\Bigl(1, \frac{a - x_0}{x_p - x_0}\Bigr), \quad \alpha_2 = \min\Bigl(1, \frac{x_{p+1} - a}{x_{p+1} - x_1}\Bigr),$$

with $\alpha_1 = 1$ if $x_p = x_0$ and $\alpha_2 = 1$ if $x_{p+1} = x_1$. This is [Boehm's rule](/boehm-knot-insertion/) applied to the unit coefficient vector of one B-spline.

## Operations

```pseudo id=main
INSERT(σ)
L1  add σ to the mesh, merged with the collinear segments it touches
L2  Q ← all LR B-splines
L3  while Q is not empty do take B from Q
L4      μ ← a mesh line that traverses B; if there is none, go to L3
L5      remove (B, γ, c) from the set
L6      (B₁, α₁), (B₂, α₂) ← insert the value of μ into the local knots of B
L7      for i ← 1, 2 do
L8          merge (Bᵢ, γ αᵢ, c) into the set
L9          add Bᵢ to Q
```

Line L8 adds $(B_i, \gamma\alpha_i, c)$ if $B_i$ is new. If $B_i$ is already present as $(B_i, \gamma', c')$, it becomes $(B_i, \gamma' + \gamma\alpha_i, (\gamma' c' + \gamma\alpha_i c) / (\gamma' + \gamma\alpha_i))$. INSERT refuses a segment that splits no B-spline, and then leaves the mesh and the set unchanged. EVALUATE sums $\gamma c B(x, y)$ with each factor of $B$ computed by the Cox-de Boor recursion on its local knots.

## Example

Take biquadratic B-splines on the open knot vector $0, 0, 0, 1, 2, 3, 4, 4, 4$ in both directions, 36 tensor B-splines with weight 1. Insert the vertical segment $x = \tfrac32$ for $0 \le y \le 3$. It traverses the 9 B-splines with $x$ knots $(0, 0, 1, 2)$, $(0, 1, 2, 3)$ or $(1, 2, 3, 4)$ and support in $y$ inside $[0, 3]$. Each splits into two; for example $(0, 1, 2, 3)$ gives $\tfrac34 (0, 1, \tfrac32, 2) + \tfrac34 (1, \tfrac32, 2, 3)$. The pieces of neighbours meet: $(0, 1, \tfrac32, 2)$ also gets $\tfrac14$ from $(0, 0, 1, 2)$, and its weight is 1. The result has 39 B-splines, all with weight 1, as in a tensor product refinement of that region.

Now insert the horizontal segment $y = \tfrac32$ for $0 \le x \le 3$. It splits 13 B-splines and leaves 43. One of them, with knots $(1, \tfrac32, 2, 3)$ in both directions, has weight $\tfrac{15}{16}$. It gets $\tfrac34$ from the split of a B-spline that the first segment had already split. It also gets $\tfrac14 \cdot \tfrac34 = \tfrac{3}{16}$ through a cascade: the horizontal segment splits $(0, 1, 2, 3) \times (1, 2, 3, 4)$, and the old vertical segment then traverses the piece $(0, 1, 2, 3) \times (1, \tfrac32, 2, 3)$. The missing $\tfrac{1}{16}$ would come from $(1, 2, 3, 4) \times (1, 2, 3, 4)$, which neither segment traverses. The weighted sum is still 1 at every point.

## Correctness

Each split replaces $\gamma c B$ by $\gamma\alpha_1 c B_1 + \gamma\alpha_2 c B_2$, which is the same function by the one-knot rule, and $\gamma B$ by $\gamma\alpha_1 B_1 + \gamma\alpha_2 B_2$. A merge replaces $\gamma' c' B_i + \gamma\alpha_i c B_i$ by one term with the summed weight and the weighted mean coefficient, again the same function. So the spline and the weighted sum do not change; the sum starts at 1 by the [partition of unity](/partition-of-unity/) of tensor B-splines. The weights stay positive because each $\alpha_i$ is in $(0, 1]$. The loop terminates, because each child has fewer mesh values strictly inside its support that are not among its knots than its parent. When it stops, no B-spline is traversed. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Let $b$ be the number of LR B-splines before the insertion, $s$ the number of splits, $m$ the number of mesh segments and $p$ the larger degree. The queue processes the $b$ old B-splines and at most $2s$ children. Each one is tested against every mesh line, and each test looks up the value among $p + 2$ knots, so INSERT takes $O((b + s) m p)$ time. A spatial index of the B-splines by cell reduces the work to the B-splines near the segment. The queue and the new B-splines take $O(b + s)$ extra space. EVALUATE takes $O(p^2)$ time per B-spline, or per B-spline that is nonzero at the point with a cell index.

## Variants

- **Refinement strategies.** Johannessen, Kvamsdal and Dokken compare ways to choose the segments in adaptive analysis: segments that split only the marked elements, segments over the full support of the B-splines on them, and the split of chosen B-splines through the middle of their longest knot interval. The tests use the last one.
- **Higher multiplicity.** A mesh line may have multiplicity up to the degree plus one, to lower the smoothness across it. The traversal rule then counts the multiplicity of the value among the local knots.
- **Trivariate LR B-splines.** The same splitting works with box partitions in three dimensions, with planes instead of lines.
- **Related local refinement.** [T-splines](/t-spline/) use one global T-mesh and infer the local knots from it, and [hierarchical](/hierarchical-b-spline/) and [truncated hierarchical B-splines](/truncated-hierarchical-b-spline/) use dyadic levels. LR B-splines refine by single knot insertions, so all tensor B-splines of the refined parts stay ordinary B-splines.

## When to use it

Use LR B-splines when you want local refinement that keeps every basis function an ordinary tensor B-spline with its own knots, as in adaptive [isogeometric analysis](/isogeometric-analysis/) or local surface fitting, and when the refinement is not tied to dyadic levels. If you need guaranteed linear independence without checks, prefer [truncated hierarchical B-splines](/truncated-hierarchical-b-spline/) or [analysis-suitable T-splines](/analysis-suitable-t-spline/), or restrict the meshes as the literature describes.

## Pitfalls

- **Linear dependence.** LR B-splines can be linearly dependent on some meshes. Dokken, Lyche and Pettersen discuss linear independence and how to check it, and Bressan relates local linear independence to how many B-splines cover each element. Test the result if the method needs a basis.
- **Forgetting the cascade.** Splitting only the B-splines that the new segment traverses is not enough. The children can be traversed by old mesh lines, as in the example, and must be split too.
- **Dropping the weights.** Without the weights $\gamma$, the B-splines of a refined LR mesh do not sum to 1, and merged B-splines double count.
- **Segments that split nothing.** A segment that traverses no B-spline adds a line to the mesh that no basis function sees. The definition forbids it.
- **Exact arithmetic for the knot test.** The traversal test compares knot values. With floating point values from repeated midpoints, use exact numbers or a tolerance.

## Implementations

The Python module stores the B-splines and the mesh in hash maps, implements the one-knot split, INSERT of lines L1 to L9 with merging, and EVALUATE by Cox-de Boor on local knots, all with fractions. The tests check the one-knot split against direct evaluation for degrees 1 to 3 and repeated knots, that full-length lines give the tensor product refinement of Boehm's rule on the coefficient net, the counts and the weight $\tfrac{15}{16}$ of the example, that the weighted sum is 1 at random points after random refinements with positive weights, that the surface is unchanged after each insertion, that no B-spline is left traversed, and that a segment that splits nothing is refused.

## History

Dokken, Lyche and Pettersen defined LR B-splines over locally refined box partitions in 2013, as a local refinement that keeps the tensor structure of each basis function. In the same year Bressan studied their linear independence. Johannessen, Kvamsdal and Dokken used LR B-splines for adaptive isogeometric analysis in 2014 and compared refinement strategies.

## References
