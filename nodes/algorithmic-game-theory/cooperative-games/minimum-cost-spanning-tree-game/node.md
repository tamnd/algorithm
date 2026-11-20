---
tag: 7ATMRW
kind: model
slug: minimum-cost-spanning-tree-game
name: Minimum cost spanning tree game
aliases:
- MCST game
area: algorithmic-game-theory/cooperative-games
level: core
summary: A cost game in which players must connect to a source and each coalition pays the cost of a minimum spanning tree on its members and the source.
prereqs: [minimum-spanning-tree, transferable-utility-game, core-of-a-cooperative-game]
see_also: [bird-rule, prim, steiner-tree-problem, airport-game, shapley-value, nucleolus, cross-monotonicity, jain-vazirani-steiner-cost-sharing]
sources:
  - paper: "Charles G. Bird, On cost allocation for a spanning tree: a game theoretic approach, Networks 6(4) (1976), 335-350"
    title: On cost allocation for a spanning tree, a game theoretic approach
    locator: the definition of the game, the core allocation read from a minimum spanning tree, and the irreducible core
  - paper: "Ulrich Faigle, Walter Kern, Sandor P. Fekete and Winfried Hochstattler, On the complexity of testing membership in the core of min-cost spanning tree games, International Journal of Game Theory 26(3) (1997), 361-366"
    title: On the complexity of testing membership in the core of min-cost spanning tree games
    locator: deciding whether a given allocation is in the core is coNP-complete
  - paper: "Ulrich Faigle, Walter Kern and Jeroen Kuipers, Computing the nucleolus of min-cost spanning tree games is NP-hard, International Journal of Game Theory 27(3) (1998), 443-450"
    title: Computing the nucleolus of min-cost spanning tree games is NP-hard
    locator: the NP-hardness of the nucleolus
  - paper: "Gustavo Bergantinos and Juan J. Vidal-Puga, A fair rule in minimum cost spanning tree problems, Journal of Economic Theory 137(1) (2007), 326-352"
    title: A fair rule in minimum cost spanning tree problems
    locator: the folk rule, the Shapley value of the irreducible game, and its monotonicity properties
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 15 (Kamal Jain and Mohammad Mahdian, Cost Sharing), Section 15.2 on the core of cost-sharing games
---

The minimum cost spanning tree game is a cooperative cost game about a shared network. A set of players must each be connected to a common source, such as a power plant or a server, and the cost of a link between any two points is known. A coalition that acts alone builds the cheapest tree that joins its own members to the source, a [minimum spanning tree](/minimum-spanning-tree/). The question is how to divide the cost of the tree for all players. Bird (1976) defined the game and showed that its [core](/core-of-a-cooperative-game/) is never empty. The algorithm that finds a core allocation, by charging each player the edge that connects it in Prim's tree, is on the page [Bird's rule](/bird-rule/).

## The machine

There is a set $N = \{1, \ldots, n\}$ of players and a source, written 0. A symmetric cost $c(u, v) = c(v, u) \ge 0$ is given for each pair of distinct points of $N \cup \{0\}$. The game is the cost game $(N, C)$ in which a coalition $S \subseteq N$ has the cost

$$C(S) = \text{the cost of a minimum spanning tree of the complete graph on } S \cup \{0\},$$

with $C(\emptyset) = 0$. A coalition may use the source and its own members as connection points, but not the points of players outside it. An allocation is a vector $x \in \mathbb{R}^N$ with $x(N) = C(N)$, where $x(S) = \sum_{i \in S} x_i$. It is in the core if $x(S) \le C(S)$ for every $S$, so that no coalition pays more than it would pay to build its own network.

The input has size $\Theta(n^2)$: the cost matrix. The game itself has $2^n$ coalition costs, but each is computed on demand with [Prim's algorithm](/prim/) in $O(|S|^2)$ time. So the game has a compact representation, and questions about it are asked in terms of $n$, not $2^n$.

The same game can be written as a savings game. The value $v(S) = \sum_{i \in S} c(0, i) - C(S)$ is the amount that $S$ saves by building a shared tree instead of a direct link for each member. Core allocations of the two forms correspond through $y_i = c(0, i) - x_i$.

## What it counts

The cost $C(S)$ counts the cheapest way for $S$ to reach the source with its own points.

- **The total.** $C(N)$ is one minimum spanning tree, computed in $O(n^2)$ time with Prim's algorithm on the complete graph.
- **Subadditive.** If $S$ and $T$ are disjoint, the two trees share the source, and their union connects $S \cup T$. So $C(S \cup T) \le C(S) + C(T)$.
- **Not monotone.** A larger coalition can pay less. Let $c(0, 1) = c(0, 2) = c(1, 2) = 10$ and let player 3 be at cost 1 from all three other points. Then $C(\{1, 2\}) = 20$ but $C(\{1, 2, 3\}) = 3$, because player 3 is a cheap hub.
- **Not concave in general.** The cost function need not be submodular, and the [Shapley value](/shapley-value/) can be outside the core. With $c(0, 1) = c(0, 2) = c(1, 2) = 2$, $c(0, 3) = 6$, $c(1, 3) = 5$ and $c(2, 3) = 4$, the Shapley value is $(11/6, 4/3, 29/6)$ and the coalition $\{2, 3\}$ pays $37/6 > C(\{2, 3\}) = 6$.

A small example: with $c(0, 1) = 4$, $c(0, 2) = 5$, $c(0, 3) = 6$, $c(1, 2) = 2$, $c(1, 3) = 5$ and $c(2, 3) = 3$, the coalition costs are 4, 5 and 6 for the singletons, 6, 9 and 8 for $\{1, 2\}$, $\{1, 3\}$ and $\{2, 3\}$, and 9 for $N$. Bird's rule gives $(4, 2, 3)$, which is in the core.

## Relation to other models

- **Cost games and TU games.** The game is a cost version of a [transferable utility game](/transferable-utility-game/), and every subgame on a set $S$ is the game on the restricted cost matrix. Since every such game has a nonempty core, the game is totally balanced.
- **Airport game.** If the points lie on a line, with the source at 0 and player $i$ at $r_i > 0$, and $c(u, v) = |r_u - r_v|$, then $C(S) = \max_{i \in S} r_i$. This is the [airport game](/airport-game/), so airport games are a special case. Their cost is concave, and their Shapley value is in the core.
- **Steiner tree games.** If a coalition may also use the points of other players, or extra points that belong to nobody, its cost is the cost of a [Steiner tree](/steiner-tree-problem/). Then $C(S)$ is NP-hard to compute and the core can be empty. Cost sharing for this game uses approximate methods such as [Jain-Vazirani cost sharing](/jain-vazirani-steiner-cost-sharing/).
- **Directed costs.** If $c(u, v) \ne c(v, u)$, the cheapest structure is a [minimum arborescence](/minimum-arborescence/) rooted at the source, and the results on this page do not carry over directly.

## Known results in the model

- **The core is nonempty (Bird 1976).** Charging each player the cost of the edge that joins it to its parent in a minimum spanning tree rooted at the source gives a core allocation. The proof is on the page [Bird's rule](/bird-rule/). Bird also defined the irreducible game, in which each cost $c(u, v)$ is lowered to the smallest possible largest edge on a path from $u$ to $v$, and its core, the irreducible core.
- **Testing the core is hard.** Deciding whether a given vector is in the core is coNP-complete (Faigle, Kern, Fekete and Hochstattler 1997). The difficulty is the search over $2^n$ coalitions: a violated coalition is a certificate, and no short certificate is known for its absence.
- **The nucleolus is hard.** Computing the [nucleolus](/nucleolus/) is NP-hard (Faigle, Kern and Kuipers 1998).
- **Monotone rules.** Bird's rule is not population monotonic: a player can pay more after another player joins. The folk rule, the Shapley value of the irreducible game, is in the core and is both cost monotonic and population monotonic (Bergantinos and Vidal-Puga 2007). A population monotonic allocation gives a [cross-monotonic](/cross-monotonicity/) cost-sharing method, which is what a group strategyproof mechanism needs.
- **Cost sharing with private values.** If each player has a private value for being connected, the [Moulin mechanism](/moulin-mechanism/) with a cross-monotonic method decides who is connected and what each pays, without giving any group a reason to lie.

## References
