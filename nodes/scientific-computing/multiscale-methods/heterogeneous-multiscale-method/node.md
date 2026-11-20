---
tag: HVHGX1
kind: algorithm
slug: heterogeneous-multiscale-method
name: Heterogeneous multiscale method
area: scientific-computing/multiscale-methods
level: advanced
summary: Runs a macroscale solver whose missing data, such as fluxes or forces, are estimated on the fly by short microscale simulations near each point.
model: real-ram
complexity:
  vars: {M: the number of macro elements, n: the number of micro cells in one micro problem}
  time: {worst: "Θ(M n)"}
  space: {extra: "Θ(M + n)"}
properties: {deterministic: true, cost_independent_of_eps: true, needs_scale_separation: true, concurrent_coupling: true}
history:
  year: 2003
  people: [Weinan E, Bjorn Engquist]
  note: E and Engquist proposed the framework in 2003. E, Ming and Zhang analyzed the finite element version for elliptic homogenization problems in 2005, and Abdulle, E, Engquist and Vanden-Eijnden surveyed the method in 2012.
prereqs: [periodic-homogenization, finite-element-method]
see_also: [multiscale-finite-element-method, fe2-method, representative-volume-element, coarse-projective-integration, localized-orthogonal-decomposition, multiscale-modeling, thomas-algorithm, gaussian-quadrature]
sources:
  - paper: doi:10.4310/CMS.2003.v1.n1.a8
    title: Weinan E and Bjorn Engquist, The heterogeneous multiscale methods, Communications in Mathematical Sciences 1(1), 2003, 87-132
    locator: the framework of a macroscale solver with data estimated from microscale problems, with examples for elliptic homogenization and for ODEs with fast and slow variables
  - paper: doi:10.1090/S0894-0347-04-00469-2
    title: Weinan E, Pingbing Ming and Pingwen Zhang, Analysis of the heterogeneous multiscale method for elliptic homogenization problems, Journal of the American Mathematical Society 18(1), 2005, 121-156
    locator: the finite element HMM with micro cells at the quadrature points, and the estimate of the total error by the macro error and the error of the estimated coefficients
  - paper: doi:10.1017/S0962492912000025
    title: Assyr Abdulle, Weinan E, Bjorn Engquist and Eric Vanden-Eijnden, The heterogeneous multiscale method, Acta Numerica 21, 2012, 1-87
    locator: the survey of the method, its error analysis for elliptic, parabolic and dynamical problems, and the choice of micro boundary conditions
---

The heterogeneous multiscale method (HMM) solves a problem whose macroscale equation has a known form but unknown data. It runs a macroscale solver, for example finite elements on a coarse mesh, and whenever the solver needs a datum, such as the effective flux at a quadrature point, it sets up a small microscale problem near that point, constrained by the current macro state, and estimates the datum from it. For an elliptic equation with a coefficient $a(x/\varepsilon)$, each micro problem is the fine equation on a cell of size $\delta$ with the macro gradient as boundary data, and the averaged flux replaces the unknown effective coefficient. The cost depends on the number of macro points and on the size of a micro cell in units of $\varepsilon$, not on $\varepsilon$ itself.

## In plain words

Suppose you know that heat in a composite plate follows the usual heat equation, but you do not know the effective conductivity, because the plate is made of fibers. One way is to resolve every fiber, which costs too much. HMM instead runs a coarse heat solver. At each point where the coarse solver needs the conductivity, it cuts out a tiny window of the real material, imposes the current coarse temperature slope on the edges of the window, solves the detailed problem in the window and measures the heat flow. The ratio of flow to slope is the conductivity at that point. The windows are tiny and independent, so they are cheap and run in parallel. The coarse solver never needs the full detailed model.

## The problem

Given a fine model, here $-\nabla \cdot (a_\varepsilon \nabla u_\varepsilon) = f$ in $\Omega$ with $u_\varepsilon = 0$ on $\partial \Omega$ and $a_\varepsilon$ varying on a scale $\varepsilon$, and given the form of the macro model, $-\nabla \cdot (A(x) \nabla U) = f$ with an unknown matrix $A$, compute a macro solution $U$ on a mesh of size $H \gg \varepsilon$ that approximates the homogenized solution $u_0$, the limit of $u_\varepsilon$ as $\varepsilon \to 0$. The method assumes scale separation: $A$ at a point depends only on the fine model near that point.

## The algorithm

```pseudo id=main
HMM(a_ε, f, T_H, δ)
L1  for each macro element K with quadrature point x_K do
L2      for each unit gradient e_j: solve -div(a_ε grad v_j) = 0 in I_δ(x_K), v_j - e_j · (x - x_K) = 0 on ∂I_δ
L3      A_K e_j ← mean over I_δ(x_K) of a_ε grad v_j          ▷ the estimated flux for gradient e_j
L4      add |K| A_K grad λ_m · grad λ_l to the macro matrix, and ∫_K f λ_l to the load
L5  solve the macro system for U with U = 0 at the boundary nodes
L6  return U and the estimated data A_K
```

Lines L1, L4 and L5 are a standard [finite element method](/finite-element-method/) with one quadrature point per element. Lines L2 and L3 are the estimator: the micro problem is a cell problem of [periodic homogenization](/periodic-homogenization/) on a cell $I_\delta$ of size $\delta$, with Dirichlet data in place of periodic data, and its mean flux is the response to a unit macro gradient. Since the macro model is linear in the gradient, $d$ micro problems per point give the full matrix $A_K$. For a nonlinear macro model, line L2 uses the current macro gradient $\nabla U(x_K)$ instead of $e_j$, and the macro solve becomes a Newton iteration with micro problems in each step.

In 1D the micro problem is tridiagonal and the [Thomas algorithm](/thomas-algorithm/) solves it. Its flux is constant on $I_\delta$, so $A_K$ is the harmonic mean of $a_\varepsilon$ over $I_\delta$. If $I_\delta$ holds a whole number of periods, this is the homogenized coefficient $a^*$ exactly.

## Example

Take $a_\varepsilon(x) = 2 + \sin(2\pi x/\varepsilon)$ with $\varepsilon = 10^{-3}$, $f = 1$ and $M = 8$ macro elements. The homogenized coefficient is $a^* = \sqrt 3$ and the homogenized solution is $u_0 = x(1 - x)/(2\sqrt 3)$, with $u_0(1/2) = 0.0721688$.

- With $\delta = \varepsilon$ and 16 micro cells, every $A_K$ agrees with $\sqrt 3$ to $3 \times 10^{-9}$, and the nodal values of $U$ agree with $u_0$ to $10^{-10}$. The whole run uses $8 \cdot 16 = 128$ micro cells. A fine mesh with 16 cells per period on $(0, 1)$ would need 16000 cells, and the HMM count stays at 128 for $\varepsilon = 10^{-6}$.
- With one micro cell, line L2 sees only the midpoint value $a_\varepsilon(x_K) = 2$, and $U(1/2) = 1/16 = 0.0625$, which is 13% low. The micro problem must resolve $\varepsilon$.
- With $\varepsilon = 1/64$ and $\delta = (p + \tfrac12)\varepsilon$, so that a half period is left over, the error of the estimate is $|1/A_K - 1/a^*| = 0.0963528/(p + \tfrac12)$ at a point $x_K$ one quarter of a period after a period boundary. For $p = 1, 2, 4, 8, 16$ this gives $A_K - \sqrt 3 = -0.1734, 0.1239, 0.0667, 0.0347, 0.0177$: the error decreases like $\varepsilon/\delta$.

## Correctness

The [proof](proofs/correctness.md) has two steps. First, the macro error splits into the error of the macro solver for the homogenized problem and a term from the error of the data: with $e = \max_K |A_K - a^*|$ and $u_H$ the finite element solution with the true $a^*$,

$$\|(u_H - U)'\|_{L^2} \le \frac{e}{a^*} \|U'\|_{L^2}.$$

Second, in 1D the micro estimate is the harmonic mean over $I_\delta$, and for periodic $a$ its error obeys $|1/A_K - 1/a^*| \le (\varepsilon/\delta) \max_y |1/a(y) - 1/a^*|$, with $e = 0$ for whole periods. The general analysis of E, Ming and Zhang has the same structure in several dimensions: the total error is the macro error plus the data error $e$, which they bound in terms of $\varepsilon$, $\delta$ and the micro discretization. In several dimensions the Dirichlet data of line L2 add a boundary layer of width $\varepsilon$ around $\partial I_\delta$, so $e$ does not vanish for whole periods; periodic micro data on a cell of whole periods of a periodic medium remove this term.

## Complexity

In the [real RAM](/real-ram/) model, each micro problem in 1D costs $\Theta(n)$ with $n$ micro cells, and there are $M$ of them, so lines L1 to L4 cost $\Theta(M n)$. Line L5 is a tridiagonal solve in $\Theta(M)$. The extra space is $\Theta(M + n)$, since a micro problem is dropped after line L3.

In $d$ dimensions with $n^d$ micro cells and $d$ right-hand sides per point, the work per macro point is that of $d$ sparse solves of size $n^d$, and $n$ depends only on $\delta/\varepsilon$ and the micro accuracy. The total cost is independent of $\varepsilon$, while a direct fine solve costs at least $(1/\varepsilon)^d$.

## Properties

- **Top-down.** The form of the macro model is chosen first, and the micro model only supplies its data. The method does not discover a new macro equation.
- **Independent micro problems.** The micro problems at different points do not interact, and they run in parallel.
- **Sampling, not covering.** The micro cells cover a fraction about $(\delta/H)^d$ of the domain, which is the source of the saving and also the reason that the method needs scale separation.
- **The approximation is of $u_0$.** The method computes the homogenized solution. The fine oscillations of $u_\varepsilon$ can be rebuilt locally from the micro solutions when needed.

## Variants and improvements

- **Periodic or oversampled micro cells.** Periodic data remove the boundary layer for periodic media. For other media, solve on a larger cell and average only over an inner part, which reduces the boundary error.
- **Weighted averages.** Averaging line L3 with a smooth kernel in place of a plain mean gives faster convergence in $\delta/\varepsilon$ for nonperiodic microstructure.
- **Nonlinear and time-dependent problems.** For a nonlinear flux, the micro problem depends on the current macro gradient, as in the [FE2 method](/fe2-method/). For parabolic problems, the micro problems may be stationary or short time-dependent runs.
- **Stiff ODEs and dynamics.** For a system with slow and fast variables, the macro solver is an ODE integrator for the slow variables, and its force is a time average over a short run of the full system with the slow variables fixed. Engquist and Tsai studied this case in 2005. [Coarse projective integration](/coarse-projective-integration/) is a related equation-free approach that extrapolates in time instead.

## When to use it

Use HMM when the form of the macroscale equation is known, its data are not known in closed form, and the scales are well separated: elliptic and parabolic problems with fine-scale coefficients, continuum models whose stress comes from molecular dynamics, and slow-fast ODE systems. Use the [multiscale finite element method](/multiscale-finite-element-method/) or [localized orthogonal decomposition](/localized-orthogonal-decomposition/) when there is no scale separation, or when the fine solution itself is needed, since they cover the whole domain with local problems. Use [periodic homogenization](/periodic-homogenization/) with one cell problem when the medium is exactly periodic and the same everywhere.

## Pitfalls

- **An unresolved micro problem.** A micro mesh that does not resolve $\varepsilon$ gives the wrong data, as the example with one micro cell shows. The error does not decrease with $H$.
- **The size of the cell.** For a cell with Dirichlet data, the error decreases only like $\varepsilon/\delta$. A cell of a few periods leaves an error of several percent.
- **No scale separation.** If $a_\varepsilon$ has features on scales between $\varepsilon$ and $H$, such as long channels, a small cell does not see them, and the estimated data are wrong.
- **Expecting the fine solution.** $U$ approximates $u_0$. Its gradient is the macro gradient, not the oscillating gradient of $u_\varepsilon$, so pointwise fluxes need the micro solutions.

## Implementations

## History

E and Engquist proposed the heterogeneous multiscale method in 2003 as a general framework for problems in which a macroscale model of known form needs data from a microscale model, with applications to homogenization, to molecular dynamics and to ODEs with fast and slow variables. E, Ming and Zhang analyzed the finite element version for elliptic homogenization problems in 2005. Abdulle, E, Engquist and Vanden-Eijnden surveyed the method, its analysis and its applications in Acta Numerica in 2012.

## References
