---
tag: NTG1F6
kind: technique
slug: coupling-method
name: Coupling method
aliases:
- coupling argument
area: randomized/markov-chain-monte-carlo
level: advanced
summary: Bound the mixing time by running two copies of a chain with shared randomness so that they meet fast. By the coupling inequality, d(t) is at most the chance that they have not met.
prereqs: [coupling-inequality, mixing-time, total-variation-distance]
see_also: [coupling-inequality, path-coupling, coupling-from-the-past, mixing-time, rapid-mixing, glauber-dynamics, strong-uniform-time, canonical-paths]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Chapter 5, Coupling (Theorem 5.4, Corollary 5.5, Section 5.3.1 with (5.6), Section 5.3.2, Section 5.4 with Theorems 5.8 and 5.9)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 12, Coupling of Markov Chains
  - paper: doi:10.1002/rsa.3240070205
    title: Mark Jerrum, A very simple algorithm for estimating the number of k-colorings of a low-degree graph, Random Structures and Algorithms 7(2), 1995
    locator: pages 157 to 165 (the coupling for colorings with more than 2Δ colors)
---

The coupling method bounds the [mixing time](/mixing-time/) of a [Markov chain](/markov-chain/) from above. One runs two copies of the chain from different starting states on a common probability space, so that each copy on its own is a faithful run of the chain, but their random choices are shared to pull them together. By the [coupling inequality](/coupling-inequality/), the distance from stationarity at time $t$ is at most the probability that the copies have not met by time $t$. The art lies in the choice of the joint moves.

## In plain words

Two people start walking through a city from different places, each following the same rules for choosing turns. If they flip separate coins, they may wander for a long time without meeting. If they instead agree to use the same coin whenever they can, while each still follows the rules exactly, they can be made to meet quickly. After they meet they walk together, and from then on nothing reveals where each one started. So the time until they meet is a time after which the starting point has been forgotten. Proving that the meeting happens soon, whatever the two starting places, proves that the chain settles fast. Most clever couplings come from finding which shared choices make the two walkers agree on one more part of their state at each step.

## When it applies

- There is a natural way to drive the chain with random choices that can be shared, for example "pick a site, then pick a value" for a spin system or "pick a card" for a shuffle.
- Under the shared choices, some measure of disagreement between the copies goes down, either surely, in expectation, or like a random walk that must hit zero.
- The bound is wanted for all starting states. For one fixed start one can couple with a stationary copy instead.

The method needs no reversibility, and it gives upper bounds only. For lower bounds use [conductance](/conductance/), a spectral bound, or a statistic that separates $P^t(x, \cdot)$ from $\pi$.

## The template

The notation is $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$.

1. **Write the chain as a random map.** Find a function $f$ and a random variable $U$ with $\Pr[f(x, U) = y] = P(x, y)$.
2. **Define the joint move.** For a pair $(x, y)$ choose a joint law of $(X_1, Y_1)$ with the right marginals. The simplest choice is $X_1 = f(x, U)$, $Y_1 = f(y, U)$ with the same $U$, but often $U$ for one copy is a bijective relabeling of $U$ for the other.
3. **Make the copies stick.** Once $X_s = Y_s$, use identical moves.
4. **Bound the meeting time.** Show that $\max_{x, y}\Pr_{x, y}[\tau_{couple} > t]$ is small, often through one of the two lemmas below.
5. **Conclude.** By LPW Corollary 5.5, $d(t) \le \max_{x, y}\Pr_{x, y}[\tau_{couple} > t]$, and $t_{mix} \le 4\max_{x, y}\mathbb E_{x, y}[\tau_{couple}]$.

**Lemma A (contraction).** Let $\rho$ be a metric on $\mathcal X$ with integer values, so that $\rho(x, y) \ge 1$ when $x \ne y$, and let $D = \max_{x, y}\rho(x, y)$. If for every pair $\mathbb E_{x, y}[\rho(X_1, Y_1)] \le (1 - \alpha)\rho(x, y)$ with $0 < \alpha \le 1$, then $d(t) \le D(1 - \alpha)^t \le De^{-\alpha t}$, and so $t_{mix}(\varepsilon) \le \lceil\alpha^{-1}\log(D/\varepsilon)\rceil$.

*Proof.* By the Markov property and the hypothesis, $\mathbb E[\rho(X_{t+1}, Y_{t+1}) \mid X_t, Y_t] \le (1 - \alpha)\rho(X_t, Y_t)$, so by induction $\mathbb E_{x, y}[\rho(X_t, Y_t)] \le (1 - \alpha)^tD$. Since $\rho \ge \mathbf 1\{X_t \ne Y_t\}$, Markov's inequality gives $\Pr_{x, y}[X_t \ne Y_t] \le \mathbb E_{x, y}[\rho(X_t, Y_t)]$. Apply the [coupling inequality](/coupling-inequality/) and $d(t) \le \bar d(t)$. $\square$

[Path coupling](/path-coupling/) shows that it is enough to check the hypothesis of Lemma A for neighboring pairs.

**Lemma B (a random walk distance).** If the distance $D_t$ between the copies moves like a simple random walk on $\{0, 1, \ldots, n\}$, absorbed at the ends, then $\mathbb E[\tau] = k(n - k) \le n^2/4$ from $D_0 = k$, and $t_{mix} \le n^2$. This is the gambler's ruin identity (LPW Proposition 2.1) followed by step 5.

## Classic examples

### The lazy hypercube

The lazy walk on $\{0, 1\}^n$ picks a coordinate and refreshes it with a fair bit. Couple two copies by picking the same coordinate and the same bit. A coordinate agrees forever once it is picked, so the copies have met when every coordinate has been picked: $\tau_{couple}$ is at most a coupon collector time, and $d(n\log n + cn) \le e^{-c}$, so $t_{mix}(\varepsilon) \le n\log n + n\log(1/\varepsilon)$ up to rounding (LPW (5.6)). For $n = 3$ the exact tail of this coupling time, $3(2/3)^t - 3(1/3)^t$ for opposite corners, gives $t_{mix} \le 7$, while the exact value is 3. The true leading term is $\tfrac12n\log n$, so this coupling loses a factor 2.

### The lazy cycle

On the cycle $\mathbb Z_n$, toss a fair coin to decide which copy moves, and move it one step clockwise or counterclockwise. Each copy on its own is lazy. The two copies never jump over each other, and their clockwise distance is a simple random walk absorbed at 0 and $n$. Lemma B gives $t_{mix} \le n^2$ (LPW Section 5.3.2). The order $n^2$ is correct: a walk needs about $n^2$ steps to travel distance $n$. For $n = 8$ the exact $t_{mix}$ is 6, against the bound 64.

### Grand couplings for colorings and the hard-core model

A *grand coupling* runs copies from every state at once with the same randomness. For the Metropolis chain on proper $q$-colorings of a graph with maximum degree $\Delta$, each step draws a vertex $v$ and a color $k$, and recolors $v$ with $k$ if this keeps the coloring proper. With the Hamming distance $\rho$ and the same $(v, k)$ in both copies, LPW Theorem 5.8 shows contraction when $q > 3\Delta$, with $t_{mix}(\varepsilon) \le \lceil(1 - 3\Delta/q)^{-1}n(\log n + \log(1/\varepsilon))\rceil$. For Glauber dynamics of the [hard-core model](/hard-core-model/) with fugacity $\lambda < 1/(\Delta - 1)$, the same approach gives $t_{mix}(\varepsilon) \le \frac{n}{c_H(\lambda)}(\log n + \log(1/\varepsilon))$ with $c_H(\lambda) = (1 + \lambda(1 - \Delta))/(1 + \lambda)$ (LPW Theorem 5.9).

### Jerrum's coloring coupling

For [Glauber dynamics](/glauber-dynamics/) on proper $q$-colorings, Jerrum (1995) built a coupling in which, when the copies differ at a neighbor of the chosen vertex, the color choices are matched by a bijection that swaps the two colors in conflict. This gives mixing in $O(n\log n)$ steps for $q > 2\Delta$, and with [self-reducibility](/self-reducibility/) an FPRAS for [counting graph colorings](/counting-graph-colorings/). [Path coupling](/path-coupling/) later gave a much shorter proof of the same bound.

## Variations

- **Coupling with a stationary copy.** Start $Y_0 \sim \pi$. Then $Y_t \sim \pi$ for all $t$, and $\|P^t(x, \cdot) - \pi\|_{TV} \le \Pr[\tau_{couple} > t]$ directly, without the factor in $d \le \bar d$.
- **Monotone couplings.** If the state space has a partial order with a top and a bottom and the update preserves it, then copies from all states are squeezed between the copies from the top and the bottom. Only those two need to meet. This is the basis of monotone [coupling from the past](/coupling-from-the-past/).
- **Path coupling.** Define the coupling only for neighboring states and extend it along shortest paths; see [path coupling](/path-coupling/).
- **Non-Markovian couplings.** The joint move may look ahead in time. Such couplings can be stronger, and a maximal coupling of chains always exists (Griffeath 1974/75), but they are harder to analyze.
- **Strong stationary times.** A different probabilistic bound uses one copy and a random time at which it is exactly stationary; see [strong uniform time](/strong-uniform-time/).

## Pitfalls

- **Wrong marginals.** Each copy alone must move exactly according to $P$. A coupling that forces the copies toward each other in a way that changes the law of one copy proves nothing. Check $\Pr[X_1 = x' \mid X_0 = x, Y_0 = y] = P(x, x')$ for every $y$.
- **Forgetting to stick.** If the copies may separate after they meet, $\Pr[X_t \ne Y_t]$ is still a valid bound, but the first meeting time is not.
- **Periodic chains.** Copies started in different classes of a periodic chain can never meet. Make the chain lazy first.
- **Contraction on average only.** Lemma A needs $\mathbb E\rho(X_1, Y_1) \le (1 - \alpha)\rho(x, y)$ for every pair. A bound that holds only for typical pairs does not give a bound on $d(t)$.
- **Loose constants.** The coupling time can exceed the mixing time by a constant factor, as on the hypercube, or by much more. Markovian couplings can be far from optimal.
- **Reading the meeting state.** The state where two forward copies first meet is not distributed according to $\pi$. For an exact sample, couple from the past.

## Exercises

1. For the chain on $n$ states with $P(x, y) = 1/n$ for all $x, y$, couple two copies by moving both to the same uniform state. Show that $\tau_{couple} = 1$ and that $d(1) = 0$.
2. For the random-to-top shuffle, which moves a uniform random card to the top, couple two decks by moving the card with the same label in both. Show that the decks agree once every card has been chosen, and deduce $t_{mix}(\varepsilon) \le \lceil n\log n + n\log(1/\varepsilon)\rceil$.
3. Show that for a chain with period 2 and two states $x, y$ in different classes, every coupling has $X_t \ne Y_t$ for all $t$.
4. Generalize Lemma A to a metric with $\rho(x, y) \ge \rho_{min} > 0$ for $x \ne y$: show $d(t) \le (1 - \alpha)^tD/\rho_{min}$.
5. For the lazy hypercube with $n = 3$, prove $\Pr[\tau_{couple} > t] = 3(2/3)^t - 3(1/3)^t$ for opposite corners by inclusion and exclusion, and find the smallest $t$ with value at most $1/4$.

## References
