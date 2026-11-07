---
tag: 7XFEDB
kind: concept
slug: newton-fractal
name: Newton fractal
aliases:
- Newton basins of attraction
- basins of attraction of Newton's method
- Cayley's problem
area: numerical/root-finding
level: research
summary: The picture of which root Newton's method reaches from each complex start. All basins share one fractal boundary, and some polynomials have open sets of starts that never converge.
prereqs: [newton-raphson-method, polynomial-root-finding, fixed-point-iteration]
see_also: [newton-raphson-method, fixed-point-iteration, laguerre-method, polynomial-root-finding, order-of-convergence, newton-bisection-hybrid, kantorovich-theorem, fundamental-theorem-of-algebra]
sources:
  - paper: doi:10.2307/2369201
    title: "A. Cayley, The Newton-Fourier imaginary problem, American Journal of Mathematics 2 (1879) 97"
    locator: the question of which root Newton's method reaches from a complex start, solved for quadratics and posed for cubics
  - paper: doi:10.1007/BF01211162
    title: "J. H. Curry, L. Garnett and D. Sullivan, On the iteration of a rational function: computer experiments with Newton's method, Communications in Mathematical Physics 91 (1983) 267-277"
    locator: cubic polynomials whose Newton maps have attracting cycles other than the roots
  - paper: doi:10.1007/s002220100149
    title: "J. Hubbard, D. Schleicher and S. Sutherland, How to find all roots of complex polynomials by Newton's method, Inventiones Mathematicae 146 (2001) 1-33"
    locator: a universal finite set of starting points from which Newton's method finds every root
  - book: isbn:9780691124889
    title: John Milnor, Dynamics in One Complex Variable, third edition, Princeton University Press, 2006
    locator: Section 4, the Julia set and the boundary of a basin (Corollary 4.12); Section 8, attracting points and critical points (Theorem 8.6)
  - book: "H.-O. Peitgen and P. H. Richter, The Beauty of Fractals, Springer, 1986"
    locator: the chapter on Newton's method and its basins, with colour plates for z^3 - 1
---

A *Newton fractal* is the picture obtained by running [Newton's method](/newton-raphson-method/) $z_{k+1} = N(z_k) = z_k - p(z_k)/p'(z_k)$ for a complex polynomial $p$ from every point of a grid, and colouring each starting point by the root it reaches. Each root has a *basin of attraction*, an open set of starts that converge to it, and the basins are separated by a common boundary of fractal shape, the Julia set of the rational map $N$. Arthur Cayley asked in 1879 what the basins look like; he solved the quadratic case, where the boundary is a straight line, and found the cubic case hard. The answer came a century later from complex dynamics: every point of the boundary touches every basin, and for some polynomials there are open regions of starts from which Newton's method never converges.

## In plain words

Pick a polynomial with a few roots in the complex plane. From each starting point, run Newton's method and note which root it ends at. Paint each starting point the colour of its root. Near each root the colour is solid, because Newton's method converges quickly from close by. Between the roots the colours do not meet along tidy lines: they interleave in ever smaller bands, and wherever two colours meet, every other colour is arbitrarily close too. A small change in where you start can send you to a different root.

## The idea

Notation on the root-finding pages: $p$ is a complex polynomial of degree $n \ge 2$, $N(z) = z - p(z)/p'(z)$ its Newton map, $x^*$ a root, and $A(x^*) = \{z : N^k(z) \to x^*\}$ its basin.

**The Newton map is rational (proved).** $N$ is a rational function of degree equal to the number of distinct roots of $p$. Its derivative is $N'(z) = p(z)p''(z)/p'(z)^2$, so a simple root is a superattracting fixed point ($N' = 0$, the local [quadratic convergence](/quadratic-convergence/) of Newton's method), a root of multiplicity $m$ is an attracting fixed point with multiplier $(m-1)/m$ (linear convergence), and $\infty$ is a repelling fixed point with multiplier $n/(n - 1)$. The basin of each root is open and contains a disc around the root.

**The boundary is the Julia set (proved).** For a rational map, the boundary of the basin of any attracting fixed point is the whole Julia set $J(N)$ (Milnor, Corollary 4.12). So all basins have the same boundary: every point of $J(N)$ is a limit of points of every basin. In particular the basins cannot be separated by curves when $n \ge 3$, and starting points near $J(N)$ give unpredictable results. $J(N)$ is also where $N$ is chaotic: repelling periodic points are dense in it.

**Quadratics (proved, Cayley and Schröder).** If $p$ has two distinct roots $a \ne b$, the Möbius map $z \mapsto (z - a)/(z - b)$ conjugates $N$ to $w \mapsto w^2$. So the basins are the two open half-planes bounded by the perpendicular bisector of $a$ and $b$, and on the bisector Newton's method is chaotic.

**Other attractors (proved).** Every attracting cycle of a rational map attracts at least one critical point (Fatou; Milnor, Theorem 8.6). The critical points of $N$ are the simple roots of $p$, which are fixed, and the zeros of $p''$ that are not roots of $p$. So for a cubic there is one free critical point, the inflection point of $p$; if its orbit does not converge to a root, there may be an attracting cycle whose basin is an open set of starts that never converge to any root. Whether this happens for a given cubic is decided by following that one orbit.

**Finding all roots from fixed starts (proved).** Hubbard, Schleicher and Sutherland (2001) showed that for every polynomial of degree $n$ with all roots in the unit disc, a fixed set of about $1.11\,n\log^2 n$ points on circles of radius larger than 1 contains, for each root, a start that converges to it.

**Pictures are observations.** A computed picture uses a finite grid, a maximum number of iterations and a tolerance. Points near $J(N)$ may need many iterations, and rounding can move an orbit to a different basin. The large-scale shape of the basins is reliable; the colour of individual points near the boundary is not.

## Examples

All figures below were computed in double precision on a $401 \times 401$ grid of $[-2, 2]^2$, with at most 100 Newton steps and success when $|z_k - x^*| < 10^{-8}$.

**$z^3 - 1$.** The roots are $1$, $e^{2\pi i/3}$ and $e^{-2\pi i/3}$, and the picture has threefold rotational symmetry. On the square grid the fractions of starts reaching each root are $0.353$, $0.323$ and $0.323$ (the square is not symmetric under rotation by $120°$), and the mean number of steps to the tolerance is $7.3$. Only one grid point fails: $z = 0$, where $p'(0) = 0$. On the real axis, $N(x) = (2x^3 + 1)/(3x^2)$ maps every real start other than the countably many preimages of $0$ to the root $1$, yet arbitrarily close to $0$ and to each of these preimages lie starts converging to the complex roots.

**$z^3 - 2z + 2$ (a non-convergent region).** Here $N(0) = 1$ and $N(1) = 0$, and the inflection point $0$ is a critical point of $N$, so $\{0, 1\}$ is a superattracting 2-cycle. Every start in an open set around $0$ and $1$ alternates between the two forever. On the grid, $1.1\%$ of starts never converge; the rest go to the real root $-1.769292$ ($19.7\%$) or to the pair $0.884646 \pm 0.589743i$ ($39.6\%$ each).

**Two roots.** For $z^2 - 1$ the basins of $\pm 1$ are the half-planes $\operatorname{Re} z > 0$ and $\operatorname{Re} z < 0$; starts on the imaginary axis stay on it and never converge.

## Where it is used

- **Choosing starting points.** The pictures explain why Newton's method needs good starting values or safeguards ([Newton-bisection hybrids](/newton-bisection-hybrid/), damping), and the Hubbard-Schleicher-Sutherland points give a provable global strategy for polynomials.
- **Comparing methods.** Basin pictures are a common way to compare the global behaviour of [Laguerre's method](/laguerre-method/), Halley's method and higher-order iterations: higher local order does not imply larger or simpler basins.
- **Complex dynamics.** Newton maps of cubics are a central family in the study of rational maps, and the existence of attracting cycles shows that Newton's method is not a generally convergent algorithm (McMullen, 1987).
- **Computer graphics and teaching.** Newton fractals are a standard illustration of chaos, sensitivity to initial conditions and the limits of local convergence theorems.

## References
