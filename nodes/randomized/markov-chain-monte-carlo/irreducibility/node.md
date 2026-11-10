---
tag: 1DXE53
kind: definition
slug: irreducibility
name: Irreducibility
aliases:
- irreducible Markov chain
area: randomized/markov-chain-monte-carlo
level: core
summary: A Markov chain is irreducible when each state can reach each other state with positive probability. On a finite space this means a strongly connected transition graph and a unique, positive π.
prereqs: [markov-chain, transition-matrix, strongly-connected-graph]
see_also: [aperiodicity, ergodicity, stationary-distribution, ergodic-theorem, strongly-connected-components, glauber-dynamics, metropolis-hastings, graph-coloring]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 1.3, Irreducibility and Aperiodicity (definition); Section 1.5, Stationary Distributions (Lemma 1.13, Corollary 1.17); Section 1.7, Classifying the States of a Markov Chain
  - book: isbn:9780521633963
    title: J. R. Norris, Markov Chains, Cambridge University Press, 1997
    locator: Section 1.2, Class structure
---

A [Markov chain](/markov-chain/) is irreducible when, for each pair of states $x$ and $y$, the chain started at $x$ reaches $y$ with positive probability at some time. On a finite state space this is a property of the pattern of non-zero entries of the [transition matrix](/transition-matrix/): the directed graph with an edge $x \to y$ when $P(x, y) > 0$ must be [strongly connected](/strongly-connected-graph/). Irreducibility is the condition for a unique [stationary distribution](/stationary-distribution/), positive on each state. It does not give convergence of $P^t(x, \cdot)$ to $\pi$; that needs [aperiodicity](/aperiodicity/) too, and the two together are [ergodicity](/ergodicity/).

## Definition

Let $P$ be a transition matrix on a finite set $\mathcal X$. The state $x$ *leads to* $y$, written $x \to y$, if $P^t(x, y) > 0$ for some $t \ge 0$. The states $x$ and $y$ *communicate* if $x \to y$ and $y \to x$. The chain (or $P$) is *irreducible* if each pair of states communicates:
$$
\text{for all } x, y \in \mathcal X \text{ there is } t \ge 0 \text{ with } P^t(x, y) > 0.
$$
Some books ask for $t \ge 1$. This changes nothing: for $x \ne y$ a path needs $t \ge 1$, and for $x = y$ a path $x \to y' \to x$ through any other state $y'$ has length at least 1 (and a chain with one state has $P = (1)$).

**Graph form.** Let $G(P)$ be the [directed graph](/directed-graph/) on $\mathcal X$ with an edge $x \to y$ when $P(x, y) > 0$. Then $P^t(x, y) > 0$ if and only if $G(P)$ has a [walk](/walk/) of length $t$ from $x$ to $y$, because $P^t(x, y)$ is the sum, over the walks of length $t$, of the products of the entries along them, and each product is positive exactly when each edge is in $G(P)$. So $P$ is irreducible if and only if $G(P)$ is strongly connected. The values of the positive entries do not matter. A [strongly connected components](/strongly-connected-components/) algorithm checks irreducibility in time linear in the number of states plus the number of non-zero entries.

**Classes.** "Communicate" is an equivalence relation. Its classes are the strongly connected components of $G(P)$, and they are called *communicating classes*. A class $C$ is *closed* if no edge leaves it. Each finite chain has at least one closed class: the components form an acyclic graph, and a sink of that graph is closed. A chain is irreducible exactly when it has one class.

### The return times are finite

For a state $y$ let $\tau_y^+ = \min\{t \ge 1 : X_t = y\}$.

**Lemma (LPW Lemma 1.13).** If $P$ is irreducible on a finite set, then $\mathbb E_x \tau_y^+ < \infty$ for all $x, y$.

*Proof.* Fix $y$. For each state $z$, irreducibility gives a time $s_z \ge 1$ with $P^{s_z}(z, y) > 0$. Let $r = \max_z s_z$ and $\varepsilon = \min_z P^{s_z}(z, y) > 0$. From each state $z$, the chain is at $y$ at time $s_z \le r$ with probability at least $\varepsilon$, so $\Pr_z[\tau_y^+ \le r] \ge \varepsilon$. By the Markov property at the times $r, 2r, \ldots$, $\Pr_x[\tau_y^+ > kr] \le (1 - \varepsilon)^k$. Hence
$$
\mathbb E_x \tau_y^+ = \sum_{t \ge 0} \Pr_x[\tau_y^+ > t] \le r \sum_{k \ge 0} \Pr_x[\tau_y^+ > kr] \le \frac{r}{\varepsilon}. \qquad \square
$$

**What irreducibility gives.** By the theorem on the page [stationary distribution](/stationary-distribution/), an irreducible finite chain has a unique stationary distribution $\pi$, with $\pi(x) = 1/\mathbb E_x\tau_x^+ > 0$ for each $x$. By the [ergodic theorem](/ergodic-theorem/), the fraction of time it spends in $x$ tends to $\pi(x)$ with probability 1. These two facts do not need aperiodicity.

**What irreducibility does not give.** The law of $X_t$ need not converge. The walk on two states with $P = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ is irreducible, and $P^t$ alternates between $I$ and $P$. See [aperiodicity](/aperiodicity/).

## Examples and non-examples

**The Land of Oz.** Each entry of the Land of Oz matrix is positive except $P(N, N) = 0$, and $N \to R \to N$, so the chain is irreducible.

**Random walks on graphs.** The simple random walk on an undirected graph is irreducible if and only if the graph is connected. On a [directed graph](/directed-graph/) it is irreducible if and only if the graph is strongly connected. [PageRank](/pagerank/) adds a jump to a uniform page with probability $1 - \alpha$ at each step, so all entries of its matrix are positive and the chain is irreducible on any web graph.

**The hypercube walk.** The lazy walk on $\{0, 1\}^n$ that resets a random coordinate to a fair bit is irreducible: any string becomes any other by changing the coordinates where they differ, one at a time.

**Absorbing chains (non-example).** Gambler's ruin on $\{0, 1, \ldots, N\}$ moves up or down by 1 with probability $1/2$ each and stops at $0$ and $N$. The states 0 and $N$ are closed classes, and the states in between form a class that is not closed. Each mixture of the point masses at 0 and $N$ is stationary, so the stationary distribution is not unique.

**Glauber dynamics for colorings.** Let $G$ have maximum degree $\Delta$. The [Glauber dynamics](/glauber-dynamics/) on proper $q$-colorings picks a vertex and gives it a uniform color that its neighbors do not use.

- *With $q = \Delta + 1$ it can fail.* On a triangle with $q = 3$, each vertex sees two different colors on its neighbors, so its only allowed color is its own. Each of the 6 proper colorings is absorbing, $P = I$, and the chain is not irreducible.
- *With $q \ge \Delta + 2$ it is irreducible.* Order the vertices $v_1, \ldots, v_n$, and let $x$ and $y$ be proper colorings. Change $x$ into $y$ one vertex at a time. Before vertex $v_i$ gets the color $c = y(v_i)$, recolor each neighbor $w$ of $v_i$ with $w$ later in the order and current color $c$: such a $w$ has at most $\Delta$ neighbors, so at least $q - \Delta - 1 \ge 1$ colors are free at $w$ and differ from $c$. The neighbors of $v_i$ earlier in the order already have their $y$ colors, which differ from $c$ because $y$ is proper. Then give $v_i$ the color $c$. Each move is a legal step of the chain, and the vertices $v_1, \ldots, v_i$ keep their $y$ colors.

**Metropolis chains.** A [Metropolis-Hastings](/metropolis-hastings/) chain is irreducible on the support of its target when the proposal graph is connected on that support. A proposal that never leaves a region gives a reducible chain, and its output depends on the start.

## Related definitions

- [Aperiodicity](/aperiodicity/): the gcd of the return times is 1. Irreducibility is about "can reach"; aperiodicity is about "at which times".
- [Ergodicity](/ergodicity/): on these pages, irreducible and aperiodic together. Then $P^t(x, y) \to \pi(y)$.
- [Ergodic theorem](/ergodic-theorem/): the law of large numbers along one path, which needs only irreducibility.
- [Stationary distribution](/stationary-distribution/): unique and positive for irreducible chains.
- [Strongly connected graph](/strongly-connected-graph/) and [strongly connected components](/strongly-connected-components/): the graph notions behind irreducibility and communicating classes.
- On infinite state spaces, irreducibility is not enough for a stationary distribution; one also needs positive recurrence (Norris, Sections 1.5 to 1.7).

## References
