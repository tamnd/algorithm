---
tag: V244NY
kind: algorithm
slug: interval-projected-polyhedron
name: Interval projected polyhedron algorithm
aliases:
- IPP algorithm
- projected polyhedron solver
area: cad/surface-interrogation-and-design
level: advanced
summary: Sherbrooke and Patrikalakis's solver that finds all roots of a polynomial system in a box by projecting Bernstein control polyhedra and subdividing, robust with intervals.
solves: [polynomial-system-solving]
model: floating-point-model
complexity:
  vars: {K: the number of boxes processed, D: the depth bound n (1 + log2(W / ε)) + 1 of the tree of boxes, W: the widest side of the input box, ε: the box size at which a root is reported, m: the number of equations, n: the number of variables, N: the number of Bernstein coefficients of one equation, d: the largest degree in one variable}
  time: {worst: O(K m n N d)}
  space: {extra: O(D m N)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1993
  people: [Evan C. Sherbrooke, Nicholas M. Patrikalakis]
  note: Sherbrooke and Patrikalakis found all roots of a polynomial system in a box with the projected polyhedron method, which uses the convex hull property of the multivariate Bernstein basis and subdivision. Maekawa and Patrikalakis later ran it in rounded interval arithmetic.
prereqs: [bernstein-polynomials, de-casteljau-algorithm, interval-arithmetic]
see_also: [bezier-clipping, convex-hull-property, interval-newton-method, polynomial-system-solving, real-root-isolation, subdivision-surface-intersection, curve-surface-intersection, homotopy-continuation]
sources:
  - paper: doi:10.1016/0167-8396(93)90019-Y
    title: Evan C. Sherbrooke and Nicholas M. Patrikalakis, Computation of the solutions of nonlinear polynomial systems, Computer Aided Geometric Design 10(5), 379 to 405, 1993
    locator: the whole paper (the multivariate Bernstein form, the projected polyhedron method, and subdivision of the box)
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 4, Section 4.4 (the projected polyhedron algorithm, its steps and its rate of convergence), Sections 4.7 and 4.8 (rounded interval arithmetic) and Section 4.9 (the interval projected polyhedron algorithm and its example with three roots)
---

The interval projected polyhedron method finds all real roots of a system of polynomial equations inside a box. It writes each equation in the Bernstein basis of the box, and uses the convex hull of the control points, projected onto one axis at a time, to cut away parts of the box that hold no root. It splits the box when the cuts do not shrink it enough, and stops on boxes smaller than a tolerance. All arithmetic on the coefficients rounds outward, so no root is lost to rounding.

## In plain words

Think of a search for lost keys in a field. A quick test can say for certain "the keys are not in this strip", but never where they are. So you mark off the strips the test clears, look only at what is left, and, when the test clears nothing, cut the field in two and test each half.

Here the keys are the points where all the equations are zero, and the field is a box. The test looks at a few numbers that describe each equation over the box, the control points. If a whole region is on one side of zero for some equation, it holds no solution.

The method repeats the test on smaller and smaller boxes. Every answer it gives is a tiny box, and every solution is inside one of them. Intervals take care of rounding, so no solution slips away.

## The problem

The input is $m$ polynomials $f_1, \dots, f_m$ in $n$ variables, a box $X_0 = \prod_j [a_j, b_j]$ and a tolerance $\varepsilon > 0$. The output is a list of boxes with sides shorter than $\varepsilon$ that together contain every $x \in X_0$ with $f_1(x) = \dots = f_m(x) = 0$. This is the real, bounded case of [polynomial system solving](/polynomial-system-solving/), and the form in which CAD meets it: intersections, closest points, extrema of curvature and singular points of curves and surfaces become a few polynomial equations in the parameters of patches, and only the roots inside the parameter box matter.

On a box $X$ with local coordinates $u \in [0, 1]^n$, an equation with degree $d_j$ in $x_j$ has the tensor product form

$$f(x) = \sum_I b_I \, B_I(u), \qquad B_I(u) = \prod_{j=1}^{n} B_{i_j, d_j}(u_j),$$

with the [Bernstein polynomials](/bernstein-polynomials/) $B_{i,d}$. The points $(i_1 / d_1, \dots, i_n / d_n, b_I)$ are the *control points*, and they span the *control polyhedron* of the graph of $f$.

## The algorithm

```pseudo id=main
IPP(f₁, …, f_m, X₀, ε)
L1  B_k ← the Bernstein coefficients of f_k on X₀, each rounded outward to a float interval
L2  S ← {(X₀, B)}; out ← ∅
L3  while S ≠ ∅: take (X, B) from S
L4      for each axis j: [s_j, t_j] ← ∩_k the part of the u_j axis inside the convex hull of the control points of B_k projected onto the (u_j, f) plane
L5      if some [s_j, t_j] is empty: discard X and continue
L6      if every side of X is shorter than ε: out ← out ∪ {X} and continue
L7      X, B ← the part of X over ∏_j [s_j, t_j], by de Casteljau subdivision in interval arithmetic
L8      if the side j* that was the widest before line L7 is still longer than half its old width: split X and B in the middle of side j* and put both halves in S
L9      else put (X, B) in S
L10 return out, with boxes that are at most ε apart grouped together
```

Line L4 is the projection. For axis $j$ the control points of $f_k$ project to the points $(i / d_j, b_I)$ of a plane, one column of points for each $i$. With interval coefficients each column becomes the segment from its lowest lower end $m_i$ to its highest upper end $M_i$. The part of the axis $f = 0$ inside the convex hull of these $2(d_j + 1)$ ends is an interval whose ends are among the points with $f = 0$ and the crossings of the segments from a point above the axis to a point below. The code takes the least and the greatest of these, exactly in rational arithmetic, and rounds them outward. This gives the same interval as a [convex hull](/convex-hull/) of the projected points, without building it. An equation that does not depend on $x_j$ gives the whole axis or nothing.

Line L7 restricts the coefficients to the new box with the [de Casteljau algorithm](/de-casteljau-algorithm/) along each axis, in [interval arithmetic](/interval-arithmetic/) where each operation is widened by one float step down and up. The box ends are kept as exact rational numbers, so the coefficients always describe the box they are stored with. Line L8 splits when the box does not shrink well, which happens near several roots or near a root where the hulls are wide.

## Example

Intersect the unit circle $f_1 = x^2 + y^2 - 1$ with the line $f_2 = x - y$ in the box $[\tfrac12, 1]^2$. The one root is $(1/\sqrt2, 1/\sqrt2)$. With $x = \tfrac12 + \tfrac{u}{2}$, the Bernstein coefficients of $x^2$ are $\tfrac14, \tfrac12, 1$, so those of $f_1$ are $b_{ij} = c_i + c_j - 1$ with $c = (\tfrac14, \tfrac12, 1)$:

| | $j = 0$ | $j = 1$ | $j = 2$ |
|---|---|---|---|
| $i = 0$ | $-\tfrac12$ | $-\tfrac14$ | $\tfrac14$ |
| $i = 1$ | $-\tfrac14$ | $0$ | $\tfrac12$ |
| $i = 2$ | $\tfrac14$ | $\tfrac12$ | $1$ |

Projected onto the $u$ axis, the columns are $[-\tfrac12, \tfrac14]$ at $u = 0$, $[-\tfrac14, \tfrac12]$ at $u = \tfrac12$ and $[\tfrac14, 1]$ at $u = 1$. The convex hull meets the axis from $u = 0$, where the first column crosses zero, to the crossing of the segment from $(\tfrac12, -\tfrac14)$ to $(1, \tfrac14)$, at $u = \tfrac34$. The same holds for $v$. The line has coefficients $0, -\tfrac12, \tfrac12, 0$, whose projections cover the whole axis. So line L7 shrinks the box to $[\tfrac12, \tfrac78]^2$, which maps back $u = \tfrac34$ to $x = \tfrac78$.

The side shrank from $\tfrac12$ to $\tfrac38$, which is more than half, so line L8 splits it at $x = \tfrac{11}{16}$. Line L5 later discards the left half $[\tfrac12, \tfrac{11}{16}] \times [\tfrac12, \tfrac78]$, and on the right half the projections of the line now help. In the run of the code, the widest side of the box that holds the root after each of the $12$ steps of line L7 is

$$0.375, \ 0.18, \ 0.040, \ 0.039, \ 0.019, \ 5.3 \cdot 10^{-4}, \ 5.3 \cdot 10^{-4}, \ 2.6 \cdot 10^{-4}, \ 9.9 \cdot 10^{-8}, \ 9.9 \cdot 10^{-8}, \ 4.9 \cdot 10^{-8}, \ 3.4 \cdot 10^{-15},$$

with a split after each step that does not halve the side. The output is one box of side $3.4 \cdot 10^{-15}$ around $(0.70710678118654\ldots, 0.70710678118654\ldots)$, and no other box survives.

## Correctness

The [full proof](proofs/correctness.md) shows that every root in $X_0$ lies in an output box. The key fact is the convex hull property of the Bernstein basis: the $B_I$ are nonnegative on $[0, 1]^n$, sum to $1$, and $\sum_I (i_j / d_j) B_I(u) = u_j$. So at a root with local coordinates $u$,

$$(u_j, 0) = \sum_I B_I(u) \left(\tfrac{i_j}{d_j}, b_I\right)$$

is a convex combination of the projected control points, and lies in their convex hull; see the [convex hull property](/convex-hull-property/). With intervals each point lies on the segment of its column, so it is in the hull of the column ends. A short lemma shows that a point $(\tau, 0)$ in the hull of a finite set lies between the least and the greatest of the zero points and the crossings, and line L4 rounds those outward. So line L5 discards only boxes with no root, and line L7 keeps every root of the box.

The de Casteljau scheme gives the exact coefficients on the parts of a box. In rounded interval arithmetic each computed interval contains the exact value, because with round to nearest the exact result of an operation lies between the two floats next to the computed one. The split parameters are floats and the box ends are exact rationals, so the coefficients always belong to their box. Termination follows because every step that keeps a box at least halves a side of width at least $\varepsilon$, so a path in the tree of boxes has at most $n (1 + \log_2(W / \varepsilon)) + 1$ steps.

What is not proved is the converse. An output box need not contain a root, a root can give several boxes, and the number of groups need not be the number of roots. The tests check, on systems with known simple roots (a circle and a line, products of linear factors with six roots, a sphere and two planes in three variables, five roots of one polynomial, the three close roots of the book example, $30$ random pairs of line pairs), that every root is in a box and that each group holds exactly one root. They also check the projection step alone on $60$ random polynomials, and that the interval subdivision encloses the exact pieces.

## Complexity

One step costs $O(m n N)$ to find the column ranges, $O(m n d^2)$ for the crossings, and $O(m n N d)$ for the de Casteljau restrictions, since each of the $N / (d_j + 1)$ lines along axis $j$ takes $O(d_j^2)$ operations. With $K$ boxes processed the time is $O(K m n N d)$. The stack holds at most two boxes per level of the tree, so the extra space is $O(D m N)$.

By the termination bound the tree has depth at most $D$ and at most $2^{D+1} \le 4 (2W / \varepsilon)^n$ boxes. This worst case is reached in order of magnitude when the roots form a curve or a surface, where the method covers it with boxes of side $\varepsilon$. For isolated simple roots, few boxes are processed in practice. Patrikalakis and Maekawa state that the method converges quadratically in one variable and at best linearly in several. In the example above the sides shrank faster than linearly near the root, but that is one measured input.

The box ends are exact rationals whose size grows with the depth. The float coefficients keep the cost of the heavy steps fixed, and only the ends grow.

## Properties

- **Complete.** No root in the box is lost, also under rounding, as long as no operation overflows.
- **Not certified as existing.** A reported box is a box where the test could not exclude a root. It is not a proof that a root is there.
- **Global in the box.** No start point is needed, unlike Newton's method.
- **Any number of equations.** The test works for $m \ne n$, although a system with a curve of roots gives many boxes.
- **Affine invariant in each axis.** The Bernstein form and the hulls do not change under an affine change of each variable.

## Variants and improvements

- **Plain floats.** The original projected polyhedron method of Sherbrooke and Patrikalakis uses floating point arithmetic. Patrikalakis and Maekawa show an example with roots $0.1$, $0.6$ and $0.7$ where plain floats lose the root $0.7$ and rounded intervals keep it. The tests run the same polynomial and find all three roots.
- **Exact rational arithmetic.** With rational coefficients the same steps can run without rounding. The numbers grow with each subdivision.
- **Bézier clipping.** For one equation in one variable, or two plane curves, the projection step is [Bézier clipping](/bezier-clipping/) of Sederberg and Nishita.
- **Preconditioning.** Mourrain and Pavone (2009) replace the equations by linear combinations of them that are close to the coordinate functions near a root. Then the projections are narrow, and the method cuts much more per step in several variables.
- **Other bases.** Reuter, Mikkelsen, Sherbrooke, Maekawa and Patrikalakis (2008) run the method in the barycentric Bernstein basis of a simplex, for triangular domains.
- **Certification.** After a box is small, an [interval Newton method](/interval-newton-method/) step on it can prove that it holds exactly one root.

## When to use it

Use it when all roots in a parameter box are needed, which is the case for the characteristic points of [surface surface intersection](/surface-surface-intersection/), for [curve surface intersection](/curve-surface-intersection/), and for the stationary points of distance and curvature functions. It is a good choice for small systems of low degree, since the number of coefficients grows like the product of the degrees. For one polynomial in one variable, use [real root isolation](/real-root-isolation/), and for a large system with many complex roots, use [homotopy continuation](/homotopy-continuation/) or algebraic methods.

## Pitfalls

- **Curves of roots.** If the system has a curve or a surface of solutions in the box, the number of boxes grows like a power of $1 / \varepsilon$. Detect this from the count of boxes, and treat the case with a tracing method.
- **Multiple roots.** At a tangent or a multiple root the hulls stay wide, the method splits often, and it returns many boxes near the root. The test with a double root gives $32$ boxes that form one group.
- **Spurious boxes.** A box can survive with no root in it, in particular near a root or a near miss. Group nearby boxes, and verify each group, for example with interval Newton or with the residuals.
- **Rounding of the parameters.** If the box ends are kept in floats and the coefficients are restricted with rounded split parameters, the coefficients belong to a slightly different box, and a root near a box end can be lost. Keep the ends exact, or round them outward and widen the coefficients.
- **Scaling.** The test is affine invariant in each variable but not under a change of the equations. Equations with very different sizes are fine, but equations that are nearly dependent near a root make all projections wide.

## Implementations

## History

Sherbrooke and Patrikalakis (1993) introduced the projected polyhedron method for systems of polynomial equations in the multivariate Bernstein basis. It extends to several variables the convex hull idea of Bézier clipping, which Sederberg and Nishita had used in 1990 for curves. Maekawa and Patrikalakis ran the method in rounded interval arithmetic for robustness, and Patrikalakis and Maekawa's book of 2002 uses it as the general solver for the shape interrogation problems of CAD.

## References
