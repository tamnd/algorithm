---
tag: KEX3DH
kind: definition
slug: ergodicity
name: Ergodicity
aliases:
- ergodic Markov chain
area: randomized/markov-chain-monte-carlo
level: core
summary: Here a finite Markov chain is ergodic if it is irreducible and aperiodic. Then P^t(x, ·) tends to the unique π from each start at a geometric rate. Other books use the word in other senses.
prereqs: [irreducibility, aperiodicity, stationary-distribution]
see_also: [ergodic-theorem, mixing-time, coupling-method, coupling-inequality, total-variation-distance, spectral-gap, perron-frobenius-theorem, power-iteration]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 4.3, The Convergence Theorem (Theorem 4.9); Section 1.3, Proposition 1.7; Section 5.2, Theorem 5.4
  - book: isbn:9780521633963
    title: J. R. Norris, Markov Chains, Cambridge University Press, 1997
    locator: Section 1.8, Convergence to equilibrium (proved by coupling)
  - book: isbn:9780821807491
    title: Charles M. Grinstead and J. Laurie Snell, Introduction to Probability, second revised edition, American Mathematical Society, 1997
    locator: Section 11.3, Ergodic Markov Chains (ergodic and regular chains)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 7, Markov Chains and Random Walks (ergodic states and chains)
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 6, Markov Chains (ergodicity, geometric and uniform ergodicity)
---

On these pages, a [Markov chain](/markov-chain/) on a finite state space is *ergodic* when it is [irreducible](/irreducibility/) and [aperiodic](/aperiodicity/). For such a chain the law of $X_t$ converges to the unique [stationary distribution](/stationary-distribution/) $\pi$ from each starting state, and the distance falls at a geometric rate (the convergence theorem, proved below by coupling). The word "ergodic" has other meanings in other books, and the table at the end of the definition lists them. The [ergodic theorem](/ergodic-theorem/) is a different statement: it is about time averages along one path, and it needs only irreducibility.

## Definition

Let $P$ be a transition matrix on a finite set $\mathcal X$. The chain is **ergodic** if it is irreducible and aperiodic. For finite chains the following are equivalent.

1. $P$ is irreducible and aperiodic.
2. $P$ is *primitive*: there is an $r$ with $P^r(x, y) > 0$ for all $x, y$.
3. There is a distribution $\pi$ with $\pi(y) > 0$ for all $y$ and $\lim_{t \to \infty} P^t(x, y) = \pi(y)$ for all $x, y$.

*Proof.* 1 and 2 are equivalent by Proposition 3 on the page [aperiodicity](/aperiodicity/). The convergence theorem below proves that 1 implies 3. If 3 holds, then each $P^t(x, y)$ is close to $\pi(y) > 0$ for large $t$, so there is an $r$ with all entries of $P^r$ positive, which is 2. $\square$

The notation is that of the group: $\|\cdot\|_{TV}$ is the [total variation distance](/total-variation-distance/), $d(t) = \max_x \|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$.

### The convergence theorem

**Theorem (LPW Theorem 4.9).** Let $P$ be irreducible and aperiodic on a finite set, with stationary distribution $\pi$. Let $r$ be such that $P^r$ has all entries positive, and $\delta = \min_{x, y} P^r(x, y) > 0$. Then for all $t \ge 0$,
$$
d(t) \le (1 - \delta)^{\lfloor t/r \rfloor}.
$$
In particular $d(t) \le C\alpha^t$ with $\alpha = (1 - \delta)^{1/r} < 1$ and $C = (1 - \delta)^{-1}$.

*Proof (Doeblin's coupling).* Fix $x$. Run two chains together. $X$ starts at $x$, and $Y$ starts from $\pi$. While $X_t \ne Y_t$, each makes a step of $P$, independently of the other. From the first time they are equal, they make the same steps. Each of $X$ and $Y$ alone is a Markov chain with matrix $P$, so $X_t \sim P^t(x, \cdot)$ and $Y_t \sim \pi P^t = \pi$. By the [coupling inequality](/coupling-inequality/),
$$
\|P^t(x, \cdot) - \pi\|_{TV} \le \Pr[X_t \ne Y_t].
$$
Let $E_k$ be the event that the chains have not met by time $kr$. Up to their meeting time, the pair moves like two independent chains. Given $E_k$ and $(X_{kr}, Y_{kr}) = (a, b)$, the chains fail to meet by time $(k+1)r$ only if two independent chains from $a$ and $b$ are at different states at time $r$. That has probability
$$
1 - \sum_z P^r(a, z)P^r(b, z) \le 1 - \delta\sum_z P^r(b, z) = 1 - \delta.
$$
So $\Pr[E_{k+1}] \le (1 - \delta)\Pr[E_k]$, and $\Pr[E_k] \le (1 - \delta)^k$. Once the chains meet they stay together, so $\Pr[X_t \ne Y_t] \le \Pr[E_{\lfloor t/r \rfloor}] \le (1 - \delta)^{\lfloor t/r \rfloor}$. Take the maximum over $x$. $\square$

The bound is usually weak: $\delta$ can be tiny. Sharper bounds on the rate come from the [spectral gap](/spectral-gap/), from better couplings ([coupling method](/coupling-method/), [path coupling](/path-coupling/)), and from [conductance](/conductance/). The page [mixing time](/mixing-time/) collects them.

### What "ergodic" means in other places

| Where | "Ergodic" means | Relation to these pages |
|---|---|---|
| These pages (finite chains) | irreducible and aperiodic | the definition above |
| Grinstead and Snell, Section 11.3 | irreducible ("possible to go from every state to every state"); an irreducible chain with a positive power is called *regular* | their "regular" is our "ergodic" |
| Mitzenmacher and Upfal, Chapter 7 | a state is ergodic if it is aperiodic and positive recurrent; a chain is ergodic if all its states are | the same as ours for finite irreducible chains, where each state is positive recurrent |
| General state space MCMC (for example Robert and Casella, Chapter 6) | $\|P^t(x, \cdot) - \pi\|_{TV} \to 0$ for (almost) each start, under Harris recurrence and aperiodicity | the analogue of item 3 above |
| Ergodic theory | a stationary process is ergodic if each shift-invariant event has probability 0 or 1 | the stationary chain $X_0 \sim \pi$ with $\pi > 0$ is ergodic in this sense exactly when $P$ is irreducible; aperiodicity is not needed |

Two stronger notions come from general state spaces. A chain is *uniformly ergodic* if $d(t) \le C\alpha^t$ with $\alpha < 1$, uniformly in the start, and *geometrically ergodic* if $\|P^t(x, \cdot) - \pi\|_{TV} \le C(x)\alpha^t$. The theorem above says that each finite ergodic chain is uniformly ergodic.

## Examples and non-examples

**The Land of Oz.** The chain is irreducible, and $P(R, R) > 0$, so it is ergodic. Its square $P^2$ has all entries positive, with smallest entry $\delta = 3/16$ (see [transition matrix](/transition-matrix/)), so the theorem gives $d(t) \le (13/16)^{\lfloor t/2 \rfloor}$. The true distance is much smaller: $d(t) = \tfrac45 \cdot 4^{-t}$, because the other eigenvalues of $P$ are $\pm 1/4$.

**Lazy random walks.** The lazy walk on a connected graph, and the lazy walk on the hypercube, are ergodic. Laziness makes them aperiodic.

**A periodic chain (non-example).** The walk on the cycle with 4 vertices is irreducible, with period 2. From vertex 0 the chain is at an even vertex at each even time, so $\|P^t(0, \cdot) - \pi\|_{TV} = 1/2$ for all $t \ge 1$. The law does not converge, and $t_{mix}(\varepsilon)$ is infinite for $\varepsilon < 1/2$. The time averages still converge to $\pi$; see [ergodic theorem](/ergodic-theorem/).

**A reducible chain (non-example).** With two absorbing states, the chain converges, but its limit depends on the start. Condition 3 fails because no single $\pi$ is the limit from each start.

**Frozen colorings (non-example).** The [Glauber dynamics](/glauber-dynamics/) for proper 3-colorings of a triangle has $P = I$. It is aperiodic but not irreducible.

## Related definitions

- [Irreducibility](/irreducibility/) and [aperiodicity](/aperiodicity/): the two parts of the definition.
- [Ergodic theorem](/ergodic-theorem/): for an irreducible chain, the time average of $f(X_s)$ tends to $\mathbb E_\pi f$ with probability 1. It is about one path, not about the law of $X_t$, and it holds for periodic chains too.
- [Mixing time](/mixing-time/): the quantitative form of the convergence theorem.
- [Coupling inequality](/coupling-inequality/) and [coupling method](/coupling-method/): the tools of the proof above.
- [Perron-Frobenius theorem](/perron-frobenius-theorem/): for a primitive matrix, the eigenvalue 1 is simple and each other eigenvalue has modulus less than 1. This gives the convergence theorem by linear algebra.
- [Power iteration](/power-iteration/): computes $\pi$ as the limit of $\mu P^t$, which is correct exactly because of the convergence theorem.

## References
