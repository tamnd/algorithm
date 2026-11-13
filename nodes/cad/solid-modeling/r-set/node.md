---
tag: 26CNDM
kind: definition
slug: r-set
name: r-set
aliases:
- regular semianalytic set
area: cad/solid-modeling
level: core
summary: Requicha's model of a solid, a bounded, closed, regular and semianalytic subset of 3D space, so that it has an interior, a boundary and a finite description.
see_also: [regularized-set-operations, manifold-solid, boundary-representation, constructive-solid-geometry, spatial-occupancy-enumeration, function-representation, semialgebraic-set, polygon-with-holes]
sources:
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the sections on mathematical models of solids (r-sets) and on representation schemes and their formal properties
  - paper: "Aristides A. G. Requicha and Robert B. Tilove, Mathematical foundations of constructive solid geometry, general topology of closed regular sets, Production Automation Project Technical Memorandum 27, University of Rochester, 1978"
    locator: closed regular sets and the regularized operations
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: Chapter 3, Sections 3.3 and 3.4, Mathematical models of solids and Point-set models (Section 3.4.2, Regularity, p. 33), Section 3.6, Representation schemes (p. 49), and Appendix B, Elements of point set topology
  - book: isbn:9781558600676
    title: Christoph M. Hoffmann, Geometric and Solid Modeling, An Introduction, Morgan Kaufmann, 1989
    locator: Chapter 2, Basic Concepts
---

An r-set is the mathematical model of a rigid solid that Requicha proposed in 1980: a subset of 3D Euclidean space $E^3$ that is bounded, closed, regular and semianalytic. Each of the four conditions removes a kind of set that no physical solid can be: an infinite set, a set without its skin, a set with dangling faces, edges or points, and a set with infinitely many wiggles or parts. The r-sets are the *modeling space* of solid modeling. A representation such as a [boundary representation](/boundary-representation/) or a [CSG tree](/constructive-solid-geometry/) is valid when it stands for an r-set.

## Definition

Write $\operatorname{int} X$ for the interior of a set $X \subseteq E^3$ (the points that have a small open ball inside $X$), $\operatorname{cl} X$ for its closure (the points whose every ball meets $X$), and $\partial X = \operatorname{cl} X \setminus \operatorname{int} X$ for its boundary.

- **Bounded.** $X$ lies inside some ball of finite radius.
- **Closed.** $X = \operatorname{cl} X$, so $X$ contains its boundary.
- **Regular.** $X = \operatorname{cl}(\operatorname{int} X)$. A set with this property is a *closed regular set* (in topology, a regular closed set). Each point of $X$ is a limit of interior points, so $X$ has no part of lower dimension that hangs out of the body.
- **Semianalytic.** $X$ is a finite Boolean combination (union, intersection and complement) of sets $\{p \in E^3 : f_i(p) \ge 0\}$, where each $f_i$ is a real analytic function on $E^3$, for example a polynomial.

An **r-set** is a subset of $E^3$ that is bounded, closed, regular and semianalytic. Requicha also allows $E^2$, where an r-set models a lamina. The empty set is an r-set; it is the result of the regularized intersection of two solids that do not share volume.

Four facts follow from the definition. The first two have short proofs. The last two are theorems that Requicha's survey collects.

1. **A regular set is closed.** $\operatorname{cl}(\operatorname{int} X)$ is a closure, so a regular set is closed. The condition "closed" is listed for emphasis.
2. **Rigid motions keep r-sets.** If $T$ is a rotation followed by a translation, $T$ is a homeomorphism of $E^3$, so it maps interior to interior and closure to closure, and $f_i \circ T^{-1}$ is analytic when $f_i$ is. So $T(X)$ is an r-set.
3. **Closure under the regularized operations.** If $A$ and $B$ are r-sets, then the [regularized](/regularized-set-operations/) union, intersection and difference of $A$ and $B$ are r-sets. The ordinary operations do not have this property.
4. **Finite description.** The boundary of an r-set is a semianalytic set of dimension at most 2, and semianalytic sets can be triangulated (a theorem of Łojasiewicz). So an r-set has finitely many connected components, and its boundary splits into finitely many faces. This is what lets a computer store it.

**Representation schemes.** Requicha defines a *representation scheme* as a relation $s$ from a set of syntactically correct symbol structures (the representations) to the modeling space $M$ of r-sets. The properties of a scheme are:

| property | meaning |
|---|---|
| domain | the set of solids that the scheme can describe, $s(\text{valid representations}) \subseteq M$ |
| validity | the representations that the scheme maps into $M$; a valid representation stands for an r-set |
| unambiguity (completeness) | each valid representation stands for exactly one solid |
| uniqueness | each solid in the domain has exactly one representation |

A scheme can be unambiguous and still not unique. [Constructive solid geometry](/constructive-solid-geometry/) is the standard example: the same block is the union of two half blocks in many ways.

## Examples and non-examples

Each example is checked against the four conditions.

- **The unit cube** $C = [0, 1]^3$. It is bounded and closed. Its interior is $(0, 1)^3$, and the closure of that is $C$, so it is regular. It is semianalytic as the intersection of the six sets $x \ge 0$, $1 - x \ge 0$, $y \ge 0$, $1 - y \ge 0$, $z \ge 0$ and $1 - z \ge 0$. It is an r-set.
- **A closed ball** $\{1 - x^2 - y^2 - z^2 \ge 0\}$ and **a solid torus** with radii $R > r > 0$, the set $\{4R^2(x^2 + y^2) - (x^2 + y^2 + z^2 + R^2 - r^2)^2 \ge 0\}$, are r-sets. Each is one polynomial inequality.
- **A cube with a cavity**, $[0, 3]^3$ minus the open cube $(1, 2)^3$. It is closed, and each point of the inner face $\partial [1, 2]^3$ is a limit of points of the body, so it is regular. It is an r-set with two boundary shells.
- **Two cubes that share an edge**, $[0, 1]^3 \cup [1, 2] \times [1, 2] \times [0, 1]$. It is an r-set. It is not a [manifold solid](/manifold-solid/), because near a point of the shared edge the boundary looks like two planes that cross, not like a disk.
- **Two disjoint cubes.** An r-set need not be connected.

Non-examples, each with the condition that fails:

- **An open ball** $\{x^2 + y^2 + z^2 < 1\}$ is not closed. Its boundary sphere is missing.
- **A half-space** $\{z \ge 0\}$ is closed, regular and semianalytic, but not bounded.
- **A cube with a dangling face**, $[0, 1]^3 \cup [1, 2] \times [0, 1] \times \{0\}$. It is closed, but the square $[1, 2] \times [0, 1] \times \{0\}$ has no interior points near it. So $\operatorname{cl}(\operatorname{int} X) = [0, 1]^3 \ne X$, and the set is not regular. A cube with an isolated point, or with a wire edge, fails in the same way.
- **An infinite comb.** Let $X$ be the union of the slabs $[1/(2k + 1), 1/(2k)] \times [0, 1]^2$ for $k = 1, 2, \ldots$ and the face $\{0\} \times [0, 1]^2$. It is bounded. It is closed, because the slabs pile up only at $x = 0$, and that face is in $X$. It is regular, because each point of the face is a limit of points inside the thin slabs. But it has infinitely many connected components, so it is not semianalytic by fact 4. No finite list of faces describes it, and this is exactly the case that the fourth condition removes.

The table gives the result of the check.

| set | bounded | closed | regular | semianalytic | r-set |
|---|---|---|---|---|---|
| unit cube | yes | yes | yes | yes | yes |
| cube with a cavity | yes | yes | yes | yes | yes |
| two cubes on an edge | yes | yes | yes | yes | yes |
| open ball | yes | no | no | yes | no |
| half-space | no | yes | yes | yes | no |
| cube with a dangling face | yes | yes | no | yes | no |
| infinite comb | yes | yes | yes | no | no |

## Related definitions

- [Regularized set operations](/regularized-set-operations/) are the set operations that keep r-sets closed: $A \cup^* B$, $A \cap^* B$ and $A -^* B$, each the closure of the interior of the ordinary result.
- A [manifold solid](/manifold-solid/) is an r-set whose boundary is a 2-manifold. It is a smaller class than the r-sets. Many modelers work only in this class, and the [radial edge data structure](/radial-edge-data-structure/) exists for the r-sets outside it.
- A [semialgebraic set](/semialgebraic-set/) is the case where every $f_i$ is a polynomial. Every semialgebraic set is semianalytic. The solids of a CAD system with planes, quadrics, tori and NURBS patches are semialgebraic.
- The schemes of solid modeling are [boundary representation](/boundary-representation/), [constructive solid geometry](/constructive-solid-geometry/), [spatial occupancy enumeration](/spatial-occupancy-enumeration/) and [function representation](/function-representation/). Each one has its own domain, validity test and uniqueness, as in the table of the Definition section.
- In the plane, a [polygon with holes](/polygon-with-holes/) is a 2D r-set whose boundary is made of segments. The [Jordan curve theorem](/jordan-curve-theorem/) says that each boundary cycle cuts the plane into an inside and an outside.

## References
