---
tag: 7MY1TF
kind: algorithm
slug: bird-rule
name: Bird's rule
aliases:
- Bird allocation
area: algorithmic-game-theory/cooperative-games
level: core
summary: Charges each player the cost of the edge by which Prim's algorithm connects it to the source. The charges add up to the MST cost and lie in the core of the spanning tree game.
model: word-ram
complexity:
  vars: {n: the number of players}
  time: {worst: O(n^2)}
  space: {extra: O(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1976
  people: [Charles G. Bird]
  note: Bird introduced the minimum cost spanning tree game in 1976 and showed that the allocation read from a minimum spanning tree is in its core.
prereqs: [minimum-cost-spanning-tree-game, prim, core-of-a-cooperative-game]
see_also: [minimum-spanning-tree, kruskal, cycle-property, hall-theorem, shapley-value, cross-monotonicity, airport-game, nucleolus]
sources:
  - paper: "Charles G. Bird, On cost allocation for a spanning tree: a game theoretic approach, Networks 6(4) (1976), 335-350"
    title: On cost allocation for a spanning tree, a game theoretic approach
    locator: the minimum cost spanning tree game, the allocation that charges each player the edge that connects it in a minimum spanning tree, the proof that it is in the core, and the irreducible core
  - paper: "Gustavo Bergantinos and Juan J. Vidal-Puga, A fair rule in minimum cost spanning tree problems, Journal of Economic Theory 137(1) (2007), 326-352"
    title: A fair rule in minimum cost spanning tree problems
    locator: the folk rule, its characterization by cost monotonicity, population monotonicity and equal share of extra costs, and its relation to Bird's rule and the irreducible game
  - paper: "Ulrich Faigle, Walter Kern, Sandor P. Fekete and Winfried Hochstattler, On the complexity of testing membership in the core of min-cost spanning tree games, International Journal of Game Theory 26(3) (1997), 361-366"
    title: On the complexity of testing membership in the core of min-cost spanning tree games
    locator: deciding whether a given allocation is in the core is coNP-complete
  - paper: "Ulrich Faigle, Walter Kern and Jeroen Kuipers, Computing the nucleolus of min-cost spanning tree games is NP-hard, International Journal of Game Theory 27(3) (1998), 443-450"
    title: Computing the nucleolus of min-cost spanning tree games is NP-hard
    locator: the NP-hardness of the nucleolus of the game
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 15 (Kamal Jain and Mohammad Mahdian, Cost Sharing), Section 15.2 on the core of cost-sharing games
---

Bird's rule divides the cost of a network among the users who must connect to a common source. It builds a [minimum spanning tree](/minimum-spanning-tree/) from the source with [Prim's algorithm](/prim/) and charges each player the cost of the edge by which the tree reaches it. The charges add up to the cost of the tree, and no group of players pays more than it would pay to build its own network. In the language of cooperative games, the allocation is in the [core](/core-of-a-cooperative-game/) of the [minimum cost spanning tree game](/minimum-cost-spanning-tree-game/). Bird gave the rule and the core result in 1976. This page is the rule as an algorithm, with a full proof; the game itself, its other solutions and its complexity results are on the model page.

## In plain words

Several houses must be connected to a power plant. Any two points can be joined by a cable with a known price. The cheapest network that reaches every house is a minimum spanning tree. Build it outward from the plant, one house at a time, always adding the cheapest cable that reaches a new house. Each house pays for the cable that brought the network to it. The payments cover the whole network. No group of houses can complain that it could build its own network to the plant for less than it pays now. The rule is quick to compute and easy to explain, but a house can pay more after a new house joins, so it is not stable under growth.

## The problem

The input is a symmetric cost $c(u, v) = c(v, u)$ for each pair of vertices of $V = N \cup \{0\}$, where vertex 0 is the source and $N = \{1, \ldots, n\}$ are the players. The game is a cost game: for a coalition $S \subseteq N$, the cost $c(S)$ is the cost of a minimum spanning tree of the complete graph on $S \cup \{0\}$. A coalition may use only its own vertices and the source. The output is an allocation $x \in \mathbb{R}^N$ that splits the total cost, $x(N) = c(N)$, where $x(S) = \sum_{i \in S} x_i$. The goal is a core allocation: $x(S) \le c(S)$ for every coalition $S$, so that no coalition pays more than its stand-alone cost.

The core of a general cost game can be empty, and testing whether a given vector is in the core of this game is coNP-complete (Faigle, Kern, Fekete and Hochstattler 1997). Bird's rule avoids the test: it outputs a vector that is always in the core, in $O(n^2)$ time.

## The algorithm

```pseudo id=main
BIRD(c)
L1  for v ← 1 to n: d[v] ← c(0, v); p[v] ← 0
L2  T ← {0}
L3  repeat n times:
L4      v ← the vertex outside T with the smallest d[v] (smallest index on ties)
L5      x_v ← d[v]; T ← T ∪ {v}
L6      for each w outside T: if c(v, w) < d[w]: d[w] ← c(v, w); p[w] ← v
L7  return x, p
```

The procedure is Prim's algorithm on the complete graph, started at the source. The array $d$ holds, for each vertex $w$ that is not yet in the tree, the cost of the cheapest edge from the tree to $w$, and $p[w]$ is the tree end of that edge. Line L1 starts with the edges from the source. Line L4 takes the vertex that is cheapest to reach, and line L5 charges it exactly that cost. Line L6 lowers $d[w]$ when the new vertex $v$ is a cheaper way to reach $w$. When the loop ends, the parent pointers $p$ describe the tree, and player $v$ pays $x_v = c(p[v], v)$, the cost of the edge that joins $v$ to its parent.

## Example

The source is 0 and the players are 1, 2 and 3, with the costs

| | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 0 | 0 | 4 | 5 | 6 |
| 1 | 4 | 0 | 2 | 5 |
| 2 | 5 | 2 | 0 | 3 |
| 3 | 6 | 5 | 3 | 0 |

The trace shows $d$ and $p$ after each step.

| step | vertex added | charge | $d[1], d[2], d[3]$ after line L6 | $p[1], p[2], p[3]$ |
|---|---|---|---|---|
| L1 | none | none | 4, 5, 6 | 0, 0, 0 |
| 1 | 1 | $x_1 = 4$ | done, 2, 5 | 0, 1, 1 |
| 2 | 2 | $x_2 = 2$ | done, done, 3 | 0, 1, 2 |
| 3 | 3 | $x_3 = 3$ | done, done, done | 0, 1, 2 |

The tree is the path $0 - 1 - 2 - 3$ with cost $4 + 2 + 3 = 9 = c(N)$, and Bird's rule gives $x = (4, 2, 3)$. The table checks every core inequality.

| coalition $S$ | $c(S)$ | $x(S)$ |
|---|---|---|
| {1} | 4 | 4 |
| {2} | 5 | 2 |
| {3} | 6 | 3 |
| {1, 2} | 6 | 6 |
| {1, 3} | 9 | 7 |
| {2, 3} | 8 | 5 |
| {1, 2, 3} | 9 | 9 |

Player 1 pays its full stand-alone cost, because the tree reaches it first by its own direct edge. Players 2 and 3 pay much less than alone, because they use the edges through player 1. The [Shapley value](/shapley-value/) of the same game is $(7/3, 7/3, 13/3)$: it charges player 1 less and player 3 more, and here it is also in the core.

## Correctness

The file proofs/correctness.md gives the full proof. The charges add up to $c(N)$ because lines L1 to L6 are Prim's algorithm, so the tree $T$ of the parent edges is a minimum spanning tree and each of its edges is charged once.

For the core inequality, fix a coalition $S$ and a minimum spanning tree $T_S$ on $S \cup \{0\}$. The proof matches each player $v \in S$ with its own edge of $T_S$ that costs at least $x_v$. An edge $(a, b)$ of $T_S$ can be matched with $v$ when the parent edge of $v$ is on the path from $a$ to $b$ in $T$. Then $x_v \le c(a, b)$ by the [cycle property](/cycle-property/) of minimum spanning trees: otherwise $T$ minus the parent edge of $v$ plus $(a, b)$ would be a cheaper spanning tree. For any set $W \subseteq S$, removing the parent edges of $W$ cuts $T$ into $|W| + 1$ parts, and each part contains a vertex of $S \cup \{0\}$. The tree $T_S$ must cross between these parts at least $|W|$ times, and each crossing edge can be matched with some player of $W$. So [Hall's condition](/hall-theorem/) holds, a perfect matching exists, and $x(S) \le c(T_S) = c(S)$.

The proof uses only that $T$ is a minimum spanning tree. So the allocation read from any minimum spanning tree is in the core, also when ties make the tree not unique.

## Complexity

The loop of line L3 runs $n$ times. Lines L4 and L6 each scan at most $n$ vertices, so the time is $O(n^2)$ in the word RAM model with costs that fit in a word. The input is a complete cost matrix with $\Theta(n^2)$ entries, so no algorithm can do better in general. The extra space is $O(n)$ for $d$, $p$, $x$ and the tree flags. On a sparse input graph with $m$ edges, where the missing edges have infinite cost, Prim's algorithm with a binary heap gives the same allocation in $O(m \log n)$ time.

## Properties

- **Efficient.** The charges add up to exactly $c(N)$, the cost of the cheapest network.
- **In the core.** No coalition pays more than its stand-alone cost, as proved above. Since every subgame of a minimum cost spanning tree game is again such a game, Bird's rule also shows that every subgame has a nonempty core: the game is totally balanced.
- **Not unique.** With ties, different minimum spanning trees give different allocations. The code breaks ties by the smallest index.
- **Not population monotonic.** With $c(0, 1) = 8$, $c(0, 2) = 9$, $c(0, 3) = 7$, $c(1, 2) = 1$, $c(1, 3) = 8$ and $c(2, 3) = 4$, the game on players 1 and 2 gives $x = (8, 1)$. When player 3 joins, the tree is $0 - 3 - 2 - 1$, and the charges are $(1, 4, 7)$. Player 2 pays 4 instead of 1, although the new player only adds options. So Bird's rule is not [cross-monotonic](/cross-monotonicity/), and it cannot be used in a [Moulin mechanism](/moulin-mechanism/).

## Variants and improvements

- **Shapley value.** The [Shapley value](/shapley-value/) of the game is symmetric and additive, but it needs the costs of exponentially many coalitions, and it can be outside the core. With $c(0, 1) = 2$, $c(0, 2) = 2$, $c(0, 3) = 6$, $c(1, 2) = 2$, $c(1, 3) = 5$ and $c(2, 3) = 4$, the Shapley value is $(11/6, 4/3, 29/6)$, and the coalition $\{2, 3\}$ pays $37/6 > c(\{2, 3\}) = 6$.
- **Folk rule.** Bergantinos and Vidal-Puga (2007) studied a rule that is the Shapley value of the irreducible game, where each cost $c(u, v)$ is replaced by the smallest possible largest edge cost on a path from $u$ to $v$. It is in the core, it is cost monotonic, and it is population monotonic, which Bird's rule is not.
- **Nucleolus.** The [nucleolus](/nucleolus/) of the game is in the core and is unique, but computing it is NP-hard for this game (Faigle, Kern and Kuipers 1998).
- **Steiner networks.** If a coalition may also route through the vertices of other players, the game becomes a Steiner tree game. Cost sharing for Steiner trees needs other methods, such as [Jain-Vazirani cost sharing](/jain-vazirani-steiner-cost-sharing/), which recovers only part of the cost.

## When to use it

Use Bird's rule when a fixed group of users shares the cost of a tree network to a source and the allocation must be in the core: no group of users should be able to leave and build its own network for less. It is a good default when the users and the costs are known and do not change, because it needs only one run of Prim's algorithm. Do not use it when users join and leave over time and each user must never pay more after a new user joins; use the folk rule or another population monotonic rule. Do not use it in a mechanism that asks users for their values, because without cross-monotonicity the Moulin mechanism built on it is not strategyproof.

## Pitfalls

- **Coalitions that use other players' vertices.** The core result is for the game in which a coalition builds a tree on its own vertices and the source. If a coalition may route through outside vertices, its cost can be lower, and the core inequalities change.
- **Asymmetric costs.** The proof uses $c(u, v) = c(v, u)$. With directed costs the right structure is a [minimum arborescence](/minimum-arborescence/), and the proof does not apply. The code rejects an asymmetric matrix.
- **A tree that is not minimum.** Charging the edges of any spanning tree adds up to that tree's cost, which can exceed $c(N)$. The proof needs a minimum spanning tree.
- **Charging the wrong end of an edge.** Each player pays the edge toward the source, its parent edge in the tree rooted at 0. If Prim's algorithm starts at a player, the order in which vertices enter changes, and the edge charged to a vertex may be an edge away from the source. Orient the tree from the source before charging.
- **Using the rule in a mechanism.** The Moulin mechanism needs cross-monotonic shares. With Bird's shares and the costs of the population monotonicity example, a player with value 2 that bids 4 when players 1 and 3 bid their values 8 and 0 is served at price 1 and gains, while the truthful bid leaves it unserved.

## Implementations

## History

Bird (1976) formulated cost allocation for a spanning tree as a cooperative game. He showed that the allocation that charges each player the edge connecting it in a minimum spanning tree is in the core, and he introduced the irreducible core, the core of the game in which every cost is lowered as far as possible without changing the cost of the minimum spanning tree. Later work studied the complexity of the core and the nucleolus of the game (Faigle and coauthors, 1997 and 1998) and rules with stronger monotonicity properties, such as the folk rule of Bergantinos and Vidal-Puga (2007).

## References
