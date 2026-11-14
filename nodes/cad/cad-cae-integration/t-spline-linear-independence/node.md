---
tag: 8C8B3H
kind: theorem
slug: t-spline-linear-independence
name: Linear independence of analysis-suitable T-splines
aliases:
- analysis-suitable T-spline independence theorem
area: cad/cad-cae-integration
level: research
summary: Li, Zheng, Sederberg, Hughes and Scott proved the blending functions of analysis-suitable T-splines linearly independent, which general T-splines need not be.
prereqs: [t-spline, analysis-suitable-t-spline, b-spline, curry-schoenberg-theorem, tensor-product-surface]
see_also: [t-spline-local-refinement, isogeometric-analysis, bezier-extraction, partition-of-unity, hierarchical-b-spline, truncated-hierarchical-b-spline, lr-b-spline, pht-spline]
sources:
  - paper: doi:10.1016/j.cagd.2011.08.005
    title: Xin Li, Jianmin Zheng, Thomas W. Sederberg, Thomas J. R. Hughes and Michael A. Scott, On linear independence of T-spline blending functions, Computer Aided Geometric Design 29(1) (2012), 63 to 76
    locator: Section 4.1 (Theorem 1 and Figure 4, the 56 by 40 matrix of rank 39), Section 4.2 (column reduction, Lemma 2, Corollary 4, and the knot condition for the example), Section 5 (the directed graph, V2-subgraphs, Theorem 5), Section 6 (Definition 7, Lemmas 8 to 17, Theorem 18)
  - paper: doi:10.1016/j.cma.2009.12.004
    title: A. Buffa, D. Cho and G. Sangalli, Linear independence of the T-spline blending functions associated with some particular T-meshes, Computer Methods in Applied Mechanics and Engineering 199(23-24) (2010), 1437 to 1445
    locator: the T-mesh with linearly dependent blending functions, and the relation between the three functions (general locator)
  - paper: doi:10.1016/j.cma.2012.02.025
    title: L. Beirão da Veiga, A. Buffa, D. Cho and G. Sangalli, Analysis-suitable T-splines are dual-compatible, Computer Methods in Applied Mechanics and Engineering 249-252 (2012), 42 to 51
    locator: a second proof of linear independence, through dual functionals (general locator)
  - paper: doi:10.1142/S0218202513500231
    title: L. Beirão da Veiga, A. Buffa, G. Sangalli and R. Vázquez, Analysis-suitable T-splines of arbitrary degree, definition, linear independence and approximation properties, Mathematical Models and Methods in Applied Sciences 23(11) (2013), 1979 to 2003
    locator: linear independence for every degree (general locator)
  - paper: doi:10.1007/s40304-015-0064-z
    title: Jingjing Zhang and Xin Li, On the linear independence and partition of unity of arbitrary degree analysis-suitable T-splines, Communications in Mathematics and Statistics 3(3) (2015), 353 to 364
    locator: linear independence and partition of unity for every degree (general locator)
---

The blending functions of a [T-spline](/t-spline/) are products of B-splines on local knot vectors, one for each control point. On a general T-mesh they can be linearly dependent: Buffa, Cho and Sangalli found a T-mesh with 40 functions that span a space of dimension 39. Li, Zheng, Sederberg, Hughes and Scott proved two results in 2012. First, the functions are independent if and only if the T-spline-to-NURBS matrix $M$ has full column rank. Second, on an [analysis-suitable](/analysis-suitable-t-spline/) T-mesh they are always independent, for every choice of knot values. So analysis-suitable T-splines give a basis, as [isogeometric analysis](/isogeometric-analysis/) needs.

## Statement

Let a bicubic T-spline be given in index space, as on the [T-spline](/t-spline/) page: vertical lines $0, \ldots, m$ with knot values $sv_0 \le \cdots \le sv_m$, horizontal lines $0, \ldots, n$ with values $tv_0 \le \cdots \le tv_n$, the two outer lines on each side complete, and no value on more than four lines. Let $T_1, \ldots, T_\tau$ be the blending functions of the $\tau$ anchors. Let $B_a(s)$, $0 \le a \le m - 4$, and $B_b(t)$, $0 \le b \le n - 4$, be the cubic B-splines on the global knot vectors $sv$ and $tv$, and $\nu = (m - 3)(n - 3)$. Each $T_A$ is a combination

$$T_A(s, t) = \sum_{a, b} M_{(a, b), A}\, B_a(s)\, B_b(t),$$

and $M$ is the $\nu \times \tau$ *T-spline-to-NURBS matrix*.

**Theorem 1 (Li, Zheng, Sederberg, Hughes and Scott).** $M$ is unique, and $T_1, \ldots, T_\tau$ are linearly independent if and only if $M$ has rank $\tau$.

**Theorem 18 (Li, Zheng, Sederberg, Hughes and Scott).** If the T-mesh is analysis-suitable, then $T_1, \ldots, T_\tau$ are linearly independent, for every choice of the knot values.

With positive weights $w_A$, the rational functions $w_A T_A / \sum_B w_B T_B$ are independent exactly when the $T_A$ are, because they differ by a positive common factor and a positive scaling of each function.

## In plain words

Each control point of a T-spline has a smooth bump. A finite element method needs the bumps to be a basis: no bump may be a mix of the others, or the system of equations has no unique solution.

The first result says how to test this. Write every bump as a sum of the bumps of an ordinary grid, which are known to be a basis. Put the numbers in a table, one column per bump. The bumps are a basis exactly when no column is a mix of the other columns.

The second result says that one simple rule on the mesh is enough. If the short extensions of the T-shaped joints never meet, the bumps are always a basis, whatever the spacing of the lines.

## Proof

**Theorem 1.** Each $T_A$ is a product of a cubic B-spline on five of the lines $sv$ and one on five of the lines $tv$. Inserting into each factor the missing lines between its first and last line, by [Boehm's rule](/boehm-knot-insertion/), writes it as a combination of the global B-splines; this is the construction on the T-spline page, so $M$ exists. The global B-splines $B_a$ are linearly independent on $[sv_3, sv_{m-3}]$, by the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/), because no value has multiplicity above 4. The same holds for the $B_b$, and the products $B_a(s) B_b(t)$ of two independent families are independent: if $\sum_{a, b} c_{ab} B_a(s) B_b(t) = 0$, then for each fixed $t$ the coefficients $\sum_b c_{ab} B_b(t)$ of the $B_a$ vanish, and then each $c_{ab} = 0$. So the coefficients of each $T_A$ are unique, and $M$ is unique.

For a vector $\delta \in \mathbb R^\tau$,

$$\sum_A \delta_A T_A = \sum_{a, b} (M \delta)_{(a, b)}\, B_a B_b,$$

and by the independence of the products this is the zero function if and only if $M \delta = 0$. So a nonzero $\delta$ with $\sum_A \delta_A T_A = 0$ exists if and only if $M$ has a nonzero null vector, that is, if and only if $\operatorname{rank} M < \tau$. $\square$

**A lemma for the rank.** Call column $A$ of $M$ *innocuous* if some row $r$ has $M_{rA} \ne 0$ and $M_{rB} = 0$ for every other column $B$. Removing an innocuous column, and the rows that become zero, does not change the nullity. Indeed, if $M \delta = 0$, row $r$ gives $M_{rA}\, \delta_A = 0$, so $\delta_A = 0$. Hence the null vectors of $M$ are the null vectors of $M$ without column $A$, with a 0 added at position $A$, and zero rows do not affect a null space. So if repeated removal of innocuous columns ends with no column, $M$ has full column rank (Li and coauthors, Lemma 2 and Corollary 4).

**Theorem 18 (outline of the published proof).** Li and coauthors draw $M$ as a directed graph. Each column is a *T-node*, each row an *N-node*, and each nonzero entry an edge from the T-node to the N-node. The set of N-nodes that a T-node points to is its *footprint*; when the local knots are distinct, it is the rectangle of global B-splines whose middle knots lie inside the local knot vectors. Removing innocuous columns is *pruning*: a T-node that points to an N-node of valence 1 is removed. Pruning ends either with nothing or with a *V2-subgraph*, a set of T-nodes whose footprints cover each of their N-nodes at least twice. By the lemma above, a T-mesh without V2-subgraphs gives a matrix of full rank, for every choice of knots (Theorem 5), since the footprints depend only on the topology. The remaining step shows that an analysis-suitable T-mesh has no V2-subgraph. Suppose that it has one, and take its lowest, then leftmost, N-node $N$. Then two T-nodes of the subgraph cover $N$; they lie to the north-east of $N$ (Lemma 17), they have the same leftmost and lowest knot lines, and they do not lie on one horizontal or one vertical line. Lemmas 15 and 16, which use the absence of L-junctions, I-junctions and isolated nodes (Lemma 8) and the structure of the mesh between the two T-nodes (Lemmas 11 to 14), show that two of their T-junction extensions then intersect. This contradicts Definition 7. We cite these lemmas and do not repeat their case analysis. Beirão da Veiga, Buffa, Cho and Sangalli give a second proof: an analysis-suitable T-mesh is dual-compatible, so every $T_A$ has a dual functional $\lambda_A$ with $\lambda_A(T_B) = \delta_{AB}$, and applying $\lambda_A$ to $\sum_B \delta_B T_B = 0$ gives $\delta_A = 0$. $\blacksquare$

## Consequences

- **A basis and its dimension.** On an analysis-suitable T-mesh the blending functions are a basis of their span, so the dimension of the T-spline space is the number of anchors. The mass matrix $\int T_A T_B$ is then symmetric positive definite, and a Galerkin stiffness matrix of a coercive problem is nonsingular after the boundary conditions are imposed.
- **Unique control points.** A T-spline surface on an analysis-suitable T-mesh has exactly one set of control points. Refinement matrices, such as the one of [local refinement](/t-spline-local-refinement/), are then unique too.
- **A practical test for any T-mesh.** For a general T-mesh, compute $M$ and its rank in exact arithmetic, or prune its graph. In [Bezier extraction](/bezier-extraction/) the same matrix appears element by element.
- **Together with partition of unity.** Analysis-suitable T-splines also form a [partition of unity](/partition-of-unity/), a cited result of Zhang and Li (2015) for every degree. With independence, they behave like B-splines in a finite element code.

## Tightness

- **General T-meshes can be dependent.** For the T-mesh of Buffa, Cho and Sangalli, drawn as Figure 4 of Li and coauthors, $M$ is $56 \times 40$ with rank 39, and the functions $T_1$, $T_2$, $T_3$ of three T-junctions satisfy $T_1 = T_2 + \tfrac13 T_3$. The mesh is not analysis-suitable. The tests rebuild it in index space and get the same rank and relation.
- **Dependence can need special knots.** For the same topology, Li and coauthors show by column reduction that the functions are dependent if and only if three consecutive $s$ knots are equal and three consecutive $t$ knots are equal, as in the example, where both are $\tfrac12$. The tests check that moving either triple knot apart gives rank 40. Theorem 18 is stronger: the topology alone gives independence.
- **Analysis-suitable is sufficient, not necessary.** A tensor mesh with one face split by a cross is not analysis-suitable, because its extensions touch at the centre, but its blending functions are independent for the knots of the tests. Theorem 18 gives no information on such meshes.
- **Degree.** The theorem above is bicubic. Beirão da Veiga, Buffa, Sangalli and Vázquez extend analysis-suitability and independence to every degree.

## History

Sederberg and coauthors introduced T-splines in 2003. Buffa, Cho and Sangalli showed in 2010 that their blending functions can be linearly dependent, which ruled out general T-splines as a basis for analysis. Li, Zheng, Sederberg, Hughes and Scott replied with the rank criterion and with analysis-suitable T-splines, and proved them independent; the paper appeared in Computer Aided Geometric Design in 2012. In the same year Beirão da Veiga, Buffa, Cho and Sangalli proved that analysis-suitable T-splines are dual-compatible, and with Vázquez extended the theory to arbitrary degree in 2013. Zhang and Li proved partition of unity for arbitrary degree in 2015.

## References
