---
tag: FA6B7M
kind: problem
slug: online-steiner-tree-problem
name: Online Steiner tree problem
aliases:
- online Steiner network
- online Steiner tree
- dynamic Steiner tree problem
area: online-and-streaming/competitive-analysis
level: advanced
summary: Connect terminals that arrive one at a time to a growing tree, without removing edges.
prereqs: [steiner-tree-problem, competitive-ratio, online-algorithm, yao-minimax-principle]
see_also: [online-greedy-steiner-tree, online-minimum-spanning-tree-problem, steiner-forest, online-facility-location-problem, online-set-cover-problem, kou-markowsky-berman]
sources:
  - paper: "Makoto Imase and Bernard M. Waxman, Dynamic Steiner tree problem, SIAM Journal on Discrete Mathematics 4(3) (1991), 369-384"
    title: "Imase and Waxman, Dynamic Steiner tree problem (1991)"
    locator: the online model, the diamond graph lower bound Omega(log k), the O(log k) bound for greedy, and the model with deletions
  - paper: "Noga Alon and Yossi Azar, On-line Steiner trees in the Euclidean plane, Discrete and Computational Geometry 10 (1993), 113-121"
    title: "Alon and Azar, On-line Steiner trees in the Euclidean plane (1993)"
    locator: the lower bound Omega(log k / log log k) for points in the plane
  - paper: "Baruch Awerbuch, Yossi Azar and Yair Bartal, On-line generalized Steiner problem, SODA 1996; Theoretical Computer Science 324 (2004)"
    title: "Awerbuch, Azar and Bartal, On-line generalized Steiner problem"
    locator: the O(log^2 k) bound for the greedy rule on the online Steiner forest problem
  - paper: "Nicole Megow, Martin Skutella, Jose Verschae and Andreas Wiese, The power of recourse for online MST and TSP, SIAM Journal on Computing 45(3) (2016), 859-880"
    title: "Megow, Skutella, Verschae and Wiese, The power of recourse for online MST and TSP (2016)"
    locator: online Steiner tree and MST with recourse, and the (1 + epsilon) bound with amortized constant recourse
  - url: https://arxiv.org/abs/1307.3757
    title: "Albert Gu, Anupam Gupta and Amit Kumar, The power of deferral: maintaining a constant-competitive Steiner tree online, STOC 2013"
    locator: a constant ratio with one edge swap per arrival
---

The online Steiner tree problem asks for a cheap tree that connects terminals of a weighted graph, when the terminals arrive one at a time and the bought edges can never be removed. It is the online version of the [Steiner tree problem](/steiner-tree-problem/), and Imase and Waxman introduced it in 1991 for multicast routing. They proved that the [greedy rule](/online-greedy-steiner-tree/), which connects each new terminal to the nearest point of the tree, is $O(\log k)$-competitive for $k$ terminals, and that no online algorithm, deterministic or randomized, does better than $\Omega(\log k)$. So the competitive ratio of the problem is $\Theta(\log k)$.

## In plain words

A company lays cable to new customers in a city whose streets it already knows. Customers sign up one by one. Each time, the company must connect the new customer to its cable network, and it cannot take old cable out.

With the full list of customers, a planner could find the shortest network that reaches them all. Online, the company may lay a cable that is useless for later customers, while a different early choice would have served them. Some lists of customers force this waste on every strategy, even a strategy that flips coins. The waste grows slowly, like the number of digits of the number of customers, and a simple greedy rule reaches this limit.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $G = (V, E)$, $w$ | the graph and its nonnegative edge weights, known in advance |
| $d$ | the shortest path metric of $G$ |
| $n$ | the number of vertices |
| $\sigma = t_1, \ldots, t_k$ | the request sequence: $k$ terminals |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the weight bought online, and the weight of a minimum Steiner tree for $t_1, \ldots, t_k$ |
| $c$ | the competitive ratio |

**Input.** The graph, and terminals $t_1, \ldots, t_k$ that arrive one at a time. In the metric version, the input is a metric space, and the algorithm buys straight connections between points.

**Output.** After terminal $t_i$ arrives, a set $F_i \supseteq F_{i-1}$ of edges that connects $t_1, \ldots, t_i$.

**Cost.** $\mathrm{ALG}(\sigma) = w(F_k)$.

**Competitive ratio.** A deterministic algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$. Here $c$ may depend on $k$, and the bounds below have additive constant $0$. A randomized algorithm is $c$-competitive if $\mathbb{E}[\mathrm{ALG}(\sigma)] \le c \cdot \mathrm{OPT}(\sigma)$ against an [oblivious adversary](/oblivious-adversary/).

## Variants

- **Steiner forest.** Requests are pairs $(s_i, t_i)$ that must be connected. The greedy rule is $O(\log^2 k)$-competitive (Awerbuch, Azar and Bartal 1996), and Berman and Coulston (1997) reached $O(\log k)$. See [Steiner forest](/steiner-forest/).
- **Euclidean and planar.** For points in the plane the lower bound is $\Omega(\log k / \log\log k)$ (Alon and Azar 1993), so even geometry does not give a constant ratio.
- **Node-weighted.** Vertices instead of edges have costs. The problem then contains [online set cover](/online-set-cover-problem/), and the known ratios are polylogarithmic.
- **Deletions and recourse.** Terminals may also leave, or the algorithm may replace a few edges per step. Imase and Waxman showed that a bounded number of rearrangements gives a constant ratio. Megow, Skutella, Verschae and Wiese reached $1 + \varepsilon$ with amortized constant recourse, and Gu, Gupta and Kumar a constant with one swap per arrival.
- **Online MST.** If every vertex that arrives is a terminal and the metric is given only among the vertices so far, the problem is the [online minimum spanning tree problem](/online-minimum-spanning-tree-problem/). Steiner points are then not available.

## Examples

**Why online is harder.** Take a star with center $s$ and leaves $t_1, t_2, t_3$, with edges of weight $1$, plus direct edges $t_1 t_2$ and $t_2 t_3$ of weight $1.5$. If $t_1$ and $t_2$ arrive first, the direct edge of weight $1.5$ is the cheapest connection, and the greedy tree pays $1.5$. After $t_3$ arrives it pays $1.5$ more, for a total of $3$, while the star costs $3$ as well. If a fourth leaf $t_4$ arrives, joined only to $s$ by an edge of weight $1$, greedy pays $2$ for the path $t_4 s t_1$, total $5$, against the star with weight $4$. The online algorithm cannot know whether to invest in the center early.

**The diamond graphs.** Let $G_0$ be one edge between $s$ and $t$, of length $1$. To get $G_j$ from $G_{j-1}$, replace each edge $uv$ by two paths $u, a, v$ and $u, b, v$ of two edges each, with each new edge half as long as the old one. So $G_L$ has $4^L$ edges of length $2^{-L}$, $n = 2 + \tfrac{2}{3}(4^L - 1)$ vertices, and $d(s, t) = 1$. A *segment* of level $j$ is the copy of $G_{L-j}$ that replaced one edge of $G_j$. Each segment of level $j < L$ between $u$ and $v$ has two *sides*: the two segments of level $j + 1$ through one midpoint, and the two through the other.

**The adversary.** First request $s$ and $t$. The current path is the segment of level $0$. In round $j = 1, \ldots, L$, for each of the $2^{j-1}$ segments of level $j - 1$ on the current path, request the midpoint of one of its two sides. The chosen sides form the next current path, of length $1$ again. The deterministic adversary chooses the side in which the online tree has less weight at that moment. The randomized adversary chooses a side uniformly at random. In total there are $k = 2^L + 1$ terminals, and all of them lie on one path from $s$ to $t$ of length $1$, so $\mathrm{OPT} = 1$.

With unit edges at level $L$ (so all lengths are multiplied by $2^L$), the greedy algorithm against the deterministic adversary pays $3, 8, 20, 48, 112, 256$ for $L = 1, \ldots, 6$, against $\mathrm{OPT} = 2, 4, 8, 16, 32, 64$. That is exactly $(1 + L/2) \cdot \mathrm{OPT}$.

## Known algorithms

- **Greedy.** Connect each terminal to the nearest vertex of the current tree. It is $2(H_k - 1)$-competitive, see [online greedy Steiner tree](/online-greedy-steiner-tree/).
- **Greedy with recourse.** Megow, Skutella, Verschae and Wiese, and Gu, Gupta and Kumar, combine greedy with a few edge swaps per step to reach a constant ratio.
- **Primal-dual.** The [online primal-dual](/online-primal-dual/) method of Buchbinder and Naor is the general tool for online covering problems of this kind. It is used for the node-weighted and the generalized versions, where greedy is not enough.
- **Offline algorithms for comparison.** Offline, the algorithm of [Kou, Markowsky and Berman](/kou-markowsky-berman/) has ratio $2$, and the best known ratios are below $1.4$. Online, no constant ratio is possible.

## Bounds

| Setting | Lower bound | Upper bound |
|---|---|---|
| deterministic, graphs | $\tfrac14 \log_2 (k - 1)$ (proved below; Imase and Waxman 1991) | $2(H_k - 1) \le 2 \ln k$ (greedy) |
| randomized, oblivious, graphs | $\tfrac14 \log_2 (k - 1)$ (proved below) | $2(H_k - 1)$ |
| deterministic, Euclidean plane | $\Omega(\log k / \log\log k)$ (Alon and Azar 1993) | $O(\log k)$ |
| Steiner forest | $\Omega(\log k)$ | $O(\log k)$ (Berman and Coulston 1997) |

**Theorem (lower bound on the diamond).** Let $L \ge 1$ and $k = 2^L + 1$. For every deterministic online algorithm, the deterministic adversary gives $\mathrm{ALG} \ge \max(1, L/4)$ while $\mathrm{OPT} = 1$. For every randomized online algorithm, there is a fixed sequence of $k$ terminals with $\mathbb{E}[\mathrm{ALG}] \ge L/4$ and $\mathrm{OPT} = 1$. So the competitive ratio of every online algorithm is at least $\tfrac14 \log_2 (k - 1)$.

*Proof.* Let $T$ be the edge set of the online tree just before the midpoint $m$ of side $S$ of a segment $e$ from $u$ to $v$, of level $j - 1$, is requested. Let $Q$ be the other side of $e$, and write $w(T \cap S)$ for the weight of the edges of $T$ inside $S$.

*Step 1: the cost to connect $m$.* The online tree contains $s$ and $t$, which are outside the inside of $S$ (or equal to $u$ or $v$), and it is connected. The inside of $S$ meets the rest of the graph only at $u$ and $v$. So every component of $T \cap S$ that has a vertex inside $S$ contains $u$ or $v$. Let $x$ be the vertex of the tree nearest to $m$. If a shortest path from $m$ to $x$ leaves $S$, it passes $u$ or $v$, and its length is at least $d(m, \{u, v\}) = 2^{-j}$. Otherwise $x$ is in a component of $T \cap S$ that contains $u$ or $v$, so $d(x, \{u, v\}) \le w(T \cap S)$, and $d(m, x) \ge 2^{-j} - w(T \cap S)$. In both cases the online algorithm pays at least

$$\mathrm{inc}_e \ge 2^{-j} - w(T \cap S)$$

for this request, since it must connect $m$ to its tree, and only the new edges count.

*Step 2: charging to the unchosen side.* Let $T_{\mathrm{end}}$ be the final tree. The deterministic adversary chooses $S$ with $w(T \cap S) \le w(T \cap Q)$, so $\mathrm{inc}_e + w(T_{\mathrm{end}} \cap Q) \ge \mathrm{inc}_e + w(T \cap S) \ge 2^{-j}$. The unchosen sides $Q(e)$ of all segments $e$ of all rounds are pairwise edge disjoint: segments of one level are disjoint, and every later segment lies inside a chosen side. Summing over the $2^{j-1}$ segments of round $j$ and over all rounds,

$$\sum_e \mathrm{inc}_e + \sum_e w(T_{\mathrm{end}} \cap Q(e)) \ge \sum_{j=1}^{L} 2^{j-1} \cdot 2^{-j} = \frac{L}{2}.$$

The first sum is at most $\mathrm{ALG}$, and the second is at most $w(T_{\mathrm{end}}) \le \mathrm{ALG}$, by disjointness. So $\mathrm{ALG} \ge L/4$. Also $\mathrm{ALG} \ge d(s, t) = 1$.

*Step 3: randomized algorithms.* By [Yao's principle](/yao-minimax-principle/), it is enough to show $\mathbb{E}[\mathrm{ALG}] \ge L/4$ for every deterministic algorithm when the adversary chooses each side uniformly at random. Given the past, $T$ is fixed and $(S, Q)$ is a uniformly random order of the two sides, so $\mathbb{E}[w(T \cap S)] = \mathbb{E}[w(T \cap Q)]$. Then $\mathbb{E}[\mathrm{inc}_e + w(T_{\mathrm{end}} \cap Q)] \ge \mathbb{E}[2^{-j} - w(T \cap S) + w(T \cap Q)] = 2^{-j}$, and the sum of Step 2 gives $2\,\mathbb{E}[\mathrm{ALG}] \ge L/2$. Every sequence of the random adversary has $\mathrm{OPT} = 1$. $\square$

In terms of the number of vertices, $L \approx \tfrac12 \log_2 n$, so the bound is also $\Omega(\log n)$.

## Reductions

- **From offline Steiner tree.** An online algorithm that runs in polynomial time is also an offline approximation algorithm, so its ratio is at least the offline hardness bound. The online lower bound is much larger, and it comes from the lack of information, not from computation: it holds even for online algorithms with unbounded time.
- **To online set cover.** The node-weighted version contains [online set cover](/online-set-cover-problem/) as a special case, which explains its larger bounds.
- **Relation to online MST and TSP.** A Steiner tree on the terminals is at most the minimum spanning tree of the terminals, which is at most twice the Steiner tree. So bounds for online Steiner tree and the [online minimum spanning tree problem](/online-minimum-spanning-tree-problem/) differ by a factor of at most $2$, when Steiner points are free to use.
- **Facility location.** Connecting a new client to the nearest open point is also the core of [online facility location](/online-facility-location-problem/), where the algorithm may open new centers instead of buying long paths.

## Applications

- **Multicast routing.** A multicast group in a network grows as receivers join, and each new receiver is connected to the existing distribution tree. This was the motivation of Imase and Waxman.
- **Incremental network design.** Cables, pipes or roads to new customers, when old links stay in place.
- **Buy-at-bulk and rent-or-buy.** Online network design problems with several cable types use online Steiner tree algorithms as building blocks.

## References
