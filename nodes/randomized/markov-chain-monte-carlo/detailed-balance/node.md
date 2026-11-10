---
tag: 1BQA62
kind: definition
slug: detailed-balance
name: Detailed balance
aliases:
- reversibility condition
area: randomized/markov-chain-monte-carlo
level: core
summary: A chain satisfies detailed balance for π when π(x)P(x, y) = π(y)P(y, x) for all pairs. Then π is stationary and the stationary chain looks the same run forward or backward.
prereqs: [markov-chain, stationary-distribution, transition-matrix]
see_also: [metropolis-hastings, gibbs-sampling, glauber-dynamics, spectral-gap, conductance, top-to-random-shuffle, irreducibility, spectral-theorem]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 1.6, Reversibility and Time Reversals (equations (1.29) to (1.31), Proposition 1.20, Example 1.22 (the biased walk on a cycle), the time reversal (1.32) and Proposition 1.23); Section 2.5, Birth-and-Death Chains; Section 3.3, Glauber Dynamics
  - book: isbn:9780521633963
    title: J. R. Norris, Markov Chains, Cambridge University Press, 1997
    locator: Section 1.9, Time reversal (detailed balance and reversibility)
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 6, Markov Chains (the detailed balance condition); Chapter 7, The Metropolis-Hastings Algorithm
---

A [Markov chain](/markov-chain/) with [transition matrix](/transition-matrix/) $P$ satisfies *detailed balance* for a distribution $\pi$ when $\pi(x)P(x, y) = \pi(y)P(y, x)$ for each pair of states. In words, at equilibrium the flow of probability from $x$ to $y$ equals the flow from $y$ to $x$, for each pair separately. Detailed balance implies that $\pi$ is a [stationary distribution](/stationary-distribution/), and it is much easier to check than $\pi P = \pi$ because it is local. A chain with this property is called *reversible*: started from $\pi$, its path has the same law forward and backward. Most Markov chain Monte Carlo methods, such as [Metropolis-Hastings](/metropolis-hastings/) and [Gibbs sampling](/gibbs-sampling/), are built to satisfy it.

## Definition

Let $P$ be a transition matrix on a finite set $\mathcal X$, and $\pi$ a probability distribution on $\mathcal X$. The pair $(P, \pi)$ satisfies **detailed balance** if
$$
\pi(x)P(x, y) = \pi(y)P(y, x) \qquad \text{for all } x, y \in \mathcal X. \qquad (1)
$$
Then $P$ is called *reversible with respect to* $\pi$. Write $Q(x, y) = \pi(x)P(x, y)$, the probability that the stationary chain makes the step from $x$ to $y$; condition (1) says that $Q$ is a symmetric matrix. The [conductance](/conductance/) and the [spectral gap](/spectral-gap/) of a reversible chain are defined through $Q$.

The weaker condition $\pi P = \pi$ is sometimes called *global balance*: for each $x$, the total flow out of $x$ equals the total flow into $x$, $\sum_y Q(x, y) = \sum_y Q(y, x)$.

### Facts and proofs

**Proposition 1 (detailed balance implies stationarity; LPW Proposition 1.20).** If (1) holds, then $\pi P = \pi$.

*Proof.* Sum (1) over $x$: $\sum_x \pi(x)P(x, y) = \pi(y)\sum_x P(y, x) = \pi(y)$. $\square$

**Proposition 2 (reversibility).** Let $X_0 \sim \pi$. Then (1) holds if and only if, for each $t$, the reversed path $(X_t, X_{t-1}, \ldots, X_0)$ has the same law as $(X_0, X_1, \ldots, X_t)$.

*Proof.* If (1) holds, use it once for each factor of the path formula of [Markov chain](/markov-chain/):
$$
\pi(x_0)P(x_0, x_1)\cdots P(x_{t-1}, x_t) = P(x_1, x_0)\pi(x_1)P(x_1, x_2)\cdots P(x_{t-1}, x_t) = \cdots = \pi(x_t)P(x_t, x_{t-1})\cdots P(x_1, x_0).
$$
The left side is $\Pr_\pi[X_0 = x_0, \ldots, X_t = x_t]$ and the right side is $\Pr_\pi[X_0 = x_t, \ldots, X_t = x_0]$. Conversely, for $t = 1$ the equality of the two laws is $\Pr_\pi[X_0 = x, X_1 = y] = \Pr_\pi[X_0 = y, X_1 = x]$, which is (1). $\square$

**The time reversal.** Let $P$ be irreducible with stationary $\pi$, and define
$$
\hat P(x, y) = \frac{\pi(y)P(y, x)}{\pi(x)}.
$$
Then $\hat P$ is a transition matrix (its rows sum to 1 because $\pi P = \pi$), $\pi$ is stationary for $\hat P$, and the stationary chain of $\hat P$ is the stationary chain of $P$ read backward (LPW Section 1.6). $P$ is reversible exactly when $\hat P = P$. By induction on $t$, $\pi(x)P^t(x, y) = \pi(y)\hat P^t(y, x)$ for all $t$.

**Kolmogorov's criterion.** Let $P$ be irreducible. Then $P$ is reversible with respect to some distribution if and only if, for each cycle of states $x_0, x_1, \ldots, x_k = x_0$,
$$
P(x_0, x_1)P(x_1, x_2)\cdots P(x_{k-1}, x_0) = P(x_0, x_{k-1})\cdots P(x_2, x_1)P(x_1, x_0). \qquad (2)
$$
*Proof.* If (1) holds, multiply (1) over the steps of the cycle; the factors $\pi(x_i) > 0$ appear on both sides and cancel. Conversely, assume (2). First, $P(x, y) > 0$ implies $P(y, x) > 0$: by irreducibility there is a positive path from $y$ back to $x$, and (2) for the cycle $x \to y \to \cdots \to x$ makes the reversed product positive, and that product contains $P(y, x)$. Now fix $z$. For each $x$ choose a path $z = x_0, \ldots, x_k = x$ with positive steps and let $w(x) = \prod_i P(x_i, x_{i+1})/P(x_{i+1}, x_i)$. Two paths from $z$ to $x$ give the same value, because one path followed by the reverse of the other is a cycle and (2) holds for it. If $P(x, y) > 0$, a path to $x$ followed by the step to $y$ is a path to $y$, so $w(y) = w(x)P(x, y)/P(y, x)$, which is (1) for $w$. If $P(x, y) = 0$ then $P(y, x) = 0$ and (1) holds trivially. Normalize $w$ to get $\pi$. $\square$

**The spectrum is real.** With the inner product $\langle f, g\rangle_\pi = \sum_x \pi(x)f(x)g(x)$, condition (1) gives $\langle Pf, g\rangle_\pi = \sum_{x, y}Q(x, y)f(y)g(x) = \langle f, Pg\rangle_\pi$. So $P$ is self-adjoint, and by the [spectral theorem](/spectral-theorem/) it has real eigenvalues and an orthonormal basis of eigenfunctions. The pages [spectral gap](/spectral-gap/), [conductance](/conductance/) and [Cheeger inequality](/cheeger-inequality/) use this.

## Examples and non-examples

**The Land of Oz.** With $\pi = (2/5, 1/5, 2/5)$ on (rain, nice, snow), each pair has the same flow both ways: $\pi(R)P(R, N) = \tfrac25\cdot\tfrac14 = \tfrac1{10} = \tfrac15\cdot\tfrac12 = \pi(N)P(N, R)$, and in the same way $Q(R, S) = Q(S, R) = 1/10$ and $Q(N, S) = Q(S, N) = 1/10$. The chain is reversible.

**Random walks on graphs.** On a connected graph with $m$ edges, $\pi(x) = \deg(x)/(2m)$ gives $\pi(x)P(x, y) = 1/(2m) = \pi(y)P(y, x)$ for each edge. With edge weights $c(x, y) = c(y, x)$ and $P(x, y) = c(x, y)/c(x)$, where $c(x) = \sum_y c(x, y)$, the same computation gives $\pi(x) = c(x)/\sum_y c(y)$. Each reversible chain is a weighted walk of this kind, with $c = Q$.

**Birth-and-death chains.** On $\{0, \ldots, n\}$ let $P(k, k+1) = p_k$, $P(k, k-1) = q_k$ and $P(k, k) = 1 - p_k - q_k$, with $p_k, q_{k+1} > 0$. Condition (1) is needed only for neighbors, and it gives
$$
\pi(k) \propto \prod_{i=0}^{k-1}\frac{p_i}{q_{i+1}}.
$$
So each such chain is reversible. For example, with $p_k = 1/4$ and $q_k = 1/2$ on $\{0, 1, 2\}$, $\pi = (4/7, 2/7, 1/7)$. This chain is the example of [coupling from the past](/coupling-from-the-past/).

**Metropolis-Hastings.** The acceptance rule of [Metropolis-Hastings](/metropolis-hastings/) is chosen so that (1) holds for the target $\pi$, whatever the proposal. This is why the method only needs $\pi$ up to a constant factor: (1) involves only the ratios $\pi(y)/\pi(x)$.

**Heat-bath dynamics.** In [Glauber dynamics](/glauber-dynamics/) and [Gibbs sampling](/gibbs-sampling/), a step picks a site $v$ and redraws its value from $\pi$ conditioned on the other sites. If $x$ and $y$ differ only at $v$, and $S$ is the set of configurations that agree with $x$ off $v$ (the same set for $y$), then $P(x, y) = \frac1n\cdot\frac{\pi(y)}{\pi(S)}$, so $\pi(x)P(x, y) = \frac{\pi(x)\pi(y)}{n\,\pi(S)}$ is symmetric in $x$ and $y$.

**A biased 3-cycle (non-example).** On $\{0, 1, 2\}$ let $P(i, i+1) = 2/3$ and $P(i, i-1) = 1/3$, mod 3. The matrix is doubly stochastic, so $\pi$ is uniform. But $\pi(0)P(0, 1) = 2/9$ and $\pi(1)P(1, 0) = 1/9$: detailed balance fails, although $\pi$ is stationary. Kolmogorov's criterion shows it at once: the cycle $0 \to 1 \to 2 \to 0$ has probability $8/27$, and its reverse has probability $1/27$.

**Top-to-random (non-example).** The [top-to-random shuffle](/top-to-random-shuffle/) moves the top card to a uniform position. The uniform distribution is stationary, but the move from a deck to the deck with its third card on top has probability 0, while the reverse move has positive probability. So the chain is not reversible.

**Non-reversible samplers.** Some samplers keep $\pi$ stationary by global balance only, for example a systematic sweep of the sites in a fixed order in Gibbs sampling. The composition of reversible steps need not be reversible. Such chains are still valid for $\pi$, but the spectral tools of reversible chains do not apply to them directly.

## Related definitions

- [Stationary distribution](/stationary-distribution/): $\pi P = \pi$. Detailed balance is a sufficient, local condition for it, not a necessary one.
- [Spectral gap](/spectral-gap/): defined through the real eigenvalues of a reversible $P$.
- [Conductance](/conductance/) and [Cheeger inequality](/cheeger-inequality/): use the symmetric edge measure $Q$.
- [Metropolis-Hastings](/metropolis-hastings/), [Gibbs sampling](/gibbs-sampling/) and [Glauber dynamics](/glauber-dynamics/): chains designed through detailed balance.
- [Irreducibility](/irreducibility/): needed in Kolmogorov's criterion and for $\pi$ to be unique.

## References
