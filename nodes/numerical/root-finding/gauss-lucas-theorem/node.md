---
tag: 5ENK5D
kind: theorem
slug: gauss-lucas-theorem
name: Gauss-Lucas theorem
aliases:
- Lucas theorem on critical points
- Lucas's theorem
- Gauss-Lucas theorem on critical points
area: numerical/root-finding
level: advanced
summary: Every root of p' lies in the convex hull of the roots of p, and in its relative interior unless it is a multiple root of p. A complex analogue of Rolle's theorem.
prereqs: [fundamental-theorem-of-algebra, convex-hull]
see_also: [cauchy-root-bound, multiplicity-of-roots, newton-fractal, laguerre-method, polynomial-root-finding, budan-fourier-theorem, homotopy-continuation, newton-raphson-method]
sources:
  - paper: "Félix Lucas, Propriétés géométriques des fractions rationnelles, Comptes Rendus de l'Académie des Sciences 78, 271-274, 1874"
    locator: the statement that the zeros of the derivative lie in every convex region containing the zeros of the polynomial
  - book: "Morris Marden, Geometry of Polynomials, second edition, Mathematical Surveys 3, American Mathematical Society, 1966"
    locator: the chapter on the critical points of a polynomial (Lucas's theorem, its proof by the logarithmic derivative, and Jensen's theorem for real polynomials)
  - book: "Q. I. Rahman and G. Schmeisser, Analytic Theory of Polynomials, London Mathematical Society Monographs 26, Oxford University Press, 2002"
    locator: the chapter on critical points in terms of zeros (the Gauss-Lucas theorem and its refinements)
---

The Gauss-Lucas theorem says that the critical points of a polynomial, the roots of $p'$, lie in the convex hull of the roots of $p$. Each critical point that is not a root of $p$ is a weighted average of the roots, with weights proportional to $m_k/|w - x_k|^2$. It is the complex form of Rolle's theorem, which puts a root of $p'$ between any two real roots of $p$. In root finding it explains where Newton's method and its relatives can stall, since $p'$ vanishes only inside the hull, and it lets bounds on the roots of $p$ pass to all its derivatives.

## Statement

Let $p$ be a polynomial of degree $n \ge 1$ with complex coefficients and distinct roots $x_1, \dots, x_s$ of [multiplicities](/multiplicity-of-roots/) $m_1, \dots, m_s$, so $p(z) = a_0 \prod_k (z - x_k)^{m_k}$ with $a_0 \ne 0$ and $\sum_k m_k = n$. Let $H$ be the [convex hull](/convex-hull/) of $\{x_1, \dots, x_s\}$.

**Theorem (Gauss-Lucas).**

1. Every root of $p'$ lies in $H$.
2. More precisely, if $p'(w) = 0$ and $p(w) \ne 0$, then
$$w = \sum_{k=1}^{s}\lambda_k x_k, \qquad \lambda_k = \frac{m_k/|w - x_k|^2}{\sum_j m_j/|w - x_j|^2} > 0,$$
so $w$ lies in the relative interior of $H$. A root of $p'$ on the relative boundary of $H$ is a multiple root of $p$.
3. The roots of every derivative $p^{(j)}$, $1 \le j < n$, lie in $H$.
4. The centroid of the $n - 1$ roots of $p'$, counted with multiplicity, equals the centroid $-a_1/(n a_0)$ of the $n$ roots of $p$.

For $n = 1$ the derivative is a nonzero constant and items 1 to 3 hold vacuously.

## In plain words

Mark the roots of a polynomial in the complex plane and stretch a rubber band around them. Every point where the derivative is zero lies inside the band. A real version is Rolle's theorem: between two real roots the graph has a turning point. In the plane, each turning point is a balance point of the roots, where each root pulls with a strength that falls off with the square of its distance, and a repeated root pulls as many times as it is repeated.

## Proof

*Item 2.* Away from the roots, the logarithmic derivative is
$$\frac{p'(z)}{p(z)} = \sum_{k=1}^{s}\frac{m_k}{z - x_k}.$$
Let $p'(w) = 0$ with $p(w) \ne 0$. Then $\sum_k m_k/(w - x_k) = 0$. Take complex conjugates and write $1/\overline{(w - x_k)} = (w - x_k)/|w - x_k|^2$:
$$\sum_{k=1}^{s} m_k\frac{w - x_k}{|w - x_k|^2} = 0, \qquad\text{so}\qquad w\sum_k\frac{m_k}{|w - x_k|^2} = \sum_k\frac{m_k}{|w - x_k|^2}x_k .$$
Dividing by the positive sum gives $w = \sum_k\lambda_kx_k$ with all $\lambda_k > 0$ and $\sum_k\lambda_k = 1$. A convex combination with all weights positive lies in the relative interior of the hull of the points.

*Item 1.* If $p'(w) = 0$ and $p(w) = 0$, then $w$ is one of the $x_k$, which lies in $H$. Otherwise item 2 applies.

*Item 3.* By induction on $j$: if the roots of $p^{(j)}$ lie in $H$, item 1 applied to $p^{(j)}$ puts the roots of $p^{(j+1)}$ in the hull of the roots of $p^{(j)}$, which is contained in $H$ because $H$ is convex.

*Item 4.* With $p = a_0z^n + a_1z^{n-1} + \cdots$, $p' = na_0z^{n-1} + (n-1)a_1z^{n-2} + \cdots$. By Vieta's formulas the sum of the roots of $p$ is $-a_1/a_0$ and that of $p'$ is $-(n-1)a_1/(na_0)$, so both centroids are $-a_1/(na_0)$. $\square$

## Consequences

- **Example.** For $p(z) = z^3 - z - 2$ the roots are $1.5213797$ and $-0.7606899 \pm 0.8578736i$, and $p'(z) = 3z^2 - 1$ has roots $\pm 1/\sqrt3 = \pm 0.5773503$. The weights of item 2 are $(0.5863, 0.2068, 0.2068)$ for $+0.5774$ and $(0.0803, 0.4598, 0.4598)$ for $-0.5774$; each gives back the critical point as an average of the three roots. Both centroids are 0, as item 4 says, since $a_1 = 0$.
- **Rolle's theorem.** For a real polynomial with all roots real, $H$ is an interval of the real line and the theorem says the roots of $p'$ lie in $[\min x_k, \max x_k]$; Rolle's theorem gives more, one root between consecutive roots.
- **Newton's method.** The Newton map $z - p(z)/p'(z)$ has its poles at the roots of $p'$ that are not roots of $p$, so all of them lie in $H$. Far outside $H$ the map behaves like $z \mapsto z - (z - c)/n$ with $c$ the centroid, which is why Newton iterates from far away move toward the roots slowly but steadily.
- **Bounds pass to derivatives.** Any convex set that contains the roots of $p$, such as the disc of the [Cauchy bound](/cauchy-root-bound/), contains those of all derivatives. Methods that use $p'$ and $p''$, such as [Laguerre's method](/laguerre-method/), thus work with polynomials whose roots stay in the same region.

## Tightness

- **Boundary points are multiple roots.** For $p = (z - 1)^2(z + 1)$, $p' = (z - 1)(3z + 1)$ has the root 1, a vertex of $H = [-1, 1]$; it is a double root of $p$, as item 2 requires.
- **Critical points can approach a simple root.** For $p = (z - 1)^m(z + 1)$, $p' = (z - 1)^{m-1}((m + 1)z + m - 1)$, so besides 1 the critical point is $-(m - 1)/(m + 1)$, which tends to the simple root $-1$ as $m$ grows. So no fixed margin inside $H$ holds.
- **Equality in the centroid.** For $p = z^n - 1$ all $n - 1$ critical points sit at 0, the centroid; for $p = (z - a)(z - b)$ the single critical point is the midpoint. Together with the previous example, they show that critical points can sit anywhere from the centroid to near the boundary of $H$.
- **Real polynomials.** For real $p$, Jensen's theorem sharpens the result: each non-real root of $p'$ lies in one of the Jensen discs, the closed discs whose diameters are the segments joining pairs of conjugate non-real roots of $p$.

## History

Gauss stated the property in a note in terms of a mechanical equilibrium: the critical points are the positions of equilibrium in the field of unit masses at the roots, attracting with a force inversely proportional to distance. Félix Lucas proved it in 1874 in the Comptes Rendus, in a paper on the geometry of rational functions, and it has carried both names since. Jensen's 1913 theorem on real polynomials and many refinements are collected in Marden's Geometry of Polynomials.

## References
