---
tag: KYF8ST
kind: algorithm
slug: nose-hoover-chains
name: "Nose-Hoover chains"
area: scientific-computing/molecular-simulation
level: advanced
summary: Couples the Nose-Hoover friction to further thermostats in a chain, curing the lack of ergodicity of one thermostat on small or stiff systems.
model: real-ram
complexity:
  vars: {N: the number of particles, M: the number of links in the chain, S: the number of time steps}
  time: {worst: O(S (N^2 + M))}
  space: {extra: O(N + M)}
properties: {deterministic: true, iterative: true, symplectic: false, symmetric: true}
history:
  year: 1992
  people: [Glenn J. Martyna, Michael L. Klein, Mark E. Tuckerman]
  note: Martyna, Klein and Tuckerman thermostatted the Nose-Hoover friction by a second thermostat, and so on, and showed that the chain samples the canonical distribution of one harmonic oscillator where one thermostat does not.
prereqs: [nose-hoover-thermostat]
see_also: [canonical-ensemble, ergodicity, operator-splitting, langevin-dynamics, stochastic-velocity-rescaling, andersen-thermostat, parrinello-rahman-barostat, respa-multiple-time-step]
sources:
  - paper: doi:10.1063/1.463940
    title: Glenn J. Martyna, Michael L. Klein and Mark Tuckerman, Nose-Hoover chains, The canonical ensemble via continuous dynamics, Journal of Chemical Physics 97(4), 1992, 2635-2643
    locator: the equations of the chain, the conserved energy, the proof of the stationary canonical density and the harmonic oscillator test
  - paper: doi:10.1080/00268979600100761
    title: Glenn J. Martyna, Mark E. Tuckerman, Douglas J. Tobias and Michael L. Klein, Explicit reversible integrators for extended systems dynamics, Molecular Physics 87(5), 1996, 1117-1157
    locator: the factorization of the chain part into exact flows, which gives the reversible step of this page
  - book: isbn:9780198525264
    title: Mark E. Tuckerman, Statistical Mechanics, Theory and Molecular Simulation, Oxford University Press, 2010
    locator: Chapter 4, the canonical ensemble (Nose-Hoover chains and their integration)
  - book: isbn:9783319163741
    title: Ben Leimkuhler and Charles Matthews, Molecular Dynamics, With Deterministic and Stochastic Numerical Methods, Springer, 2015
    locator: Chapter 8, extended variable methods
---

Nose-Hoover chains are a deterministic thermostat for [molecular dynamics](/molecular-dynamics/) that extends the [Nose-Hoover thermostat](/nose-hoover-thermostat/). The friction $\xi_1$ that controls the particles is itself controlled by a second friction $\xi_2$, which is controlled by a third, and so on, in a chain of $M$ links. The extended system conserves an energy, and the [canonical ensemble](/canonical-ensemble/) is a stationary density of its flow (a theorem). The extra links make the motion chaotic in cases where one thermostat is not, so in practice the chain samples the canonical distribution of small and stiff systems such as one harmonic oscillator. This is a measurement, not a proof of ergodicity.

## In plain words

One Nose-Hoover thermostat is a pedal that brakes or speeds up all atoms together. The pedal itself swings in a regular way, and for simple systems the atoms and the pedal fall into a fixed rhythm that never explores all the states.

The chain adds a second pedal that acts on the first one, a third that acts on the second, and so on. Each pedal tries to keep the one before it at the right temperature. The extra pedals break the fixed rhythm, so the motion becomes irregular and fills the space of states. A total energy that includes all pedals stays fixed, so the program can still be checked.

## The problem

The input is as for the Nose-Hoover thermostat: positions $x_i \in \mathbb{R}^d$, velocities $v_i$, masses $m_i$, forces $f_i = -\nabla_i U$, a time step $h$, a number of steps $S$, the target $k_B T$ and the number $N_f$ of velocity components that link 1 scales. In addition it takes the masses $Q_1, \ldots, Q_M > 0$ of the links and start values of $\xi_j$ and $\eta_j$ (often 0). The output is the trajectory of the equations of Martyna, Klein and Tuckerman (1992):
$$\dot x_i = v_i, \qquad \dot v_i = \frac{f_i}{m_i} - \xi_1 v_i, \qquad \dot \xi_j = G_j - \xi_j \xi_{j+1} \ (j < M), \qquad \dot \xi_M = G_M, \qquad \dot \eta_j = \xi_j,$$
with the thermostat forces
$$G_1 = \frac{2K - N_f k_B T}{Q_1}, \qquad G_j = \frac{Q_{j-1}\xi_{j-1}^2 - k_B T}{Q_j} \ (j \ge 2),$$
and the extended energy after each step,
$$H' = K + U + \sum_{j=1}^{M} \tfrac12 Q_j \xi_j^2 + N_f k_B T\, \eta_1 + k_B T \sum_{j=2}^{M} \eta_j,$$
which the exact flow conserves. Link $j \ge 2$ has one degree of freedom, $\xi_{j-1}$, to control, which is the reason $G_j$ has $k_B T$ and not $N_f k_B T$. In the implementation $N_f = dN$; with the total momentum fixed, use $N_f = dN - d$. The masses of Martyna, Klein and Tuckerman are $Q_1 = N_f k_B T \tau^2$ and $Q_j = k_B T \tau^2$ for $j \ge 2$, with a thermostat period $\tau$ that is a choice.

## The algorithm

```pseudo id=main
NOSE-HOOVER-CHAINS(x, v, m, FORCES, h, S, kT, Q_1..Q_M, N_f, xi, eta)
L1  (U, f) ← FORCES(x)
L2  for step ← 1 to S do
L3      CHAIN-HALF(v, xi, eta)
L4      v_i ← v_i + (h / 2) f_i / m_i for each particle i     ▷ half kick
L5      x_i ← x_i + h v_i for each particle i                ▷ drift
L6      (U, f) ← FORCES(x)
L7      v_i ← v_i + (h / 2) f_i / m_i for each particle i     ▷ half kick
L8      CHAIN-HALF(v, xi, eta)
L9      record H'
L10 return (x, v, xi, eta, the recorded H')

LINK-QUARTER(j)                                      ▷ exact flows of link j for a time h / 4
L11 if j = M then xi_M ← xi_M + (h / 4) G_M and return
L12 s ← exp(-xi_{j+1} h / 8)
L13 xi_j ← s xi_j
L14 xi_j ← xi_j + (h / 4) G_j
L15 xi_j ← s xi_j

CHAIN-HALF(v, xi, eta)                               ▷ exact flows of the chain for a time h / 2
L16 for j ← M down to 1 do LINK-QUARTER(j)
L17 v_i ← exp(-xi_1 h / 2) v_i for each particle i, and update K
L18 eta_j ← eta_j + (h / 2) xi_j for j ← 1 to M
L19 for j ← 1 to M do LINK-QUARTER(j)
```

Each line is the exact flow of a part of the equations with the other variables fixed. $G_j$ does not depend on $\xi_j$, so line L14 is exact, and the friction term $-\xi_j \xi_{j+1}$ alone is the exponential decay of lines L13 and L15. The order of the sweep, from the end of the chain to the particles and back, makes CHAIN-HALF a palindrome, and with the Verlet step in the middle the whole step is time-reversible and of order 2. This is the splitting of Martyna, Tuckerman, Tobias and Klein (1996), with one stage per half step. With $M = 1$, LINK-QUARTER is one quarter kick, and the step is the Nose-Hoover step.

## Example

**One step by hand.** One particle on a spring with $m = k = k_B T = 1$ in reduced units, $N_f = 1$, $M = 2$, $Q_1 = Q_2 = 1$, $x = 1$, $v = 0$, all $\xi_j = \eta_j = 0$ and $h = 0.1$, so $H' = 0.5$. In the first CHAIN-HALF, $K = 0$, so link 2 gets $G_2 = (0 - 1)/1$ and $\xi_2 = -0.025$ (L11). Link 1 is scaled by $e^{0.025 \cdot 0.1/8}$, which changes nothing since $\xi_1 = 0$, kicked by $G_1 = -1$ to $\xi_1 = -0.025$ (L14), and scaled again to $-0.0250078$ (L15). The rest of the step goes as on the Nose-Hoover page, and after it

| variable | $x$ | $v$ | $\xi_1$ | $\xi_2$ | $\eta_1$ | $\eta_2$ | $H'$ |
|---|---|---|---|---|---|---|---|
| value | 0.995 | $-0.1001243$ | $-0.0998123$ | $-0.0996258$ | $-0.0049954$ | $-0.0049937$ | 0.4999797 |

**The extended energy is conserved to second order.** Two oscillators with $k = 1$, masses 1 and 2, started at $x = (1, 0.3)$, $v = (0, 0.7)$, with $k_B T = 1$, $N_f = 2$ and $M = 3$ links with the masses $Q = (2, 1, 1)$ of Martyna, Klein and Tuckerman for $\tau = 1$, run to $t = 20$:

| $h$ | 0.1 | 0.05 | 0.025 |
|---|---|---|---|
| spread of $H'$ | 0.02196 | 0.005495 | 0.001375 |

The spread falls by a factor of 4 when $h$ is halved. A run of 300 steps forward and 300 back with $v$ and all $\xi_j$ flipped recovers the start to $10^{-9}$.

**One oscillator becomes canonical.** One oscillator with $m = k = k_B T = 1$ and $N_f = 1$, from $x = 1$, $v = 0$, with $h = 0.05$ and a sample every 10 steps:

| thermostat | run length | $\langle x^2 \rangle$ | $\langle x^4 \rangle / \langle x^2 \rangle^2$ |
|---|---|---|---|
| one Nose-Hoover, $Q = 1$ | $10^4$ | 0.793 | 1.538 |
| chain, $M = 4$, all $Q_j = 1$ | 500 | 0.993 | 2.890 |
| chain, $M = 4$, all $Q_j = 1$ | $10^4$ | 0.980 | 2.913 |

The canonical values are 1 and 3. These are measurements: the chain gives the canonical moments within the sampling error, and one thermostat does not.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The extended energy** $H'$ is conserved: in $\sum_j Q_j \xi_j \dot\xi_j$ the coupling terms cancel in pairs, and the $\eta$ terms cancel the rest.
2. **The canonical density is stationary.** The density $\exp(-\beta(K + U + \sum_j \frac12 Q_j \xi_j^2))$ solves the stationary Liouville equation, since the flow has divergence $-N_f\xi_1 - \sum_{j \ge 2}\xi_j$. Its marginal in $(x, v)$ is canonical, and each $\xi_j$ is normal with variance $k_B T / Q_j$.
3. **The step is a palindrome of exact flows**, so it is time-reversible and of order 2.
4. **Length 1** gives the Nose-Hoover step.

So the method samples the canonical ensemble if the extended flow is ergodic. This is still a hypothesis. The chain does not prove ergodicity; it makes it much more likely in practice, as the measurements show. The dynamics of the particles are disturbed as little as with one thermostat, since only $\xi_1$ acts on them.

## Complexity

Each step does one force evaluation, $O(N)$ work for the particles and $O(M)$ work for the chain, with four exponentials per link. With the all-pairs forces of the molecular dynamics page, $S$ steps cost $O(S(N^2 + M))$ time. The extra space is $O(N + M)$. In practice $M$ is a small number such as 3 to 5, which is a choice, and the chain costs nothing next to the forces.

## Properties

- **Ensemble.** Canonical (NVT) for the $(x, v)$ marginal, if the extended dynamics is ergodic, up to the time step error.
- **Deterministic and time-reversible.** The step is a palindrome of exact flows.
- **A conserved quantity to monitor.** $H'$ drifts only by integration error.
- **Not symplectic.** The flow does not keep phase-space volume; it keeps the measure $\exp(N_f \eta_1 + \sum_{j \ge 2}\eta_j)$ times the volume.
- **Robust where one thermostat fails.** On one harmonic oscillator and on harmonic solids, measured moments agree with the canonical values.

## Variants and improvements

- **Multiple time steps in the chain.** Martyna, Tuckerman, Tobias and Klein (1996) split the chain part further, into several stages with Suzuki-Yoshida weights, for stiff chains. This page uses one stage per half step. The same idea for the forces is [RESPA](/respa-multiple-time-step/).
- **Massive chains.** One chain for each degree of freedom, as in path integral simulations, makes the thermostat act locally.
- **Barostats.** The constant pressure methods of Martyna, Tobias and Klein put chains on the particles and on the volume or cell variables. The [Parrinello-Rahman barostat](/parrinello-rahman-barostat/) needs such a thermostat to sample NPT.
- **Stochastic thermostats.** [Langevin dynamics](/langevin-dynamics/) and [stochastic velocity rescaling](/stochastic-velocity-rescaling/) reach ergodicity with noise, and there is a proof for them. A Langevin thermostat on the last link of a chain is a hybrid that some codes use.

## When to use it

Use Nose-Hoover chains when a deterministic, time-reversible thermostat with a conserved quantity is wanted and the system is small, stiff or close to harmonic: crystals at low temperature, small molecules, path integral beads. For large disordered systems, one thermostat often works as well. When a proof of ergodicity matters more than a deterministic trajectory, use a stochastic thermostat.

## Pitfalls

- **Chain masses that are too small.** The links then move fast, and the time step must resolve them. Check the spread of $H'$.
- **Reporting the wrong energy.** Only $H'$ with all $\eta_j$ terms is conserved.
- **A wrong $N_f$.** The first link targets $N_f k_B T$, and $N_f$ must count the constraints and a fixed centre of mass.
- **Assuming ergodicity.** The chain is a remedy that works well in tests, not a theorem. Check the distribution, not only the mean temperature, for example with $\langle x^4 \rangle / \langle x^2 \rangle^2$ on a harmonic test.

## Implementations

## History

Hoover (1985) showed that one Nose-Hoover thermostat does not give the canonical distribution of one harmonic oscillator. Martyna, Klein and Tuckerman (1992) proposed to thermostat the thermostat, proved that the chain keeps the canonical density, and showed in numerical tests that it samples the harmonic oscillator correctly. Martyna, Tuckerman, Tobias and Klein (1996) gave the reversible integrators built from exact flows, including those for the chains and for constant pressure. The method is a standard option in many molecular dynamics codes.

## References
