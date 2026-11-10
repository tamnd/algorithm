---
tag: 381BFJ
kind: algorithm
slug: parallel-tempering
name: Parallel tempering
aliases:
- Replica exchange Monte Carlo
- replica exchange
- replica exchange Monte Carlo
- Metropolis-coupled MCMC
area: randomized/markov-chain-monte-carlo
level: advanced
summary: Runs chains on the flattened targets π^β with 1 = β_1 > … > β_K and swaps neighbour states with probability min(1, (π(x_{k+1})/π(x_k))^(β_k − β_{k+1})), so the cold chain can leave a mode.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {T: the number of iterations, K: the number of levels, c: the cost of one local step at one level, d: the size of one state}
  time: {worst: Θ(T K c)}
  space: {extra: Θ(K d)}
properties: {in_place: true, online: true, deterministic: false, recursive: false}
history:
  year: 1986
  people: [Robert H. Swendsen, Jian-Sheng Wang, Charles J. Geyer, Koji Hukushima, Koji Nemoto]
  note: Swendsen and Wang exchanged parts of states between replicas at different temperatures in 1986. Geyer proposed swaps of whole states in 1991, and Hukushima and Nemoto made the method common in physics in 1996.
prereqs: [metropolis-hastings]
see_also: [random-walk-metropolis, gibbs-sampling, ising-model, wang-landau, swendsen-wang, mixing-time, spectral-gap, reversible-jump-mcmc]
sources:
  - paper: doi:10.1103/PhysRevLett.57.2607
    title: Robert H. Swendsen and Jian-Sheng Wang, Replica Monte Carlo simulation of spin-glasses, Physical Review Letters 57(21), 1986
    locator: pages 2607 to 2609 (replicas at several temperatures that exchange information)
  - paper: doi:10.1143/JPSJ.65.1604
    title: Koji Hukushima and Koji Nemoto, Exchange Monte Carlo method and application to spin glass simulations, Journal of the Physical Society of Japan 65(6), 1996
    locator: pages 1604 to 1608 (the swap move of whole states and its acceptance probability)
  - paper: doi:10.1209/0295-5075/19/6/002
    title: Enzo Marinari and Giorgio Parisi, Simulated tempering, a new Monte Carlo scheme, Europhysics Letters 19(6), 1992
    locator: pages 451 to 458 (one chain with the temperature as a random variable)
  - paper: doi:10.1039/B509983H
    title: David J. Earl and Michael W. Deem, Parallel tempering, theory, applications, and new perspectives, Physical Chemistry Chemical Physics 7(23), 2005
    locator: pages 3910 to 3916 (a review, with the choice of temperatures)
  - paper: doi:10.1063/1.1917749
    title: Aftab Kone and David A. Kofke, Selection of temperature intervals for parallel-tempering simulations, Journal of Chemical Physics 122(20), 2005
    locator: article 206101 (the spacing of temperatures and the target swap rate)
  - paper: doi:10.1214/08-AAP555
    title: Dawn B. Woodard, Scott C. Schmidler and Mark Huber, Conditions for rapid mixing of parallel and simulated tempering on multimodal distributions, Annals of Applied Probability 19(2), 2009
    locator: pages 617 to 640 (spectral gap bounds by decomposition into modes)
---

Parallel tempering, or replica exchange, samples from a target $\pi$ with several separated modes. It runs $K$ chains at once. Chain $k$ has the flattened target $\pi_k \propto \pi^{\beta_k}$, with inverse temperatures $1 = \beta_1 > \beta_2 > \dots > \beta_K > 0$. Each chain takes ordinary [Metropolis-Hastings](/metropolis-hastings/) steps for its own target, and after that the algorithm proposes to swap the states of two neighbour levels $k$ and $k+1$. It accepts the swap with probability

$$\min\Big(1,\ \Big(\frac{\pi(x_{k+1})}{\pi(x_k)}\Big)^{\beta_k - \beta_{k+1}}\Big).$$

The hot chains cross the low regions between modes easily, and the swaps carry their states down to the cold chain. The joint chain has the product $\pi_1 \otimes \dots \otimes \pi_K$ as a stationary law, so the cold chain $x_1$ has the law $\pi$. Swendsen and Wang (1986) exchanged parts of states between replicas, Geyer (1991) proposed swaps of whole states, and Hukushima and Nemoto (1996) made the method common in physics.

## In plain words

A walker that takes small steps on a landscape with two deep valleys stays in the valley where it starts. Parallel tempering adds more walkers. Each one sees a flatter copy of the landscape, and the flattest copy has almost no hills, so its walker goes everywhere.

From time to time, two walkers on neighbouring copies propose to exchange their positions. A fair coin, weighted by how well each position suits each copy, decides. In this way a good position found by a free walker moves down step by step to the walker on the true landscape. The exchange rule is chosen so that each walker still visits places in the right proportions for its own copy. Only the walker on the true landscape gives the samples that we keep.

## The problem

The input is a function $\log\tilde\pi$ with $\tilde\pi = Z\pi$ positive on a state space $\mathcal{X}$, a ladder $1 = \beta_1 > \dots > \beta_K > 0$, one start per level, a local kernel $P_\beta$ that keeps $\pi^\beta/Z_\beta$ invariant for each $\beta$ in the ladder, and a number of iterations $T$. The output is a Markov chain on $\mathcal{X}^K$ whose stationary law is the product $\Pi(x_1, \dots, x_K) = \prod_k\pi_k(x_k)$, with $\pi_k = \tilde\pi^{\beta_k}/Z_k$. The first coordinate is then a chain with stationary law $\pi$, as in [sampling from a stationary distribution](/sampling-from-stationary-distribution/). The normalizing constants $Z_k$ are not known and are not needed. The model of randomness is the randomness of the local kernels, one uniform choice of a level pair and one uniform real per iteration.

## The algorithm

```pseudo id=main
PARALLEL-TEMPERING(log π̃, β_1 = 1 > … > β_K > 0, x_1, …, x_K, T)
L1  for t ← 1 to T do
L2      for k ← 1 to K do
L3          x_k ← one step of a kernel that keeps π̃^{β_k} invariant, from x_k
L4      draw k uniformly from {1, …, K − 1}
L5      r ← (π̃(x_{k+1}) / π̃(x_k))^{β_k − β_{k+1}}
L6      draw u uniformly from [0, 1)
L7      if u < r then exchange x_k and x_{k+1}
L8      record x_1, …, x_K as the state at time t
L9  return the recorded states
```

Line L5 is computed in logarithms, as $(\beta_k - \beta_{k+1})(\log\tilde\pi(x_{k+1}) - \log\tilde\pi(x_k))$. The swap uses only values of $\log\tilde\pi$ that the local steps already computed. The local step in the implementation is [random-walk Metropolis](/random-walk-metropolis/) with step size $\sigma/\sqrt{\beta}$, because hot levels are wider. Any kernel that keeps $\pi^\beta$ invariant, such as [Gibbs sampling](/gibbs-sampling/) for the [Ising model](/ising-model/), can take its place. The samples of $\pi$ are the values of $x_1$. The other levels are tools, and their samples belong to other laws.

## Example

**The swap test by hand.** Let $\mathcal{X} = \{0, 1, 2, 3\}$ with energies $E = (0, 3, 3, 0)$ and $\tilde\pi(x) = 8^{-E(x)}$, so $\tilde\pi = (1, \frac1{512}, \frac1{512}, 1)$: two modes, 0 and 3, with a barrier between them. Take three levels with $8^{-\beta_k} = \frac18, \frac12, \frac45$, so that the weights of the levels are $(1, \frac1{512}, \frac1{512}, 1)$, $(1, \frac18, \frac18, 1)$ and $(1, 0.512, 0.512, 1)$. Suppose the cold level is at $x_1 = 1$ and level 2 is at $x_2 = 0$. Then

$$r = \Big(\frac{\tilde\pi(0)}{\tilde\pi(1)}\Big)^{\beta_1 - \beta_2} = 512^{2/3} = 64,$$

and the swap is always accepted: the cold level gets the good state 0. The reverse swap, from $(x_1, x_2) = (0, 1)$, has $r = \frac1{64}$. Only the ratio of the weights of one level enters, so $Z_k$ is never needed.

**The effect on mixing.** Each level uses Metropolis with proposals $x \pm 1$ of probability $\frac12$ each. The cold chain alone must climb through state 1, which it enters with probability $\frac12 \cdot \frac1{512}$ per step. The table gives the exact probability, computed with the $64 \times 64$ transition matrix of the joint chain, that the cold level is in the right mode $\{2, 3\}$ after $t$ iterations, when every level starts at 0. The correct value is $0.5$.

| $t$ | parallel tempering | cold chain alone |
|---|---|---|
| 10 | 0.1526 | 0.0030 |
| 25 | 0.3467 | 0.0079 |
| 50 | 0.4608 | 0.0158 |
| 100 | 0.4974 | 0.0313 |
| 200 | 0.5000 | 0.0609 |

**A continuous target.** Let $\pi = 0.3\,\mathcal{N}(-6, 1) + 0.7\,\mathcal{N}(6, 1)$. At $x = 0$ the density is about $e^{-18}$ times its peak. Random-walk Metropolis started at $-6$ with $\sigma = 1.5$ did not visit $x > 0$ once in 20000 steps. Parallel tempering with $\beta = (1, 0.3, 0.1, 0.03)$, the same local step and seed 1 spent a fraction $0.660$ of its 20000 cold samples in the right mode, with 1841 changes of mode, and the swap rates of the three pairs were $0.60$, $0.68$ and $0.72$. The tests check these behaviours against the Monte Carlo error.

## Correctness

**Theorem.** Each swap move (lines L4 to L7) satisfies [detailed balance](/detailed-balance/) with respect to the product law $\Pi$, and each local sweep (lines L2 and L3) keeps $\Pi$ invariant. So $\Pi$ is a stationary law of the joint chain, and its first coordinate has the law $\pi$ in stationarity.

The swap of levels $k$ and $k+1$ is a Metropolis-Hastings move whose proposal is the map $\tau_k$ that exchanges two coordinates. This map is its own inverse and keeps the reference measure, so the Hastings factor is 1 and the acceptance ratio is $\Pi(\tau_kx)/\Pi(x)$. In this ratio every factor $\pi_j$ with $j \ne k, k+1$ cancels, and so do $Z_k$ and $Z_{k+1}$:

$$\frac{\Pi(\tau_kx)}{\Pi(x)} = \frac{\tilde\pi(x_{k+1})^{\beta_k}\,\tilde\pi(x_k)^{\beta_{k+1}}}{\tilde\pi(x_k)^{\beta_k}\,\tilde\pi(x_{k+1})^{\beta_{k+1}}} = \Big(\frac{\tilde\pi(x_{k+1})}{\tilde\pi(x_k)}\Big)^{\beta_k - \beta_{k+1}},$$

which is line L5. The local sweep changes one coordinate at a time with a kernel that keeps that factor of $\Pi$. The proof file gives the details on a general space and a condition for convergence. The tests check the theorem with exact rational transition matrices: the product law is stationary for both the local sweep and the swap, and the swap is reversible.

Stationarity does not say how fast the chain converges. Woodard, Schmidler and Huber (2009) bound the [spectral gap](/spectral-gap/) of the joint chain from below when the target splits into modes whose shape changes little with the temperature, and the ladder is dense enough. When a narrow mode loses its weight much faster than a wide mode as $\beta$ falls, the hot levels hardly visit it, and tempering can still mix slowly.

## Complexity

One iteration takes $K$ local steps and one swap test, which reuses values that the local steps already computed, so $T$ iterations take $\Theta(TKc)$ time, and the current states take $\Theta(Kd)$ memory. Only the cold level gives samples of $\pi$, so the cost per useful sample is $K$ times that of a single chain. The gain is in the [mixing time](/mixing-time/), which can fall from exponential in the height of the barrier to a small number of iterations, as in the example.

**The number of levels.** Two neighbour levels swap often only when their laws overlap. For a target on $\mathbb{R}^d$ the fluctuations of $\log\pi$ grow like $\sqrt d$, so to keep a fixed swap rate the ratio $\beta_{k+1}/\beta_k$ must approach 1 like $1 - c/\sqrt d$, and the number of levels between fixed end temperatures grows like $\sqrt d$. A geometric ladder is the usual first choice. Kone and Kofke (2005) studied how to space the levels and suggest a swap rate near 20 percent.

## Properties

- **Exact.** For every ladder, the cold chain has stationary law $\pi$. The ladder affects only the speed.
- **No normalizing constants.** The swap test uses only $\tilde\pi$, unlike simulated tempering.
- **Parallel.** The $K$ local steps are independent given the current states and can run at the same time.
- **Modular.** Any local kernel that keeps $\pi^\beta$ invariant can be used at each level.
- **Not a single-chain method.** It needs memory for $K$ states, and all but one level give no direct samples of $\pi$.

## Variants and improvements

- **Simulated tempering** (Marinari and Parisi 1992). One chain on $\mathcal{X} \times \{1, \dots, K\}$ with the level as a random variable. It needs estimates of the $Z_k$ to visit all levels evenly.
- **Deterministic swap schemes.** Instead of a random pair in line L4, try all even pairs and then all odd pairs in turn. The swaps are then not reversible as a whole, and states can travel through the ladder faster.
- **Adaptive ladders.** Tune the $\beta_k$ during a first run so that all neighbour pairs have about the same swap rate.
- **Hamiltonian replica exchange.** The levels differ by another parameter of the energy, not by the temperature. The proof is the same.
- **Combination with [Wang-Landau](/wang-landau/).** Both attack barriers. Wang-Landau flattens the histogram of the energy with one chain, and parallel tempering uses many chains with fixed weights.
- **Cluster moves.** For spin models near a critical point, [Swendsen-Wang](/swendsen-wang/) updates large clusters at once. Tempering helps more where clusters do not, for example in spin glasses with frustration.

## When to use it

Use parallel tempering when the target has several modes separated by regions of low probability, and a local kernel mixes well inside a mode: spin glasses, protein folding, phylogenetic trees and mixture models. It is easy to add to an existing sampler and to run on many cores. When the target has one mode, it only wastes work. When the modes are of very different width, check the result with care, because tempering can still mix slowly.

## Pitfalls

- **Using all levels as samples of $\pi$.** Only level 1 has the law $\pi$. The other levels can give estimates for $\pi$ only through importance weights $\tilde\pi^{1 - \beta_k}$, which are often of high variance.
- **Gaps that are too large.** If neighbour levels do not overlap, swaps are almost never accepted and the levels run as independent chains. Look at the swap rate of every pair.
- **Too many levels.** States move through the ladder like a random walk, so a ladder with many more levels than needed is slow to cross.
- **Following replicas instead of levels.** The chain of level 1 is the one with stationary law $\pi$. The path of one replica as it moves between levels is not a sample of $\pi$.
- **A hot level that is not hot enough.** If $\pi^{\beta_K}$ still has high barriers, the top of the ladder does not mix and nothing passes down.
- **Trusting the diagnostics.** Like all MCMC, parallel tempering can miss a mode that no level found, and no diagnostic can prove that this did not happen.

## Implementations

## History

Swendsen and Wang (1986) introduced replica Monte Carlo for spin glasses, with replicas at several temperatures that exchange clusters of spins. Geyer (1991), in a conference paper on Monte Carlo maximum likelihood, proposed Metropolis-coupled MCMC: several chains on tempered targets that propose to exchange whole states. Marinari and Parisi (1992) introduced simulated tempering, a single chain that moves between temperatures. Hukushima and Nemoto (1996) proposed the exchange Monte Carlo method with swaps of whole states between neighbour temperatures and used it for spin glasses, and from then on the method was in wide use in physics, chemistry and Bayesian statistics.

## References
