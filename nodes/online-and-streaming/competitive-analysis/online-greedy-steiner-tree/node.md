---
tag: HET07A
kind: algorithm
slug: online-greedy-steiner-tree
name: Online greedy Steiner tree
aliases:
- greedy connection heuristic
- greedy online Steiner tree
- online greedy Steiner algorithm
area: online-and-streaming/competitive-analysis
level: advanced
summary: Connects each new terminal to the nearest point of the current tree; O(log k) competitive.
solves: [online-steiner-tree-problem]
model: word-ram
complexity:
  vars: {k: the number of terminals, n: the number of vertices, e: the number of edges}
  time: {worst: O(k (n + e) log n)}
  space: {extra: O(n + e)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1991
  people: [Makoto Imase, Bernard M. Waxman]
  note: Imase and Waxman proved in 1991 that the greedy rule is O(log k)-competitive for the online Steiner tree problem, and that no online algorithm does better than Omega(log k).
prereqs: [online-steiner-tree-problem, steiner-tree-problem, dijkstra, competitive-ratio, harmonic-series]
see_also: [prim, kou-markowsky-berman, nearest-neighbor-tsp, online-minimum-spanning-tree-problem, steiner-forest, online-facility-location-problem]
sources:
  - paper: "Makoto Imase and Bernard M. Waxman, Dynamic Steiner tree problem, SIAM Journal on Discrete Mathematics 4(3) (1991), 369-384"
    title: "Imase and Waxman, Dynamic Steiner tree problem (1991)"
    locator: the greedy algorithm for terminal arrivals, its O(log k) upper bound, the lower bound for every online algorithm, and the version with deletions and rearrangements
  - paper: "Noga Alon and Yossi Azar, On-line Steiner trees in the Euclidean plane, Discrete and Computational Geometry 10 (1993), 113-121"
    title: "Alon and Azar, On-line Steiner trees in the Euclidean plane (1993)"
    locator: the analysis of the greedy rule by the sorted connection costs, and the lower bound Omega(log k / log log k) for points in the plane
  - paper: "Piotr Berman and Chris Coulston, On-line algorithms for Steiner tree problems, STOC 1997"
    title: "Berman and Coulston, On-line algorithms for Steiner tree problems (1997)"
    locator: the O(log k)-competitive algorithm for the online generalized Steiner problem, and the analysis of greedy rules
  - paper: "Nicole Megow, Martin Skutella, Jose Verschae and Andreas Wiese, The power of recourse for online MST and TSP, SIAM Journal on Computing 45(3) (2016), 859-880"
    title: "Megow, Skutella, Verschae and Wiese, The power of recourse for online MST and TSP (2016)"
    locator: the Theta(log k) bound for greedy without recourse, and the near-optimal trees with a bounded number of edge swaps
---

The online greedy Steiner tree algorithm builds a tree that connects terminals that arrive one at a time in a weighted graph. When a new terminal arrives, it buys a shortest path from the terminal to the nearest vertex of the tree it has built, and it never removes an edge. Imase and Waxman proved in 1991 that it costs at most $O(\log k)$ times the optimal [Steiner tree](/steiner-tree-problem/) on the first $k$ terminals, and that no online algorithm can do better than $\Omega(\log k)$. So the simplest rule is optimal up to a constant factor for the [online Steiner tree problem](/online-steiner-tree-problem/).

## In plain words

A town builds a water network one house at a time. When a new house is added, the town lays the shortest pipe from the house to the nearest point of the network that already exists. It never digs up old pipes.

This can waste pipe. An early pipe can take a long detour that a planner with the full list of houses would have avoided. But the waste is limited. Only a few new houses can be far from all the others, and most houses are close to some earlier house. If the town connects many houses, the total pipe is at most a small multiple of the best network, and the multiple grows only like the number of digits of the number of houses.

## The problem

An undirected graph $G = (V, E)$ with $n$ vertices, $e$ edges and nonnegative edge weights $w$ is known in advance. Terminals $t_1, t_2, \ldots, t_k$ arrive one at a time. After terminal $t_i$ arrives, the algorithm must buy edges so that the bought edges connect $t_1, \ldots, t_i$. Bought edges stay bought. The cost $\mathrm{ALG}(\sigma)$ is the total weight of the bought edges, and $\mathrm{OPT}(\sigma)$ is the weight of a minimum Steiner tree for the set $\{t_1, \ldots, t_k\}$. The request sequence is $\sigma = t_1, \ldots, t_k$, and $d$ is the shortest path metric of $G$. The [online Steiner tree problem](/online-steiner-tree-problem/) page gives the model and its variants.

## The algorithm

```pseudo id=main
ONLINE-GREEDY-STEINER(G, w, σ)
L1  T ← the empty tree
L2  cost ← 0
L3  for each terminal t of σ, in the order of arrival do
L4      if T is empty or t is a vertex of T then add t to T and continue
L5      P ← a shortest path in G from t to the nearest vertex of T
L6      add the vertices and edges of P to T
L7      cost ← cost + w(P)
L8  return T, cost
```

Line L5 is one run of [Dijkstra's algorithm](/dijkstra/) from $t$ that stops at the first vertex of $T$ it settles. That vertex may be a terminal or a Steiner vertex that an earlier path passed through. Line L6 keeps $T$ a tree: $P$ meets $T$ only at its last vertex.

A common variant, used in metric spaces, connects $t_i$ to the nearest earlier terminal instead of the nearest vertex of the tree. Its step cost is $\min_{j < i} d(t_i, t_j)$, which is at least the step cost of the rule above. The analysis below holds for both.

## Example

The graph is a cycle $t_1, t_2, t_3, t_4$ with edges of weight $3$, plus a center $s$ joined to each $t_i$ by an edge of weight $2$. The optimal Steiner tree is the star at $s$, with weight $8$.

| order | step costs | paths bought | total |
|---|---|---|---|
| $t_1, t_2, t_3, t_4$ | $0, 3, 3, 3$ | $t_2 t_1$, $t_3 t_2$, $t_4 t_3$ | $9$ |
| $t_1, t_3, t_2, t_4$ | $0, 4, 2, 2$ | $t_3 s t_1$, $t_2 s$, $t_4 s$ | $8$ |

In the first order, each new terminal is at distance $3$ from the tree by a cycle edge, and $4$ through the center, so greedy takes the cycle edges. In the second order, the path from $t_3$ to $t_1$ goes through $s$, and then $t_2$ and $t_4$ join at $s$ for $2$ each. The order of arrival changes the result.

**A bad order.** On the diamond graphs of the [online Steiner tree problem](/online-steiner-tree-problem/), the adversary that always requests the midpoint on the side where the tree is lighter forces greedy to pay exactly $(1 + L/2) \cdot \mathrm{OPT}$ at level $L$, with $k = 2^L + 1$ terminals:

| $L$ | $k$ | $n$ | greedy | OPT | ratio |
|---|---|---|---|---|---|
| 1 | 3 | 4 | 3 | 2 | 1.5 |
| 2 | 5 | 12 | 8 | 4 | 2.0 |
| 3 | 9 | 44 | 20 | 8 | 2.5 |
| 4 | 17 | 172 | 48 | 16 | 3.0 |
| 5 | 33 | 684 | 112 | 32 | 3.5 |
| 6 | 65 | 2732 | 256 | 64 | 4.0 |

Here every edge has weight $1$. The ratio grows like $\tfrac{1}{2} \log_2 k$.

## Correctness

The output is a tree that contains every terminal, because each step joins the new terminal to the tree by a path that meets it in one vertex. For the cost, let $c_i$ be the cost of step $i$, and sort the costs of steps $2, \ldots, k$ as $c_{(1)} \ge c_{(2)} \ge \cdots \ge c_{(k-1)}$. Each $c_i$ is at most $\min_{j < i} d(t_i, t_j)$. The terminals of the $j$ most expensive steps, together with $t_1$, are $j + 1$ points that are pairwise at distance at least $c_{(j)}$. A closed walk around the optimal Steiner tree visits all of them and has length $2\,\mathrm{OPT}$, so $(j + 1)\,c_{(j)} \le 2\,\mathrm{OPT}$. Summing over $j$ gives

$$\mathrm{ALG}(\sigma) \le 2\Big(\frac{1}{2} + \frac{1}{3} + \cdots + \frac{1}{k}\Big)\,\mathrm{OPT}(\sigma) = 2\,(H_k - 1)\,\mathrm{OPT}(\sigma),$$

where $H_k$ is the $k$-th [harmonic number](/harmonic-series/). The full proof is below.

## Complexity

Each step runs Dijkstra's algorithm with a binary heap, in $O((n + e) \log n)$ time, so $k$ terminals take $O(k (n + e) \log n)$ time. The algorithm stores the tree and the search state, $O(n + e)$ space. If all pairwise distances are precomputed, a step of the metric variant takes $O(k)$ time by a scan of the earlier terminals.

## Properties

- **Competitive ratio.** $\mathrm{ALG} \le 2(H_k - 1)\,\mathrm{OPT}$ for every sequence of $k$ terminals, with additive constant $0$. Since $H_k \le 1 + \ln k$, the ratio is at most $2 \ln k$.
- **Rank bound.** The $j$-th largest step cost is at most $2\,\mathrm{OPT}/(j + 1)$. So only a few steps can be expensive.
- **Tight up to a constant.** On the diamond graphs, greedy pays $(1 + \tfrac12 \log_2 (k - 1))\,\mathrm{OPT}$. Every online algorithm, even a randomized one, pays $\Omega(\log k)\,\mathrm{OPT}$ on some input, so greedy is optimal up to a constant factor.
- **No recourse.** It never removes an edge. With a small number of edge swaps per arrival, a constant or even a $(1 + \varepsilon)$ ratio is possible, as in the work of Megow, Skutella, Verschae and Wiese.
- **Deterministic and memoryless.** The only state is the tree.

## Variants and improvements

- **Steiner forest.** For requests that are pairs of vertices, the greedy rule that connects each pair by the cheapest path given the edges already bought is $O(\log^2 k)$-competitive (Awerbuch, Azar and Bartal 1996). Berman and Coulston (1997) gave an $O(\log k)$-competitive algorithm for the generalized problem. See [Steiner forest](/steiner-forest/).
- **Deletions and rearrangements.** Imase and Waxman also allowed terminals to leave, and showed that a bounded number of rearrangements keeps a constant ratio. Gu, Gupta and Kumar (2013) showed that one swap per arrival is enough for a constant ratio.
- **Euclidean plane.** For points in the plane, greedy is still $O(\log k)$-competitive, and Alon and Azar proved a lower bound of $\Omega(\log k / \log\log k)$ for every online algorithm.
- **Offline use.** If the algorithm may choose the order and always adds the terminal nearest to the tree, the rule becomes the offline heuristic of Takahashi and Matsuyama (1980), which is a $2$-approximation, like the algorithm of [Kou, Markowsky and Berman](/kou-markowsky-berman/). The logarithmic loss comes only from the order of arrival.

## When to use it

Use the greedy rule when terminals join a network that is already laid out and the bought links cannot be changed: multicast groups in a fixed network, cables or pipes to new customers, or incremental network design. It is simple, needs only shortest path searches, and its guarantee is the best possible up to a constant. When the terminals are known in advance, use an offline [Steiner tree](/steiner-tree-problem/) algorithm instead.

## Pitfalls

- **Nearest terminal or nearest tree vertex.** The two rules differ. The analysis covers both, but the tree rule is never worse on a single step, since the tree contains the earlier terminals.
- **Repeated terminals.** A terminal that is already in the tree costs nothing. Count $k$ as the number of distinct terminals in the bound.
- **The constant.** The bound $2(H_k - 1)$ uses a closed walk around the optimal tree. Other analyses give other constants, but the order $\log k$ cannot be improved.
- **Disconnected graphs.** A terminal in another component cannot be connected. The implementation raises an error.
- **Ties.** Different shortest paths give different trees and different later costs, as the example shows. The bound holds for every choice.

## Implementations

## History

Imase and Waxman introduced the dynamic Steiner tree problem in 1991, for multicast routing in communication networks. They proved the $O(\log k)$ bound for the greedy rule, the $\Omega(\log k)$ lower bound for every online algorithm, and results for the version with deletions. Alon and Azar studied the Euclidean plane in 1993. Awerbuch, Azar and Bartal, and then Berman and Coulston, extended the analysis to the generalized Steiner problem. Later work by Megow, Skutella, Verschae and Wiese, and by Gu, Gupta and Kumar, studied how much recourse beats the logarithmic bound.

## References
