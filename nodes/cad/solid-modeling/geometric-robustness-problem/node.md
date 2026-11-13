---
tag: 7BX1AZ
kind: concept
slug: geometric-robustness-problem
name: Geometric robustness problem
aliases:
- robustness of geometric algorithms
area: cad/solid-modeling
level: core
summary: Rounded geometric tests in a modeler can disagree with each other, so the computed topology can be impossible and Booleans or offsets fail.
prereqs: [orientation-test, catastrophic-cancellation, real-ram]
see_also: [exact-geometric-computation, simulation-of-simplicity, general-position, shewchuk-expansion-sum, interval-arithmetic, solid-boolean-operations, boundary-evaluation, vertex-neighborhood-classification]
sources:
  - paper: doi:10.1109/2.16223
    title: Christoph M. Hoffmann, The problems of accuracy and robustness in geometric computation, IEEE Computer 22(3), 31 to 41, 1989
    locator: the whole paper (why rounded tests give inconsistent topology in solid modeling, and the approaches of exact arithmetic, tolerances and consistent reasoning)
  - paper: doi:10.1016/j.comgeo.2007.06.003
    title: Lutz Kettner, Kurt Mehlhorn, Sylvain Pion, Stefan Schirra and Chee Yap, Classroom examples of robustness problems in geometric computations, Computational Geometry 40(1), 61 to 78, 2008
    locator: the whole paper (float inputs on which the orientation test fails and a textbook convex hull program gives a wrong result)
  - paper: doi:10.1016/0925-7721(95)00040-2
    title: Chee K. Yap, Towards exact geometric computation, Computational Geometry 7(1-2), 3 to 23, 1997
    locator: the discussion of the sources of nonrobustness and of the exact geometric computation approach
  - paper: doi:10.1109/38.41469
    title: Christoph M. Hoffmann, John E. Hopcroft and Michael S. Karasick, Robust set operations on polyhedral solids, IEEE Computer Graphics and Applications 9(6), 50 to 59, 1989
    locator: the whole paper (Boolean operations in floating point that keep the topological decisions consistent)
  - book: isbn:9781558600676
    title: Christoph M. Hoffmann, Geometric and Solid Modeling, An Introduction, Morgan Kaufmann, 1989
    locator: Chapter 4, Robust and error-free geometric operations
---

The geometric robustness problem is the failure of geometric programs that make exact decisions from rounded numbers. A modeler decides with signs, such as whether a point is above a plane or whether two edges cross, and the topology of its output follows from these decisions. With floating point, each sign is computed from rounded values, and the signs need not agree with each other or with any real input. The program can then build a face that does not close, a vertex on both sides of a plane, or a solid that breaks the [Euler-Poincaré formula](/euler-poincare-formula/), and it may crash or loop. There is no single formal problem: the name covers a family of failures and of fixes, and authors define a robust algorithm in different ways.

## In plain words

A CAD program asks yes or no questions about shapes. Is this corner above that face? Do these two edges cross? The answers decide how the pieces of a model connect.

The computer computes with numbers that are rounded after each step. Most of the time a small rounding error does not change an answer. But when a corner is almost exactly on a face, the error is larger than the true distance, and the answer can be wrong.

One wrong answer is not the real trouble. The trouble is two answers that cannot both be true, such as "this corner is above the face" and "this corner is below the face", asked in two different ways. The program trusts both, connects the pieces in an impossible way, and the result is a broken model or a crash.

## The idea

**Predicates and constructions.** A geometric program has two kinds of steps. A *construction* computes new numbers: the point where three planes meet, the plane of a face, the parameter where a ray enters a box. A *predicate* computes a sign from numbers: the [orientation test](/orientation-test/) of three points in the plane or four points in space, the side of a point against a plane, the [in-circle test](/in-circle-test/). Only predicates choose branches, so the combinatorial output, which vertices bound which edges and which faces meet at which vertex, is a function of the predicate values alone.

**Exact reals and floating point.** Algorithms are designed and proved in the [real RAM](/real-ram/), where every sign is exact. In that model a set of answers always comes from one real input, and so it obeys every geometric law: a point is on one side of a plane only, three cyclic orders of a triangle have one orientation, a constructed point lies on the planes it was built from. A floating-point program computes each sign from rounded values, and the error is largest exactly when the true value is near zero ([catastrophic cancellation](/catastrophic-cancellation/)). A set of rounded answers may come from no real input at all. Proofs assume that it does, so they no longer apply.

**Three sources of failure.** The examples below show each one.

1. *Rounded predicates.* The same sign, computed by two formulas that are equal in exact arithmetic, comes out different.
2. *Rounded constructions.* A constructed point is rounded, so it is not on the objects it came from, and later predicates on it see a small error as real geometry.
3. *Degenerate input.* Coplanar faces, touching solids and a vertex on a face give predicates that are exactly zero. CAD models have many such cases on purpose, because designers align faces. Code that treats zero as an error, or that assumes [general position](/general-position/), fails even with exact arithmetic.

**What "robust" means.** Hoffmann separated accuracy, how close the numbers of the output are to the true ones, from robustness, whether the program ends with a valid and consistent result. There are several formal goals in use:

- *Exact decisions.* Every predicate is evaluated exactly on the input, so the combinatorial output is the exact one. This is [exact geometric computation](/exact-geometric-computation/).
- *Consistent decisions.* The decisions need not be exact, but they must be consistent with some real input near the given one, so the output is a valid structure for a perturbed input. Hoffmann, Hopcroft and Karasick built Boolean operations on polyhedra in this style, deriving an uncertain sign from decisions already made.
- *Tolerances.* Two entities closer than a tolerance are taken as equal. This is common in commercial kernels, but it is not a proof of anything: "closer than $\delta$" is not transitive, so a chain of almost equal points can join points far apart.

**The fixes in short.** Exact integer or rational arithmetic; floating-point filters with an exact fallback ([Shewchuk's expansion sum](/shewchuk-expansion-sum/), [interval arithmetic](/interval-arithmetic/)); an infinitesimal move of the input that removes the degenerate cases ([simulation of simplicity](/simulation-of-simplicity/)); and the design of algorithms whose decisions are few and independent, so that they cannot contradict each other.

## Examples

All numbers below were computed in IEEE double precision, with $u = 2^{-53}$, and checked with exact rational arithmetic on the same doubles.

**A triangle with three orientations.** The orientation test page gives a point $p = (0.5 + 41u, 0.5 + 48u)$ with $q = (12, 12)$ and $r = (24, 24)$, where the exact value is $D(p, q, r) = 84u > 0$ and the float value is negative. The three cyclic orders of the same triangle are equal in exact arithmetic, but in floating point:

| order | float value | float sign |
|---|---|---|
| $D(p, q, r)$ | $-5.68 \times 10^{-14}$ | right turn |
| $D(q, r, p)$ | $0$ | collinear |
| $D(r, p, q)$ | $+5.68 \times 10^{-14}$ | left turn |

Over the $256 \times 256$ grid of points $p = (0.5 + iu, 0.5 + ju)$, $0 \le i, j < 256$, the three orders do not all agree for $13968$ of the $65536$ points, and for $560$ points they give both a left and a right turn. A program that tests the triangle once from each vertex sees an impossible triangle.

**A point on both sides of a face.** Let a face lie in the plane of $a = (0.1, 0.2, 0.3)$, $b = (1.7, 0.4, 0.9)$ and $c = (0.6, 2.3, 1.1)$, as doubles, and let $x = (0.37681589533836873, 1.1181550673794072, 0.6694139419950996)$ be a point near it. The side of $x$ is the sign of the $3 \times 3$ determinant of the differences from a base vertex. With base $a$ the float value is $-1.25 \times 10^{-16}$, below the plane. With base $b$, the determinant of $c - b$, $a - b$, $x - b$, which is the same number in exact arithmetic, the float value is $+1.67 \times 10^{-16}$, above the plane. The exact sign is negative. Two edges of a B-rep that test the same vertex against the same face, each with its own base vertex, disagree about where the vertex is. In a test of $200000$ points placed in the plane of the triangle and rounded to doubles, $85294$ gave different signs with the two base vertices.

**A constructed point that is off its lines.** The lines $y = x$ and $y = 1 - 2x$ meet at $(1/3, 1/3)$. The usual formula for the crossing of two segments, from $(0, 0)$ to $(1, 1)$ and from $(0, 1)$ to $(1, -1)$, gives $(0.3333333333333333, 0.3333333333333333)$ in floating point. The line through $(1, 0)$ and $(-1, 1)$ passes exactly through $(1/3, 1/3)$, so the three lines are concurrent. The float orientation of $(1, 0)$, $(-1, 1)$ and the computed point is $+1.11 \times 10^{-16}$, a left turn. The program sees a tiny triangle between three lines that meet in one point. In a solid, three planes through one line give the same kind of sliver face.

**Classroom examples.** Kettner, Mehlhorn, Pion, Schirra and Yap give small float inputs, built on grids like the one above, on which a textbook incremental convex hull program returns a polygon that is not convex or leaves out a point far from the polygon. The programs are correct in the real RAM, and the only change is the rounding of the orientation test.

**A degenerate case with exact numbers.** The cubes $[0, 1]^3$ and $[1, 2] \times [0, 1]^2$ share the face $x = 1$. Every point of that face gives a side-of-plane value of exactly $0$ against both cubes. The page on [regularized set operations](/regularized-set-operations/) shows that the regularized intersection is empty while the plain one is the face. A Boolean that takes $0$ as "inside" keeps the face, and one that takes it as "outside" drops faces it needs. No precision helps here, because the issue is the rule for zero.

## Where it is used

- **Boolean operations.** [Solid Boolean operations](/solid-boolean-operations/), [boundary evaluation](/boundary-evaluation/) and [vertex neighborhood classification](/vertex-neighborhood-classification/) cut faces at rounded points and then classify the pieces. Most of their published failures are of the kinds above. The same holds for [mesh Boolean operations](/mesh-boolean-operations/).
- **Ray casting and classification.** [CSG ray casting](/csg-ray-casting/) can return a sliver interval at a shared face when the exit from one primitive and the entry into the next are rounded apart.
- **Intersections of curved surfaces.** [Surface surface intersection](/surface-surface-intersection/) and [solid offsetting](/solid-offsetting/) construct curves by numerical methods, so their output is always approximate, and the decisions made on it need a tolerance or a proof of consistency.
- **Computational geometry in general.** Convex hulls, [Delaunay](/in-circle-test/) triangulations and sweeps ([degeneracies in sweeps](/degeneracy-in-sweeps/)) have the same failure modes. The classroom examples are planar hulls.
- **Mass properties.** Volumes and moments are constructions, not decisions, so rounding makes them a little wrong but not inconsistent. [Mirtich's method](/mirtich-polyhedral-mass-properties/) is exact with rational input.

## References
