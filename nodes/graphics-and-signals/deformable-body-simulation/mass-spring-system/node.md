---
tag: 4B6KHP
kind: model
slug: mass-spring-system
name: Mass-spring system
aliases:
- mass-spring model
- spring-mass system
area: graphics-and-signals/deformable-body-simulation
level: intro
summary: Point masses joined by damped Hooke springs along their lines. Simple and fast, but the response depends on the mesh, and stiff springs force small explicit time steps.
prereqs: [particle-system, symplectic-euler-method]
see_also: [cloth-simulation, provot-strain-limiting, baraff-witkin-cloth, fast-mass-spring, penalty-contact, finite-element-method, position-based-dynamics, discrete-shells]
sources:
  - paper: doi:10.20380/GI1995.17
    title: "Xavier Provot, Deformation constraints in a mass-spring model to describe rigid cloth behavior, Graphics Interface 95, 147-154, 1995"
    locator: "Section 2.1 (structural, shear and flexion springs on a grid), Section 2.2 (the forces) and Section 4, equation (3) (the critical stiffness for a given step)"
  - book: isbn:9781568810904
    title: "Donald H. House and David E. Breen (editors), Cloth Modeling and Animation, A K Peters, 2000"
    locator: the chapters on particle and spring models of cloth (general locator)
---

A mass-spring system models a deformable object as point masses joined by springs. Each spring pulls or pushes its two masses along the line between them, with a force that grows with the change of its length. Cloth, hair, ropes and soft bodies in graphics were first built this way, and the model is still the usual first step. It differs from a [particle system](/particle-system/), where the particles do not interact, and from the [finite element method](/finite-element-method/), where the forces come from a continuum energy with material parameters: a spring network has no continuum behind it, so its response depends on the mesh.

## The machine

The state is a set of $n$ particles with masses $m_i$ (kg), positions $\mathbf x_i$ (m) and velocities $\mathbf v_i$ (m/s), and a set of $m$ springs. A spring $(i, j)$ has a rest length $L$ (m), a stiffness $k$ (N/m) and a damping coefficient $c$ (N s/m). Write $\mathbf x_{ij} = \mathbf x_j - \mathbf x_i$, $l = |\mathbf x_{ij}|$, $\hat{\mathbf x}_{ij} = \mathbf x_{ij} / l$ and $\mathbf v_{ij} = \mathbf v_j - \mathbf v_i$. The spring puts the force

$$\mathbf f_j = -\left(k (l - L) + c \, \mathbf v_{ij} \cdot \hat{\mathbf x}_{ij}\right) \hat{\mathbf x}_{ij}, \qquad \mathbf f_i = -\mathbf f_j$$

on its two ends. The first term is Hooke's law for the spring and the second is a damper along the spring. The elastic part is the negative gradient of the energy

$$E(\mathbf x) = \sum_{(i,j)} \tfrac12 k \, (|\mathbf x_{ij}| - L)^2 .$$

Each particle then follows Newton's second law $m_i \ddot{\mathbf x}_i = \sum \mathbf f_i + m_i \mathbf g$ with gravity $\mathbf g = (0, -9.81, 0)$ m/s$^2$. A particle with infinite mass (inverse mass 0) is fixed.

On a rectangular grid of particles, as for cloth, Provot (1995, Section 2.1) uses three kinds of springs. Structural springs join $[i, j]$ to $[i+1, j]$ and $[i, j+1]$ and resist stretch. Shear springs join the two diagonals of each cell. Bending (flexion) springs join $[i, j]$ to $[i+2, j]$ and $[i, j+2]$ and resist folding, but only weakly and only through a change of length.

The standing assumptions are: all forces are central (along the line of the two particles); the springs are linear in the change of length, which is a modelling choice and not a law of the material; and the parameters $k$, $c$ and $L$ are set per spring by the user. Hooke's law is a good model of a real spring for small changes of length, but a spring network is not a discretization of a continuum material.

In time the model is a system of ordinary differential equations, and any integrator can advance it. The usual explicit choice is [symplectic Euler](/symplectic-euler-method/), velocity first:

```pseudo id=main
MASS-SPRING-STEP(x, v, dt)
L1  for each particle i: f_i <- m_i g
L2  for each spring (i, j, L, k): d <- x_j - x_i, l <- |d|, u <- d / l
L3      s <- k (l - L) + c (v_j - v_i) . u
L4      f_i <- f_i + s u, f_j <- f_j - s u
L5  for each free particle i: v_i <- v_i + dt f_i / m_i
L6      x_i <- x_i + dt v_i
```

The code with this page is this step in 2D, with the grid builder for the three kinds of springs.

## What it counts

The model gives the forces on the particles, the elastic energy $E$ and, through an integrator, the motion. One force evaluation costs $\Theta(n + m)$ time, and a step of an explicit method costs the same. A grid of $n$ particles with all three kinds of springs has $m < 6n$ springs.

The quantities are the ones of a real mechanical network of springs. When the network stands for cloth or a soft solid, $k$ and $c$ are tuned until the motion looks right, and they do not map in a simple way to the Young's modulus or the Poisson ratio of the material.

## Relation to other models

- A [particle system](/particle-system/) is the same state without the springs.
- The [finite element method](/finite-element-method/) with a hyperelastic energy such as the [St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/) gives forces that converge to a chosen continuum material as the mesh is refined. [Baraff-Witkin cloth](/baraff-witkin-cloth/) sits between the two: its stretch and shear conditions are measured per triangle in the cloth's own coordinates.
- [Discrete shells](/discrete-shells/) and the [quadratic bending model](/quadratic-bending-model/) replace bending springs by an energy of the dihedral angles, which does not mix bending with stretching.
- [Position-based dynamics](/position-based-dynamics/) treats each spring as a distance constraint and moves the positions to meet it, which acts like an infinitely stiff spring whose effective stiffness depends on the step and the iteration count.
- [Penalty contact](/penalty-contact/) uses a stiff spring at each contact and has the same step limit as a stiff spring here.
- [Provot's strain limiting](/provot-strain-limiting/), [Baraff-Witkin cloth](/baraff-witkin-cloth/) and [fast mass-spring simulation](/fast-mass-spring/) are three ways to live with stiff springs: limit the strain after the step, take implicit steps, or solve the implicit step by local and global steps.

## Known results in the model

1. **Forces from the energy (proved).** Without damping, $\mathbf f = -\nabla E$. The force is zero at the rest shape and after any rigid motion of the rest shape, because $E$ depends only on the lengths. The test checks the gradient against central differences with $h = 10^{-6}$ and a relative tolerance of $10^{-6}$ (num_grad of the shared helper), and the zero force after three rigid motions.
2. **Momentum (proved).** The two forces of a spring are equal and opposite, so the total linear momentum changes only by the external forces. They also lie on the line of the two particles, so their torques cancel and the angular momentum is kept as well. Symplectic Euler keeps both exactly in exact arithmetic: $\mathbf x_{n+1} \times \mathbf v_{n+1} = \mathbf x_n \times \mathbf v_{n+1}$, and the change $\mathbf x_n \times \Delta t \, \mathbf f(\mathbf x_n, \mathbf v_n)$ sums to zero over central pair forces. The damper is central too. The test runs 300 damped steps of a free random grid and finds no change above $10^{-10}$ relative.
3. **Damping dissipates (proved).** In the continuous system the damper takes the power $c \, (\mathbf v_{ij} \cdot \hat{\mathbf x}_{ij})^2 \ge 0$ out of the kinetic plus elastic energy. Damping along the spring does not slow a rigid rotation.
4. **Step limit (proved).** For one mass $m$ on a spring $k$ to a fixed point, $\omega = \sqrt{k / m}$, and symplectic Euler is stable if and only if $\omega \Delta t < 2$. With $k = 100$ N/m and $m = 1$ kg, $\omega = 10$ rad/s and the limit is $\Delta t = 0.2$ s. The test finds the motion bounded at $0.19$ s and growing past $10^3$ at $0.21$ s. For a network the limit is $2 / \omega_{\max}$, where $\omega_{\max}^2$ is the largest eigenvalue of $M^{-1} K$ for the stiffness matrix $K$ at the current state. For cloth with a fixed material and a grid spacing $h$, the mass per particle scales as $h^2$ while the stiffness of a stretch spring stays the same, so $\omega_{\max}$ grows like $1/h$ and the stable step shrinks like $h$. Stretch springs are stiff, so explicit cloth needs small steps. [Penalty contact](/penalty-contact/) has the same limit.
5. **Energy band of symplectic Euler (proved).** For the oscillator above, $Q = \omega^2 x^2 + v^2 - \omega^2 \Delta t \, x v$ is kept exactly by the step, where $x$ is the stretch. So the energy $E = (\omega^2 x^2 + v^2)/2$ stays in $[E_0 / (1 + \omega\Delta t/2), E_0 / (1 - \omega\Delta t/2)]$ for a start at rest, and does not drift. With $k = m = 1$, a stretch of 1 and $\Delta t = 0.1$ s, the band is $[0.476190, 0.526315]$. The test runs $10^4$ steps and finds the energy inside the band and close to both ends.
6. **The response depends on the mesh (proved for the square lattice).** Stretch an infinite square lattice of spacing $L$ by a small strain $\varepsilon$ along the direction $(\cos\phi, \sin\phi)$. A spring of direction $\mathbf e$ changes length by $l \varepsilon (\mathbf e \cdot \mathbf d)^2$ to first order, and summing the four springs of a cell gives the energy per cell

   $$\tfrac12 L^2 \varepsilon^2 \left(k + k_d + \cos^2\phi \sin^2\phi \, (4 k_d - 2 k)\right)$$

   for structural springs $k$ and diagonal springs $k_d$. With structural springs only, the cloth is half as stiff at 45 degrees as along the grid lines. The choice $k_d = k / 2$ makes the uniaxial stiffness the same in all directions. Even then the network cannot match a chosen material: its small strain stiffness tensor is $C_{abcd} = L^{-2} \sum k \, l^2 e_a e_b e_c e_d$ over the springs of a cell, which is symmetric in all four indices, so the Lamé parameters satisfy $\lambda = \mu$ (the Cauchy relation) and the 2D Poisson ratio is fixed at $1/3$. On an irregular triangle mesh the stiffness changes from triangle to triangle with the shapes. So a spring network does not converge to a chosen continuum elastic model as the mesh is refined, and its behaviour depends on the mesh. The test checks the formula against the energy of a strained patch and the two special cases.
7. **Super-elasticity (measured).** Provot (1995, Section 3) hung a 17 by 17 grid by two corners and found that, with a stiffness low enough for a stable step, the most stretched springs passed 100% elongation, while woven cloth stretches by about 10% at most. This is the reason for [Provot's strain limiting](/provot-strain-limiting/).

## References
