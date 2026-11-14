---
tag: 8125BY
kind: algorithm
slug: gordon-surface
name: Gordon surface
aliases:
- Gordon-Coons surface
- curve network surface
area: cad/surface-interrogation-and-design
level: core
summary: Builds one surface through a compatible network of curves in two directions, as the sum of the two lofts minus the tensor product interpolant of the crossing points.
model: real-ram
complexity:
  vars: {N: "the total of the numbers of curves and of control points per curve, after the knot merge"}
  time: {worst: O(N^3)}
  space: {extra: Θ(N^2)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1969
  people: [William J. Gordon]
  note: Gordon, at General Motors Research, generalized the Coons patch from four boundary curves to a whole network, with spline blending functions in place of the Coons blends, and later described it as a Boolean sum of commuting projectors.
prereqs: [coons-patch, curve-interpolation, b-spline, boehm-knot-insertion]
see_also: [surface-skinning, coons-patch, transfinite-interpolation-grid, tensor-product-surface, schoenberg-whitney-theorem, twist-compatibility, knot-refinement, n-sided-patch]
sources:
  - paper: "William J. Gordon, Spline-blended surface interpolation through curve networks, Journal of Mathematics and Mechanics 18(10), 931 to 952, 1969"
    title: Gordon 1969
    locator: the surface through a rectangular network of curves as the sum of two spline blended lofts minus the tensor product spline interpolant of the crossing points
  - paper: doi:10.1137/0708019
    title: "William J. Gordon, Blending-function methods of bivariate and multivariate interpolation and approximation, SIAM Journal on Numerical Analysis 8(1), 158 to 177, 1971"
    locator: the Boolean sum P + Q - PQ of commuting projectors, and the statement that it interpolates wherever P or Q does
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 10.5, Interpolation of a Bidirectional Curve Network (p. 485), and Section 9.2.1 (global curve interpolation with averaged knots)
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 22, Coons Patches (Boolean sums of blending projectors)
---

A Gordon surface is a single surface that passes through every curve of a network of curves in two directions: $n + 1$ curves along which $v$ varies and $m + 1$ curves along which $u$ varies, which cross each other in a grid of points. It is the sum of two lofted surfaces, one through each family, minus the tensor product surface through the crossing points. The construction is the [Coons patch](/coons-patch/) with interpolation through many curves in place of the linear blend between two, and Gordon published it in 1969. With B-spline curves and spline interpolation the result is one B-spline surface, which is how CAD systems build it.

## In plain words

A designer draws a grid of curves, like the frames and the long stringers of a ship hull. The task is to find one smooth skin that contains every curve. A first try is to skin only the frames: stretch a surface across them from front to back. This surface holds the frames, but between them it takes its own shape, and it misses the stringers. A second skin across the stringers holds the stringers and misses the frames. Adding the two skins counts the shape twice, so subtract a third skin that only knows the points where the curves cross. On a frame, the second and third skins both see the same crossing points, so they cancel, and what remains is the first skin, which is exactly the frame. The same happens on a stringer. So the sum holds every curve of the grid.

## The problem

**Input.** The *v-curves* $f_0(v), \dots, f_n(v)$, B-spline curves of one degree $q$ with clamped knot vectors on $[v_0, v_m]$, and the *u-curves* $g_0(u), \dots, g_m(u)$, B-spline curves of one degree $p$ on $[u_0, u_n]$. Increasing parameters $u_0 < \dots < u_n$ and $v_0 < \dots < v_m$, with $n \ge p$ and $m \ge q$. The curve $f_i$ is meant to lie on the surface at $u = u_i$, and $g_j$ at $v = v_j$.

**Compatibility.** The network is *compatible* if the curves meet where they should:

$$f_i(v_j) = g_j(u_i) =: p_{ij} \qquad \text{for all } i, j.$$

**Output.** A B-spline surface $S(u, v)$ of degree $(p, q)$ with

$$S(u_i, v) = f_i(v) \ \text{for all } v \text{ and } i, \qquad S(u, v_j) = g_j(u) \ \text{for all } u \text{ and } j.$$

No surface can do this for an incompatible network, since $S(u_i, v_j)$ would have two values. The network must also be rectangular: each u-curve crosses every v-curve once, at the same parameters $u_i$ for all $j$. Curves of one family with different degrees must first be raised to one degree, which does not change them.

## The algorithm

Write $\mathcal{L}_u$ for the operator that interpolates data given at $u_0, \dots, u_n$ by a [B-spline curve](/b-spline/) of degree $p$ with averaged knots, as on the [curve interpolation](/curve-interpolation/) page, and $\mathcal{L}_v$ for the same operator in $v$ with degree $q$. Applied to points that are themselves control points of curves, the operator works entry by entry.

```pseudo id=main
GORDON(f_0..f_n, g_0..g_m, u_0..u_n, v_0..v_m)
L1  refine all f_i to one knot vector V_c by knot insertion; F_i ← the control points of f_i on V_c
L2  refine all g_j to one knot vector U_c by knot insertion; G_j ← the control points of g_j on U_c
L3  p_ij ← f_i(v_j); if p_ij ≠ g_j(u_i) for some i, j then report "incompatible network"
L4  S1 ← ℒ_u(F_0, .., F_n): for each index l, interpolate F_0[l], .., F_n[l] at u_0, .., u_n    ▷ knots U_1 × V_c
L5  S2 ← ℒ_v(G_0, .., G_m): for each index k, interpolate G_0[k], .., G_m[k] at v_0, .., v_m    ▷ knots U_c × V_2
L6  T ← ℒ_v ℒ_u(p_ij): interpolate each column p_0j, .., p_nj in u, then each row of the result in v   ▷ knots U_1 × V_2
L7  U ← U_1 merged with U_c; V ← V_c merged with V_2; refine S1, S2 and T to U × V by knot insertion
L8  return the surface of degree (p, q) on U × V with control net P1 + P2 − P3
```

Lines L1 and L2 put each family on one knot vector, so that the control points of all curves of a family refer to the same basis. Merging takes each knot value with its largest multiplicity in the family. Lines L4 to L6 are three interpolations that share the same two operators: $S1$ and $T$ use the same knots $U_1$ and the same parameters in $u$, and $S2$ and $T$ use the same knots $V_2$ in $v$. This is what makes the terms cancel on the curves. Line L7 changes only the representation of the three surfaces, so that in line L8 their control nets refer to one basis and can be added.

As functions, the three surfaces are

$$S_1 = \sum_{i=0}^{n} \phi_i(u) f_i(v), \qquad S_2 = \sum_{j=0}^{m} \psi_j(v) g_j(u), \qquad T = \sum_{i=0}^{n} \sum_{j=0}^{m} \phi_i(u) \psi_j(v) p_{ij},$$

where $\phi_i$ is the spline on $U_1$ with $\phi_i(u_k) = \delta_{ik}$ and $\psi_j$ is the spline on $V_2$ with $\psi_j(v_l) = \delta_{jl}$. In the language of Gordon 1971, let $\mathcal{P} F(u, v) = \sum_i \phi_i(u) F(u_i, v)$ and $\mathcal{Q} F(u, v) = \sum_j \psi_j(v) F(u, v_j)$ for a surface $F$. These are projectors, and they commute. For any $F$ that contains the network, $S = (\mathcal{P} \oplus \mathcal{Q}) F = (\mathcal{P} + \mathcal{Q} - \mathcal{P}\mathcal{Q}) F$, the Boolean sum, and it uses only the values of $F$ on the network. With $n = m = 1$ and linear $\phi$ and $\psi$ it is the bilinearly blended Coons patch.

## Example

Take three u-curves at $v = 0, \frac12, 1$ and three v-curves at $u = 0, \frac12, 1$, all of degree $2$ ($p = q = 2$), in the height field form $(x, y, z)$. The outer curves are straight lines at height $0$ on the edges of the unit square, Bezier curves with knots $(0, 0, 0, 1, 1, 1)$. The two middle curves are the same leaning bump $h$: a quadratic B-spline on the knots $H = (0, 0, 0, \frac12, 1, 1, 1)$ with heights $0, 2, 0, 0$, so $h(0) = h(1) = 0$, $h(\frac18) = \frac{13}{16}$, $h(\frac14) = \frac54$ and $h(\frac12) = 1$. The middle u-curve is $g_1(u) = (u, \frac12, h(u))$ and the middle v-curve is $f_1(v) = (\frac12, v, h(v))$. They cross at the centre at height $h(\frac12) = 1$, and all other crossings are at height $0$, so the network is compatible.

- **L1, L2.** The merged knot vector of each family is $H$. The outer lines get four control points by the insertion of the knot $\frac12$.
- **L4.** Three curves at $u = 0, \frac12, 1$ with degree $2$ give the averaged knots $U_1 = (0, 0, 0, 1, 1, 1)$, so $\phi_1(u) = 4u(1 - u)$ is the quadratic Lagrange polynomial and $S_1 = (u, v, 4u(1 - u) h(v))$.
- **L5, L6.** In the same way $S_2$ has height $4v(1 - v) h(u)$, and $T$ has height $16 u v (1 - u)(1 - v)$, since the only non zero crossing height is $p_{11} = 1$.
- **L7, L8.** $U = V = H$, and the $4 \times 4$ control net of the result has the $x$ and $y$ coordinates $0, \frac14, \frac34, 1$ and the heights

$$\begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 3 & 1 & 0 \\ 0 & 1 & -1 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix},$$

In the inner $2 \times 2$ block the refined nets of $S_1$, $S_2$ and $T$ have the heights $\begin{pmatrix} 2 & 0 \\ 2 & 0 \end{pmatrix}$, $\begin{pmatrix} 2 & 2 \\ 0 & 0 \end{pmatrix}$ and $\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$, so for example $3 = 2 + 2 - 1$.

The heights of the three parts at two points show how the terms cancel:

| point $(u, v)$ | $S_1$ | $S_2$ | $T$ | $S = S_1 + S_2 - T$ | target |
|---|---|---|---|---|---|
| $(\frac14, \frac12)$, on $g_1$ | $\frac34$ | $\frac54$ | $\frac34$ | $\frac54$ | $h(\frac14) = \frac54$ |
| $(\frac14, \frac14)$, off the network | $\frac{15}{16}$ | $\frac{15}{16}$ | $\frac{9}{16}$ | $\frac{21}{16}$ | none |

On the u-curve $g_1$ the loft $S_1$ alone gives $\frac34$, the height of the quadratic through the three crossing points, and misses the curve. There $S_2 - T$ adds the missing $\frac12$.

## Correctness

The proof has two parts. First, each interpolation of lines L4 to L6 is well defined, and $S_1$, $S_2$ and $T$ are the functions displayed above: the collocation matrix of averaged knots is nonsingular by the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/), and interpolation is linear in the data, so interpolating control points entry by entry interpolates the curves. Second, on the line $u = u_k$, $S_1 = f_k$ because $\phi_i(u_k) = \delta_{ik}$, while $S_2(u_k, v) = \sum_j \psi_j(v) g_j(u_k) = \sum_j \psi_j(v) p_{kj} = T(u_k, v)$ by compatibility, so $S(u_k, v) = f_k(v)$. The line $v = v_l$ is symmetric. Knot insertion in lines L1, L2 and L7 never changes a curve or a surface, so the sum of the refined nets is the sum of the surfaces. The full proof, with the operator form $I - \mathcal{P} \oplus \mathcal{Q} = (I - \mathcal{P})(I - \mathcal{Q})$, is in the proof file.

## Complexity

Let $N$ be the total size: the numbers of curves $n + 1$ and $m + 1$ and the numbers of control points of a curve after lines L1 and L2. Each interpolation solves one $(n + 1) \times (n + 1)$ or $(m + 1) \times (m + 1)$ system with many right sides, one for each control point of a curve. The implementation uses dense [Gaussian elimination](/gaussian-elimination/), which costs $\Theta(n^3 + n^2 N)$ for $S_1$, and the same with $m$ for $S_2$ and $T$. Line L7 inserts $O(N)$ knots into nets of $O(N^2)$ points. Each insertion changes $p$ or $q$ points in each of $O(N)$ rows or columns, but the implementation copies the whole row, so line L7 costs $O(N^3)$. The total is $O(N^3)$. The collocation matrices are [banded](/banded-matrix/), with at most $p$ or $q$ non zero entries beside the diagonal in each row, so a banded solver and an insertion in place bring the cost down to $\Theta(N^2)$ for fixed degrees, which is the size of the output. The extra space is the three nets, $\Theta(N^2)$.

## Properties

- **Exact on the network.** For a compatible network the surface contains every curve exactly, not within a tolerance, and the implementation checks this in exact rational arithmetic.
- **Linear.** The surface depends linearly on the curves, so moving one curve moves the surface by a fixed blend of that change.
- **Not local.** Spline interpolation is global: the cardinal splines $\phi_i$ are non zero, though decaying, far from $u_i$. Changing one curve changes the surface everywhere, mostly near the curve.
- **Affine invariant.** The construction commutes with affine maps of space, because it only takes affine combinations of points: $\sum_i \phi_i = 1$, and $1 + 1 - 1 = 1$ in the Boolean sum.
- **Reproduces a surface of its own space.** If the network is cut from a surface $F$ whose sections $u \mapsto F(u, v)$ are all splines on $U_1$, then $\mathcal{P} F = F$ and $S = F + \mathcal{Q} F - \mathcal{Q} \mathcal{P} F = F$. The same holds with $v$ and $V_2$.

## Variants and improvements

- **Polynomial Gordon surfaces.** With Lagrange interpolation in place of splines, as in the example, $\phi_i$ and $\psi_j$ are Lagrange polynomials. This is fine for three or four curves per family and oscillates for many.
- **Gordon-Coons surfaces with derivatives.** Hermite projectors that also interpolate cross derivatives along the curves give $G^1$ or $C^1$ joins to other surfaces. They need consistent twists at the crossing points, see [twist compatibility](/twist-compatibility/).
- **Unequal crossing parameters.** In practice the u-curves cross the v-curves at different parameters. Piegl and Tiller reparametrize the curves first so that all crossings of a family happen at common parameters.
- **Transfinite interpolation grids.** The same Boolean sum with linear or spline blends maps a square to a curved domain in [structured grid generation](/transfinite-interpolation-grid/).
- **Rational curves.** The construction runs on homogeneous control points. It interpolates the curves only if the network is compatible in homogeneous form, that is, if the weights also agree at the crossings.
- **Irregular networks.** A network with triangles or n-gons among its cells needs [n-sided patches](/n-sided-patch/), not a single tensor product surface.

## When to use it

Use a Gordon surface when the shape is given by section curves in two directions that cross in a regular grid, as for hulls, fuselages, car bodies and turbine blades, and the surface must contain all of them exactly. If only one family of sections is given, use [skinning](/surface-skinning/). If only four boundary curves are given, the Coons patch is enough. If the curves are measured and contain noise, an exact interpolant follows the noise, and an approximating surface fitted by least squares is better.

## Pitfalls

- **Incompatible networks.** Curves that are drawn separately rarely meet exactly. A small mismatch makes the problem impossible, so the program must either move the curves until they meet, or work to a tolerance and accept that the surface misses the curves by about the size of the mismatch.
- **Knot growth.** The merged knot vectors hold every knot of every curve and of the interpolation, so a network of curves with unrelated knots gives a surface with many control points.
- **Wiggles from the parameters.** The shape between the curves depends on the parameters $u_i$ and $v_j$. Parameters that do not follow the spacing of the curves give bulges and waves, as in all interpolation.
- **Shape between curves is not designed.** The surface interpolates the curves, but nothing controls its fairness between them. Check it with [reflection lines](/reflection-lines/) or curvature plots.
- **Degrees.** The implementation needs one degree per family and at least $p + 1$ v-curves and $q + 1$ u-curves. With fewer curves, use a lower interpolation degree and raise the degrees of the parts before line L7.

## Implementations

The Python file in this folder has `gordon_surface(u_curves, v_curves, us, vs)`, which returns the surface as knot vectors, degrees and a control net, and `gordon_parts`, which returns the three surfaces $S_1$, $S_2$ and $T$. The shared helper `si3spline.py` holds the basis functions, the evaluation, Boehm knot insertion, the knot merge and global interpolation with an exact Gauss-Jordan solver. With integer or Fraction input everything is exact. The tests check the worked example, and on random compatible networks whose curves have different knot vectors they check that each iso-curve of the result at $u_i$ or $v_j$ has exactly the control points of the input curve refined to the same knots. They also check that the sum of the nets equals the Boolean sum of the three parts at random points, that one loft alone misses the other family, and that incompatible networks and too few curves are rejected.

## History

Coons described his patches at MIT in the 1960s, and Gordon, at General Motors Research, extended the idea in 1969 from four boundary curves to a whole network of curves, blended with splines. In 1971 he put the patches of Coons and his own surfaces into one theory of blending function methods, in which the surfaces are Boolean sums of commuting projectors. Piegl and Tiller give the B-spline form used here, with compatible knot vectors and the sum of control nets.

## References
