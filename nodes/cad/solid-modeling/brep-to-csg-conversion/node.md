---
tag: 4T6TA6
kind: problem
slug: brep-to-csg-conversion
name: B-rep to CSG conversion
aliases:
- boundary to CSG conversion
area: cad/solid-modeling
level: research
summary: Find a CSG tree for a solid given by its boundary. Shapiro and Vossler solved it for curved solids by separating halfspaces and a Boolean construction.
prereqs: [constructive-solid-geometry, boundary-representation, regularized-set-operations]
see_also: [boundary-evaluation, set-membership-classification, solid-boolean-operations, feature-recognition, function-representation, line-arrangement, quine-mccluskey, r-set]
sources:
  - paper: "Vadim Shapiro and Donald L. Vossler, Construction and optimization of CSG representations, Computer-Aided Design 23(1), 4 to 20, 1991"
    locator: the whole paper (the canonical union of cells built from the half-spaces of the faces, and the reduction of its size)
  - paper: doi:10.1145/169728.169723
    title: Vadim Shapiro and Donald L. Vossler, Separation for boundary to CSG conversion, ACM Transactions on Graphics 12(1), 35 to 55, 1993
    locator: the whole paper (why the face half-spaces of a curved solid may not be enough, and how separating half-spaces are found)
  - paper: doi:10.1145/378456.378472
    title: David Dobkin, Leonidas Guibas, John Hershberger and Jack Snoeyink, An efficient algorithm for finding the CSG representation of a simple polygon, Computer Graphics 22(4), Proceedings of SIGGRAPH 1988
    locator: the whole paper (a formula for a simple polygon in which each edge half-plane appears once)
  - paper: doi:10.1007/BF01908629
    title: David Dobkin, Leonidas Guibas, John Hershberger and Jack Snoeyink, An efficient algorithm for finding the CSG representation of a simple polygon, Algorithmica 10(1), 1 to 23, 1993
    locator: the journal version, with the O(n log n) construction of the formula
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the discussion of conversion between representations
---

B-rep to CSG conversion asks for a [CSG](/constructive-solid-geometry/) formula, a Boolean combination of half-spaces or primitives, whose regularized value is a solid given by its [boundary](/boundary-representation/). It is the reverse of [boundary evaluation](/boundary-evaluation/). For polyhedra the half-spaces of the faces are always enough. For curved solids they may not be, because a region with one sign pattern can have parts inside and outside the solid, and extra *separating* half-spaces are needed. Shapiro and Vossler gave the theory and the construction for curved solids, and the size of a shortest formula is a separate optimization problem.

## In plain words

A CSG model says how to build a shape from simple pieces: take this block, cut away that cylinder, add this other block. A boundary model only lists the outer faces. This problem goes from the faces back to a recipe of pieces.

Each face lies on a surface, such as a plane or a cylinder, and the surface splits space into an inside and an outside. The idea is to build the shape from these sides with "and", "or" and "not".

For flat faces this always works. For curved faces it can fail: two places can be on the same side of every surface, while only one of them is in the shape. Then the recipe needs an extra surface that is not a face, only to tell the two places apart.

## Definition

**Input.** A solid $S \subset E^3$, an [r-set](/r-set/), given as a B-rep whose faces lie on surfaces $\{f_i = 0\}$, $i = 1, \ldots, k$. Each surface gives a half-space $h_i = \{f_i \le 0\}$, oriented so that $S$ is locally on the side $f_i \le 0$ of each face on it. The $h_i$ are the *face half-spaces*.

**Output.** A Boolean formula $\Phi$ whose leaves are half-spaces, and whose inner nodes are $\cup^*$, $\cap^*$ and $-^*$, with value exactly $S$. The leaves are the face half-spaces and, if needed, further half-spaces $g_1, \ldots, g_r$ of a fixed family, such as planes or quadrics.

**Objective.** In the decision form, does $S$ have a formula over the face half-spaces alone? In the construction form, find a formula, with extra half-spaces when the face half-spaces are not enough. In the optimization form, find a formula with the fewest leaf occurrences.

**Notation.** For a point $p$ that lies on no surface $\{f_i = 0\}$, its *sign vector* is $\sigma(p) \in \{-, +\}^k$, the signs of $f_1(p), \ldots, f_k(p)$. A *cell* is a connected component of the set of points with one sign vector.

## Variants

- **Polygons and polyhedra.** All surfaces are lines or planes. The face half-spaces are always enough, by the lemma below.
- **Each half-space once.** For a simple polygon, a formula in which each edge half-plane appears exactly once always exists, and Dobkin, Guibas, Hershberger and Snoeyink compute it in $O(n \log n)$ time for $n$ edges.
- **Curved solids.** Faces on quadrics, tori and general algebraic surfaces. Separating half-spaces may be needed, and Shapiro and Vossler give methods to find them.
- **Primitives instead of half-spaces.** The leaves must be bounded primitives such as blocks and cylinders. This is close to [feature recognition](/feature-recognition/), which looks for holes, slots and pockets in a B-rep.
- **Minimum formula.** Among the formulas for $S$, find a shortest one. This is a form of Boolean function minimization, as in [Quine-McCluskey](/quine-mccluskey/), over the sign vectors that occur.
- **Approximate input.** The input is a mesh or a point cloud, and the output is a formula whose solid is close to it.

## Examples

**An L-shaped polygon.** $S = [0, 2]^2 - (1, 2]^2$ has six edges on the lines $x = 0$, $y = 0$, $x = 2$, $y = 2$, $x = 1$, $y = 1$. A formula over the six edge half-planes, with each one used once, is
$$S = \{x \ge 0\} \cap \{y \ge 0\} \cap \{x \le 2\} \cap \{y \le 2\} \cap \big(\{x \le 1\} \cup \{y \le 1\}\big).$$
The point $(1.5, 1.5)$ fails both $x \le 1$ and $y \le 1$, so it is outside, and every point of the L satisfies one of them.

**Face half-spaces that are not enough.** In the plane, let $S = \{(x, y) : 0 \le y \le 1,\ \sqrt{1 + y} \le x \le 3\}$, the region right of the parabola branch $x = \sqrt{1 + y}$, below $y = 1$, above $y = 0$ and left of $x = 3$. Its boundary lies on the four curves $y = 0$, $y = 1$, $x = 3$ and $y = x^2 - 1$, so these give the face half-planes. The points $p = (2, 0.5)$ and $q = (-2, 0.5)$ both satisfy all four inequalities strictly: $0 < 0.5 < 1$, $0.5 < 3$, $2 < 3$ and $-2 < 3$. So $\sigma(p) = \sigma(q)$, but $p \in S$ and $q \notin S$. By the lemma below, no formula over the four face half-planes has the value $S$. The separating half-plane $x \ge 0$ fixes it:
$$S = \{y \ge 0\} \cap \{y \le 1\} \cap \{x \le 3\} \cap \{y \le x^2 - 1\} \cap \{x \ge 0\}.$$
The same happens in space with faces on a cylinder or a torus.

## Known algorithms

There are no algorithm pages for this problem yet. The known methods are these.

- **Canonical union of cells** (Shapiro and Vossler 1991). Compute the cells of the arrangement of the face surfaces, classify one point of each cell against $S$ with [set membership classification](/set-membership-classification/), and take the union of the cells inside $S$, each written as the intersection of the $k$ half-spaces or their complements. The result is correct whenever the face half-spaces are enough, and its size is the number of inside cells times $k$. A second phase reduces the formula by Boolean minimization.
- **Separation** (Shapiro and Vossler 1993). When two cells with one sign vector have different classifications, add half-spaces that split them, then run the canonical construction on the larger set.
- **Single-occurrence formulas for simple polygons** (Dobkin, Guibas, Hershberger and Snoeyink). A formula in which each edge half-plane appears once, built in $O(n \log n)$ time for $n$ edges.

## Bounds

**Lemma (describability).** $S$ has a formula over half-spaces $H = \{h_1, \ldots, h_k\}$ if and only if every two points $p, q$ that lie on none of the surfaces and have $\sigma(p) = \sigma(q)$ are both in $S$ or both outside $S$.

*Proof.* (Only if.) Let $\Phi$ be a formula and $p$ a point on none of the surfaces. Near $p$ each $f_i$ keeps its sign, so the plain Boolean value of $\Phi$ is the same at all points of a ball around $p$, and it depends only on $\sigma(p)$. Regularization does not change the value at a point of an open set where the plain value is constant. So the value of $\Phi$ at $p$ is a function of $\sigma(p)$, and two points with the same sign vector are both in or both out. (If.) Let $\Sigma$ be the set of sign vectors of points of $\operatorname{int} S$ off the surfaces, and let $\Phi = \bigcup^*_{\sigma \in \Sigma} \bigcap^*_i h_i^{\sigma_i}$, where $h_i^-$ is $h_i$ and $h_i^+$ is its closed complement. By the condition, a point off the surfaces is in $\Phi$ exactly when it is in $S$. The surfaces have no interior, and both $\Phi$ and $S$ are regular closed, so they are the closures of the same open set, and $\Phi = S$. $\blacksquare$

**Polyhedra.** For planes, each set of points with one sign vector is an intersection of open half-spaces, which is convex and so connected. A connected set that does not meet $\partial S$ lies in $\operatorname{int} S$ or outside $S$. So the condition of the lemma holds, and every polyhedron has a formula over its face half-spaces. The arrangement of $k$ planes has $O(k^3)$ cells, so the canonical formula has $O(k^4)$ leaf occurrences. In the plane, $k$ lines give $O(k^2)$ cells and $O(k^3)$ occurrences. Each half-plane once is enough for simple polygons.

**Curved solids.** The parabola example shows that the condition can fail for curved faces, so separating half-spaces are needed in general. Shapiro and Vossler show how to find them for the surfaces of common solids. A bound on how many are needed in the worst case is not given in the sources here.

**Minimum size.** Finding a shortest formula is a minimization over Boolean formulas. Shapiro and Vossler reduce the canonical formula by methods of Boolean minimization, and their results on the size are measured on examples. The complexity of computing a minimum formula for a solid is not settled in the sources here.

## Reductions

- **To set membership classification.** The canonical construction needs one in or out answer per cell, which is a point classification against the B-rep.
- **To arrangements.** The cells are those of the arrangement of the face surfaces. For polygons this is the [line arrangement](/line-arrangement/) of the edge lines.
- **To Boolean minimization.** Once the inside and outside sign vectors are known, a shortest formula over the given half-spaces is a shortest Boolean formula for a partial function on $\{-, +\}^k$, where the sign vectors that occur in no cell are don't-cares.
- **Inverse of boundary evaluation.** Boundary evaluation of the output formula must return the input solid, which gives a check of any conversion.

## Applications

- **Editing.** A CSG tree can be edited by changing a parameter of a primitive, so a conversion makes imported B-rep models editable.
- **Ray casting and classification.** [CSG ray casting](/csg-ray-casting/) and point classification work directly on the formula.
- **Model exchange and compression.** A short formula can be a compact description of a solid.
- **Reverse engineering.** A CSG description of a scanned part, built from the fitted surfaces, gives a model with design intent.

## References
