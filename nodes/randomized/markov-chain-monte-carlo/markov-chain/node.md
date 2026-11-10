---
tag: TW6RYZ
kind: definition
slug: markov-chain
name: Markov chain
aliases:
- Markov process
- discrete-time Markov chain
area: randomized/markov-chain-monte-carlo
level: intro
summary: A sequence of random states in which the next state depends only on the current state, through fixed transition probabilities.
prereqs: [random-variable, conditional-probability, probability-distribution]
see_also: [transition-matrix, stationary-distribution, irreducibility, ergodicity, detailed-balance, mixing-time, markov-property, hidden-markov-model]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 1.1, Markov Chains (definition (1.1)); Section 1.2, Random Mapping Representation (Proposition 1.5); Section 1.4, Random Walks on Graphs
  - book: isbn:9780521633963
    title: J. R. Norris, Markov Chains, Cambridge University Press, 1997
    locator: Section 1.1, Definition and basic properties (Theorem 1.1.1, the law of the path)
  - book: isbn:9780821807491
    title: Charles M. Grinstead and J. Laurie Snell, Introduction to Probability, second revised edition, American Mathematical Society, 1997
    locator: Chapter 11, Markov Chains (Example 11.1, the Land of Oz)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 7, Markov Chains and Random Walks
---

A Markov chain is a sequence of random states $X_0, X_1, X_2, \ldots$ in which the law of the next state depends only on the current state, and not on the earlier ones. On a finite state space, one number $P(x, y)$ for each pair of states gives the probability to go from $x$ to $y$ in one step, and the same numbers are used at each step. This page is about the random process and the law of its paths. The table of numbers itself, and the algebra of its powers, are on the page [transition matrix](/transition-matrix/).

## Definition

Let $\mathcal X$ be a finite set, the *state space*. Let $P$ be a $\mathcal X \times \mathcal X$ matrix with $P(x, y) \ge 0$ and $\sum_{y} P(x, y) = 1$ for each $x$. A sequence of [random variables](/random-variable/) $X_0, X_1, \ldots$ with values in $\mathcal X$ is a *Markov chain with transition matrix* $P$ if, for each $t \ge 0$, all states $x_0, \ldots, x_{t-1}, x, y$, and each history with positive probability,
$$
\Pr[X_{t+1} = y \mid X_0 = x_0, \ldots, X_{t-1} = x_{t-1}, X_t = x] = P(x, y).
$$
Two parts of this definition are separate conditions.

- **Markov property.** The conditional law of $X_{t+1}$ given the whole past depends only on $X_t$. The general form of this condition is on the page [Markov property](/markov-property/).
- **Time homogeneity.** The same matrix $P$ is used at each time $t$. Some books allow a matrix $P_t$ that changes with $t$; this encyclopedia calls that a *time-inhomogeneous* chain and says so when it uses one.

The law $\mu$ of $X_0$ is the *initial distribution*. We write $\Pr_\mu$ and $\mathbb E_\mu$ for the chain with $X_0 \sim \mu$, and $\Pr_x$ and $\mathbb E_x$ when $X_0 = x$.

**The law of a path.** For each $t$ and all states,
$$
\Pr_\mu[X_0 = x_0, X_1 = x_1, \ldots, X_t = x_t] = \mu(x_0)\, P(x_0, x_1)\, P(x_1, x_2) \cdots P(x_{t-1}, x_t). \qquad (1)
$$
*Proof.* Use induction on $t$. For $t = 0$ the claim is the definition of $\mu$. For the step, write the probability of the path up to $t+1$ as the probability of the path up to $t$ times the conditional probability of $X_{t+1} = x_{t+1}$ given that path. If the path up to $t$ has probability 0, both sides are 0. If not, the definition gives the factor $P(x_t, x_{t+1})$. $\square$

Formula (1) shows that $\mu$ and $P$ fix the law of the whole sequence. Summing (1) over $x_0, \ldots, x_{t-1}$ gives $\Pr_\mu[X_t = y] = (\mu P^t)(y)$, where $\mu$ is a row vector. The [transition matrix](/transition-matrix/) page proves the rules for $P^t$.

**Random mapping representation.** Let $U_1, U_2, \ldots$ be independent random values with the same law, independent of $X_0$, and let $f$ be a function with $\Pr[f(x, U) = y] = P(x, y)$ for all $x, y$. Then $X_{t+1} = f(X_t, U_{t+1})$ is a Markov chain with transition matrix $P$. Each $P$ on a finite set has such a representation: number the states $y_1, \ldots, y_n$, take $U$ uniform on $[0, 1)$, and let $f(x, u) = y_k$ when $\sum_{j < k} P(x, y_j) \le u < \sum_{j \le k} P(x, y_j)$ (LPW Proposition 1.5). This is the way a program runs a chain: one call to a random source per step. [Coupling from the past](/coupling-from-the-past/) and the [coupling method](/coupling-method/) use one $f$ and the same $U$ values for chains that start in different states.

**Notation used on the pages of this group.** $P$ is the transition matrix, $\pi$ a [stationary distribution](/stationary-distribution/), $\|\cdot\|_{TV}$ the [total variation distance](/total-variation-distance/), $d(t) = \max_x \|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon)$ the least $t$ with $d(t) \le \varepsilon$, and $t_{mix} = t_{mix}(1/4)$. See [mixing time](/mixing-time/).

## Examples and non-examples

**The Land of Oz.** The weather in the Land of Oz is rain (R), nice (N) or snow (S). There are never two nice days in a row. After a nice day, rain and snow are equally likely. After rain or snow, the weather stays the same with probability $1/2$, and otherwise each of the two other kinds has probability $1/4$ (Grinstead and Snell, Example 11.1). With the order R, N, S:
$$
P = \begin{pmatrix} 1/2 & 1/4 & 1/4 \\ 1/2 & 0 & 1/2 \\ 1/4 & 1/4 & 1/2 \end{pmatrix}.
$$
By (1), the path R, R, N, S has probability $\Pr_R[X_1 = R, X_2 = N, X_3 = S] = \tfrac12 \cdot \tfrac14 \cdot \tfrac12 = \tfrac1{16}$. The law of the weather after $t$ days from rain is the row $(1, 0, 0)P^t$:

| $t$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $\Pr_R[X_t = R]$ | 1 | 1/2 | 7/16 | 13/32 | 103/256 |
| $\Pr_R[X_t = N]$ | 0 | 1/4 | 3/16 | 13/64 | 51/256 |
| $\Pr_R[X_t = S]$ | 0 | 1/4 | 3/8 | 25/64 | 51/128 |

The rows move toward $(2/5, 1/5, 2/5)$, the [stationary distribution](/stationary-distribution/) of this chain.

**Random walk on a graph.** Let $G$ be a finite [graph](/graph/) with no isolated vertex. From vertex $x$, move to a neighbor chosen uniformly at random: $P(x, y) = 1/\deg(x)$ when $y$ is a neighbor of $x$, and 0 otherwise. The *lazy* walk first stays put with probability $1/2$. [PageRank](/pagerank/) is a random walk on a [directed graph](/directed-graph/) with random jumps.

**Lazy random walk on the hypercube.** The states are the binary strings of length $n$. At each step, choose a coordinate $i$ uniformly and a fair bit $b$, and set coordinate $i$ to $b$. In the random mapping form, $U = (i, b)$ and $f(x, (i, b))$ is $x$ with coordinate $i$ set to $b$. The chain stays put with probability $1/2$.

**Glauber dynamics.** The states are the proper colorings of a graph. At each step, choose a vertex and give it a uniform color that no neighbor has. See [Glauber dynamics](/glauber-dynamics/).

**Sampling without replacement (non-example).** Draw balls one by one, without replacement, from an urn with 2 red balls and 2 blue balls, and let $X_t$ be the color of the $t$-th ball. Then $\Pr[X_3 = \text{red} \mid X_2 = \text{red}] = 1/3$, but $\Pr[X_3 = \text{red} \mid X_1 = \text{red}, X_2 = \text{red}] = 0$ and $\Pr[X_3 = \text{red} \mid X_1 = \text{blue}, X_2 = \text{red}] = 1/2$. The next color depends on more than the current one, so $(X_t)$ is not a Markov chain. The pair of counts of the red and blue balls that remain is a Markov chain: from $(r, b)$ it goes to $(r - 1, b)$ with probability $r/(r + b)$. A larger state can often restore the Markov property.

**A second-order process (non-example).** If $X_{t+1}$ is a function of $(X_{t-1}, X_t)$ and fresh randomness, then $(X_t)$ need not be a Markov chain, but the pairs $Y_t = (X_{t-1}, X_t)$ form one.

## Related definitions

- [Transition matrix](/transition-matrix/): the matrix $P$, its powers $P^t$, and the evolution $\mu \mapsto \mu P$ of the distribution. The chain is the random process; the matrix is the data that fixes its law.
- [Stationary distribution](/stationary-distribution/): a distribution $\pi$ with $\pi P = \pi$.
- [Irreducibility](/irreducibility/), [aperiodicity](/aperiodicity/) and [ergodicity](/ergodicity/): the conditions under which $\pi$ is unique and the law of $X_t$ converges to it.
- [Detailed balance](/detailed-balance/): the condition $\pi(x)P(x, y) = \pi(y)P(y, x)$ of a reversible chain.
- [Ergodic theorem](/ergodic-theorem/): time averages along one path converge to averages under $\pi$.
- [Mixing time](/mixing-time/): how many steps the chain needs to come close to $\pi$.
- [Hidden Markov model](/hidden-markov-model/): a Markov chain that is seen only through noisy outputs. [Markov decision process](/markov-decision-process/): a chain whose transition probabilities depend on actions.
- A *continuous-time* Markov chain jumps at random times. A chain on an infinite state space needs the extra notions of recurrence and positive recurrence (Norris, Chapter 1). The pages of this group treat finite state spaces in discrete time, unless they say otherwise.

## References
