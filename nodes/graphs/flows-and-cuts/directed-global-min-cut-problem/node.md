---
tag: W4R1ST
kind: problem
slug: directed-global-min-cut-problem
name: Directed global minimum cut problem
aliases:
- directed min cut
- arc connectivity
area: graphs/flows-and-cuts
level: advanced
summary: Find a minimum cut in a directed graph over all choices of source and sink.
prereqs: [global-min-cut-problem, min-cut-problem, max-flow-min-cut-theorem]
see_also: [hao-orlin, strongly-connected-components, edmonds-arborescence, push-relabel, edge-connectivity, arborescence]
sources:
  - paper: doi:10.1006/jagm.1994.1043
    title: Jianxiu Hao and James B. Orlin, A faster algorithm for finding the minimum cut in a directed graph, Journal of Algorithms 17(3), 424 to 446 (1994)
    locator: the whole paper (the reduction to 2(n - 1) cut problems and their solution in one push-relabel run)
  - paper: doi:10.1006/jcss.1995.1022
    title: Harold N. Gabow, A matroid approach to finding edge connectivity and packing arborescences, Journal of Computer and System Sciences 50(2), 259 to 273 (1995)
    locator: the arc connectivity algorithm for directed graphs with unit capacities
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 6, Maximum Flows, Basic Ideas (network connectivity) and Chapter 8, Maximum Flows, Additional Topics (the minimum cut of a network)
---

The directed global minimum cut problem asks, for a directed graph with nonnegative capacities, for a nonempty proper set $S$ of vertices that minimizes the total capacity of the edges leaving $S$. Unlike the undirected [global minimum cut](/global-min-cut-problem/), a set and its complement give different values, so the problem must look at both orientations. Its value is 0 exactly when the graph is not strongly connected, and with unit capacities it is the *arc connectivity*. The standard solution reduces it to $2(n - 1)$ [minimum s-t cuts](/min-cut-problem/), and the [Hao-Orlin algorithm](/hao-orlin/) solves all of them in the time of one maximum flow.

## In plain words

A city has one-way streets, each with a capacity. You want the cheapest set of streets to close so that some part of the city can no longer drive out to the rest. Any part counts, as long as it is not empty and not the whole city.

Because streets are one-way, closing the exits from a district is not the same as closing its entrances. So it is not enough to look at splits of the city; you must also say which side is cut off from which. Pick any one corner of the city. In the best answer it is either inside the trapped part or outside it. So try every other corner as the partner, in both directions, with a minimum cut each time, and keep the cheapest.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n \ge 2$ vertices, $m$ edges, and capacities $c(e) \ge 0$. Capacities may be reals; unit capacities give arc connectivity, an integer case. Antiparallel edges $(u, v)$ and $(v, u)$ are separate edges and can lie on opposite sides of a cut, so only the one leaving $S$ counts. Parallel edges add up and self-loops never cross a cut.

**Output.** A set $S$ with $\emptyset \ne S \subsetneq V$ minimizing
$$c(\delta^{\text{out}}(S)) = \sum_{(u, v) \in E,\ u \in S,\ v \notin S} c(u, v),$$
and the value $\lambda(G)$.

**Relation to s-t cuts.** For an ordered pair $(s, t)$ let $\lambda(s, t)$ be the minimum s-t cut. Then $\lambda(G) = \min_{s \ne t} \lambda(s, t)$. For any fixed vertex $v$, an optimal $S$ either contains $v$, and then it is an s-t cut for $s = v$ and some $t \notin S$, or it does not, and then it is an s-t cut for $t = v$ and some $s \in S$. So
$$\lambda(G) = \min\left(\min_{t \ne v} \lambda(v, t),\ \min_{s \ne v} \lambda(s, v)\right).$$

**Undirected graphs as a special case.** An undirected graph with each edge replaced by two antiparallel arcs of the same capacity has $c(\delta^{\text{out}}(S)) = c(\delta^{\text{out}}(V \setminus S))$, and the problem becomes the undirected one.

## Variants

- **Arc connectivity.** With unit capacities, $\lambda(G)$ is the largest $k$ such that $G$ stays strongly connected after deleting any $k - 1$ edges.
- **Rooted connectivity.** For a fixed root $r$, $\min_{t \ne r} \lambda(r, t)$. By Edmonds' branching theorem it equals, for integer capacities, the largest number of edge-disjoint spanning [arborescences](/arborescence/) rooted at $r$, counted with capacities. Then $\lambda(G)$ is the smaller of the rooted connectivity at $r$ in $G$ and in the graph with all edges reversed.
- **Vertex version.** The fewest vertices whose removal destroys strong connectivity; solved by flows with vertex capacities.
- **Strong connectivity test.** $\lambda(G) > 0$ if and only if $G$ is strongly connected, which [strongly connected components](/strongly-connected-components/) decide in $O(n + m)$ time.

## Examples

**The running network with a return edge.** Take $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10 and add $t s$ with capacity 15, so that the graph is strongly connected. Checking all 62 nonempty proper subsets gives $\lambda(G) = 9$, with $S = \{c\}$: the only edge leaving $c$ is $c d$. The complement $V \setminus \{c\}$ has the edges $s c$ and $a c$ leaving it, of capacity 12, so the two orientations differ. With $v = s$, the rooted value $\min_t \lambda(s, t)$ is only 10 (the set $\{s, a, c, d, t\}$ with exits $a b$ and $d b$), and the minimum comes from the other direction, $\lambda(c, s) = 9$. A method that looks only at cuts with $s$ inside would answer 10.

**Not strongly connected.** Without the edge $t s$, the vertex $t$ has no outgoing edge, so $S = \{t\}$ has $c(\delta^{\text{out}}(S)) = 0$ and $\lambda(G) = 0$. Also $\lambda(t, s) = 0$: there is no path from $t$ to $s$.

**Zero-capacity edges.** An edge of capacity 0 counts as missing; a graph that is strongly connected only through such edges has $\lambda(G) = 0$.

**A directed cycle.** The directed cycle $C_n$ with unit capacities has $\lambda = 1$, and every nonempty proper set whose vertices form a contiguous run is optimal.

## Known algorithms

- **$2(n - 1)$ maximum flows.** Fix $v$, and compute $\lambda(v, t)$ and $\lambda(t, v)$ for each $t \ne v$ with any maximum flow algorithm.
- **[Hao-Orlin](/hao-orlin/).** Computes $\min_t \lambda(v, t)$ over a changing sink in one run of [push-relabel](/push-relabel/), in $O(nm \log(n^2/m))$ time; a second run on the reversed graph gives the other direction.
- **Unit capacities.** Gabow's matroid method finds the arc connectivity $\lambda$ in $O(\lambda m \log(n^2/m))$ time, by packing arborescences.
- **Faster flows.** With the $m^{1 + o(1)}$ maximum flow algorithm, the $2(n - 1)$ flow reduction takes $n m^{1 + o(1)}$ time. Since 2021 several randomized algorithms do better on dense or weighted directed graphs by sparsifying first; their exact bounds differ by model.

The contraction methods of Karger and the maximum adjacency method of [Stoer-Wagner](/stoer-wagner/) do not work for directed graphs: both rely on the symmetry $c(\delta(S)) = c(\delta(V \setminus S))$.

## Bounds

The Hao-Orlin bound $O(nm \log(n^2/m))$ is the time of one push-relabel maximum flow. For unit capacities, Gabow's $O(\lambda m \log(n^2/m))$ is better when $\lambda$ is small. The trivial lower bound is $\Omega(n + m)$.

## Reductions

- **To $2(n - 1)$ s-t minimum cuts**, as above.
- **From the undirected global minimum cut**, by replacing each edge by two arcs.
- **To rooted arc connectivity**, at a root and in the reversed graph, and from there to arborescence packing by Edmonds' theorem.
- **Strong connectivity** is the question $\lambda(G) > 0$.

## Applications

Reliability of one-way networks such as road systems and data links, the arc connectivity of directed communication graphs, and the separation step for cutting plane methods on the asymmetric traveling salesman problem, where a violated subtour constraint is a directed cut of capacity below 1.

## References
