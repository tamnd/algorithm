---
tag: JJZHX2
kind: definition
slug: stationary-distribution
name: Stationary distribution
aliases:
- equilibrium distribution
- invariant distribution
area: randomized/markov-chain-monte-carlo
level: intro
summary: A distribution π with πP = π, so a chain started from π keeps the law π. Each finite chain has one, and an irreducible chain has exactly one, with π(x) = 1 / E_x(return time to x).
prereqs: [markov-chain, transition-matrix, probability-distribution]
see_also: [irreducibility, ergodicity, ergodic-theorem, detailed-balance, mixing-time, sampling-from-stationary-distribution, power-iteration, matrix-tree-theorem]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 1.5, Stationary Distributions (Lemma 1.13, Proposition 1.14, Lemma 1.16, Corollary 1.17, Proposition 1.19 (Kac))
  - book: isbn:9780521633963
    title: J. R. Norris, Markov Chains, Cambridge University Press, 1997
    locator: Section 1.7, Invariant distributions
  - book: isbn:9780821807491
    title: Charles M. Grinstead and J. Laurie Snell, Introduction to Probability, second revised edition, American Mathematical Society, 1997
    locator: Section 11.3, Ergodic Markov Chains (the fixed row vector)
---

A stationary distribution of a [Markov chain](/markov-chain/) with [transition matrix](/transition-matrix/) $P$ is a probability distribution $\pi$ on the states with $\pi P = \pi$. If the chain starts with law $\pi$, it has law $\pi$ at every later step. Each chain on a finite state space has at least one stationary distribution. An [irreducible](/irreducibility/) chain has exactly one, it gives positive mass to each state, and $\pi(x)$ is the inverse of the mean return time to $x$.

## Definition

Let $P$ be a transition matrix on a finite set $\mathcal X$. A row vector $\pi$ is a *stationary distribution* of $P$ if
$$
\pi(y) \ge 0, \qquad \sum_{y} \pi(y) = 1, \qquad \sum_{x} \pi(x)P(x, y) = \pi(y) \quad \text{for all } y.
$$
The last condition is $\pi P = \pi$: $\pi$ is a left [eigenvector](/eigenvector/) of $P$ for the [eigenvalue](/eigenvalue/) 1, scaled to be a probability vector. By induction $\pi P^t = \pi$ for all $t$, so $X_0 \sim \pi$ gives $X_t \sim \pi$ for all $t$. The chain is then a stationary process: the law of $(X_s, \ldots, X_{s+k})$ does not depend on $s$, by formula (1) of [Markov chain](/markov-chain/).

Stationary does not mean "the limit of the chain". A periodic chain has a stationary distribution, but its law need not converge to it; see [aperiodicity](/aperiodicity/). The limit statement needs [ergodicity](/ergodicity/).

### Existence, positivity, uniqueness

Write $\tau_y^+ = \min\{t \ge 1 : X_t = y\}$ for the first time after time 0 at which the chain is at $y$. LPW Lemma 1.13, proved on the page [irreducibility](/irreducibility/), says that $\mathbb E_x \tau_y^+ < \infty$ for all $x, y$ when $P$ is irreducible.

**Theorem.** Let $P$ be a transition matrix on a finite set.

1. $P$ has a stationary distribution.
2. If $P$ is irreducible, then each stationary distribution has $\pi(y) > 0$ for all $y$.
3. If $P$ is irreducible, then the stationary distribution is unique.
4. (Kac) If $P$ is irreducible, then $\pi(z) = 1/\mathbb E_z \tau_z^+$ for each $z$.

*Proof of 1 (Cesàro averages).* Fix a distribution $\mu$ and let $\nu_T = \frac1T \sum_{t=0}^{T-1} \mu P^t$. Each $\nu_T$ is a distribution, and
$$
\nu_T P - \nu_T = \tfrac1T(\mu P^T - \mu),
$$
whose entries have absolute values that sum to at most $2/T$. The set of distributions on $\mathcal X$ is closed and bounded in $\mathbb R^{\mathcal X}$, so a subsequence $\nu_{T_k}$ converges to a distribution $\nu$. The map $\nu \mapsto \nu P - \nu$ is continuous, so $\nu P - \nu = \lim_k (\nu_{T_k}P - \nu_{T_k}) = 0$. $\square$

*Proof of 2.* Some state $x$ has $\pi(x) > 0$. For each $y$, irreducibility gives $t$ with $P^t(x, y) > 0$. Then $\pi(y) = (\pi P^t)(y) \ge \pi(x)P^t(x, y) > 0$. $\square$

*Proof of 3 (maximum principle).* Call $h : \mathcal X \to \mathbb R$ *harmonic* if $Ph = h$. Let $h$ be harmonic and let $x$ be a state where $h$ is largest, with value $M$. Then $M = h(x) = \sum_y P(x, y)h(y)$ is an average of values at most $M$, so $h(y) = M$ for each $y$ with $P(x, y) > 0$. Repeat this from these states. By irreducibility, each state is reached, so $h \equiv M$. The kernel of $P - I$ is therefore the line spanned by $\mathbf 1$, and $P - I$ has rank $|\mathcal X| - 1$. The left kernel $\{\mu : \mu(P - I) = 0\}$ then has dimension 1 too. Two stationary distributions lie on this line and both sum to 1, so they are equal. $\square$

*Proof of 4.* Fix $z$ and define, for each $y$, the expected number of visits to $y$ in one excursion from $z$:
$$
\tilde\pi(y) = \mathbb E_z\Bigl[\sum_{t=0}^{\tau_z^+ - 1} \mathbf 1\{X_t = y\}\Bigr] = \sum_{t \ge 0} \Pr_z[X_t = y,\ \tau_z^+ > t].
$$
Then $\tilde\pi(z) = 1$ and $\sum_y \tilde\pi(y) = \mathbb E_z \tau_z^+ < \infty$. The event $\{\tau_z^+ > t\} = \{\tau_z^+ \ge t + 1\}$ depends only on $X_0, \ldots, X_t$, so by the Markov property
$$
\sum_x \tilde\pi(x)P(x, y) = \sum_{t \ge 0} \Pr_z[X_{t+1} = y,\ \tau_z^+ \ge t + 1] = \sum_{s \ge 1} \Pr_z[X_s = y,\ \tau_z^+ \ge s].
$$
Subtract $\tilde\pi(y) = \sum_{s \ge 0}\Pr_z[X_s = y, \tau_z^+ > s]$. The terms with $\tau_z^+ > s$ cancel for $s \ge 1$, and what is left is $\sum_{s \ge 1}\Pr_z[X_s = y, \tau_z^+ = s] - \Pr_z[X_0 = y] = \Pr_z[X_{\tau_z^+} = y] - \mathbf 1\{y = z\} = 0$, because $X_{\tau_z^+} = z$ and $\tau_z^+ < \infty$ with probability 1. So $\tilde\pi P = \tilde\pi$, and $\tilde\pi / \mathbb E_z\tau_z^+$ is a stationary distribution. By part 3 it is $\pi$, and at $z$ it is $1/\mathbb E_z \tau_z^+$. $\square$

Without irreducibility, uniqueness fails (see below), but part 1 still holds. The [Perron-Frobenius theorem](/perron-frobenius-theorem/) gives parts 2 and 3 by linear algebra.

### Computing $\pi$

- **Linear system.** Solve $\pi(P - I) = 0$ with $\sum_y \pi(y) = 1$, for example by [Gaussian elimination](/gaussian-elimination/). For an irreducible $P$, drop one of the equations of $\pi(P - I) = 0$ and add the normalization; the system then has a unique solution. With rational entries, exact arithmetic gives $\pi$ exactly in $O(n^3)$ arithmetic operations for $n$ states.
- **Power iteration.** For an irreducible and [aperiodic](/aperiodicity/) chain, $\mu P^t \to \pi$ for each start $\mu$ ([ergodicity](/ergodicity/)). This is [power iteration](/power-iteration/) on $P^\top$, and it is how [PageRank](/pagerank/) is computed.
- **Detailed balance.** If $\pi(x)P(x, y) = \pi(y)P(y, x)$ for all pairs, then $\pi$ is stationary; see [detailed balance](/detailed-balance/). This often gives $\pi$ by a product formula.
- **Spanning trees.** For an irreducible chain, $\pi(x)$ is proportional to the sum, over the spanning trees directed toward $x$, of the products of the transition probabilities on their edges (the Markov chain tree theorem, a form of the [matrix-tree theorem](/matrix-tree-theorem/)).

When the state space is too large to list, as for the colorings of a graph, nobody computes $\pi$. One designs a chain whose $\pi$ is the target and runs it; see [sampling from the stationary distribution](/sampling-from-stationary-distribution/).

## Examples and non-examples

**The Land of Oz.** For $P$ on the page [Markov chain](/markov-chain/), $\pi = (2/5, 1/5, 2/5)$ on (rain, nice, snow). Check the column of N: $\tfrac25 \cdot \tfrac14 + \tfrac15 \cdot 0 + \tfrac25 \cdot \tfrac14 = \tfrac15$. Kac's formula says that the mean time between two nice days is $1/\pi(N) = 5$. Directly: from N the next day is R or S, and from R or S the mean time $h$ to the next nice day solves $h = 1 + \tfrac34 h$, so $h = 4$ and the mean return time is $1 + 4 = 5$.

**Two states.** For $P = \begin{pmatrix} 1 - a & a \\ b & 1 - b \end{pmatrix}$ with $a + b > 0$, $\pi = \bigl(b/(a + b),\ a/(a + b)\bigr)$.

**Random walk on a graph.** On a connected graph with $m$ edges, $\pi(x) = \deg(x)/(2m)$: then $\pi(x)P(x, y) = 1/(2m)$ for each edge, which is [detailed balance](/detailed-balance/). On a regular graph, $\pi$ is uniform.

**Doubly stochastic matrices.** If each column of $P$ sums to 1, the uniform distribution is stationary. So a random [card shuffling](/card-shuffling/) step keeps a uniform deck uniform.

**Two closed classes (non-uniqueness).** On $\{1, 2, 3\}$, let state 1 and state 3 be absorbing, and let state 2 move to 1 or 3 with probability $1/2$ each. Then $(1, 0, 0)$, $(0, 0, 1)$ and each mixture $(p, 0, 1 - p)$ are stationary. The chain is not irreducible, and state 2 gets mass 0.

**A periodic chain.** The walk $0 \to 1 \to 0$ with $P = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ has the unique stationary distribution $(1/2, 1/2)$, but from state 0 the law of $X_t$ alternates between $(1, 0)$ and $(0, 1)$. The time averages still converge to $(1/2, 1/2)$; see [ergodic theorem](/ergodic-theorem/).

**Infinite state spaces (non-example).** The simple random walk on the integers has no stationary distribution. A stationary $\pi$ would satisfy $\pi(x) = \tfrac12\pi(x - 1) + \tfrac12\pi(x + 1)$, so $\pi$ would be a linear function of $x$; a bounded linear function is constant, and a constant that sums to 1 over the integers does not exist. Existence on infinite spaces needs positive recurrence (Norris, Section 1.7).

## Related definitions

- [Irreducibility](/irreducibility/): the condition for uniqueness and positivity.
- [Aperiodicity](/aperiodicity/) and [ergodicity](/ergodicity/): the conditions for $P^t(x, \cdot) \to \pi$.
- [Ergodic theorem](/ergodic-theorem/): for an irreducible chain, the fraction of time spent in $y$ tends to $\pi(y)$ with probability 1, also for periodic chains.
- [Detailed balance](/detailed-balance/): a stronger, local condition that implies stationarity.
- [Total variation distance](/total-variation-distance/) and [mixing time](/mixing-time/): how far the law of $X_t$ is from $\pi$, and how fast it gets close.
- [Metropolis-Hastings](/metropolis-hastings/) and [Gibbs sampling](/gibbs-sampling/): ways to build a chain with a given $\pi$.

## References
