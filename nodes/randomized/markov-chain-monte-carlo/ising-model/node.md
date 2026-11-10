---
tag: QENBV9
kind: model
slug: ising-model
name: Ising model
aliases:
- Ising spin model
- Ising ferromagnet
area: randomized/markov-chain-monte-carlo
level: core
summary: A distribution on spin vectors σ ∈ {−1, +1}^V of a graph, with π(σ) ∝ exp(β Σ_{uv∈E} σ_uσ_v + h Σ_v σ_v). Its phase transition makes it the standard MCMC test case.
prereqs: [markov-random-field, partition-function]
see_also: [glauber-dynamics, swendsen-wang, gibbs-sampling, potts-model, hard-core-model, mixing-time, coupling-from-the-past, fpras]
sources:
  - paper: doi:10.1007/BF02980577
    title: Ernst Ising, Beitrag zur Theorie des Ferromagnetismus, Zeitschrift für Physik 31, 1925
    locator: pages 253 to 258 (the one-dimensional chain has no phase transition)
  - paper: doi:10.1017/S0305004100019174
    title: Rudolf Peierls, On Ising's model of ferromagnetism, Mathematical Proceedings of the Cambridge Philosophical Society 32(3), 1936
    locator: pages 477 to 481 (the contour argument for spontaneous magnetization in two dimensions)
  - paper: doi:10.1103/PhysRev.60.252
    title: Hendrik A. Kramers and Gregory H. Wannier, Statistics of the two-dimensional ferromagnet. Part I, Physical Review 60(3), 1941
    locator: pages 252 to 262 (the duality that locates the critical point of the square lattice)
  - paper: doi:10.1103/PhysRev.65.117
    title: Lars Onsager, Crystal statistics. I. A two-dimensional model with an order-disorder transition, Physical Review 65(3-4), 1944
    locator: pages 117 to 149 (the exact free energy of the square lattice with no field)
  - paper: doi:10.1137/0222066
    title: Mark Jerrum and Alistair Sinclair, Polynomial-time approximation algorithms for the Ising model, SIAM Journal on Computing 22(5), 1993
    locator: pages 1087 to 1116 (an FPRAS for the ferromagnetic partition function, and hardness for the antiferromagnet)
  - paper: doi:10.1088/0305-4470/15/10/028
    title: Francisco Barahona, On the computational complexity of Ising spin glass models, Journal of Physics A 15(10), 1982
    locator: pages 3241 to 3253 (ground states of planar spin glasses in polynomial time, and NP-hardness for nonplanar ones)
  - paper: doi:10.1007/s00440-008-0189-z
    title: David A. Levin, Malwina J. Luczak and Yuval Peres, Glauber dynamics for the mean-field Ising model, Probability Theory and Related Fields 146, 2010
    locator: pages 223 to 265 (fast mixing with cutoff for β < 1, and exponential mixing time for β > 1, on the complete graph)
  - paper: doi:10.1214/17-AAP1335
    title: Heng Guo and Mark Jerrum, Random cluster dynamics for the Ising model is rapidly mixing, Annals of Applied Probability 28(2), 2018
    locator: pages 1292 to 1313 (random-cluster dynamics and Swendsen-Wang mix in polynomial time on every graph)
  - book: isbn:9781470429621
    title: David A. Levin, Yuval Peres and Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, AMS, 2017
    locator: Chapter 15, The Ising model (Glauber dynamics at high temperature, and slow mixing at low temperature)
---

The Ising model is a probability distribution on the spin configurations $\sigma \in \{-1, +1\}^V$ of a graph $G = (V, E)$. Neighbors that agree are favored when the inverse temperature $\beta$ is positive, and the external field $h$ favors one sign. The normalizing constant is the partition function $Z_G(\beta, h)$. Physicists use it as the simplest model of a magnet with a phase transition. In computer science, it is the standard test case for [Markov chain Monte Carlo](/markov-chain/): [Glauber dynamics](/glauber-dynamics/), [Metropolis](/metropolis-hastings/) and [Swendsen-Wang](/swendsen-wang/) all sample it, and their mixing times change sharply at the phase transition. Computing $Z$ exactly is #P-hard in general, but the ferromagnetic case has an [FPRAS](/fpras/) (Jerrum and Sinclair 1993).

## The machine

A configuration assigns a spin $\sigma_v \in \{-1, +1\}$ to each vertex $v \in V$, so there are $2^n$ configurations for $n = |V|$. The energy (Hamiltonian) is

$$H(\sigma) = -\sum_{uv \in E}J_{uv}\sigma_u\sigma_v - h\sum_{v \in V}\sigma_v,$$

and the Gibbs distribution at inverse temperature $\beta \ge 0$ is

$$\pi(\sigma) = \frac{e^{-\beta H(\sigma)}}{Z}, \qquad Z = \sum_{\sigma \in \{-1, +1\}^V}e^{-\beta H(\sigma)}.$$

The usual case is $J_{uv} = J > 0$ for all edges (ferromagnetic), with $J = 1$. Then each agreeing edge contributes the factor $e^{\beta}$ and each disagreeing edge $e^{-\beta}$, so $\pi(\sigma) \propto e^{2\beta\,a(\sigma)}e^{\beta h\sum_v\sigma_v}$, where $a(\sigma)$ is the number of agreeing edges. With $J < 0$ the model is antiferromagnetic, and with couplings of mixed sign it is a spin glass.

**Small example.** Let $G$ be the 4-cycle with $J = 1$ and $h = 0$. The 16 configurations have 4, 2 or 0 agreeing edges, in 2, 12 and 2 configurations. So

$$Z = 2e^{4\beta} + 12 + 2e^{-4\beta}.$$

At $e^{2\beta} = 3$, this is $Z = 272/9$, and the [Gibbs sampling](/gibbs-sampling/) page checks a sampler against it. On the cycle $C_n$ in general, the transfer matrix gives $Z = (2\cosh\beta)^n + (2\sinh\beta)^n$, and the correlation of two neighbors is $E[\sigma_1\sigma_2] = (t + t^{n-1})/(1 + t^n)$ with $t = \tanh\beta$. At $e^{2\beta} = 3$, $t = 1/2$, and $E[\sigma_1\sigma_2] = 10/17$ for $n = 4$, which matches the brute-force sum $(2 \cdot 864/272 - 4)/4$.

## What it counts

- **The partition function** $Z_G(\beta, h)$, a weighted count of configurations. At $\beta = 0$ it is $2^n$, and as a polynomial in $e^{-2\beta}$ its coefficients count configurations by the number of disagreeing edges, that is, cuts of $G$ by size. So the ground state of the antiferromagnet is a maximum cut.
- **Expectations.** The magnetization $M = \sum_v\sigma_v$, the energy, and correlations $E[\sigma_u\sigma_v]$. These are derivatives of $\log Z$, for example $E[M] = \beta^{-1}\,\partial\log Z/\partial h$.
- **The free energy** $\frac1n\log Z$ per vertex on a sequence of growing graphs, such as $L \times L$ boxes of $\mathbb{Z}^2$. A phase transition is a point where this limit is not analytic in $\beta$.

For MCMC, the model is a family of target distributions with a tunable difficulty: $\beta$ near 0 gives nearly independent spins, and large $\beta$ gives two separated modes, mostly $+1$ and mostly $-1$, with a bottleneck between them.

## Relation to other models

- **[Potts model](/potts-model/).** Spins take $q$ values, and agreeing edges get weight $e^{\beta'}$. The Ising model is the case $q = 2$, with $\beta' = 2\beta$.
- **Random-cluster model.** The Fortuin and Kasteleyn representation writes the Ising and Potts partition functions as a sum over edge subsets. The [Swendsen-Wang](/swendsen-wang/) algorithm is built on it.
- **[Hard-core model](/hard-core-model/).** Both are spin systems on a graph with two states per vertex and nearest-neighbor interaction. The hard-core model has a hard constraint (no two adjacent occupied vertices) instead of an energy.
- **[Markov random fields](/markov-random-field/) and Boltzmann machines.** The Ising model is the pairwise binary Markov random field. With general couplings $J_{uv}$ and fields $h_v$, it is the Boltzmann machine of machine learning, and it is used in image models such as the one of Geman and Geman.
- **The lattice gas.** With $n_v = (1 + \sigma_v)/2 \in \{0, 1\}$, the model becomes a gas of particles on a lattice with nearest-neighbor attraction.

## Known results in the model

**Phase transition.** On the line, Ising (1925) showed that there is no phase transition: the correlation $E[\sigma_0\sigma_k] = (\tanh\beta)^k$ decays for every finite $\beta$. On $\mathbb{Z}^2$, Peierls (1936) proved with a contour argument that the spins stay ordered at low temperature. Kramers and Wannier (1941) located the critical point by duality, and Onsager (1944) computed the free energy exactly. For the square lattice with $J = 1$ and $h = 0$, the critical point is

$$\beta_c = \tfrac12\ln(1 + \sqrt2) \approx 0.4407.$$

For $\beta < \beta_c$, correlations decay exponentially with distance, and for $\beta > \beta_c$ there is spontaneous magnetization. On the complete graph $K_n$ with couplings $1/n$ (the Curie-Weiss model), the critical point is $\beta = 1$.

**Counting complexity.**

- Computing $Z$ exactly is #P-hard for general graphs, as Jerrum and Sinclair (1993) note. The reason is that the coefficients of $Z$ as a polynomial in $e^{-2\beta}$ count cuts by size, and counting the maximum cuts is #P-hard.
- For planar graphs with $h = 0$, $Z$ can be computed exactly in polynomial time by the Pfaffian method of Kasteleyn and Fisher. Barahona (1982) showed that the ground state of a planar spin glass can be found in polynomial time, and that it is NP-hard for nonplanar graphs, for example for two-layer grids.
- Jerrum and Sinclair (1993) gave an [FPRAS](/fpras/) for the ferromagnetic partition function on every graph, with a consistent field. It uses a Markov chain on subgraphs from the high-temperature expansion. They also showed that the antiferromagnetic partition function has no FPRAS unless $\mathrm{RP} = \mathrm{NP}$.

**Mixing of MCMC samplers.**

- **High temperature.** If $\Delta\tanh\beta < 1$, where $\Delta$ is the maximum degree, single-site [Glauber dynamics](/glauber-dynamics/) mixes in $O(n\log n)$ steps, by [path coupling](/path-coupling/) (see Chapter 15 of Levin, Peres and Wilmer).
- **The complete graph.** Levin, Luczak and Peres (2010) showed that Glauber dynamics on the Curie-Weiss model has mixing time of order $n\log n$ with cutoff for $\beta < 1$, of order $n^{3/2}$ at $\beta = 1$, and exponential in $n$ for $\beta > 1$.
- **Low temperature on the lattice.** On an $L \times L$ box with free or periodic boundary and $\beta > \beta_c$, the mostly $+$ and mostly $-$ configurations are separated by a bottleneck whose [conductance](/conductance/) is $e^{-\Theta(L)}$, so local dynamics need time exponential in $L$.
- **Cluster dynamics.** Guo and Jerrum (2018) proved that random-cluster dynamics, and so the [Swendsen-Wang](/swendsen-wang/) algorithm, mixes in polynomial time on every graph at every temperature for the ferromagnetic Ising model with no field. This is the main reason to prefer Swendsen-Wang at low temperature.
- **Exact sampling.** Propp and Wilson used the Ising model as the first large example of [coupling from the past](/coupling-from-the-past/), because the heat-bath dynamics of the ferromagnet is monotone.

## References
