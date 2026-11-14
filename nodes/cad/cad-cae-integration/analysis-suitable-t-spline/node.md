---
tag: HTWJEQ
kind: definition
slug: analysis-suitable-t-spline
name: Analysis-suitable T-spline
aliases:
- AS T-spline
area: cad/cad-cae-integration
level: research
summary: A T-spline whose T-junction extensions do not cross, which gives linearly independent, partition-of-unity blending functions fit for analysis.
prereqs: [t-spline, b-spline, partition-of-unity]
see_also: [t-spline-linear-independence, t-spline-local-refinement, isogeometric-analysis, bezier-extraction, hierarchical-b-spline, truncated-hierarchical-b-spline, lr-b-spline, pht-spline]
sources:
  - paper: doi:10.1016/j.cagd.2011.08.005
    title: Xin Li, Jianmin Zheng, Thomas W. Sederberg, Thomas J. R. Hughes and Michael A. Scott, On linear independence of T-spline blending functions, Computer Aided Geometric Design 29(1) (2012), 63 to 76
    locator: Definition 7 (analysis-suitable T-meshes, with closed extensions), Figures 7 and 8 (extensions that cross and that touch), Lemma 8 and Corollary 9 (no L-junctions, I-junctions or isolated nodes), Theorem 18 (linear independence)
  - paper: doi:10.1016/j.cma.2011.11.022
    title: Michael A. Scott, Xin Li, Thomas W. Sederberg and Thomas J. R. Hughes, Local refinement of analysis-suitable T-splines, Computer Methods in Applied Mechanics and Engineering 213-216 (2012), 206 to 222
    locator: Section 3.1 (face and edge extensions), Section 3.3 (the definition by the extended T-mesh), Section 3.4 (partition of unity, cited there to work in preparation), Section 3.5 (the elemental T-mesh)
  - paper: doi:10.1016/j.cma.2012.02.025
    title: L. Beirão da Veiga, A. Buffa, D. Cho and G. Sangalli, Analysis-suitable T-splines are dual-compatible, Computer Methods in Applied Mechanics and Engineering 249-252 (2012), 42 to 51
    locator: the proof that analysis-suitable T-meshes are dual-compatible, so that each blending function has a dual functional (general locator)
  - paper: doi:10.1142/S0218202513500231
    title: L. Beirão da Veiga, A. Buffa, G. Sangalli and R. Vázquez, Analysis-suitable T-splines of arbitrary degree, definition, linear independence and approximation properties, Mathematical Models and Methods in Applied Sciences 23(11) (2013), 1979 to 2003
    locator: the definition for any degree and the approximation estimates (general locator)
  - paper: doi:10.1142/S0218202513500796
    title: Xin Li and Michael A. Scott, Analysis-suitable T-splines, characterization, refineability, and approximation, Mathematical Models and Methods in Applied Sciences 24(6) (2014), 1141 to 1164
    locator: the characterization of the analysis-suitable T-spline space, nested refinement, and approximation (general locator)
  - paper: doi:10.1007/s40304-015-0064-z
    title: Jingjing Zhang and Xin Li, On the linear independence and partition of unity of arbitrary degree analysis-suitable T-splines, Communications in Mathematics and Statistics 3(3) (2015), 353 to 364
    locator: the proof of partition of unity for analysis-suitable T-splines of any degree (general locator)
---

An analysis-suitable T-spline is a [T-spline](/t-spline/) whose T-mesh has no horizontal T-junction extension that meets a vertical one. Li, Zheng, Sederberg, Hughes and Scott defined the class in 2012, after Buffa, Cho and Sangalli had shown that the blending functions of a general T-spline can be linearly dependent. The condition is a simple test on the T-mesh, it gives a basis that is linearly independent and sums to 1, and it allows local refinement with nested spaces. So the class is the one used for T-spline [isogeometric analysis](/isogeometric-analysis/).

## Definition

Use the T-mesh of a bicubic [T-spline](/t-spline/) in index space. A *T-junction* is a vertex that has three of its four edges; the missing edge points in a direction $d$. The *T-junction extension* of a T-junction $J$ is the closed segment that is the union of two parts:

- the *face extension*, from $J$ in direction $d$ across two faces, to the second line perpendicular to $d$ that it meets;
- the *edge extension*, from $J$ in the opposite direction to the first perpendicular line or T-node that it meets.

An extension is *horizontal* or *vertical* by its direction. A T-mesh is *analysis-suitable* if no horizontal T-junction extension intersects a vertical T-junction extension. A T-spline is analysis-suitable if its T-mesh is.

Three points of the definition matter in practice.

1. The extensions are closed segments. Two extensions that only touch, at an end point of one or both, intersect, and the mesh is not analysis-suitable.
2. The lengths come from the degree. For degree $p$ odd the face extension crosses $\frac{p+1}{2}$ faces and the edge extension $\frac{p-1}{2}$; for bicubic splines that is two and one. Beirão da Veiga, Buffa, Sangalli and Vázquez give the definition for every degree.
3. The rule counts index lines, not knot values, so a line with a repeated knot value is still a line.

## Examples and non-examples

The index meshes below are the ones of the [T-spline](/t-spline/) and [local refinement](/t-spline-local-refinement/) pages, and their tests check each claim.

- **Every tensor mesh.** A full grid has no T-junctions, so it has no extensions, and it is analysis-suitable. Its T-spline is a bicubic NURBS surface.
- **Only vertical T-junctions.** In the example of the T-spline page, a vertical line stops after one edge, which gives two T-junctions, both missing a vertical edge. All extensions are vertical, so none can meet a horizontal one: the mesh is analysis-suitable. Its 40 blending functions have a $42 \times 40$ matrix $M$ of rank 40 and sum to 1.
- **One face split into four.** In the tensor mesh on the knots $0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4$, split the face $[1, 2] \times [1, 2]$ by a cross at $s = \tfrac32$ and $t = \tfrac32$. This gives four T-junctions, and their extensions all reach the centre of the cross. A horizontal and a vertical extension touch there, so the mesh is **not** analysis-suitable. Extending the horizontal line of the cross by one face to the left and one to the right makes it analysis-suitable, with 56 control points.
- **L-junctions.** A vertex with only two edges, at a right angle, has a horizontal and a vertical extension that both contain the vertex. So an analysis-suitable T-mesh has no L-junction, no I-junction and no isolated node (Lemma 8 and Corollary 9 of Li and coauthors). A vertex with two collinear edges and a third edge is a T-junction, which is allowed.
- **The Buffa-Cho-Sangalli mesh.** The T-mesh of Buffa, Cho and Sangalli, whose blending functions are linearly dependent, has crossing extensions, so it is **not** analysis-suitable. See [linear independence](/t-spline-linear-independence/).
- **Analysis-suitable but not a refinement.** Take the split face above after its two extra edges, and add the whole horizontal line $t = \tfrac12$. The result is analysis-suitable, but the old blending function at $(s, t) = (\tfrac32, 1)$ is not a combination of the new ones. The reason is that a face extension of the new mesh ends inside a face extension of the old mesh. Analysis-suitable T-meshes are nested only under the stronger condition of Scott and coauthors, which [local refinement](/t-spline-local-refinement/) keeps.

## Related definitions

- **Extended T-mesh.** Scott, Li, Sederberg and Hughes add all T-junction extensions to the T-mesh as segments. The mesh is analysis-suitable when the extended T-mesh has no crossing of a horizontal and a vertical extension. Adding only the face extensions gives the *elemental T-mesh*, whose faces are the elements of analysis, on which every blending function is one polynomial.
- **Linear independence.** Li and coauthors prove that the blending functions of an analysis-suitable T-spline are linearly independent (Theorem 18). The proof shows that the mesh has no subgraph that makes the T-spline-to-NURBS matrix lose rank; see [linear independence](/t-spline-linear-independence/).
- **Partition of unity.** For an analysis-suitable T-mesh with a minor condition on the boundary lines, the blending functions satisfy $\sum_A N_A = 1$, so they have the [partition of unity](/partition-of-unity/) property without the rational weights. Scott and coauthors state this in Section 3.4 and cite work then in preparation; Zhang and Li prove it for every degree in 2015. The idea of the proof is duality: the T-spline space contains the constants, and each $N_A$ has a dual functional $\lambda_A$, the tensor product of the univariate dual functionals of its local knot vectors, with $\lambda_A(N_B) = \delta_{AB}$ and $\lambda_A(1) = 1$. Applying $\lambda_A$ to $1 = \sum_B c_B N_B$ gives $c_A = 1$. This page does not prove the two facts that the argument uses, and cites them. The tests of the T-spline and local refinement pages check $\sum_A N_A = 1$ exactly at sample points of their meshes.
- **Dual-compatible T-splines.** A T-mesh is dual-compatible when any two blending functions that overlap have local knot vectors that overlap in the sense of univariate B-splines in at least one direction. Beirão da Veiga, Buffa, Cho and Sangalli prove that analysis-suitable T-meshes are dual-compatible, which gives the dual functionals above, and so linear independence and local approximation estimates.
- **Analysis-suitable refinement.** A refinement of an analysis-suitable T-mesh that stays analysis-suitable and keeps the spaces nested is given by [local refinement](/t-spline-local-refinement/). Li and Scott (2014) prove the nesting.
- **Other local spline spaces.** [Hierarchical B-splines](/hierarchical-b-spline/), [truncated hierarchical B-splines](/truncated-hierarchical-b-spline/), [LR B-splines](/lr-b-spline/) and [PHT-splines](/pht-spline/) get linear independence or partition of unity by other rules on the mesh.

## References
