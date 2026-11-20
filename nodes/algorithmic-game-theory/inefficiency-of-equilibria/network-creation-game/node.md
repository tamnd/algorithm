---
tag: H8E896
kind: model
slug: network-creation-game
name: Network creation game
aliases:
- Fabrikant network creation game
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: Players buy edges at a fixed price each and pay for their distances to all other players. Its equilibria and price of anarchy are studied.
prereqs: [pure-nash-equilibrium, price-of-anarchy, breadth-first-search]
see_also: [shapley-network-design-game, price-of-stability, best-response, spanning-tree, complete-graph, dominating-set, potential-game, all-pairs-shortest-paths]
sources:
  - paper: "Alex Fabrikant, Ankur Luthra, Elitza Maneva, Christos H. Papadimitriou and Scott Shenker, On a network creation game, PODC 2003"
    locator: "the model, the social optimum, the bound O(sqrt(alpha)) on the price of anarchy, the hardness of a best response, and the tree conjecture"
  - paper: "Susanne Albers, Stefan Eilts, Eyal Even-Dar, Yishay Mansour and Liam Roditty, On Nash equilibria for a network creation game, SODA 2006; ACM Transactions on Economics and Computation 2(1) (2014)"
    locator: "constant price of anarchy for small alpha and for alpha at least 12 n log n, and equilibria that are not trees"
  - paper: "Erik D. Demaine, MohammadTaghi Hajiaghayi, Hamid Mahini and Morteza Zadimoghaddam, The price of anarchy in network creation games, PODC 2007; ACM Transactions on Algorithms 8(2) (2012)"
    locator: "constant price of anarchy for alpha = O(n^(1 - epsilon)), the general bound 2^O(sqrt(log n)), and the MAX version"
  - paper: doi:10.4230/LIPIcs.STACS.2024.28
    title: "Jack Dippel and Adrian Vetta, One n remains to settle the tree conjecture, STACS 2024, LIPIcs 289"
    locator: "every equilibrium is a tree for alpha > 2n, and the history of the bounds before it"
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: "Chapter 19, Eva Tardos and Tom Wexler, Network formation games and the potential function method"
---

The network creation game of Fabrikant, Luthra, Maneva, Papadimitriou and Shenker (2003) models a network that selfish nodes build. Each node buys links to other nodes at a fixed price per link, and it wants to be close to everyone else. The question is how far the networks that the nodes build on their own are from the best network. In the close [Shapley network design game](/shapley-network-design-game/) players share the cost of the edges on their own paths; here each player pays alone for the edges it buys and pays for its distances.

## The machine

**Players and strategies.** There are $n$ players, which are the nodes $1, \dots, n$, and an edge price $\alpha > 0$. Player $i$ chooses a set $s_i \subseteq \{1, \dots, n\} \setminus \{i\}$ of nodes and buys the edges $\{i, j\}$ for $j \in s_i$. The strategy profile $s = (s_1, \dots, s_n)$ gives the undirected graph $G(s)$ with all the bought edges. Who bought an edge does not matter for its use: both ends can use it.

**Costs.** This is a cost game. The cost of player $i$ is

$$c_i(s) = \alpha\, |s_i| + \sum_{j = 1}^{n} d_{G(s)}(i, j),$$

where $d_{G(s)}(i, j)$ is the number of edges on a shortest path from $i$ to $j$, and the cost is $\infty$ if $G(s)$ is not connected. A [breadth-first search](/breadth-first-search/) from $i$ computes the sum of distances in $O(n + |E|)$ time.

**Equilibrium notion.** The game is studied with [pure Nash equilibria](/pure-nash-equilibrium/): no player can lower its cost by a change of its whole set $s_i$, which may drop, keep and add edges at once. A pure equilibrium exists for every $\alpha$ (below). A mixed best response has its support inside the set of pure best responses, but mixed equilibria are not the object of study in this model.

**Social cost.** The social cost is the sum of the player costs,

$$C(s) = \alpha\, |E(G(s))| + \sum_{i} \sum_{j} d_{G(s)}(i, j),$$

when no edge is bought twice. In an equilibrium no edge is bought twice, because one of its two buyers could drop it and keep all distances.

## What it counts

- The [price of anarchy](/price-of-anarchy/): the largest ratio $C(s)/C(s^*)$ over equilibria $s$ and an optimal graph $s^*$, as a function of $n$ and $\alpha$.
- The [price of stability](/price-of-stability/), for the best equilibrium.
- The shape of equilibrium graphs, above all whether they are trees, and their diameter.
- The time to compute a [best response](/best-response/).

## Relation to other models

- **Shapley network design.** In the [Shapley network design game](/shapley-network-design-game/) the players share the cost of the edges they use and each player has one source and one sink. That game is a [potential game](/potential-game/). The network creation game has no such cost sharing, and its interest is the tradeoff between edge cost and distance.
- **Network formation in economics.** Jackson and Wolinsky (1996) studied link formation in which both ends must agree to a link; Corbo and Parkes (2005) studied this bilateral version of the network creation game. In the model here, one player buys an edge alone.
- **Variants.** In the MAX version the distance term is the largest distance $\max_j d(i, j)$ instead of the sum (Demaine et al.). In the basic or swap game of Alon, Demaine, Hajiaghayi and Leighton (2010) there is no edge price, and a player may only swap one of its edges for another.

## Known results in the model

Each item is a theorem unless it is marked as an open problem.

**Social optimum.** For $\alpha \le 2$ the complete graph $K_n$ is optimal, and for $\alpha \ge 2$ the star is optimal. Proof: let a connected graph have $k$ edges. Each of the $2k$ ordered pairs at the ends of an edge has distance 1, and each of the other $n(n - 1) - 2k$ ordered pairs has distance at least 2. So

$$C \ge \alpha k + 2k + 2\,(n(n - 1) - 2k) = (\alpha - 2)\, k + 2n(n - 1).$$

If $\alpha \le 2$, the right side is smallest at the largest $k = n(n - 1)/2$, and $K_n$ meets it with equality. If $\alpha \ge 2$, it is smallest at the smallest $k = n - 1$, and the star meets it with equality because its diameter is 2. The costs are $\alpha n(n - 1)/2 + n(n - 1)$ for $K_n$ and $\alpha(n - 1) + 2(n - 1)^2$ for the star.

**Existence of pure equilibria.** For $\alpha < 1$, $K_n$ is the only equilibrium graph: if $i$ and $j$ are not adjacent, $d(i, j) \ge 2$, and $i$ lowers its cost by at least $1 - \alpha > 0$ if it buys $\{i, j\}$. For $\alpha \ge 1$, the star in which the center buys all edges is an equilibrium: the center cannot drop an edge, and a leaf that buys $k$ edges to other leaves pays $k\alpha$ and saves only $k$ in distance. For $\alpha = 1$ both graphs are equilibria.

**Small edge prices.** For $\alpha < 1$ the price of anarchy is 1. For $1 \le \alpha < 2$ it is at most $4/3$ (Fabrikant et al.): every equilibrium has diameter at most 2, and the star against $K_n$ gives the ratio $(2n - 1)/(1.5\, n)$ at $\alpha = 1$, which tends to $4/3$.

**General bounds on the price of anarchy.**

| range of $\alpha$ | price of anarchy | source |
|---|---|---|
| all $\alpha$ | $O(\sqrt{\alpha})$ | Fabrikant et al. 2003 |
| equilibria that are trees | at most 5 | Fabrikant et al. 2003 |
| $\alpha = O(\sqrt{n})$ or $\alpha \ge 12 n \log n$ | $O(1)$ | Albers et al. 2006 |
| $\alpha = O(n^{1 - \varepsilon})$ for a fixed $\varepsilon > 0$ | $O(1)$ | Demaine et al. 2007 |
| all $\alpha$ | $2^{O(\sqrt{\log n})}$ | Demaine et al. 2007 |
| $\alpha > n (1 + \varepsilon)$ for a fixed $\varepsilon > 0$ | $O(1)$ | Alvarez and Messegue 2019 |

**The tree conjecture.** Fabrikant et al. conjectured that every equilibrium graph is a tree when $\alpha$ is larger than a constant. Albers et al. disproved this form: there are equilibria with cycles for values of $\alpha$ that grow with $n$. The revised conjecture is that every equilibrium is a tree for $\alpha > n$. Since the price of anarchy of tree equilibria is at most 5, each result of the form "every equilibrium is a tree for $\alpha > c\, n$" gives a constant price of anarchy in that range. The constant $c$ came down over time: $12 \log n$ (Albers et al. 2006), 273 (Mihalak and Schlegel 2010), 65, 17, then $4 - 13/n$ (Bilo and Lenzner 2018), $3 - 3/n$ (Dippel and Vetta 2022) and 2 (Dippel and Vetta, STACS 2024).

**Open problem (Dippel and Vetta, 2024).** Is every equilibrium a tree for $\alpha$ between about $n$ and $2n$? This is the only range left for the tree conjecture.

**Open problem (Demaine et al., 2007; still open in the 2024 literature).** Is the price of anarchy bounded by a constant for every $\alpha$? The gap is the range from $n^{1 - \varepsilon}$ to about $n$, where the best general bound is $2^{O(\sqrt{\log n})}$.

**Computing a best response is NP-hard** (Fabrikant et al. 2003). A player must choose a set of nodes to link to so that the others are close, which is a problem of the kind of [dominating set](/dominating-set/). So it is also hard in general to decide whether a player can improve, that is, to check that a profile is an equilibrium. For small $n$, as in the example below, a search over all sets is easy.

### Example

Take $n = 4$ and $\alpha = 3$. Since $\alpha \ge 2$, the star is optimal, with cost $3 \cdot 3 + 2 \cdot 3^2 = 27$.

Now take the path $a - b - c - d$ in which $b$ buys $\{a, b\}$ and $\{b, c\}$, and $c$ buys $\{c, d\}$.

| player | edges bought | sum of distances | cost |
|---|---|---|---|
| $a$ | 0 | $1 + 2 + 3 = 6$ | 6 |
| $b$ | 2 | $1 + 1 + 2 = 4$ | 10 |
| $c$ | 1 | $1 + 1 + 2 = 4$ | 7 |
| $d$ | 0 | 6 | 6 |

The social cost is 29. To check that this is an equilibrium, look at each player:

- $a$ could buy an edge to $c$ or $d$. Its distances would sum to 4, so it would pay $3 + 4 = 7 > 6$. Two or more edges cost at least 6 plus 3 in distance.
- $d$ is the same as $a$ by symmetry.
- $b$ cannot drop an edge, since the graph would split. It could swap $\{b, c\}$ for $\{b, d\}$, but its distances still sum to 4. A third edge costs 3 and saves only 1.
- $c$ cannot drop $\{c, d\}$, and a new edge to $a$ costs 3 and saves 1.

So the path is an equilibrium, and the ratio is $29/27$. A brute-force search over all $(2^3)^4 = 4096$ profiles for $n = 4$ confirms that $29/27$ is the worst ratio for $\alpha = 3$. For $\alpha = 3/2$, the 4-cycle in which each node buys the edge to the next node is an equilibrium of cost $6 + 16 = 22$, against the optimum $K_4$ of cost $9 + 12 = 21$.

## References
