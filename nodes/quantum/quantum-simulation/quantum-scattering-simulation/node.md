---
tag: 5DG7KS
kind: problem
slug: quantum-scattering-simulation
name: Quantum scattering simulation
aliases:
- Jordan-Lee-Preskill scattering
area: quantum/quantum-simulation
level: research
summary: "Given a quantum field theory and incoming particles with set momenta, sample the outgoing particles of their collision, or estimate a scattering probability to error epsilon."
prereqs: [quantum-field-theory-simulation]
see_also: [hamiltonian-simulation, quantum-many-body-simulation, bqp, lieb-robinson-bound, quantum-phase-estimation, trotter-suzuki-product-formulas, discrete-fourier-transform, second-quantization]
sources:
  - paper: doi:10.1126/science.1217069
    title: Stephen P. Jordan, Keith S. M. Lee and John Preskill, Quantum algorithms for quantum field theories, Science 336(6085), 2012, pages 1130 to 1133
    locator: the algorithm for scattering in lattice phi^4 theory, with gate counts polynomial in the number of particles, the energy and 1/ε, and the exponents at weak coupling
  - paper: doi:10.26421/QIC14.11-12-8
    title: Stephen P. Jordan, Keith S. M. Lee and John Preskill, Quantum computation of scattering in scalar quantum field theories, Quantum Information and Computation 14(11-12), 2014, pages 1014 to 1080 (arXiv:1112.4833)
    locator: the full error analysis for the scalar theory, the wave packet preparation and the adiabatic turn-on of the interaction
  - paper: arxiv:1404.7115
    title: Stephen P. Jordan, Keith S. M. Lee and John Preskill, Quantum algorithms for fermionic quantum field theories, 2014
    locator: the extension to the massive Gross-Neveu model, a theory of interacting fermions in 1 + 1 dimensions
  - paper: doi:10.22331/q-2018-01-08-44
    title: Stephen P. Jordan, Hari Krovi, Keith S. M. Lee and John Preskill, BQP-completeness of scattering in scalar quantum field theory, Quantum 2, 2018, article 44
    locator: the BQP-completeness of the vacuum-to-vacuum amplitude with spacetime-dependent sources in a massive scalar theory in 1 + 1 dimensions
---

*Quantum scattering simulation* is the problem of computing what comes out when particles collide, from the laws of a quantum field theory. The input is the theory and the incoming particles, with their momenta. The output is a sample of the outgoing particles, or the probability of a given outcome. These are the numbers that particle colliders measure. At weak coupling, perturbation theory with Feynman diagrams gives them as a series in the coupling, but at strong coupling or for many particles no efficient classical method is known. Jordan, Lee and Preskill (2012) gave a quantum algorithm for $\phi^4$ theory whose cost is polynomial in the number of particles, their energy and $1/\epsilon$, which is why this problem carries their name. It is one task of [quantum field theory simulation](/quantum-field-theory-simulation/), and it is BQP-complete in a form with external sources.

## In plain words

Two particles fly toward each other, meet, and something comes out: the same two particles with new directions, or more particles. Quantum mechanics gives only the odds of each outcome. A quantum computer can play the whole event. It builds the two incoming particles as waves on a lattice, lets them move and meet under the rules of the theory, and then counts the particles that come out. Running this many times gives the odds. The hard parts are building clean incoming particles and making the lattice fine enough that the answer does not depend on it.

## Definition

**Input.**

- A quantum field theory, given by its lattice Hamiltonian as on the [quantum field theory simulation](/quantum-field-theory-simulation/) page, with physical mass $m$ and coupling $\lambda$, in $d$ spatial dimensions.
- The incoming state: $k$ particles with momenta $p_1, \ldots, p_k$, as wave packets that are far apart at the start. The total energy is $E$.
- An error $\epsilon$.

**Output.** One of:

- a sample from the distribution of the outgoing particles (their number and their momenta), from a distribution within total variation distance $\epsilon$ of the true one;
- an estimate of the probability of a given outcome, within $\epsilon$, with probability at least $\frac23$.

**The S-matrix.** The scattering operator $S$ maps the free incoming states to the free outgoing states, $S = \lim_{t\to\infty} e^{iH_0 t}e^{-2iHt}e^{iH_0t}$ in the interaction picture, with $H_0$ the free part of $H$. The probabilities are $|\langle\text{out}|S|\text{in}\rangle|^2$. On a finite lattice the limit is replaced by a finite time long enough for the packets to separate, and short enough that they do not wrap around the box.

## Variants

- **Theories.** Scalar $\phi^4$ theory (Jordan, Lee and Preskill 2012 and 2014); fermionic theories such as the Gross-Neveu model (Jordan, Lee and Preskill, arXiv:1404.7115); gauge theories, where the problem is open in general.
- **Inclusive and exclusive.** Ask for all outcomes (sampling), or for one channel, such as $2 \to 4$ particle production.
- **Quantum mechanics.** With a fixed number of particles and a potential, the same task is the scattering of nonrelativistic particles, for example in chemistry. One particle on a lattice is a problem of size $L^d$ and is easy classically.
- **With external sources.** The theory is driven by classical fields that vary in space and time. Jordan, Krovi, Lee and Preskill (2018) use this form for their hardness result.

## Examples

- **One particle and one impurity.** A particle hops on a chain with $H = -J\sum_x(|x\rangle\langle x+1| + |x+1\rangle\langle x|) + V|0\rangle\langle0|$, with energies $E = -2J\cos k$ for momentum $k$. Put $\psi_x = e^{ikx} + r\,e^{-ikx}$ for $x \le 0$ and $\psi_x = \tau\,e^{ikx}$ for $x \ge 0$. Continuity at $0$ gives $1 + r = \tau$, and the equation $E\psi_0 = -J(\psi_1 + \psi_{-1}) + V\psi_0$ gives $\tau = 2iJ\sin k/(2iJ\sin k - V)$. So the probability of passing is
$$T(k) = |\tau|^2 = \frac{4J^2\sin^2 k}{4J^2\sin^2 k + V^2}.$$
  It is 1 for $V = 0$ and goes to 0 at the band edges $k \to 0, \pi$, where the particle is slow. A wide wave packet centred at $k$ passes with probability close to $T(k)$. This is the simplest case of the problem, with a closed form to check a simulation.
- **The free theory.** For $\lambda = 0$, $S = I$: every outgoing state equals the incoming one. A simulation must reproduce this exactly up to its truncation errors, which tests the wave packet preparation and the measurement apart from the interaction.
- **Weak coupling in $\phi^4$ theory.** For small $\lambda$, the leading $2 \to 2$ amplitude is the single vertex, of order $\lambda$, and particle production $2 \to 4$ is of order $\lambda^2$ in the amplitude. Perturbation theory gives these, so they are checks for a simulation at weak coupling. The quantum algorithm matters where the series fails: at strong coupling or high energy.

## Known algorithms

Classically, perturbation theory works at weak coupling, and lattice Monte Carlo in imaginary time cannot follow real-time collisions. The algorithm of Jordan, Lee and Preskill has these parts, each on its own page or in the cited papers:

| part | method | cost driver |
|---|---|---|
| free vacuum | preparation of a Gaussian state of the lattice oscillators | the number of sites |
| incoming particles | wave packets created in the free theory | the packet width |
| interaction | turned on slowly, so that the free packets become interacting particles | the mass gap, which sets the speed |
| collision | [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) for the lattice Hamiltonian | $L^d$ terms per step, time $t$ |
| outgoing particles | interaction turned off, then a measurement of the particle numbers by [quantum phase estimation](/quantum-phase-estimation/) | the momentum resolution |

At weak coupling the number of gates grows like $(1/\epsilon)^{1.5}$, $(1/\epsilon)^{2.376}$ and $(1/\epsilon)^{3.564}$ for $d = 1, 2, 3$. At strong coupling the cost stays polynomial but grows near a phase transition, where the mass gap closes and the slow turn-on of the interaction takes longer.

## Bounds

- **BQP-complete.** Jordan, Krovi, Lee and Preskill (2018) proved that estimating the vacuum-to-vacuum transition amplitude of a massive scalar theory in 1 + 1 dimensions, with classical sources that vary in space and time, is BQP-hard, even at weak coupling. The quantum algorithm puts it in [BQP](/bqp/), so it is BQP-complete. An efficient classical algorithm would put every problem in BQP into classical polynomial time.
- **Polynomial upper bound.** The Jordan, Lee and Preskill algorithm uses a number of gates polynomial in the number of particles, the energy and $1/\epsilon$, with the exponents above at weak coupling. These are proved upper bounds with large constants, not measured costs.
- **Space.** The lattice must be larger than the region the particles cover during the collision. By the [Lieb-Robinson bound](/lieb-robinson-bound/), this region grows linearly in time, so the number of sites is polynomial in $t$.

## Reductions

- **To field theory simulation.** Scattering is one task of [quantum field theory simulation](/quantum-field-theory-simulation/), with special initial states and measurements.
- **To Hamiltonian simulation.** Each part of the algorithm is a [Hamiltonian simulation](/hamiltonian-simulation/) of a local Hamiltonian, free or interacting, possibly time-dependent.
- **From quantum circuits.** Jordan, Krovi, Lee and Preskill encode a quantum circuit into the sources of the field theory, so that the circuit's output probability is a vacuum-to-vacuum probability. This is the reduction behind the hardness.
- **One particle to linear algebra.** With one particle the problem is a linear system on $L^d$ amplitudes, as in the impurity example, solvable classically by the [discrete Fourier transform](/discrete-fourier-transform/) for translation-invariant parts.

## Applications

- **Particle physics at strong coupling.** Predictions for collisions where perturbation theory fails, such as hadron scattering in quantum chromodynamics.
- **Tests of the quantum advantage.** A problem that is BQP-complete and physically natural, so a demonstration on hardware would test quantum computation on its own terms.
- **Nuclear and chemical reactions.** The nonrelativistic form of the problem, with few particles and many channels.

## References
