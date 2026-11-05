---
tag: G0RYGC
kind: algorithm
slug: girvan-newman-algorithm
name: Girvan-Newman algorithm
aliases:
- edge betweenness community detection
area: graphs/network-analysis
level: core
summary: Repeatedly removes the edge of highest betweenness to split the graph into communities.
solves: [community-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m^2 n), best: Ω(m n)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2002
  people: [Michelle Girvan, Mark Newman]
  note: Published in PNAS in 2002; the choice of the cut by modularity was added by Newman and Girvan in 2004.
prereqs: [community-detection, betweenness-centrality, breadth-first-search, connected-components, modularity]
see_also: [brandes-algorithm, betweenness-centrality-computation, louvain-method, leiden-algorithm, label-propagation-algorithm, walktrap-algorithm]
sources:
  - paper: doi:10.1073/pnas.122653799
    title: M. Girvan and M. E. J. Newman, Community structure in social and biological networks, Proceedings of the National Academy of Sciences 99(12), 7821 to 7826 (2002)
    locator: the algorithm (remove the edge of highest betweenness, recalculate, repeat) and the tests on Zachary's karate club and on computer-generated graphs
  - paper: doi:10.1103/PhysRevE.69.026113
    title: M. E. J. Newman and Michelle Girvan, Finding and evaluating community structure in networks, Physical Review E 69, 026113 (2004)
    locator: the fast computation of edge betweenness from each source, the need to recalculate after each removal, and the modularity Q used to choose the cut of the dendrogram
  - paper: doi:10.1080/0022250X.2001.9990249
    title: Ulrik Brandes, A faster algorithm for betweenness centrality, Journal of Mathematical Sociology 25(2), 163 to 177 (2001)
    locator: the accumulation of dependencies over the shortest-path DAG of each source, in O(nm) time for unweighted graphs
  - paper: doi:10.1016/j.physrep.2009.11.002
    title: Santo Fortunato, Community detection in graphs, Physics Reports 486(3-5), 75 to 174 (2010)
    locator: the section on divisive algorithms (the Girvan-Newman algorithm, its cost and its variants)
---

The Girvan-Newman algorithm finds [communities](/community-detection/) in a network by deleting edges. It computes the edge betweenness of every edge, the number of shortest paths between pairs of vertices that use the edge, deletes an edge with the largest value, recomputes, and repeats until no edge is left. The [connected components](/connected-components/) after each deletion form a tree of nested partitions, and the partition with the largest [modularity](/modularity/) is the answer. Edges between communities carry many shortest paths, so they go first. Each recomputation costs $O(mn)$ time on an unweighted graph, so the whole run costs $O(m^2 n)$.

## In plain words

Picture a network of friends with a few groups. The groups are dense inside, and only a few friendships cross between groups. If every person sends a message to every other person along a shortest route, the messages between groups must squeeze through those few crossing friendships. So those friendships carry the most traffic.

The algorithm counts the traffic on each friendship, cuts the busiest one, and counts again, since the traffic moves to other routes once one is cut. Every time the network falls apart into more pieces, it notes the pieces. At the end, it has a list of ever finer splits, from the whole network down to single people. It picks the split that scores best.

## The problem

The input is an undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and $m$ edges, without weights, self-loops or parallel edges. It need not be connected. The output is a partition of $V$ that is meant to have large [modularity](/modularity/) $Q$, together with the sequence of partitions, the *dendrogram*, from which it was chosen. This is a heuristic for [community detection](/community-detection/): the output is the best partition in the sequence, not the best partition overall.

The **edge betweenness** of an edge $e$ in a graph $H$ is

$$B_H(e) = \sum_{\{s, t\} \subseteq V,\ s \ne t} \frac{\sigma_{st}(e)}{\sigma_{st}},$$

where $\sigma_{st}$ is the number of shortest $s$-$t$ paths in $H$ and $\sigma_{st}(e)$ the number of those that use $e$. A pair with no path adds nothing. This is the edge form of [betweenness centrality](/betweenness-centrality/).

## The algorithm

```pseudo id=main
GIRVAN-NEWMAN(G)
L1  H ← a copy of G; P ← the components of H; levels ← [P]; best ← P
L2  while H has an edge do
L3      B ← EDGE-BETWEENNESS(H)
L4      e ← the first edge {u, v}, u < v, in lexicographic order with B[e] maximum
L5      remove e from H
L6      if H has more components than |P| then
L7          P ← the components of H; append P to levels
L8          if Q_G(P) > Q_G(best) then best ← P            ▷ modularity in the original G
L9  return best, levels

EDGE-BETWEENNESS(H)
L10 for each edge e of H do B[e] ← 0
L11 for each vertex s do
L12     BFS from s: dist[v], σ[v] (the number of shortest s-v paths), and the list S of reached vertices in BFS order
L13     for each vertex v do δ[v] ← 0
L14     for each w in S, from last to first do
L15         for each neighbour v of w with dist[v] = dist[w] − 1 do
L16             c ← σ[v] / σ[w] · (1 + δ[w]); B[{v, w}] ← B[{v, w}] + c; δ[v] ← δ[v] + c
L17 for each edge e of H do B[e] ← B[e] / 2
L18 return B
```

EDGE-BETWEENNESS is [Brandes' accumulation](/brandes-algorithm/) for edges. For a fixed source $s$, $\delta[v]$ ends as the expected number of targets $t \ne s$ whose shortest path from $s$ passes through $v$, when one shortest path is picked uniformly at random for each $t$, and $c$ is the share of that flow on the edge $\{v, w\}$. Each unordered pair is counted from both of its ends, so line L17 halves the sums.

Line L4 breaks ties by a fixed order of the edges, so the run is deterministic. Newman and Girvan stress that the betweenness must be recomputed after each removal (line L3), because paths that used the removed edge now take other edges. Removing one edge splits at most one component into two, so line L6 adds one level at a time.

## Example

Take the vertices 0 to 6 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$: a group of four and a triangle, joined by $\{3, 4\}$.

In the first round the edge betweenness is 12 for $\{3,4\}$, since all $4 \cdot 3$ pairs across use it, 6 for $\{1,3\}$ and $\{2,3\}$, 5 for $\{4,5\}$ and $\{4,6\}$, 3 for $\{0,1\}$ and $\{0,2\}$, and 1 for $\{1,2\}$ and $\{5,6\}$.

| round | edge removed | its betweenness | new partition | $Q$ |
|---|---|---|---|---|
| 0 | | | $\{0..6\}$ | 0 |
| 1 | $\{3,4\}$ | 12 | $\{0,1,2,3\}$, $\{4,5,6\}$ | $59/162 \approx 0.364$ |
| 2 | $\{0,1\}$ | 3/2, tied with 3 others | no split | |
| 3 | $\{0,2\}$ | 3 | $\{0\}$, $\{1,2,3\}$, $\{4,5,6\}$ | $41/162 \approx 0.253$ |
| 4 | $\{1,2\}$ | 1, tied with all | no split | |
| 5 | $\{1,3\}$ | 2 | $\{0\}$, $\{1\}$, $\{2,3\}$, $\{4,5,6\}$ | $23/162 \approx 0.142$ |
| 6 | $\{2,3\}$ | 1, tied | $\{0\}$, $\{1\}$, $\{2\}$, $\{3\}$, $\{4,5,6\}$ | $7/81 \approx 0.086$ |
| 7 | $\{4,5\}$ | 1, tied | no split | |
| 8 | $\{4,6\}$ | 2 | $\{5,6\}$ and singletons | $-5/81 \approx -0.062$ |
| 9 | $\{5,6\}$ | 1 | all singletons | $-4/27 \approx -0.148$ |

The best level is round 1, with $Q = 59/162$, which is also the largest modularity of all partitions of this graph. In round 2, the four edges of the group $\{0,1,2,3\}$ other than $\{1,2\}$ tie at $3/2$, and the rule of line L4 picks $\{0,1\}$.

## Correctness

Two claims make the algorithm correct. First, EDGE-BETWEENNESS returns $B_H(e)$ for every edge. For a fixed source $s$, the edges $\{v, w\}$ with $\mathrm{dist}[v] = \mathrm{dist}[w] - 1$ form the shortest-path DAG of $s$, and a shortest $s$-$t$ path uses $\{v, w\}$ in $\sigma_{sv} \cdot \sigma_{wt}^{\mathrm{DAG}}$ ways. Brandes' recursion

$$\delta_s(v) = \sum_{w : v \to w \text{ in the DAG}} \frac{\sigma_{sv}}{\sigma_{sw}} \big(1 + \delta_s(w)\big)$$

holds, the reverse BFS order of line L14 finishes every $\delta[w]$ before it is used, and the edge term $c$ equals $\sum_{t} \sigma_{st}(\{v,w\})/\sigma_{st}$. Second, the main loop keeps the invariant that $P$ is the set of components of $H$ and $levels$ lists, in order, every distinct component partition seen so far, with $best$ the first one of largest modularity. The loop removes one edge per round, so it stops after exactly $m$ rounds. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **One betweenness computation.** For each source, the BFS of line L12 and the loop of lines L14 to L16 scan each edge a constant number of times, so they take $O(n + m)$. Over $n$ sources this is $O(n(n + m))$, which is $O(mn)$ when every vertex has an edge.
- **The whole run.** Line L3 runs once per removed edge, so $m$ times. The total is $O(m \cdot n(n + m))$, which is $O(m^2 n)$ for graphs without isolated vertices, and $O(n^3)$ for sparse graphs with $m = O(n)$. The components and the modularity in lines L6 to L8 take $O(n + m)$ per round, which does not change the bound.
- **Best case.** Each round still runs a full betweenness computation, so the time is $\Omega(mn)$ on any graph where every vertex has an edge.
- **Weighted graphs.** With edge lengths, line L12 becomes [Dijkstra's algorithm](/dijkstra/) with path counts, and the bound becomes $O(m n (m + n \log n))$.
- **Space.** The copy $H$, the arrays $\mathrm{dist}$, $\sigma$, $\delta$ and the map $B$ take $\Theta(n + m)$ words. The list $levels$ holds up to $n$ partitions, $O(n^2)$ words if they are all kept; storing only the order of the splits keeps it at $O(n)$.
- **Number sizes.** The counts $\sigma[v]$ can be exponential in $n$, so they need about $n$ bits in the worst case. Floating-point betweenness makes the tie test of line L4 fragile; exact rationals, as in the implementation, or a tolerance avoid this.

## Properties

- **Divisive and hierarchical.** It produces a full dendrogram, not one partition, so the scale of the communities can be chosen afterwards.
- **Deterministic.** With the tie rule of line L4, the output is a function of the graph and its numbering. Other tie rules can give other dendrograms.
- **Recomputation is essential.** Computing the betweenness once and removing edges in that order gives worse results; Newman and Girvan report that the recalculation step is essential.
- **Respects components.** It never puts two components of $G$ in one group, since line L1 starts from the components.
- **Slow.** Its cost limits it to graphs of a few thousand vertices.

## Variants and improvements

- **Recompute only the split component.** After removing $e$, only the betweenness inside the component that held $e$ changes, so line L3 can run on that component only. This helps in practice but not in the worst case.
- **Other edge scores.** Random-walk betweenness and current-flow betweenness, proposed in the 2004 paper, and the edge clustering coefficient of Radicchi and co-authors, which counts the triangles that contain an edge and is much faster to compute.
- **Approximate betweenness.** Sampling sources gives an estimate of $B$ in a fraction of the time, at the cost of a less exact choice of edge.
- **Directed and weighted graphs.** The definitions carry over, with directed BFS or Dijkstra in line L12.

## When to use it

Use it on small networks, up to a few thousand vertices, when a full hierarchy of splits is wanted and the result must be easy to explain: each cut is justified by a count of shortest paths. For larger graphs, or when only one good partition is needed, use the [Louvain method](/louvain-method/) or the [Leiden algorithm](/leiden-algorithm/), which optimize modularity directly in close to linear time, or [label propagation](/label-propagation-algorithm/), which is faster still.

## Pitfalls

- **Not recomputing.** Line L3 must run inside the loop. Computing $B$ once before the loop and removing edges in the order of those values gives a different, poorer dendrogram.
- **Counting each pair twice.** Summing over all sources counts the pair $\{s, t\}$ from $s$ and from $t$. Without line L17 every value is doubled. The order does not change, but values reported against the definition are wrong.
- **Choosing the cut by the number of groups.** The algorithm says nothing about the right number of communities. Line L8 picks the level by modularity in the original graph $G$, not in the current $H$; computing $Q$ in $H$ gives values that grow as edges disappear and mean nothing.
- **Floating-point ties.** In the example, four edges tie at $3/2$ in round 2. With floating-point sums, rounding can make one of them look larger, and the run then depends on the order of the arithmetic.

## Implementations

## History

Michelle Girvan and Mark Newman proposed the method in 2002, as a divisive alternative to the agglomerative hierarchical clustering then used in sociology, and tested it on Zachary's karate club network, where it recovers the split of the club almost exactly. In 2004 Newman and Girvan gave the faster computation of edge betweenness, other betweenness measures, and the modularity $Q$ for choosing where to cut the dendrogram, which became the most used objective of community detection.

## References
