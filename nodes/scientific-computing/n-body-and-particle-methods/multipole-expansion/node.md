---
tag: FSZE62
kind: concept
slug: multipole-expansion
name: Multipole expansion
aliases:
- multipole series
area: scientific-computing/n-body-and-particle-methods
level: core
summary: Writes the far-field potential of a cluster of sources as a series in inverse powers of distance, whose first terms are the monopole, dipole and quadrupole.
prereqs: [legendre-polynomials]
see_also: [multipole-truncation-error-bound, multipole-acceptance-criterion, multipole-to-local-translation, fast-multipole-method, barnes-hut-algorithm, poisson-equation, orthogonal-polynomials, gravitational-softening]
sources:
  - book: isbn:9780262071109
    title: Leslie Greengard, The Rapid Evaluation of Potential Fields in Particle Systems, MIT Press, 1988
    locator: the multipole expansions in two and three dimensions and their error bounds
  - book: isbn:9780521432726
    title: Sverre J. Aarseth, Gravitational N-Body Simulations, Tools and Algorithms, Cambridge University Press, 2003
    locator: Section 3.4 (multipole expansion)
  - book: isbn:9780691130279
    title: James Binney and Scott Tremaine, Galactic Dynamics, 2nd edition, Princeton University Press, 2008
    locator: Chapter 2 (potential theory)
  - paper: doi:10.1006/jcph.1994.1050
    title: "John K. Salmon and Michael S. Warren, Skeletons from the treecode closet, Journal of Computational Physics 111(1), 1994, 136-155"
    locator: the error bounds of truncated multipole expansions in tree codes
---

A multipole expansion writes the potential of a group of sources, seen from far away, as a sum of terms that fall off faster and faster with distance. For sources of mass $m_k$ at positions $\mathbf{y}_k$ inside a ball of radius $a$ around a center, and a point $\mathbf{x}$ at distance $r = |\mathbf{x}| > a$ from that center, the gravitational potential is

$$\phi(\mathbf{x}) = -G \sum_k \frac{m_k}{|\mathbf{x} - \mathbf{y}_k|} = -G \sum_{l=0}^{\infty} \frac{1}{r^{l+1}} \sum_k m_k |\mathbf{y}_k|^l P_l(\cos\gamma_k),$$

where $\gamma_k$ is the angle between $\mathbf{x}$ and $\mathbf{y}_k$ and $P_l$ is the [Legendre polynomial](/legendre-polynomials/) of degree $l$. The term of degree $l$ is of size $(a / r)^l$ relative to the first one, so a few terms give the potential to a known accuracy. The coefficients depend only on the sources, so they can be computed once and used for many far points. This is the basis of tree codes and of the [fast multipole method](/fast-multipole-method/).

## In plain words

From far away, a group of stars pulls almost like one star with the total weight, placed at the center of the group. This is the first and largest part of the pull. The next parts correct for the shape of the group: whether it is stretched out in one direction, or flat, and so on.

Each correction is smaller than the one before it, and it gets smaller faster when the point is farther away. So for a distant point, a few numbers that describe the group give its pull almost exactly. These numbers are the same for every distant point, so they are worked out once and used many times. A computer can then treat a far group as one object instead of adding up each of its stars.

## The idea

**The expansion.** The generating function of the Legendre polynomials gives, for $|\mathbf{y}| < |\mathbf{x}|$,

$$\frac{1}{|\mathbf{x} - \mathbf{y}|} = \frac{1}{\sqrt{r^2 - 2 r r' \cos\gamma + r'^2}} = \sum_{l=0}^{\infty} \frac{r'^l}{r^{l+1}} P_l(\cos\gamma), \qquad r' = |\mathbf{y}|,$$

and the series converges absolutely because $|P_l| \le 1$ on $[-1, 1]$ (theorem). Summing over the sources gives the expansion above.

**The first terms in Cartesian form.** With $M = \sum_k m_k$, the dipole $\mathbf{p} = \sum_k m_k \mathbf{y}_k$ and the traceless quadrupole $Q_{ab} = \sum_k m_k (3 y_{k,a} y_{k,b} - |\mathbf{y}_k|^2 \delta_{ab})$,

$$\phi(\mathbf{x}) = -G \left( \frac{M}{r} + \frac{\mathbf{p} \cdot \mathbf{x}}{r^3} + \frac{1}{2} \frac{\sum_{a,b} Q_{ab} x_a x_b}{r^5} + O\!\left(\frac{M a^3}{r^4}\right) \right).$$

Gravity has only positive masses, so the monopole $M$ is never zero. If the center is the center of mass, the dipole is zero, and the first correction is the quadrupole, of relative size $(a / r)^2$. This is why tree codes put the expansion center of a cell at its center of mass.

**The truncation error.** If all sources lie within radius $a$ of the center and the expansion stops after degree $p$, the error is at most $\frac{G M}{r - a} (a / r)^{p+1}$ (theorem, for positive masses; see the [multipole truncation error bound](/multipole-truncation-error-bound/)). The error falls geometrically in $p$ with ratio $a / r$, which is what a [multipole acceptance criterion](/multipole-acceptance-criterion/) controls.

**Spherical harmonics and two dimensions.** In three dimensions, the addition theorem writes $P_l(\cos\gamma)$ with $2l + 1$ spherical harmonics, so an expansion to degree $p$ has $(p+1)^2$ coefficients. In two dimensions, with complex positions $z$ and the potential $\log |z - z_k|$, the expansion is $\mathrm{Re}\left(Q \log z + \sum_{j \ge 1} a_j z^{-j}\right)$ with $Q = \sum_k q_k$ and $a_j = -\sum_k q_k z_k^j / j$, so degree $p$ needs $p + 1$ coefficients (Greengard 1988).

**Translations.** An expansion about one center can be moved to another center farther from the far point, and a far expansion can be turned into a local Taylor series near the target ([multipole-to-local translation](/multipole-to-local-translation/)). These two operations make the fast multipole method run in $O(N)$ time.

## Examples

**Two masses on a line.** Take unit masses at $(\pm 1, 0, 0)$, $G = 1$, and the point $\mathbf{x} = (3, 0, 0)$. The exact potential is $-(1/2 + 1/4) = -0.75$.

| degree $l$ | term | partial sum (sign of $\phi$ dropped) |
|---|---|---|
| 0 (monopole) | $2/3$ | 0.666667 |
| 1 (dipole) | $0$ | 0.666667 |
| 2 (quadrupole) | $2/27$ | 0.740741 |
| 3 | $0$ | 0.740741 |
| 4 | $2/243$ | 0.748971 |

The center is the center of mass, so all odd terms are zero. In Cartesian form, $Q_{xx} = 2 (3 - 1) = 4$, and the quadrupole term is $\frac{1}{2} \cdot 4 \cdot 9 / 3^5 = 18/243 = 2/27$. The series is $\frac{2}{3} \sum_{j \ge 0} 9^{-j} = 0.75$. Here $a / r = 1/3$, and the bound of degree $p = 2$ gives $\frac{2}{2} (1/3)^3 = 0.037$, larger than the true error $0.0093$.

**A non-example.** The expansion does not converge for a point inside the ball of the sources. At $\mathbf{x} = (0.5, 0, 0)$ the terms of the series grow like $2^l$; this is why a tree code must open a cell that is too close.

## Where it is used

- The [Barnes-Hut algorithm](/barnes-hut-algorithm/) and other tree codes use the monopole, or the monopole and the quadrupole, of each cell about its center of mass.
- The [fast multipole method](/fast-multipole-method/) uses expansions to a degree $p$ chosen for the accuracy, with [translations](/multipole-to-local-translation/) between centers.
- Error analysis of tree codes: the [multipole acceptance criterion](/multipole-acceptance-criterion/) and the bounds of Salmon and Warren (1994) are bounds on the truncated series.
- Potential theory for galaxies: the potential of a smooth density is expanded in spherical harmonics outside and inside each radius (Binney and Tremaine, Chapter 2).
- Electrostatics and the gravity field of the Earth, with the same series.

## References
