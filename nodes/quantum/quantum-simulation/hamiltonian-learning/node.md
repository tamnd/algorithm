---
tag: 7XH1T8
kind: problem
slug: hamiltonian-learning
name: Hamiltonian learning
aliases:
- learning a Hamiltonian from dynamics
- Hamiltonian parameter estimation
area: quantum/quantum-simulation
level: research
summary: "Recover the coefficients of an unknown local Hamiltonian H = sum_a c_a P_a to within epsilon from access to its dynamics e^(-iHt) or to its Gibbs states e^(-beta H)/Z."
prereqs: [pauli-string-decomposition, hamiltonian-simulation, density-matrix, quantum-measurement]
see_also: [quantum-state-tomography, gibbs-state-preparation, maximum-likelihood-estimation, pac-learning, hoeffding-inequality, partition-function, density-matrix-exponentiation, quantum-phase-estimation]
sources:
  - paper: doi:10.1038/s41567-021-01232-0
    title: Anurag Anshu, Srinivasan Arunachalam, Tomotaka Kuwahara and Mehdi Soleimanifar, Sample-efficient learning of interacting quantum systems, Nature Physics 17, 2021, pages 931-935
    locator: learning a local Hamiltonian from copies of its Gibbs state with a number of copies polynomial in n, by strong convexity of the log-partition function
  - paper: doi:10.1103/PhysRevLett.130.200403
    title: Hsin-Yuan Huang, Yu Tong, Di Fang and Yuan Su, Learning many-body Hamiltonians with Heisenberg-limited scaling, Physical Review Letters 130, 2023, article 200403 (arXiv:2210.03030)
    locator: learning the coefficients of a local Hamiltonian from its dynamics with total evolution time of order 1/epsilon
  - paper: arxiv:2310.02243
    title: Ainesh Bakshi, Allen Liu, Ankur Moitra and Ewin Tang, Learning quantum Hamiltonians at any temperature in polynomial time, 2023
    locator: a polynomial-time learner from Gibbs states for every constant inverse temperature
  - paper: doi:10.1103/PhysRevLett.122.020504
    title: Eyal Bairey, Itai Arad and Netanel H. Lindner, Learning a local Hamiltonian from local measurements, Physical Review Letters 122, 2019, article 020504
    locator: recovering a local Hamiltonian from local expectation values in one eigenstate or steady state, as the null space of a constraint matrix
  - paper: doi:10.1103/PhysRevLett.112.190501
    title: Nathan Wiebe, Christopher Granade, Christopher Ferrie and David G. Cory, Hamiltonian learning and certification using quantum resources, Physical Review Letters 112, 2014, article 190501
    locator: Bayesian learning of Hamiltonian parameters with a trusted quantum simulator that computes the likelihoods
  - paper: doi:10.1038/s41567-020-0932-7
    title: Hsin-Yuan Huang, Richard Kueng and John Preskill, Predicting many properties of a quantum system from very few measurements, Nature Physics 16, 2020, pages 1050-1057
    locator: Theorem 1 (median of means over K = 2 ln(2M/delta) batches of N = 34 ||O||^2_shadow / epsilon^2 snapshots) and the shadow norm 3^k of a Pauli string of weight k for random Pauli measurements
---

*Hamiltonian learning* is the problem of finding the coefficients of an unknown Hamiltonian from experiments on the system it governs. The Hamiltonian is assumed to have a known form $H = \sum_{a=1}^Mc_aP_a$, with $P_a$ given Pauli strings that act on at most $k$ qubits each and unknown real coefficients $c_a$, and the learner may either run the dynamics $e^{-iHt}$ on inputs of its choice or receive copies of the Gibbs state $e^{-\beta H}/Z$. The goal is every $c_a$ to within $\epsilon$ with probability at least $1 - \delta$. A full description of $e^{-iHt}$ by process [tomography](/quantum-state-tomography/) costs a number of experiments exponential in $n$; with the local structure, polynomial cost is possible. From dynamics, a total evolution time of order $1/\epsilon$ is achievable (Huang, Tong, Fang and Su, 2023), and it is optimal by the Heisenberg limit; from Gibbs states, a number of copies polynomial in $n$ is enough at any constant temperature (Anshu et al., 2021, for the sample count; Bakshi, Liu, Moitra and Tang, 2023, for polynomial time).

## In plain words

Physicists describe a quantum system by a rule that says how each part of it pushes on its neighbours, and how strongly. Often the form of the rule is known, but the strengths are not, for example in a new device whose parts were built with small errors. Hamiltonian learning asks for those strengths. You may let the system run for a time you choose and then look at it, or you may look at the system after it has settled at some temperature. Each look gives only a little random information, so you must repeat it many times. The questions are how many looks, and how much total running time, are needed for a given accuracy, and how the answer grows with the size of the system.

## Definition

Fix $n$ qubits, a set of $M$ distinct non-identity Pauli strings $P_1, \ldots, P_M$, each of weight at most $k$, and unknown coefficients $c \in [-1, 1]^M$, so $H = \sum_ac_aP_a$ as in a [Pauli string decomposition](/pauli-string-decomposition/). Qubit 0 is the least significant bit, as on [quantum state](/quantum-state/). The output is $\hat c$ with $\max_a|\hat c_a - c_a| \le \epsilon$ with probability at least $1 - \delta$. The cost depends on the access model:

- **Dynamics.** An experiment prepares a state of the learner's choice, applies $e^{-iHt}$ for a chosen $t \ge 0$, possibly interleaved with the learner's own gates, and measures. The costs are the number of experiments and the total evolution time $T$, the sum of all $t$ used.
- **Gibbs states.** The learner gets copies of $\rho_\beta = e^{-\beta H}/Z$, $Z = \mathrm{Tr}\,e^{-\beta H}$, at a known inverse temperature $\beta$, and may measure them. The cost is the number of copies.

In both models the classical running time is a further cost.

## Variants

- **Eigenstates and steady states.** The learner gets copies of one eigenstate of $H$, or of a steady state of the dynamics. Every such state $\rho$ satisfies $\mathrm{Tr}(\rho[H, O]) = 0$ for every observable $O$, which gives linear equations in $c$; Bairey, Arad and Lindner show that these equations often determine $c$ up to scale.
- **Unknown structure.** The support of the terms is not given, only the locality $k$ or a sparsity bound, and the learner must find which $P_a$ appear.
- **Other error measures.** The $\ell_2$ error $\|\hat c - c\|_2$, which for $M$ terms is up to $\sqrt M$ times the $\ell_\infty$ error.
- **Open systems.** The dynamics is a Lindbladian, and the learner must find both the Hamiltonian and the dissipative part.
- **With a trusted simulator.** The learner also has a quantum simulator that can run any candidate $H'$, and compares the two, as in Wiebe et al.

## Examples

**One qubit at temperature.** For $H = hZ$, $\langle Z\rangle_\beta = -\tanh(\beta h)$, so $h = -\mathrm{artanh}(\langle Z\rangle)/\beta$. The derivative $dh/d\langle Z\rangle = -1/(\beta(1 - \langle Z\rangle^2))$ shows where learning is hard: at high temperature the factor $1/\beta$ amplifies the statistical error of $\langle Z\rangle$, so the number of copies grows as $1/(\beta^2\epsilon^2)$; at low temperature $\langle Z\rangle$ is near $\pm1$ and the factor $1/(1 - \langle Z\rangle^2)$ grows as $e^{2\beta|h|}$.

**One qubit in time.** For $H = \tfrac\omega2Z$ and the input $|{+}\rangle$, the expectation of $X$ after time $t$ is $\cos(\omega t)$. A shift $\Delta\omega$ of the frequency moves this value by up to $t\,\Delta\omega$, so long evolutions resolve small shifts. With total time $T$ spent at short times $t$ and $T/t$ repetitions, the error falls as $1/(t\sqrt{T/t}) = 1/\sqrt{tT}$; with adaptively chosen times up to $T$, as in [phase estimation](/quantum-phase-estimation/), it falls as $1/T$.

**Three qubits.** All numbers below are from the page's simulator with exact density matrices and sampled measurements. Let $H = -Z_2Z_1 - 0.8Z_1Z_0 - 0.6X_2 - 0.5X_1 - 0.7X_0$. At $\beta = 1$ the Gibbs state has $\langle Z_2Z_1\rangle = 0.6744$, $\langle Z_1Z_0\rangle = 0.5655$, $\langle X_2\rangle = 0.4299$, $\langle X_1\rangle = 0.3223$ and $\langle X_0\rangle = 0.5230$. These local expectation values are the data that learners from Gibbs states start from. Classical shadows from random single-qubit Pauli measurements, in the form of Huang, Kueng and Preskill, estimate all $M = 36$ Pauli strings of weight 1 or 2 with the sample count of their theorem for $\epsilon = 0.3$ and $\delta = 0.01$: $K = 18$ batches of $N = 3400$ snapshots, 61200 in all. With seed 1 the largest error over the 36 values is $0.037$ and the mean error is $0.010$, so the theorem is conservative here by a factor of about 8. At high temperature, $\rho_\beta = (I - \beta H)/2^n + O(\beta^2)$, so $c_a \approx -\mathrm{Tr}(P_a\rho_\beta)/\beta$; for this $H$ the largest error of that first-order value is $0.0778$, $0.0209$, $0.00533$ and $0.00134$ at $\beta = 0.4$, $0.2$, $0.1$ and $0.05$.

## Known algorithms

- **Heisenberg-limited learning from dynamics.** Huang, Tong, Fang and Su (2023) learn all coefficients of a local Hamiltonian with total evolution time $O(\epsilon^{-1}\log(1/\delta))$ for fixed locality and bounded degree, using evolutions interleaved with control operations that decouple the system into small pieces.
- **Learning from Gibbs states.** Anshu, Arunachalam, Kuwahara and Soleimanifar (2021) show that the log-partition function is strongly convex in $c$, so a maximum-entropy fit to local expectation values, a form of [maximum likelihood estimation](/maximum-likelihood-estimation/), recovers $c$ from a number of copies polynomial in $n$ for constant $\beta$. Bakshi, Liu, Moitra and Tang (2023) give a learner that is polynomial in both copies and time at every constant $\beta$.
- **Learning from one eigenstate.** Bairey, Arad and Lindner (2019) collect the equations $\mathrm{Tr}(\rho[H, O]) = 0$ for local $O$ and take the null space.
- **Bayesian learning with a trusted simulator.** Wiebe, Granade, Ferrie and Cory (2014) update a distribution over $c$ with likelihoods computed on a second quantum device.
- **Local data from shadows.** Most learners need many local expectation values; classical shadows give $M$ of them on $k$ qubits from $O(3^k\log(M/\delta)/\epsilon^2)$ single-copy measurements, as in the example. The method is described on [quantum state tomography](/quantum-state-tomography/).

## Bounds

- **Heisenberg limit (dynamics model).** Any learner that estimates a single coefficient to error $\epsilon$ with constant probability needs total evolution time $\Omega(1/\epsilon)$; this is the standard bound of quantum metrology, and the algorithm of Huang et al. meets it up to the logarithmic factor in $1/\delta$. Learners that use only fixed short evolutions and average independent shots reach $T$ of order $1/\epsilon^2$, the standard quantum limit.
- **Copies of the Gibbs state (Gibbs model).** Anshu et al. show that a number of copies polynomial in $n$, $1/\epsilon$ and $\log(1/\delta)$ suffices for local Hamiltonians at constant $\beta$, and that polynomially many are also necessary. Their bound grows fast with $\beta$; the one-qubit example shows a growth as $1/\beta^2$ at high temperature and as $e^{2\beta|h|}$ at low temperature already for a single coefficient.
- **Shadow sample count.** With random Pauli measurements, $68\ln(2M/\delta)\,3^k/\epsilon^2$ snapshots estimate $M$ Pauli expectation values of weight at most $k$ to error $\epsilon$ with probability $1 - \delta$, by the theorem of Huang, Kueng and Preskill, since a single-snapshot estimate of a weight-$k$ Pauli string takes the values $\pm3^k$ and $0$ and has second moment exactly $3^k$.
- **Without structure.** If $H$ is an arbitrary Hermitian matrix on $n$ qubits, it has $4^n$ real parameters, and learning it is as hard as process tomography.

## Reductions

- **Gibbs states to expectation values.** The Gibbs state $e^{-\beta H}/Z$ is the state of maximum entropy among all states with the same values of $\langle P_a\rangle$, and the map from $c$ to these values is one to one, since $\log Z$ is strictly convex in $c$. So learning from Gibbs states reduces to estimating the $M$ values $\langle P_a\rangle$ and inverting a convex map; the difficulty is how much the inversion amplifies errors, which is what strong convexity bounds.
- **Short-time dynamics to linear regression.** For an observable $O$, $\frac{d}{dt}\langle O\rangle_t = i\langle[H, O]\rangle_t$, which is linear in $c$. Estimates of the left side at many $O$ and inputs give a linear system for $c$.
- **Eigenstates to a null space.** As in the variant above, an eigenstate gives a homogeneous linear system whose null space contains $c$.
- **Relation to phase estimation.** For a single term, learning $c$ from dynamics is the [phase estimation problem](/phase-estimation-problem/) for $e^{-icPt}$ on an eigenvector of $P$, which explains the $1/\epsilon$ scaling.

## Applications

- **Calibration of quantum hardware.** The couplings and fields of superconducting, ion and atom devices are learned to build and correct their gates.
- **Verification of quantum simulators.** A quantum simulator meant to run $H$ is checked by learning the Hamiltonian it actually runs, possibly with a second trusted device as in Wiebe et al.
- **Effective models.** The local Hamiltonian of a material or of a part of a larger system is learned from measured correlations, as an inverse problem to [Gibbs state preparation](/gibbs-state-preparation/).
- **Entanglement Hamiltonians.** The logarithm of a reduced state is a Hamiltonian, and learning it from measurements of the reduced state is a Gibbs-state learning problem with $\beta = 1$.

## References
