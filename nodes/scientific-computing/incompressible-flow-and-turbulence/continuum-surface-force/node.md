---
tag: BE52KW
kind: technique
slug: continuum-surface-force
name: Continuum surface force model
aliases:
- CSF model
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: Models surface tension as a volume force near the interface, equal to curvature times the gradient of a smoothed color function.
prereqs: [navier-stokes-equations, volume-of-fluid-method]
see_also: [level-set-method, front-tracking-method, piecewise-linear-interface-calculation, ghost-fluid-method, phase-field-model, smoothed-particle-hydrodynamics, lattice-boltzmann-method, immersed-boundary-method]
sources:
  - paper: doi:10.1016/0021-9991(92)90240-Y
    title: "J. U. Brackbill, D. B. Kothe and C. Zemach, A continuum method for modeling surface tension, Journal of Computational Physics 100 (1992) 335-354"
    locator: "the volume force from the color function, the curvature as minus the divergence of the unit normal, and the static drop test"
  - paper: doi:10.1016/j.jcp.2005.08.004
    title: "M. M. Francois, S. J. Cummins, E. D. Dendy, D. B. Kothe, J. M. Sicilian and M. W. Williams, A balanced-force algorithm for continuous and sharp interfacial surface tension models within a volume tracking framework, Journal of Computational Physics 213 (2006) 141-173"
    locator: "the balanced-force discretization and the spurious currents caused by curvature errors"
  - paper: doi:10.1146/annurev-fluid-122316-045034
    title: "Stéphane Popinet, Numerical models of surface tension, Annual Review of Fluid Mechanics 50 (2018) 49-75"
    locator: "well-balanced surface tension, curvature estimation and the time step limit for capillary waves"
  - paper: doi:10.1146/annurev.fluid.31.1.567
    title: "Ruben Scardovelli and Stéphane Zaleski, Direct numerical simulation of free-surface and interfacial flow, Annual Review of Fluid Mechanics 31 (1999) 567-603"
---

The continuum surface force (CSF) model of Brackbill, Kothe and Zemach (1992) puts surface tension into a grid flow solver as an ordinary body force. At a curved interface between two fluids, surface tension makes a jump in pressure, $\sigma\kappa$ in the normal direction, where $\sigma$ is the surface tension coefficient and $\kappa$ the curvature. A grid code cannot apply a force on a surface that cuts through its cells. The CSF model replaces it with the volume force $f = \sigma\kappa\nabla\tilde c$, where $\tilde c$ is a color function that is 1 in one fluid and 0 in the other, smoothed over a few cells. Integrated across the interface, this force gives exactly the jump $\sigma\kappa$, whatever the width of the smoothing. It works with the [volume of fluid method](/volume-of-fluid-method/), with a [level set](/level-set-method/), and in particle codes.

## In plain words

Surface tension acts like a stretched skin on a drop: it squeezes the drop, so the pressure inside is higher than outside, by more when the drop is smaller. A grid code does not know where the skin is exactly; it only has a field that tells, cell by cell, how much of each fluid is there. The CSF model smooths that field a little, so it changes from 1 to 0 over a few cells. Where it changes, its gradient points across the interface. The model pushes on the fluid in those cells, along the gradient, with a strength set by the curvature. The total push across the band is the same as the push of the real skin, so the flow solver sees the right pressure jump. The weak point is the curvature, which must be computed from the smoothed field and is noisy.

## When it applies

- Any flow solver that works with a body force and represents the interface with a field: VOF fractions, a level set, a phase field, or SPH particle colors.
- Surface tension that matters at the scale of the grid: drops, bubbles, jets, capillary waves, films, and flows at small Bond or Weber number.
- The model needs a curvature estimate at the interface. Its accuracy, not the CSF form, sets the accuracy of the surface tension.
- For a sharp pressure jump without a smoothed force, use a jump condition in the pressure solve, as in the [ghost fluid method](/ghost-fluid-method/). For an explicit interface mesh, compute the force on the mesh and spread it, as in [front tracking](/front-tracking-method/).

## The template

```pseudo id=main
CSF-FORCE(c, σ)
L1  c̃ ← smooth(c)                          ▷ a few passes of a 1-2-1 filter, or a kernel
L2  g ← ∇c̃                                 ▷ at the cell corners
L3  n̂ ← g / |g| where |g| > 0               ▷ unit normal, into the fluid with c = 1
L4  κ ← -∇ · n̂                             ▷ at the cell centers
L5  f ← σ κ ∇c̃ / [c]                        ▷ [c] = 1 is the jump of the color function
L6  add f to the momentum equation, with ∇p and f on the same faces
L7  return f
```

The holes are the color function $c$ (the VOF fractions, or a Heaviside function of a level set), the smoothing of line L1, and the places where $\nabla\tilde c$ and $\kappa$ are evaluated. In Brackbill, Kothe and Zemach (1992) the force is also scaled by $\rho/\langle\rho\rangle$ with $\langle\rho\rangle$ the mean of the two densities, which moves the force toward the denser fluid.

**Why the integral is right.** Take a point on the interface and a coordinate $s$ along the normal, through the band where $\tilde c$ goes from 1 to 0. If the curvature is the same across the band, then

$$\int f \cdot \hat n\,ds = \sigma\kappa\int\frac{d\tilde c}{ds}\,ds = \sigma\kappa\,[c],$$

which is the jump of the sharp interface for any smoothing, since only the end values of $\tilde c$ enter. For example, with a linear ramp of width $\varepsilon$, $d\tilde c/ds = 1/\varepsilon$ over a length $\varepsilon$, and the integral is 1 for every $\varepsilon$.

**The Laplace check.** A drop at rest must have $\nabla p = f$ and zero velocity. In 2D a circle of radius $R$ has $\kappa = 1/R$, so the pressure jump is $\sigma/R$ (the Young-Laplace law; in 3D a sphere has $\kappa = 2/R$ and the jump is $2\sigma/R$). For $\sigma = 1$ and $R = 0.25$ the exact jump is 4. A short script computed the fractions of the circle on an $N \times N$ periodic grid, smoothed them with 0 to 4 passes of the 1-2-1 filter in each direction, and applied lines L2 to L5. The table gives the root mean square and the largest error of $\kappa R$ in the mixed cells of the unsmoothed field, and the jump $\int f_x\,dx$ along the grid row through the center, times $R/\sigma$:

| $N$ | passes | rms error of $\kappa R$ | max error of $\kappa R$ | $\Delta p\,R/\sigma$ |
|---|---|---|---|---|
| 32 | 0 | 0.40 | 0.65 | 1.061 |
| 32 | 1 | 0.13 | 0.21 | 1.096 |
| 32 | 2 | 0.070 | 0.11 | 1.082 |
| 32 | 4 | 0.041 | 0.059 | 1.089 |
| 64 | 0 | 0.52 | 1.20 | 1.000 |
| 64 | 1 | 0.16 | 0.37 | 1.062 |
| 64 | 2 | 0.087 | 0.21 | 1.039 |
| 64 | 4 | 0.042 | 0.086 | 1.022 |

Without smoothing, the curvature of the raw fractions has errors of 40% to 50% that do not go down with refinement, which is the known failure of curvature from second differences of a step function. Smoothing reduces them to about 4%. The jump along one line is within 2% to 10% of $\sigma/R$; the smoothed field has level lines of radii a little different from $R$, so the force is spread over a band where the curvature is not exactly $1/R$, and the bias falls as the band becomes thinner on the finer grid. The value 1.000 for the raw field at $N = 64$ comes from errors that cancel along that particular row. The total force on the grid was zero to $10^{-15}$ in all cases.

## Classic examples

- **VOF with CSF.** The model was built for the [volume of fluid method](/volume-of-fluid-method/), with $c$ the volume fractions and the reconstruction of [PLIC](/piecewise-linear-interface-calculation/) used only for the advection. Many VOF codes still use CSF, now with curvature from height functions.
- **Level set methods.** With a [level set](/level-set-method/) $\phi$, the color function is a smoothed Heaviside $H_\varepsilon(\phi)$, so $\nabla\tilde c = \delta_\varepsilon(\phi)\nabla\phi$, and the curvature is $-\nabla \cdot (\nabla\phi/|\nabla\phi|)$ of a smooth distance function. This gives much better curvature than raw fractions.
- **Smoothed particle hydrodynamics.** [SPH](/smoothed-particle-hydrodynamics/) codes give each particle a color, compute $\nabla c$ and the curvature with kernel sums, and add $\sigma\kappa\nabla c/\rho$ as a force per particle.
- **Phase field and lattice Boltzmann models.** In a [phase field model](/phase-field-model/) the force comes from the chemical potential and has the same integral; color-gradient models of the [lattice Boltzmann method](/lattice-boltzmann-method/) use a force of the CSF form on the lattice.
- **Front tracking.** [Front tracking](/front-tracking-method/) uses the same idea in the other direction: the surface force is computed on the front and spread onto the grid as a body force with a smoothed delta function.

## Variations

- **Density scaling.** The factor $\rho/\langle\rho\rangle$ of Brackbill, Kothe and Zemach (1992) shifts the force toward the denser fluid, so that the two sides of an interface with a large density ratio are accelerated more evenly.
- **Continuum surface stress.** The force is written as the divergence of a capillary stress tensor built from $\sigma$, $\hat n$ and $|\nabla\tilde c|$, which needs no explicit curvature and conserves momentum in conservative form.
- **Balanced force.** Francois and co-workers (2006) evaluate $\nabla p$ and $\sigma\kappa\nabla\tilde c$ with the same discrete gradient at the same faces. Then a drop with a constant discrete curvature is at rest exactly, and the spurious currents come only from curvature errors.
- **Height functions.** The curvature is computed from sums of volume fractions along grid columns near the interface, which gives a second-order curvature in VOF codes; see Popinet (2018) for a review.
- **Sharp interface methods.** The [ghost fluid method](/ghost-fluid-method/) puts the jump $\sigma\kappa$ into the pressure solve without smoothing; it has the same sensitivity to curvature errors.

## Pitfalls

- **Spurious currents.** A drop at rest develops small vortices around its interface, called spurious or parasitic currents. They appear when the discrete $\nabla p$ cannot balance the discrete force, and when the curvature is not constant along a circle. With a balanced-force scheme only the curvature error is left, and the velocities scale with $\sigma/\mu$ times that error.
- **Raw curvature.** The table shows that the curvature of unsmoothed fractions does not converge. Smooth, use height functions, or compute it from a level set.
- **Too much smoothing.** A wide band moves the force away from the interface and blurs small features. Smooth just enough to tame the curvature, typically over two to four cells.
- **The capillary time step.** Explicit surface tension is stable only for $\Delta t \lesssim \sqrt{\langle\rho\rangle\Delta x^3/(2\pi\sigma)}$, the time scale of the shortest capillary wave on the grid. This limit falls like $\Delta x^{3/2}$ and is often the smallest step in the run.
- **Force at the wrong place.** Evaluating $\kappa$ and $\nabla\tilde c$ at different points, or $f$ and $\nabla p$ at different points, breaks the balance with the pressure and increases the spurious currents.
- **The 3D jump.** The Laplace check in 3D uses $2\sigma/R$, since a sphere has two principal curvatures $1/R$; using $\sigma/R$ is a common error when moving a 2D test to 3D.

## Exercises

1. For the linear ramp of width $\varepsilon$, show that $\int\sigma\kappa\,d\tilde c/ds\,ds = \sigma\kappa$. Then take a circle, with $\tilde c$ a linear ramp in $r$ over $R - \varepsilon/2 < r < R + \varepsilon/2$ and the curvature of its level lines, $\kappa = 1/r$. Find the jump, and show that it is $\frac{\sigma}{R}\bigl(1 + \frac{\varepsilon^2}{12R^2} + O(\varepsilon^4/R^4)\bigr)$.
2. Show that the total CSF force on a closed drop, $\int\sigma\kappa\nabla\tilde c\,dV$, is zero when $\kappa$ is constant, and explain why it is not zero in general for a discrete $\kappa$.
3. Estimate the capillary time step for water and air ($\sigma = 0.07$ N/m, $\langle\rho\rangle = 500$ kg/m³) on a grid with $\Delta x = 10\,\mu$m, and compare it with the time step from the flow speed of 1 m/s at a Courant number of 0.5.

## References
