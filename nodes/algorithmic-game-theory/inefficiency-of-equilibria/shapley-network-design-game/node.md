---
tag: P5PV58
kind: model
slug: shapley-network-design-game
name: Shapley network design game
aliases:
- fair cost allocation game
- Anshelevich network design game
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: Players buy paths between their terminals and split the cost of each edge equally among its users. It is a congestion game.
prereqs: [atomic-congestion-game]
see_also: [harmonic-price-of-stability, price-of-stability, steiner-tree-problem, cost-sharing-mechanism, shapley-value, rosenthal-potential-theorem, network-creation-game, price-of-anarchy]
sources:
  - paper: "Elliot Anshelevich, Anirban Dasgupta, Jon Kleinberg, Eva Tardos, Tom Wexler and Tim Roughgarden, The price of stability for network design with fair cost allocation, SIAM Journal on Computing 38(4) (2008), 1602-1623; FOCS 2004, 295-304"
    locator: the model with fair cost allocation, the potential, the price of anarchy n, the price of stability H(n) and its tight example in directed graphs
  - paper: doi:10.1007/BF01737559
    title: "Robert W. Rosenthal, A class of games possessing pure-strategy Nash equilibria, International Journal of Game Theory 2 (1973), 65-67"
    locator: the potential of congestion games, which with costs c_e/x gives the potential of this game
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 19 (Eva Tardos and Tom Wexler, Network formation games and the potential function method), the section on fair cost sharing
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 15 (network cost-sharing games and the price of stability)
---

In the Shapley network design game, players who need to connect two points of a network buy paths, and the users of each edge split its cost equally. It is a [congestion game](/atomic-congestion-game/) with decreasing costs: the more players use an edge, the less each of them pays. This page defines the model and collects its results. The bound on the best equilibrium, the harmonic number $H(n)$, is proved on its own page, [price of stability of network design](/harmonic-price-of-stability/). The [network creation game](/network-creation-game/) is a different model: there the players are vertices that buy edges to be close to all other vertices.

## The machine

- **Network.** A graph $G = (V, E)$, directed or undirected, with a cost $c_e \ge 0$ on each edge.
- **Players.** $n$ players. Player $i$ has a source $s_i$ and a sink $t_i$ in $V$.
- **Strategies.** Player $i$ picks a path $P_i$ from $s_i$ to $t_i$. A profile is $P = (P_1, \ldots, P_n)$, and the load $x_e$ is the number of players whose path uses $e$.
- **Costs.** The users of an edge share its cost equally, so player $i$ pays
$$c_i(P) = \sum_{e \in P_i} \frac{c_e}{x_e},$$
and minimizes it. The equilibrium notion is pure Nash equilibrium.

This is a congestion game with resource costs $c_e(x) = c_e / x$, which decrease in $x$. The equal split is the [Shapley value](/shapley-value/) of the cost of one edge among its users, which gives the name; the same rule is called fair cost allocation. Common special cases:

- **Single source.** All players have the same source; the paths then form a network that connects the source to all sinks.
- **Broadcast.** Single source, and every vertex other than the source is the sink of one player.
- **Directed or undirected.** The bounds differ between the two cases, as the results below show.

## What it counts

- **Player cost** $c_i(P)$, which defines the equilibria.
- **Social cost**, the total cost of the edges that some player uses,
$$C(P) = \sum_{e : x_e \ge 1} c_e = \sum_{i=1}^n c_i(P).$$
The two forms agree because the shares of each used edge add up to its cost. A cheapest profile is a cheapest network that connects every $s_i$ to $t_i$: a minimum Steiner forest, or a minimum [Steiner tree](/steiner-tree-problem/) in the single source case. Computing it is NP-hard.
- **Rosenthal's potential**, which with $c_e(j) = c_e / j$ becomes
$$\Phi(P) = \sum_{e \in E} c_e\, H(x_e), \qquad H(k) = 1 + \tfrac{1}{2} + \cdots + \tfrac{1}{k},\ H(0) = 0.$$
Since $1 \le H(x_e) \le H(n)$ for each used edge, $C(P) \le \Phi(P) \le H(n)\, C(P)$ for every profile.
- **The price of anarchy and the price of stability**, the worst and the best equilibrium cost divided by the optimum.

## Relation to other models

- **Congestion games.** The game is a congestion game, so [Rosenthal's theorem](/rosenthal-potential-theorem/) applies: $\Phi$ is an exact potential, pure equilibria exist, and improvement dynamics ends. Unlike in routing games, costs fall with load, so players want to share.
- **Steiner problems.** The optimum is the [Steiner tree](/steiner-tree-problem/) or Steiner forest of the terminals. An equilibrium is a network that is stable when each player pays its share, so the model asks how much stability costs over the cheapest network.
- **Cost sharing.** The equal split is one [cost-sharing mechanism](/cost-sharing-mechanism/) for a network. Other rules, for example rules that charge players by their order or by weights, give other games, and some of them have no pure equilibrium.
- **Network creation.** In the [network creation game](/network-creation-game/), each vertex buys edges alone and pays for its distances to all other vertices. There is no sharing of edge costs, and the model is different.

## Known results in the model

**Pure equilibria exist, and best-response dynamics finds one.** By Rosenthal's theorem every improving move lowers $\Phi$ by the gain of the player who moves. A best response of player $i$ is a shortest $s_i$-$t_i$ path with length $c_e / (x_e + 1)$ on the edges that $i$ does not use and $c_e / x_e$ on the edges it uses.

**The price of anarchy is $n$.** Let $P$ be an equilibrium and $P^*$ any profile. If player $i$ moved to $P_i^*$, it would pay at most the full cost of that path, so $c_i(P) \le \sum_{e \in P_i^*} c_e \le C(P^*)$. Adding over the players gives $C(P) \le n\, C(P^*)$.

The bound is tight. Take $n$ players with the same source $s$ and sink $t$, joined by two parallel edges of costs 1 and $n$. For $n = 3$:

| players on edge of cost 1 | player costs | social cost $C$ | potential $\Phi$ | equilibrium |
|---|---|---|---|---|
| 3 | 1/3, 1/3, 1/3 | 1 | 11/6 | yes |
| 2 | 1/2, 1/2, 3 | 4 | 9/2 | no |
| 1 | 1, 3/2, 3/2 | 4 | 11/2 | no |
| 0 | 1, 1, 1 | 3 | 11/2 | yes |

When all three use the edge of cost 3, each pays 1, and a player who moves alone to the other edge also pays 1, so nobody gains. The equilibrium costs 3 and the optimum costs 1. In general this equilibrium costs $n$, against an optimum of 1.

**The price of stability is $H(n)$.** A minimizer $P$ of $\Phi$ is an equilibrium, and for an optimal profile $P^*$,
$$C(P) \le \Phi(P) \le \Phi(P^*) \le H(n)\, C(P^*).$$
In directed graphs there are games where every equilibrium costs $H(n)/(1 + \varepsilon)$ times the optimum, for any $\varepsilon > 0$, so $H(n)$ is tight. In undirected graphs the exact value is open. See [price of stability of network design](/harmonic-price-of-stability/).

**Computing a good equilibrium.** Starting best-response dynamics from an optimal profile gives an equilibrium within $H(n)$ of the optimum, since $\Phi$ only falls. But the optimum is a Steiner problem and NP-hard, and Anshelevich and coauthors showed that finding the cheapest equilibrium is NP-hard as well.

## References
