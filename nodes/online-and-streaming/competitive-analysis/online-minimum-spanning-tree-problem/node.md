---
tag: N7Y4QP
kind: problem
slug: online-minimum-spanning-tree-problem
name: Online minimum spanning tree problem
aliases:
- online MST
- online spanning tree
- incremental minimum spanning tree
area: online-and-streaming/competitive-analysis
level: advanced
summary: Vertices of a metric space arrive online, and each new vertex must be connected at once by edges that are never removed, at small total cost compared to the minimum spanning tree.
prereqs: [minimum-spanning-tree, competitive-ratio, online-algorithm, metric-space]
see_also: [online-steiner-tree-problem, online-greedy-steiner-tree, online-traveling-salesman-problem, dynamic-minimum-spanning-tree, steiner-tree-problem, harmonic-series]
sources:
  - paper: "Makoto Imase and Bernard M. Waxman, Dynamic Steiner tree problem, SIAM Journal on Discrete Mathematics 4(3) (1991), 369-384"
    title: "Imase and Waxman, Dynamic Steiner tree problem (1991)"
    locator: the greedy rule, its O(log n) bound, the Omega(log n) lower bound, and the model with rearrangements
  - paper: "Nicole Megow, Martin Skutella, Jose Verschae and Andreas Wiese, The power of recourse for online MST and TSP, SIAM Journal on Computing 45(3) (2016), 859-880"
    title: "Megow, Skutella, Verschae and Wiese, The power of recourse for online MST and TSP (2016)"
    locator: online MST with recourse, the (1 + epsilon) bound with amortized constant recourse, and the consequences for online TSP
  - url: https://arxiv.org/abs/1307.3757
    title: "Albert Gu, Anupam Gupta and Amit Kumar, The power of deferral: maintaining a constant-competitive Steiner tree online, STOC 2013"
    locator: a constant ratio with one edge swap per arrival
---

The online minimum spanning tree problem asks for a cheap spanning tree of points that arrive one at a time in a metric space. When a point arrives, its distances to the earlier points become known, and the algorithm must connect it to the current tree at once, with edges that are never removed. The cost is compared with the [minimum spanning tree](/minimum-spanning-tree/) of all the points. In this model the greedy rule, which connects each point to the nearest earlier point, is the best online algorithm on every input, and its competitive ratio is $\Theta(\log n)$ for $n$ points: at least $1 + \tfrac12 \log_2 (n - 1)$, already on a line, and at most $2(H_n - 1) \le 2 \ln n$. With a few edge swaps per step, a ratio of $1 + \varepsilon$ is possible.

## In plain words

Houses are built one at a time, and each new house must be joined to the power grid on the day it is built. The power company can lay a cable from the new house to any older house, at a cost equal to the length. Old cables stay in the ground.

If the company knew all future houses, it would lay the shortest network that joins them all. Online, a long cable laid early may later be useless, because new houses fill the gap and short cables would have done the same job. No strategy avoids this, because each new house needs at least one cable to an older house. So the best plan is simply to use the shortest such cable each day. Its waste grows slowly with the number of houses.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $(M, d)$ | a metric space |
| $\sigma = v_1, \ldots, v_n$ | the request sequence: $n$ distinct points of $M$, in the order of arrival |
| $E_i$ | the set of edges bought after step $i$, with $E_{i-1} \subseteq E_i$ |
| $\mathrm{MST}(\sigma)$ | the weight of a minimum spanning tree of $v_1, \ldots, v_n$ with edge weights $d$ |
| $\mathrm{ALG}(\sigma)$ | the total weight of the edges bought online |
| $H_n$ | the harmonic number $\sum_{i=1}^{n} 1/i$ |

**Input.** The points $v_1, \ldots, v_n$, revealed one at a time. At step $i$, the algorithm learns $d(v_i, v_j)$ for all $j < i$. It does not know $n$.

**Output.** At step $i$, a set $E_i \supseteq E_{i-1}$ of edges between the points $v_1, \ldots, v_i$ such that $(\{v_1, \ldots, v_i\}, E_i)$ is connected.

**Cost.** $\mathrm{ALG}(\sigma) = \sum_{e \in E_n} d(e)$. The offline optimum is $\mathrm{MST}(\sigma)$.

**Competitive ratio.** An algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{MST}(\sigma)$ for every $\sigma$, with additive constant $0$. For a randomized algorithm, $\mathbb{E}[\mathrm{ALG}(\sigma)]$ replaces $\mathrm{ALG}(\sigma)$, against an [oblivious adversary](/oblivious-adversary/). Here $c$ may depend on $n$.

## Variants

- **Steiner points allowed.** If the points lie in a known graph and the algorithm may buy paths through other vertices, the problem is the [online Steiner tree problem](/online-steiner-tree-problem/). The bounds of the two problems differ by a factor of at most $2$, because the minimum spanning tree of a set of points is at most twice its minimum Steiner tree.
- **Recourse.** The algorithm may remove a few old edges when it buys new ones. Imase and Waxman showed that a bounded number of rearrangements per step gives a constant ratio. Megow, Skutella, Verschae and Wiese gave a $(1 + \varepsilon)$-competitive algorithm with amortized $O(\tfrac{1}{\varepsilon} \log \tfrac{1}{\varepsilon})$ edge swaps per step. Gu, Gupta and Kumar reached a constant ratio with at most one swap per arrival.
- **Deletions.** Points may also leave. With a bounded number of rearrangements, constant ratios are still possible.
- **No triangle inequality.** If the edge weights to earlier points are arbitrary, no online algorithm is competitive. With $d(v_1, v_2) = W$ and $d(v_3, v_1) = d(v_3, v_2) = 1$, every algorithm pays at least $W + 1$, while the minimum spanning tree weighs $2$.
- **Dynamic data structures.** Maintaining the exact minimum spanning tree of a changing graph, with any number of edge changes allowed, is a different problem; see [dynamic minimum spanning tree](/dynamic-minimum-spanning-tree/).

## Examples

**Binary refinement on a line.** Points arrive at $0$ and $8$, then $4$, then $2, 6$, then $1, 3, 5, 7$. Each new point must have an edge to an earlier point, and the nearest earlier point is at distance $8, 4, 2, 2, 1, 1, 1, 1$. So every online algorithm pays at least $20$, the greedy rule pays exactly $20$, and the minimum spanning tree, the path along the line, weighs $8$. The ratio is $5/2$.

The same refinement with $n = 2^L + 1$ points on $[0, 2^L]$ gives these values.

| $L$ | $n$ | greedy cost | $\mathrm{MST}$ | ratio |
|---|---|---|---|---|
| $1$ | $3$ | $3$ | $2$ | $3/2$ |
| $2$ | $5$ | $8$ | $4$ | $2$ |
| $3$ | $9$ | $20$ | $8$ | $5/2$ |
| $4$ | $17$ | $48$ | $16$ | $3$ |
| $5$ | $33$ | $112$ | $32$ | $7/2$ |

The ratio is $1 + L/2$. On the diamond graphs of the [online Steiner tree problem](/online-steiner-tree-problem/), with unit edges at level $L$, the nearest earlier terminal of each midpoint of round $j$ is also at distance $2^{L-j}$, so the greedy cost and the ratio are the same.

## Known algorithms

- **Greedy.** Connect $v_i$ to its nearest earlier point. It takes $O(i)$ time at step $i$, and it is the best online algorithm on every input (Theorem 1). Its ratio is $2(H_n - 1)$ at most (Theorem 2). See [online greedy Steiner tree](/online-greedy-steiner-tree/) for the same rule in graphs.
- **Greedy with swaps.** After the greedy edge, replace an old edge $e$ by a new edge $e'$ when $d(e')$ is smaller than $d(e)$ by a large enough factor and the swap keeps the tree connected. Megow, Skutella, Verschae and Wiese analyze rules of this kind and reach a $(1 + \varepsilon)$-competitive tree with amortized bounded recourse.

## Bounds

| Setting | Lower bound | Upper bound |
|---|---|---|
| no recourse, deterministic or randomized | $1 + \tfrac12 \log_2 (n - 1)$ for $n = 2^L + 1$, on a line (Theorem 3) | $2(H_n - 1) \le 2 \ln n$, greedy (Theorem 2) |
| amortized recourse $O(\tfrac1\varepsilon \log \tfrac1\varepsilon)$ | $1$ | $1 + \varepsilon$ (Megow, Skutella, Verschae and Wiese) |
| one swap per arrival | $1$ | $O(1)$ (Gu, Gupta and Kumar) |

**Theorem 1 (greedy is optimal online).** For every online algorithm $A$, deterministic or randomized, and every sequence $\sigma$, $A$ pays at least the greedy cost $G(\sigma) = \sum_{i=2}^{n} \min_{j < i} d(v_i, v_j)$.

*Proof.* At step $i \ge 2$, the graph $(\{v_1, \ldots, v_i\}, E_i)$ is connected, so $E_i$ contains an edge at $v_i$. The other end of this edge is an earlier point, because the later points are not yet known. The edge was not in $E_{i-1}$, because $v_i$ was not known before step $i$. So step $i$ adds an edge of weight at least $\min_{j < i} d(v_i, v_j)$, and these edges are different for different $i$. Summing over $i$ gives $\mathrm{ALG}(\sigma) \ge G(\sigma)$, for every run of a randomized algorithm. $\square$

So the competitive ratio of the problem is exactly $\sup_\sigma G(\sigma) / \mathrm{MST}(\sigma)$.

**Theorem 2 (upper bound).** $G(\sigma) \le 2 (H_n - 1)\,\mathrm{MST}(\sigma)$.

*Proof.* Let $c_i = \min_{j < i} d(v_i, v_j)$ for $i \ge 2$, and sort these costs as $c_{(1)} \ge \cdots \ge c_{(n-1)}$. Fix $j$, and let $U$ be $v_1$ with the $j$ points of the $j$ largest costs. For two points of $U$, the later one $v_b$ has $c_b \ge c_{(j)}$, and the earlier one is an earlier point, so their distance is at least $c_{(j)}$. A walk around a minimum spanning tree has length $2\,\mathrm{MST}$ and visits all points. It splits into $j + 1$ parts between the consecutive points of $U$ in the order of the first visit, and each part has length at least $c_{(j)}$. So $c_{(j)} \le 2\,\mathrm{MST}/(j + 1)$, and summing over $j = 1, \ldots, n - 1$ gives $G \le 2 (H_n - 1)\,\mathrm{MST}$. $\square$

**Theorem 3 (lower bound).** Let $L \ge 1$ and $n = 2^L + 1$. On the points $0, 1, \ldots, 2^L$ of the line, in the order of binary refinement, every online algorithm pays at least $(1 + L/2)\,\mathrm{MST}$.

*Proof.* Round $0$ requests $0$ and $2^L$. Round $j = 1, \ldots, L$ requests the $2^{j-1}$ odd multiples of $2^{L-j}$ in $(0, 2^L)$. Before round $j$, the requested points are exactly the multiples of $2^{L-j+1}$, and the points of round $j$ are at distance at least $2^{L-j+1}$ from each other. So each point of round $j$ has its nearest earlier point at distance exactly $2^{L-j}$. Then

$$G(\sigma) = 2^L + \sum_{j=1}^{L} 2^{j-1} \cdot 2^{L-j} = 2^L \Big(1 + \frac{L}{2}\Big),$$

and $\mathrm{MST}(\sigma) = 2^L$. Theorem 1 finishes the proof. $\square$

The sequence is fixed in advance, so the bound holds for randomized algorithms without [Yao's principle](/yao-minimax-principle/). The two bounds are $\tfrac12 \log_2 n$ and $2 \ln n \approx 1.39 \log_2 n$ to leading order, so they differ by a factor of about $2.8$. This page does not give the exact constant.

## Reductions

- **To online Steiner tree.** Every online MST algorithm is an online Steiner tree algorithm in the metric closure, and $\mathrm{MST} \le 2 \cdot$ Steiner optimum. So upper bounds carry over with a factor $2$, and the diamond lower bound of the [online Steiner tree problem](/online-steiner-tree-problem/) gives $\Omega(\log n)$ here as well.
- **To online TSP.** Doubling the edges of an online spanning tree and taking shortcuts gives a tour of at most twice the weight. Megow, Skutella, Verschae and Wiese use this to get online TSP tours with recourse. The [online traveling salesman problem](/online-traveling-salesman-problem/) with release times is a different model, in which a server moves in time.
- **To offline MST.** Offline, Kruskal's or Prim's algorithm finds the [minimum spanning tree](/minimum-spanning-tree/) exactly in polynomial time. The online loss is only from the lack of information.

## Applications

- **Incremental network design.** Cables, pipes or links to new sites, when old links stay in place.
- **Multicast trees.** New receivers join a distribution tree, as in the work of Imase and Waxman.
- **Sensor and wireless networks.** New nodes join a backbone with a link to a node that is already deployed.

## References
