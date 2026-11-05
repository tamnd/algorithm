---
tag: 5FKWBN
kind: concept
slug: graph-transpose
name: Graph transpose
aliases:
- Reverse graph
area: graphs/connectivity
level: intro
summary: The directed graph obtained by reversing every edge of a directed graph.
prereqs: [directed-graph]
see_also: [transpose-graph, kosaraju-sharir, strongly-connected-components, condensation-graph, strongly-connected-graph, reachability, adjacency-matrix]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1, Exercise 20.1-3 (the transpose and its construction), and Section 20.5, Strongly connected components (G and its transpose have the same strong components)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 3.5, Connectivity in directed graphs (the reversed graph and the test for strong connectivity with two searches)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2, Directed graphs (the reverse() method and the Kosaraju-Sharir algorithm)
---

The transpose of a [directed graph](/directed-graph/) $G$ is the directed graph $G^T$ on the same vertices with every edge reversed: $G^T$ has an edge $v \to u$ for each edge $u \to v$ of $G$. A path from $u$ to $v$ in $G$ is a path from $v$ to $u$ in $G^T$, so the transpose turns the question "where can I go from here?" into "who can come here?". The two graphs have the same [strongly connected components](/strongly-connected-components/), which is the key fact behind the [Kosaraju-Sharir algorithm](/kosaraju-sharir/). The construction of $G^T$ from adjacency lists, in $\Theta(n + m)$ time, is the [graph transposition](/transpose-graph/) problem.

## In plain words

Take a map of one-way streets and turn every arrow around. You get the transpose. Every road that you could drive in one direction, you can now drive only in the other direction.

A trip on the old map from one crossing to another becomes a trip on the new map that goes back from the second crossing to the first. So if you search the new map from a crossing, you find every crossing from which the old map leads to it.

A group of crossings where each one can reach each other one stays such a group after the turn, because each trip in the group has a return trip. So these groups are the same on both maps.

## The idea

Let $G = (V, E)$ be a directed graph. Parallel edges and [self-loops](/self-loop/) are allowed, so $E$ is a multiset of ordered pairs. The transpose is

$$G^T = (V, E^T), \qquad E^T = \{\, (v, u) : (u, v) \in E \,\},$$

with each edge kept with its multiplicity. A loop $(u, u)$ is its own reverse, so it stays a loop. If $A$ is the [adjacency matrix](/adjacency-matrix/) of $G$, with $A_{uv}$ the number of edges from $u$ to $v$, then the adjacency matrix of $G^T$ is the matrix transpose $A^T$, which gives the name.

These facts follow from the definition.

1. **Involution.** $(G^T)^T = G$, because reversing a pair twice gives the pair back.
2. **Degrees swap.** The out-degree of $v$ in $G^T$ is the in-degree of $v$ in $G$, and the in-degree in $G^T$ is the out-degree in $G$. The number of edges is the same.
3. **Paths reverse.** The sequence $x_0, x_1, \ldots, x_k$ is a directed walk in $G$ if and only if $x_k, \ldots, x_1, x_0$ is a directed walk in $G^T$: each step $x_{i-1} \to x_i$ of $G$ is the step $x_i \to x_{i-1}$ of $G^T$. So $v$ is reachable from $u$ in $G^T$ if and only if $u$ is reachable from $v$ in $G$. A search from $s$ in $G^T$ finds the set of vertices that can reach $s$ in $G$.
4. **Same strong components.** Two vertices $u$ and $v$ are in one strong component of $G$ when each is reachable from the other. By fact 3, this condition is the same in $G^T$, with the two paths swapped. So the partition of $V$ into strong components is the same for $G$ and $G^T$.
5. **The condensation is transposed.** The [condensation](/condensation-graph/) of $G^T$ has an edge $D \to C$ exactly when the condensation of $G$ has an edge $C \to D$, since an edge from $C$ to $D$ in $G$ becomes an edge from $D$ to $C$ in $G^T$. So a source component of $G$ is a sink component of $G^T$. Kosaraju's algorithm uses exactly this.
6. **Acyclic stays acyclic.** $G$ has a directed cycle if and only if $G^T$ has one (reverse it). A [topological order](/topological-ordering/) of a [DAG](/directed-acyclic-graph/) $G$, read backwards, is a topological order of $G^T$.
7. **Walk counts.** The number of walks of length $k$ from $u$ to $v$ in $G$ is $(A^k)_{uv}$, and $(A^T)^k = (A^k)^T$. So it equals the number of walks of length $k$ from $v$ to $u$ in $G^T$.
8. **Undirected graphs.** If each undirected edge $\{u, v\}$ is stored as the two directed edges $u \to v$ and $v \to u$, then $G^T = G$. The transpose adds nothing for undirected graphs.

**A test for strong connectivity.** Pick any vertex $s$. Then $G$ is [strongly connected](/strongly-connected-graph/) if and only if a search from $s$ reaches every vertex in $G$ and a search from $s$ reaches every vertex in $G^T$.

*Proof.* If $G$ is strongly connected, both searches reach everything, by fact 3. Conversely, suppose both searches reach everything, and let $u, v \in V$. The search in $G^T$ reached $u$, so by fact 3, $G$ has a path from $u$ to $s$. The search in $G$ reached $v$, so $G$ has a path from $s$ to $v$. Joined, these give a walk from $u$ to $v$. $\square$

The test takes two searches and one transpose, so $\Theta(n + m)$ time.

## Examples

The graph $G$ has the vertices 0 to 4 and 8 edges: $0 \to 1$, $1 \to 2$, $2 \to 0$, $1 \to 3$ twice (parallel), $3 \to 4$, $4 \to 3$, and the loop $4 \to 4$.

| vertex | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| out-list in $G$ | 1 | 2, 3, 3 | 0 | 4 | 3, 4 |
| out-list in $G^T$ | 2 | 0 | 1 | 1, 1, 4 | 3, 4 |
| out-degree in $G$ | 1 | 3 | 1 | 1 | 2 |
| out-degree in $G^T$ | 1 | 1 | 1 | 3 | 2 |

Both rows of degrees add up to 8. The loop at 4 is in both graphs, and the two parallel edges $1 \to 3$ become two parallel edges $3 \to 1$.

| start $s$ | reachable from $s$ in $G$ | reachable from $s$ in $G^T$ (the vertices that reach $s$ in $G$) |
|---|---|---|
| 0, 1 or 2 | 0, 1, 2, 3, 4 | 0, 1, 2 |
| 3 or 4 | 3, 4 | 0, 1, 2, 3, 4 |

The strong components are $C = \{0, 1, 2\}$ and $D = \{3, 4\}$ in both graphs. The condensation of $G$ has the one edge $C \to D$, and the condensation of $G^T$ has the one edge $D \to C$. The test for strong connectivity from $s = 0$ fails: the search in $G^T$ misses 3 and 4. So $G$ is not strongly connected, and indeed no path goes from 3 to 0.

**An undirected example.** The path $0 - 1 - 2$, stored as the four directed edges $0 \to 1$, $1 \to 0$, $1 \to 2$, $2 \to 1$, is equal to its transpose.

## Where it is used

- [Kosaraju-Sharir algorithm](/kosaraju-sharir/): one [depth-first search](/depth-first-search/) of $G$ for the finish times, then searches of $G^T$ in decreasing order of finish time. Each search of $G^T$ finds exactly one [strongly connected component](/strongly-connected-components/).
- [Reachability](/reachability/) backwards: the set of vertices that can reach a target, for example the states of a program that can reach an error state, or the pages that link to a page, is one search of $G^T$.
- [Bidirectional Dijkstra](/bidirectional-dijkstra/): the backward search from the target runs on the transpose.
- [Strongly connected graph](/strongly-connected-graph/): the two-search test above.
- [Transitive closure](/transitive-closure/) and [graph transposition](/transpose-graph/): the transpose of the closure is the closure of the transpose, and the transposition page covers how to build $G^T$ fast from lists, a matrix or a compressed array.

## References
