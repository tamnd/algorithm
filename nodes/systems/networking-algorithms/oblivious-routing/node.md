---
tag: 5054NE
kind: concept
slug: oblivious-routing
name: Oblivious routing
aliases:
- oblivious routing algorithm
- oblivious routing scheme
area: systems/networking-algorithms
level: advanced
summary: "A routing that fixes, for each source and destination, a path or a probability distribution on paths, without looking at the other traffic. Its quality is the worst ratio to the best congestion."
prereqs: [routing-problem, multi-commodity-flow-problem, competitive-ratio]
see_also: [valiant-routing, dimension-order-routing, permutation-routing, frt-tree-embedding, low-stretch-spanning-tree, electrical-flow, lp-duality, edge-disjoint-paths]
sources:
  - paper: doi:10.1109/SFCS.2002.1181895
    title: "Harald Räcke, Minimizing congestion in general networks, Proceedings of the 43rd IEEE Symposium on Foundations of Computer Science (FOCS 2002), 43-52"
    locator: the existence of an oblivious routing with competitive ratio O(log^3 n) for every undirected graph, by a hierarchical decomposition
  - paper: doi:10.1145/1374376.1374415
    title: "Harald Räcke, Optimal hierarchical decompositions for congestion minimization in networks, Proceedings of the 40th ACM Symposium on Theory of Computing (STOC 2008), 255-264"
    locator: an oblivious routing with competitive ratio O(log n) as a convex combination of trees, built from tree embeddings of the graph
  - paper: doi:10.1145/780542.780599
    title: "Yossi Azar, Edith Cohen, Amos Fiat, Haim Kaplan and Harald Räcke, Optimal oblivious routing in polynomial time, Proceedings of the 35th ACM Symposium on Theory of Computing (STOC 2003), 383-388"
    locator: a linear program, solved with a separation oracle, that computes the oblivious routing with the best ratio for a given graph
  - paper: doi:10.1137/0211027
    title: "Leslie G. Valiant, A scheme for fast parallel communication, SIAM Journal on Computing 11(2) (1982), 350-361"
    locator: randomized two-phase routing through a random intermediate node, the first oblivious routing with good worst-case behavior on the hypercube
  - paper: doi:10.1007/BF02090400
    title: "Christos Kaklamanis, Danny Krizanc and Thanassis Tsantilas, Tight bounds for oblivious routing in the hypercube, Mathematical Systems Theory 24 (1991), 223-232"
    locator: the lower bound for deterministic oblivious routing (one path for each pair) on graphs of bounded degree and on the hypercube
  - paper: "Yair Bartal and Stefano Leonardi, On-line routing in all-optical networks, Theoretical Computer Science 221(1-2) (1999), 19-39"
    locator: the lower bound of order log n on the competitive ratio of online (and so of oblivious) routing for congestion on the two-dimensional mesh
  - paper: doi:10.1145/863955.863991
    title: "David Applegate and Edith Cohen, Making intra-domain routing robust to changing and uncertain traffic demands (understanding fundamental tradeoffs), Proceedings of ACM SIGCOMM 2003, 313-324"
    locator: computing oblivious routings for real ISP topologies with linear programming, and their measured ratios to the best routing
  - book: isbn:9780122007514
    title: William J. Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: Chapter 9, oblivious routing (Valiant's algorithm, minimal oblivious routing and load balance on tori)
---

A routing is **oblivious** when the route of each packet depends only on its source, its destination and perhaps a random choice, and not on the other packets in the network. For each ordered pair $(s, t)$ an oblivious routing fixes in advance one path, or a probability distribution on paths, from $s$ to $t$. [Dimension-order routing](/dimension-order-routing/) is oblivious and deterministic; [Valiant's two-phase routing](/valiant-routing/) is oblivious and randomized; routing on shortest paths with a fixed tie rule is oblivious. Adaptive routing, which looks at queue lengths, and routing that solves an optimization over the whole demand matrix, are not. The main question is how much an oblivious routing loses against the best routing for each demand. Räcke showed in 2002 that every undirected network has an oblivious routing whose congestion is within a polylogarithmic factor of the best, and in 2008 he improved the factor to $O(\log n)$, which is best possible in general.

## In plain words

Imagine a city where each driver gets a route from a fixed map book. The book says, for each start and each end, which roads to take. Nobody looks at today's traffic. The book is written once, before anyone knows where people will go on a given day.

A good book makes sure that, whatever the trips are, no road gets much more traffic than it would get under the best plan made for exactly those trips. A bad book sends everybody over the same bridge on some days. With a coin flip in the book, such as "first drive to a random place, then to your goal", the bad days become very rare. The surprise is that a good book exists for every road network.

## The idea

**Definitions.** Let $G = (V, E)$ be a network with $n$ nodes and a capacity $c(e) > 0$ on each edge. An **oblivious routing** is a family of unit flows $f_{st}$, one for each ordered pair of nodes, where $f_{st}$ sends one unit from $s$ to $t$. A deterministic oblivious routing puts the whole unit on one path; a randomized one splits it over several paths, and a packet picks a path with those probabilities. A **demand** $D$ gives an amount $D(s, t) \ge 0$ for each pair. The oblivious routing sends $D(s, t) \cdot f_{st}$ for each pair, so the load on edge $e$ is

$$\mathrm{load}(e) = \sum_{s, t} D(s, t) \, f_{st}(e),$$

and the **congestion** is $\max_e \mathrm{load}(e) / c(e)$. Let $\mathrm{OPT}(D)$ be the smallest congestion of any [multicommodity flow](/multi-commodity-flow-problem/) that routes $D$. The **competitive ratio** of the oblivious routing is the largest value of its congestion divided by $\mathrm{OPT}(D)$, over all demands $D$. For a randomized routing used by single packets, the load is the expected load; with many packets and short paths, Chernoff bounds turn it into a bound that holds with high probability, as on the [Valiant routing](/valiant-routing/) page.

**Why the ratio is a fair measure.** The routing is fixed before $D$ is known, while $\mathrm{OPT}(D)$ is computed with full knowledge of $D$. So the ratio is the price of not knowing the traffic, in the same sense as the [competitive ratio](/competitive-ratio/) of an online algorithm. A ratio of $\alpha$ means that for every demand that the network can carry at all, the fixed routing carries it with edges at most $\alpha$ times as full.

**Deterministic oblivious routing is weak.** If each pair has one path, an adversary can pick a permutation that puts many paths on one edge. Borodin and Hopcroft (1985) proved a bound of about $\sqrt{N}$ divided by a power of $d$, and Kaklamanis, Krizanc and Tsantilas (1991) improved it: on a graph with $N$ nodes and largest degree $d$, every deterministic oblivious routing has a permutation that puts $\Omega(\sqrt{N} / d)$ paths on one edge, while the best routing of a permutation on a hypercube has constant congestion. On the hypercube with $N = 2^n$ nodes this means $\Omega(\sqrt{N} / \log N)$; see [permutation routing](/permutation-routing/).

**Randomness fixes it on special networks.** Valiant's routing first sends each packet to a random intermediate node by the fixed path rule, then from there to its destination. On the hypercube each directed edge then carries an expected load of at most $R/2$ in each phase, where $R$ is the largest amount that one node sends or receives. Since a node has only $n$ outgoing edges of capacity 1, $\mathrm{OPT}(D) \ge R / n$. So Valiant's routing has competitive ratio at most $n = \log_2 N$ on the hypercube, for every demand.

**Räcke's theorem.** For every undirected graph with $n$ nodes and any capacities, there is an oblivious routing with competitive ratio $O(\log^3 n)$ (Räcke 2002). The proof builds a hierarchical decomposition of the graph into clusters and routes inside the clusters in a way that is good for every demand that fits through the cluster boundaries. Azar, Cohen, Fiat, Kaplan and Räcke (2003) showed that the oblivious routing with the best ratio for a given graph is the solution of a linear program that a separation oracle can solve in polynomial time. Harrelson, Hildrum and Rao (2003) gave a polynomial-time construction with ratio $O(\log^2 n \log \log n)$. Räcke (2008) showed that a convex combination of trees, each mapped back into the graph, gives ratio $O(\log n)$: route a demand in each tree, where paths are unique, and send the tree paths along graph paths. The trees come from a [tree embedding](/frt-tree-embedding/) of a metric that the algorithm changes by multiplicative weights. Bartal and Leonardi showed that on the $\sqrt{n} \times \sqrt{n}$ mesh no online routing, and so no oblivious routing, has ratio better than $\Omega(\log n)$. So $O(\log n)$ is tight in general.

**What it does not promise.** The ratio is about congestion only. An oblivious routing may use long paths: Valiant's routing doubles the expected path length, and Räcke's trees may send a packet far from the straight line. Path length and congestion together decide how long a batch of packets takes, and later work studies routings that bound both. On directed graphs and on graphs with node capacities, oblivious routing can be much worse. There are directed graphs and node-capacitated graphs on which every oblivious routing has ratio $\Omega(\sqrt{n})$ (Hajiaghayi, Kleinberg, Leighton and Räcke 2005), and for directed graphs Ene, Miller, Pachocki and Sidford (2016) raised the bound to $\Omega(n)$.

## Examples

**Trees.** In a tree there is one path between each pair of nodes, so every routing is the same routing, it is oblivious, and its ratio is 1. Räcke's 2008 construction uses this fact: it reduces a general graph to a mix of trees.

**The hypercube, deterministic.** The scratch computation for this page routed bit reversal on the $n$-dimensional hypercube with bit-fixing paths (dimension-order routing). The largest load on a directed edge was 1, 2, 4, 8 and 16 for $n = 2, 4, 6, 8, 10$, that is $2^{n/2 - 1}$. The best congestion for bit reversal is at least $1/2$, because the paths have $n/2$ hops on average and there are $nN$ directed edges, and at most the load of Valiant's routing below, which is under 1. So for $n = 10$ the deterministic routing is between 16 and 32 times worse than the best, and the gap grows as $\sqrt{N}$. Transpose gives the same numbers.

**The hypercube, randomized.** For the same bit-reversal demand, Valiant's routing gives an expected largest load of exactly $3/4, 7/8, 15/16, 31/32, 63/64$ for $n = 2, 4, 6, 8, 10$. It is just under 1 because the $2^{n/2}$ nodes whose address is a palindrome send nothing.

**Where Valiant's routing loses.** Let every node of the hypercube send one unit to each of its $n$ neighbors. The best routing sends each unit over its own edge, so $\mathrm{OPT} = 1$. Valiant's routing spreads each unit over the whole cube: the computed largest load was exactly $n$ for $n = 2, \ldots, 6$. This meets the upper bound $n$ above, so on the hypercube the ratio of Valiant's routing is exactly $\log_2 N$. The traffic is local, and the random intermediate node destroys the locality. Räcke's routing, built for the graph, does not have this loss on local traffic. A deterministic routing such as bit-fixing has load 1 here, which shows that no one routing in these examples is best for every demand.

**Mesh and torus networks.** On a $k \times k$ torus, oblivious routings trade worst-case throughput against path length. Valiant's routing has a good worst case but doubles the average path length, so it halves the throughput on local traffic. Dimension-order routing has short paths and a poor worst case. Dally and Towles describe minimal oblivious routings, such as ROMM, that pick a random intermediate node only inside the smallest box that holds the source and the destination, as a point between these two ends.

## Where it is used

- **Parallel computers and networks on chip.** Routers that must decide in a few clock cycles use oblivious routing: [dimension-order routing](/dimension-order-routing/) on meshes and tori, Valiant-style randomization on some supercomputer networks, and randomized choice of XY or YX order.
- **Internet traffic engineering.** Applegate and Cohen (2003) computed oblivious routings for real ISP topologies with linear programming and found ratios close to 1 for many of them, so a fixed routing can cope with demands that change and are hard to measure. Valiant load balancing was also proposed for backbone design, so that the backbone carries any traffic matrix within the limits of its access links.
- **Data center networks.** Spreading flows over random paths or random intermediate switches, as in VL2 and in ECMP hashing, is oblivious load balancing in Valiant's spirit.
- **Semi-oblivious routing.** Later systems, such as SMORE, choose a small set of paths for each pair with Räcke's method and then adapt only the split rates to the measured demand. This keeps the robustness of the oblivious paths and gains from knowing the demand.
- **Algorithms.** Oblivious routings and the tree decompositions behind them are tools in fast approximate [max-flow](/max-flow-problem/) algorithms, in online routing and in approximation algorithms for cut problems, because a fixed routing that is good for all demands gives a linear operator that approximates the cut structure of the graph.

## References
