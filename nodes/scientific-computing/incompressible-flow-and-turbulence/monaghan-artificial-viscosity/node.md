---
tag: 2F76S1
kind: technique
slug: monaghan-artificial-viscosity
name: Monaghan artificial viscosity
aliases:
- SPH artificial viscosity
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: Adds a pairwise viscous pressure between approaching SPH particles so shocks are captured without particles passing through each other.
prereqs: [smoothed-particle-hydrodynamics, sph-smoothing-kernel]
see_also: [euler-equations-of-gas-dynamics, rankine-hugoniot-conditions, exact-riemann-solver, riemann-problem, godunov-method, weakly-compressible-sph, lax-entropy-condition]
sources:
  - paper: doi:10.1016/0021-9991(83)90036-0
    title: "J. J. Monaghan and R. A. Gingold, Shock simulation by the particle method SPH, Journal of Computational Physics 52 (1983) 374-389"
  - paper: doi:10.1146/annurev.aa.30.090192.002551
    title: "Joseph J. Monaghan, Smoothed particle hydrodynamics, Annual Review of Astronomy and Astrophysics 30 (1992) 543-574"
    locator: "the artificial viscosity with alpha and beta and its use in the momentum and energy equations"
  - paper: "J. J. Monaghan, SPH and Riemann solvers, Journal of Computational Physics 136 (1997) 298-307"
    locator: "the signal velocity form of the viscosity"
  - paper: doi:10.1006/jcph.1997.5690
    title: "J. P. Morris and J. J. Monaghan, A switch to reduce SPH viscosity, Journal of Computational Physics 136 (1997) 41-50"
  - paper: "D. S. Balsara, von Neumann stability analysis of smoothed particle hydrodynamics, suggestions for optimal algorithms, Journal of Computational Physics 121 (1995) 357-372"
    locator: "the shear limiter of the viscosity"
  - paper: doi:10.1111/j.1365-2966.2010.17158.x
    title: "Lee Cullen and Walter Dehnen, Inviscid smoothed particle hydrodynamics, Monthly Notices of the Royal Astronomical Society 408 (2010) 669-683"
  - paper: doi:10.1006/jcph.1997.5776
    title: "Joseph P. Morris, Patrick J. Fox and Yi Zhu, Modeling low Reynolds number incompressible flows using SPH, Journal of Computational Physics 136 (1997) 214-226"
  - paper: doi:10.1088/0034-4885/68/8/R01
    title: "Joseph J. Monaghan, Smoothed particle hydrodynamics, Reports on Progress in Physics 68 (2005) 1703-1759"
---

The Monaghan artificial viscosity is the term that lets [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) (SPH) compute shocks. The inviscid SPH equations have no mechanism that turns kinetic energy into heat at a shock, so the particles behind a shock oscillate, and in a strong collision particle streams pass through each other. Monaghan and Gingold (1983) added a viscous pressure $\Pi_{ij}$ to every pair of particles that approach each other. It has a linear term, which acts like a bulk and shear viscosity, and a quadratic term, which acts like the von Neumann-Richtmyer viscosity and stops interpenetration. The pairwise form keeps the exact momentum conservation of SPH, and the heat it makes is exactly the kinetic energy it removes.

## In plain words

When two SPH particles move toward each other fast, as they do in a shock, the plain equations let them overshoot and ring, or even pass through each other. The artificial viscosity adds an extra repulsive pressure between any two particles that are approaching. The pressure grows with the closing speed: in proportion to it for slow approach, and with its square for fast approach. The force pushes the pair apart equally and oppositely, so total momentum does not change. The kinetic energy that the force removes is added to the internal energy of the pair, so total energy does not change either. Particles that move apart feel no extra force. The result is a shock that is a few particle spacings wide, with the correct jump in density, velocity and pressure.

## When it applies

- SPH for compressible flow: gas dynamics, astrophysics, impacts and explosions. The [Euler equations](/euler-equations-of-gas-dynamics/) have discontinuous solutions, and a particle method needs some dissipation to find the physically correct one.
- [Weakly compressible SPH](/weakly-compressible-sph/) for liquids, where a small linear term ($\alpha$ of about 0.01 to 0.1, $\beta = 0$) damps pressure noise and keeps the particles in order.
- Any pairwise particle scheme in which the force between two particles depends on their distance and the kernel gradient, so that a pair term can be added without changing the conservation structure.
- It is not a physical viscosity model. For a real viscous fluid, use a physical viscous term, such as the one of Morris, Fox and Zhu (1997); the artificial term adds an effective viscosity proportional to $\alpha h \bar c$ that does not converge to a prescribed value of $\nu$.

## The template

```pseudo id=main
VISCOUS-PAIR-TERM(i, j, x, v, ρ, c, h; α, β, ε)
L1  x_ij ← x_i - x_j;  v_ij ← v_i - v_j
L2  if v_ij · x_ij ≥ 0 then return 0                     ▷ the pair is moving apart
L3  h̄ ← (h_i + h_j)/2;  c̄ ← (c_i + c_j)/2;  ρ̄ ← (ρ_i + ρ_j)/2
L4  μ ← h̄ (v_ij · x_ij) / (|x_ij|^2 + ε h̄^2)            ▷ μ < 0
L5  Π ← (-α c̄ μ + β μ^2) / ρ̄                            ▷ Π > 0
L6  a_i -= m_j Π ∇_i W_ij;  a_j += m_i Π ∇_i W_ij
L7  ė_i += (1/2) m_j Π v_ij · ∇_i W_ij;  ė_j += (1/2) m_i Π v_ij · ∇_i W_ij
```

The holes are the two coefficients $\alpha$ and $\beta$ and the small number $\varepsilon$. The values $\alpha = 1$, $\beta = 2$ and $\varepsilon = 0.01$ are the usual choice for gas dynamics and are used on the [SPH page](/smoothed-particle-hydrodynamics/). They are rules of thumb found by trial on shock tubes, not values that follow from a theory. The term is added for each pair inside the kernel support, in the same loop as the pressure force; in the SPH momentum equation it is simply added to $P_i/\rho_i^2 + P_j/\rho_j^2$.

Line L2 switches the term off for receding pairs, so expansion waves are not smeared. Line L4 measures the closing speed: $\mu$ is about $h\,(v_{ij} \cdot x_{ij})/|x_{ij}|^2$, a velocity difference times $h/|x_{ij}|$, which is close to the velocity divergence times $h$. The term $\varepsilon\bar h^2$ keeps $\mu$ finite when two particles nearly coincide. Line L5 is the viscous pressure. The linear term $-\alpha\bar c\mu$ gives an effective viscosity proportional to $\alpha h\bar c$, which spreads the shock. The quadratic term $\beta\mu^2$ is large only when the closing speed is large compared with $\bar c$, as in a strong shock or a collision of two streams; it is the particle form of the von Neumann-Richtmyer viscosity. Lines L6 and L7 apply the term with the antisymmetric kernel gradient.

**Why it conserves momentum and only heats.** Line L6 changes $m_iv_i$ by $-m_im_j\Pi\nabla_iW_{ij}$ and $m_jv_j$ by the opposite amount, so the total momentum is unchanged. The rate of change of the kinetic energy of the pair is $m_iv_i \cdot a_i + m_jv_j \cdot a_j = -m_im_j\Pi\,v_{ij} \cdot \nabla_iW_{ij}$, and line L7 adds exactly $m_im_j\Pi\,v_{ij} \cdot \nabla_iW_{ij}$ to the internal energy. For a radial kernel, $\nabla_iW_{ij} = W'(|x_{ij}|)\,x_{ij}/|x_{ij}|$ with $W' \le 0$, so $v_{ij} \cdot \nabla_iW_{ij} = W'\,(v_{ij} \cdot x_{ij})/|x_{ij}| \ge 0$ for an approaching pair. With $\mu < 0$ both terms of $\Pi$ are positive. So the viscosity always turns kinetic energy into internal energy and never the reverse, which is the discrete form of the entropy condition at a shock.

**Hand example.** Take two particles in 1D with $m = 1$, $h = 1$, $\rho = 1$ and $c = 1$, at distance $x_{ij} = 1$ and with closing velocity $v_{ij} = -1$. Line L4 gives $\mu = -1/1.01 = -0.990099$. Line L5 gives

$$\Pi = 0.990099 + 2 \cdot 0.980296 = 2.950690.$$

The cubic spline has $\frac{dW}{dr}(1) = \frac23(-3 + \frac94) = -\frac12$, so $\nabla_iW_{ij} = -\frac12$. Line L6 gives $a_i = +1.475345$, a push of $i$ away from $j$, and $a_j = -1.475345$. Line L7 gives $\dot e_i = \dot e_j = \frac12 \cdot 2.950690 \cdot \frac12 = 0.737673$. The kinetic energy changes at the rate $v_i a_i + v_j a_j = v_{ij}a_i = -1.475345$, which is minus the sum of the two heating rates.

## Classic examples

**The Sod shock tube.** The standard test is the [Riemann problem](/riemann-problem/) of Sod: $(\rho, v, P) = (1, 0, 1)$ on the left and $(0.125, 0, 0.1)$ on the right, $\gamma = 1.4$. The run below used the code of the [SPH page](/smoothed-particle-hydrodynamics/) with 80 equal-mass particles on $[-0.75, 0]$, leapfrog with $\Delta t = 0.3\min h/1.2$, to $t = 0.2$, and compared with the [exact Riemann solution](/exact-riemann-solver/). The error is the mean absolute density error on $-0.5 < x < 0.5$; the overshoot is the largest velocity in $0.1 < x < 0.4$ minus the exact post-shock velocity 0.92745.

| $(\alpha, \beta)$ | (1, 2) | (0.5, 1) | (1, 0) | (0.1, 0.2) | (0, 0) |
|---|---|---|---|---|---|
| density error | 0.0134 | 0.0129 | 0.0124 | 0.0167 | 0.0470 |
| velocity overshoot | 0.041 | 0.050 | 0.027 | 0.340 | 1.770 |

Without viscosity the post-shock state is noise, with velocity errors larger than the flow itself. With a small viscosity the shock rings. Every choice with $\alpha$ from 0.5 to 1 gives a clean shock; for this weak shock the quadratic term is not needed, and in this run it gave a slightly larger error. The total energy changed by about $4 \cdot 10^{-5}$ of its value in all runs, which is the time-stepping error, because the viscosity itself conserves energy.

**Strong shocks and colliding streams.** In a Mach 10 or stronger shock, or when two gas streams collide, the closing speed is many times the sound speed in the cold gas. Then $\alpha\bar c\mu$ is small next to the momentum flux and particles from the two sides interpenetrate. The quadratic term grows like the square of the closing speed and stops this; this is the reason for $\beta = 2$ in astrophysical codes. The [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/) give the exact jumps to compare with.

**Liquids with weakly compressible SPH.** In dam break and sloshing problems the flow is subsonic, and an $\alpha$ between about 0.01 and 0.1 with $\beta = 0$ is used to damp the acoustic noise of the stiff equation of state. Here the term acts as a numerical viscosity, and the Reynolds number of the run depends on it.

**Comparison with Riemann solvers.** In [Godunov](/godunov-method/) type finite volume schemes the dissipation comes from upwinding. Monaghan (1997) wrote the SPH viscosity in the same form, as a signal speed times a velocity jump, which shows that the two approaches are close.

## Variations

- **Signal velocity form.** Monaghan (1997) writes $\Pi_{ij} = -\frac{\alpha}{2}\,v_{\rm sig}\,w_{ij}/\bar\rho_{ij}$, with $w_{ij} = v_{ij} \cdot x_{ij}/|x_{ij}|$ and a signal speed $v_{\rm sig} = c_i + c_j - \beta w_{ij}$. It has the same linear and quadratic parts, and it extends to an artificial thermal conductivity.
- **Time-dependent coefficients.** Morris and Monaghan (1997) give each particle its own $\alpha_i$, which grows where the flow is compressed ($\nabla \cdot v < 0$) and decays back to a small floor over a few sound crossing times of $h$. Away from shocks the viscosity is then small.
- **Cullen and Dehnen switch.** Cullen and Dehnen (2010) use the time derivative of $\nabla \cdot v$ to detect a shock before it arrives, and set $\alpha$ near zero elsewhere; it gives nearly inviscid SPH away from shocks.
- **Shear limiter.** Balsara (1995) multiplies $\Pi_{ij}$ by a factor $|\nabla \cdot v|/(|\nabla \cdot v| + |\nabla \times v|)$, which reduces the unwanted viscosity in shear flows and rotating disks.
- **Physical viscosity instead.** For a viscous liquid with a given $\nu$, use a physical viscous term, such as the one of Morris, Fox and Zhu (1997), and keep at most a small artificial term for stability.

## Pitfalls

- **Viscosity on receding pairs.** Without the test on line L2 the term also acts in expansions, where it smears rarefaction waves and adds heat that should not be there.
- **Dropping $\varepsilon$.** Without $\varepsilon\bar h^2$ on line L4, $\mu$ blows up when two particles come very close, and the time step must collapse.
- **Unequal pair terms.** If $\Pi_{ij}$ is computed with values of $i$ only, such as $h_i$ and $c_i$, then $\Pi_{ij} \neq \Pi_{ji}$ and momentum is no longer conserved. Use symmetric averages, as on line L3.
- **Leaving the heating out.** Applying line L6 without line L7 removes kinetic energy without heating the gas. Total energy then falls at every shock and the post-shock temperature is wrong.
- **Too much viscosity in shear flows.** The linear term acts also in pure shear, where $v_{ij} \cdot x_{ij} < 0$ for half the pairs. Rotating disks and vortices decay too fast; use a switch or a limiter.
- **Treating $\alpha$ and $\beta$ as physical constants.** The best values depend on the kernel, the ratio $h/\Delta x$ and the test. Check them on a shock tube with the same setup as the production run.
- **The time step.** The viscosity adds its own stability limit, which shrinks as $\alpha\bar c$ and $\beta\max|\mu|$ grow. A step chosen from the sound speed alone can be unstable in a strong shock; include the signal speed $c + \alpha c + \beta\max|\mu|$, up to constants, in the Courant limit.

## Exercises

1. Show that $\Pi_{ij} \ge 0$ for every approaching pair and that the total energy $\sum m_i(\frac12 v_i^2 + e_i)$ is unchanged by lines L6 and L7 in the semi-discrete system.
2. For two particles in 1D at distance $h$, with $\varepsilon = 0$, find the closing speed at which the quadratic term equals the linear term, for $\alpha = 1$ and $\beta = 2$.
3. Run the Sod test with $(\alpha, \beta) = (1, 2)$ at 80 and 160 particles on the left, and check that the shock width, measured in particle spacings, stays about the same.

## References
