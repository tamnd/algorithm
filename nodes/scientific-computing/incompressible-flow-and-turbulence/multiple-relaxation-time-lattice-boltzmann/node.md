---
tag: JZ1BG8
kind: algorithm
slug: multiple-relaxation-time-lattice-boltzmann
name: Multiple-relaxation-time lattice Boltzmann method
aliases:
- MRT lattice Boltzmann
- MRT collision operator
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: Lattice Boltzmann with collision in moment space, where each moment relaxes at its own rate. It is often more stable than BGK at low viscosity, and the free rates can place bounce-back walls exactly.
solves: [navier-stokes-equations]
model: real-ram
complexity:
  vars: {M: "the number of lattice nodes", K: "the number of time steps"}
  time: {worst: "Θ(K M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, explicit: true, local_collision: true, conserves_mass_exactly: true, conserves_momentum_exactly: true, order_in_space: "2", reduces_to_bgk: "when all rates are equal"}
history:
  year: 1992
  people: [Dominique d'Humières, Pierre Lallemand, Li-Shi Luo]
  note: "d'Humières proposed generalized lattice Boltzmann equations with a collision matrix in moment space in 1992. Lallemand and Luo (2000) gave the D2Q9 moment basis used here and its linear stability analysis; d'Humières, Ginzburg, Krafczyk, Lallemand and Luo (2002) gave 3D models."
prereqs: [lattice-boltzmann-method, bgk-collision-operator, bounce-back-boundary-condition]
see_also: [chapman-enskog-expansion, navier-stokes-equations, von-neumann-stability-analysis, gram-schmidt-process, orthogonal-polynomials, large-eddy-simulation]
sources:
  - paper: "D. d'Humières, Generalized lattice-Boltzmann equations, in B. D. Shizgal and D. P. Weaver (eds.), Rarefied Gas Dynamics: Theory and Simulations, Progress in Astronautics and Aeronautics 159, AIAA, 1992"
    locator: "pp. 450-458"
  - paper: doi:10.1103/PhysRevE.61.6546
    title: "Pierre Lallemand and Li-Shi Luo, Theory of the lattice Boltzmann method: Dispersion, dissipation, isotropy, Galilean invariance, and stability, Physical Review E 61 (2000) 6546-6562"
    locator: "the D2Q9 moment basis, the equilibrium moments and the linear stability analysis"
  - paper: doi:10.1098/rsta.2001.0955
    title: "Dominique d'Humières, Irina Ginzburg, Manfred Krafczyk, Pierre Lallemand and Li-Shi Luo, Multiple-relaxation-time lattice Boltzmann models in three dimensions, Philosophical Transactions of the Royal Society A 360 (2002) 437-451"
  - paper: doi:10.1103/PhysRevE.68.066614
    title: "Irina Ginzburg and Dominique d'Humières, Multireflection boundary conditions for lattice Boltzmann models, Physical Review E 68 (2003) 066614"
    locator: "the dependence of the bounce-back wall position on the relaxation rates"
  - book: isbn:9783319446479
    title: "Timm Krüger, Halim Kusumaatmaja, Alexandr Kuzmin, Orest Shardt, Goncalo Silva and Erlend Magnus Viggen, The Lattice Boltzmann Method: Principles and Practice, Springer, 2017"
    locator: "Chapter 10 (MRT and TRT collision operators)"
  - paper: doi:10.1103/PhysRevE.65.046308
    title: "Zhaoli Guo, Chuguang Zheng and Baochang Shi, Discrete lattice effects on the forcing term in the lattice Boltzmann method, Physical Review E 65 (2002) 046308"
---

The multiple-relaxation-time (MRT) lattice Boltzmann method is the [lattice Boltzmann method](/lattice-boltzmann-method/) with a different collision step. The [BGK collision operator](/bgk-collision-operator/) relaxes all nine populations of a D2Q9 node toward equilibrium at one rate $1/\tau$. MRT first maps the populations to nine moments (density, energy, momentum, heat flux, stress), relaxes each moment at its own rate, and maps back. The shear rate fixes the viscosity as in BGK, and the other rates are free. The streaming step and the [bounce-back walls](/bounce-back-boundary-condition/) are the same as in BGK.

## In plain words

Each lattice node carries nine numbers, one for each direction a particle can move. A collision pushes these numbers toward a target that depends only on the local density and velocity. BGK pushes all nine with the same strength. MRT first rewrites the nine numbers as nine physical quantities: mass, momentum, energy, stress and two more. It then pushes each quantity with its own strength. Mass and momentum are not changed. The stress decides the viscosity. The other quantities have no physical role in slow flow, so you can choose their strengths to damp noise or to make walls sit exactly where you want them. If every strength is the same, MRT is exactly BGK.

## The problem

Solve the weakly compressible [Navier-Stokes equations](/navier-stokes-equations/) on a lattice, as the lattice Boltzmann method does, but with a collision that has more than one free parameter. With BGK the single time $\tau$ sets the viscosity $\nu = (\tau - \frac12)/3$ and also every other property of the scheme: its stability at small $\nu$, the decay of nonhydrodynamic modes, and the position of bounce-back walls. MRT separates these. Units are lattice units: grid spacing 1, time step 1, $c_s^2 = \frac13$.

## The algorithm

The populations $f_0, \ldots, f_8$ use the velocities $c_0 = (0,0)$, $c_1 = (1,0)$, $c_2 = (0,1)$, $c_3 = (-1,0)$, $c_4 = (0,-1)$, $c_5 = (1,1)$, $c_6 = (-1,1)$, $c_7 = (-1,-1)$, $c_8 = (1,-1)$, in the same order as the lattice Boltzmann page. The moments are $m = Mf$ with the matrix of Lallemand and Luo (2000):

| moment | row of $M$ | equilibrium $m^{\mathrm{eq}}$ | rate |
|---|---|---|---|
| $\rho$ (density) | $1, 1, 1, 1, 1, 1, 1, 1, 1$ | $\rho$ | any |
| $e$ (energy) | $-4, -1, -1, -1, -1, 2, 2, 2, 2$ | $-2\rho + 3\rho\lvert u\rvert^2$ | $s_e$ |
| $\epsilon$ (energy squared) | $4, -2, -2, -2, -2, 1, 1, 1, 1$ | $\rho - 3\rho\lvert u\rvert^2$ | $s_\epsilon$ |
| $j_x$ (momentum) | $0, 1, 0, -1, 0, 1, -1, -1, 1$ | $\rho u_x$ | any |
| $q_x$ (heat flux) | $0, -2, 0, 2, 0, 1, -1, -1, 1$ | $-\rho u_x$ | $s_q$ |
| $j_y$ | $0, 0, 1, 0, -1, 1, 1, -1, -1$ | $\rho u_y$ | any |
| $q_y$ | $0, 0, -2, 0, 2, 1, 1, -1, -1$ | $-\rho u_y$ | $s_q$ |
| $p_{xx}$ (normal stress) | $0, 1, -1, 1, -1, 0, 0, 0, 0$ | $\rho(u_x^2 - u_y^2)$ | $s_\nu$ |
| $p_{xy}$ (shear stress) | $0, 0, 0, 0, 0, 1, -1, 1, -1$ | $\rho u_x u_y$ | $s_\nu$ |

The rows are orthogonal, so $M^{-1} = M^T D^{-1}$ with $D = \mathrm{diag}(9, 36, 36, 6, 12, 6, 12, 4, 4)$. $S$ is the diagonal matrix of the rates. $F$ is Guo's force term $F_i = w_i\bigl(3(c_i - u) + 9(c_i \cdot u)c_i\bigr) \cdot g$ for a body force $g$ per unit volume.

```pseudo id=main
MRT-D2Q9(n_x, n_y, S, K, init, g, walls)
L1  for each node x: (ρ, u) ← init(x); f(x) ← f^eq(ρ, u)
L2  repeat K times
L3      for each node x: ρ ← Σ f_i,  u ← (Σ c_i f_i + g/2) / ρ
L4          m ← M f
L5          m* ← m - S (m - m^eq(ρ, u)) + (I - S/2) M F(u, g)
L6          f* ← M^-1 m*
L7      for each node x and each i: f_i(x + c_i) ← f*_i(x); if x + c_i is beyond a wall, f_ī(x) ← f*_i(x)
L8  return ρ, u at every node
```

Line L3 computes the density and the velocity, with the half force shift of Guo's scheme. Line L4 maps the populations to moments; with the integer rows of $M$ this is a few additions and no multiplications. Line L5 is the collision: the conserved moments $\rho$, $j_x$ and $j_y$ equal their equilibrium (up to the force shift), so their rates have no effect, and each other moment moves toward its equilibrium by the fraction $s_k$. Line L6 maps back. Line L7 is the streaming step of the lattice Boltzmann method, periodic in $x$, with halfway bounce-back walls at $y = -\frac12$ and $y = n_y - \frac12$ when walls are on ($\bar\imath$ is the index with $c_{\bar\imath} = -c_i$).

The rates must lie in $(0, 2)$. The shear rate sets the kinematic viscosity

$$\nu = \frac13\Bigl(\frac1{s_\nu} - \frac12\Bigr),$$

so $s_\nu$ plays the role of $1/\tau$. The rate $s_e$ sets the bulk viscosity. The rate $s_q$ of the heat flux moments has no effect on the Navier-Stokes limit, but it changes the error terms, in particular at walls.

## Example

**One collision by hand.** Take a node at rest with $f_i = w_i$, and add $\frac1{100}$ to $f_1$ and to $f_3$ (two populations along $\pm x$). The moments are $\rho = \frac{51}{50}$, $e = -\frac{101}{50}$, $\epsilon = \frac{24}{25}$, $p_{xx} = \frac1{50}$, and the others are 0. The velocity is 0, so the equilibrium moments are $e^{\mathrm{eq}} = -2\rho = -\frac{51}{25}$, $\epsilon^{\mathrm{eq}} = \rho = \frac{51}{50}$ and $p_{xx}^{\mathrm{eq}} = 0$. Choose $s_e = s_\epsilon = 1$, $s_\nu = \frac54$ (so $\nu = 0.1$) and $s_q = \frac89$. Line L5 gives:

| moment | $m$ | $m^{\mathrm{eq}}$ | rate | $m^*$ |
|---|---|---|---|---|
| $\rho$ | $1.02$ | $1.02$ | any | $1.02$ |
| $e$ | $-2.02$ | $-2.04$ | 1 | $-2.04$ |
| $\epsilon$ | $0.96$ | $1.02$ | 1 | $1.02$ |
| $p_{xx}$ | $0.02$ | 0 | $\frac54$ | $-0.005$ |
| others | 0 | 0 |  | 0 |

The energy moments reach their equilibrium in one step, and the stress overshoots to $-0.005$, as any rate above 1 does. Line L6 gives $f^* = (\frac{34}{75}, \frac{269}{2400}, \frac{11}{96}, \frac{269}{2400}, \frac{11}{96}, \frac{17}{600}, \frac{17}{600}, \frac{17}{600}, \frac{17}{600}) \approx (0.45333, 0.11208, 0.11458, 0.11208, 0.11458, 0.02833, \ldots)$. BGK with $\tau = 0.8$ (the same viscosity) gives $(\frac{41}{90}, \frac{401}{3600}, \frac{41}{360}, \frac{401}{3600}, \frac{41}{360}, \frac{41}{1440}, \ldots) \approx (0.45556, 0.11139, 0.11389, \ldots, 0.02847)$: the same density and the same stress $-0.005$, but the energy moments also overshoot, to $e^* = -2.045$ and $\epsilon^* = 1.035$, because they relax at $\frac54$ instead of 1. The test file checks the MRT fractions.

**Poiseuille flow.** A channel of $n_y = 8$ nodes, one node wide and periodic in $x$, with halfway bounce-back walls and a force $g = 10^{-6}$ along $x$, run to steady state. The exact profile is $u(y) = \frac{g}{2\nu}(y + \frac12)(n_y - \frac12 - y)$. With $s_q = s_\nu$ (all nonconserved rates equal, which is BGK) the computed profile is the parabola plus a constant slip. With $s_q$ chosen so that $\Lambda = (\frac1{s_\nu} - \frac12)(\frac1{s_q} - \frac12) = \frac3{16}$, the slip goes away:

| $s_\nu$ ($\tau = 1/s_\nu$) | $\frac53$ (0.6) | $\frac54$ (0.8) | 1 (1.0) |
|---|---|---|---|
| slip $/g$ with $s_q = s_\nu$ | $-3.55$ | $-0.65$ | $0.25$ |
| $s_q$ for $\Lambda = \frac3{16}$ | $\frac8{19}$ | $\frac89$ | $\frac87$ |
| max error $/g$ with that $s_q$ | $1.8 \cdot 10^{-9}$ | $5.1 \cdot 10^{-10}$ | $4.5 \cdot 10^{-10}$ |

The BGK slips match the formula $s = g\bigl(2(\tau - \frac12) - \frac3{8(\tau - \frac12)}\bigr)$ of the lattice Boltzmann page. The remaining errors with $\Lambda = \frac3{16}$ are the convergence tolerance of the run, not a discretization error. These runs used $s_e = s_\epsilon = s_\nu$. This is a measurement; the result that the wall position depends on the rates only through $\Lambda$, and that $\Lambda = \frac3{16}$ puts it exactly halfway for this flow, is from the analysis of Ginzburg and d'Humières (2003) for two-rate schemes.

**Taylor-Green vortex.** On an $N \times N$ periodic lattice with $k = 2\pi/N$, $u_0 = 0.16/N$, $s_\nu = \frac54$ and $N^2/8$ steps, the relative max error of $u$ against $-u_0\cos kx\sin ky\,e^{-2\nu k^2 t}$ was:

| $s_q$ | $N = 8$ | $N = 16$ | $N = 32$ | observed orders |
|---|---|---|---|---|
| $\frac54$ (BGK) | 8.64e-2 | 2.11e-2 | 5.26e-3 | 2.03, 2.01 |
| 1.1 | 7.96e-2 | 1.95e-2 | 4.84e-3 | 2.03, 2.01 |
| $\frac89$ ($\Lambda = \frac3{16}$) | 6.63e-2 | 1.62e-2 | 4.02e-3 | 2.03, 2.01 |

The order is 2 for every $s_q$; the rate changes only the constant.

## Correctness

Proved in [the correctness file](proofs/correctness.md), in exact arithmetic: the rows of $M$ are orthogonal; $Mf^{\mathrm{eq}}$ equals the closed-form $m^{\mathrm{eq}}$ of the table; the collision of lines L3 to L6 keeps the density of each node and adds exactly $g$ to its momentum, for any rates of the conserved moments; with every rate equal to $1/\tau$ the collision is BGK with Guo forcing, term by term; and streaming permutes the populations, so the total mass is constant, and on a fully periodic lattice the total momentum grows by exactly $n_xn_yg$ per step. The tests check all of this with `fractions.Fraction`, and check the BGK reduction against an independent BGK collision on 500 random nodes.

The link to the Navier-Stokes equations with $\nu = \frac13(\frac1{s_\nu} - \frac12)$ is a consistency result from the [Chapman-Enskog expansion](/chapman-enskog-expansion/) (Lallemand and Luo 2000). It holds for small Mach and Knudsen numbers, and it is not proved here. The Taylor-Green table shows the second order in space that it predicts.

## Complexity

In the real-RAM model with $M$ lattice nodes (in this section $M$ is the node count, not the moment matrix), one step does a constant amount of work per node. Line L4 is a fixed set of about 30 additions and a few doublings, line L5 is 9 multiply-adds, plus the 9 force moments when $g \ne 0$, line L6 is about 30 additions and 9 divisions by constants, and line L7 moves 9 values. That is a few times the work of a BGK collision, and $\Theta(M)$ per step. $K$ steps cost $\Theta(KM)$. The lattice stores 9 populations per node, plus a second array for streaming, so the memory is $\Theta(M)$. Reaching a physical time $T$ with grid spacing $h$ in diffusive scaling takes $K \propto T/h^2$ steps, as for BGK.

## Properties

- **Exact conservation.** Mass is conserved exactly by every step, and momentum changes only by the force and by the walls.
- **Contains BGK.** With $S = \frac1\tau I$ the method is BGK, so every BGK result applies as a special case.
- **Free rates.** $s_e$ sets the bulk viscosity, $s_\epsilon$ and $s_q$ act only on nonhydrodynamic moments. Tuning them changes stability and wall errors, not the viscosity.
- **Galilean invariance and isotropy.** As for D2Q9 BGK, these hold only to second order in $u$; Lallemand and Luo (2000) analyse the dispersion and the isotropy of the D2Q9 MRT model.
- **Second order in space** for smooth flow, as measured above.

## Variants and improvements

- **Two-relaxation-time (TRT).** Ginzburg's TRT scheme uses one rate for all even moments and one for all odd moments. It is the simplest form of MRT that keeps the free parameter $\Lambda$, and $\Lambda = \frac3{16}$ is the choice that puts halfway bounce-back walls exactly halfway for Poiseuille flow (Ginzburg and d'Humières 2003).
- **Other bases.** The basis can use raw moments, central moments (moments in the frame moving with $u$) or cumulants. Central moment and cumulant schemes reduce the Galilean errors at high speed.
- **Three dimensions.** d'Humières et al. (2002) give D3Q15 and D3Q19 MRT models.
- **Turbulence.** An eddy viscosity from a [large eddy simulation](/large-eddy-simulation/) model enters by changing $s_\nu$ at each node.
- **Regularized and entropic schemes** are other ways to make the collision more stable at small viscosity.

## When to use it

Use MRT (or TRT) instead of BGK when the viscosity is small and BGK becomes unstable, when bounce-back walls must sit at a position that does not change with the viscosity (porous media, permeability computations), or when the bulk viscosity must differ from the shear viscosity. For smooth periodic flow at moderate viscosity, BGK is simpler and gives the same accuracy. MRT does not make the lattice Boltzmann method suitable for compressible flow or high Mach numbers.

## Pitfalls

- **A basis that is not the one of the equilibrium table.** The closed forms of $m^{\mathrm{eq}}$ hold only for the rows of $M$ in the table above, in the velocity order above. With another velocity numbering, permute the columns of $M$ too, and check $Mf^{\mathrm{eq}} = m^{\mathrm{eq}}$ before the first run.
- **Using $M^T$ as the inverse.** The rows are orthogonal but not normalized, so line L6 needs $M^T D^{-1}$, not $M^T$.
- **The force term in population space.** Adding $F$ after line L6 with the BGK factor $(1 - \frac1{2\tau})$ is wrong when the rates differ; the factor $(I - \frac{S}{2})$ must act in moment space on line L5.
- **Velocity without the half shift.** Line L3 must use $u = (\sum c_if_i + g/2)/\rho$. Without the shift the scheme is first order in the force.
- **Expecting exact walls for free.** With $s_q = s_\nu$ the wall slip of BGK remains. The wall position is exact only for the right $\Lambda$, and only for flows like Poiseuille flow whose profile is at most quadratic.
- **Rates outside $(0, 2)$.** A rate of 2 or more makes the moment grow instead of decay.

## Implementations

## History

Lattice Boltzmann models grew from lattice gas automata in the late 1980s. In 1992 d'Humières proposed a generalized lattice Boltzmann equation whose collision is a matrix acting in a basis of moments, in the same year that the single-rate BGK form of Qian, d'Humières and Lallemand and of Chen, Chen and Matthaeus appeared. BGK became the common choice because it is simple. Lallemand and Luo (2000) gave a full linear analysis of the D2Q9 MRT model, with the basis above, and showed that the free rates improve its stability. d'Humières, Ginzburg, Krafczyk, Lallemand and Luo (2002) extended the method to three dimensions, and Ginzburg and coworkers developed the two-relaxation-time form and the analysis of the wall position.

## References
