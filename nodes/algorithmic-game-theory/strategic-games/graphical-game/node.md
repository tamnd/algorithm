---
tag: 7E9RCF
kind: model
slug: graphical-game
name: Graphical game
aliases:
- Kearns-Littman-Singh graphical game
area: algorithmic-game-theory/strategic-games
level: advanced
summary: A succinct game on a graph in which the payoff of each player depends only on the actions of the player and of its neighbours.
prereqs: [normal-form-game, nash-equilibrium]
see_also: [nash-equilibrium-computation, ppad, epsilon-nash-equilibrium, graphical-model, belief-propagation, treewidth, correlated-equilibrium, potential-game]
sources:
  - paper: "Michael Kearns, Michael L. Littman and Satinder Singh, Graphical models for game theory, Proceedings of the 17th Conference on Uncertainty in Artificial Intelligence (UAI 2001), 253-260"
    title: Graphical models for game theory
    locator: the definition of graphical games and the dynamic program on trees that finds approximate Nash equilibria
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 7, Graphical Games, by Michael Kearns, pp. 159-180
  - paper: "Edith Elkind, Leslie Ann Goldberg and Paul W. Goldberg, Nash equilibria in graphical games on trees revisited, Proceedings of the 7th ACM Conference on Electronic Commerce (EC 2006), 100-109"
    title: Nash equilibria in graphical games on trees revisited
    locator: a quadratic time algorithm for paths, exponential running time of the tree algorithm on some trees of bounded degree, and PPAD-completeness for degree 3
  - paper: doi:10.1613/jair.1683
    title: "Georg Gottlob, Gianluigi Greco and Francesco Scarcello, Pure Nash equilibria: hard and easy games, Journal of Artificial Intelligence Research 24 (2005), 357-406"
    locator: NP-completeness of the existence of a pure Nash equilibrium in graphical games, and tractable classes of acyclic and bounded treewidth graphs
  - paper: doi:10.1137/070699652
    title: "Constantinos Daskalakis, Paul W. Goldberg and Christos H. Papadimitriou, The complexity of computing a Nash equilibrium, SIAM Journal on Computing 39(1) (2009), 195-259"
    locator: the reduction from games with many players to graphical games of bounded degree, used for PPAD-completeness
---

A graphical game is a game with many players whose interactions are given by a graph: each player is a node, and the payoff of a player depends only on its own action and on the actions of its neighbours in the graph. Kearns, Littman and Singh (2001) introduced it as a compact way to write a [normal-form game](/normal-form-game/) with $n$ players, in the same way that a [graphical model](/graphical-model/) writes a joint probability distribution with local factors. The solution concept is the usual [Nash equilibrium](/nash-equilibrium/) of the full game; what changes is the size of the input, and so what "polynomial time" means. On trees and on paths the graph gives fast algorithms, while on graphs of degree 3 finding an equilibrium is already [PPAD](/ppad/)-complete.

## The machine

A graphical game has

- an undirected graph $G = (V, E)$ with $V = \{1, \ldots, n\}$, one node for each player; $N(i)$ is the set of neighbours of $i$, and $d$ is the largest degree;
- for each player $i$, a finite set $S_i$ of actions, with $|S_i| \le k$;
- for each player $i$, a *local payoff function* $u_i : \prod_{j \in \{i\} \cup N(i)} S_j \to \mathbb{R}$, which the player maximizes.

The game it stands for is the normal-form game with players $V$, actions $S_i$ and payoffs $u_i(s) = u_i(s_i, s_{N(i)})$, where $s_{N(i)}$ is the restriction of $s$ to the neighbours. The players move once, at the same time, and use mixed strategies $\sigma_i \in \Delta(S_i)$ as usual. Every normal-form game is a graphical game on the complete graph; the model is useful when $d$ is much smaller than $n$. Some authors use a directed graph, in which $u_i$ depends on the players with an edge into $i$; the results below are stated for the undirected form.

**The input size.** Player $i$ needs a table of $k^{|N(i)| + 1}$ numbers, so the game has at most $n k^{d + 1}$ numbers, against $n k^n$ for the table of the full game. For a path of 3 players with 2 actions each, the end players need $2^2 = 4$ numbers and the middle one $2^3 = 8$, so 16 numbers in all against $3 \cdot 2^3 = 24$. For a path of 20 players, the count is $2 \cdot 4 + 18 \cdot 8 = 152$, against $20 \cdot 2^{20}$, which is more than 20 million.

## What it counts

The model counts the cost of computing equilibria as a function of the size $n k^{d + 1}$ of the succinct input, and of the shape of the graph: whether it is a tree or a path, its degree $d$, and its [treewidth](/treewidth/). The expected payoff of player $i$ under a mixed profile is a sum over the $k^{|N(i)| + 1}$ local profiles, so it costs time polynomial in the input, and a claimed Nash or [$\varepsilon$-Nash equilibrium](/epsilon-nash-equilibrium/) is checked in time polynomial in the input. The questions are then how fast an exact or approximate Nash equilibrium can be found, whether a pure one exists, and the same for [correlated equilibria](/correlated-equilibrium/). For approximate notions the payoffs are taken in $[0, 1]$.

**A small example.** Three players on the path $1 - 2 - 3$ each choose 0 or 1, and each player gets one unit for every neighbour whose action differs from its own. The profiles $(0, 1, 0)$ and $(1, 0, 1)$ are pure Nash equilibria: every player differs from all neighbours and gets the most it can. There are no other pure equilibria. In any other profile, some edge has two equal ends, and every edge of this path has an end player, 1 or 3, whose only neighbour is the other end; that player gains 1 by switching.

## Relation to other models

- **Normal-form games.** A graphical game is a normal-form game written compactly; the complete graph gives back the full table.
- **Graphical models.** The structure is the same as in a [Markov random field](/markov-random-field/), with local payoff tables in place of local potentials. The algorithm of Kearns, Littman and Singh for trees passes messages along the edges, like [belief propagation](/belief-propagation/), but its messages are best response tables, not probabilities.
- **Polymatrix games.** If each $u_i$ is a sum over the edges at $i$ of a two-player payoff, the game is a polymatrix game, and the input has only $O(|E| k^2)$ numbers.
- **Potential games.** If each edge carries a two-player game that gives both of its ends the same payoff, the sum of the edge payoffs is a potential, so the game is a [potential game](/potential-game/), and best response dynamics, with one player moving at a time, reach a pure equilibrium.
- **Other succinct games.** Congestion games and action-graph games are other compact forms of games with many players; the expected payoff in each is computable in polynomial time, which is what the general algorithms for correlated equilibria need.

## Known results in the model

- **Trees (Kearns, Littman and Singh 2001).** For two actions per player on a tree, a dynamic program sends a table from each node to its parent, from the leaves to the root. The table of the edge from $u$ to its parent $v$ says, for each mixed strategy of $v$, which mixed strategies of $u$ are best responses to it and to some consistent choice in the subtree below $u$. A pass from the root down then picks an equilibrium. With mixed strategies restricted to a fine grid, the program finds an $\varepsilon$-Nash equilibrium in time polynomial in $n$ and $1/\varepsilon$ when the degree is bounded. The exact version can represent all equilibria, but Elkind, Goldberg and Goldberg (2006) show that its tables can grow exponentially, even on trees of bounded degree.
- **Paths.** Elkind, Goldberg and Goldberg (2006) find an exact Nash equilibrium of a graphical game on a path, with two actions per player, in quadratic time.
- **Bounded degree in general.** Daskalakis, Goldberg and Papadimitriou (2009) reduce games with many players to graphical games of bounded degree with two actions per player, and this is a step of the proof that computing a Nash equilibrium is PPAD-complete. Finding a Nash equilibrium of a graphical game of degree 3 with two actions per player is PPAD-complete (Elkind, Goldberg and Goldberg 2006). These are hardness results for approximate equilibria in the sense of [PPAD](/ppad/), not unconditional lower bounds. See [Nash equilibrium computation](/nash-equilibrium-computation/).
- **Pure equilibria.** Deciding whether a graphical game has a pure Nash equilibrium is [NP-complete](/np-complete/) (Gottlob, Greco and Scarcello 2005). The problem becomes tractable when the graph is acyclic or has bounded treewidth, by dynamic programming over a [tree decomposition](/tree-decomposition/), as for constraint satisfaction.
- **Correlated equilibria.** A correlated equilibrium of the full game is a distribution over $k^n$ profiles, but for graphical games one can be found in time polynomial in the succinct input (Papadimitriou and Roughgarden, Journal of the ACM 55(3), 2008, by the ellipsoid against hope method; Jiang and Leyton-Brown 2015 made the output exact), because expected payoffs of product distributions are easy to compute.

## References
