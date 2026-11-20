---
tag: AE0S3S
kind: model
slug: atomic-congestion-game
name: Congestion game
aliases:
- atomic congestion game
- Rosenthal congestion game
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: A finite game where each player picks a set of resources and pays the sum of their costs, and each resource cost depends only on how many players use it.
prereqs: [normal-form-game, pure-nash-equilibrium]
see_also: [rosenthal-potential-theorem, potential-game, selfish-routing-model, symmetric-network-congestion-min-cost-flow, pls-completeness-of-congestion-games, atomic-linear-congestion-price-of-anarchy, shapley-network-design-game, load-balancing-game]
sources:
  - paper: doi:10.1007/BF01737559
    title: "Robert W. Rosenthal, A class of games possessing pure-strategy Nash equilibria, International Journal of Game Theory 2 (1973), 65-67"
    locator: the definition of congestion games and the potential that proves they have pure equilibria
  - paper: doi:10.1006/game.1996.0044
    title: "Dov Monderer and Lloyd S. Shapley, Potential games, Games and Economic Behavior 14(1) (1996), 124-143"
    locator: the isomorphism between finite exact potential games and congestion games
  - paper: doi:10.1145/1007352.1007445
    title: "Alex Fabrikant, Christos Papadimitriou and Kunal Talwar, The complexity of pure Nash equilibria, Proceedings of the 36th Annual ACM Symposium on Theory of Computing (STOC 2004), 604-612"
    locator: PLS-completeness of finding a pure equilibrium, and the polynomial case of symmetric network games
  - paper: doi:10.1145/1060590.1060600
    title: "George Christodoulou and Elias Koutsoupias, The price of anarchy of finite congestion games, Proceedings of the 37th Annual ACM Symposium on Theory of Computing (STOC 2005), 67-73"
    locator: the price of anarchy 5/2 for linear costs
  - paper: doi:10.1145/1060590.1060599
    title: "Baruch Awerbuch, Yossi Azar and Amir Epstein, The price of routing unsplittable flow, Proceedings of the 37th Annual ACM Symposium on Theory of Computing (STOC 2005), 57-66"
    locator: the price of anarchy 5/2 for linear costs, (3 + 5^(1/2))/2 for weighted players, and the bounds for polynomial costs
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 12 (atomic selfish routing), Lecture 13 (potential games) and Lecture 16 (best-response dynamics)
---

A congestion game models players who share resources, such as links of a network, machines or facilities. Each player picks a set of resources, and each resource charges all its users the same cost, which depends only on the number of its users. The model is atomic: each player is one indivisible unit and its choice changes the loads. That is the difference from the [selfish routing model](/selfish-routing-model/), where traffic is a continuum of tiny users. The result that makes the model useful is [Rosenthal's theorem](/rosenthal-potential-theorem/): every congestion game is a [potential game](/potential-game/) and has a pure Nash equilibrium.

## The machine

- **Players.** A finite set $N = \{1, \ldots, n\}$.
- **Resources.** A finite set $E$ of $m$ resources. Each resource $e$ has a cost function $c_e : \{1, \ldots, n\} \to \mathbb{R}$, where $c_e(j)$ is the cost that each user of $e$ pays when $j$ players use it. The standard assumptions are that $c_e$ is nonnegative and nondecreasing; Rosenthal's theorem needs neither.
- **Strategies.** Player $i$ has a finite set $S_i$ of nonempty subsets of $E$. A profile is $s = (s_1, \ldots, s_n)$ with $s_i \in S_i$, and players use pure strategies unless the text says otherwise.
- **Loads and costs.** The load of $e$ is $x_e(s) = |\{i : e \in s_i\}|$. Player $i$ pays $c_i(s) = \sum_{e \in s_i} c_e(x_e(s))$ and minimizes it. All players know the game.

Common special cases:

- **Network games.** $E$ is the edge set of a directed graph, and $S_i$ is the set of paths from $s_i$ to $t_i$. The game is symmetric if all players have the same source and sink.
- **Symmetric games.** All $S_i$ are equal.
- **Singleton games.** Every strategy is one resource, for example parallel links or identical machines.
- **Matroid games.** Each $S_i$ is the set of bases of a [matroid](/matroid/) on $E$, for example spanning trees.
- **Affine costs.** $c_e(x) = a_e x + b_e$ with $a_e, b_e \ge 0$; linear if $b_e = 0$.

A congestion game is a normal-form game with a short description: the cost tables and the strategy sets. Network games describe $S_i$ by the graph, so a player can have exponentially many strategies.

## What it counts

- **The cost of each player**, $c_i(s)$, which defines the equilibria.
- **The social cost** $C(s) = \sum_i c_i(s) = \sum_{e \in E} x_e(s)\, c_e(x_e(s))$, which defines the optimum and so the [price of anarchy](/price-of-anarchy/) (the worst equilibrium over the optimum) and the [price of stability](/price-of-stability/) (the best equilibrium over the optimum). Some papers use the largest player cost, $\max_i c_i(s)$, in its place.
- **Rosenthal's potential** $\Phi(s) = \sum_{e \in E} \sum_{j=1}^{x_e(s)} c_e(j)$, the tool of most proofs. A unilateral deviation changes $\Phi$ by exactly the change in the deviator's cost. With nonnegative nondecreasing costs, $\Phi(s) \le C(s) \le n\, \Phi(s)$, and with affine costs $C(s) \le 2\, \Phi(s)$.
- **The number of steps** of [best-response dynamics](/best-response-dynamics/), and the time to compute an equilibrium.

## Relation to other models

- **Potential games.** Every congestion game is an exact potential game, and Monderer and Shapley proved the converse up to isomorphism: every finite exact potential game is isomorphic to a congestion game. The two classes are the same up to renaming.
- **Nonatomic selfish routing.** In the [selfish routing model](/selfish-routing-model/) the traffic is divisible, the equilibrium is a [Wardrop equilibrium](/wardrop-equilibrium/), and the potential is the [Beckmann potential](/beckmann-potential/), an integral in place of Rosenthal's sum. Atomic games can have several equilibria with different costs, and their price of anarchy for affine costs is $5/2$, against $4/3$ in the nonatomic model.
- **Load balancing.** A [load balancing game](/load-balancing-game/) is a singleton game, usually with weighted jobs and the makespan as social cost.
- **Network design.** The [Shapley network design game](/shapley-network-design-game/) is a congestion game with decreasing costs $c_e(x) = c_e / x$: users share the cost of an edge.
- **Weighted and player-specific games.** If players have weights and a resource cost depends on the total weight, pure equilibria may not exist (Libman and Orda 2001; Goemans, Mirrokni and Vetta 2005); with affine costs a weighted potential exists (Fotakis, Kontogiannis and Spirakis 2005). If each player has its own cost function per resource, the game leaves the model; for singleton strategies a pure equilibrium still exists (Milchtaich 1996).

## Known results in the model

**Pure equilibria exist.** Every congestion game has a pure Nash equilibrium, because a minimizer of $\Phi$ is one ([Rosenthal's theorem](/rosenthal-potential-theorem/)). In fact the pure equilibria are exactly the profiles from which no unilateral deviation lowers $\Phi$.

**Best-response dynamics converges.** The game has the [finite improvement property](/finite-improvement-property/): every sequence of strict improvements ends, at an equilibrium. The round-robin version is:

```pseudo id=main
BEST-RESPONSE-DYNAMICS(game, s)
L1  repeat
L2      for each player i in turn:
L3          b ← a strategy of i that minimizes c_i(b, s_-i)
L4          if c_i(b, s_-i) < c_i(s): s_i ← b    ▷ Φ falls by exactly the gain of i
L5  until no player moved in a full round; return s
```

The file proofs/correctness.md proves that each move lowers $\Phi$ by exactly the gain of the player who moves, and that the loop ends at a pure equilibrium. With integer costs it ends after at most $\Phi(s^0)$ moves, a pseudo-polynomial bound.

**Atomic Pigou example.** Two players choose between link 1, with cost 2 for any load, and link 2, with cost $c(x) = x$.

| profile | player costs | social cost $C$ | potential $\Phi$ | pure equilibrium |
|---|---|---|---|---|
| both on link 1 | 2, 2 | 4 | 4 | no |
| one on each link | 2, 1 | 3 | 3 | yes |
| both on link 2 | 2, 2 | 4 | 3 | yes |

From "both on link 1", player 1 moves to link 2: its cost falls from 2 to 1, and $\Phi$ falls from 4 to 3. Then player 2 would pay 2 on link 2, no less than on link 1, and the dynamics stops at the split. Both equilibria minimize $\Phi$, but one costs 3 and the other 4, so the optimum is 3, the price of anarchy is $4/3$ and the price of stability is 1. In the nonatomic Pigou example the equilibrium is unique; here the indivisible players make a second, worse equilibrium.

**Computing an equilibrium.** Finding a pure equilibrium is PLS-complete, for general games, for symmetric games and for network games with different sources and sinks, and best-response dynamics can need exponentially many steps ([PLS-completeness of congestion games](/pls-completeness-of-congestion-games/)). Symmetric network games are easy: a [min-cost flow](/symmetric-network-congestion-min-cost-flow/) gives the minimizer of $\Phi$ in polynomial time. In matroid games, best-response dynamics converges after polynomially many moves (Ackermann, Roglin and Vocking 2008). Computing a mixed Nash equilibrium of a congestion game is CLS-complete (Babichenko and Rubinstein, STOC 2021).

**Price of anarchy and stability.** With affine costs and social cost $C$, every pure equilibrium costs at most $5/2$ times the optimum, and this is tight ([price of anarchy of linear congestion games](/atomic-linear-congestion-price-of-anarchy/); Christodoulou and Koutsoupias 2005, Awerbuch, Azar and Epstein 2005). The bound extends to mixed, correlated and coarse correlated equilibria by the [smoothness framework](/smoothness-framework/). With weighted players it is $(3 + \sqrt{5})/2$. The price of stability for affine costs is $1 + 1/\sqrt{3} \approx 1.577$ (lower bound by Christodoulou and Koutsoupias, ESA 2005; upper bound by Caragiannis and others, ICALP 2006). For polynomial costs of degree $d$ with nonnegative coefficients, the price of anarchy grows exponentially in $d$ (Awerbuch, Azar and Epstein 2005).

## References
