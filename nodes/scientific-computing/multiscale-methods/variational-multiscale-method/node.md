---
tag: MGX1Q1
kind: technique
slug: variational-multiscale-method
name: Variational multiscale method
aliases:
- VMS method
area: scientific-computing/multiscale-methods
level: advanced
summary: Splits the solution into resolved and unresolved scales and models the effect of the unresolved ones, which explains stabilized finite element methods.
model: real-ram
prereqs: [galerkin-method, streamline-upwind-petrov-galerkin]
see_also: [large-eddy-simulation, static-condensation, finite-element-method, multiscale-finite-element-method, localized-orthogonal-decomposition, navier-stokes-equations, multiscale-modeling]
sources:
  - paper: doi:10.1016/0045-7825(95)00844-9
    title: Thomas J. R. Hughes, Multiscale phenomena, Green's functions, the Dirichlet-to-Neumann formulation, subgrid scale models, bubbles and the origins of stabilized methods, Computer Methods in Applied Mechanics and Engineering 127, 1995, 387-401
    locator: the split into resolved and unresolved scales, the fine-scale Green's function, the element approximation of it and the stabilization parameter as its element integral
  - paper: doi:10.1016/S0045-7825(98)00079-6
    title: Thomas J. R. Hughes, Gonzalo R. Feijoo, Luca Mazzei and Jean-Baptiste Quincy, The variational multiscale method, a paradigm for computational mechanics, Computer Methods in Applied Mechanics and Engineering 166, 1998, 3-24
    locator: the general framework, the exact fine-scale solution in terms of the fine-scale Green's function, and the one-dimensional advection-diffusion example
---

The variational multiscale (VMS) method splits the solution of a variational problem into a part $\bar u$ that the finite element space resolves and a part $u'$ that it does not, $u = \bar u + u'$. It writes one equation for each part, solves the fine-scale equation approximately in terms of the residual of $\bar u$, and puts the result back into the coarse equation. With the simplest model of the fine scales, $u' \approx -\tau (L \bar u - f)$ on each element, the coarse equation is a stabilized finite element method, and for advection-diffusion with linear elements it is the [SUPG method](/streamline-upwind-petrov-galerkin/). The parameter $\tau$ is then not a tuning constant: it is the element mean of the fine-scale Green's function. In 1D this choice makes the coarse solution exact at the nodes.

## In plain words

A finite element mesh can only show features that are larger than its cells. The finer features still act on the coarse ones: in a flow with a thin boundary layer, the plain Galerkin method feels that something is missing and answers with wiggles. The variational multiscale method asks what the missing fine part looks like. It finds that, inside each cell, the fine part is driven by how badly the coarse solution fails the equation there, the residual. A simple model says the fine part is a constant times that residual. Adding the effect of this modeled fine part to the coarse equation gives extra terms, and these terms are exactly the stabilization terms that engineers had added by hand. The method thus explains them and tells how large they must be.

## When it applies

- A linear or nonlinear problem in weak form $a(v, u) = (v, f)$, with a differential operator $L$ and its formal adjoint $L^*$, solved by a finite element space that cannot resolve all scales of $u$.
- Convection-dominated transport, where plain Galerkin oscillates when the mesh Peclet number $a h / (2 \kappa)$ exceeds 1.
- Incompressible flow with equal-order velocity and pressure elements, where the same model of the fine scales gives the pressure stabilization terms.
- Turbulent flow, where the unresolved scales are the small eddies and the method is a form of [large eddy simulation](/large-eddy-simulation/) without a filter.

## The template

Let $V$ be the solution space and $\bar V_h \subset V$ the finite element space. Choose a fine-scale space $V'$ with $V = \bar V_h \oplus V'$, for example the functions that vanish at all mesh nodes.

```pseudo id=main
VARIATIONAL-MULTISCALE(a, L, f, V_h)
L1  split u = ū + u' and v = v̄ + v' with ū, v̄ in V_h and u', v' in V'
L2  coarse equation: a(v̄, ū) + a(v̄, u') = (v̄, f) for every v̄ in V_h
L3  fine equation: a(v', u') = -(v', L ū - f) for every v' in V', so u' = -∫ g'(x, y) (L ū - f)(y) dy
L4  model u' ≈ -τ_K (L ū - f) on each element K, with τ_K = |K|⁻¹ ∫_K ∫_K g_K(x, y) dx dy
L5  solve a(v̄, ū) - Σ_K (L* v̄, τ_K (L ū - f))_K = (v̄, f) for every v̄ in V_h; return ū and u'
```

**Lines L1 to L3.** The test functions $\bar v$ and $v'$ split the single equation $a(v, u) = (v, f)$ into two coupled equations. In the fine equation, $\bar u$ acts as data: integration by parts on each element moves $a(v', \bar u)$ to $(v', L \bar u)$ when $v'$ vanishes on the element boundaries. The fine-scale Green's function $g'$ solves the fine equation for a point source, so $u'$ is a linear map of the coarse residual $L \bar u - f$. This step is exact, and the coarse equation of line L2 with this $u'$ gives the exact $\bar u$, but $g'$ is as hard to compute as the full solution.

**Line L4.** Replace $g'$ by the Green's function $g_K$ of $L$ on one element with zero boundary values, and assume the residual is constant on $K$. Then $u' = -(L \bar u - f)\, b_K$, where $b_K$ solves $L b_K = 1$ in $K$ and $b_K = 0$ on $\partial K$, a residual-free bubble. The parameter $\tau_K$ is the mean of $b_K$ over $K$.

**Line L5.** Integrate $a(\bar v, u')$ by parts on each element. Since $u'$ vanishes on $\partial K$, $a(\bar v, u') = \sum_K (L^* \bar v, u')_K$, and the model of line L4 gives the stabilized equation. For $L u = -\kappa u'' + a u'$ and linear elements, $L^* \bar v = -\kappa \bar v'' - a \bar v' = -a \bar v'$ on each element, so the added term is $\sum_K (a \bar v', \tau_K (L \bar u - f))_K$, the SUPG term.

**The parameter in 1D.** For $L u = -\kappa u'' + a u'$ on an element of length $h$, the bubble is $b(x) = x/a - (h/a)(e^{a x / \kappa} - 1)/(e^{a h / \kappa} - 1)$, and its mean is

$$\tau = \frac{h}{2a} \Big( \coth \mathrm{Pe} - \frac{1}{\mathrm{Pe}} \Big), \qquad \mathrm{Pe} = \frac{a h}{2 \kappa}.$$

This is the optimal SUPG parameter. For large $\mathrm{Pe}$ it tends to $h/(2a)$, and for small $\mathrm{Pe}$ it tends to $h^2/(12 \kappa)$.

**Why 1D is exact.** In 1D, the functions that vanish at all nodes are the sum of the bubble spaces of the elements, so $g' = g_K$ on each element exactly. For $f = 0$ the residual $a \bar u'$ of a linear function is constant on each element. Lines L3 and L4 then agree, and $\bar u$ is the nodal interpolant of $u$.

## Classic examples

- **Advection-diffusion in 1D, by numbers.** Take $-0.01 u'' + u' = 0$ on $(0, 1)$, $u(0) = 0$, $u(1) = 1$, and 10 linear elements, so $h = 0.1$ and $\mathrm{Pe} = 5$. The exact solution $u = (e^{100 x} - 1)/(e^{100} - 1)$ has a boundary layer of width 0.01 and $u(0.9) = 4.54 \times 10^{-5}$. Plain Galerkin gives the recurrence ratio $(1 + \mathrm{Pe})/(1 - \mathrm{Pe}) = -1.5$ and the values $u_8 = 0.4346$, $u_9 = -0.6961$, which oscillate. The VMS parameter is $\tau = 0.05 (\coth 5 - 0.2) = 0.04000454$. With it the method adds the diffusion $\tau a^2$ along the flow, and the computed $u_9$ is $4.540 \times 10^{-5}$, the exact nodal value.
- **SUPG and Galerkin/least squares.** The [SUPG method](/streamline-upwind-petrov-galerkin/) uses the advective part $a \cdot \nabla \bar v$ in place of $-L^* \bar v$, and Galerkin/least squares uses $L \bar v$. For linear elements in 1D the three forms are the same. VMS gives the adjoint form and the value of $\tau$.
- **Bubbles and static condensation.** If one enriches each element with the bubble $b_K$ and eliminates it by [static condensation](/static-condensation/), the condensed coarse equation is the stabilized equation of line L5. This is the residual-free bubble view of the same method.
- **Turbulence.** For the [Navier-Stokes equations](/navier-stokes-equations/), the fine scales modeled by $-\tau$ times the momentum and continuity residuals give a residual-based [large eddy simulation](/large-eddy-simulation/). Bazilevs, Calo, Cottrell, Hughes, Reali and Scovazzi described such a model in 2007; it needs no eddy viscosity and no filter.

## Variations

- **Algebraic subgrid scales.** $u' = -\tau (L \bar u - f)$ with an algebraic formula for $\tau$ in several dimensions that blends the two limits $h/(2|a|)$ and $h^2/(12 \kappa)$ of the 1D value. This is the common choice in practice; the constants differ between codes and element types.
- **Orthogonal subgrid scales.** Choose $V'$ orthogonal to $\bar V_h$ in $L^2$ and model $u'$ by the projection of the residual onto that complement.
- **Dynamic subgrid scales.** In time-dependent problems, give $u'$ its own ODE in time, $\partial_t u' + \tau^{-1} u' = -(L \bar u - f)$, in place of the static model.
- **Exact fine scales in a coarse space.** If the fine-scale problem is solved numerically on patches, with $V'$ the kernel of an interpolation, the method becomes [localized orthogonal decomposition](/localized-orthogonal-decomposition/). The [multiscale finite element method](/multiscale-finite-element-method/) solves local problems in the same spirit for rough coefficients.

## Pitfalls

- **Treating $\tau$ as a free constant.** A value much too small brings back the oscillations, and a value much too large smears the layers. The formula above gives the right limits in both regimes.
- **Dropping terms of the residual.** For linear elements, the second derivative of $\bar u$ is zero inside each element, so the diffusive part of $L \bar u$ is lost. In several dimensions this reduces the accuracy at moderate Peclet numbers, and higher-order elements must keep all terms.
- **Expecting nodal exactness in several dimensions.** The element Green's function is then only a model of $g'$, because the fine scales do not vanish on element edges. The method is stable and consistent, but it is not exact at the nodes.
- **Inconsistent stabilization.** The added term must contain the full residual $L \bar u - f$, not only $L \bar u$. Without $f$, the exact solution no longer satisfies the discrete equation, and the error does not go to zero with $h$.

## Exercises

1. Solve $-\kappa b'' + a b' = 1$ on $(0, h)$ with $b(0) = b(h) = 0$, and check that the mean of $b$ is $\tau = (h/2a)(\coth \mathrm{Pe} - 1/\mathrm{Pe})$.
2. Show that SUPG with the parameter $\tau$ for linear elements equals the central difference scheme with the diffusion $\kappa + \tau a^2$, and that this scheme is exact at the nodes for $f = 0$.
3. Show that for $f = 0$ the limit of $\tau$ as $\kappa \to 0$ gives the fully upwind scheme $a (u_i - u_{i-1})/h = 0$.

## References
