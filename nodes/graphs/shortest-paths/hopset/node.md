---
tag: CKGDWJ
kind: concept
slug: hopset
name: Hopset
aliases:
- (beta,epsilon)-hopset
- Hopsets
- hop-set
- hopset
- hopsets
- shortcut edges with bounded hop count
area: graphs/shortest-paths
level: research
summary: Added shortcut edges that let approximately shortest paths be found with few hops, speeding up parallel and distributed SSSP.
prereqs: [shortest-path, bellman-ford, single-source-shortest-paths]
see_also: [bellman-ford, ullman-yannakakis, distributed-approximate-sssp, decremental-sssp, thorup-zwick-oracle, distance-oracle, low-diameter-decomposition, pram-model]
sources:
  - paper: doi:10.1137/0220006
    title: Jeffrey D. Ullman and Mihalis Yannakakis, High-probability parallel transitive-closure algorithms, SIAM Journal on Computing 20(1), 100 to 125 (1991)
    locator: the sampling idea (a random set of about (n/beta) log n vertices meets every path of beta edges, with high probability, and the sampled vertices are joined by shortcut edges)
  - paper: doi:10.1145/331605.331610
    title: Edith Cohen, Polylog-time and near-linear work approximation scheme for undirected shortest paths, Journal of the ACM 47(1), 132 to 166 (2000)
    locator: the definition of (beta, epsilon)-hopsets, their construction with polylogarithmic hopbound and size O(n^(1+mu)), and their use for parallel approximate shortest paths
  - paper: doi:10.1137/18M1166791
    title: Michael Elkin and Ofer Neiman, Hopsets with constant hopbound, and applications to approximate shortest paths, SIAM Journal on Computing 48(4), 1436 to 1480 (2019)
    locator: the abstract and introduction (hopsets whose hopbound does not depend on n, and the applications to parallel, distributed and streaming shortest paths)
  - paper: doi:10.1016/j.ipl.2018.10.001
    title: Shang-En Huang and Seth Pettie, Thorup-Zwick emulators are universally optimal hopsets, Information Processing Letters 142, 9 to 13 (2019)
    locator: the main theorem (the Thorup-Zwick emulator is a hopset, with a size and hopbound tradeoff that matches the known lower bounds)
---

A hopset is a set $H$ of extra weighted edges added to a graph so that every distance is achieved, exactly or within a factor $1 + \epsilon$, by a path with few edges. The bound on the number of edges is the *hopbound* $\beta$. With a hopset, $\beta$ rounds of [Bellman-Ford](/bellman-ford/) on $G \cup H$ find all distances from a source, and $\beta$ rounds are cheap to run in parallel or in a distributed network. Ullman and Yannakakis used the idea for parallel transitive closure in 1991. Edith Cohen defined $(\beta, \epsilon)$-hopsets in 2000 and used them for parallel approximate shortest paths.

## In plain words

A road map can have a short route between two towns that still goes through hundreds of small road segments. An algorithm that extends routes one segment per round then needs hundreds of rounds.

A hopset adds express roads. Each express road joins two places, and its length is the true distance between them, or slightly more. With enough of them, every trip can be made from a few segments, close to the shortest length. The question is how few express roads are enough for a given number of segments per trip.

## The idea

**Hop-limited distance.** Let $G = (V, E)$ have $n$ vertices and nonnegative weights. For an integer $\beta \ge 1$, let $d^{(\beta)}_G(u, v)$ be the smallest weight of a path from $u$ to $v$ with at most $\beta$ edges, or $\infty$ if there is none. Bellman-Ford computes $d^{(\beta)}_G(s, \cdot)$ from one source in $\beta$ rounds, each round one relaxation of every edge.

**Definition.** A set $H$ of weighted edges on $V$ is a $(\beta, \epsilon)$-hopset for $G$ if, for all $u, v \in V$,

$$d_G(u, v) \;\le\; d^{(\beta)}_{G \cup H}(u, v) \;\le\; (1 + \epsilon)\, d_G(u, v).$$

The left inequality holds when every hopset edge $(x, y)$ has weight at least $d_G(x, y)$. This is the usual requirement, and most constructions use exactly $d_G(x, y)$. With $\epsilon = 0$ the hopset is *exact*.

**Weight assumptions.** The definition is for nonnegative weights, where $d_G$ is well defined. If $G$ has a negative cycle, $d_G$ is $-\infty$ for some pairs, and no hop-limited distance can match it, so hopsets are not defined for such graphs. If $v$ is unreachable from $u$, then $d_G(u, v) = \infty$, and any valid hopset keeps it at $\infty$: an edge $(x, y)$ with finite weight needs $d_G(x, y) < \infty$, so a hopset adds no new reachability. Most of the theory is for undirected graphs. For directed graphs exact sampling hopsets still work, and the related *shortcut sets* keep only reachability.

**The tradeoff.** There are three quantities: the size $|H|$, the hopbound $\beta$, and the error $\epsilon$. $H = \emptyset$ gives $\beta = n - 1$. Adding all $n^2$ pairs with their distances gives $\beta = 1$. Useful hopsets lie between: near-linear size with a polylogarithmic or even constant $\beta$, for a fixed $\epsilon > 0$.

**Why sampling works.** Ullman and Yannakakis observed the following. Sample each vertex with probability $p = (c \ln n)/\beta$. A fixed path of $\beta$ vertices then misses the sample with probability $(1 - p)^\beta \le n^{-c}$. A union bound over the shortest paths shows that, with high probability, every shortest path of at least $\beta$ edges has a sampled vertex among every $\beta$ consecutive ones. Join every two sampled vertices $x, y$ by an edge of weight $d_G(x, y)$. A shortest path from $u$ to $v$ now uses at most $\beta - 1$ edges to the first sampled vertex, one hopset edge to the last, and at most $\beta - 1$ edges after it. This exact hopset has hopbound at most $2\beta - 1$ and about $(n \ln n / \beta)^2$ edges.

**Better tradeoffs.** For undirected graphs, Cohen built $(\beta, \epsilon)$-hopsets of size $O(n^{1 + \mu})$ with $\beta$ polylogarithmic in $n$, by clustering the graph at several distance scales. Elkin and Neiman built hopsets whose hopbound depends only on $\epsilon$ and the size exponent, not on $n$. Huang and Pettie showed that the emulators of Thorup and Zwick, the sparse graphs behind the [Thorup-Zwick distance oracle](/thorup-zwick-oracle/), are already hopsets with the best known tradeoff, which matches the known lower bounds.

## Examples

**A path, by hubs.** Take the undirected path $0, 1, \ldots, 15$ with unit weights. Without a hopset, the pair $(0, 15)$ needs 15 hops. Choose the hubs $\{0, 4, 8, 12\}$ and join each pair of hubs by an edge of weight equal to their distance: 6 edges. Now every exact distance is achieved within 7 hops. The worst pair is $(1, 11)$, whose path is $1 \to 2 \to 3 \to 4$, then $4 \to 8$, then $8 \to 9 \to 10 \to 11$. A script that computes $d^{(b)}$ for $b = 1, 2, \ldots$ over all 256 pairs confirms the maximum of 7. This is the sampling idea with spacing 4 chosen by hand.

**A path, by midpoints.** On the same path, connect the midpoint 7 to every vertex of $0 \ldots 15$ by an edge of weight equal to the distance, and recurse on $0 \ldots 6$ and $8 \ldots 15$. Each pair $(u, v)$ is separated by some midpoint $m$ that lies between them, and $u \to m \to v$ uses 2 hops. Leaving out the edges that already exist, this adds 23 edges, and the script checks that $d^{(2)} = d$ for all pairs. For $n = 8, 16, 32, 64$ the counts are 6, 23, 72 and 201, which grows like $n \log_2 n$. The same divide-and-conquer with separators works for trees and planar graphs.

**An approximate shortcut.** In the hub example, the 3-hop path $1 \to 0 \to 12 \to 11$ has weight $1 + 12 + 1 = 14$ against $d(1, 11) = 10$, a factor $1.4$. Allowing error lets a hopset use fewer, longer edges and still keep few hops; this is the role of $\epsilon$.

**Not a hopset.** Adding an edge $(0, 15)$ of weight 10 to the path breaks the left inequality: $d^{(1)}(0, 15) = 10 < d(0, 15) = 15$. A hopset may never make a distance shorter.

## Where it is used

- **Parallel shortest paths.** On a [PRAM](/pram-model/), one Bellman-Ford round has polylogarithmic depth. With a $(\beta, \epsilon)$-hopset, $\beta$ rounds give $(1 + \epsilon)$-approximate single-source distances in depth about $\beta$ times polylogarithmic, with work close to $|E| + |H|$. This is Cohen's application, and the reason hopsets were defined.
- **Parallel transitive closure.** The [Ullman-Yannakakis algorithm](/ullman-yannakakis/) uses sampled shortcuts to avoid squaring the adjacency matrix $\log n$ times.
- **Distributed algorithms.** In the CONGEST model, Bellman-Ford takes one round per hop, so a hopset that can be built and simulated quickly gives fast [distributed approximate SSSP](/distributed-approximate-sssp/). Elkin and Neiman list this application.
- **Dynamic and streaming algorithms.** [Decremental SSSP](/decremental-sssp/) algorithms maintain hop-limited distances, which are cheap to update, and use hopsets to make hop-limited distances approximate the true ones. Elkin and Neiman also give streaming applications.
- **Related objects.** Spanners remove edges and keep distances approximately; emulators replace the graph by a sparse weighted graph; hopsets keep the graph and add edges to bound the hop count. Distance oracles such as [Thorup-Zwick](/thorup-zwick-oracle/) are built on the same sampled hierarchies.

## References
