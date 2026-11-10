---
tag: 3S0NKB
kind: algorithm
slug: coupling-from-the-past
name: Coupling from the past
aliases:
- Propp-Wilson algorithm
- perfect sampling
area: randomized/markov-chain-monte-carlo
level: advanced
summary: An exact sampler. Compose random update maps from time -T up to time 0, reusing them and doubling T, until all starting states give one state. That state has law exactly π.
solves: [exact-sampling-from-stationary-distribution]
model: word-ram
complexity:
  vars: {T: "the start time at which the copies coalesce, a random number less than twice the coalescence time", c: "the cost of one update"}
  time: {worst: Θ(c·T), average: Θ(c·T), best: Θ(c)}
  space: {extra: Θ(T)}
properties: {in_place: false, online: false, deterministic: false, recursive: false}
history:
  year: 1996
  people: [James Gary Propp, David Bruce Wilson]
  note: Propp and Wilson published coupling from the past, with monotone CFTP and exact samples of the Ising model, in Random Structures and Algorithms in 1996.
prereqs: [coupling-method, stationary-distribution, las-vegas-algorithm]
see_also: [exact-sampling-from-stationary-distribution, sampling-from-stationary-distribution, coupling-method, coupling-inequality, wilson-algorithm, ising-model, hard-core-model, glauber-dynamics]
sources:
  - paper: "James Gary Propp and David Bruce Wilson, Exact sampling with coupled Markov chains and applications to statistical mechanics, Random Structures and Algorithms 9(1-2), 1996, 223-252"
    locator: the algorithm, its correctness, monotone CFTP, and the bound on the coalescence time
  - paper: doi:10.1006/jagm.1997.0917
    title: James Gary Propp and David Bruce Wilson, How to get a perfectly random sample from a generic Markov chain and generate a random spanning tree of a directed graph, Journal of Algorithms 27(2), 1998
    locator: pages 170 to 217
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Chapter 25, Coupling from the Past (Sections 25.1 to 25.4)
  - book: isbn:9780521890014
    title: Olle Häggström, Finite Markov Chains and Algorithmic Applications, Cambridge University Press, 2002
    locator: Chapters 10 and 11 (the Propp-Wilson algorithm and sandwiching)
---

Coupling from the past (CFTP) draws a sample whose law is *exactly* the [stationary distribution](/stationary-distribution/) $\pi$ of an ergodic [Markov chain](/markov-chain/). It fixes random update maps for the steps from time $-1$, $-2$, $-3$, and so on, back into the past, and composes them from a start time $-T$ up to time 0. When every starting state leads to the same state at time 0, that state is the output; otherwise $T$ is doubled and the same maps are reused. Propp and Wilson introduced it in 1996, with a monotone form that tracks only two copies of the chain.

## In plain words

Imagine that the chain has been running since the beginning of time, so that today its state is a perfect random sample. You do not know where it started, so you try every start at once. Fix the random choices for yesterday, the day before, and so on. Starting one day ago from every possible state, apply yesterday's choice and see where each start lands today. If all starts land on the same state, the start did not matter, and that state is today's state. If not, go back two days, then four, always keeping the choices already made for the recent days. Once all starts merge, the answer is final. The trick is to look backward. Running forward from now until copies merge, and taking the meeting point, gives a biased answer.

## The problem

Given an update rule $\phi$ for an irreducible transition matrix $P$ on a finite set $\mathcal X$, so that $\Pr[\phi(x, U) = y] = P(x, y)$ for a random draw $U$, output a state with law exactly $\pi$. This is the problem [exact sampling from a stationary distribution](/exact-sampling-from-stationary-distribution/). The monotone form needs a partial order on $\mathcal X$ with a least element $\hat0$ and a greatest element $\hat1$, such that $x \le y$ implies $\phi(x, u) \le \phi(y, u)$ for every $u$.

## The algorithm

The draw $u_t$ drives the step from time $-t$ to time $-t + 1$. It is drawn once and reused for every later, larger start time.

```pseudo id=main
MONOTONE-CFTP(φ, 0̂, 1̂)                     ▷ returns a state with law π, and the start time used
L1  T ← 1
L2  u ← an empty list                       ▷ u[t] drives the step from time −t to −t + 1
L3  loop
L4      draw u[t] for each t ≤ T that has no value yet   ▷ old values are kept
L5      lo ← 0̂, hi ← 1̂                       ▷ the copies from the bottom and the top, at time −T
L6      for t ← T down to 1 do
L7          lo ← φ(lo, u[t]), hi ← φ(hi, u[t])
L8      if lo = hi then return (lo, T)
L9      T ← 2T
```

For a chain without an order, the general form replaces $lo$ and $hi$ by the set of images of all states, and stops when that set has one element. It costs $|\mathcal X|$ updates per step, so it is for small chains.

## Example

Take the walk on $\{0, 1, 2\}$ driven by $u \in \{0, 1, 2, 3\}$: $u \in \{0, 1\}$ moves down, $u = 3$ moves up, $u = 2$ stays, with moves blocked at the ends. The update is monotone, and $\pi = (4/7, 2/7, 1/7)$ by [detailed balance](/detailed-balance/), since $\pi(x + 1)/\pi(x) = (1/4)/(1/2)$.

Suppose the draws come out as $u_1 = 2$, then $u_2 = 3$, then $u_3 = 0$ and $u_4 = 0$.

| $T$ | draws used, from time $-T$ | $(lo, hi)$ after each step | result |
|---|---|---|---|
| 1 | $u_1 = 2$ | $(0, 2)$ | differ, double |
| 2 | $u_2 = 3$, $u_1 = 2$ | $(1, 2)$, $(1, 2)$ | differ, double |
| 4 | $u_4 = 0$, $u_3 = 0$, $u_2 = 3$, $u_1 = 2$ | $(0, 1)$, $(0, 0)$, $(1, 1)$, $(1, 1)$ | return $(1, 4)$ |

The copies meet at time $-2$, in state 0, but the output is the state at time 0, which is 1. The draws $u_1$ and $u_2$ from the earlier rounds are reused in the last round.

With the start time capped at 8, an exact enumeration of all draws gives output 0, 1 and 2 with probabilities $9105/16384$, $8817/32768$ and $9105/65536$, and no coalescence with probability $2377/65536$. Each of $\pi(0)$, $\pi(1)$ and $\pi(2)$ lies between the probability of that output and that value plus $2377/65536$, as the proof requires.

## Correctness

Let $f_t = \phi(\cdot, u_t)$, let $F_{-t} = f_1 \circ f_2 \circ \cdots \circ f_t$ be the map from time $-t$ to time 0, and let $T_*$ be the least $t$ for which $F_{-t}$ is constant. Three facts give correctness.

1. **Once constant, always the same constant.** For $s \ge t$, $F_{-s} = F_{-t} \circ (f_{t+1} \circ \cdots \circ f_s)$. So if $F_{-t}$ is constant, every $F_{-s}$ with $s \ge t$ is the same constant $Y$. This needs the maps to be reused.
2. **Sandwiching.** By monotonicity and induction over line L7, $lo \le F(x) \le hi$ for every state $x$, where $F$ is the composition run so far. So $lo = hi$ exactly when the composition is constant, and the algorithm returns $Y$ at the first doubled $T \ge T_*$.
3. **The law is $\pi$.** Let $X \sim \pi$ be independent of the draws. Then $F_{-t}(X) \sim \pi P^t = \pi$, and $F_{-t}(X) = Y$ on the event $\{T_* \le t\}$. So $|\Pr[Y = y] - \pi(y)| \le \Pr[T_* > t]$ for every $t$, and this tends to 0 when $T_*$ is finite with probability 1.

For a monotone ergodic chain $T_*$ is finite with probability 1, because $\Pr[T_* > t] \le \ell\,\bar d(t) \to 0$, where $\ell$ is the length of the longest chain in the order. The full proofs, with the termination bound and the reason why forward reading is biased, are below.

## Complexity

The algorithm stops at the first power of two $T \ge T_*$, so $T < 2T_*$. Round $k$ costs $2^k$ steps for each of the two copies, so the total is $1 + 2 + \cdots + T = 2T - 1 < 4T_*$ steps per copy, and the time is $\Theta(c\,T)$ for an update of cost $c$. The expected time is $\Theta(c\,\mathbb E[T])$, and $T$ is random and unbounded. The draws are stored, which costs $\Theta(T)$ space.

The coalescence time is tied to the mixing time. With $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $\bar d(t) = \max_{x, y}\|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$,
$$
d(t) \le \bar d(t) \le \Pr[T_* > t] \le \ell\,\bar d(t).
$$
The left inequality is the [coupling inequality](/coupling-inequality/) applied to the forward composition, which has the same law as $F_{-t}$. So $\Pr[T_* \ge t_{mix}] > 1/4$: CFTP never beats the mixing time by much. For the example chain, $\Pr[T_* > 4] = 69/256$, against $\bar d(4) = 0.160$ and $2\bar d(4) = 0.320$.

## Properties

- **Exact.** The output has law $\pi$ exactly, with no burn-in and no error term.
- **Las Vegas.** The running time is random and unbounded, but finite with probability 1 under the conditions above.
- **Not interruptible.** The output depends on the running time: long runs tend to end in particular states. A user who aborts long runs and restarts biases the output. Fill's algorithm avoids this.
- **Two copies suffice for monotone chains,** however large $\mathcal X$ is.
- **No aperiodicity is assumed for correctness,** only that $T_*$ is finite with probability 1. That condition itself forces $\bar d(t) \to 0$, so a periodic chain never coalesces.

## Variants and improvements

- **General CFTP.** Track the image set of all states. Correct for any grand coupling with $\Pr[T_* < \infty] = 1$, but the cost grows with $|\mathcal X|$.
- **Bounding chains and anti-monotone systems.** Track a set of candidate values per site that is guaranteed to contain all copies, and stop when it is a single configuration.
- **Read-once CFTP (Wilson 2000).** Uses blocks of fixed length, each read once forward, so the draws need not be stored.
- **Dominated CFTP (Kendall).** Extends the idea to infinite spaces with a dominating process.
- **Fill's algorithm (1998).** An interruptible exact sampler for monotone chains, based on the time reversal.
- **Cycle popping.** For a chain given only by a step oracle, Propp and Wilson (1998) sample the root of a random arborescence, which has law $\pi$; see [Wilson's algorithm](/wilson-algorithm/).

## When to use it

Use CFTP when exact samples matter, for example to test approximate samplers or to report results with no burn-in bias, and when the chain has a monotone grand coupling or another way to detect coalescence. Classic cases are the ferromagnetic [Ising model](/ising-model/) with heat bath updates, the [hard-core model](/hard-core-model/) on bipartite graphs, and random tilings. For chains with no such structure on a large space, coalescence cannot be detected, and an approximate sampler such as [Glauber dynamics](/glauber-dynamics/) is the practical choice.

## Pitfalls

- **Fresh draws for each $T$.** Drawing new values $u_t$ in each round makes the output depend on the round at which coalescence happens, and the law is no longer $\pi$. The draws for recent times must be reused.
- **Reading forward.** Running copies forward from now until they meet, and returning the meeting state, is biased. In the example the copies from 0 and 2 can meet only at 0 or 2, so that method never returns 1, although $\pi(1) = 2/7$.
- **The wrong order of composition.** The newest step must be applied last: $u_1$ drives the step into time 0. Applying the draws in the other order gives a forward run.
- **A rule that is not monotone.** If $\phi(\cdot, u)$ does not preserve the order, the copies from $\hat0$ and $\hat1$ can meet while other copies have not, and the output is wrong.
- **Aborting long runs.** CFTP is not interruptible. A time limit that discards slow runs biases the output.
- **A grand coupling that never coalesces.** For example, if each $\phi(\cdot, u)$ is a bijection, the image set never shrinks. The chain can still be ergodic.

## Implementations

## History

Propp and Wilson introduced coupling from the past in 1996, together with the monotone form, and used it to draw exact samples of the Ising model at the critical temperature on large grids. The idea that compositions of random maps taken backward in time settle down, while forward compositions do not, appeared earlier in work on iterated random functions. In 1998 Propp and Wilson extended exact sampling to chains known only through a step oracle by cycle popping, and Fill gave an interruptible algorithm.

## References
