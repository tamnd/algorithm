---
tag: W15DY8
kind: technique
slug: periodic-homogenization
name: Periodic homogenization
aliases:
- two-scale asymptotic expansion
area: scientific-computing/multiscale-methods
level: core
summary: Replaces a PDE with rapidly oscillating periodic coefficients by an effective PDE whose coefficients come from cell problems on one period.
model: real-ram
prereqs: [poisson-equation, weak-formulation, multiscale-modeling]
see_also: [two-scale-convergence, representative-volume-element, multiscale-finite-element-method, heterogeneous-multiscale-method, fe2-method, localized-orthogonal-decomposition, homogenization-method, finite-element-method]
sources:
  - book: isbn:9780821853245
    title: Alain Bensoussan, Jacques-Louis Lions and George Papanicolaou, Asymptotic Analysis for Periodic Structures, AMS Chelsea Publishing 374, 2011 (reprint of the North-Holland edition of 1978)
    locator: the elliptic problems with periodic coefficients, the two-scale expansion, the cell problem and the error of the first-order corrector
  - book: isbn:9780387738284
    title: Grigorios A. Pavliotis and Andrew M. Stuart, Multiscale Methods, Averaging and Homogenization, Texts in Applied Mathematics 53, Springer, 2008
    locator: the chapters on homogenization of elliptic PDEs (the formal expansion, the cell problem, the 1D harmonic mean and the layered media)
  - book: isbn:9781107096547
    title: Weinan E, Principles of Multiscale Modeling, Cambridge University Press, 2011
    locator: Chapter 2 (analytical methods, homogenization) and Chapter 8 (elliptic equations with multiscale coefficients)
  - paper: doi:10.1137/0523084
    title: Gregoire Allaire, Homogenization and two-scale convergence, SIAM Journal on Mathematical Analysis 23(6), 1992, 1482-1518
    locator: the proof of the homogenized equation by two-scale convergence
---

Periodic homogenization replaces an elliptic equation $-\nabla \cdot (A(x/\varepsilon) \nabla u_\varepsilon) = f$, whose coefficient is periodic with a small period $\varepsilon$, by an equation $-\nabla \cdot (A^* \nabla u_0) = f$ with a constant effective matrix $A^*$. The matrix $A^*$ comes from $d$ cell problems on one period, which do not depend on $\varepsilon$ or on the domain. The solution $u_0$ is the limit of $u_\varepsilon$ as $\varepsilon \to 0$, and a first-order corrector gives back the gradient of $u_\varepsilon$. The effective coefficient is not the average of $A$: in 1D it is the harmonic mean, and for $a(y) = 2 + \sin(2\pi y)$ it is $\sqrt 3 = 1.732051$, while the average is 2.

## In plain words

Think of a plate made of many thin layers of two metals that conduct heat differently. A computer model that resolves every layer needs a very fine mesh. Far from the layers, though, the plate acts like one uniform material with some effective conductivity. Homogenization computes that effective value from a single repeating piece of the material, called the cell. You solve a small problem on the cell once, and you get the constants of a simple model that has no layers in it. The simple model gives the large-scale behavior. A correction term adds back the small ripples when you need them. The effective value is not a plain average. Across the layers, the poor conductor controls the result, as resistors in series do. Along the layers, the good conductor carries most of the heat, as resistors in parallel do.

## When it applies

- The coefficients are periodic, or periodic after a smooth change of variables, with a period $\varepsilon$ much smaller than the size of the domain and the scale of $f$. Random stationary media need the stochastic version (see the [representative volume element](/representative-volume-element/)).
- Only the large-scale solution, or averages of fluxes, are of interest. Pointwise gradients need the corrector.
- The equation is elliptic or parabolic in divergence form: heat conduction in composites, flow in porous media (Darcy's law), linear elasticity of composites. Wave equations and nonlinear problems have their own forms of the cell problem.
- A direct fine mesh would need many cells per period, so $\varepsilon \ll H$ for any affordable mesh size $H$.

## The template

Let $Y = [0, 1)^d$ be the unit cell and $A(y)$ symmetric, $Y$-periodic, with $\alpha |\xi|^2 \le \xi \cdot A(y) \xi \le \beta |\xi|^2$.

```pseudo id=main
PERIODIC-HOMOGENIZATION(A, f, Ω, ε)
L1  for j ← 1 to d do
L2      solve -div_y(A(y)(e_j + grad_y χ_j)) = 0 in Y, χ_j periodic with mean 0
L3  A*_ij ← mean over Y of e_i · A(y)(e_j + grad_y χ_j), for i, j = 1..d
L4  solve -div(A* grad u_0) = f in Ω, u_0 = 0 on the boundary of Ω
L5  grad u_ε ≈ Σ_j (e_j + grad_y χ_j(x/ε)) ∂u_0/∂x_j        ▷ first-order corrector
L6  return A*, u_0 and the corrected gradient
```

**Where the cell problem comes from.** Put $u_\varepsilon(x) = u_0(x, x/\varepsilon) + \varepsilon u_1(x, x/\varepsilon) + \varepsilon^2 u_2(x, x/\varepsilon) + \cdots$ with every $u_k(x, y)$ periodic in $y$, and use $\nabla = \nabla_x + \varepsilon^{-1} \nabla_y$. At order $\varepsilon^{-2}$ the equation is $-\nabla_y \cdot (A \nabla_y u_0) = 0$, so $u_0$ does not depend on $y$. At order $\varepsilon^{-1}$ it is $-\nabla_y \cdot (A (\nabla_x u_0 + \nabla_y u_1)) = 0$, which is solved by $u_1 = \sum_j \chi_j(y)\, \partial_j u_0(x)$ with the cell problems of line L2. At order $\varepsilon^0$, the equation for $u_2$ has a periodic solution only if the mean over $Y$ of the remaining terms is zero. That condition is the equation of line L4, with $A^*$ from line L3.

**Two facts about $A^*$.** First, $\xi \cdot A^* \xi = \min_\phi \langle (\xi + \nabla \phi) \cdot A (\xi + \nabla \phi) \rangle$ over periodic $\phi$, and $\chi_\xi = \sum_j \xi_j \chi_j$ is the minimizer. So $A^*$ is symmetric and positive definite. Second, with $\langle \cdot \rangle$ the mean over $Y$,

$$\langle A^{-1} \rangle^{-1} \le A^* \le \langle A \rangle$$

in the order of symmetric matrices. The upper bound takes $\phi = 0$ in the minimum. The lower bound comes from the same argument for the complementary energy with a constant flux. These are the Voigt and Reuss bounds.

**The 1D case.** For $d = 1$ the flux $a(y)(1 + \chi'(y))$ is a constant $q$. Periodicity of $\chi$ gives $\int_0^1 \chi' = 0$, so $q \int_0^1 a^{-1} = 1$ and

$$a^* = \Big( \int_0^1 \frac{dy}{a(y)} \Big)^{-1}, \qquad \chi'(y) = \frac{a^*}{a(y)} - 1.$$

**Validity.** For smooth $A$, $f$ and $\partial \Omega$, $\|u_\varepsilon - u_0\|_{L^2} \le C \varepsilon$ and $\|u_\varepsilon - u_0 - \varepsilon u_1\|_{H^1} \le C \varepsilon^{1/2}$. The rate $\varepsilon^{1/2}$ comes from a boundary layer, because $u_1$ does not vanish on $\partial \Omega$. Without the corrector, $\nabla u_\varepsilon - \nabla u_0$ does not go to zero in $L^2$; it only goes to zero weakly. The rigorous proof of the limit uses [two-scale convergence](/two-scale-convergence/) or Tartar's energy method.

## Classic examples

- **The 1D bar.** For $a(y) = 2 + \sin(2\pi y)$, $\int_0^1 dy/(2 + \sin 2\pi y) = 1/\sqrt{3}$, so $a^* = \sqrt 3 = 1.732051$. With $f = 1$ on $(0, 1)$ the limit is $u_0(x) = x(1 - x)/(2\sqrt 3)$ and $u_0(1/2) = 1/(8\sqrt 3) = 0.0721688$. The largest error $|u_\varepsilon - u_0|$ over the interior is 0.00948, 0.00525, 0.00247 and 0.00134 for $\varepsilon = 1/4, 1/8, 1/16, 1/32$, so it is of order $\varepsilon$. A P1 element method on a coarse mesh with $H = 1/4$ and $\varepsilon = 1/8$, with exact element integrals of $a$, uses the average 2 on each element and gives $u_H(1/2) = 1/16 = 0.0625$. That value is 13% too small for every $\varepsilon$ that divides $H$, and it does not improve as $\varepsilon \to 0$.
- **Two phases by hand.** Let $a = 1$ on $[0, \tfrac12)$ and $a = 4$ on $[\tfrac12, 1)$. Then $a^* = 1 / (\tfrac12 + \tfrac18) = 1.6$, and $\chi' = 1.6 - 1 = 0.6$ in the first phase and $1.6/4 - 1 = -0.6$ in the second. The flux $a(1 + \chi')$ is 1.6 in both phases, and $\chi$ is periodic because the two slopes cancel.
- **A laminate in 2D.** Let $A(y) = a(y_1) I$ with the two phases of the last example. For $e_2$ the cell solution is $\chi_2 = 0$, because $A e_2$ has zero divergence, so $A^*_{22} = \langle a \rangle = 2.5$. For $e_1$ the problem is the 1D one, so $A^*_{11} = \langle a^{-1} \rangle^{-1} = 1.6$. The off-diagonal terms are zero. Both bounds above are attained, each in one direction.
- **Composites and porous media.** The same cell problem gives the effective elasticity tensor of a fiber composite and the permeability of a periodic porous medium. In numerical form it is the micro problem of the [FE2 method](/fe2-method/) and of the [heterogeneous multiscale method](/heterogeneous-multiscale-method/).

## Variations

- **Random stationary coefficients.** The cell problem lives on all of $\mathbb R^d$, and in practice on a large sample. The error of the truncated sample leads to the [representative volume element](/representative-volume-element/).
- **Locally periodic coefficients** $A(x, x/\varepsilon)$. Solve one cell problem for each macroscopic point $x$; $A^*$ then depends on $x$.
- **Numerical homogenization without periodicity.** The [multiscale finite element method](/multiscale-finite-element-method/) and [localized orthogonal decomposition](/localized-orthogonal-decomposition/) build coarse spaces from local fine problems and need no cell or scale separation (LOD), or only a weak form of it (MsFEM).
- **Higher-order and boundary-layer correctors.** A second corrector $u_2$ and a boundary-layer term restore higher rates near $\partial \Omega$.
- **Topology optimization.** The [homogenization method](/homogenization-method/) of structural design uses the same effective tensors of microstructures, but it is a different topic: it optimizes the microstructure, it does not approximate a given one.

## Pitfalls

- **Averaging the coefficient.** The arithmetic mean $\langle A \rangle$ is only an upper bound. In 1D it is always wrong unless $a$ is constant. The coarse element example above shows a 13% error that does not go away as $\varepsilon \to 0$.
- **Expecting strong convergence of the gradient.** $\nabla u_\varepsilon$ oscillates at scale $\varepsilon$ with an amplitude of order 1. Stresses and fluxes need the corrector of line L5, and even then the error near the boundary is of order $\varepsilon^{1/2}$ in $H^1$.
- **The wrong boundary conditions in the cell.** The cell problem of line L2 is periodic. Dirichlet or Neumann conditions on the cell give an upper or a lower bound of $A^*$, which converge only as the cell grows over many periods.
- **No scale separation.** If $\varepsilon$ is not small compared with the scale of $f$, of the domain or of the mesh, $u_0$ is a poor model.

## Exercises

1. For $a(y) = 1 / (1 + \tfrac12 \cos 2\pi y)$, show that $a^* = 1$ and that the arithmetic mean is $2/\sqrt 3 = 1.1547$.
2. Show that for a laminate $A(y) = a(y_1) I$ in 3D, $A^* = \mathrm{diag}(\langle a^{-1} \rangle^{-1}, \langle a \rangle, \langle a \rangle)$.
3. Prove the lower bound $\langle a^{-1} \rangle^{-1} \le \xi \cdot A^* \xi / |\xi|^2$ for $A = a I$ from the dual minimum principle over periodic divergence-free fluxes with mean $\sigma$.

## References
