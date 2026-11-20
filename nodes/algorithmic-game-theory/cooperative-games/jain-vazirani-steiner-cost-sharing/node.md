---
tag: F0QV3E
kind: algorithm
slug: jain-vazirani-steiner-cost-sharing
name: Jain-Vazirani cost sharing for Steiner trees
aliases:
- primal-dual cost sharing for Steiner trees
area: algorithmic-game-theory/cooperative-games
level: research
summary: A cross-monotonic cost-sharing method for Steiner trees from a primal-dual algorithm. The shares pay for a spanning tree of the metric closure and are at most twice the optimal cost.
model: word-ram
complexity:
  vars: {N: the number of vertices of the graph, k: the number of terminals}
  time: {worst: O(N^3 + k^2 log k)}
  space: {extra: O(N^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2001
  people: [Kamal Jain, Vijay V. Vazirani]
  note: Jain and Vazirani derived cross-monotonic cost shares for Steiner trees from a primal-dual algorithm in 2001, which gives a group strategyproof mechanism through the Moulin mechanism.
prereqs: [moulin-mechanism, cross-monotonicity, steiner-tree-problem, kruskal]
see_also: [jain-vazirani-facility-location, goemans-williamson-steiner-forest, primal-dual-schema, minimum-arborescence, floyd-warshall, bird-rule, budget-balance, approximation-ratio]
sources:
  - paper: "Kamal Jain and Vijay V. Vazirani, Applications of approximation algorithms to cooperative games, Proceedings of the 33rd ACM Symposium on Theory of Computing (STOC 2001), 364-372"
    title: Applications of approximation algorithms to cooperative games
    locator: the cross-monotonic cost-sharing method for Steiner trees from a primal-dual algorithm, and the group strategyproof mechanism built on it
  - paper: "Jack Edmonds, Optimum branchings, Journal of Research of the National Bureau of Standards 71B(4) (1967), 233-240"
    title: Optimum branchings
    locator: minimum cost arborescences, the directed relaxation on which the dual growth is based
  - paper: doi:10.1145/1538902.1538907
    title: Quantifying inefficiency in cost-sharing mechanisms
    locator: Tim Roughgarden and Mukund Sundararajan, Journal of the ACM 56(4), Article 23, 2009, the O(log^2 k) social cost bound for the Jain-Vazirani mechanism and the matching lower bound for Moulin mechanisms for Steiner tree with constant budget balance
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 15 (Kamal Jain and Mohammad Mahdian, Cost Sharing), on cross-monotonic cost-sharing methods and the Moulin mechanism
---

Jain-Vazirani cost sharing splits the cost of a Steiner tree among the terminals that must be connected to a root. The cost of serving a set of terminals is the cost of an optimal [Steiner tree](/steiner-tree-problem/) for them, which is NP-hard to compute, so exact budget balance is out of reach. Jain and Vazirani (2001) took a primal-dual algorithm, in which the components of terminals grow a dual value over time, and charged each terminal its part of the dual of its component. The shares pay for a minimum spanning tree of the terminals and the root in the shortest path metric, so they cover a tree that serves the set and are at most twice the optimal cost. They are [cross-monotonic](/cross-monotonicity/): a terminal never pays more when more terminals join. Run inside the [Moulin mechanism](/moulin-mechanism/), they give a group strategyproof mechanism for multicast and network design.

## In plain words

A server must send a stream to some users through a network, and each link has a cost. The users who join must pay for the links. Think of a clock that runs from zero. At each moment, users who are close enough to each other form a group, and a group joins the server when it is close enough to it. Until its group reaches the server, each user pays a small amount for every tick of the clock, split equally inside the group. So a user in a big group pays less per tick, and a group near the server stops paying early. The total paid is enough to build a network that reaches all users, and at most twice the cheapest one. When more users join, groups form sooner and grow larger, so nobody pays more.

## The problem

The input is a connected undirected graph $G$ with $N$ vertices and nonnegative edge costs, a root $r$, and a set $S$ of $k$ terminals, the players. For a set $T \subseteq S$, the cost $C(T)$ is the cost of a cheapest connected subgraph of $G$ that contains $T \cup \{r\}$, the optimal Steiner tree. The output is a share $\xi(i, T)$ for each $T \subseteq S$ and each $i \in T$, computed for one given $T$ at a time. The goals are:

- **Cross-monotonicity.** $\xi(i, T) \ge \xi(i, T')$ whenever $i \in T \subseteq T'$.
- **Approximate budget balance.** $C(T) \le \sum_{i \in T} \xi(i, T) \le \beta\, C(T)$ for a small $\beta$.

This page uses the form of $\beta$-budget balance in which the shares cover the cost and are at most $\beta$ times it, and the method here has $\beta = 2$. Jain and Vazirani state the result in the other form, $\frac{1}{2} C(T) \le \sum_i \xi(i, T) \le C(T)$, which is the same method with all shares divided by 2. Exact budget balance would need $\sum_i \xi(i, T) = C(T)$, and computing $C(T)$ is NP-hard.

## The algorithm

```pseudo id=main
JV-SHARES(G, r, S)
L1  d ← shortest path costs of G between the points of P = S ∪ {r}
L2  E ← the pairs {u, v} of P, sorted by d(u, v)
L3  each point of P is its own component; ξ_i ← 0 for i ∈ S; t ← 0
L4  for each {u, v} in E with u and v in different components:
L5      for each component K without r: ξ_i ← ξ_i + (d(u, v) - t)/|K| for i ∈ K
L6      t ← d(u, v); merge the components of u and v
L7  return ξ
```

Line L1 builds the metric closure of $G$ on the terminals and the root, for example with [Floyd-Warshall](/floyd-warshall/). Lines L2 to L6 run [Kruskal's algorithm](/kruskal/) on the complete graph on $P$, and use the merge costs as a clock. Between two merges, the components do not change. Line L5 charges each component that has not reached the root for the time since the last merge, split equally among its members. Line L6 moves the clock and merges. Once all points are in the component of $r$, nothing more is charged. The tree that Kruskal's algorithm builds, with each closure edge replaced by a shortest path in $G$, is the network that the shares pay for.

This is the threshold form of the method. Jain and Vazirani describe it as a primal-dual algorithm on the bidirected graph on $P$, with the cut relaxation used by [Edmonds for arborescences](/minimum-arborescence/). Each component without $r$ is an active set that raises its dual at rate 1, and its terminals split the increase equally. An arc into an active component becomes tight when the dual of the component reaches its cost, which happens exactly when the pair enters the graph of pairs with $d(u, v) \le t$. The proof file shows that both views give the same shares.

## Example

The root is $r$ and the terminals are $a$, $b$ and $c$. One more vertex $s$ is not a terminal. The edges are $r s = 4$, $s a = 1$, $s b = 1$, $s c = 2$ and $r c = 5$. The metric closure on $P = \{r, a, b, c\}$ has $d(a, b) = 2$, $d(a, c) = d(b, c) = 3$ and $d(r, a) = d(r, b) = d(r, c) = 5$.

| time | components without $r$ | charge per unit of time | $\xi_a$, $\xi_b$, $\xi_c$ at the end |
|---|---|---|---|
| 0 to 2 | {a}, {b}, {c} | 1 each | 2, 2, 2 |
| 2 to 3 | {a, b}, {c} | 1/2, 1/2, 1 | 5/2, 5/2, 3 |
| 3 to 5 | {a, b, c} | 1/3 each | 19/6, 19/6, 11/3 |

At time 5 the component reaches $r$ and the charges stop. The shares are $(19/6, 19/6, 11/3)$, and they sum to 10, the cost of a minimum spanning tree on $P$ with the costs $d$: for example $ab$, $ac$ and $ra$ with costs 2, 3 and 5. With the shortest paths in $G$, this tree uses the edges $rs$, $sa$, $sb$ and $sc$, of total cost 8, which is also the optimal Steiner tree. So here the shares are 10, between the optimal cost 8 and twice it.

Cross-monotonicity shows in the shares of $a$ for the sets that contain it.

| set | shares | sum | optimal cost |
|---|---|---|---|
| {a} | 5 | 5 | 5 |
| {a, b} | 7/2, 7/2 | 7 | 6 |
| {a, c} | 4, 4 | 8 | 7 |
| {a, b, c} | 19/6, 19/6, 11/3 | 10 | 8 |

The share of $a$ falls from 5 to $7/2$ or 4, and then to $19/6$, as more terminals join.

## Correctness

The file proofs/correctness.md gives the full proofs. Let $G_t$ be the graph on $P$ with the pairs of cost at most $t$, and $K_t(i)$ the component of $i$ in it. Then the share of terminal $i$ is the integral over $t$ of $1/|K_t(i)|$, over the times at which $K_t(i)$ does not contain $r$.

- **The sum.** Each component without $r$ pays at total rate 1, so the sum of the shares is the integral of the number of components of $G_t$ minus 1. This is the sum of the Kruskal merge costs, the cost of a minimum spanning tree on $P$.
- **Budget.** A minimum spanning tree on $P$ maps to a connected subgraph of $G$ through shortest paths, so it costs at least the optimal Steiner tree. Doubling an optimal Steiner tree and shortcutting its Euler tour gives a spanning path of $P$ of cost at most twice the optimum, so the minimum spanning tree costs at most twice the optimum.
- **Cross-monotonicity.** Adding terminals does not change the metric. So $G_t$ for a smaller set is an induced subgraph of $G_t$ for a larger set, each component only grows, and each component reaches $r$ no later. The integrand, and so the share, can only fall.

## Complexity

Line L1 takes $O(N^3)$ time with Floyd-Warshall, or $k + 1$ runs of [Dijkstra's algorithm](/dijkstra/) on a sparse graph. Line L2 sorts $O(k^2)$ pairs in $O(k^2 \log k)$ time. There are $k$ merges, and each runs line L5 in $O(k)$ time, so lines L3 to L6 take $O(k^2)$ time. The total is $O(N^3 + k^2 \log k)$ time with $O(N^2)$ space for the metric. When the method runs inside the Moulin mechanism, the metric is computed once, and each round costs $O(k^2 \log k)$, so the mechanism takes $O(N^3 + k^3 \log k)$ time.

## Properties

- **Cross-monotonic**, so the Moulin mechanism built on it is group strategyproof, with no positive transfers, voluntary participation and consumer sovereignty.
- **2-budget balanced** with respect to the optimal Steiner tree cost, and exactly budget balanced for the minimum spanning tree on $P$ that the mechanism builds.
- **Deterministic and exact.** With rational costs the shares are rational. Ties among pair costs do not change the shares, because they give intervals of length zero.
- **Symmetric inside a component.** Terminals in the same component at all times pay the same.
- **Not efficient.** Roughgarden and Sundararajan (2009) showed that the Moulin mechanism with these shares has social cost within a factor $O(\log^2 k)$ of the optimum, and that every Moulin mechanism for Steiner tree with constant budget balance has social cost $\Omega(\log^2 k)$ times the optimum on some inputs.

## Variants and improvements

- **Spanning tree games.** In a [minimum cost spanning tree game](/minimum-cost-spanning-tree-game/) whose costs already satisfy the triangle inequality, the metric closure changes no cost. Then the shares of a coalition sum to exactly its minimum spanning tree cost, and they never rise when a player joins, which [Bird's rule](/bird-rule/) does not guarantee. Without the triangle inequality, a coalition in the closure may route through other players' vertices, and the shares are budget balanced only for the closure.
- **Steiner forest.** For pairs of terminals that must be connected, without a common root, the [Goemans-Williamson](/goemans-williamson-steiner-forest/) primal-dual algorithm is a 2-approximation. Its natural shares are not cross-monotonic. Könemann, Leonardi, Schäfer and van Zwam (2008) gave a group strategyproof mechanism for Steiner forest with a constant budget balance factor, based on a stronger relaxation.
- **Facility location.** The facility location algorithm of [Jain and Vazirani](/jain-vazirani-facility-location/) is a different primal-dual algorithm by the same authors, for a different problem. Later work turned primal-dual algorithms for facility location into cross-monotonic methods as well.
- **Halved shares.** Dividing every share by 2 gives the form used by Jain and Vazirani: the shares never exceed the optimal cost, so no set of terminals is overcharged, and they recover at least half the cost of the tree that is built.

## When to use it

Use these shares when a network with a root, such as a multicast tree, is offered to users with private values, the users must pay for the network, and the mechanism must resist collusion. The Moulin mechanism with these shares is group strategyproof and covers the cost of the tree it builds. Use the spanning tree on the metric closure as the network, or prune it to a cheaper Steiner tree and accept a surplus. Do not use it when the operator needs exact budget balance for the optimal tree, which is impossible in polynomial time unless P = NP, or when the efficiency loss of a factor $\log^2 k$ is too large.

## Pitfalls

- **Charging the edges of $G$ instead of the closure.** The method works on the shortest path metric between terminals and the root. Steiner vertices are not players and pay nothing. Running the clock on the edges of $G$ itself would charge for edges that the tree does not need.
- **Two forms of budget balance.** The shares here cover the cost of the spanning tree on $P$ and are at most twice the optimum. Papers that use the other form divide them by 2. Mixing the two forms changes every stated factor by 2.
- **Overcharging the built network.** In the example, the shares sum to 10, but the network in $G$ that the spanning tree maps to costs only 8. A mechanism that builds the pruned network collects a surplus. This does not break group strategyproofness.
- **Shares that depend on the order of ties.** The shares do not depend on how ties among pair costs are broken, but the tree does. Do not report the tree as unique.
- **Inexact arithmetic.** The Moulin mechanism compares bids with shares. Shares with denominators such as $1/6$ cannot be stored exactly in floating point. Use rationals.

## Implementations

## History

Moulin (1999) showed that a cross-monotonic cost-sharing method gives a group strategyproof mechanism, and Feigenbaum, Papadimitriou and Shenker (2001) studied the cost of multicast transmissions over a fixed tree from the point of view of computation. For Steiner trees exact budget balance is NP-hard, so Jain and Vazirani (2001) gave a cross-monotonic method with a budget balance factor of 2, read off from the dual of a primal-dual algorithm on the directed relaxation of Edmonds (1967). The paper started a line of work that turned primal-dual approximation algorithms into cost-sharing methods, for facility location, Steiner forest and other problems. Roughgarden and Sundararajan (2009) later measured the efficiency loss of these mechanisms and showed that the factor $O(\log^2 k)$ is the best possible for Moulin mechanisms for Steiner tree with constant budget balance.

## References
