---
tag: 5AWK8F
kind: definition
slug: walk
name: Walk
aliases:
- edge sequence
- path (in CLRS)
area: graphs/paths-and-cycles
level: intro
summary: A sequence of vertices with consecutive pairs adjacent; vertices and edges may repeat.
prereqs: [graph, directed-and-undirected-graphs, adjacency-matrix]
see_also: [trail, simple-path, simple-cycle, counting-fixed-length-paths, eulerian-path, bipartite-odd-cycle-theorem, shortest-path, reachability]
sources:
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 3 (Connected Graphs), Section 3.1, walks, trails, paths and connection
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.3 (Paths and cycles), the definition of a walk and the remark that every walk between two vertices contains a path
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.2 (Paths, cycles, and trails), the definitions of walk, trail and path and the lemma that every u,v-walk contains a u,v-path
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), where a walk is called a path and a path with distinct vertices is called a simple path
---

A walk in a [graph](/graph/) is a sequence of vertices in which each vertex is joined to the next one by an edge, together with the edges that are used. Vertices and edges may repeat. The walk is the most general way to move through a graph: a [trail](/trail/) is a walk with no repeated edge, a [simple path](/simple-path/) is a walk with no repeated vertex, and a [simple cycle](/simple-cycle/) is a closed walk with no repeated vertex except its two ends. Walks are what powers of the [adjacency matrix](/adjacency-matrix/) count, and what a random walk or a Markov chain follows.

## Definition

Let $G = (V, E)$ be a graph, directed or undirected, possibly a [multigraph](/multigraph/) with [self-loops](/self-loop/).

**Walk.** A *walk* of length $k \ge 0$ from $v_0$ to $v_k$ is an alternating sequence

$$W = (v_0, e_1, v_1, e_2, v_2, \ldots, e_k, v_k)$$

of vertices $v_i \in V$ and edges $e_i \in E$ such that, for each $i$ with $1 \le i \le k$, the edge $e_i$ joins $v_{i-1}$ and $v_i$. In an undirected graph, the ends of $e_i$ are $v_{i-1}$ and $v_i$ in either order. In a directed graph, $e_i$ has tail $v_{i-1}$ and head $v_i$, so the walk follows the arcs in their direction.

- The *length* of $W$ is $k$, the number of edge steps, counted with repetition. The number of vertex positions is $k + 1$.
- $v_0$ is the *start* and $v_k$ is the *end*. $W$ is a $v_0$-$v_k$ walk.
- $W$ is *closed* if $k \ge 1$ and $v_0 = v_k$, and *open* otherwise.
- The *trivial walk* $(v_0)$ has length 0.

In a simple graph, the edge $e_i$ is determined by $v_{i-1}$ and $v_i$, so a walk can be written as the vertex sequence $(v_0, v_1, \ldots, v_k)$ with $v_{i-1} v_i \in E$ for each $i$. In a multigraph the edges must be listed: two walks with the same vertices that use different parallel edges are different walks.

**Operations.** If $W$ ends at $v$ and $W'$ starts at $v$, the *concatenation* $W W'$ is a walk of length $|W| + |W'|$. In an undirected graph the *reverse* $(v_k, e_k, \ldots, e_1, v_0)$ is a $v_k$-$v_0$ walk. A directed walk has no reverse in general.

**Every walk contains a path.** If $G$ has a $u$-$v$ walk, it has a $u$-$v$ [simple path](/simple-path/) whose edges are among those of the walk, and whose length is at most the length of the walk.

*Proof.* Take a $u$-$v$ walk $W$ of minimum length among the walks that use only edges of the given walk. If some vertex appeared twice, as $v_i = v_j$ with $i < j$, then deleting the part $e_{i+1}, v_{i+1}, \ldots, e_j, v_j$ would leave a $u$-$v$ walk of length $k - (j - i) < k$ on a subset of the edges, against the minimality. So no vertex repeats, and $W$ is a path. $\square$

So $v$ is [reachable](/reachability/) from $u$ by a walk exactly when it is reachable by a path, and the distance from $u$ to $v$ is the minimum length of a $u$-$v$ walk.

**Counting walks.** Let $A$ be the $n \times n$ matrix in which $A_{uv}$ is the number of edges from $u$ to $v$ (for an undirected graph, the number of edges joining $u$ and $v$, and $A_{vv}$ the number of loops at $v$). Then, for each $k \ge 0$, $(A^k)_{uv}$ is the number of walks of length $k$ from $u$ to $v$.

*Proof.* By induction on $k$. For $k = 0$, $A^0 = I$, and the only walk of length 0 from $u$ is the trivial walk at $u$. For $k \ge 1$, each walk of length $k$ from $u$ to $v$ is, in exactly one way, a walk of length $k - 1$ from $u$ to some $x$ followed by one of the $A_{xv}$ edges from $x$ to $v$. So the number is $\sum_x (A^{k-1})_{ux} A_{xv} = (A^k)_{uv}$. $\square$

With this convention, a loop counts as one step in one way. See [counting fixed-length paths](/counting-fixed-length-paths/) for algorithms based on this identity.

**Odd closed walks.** In an undirected graph, every closed walk of odd length contains a cycle of odd length. *Proof* by induction on the length $k$. A closed walk of length 1 is a loop, a cycle of length 1. Let $k \ge 3$ be odd. If no vertex repeats except $v_0 = v_k$, the walk is an odd cycle. Otherwise some $v_i = v_j$ with $0 \le i < j \le k$ and $(i, j) \ne (0, k)$, and the walk splits at that vertex into two closed walks of lengths $j - i$ and $k - (j - i)$, both shorter and with sum $k$. One of the two lengths is odd, and the induction hypothesis gives an odd cycle in it. $\square$ This is the key step of the [bipartite odd cycle theorem](/bipartite-odd-cycle-theorem/).

## Examples and non-examples

Take the undirected simple graph with vertices $0, 1, 2, 3$ and edges $01, 12, 20, 23$ (a triangle with a pendant vertex 3).

- $(0, 1, 2, 0, 1)$ is a walk of length 4. It repeats the vertices 0 and 1 and the edge $01$.
- $(2, 3, 2)$ is a closed walk of length 2. It uses the edge $23$ twice, so it is not a trail and not a cycle.
- $(0, 1, 2, 3)$ is a walk of length 3 with no repeated vertex: a path.
- $(0, 3)$ is not a walk, because $0$ and $3$ are not adjacent.
- $(1)$ is the trivial walk of length 0 at vertex 1.

The powers of the adjacency matrix count the walks. Here

$$A^3 = \begin{pmatrix} 2 & 3 & 4 & 1 \\ 3 & 2 & 4 & 1 \\ 4 & 4 & 2 & 3 \\ 1 & 1 & 3 & 0 \end{pmatrix}.$$

The entry $(A^3)_{02} = 4$ counts the walks $(0, 1, 0, 2)$, $(0, 2, 0, 2)$, $(0, 2, 1, 2)$ and $(0, 2, 3, 2)$. The entry $(A^3)_{03} = 1$ counts only $(0, 1, 2, 3)$. The diagonal entry $(A^3)_{00} = 2$ counts the triangle walked in its two directions; the trace of $A^3$ is $6$, which is $6$ times the number of triangles.

**Directed.** In the directed graph with arcs $0 \to 1$ and $1 \to 0$, $(0, 1, 0, 1, 0)$ is a closed walk of length 4. In the directed graph with only the arc $0 \to 1$, $(1, 0)$ is not a walk.

**Multigraph.** If $u$ and $v$ are joined by two parallel edges $a$ and $b$, then $(u, a, v, b, u)$ is a closed walk of length 2 that repeats no edge. With a loop $c$ at $u$, $(u, c, u)$ is a closed walk of length 1.

## Related definitions

- **Trail.** A walk with no repeated edge. See [trail](/trail/). An [Eulerian path](/eulerian-path/) is a trail that uses every edge.
- **Path.** A walk with no repeated vertex. See [simple path](/simple-path/). Many books, CLRS among them, use "path" for what this page calls a walk, and "simple path" for a path.
- **Cycle.** A closed walk with no repeated vertex except the two ends, and with the length conditions given in [simple cycle](/simple-cycle/).
- **Shortest path.** A minimum-weight walk between two vertices; with no negative cycle it can be taken to be a path. See [shortest path](/shortest-path/).
- **Reachability.** $v$ is reachable from $u$ when a $u$-$v$ walk exists. See [reachability](/reachability/).

## References
