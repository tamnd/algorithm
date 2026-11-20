---
tag: BYYCSC
kind: algorithm
slug: stochastic-velocity-rescaling
name: Stochastic velocity rescaling thermostat
aliases:
- Bussi thermostat
area: scientific-computing/molecular-simulation
level: advanced
summary: Rescales the kinetic energy by a random factor drawn so that it follows the canonical distribution, keeping Berendsen's smoothness with correct sampling.
model: real-ram
complexity:
  vars: {N: the number of particles, S: the number of time steps}
  time: {worst: O(S N^2)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, iterative: true, symplectic: false, symmetric: false}
history:
  year: 2007
  people: [Giovanni Bussi, Davide Donadio, Michele Parrinello]
  note: Bussi, Donadio and Parrinello added a noise term to the Berendsen equation for the kinetic energy, chosen so that its stationary law is canonical, and gave an exact way to draw its solution over one step.
prereqs: [berendsen-thermostat, stochastic-differential-equation]
see_also: [canonical-ensemble, langevin-dynamics, andersen-thermostat, nose-hoover-thermostat, nose-hoover-chains, molecular-dynamics, parrinello-rahman-barostat, euler-maruyama-method]
sources:
  - paper: doi:10.1063/1.2408420
    title: Giovanni Bussi, Davide Donadio and Michele Parrinello, Canonical sampling through velocity rescaling, Journal of Chemical Physics 126, 014101, 2007
    locator: the stochastic equation for the kinetic energy, its exact solution over a time step, the effective energy and the tests on water and other systems
  - paper: doi:10.1103/PhysRevE.75.056707
    title: Giovanni Bussi and Michele Parrinello, Accurate sampling using Langevin dynamics, Physical Review E 75, 056707, 2007
    locator: the effective energy as a check of stochastic thermostats and the relation between global and local thermostats
  - paper: doi:10.1063/1.448118
    title: H. J. C. Berendsen, J. P. M. Postma, W. F. van Gunsteren, A. DiNola and J. R. Haak, Molecular dynamics with coupling to an external bath, Journal of Chemical Physics 81(8), 1984, 3684-3690
    locator: the weak coupling equation for the temperature, which is the drift part of the method
---

The stochastic velocity rescaling thermostat, also called the Bussi thermostat, controls the temperature in [molecular dynamics](/molecular-dynamics/). After each step it multiplies all velocities by one factor, as the [Berendsen thermostat](/berendsen-thermostat/) does. The factor is random: the kinetic energy follows the Berendsen relaxation plus a noise term, and the noise is chosen so that the stationary law of the kinetic energy is the canonical one. The method samples the [canonical ensemble](/canonical-ensemble/) (a theorem, up to the error of the Verlet step), and the new kinetic energy is drawn exactly, with no time step error. Since the factor is close to 1 for many particles, the dynamics stay close to Newtonian.

## In plain words

The Berendsen thermostat gently pushes the temperature toward the target. It does this so well that the temperature stops moving, but in a real system at fixed temperature the energy in motion goes up and down a little. So Berendsen gives the wrong spread.

This method adds a random push of the right size. Each step it looks at the energy in motion, picks a new value at random from the law it would reach after a short relaxation with random kicks, and scales all speeds by one common factor to get there. On average it still pulls toward the target, and the spread is now exactly right. All atoms keep their directions of motion, so the motion looks almost like plain molecular dynamics. A bookkeeping of the energy the bath adds or removes gives a total that must stay fixed, which checks the program.

## The problem

The input is positions $x_i \in \mathbb{R}^d$, velocities $v_i$ and masses $m_i$ of $N$ particles, a force routine for $f_i = -\nabla_i U$, a time step $h$, a number of steps $S$, the target $k_B T$, the coupling time $\tau > 0$, the number $N_f$ of degrees of freedom and a random number source. In the implementation $N_f = dN$; with the total momentum fixed, use $N_f = dN - d$, and remove also one degree of freedom for each constraint. Let $K_0 = N_f k_B T / 2$. Bussi, Donadio and Parrinello (2007) let the kinetic energy follow
$$dK = \frac{K_0 - K}{\tau}\, dt + 2\sqrt{\frac{K K_0}{N_f\, \tau}}\, dW,$$
with a Wiener process $W$. The drift is the Berendsen equation for $K$. The stationary law of this equation is the canonical law of $K$, the gamma law with density proportional to $K^{N_f/2 - 1} e^{-K/k_B T}$. The output is the trajectory, the kinetic energy after each step and the effective energy
$$\tilde H = K + U - \sum (\text{the changes of } K \text{ made by the thermostat}),$$
which is conserved up to the error of the integrator.

## The algorithm

```pseudo id=main
STOCHASTIC-VELOCITY-RESCALING(x, v, m, FORCES, h, S, kT, tau, N_f)
L1  (U, f) ← FORCES(x); K_0 ← N_f kT / 2; c ← exp(-h / tau); sigma² ← (1 - c) K_0 / N_f; Q ← 0
L2  for step ← 1 to S do
L3      v_i ← v_i + (h / 2) f_i / m_i for each particle i            ▷ velocity Verlet
L4      x_i ← x_i + h v_i for each particle i
L5      (U, f) ← FORCES(x)
L6      v_i ← v_i + (h / 2) f_i / m_i for each particle i
L7      K ← Σ_i m_i |v_i|² / 2
L8      R_1 ← a standard normal number
L9      S_g ← 2 GAMMA((N_f - 1) / 2, 1), or 0 if N_f = 1             ▷ chi-squared with N_f - 1 degrees of freedom
L10     K' ← (sqrt(c K) + sigma R_1)² + sigma² S_g
L11     alpha ← sqrt(K' / K), with the sign of sqrt(c K) + sigma R_1
L12     v_i ← alpha v_i for each particle i
L13     Q ← Q + (K' - K)                                             ▷ heat from the bath
L14     record K' and the effective energy K' + U - Q
L15 return (x, v, the recorded K', the recorded effective energies)
```

Lines L8 to L10 draw the exact solution of the equation for $K$ over a time $h$. The equation is the law of $\sum_a y_a^2$ for $N_f$ independent Ornstein-Uhlenbeck processes $y_a$, and by symmetry one of them can be taken along the current direction: it gives the term with $R_1$, and the other $N_f - 1$ give the chi-squared term. For $\tau \to \infty$, $c = 1$ and $K' = K$, so the method is plain velocity Verlet. For $\tau \to 0$, $c = 0$ and $K'$ is a fresh draw from the canonical law at each step.

## Example

**One rescaling by hand.** Take $K = 4$, $K_0 = 1$, $N_f = 2$ and $h/\tau = 0.5$, so $c = e^{-0.5} = 0.606531$ and $\sigma^2 = (1 - c) K_0 / N_f = 0.196735$, $\sigma = 0.443548$. With the draws $R_1 = 0.5$ and $S_g = 1$:

| quantity | $\sqrt{cK}$ | $\sqrt{cK} + \sigma R_1$ | $K'$ | $\alpha$ |
|---|---|---|---|---|
| value | 1.557602 | 1.779375 | 3.362912 | 0.916912 |

Over many draws the mean of $K'$ is $cK + (1 - c)K_0 = 2.819592$, the Berendsen value, and the variance is $2(1 - c)(K_0/N_f)(2cK + (1 - c)K_0) = 2.064028$. Berendsen gives the same mean with variance 0.

**Canonical fluctuations.** 20 harmonic oscillators in one dimension with $m = k = k_B T = 1$ in reduced units, $N_f = 20$, random normal start values (seed 4), $h = 0.05$ and 40000 steps, of which the first 2000 are dropped. The canonical law of $K$ is gamma with mean and variance $N_f/2 = 10$. Errors are batch-means standard errors with 20 batches.

| $\tau$ | mean of $K$ | variance of $K$ | spread of $\tilde H$ |
|---|---|---|---|
| 0.1 | $10.006 \pm 0.043$ | $9.93 \pm 0.16$ | 0.0167 |
| 1 | $9.997 \pm 0.113$ | $9.41 \pm 0.31$ | 0.0148 |
| 10 | $10.014 \pm 0.317$ | $9.29 \pm 0.83$ | 0.0126 |

These are measurements. The mean and the variance agree with 10 for all $\tau$. A larger $\tau$ gives a slower decorrelation and larger errors, but not a bias, which is the difference from Berendsen. The effective energy stays within about 0.015 of its start, which is the size of the Verlet error at this step.

**Free particles.** With no forces, the rescaling is the whole dynamics and it is exact for any step. Five free particles with $h = 1$, $\tau = 0.2$ and 8000 steps (seed 8) give a mean of $K$ of $2.461 \pm 0.018$ and a variance of $2.40 \pm 0.06$, against 2.5 and 2.5.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **A representation.** $K = \sum_a y_a^2$ for $N_f$ independent Ornstein-Uhlenbeck processes solves the equation for $K$ in law.
2. **The exact step.** Lines L8 to L10 draw $K'$ with the law of the solution at time $h$, for any $h$ and $\tau$.
3. **The canonical law of $K$ is stationary.** It is the gamma law with shape $N_f / 2$ and scale $k_B T$.
4. **The canonical distribution is kept by the rescaling.** Under the canonical law, $K$ and the direction of the scaled velocity vector are independent, and the rescaling changes only $K$.
5. **The effective energy** changes only in the Verlet parts.
6. **The sign** of $\alpha$ does not change the law; it keeps the velocity path continuous as $h \to 0$.

So the method samples the canonical ensemble up to the $O(h^2)$ error of the Verlet step. Ergodicity needs the Hamiltonian motion to mix the directions of the velocities, since the thermostat acts only on their length; for systems with a few independent parts, such as identical oscillators, it is not enough.

## Complexity

Each step does one force evaluation, $O(N)$ work for the kinetic energy and the scaling, one normal draw and one gamma draw. A gamma draw takes $O(1)$ expected time with the usual rejection methods. With the all-pairs forces of the molecular dynamics page, $S$ steps take $O(S N^2)$ time. The extra space is $O(N)$ for the copies of $x$ and $v$.

## Properties

- **Ensemble.** Canonical (NVT), up to the time step error of the Verlet part, if the Hamiltonian motion mixes the velocity directions.
- **Exact thermostat step.** The new kinetic energy has no time step error.
- **Global and gentle.** One factor scales all velocities, close to 1 when $N_f$ is large, since the relative fluctuation of $K$ is $\sqrt{2/N_f}$. Directions of motion are kept, and a total momentum of zero stays zero.
- **Dynamics stay physical.** Diffusion and other dynamical properties are close to those of plain molecular dynamics for usual values of $\tau$ (a measurement in the 2007 paper).
- **A quantity to monitor.** The effective energy drifts only by integration error.
- **Not deterministic.** The trajectory depends on the random numbers.

## Variants and improvements

- **Several thermostats.** Separate groups of atoms, such as solute and solvent, can each have their own rescaling with their own $N_f$.
- **Constant pressure.** Bussi, Zykova-Timan and Parrinello (2009) combined the rescaling with a stochastic barostat, and Bernetti and Bussi (2020) gave stochastic cell rescaling. The [Parrinello-Rahman barostat](/parrinello-rahman-barostat/) with this thermostat is a common NPT setup.
- **Local thermostats.** [Langevin dynamics](/langevin-dynamics/) acts on each degree of freedom and has a proof of ergodicity, at the cost of a larger change of the dynamics. The [Andersen thermostat](/andersen-thermostat/) redraws single velocities.
- **Deterministic thermostats.** [Nose-Hoover chains](/nose-hoover-chains/) give a time-reversible, deterministic alternative.
- **Small time step limit.** Integrating the equation for $K$ with the [Euler-Maruyama method](/euler-maruyama-method/) works for small $h/\tau$, but the exact draw costs the same and has no error.

## When to use it

Use it as a default thermostat for production runs in the NVT ensemble, in particular to replace Berendsen: it equilibrates as fast and samples the right distribution. It is a good choice when dynamical properties such as diffusion are measured, since it changes the dynamics little. For very small or nearly harmonic systems, where the Hamiltonian motion does not mix, prefer a local thermostat such as Langevin.

## Pitfalls

- **A wrong $N_f$.** The target is $K_0 = N_f k_B T / 2$, so constraints and a fixed centre of mass must be counted, or the temperature is wrong.
- **Zero kinetic energy.** The factor $\sqrt{K'/K}$ needs $K > 0$. Start from random velocities.
- **Identical copies.** One global factor cannot make identical oscillators different. Start them at different values, as in the test.
- **A wrong chi-squared draw.** For large $N_f$, summing $N_f - 1$ squared normals is slow, and an approximation by one normal is not exact. Use a gamma generator, as on line L9.
- **Ignoring the effective energy.** A drift of $\tilde H$ shows a too large step, which no thermostat hides.

## Implementations

## History

Berendsen and coworkers (1984) introduced weak coupling, which relaxes the kinetic energy toward the target but suppresses its fluctuations. Bussi, Donadio and Parrinello (2007) added a stochastic term that gives the canonical law, showed how to draw the exact solution over one step, and defined the effective energy. In the same year Bussi and Parrinello studied the effective energy for Langevin dynamics. The thermostat is the v-rescale option of GROMACS and is available in many other codes.

## References
