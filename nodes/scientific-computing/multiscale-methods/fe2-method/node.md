---
tag: 6626AA
kind: algorithm
slug: fe2-method
name: FE2 method
aliases:
- FE squared method
area: scientific-computing/multiscale-methods
level: advanced
summary: Computes the stress at each integration point of a macroscopic finite element model by solving a finite element problem on a representative volume element.
model: real-ram
complexity:
  vars: {M: the number of macro integration points, n: the number of micro cells of the RVE, p: the number of macro Newton steps, q: the number of micro Newton steps per RVE solve}
  time: {worst: "Θ(p q M n)"}
  space: {extra: "Θ(M + n)"}
properties: {deterministic: true, concurrent_coupling: true, consistent_tangent: true, nested_newton: true}
history:
  year: 1999
  people: [Frederic Feyel, Jean-Louis Chaboche]
  note: Feyel named the method FE2 in 1999 and applied it with Chaboche to elastoviscoplastic fiber composites in 2000. Smit, Brekelmans and Meijer in 1998 and Miehe, Schroder and Schotte in 1999 described similar nested finite element schemes.
prereqs: [representative-volume-element, newton-method-for-systems, finite-element-method]
see_also: [periodic-homogenization, heterogeneous-multiscale-method, static-condensation, return-mapping-algorithm, newton-raphson-method, multiscale-finite-element-method, model-order-reduction, multiscale-modeling]
sources:
  - paper: doi:10.1016/S0927-0256(99)00077-4
    title: Frederic Feyel, Multiscale FE2 elastoviscoplastic analysis of composite structures, Computational Materials Science 16, 1999, 344-354
    locator: the nested scheme with a finite element RVE problem at each macro integration point, the periodic boundary conditions of the RVE and the parallel computation
  - paper: doi:10.1016/S0045-7825(99)00224-8
    title: Frederic Feyel and Jean-Louis Chaboche, FE2 multiscale approach for modelling the elastoviscoplastic behaviour of long fibre SiC/Ti composite materials, Computer Methods in Applied Mechanics and Engineering 183(3-4), 2000, 309-330
    locator: the FE2 algorithm with history variables stored at the micro integration points, the macro tangent and the structural examples
  - paper: doi:10.1016/0022-5096(63)90036-X
    title: R. Hill, Elastic properties of reinforced solids, some theoretical principles, Journal of the Mechanics and Physics of Solids 11(5), 1963, 357-372
    locator: the averages of stress and strain over a representative volume and the energy identity that links the two scales
---

The FE2 method is a nested [finite element method](/finite-element-method/) for materials whose stress-strain law is not known in closed form, because it comes from a microstructure. A macroscopic finite element model of the part needs the stress at each integration point. FE2 computes it by solving a second finite element problem on a [representative volume element](/representative-volume-element/) (RVE) of the microstructure, loaded by the macroscopic strain at that point, and taking the volume average of the micro stress. The same RVE problem gives the macroscopic tangent by static condensation, so the macro problem can be solved by Newton's method. The method needs no fitted constitutive law, and it follows nonlinear and history-dependent micro behavior at the cost of one RVE solve per integration point per Newton step.

## In plain words

An engineer wants to know how a composite part bends under load. The fibers and the matrix each have a known behavior, but how the mix behaves is not known, and it changes as the matrix yields. FE2 runs two simulations, one inside the other. The big one models the part on a coarse mesh. Wherever the big one asks how much stress a given stretch causes, a small simulation stretches a tiny sample of the real fibers and matrix by that amount and reports the average stress back. The small simulations also report how stiff the sample is, so the big one can find its answer quickly by Newton's method. Nothing is fitted in advance, but there are many small simulations.

## The problem

Given a macroscopic domain with loads and boundary conditions, a mesh with integration points $x_K$, and an RVE: a cell $Y$ with a fine mesh and the constitutive law $\sigma(y, \varepsilon)$ of each phase, find the macroscopic displacement $U$ such that the macro equilibrium equations hold with the macro stress

$$\Sigma(E) = \langle \sigma(y, E + \nabla_y w) \rangle_Y,$$

where $E$ is the macro strain at $x_K$ and the fluctuation $w$ solves the micro equilibrium problem on $Y$ with periodic, linear displacement or uniform traction boundary conditions. The macro stress and strain must satisfy the Hill-Mandel condition $\langle \sigma : \varepsilon \rangle = \Sigma : E$, which holds for these boundary conditions.

## The algorithm

```pseudo id=main
FE2(macro mesh, RVE, loads)
L1  U ← a start value that satisfies the boundary conditions
L2  repeat
L3      for each macro integration point K do E_K ← strain of U at x_K
L4          solve the RVE problem with mean strain E_K by Newton's method for the fluctuation w
L5          Σ_K ← mean micro stress, C_K ← ⟨k⟩ - Bᵀ K⁻¹ B           ▷ consistent tangent by condensation
L6      assemble the residual r(U) from the Σ_K and the loads, and the Jacobian from the C_K
L7      solve J ΔU = -r and set U ← U + ΔU
L8  until the norm of r is below the tolerance
L9  return U and the macro stresses Σ_K
```

Lines L3 to L5 are the constitutive routine of an ordinary nonlinear finite element code, replaced by a micro finite element solve. In line L5, $k$ is the micro tangent stiffness, $K$ its block on the fluctuation unknowns and $B$ its coupling to the macro strain; eliminating the fluctuation by [static condensation](/static-condensation/) gives the exact derivative $d\Sigma / dE$. Lines L6 and L7 are a step of [Newton's method for systems](/newton-method-for-systems/). With the exact tangent the outer Newton iteration converges quadratically near the solution. For history-dependent materials, each RVE stores its internal variables, such as plastic strains, between load steps, and line L4 updates them with the micro [return mapping](/return-mapping-algorithm/).

In 1D, the RVE is a chain of $n$ cells with a periodic fluctuation $w$, $w_0 = w_n = 0$. The micro equilibrium is equal stress in all cells, and line L4 is a tridiagonal Newton iteration. The condensed tangent equals the harmonic mean $\langle 1/k \rangle^{-1}$ of the micro tangents.

## Example

Take a bar on $(0, 1)$ whose period has 10 cells: 5 cells with $c = 1$ and 5 with $c = 4$, and the law $\sigma = c\, e + e^3$ in each cell.

- **The RVE at $E = 0.3$.** Micro Newton converges in 4 steps. The strain is $0.461$ in the soft cells and $0.139$ in the stiff cells, both with stress $\Sigma = 0.558890$. The tangent is $C = 2.333336$, and a central difference of $\Sigma(E)$ gives the same value to 7 digits.
- **The linear case by hand.** Without the cubic term, the RVE gives $\Sigma = 1.6 E$, the harmonic mean of 1 and 4. With body force $b = 1$ and fixed ends, FE2 on 8 elements takes one Newton step and returns $U_i = x_i(1 - x_i)/3.2$ at the nodes, the exact solution of the homogenized bar.
- **Against a resolved bar.** With the end displacement $g = 0.1$ and no body force, FE2 agrees with the resolved bar at the macro nodes to rounding for $M = 2, 5, 10$ elements of one period each. With $b = 1$ the macro stress varies along the bar; macro Newton takes 4 or 5 steps, and the largest nodal difference from the resolved bar is $7.8 \times 10^{-4}$, $3.7 \times 10^{-4}$ and $1.8 \times 10^{-4}$ for periods $1/5$, $1/10$ and $1/20$. At $x = 1/2$ with period $1/10$, FE2 gives $0.119848$ and the resolved bar $0.119500$.

## Correctness

The [proof](proofs/correctness.md) shows four facts for the 1D case with convex cell energies. The RVE problem is the minimization of a strictly convex energy over the fluctuation, so it has one solution, the stress is the same in all cells, the mean strain is $E$ and the Hill-Mandel condition holds. The condensed tangent of line L5 is exactly $d\Sigma / dE$, by the implicit function theorem and summation by parts, and it equals $\langle 1/k \rangle^{-1}$. The macro law $\Sigma$ is the derivative of the convex function $W(E) = \min_w \Phi_E(w)$, so the macro equations have one solution and line L7 is an exact Newton step for them. Without body force, FE2 reproduces the resolved bar at the nodes when each element holds whole periods.

FE2 is a numerical form of first-order homogenization: it is correct for the macro problem with the homogenized law, and that law describes the real part only when the RVE is small compared with the scale on which the macro strain changes.

## Complexity

In the [real RAM](/real-ram/) model, one micro Newton step costs $\Theta(n)$ in 1D with the [Thomas algorithm](/thomas-algorithm/), and the condensed tangent costs one more tridiagonal solve. With $q$ micro steps per RVE and $M$ integration points, one macro step costs $\Theta(q M n)$, and $p$ macro steps cost $\Theta(p q M n)$. The extra space is $\Theta(M + n)$ for an elastic law, since each RVE can be dropped after line L5; with history variables, all $M$ RVE states must be kept, which costs $\Theta(M n)$.

In 3D, the RVE problem is a sparse nonlinear solve with thousands to millions of unknowns, repeated at every macro integration point in every Newton step and load step. This is the main cost of FE2, and it is the reason for parallel RVE solves and for reduced order models of the RVE.

## Properties

- **No closed-form law.** The macro law is computed, not fitted, so it follows nonlinear and history-dependent micro behavior.
- **Nested Newton.** An outer Newton iteration on the macro unknowns, and an inner Newton iteration in each RVE. The exact tangent keeps the outer convergence quadratic.
- **Embarrassingly parallel.** The RVE problems at different integration points do not interact within one macro step.
- **Energy consistent.** The Hill-Mandel condition makes the macro work equal to the mean micro work.

## Variants and improvements

- **Boundary conditions of the RVE.** Periodic conditions are usual for periodic media; linear displacement conditions give a stiffer and uniform traction conditions a softer apparent response.
- **Second-order homogenization.** Pass the macro strain gradient to the RVE as well, for problems with localization or strong gradients over the RVE.
- **Reduced order RVE models.** Replace the RVE solve by a reduced basis or a proper orthogonal decomposition of its fluctuation fields, or by a model trained on RVE results, to cut the cost of line L4; this is an application of [model order reduction](/model-order-reduction/).
- **Selective FE2.** Run the RVE only at integration points where the macro strain leaves the range in which a cheap fitted or tabulated law is valid.
- **The [heterogeneous multiscale method](/heterogeneous-multiscale-method/)** has the same structure for general macro solvers, with micro problems that need not be RVEs.

## When to use it

Use FE2 when the macroscopic behavior of a heterogeneous material is nonlinear or history-dependent, is not well described by any closed-form law, and the microstructure is much smaller than the part: fiber composites under damage or plasticity, polycrystals, porous metals, foams. If the material is linear elastic, compute the effective tensor once by [periodic homogenization](/periodic-homogenization/) and use it everywhere. If the micro scale is not much smaller than the part, or if strain localizes into bands, a first-order FE2 model is not valid, and the microstructure must be resolved in the critical region.

## Pitfalls

- **An approximate tangent.** A tangent from the micro phases alone, or a secant, keeps the macro iteration but slows it to linear convergence, or makes it fail at large load steps.
- **Loose micro tolerances.** The macro residual can be only as small as the error of the micro solves allows. Inner tolerances must be tighter than the outer one.
- **Softening.** When the micro material softens, the RVE response depends on the RVE size, and the macro problem loses ellipticity. The results then depend on the mesh at both scales.
- **The size of the RVE.** For random microstructure, a small RVE gives a law that differs from sample to sample, as the definition of the representative volume element explains.
- **Storage.** History variables at all micro integration points of all RVEs take a lot of memory in 3D.

## Implementations

## History

Smit, Brekelmans and Meijer described multi-level finite element modeling of nonlinear heterogeneous materials in 1998, and Miehe, Schroder and Schotte gave a computational homogenization scheme for polycrystals in 1999. Feyel named the method FE2 in 1999, and Feyel and Chaboche applied it to elastoviscoplastic SiC/Ti fiber composites in 2000, with parallel RVE solves. The averaging and energy condition at its core go back to Hill (1963) and Mandel. Later work added second-order homogenization, reduced order models of the RVE and data-driven replacements of the micro solve.

## References
