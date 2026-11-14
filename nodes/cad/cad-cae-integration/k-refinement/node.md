---
tag: H90MTM
kind: technique
slug: k-refinement
name: k-refinement
aliases:
- order elevation before knot insertion
area: cad/cad-cae-integration
level: advanced
summary: Raise the degree of a B-spline space first and insert the new knots after, so each new knot has smoothness C^(p-1) and the space has fewer functions than with the other order.
prereqs: [bernstein-polynomials, knot-vector, b-spline, curry-schoenberg-theorem, boehm-knot-insertion]
see_also: [isogeometric-analysis, knot-refinement, oslo-algorithm, bezier-extraction, nurbs-approximation-estimates, parametric-continuity, nurbs, finite-element-method]
sources:
  - paper: doi:10.1016/j.cma.2004.10.008
    title: "T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis: CAD, finite elements, NURBS, exact geometry and mesh refinement, Computer Methods in Applied Mechanics and Engineering 194(39-41), 2005, 4135 to 4195"
    locator: the part on refinement of NURBS, where h-, p- and k-refinement are defined and compared
  - paper: doi:10.1016/j.cma.2007.04.007
    title: J. A. Cottrell, T. J. R. Hughes and A. Reali, Studies of refinement and continuity in isogeometric structural analysis, Computer Methods in Applied Mechanics and Engineering 196(41-44), 2007, 4160 to 4183
    locator: the whole paper, numerical comparison of p- and k-refinement and of the continuity at element boundaries
  - book: isbn:9780470748732
    title: J. A. Cottrell, T. J. R. Hughes and Y. Bazilevs, Isogeometric Analysis, Toward Integration of CAD and FEA, Wiley, 2009
    locator: Chapter 2 (NURBS as a pre-analysis tool, p. 19), the part on refinement
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, 2nd edition, Springer, 1997
    locator: Chapter 5 (knot insertion, knot refinement, knot removal and degree elevation)
  - paper: doi:10.1016/0167-8396(84)90031-1
    title: Hartmut Prautzsch, Degree elevation of B-spline curves, Computer Aided Geometric Design 1(2), 1984, 193 to 198
    locator: the whole paper, a degree elevation algorithm for B-spline curves
  - paper: doi:10.1145/282957.282962
    title: Elaine Cohen, Tom Lyche and Larry L. Schumaker, Algorithms for degree-raising of splines, ACM Transactions on Graphics 4(3), 1985, 171 to 181
    locator: the whole paper, formulas for the raised coefficients
  - paper: doi:10.1016/0010-4485(94)90004-3
    title: Les Piegl and Wayne Tiller, Software-engineering approach to degree elevation of B-spline curves, Computer-Aided Design 26(1), 1994, 17 to 28
    locator: the whole paper, elevation by Bezier decomposition, Bezier degree raising and knot removal
  - paper: doi:10.1016/j.cma.2005.09.027
    title: J. A. Cottrell, A. Reali, Y. Bazilevs and T. J. R. Hughes, Isogeometric analysis of structural vibrations, Computer Methods in Applied Mechanics and Engineering 195(41-43), 2006, 5257 to 5296
    locator: the spectra of k-refined and p-refined discretizations
  - paper: doi:10.1007/s00211-010-0338-z
    title: L. Beirão da Veiga, A. Buffa, J. Rivas and G. Sangalli, Some estimates for h-p-k-refinement in isogeometric analysis, Numerische Mathematik 118(2), 2011, 271 to 305
    locator: the whole paper, error bounds that are explicit in the degree and the smoothness
---

k-refinement is a way to make the spline space of [isogeometric analysis](/isogeometric-analysis/) larger. You raise the degree of the [B-spline](/b-spline/) basis first, and you insert the new knots after that. Each new knot then has multiplicity one in a basis of the new degree, so the functions are $C^{p-1}$ there, where $p$ is the new degree. Raising the degree after the knot insertion gives a different space: it is larger, and it is only as smooth at the new knots as the old degree allowed. Hughes, Cottrell and Bazilevs named the technique in 2005, and Cottrell, Hughes and Reali studied it against classical p-refinement in 2007. The geometry never changes. Both steps write the same curve in a larger space, so the refined model is exactly the CAD model.

The notation is the one of the [B-spline](/b-spline/) page. A curve of degree $p$ is $C(u) = \sum_{i=0}^{n} N_{i,p}(u) P_i$ on a clamped [knot vector](/knot-vector/) $t_0 \le \cdots \le t_{n+p+1}$, where the first and the last value have multiplicity $p + 1$. Let the distinct interior values be $\xi_1 < \cdots < \xi_l$ with multiplicities $m_1, \ldots, m_l \le p$. The curve is $C^{p - m_j}$ at $\xi_j$, and the $l + 1$ intervals between distinct values are the *elements*. $S_p(t)$ is the span of the $N_{i,p}$, of dimension $n + 1 = p + 1 + \sum_j m_j$ by the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/). The same holds for each coordinate of a NURBS curve in homogeneous form, so everything below applies to [NURBS](/nurbs/) through the weighted control points.

## In plain words

A spline is made of polynomial pieces glued together smoothly. You can make the space of such splines richer in two ways: cut the pieces into shorter pieces, or allow polynomials of higher degree. If you cut first and then raise the degree, the new cuts keep the weak glue of the old degree, and each cut costs extra unknowns. If you raise the degree first and then cut, each new cut gets the strongest glue the new degree allows, and it costs only one unknown. The second order is k-refinement. It gives smoother functions with fewer unknowns, which is what a smooth solution of a physics problem wants. In both orders the shape you started from stays exactly the same.

## When it applies

- The discretization uses a B-spline or NURBS basis, as in [isogeometric analysis](/isogeometric-analysis/), the [Galerkin method](/galerkin-method/) or the [collocation method](/collocation-method/) with splines. Lagrange finite elements have no smoothness to raise, so for them the two orders give the same space.
- You need both a higher degree and a finer mesh than the CAD model has. The CAD model fixes the coarsest mesh, the degree and the geometry. k-refinement adds functions without changing that geometry.
- The solution is smooth, or the equation needs smooth functions, for example a fourth order problem such as a Kirchhoff-Love plate or shell (see [isogeometric Kirchhoff-Love shells](/isogeometric-kirchhoff-love-shell/)), where $C^1$ functions are needed for a conforming Galerkin method.
- It does not apply when you want the low smoothness, for example at a material interface or a kink of the solution. There you keep or raise the multiplicity of the knot on purpose.

## The template

*Degree elevation* of a curve of degree $p$ on $t$ writes the same curve with degree $p + 1$ on the knot vector $t^+$ that has each distinct value of $t$ once more: $\xi_j$ gets multiplicity $m_j + 1$ and the two ends get $p + 2$. The smoothness at $\xi_j$ stays $(p + 1) - (m_j + 1) = p - m_j$. *Knot insertion* adds one knot and keeps the degree, with [Boehm's algorithm](/boehm-knot-insertion/). The template below does $r$ elevations and then inserts the new knots $X$, each once.

```pseudo id=main
K-REFINE(t, p, P, r, X)             ▷ raise the degree by r, then insert the knots X
L1  repeat r times: (t, P) ← ELEVATE(t, p, P) and p ← p + 1
L2  for each x in X: (t, P) ← INSERT(t, p, P, x)     ▷ Boehm, x gets multiplicity 1
L3  return (t, p, P)

ELEVATE(t, p, P)                    ▷ degree elevation by decomposition and removal
L4  insert each interior value ξ_j until it has multiplicity p     ▷ Bezier pieces Q
L5  raise each Bezier piece: R_0 = Q_0, R_i = (i/(p+1)) Q_{i-1} + (1 - i/(p+1)) Q_i, R_{p+1} = Q_p
L6  t⁺ ← t with each distinct value one more time
L7  solve A P⁺ = R exactly, where A is the knot insertion matrix from t⁺ to the Bezier knot vector
L8  return (t⁺, P⁺)
```

Line L4 is knot insertion, so the curve does not change. After it, the control points of the element $[\xi_j, \xi_{j+1}]$ are the Bezier points of that piece ([Bernstein polynomials](/bernstein-polynomials/), with the parameter mapped to $[0, 1]$). Line L5 is the degree elevation identity $B_i^p = \frac{p + 1 - i}{p + 1} B_i^{p+1} + \frac{i + 1}{p + 1} B_{i+1}^{p+1}$ of the Bernstein page, item 10, collected by coefficient of $B_i^{p+1}$. Line L7 is *knot removal*: the curve is now in Bezier form of degree $p + 1$, where each interior value has multiplicity $p + 1$, and L7 finds its coefficients on the smaller knot vector $t^+$. The textbook route of Piegl and Tiller (1994) does L7 with a local removal formula. Here it is an exact linear solve, which is the same result because the solution is unique.

**Why knot insertion keeps the curve.** Let $\hat t$ be $t$ with one more knot. A function of $S_p(t)$ is a piecewise polynomial of degree $p$ with the breaks of $t$ and the smoothness $C^{p - m_j}$ at each $\xi_j$. With respect to $\hat t$ it has the same pieces, one more break where it is $C^\infty$, and at the knot that got one more copy it needs only one less order of smoothness than it has. So $S_p(t) \subseteq S_p(\hat t)$. By the Curry-Schoenberg theorem the B-splines on $\hat t$ are a basis of $S_p(\hat t)$, so $C$ has exactly one set of coefficients $\hat P$ on $\hat t$, and Boehm's formulas compute them (the proof of the formulas is on the [Boehm page](/boehm-knot-insertion/)). The curve, as a function of $u$, is the same.

**Why degree elevation keeps the curve.** A polynomial of degree at most $p$ is a polynomial of degree at most $p + 1$. At $\xi_j$, a function of $S_p(t)$ has continuous derivatives of the orders $0, \ldots, p - m_j$, and $S_{p+1}(t^+)$ asks for the orders $0, \ldots, (p + 1) - (m_j + 1) = p - m_j$, the same orders. So $S_p(t) \subseteq S_{p+1}(t^+)$, and by the Curry-Schoenberg theorem $C$ has exactly one coefficient vector $P^+$ on $t^+$. The algorithm finds it. After L5, $C = \sum_i N_{i,p+1}^{bez}(u) R_i$ on the Bezier knot vector $t^{bez}$, by Boehm and the Bernstein identity. Since $t^+ \subseteq t^{bez}$, insertion of the missing knots maps the coefficients $P^+$ to the coefficients of $C$ on $t^{bez}$, that is $A P^+ = R$, because the coefficients on $t^{bez}$ are unique. If $A Q = 0$ then the curve $\sum N_{i,p+1} Q_i$ on $t^+$ is zero, so $Q = 0$ by linear independence. So $A$ has full column rank, and the solution of L7 is $P^+$ and nothing else.

**Why the order matters.** Start from $S_p(t)$ with $l$ interior values and $l + 1$ elements. Raise the degree by $r$ and add $s$ new distinct values. Count with the Curry-Schoenberg formula $\dim = (\text{degree}) + 1 + \sum (\text{interior multiplicities})$.

- k-refinement: the degree is $p + r$, the old values have multiplicity $m_j + r$ and the new values multiplicity $1$. The dimension is $p + r + 1 + \sum_j (m_j + r) + s = \dim S_p(t) + r(l + 1) + s$. The functions are $C^{p+r-1}$ at the new values.
- Insert, then elevate: the new values get multiplicity $1$ at degree $p$ and then $1 + r$ at degree $p + r$. The dimension is $\dim S_p(t) + s + r(l + 1 + s)$, larger by $r s$. The functions are only $C^{(p+r) - (r+1)} = C^{p-1}$ at the new values.

Both have the same degree and the same breaks, and the second knot vector contains the first, so the k-refined space is a subspace of the other one, a strict subspace when $r \ge 1$ and $s \ge 1$. Neither changes the curve, since both are chains of insertions and elevations.

## Classic examples

**The smallest case.** Start with degree $p = 1$ on one element, $t = (0, 0, 1, 1)$, two functions. The goal is degree 2 with the new knot $1/2$.

| order | knot vector | dimension | smoothness at $1/2$ |
|---|---|---|---|
| elevate, then insert (k) | $(0, 0, 0, \tfrac12, 1, 1, 1)$ | 4 | $C^1$ |
| insert, then elevate | $(0, 0, 0, \tfrac12, \tfrac12, 1, 1, 1)$ | 5 | $C^0$ |

With the formulas above, $\dim S_1 = 2$, $l = 0$, $r = 1$, $s = 1$: $2 + 1 + 1 = 4$ and $4 + 1 = 5$. The extra function of the second space is the one that allows a kink at $1/2$. The space with $C^{p-1}$ at the new knot, here $C^1$, is the k-refined one.

**Many elements.** Start from the same linear element and go to degree $q$ with $n_{el}$ equal elements, so $r = q - 1$ and $s = n_{el} - 1$. k-refinement gives $n_{el} + q$ functions, which are $C^{q-1}$ everywhere. Inserting first gives $q\, n_{el} + 1$ functions, $C^0$ at the element boundaries, the same space as Lagrange finite elements of degree $q$. For $q = 3$ and $n_{el} = 8$ that is 11 against 25 functions. For a tensor product in $d$ dimensions the counts are $(n_{el} + q)^d$ against $(q\, n_{el} + 1)^d$, so 1331 against 15625 for $d = 3$.

**A curve.** Take the quadratic Bezier curve with control points $(0, 0)$, $(2, 4)$, $(4, 0)$ on $t = (0, 0, 0, 1, 1, 1)$.

- Elevation gives $t^+ = (0, 0, 0, 0, 1, 1, 1, 1)$ and the points $(0, 0)$, $(4/3, 8/3)$, $(8/3, 8/3)$, $(4, 0)$, the classical Bezier degree raising.
- Inserting $1/2$ after that (k-refinement) gives $(0, 0, 0, 0, \tfrac12, 1, 1, 1, 1)$ and five points $(0, 0)$, $(2/3, 4/3)$, $(2, 8/3)$, $(10/3, 4/3)$, $(4, 0)$.
- The other order first gives $(0, 0, 0, \tfrac12, 1, 1, 1)$ with $(0, 0)$, $(1, 2)$, $(3, 2)$, $(4, 0)$, and elevation then gives $(0, 0, 0, 0, \tfrac12, \tfrac12, 1, 1, 1, 1)$ with six points $(0, 0)$, $(2/3, 4/3)$, $(4/3, 2)$, $(8/3, 2)$, $(10/3, 4/3)$, $(4, 0)$.

All three evaluate to the same curve, for example $C(1/4) = (1, 3/2)$. Both spaces contain this curve, but only the six-point space contains cubics with a kink at $1/2$.

**An interior knot.** For the scalar quadratic spline with $t = (0, 0, 0, \tfrac12, 1, 1, 1)$ and coefficients $0, 1, 3, 2$, which is $C^1$ at $1/2$, elevation gives $t^+ = (0, 0, 0, 0, \tfrac12, \tfrac12, 1, 1, 1, 1)$ and coefficients $0, 2/3, 4/3, 8/3, 8/3, 2$. It is still $C^1$ at $1/2$, now as a cubic.

## Variations

- **Pure p-refinement.** Elevate and insert nothing. The smoothness at the old knots stays the same, so a $C^0$ mesh stays $C^0$. This is the p-refinement of [isogeometric analysis](/isogeometric-analysis/), and on a mesh that was refined first it gives the larger space of the second order above.
- **Pure h-refinement.** Insert and do not elevate. This is [knot refinement](/knot-refinement/), done one knot at a time by [Boehm's algorithm](/boehm-knot-insertion/) or all at once by the [Oslo algorithm](/oslo-algorithm/).
- **Other elevation algorithms.** Prautzsch (1984) and Cohen, Lyche and Schumaker (1985) give the elevated coefficients directly, as averages over the knot vector, without the Bezier form. The decomposition, Bezier raising and removal route is the one of Piegl and Tiller (1994) and of The NURBS Book, Chapter 5.
- **Reduced smoothness on purpose.** Insert a knot several times after elevation, to get $C^{p-k}$ for a chosen $k$, for example to model a kink or to compare continuities as Cottrell, Hughes and Reali (2007) do.
- **Surfaces and solids.** On a [tensor product surface](/tensor-product-surface/) apply the template to each parametric direction separately, on all rows of control points at once.

## Pitfalls

- **The geometry fixes the coarsest mesh.** The knots of the CAD model stay in the space with their multiplicities. A kink of the geometry, a knot of multiplicity $p$, stays a kink after any refinement. k-refinement cannot make the space smoother there than the model is.
- **Elevation raises every knot.** The elevated knot vector has each value once more, so the smoothness at the old knots does not go up. Only the knots inserted after the elevation get the full $C^{p-1}$. Inserting knots first and elevating after loses this on the new knots.
- **NURBS weights.** Elevate and insert in homogeneous form, with the points $(w_i P_i, w_i)$, and divide at the end. Elevating the points and the weights separately gives a wrong curve.
- **Cost per function.** Fewer functions does not mean a cheaper solve for all sizes. A smooth basis of degree $p$ has supports of $p + 1$ elements in each direction, so the matrix rows are longer than for $C^0$ elements with the same number of functions, and Gauss quadrature with $p + 1$ points per direction costs more per element (see [isogeometric quadrature](/isogeometric-quadrature/)).
- **What is proved and what is measured.** That k-refinement gives fewer functions and higher smoothness is the count above. That it gives better accuracy per degree of freedom is shown in numerical studies, mainly for vibration spectra (Cottrell, Reali, Bazilevs and Hughes 2006, and the 2007 paper). Error bounds that are explicit in $p$ and the smoothness are partial results, for example Beirão da Veiga, Buffa, Rivas and Sangalli (2011). For fixed $p$ under h-refinement, see [NURBS approximation estimates](/nurbs-approximation-estimates/).

## Exercises

1. Start from the quadratic spline on $t = (0, 0, 0, \tfrac13, \tfrac23, 1, 1, 1)$. Give the knot vector and the dimension after k-refinement to degree 4 with the new knots $\tfrac16, \tfrac12, \tfrac56$, and after the other order.
2. Show that two elevations from $p$ to $p + 2$ give the same knot vector and the same coefficients as one elevation by two, defined as the representation on the knot vector with each value twice more.
3. Prove that the points $R$ after line L5 lie in the [convex hull](/convex-hull-property/) of the original control points $P$. Hint: Boehm's formulas and line L5 both take convex combinations.
4. For the space of the second order in the smallest example, write a function in it that is not in the k-refined space.
5. A $C^0$ NURBS circle has knots of multiplicity 2 at quarter points. Explain why no refinement makes its basis $C^1$ at those knots, although the circle itself is smooth.

## References
