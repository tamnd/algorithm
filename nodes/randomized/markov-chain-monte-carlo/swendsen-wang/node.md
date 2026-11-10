---
tag: PXDRJN
kind: algorithm
slug: swendsen-wang
name: Swendsen-Wang algorithm
aliases:
- cluster MCMC
- Swendsen-Wang dynamics
- Swendsen-Wang cluster algorithm
area: randomized/markov-chain-monte-carlo
level: advanced
summary: A Potts and Ising sampler that bonds each edge with equal spins with probability 1 − e^(−J) and gives each bond cluster a new uniform colour. It is a Gibbs step on the Edwards-Sokal measure.
solves: [sampling-from-stationary-distribution]
model: word-ram
complexity:
  vars: {T: the number of updates, n: the number of vertices, m: the number of edges, α: the inverse Ackermann function from union-find}
  time: {worst: Θ(T (n + m α(n)))}
  space: {extra: Θ(n + m)}
properties: {in_place: false, online: true, deterministic: false, recursive: false}
history:
  year: 1987
  people: [Robert H. Swendsen, Jian-Sheng Wang, Cees M. Fortuin, Pieter W. Kasteleyn, Robert G. Edwards, Alan D. Sokal]
  note: Swendsen and Wang built the algorithm in 1987 on the random-cluster model of Fortuin and Kasteleyn (1972). Edwards and Sokal (1988) explained it as a Gibbs sampler on a joint law of spins and bonds.
prereqs: [ising-model, gibbs-sampling]
see_also: [glauber-dynamics, metropolis-hastings, parallel-tempering, hard-core-model, mixing-time, coupling-from-the-past, connected-components, disjoint-set]
sources:
  - paper: doi:10.1103/PhysRevLett.58.86
    title: Robert H. Swendsen and Jian-Sheng Wang, Nonuniversal critical dynamics in Monte Carlo simulations, Physical Review Letters 58(2), 1987
    locator: pages 86 to 88 (the cluster algorithm and its small dynamic exponent)
  - paper: doi:10.1016/0031-8914(72)90045-6
    title: Cees M. Fortuin and Pieter W. Kasteleyn, On the random-cluster model I. Introduction and relation to other models, Physica 57(4), 1972
    locator: pages 536 to 564 (the random-cluster model and its relation to the Potts model)
  - paper: doi:10.1103/PhysRevD.38.2009
    title: Robert G. Edwards and Alan D. Sokal, Generalization of the Fortuin-Kasteleyn-Swendsen-Wang representation and Monte Carlo algorithm, Physical Review D 38(6), 1988
    locator: pages 2009 to 2012 (the joint measure of spins and bonds, with the algorithm as a Gibbs sampler on it)
  - paper: doi:10.1103/PhysRevLett.62.361
    title: Ulli Wolff, Collective Monte Carlo updating for spin systems, Physical Review Letters 62(4), 1989
    locator: pages 361 to 364 (the single-cluster variant)
  - paper: doi:10.1103/PhysRevLett.63.827
    title: Xiao-Jian Li and Alan D. Sokal, Rigorous lower bound on the dynamic critical exponents of the Swendsen-Wang algorithm, Physical Review Letters 63(8), 1989
    locator: pages 827 to 830 (the autocorrelation time is at least of the order of the specific heat)
  - paper: doi:10.1023/A:1004610900745
    title: Vivek K. Gore and Mark R. Jerrum, The Swendsen-Wang process does not always mix rapidly, Journal of Statistical Physics 97(1-2), 1999
    locator: pages 67 to 86 (exponential mixing time for the Potts model with q at least 3 on the complete graph at the critical temperature)
  - paper: doi:10.1214/17-AAP1335
    title: Heng Guo and Mark Jerrum, Random cluster dynamics for the Ising model is rapidly mixing, Annals of Applied Probability 28(2), 2018
    locator: pages 1292 to 1313 (polynomial mixing time for the Ising model on every graph at every temperature)
---

The Swendsen-Wang algorithm samples the ferromagnetic Potts model, and so the [Ising model](/ising-model/), by changing whole clusters of spins at once. Let $G = (V, E)$ be a graph and $q \ge 2$ an integer. The Potts law on colourings $\sigma \in \{1, \dots, q\}^V$ is

$$\pi(\sigma) \propto \exp\Big(J\sum_{uv \in E}\mathbf 1[\sigma_u = \sigma_v]\Big), \qquad J > 0.$$

The Ising model with coupling $\beta$, $\pi(\sigma) \propto \exp(\beta\sum_{uv}\sigma_u\sigma_v)$, is the case $q = 2$ with $J = 2\beta$. One update keeps each edge whose two ends have the same colour as a bond, independently with probability $p = 1 - e^{-J}$, finds the [connected components](/connected-components/) of the bonds, and gives every component a new colour, uniform and independent. Edwards and Sokal (1988) showed that this is a two-block [Gibbs sampler](/gibbs-sampling/) on a joint law of spins and bonds, and so the Potts law is stationary. Near the critical temperature, where single-spin [Glauber dynamics](/glauber-dynamics/) slows down a lot, the large clusters change in one step. Swendsen and Wang (1987) introduced the method.

## In plain words

On a magnet model, neighbours like to point the same way. Near the critical temperature, the model forms large islands of spins that point the same way, and a method that changes one spin at a time must erode an island spin by spin, which takes very long.

Swendsen-Wang does something else. For every pair of neighbours that point the same way, it flips a biased coin and, on heads, ties them together. The ties join spins into clusters. Then each cluster, as one piece, gets a new direction, chosen at random. A whole island can change in a single step. The coin bias depends on the temperature, and it is chosen so that the method samples the correct model.

## The problem

The input is a graph $G = (V, E)$ with $n$ vertices and $m$ edges, a number of colours $q \ge 2$, a coupling $J > 0$ (given as $p = 1 - e^{-J} \in [0, 1)$), a start $\sigma_0$ and a number of updates $T$. The output is a Markov chain $X_1, \dots, X_T$ on $\{1, \dots, q\}^V$ with the Potts law $\pi$ as stationary distribution, as in [sampling from a stationary distribution](/sampling-from-stationary-distribution/). The model of randomness is one uniform real for each edge with equal ends and one uniform colour for each cluster.

## The algorithm

```pseudo id=main
SWENDSEN-WANG(G = (V, E), q, p, σ0, T)
L1  σ ← σ0
L2  for t ← 1 to T do
L3      A ← the set of edges uv with σ_u = σ_v, each kept independently with probability p
L4      find the connected components C_1, …, C_c of the graph (V, A)
L5      draw colours c_1, …, c_c independently and uniformly from {1, …, q}
L6      σ_v ← c_j for every vertex v in C_j
L7      X_t ← σ
L8  return X_1, …, X_T
```

Line L4 uses [union-find](/disjoint-set/) or a graph search. Vertices with no bond are clusters of size 1, so they get a uniform colour of their own. Edges whose ends have different colours are never bonds: this is what makes the bonds depend on $\sigma$.

## Example

**One update by hand.** Take the path $0 - 1 - 2$ with $q = 2$ and $\sigma = (a, a, b)$, where $a \ne b$. Only edge $01$ has equal ends. With probability $p$ it is a bond, the clusters are $\{0, 1\}$ and $\{2\}$, and each of the $2^2$ colourings that are constant on $\{0, 1\}$ has probability $\frac14$. With probability $1 - p$ there are no bonds, three clusters, and each of the $2^3$ colourings has probability $\frac18$. So

$$P\big((a, a, b) \to (a, a, a)\big) = \frac p4 + \frac{1 - p}8.$$

The reverse move from $(a, a, a)$ needs no bond on edge $12$, so $P((a, a, a) \to (a, a, b)) = (1 - p)\big(\frac p4 + \frac{1 - p}8\big)$. The ratio of the two is $1/(1 - p) = e^J$, which is the ratio $\pi(a, a, a)/\pi(a, a, b)$: detailed balance holds for this pair. The tests check this value and detailed balance for every pair of states on two small graphs, with exact rational matrices.

**Critical slowing down.** Take the Ising model on the $L \times L$ torus at the critical coupling $\beta_c = \frac12\ln(1 + \sqrt2) \approx 0.4407$, and the observable $M^2$, the squared mean spin. The table gives the integrated autocorrelation time, measured from runs of 20000 Swendsen-Wang updates and 20000 sweeps of single-spin Metropolis, both with seed 1 and all spins up at the start. One sweep and one update cost about the same.

| $L$ | Swendsen-Wang | Metropolis sweeps |
|---|---|---|
| 4 | 4.7 | 2.6 |
| 8 | 5.1 | 6.3 |
| 16 | 6.7 | 18.5 |
| 32 | 7.7 | 83.6 |

The time of Metropolis grows quickly with $L$, and that of Swendsen-Wang grows slowly. On the $4 \times 4$ torus the exact value is $\mathbb{E}M^2 = 0.76136$, computed over all $2^{16}$ states, and both chains agree with it within their Monte Carlo error.

## Correctness

**Theorem.** Let $\mu$ be the Edwards-Sokal law on pairs $(\sigma, A)$ with $A \subseteq E$:

$$\mu(\sigma, A) \propto \prod_{e \in A}p\,\mathbf 1[\sigma \text{ is constant on } e]\prod_{e \notin A}(1 - p).$$

Its marginal on $\sigma$ is the Potts law $\pi$, and its marginal on $A$ is the random-cluster law $\phi(A) \propto p^{|A|}(1 - p)^{m - |A|}q^{c(A)}$, where $c(A)$ is the number of components of $(V, A)$. Line L3 draws $A$ from $\mu(A \mid \sigma)$, and lines L4 to L6 draw $\sigma$ from $\mu(\sigma \mid A)$. So the update is a two-block Gibbs sampler on $\mu$, the $\sigma$ chain is reversible with respect to $\pi$, and since every state is reached in one step with positive probability, it converges to $\pi$.

Summing $\mu$ over $A$ gives a factor $p + (1 - p) = 1$ for each edge with equal ends and $1 - p$ for each other edge, so $\pi(\sigma) \propto (1 - p)^{m - a(\sigma)} \propto e^{Ja(\sigma)}$, where $a(\sigma)$ counts the edges with equal ends. Given $\sigma$, the factors of $\mu$ are independent over edges: an edge with equal ends is in $A$ with probability $p$, and an edge with different ends is never in $A$. Given $A$, the only condition on $\sigma$ is that it be constant on each bond, so $\sigma$ is uniform on the $q^{c(A)}$ colourings that are constant on each cluster. The proof file gives the details. The tests check both marginals, stationarity and detailed balance exactly.

## Complexity

One update looks at each edge once, runs union-find on at most $m$ bonds and colours $n$ vertices, so it takes $\Theta(n + m\,\alpha(n))$ time with union by rank and path compression, and $\Theta(n + m)$ memory. On a lattice this is the same order as one sweep of single-spin updates.

**Mixing.** The table above shows the practical gain. Li and Sokal (1989) proved that the autocorrelation time of the energy is at least of the order of the specific heat, so it still grows at the critical point of models whose specific heat diverges. In theory:

- For the Ising model ($q = 2$), Guo and Jerrum (2018) proved that the [mixing time](/mixing-time/) is polynomial in $n$ on every graph and at every temperature.
- For $q \ge 3$, Gore and Jerrum (1999) proved that on the complete graph, at the critical temperature, the mixing time is exponential in $n$. Near a first-order transition, the ordered and disordered phases coexist, and the chain must pass through states of very low probability to go from one to the other.

## Properties

- **Exact.** The Potts law is stationary for every graph, every $q$ and every $J > 0$.
- **No tuning.** There is no step size: $p$ is fixed by $J$.
- **Global moves.** One update can change every spin.
- **Ferromagnetic only.** It needs $J \ge 0$, so that $p \in [0, 1)$. For antiferromagnets and spin glasses the method does not apply in this form.
- **Reversible.** It is a two-block Gibbs sampler, so it is reversible with respect to $\pi$, and every state is reached in one step.

## Variants and improvements

- **Wolff's single-cluster algorithm** (Wolff 1989). Grow one cluster from a random vertex and flip it. Large clusters are picked more often, and it is often faster than Swendsen-Wang in practice.
- **External field.** For the Ising model with a field $h$, give a cluster $C$ the spin $s \in \{-1, +1\}$ with probability proportional to $e^{hs|C|}$, in place of a uniform spin. The proof is the same Gibbs argument.
- **Random-cluster dynamics.** Run a chain on the bonds $A$ with the law $\phi$. This makes sense for every real $q > 0$, not only for integers. Guo and Jerrum first prove their bound for such a chain and then transfer it to Swendsen-Wang.
- **Coupling from the past.** The monotone structure of the random-cluster model allows [exact sampling](/coupling-from-the-past/) for some parameter ranges.
- **Tempering.** For spin glasses, where clusters percolate at all temperatures, use [parallel tempering](/parallel-tempering/) instead.

## When to use it

Use Swendsen-Wang, or Wolff, for ferromagnetic Ising and Potts models near the critical temperature on lattices, where single-spin updates suffer critical slowing down. At high temperature single-spin updates are already fast and simpler. For $q \ge 3$ near a first-order transition, and for frustrated models, the method can be slow or invalid, and other tools such as tempering or [Wang-Landau](/wang-landau/) sampling are better choices.

## Pitfalls

- **The wrong bond probability.** For the Ising model written with $\pm1$ spins and coupling $\beta$, the bond probability is $1 - e^{-2\beta}$, not $1 - e^{-\beta}$. The two conventions differ by a factor 2 in $J$.
- **Bonds on edges with different ends.** Only edges with equal ends may be bonds. Bonding other edges gives a different and wrong chain.
- **Not recolouring single vertices.** A vertex with no bond is a cluster and must get a new random colour too.
- **Assuming it is always fast.** For $q \ge 3$ the mixing time can be exponential near the critical point, as Gore and Jerrum proved.
- **Trusting the diagnostics.** A small measured autocorrelation time of one observable is not a proof of fast mixing, and no diagnostic can prove convergence.

## Implementations

## History

Fortuin and Kasteleyn (1972) introduced the random-cluster model, which writes the Potts partition function as a sum over bond sets. Swendsen and Wang (1987) used this to build the cluster algorithm and found that its dynamic critical exponent for the two-dimensional Ising model was much smaller than that of local algorithms. Edwards and Sokal (1988) gave the joint measure on spins and bonds and showed that the algorithm is a Gibbs sampler on it. Wolff (1989) introduced the single-cluster variant. Li and Sokal (1989) gave a lower bound on the autocorrelation time in terms of the specific heat. Gore and Jerrum (1999) showed exponential mixing for the Potts model with $q \ge 3$ on the complete graph at the critical temperature, and Guo and Jerrum (2018) proved polynomial mixing for the Ising model on every graph.

## References
