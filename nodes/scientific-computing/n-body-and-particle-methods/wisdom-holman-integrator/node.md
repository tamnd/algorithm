---
tag: JQMB4C
kind: algorithm
slug: wisdom-holman-integrator
name: Wisdom-Holman integrator
aliases:
- mixed-variable symplectic integrator
- Wisdom-Holman map
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: A symplectic splitting for planetary systems that advances the Kepler motion of each planet exactly and adds the mutual perturbations as kicks.
model: real-ram
complexity:
  vars: {N: the number of bodies}
  time: {step: "Θ(N^2)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true, implicit: false, one_step: true, order: "2", symplectic: true, symmetric: true}
history:
  year: 1991
  people: [Jack Wisdom, Matthew Holman]
  note: Wisdom and Holman split the planetary Hamiltonian in Jacobi coordinates into Kepler motions and interactions, and used the map for integrations of the outer solar system over a billion years.
prereqs: [symplectic-integrators, operator-splitting, gravitational-n-body-problem]
see_also: [verlet-integration, hamiltonian-systems, shadow-hamiltonian, backward-error-analysis, newton-raphson-method, hermite-n-body-integrator, kustaanheimo-stiefel-regularization, block-time-steps]
sources:
  - paper: doi:10.1086/115978
    title: "Jack Wisdom and Matthew Holman, Symplectic maps for the n-body problem, Astronomical Journal 102(4), 1991, 1528-1538"
    locator: the splitting in Jacobi coordinates and the kick-drift-kick map
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, 2nd edition, Springer, 2006
    locator: Chapter II (splitting methods) and Chapter IX (backward error analysis)
  - book: isbn:9780943396200
    title: J. M. A. Danby, Fundamentals of Celestial Mechanics, 2nd edition, Willmann-Bell, 1988
    locator: the f and g functions and the solution of Kepler's equation
---

The Wisdom-Holman integrator advances a planetary system, a star of mass $m_0$ with planets of much smaller masses, by splitting the Hamiltonian into two parts that can each be solved exactly. The first part is a sum of independent Kepler problems, one per planet, in Jacobi coordinates; its flow moves each planet along its exact conic in closed form. The second part, the mutual pull of the planets, depends on the positions only; its flow is a kick of the velocities. The step is the symmetric composition kick-drift-kick of [operator splitting](/operator-splitting/), as in [leapfrog](/verlet-integration/), so the map is [symplectic](/symplectic-integrators/), time-symmetric and of second order. But because the large Kepler force is treated exactly, the error is of order $\varepsilon h^2$ with $\varepsilon$ the ratio of the planet masses to $m_0$, and steps of a twentieth of an orbit are common. It is the standard method for long integrations of planetary systems.

## In plain words

In a planetary system, each planet mostly goes around the star on a fixed ellipse, and the planets only pull each other a little. The motion on an ellipse can be computed exactly for any time, with a formula.

So the method alternates two simple moves. First it gives each planet a small push from the other planets, for half a step. Then it moves each planet along its own ellipse around the star for a full step, exactly. Then it gives the second half push. The only error comes from doing the two moves one after the other instead of at the same time, and that error is small because the pushes are small. The steps can be long, and the errors in energy stay bounded over billions of orbits.

## The problem

The input is a star (body 0) and planets $1, \ldots, N - 1$ with masses $m_i$, positions $\mathbf{x}_i$ and velocities $\mathbf{v}_i$, $G = 1$, and a time step $h$. The output is an approximation of the state at time $t + h$ of the [gravitational N-body problem](/gravitational-n-body-problem/), without softening.

**Jacobi coordinates.** Let $\eta_i = m_0 + \cdots + m_i$ and let $\mathbf{X}_i$ be the center of mass of bodies $0, \ldots, i$. Set $\mathbf{x}'_i = \mathbf{x}_i - \mathbf{X}_{i-1}$ for $i \ge 1$ and $\mathbf{x}'_0 = \mathbf{X}_{N-1}$, and the same for velocities. With the masses $m'_i = m_i \eta_{i-1} / \eta_i$ the kinetic energy is diagonal, and the Hamiltonian is $H = H_K + H_I$ with

$$H_K = \frac{|\mathbf{p}'_0|^2}{2\eta_{N-1}} + \sum_{i \ge 1} \left( \frac{|\mathbf{p}'_i|^2}{2 m'_i} - \frac{G m'_i \eta_i}{r'_i} \right), \qquad H_I = -\sum_{i < j} \frac{G m_i m_j}{|\mathbf{x}_i - \mathbf{x}_j|} + \sum_{i \ge 1} \frac{G m'_i \eta_i}{r'_i}.$$

The flow of $H_K$ is a free motion of the center of mass and, for each planet, a Kepler orbit $\ddot{\mathbf{x}}'_i = -\mu_i \mathbf{x}'_i / r'^3_i$ with $\mu_i = G \eta_i$. The part $H_I$ depends only on positions, and it is of the size of the planet-planet terms, smaller than $H_K$ by a factor of about $\varepsilon$.

## The algorithm

```pseudo id=main
WISDOM-HOLMAN-STEP(x, v, h)
L1  (x', v') ← JACOBI(x, v)
L2  v' ← v' + (h/2) KICK(x')
L3  for i ← 1 to N-1: (x'_i, v'_i) ← KEPLER(x'_i, v'_i, G η_i, h)
L4  x'_0 ← x'_0 + h v'_0
L5  v' ← v' + (h/2) KICK(x')
L6  return CARTESIAN(x', v')

KICK(x'):
L7      a' ← JACOBI(Newtonian accelerations at CARTESIAN(x')), a'_0 ← 0
L8      a'_i ← a'_i + G η_i x'_i / r'_i³ for i ≥ 1; return a'

KEPLER(x, v, μ, Δt):  a ← 1/(2/r - v²/μ), n ← sqrt(μ/a³), e_c ← 1 - r/a, e_s ← x·v / sqrt(μ a)
L9      solve n Δt = ΔE - e_c sin ΔE + e_s (1 - cos ΔE) for ΔE by safeguarded Newton
L10     return (f x + g v, ḟ x + ġ v)
```

Lines L2 and L5 are the two half kicks with the flow of $H_I$. Because $\mathbf{x}' = J \mathbf{x}$ for a fixed linear map $J$, the Jacobi accelerations of the full potential are $J$ applied to the Cartesian ones (line L7); line L8 removes the Kepler part that $H_K$ already contains. Lines L3 and L4 are the exact flow of $H_K$ for the time $h$. Line L9 is Kepler's equation in differences of the eccentric anomaly $E$, with $e_c = e \cos E_0$ and $e_s = e \sin E_0$; its left side is increasing in $\Delta E$, and its root lies within 2 of $n \Delta t$, so Newton's method with a bisection safeguard ([Newton-Raphson](/newton-raphson-method/)) always converges. Line L10 uses the Gauss $f$ and $g$ functions,

$$f = 1 - \frac{a}{r_0}(1 - \cos \Delta E), \quad g = \Delta t - \frac{\Delta E - \sin \Delta E}{n}, \quad \dot f = -\frac{\sqrt{\mu a}\, \sin \Delta E}{r r_0}, \quad \dot g = 1 - \frac{a}{r}(1 - \cos \Delta E),$$

with $r = a(1 - e_c \cos \Delta E + e_s \sin \Delta E)$. The code is for bound orbits only; hyperbolic planets need the universal variables.

## Example

Take the star $m_0 = 1$ at the origin, planet 1 with $m_1 = 10^{-3}$ at $(1, 0, 0)$, and planet 2 with $m_2 = 3 \times 10^{-4}$ at $(0, 1.6, 0.05)$, on near-circular orbits. The Jacobi vectors are $\mathbf{x}'_1 = (1, 0, 0)$ and $\mathbf{x}'_2 = (-0.000999, 1.6, 0.05)$, with $\mu_1 = 1.001$ and $\mu_2 = 1.0013$. The Jacobi acceleration of planet 1 is $(-1.001045, -0.0000456, -0.0000014)$, and the kick of line L8 is $(-0.0000446, -0.0000456, -0.0000014)$: the exact Kepler part takes away all but a part in $10^4$ of the force.

Over one orbit of planet 1 ($T = 2\pi$), compared with a classical Runge-Kutta integration with 6000 steps, the largest position error is (measurement with this implementation):

| steps per orbit | 20 | 40 | 80 |
|---|---|---|---|
| error, planet masses $10^{-3}$ and $3 \times 10^{-4}$ | $1.17 \times 10^{-5}$ | $2.92 \times 10^{-6}$ | $7.31 \times 10^{-7}$ |
| error, planet masses ten times larger | $2.35 \times 10^{-4}$ | $5.88 \times 10^{-5}$ | $1.47 \times 10^{-5}$ |

Halving the step divides the error by 4, as for a second-order method. Over 10 orbits with 40 steps per orbit, the largest relative energy error $|E(t) - E(0)| / |E(0)|$ is $1.9 \times 10^{-6}$, against $2.1 \times 10^{-4}$ for Cartesian leapfrog with the same step (measurement).

## Correctness

The Jacobi map is linear with $\mathbf{x}' = J\mathbf{x}$, and the kinetic energy in Jacobi velocities is $\sum m'_i |\mathbf{v}'_i|^2 / 2$ plus the term of the center of mass, so $H = H_K + H_I$ holds exactly with $H_I$ a function of positions only (Lemma 1 of the proof file). The flow of $H_I$ is the kick of lines L7 and L8 (Lemma 2), and lines L9 and L10 give the exact Kepler flow from the eccentric anomaly (Lemma 3). The step is the composition $\varphi^{I}_{h/2} \circ \varphi^{K}_h \circ \varphi^{I}_{h/2}$ of exact Hamiltonian flows. So it is symplectic, it is symmetric ($\Phi_{-h} = \Phi_h^{-1}$), and it is of second order by the Baker-Campbell-Hausdorff formula (theorem). By [backward error analysis](/backward-error-analysis/), it is the exact flow of a modified Hamiltonian $\tilde H = H + h^2 H_2 + O(h^4)$, where $H_2$ is a combination of the Poisson brackets $\{H_K, \{H_K, H_I\}\}$ and $\{H_I, \{H_I, H_K\}\}$. Both contain $H_I$, so $\tilde H - H = O(\varepsilon h^2)$, and the energy error stays bounded by $O(\varepsilon h^2)$ over exponentially long times (theorem, under the assumptions of backward error analysis, see [shadow Hamiltonian](/shadow-hamiltonian/)).

## Complexity

In the [real RAM](/real-ram/) model with a fixed number of Newton iterations, one step costs $\Theta(N^2)$ for the Newtonian accelerations of one kick (the second kick of a step is the first of the next, when steps are joined), $\Theta(N)$ for the Kepler drifts and $\Theta(N)$ for the coordinate changes. The extra space is $\Theta(N)$. In practice the Newton solve converges in a few iterations from a good start, and for a few planets the Kepler drifts dominate the cost.

## Properties

- **Symplectic, symmetric and second order.** Like leapfrog, but with an error constant smaller by a factor of about $\varepsilon$.
- **Exact for one planet.** With one planet $H_I = 0$, so the map gives the exact two-body motion for any step (tested).
- **Bounded energy error.** For the example, the relative energy error over 50 orbits stays below $2 \times 10^{-6}$ and does not grow (measurement). The total momentum is conserved up to rounding, because the kick does not change $\mathbf{v}'_0$.
- **Time-reversible.** Running the map backward with reversed velocities returns to the start up to rounding.

## Variants and improvements

- **Democratic heliocentric coordinates.** Heliocentric positions with barycentric velocities, which split $H$ into Kepler, interaction and a "jump" part; used for close encounters in the code of Duncan, Levison and Lee.
- **Symplectic correctors.** A near-identity change of variables at the output removes the $O(\varepsilon h^2)$ error, leaving $O(\varepsilon^2 h^2 + \varepsilon h^4)$ (Wisdom, Holman and Touma 1996).
- **Higher-order splittings.** Compositions of the kick and drift with more stages, designed for $\varepsilon \ll 1$, as by McLachlan and by Laskar and Robutel.
- **Close encounters.** The hybrid method of Chambers switches a close pair of planets to an adaptive integrator, and the code of Duncan, Levison and Lee splits the interaction by distance.
- **Fast implementations.** The WHFast code of Rein and Tamayo uses universal Stumpff functions for the Kepler step and compensated summation.

## When to use it

Use it for long integrations of planetary systems, satellite systems and other systems dominated by one central mass, where the orbits stay well separated, as in the stability of the solar system or of exoplanet systems. Use [Hermite integrators](/hermite-n-body-integrator/) with [block time steps](/block-time-steps/) for star clusters without a dominant mass, and [Kustaanheimo-Stiefel regularization](/kustaanheimo-stiefel-regularization/) for close pairs.

## Pitfalls

- **Close encounters.** When two planets come close, $H_I$ is no longer small and the fixed step is too long; the energy error jumps.
- **Pericenter resolution.** For eccentric orbits, the step must resolve the pericenter passage even though the Kepler part is exact; otherwise the kick at a far point misses the fast change of $H_I$, and symplectic maps show step-size resonances.
- **Changing the step.** A symplectic map with a variable step loses its bounded energy error, unless the step change is itself done symplectically.
- **Output at the wrong point.** The state between the half kick and the drift is not the state at a full time; synchronize with a final half kick before output.
- **Unbound orbits.** The $f$ and $g$ functions of the eccentric anomaly fail for $1/a \le 0$; ejected bodies need universal variables.
- **Cancellation in the kick.** Line L8 subtracts two nearly equal terms of size $\mu_i / r'^2_i$; for very small masses compute the planet-planet terms and the indirect term directly instead.

## Implementations

## History

Wisdom and Holman (1991) introduced the map, in Jacobi coordinates, and used it to integrate the outer planets of the solar system for a billion years. It extended Wisdom's earlier mapping methods for asteroids, which averaged the short-period terms. Kinoshita, Yoshida and Nakai proposed a related splitting the same year. The symplectic correctors, the democratic heliocentric form and the hybrid schemes followed in the 1990s, and the method is now the basis of planetary integrators such as the MERCURY, SWIFT and REBOUND packages.

## References
