---
tag: J9FYN4
kind: definition
slug: cut
name: Cut
area: graphs/flows-and-cuts
level: intro
summary: Partition of a graph's vertices into two disjoint sets, used to reason about crossing edges in spanning trees and flows.
prereqs: [graph, directed-graph]
see_also: [cut-capacity, flow-network, min-cut-problem, global-min-cut-problem, cut-property, max-flow-min-cut-theorem, edge-connectivity, vertex-cut]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 21.1 (cuts, crossing edges and light edges for minimum spanning trees) and Section 24.2 (cuts of flow networks)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5 (the cut property of minimum spanning trees), Section 7.2 (s-t cuts) and Section 13.2 (the global minimum cut)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (s-t cuts)
---

A cut of a graph is a split of its vertex set into two nonempty parts $S$ and $V \setminus S$; the edges with one end in each part *cross* the cut. In a [flow network](/flow-network/), an *s-t cut* is a cut with the source $s$ in $S$ and the sink $t$ in $V \setminus S$, and its [capacity](/cut-capacity/) bounds the value of every flow. Cuts are the dual object of paths: a set of edges meets every path from $s$ to $t$ exactly when it contains the edges that leave some s-t cut, and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) turns this into an equality of numbers.

## Definition

Let $G = (V, E)$ be a [graph](/graph/), directed or undirected, with $V$ finite.

**Cut.** A *cut* is an ordered pair $(S, \bar S)$ with $\emptyset \ne S \subsetneq V$ and $\bar S = V \setminus S$. In an undirected graph, $(S, \bar S)$ and $(\bar S, S)$ are usually seen as the same cut. Some texts call the set $S$ itself the cut, and some call the set of crossing edges the cut; this site says *cut* for the partition and *cut set* for the edges.

**Crossing edges.** In an undirected graph, the cut set is

$$\delta(S) = \{\, \{u, v\} \in E : u \in S,\ v \notin S \,\}.$$

In a directed graph, the edges that leave $S$ and the edges that enter $S$ are

$$\delta^{+}(S) = \{(u, v) \in E : u \in S,\ v \notin S\}, \qquad \delta^{-}(S) = \{(u, v) \in E : u \notin S,\ v \in S\} = \delta^{+}(\bar S).$$

An edge *crosses* the cut if it lies in $\delta(S)$, or in $\delta^+(S) \cup \delta^-(S)$ for a directed graph. A self-loop never crosses a cut. Two antiparallel edges $(u, v)$ and $(v, u)$ with $u \in S$ and $v \notin S$ are in different sets: the first in $\delta^+(S)$, the second in $\delta^-(S)$.

**s-t cut.** For two distinct vertices $s$ and $t$, an *s-t cut* is a cut with $s \in S$ and $t \in \bar S$. The set $S$ is the *source side* and $\bar S$ the *sink side*. A graph with $n$ vertices has $2^{n-2}$ s-t cuts, one for each subset of $V \setminus \{s, t\}$ that joins $s$.

**Global cut.** With no named vertices, a graph with $n \ge 2$ vertices has $2^n - 2$ ordered cuts and $2^{n-1} - 1$ unordered ones. The [global minimum cut problem](/global-min-cut-problem/) searches over all of them.

**Cuts and paths.** Let $s \ne t$ in a directed graph. (1) For each s-t cut $(S, \bar S)$, every directed path from $s$ to $t$ uses an edge of $\delta^+(S)$: the path starts in $S$ and ends outside $S$, so at the first step where it leaves $S$ it uses an edge from $S$ to $\bar S$. (2) Conversely, if a set $F \subseteq E$ meets every path from $s$ to $t$, let $S$ be the set of vertices that $s$ reaches in $G - F$. Then $t \notin S$, and each edge $(u, v)$ with $u \in S$, $v \notin S$ is in $F$ (else $v$ would be reachable). So $\delta^+(S) \subseteq F$. Every minimal set of edges that meets all paths from $s$ to $t$ is therefore of the form $\delta^+(S)$ for an s-t cut.

**Capacity.** With edge weights or capacities $c$, the capacity of a directed cut counts only the edges that leave $S$: $c(S, \bar S) = \sum_{e \in \delta^+(S)} c(e)$. The page [cut capacity](/cut-capacity/) treats it.

## Examples and non-examples

**The running network.** In the [flow network](/flow-network/) with edges $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10 there are $2^{6 - 2} = 16$ s-t cuts. Three of them:

| source side $S$ | $\delta^+(S)$ | $\delta^-(S)$ |
|---|---|---|
| $\{s\}$ | $s a$, $s c$ | none |
| $\{s, c\}$ | $s a$, $c d$ | $a c$ |
| $\{s, a, c\}$ | $a b$, $a d$, $c d$ | none |

For $S = \{s, c\}$, the edge $a c$ goes from the sink side to the source side, so it is in $\delta^-(S)$ and does not count in the capacity, which is $10 + 9 = 19$.

**A graph where $t$ is unreachable.** In $s \to a$, $t \to a$, the cut $S = \{s, a\}$ has $\delta^+(S) = \emptyset$ and $\delta^-(S) = \{(t, a)\}$. An s-t cut with no leaving edge exists exactly when no directed path goes from $s$ to $t$, by fact (2) above with $F = \emptyset$.

**Undirected example.** In the cycle $1 - 2 - 3 - 4 - 1$, the cut $S = \{1, 2\}$ has $\delta(S) = \{\{2, 3\}, \{4, 1\}\}$, and $S = \{1, 3\}$ has all four edges in $\delta(S)$. Every cut of a cycle has an even number of crossing edges, because a closed walk crosses from $S$ to $\bar S$ as often as back.

**Minimum spanning trees.** The [cut property](/cut-property/) says that, for each cut of a connected weighted undirected graph, a crossing edge of least weight belongs to some minimum spanning tree. Here the cut needs no $s$ or $t$.

**Non-example: $S = \emptyset$ or $S = V$.** These are not cuts. No edge crosses them, and allowing them would make the minimum cut always 0.

**Non-example: a set of edges that is not a cut set.** In the running network, $F = \{s a, d t\}$ meets the path $s\,a\,b\,t$ but not $s\,c\,d\,b\,t$, so it does not separate $s$ from $t$. Removing $F$ leaves $t$ reachable, so $F$ contains no set $\delta^+(S)$ of an s-t cut.

**Non-example: a vertex cut.** A set of vertices whose removal separates $s$ from $t$ is a [vertex cut](/vertex-cut/), a different object. It is reduced to an edge cut by splitting each vertex into an in-copy and an out-copy.

## Related definitions

- The [capacity of a cut](/cut-capacity/) is the total capacity of $\delta^+(S)$.
- The [minimum s-t cut problem](/min-cut-problem/) asks for an s-t cut of least capacity; the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) equates it with the maximum flow value.
- The [global minimum cut problem](/global-min-cut-problem/) and its [directed form](/directed-global-min-cut-problem/) drop $s$ and $t$.
- The [edge connectivity](/edge-connectivity/) of an undirected graph is the least size of $\delta(S)$ over all cuts.
- The [cut property](/cut-property/) uses cuts to prove the greedy algorithms for minimum spanning trees.
- A [Gomory-Hu tree](/gomory-hu-tree/) stores a minimum s-t cut for every pair of vertices of an undirected graph.

## References
