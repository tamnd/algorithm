---
tag: 68W35K
kind: technique
slug: level-set-method
name: Level set method
aliases:
- Chan-Vese model
- level set segmentation
- Osher-Sethian level set method
area: numerical/differential-equations
level: research
summary: "Represent a moving curve or surface as the zero set of a function phi and evolve phi by phi_t + F |grad phi| = 0 on a fixed grid; merging, splitting and curvature come for free."
prereqs: [advection-equation, upwind-scheme, signed-distance-function]
see_also: [fast-marching-method, eikonal-equation, active-contours, image-segmentation, courant-friedrichs-lewy-condition, method-of-characteristics, navier-stokes-equations, burgers-equation]
sources:
  - paper: doi:10.1016/0021-9991(88)90002-2
    title: "Stanley Osher and James A. Sethian, Fronts propagating with curvature-dependent speed: algorithms based on Hamilton-Jacobi formulations, Journal of Computational Physics 79 (1988) 12-49"
  - book: isbn:9780387954820
    title: "Stanley Osher and Ronald Fedkiw, Level Set Methods and Dynamic Implicit Surfaces, Springer, 2003"
    locator: "Chapters 1 and 2 (implicit functions and signed distance), 3 (motion in a velocity field), 4 (mean curvature), 5 and 6 (Hamilton-Jacobi equations and upwind schemes), 7 and 8 (reinitialisation and extrapolation)"
  - book: isbn:9780521645577
    title: "James A. Sethian, Level Set Methods and Fast Marching Methods, 2nd ed., Cambridge University Press, 1999"
  - paper: doi:10.1109/83.902291
    title: "Tony F. Chan and Luminita A. Vese, Active contours without edges, IEEE Transactions on Image Processing 10 (2001) 266-277"
  - paper: doi:10.1006/jcph.1994.1155
    title: "Mark Sussman, Peter Smereka and Stanley Osher, A level set approach for computing solutions to incompressible two-phase flow, Journal of Computational Physics 114 (1994) 146-159"
---

The level set method tracks a moving interface $\Gamma(t)$, a curve in the plane or a surface in space, by storing a function $\phi(x, t)$ on a fixed grid and declaring $\Gamma(t) = \{x : \phi(x, t) = 0\}$, with $\phi < 0$ inside and $\phi > 0$ outside. If each point of $\Gamma$ moves with normal speed $F$, then $\phi$ obeys the Hamilton-Jacobi equation

$$\phi_t + F\,|\nabla\phi| = 0,$$

and if it moves with a velocity field $V$, the [advection equation](/advection-equation/) $\phi_t + V\cdot\nabla\phi = 0$. The normal $n = \nabla\phi/|\nabla\phi|$ and the curvature $\kappa = \nabla\cdot n$ are derivatives of $\phi$, so speeds that depend on geometry are easy to impose, and changes of topology (two fronts merging, one splitting) need no special treatment: the grid function simply changes sign in a different pattern. Osher and Sethian introduced the method in 1988. The Chan-Vese model, one of its best-known uses, segments an image by evolving a level set to minimise a piecewise-constant fitting energy.

## In plain words

Imagine drawing a shape on a map and wanting to let it grow, shrink, or flow with the wind. Tracking points along its outline gets messy when two shapes collide and merge, or when one pinches into two.

The level set method avoids the outline altogether. It covers the whole map with a landscape of heights: below sea level inside the shape, above outside. The shape is the coastline. To move the shape, the method raises or lowers the landscape, and the coastline follows. When two islands join, their coastlines merge by themselves.

The same idea finds objects in pictures. Start with any coastline, and push the landscape so that the regions inside and outside each look as uniform in brightness as possible, while keeping the coastline from wiggling too much. The coastline settles on the object boundaries.

## When it applies

- The interface is the boundary of a region (it has an inside and an outside), in 2D or 3D, and is evolved by a law that depends on position, the normal and the curvature, or by an external velocity field.
- Topology may change, or the interface may develop corners: the method picks the viscosity solution, which is the entropy-satisfying solution of the [Hamilton-Jacobi equation](/eikonal-equation/), so corners form and fronts merge the physically right way (Huygens' principle for $F = 1$).
- A fixed Cartesian grid is acceptable, and some loss of area or volume is tolerable or can be corrected.
- In images: the objects are separable by region statistics (Chan-Vese) or by edges (geodesic [active contours](/active-contours/)).

It does not apply directly to open curves, to interfaces that must keep exact area or mass, or to curves whose points carry information (labels, material properties) unless that information is extended off the interface as further fields.

## The template

1. **Embed.** Choose $\phi_0$ with $\Gamma(0) = \{\phi_0 = 0\}$, preferably the [signed distance](/signed-distance-function/), $|\nabla\phi_0| = 1$.
2. **Choose the speed.** A normal speed $F(x, n, \kappa)$, a velocity field $V$, or the gradient flow of an energy. If $F$ is defined only on $\Gamma$, extend it to a neighbourhood (velocity extension, solving $\nabla F\cdot\nabla\phi = 0$).
3. **Discretise in space.** For the hyperbolic part use a monotone [upwind](/upwind-scheme/) Hamiltonian. For $F > 0$, Godunov's choice is
   $$|\nabla\phi|_{ij} \approx \sqrt{\max(D^-_x\phi, 0)^2 + \min(D^+_x\phi, 0)^2 + \max(D^-_y\phi, 0)^2 + \min(D^+_y\phi, 0)^2},$$
   with the roles of $\max$ and $\min$ swapped for $F < 0$; ENO and WENO differences raise the order. Discretise the curvature term $\kappa|\nabla\phi|$ with central differences.
4. **Step in time.** Forward Euler or TVD Runge-Kutta, under the [CFL condition](/courant-friedrichs-lewy-condition/) $\Delta t\,\max|F|\,(\frac1{\Delta x} + \frac1{\Delta y}) \le 1$ for the hyperbolic part and $\Delta t \le \Delta x^2/4$ (2D) for an explicit curvature term.
5. **Reinitialise.** Every few steps restore $|\nabla\phi| \approx 1$ near $\Gamma$ without moving it, by solving $\phi_\tau + \operatorname{sign}(\phi)(|\nabla\phi| - 1) = 0$ to steady state, or by the [fast marching method](/fast-marching-method/).
6. **Restrict to a narrow band.** Update only grid points with $|\phi| < k\Delta x$, which reduces the work per step from $\Theta(M)$ grid points to $\Theta(M^{(d-1)/d})$, roughly the size of the interface.
7. **Extract.** Recover $\Gamma$ by marching squares or cubes, or use $\phi$ directly (inside test $\phi < 0$, smoothed Heaviside $H_\varepsilon(\phi)$ for integrals).

The cost per step is $\Theta(M)$ on a full grid of $M$ points or proportional to the band size, and the number of steps is $\Theta(T\max|F|/\Delta x)$ for speed laws or $\Theta(T/\Delta x^2)$ with explicit curvature.

## Classic examples

**Expanding circle, $F = 1$.** On $[-1, 1]^2$ with $\phi_0 = x^2 + y^2 - 0.3^2$ (deliberately not a distance function), first-order Godunov upwinding, forward Euler with $\Delta t = 0.5\Delta x$, run to $T = 0.4$; the exact front is the circle of radius 0.7. The largest radius error along the axis and the diagonal was observed as:

| $\Delta x$ | 1/20 | 1/40 | 1/80 |
|---|---|---|---|
| radius error | 2.45e-2 | 1.16e-2 | 5.61e-3 |
| observed order | | 1.08 | 1.05 |

The scheme is first order, as expected for monotone schemes. Starting from the exact signed distance $\phi_0 = |x| - 0.3$ instead, the error on the axis was below $10^{-4}$ on all grids, because the upwind scheme is exact for a distance function along grid lines; this is a reason to test on the diagonal and with non-distance initial data.

**Curve shortening.** $F = -\kappa$, that is $\phi_t = \kappa|\nabla\phi|$, shrinks a circle of radius $R_0$ as $R(t) = \sqrt{R_0^2 - 2t}$. With $R_0 = 0.5$, $T = 0.1$ (exact $R = 0.2236$), $\phi_0 = x^2 + y^2 - R_0^2$, central differences and $\Delta t = 0.2\Delta x^2$, the errors were $1.1 \cdot 10^{-2}$, $1.4 \cdot 10^{-3}$, $6.0 \cdot 10^{-4}$ for $\Delta x = \frac1{10}, \frac1{20}, \frac1{40}$. With $\Delta t = 0.3\Delta x^2$ the result was the same to $10^{-4}$; with $\Delta t = 0.6\Delta x^2$, above the explicit diffusion limit, the computed zero set was destroyed (radius 0.03 on the axis and 0.78 on the diagonal). Using $\phi_0 = |x| - R_0$ instead, whose gradient is singular at the centre, the unregularised curvature formula produced a front that shrank far too fast: a reminder that the formula for $\kappa$ divides by $|\nabla\phi|$.

**Chan-Vese segmentation.** The model minimises

$$E(\phi, c_1, c_2) = \mu\,\mathrm{length}(\{\phi = 0\}) + \int_{\phi > 0}(I - c_1)^2 + \int_{\phi < 0}(I - c_2)^2$$

over the level set and two constants, by alternating $c_1, c_2$ = mean of $I$ inside and outside with a gradient step $\phi_t = \delta_\varepsilon(\phi)\bigl[\mu\kappa - (I - c_1)^2 + (I - c_2)^2\bigr]$. A $64 \times 64$ test image of a square and a small disc of intensity 1 on background 0, with Gaussian noise of standard deviation 0.6 (seed 1), $\varepsilon = 1$, $\Delta t = 0.5$ and 400 iterations from a checkerboard start, gave these numbers of misclassified pixels out of 4096 (observed):

| method | threshold at 0.5 | $\mu = 0$ | $\mu = 0.5$ | $\mu = 1$ | $\mu = 2$ | $\mu = 4$ |
|---|---|---|---|---|---|---|
| wrong pixels | 857 | 1007 | 103 | 59 | 104 | 382 |

Without the length term the model is a threshold at $(c_1 + c_2)/2$ and does no better than plain thresholding; a moderate $\mu$ removes the noise; a large $\mu$ rounds the square's corners and starts to erase the small disc. The model does not care which phase is called inside, so counts are taken for the better of the two labellings.

**Two-phase flow.** Sussman, Smereka and Osher let $\phi$ be advected by the [Navier-Stokes](/navier-stokes-equations/) velocity, with density, viscosity and surface tension $\sigma\kappa\delta(\phi)n$ computed from $\phi$, which handles bubbles merging and drops breaking up.

## Variations

- **Narrow band and sparse grids** (Adalsteinsson and Sethian; VDB-style sparse storage) keep the cost proportional to the interface.
- **Fast marching and fast sweeping** solve the stationary case $F|\nabla T| = 1$ for monotone fronts in $\Theta(M\log M)$ or $\Theta(M)$; the arrival time $T$ is a level set function in time.
- **High-order schemes.** ENO and WENO spatial differences with TVD Runge-Kutta in time give orders 3 to 5 away from kinks.
- **Mass-preserving hybrids.** The particle level set method (Enright, Fedkiw, Ferziger and Mitchell) and coupled level set and volume of fluid methods correct the area loss of pure level sets.
- **Geodesic active contours** (Caselles, Kimmel and Sapiro) evolve by an edge-weighted curvature; Chan-Vese uses region statistics and needs no edges; multiphase Chan-Vese uses several level set functions to represent up to $2^m$ regions.
- **Variational level sets** without reinitialisation add a penalty $\int(|\nabla\phi| - 1)^2$ to the energy.

## Pitfalls

- **Loss of area.** First-order advection smears $\phi$ and the enclosed area drifts, typically shrinking in thin features and at corners. Use higher order schemes, finer grids or mass correction.
- **Degenerate $\phi$.** Without reinitialisation $|\nabla\phi|$ can become very large or very small near $\Gamma$, ruining the accuracy of normals and curvature; with too aggressive reinitialisation the interface moves.
- **Central differences for the hyperbolic part.** They are unstable or produce oscillations; the convective term needs upwinding.
- **Time step.** The explicit curvature term needs $\Delta t = O(\Delta x^2)$, much smaller than the hyperbolic CFL step; semi-implicit or additive operator splitting schemes remove the restriction.
- **Curvature at kinks and centres.** Dividing by $|\nabla\phi|$ where it vanishes or is undefined gives huge values; regularise or cap the curvature.
- **Chan-Vese local minima and parameters.** The energy is not convex; the result depends on the initial contour and on $\mu$, and the method assumes two roughly piecewise-constant regions.

## Exercises

1. Show that if $\phi(x(t), t) = 0$ along a trajectory moving with normal speed $F$, then $\phi_t + F|\nabla\phi| = 0$. (Differentiate in $t$ and use $x' = Fn$ with $n = \nabla\phi/|\nabla\phi|$.)
2. Show that $\nabla\cdot(\nabla\phi/|\nabla\phi|) = 1/r$ for $\phi = r - R$ in 2D, and derive $R(t) = \sqrt{R_0^2 - 2t}$ for curve shortening.
3. Show that the Godunov Hamiltonian in the template is monotone under the CFL condition and reduces to first-order upwinding of $\phi_t + |\phi_x| = 0$ in 1D.
4. For $F = 1$ starting from a square, explain why the corners become rounded (arcs of circles) and why a front moving inward ($F = -1$) instead keeps sharp corners; relate this to the entropy condition of the [Burgers equation](/burgers-equation/).
5. Derive the Euler-Lagrange equation of the Chan-Vese energy with $H_\varepsilon$ in place of the indicator of $\{\phi > 0\}$, and show that the optimal $c_1$ and $c_2$ are the region means.
6. Implement reinitialisation by $\phi_\tau + \operatorname{sign}(\phi_0)(|\nabla\phi| - 1) = 0$ and measure how far the zero level moves after 20 iterations for a circle on grids of 40 and 80 cells.

## References
