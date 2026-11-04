---
tag: YMF8H3
kind: problem
slug: optimal-polygon-triangulation
name: Minimum-weight convex polygon triangulation
aliases:
- optimal polygon triangulation
area: techniques/dynamic-programming
level: core
summary: Triangulate a convex polygon so that the total weight of the triangles is minimal, by interval DP.
prereqs: [interval-dp, convex-polygon, catalan-numbers]
see_also: [polygon-triangulation-dp, min-weight-triangulation, matrix-chain-multiplication, interval-dp, catalan-numbers, optimal-binary-search-tree]
sources:
  - paper: doi:10.1137/0211028
    title: T. C. Hu and M. T. Shing, Computation of matrix chain products, part I, SIAM Journal on Computing 11(2), 362-373, 1982
    locator: the correspondence between orders of matrix-chain products and triangulations of a convex polygon with weights p_i p_k p_j
  - paper: doi:10.1016/s0167-5060(08)70044-x
    title: G. T. Klincsek, Minimal triangulations of polygonal domains, Annals of Discrete Mathematics (Combinatorics 79), 121-123, 1980
    locator: the O(n^3) dynamic program for minimum-length triangulations of polygons
  - paper: doi:10.1145/1346330.1346336
    title: Wolfgang Mulzer and Günter Rote, Minimum-weight triangulation is NP-hard, Journal of the ACM 55(2), 2008
    locator: the NP-hardness of minimum weight triangulation of a point set
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.2, Matrix-chain multiplication (the same recurrence and the count of parenthesizations)
---

The optimal polygon triangulation problem takes a convex polygon $v_0, v_1, \ldots, v_{n-1}$ and a weight function on triangles, and asks for a triangulation (a set of $n - 3$ non-crossing diagonals that cut the polygon into $n - 2$ triangles) of least total weight. With the triangle $v_i v_k v_j$ on each side $v_i v_j$, the problem has an [interval dynamic program](/interval-dp/) with $O(n^3)$ time, which is the same recurrence as [matrix-chain multiplication](/matrix-chain-multiplication/); Hu and Shing showed that the two problems are the same when the weight of $v_i v_k v_j$ is $p_i p_k p_j$. The algorithm itself, with its proof and code, is on the [polygon triangulation DP](/polygon-triangulation-dp/) page. For point sets that are not in convex position, the [minimum weight triangulation](/min-weight-triangulation/) problem is NP-hard.

## In plain words

Cut a convex polygon into triangles with straight cuts from corner to corner that do not cross. There are many ways to do it. Each triangle has a cost, for example its perimeter, and you want the cheapest set of triangles.

Look at one side of the polygon. In any answer, that side belongs to exactly one triangle, and the third corner of that triangle splits the rest of the polygon into two smaller convex polygons, one on each side. So try each possible third corner, solve the two smaller polygons, and keep the best. The smaller polygons are always runs of consecutive corners, so there are only about $n^2$ different ones.

## Definition

**Input.** A convex polygon with vertices $v_0, v_1, \ldots, v_{n-1}$ in order, $n \ge 3$, and a weight $w(v_i, v_k, v_j) \in \mathbb{R}$ for every triangle of three vertices.

**Triangulation.** A maximal set of diagonals (segments $v_i v_j$ between vertices that are not adjacent) that do not cross inside the polygon. Every triangulation of a convex $n$-gon has $n - 3$ diagonals and $n - 2$ triangles, and the number of triangulations is the [Catalan number](/catalan-numbers/) $C_{n-2} = \frac{1}{n-1}\binom{2n-4}{n-2}$.

**Output.** A triangulation $T$ that minimizes $\sum_{\triangle \in T} w(\triangle)$.

Common weights:

- the perimeter of the triangle;
- the sum of the lengths of the diagonals used (equivalent to the perimeter weight, see below);
- $w(v_i, v_k, v_j) = p_i p_k p_j$ for numbers $p_0, \ldots, p_{n-1}$, which encodes matrix chains.

## Variants

- **Diagonal length.** Minimize the total length of the diagonals. Each diagonal lies on two triangles and each side of the polygon on one, so the sum of the triangle perimeters is the perimeter of the polygon plus twice the diagonal length. The two objectives have the same optimal triangulations.
- **Maximum weight, or a bottleneck.** Maximize the total weight, or minimize the largest triangle weight. The same recurrence works with max, or with max in place of the sum.
- **Simple polygons.** For a simple polygon that is not convex, only the diagonals inside the polygon are allowed. Klincsek's dynamic program still runs in $O(n^3)$ time, after testing which diagonals are valid.
- **Point sets.** For $n$ points in general position, with no fixed polygon, the minimum total edge length triangulation is NP-hard (Mulzer and Rote). See [minimum weight triangulation](/min-weight-triangulation/).

## Examples

Take the convex hexagon

$$v_0 = (0, 0),\; v_1 = (4, 0),\; v_2 = (6, 2),\; v_3 = (5, 5),\; v_4 = (1, 6),\; v_5 = (-1, 3)$$

with the perimeter weight. It has $C_4 = 14$ triangulations. The best uses the diagonals $v_1 v_3$, $v_3 v_5$ and $v_1 v_5$, with the triangles $v_1 v_2 v_3$, $v_3 v_4 v_5$, $v_1 v_3 v_5$ and $v_0 v_1 v_5$. Its total perimeter is about 55.391, and the worst of the 14 triangulations has about 60.479. The diagonals have lengths $\sqrt{26} + \sqrt{40} + \sqrt{34} \approx 17.255$, the hexagon has perimeter about 20.882, and $20.882 + 2 \cdot 17.255 = 55.391$, as the variant above says. A check of all 14 triangulations confirms the optimum.

**Matrix chains.** For the matrix dimensions $p = (5, 4, 6, 2, 7)$, take a pentagon with vertex weights $p_0, \ldots, p_4$ and the triangle weight $p_i p_k p_j$. The best triangulation costs 158, the least number of scalar multiplications for $A_1 A_2 A_3 A_4$ computed on the [interval DP](/interval-dp/) page. The side $v_0 v_4$ stands for the whole product, and the apex of its triangle, $v_3$, is the last split of the product.

## Known algorithms

**Interval dynamic program, $O(n^3)$.** Let $t(i, j)$ be the least weight of a triangulation of the convex polygon $v_i, v_{i+1}, \ldots, v_j$, for $0 \le i < j \le n - 1$, with $t(i, i+1) = 0$. In a triangulation of this polygon, the side $v_i v_j$ lies on exactly one triangle $v_i v_k v_j$ with $i < k < j$, and the triangle cuts the rest into the polygons $v_i, \ldots, v_k$ and $v_k, \ldots, v_j$, which are triangulated independently. So

$$t(i, j) = \min_{i < k < j} \bigl( t(i, k) + t(k, j) + w(v_i, v_k, v_j) \bigr),$$

and the answer is $t(0, n-1)$. There are $O(n^2)$ pairs and $O(n)$ choices of $k$, so the time is $O(n^3)$ and the space $O(n^2)$. The [polygon triangulation DP](/polygon-triangulation-dp/) page has the full algorithm.

**Matrix-chain weights, $O(n \log n)$.** For the weight $p_i p_k p_j$, Hu and Shing gave an $O(n \log n)$ algorithm, based on the structure of optimal triangulations for these weights.

**Faster general methods.** When the weight has the form needed for [Knuth's optimization](/knuth-optimization/) (a weight that depends only on the side $v_i v_j$ and satisfies the quadrangle inequality and monotonicity), the time drops to $O(n^2)$. The perimeter weight depends on $k$ and does not have this form.

## Bounds

- $O(n^3)$ time for any triangle weight, by the dynamic program.
- For arbitrary triangle weights given as an oracle, the input has $\Theta(n^3)$ possible triangles, and any algorithm that does not look at a triangle can miss a very cheap one. So $\Omega(n^3)$ queries are needed in that model, and the dynamic program is optimal there.
- For the matrix-chain weights, $O(n \log n)$ by Hu and Shing.

## Reductions

- **Matrix-chain multiplication is a special case.** Hu and Shing: the parenthesizations of $A_1 \cdots A_{n-1}$, where $A_i$ is $p_{i-1} \times p_i$, correspond one to one to the triangulations of an $n$-gon with vertex weights $p_0, \ldots, p_{n-1}$, and the cost of a parenthesization is the total weight $\sum p_i p_k p_j$ of the triangles. Each product of two subchains is a triangle, and the side $v_0 v_{n-1}$ is the full product.
- **Binary trees.** Triangulations of an $n$-gon correspond to full binary trees with $n - 1$ leaves (the dual tree, rooted at the triangle on $v_0 v_{n-1}$). This explains the Catalan count and links the problem to [optimal binary search trees](/optimal-binary-search-tree/) and other interval problems.
- **To point set triangulation.** A convex polygon is a point set in convex position, where the minimum weight triangulation becomes this polynomial problem.

## Applications

- **Matrix-chain ordering**, through the reduction above.
- **Computer graphics and meshing**, where a polygon face is split into triangles and short diagonals or well-shaped triangles are wanted.
- **Teaching.** A geometric face of the interval DP pattern, often taught next to matrix chains.

## References
