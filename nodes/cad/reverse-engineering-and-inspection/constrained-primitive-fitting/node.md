---
tag: 04S2RE
kind: technique
slug: constrained-primitive-fitting
name: Constrained fitting in reverse engineering
aliases:
- GlobFit
- constrained reverse engineering
area: cad/reverse-engineering-and-inspection
level: research
summary: Fits several primitives at once subject to relations such as parallel axes, orthogonal faces and equal radii, so the model keeps the design intent.
prereqs: [geometric-primitive-fitting, lagrange-multiplier]
see_also: [efficient-ransac-shape-detection, ransac, penalty-method, augmented-lagrangian-method, brep-reconstruction-from-scans, reverse-engineering-of-geometric-models, principal-component-analysis, quadratic-programming]
sources:
  - paper: doi:10.1016/S0167-8396(01)00085-1
    title: Pál Benkő, Géza Kós, Tamás Várady, László Andor and Ralph Martin, Constrained fitting in reverse engineering, Computer Aided Geometric Design 19(3), 2002, 173 to 205
    locator: the simultaneous fit of several curves and surfaces under constraints between their parameters, the section on numerical methods for constrained fitting, and the 2D and 3D examples
  - paper: doi:10.1145/1964921.1964947
    title: Yangyan Li, Xiaokun Wu, Yiorgos Chrysanthou, Andrei Sharf, Daniel Cohen-Or and Niloy J. Mitra, GlobFit, consistently fitting primitives by discovering global relations, ACM Transactions on Graphics 30(4) (SIGGRAPH 2011), article 52
    locator: the detection of global relations among RANSAC primitives and the three stages of constrained refitting (orientation, placement, equality)
  - paper: doi:10.1016/S0010-4485(99)00038-X
    title: Naoufel Werghi, Robert Fisher, Craig Robertson and Anthony Ashbrook, Object reconstruction by incorporating geometric constraints in reverse engineering, Computer-Aided Design 31(6), 1999, 363 to 399
    locator: the global improvement of a reconstructed shape from feature positions and the geometric relations between features, posed as constrained least squares
---

Constrained fitting fits several primitives of a scanned part at the same time, so that the fitted surfaces satisfy geometric relations that the designer intended: faces that are parallel or orthogonal, holes that are coaxial or of equal radius, a fillet that is tangent to its two faces. If each region of a [segmented](/primitive-segmentation/) scan is fitted alone, as on the [geometric primitive fitting](/geometric-primitive-fitting/) page, the noise makes two faces that should be orthogonal meet at $89.7$ degrees, and the model is useless for redesign. The technique has three parts: find candidate relations among the separate fits, choose a subset that is consistent and not redundant, and refit all primitives together, minimizing the total fitting error subject to the chosen relations as equality constraints. The constrained problem is solved by sharing parameters, by [Lagrange multipliers](/lagrange-multiplier/), or by a [penalty](/penalty-method/) or [augmented Lagrangian](/augmented-lagrangian-method/) method. Benkő, Kós, Várady, Andor and Martin (2002) set out this approach for reverse engineering. GlobFit, by Li, Wu, Chrysanthou, Sharf, Cohen-Or and Mitra (2011), is one method of this kind: it discovers the relations among primitives found by [RANSAC](/ransac/) and enforces them in three stages.

## In plain words

When a part is scanned and each face is fitted on its own, the result is close but not exact. Two walls that were drawn at a right angle come out at almost a right angle. Two holes that were drawn with the same radius come out with slightly different radii. An engineer who reads the model cannot tell an intended small angle from a scanning error.

Constrained fitting looks for such near coincidences, decides which of them the designer most likely meant, and then fits all the faces again together, so that the right angle is exactly a right angle and the radii are exactly equal. The fit gets a little worse in the strict sense of distance to the points, but the model now says what the part is.

## When it applies

- A scan has been segmented into regions, and each region has been fitted with a primitive: plane, sphere, cylinder, cone or torus.
- The object is a manufactured part, so its design is full of exact relations: parallel, orthogonal, coplanar, coaxial, concentric, equal radii, tangent, symmetric.
- The separate fits are close to satisfying these relations, within the noise. A relation that is clearly violated by the data is not a relation of the part.
- The result is used as a CAD model, for redesign, for machining, or as the nominal of an inspection, where the intent matters more than the last micrometer of fit.

## The template

Each primitive $j$ has parameters $\theta_j$ and a fitting error $E_j(\theta_j) = \sum_{x \in R_j} d(x, S(\theta_j))^2$ over its region $R_j$. A relation is an equation $g(\theta) = 0$ in the parameters of a few primitives, such as $n_1 \cdot n_2 = 0$ for orthogonal planes or $r_1 - r_2 = 0$ for equal radii.

```pseudo id=main
CONSTRAINED-FIT(regions R_1..R_k, tolerance τ, budget β)
L1  for j ← 1 to k do θ_j ← geometric fit of the primitive of R_j alone
L2  C ← candidate relations g with |g(θ)| ≤ τ for the separate fits
L3  A ← ∅
L4  for each stage s in (orientation, placement, equality) do
L5      for each candidate g of stage s in C, the most nearly satisfied first do
L6          if A ∪ {g} is consistent and g is not implied by A then
L7              θ' ← argmin Σ_j E_j(θ_j) subject to h(θ) = 0 for every h in A ∪ {g}
L8              if Σ_j E_j(θ'_j) − Σ_j E_j(θ_j) ≤ β then A ← A ∪ {g}; θ ← θ'
L9  return θ and the accepted relations A
```

The holes are the list of relation types and their tolerances $\tau$, the order in which candidates are tried, the test for consistency and redundancy, the solver of line L7, and the error budget $\beta$.

**Line L2, candidates.** Orientation relations compare directions: the normals of planes and the axes of cylinders, cones and tori. Two directions within a few degrees are candidates for parallel, within a few degrees of $90$ for orthogonal. Placement relations compare positions: coplanar planes, coaxial cylinders, concentric spheres. Equality relations compare sizes: equal radii, equal distances between parallel planes. The tolerance comes from the noise of the scanner and the size of the regions.

**Lines L4 and L5, the order.** Orientations come first, because a placement such as coaxial only makes sense once the axes are parallel, and a size equality only once the placement is fixed. This is the order of the three stages of GlobFit. Within a stage, trying the most nearly satisfied candidate first is a greedy choice; it gives a consistent answer but not necessarily the set of relations that a designer would choose.

**Line L6, consistency and redundancy.** Candidates can conflict: if $n_1 \parallel n_2$, $n_2 \parallel n_3$ and $n_1 \perp n_3$ are all accepted, the system has no solution. They can also be redundant: $n_1 \parallel n_3$ follows from the first two. A redundant constraint makes the Jacobian of the constraints rank deficient, so the Lagrange system of line L7 is singular even when the constrained problem itself is fine. Both are detected by checking whether the new constraint gradient is a combination of the others at the current solution, or, for orientation relations, by grouping the directions into classes of parallel directions first and relating classes, not pairs.

**Line L7, the solver.** Three common ways:
- *Shared parameters.* Write the constrained family directly: parallel planes share one unit normal, coaxial cylinders share an axis, equal radii share $r$. The problem becomes an unconstrained fit with fewer parameters, solved by [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/). This is exact and well conditioned when the relations have such a form.
- *Lagrange multipliers.* Solve $\nabla E(\theta) + \sum_h \lambda_h \nabla h(\theta) = 0$, $h(\theta) = 0$ by Newton steps on this system. Exact at convergence, but it needs independent constraints.
- *Penalties.* Minimize $E(\theta) + w \sum_h h(\theta)^2$ for growing $w$, or use an augmented Lagrangian. Simple, but a pure penalty meets the constraints only in the limit and gets badly conditioned as $w$ grows.

**Line L8, the budget.** A relation that raises the error by much more than the noise explains is rejected: the data say that the part does not have it.

**Why the parallel case is exact.** For two planar regions $A$ and $B$ with one shared unit normal $n$ and offsets $d_A$, $d_B$, the error is $\sum_{x \in A} (n \cdot x - d_A)^2 + \sum_{x \in B} (n \cdot x - d_B)^2$. For fixed $n$, setting the derivatives in $d_A$ and $d_B$ to zero gives $d_A = n \cdot \bar x_A$ and $d_B = n \cdot \bar x_B$ for the centroids. What remains is $n^{\mathsf T} (S_A + S_B) n$ with the scatter matrices $S_A = \sum_{x \in A} (x - \bar x_A)(x - \bar x_A)^{\mathsf T}$ and $S_B$ alike, so $n$ is the eigenvector of the smallest eigenvalue of $S_A + S_B$, by the [Rayleigh quotient](/rayleigh-quotient/) argument of [principal component analysis](/principal-component-analysis/). The separate fits have the errors $\lambda_{\min}(S_A)$ and $\lambda_{\min}(S_B)$, and the increase $\lambda_{\min}(S_A + S_B) - \lambda_{\min}(S_A) - \lambda_{\min}(S_B)$ is never negative, since $n^{\mathsf T} S_A n \ge \lambda_{\min}(S_A)$ and $n^{\mathsf T} S_B n \ge \lambda_{\min}(S_B)$ for every unit $n$. The same pooling works for any number of parallel planes.

## Classic examples

- **Two parallel lines.** Region $A$ has the points $(0, 0)$, $(1, 0.1)$, $(2, -0.1)$, $(3, 0.1)$, $(4, 0)$ and region $B$ the points $(0, 2)$, $(1, 2.1)$, $(2, 1.9)$, $(3, 2)$, $(4, 1.9)$. The separate orthogonal fits give a horizontal line for $A$, with error $0.0280$, and a line for $B$ tilted by $1.72$ degrees, with error $0.0190$. The joint fit with a shared normal, from the pooled scatter matrix, tilts both lines by $0.86$ degrees, with total error $0.0515$ against $0.0470$ for the separate fits, and puts them $1.960$ apart. The increase of $0.0045$ is the price of the relation.
- **The faces of a box.** Six planes in three parallel pairs with mutually orthogonal normals. The constrained fit makes the normals an orthonormal frame, which is what the [B-rep reconstruction](/brep-reconstruction-from-scans/) of a prismatic part needs to produce exact right angles and straight edges.
- **Holes and shafts.** Cylinders of a flange that share an axis, or a bolt circle of holes with equal radii and parallel axes, fitted with shared axis and radius parameters by the [geometric fit](/geometric-primitive-fitting/).
- **Fillets.** A blend cylinder tangent to two planes, as in a [rolling ball blend](/rolling-ball-blend/), has its axis parallel to the line where the planes meet and its axis at distance $r$ from both; Benkő and his coauthors treat such tangency relations.
- **GlobFit.** Primitives from [efficient RANSAC shape detection](/efficient-ransac-shape-detection/) are compared in orientation, placement and equality, relations are chosen greedily stage by stage, and the primitives are refitted after each stage under the accepted relations.

## Variations

- **Relations given by the user.** In interactive reverse engineering the user picks the relations, and only lines L7 and L8 run.
- **Global search of relations.** Instead of a greedy pass, the choice of relations is a combinatorial problem: maximize the number or weight of relations subject to an error budget. Exact search is exponential; greedy order, clustering of directions and of sizes, and voting are the usual heuristics.
- **Soft constraints.** Keep every candidate with a weight, as a penalty term, and let the fit decide. This avoids hard choices but does not produce exact relations.
- **Constraints among curves.** The same scheme applies to 2D profiles and sketches: lines and arcs with tangency, parallelism and equal lengths, which is how a profile for extrusion is rebuilt.
- **Template fitting.** Fit a whole parametric model, such as a standard part from a catalog, whose parameters already encode all relations.

## Pitfalls

- **Conflicting relations.** Three planes pairwise within tolerance of parallel and orthogonal give an infeasible system. Check consistency before solving, as in line L6.
- **Redundant relations.** They make the Lagrange or Newton system singular. Work with classes of parallel directions, or test the rank of the constraint Jacobian.
- **Tolerance too large.** Relations that the designer did not intend get enforced, and real small angles of drafts disappear. A draft angle of one or two degrees on a molded part looks like a near parallel.
- **Tolerance too small.** Intended relations are missed when a region is small or noisy, because its fitted direction is uncertain. The tolerance should depend on the uncertainty of each fit, not be one number for all.
- **Order dependence.** A greedy pass can accept a weak relation early that blocks a stronger one later. Sorting by how nearly each candidate holds reduces this but does not remove it.
- **Bad segmentation.** A relation is only as good as the regions it relates; points from a fillet left in a plane region tilt the plane and can hide a true orthogonality.

## Exercises

1. Show that for $q$ planar regions with one shared normal, the best normal is the smallest eigenvector of $\sum_j S_j$, and that the error increase over the separate fits is $\lambda_{\min}(\sum_j S_j) - \sum_j \lambda_{\min}(S_j) \ge 0$.
2. Give three relations among three plane normals that are pairwise consistent but jointly infeasible, and three that are jointly consistent but redundant. *Answer:* $n_1 \parallel n_2$, $n_2 \parallel n_3$, $n_1 \perp n_3$; and $n_1 \parallel n_2$, $n_2 \parallel n_3$, $n_1 \parallel n_3$.
3. Two coaxial cylinders share an axis but have different radii. Write the shared-parameter form of their joint fit and count its parameters. *Answer:* one axis (4 parameters) and two radii, 6 in total, against 10 for two separate cylinders.

## References
