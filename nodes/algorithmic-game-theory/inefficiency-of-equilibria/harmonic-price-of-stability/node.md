---
tag: TA4B7X
kind: theorem
slug: harmonic-price-of-stability
name: Price of stability of network design
aliases:
- H(n) price of stability
- Anshelevich price of stability theorem
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: In the Shapley network design game with n players some pure equilibrium costs at most H(n) times the optimum. The bound is tight in directed graphs and open in undirected ones.
prereqs: [shapley-network-design-game, price-of-stability]
see_also: [rosenthal-potential-theorem, potential-game, best-response-dynamics, steiner-tree-problem, price-of-anarchy, atomic-linear-congestion-price-of-anarchy, cost-sharing-mechanism, shapley-value]
sources:
  - paper: "Elliot Anshelevich, Anirban Dasgupta, Jon Kleinberg, Eva Tardos, Tom Wexler and Tim Roughgarden, The price of stability for network design with fair cost allocation, SIAM Journal on Computing 38(4) (2008), 1602-1623; FOCS 2004, 295-304"
    locator: the upper bound H(n) by the potential function method and the tight example in directed graphs
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 19 (Eva Tardos and Tom Wexler, Network formation games and the potential function method)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 15 (network cost-sharing games and the price of stability H(k))
  - paper: "Yann Disser, Andreas Emil Feldmann, Max Klimm and Matus Mihalak, Improving the H_k-bound on the price of stability in undirected Shapley network design games, Theoretical Computer Science 562 (2015), 557-564"
    locator: an upper bound of (1 - Theta(1/k^4)) H(k) for undirected graphs with k players
  - paper: "Akaki Mamageishvili, Matus Mihalak and Simone Montemezzani, An H_{n/2} upper bound on the price of stability of undirected network design games, Mathematical Foundations of Computer Science (MFCS 2014), LNCS 8635, 541-552"
    locator: the upper bound H(n/2) + epsilon for undirected graphs, and the summary of the open problem
  - paper: "Vittorio Bilo, Ioannis Caragiannis, Angelo Fanelli and Gianpiero Monaco, Improved lower bounds on the price of stability of undirected network design games, Algorithmic Game Theory (SAGT 2010), LNCS 6386, 90-101"
    locator: the lower bound 348/155 for undirected graphs
---

This theorem bounds the best equilibrium of the [Shapley network design game](/shapley-network-design-game/), where players buy paths and split each edge cost equally among its users. The worst equilibrium of that game can cost $n$ times the optimum. This page shows that some equilibrium always costs at most $H(n) = 1 + \tfrac{1}{2} + \cdots + \tfrac{1}{n} \approx \ln n$ times the optimum, and that in directed graphs no better bound holds. The model page defines the game and lists its results; this page gives the proof and the tight example, and it is the standard first use of the potential function method for the [price of stability](/price-of-stability/).

## Statement

A Shapley network design game has a graph $G = (V, E)$, directed or undirected, edge costs $c_e \ge 0$, and $n$ players. Player $i$ picks a path $P_i$ from $s_i$ to $t_i$ and pays $\sum_{e \in P_i} c_e / x_e$, where $x_e$ is the number of players whose paths use $e$; it minimizes this cost. The social cost is $C(P) = \sum_{e : x_e \ge 1} c_e$. The game is a finite congestion game, the equilibrium notion is pure Nash equilibrium, and pure equilibria exist.

**Theorem (Anshelevich, Dasgupta, Kleinberg, Tardos, Wexler and Roughgarden 2004).**

1. In every such game, directed or undirected, there is a pure Nash equilibrium $P$ with $C(P) \le H(n)\, C(P^*)$ for every profile $P^*$. Every path of strict unilateral improvements that starts at an optimal profile ends at such an equilibrium.
2. In directed graphs the bound is tight: for every $n \ge 1$ and every $\varepsilon > 0$ there is a game with $n$ players whose only pure equilibrium costs $H(n)/(1 + \varepsilon)$ times the optimum.

So the price of stability of the class is $H(n)$ in directed graphs and at most $H(n)$ in undirected graphs.

## In plain words

Several people need routes through a network, and people who use the same link split its price equally. Some stable choices can be very wasteful. But there is always a stable choice whose total price is at most a small factor above the cheapest network, and the factor grows only like the logarithm of the number of people. To find such a choice, start from the cheapest network and let people switch to cheaper routes one at a time. In networks with one-way links, an example shows that this factor is the best possible. In networks with two-way links, the exact factor is still unknown.

## Proof

**The potential.** By [Rosenthal's theorem](/rosenthal-potential-theorem/) with resource costs $c_e(j) = c_e / j$, the function

$$\Phi(P) = \sum_{e \in E} c_e\, H(x_e), \qquad H(0) = 0,$$

is an exact potential: when one player changes its path, $\Phi$ changes by exactly the change in that player's cost.

**The sandwich.** For every profile $P$, each used edge has $1 \le x_e \le n$, so $c_e \le c_e H(x_e) \le c_e H(n)$, and unused edges add 0 to both $C$ and $\Phi$. Adding over the edges,

$$C(P) \le \Phi(P) \le H(n)\, C(P).$$

**The bound.** Let $P^*$ be an optimal profile. Run any improvement dynamics from $P^*$. Each step lowers $\Phi$ strictly, and the game is finite, so the dynamics ends at a pure equilibrium $P$ with $\Phi(P) \le \Phi(P^*)$. Then

$$C(P) \le \Phi(P) \le \Phi(P^*) \le H(n)\, C(P^*).$$

The same holds for a global minimizer of $\Phi$. This proves part 1.

**The tight example.** Take a directed graph with a sink $t$, a vertex $v$, and sources $s_1, \ldots, s_n$. For each $i$ there is an edge $s_i \to t$ of cost $1/i$ and an edge $s_i \to v$ of cost 0, and there is one edge $v \to t$ of cost $1 + \varepsilon$. Player $i$ goes from $s_i$ to $t$ and has two paths: direct, or through $v$. No edge leaves $t$ or $v$ except $v \to t$, and no edge enters a source, so the direct edge $s_i \to t$ can be used only by player $i$.

If all players go through $v$, the cost is $1 + \varepsilon$, so the optimum is at most $1 + \varepsilon$. Now take any pure equilibrium, and suppose that a set $S$ of $k \ge 1$ players uses $v \to t$. Let $j$ be the largest index in $S$; then $j \ge k$. Player $j$ pays $(1 + \varepsilon)/k$, but its direct edge costs $1/j \le 1/k < (1 + \varepsilon)/k$, so it gains by leaving, which is a contradiction. So in every equilibrium all players go direct, with cost $\sum_i 1/i = H(n)$. That profile is an equilibrium, because player $i$ pays $1/i \le 1$, and alone on $v \to t$ it would pay $1 + \varepsilon$. The ratio is $H(n)/(1 + \varepsilon)$. This proves part 2. $\blacksquare$

### Example

Take the tight example with $n = 4$ and $\varepsilon = 1/10$. Start at the optimum, all four players through $v$, with social cost $11/10$ and $\Phi = \tfrac{11}{10} H(4) = 55/24$. Let the players move in the order 1, 2, 3, 4, repeatedly, each switching when the other path is cheaper.

| move | share on $v \to t$ before | direct cost | gain | $\Phi$ after | social cost after |
|---|---|---|---|---|---|
| player 4 leaves $v$ | $11/40$ | $1/4$ | $1/40$ | $34/15$ | $27/20$ |
| player 3 leaves $v$ | $11/30$ | $1/3$ | $1/30$ | $67/30$ | $101/60$ |
| player 2 leaves $v$ | $11/20$ | $1/2$ | $1/20$ | $131/60$ | $131/60$ |
| player 1 leaves $v$ | $11/10$ | $1$ | $1/10$ | $25/12$ | $25/12$ |

In the first round players 1, 2 and 3 do not move, because their direct edges cost more than their shares; player 4 moves first. Each move lowers $\Phi$ by exactly the gain of the mover. The social cost rises at each step, from $11/10$ to $25/12 = H(4)$, but it stays below the starting $\Phi = 55/24$, as the proof says. The ratio of the only equilibrium to the optimum is $\tfrac{25/12}{11/10} = 125/66 \approx 1.894$, against $H(4) \approx 2.083$.

## Consequences

- **The potential function method.** The proof uses only that $\Phi$ is an exact potential and that $A^{-1} C \le \Phi \le B\, C$ with $A = 1$ and $B = H(n)$; any game with such a potential has price of stability at most $AB$. For affine congestion games the same argument gives 2.
- **A good equilibrium from the optimum.** If a planner proposes the optimal network and lets players improve, the result is within $H(n)$ of the optimum. Finding the optimum is a Steiner problem and NP-hard, but starting from an $\alpha$-approximate network gives an equilibrium within $\alpha H(n)$, because $C(P) \le \Phi(P) \le \Phi(P^0) \le H(n)\, C(P^0)$ for the start $P^0$. The proof gives no polynomial bound on the number of steps.
- **The best and the worst equilibrium are far apart.** The price of anarchy of the class is $n$, so the gap between $H(n)$ and $n$ shows how much a planner who can choose the starting point gains.

## Tightness

- **Directed graphs.** The example above shows that $H(n)$ is the exact price of stability for every $n$.
- **Undirected graphs.** The exact value is open. In an undirected version of the example the players have more paths, for example $s_i$, $v$, $s_j$, $t$, and the proof of uniqueness above does not apply. The upper bound $H(n)$ has been improved only slightly: to $(1 - \Theta(1/n^4)) H(n)$ (Disser, Feldmann, Klimm and Mihalak, TCS 2015) and to $H(n/2) + \varepsilon$ (Mamageishvili, Mihalak and Montemezzani, MFCS 2014). The best lower bound in these sources is a constant, $348/155 \approx 2.245$ (Bilo, Caragiannis, Fanelli and Monaco, SAGT 2010). For a common sink the price of stability is $O(\log n / \log \log n)$ (Li 2009), and in the broadcast case it is a constant (Bilo, Flammini and Moscardelli). These are the bounds known in the sources of 2014 and 2015; whether the price of stability in undirected graphs is constant or grows with $n$ is open there.
- **Weights.** With weighted players who share costs in proportion to their weights, the game need not have an exact potential, and the bound $H(n)$ does not follow.

## History

Anshelevich, Dasgupta, Kleinberg, Tardos, Wexler and Roughgarden introduced the game at FOCS 2004 and made the term "price of stability" standard; the journal version appeared in 2008. Their proof made the potential function method a standard tool for bounding the best equilibrium. The undirected case became a well known open problem, and work from 2006 to 2015 improved the bounds for broadcast, single sink and general undirected games.

## References
