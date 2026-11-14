---
tag: 80ZTCE
kind: data-structure
slug: t-spline
name: T-spline
aliases:
- T-spline surface
area: cad/cad-cae-integration
level: advanced
summary: Sederberg's generalisation of NURBS whose control grid may have T-junctions, so control points can be added locally and patches joined watertight.
model: real-ram
complexity:
  vars: {a: the number of control points (anchors), m: the number of vertical index lines, n: the number of horizontal index lines}
  time: {worst: O(a (m + n)), average: O(a (m + n)), best: O(a (m + n))}
  space: {extra: O(a)}
properties: {deterministic: true, recursive: false}
history:
  year: 2003
  people: [Thomas W. Sederberg, Jianmin Zheng, Almaz Bakenov, Ahmad Nasri]
  note: Sederberg, Zheng, Bakenov and Nasri introduced T-splines and T-NURCCs at SIGGRAPH 2003. Sederberg and coauthors added local refinement and simplification in 2004, and Bazilevs and coauthors used T-splines for isogeometric analysis in 2010.
prereqs: [knot-vector, b-spline, cox-de-boor-recursion, nurbs, tensor-product-surface, boehm-knot-insertion]
see_also: [analysis-suitable-t-spline, t-spline-linear-independence, t-spline-local-refinement, isogeometric-analysis, hierarchical-b-spline, lr-b-spline, pht-spline, bezier-extraction]
sources:
  - paper: doi:10.1145/882262.882295
    title: Thomas W. Sederberg, Jianmin Zheng, Almaz Bakenov and Ahmad Nasri, T-splines and T-NURCCs, ACM Transactions on Graphics 22(3) (SIGGRAPH 2003), 477 to 484
    locator: the definition of the T-mesh, the rule that infers the local knot vectors of a control point from the T-mesh, and the point-based form of the surface (general locator)
  - paper: doi:10.1145/1015706.1015715
    title: Thomas W. Sederberg, David L. Cardon, G. Thomas Finnigan, Nicholas S. North, Jianmin Zheng and Tom Lyche, T-spline simplification and local refinement, ACM Transactions on Graphics 23(3) (SIGGRAPH 2004), 276 to 283
    locator: the local refinement of blending functions and the merging of NURBS patches (general locator)
  - paper: doi:10.1016/j.cma.2009.02.036
    title: Y. Bazilevs, V. M. Calo, J. A. Cottrell, J. A. Evans, T. J. R. Hughes, S. Lipton, M. A. Scott and T. W. Sederberg, Isogeometric analysis using T-splines, Computer Methods in Applied Mechanics and Engineering 199(5-8), 2010, 229 to 263
    locator: T-splines of odd and even degree in index space, and their use as a basis for analysis
  - paper: doi:10.1016/j.cagd.2011.08.005
    title: Xin Li, Jianmin Zheng, Thomas W. Sederberg, Thomas J. R. Hughes and Michael A. Scott, On linear independence of T-spline blending functions, Computer Aided Geometric Design 29(1), 2012, 63 to 76
    locator: Section 2 (review of T-splines, the local knot vectors of Figure 2) and Section 3 (the T-spline-to-NURBS matrix M and its computation by knot insertion)
  - paper: doi:10.1016/j.cma.2009.12.004
    title: A. Buffa, D. Cho and G. Sangalli, Linear independence of the T-spline blending functions associated with some particular T-meshes, Computer Methods in Applied Mechanics and Engineering 199(23-24), 2010, 1437 to 1445
    locator: the example of a T-mesh whose blending functions are linearly dependent
---

A T-spline is a spline surface whose control grid, the *T-mesh*, may have T-junctions: a line of the grid may stop in the middle of another line. Each control point gets its own blending function, a product of two cubic [B-splines](/b-spline/) whose knots are read from the T-mesh near the point. When the T-mesh is a full grid, the T-spline is a tensor product [NURBS](/nurbs/) surface. Sederberg, Zheng, Bakenov and Nasri introduced T-splines in 2003 to remove the superfluous control points of NURBS: a row of control points no longer has to run across the whole surface. This page treats the bicubic case on a single T-mesh, without extraordinary points.

## In plain words

A NURBS surface has its control points on a full grid. If a designer wants more detail in one corner, a whole row and a whole column of points must be added across the surface, and most of them do nothing useful.

A T-spline allows a row to stop where it is no longer needed. The grid then has places shaped like the letter T. Each control point still pulls on the surface with a smooth bump. The size and shape of the bump depend on the grid lines that are close to the point in the four directions, so a point near a short line gets a narrower bump than a point far from it.

Two NURBS surfaces can be joined into one T-spline without a gap, and the result can be refined in one place only.

## The abstract type

A T-spline surface stores a T-mesh, one control point $P_A \in \mathbb R^3$ and one weight $w_A > 0$ for each anchor $A$. The operations are:

- ANCHORS: list the control points of the T-mesh.
- LOCAL-KNOTS$(A)$: the local knot vectors $s_A = (s_{A,0}, \ldots, s_{A,4})$ and $t_A = (t_{A,0}, \ldots, t_{A,4})$ of anchor $A$.
- BLEND$(A, s, t)$: the blending function $T_A(s, t) = N[s_A](s)\, N[t_A](t)$, where $N[\cdot]$ is the cubic B-spline on five knots, computed by the [Cox-de Boor recursion](/cox-de-boor-recursion/).
- EVALUATE$(s, t)$: the point of the surface

$$S(s, t) = \frac{\sum_A w_A P_A\, T_A(s, t)}{\sum_A w_A\, T_A(s, t)}.$$

- TO-NURBS: the matrix $M$ that writes each $T_A$ in the tensor B-splines of the global knot vectors, so that the T-spline is a NURBS surface with control points $M$ times the homogeneous T-spline points.

## Representation

The T-mesh lives in *index space*. The vertical lines have the indices $0, \ldots, m$ and carry the knot values $sv_0 \le \cdots \le sv_m$; the horizontal lines have the indices $0, \ldots, n$ and carry $tv_0 \le \cdots \le tv_n$. A repeated value is a zero knot interval: an open knot vector at the boundary is four lines with the same value. The mesh is a set of unit edges: $(i, j)$ in the horizontal set means the edge from $(i, j)$ to $(i + 1, j)$, and in the vertical set the edge from $(i, j)$ to $(i, j + 1)$. A line can be present on some unit edges and absent on others, and that is how a T-junction appears.

A *vertex* is a point that lies on a horizontal edge and on a vertical edge. For a bicubic T-spline the anchors are the vertices $(i, j)$ with $2 \le i \le m - 2$ and $2 \le j \le n - 2$. The four outer lines on each side are complete, so every ray of the knot rule finds two lines. Working in index space avoids two problems with knot values alone: zero knot intervals do not collapse the mesh, and the topology is kept apart from the values.

## Operations

```pseudo id=main
LOCAL-KNOTS(mesh, A = (i, j))                    ▷ bicubic, in index space
L1  s₂ ← i
L2  walk right along row j from i; s₃, s₄ ← the first two columns k such that (k, j) lies on a vertical edge
L3  walk left along row j from i; s₁, s₀ ← the first two such columns
L4  walk up and down column i, with horizontal edges, to get t₀, t₁, t₂ = j, t₃, t₄
L5  return the values sv[s₀], …, sv[s₄] and tv[t₀], …, tv[t₄]
```

This is the knot rule of Sederberg and coauthors: cast a ray from the anchor in each of the four directions and record the first two lines that it crosses. A ray at row $j$ meets column $k$ only if the vertical line $k$ is present at the height $j$; a line that stops below the ray is skipped.

```pseudo id=evaluate
EVALUATE(mesh, P, w, s, t)
L6  num ← 0; den ← 0
L7  for each anchor A of the mesh do
L8      T_A ← N[s_A](s) · N[t_A](t)          ▷ cubic B-splines on the local knots
L9      num ← num + w_A P_A T_A; den ← den + w_A T_A
L10 return num / den
```

```pseudo id=extract
TO-NURBS(mesh)
L11 for each anchor A (a column of M) do
L12     insert into s_A, one line at a time, every column between s_{A,0} and s_{A,4} that s_A lacks, and the same for t_A   ▷ Boehm
L13     M[(a, b), A] ← d_a e_b, where N[s_A] = Σ_a d_a B_a and N[t_A] = Σ_b e_b B_b
L14 return M
```

Line L12 uses [Boehm's rule](/boehm-knot-insertion/) for one B-spline: inserting a knot $u$ into $N[t_0, \ldots, t_4]$ gives

$$N[t_0, \ldots, t_4] = c_0\, N[\tau_0, \ldots, \tau_4] + c_1\, N[\tau_1, \ldots, \tau_5], \quad c_0 = \min\Big(1, \frac{u - t_0}{t_3 - t_0}\Big), \quad c_1 = \min\Big(1, \frac{t_4 - u}{t_4 - t_1}\Big),$$

where $\tau$ is the sorted list of the six knots. After all insertions every piece has five consecutive global lines, so it is a global B-spline $B_a$. The matrix $M$ is the T-spline-to-NURBS matrix of Li, Zheng, Sederberg, Hughes and Scott.

## Example

Take $sv = (0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4)$ and $tv = (0, 0, 0, 0, 1, 2, 3, 3, 3, 3)$, so the lines have the indices $0..10$ and $0..9$. The full grid on these lines has $7 \times 6 = 42$ anchors, the control points of a bicubic NURBS surface. Now remove the vertical line $s = 2$ (index 5) inside the surface, except for the edge from $t = 1$ to $t = 2$ (rows 4 to 5). The anchors $(5, 3)$ and $(5, 6)$, at $(s, t) = (2, 0)$ and $(2, 3)$, are no longer vertices, so 40 anchors remain. The short line ends in two T-junctions, at $(2, 1)$ and $(2, 2)$.

| anchor (index) | at $(s, t)$ | $s_A$ | $t_A$ | the same as the tensor product? |
|---|---|---|---|---|
| $(4, 4)$ | $(1, 1)$ | $0, 0, 1, 2, 3$ | $0, 0, 1, 2, 3$ | yes, the ray at $t = 1$ meets $s = 2$ |
| $(4, 3)$ | $(1, 0)$ | $0, 0, 1, 3, 4$ | $0, 0, 0, 1, 2$ | no, the ray at $t = 0$ skips $s = 2$ |
| $(6, 6)$ | $(3, 3)$ | $0, 1, 3, 4, 4$ | $1, 2, 3, 3, 3$ | no, the ray at $t = 3$ skips $s = 2$ |
| $(5, 4)$ | $(2, 1)$ | $0, 1, 2, 3, 4$ | $0, 0, 1, 2, 3$ | yes |

For the anchor $(4, 3)$ line L12 inserts $u = 2$ into $s_A = (0, 0, 1, 3, 4)$. Then $c_0 = (2 - 0)/(3 - 0) = \tfrac23$ and $c_1 = (4 - 2)/(4 - 0) = \tfrac12$, so

$$N[0, 0, 1, 3, 4] = \tfrac23\, N[0, 0, 1, 2, 3] + \tfrac12\, N[0, 1, 2, 3, 4],$$

and its column of $M$ has the two entries $\tfrac23$ and $\tfrac12$ in the rows of the tensor B-splines with $s$ indices 2 and 3 and $t$ index 1. $M$ is $42 \times 40$ with rank 40, so the 40 blending functions are linearly independent. At every point that the tests try, including $(2, \tfrac32)$ on the short line, the blending functions are nonnegative, they sum to 1, and with the coefficients $\tfrac13(s_{A,1} + s_{A,2} + s_{A,3})$ they reproduce the function $s$.

## Correctness

Three facts make the data structure correct. First, on a full grid every point of every line lies on an edge, so each ray of lines L2 to L4 meets the next two lines, and the local knot vectors are the windows $sv_{i-2}, \ldots, sv_{i+2}$ of the global knot vectors: the T-spline is the tensor product NURBS surface. Second, Boehm's rule is an identity between functions, so each $T_A$ equals the sum in column $A$ of $M$, and the T-spline surface is the NURBS surface on the global knot vectors with the homogeneous control points $M\,(w_A P_A, w_A)$. Third, each $T_A$ is nonnegative, is zero outside the box $[s_{A,0}, s_{A,4}] \times [t_{A,0}, t_{A,4}]$, and is $C^2$ across a simple knot, because it is a product of two cubic B-splines. Partition of unity and linear independence are not part of the definition: they hold for [analysis-suitable T-splines](/analysis-suitable-t-spline/) and can fail for others. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | extra space |
|---|---|---|
| LOCAL-KNOTS | $O(m + n)$ for the walks | $O(1)$ |
| BLEND | $O(1)$ for two cubic B-splines | $O(1)$ |
| EVALUATE, as written | $O(a)$ blends, after the local knots are stored | $O(a)$ |
| TO-NURBS | $O(a\, m n)$ in the worst case, since a column can have $O(m n)$ nonzero entries | $O(a\, m n)$ for a dense $M$ |

Here $a$ is the number of anchors, and $m$ and $n$ are the numbers of index lines. Inferring all the local knot vectors takes $O(a (m + n))$ time.

A surface code stores the local knot vectors once and finds the anchors whose box contains $(s, t)$ with a spatial index, so that EVALUATE touches only the nonzero blending functions. The walks of lines L2 to L4 take $O(\log)$ time per step with a sorted list of the lines present at each row, but the simple walk is enough for small meshes.

## Variants

- **Even degree.** For degree 2 the anchors are the centres of the faces, not the vertices, and the rays start from the face centre. Bazilevs and coauthors (2010) give both cases in index space.
- **Arbitrary degree.** For degree $p$ odd the local knot vectors have $p + 2$ entries, $\frac{p+1}{2}$ on each side of the anchor.
- **T-NURCCs.** Sederberg and coauthors (2003) allow extraordinary points and use Catmull-Clark rules near them, for surfaces of any topology.
- **Analysis-suitable T-splines.** The T-meshes whose T-junction extensions do not cross; see [analysis-suitable T-spline](/analysis-suitable-t-spline/), [linear independence](/t-spline-linear-independence/) and [local refinement](/t-spline-local-refinement/).
- **Related local spline spaces.** [Hierarchical B-splines](/hierarchical-b-spline/), [LR B-splines](/lr-b-spline/) and [PHT-splines](/pht-spline/) also refine locally, with different rules.

## When to use it

Use T-splines to model a surface that needs detail in some places only, to join NURBS patches without gaps, and to remove superfluous control points from a NURBS model. For analysis, keep the T-mesh analysis-suitable, so that the blending functions are a basis and refinement stays local. For an element-wise implementation, extract the blending functions to Bernstein form on each element, as in [Bezier extraction](/bezier-extraction/).

## Pitfalls

- **Knot values instead of index space.** With zero knot intervals two lines have the same value. A ray that compares values instead of indices stops at the wrong line.
- **Rays that run out.** If the outer lines are not complete, a ray near the boundary finds fewer than two lines. The code raises an error instead of guessing a knot.
- **Assuming a basis.** For a general T-mesh the blending functions can be linearly dependent. Buffa, Cho and Sangalli give a T-mesh whose 40 blending functions have rank 39; see [linear independence](/t-spline-linear-independence/).
- **Assuming partition of unity.** The weights in the denominator hide this in modelling, but a finite element code that relies on $\sum_A T_A = 1$ needs an analysis-suitable T-mesh with suitable boundary lines.
- **Moving a T-junction without its knot.** In index space a T-junction belongs to one index line. Changing the value of that line changes every blending function whose ray meets it.

## Implementations

The Python module stores the T-mesh as two sets of unit edges in index space, with the knot values of the lines. It implements the anchors, LOCAL-KNOTS by ray casting, BLEND with an exact Cox-de Boor recursion on five knots, EVALUATE of the rational surface, TO-NURBS by Boehm insertion one knot at a time, and an exact rank. The tests check that on a full grid every blending function is the tensor B-spline of a separate global Cox-de Boor evaluation and that the surface is the NURBS surface, that the local knot vectors of the example match the table, that each blending function equals its expansion in column $A$ of $M$ at random rational points, that the example has partition of unity, nonnegativity and linear precision, and that each blending function vanishes outside its local box.

## History

Sederberg, Zheng, Bakenov and Nasri introduced T-splines and T-NURCCs at SIGGRAPH 2003. In 2004 Sederberg, Cardon, Finnigan, North, Zheng and Lyche gave local refinement and the simplification of NURBS models into T-splines. Bazilevs, Calo, Cottrell, Evans, Hughes, Lipton, Scott and Sederberg used T-splines for [isogeometric analysis](/isogeometric-analysis/) in 2010. In the same year Buffa, Cho and Sangalli found a T-mesh with linearly dependent blending functions, and Li, Zheng, Sederberg, Hughes and Scott answered with analysis-suitable T-splines, published in 2012.

## References
