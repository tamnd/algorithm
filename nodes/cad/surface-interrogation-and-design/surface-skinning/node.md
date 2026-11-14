---
tag: 5J15FM
kind: algorithm
slug: surface-skinning
name: Surface skinning
aliases:
- lofting
- lofted surface
area: cad/surface-interrogation-and-design
level: core
summary: Builds a B-spline surface through an ordered set of section curves, after making them compatible in degree and knot vector, by interpolating across them.
model: real-ram
complexity:
  vars: {K: "the number of sections minus one", n: "the number of control points of a section after the knot merge, minus one"}
  time: {worst: O(K^3 + K^2 n + K n^2)}
  space: {extra: Θ(K n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Charles D. Woodward]
  note: Skinning through drawn sections was already a common CAD tool. Woodward described B-spline skinning with compatible sections and interpolation across them, and added curves that control the shape in the long direction.
prereqs: [curve-interpolation, b-spline, boehm-knot-insertion, knot-vector]
see_also: [gordon-surface, ruled-surface, sweep-surface, coons-patch, tensor-product-surface, schoenberg-whitney-theorem, knot-refinement, curve-interpolation]
sources:
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 10.3, Skinned Surfaces (p. 457), and Section 9.2.1 (global curve interpolation with averaged knots)
  - paper: doi:10.1016/0010-4485(88)90002-4
    title: "Charles D. Woodward, Skinning techniques for interactive B-spline surface interpolation, Computer-Aided Design 20(8), 441 to 451, 1988"
    locator: skinning of B-spline sections, and projection curves for shape control in the long direction
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapters on tensor product B-spline surfaces and on surface interpolation
---

Skinning, also called lofting, builds one surface through an ordered list of section curves $C_0(u), \dots, C_K(u)$. The surface $S(u, v)$ contains each section as an iso-curve: $S(u, v_k) = C_k(u)$ for chosen parameters $v_0 < \dots < v_K$. With B-spline sections the method has three steps. It makes the sections compatible, so that all have the same degree and the same knot vector. It chooses the parameters $v_k$. Then it interpolates each column of control points across the sections with a [B-spline curve](/b-spline/) in $v$. The result is one tensor product B-spline surface, and the proof that it holds every section is one line once the sections share a knot vector.

## In plain words

Think of the frames of a boat, cut from wood and set up in a row. A thin sheet bent over all the frames gives the hull. Skinning does this with curves. Each frame is a curve with its own control points. First the method gives every frame the same number of control points, in the same arrangement, without changing its shape. Now the first control points of all frames form a row from the bow to the stern, and so do the second ones, and so on. The method draws a smooth curve through each such row. These curves together are the control points of a surface, and that surface passes through every frame. Between the frames the surface takes the shape of the smooth rows.

## The problem

**Input.** Section curves $C_0, \dots, C_K$, $K \ge 1$, each a clamped B-spline curve of one degree $p$ on the same parameter interval, with its own knot vector. A degree $q$ in $v$. Optionally, parameters $v_0 < \dots < v_K$.

**Output.** A B-spline surface $S(u, v)$ of degree $(p, \min(q, K))$ with $S(u, v_k) = C_k(u)$ for every $k$ and every $u$.

Sections of different degrees must first be raised to the highest degree, which does not change them. Sections on different parameter intervals must first be reparametrized to one interval.

## The algorithm

```pseudo id=main
SKIN(C_0..C_K, q, v_0..v_K optional)
L1  U ← the merge of the knot vectors of all C_k; refine each C_k to U by knot insertion; P_k ← its control points P_{k,0}, .., P_{k,n}
L2  if no parameters are given: for each column i, take the chord length parameters of P_{0,i}, .., P_{K,i}; v_k ← their average over the columns
L3  q ← min(q, K); V ← the averaged knots of degree q for v_0, .., v_K; for each column i, solve for Q_{i,0}, .., Q_{i,K} with Σ_l M_l(v_k) Q_{i,l} = P_{k,i} for all k
L4  the control net of the surface is Q_{i,l}, with i along u and l along v
L5  return the surface of degree (p, q) on U × V with the net Q
```

Line L1 is the key step. The merged knot vector $U$ takes each knot value with its largest multiplicity in any section, and [knot insertion](/boehm-knot-insertion/) puts every section on $U$ without changing its shape. After that, all sections are combinations of the same basis functions $N_0(u), \dots, N_n(u)$: $C_k(u) = \sum_i N_i(u) P_{k,i}$. Line L2 is the parameter choice of Piegl and Tiller: for each column of control points it takes the chord length parameters, which divide $[0, 1]$ in proportion to the distances between consecutive points, and it averages them over the columns. A column whose points all coincide, such as a pole, carries no information and is skipped. Line L3 is [global curve interpolation](/curve-interpolation/) with the averaged knots $t_{j+q} = (v_j + \dots + v_{j+q-1})/q$, done once for each column. All columns share the same matrix $A_{kl} = M_l(v_k)$, so one elimination serves all of them.

## Example

Take three quadratic sections ($p = 2$) in space, in planes $y = 0, 1, 2$. The section $C_0$ is the straight line from $(0, 0, 0)$ to $(2, 0, 0)$ with control points $(0, 0, 0), (1, 0, 0), (2, 0, 0)$ on the knots $(0, 0, 0, 1, 1, 1)$. The section $C_2$ is the line from $(0, 2, 1)$ to $(2, 2, 1)$, built in the same way. The middle section $C_1$ is a bump on the knots $H = (0, 0, 0, \frac12, 1, 1, 1)$ with control points $(0, 1, 0), (\frac12, 1, 2), (\frac32, 1, 0), (2, 1, 0)$, so $C_1(\frac14) = (\frac12, 1, \frac54)$. Use $q = 2$ and the given parameters $v = 0, \frac12, 1$.

- **L1.** The merged knot vector is $U = H$. Inserting $\frac12$ into $C_0$ gives $(0, 0, 0), (\frac12, 0, 0), (\frac32, 0, 0), (2, 0, 0)$, and the same for $C_2$ at $y = 2$, $z = 1$.
- **L3.** Three parameters and $q = 2$ give $V = (0, 0, 0, 1, 1, 1)$, so each column is interpolated by a quadratic Bezier curve. For the column $i = 1$ the points are $(\frac12, 0, 0)$, $(\frac12, 1, 2)$, $(\frac12, 2, 1)$. The quadratic with these values at $0, \frac12, 1$ has the middle control point $2 \cdot (\frac12, 1, 2) - \frac12 \bigl((\frac12, 0, 0) + (\frac12, 2, 1)\bigr) = (\frac12, 1, \frac72)$.
- **L4.** The middle row of the net is $(0, 1, -\frac12)$, $(\frac12, 1, \frac72)$, $(\frac32, 1, -\frac12)$, $(2, 1, -\frac12)$. The outer rows are the refined control points of $C_0$ and $C_2$.

The surface passes through all three sections. For example $S(\frac14, \frac12) = (\frac12, 1, \frac54) = C_1(\frac14)$. Between the sections it follows the quadratics in $v$: $S(\frac14, \frac14) = (\frac12, \frac12, \frac{13}{16})$, above the straight line $z = \frac14$ that a ruled surface between $C_0$ and $C_1$ would give. The middle row of the net lies off the middle section, at height $\frac72$ over a bump of height $2$, because a quadratic through three points overshoots its middle value.

With the default parameters of line L2, three columns have the distances $1$ and $\sqrt2$, and the column $i = 1$ has $\sqrt5$ and $\sqrt2$. The average of the four ratios is

$$v_1 = \frac14 \Bigl(\frac{3}{1 + \sqrt2} + \frac{\sqrt5}{\sqrt5 + \sqrt2}\Bigr) \approx 0.4638.$$

## Correctness

After line L1 every section is $C_k(u) = \sum_{i=0}^{n} N_i(u) P_{k,i}$ with the same basis $N_i$ on $U$, because knot insertion does not change a curve. The matrix $A_{kl} = M_l(v_k)$ of line L3 is nonsingular by the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/), since each averaged inner knot lies strictly between the parameters around it. So line L3 finds $Q$ with $\sum_l M_l(v_k) Q_{i,l} = P_{k,i}$. Then

$$S(u, v_k) = \sum_i N_i(u) \sum_l M_l(v_k) Q_{i,l} = \sum_i N_i(u) P_{k,i} = C_k(u).$$

The common knot vector is what makes the second equality an identity of curves and not only of points. Without line L1 the sections would have control points on different bases, and the rows of control points would not mean anything. The full proof is in the proof file.

## Complexity

Let $K + 1$ be the number of sections and $n + 1$ the number of control points of a section after line L1. Line L1 inserts at most $n$ knots into each section. The implementation copies the control polygon at each insertion, which costs $O(K n^2)$ in total, and an insertion in place costs $O(K n p)$. Line L2 computes $(K + 1)(n + 1)$ distances. Line L3 solves one $(K + 1) \times (K + 1)$ system with $n + 1$ right sides by dense Gauss-Jordan elimination, in $O(K^3 + K^2 n)$ operations. The total is $O(K^3 + K^2 n + K n^2)$. The matrix of line L3 is [banded](/banded-matrix/), with at most $q$ non zero entries beside the diagonal in each row, so a banded solver and insertion in place give $\Theta(K n)$ for fixed degrees, which is the size of the output. The extra space is the net, $\Theta(K n)$.

## Properties

- **Exact on the sections.** Each section is an iso-curve of the surface exactly, not within a tolerance. With rational input and given parameters the implementation is exact.
- **Linear in the sections.** For fixed parameters, the net depends linearly on the control points of the sections.
- **Global in $v$.** Interpolation by splines is global, so changing one section changes the surface between all sections, mostly near the changed one.
- **Affine invariant.** The construction uses affine combinations only, so it commutes with affine maps of space. The chord length parameters are also invariant under rigid motions and uniform scaling.
- **Two sections give a ruled surface.** With $K = 1$ the degree in $v$ is $1$ and the surface is the [ruled surface](/ruled-surface/) $(1 - v) C_0(u) + v C_1(u)$.
- **Shape between sections depends on the parameters.** The parameters $v_k$ and the knots $V$ fix the shape across the sections. Neither is part of the data.

## Variants and improvements

- **Rational sections.** For NURBS sections the method runs on the homogeneous control points. The result is a NURBS surface, but the weights of the sections must agree in a way that keeps the interpolated weights positive.
- **Approximate skinning.** Sections with many unrelated knots give a merged knot vector with many knots. Piegl and Tiller also give a method that approximates the sections within a tolerance on fewer knots.
- **Skinning with spine or guide curves.** Woodward places planar sections along a spine curve and adds curves in the long direction to control the shape between sections. A network of curves in both directions leads to the [Gordon surface](/gordon-surface/).
- **Lofting with end conditions.** Hermite conditions at the first and last section, such as given cross tangents, let the surface join other surfaces with tangent plane continuity.
- **Sweeps.** A [sweep surface](/sweep-surface/) moves one section along a path, and many sweeps are built by skinning copies of the section placed along the path.

## When to use it

Use skinning when a shape is given by a row of cross sections, as for hulls, fuselages, wings, bottles, ducts and blades, and the surface must contain them exactly. If curves are also given in the other direction, use a [Gordon surface](/gordon-surface/). If only two sections are given, a ruled surface is the same thing. If the sections come from measured data, an interpolant follows the noise, and a fitted surface is better.

## Pitfalls

- **Incompatible sections.** The sections must have one degree, one parameter interval and the same direction. A section drawn in the reverse direction or with a different start point on a closed curve gives a twisted surface. The program must check this, since the mathematics accepts it.
- **Knot growth.** The merged knot vector holds every knot of every section, so sections with unrelated knots give many control points.
- **Bad parameters.** Equal spacing of the $v_k$ when the sections are unequally spaced gives bulges. Chord length averages help, but sections with very different sizes can still give waves.
- **Overshoot.** Like all interpolation, the surface can overshoot between sections. In the example the middle row of the net is at height $\frac72$ over a bump of height $2$. Check the result with [reflection lines](/reflection-lines/).
- **Coincident sections.** Two equal consecutive sections give equal chord length parameters, and the interpolation has no solution. The implementation rejects this.

## Implementations

The Python file in this folder has `surface_skinning(sections, q, vs)`, which returns the knot vectors, the degrees and the control net, and `chord_parameters`, which computes the default parameters of line L2. The shared helper `si3spline.py` holds the basis functions, the evaluation, Boehm knot insertion, the knot merge and global interpolation with an exact Gauss-Jordan solver. The default parameters use floating point square roots and are then turned into exact fractions, so the rest of the computation is exact. The tests check the worked example and the default parameter $v_1$ of the example. On random sections with different knot vectors, both with given and with default parameters, they check that the iso-curve of the result at each $v_k$ has exactly the control points of the section refined to $U$, and that the surface and the section agree at a random point. They also check that two sections give the ruled surface and that coincident sections, mixed degrees and a single section are rejected.

## History

Lofting is older than computers. In shipyards and aircraft plants, full size sections were drawn on the floor of the mould loft and faired by hand with long flexible battens, the original splines. In CAD, skinning through drawn sections became a common tool for surface design in the 1980s. Woodward described B-spline skinning in 1988, with spine and projection curves for shape control. Piegl and Tiller give the form used here, with the merged knot vector and parameters averaged over the columns.

## References
