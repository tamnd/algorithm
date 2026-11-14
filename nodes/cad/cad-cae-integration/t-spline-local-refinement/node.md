---
tag: WVHYV3
kind: algorithm
slug: t-spline-local-refinement
name: Local refinement of analysis-suitable T-splines
aliases:
- Scott T-spline refinement
area: cad/cad-cae-integration
level: research
summary: Scott and coauthors' refinement that inserts the requested control points and any extra ones needed so the T-mesh stays analysis-suitable and refinement stays local.
model: real-ram
complexity:
  vars: {k: the number of insertion edges that the loop adds, c: the number of candidate edges in one round, m: the number of vertical index lines, n: the number of horizontal index lines, x: the number of T-junction extensions, a: the number of anchors}
  time: {worst: O(k c (m n (m + n) + x^2) + a^2)}
  space: {extra: O(m n + a^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 2012
  people: [Michael A. Scott, Xin Li, Thomas W. Sederberg, Thomas J. R. Hughes]
  note: Scott, Li, Sederberg and Hughes published the algorithm in Computer Methods in Applied Mechanics and Engineering in 2012, after the ICES report 11-06 of 2011. It replaces the local refinement of Sederberg and coauthors (2004), which can add superfluous control points and can leave the class of analysis-suitable T-splines.
prereqs: [t-spline, analysis-suitable-t-spline, boehm-knot-insertion, oslo-algorithm]
see_also: [t-spline-linear-independence, knot-refinement, isogeometric-analysis, bezier-extraction, hierarchical-b-spline, truncated-hierarchical-b-spline, lr-b-spline, pht-spline]
sources:
  - paper: doi:10.1016/j.cma.2011.11.022
    title: Michael A. Scott, Xin Li, Thomas W. Sederberg and Thomas J. R. Hughes, Local refinement of analysis-suitable T-splines, Computer Methods in Applied Mechanics and Engineering 213-216 (2012), 206 to 222
    locator: Section 3.1 (face and edge extensions), Section 3.3 (analysis-suitable T-meshes by the extended T-mesh), Section 4.1 (nested T-spline spaces and the coupled extension graph), Section 4.2 (the refinement algorithm, steps 1 to 5, and the greedy choice of insertion edges), Section 4.3 (the refinement matrix computed one pair of functions at a time)
  - paper: doi:10.1142/S0218202513500796
    title: Xin Li and Michael A. Scott, Analysis-suitable T-splines, characterization, refineability, and approximation, Mathematical Models and Methods in Applied Sciences 24(6) (2014), 1141 to 1164
    locator: the proof that analysis-suitable T-spline spaces are nested when the extended T-meshes are nested (general locator)
  - paper: doi:10.1016/j.cagd.2011.08.005
    title: Xin Li, Jianmin Zheng, Thomas W. Sederberg, Thomas J. R. Hughes and Michael A. Scott, On linear independence of T-spline blending functions, Computer Aided Geometric Design 29(1) (2012), 63 to 76
    locator: Definition 7 (analysis-suitable T-meshes) and Theorem 18 (their blending functions are linearly independent)
  - paper: doi:10.1145/1015706.1015715
    title: Thomas W. Sederberg, David L. Cardon, G. Thomas Finnigan, Nicholas S. North, Jianmin Zheng and Tom Lyche, T-spline simplification and local refinement, ACM Transactions on Graphics 23(3) (SIGGRAPH 2004), 276 to 283
    locator: the earlier local refinement by blending function refinement (general locator)
---

Local refinement of analysis-suitable T-splines takes a [T-spline](/t-spline/) on an [analysis-suitable](/analysis-suitable-t-spline/) T-mesh $T_1$ and a set of edges that the user wants to add. It adds those edges, then adds a few more edges, one at a time, until the new T-mesh $T_2$ is analysis-suitable again and its T-junction extensions do not run into the extensions of $T_1$ in a way that breaks nesting. Then every old blending function is a combination of new ones, and the algorithm computes that combination, the refinement matrix $M$. The new control points are $M^\top$ times the old homogeneous control points, so the surface does not change. Scott, Li, Sederberg and Hughes gave the algorithm in 2012. This page treats the bicubic case in index space, with the representation of the [T-spline](/t-spline/) page.

## In plain words

A T-spline lets a row of control points stop in the middle of the surface. To get more detail in one place, you draw a few new short lines there. For analysis, this is not always safe. The short lines can make the smooth bumps of the control points depend on each other, and the old bumps may no longer be sums of the new ones.

The algorithm draws your lines first. Then it looks for places where the ends of short lines come too close to each other. At each such place it can make one short line a little longer. It tries every such step and keeps the one that removes the most problems. It repeats until no problem is left.

At the end, each old bump is an exact sum of new bumps, so the shape does not change.

## The problem

The input is an analysis-suitable bicubic T-mesh $T_1$ in index space, with the four outer lines on each side complete, and a request $R$: a list of horizontal and vertical segments on index lines. The output is a T-mesh $T_2 \supseteq T_1 \cup R$ and a matrix $M$ such that

1. $T_2$ is analysis-suitable,
2. every blending function $N_A$ of $T_1$ satisfies $N_A = \sum_B M_{AB} N_B$ over the blending functions $N_B$ of $T_2$,
3. $T_2$ adds as few edges beyond $R$ as the greedy rule finds.

With homogeneous control points $Q_A = (w_A P_A, w_A)$, condition 2 gives $\sum_A Q_A N_A = \sum_B \big(\sum_A M_{AB} Q_A\big) N_B$, so the rational surface is the same.

Analysis-suitable alone is not enough for condition 2. A T-mesh $T_2 \supseteq T_1$ can be analysis-suitable while some old function is not in the new space; the tests give one. Scott and coauthors use a stronger condition, which they write $T_1^{ext} \subseteq^{\wedge} T_2^{ext}$: $T_1 \subseteq T_2$, and no face extension of $T_2$ ends strictly inside a face extension of $T_1$ that goes in the same direction. Li and Scott (2014) prove that two analysis-suitable T-meshes with this property give nested spline spaces.

## The algorithm

The *T-junction extension* of a T-junction $J$ that is missing the edge in direction $d$ has two parts: the *face extension* goes from $J$ in direction $d$ to the second perpendicular line that it meets, and the *edge extension* goes from $J$ the other way to the first perpendicular line. A T-mesh is analysis-suitable when no horizontal extension meets a vertical one, the segments being closed.

The *coupled extension graph* $E(T_1 \to T_2)$ has one edge for each pair of a horizontal and a vertical extension of $T_2$ that meet, and one *loop edge* for each face extension of $T_2$ that ends strictly inside a same-direction face extension of $T_1$. Its weight $W$ is the number of edges. $W = 0$ means that $T_2$ is analysis-suitable and that $T_1^{ext} \subseteq^{\wedge} T_2^{ext}$.

```pseudo id=main
REFINE(T₁, R)
L1  T₂ ← T₁ ∪ R
L2  W ← the weight of the coupled extension graph E(T₁ → T₂)
L3  while W > 0 do
L4      for each insertion edge e: from a T-junction J of T₂ whose extension is in an edge of E, along J's missing direction, to the next perpendicular line
L5          keep the e for which the weight of E(T₁ → T₂ ∪ {e}) is smallest (the first one on a tie)
L6      T₂ ← T₂ ∪ {e}; W ← that weight
```

```pseudo id=operator
REFINEMENT-MATRIX(T₁, T₂, Q)
L7  for each old function N_A, and each new N_B whose index box lies in that of N_A do
L8      insert into s_A the index lines of s_B that s_A lacks, and the same for t_A   ▷ Boehm, one B-spline
L9      c ← (coefficient of N[s_B] in N[s_A]) · (coefficient of N[t_B] in N[t_A]), or 0 if a factor is not a piece
L10     M_AB ← c
L11 return the new control points Q_B ← Σ_A M_AB Q_A
```

Finding the set of insertion edges that makes $W$ zero with the fewest edges is NP-hard, as Scott and coauthors note, so line L5 is greedy. Lines L7 to L10 use the fact that the coefficient of a fine B-spline in a coarse one depends only on the coarse knots and on the knots of the fine B-spline: it is a discrete B-spline of the [Oslo algorithm](/oslo-algorithm/). So each pair $(A, B)$ can be treated alone, by [Boehm's rule](/boehm-knot-insertion/) on two short knot vectors.

## Example

Take the index lines $0..14$ in both directions with the values $0, 0, 0, 0, \tfrac12, 1, \tfrac32, \ldots, \tfrac72, 4, 4, 4, 4$, and let $T_1$ be the tensor mesh on the lines with integer values, the lines $0, 1, 2, 3, 5, 7, 9, 11, 12, 13, 14$. It is a bicubic B-spline surface with $7 \times 7 = 49$ control points. The request splits the face $[1, 2] \times [1, 2]$ into four: the vertical segment on column 6 ($s = \tfrac32$) from row 5 to row 7, and the horizontal segment on row 6 ($t = \tfrac32$) from column 5 to column 7.

After line L1 the mesh has four new T-junctions, at index $(6, 5)$, $(6, 7)$, $(5, 6)$ and $(7, 6)$. The vertical extension of $(6, 5)$ runs on column 6 from row 2 to row 6, and the horizontal extension of $(5, 6)$ runs on row 6 from column 2 to column 6. They meet at the centre $(6, 6)$, so $T_1 \cup R$ is not analysis-suitable and $W > 0$. The loop adds two insertion edges, from $(5, 6)$ left to column 3 and from $(7, 6)$ right to column 9: row 6 now runs from $s = 0$ to $s = 3$. The vertical extensions stay on column 6, and the two horizontal ones now run on row 6 from column 1 to column 5 and from column 7 to column 12, so they do not meet, $W = 0$, and $T_2$ has $56$ anchors.

For the old anchor at $(s, t) = (1, 1)$ the local knot vectors are $(0, 0, 1, 2, 3)$ in both directions. Inserting $\tfrac32$ gives $c_0 = \tfrac{3/2}{2} = \tfrac34$ and $c_1 = \tfrac{3 - 3/2}{3} = \tfrac12$, so

$$N[0, 0, 1, 2, 3] = \tfrac34\, N[0, 0, 1, \tfrac32, 2] + \tfrac12\, N[0, 1, \tfrac32, 2, 3],$$

and the row of $M$ has the four products $\tfrac{9}{16}$, $\tfrac38$, $\tfrac38$ and $\tfrac14$ on the new anchors at $(1, 1)$, $(\tfrac32, 1)$, $(1, \tfrac32)$ and $(\tfrac32, \tfrac32)$. Sixteen of the 49 rows change; the other 33 old functions are new functions too.

## Correctness

The loop stops, because each round adds a unit edge that $T_2$ did not have, the edges of the index grid are finite, and while $W > 0$ there is always a candidate: an extension in an edge of $E$ has a face part, so its junction has a next perpendicular line. At the end $W = 0$, so $T_2$ has no crossing extensions, which is the definition of analysis-suitable, and no loop edges, which is $T_1^{ext} \subseteq^{\wedge} T_2^{ext}$. Then the spaces are nested by the theorem of Li and Scott (2014), and the new functions are linearly independent by Theorem 18 of Li, Zheng, Sederberg, Hughes and Scott, so the coefficients of each $N_A$ are unique. Scott and coauthors (Section 4.3) show that lines L7 to L10 compute them. Given condition 2, the new control points give the same surface. The [proof](proofs/correctness.md) has the details and marks the cited steps. The tests check condition 2 exactly, as an identity between the expansions of both sides in the tensor B-splines on all index lines.

## Complexity

Let $k$ be the number of rounds, $c$ the number of candidates in a round, $x$ the number of extensions and $a$ the number of anchors. One weight takes $O(m n (m + n))$ time to find the extensions by walks on the index grid and $O(x^2)$ to test pairs, so the loop takes $O(k c (m n (m + n) + x^2))$. Lines L7 to L10 test $O(a^2)$ pairs, and each pair inserts at most eight knots into two knot vectors of length 5, which is $O(1)$. The extra space is $O(m n)$ for the edge sets and $O(a^2)$ for a dense $M$; $M$ has $O(a)$ nonzero entries in practice, because a new function lies in the box of only a few old ones.

These bounds are for the simple implementation. A production code keeps the extensions in a spatial index and updates the weight after each edge instead of starting again, so one round costs time proportional to the size of the change.

## Properties

- **Local.** An insertion edge starts at a T-junction whose extension is in conflict, so new edges appear only near the request and near the edges added before them.
- **Not unique.** The result depends on the order of the candidates when two of them give the same weight, and the greedy choice need not be the smallest set of edges.
- **Convex rows.** Each entry of $M$ is a product of Boehm coefficients, so it is nonnegative. Each new control point is a nonnegative combination of old homogeneous points.
- **A request is never undone.** The algorithm only adds edges, so the requested segments are in $T_2$.

## Variants and improvements

- **Sederberg and coauthors (2004).** The first local refinement of T-splines inserts control points and then fixes the blending functions one at a time. It can add superfluous control points and can produce a T-mesh that is not analysis-suitable.
- **Arbitrary degree.** Beirão da Veiga, Buffa, Sangalli and Vázquez (2013) define analysis-suitable T-splines of any degree and show that they are dual-compatible. The extensions are longer for higher degree, and the same test of crossing extensions applies.
- **Other local spline spaces.** [Hierarchical B-splines](/hierarchical-b-spline/), [truncated hierarchical B-splines](/truncated-hierarchical-b-spline/), [LR B-splines](/lr-b-spline/) and [PHT-splines](/pht-spline/) refine locally with simpler rules, at the cost of other properties.

## When to use it

Use this algorithm in adaptive [isogeometric analysis](/isogeometric-analysis/) with T-splines: an error estimator marks elements, each marked face is split into four, and the algorithm makes the result analysis-suitable and nested, so the old solution is in the new space. For modelling alone, where only the shape matters, the 2004 refinement is enough.

## Pitfalls

- **Analysis-suitable is not nested.** A T-mesh $T_2 \supseteq T_1$ can be analysis-suitable while an old function is not a combination of the new ones. The loop edges of the coupled graph catch this case.
- **Closed segments.** Two extensions that touch at one point count as meeting. With open segments the example above would look analysis-suitable, and it is not.
- **Superfluous edges.** The greedy rule can add more edges than the minimum, because the exact minimum is NP-hard to find.
- **The pair formula needs nesting.** Lines L7 to L10 give the right $M$ only when $N_A$ is in the new space. Called on a pair of meshes that is not nested, they return numbers whose sum is not $N_A$.
- **Knot values instead of indices.** As for every T-spline code, repeated knot values need index space, or the extensions end at the wrong lines.

## Implementations

The Python module stores the T-mesh in index space as two sets of unit edges, finds the face and edge extensions of every T-junction by walks on the grid, and implements the analysis-suitable test with closed segments, the weight of the coupled extension graph, the greedy loop of lines L1 to L6, the pair-by-pair matrix of lines L7 to L10 with exact Boehm insertion, and the new control points of line L11. The tests check the face cross example and its two insertion edges, that an L-junction is not analysis-suitable, that an analysis-suitable T-mesh can fail to be nested and that the algorithm repairs it, that four random face splits stay analysis-suitable with every old function equal to its row of $M$, compared exactly with the expansion of both sides in the tensor B-splines on all index lines, and that the rational surface and the partition of unity do not change at sample points.

## History

Sederberg, Cardon, Finnigan, North, Zheng and Lyche gave the first local refinement of T-splines in 2004. Buffa, Cho and Sangalli showed in 2010 that T-spline blending functions can be linearly dependent, and Li, Zheng, Sederberg, Hughes and Scott answered with analysis-suitable T-splines. Scott, Li, Sederberg and Hughes then gave this refinement, which keeps the class of analysis-suitable T-splines and the nesting of the spaces, in a 2011 ICES report and in Computer Methods in Applied Mechanics and Engineering in 2012. Li and Scott proved the nesting theorem and the approximation properties in 2014.

## References
