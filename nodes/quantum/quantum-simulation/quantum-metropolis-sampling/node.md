---
tag: TDQQYG
kind: algorithm
slug: quantum-metropolis-sampling
name: Quantum Metropolis sampling
aliases:
- quantum Metropolis algorithm
- quantum Metropolis walk
area: quantum/quantum-simulation
level: research
summary: "Temme et al. (2011): a random walk on the eigenvectors of H that applies a random unitary, measures the energy and accepts by the Metropolis rule; its fixed point is the Gibbs state."
solves: [gibbs-state-preparation]
model: quantum-circuit-model
complexity:
  vars: {n: the number of qubits, t: the number of steps, r: the number of bits of an energy measurement}
  time: {steps: t, ideal_moves_and_energy_measurements_per_step: O(1), phase_estimation_time_per_energy_measurement: O(2^r)}
  space: {qubits: O(n + r)}
properties: {randomized: true, exact: false, reversible_chain: true, needs_nondegenerate_spectrum: true, sign_problem_free: true}
history:
  year: 2011
  people: [Kristan Temme, Tobias J. Osborne, Karl G. Vollbrecht, David Poulin, Frank Verstraete]
  note: Temme et al. posted the algorithm on arXiv in 2009 and published it in Nature in 2011. It builds on the Metropolis rule of 1953 and on the rewinding method of Marriott and Watrous (2005).
prereqs: [metropolis-hastings, quantum-phase-estimation, gibbs-state-preparation, density-matrix]
see_also: [detailed-balance, mixing-time, spectral-gap, quantum-imaginary-time-evolution, open-quantum-system-simulation, glauber-dynamics, simulated-annealing, partition-function]
sources:
  - paper: doi:10.1038/nature09770
    title: Kristan Temme, Tobias J. Osborne, Karl G. Vollbrecht, David Poulin and Frank Verstraete, Quantum Metropolis sampling, Nature 471, 2011, pages 87-90 (arXiv:0911.3635)
    locator: the walk on eigenvectors with energy measurement by phase estimation, the Metropolis acceptance, the return to the old eigenvector on rejection, and the claim that the method avoids the sign problem
  - paper: doi:10.1007/s00037-005-0194-x
    title: Chris Marriott and John Watrous, Quantum Arthur-Merlin games, Computational Complexity 14, 2005, pages 122-152
    locator: the in-place amplification by alternating two binary measurements, the method that quantum Metropolis uses to undo a measurement
  - paper: doi:10.1073/pnas.1111758109
    title: Man-Hong Yung and Alan Aspuru-Guzik, A quantum-quantum Metropolis algorithm, Proceedings of the National Academy of Sciences 109, 2012, pages 754-759
    locator: a Szegedy-type quantum walk version that prepares a purification of the Gibbs state with a quadratic speedup in the gap
  - paper: arxiv:2303.18224
    title: Chi-Fang Chen, Michael J. Kastoryano, Fernando G. S. L. Brandao and Andras Gilyen, Quantum thermal state preparation, 2023
    locator: Lindbladian Gibbs samplers built from operator Fourier transforms, with approximate detailed balance and a cost bound in terms of the mixing time
  - paper: arxiv:2311.09207
    title: Chi-Fang Chen, Michael J. Kastoryano and Andras Gilyen, An efficient and exact noncommutative quantum Gibbs sampler, 2023
    locator: a Lindbladian that is exactly detailed balanced for the Gibbs state, called a continuous-time quantum analogue of Metropolis-Hastings
---

Quantum Metropolis sampling is an algorithm for [Gibbs state preparation](/gibbs-state-preparation/), introduced by Temme, Osborne, Vollbrecht, Poulin and Verstraete in 2011. It is the [Metropolis-Hastings](/metropolis-hastings/) walk with the configurations replaced by the eigenvectors $|E_i\rangle$ of the Hamiltonian $H$. A step applies a random unitary $C$ to the current eigenvector, measures the energy to get a new eigenvector $|E_k\rangle$, and accepts it with probability $\min(1, e^{-\beta(E_k - E_i)})$; on rejection the walk returns to $|E_i\rangle$. If the move set contains $C^\dagger$ with the same probability as $C$, the walk satisfies [detailed balance](/detailed-balance/) for the weights $e^{-\beta E_i}/Z$, so its fixed point is the Gibbs state $e^{-\beta H}/Z$. The method needs no knowledge of the eigenvectors and has no sign problem, but the number of steps is the [mixing time](/mixing-time/) of the walk, which is not known in general, and the circuit version obtains detailed balance only approximately.

## In plain words

A classical Metropolis walk samples the states of a system at a given temperature: it proposes a small random change, keeps the change if it lowers the energy, and keeps it only sometimes if it raises the energy. The quantum version does the same with the true quantum states of fixed energy. It gives the current state a random kick, measures the energy, and then decides by the same rule whether to keep the new state. The hard part is going back when the rule says no, because the measurement has destroyed the old state; the method uses a trick that repeats two measurements until the old state comes back. After enough steps the walk visits each state with the probability that physics predicts at that temperature.

## The problem

The input is a Hamiltonian $H$ on $n$ qubits, an inverse temperature $\beta \ge 0$, a list of unitary moves $C_j$ with probabilities $p_j$, a starting eigenvector and a number of steps $t$. The output is a state whose average over the random outcomes approximates the Gibbs state $\rho_\beta = e^{-\beta H}/Z$, $Z = \mathrm{Tr}\,e^{-\beta H}$. On this page the energy measurement is ideal: it is the projective measurement onto the eigenvectors of $H$, and $H$ has a nondegenerate spectrum $E_0 < E_1 < \cdots < E_{2^n - 1}$, so the outcome fixes the eigenvector. Qubit 0 is the least significant bit, as on [quantum state](/quantum-state/).

## The algorithm

```pseudo id=main
QUANTUM-METROPOLIS(H, β, C_1..C_K with probabilities p_1..p_K, i_0, t)
L1  ψ ← |E_{i_0}⟩, E ← E_{i_0}
L2  repeat t times
L3      draw j with probability p_j
L4      φ ← C_j ψ
L5      measure the energy of φ: outcome E_k with probability |⟨E_k|φ⟩|², state |E_k⟩
L6      with probability min(1, e^(-β(E_k - E))): ψ ← |E_k⟩, E ← E_k     ▷ accept
L7      else return to ψ = |E⟩                                           ▷ reject
L8  return ψ
```

The walk never needs the eigenvectors in advance: line L5 produces them. In the circuit of Temme et al. line L5 is [quantum phase estimation](/quantum-phase-estimation/) of $e^{-iH}$ into an energy register with $r$ bits, and lines L6 and L7 are done coherently: a rotation of one ancilla qubit, controlled by the old and the new energy registers, encodes the acceptance probability, and the ancilla is measured. On acceptance the new energy register is kept. On rejection the old state $|E_i\rangle$ is gone, since line L5 measured the system. It is recovered by the rewinding method of Marriott and Watrous: two binary measurements, one that asks whether the move was rejected and one that asks whether the energy is again $E_i$, are applied in turn until the second one says yes. The code simulates the ideal version, which keeps a copy of the old state.

## Example

**One qubit by hand.** Let $H = -(\cos\phi\,Z + \sin\phi\,X)$, with eigenvalues $E_0 = -1$ and $E_1 = 1$, and take the single move $C = Z$, which is its own inverse. Since $\langle E_1|Z|E_0\rangle$ has modulus $\sin\phi$, a step from $|E_0\rangle$ goes up with probability $\sin^2\phi\,e^{-2\beta}$ and a step from $|E_1\rangle$ goes down with probability $\sin^2\phi$. The ratio of the two is $e^{-2\beta} = \pi_1/\pi_0$, so the Gibbs weights are stationary. The second eigenvalue of the $2 \times 2$ transition matrix is $1 - \sin^2\phi\,(1 + e^{-2\beta})$, so the walk mixes fast for $\phi$ near $\pi/2$ and not at all for $\phi = 0$, where the move commutes with $H$.

**Three qubits.** All numbers below are from the page's simulator in the ideal model, for $H = -Z_2Z_1 - Z_1Z_0 - X_2 - X_1 - X_0 - 0.3Z_2$, with the nine moves $X_q, Y_q, Z_q$ drawn uniformly. The spectrum is $\pm3.56025, \pm2.56899, \pm1.04045, \pm0.04919$, with no degeneracy. At $\beta = 1$ the Gibbs weights of the four lowest levels are $0.6572, 0.2439, 0.0529, 0.0196$, and the density matrix $\sum_i\pi_i|E_i\rangle\langle E_i|$ agrees with $e^{-\beta H}/Z$ from a Taylor series to $6 \cdot 10^{-16}$. The spectral gap of the transition matrix is $0.333$, $0.278$ and $0.246$ for $\beta = 0.5$, $1$ and $2$. From the highest eigenvector at $\beta = 1$, the total variation distance to the Gibbs weights is:

| steps $t$ | 0 | 1 | 2 | 5 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|---|
| distance | 0.999 | 0.879 | 0.716 | 0.319 | 0.0747 | 0.00311 | $4.7 \cdot 10^{-6}$ |

Sampling 2000 trajectories of 10 steps from the same start with seed 7, the frequency of each final eigenvector differs from the exact distribution after 10 steps by at most $0.0064$, inside the radius $0.043$ that [Hoeffding's inequality](/hoeffding-inequality/) with a [union bound](/union-bound/) gives at failure probability $0.01$. The fraction of accepted moves is $0.557$.

## Correctness

The full proof is below. In the ideal model the walk is a Markov chain on the eigenvectors with $T_{ki} = \big(\sum_jp_j|\langle E_k|C_j|E_i\rangle|^2\big)\min(1, e^{-\beta(E_k - E_i)})$ for $k \ne i$. If the move set is balanced, that is, $C^\dagger$ is in it with the probability of $C$, then the first factor is symmetric in $i$ and $k$, and $\min(1, e^{-\beta(E_k - E_i)})e^{-\beta E_i}$ is symmetric too, so $T_{ki}\pi_i = T_{ik}\pi_k$ and the Gibbs state is stationary. If the moves generate every matrix, for example the Pauli matrices on every qubit, no proper set of eigenvectors is closed under the walk, so for $\beta > 0$ the chain is irreducible and aperiodic, and it converges to the Gibbs state with $2\,\mathrm{TV} \le \sqrt{(1 - \pi_x)/\pi_x}\,(1 - \gamma)^t$ for the [spectral gap](/spectral-gap/) $\gamma$ and the start $x$. Without balance the fixed point can differ from the Gibbs state.

Not proved: any bound on $\gamma$ for a family of Hamiltonians, and exact detailed balance for the circuit version. With phase estimation of finite resolution, energies are rounded, eigenvalues closer than the resolution mix, and the stationary state is close to the Gibbs state only to the extent that Temme et al. bound those errors.

## Complexity

- **Steps.** The number of steps is the mixing time of the chain, $O(\gamma^{-1}\log(1/(\pi_{\min}\epsilon)))$ for distance $\epsilon$ in the ideal model, by the bound above. As for classical Metropolis chains, $\gamma$ depends on $H$, $\beta$ and the moves, and can be exponentially small in $n$ at low temperature.
- **One step, ideal model.** One move and one energy measurement, plus one more measurement to return on rejection.
- **One step, circuit model.** An energy measurement to $r$ bits by phase estimation needs controlled evolution under $H$ for total time $O(2^r)$, done by [Hamiltonian simulation](/hamiltonian-simulation/). On rejection the rewinding loop repeats measurements a random number of times.
- **Space.** The $n$ system qubits, energy registers of $r$ qubits for the old and the new energy, and one acceptance qubit: $O(n + r)$ qubits.

## Properties

- **No sign problem.** The acceptance probabilities are nonnegative by construction, so the walk does not suffer from the negative weights that limit quantum Monte Carlo for fermions and frustrated magnets. This was the main motivation of Temme et al.
- **Reversible chain.** With a balanced move set the chain is reversible with respect to the Gibbs weights, so its eigenvalues are real and the spectral gap controls convergence, as for classical reversible chains.
- **Classical Metropolis as a special case.** If $H$ is diagonal in the computational basis with a nondegenerate spectrum and the moves are single bit flips $X_q$, the walk is exactly classical Metropolis with uniform single-flip proposals.
- **Energy measurement destroys coherence.** Each step leaves the system in an eigenvector, so the output is a classical mixture of eigenvectors. This is right for the Gibbs state, which is diagonal in the eigenbasis, but the walk cannot produce a purification of it.

## Variants and improvements

- **Quantum-quantum Metropolis.** Yung and Aspuru-Guzik (2012) build a Szegedy-type quantum walk from the same transition rule, which prepares a coherent purification of the Gibbs state with a cost that scales as the inverse square root of the gap.
- **Lindbladian samplers.** Chen, Kastoryano, Brandao and Gilyen (2023) replace the discrete steps by a continuous-time Lindbladian built from operator Fourier transforms, which avoids the rewinding step and has an approximate detailed balance with explicit error bounds. Chen, Kastoryano and Gilyen (2023) give a Lindbladian that is exactly detailed balanced for the Gibbs state, with a cost of order the mixing time times $\beta$ up to logarithmic factors; it is simulated with methods of [open quantum system simulation](/open-quantum-system-simulation/).
- **Annealing.** As with [simulated annealing](/simulated-annealing/), lowering $\beta^{-1}$ slowly toward zero turns the sampler into a heuristic for the ground state.
- **Other moves.** Any balanced move set works, for example pairs $e^{\mp i\theta P/2}$ of Pauli rotations. Moves that change the state little give high acceptance and slow motion; the choice is a trade-off, as in classical Metropolis.

## When to use it

Use quantum Metropolis sampling when the task is thermal expectation values of a quantum Hamiltonian at a temperature where the walk mixes fast, and classical quantum Monte Carlo fails because of the sign problem. It needs a fault-tolerant computer, since phase estimation and rewinding take long coherent circuits. For new work, consider the Lindbladian samplers of Chen et al., which have better error control. At high temperature, simpler methods exist; see [Gibbs state preparation](/gibbs-state-preparation/). For ground states use [quantum phase estimation](/quantum-phase-estimation/) on a good trial state instead, since the walk at large $\beta$ mixes slowly.

## Pitfalls

- **Unbalanced move sets.** If $C$ is in the set but $C^\dagger$ is not, detailed balance fails. In the three-qubit example, adding the cyclic shift of the eight basis states without its inverse moves the stationary weights away from the Gibbs weights by total variation $0.0168$.
- **Moves that commute with $H$.** A move that commutes with $H$ maps each eigenvector to itself and never changes the energy, as with $\phi = 0$ in the one-qubit example. The moves must generate enough of the operator algebra to connect all eigenvectors.
- **Degenerate or close energies.** If two eigenvalues are closer than the resolution of phase estimation, the measurement does not fix the eigenvector, and the walk leaves the eigenbasis. The ideal model of this page needs a nondegenerate spectrum.
- **Slow mixing.** Small moves such as rotations by small angles give a small gap. In the three-qubit example at $\beta = 1$, rotation pairs $e^{\mp i\theta X_q/2}$ with $\theta = 1.3$ and $e^{\mp i\theta Y_q/2}$ with $\theta = 0.8$ give a gap of $0.0267$, ten times smaller than with Pauli moves.
- **Low temperature.** Near $\beta \to \infty$ the walk becomes a local search on eigenvectors and can stay in a local minimum for an exponentially long time. Preparing low-temperature Gibbs states is QMA-hard in general, so no sampler is fast for every $H$.

## Implementations

## History

The classical Metropolis rule dates from Metropolis, Rosenbluth, Rosenbluth, Teller and Teller in 1953, and Hastings generalized it in 1970. Early quantum Gibbs samplers, such as the one of Poulin and Wocjan (2009), used phase estimation and amplitude amplification with a cost that grows as a power of the Hilbert space dimension. Temme, Osborne, Vollbrecht, Poulin and Verstraete posted quantum Metropolis sampling in 2009 and published it in Nature in 2011; the key idea was the return to the old eigenvector by the rewinding method of Marriott and Watrous (2005). Yung and Aspuru-Guzik gave a quantum walk version in 2012. Since 2023 the field has moved to continuous-time Lindbladian samplers, beginning with Chen, Kastoryano, Brandao and Gilyen.

## References
