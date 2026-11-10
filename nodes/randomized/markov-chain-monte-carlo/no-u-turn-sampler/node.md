---
tag: 1360ZZ
kind: algorithm
slug: no-u-turn-sampler
name: No-U-Turn sampler
aliases:
- NUTS
area: randomized/markov-chain-monte-carlo
level: advanced
summary: HMC that grows the leapfrog path forward and backward in time, doubling it, until the two ends start to come back toward each other. It then picks the next state from the path, so L need not be set.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {T: the number of iterations, D: the largest tree depth allowed, d: the dimension, c: the cost of one gradient of the log target}
  time: {worst: Θ(T 2^D (d + c))}
  space: {extra: Θ(D d)}
properties: {in_place: true, online: true, deterministic: false, recursive: true}
history:
  year: 2014
  people: [Matthew D. Hoffman, Andrew Gelman]
  note: Hoffman and Gelman published the No-U-Turn sampler, with dual averaging for the step size, in the Journal of Machine Learning Research in 2014. It became the default sampler of Stan.
prereqs: [hamiltonian-monte-carlo]
see_also: [hamiltonian-dynamics, slice-sampling, metropolis-adjusted-langevin-algorithm, effective-sample-size, gelman-rubin-diagnostic, burn-in]
sources:
  - url: https://jmlr.org/papers/v15/hoffman14a.html
    title: Matthew D. Hoffman and Andrew Gelman, The No-U-Turn sampler, adaptively setting path lengths in Hamiltonian Monte Carlo, Journal of Machine Learning Research 15, 2014
    locator: pages 1593 to 1623 (the doubling procedure, the conditions C.1 to C.4, the efficient Algorithm 3, and dual averaging)
  - book: isbn:9781420079418
    title: Steve Brooks, Andrew Gelman, Galin L. Jones and Xiao-Li Meng (editors), Handbook of Markov Chain Monte Carlo, Chapman and Hall/CRC, 2011
    locator: Chapter 5, Radford M. Neal, MCMC using Hamiltonian dynamics, pages 113 to 162 (HMC and the leapfrog method that NUTS builds on)
  - paper: doi:10.18637/jss.v076.i01
    title: Bob Carpenter, Andrew Gelman, Matthew D. Hoffman and others, Stan, a probabilistic programming language, Journal of Statistical Software 76(1), 2017
    locator: the description of the sampler (NUTS with adaptation of the step size and the mass matrix during warm-up)
  - paper: doi:10.1111/1467-9868.00198
    title: Gareth O. Roberts and Jeffrey S. Rosenthal, Convergence of slice sampler Markov chains, Journal of the Royal Statistical Society Series B 61(3), 1999
    locator: pages 643 to 660 (the slice variable that NUTS uses, as an auxiliary variable)
---

The No-U-Turn sampler (NUTS) is a form of [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) that chooses the length of each trajectory by itself. HMC needs a number of leapfrog steps $L$: too few and it moves like a random walk, too many and the trajectory comes back to where it started, which wastes work. NUTS draws a momentum and builds a trajectory by repeated doubling. At each doubling it picks forward or backward in time at random and adds as many leapfrog steps as the trajectory already has. It stops when the two ends of the trajectory start to move toward each other (a "U-turn"), or when the energy error becomes huge. It then picks the next state from the states of the trajectory that are in a slice $\{e^{-H} \ge u\}$. The doubling, the random directions and the choice rule make the chain exactly $\pi$-invariant, with no Metropolis test of the end point. Hoffman and Gelman (2014) introduced it, together with dual averaging to set the step size $\varepsilon$, and it is the default sampler in Stan and PyMC.

## In plain words

HMC rolls a ball across the landscape of the target for a fixed number of small steps. The right number depends on the shape of the landscape, and a bad choice wastes work or makes the ball go back where it came from.

NUTS lets the ball roll both forward and backward in time and keeps doubling the length of the path. It stops as soon as the path starts to bend back on itself, like a U-turn. Then it picks one of the points along the path as the next sample. The doubling and the random choice of direction are arranged so that the rule for picking is fair, and the sampler stays exact.

## The problem

The input is a function $\log\tilde\pi$ with $\tilde\pi = Z\pi$ positive and differentiable on $\mathbb{R}^d$, its gradient, a start $q_0$, a step size $\varepsilon > 0$, a largest tree depth $D \ge 1$ and a number of iterations $T$. The output is a Markov chain $X_1, \ldots, X_T$ with $\pi$ as a stationary distribution, as in [sampling from a stationary distribution](/sampling-from-stationary-distribution/). Write $H(q, p) = -\log\tilde\pi(q) + |p|^2/2$ and $\Delta_{\max} = 1000$. The bracket $[A]$ is 1 if $A$ is true and 0 otherwise. The model of randomness is $d$ standard normal reals, one uniform real for the slice, and at most $2D$ further uniform draws per iteration.

## The algorithm

This is the efficient version (Algorithm 3 of Hoffman and Gelman) with a fixed step size. The dot is the inner product, and LEAPFROG is one leapfrog step from the [Hamiltonian dynamics](/hamiltonian-dynamics/) page.

```pseudo id=main
NUTS(log π̃, ∇log π̃, q0, ε, D, T)
L1  q ← q0
L2  for t ← 1 to T do
L3      draw p ~ N(0, I_d); draw u uniformly from (0, exp(−H(q, p))]   ▷ slice variable
L4      (q⁻, p⁻, q⁺, p⁺) ← (q, p, q, p); n ← 1; s ← 1; j ← 0; q_new ← q
L5      while s = 1 and j < D do
L6          draw v uniformly from {−1, +1}
L7          if v = −1 then (q⁻, p⁻, ·, ·, q', n', s') ← BUILD-TREE(q⁻, p⁻, u, v, j)
L8          else (·, ·, q⁺, p⁺, q', n', s') ← BUILD-TREE(q⁺, p⁺, u, v, j)
L9          if s' = 1 then with probability min(1, n'/n) set q_new ← q'
L10         n ← n + n'
L11         s ← s' · [(q⁺ − q⁻)·p⁻ ≥ 0] · [(q⁺ − q⁻)·p⁺ ≥ 0]
L12         j ← j + 1
L13     q ← q_new; X_t ← q
L14 return X_1, …, X_T

BUILD-TREE(q, p, u, v, j)                ▷ 2^j leapfrog steps in time direction v
L15 if j = 0 then
L16     (q', p') ← LEAPFROG(q, p, v ε)
L17     n' ← [u ≤ exp(−H(q', p'))]; s' ← [u < exp(Δmax − H(q', p'))]
L18     return (q', p', q', p', q', n', s')
L19 (q⁻, p⁻, q⁺, p⁺, q', n', s') ← BUILD-TREE(q, p, u, v, j − 1)
L20 if s' = 1 then
L21     if v = −1 then (q⁻, p⁻, ·, ·, q'', n'', s'') ← BUILD-TREE(q⁻, p⁻, u, v, j − 1)
L22     else (·, ·, q⁺, p⁺, q'', n'', s'') ← BUILD-TREE(q⁺, p⁺, u, v, j − 1)
L23     with probability n''/(n' + n'') set q' ← q''          ▷ skip if n' + n'' = 0
L24     s' ← s'' · [(q⁺ − q⁻)·p⁻ ≥ 0] · [(q⁺ − q⁻)·p⁺ ≥ 0]
L25     n' ← n' + n''
L26 return (q⁻, p⁻, q⁺, p⁺, q', n', s')
```

Here $n'$ counts the states of a subtree that lie in the slice $\{e^{-H} \ge u\}$, and $q'$ is one of them, chosen uniformly by the rule of line L23. The flag $s'$ is 0 when some balanced subtree inside makes a U-turn, or when some state has an energy error above $\Delta_{\max}$ (a divergence). A subtree with $s' = 0$ is not used as a candidate (line L9), and the run stops. In code, the slice is kept as $\log u$.

## Example

Take $\pi = \mathcal{N}(0, 1)$, $\varepsilon = 1/2$, the start $q = 0$ with drawn momentum $p = 1$, so $H = 0.5$, and $u = 0.5e^{-0.5}$, so the slice is $\{H \le 0.5 + \log 2 = 1.19\}$. Number the states by their time index, so the start is state 0. The directions drawn are $-1, +1, +1$.

| state | $-1$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|---|
| $q$ | $-0.5$ | 0 | 0.5 | 0.875 | 1.031 | 0.930 | 0.596 | 0.113 |
| $p$ | 0.875 | 1 | 0.875 | 0.531 | 0.055 | $-0.436$ | $-0.817$ | $-0.994$ |
| $H$ | 0.508 | 0.5 | 0.508 | 0.524 | 0.533 | 0.527 | 0.511 | 0.500 |

- **Depth 0 to 1.** Direction $-1$ adds state $-1$. The ends are states $-1$ and 0, with $q^+ - q^- = 0.5$ and both momenta positive, so there is no U-turn.
- **Depth 1 to 2.** Direction $+1$ adds states 1 and 2. The new subtree and the whole path $[-1, 2]$ pass the test.
- **Depth 2 to 3.** Direction $+1$ adds states 3 to 6. Inside this subtree, the pair $\{3, 4\}$ makes a U-turn: $(q_4 - q_3)p_3 = (-0.102)(0.055) < 0$. So $s' = 0$, the new states are not candidates, and the run stops.

All states are in the slice, so the candidate set is $C = \{-1, 0, 1, 2\}$. The naive rule picks uniformly from $C$. The efficient rule of line L9 does better: at depth 1 it switches to state $-1$ with probability $\min(1, 1/1) = 1$, and at depth 2 it switches to a uniform state of $\{1, 2\}$ with probability $\min(1, 2/2) = 1$. So the next state is $q = 0.5$ or $q = 0.875$, each with probability $1/2$. Both rules keep $\pi$ invariant. The efficient rule favours the newer and farther states, and here its mean squared jump is 0.51 against 0.32 for the naive rule. The trajectory stopped after about a quarter of the period $2\pi$ of the exact dynamics, when the particle reached the turning point at $q \approx 1$.

## Correctness

**Theorem.** For every $\varepsilon > 0$ and $D \ge 1$, each iteration of NUTS leaves the joint law $\bar\pi(q, p) \propto \tilde\pi(q)e^{-|p|^2/2}$ invariant, so $\pi$ is a stationary distribution of $(X_t)$.

The proof is in the proof file. Its structure follows Hoffman and Gelman:

1. The pair $(z, u)$ with $z = (q, p) \sim \bar\pi$ and $u$ uniform on $(0, e^{-H(z)}]$ is uniform on the region under the graph of $e^{-H}$, as in [slice sampling](/slice-sampling/).
2. All states of the path are $\Psi^i(z)$ for integers $i$, where $\Psi$ is one leapfrog step, which is a volume-preserving bijection.
3. Because the path grows by doubling, after $k$ doublings it is always the aligned block of $2^k$ time indices that contains the start. So from every candidate state $z' \in C$, exactly one sequence of directions builds the same path and the same set $C$, with the same number of doublings and the same probability. This is condition C.4 of Hoffman and Gelman.
4. Given the slice and the path, the start is therefore uniform on $C$, and the rule of lines L9 and L23 maps the uniform law on $C$ to itself.

Together these give invariance of $(z, u)$, so of $\bar\pi$. The test file checks step 3 exactly, in rational arithmetic, from every candidate of several paths, and checks step 4 exactly on random candidate sets. As with all MCMC, invariance does not give convergence.

## Complexity

One iteration builds a path of at most $2^D$ leapfrog steps, each with one new gradient, so it costs $O(2^D(d + c))$, and $T$ iterations cost $\Theta(T 2^D(d + c))$ in the worst case. The actual cost adapts to the target: on a Gaussian with standard deviations from $\sigma_{\min}$ to $\sigma_{\max}$, the path stops after a time of order $\sigma_{\max}$, so it uses about $\sigma_{\max}/\varepsilon$ steps, with $\varepsilon$ of order $\sigma_{\min}$. The recursion of BUILD-TREE has depth at most $D$, and each level keeps a constant number of vectors, so the memory is $\Theta(Dd)$. The naive version that stores all of $C$ needs $\Theta(2^Dd)$.

## Properties

- **No path length to tune.** Only $\varepsilon$ remains, and dual averaging sets it during warm-up to reach a target mean acceptance statistic, usually 0.8.
- **Exact.** Invariance holds for every $\varepsilon$, without a Metropolis test of the end point.
- **Recursive.** BUILD-TREE calls itself twice on half-size subtrees.
- **Wasted work bounded by a constant factor.** The last doubling may be thrown away, so at most about half of the leapfrog steps are not used as candidates.
- **Needs gradients**, like HMC.

## Variants and improvements

- **Dual averaging for $\varepsilon$** (Hoffman and Gelman, Algorithm 6). During warm-up, adapt $\log\varepsilon$ so that the average acceptance statistic of the path is near a target value. Then freeze $\varepsilon$.
- **Multinomial NUTS.** Stan replaced the slice variable by sampling states with weights $e^{-H}$, which uses more information about the path, and uses a generalized U-turn test with the sum of the momenta (Betancourt 2017).
- **Mass matrix adaptation.** Estimate the covariance of $\pi$ during warm-up, as for [HMC](/hamiltonian-monte-carlo/).
- **Naive NUTS** (Hoffman and Gelman, Algorithm 2). Keep the whole candidate set and pick uniformly from it. It is simpler to prove and uses more memory.

## When to use it

NUTS is the default choice for smooth targets with continuous parameters, from a few to many thousands of dimensions, especially when you do not want to tune HMC by hand. It needs gradients, so it does not handle discrete parameters directly. Like HMC, it has trouble with strongly varying curvature and with separated modes.

## Pitfalls

- **Divergences.** A path that hits a state with energy error above $\Delta_{\max}$ stops early. Many divergences show a region of high curvature that the sampler does not explore, and the estimates can be biased in practice even though the chain is exact in theory. Reparametrize the model, or lower $\varepsilon$.
- **Hitting the largest depth.** If many iterations reach depth $D$, the paths are cut before the U-turn, and the chain moves less than it could. This often means $\varepsilon$ is very small compared to the largest scale of the target.
- **Adapting forever.** Changing $\varepsilon$ after warm-up, based on the chain's history, can break invariance. Freeze it.
- **The U-turn test uses Euclidean geometry.** With a non-identity mass matrix the test must use $M^{-1}p$ instead of $p$; mixing the two gives paths that stop too early or too late.

## Implementations

## History

Hoffman and Gelman (2014) introduced NUTS, with the conditions C.1 to C.4 for its validity, the memory-efficient Algorithm 3, and dual averaging for the step size. The idea of building a path by doubling in random time directions, and of choosing a state from it in a way that keeps the uniform law, made HMC usable without tuning the path length. Stan (Carpenter et al. 2017) made NUTS its default sampler, later with multinomial sampling of states.

## References
