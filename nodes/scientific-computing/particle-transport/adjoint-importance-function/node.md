---
tag: MHDANB
kind: concept
slug: adjoint-importance-function
name: Adjoint flux as importance
aliases:
- importance function
area: scientific-computing/particle-transport
level: core
summary: The solution of the adjoint transport equation gives the expected contribution of a particle at each phase-space point to a tally, guiding variance reduction.
prereqs: [linear-boltzmann-transport-equation]
see_also: [cadis, weight-window, particle-splitting, exponential-transform, k-eigenvalue-problem, adjoint-model, adjoint-sensitivity-analysis, markov-chain]
sources:
  - book: "Jeffery Lewins, Importance: The Adjoint Function. The Physical Basis of Variational and Perturbation Theory in Transport and Diffusion Problems, Pergamon Press, 1965"
    locator: the definition of importance as the expected contribution of a neutron to a measurement, and the derivation of the adjoint equation from a balance of importance
  - book: "George I. Bell and Samuel Glasstone, Nuclear Reactor Theory, Van Nostrand Reinhold, 1970"
    locator: the treatment of the adjoint transport equation, its physical meaning as an importance and its use in perturbation theory
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Computational Methods of Neutron Transport, Wiley, 1984 (ANS reprint 1993)
    locator: the sections on the adjoint transport equation and its boundary conditions
  - paper: doi:10.13182/NSE98-2
    title: John C. Wagner and Alireza Haghighat, Automated variance reduction of Monte Carlo shielding calculations using the discrete ordinates adjoint function, Nuclear Science and Engineering 128(2), 1998, 186-208
    locator: the use of the adjoint function as the importance for source biasing and weight windows
---

The adjoint flux $\psi^+$ is the solution of the adjoint of the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/), with the detector response as its source. Its value at a point of phase space (a position, a direction and an energy) is the expected score that one particle at that point, together with all the particles it makes, adds to the detector. This is why the adjoint flux is also called the importance function. It turns a question about one tally into a field over all of phase space, and that field tells a Monte Carlo code where to spend its particles.

## In plain words

Think of a detector far away behind a thick wall. A particle near the detector that moves toward it has a good chance to be counted. A particle on the far side of the wall, or one that moves away, almost never counts. The importance of a particle is its expected count: how much, on average, it will add to the detector reading before it is lost.

The importance is a property of the place, the direction and the energy, not of one particle. It can be computed for all points at once by solving the same kind of equation as the normal particle flow, but run backward, from the detector toward the source. A simulation then uses it as a map: it makes more copies of particles in important places and removes particles in unimportant places, so that the count gets more accurate for the same work.

## The idea

**The forward problem.** Write the steady transport equation as $L\psi = q$, where $q$ is the source and
$$L\psi = \Omega \cdot \nabla \psi + \Sigma_t \psi - \int \Sigma_s(\Omega' \to \Omega)\, \psi(\Omega')\, d\Omega'$$
(energy is left out to keep the notation short). On the boundary, $\psi = 0$ for directions that enter the body (vacuum). A detector has a response function $q^+(x, \Omega)$, for example $\Sigma_d(x)$ inside the detector and 0 outside, and the reading is $R = \langle q^+, \psi \rangle$, the integral of $q^+ \psi$ over all of phase space.

**The adjoint problem.** The adjoint operator reverses the streaming and the scattering:
$$L^+\psi^+ = -\Omega \cdot \nabla \psi^+ + \Sigma_t \psi^+ - \int \Sigma_s(\Omega \to \Omega')\, \psi^+(\Omega')\, d\Omega',$$
with $\psi^+ = 0$ for directions that leave the body. The adjoint flux solves $L^+ \psi^+ = q^+$.

**Reciprocity.** This is a theorem. Integration by parts along each direction gives $\langle \psi^+, L\psi \rangle = \langle L^+\psi^+, \psi \rangle$. The boundary term is zero, because on every part of the boundary either $\psi = 0$ (incoming directions) or $\psi^+ = 0$ (outgoing directions). With $L\psi = q$ and $L^+\psi^+ = q^+$ this gives
$$R = \langle q^+, \psi \rangle = \langle \psi^+, q \rangle.$$
The same reading comes from one forward solve with the true source, or from one adjoint solve with the detector as the source.

**Importance.** This is also a theorem (Lewins 1965; Bell and Glasstone 1970). Let $I(x, \Omega)$ be the expected track-length score that a particle at $x$ with direction $\Omega$ adds to $R$, with all its descendants. Condition on the first flight. The particle reaches the distance $s$ with probability $e^{-\Sigma_t s}$ and scores $q^+$ per unit length there; it collides at $s$ and scatters into $\Omega'$ with density $e^{-\Sigma_t s}\, \Sigma_s(\Omega \to \Omega')$, and then has the expected score $I(x + s\Omega, \Omega')$. So
$$I(x, \Omega) = \int_0^{d(x, \Omega)} e^{-\Sigma_t s} \Big[ q^+(x + s\Omega) + \int \Sigma_s(\Omega \to \Omega')\, I(x + s\Omega, \Omega')\, d\Omega' \Big] ds,$$
where $d(x, \Omega)$ is the distance to the boundary. The derivative along the path gives $-\Omega \cdot \nabla I + \Sigma_t I = q^+ + \int \Sigma_s(\Omega \to \Omega') I(\Omega')\, d\Omega'$, and $I = 0$ where the particle leaves the body. This is the adjoint equation with its boundary condition, so $I = \psi^+$. Reciprocity then reads: the reading is the source, weighted by the importance of each source particle.

**Discrete form.** The same idea holds for any Markov chain with scores. Let a particle move from state $i$ to state $j$ with probability $P_{ij}$, where the rows sum to less than 1 (the rest is absorption or leakage), and score $s_i$ at each visit to $i$. The importance $v_i$ is the expected total score of a particle that starts in $i$. Conditioning on the first step gives $v = s + Pv$. The expected number of visits $f$ from a start distribution $q$ solves $f = q + P^T f$. Then $q^T v = q^T (I - P)^{-1} s = f^T s$, which is reciprocity in matrix form: the adjoint is the transpose.

**Symmetry in a slab.** In a one-speed slab with isotropic scattering, $\psi^+(x, \mu) = \psi_d(x, -\mu)$, where $\psi_d$ is the forward angular flux with the source $q^+$. The reason is that reversing $\mu$ maps $L^+$ onto $L$ when the scattering kernel depends only on the angle between the two directions. So a forward code gives the adjoint for such problems, and the scalar adjoint flux is the forward scalar flux of the detector source. The [CADIS](/cadis/) page uses this.

## Examples

**A beam in a pure absorber.** Take a rod of length 2 cm with $\Sigma_t = 1\ \mathrm{cm}^{-1}$, no scattering, and particles that move only to the right ($\mu = 1$). The detector scores the track length in $[1, 2]$, so $q^+ = 1$ there and 0 elsewhere. The adjoint equation is $-d\psi^+/dx + \psi^+ = q^+$ with $\psi^+(2) = 0$. On $[1, 2]$ the solution is $\psi^+(x) = 1 - e^{-(2 - x)}$, and on $[0, 1]$ it is $\psi^+(x) = (1 - e^{-1})\, e^{-(1 - x)}$. Check by hand: on $[1, 2]$, $d\psi^+/dx = -e^{-(2 - x)}$, so $-d\psi^+/dx + \psi^+ = e^{-(2 - x)} + 1 - e^{-(2 - x)} = 1$; on $[0, 1]$, $\psi^+$ is a multiple of $e^{x}$, so the left side is 0; and the two pieces meet at $x = 1$ with the value $1 - e^{-1}$. The importance of a source particle at $x = 0$ is $\psi^+(0) = (1 - e^{-1})/e = 0.232544$. The forward way gives the same number: the flux of the beam is $e^{-x}$, and $R = \int_1^2 e^{-x}\, dx = e^{-1} - e^{-2} = 0.367879 - 0.135335 = 0.232544$. The importance grows by the factor $e = 2.718$ from $x = 0$ to $x = 1$, which is the splitting ratio that [particle splitting](/particle-splitting/) at $x = 1$ would use.

**A two-state chain.** Take $P = \begin{pmatrix} 0.2 & 0.3 \\ 0.1 & 0.4 \end{pmatrix}$, a score $s = (0, 1)$ (the detector is state 2) and a source $q = (1, 0)$. The adjoint equations are $v_1 = 0.2 v_1 + 0.3 v_2$ and $v_2 = 1 + 0.1 v_1 + 0.4 v_2$. The first gives $v_1 = 0.375 v_2$, the second then gives $0.5625\, v_2 = 1$, so $v_2 = 16/9$ and $v_1 = 2/3$. The forward equations are $f_1 = 1 + 0.2 f_1 + 0.1 f_2$ and $f_2 = 0.3 f_1 + 0.4 f_2$, so $f_2 = f_1/2$, $0.75 f_1 = 1$, $f_1 = 4/3$ and $f_2 = 2/3$. Both ways give $R = q^T v = v_1 = 2/3$ and $R = s^T f = f_2 = 2/3$.

**A shielding slab.** In the slab of the [CADIS](/cadis/) page (10 cm, $\Sigma_t = 1\ \mathrm{cm}^{-1}$, scattering ratio 0.5, source in $[0, 1]$, detector in $[9, 10]$), a discrete ordinates solve with 40 cells and $S_{16}$ gives a scalar adjoint flux of $1.02$ at its peak in the detector and $4.49 \times 10^{-5}$ in the first source cell, a ratio of about 23 000. With a scattering ratio of 0.9 the ratio is only about 290, because scattered particles carry importance through the wall. In both cases the adjoint estimate $\langle \psi^+, q \rangle$ and the forward estimate $\langle q^+, \psi \rangle$ agree to rounding ($7.3771 \times 10^{-5}$ and $0.011123$ per source particle). This is a measurement of the discrete reciprocity of the solver, not a new theorem.

## Where it is used

- **Variance reduction.** The importance gives the target weights of [weight windows](/weight-window/), the splitting ratios of [particle splitting](/particle-splitting/), the biased source of [CADIS](/cadis/) and [FW-CADIS](/fw-cadis/), and a guide for the stretching parameter of the [exponential transform](/exponential-transform/). If the weight of every particle is kept equal to $R/\psi^+$, every particle carries the same expected score; with the exact importance this gives a zero variance game (see the proof on the CADIS page).
- **Perturbation theory.** For the [k-eigenvalue problem](/k-eigenvalue-problem/), the first-order change of the reactivity from a small change of the cross sections is an integral of the change, weighted by the forward flux and the adjoint flux, divided by the adjoint-weighted fission source. The adjoint fundamental mode measures the expected number of descendants that a neutron has many generations later, if the dominant eigenvalue is simple.
- **Sensitivity analysis.** One adjoint solve gives the derivative of one response with respect to all cross sections, as in general [adjoint sensitivity analysis](/adjoint-sensitivity-analysis/).
- **Source and detector design.** With $R = \langle \psi^+, q \rangle$, one adjoint solve gives the reading for every source position and spectrum.

The [adjoint model](/adjoint-model/) of data assimilation uses the same mathematics, the transpose of a linear operator with respect to an inner product, but for a different goal: there it is the transpose of the linearized forecast model, run backward in time to get the gradient of a cost function. Here the adjoint is a field with a direct physical meaning, the expected score of a particle.

## References
