---
tag: CX3297
kind: algorithm
slug: implicit-monte-carlo
name: Implicit Monte Carlo
aliases:
- Fleck-Cummings method
area: scientific-computing/particle-transport
level: advanced
summary: Solves thermal radiation transport coupled to a material energy equation by Monte Carlo, treating part of the absorption and reemission as effective scattering so large time steps stay stable.
model: real-ram
complexity:
  vars: {N: the number of particles per time step, K: the mean number of collisions per particle and step, S: the number of time steps}
  time: {average: O(S N K)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, exact: false, iterative: true, conservative: true}
history:
  year: 1971
  people: [Joseph A. Fleck, Jr., J. D. Cummings]
  note: Fleck and Cummings published the method in 1971. Larsen and Mercier showed in 1987 that it can violate the maximum principle for large time steps.
prereqs: [analog-monte-carlo-transport, backward-euler-method]
see_also: [backward-euler-method, stiff-ode-problem, a-stability, analog-monte-carlo-transport, implicit-capture, diffusion-approximation-of-transport, operator-splitting, heat-equation]
sources:
  - paper: doi:10.1016/0021-9991(71)90015-5
    title: J. A. Fleck, Jr. and J. D. Cummings, An implicit Monte Carlo scheme for calculating time and frequency dependent nonlinear radiation transport, Journal of Computational Physics 8(3), 1971, 313-342
    locator: the time discretization of the coupled equations, the Fleck factor and effective scattering
  - paper: doi:10.1016/0021-9991(87)90019-2
    title: Edward W. Larsen and Bertrand Mercier, Analysis of a Monte Carlo method for nonlinear radiative transfer, Journal of Computational Physics 71(1), 1987, 50-64
    locator: the maximum principle, which holds for small time steps and can fail for large ones
  - paper: doi:10.1080/23324309.2016.1138132
    title: Allan B. Wollaber, Four decades of implicit Monte Carlo, Journal of Computational and Theoretical Transport 45(1-2), 2016, 1-70
    locator: a review of the method, its derivation, its accuracy and its variants
---

Implicit Monte Carlo (IMC) solves the equations of thermal radiation: the radiative transfer equation for the photon intensity, coupled to an energy equation for the material that absorbs and emits the photons. The coupling is stiff, because the emission grows like $T^4$ and the material can absorb and reemit energy many times in one time step. A Monte Carlo method that takes the emission from the temperature at the start of the step (explicit coupling) oscillates and can give negative temperatures for large steps. Fleck and Cummings linearized the emission in time, which gives a factor $f = 1/(1 + \beta c \sigma \Delta t)$, the Fleck factor: in each step only the fraction $f$ of the absorptions is real, and the rest is replaced by effective scattering, absorption and immediate reemission in the same step. The particles are then followed as in [analog Monte Carlo transport](/analog-monte-carlo-transport/) with a modified medium. The method is a semi-implicit time discretization in the spirit of the [backward Euler method](/backward-euler-method/) for a [stiff problem](/stiff-ode-problem/), not an exact one. It is placed in particle transport, next to neutron Monte Carlo, because the transport part is the same random walk.

## In plain words

Hot matter glows, and the light it gives off heats other matter, which glows in turn. Light moves very fast and the glow grows very quickly with temperature, so a simulation with long time steps can go wrong: cold matter takes in so much light in one step that it gets hotter than its source, and then it sends out too much in the next step.

Implicit Monte Carlo fixes this with a guess about the future. It estimates how much of the light that the matter takes in during the step will come out again before the step ends. That part is not stored as heat. Instead, the light simply bounces on, like a scattering. Only the rest heats the matter. The steps then stay calm, even when they are long.

## The problem

In the grey case (one frequency group), the radiation intensity $I(r, \Omega, t)$ and the material temperature $T(r, t)$ obey

$$\frac{1}{c}\frac{\partial I}{\partial t} + \Omega \cdot \nabla I + \sigma I = \frac{\sigma\, a c T^4}{4\pi}, \qquad c_v \frac{\partial T}{\partial t} = \sigma\Big(\int I\, d\Omega - a c T^4\Big),$$

where $c$ is the speed of light, $a$ the radiation constant, $\sigma$ the absorption opacity in $\mathrm{cm}^{-1}$ (which depends on $T$) and $c_v$ the heat capacity per unit volume. The radiation energy density is $E_r = \frac{1}{c}\int I\, d\Omega$, and the equilibrium value is $E_r = a T^4$. Real problems add frequency dependence, physical scattering, material motion and boundaries. The model problem of this page is an infinite uniform zone, where space and direction drop out:

$$\frac{dE_r}{dt} = c\sigma (a T^4 - E_r), \qquad c_v \frac{dT}{dt} = c\sigma(E_r - a T^4),$$

and $E_r + c_v T$ is constant. Its solution tends to the equilibrium with $a T^4 + c_v T = E_r(0) + c_v T(0)$, and the maximum principle holds: $T(t)$ stays between the smallest and the largest of $T(0)$ and the radiation temperature $(E_r(0)/a)^{1/4}$.

## The algorithm

```pseudo id=main
IMC-STEP(T, census, Δt)                     ▷ census: list of particle energies; data frozen at T
L1  β ← 4 a T³ / c_v,  f ← 1 / (1 + β c σ Δt)       ▷ the Fleck factor
L2  E_em ← f c σ a T⁴ Δt; emit particles with this total energy, birth times uniform in the step
L3  for each particle (w, t_left) of the census and of the emission do
L4      loop
L5          d ← -ln(ξ)/σ; if d ≥ c t_left then put w in the new census; break
L6          t_left ← t_left - d/c
L7          with probability f: E_abs ← E_abs + w; break            ▷ real absorption
L8          otherwise effective scattering: a new isotropic direction, go on
L9  T ← T + (E_abs - E_em) / c_v                    ▷ material energy balance
L10 (one zone only) merge the census into equal-weight particles
```

Line L1 freezes the data at the start of the step. Line L2 emits the energy that the linearized material equation predicts. In a code with space, line L2 also samples the position and an isotropic direction, and line L5 compares the distance to collision with the distances to census and to the faces of the cell. Lines L7 and L8 split each collision into a real absorption with probability $f$ and an effective scattering with probability $1 - f$. Line L9 is exact energy bookkeeping: every unit of energy that left the material in line L2 and did not come back in line L7 is in the census or has left the system. Codes often replace line L7 with continuous absorption, a weight reduction along the path in the manner of [implicit capture](/implicit-capture/), which lowers the noise of the absorbed energy.

**Where the Fleck factor comes from.** Write $u = a T^4$ for the equilibrium radiation energy density. The material equation gives $du/dt = \beta\, c\sigma(E_r - u)$ with $\beta = du/d(c_v T) = 4aT^3/c_v$. A backward Euler step with $\beta$ frozen, $u^{n+1} = u^n + \beta c\sigma \Delta t (E_r - u^{n+1})$, gives $u^{n+1} = f u^n + (1 - f) E_r$. Putting this $u$ into the emission term of the radiation equation gives

$$\frac{dE_r}{dt} = c\sigma f u^n - c\sigma f E_r,$$

an emission $f c \sigma u^n$, an absorption with opacity $f\sigma$, and the remaining opacity $(1 - f)\sigma$ as scattering. This is what lines L2, L7 and L8 implement.

## Example

**The Fleck factor by hand.** With $a = c = \sigma = c_v = 1$, $T = 1$ and $\Delta t = 0.25$: $\beta = 4$, $f = 1/(1 + 4 \cdot 0.25) = 0.5$ and $E_{\mathrm{em}} = 0.5 \cdot 0.25 = 0.125$. Half of the collisions in the step are real absorptions.

**Explicit coupling against IMC.** Start with $T = 1$ and $E_r = 0$ in the same units, so the equilibrium has $T + T^4 = 1$, $T = 0.7245$. Take $\Delta t = 5$. The table gives the expected temperature after each step (the mean of the Monte Carlo step, computed in closed form). The explicit method is the same algorithm with $f = 1$.

| step | explicit, $f = 1$ | IMC |
|---|---|---|
| 1 | 0.0067 | 0.7881 |
| 2 | 0.9933 | 0.7236 |
| 3 | 0.0330 | 0.7246 |
| 4 | 0.9935 | 0.7245 |
| 5 | 0.0323 | 0.7245 |

The explicit method emits 5 units of energy in the first step from a material that holds 1, takes most of it back, and then swings between hot and cold. IMC goes to the equilibrium in two steps.

**Accuracy in time.** Start with $T = 0.1$ and $E_r = 1$, so $T + T^4 = 1.1$ and the equilibrium is $T = 0.7623$. With 2000 particles per step (`random.Random(3)`), against an accurate ODE solution:

| $t$ | exact $T$ | IMC, $\Delta t = 0.2$ | IMC, $\Delta t = 1$ |
|---|---|---|---|
| 1 | 0.6737 | 0.6698 | 0.7384 |
| 2 | 0.7561 | 0.7545 | 0.7574 |
| 4 | 0.7623 | 0.7675 | 0.7595 |

With $\Delta t = 1$ the material heats too fast in the first step: the frozen data are a first-order approximation in time.

**A violation of the maximum principle.** With the same start and one step of $\Delta t = 100$: $\beta = 0.004$, $f = 1/1.4 = 0.714$, $E_{\mathrm{em}} = 0.00714$, and almost all radiation is absorbed. The expected temperature after the step is $1.0999$, and the run gives $1.0999$. The material is now hotter than the radiation that heated it, whose temperature was 1. The exact solution never exceeds 1. This is the effect that Larsen and Mercier analysed: the frozen $\beta = 4aT^3/c_v$ at the cold start temperature greatly underestimates the emission during the step.

## Correctness

Three claims are theorems. First, total energy is conserved exactly in every step: line L9 adds to the material the absorbed energy minus the emitted energy, and every particle energy is either absorbed, in the census or gone through a boundary. Second, the algorithm is an unbiased Monte Carlo solution of the time-discrete problem defined by the frozen Fleck factor: in one zone, the expected census energy after a step is $E_r e^{-f c\sigma \Delta t} + a T^4 (1 - e^{-f c\sigma \Delta t})$, which the tests check. Third, the Fleck factor is the exact result of the backward Euler linearization above. The proofs are below.

What is not a theorem is the accuracy of the time-discrete problem. The linearization is first order in $\Delta t$, and with large steps it can violate the maximum principle, as Larsen and Mercier proved and as the example shows. They also showed that the maximum principle holds when the time step is small enough. IMC is widely described as stable for large time steps; this is a property observed in practice and supported by analysis of the linearized problem, not a proof of unconditional stability for the nonlinear one.

## Complexity

Each step costs $O(N K)$ for $N$ particles with $K$ collisions each in the step, plus $O(N)$ for emission and census. In an optically thick zone with a large step, $f$ is small and $c\sigma\Delta t$ is large, so a particle has about $c\sigma\Delta t$ effective scatterings before it is absorbed or reaches census: $K$ grows like $c\sigma\Delta t$, which is the main cost of IMC in thick, hot regions. Remedies are random walk acceleration, which replaces many small scatterings by a jump from the diffusion solution, and hybrid methods that use diffusion in thick cells. The space is $O(N)$ for the census.

## Properties

- **Conservative.** The total energy of radiation and matter is conserved to rounding in each step.
- **Stable in practice.** The step can be much longer than the explicit limit of about $1/(c\sigma\beta)$, with no oscillation in the usual problems.
- **Not monotone.** The maximum principle can fail for large steps.
- **First order in time.** The frozen data and the linearization give an error of order $\Delta t$.
- **Monte Carlo noise.** The temperature carries noise from the absorbed energy, and the noise feeds back into the next step through $\beta$, $f$ and the emission.

## Variants and improvements

- **The time-centring parameter.** Fleck and Cummings allow a parameter $\alpha$ in $[1/2, 1]$ in the linearization, with $f = 1/(1 + \alpha \beta c\sigma\Delta t)$; $\alpha = 1$ is the common choice.
- **Frequency dependence.** With multigroup or continuous frequency, the emission spectrum is the Planck function, and effective scattering changes the frequency as well as the direction.
- **Random walk and diffusion acceleration.** Replace many effective scatterings in a thick cell by one step of the diffusion solution, as in the [diffusion approximation](/diffusion-approximation-of-transport/), or use implicit Monte Carlo diffusion in thick regions.
- **Implicit Monte Carlo with better time discretization.** Iterating the step with updated $\beta$, or using a different linearization, reduces the violations of the maximum principle at extra cost.
- **Symbolic IMC and other implicit methods.** Other schemes, such as the symbolic implicit Monte Carlo of Brooks, treat the emission implicitly in a different way, with different trade-offs.

## When to use it

Use IMC for time-dependent thermal radiation problems in which transport effects matter: inertial confinement fusion, astrophysics, high energy density experiments, radiation through optically thin and thick regions together. Where the medium is optically thick everywhere, a diffusion solver is much cheaper. Choose the time step with the maximum principle in mind: a step that the explicit limit forbids is fine, but a step over which the temperature changes by a large factor is not.

## Pitfalls

- **Overheating with large steps.** A cold material next to a hot radiation field can end the step hotter than the field. Limit the relative change of $T$ per step.
- **Noise in cold regions.** With few particles in a cell, the absorbed energy is noisy, and the temperature can fluctuate strongly; continuous absorption lowers this noise.
- **Teleportation error.** In a code with space, emitting particles uniformly in a cell with a steep temperature gradient moves energy too far, and gives wrong wave speeds in thick media. Sample the emission position from a reconstructed $T^4$ profile.
- **The census count.** The number of census particles grows from step to step. Population control (combining in a cell, or Russian roulette) must conserve energy.
- **Merging in space.** Merging census particles of different positions or directions changes the solution. The merge of line L10 is valid only in one zone with no space or direction.

## Implementations

## History

Joseph Fleck and J. D. Cummings at the Lawrence Radiation Laboratory published the method in 1971, with frequency dependence and the effective scattering interpretation. It became the standard Monte Carlo method for thermal radiation in the codes of the US national laboratories. Larsen and Mercier analysed it in 1987 and proved that it satisfies a maximum principle for small enough time steps and can violate it for large ones. Wollaber's 2016 review describes four decades of analysis and variants, including acceleration methods for thick media and corrections for the teleportation error.

## References
