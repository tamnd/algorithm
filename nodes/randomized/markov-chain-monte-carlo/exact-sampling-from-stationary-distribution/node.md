---
tag: BG6NJ4
kind: problem
slug: exact-sampling-from-stationary-distribution
name: Exact sampling from a stationary distribution
aliases:
- perfect sampling problem
area: randomized/markov-chain-monte-carlo
level: advanced
summary: Given a way to simulate an ergodic Markov chain, output a state whose law is exactly its stationary distribution π, in a random but finite time. Solved by CFTP, Fill's algorithm and cycle popping.
prereqs: [sampling-from-stationary-distribution, coupling-method, las-vegas-algorithm]
see_also: [coupling-from-the-past, sampling-from-stationary-distribution, wilson-algorithm, uniform-spanning-tree-sampling, matrix-tree-theorem, rejection-sampling, las-vegas-algorithm, ising-model]
sources:
  - paper: "James Gary Propp and David Bruce Wilson, Exact sampling with coupled Markov chains and applications to statistical mechanics, Random Structures and Algorithms 9(1-2), 1996, 223-252"
    locator: coupling from the past, the monotone case, and the bound on the coalescence time by the length of the longest chain
  - paper: doi:10.1006/jagm.1997.0917
    title: James Gary Propp and David Bruce Wilson, How to get a perfectly random sample from a generic Markov chain and generate a random spanning tree of a directed graph, Journal of Algorithms 27(2), 1998
    locator: pages 170 to 217 (cycle popping and sampling the root of a random arborescence)
  - paper: doi:10.1145/237814.237880
    title: David Bruce Wilson, Generating random spanning trees more quickly than the cover time, Proceedings of the 28th ACM Symposium on Theory of Computing (STOC), 1996
    locator: pages 296 to 303
  - paper: doi:10.1214/aoap/1027961037
    title: James Allen Fill, An interruptible algorithm for perfect sampling via Markov chains, Annals of Applied Probability 8(1), 1998
    locator: pages 131 to 162
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Chapter 25, Coupling from the Past (Section 25.2, Monotone CFTP; Section 25.3; Section 25.5, Random State of an Unknown Markov Chain); Section 4.4 (Lemma 4.10)
  - book: isbn:9780521890014
    title: Olle Häggström, Finite Markov Chains and Algorithmic Applications, Cambridge University Press, 2002
    locator: Chapters 10 to 12 (the Propp-Wilson algorithm, its sandwiching form, and Fill's algorithm)
---

Exact sampling from a stationary distribution asks for a random state whose law is *exactly* the [stationary distribution](/stationary-distribution/) $\pi$ of a given ergodic [Markov chain](/markov-chain/), not just close to it. The algorithm may only simulate steps of the chain, and its running time must be finite with probability 1 but may be random, so the solutions are [Las Vegas algorithms](/las-vegas-algorithm/). The three classic solutions are [coupling from the past](/coupling-from-the-past/) (Propp and Wilson 1996), Fill's interruptible algorithm (1998), and cycle popping (Propp and Wilson 1998). The approximate version, with an error $\varepsilon$ in total variation, is [sampling from a stationary distribution](/sampling-from-stationary-distribution/).

## In plain words

An ordinary Markov chain sampler stops after a fixed number of steps and hopes that the chain has forgotten its start. Its answer is always a little biased, and nobody can tell how much from the output alone. An exact sampler removes all of that bias. It also uses the chain, but it decides for itself when to stop, by checking a condition under which the answer cannot depend on the start at all. A typical condition is that copies of the chain from every possible start, all driven by the same random choices, have merged into one. When that happens, the common state is a perfect sample. The price is that the running time is random, and the check must be done the right way: the obvious way of running forward and stopping at the first merge gives a biased answer.

## Definition

**Input.** A finite set $\mathcal X$ and access to an irreducible transition matrix $P$ with stationary distribution $\pi$, given as one of:

- an *update function* $\phi : \mathcal X \times [0, 1) \to \mathcal X$ with $\Pr[\phi(x, U) = y] = P(x, y)$ for $U$ uniform, which allows a grand coupling of copies from all states; or
- a *step oracle* that, given $x$, returns a sample from $P(x, \cdot)$.

**Output.** A random state $X$ with $\Pr[X = x] = \pi(x)$ for every $x$, produced after a number of steps that is finite with probability 1.

A solution is *interruptible* if its output is independent of its running time. Then a user who stops long runs and restarts does not bias the output.

The mixing notation is $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$, $t_{mix} = t_{mix}(1/4)$ and $\bar d(t) = \max_{x, y}\|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV}$.

## Variants

- **Monotone chains.** $\mathcal X$ has a partial order with a least element $\hat0$ and a greatest element $\hat1$, and $\phi(\cdot, u)$ preserves the order for each $u$. Then only the copies from $\hat0$ and $\hat1$ need to be run. The ferromagnetic [Ising model](/ising-model/) with heat bath updates and the [hard-core model](/hard-core-model/) on a bipartite graph, with the order reversed on one side, are monotone.
- **Anti-monotone and bounding chains.** When monotonicity fails, one can track a set of possible states that is guaranteed to contain all copies. Coalescence is detected when the set has one element.
- **Infinite or continuous spaces.** Dominated coupling from the past (Kendall) uses a dominating process in place of a top state, for example for spatial point processes.
- **Unknown chain.** Only the step oracle is available, and nothing is known about $P$. Cycle popping still works.
- **Read-once randomness.** Wilson (2000) gave a version that reads each random number only once, so that the past need not be stored.

## Examples

**A birth and death chain.** On $\{0, 1, 2\}$ let $u \in \{0, 1, 2, 3\}$ be uniform; $u \in \{0, 1\}$ moves down, $u = 3$ moves up, $u = 2$ stays, with moves blocked at the ends. Detailed balance gives $\pi = (4/7, 2/7, 1/7)$. The update is monotone, so monotone CFTP from the states 0 and 2 applies. The table gives, from exact fractions, $d(t)$, $\bar d(t)$ and the probability that the copies from 0 and 2 have not coalesced after $t$ steps, which is the probability that CFTP needs a start time before $-t$.

| $t$ | $d(t)$ | $\bar d(t)$ | $\Pr[T_* > t]$ | $2\bar d(t)$ |
|---|---|---|---|---|
| 2 | 0.321 | 0.438 | 0.688 | 0.875 |
| 4 | 0.118 | 0.160 | 0.270 | 0.320 |
| 6 | 0.043 | 0.058 | 0.099 | 0.117 |
| 8 | 0.016 | 0.021 | 0.036 | 0.043 |

Both bounds $\bar d(t) \le \Pr[T_* > t] \le 2\bar d(t)$ of the Bounds section hold, with the longest chain $0 < 1 < 2$ of length $\ell = 2$.

**Forward coupling is biased.** Run the copies from 0 and 2 *forward* with the same $u$ and output the state at the first time they meet. They can meet only at 0 or 2: a meeting at 1 would need one copy to move up and the other down in the same step. So this output is never 1, while $\pi(1) = 2/7$. With at most 8 steps, the forward output is 0 with probability $3011/4096$ and 2 with probability $14983/65536$.

**Uniform spanning trees.** For the simple random walk on a connected graph, [Wilson's algorithm](/wilson-algorithm/) by cycle popping returns a [spanning tree](/spanning-tree/) with exactly the uniform distribution; see [uniform spanning tree sampling](/uniform-spanning-tree-sampling/).

## Known algorithms

| algorithm | access | interruptible | idea |
|---|---|---|---|
| [coupling from the past](/coupling-from-the-past/) | update function | no | compose random maps from time $-T$ to 0, double $T$ until the composition is constant |
| monotone CFTP | monotone update function | no | the same, run from $\hat0$ and $\hat1$ only |
| Fill's algorithm (1998) | monotone chain and its time reversal | yes | run the reversal from $\hat1$, then accept with a test that uses a conditioned forward coupling |
| cycle popping (Propp and Wilson 1998) | step oracle | no | sample a random arborescence with weight $\prod_xP(x, \mathrm{next}(x))$; its root has law $\pi$ |
| read-once CFTP (Wilson 2000) | update function | no | blocks of fixed length read forward, each used once |
| [rejection sampling](/rejection-sampling/) | weights $w$ and a bound $M$ | yes | needs $\pi$ up to a constant and a dominating law, not a chain |

## Bounds

- **A fixed number of steps cannot work in general.** If $P^t(x, \cdot) \ne \pi$ for every $t$, as for the example above, any method that runs the chain a fixed number of steps from a fixed start has a biased output. So the running time must be random.
- **Coalescence takes at least the mixing time.** For CFTP with a grand coupling, let $T_*$ be the smallest $t$ for which the composed map over $t$ steps is constant. The forward composition over $t$ steps has the same law as the backward one, and if it is constant then copies from $x$ and $y$ agree at time $t$. By the [coupling inequality](/coupling-inequality/), $\bar d(t) \le \Pr[T_* > t]$, and so $\Pr[T_* \ge t_{mix}] > 1/4$.
- **For monotone chains it takes not much more.** Let $\ell$ be the length of the longest chain in the order and $h(x)$ the length of the longest chain below $x$. If the copies from $\hat0$ and $\hat1$ differ at time $t$, then $h$ of the upper copy exceeds $h$ of the lower one by at least 1. So
$$
\Pr[T_* > t] \le \mathbb E\big[h(X_t^{\hat1}) - h(X_t^{\hat0})\big] \le \ell\,\|P^t(\hat1, \cdot) - P^t(\hat0, \cdot)\|_{TV} \le \ell\,\bar d(t).
$$
This is the argument of Propp and Wilson (1996). With doubling, the total work is at most about 4 times $T_*$ steps for each of the two copies.
- **Cycle popping** runs in expected time of the order of a mean hitting time of the chain, which can be much smaller than the cover time (Wilson 1996).

## Reductions

- **To approximate sampling.** An exact sampler solves the approximate problem for every $\varepsilon$; the converse fails.
- **From random arborescences.** By the Markov chain tree theorem, a form of the [matrix-tree theorem](/matrix-tree-theorem/), the root of a random arborescence with weight $\prod_xP(x, \mathrm{next}(x))$ has law $\pi$. So exact sampling of such arborescences, which cycle popping does, gives exact samples from $\pi$.
- **To counting.** Exact samplers feed the same reductions from sampling to [approximate counting](/approximate-counting/) as approximate ones, with no error term from the sampler.

## Applications

- Exact samples of the Ising and Potts models and of the random cluster model, including at the critical temperature on large grids (Propp and Wilson 1996).
- Random tilings, such as domino and lozenge tilings, through monotone CFTP on height functions.
- Uniform and weighted spanning trees and arborescences.
- Spatial point processes in statistics, by dominated CFTP.
- Testing approximate samplers: an exact sampler gives a reference distribution.

## References
