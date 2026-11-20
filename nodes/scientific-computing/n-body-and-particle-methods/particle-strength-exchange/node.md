---
tag: 0HQEAM
kind: algorithm
slug: particle-strength-exchange
name: Particle strength exchange
area: scientific-computing/n-body-and-particle-methods
level: research
summary: Approximates the Laplacian on scattered particles by an integral operator, so viscous diffusion in vortex methods becomes an exchange of strength between neighbors.
model: real-ram
complexity:
  vars: {N: the number of particles, P: the number of interacting pairs}
  time: {worst: "Θ(N + P)"}
  space: {extra: "Θ(N + P)"}
properties: {deterministic: true, conservative: true, order: "1"}
history:
  year: 1989
  people: [Pierre Degond, Sylvie Mas-Gallic]
  note: Degond and Mas-Gallic analysed the weighted particle method for convection and diffusion in 1989, with the diffusion operator replaced by an integral operator.
prereqs: [heat-equation, vortex-particle-method]
see_also: [smoothed-particle-hydrodynamics, sph-smoothing-kernel, linked-cell-list, fixed-radius-near-neighbors, fast-gauss-transform, euler-method]
sources:
  - paper: doi:10.1090/S0025-5718-1989-0983559-9
    title: Pierre Degond and Sylvie Mas-Gallic, The weighted particle method for convection-diffusion equations. Part 1, The case of an isotropic viscosity, Mathematics of Computation 53(188), 1989, 485-507
    locator: the integral approximation of the Laplacian, its consistency, and the convergence of the particle scheme
  - paper: "Pierre Degond and Sylvie Mas-Gallic, The weighted particle method for convection-diffusion equations. Part 2, The anisotropic case, Mathematics of Computation 53(188), 1989, 509-525"
    locator: the extension to a general diffusion matrix
  - book: isbn:9780521621861
    title: Georges-Henri Cottet and Petros D. Koumoutsakos, Vortex Methods, Theory and Practice, Cambridge University Press, 2000
    locator: the chapter on viscous vortex methods
---

Particle strength exchange (PSE) adds diffusion, such as the viscous term $\nu \Delta \omega$ of a [vortex particle method](/vortex-particle-method/), to a set of scattered particles. It replaces the Laplacian by an integral operator over a small kernel, and evaluates the integral as a sum over the nearby particles. Every pair of particles then trades strength in proportion to the difference of their values, so whatever one particle gains, its partner loses, and the total circulation is conserved exactly.

## In plain words

Think of the particles as cups of water at different temperatures standing on a table. Each cup passes a little heat to every nearby cup that is colder, and takes a little heat from every nearby cup that is warmer. Cups that are close trade more than cups that are far apart. The heat that leaves one cup goes into another, so the total heat on the table never changes. Over time the warm and the cold cups even out, which is what diffusion does. In a vortex method the cups are vortex particles, the heat is their spin, and the friction of the fluid sets how fast they trade.

## The problem

Given $N$ particles at $x_p$ in the plane with volumes $V_p$ and values $\omega_p$ (circulation $\Gamma_p = V_p \omega_p$), a diffusivity $\nu$ and a step $h$, approximate the diffusion equation $\partial_t \omega = \nu \Delta \omega$ at the particles. PSE uses a radial, integrable kernel $\eta$ with the second moments $\int x_i x_j \eta(x)\, dx = 2 \delta_{ij}$, here $\eta(x) = (4/\pi) e^{-|x|^2}$, and $\eta_\varepsilon(x) = \varepsilon^{-2} \eta(x / \varepsilon)$. By a Taylor expansion of $\omega(y)$ about $x$,

$$\Delta_\varepsilon \omega(x) = \frac{1}{\varepsilon^2} \int \bigl(\omega(y) - \omega(x)\bigr)\, \eta_\varepsilon(y - x)\, dy = \Delta \omega(x) + O(\varepsilon^2),$$

since the odd moments of $\eta$ vanish. The particles are the quadrature points of this integral:

$$\frac{d \omega_p}{dt} = \frac{\nu}{\varepsilon^2} \sum_q V_q\, (\omega_q - \omega_p)\, \eta_\varepsilon(x_q - x_p).$$

In a vortex method the particles also move, and a step of the [vortex particle method](/vortex-particle-method/) alternates with a PSE step (operator splitting).

## The algorithm

```pseudo id=main
PSE-STEP(x, ω, V, ν, ε, h)
L1  for each pair p < q with |x_p - x_q| < c ε do      ▷ c = 5 in the code
L2      w ← (ν / ε²) η_ε(x_p - x_q)
L3      d ← w (ω_q - ω_p)
L4      r_p ← r_p + V_q d;  r_q ← r_q - V_p d          ▷ the exchange, all r start at 0
L5  ω_p ← ω_p + h r_p for every p                     ▷ explicit Euler
L6  return ω                                          ▷ Σ_p V_p ω_p is unchanged
```

Line L1 needs the pairs within the cutoff; with a [cell list](/linked-cell-list/) of cells of size $c \varepsilon$ this costs $\Theta(N + P)$. If the particles do not move between steps, as on a remeshed lattice, the pairs and their weights from lines L1 and L2 are computed once. Line L4 is the exchange: the circulation $V_p r_p$ that $p$ receives from the pair is $V_p V_q d$, and $q$ loses the same amount.

## Example

**Two particles by hand.** Put $V = 1$ particles at $(0, 0)$ and $(1, 0)$ with $\omega = (1, 0)$, and take $\nu = 1$, $\varepsilon = 1$. Line L2 gives $w = (4/\pi) e^{-1} = 0.468399$, so $r = (-0.468399, 0.468399)$, and an Euler step with $h = 0.5$ gives $\omega = (0.765801, 0.234199)$. The sum is still exactly 1.

**The Lamb-Oseen vortex.** The vorticity $\omega = \Gamma / (\pi s)\, e^{-r^2 / s}$ with $s = 4 \nu t$ solves the diffusion equation, so the vortex at $s = 0.16$ should become the vortex at $s = 0.20$ after the time $0.01$ with $\nu = 1$. Take $\Gamma = 1$, a lattice with spacing $0.1$ on $[-1, 1]^2$ (441 particles, $V = 0.01$) and $\varepsilon = 0.15$. The bound $h D_p \le 1$ below asks for $h \le 0.0066$, so two Euler steps of $0.005$ are taken. The largest error against the exact vortex is 0.28 percent of the peak value 1.59, and the total circulation 0.99962 is unchanged to rounding (measurements).

At the centre, the rate from lines L1 to L4 is $-43.604$, while the exact Laplacian gives $-49.736$. This 12 percent gap is the smoothing error of the operator for $\varepsilon^2 / s = 0.14$; the rate agrees with the value $(4/\varepsilon^2)(\omega_{s + \varepsilon^2} - \omega_s)(0) = -43.604094$ of the integral operator $\Delta_\varepsilon$ to $10^{-7}$, so the lattice sum adds almost no error. With $\varepsilon = 0.1$, equal to the spacing, the rate is $-46.698$ against $-46.810$ for the integral, a quadrature error of 0.24 percent.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It proves these facts (theorems, in exact arithmetic):

- **Exact conservation.** Every step leaves $\sum_p V_p \omega_p$ unchanged, for any positions, any volumes and any symmetric kernel, because the change from a pair is $h(V_p V_q d - V_q V_p d) = 0$.
- **Maximum principle.** If $h D_p \le 1$ for every $p$, with $D_p = \sum_q V_q w_{pq}$, then each new $\omega_p$ is a convex combination of old values, so $\min \omega$ does not decrease and $\max \omega$ does not increase. This is also the stability condition of the explicit step.
- **Consistency.** The integral operator $\Delta_\varepsilon$ differs from $\Delta$ by $O(\varepsilon^2)$ for smooth $\omega$, and on Gaussians it is the exact difference $(4/\varepsilon^2)(\omega_{s+\varepsilon^2} - \omega_s)$. It reproduces the Laplacian of every quadratic exactly.

Degond and Mas-Gallic (1989) proved that the particle scheme converges to the solution of the convection-diffusion equation as $\varepsilon \to 0$ and the particle spacing goes to zero faster than $\varepsilon$, with the order of the kernel. The overlap condition matters: the quadrature error of the lattice sum is small only when the spacing is smaller than $\varepsilon$.

## Complexity

In the [real-RAM](/real-ram/) model, lines L3 to L5 cost $\Theta(N + P)$ for $P$ pairs, and lines L1 and L2 cost $\Theta(N + P)$ with a cell list (the code on this page scans all pairs, at $\Theta(N^2)$, and is meant for small tests). With a spacing $\ell$ and a cutoff $c\varepsilon$, each particle has about $\pi (c \varepsilon / \ell)^2$ neighbours in 2D, so $P = \Theta(N)$ for a fixed ratio $\varepsilon / \ell$. The explicit step needs $h \le 1 / \max_p D_p \approx \varepsilon^2 / (4 \nu)$, the same kind of limit as for an explicit finite difference scheme with grid size $\varepsilon$.

## Properties

- **Conservative.** Total circulation is exact, to rounding in floating point.
- **Grid free.** It works on scattered particles of different volumes, with no mesh.
- **Symmetric.** The exchange is a sum over pairs, so its cost and its communication pattern match those of short-range molecular dynamics.
- **Second order in space** for a kernel with zero odd moments and second moments 2, given enough overlap.
- **First order in time** with explicit Euler, and limited by $h \le \varepsilon^2 / (4\nu)$ roughly.
- **Positivity.** Under the step limit a nonnegative field stays nonnegative.

## Variants and improvements

- **Kernels of higher order.** Kernels with more vanishing moments give $O(\varepsilon^m)$ errors; they are no longer positive, so the maximum principle is lost.
- **Anisotropic and variable diffusion.** Part 2 of Degond and Mas-Gallic handles a general diffusion matrix.
- **Other operators.** The same idea gives integral approximations of first derivatives and other differential operators on particles, with kernels chosen for the moments that each operator needs.
- **Remeshing.** Interpolating the particles to a regular lattice every few steps keeps the overlap that the quadrature needs.
- **Other viscous schemes.** Chorin's random walk, core spreading, and the diffusion velocity method add viscosity without exchange; the random walk is simple but has a statistical error that shrinks only like $1/\sqrt N$ (a heuristic estimate for Monte Carlo sampling).
- **Higher order time steps.** Runge-Kutta steps replace line L5 when the advection step is of higher order.

## When to use it

Use PSE to add viscosity or another diffusion term to a Lagrangian particle method, mainly vortex methods but also particle methods for heat or species transport, when conservation of the total amount matters. Prefer core spreading for a few large blobs, the random walk when a stochastic model is acceptable, and a grid method for diffusion-dominated problems, where the step limit $h \approx \varepsilon^2 / (4\nu)$ makes explicit PSE slow.

## Pitfalls

- **Lost overlap.** If the particles spread out so that their spacing exceeds $\varepsilon$, the sum no longer approximates the integral. Remesh.
- **The step limit.** Halving $\varepsilon$ cuts the stable step by 4; a step above $1 / \max_p D_p$ gives growing oscillations.
- **Boundaries.** Near a wall or the edge of the particle set the integral is cut, so the operator is no longer consistent there; image particles or one-sided kernels are needed.
- **A Gaussian test that looks exact.** On a Gaussian field with a Gaussian kernel, one Euler step of exactly $h = \varepsilon^2 / (4\nu)$ maps $\omega_s$ to $\omega_{s + \varepsilon^2}$, the exact solution, so the space and time errors cancel. Check convergence with other steps or other data.
- **Wrong normalisation.** The kernel must have second moments 2 in each direction; with a kernel normalised to integral 1 instead, the rate is off by a constant factor.

## Implementations

## History

Mas-Gallic had earlier approximated the diffusion operator by an integral operator and solved the resulting equation by a particle method. Degond and Mas-Gallic (1989) analysed this weighted particle method for convection and diffusion, in two papers, for an isotropic and for an anisotropic diffusion, and proved its convergence. The method became the standard deterministic way to add viscosity to vortex particle methods, and with remeshing it is the basis of accurate viscous vortex codes, as described by Cottet and Koumoutsakos (2000).

## References
