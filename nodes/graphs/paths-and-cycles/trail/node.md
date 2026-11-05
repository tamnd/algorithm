---
tag: PGBVSF
kind: definition
slug: trail
name: Trail
aliases:
- edge-simple path
- closed trail
- circuit
area: graphs/paths-and-cycles
level: intro
summary: A walk that uses no edge more than once; vertices may repeat.
prereqs: [walk, multigraph, degree]
see_also: [walk, simple-path, simple-cycle, eulerian-path, eulerian-circuit, hierholzer-algorithm, eulers-theorem-eulerian-graphs, chinese-postman-problem]
sources:
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 3 (Connected Graphs), Section 3.1 (walks and trails) and Section 3.3 (Euler tours)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.2 (Paths, cycles, and trails), the definitions of trail and circuit, and the decomposition of an even graph into cycles
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.8 (Euler tours)
---

A trail is a [walk](/walk/) in a graph that uses each edge at most once; it may pass through a vertex many times. Trails are the objects of Euler's problem: an [Eulerian path](/eulerian-path/) is a trail that uses every edge, and an [Eulerian circuit](/eulerian-circuit/) is a closed one. Every [simple path](/simple-path/) is a trail, but a trail can return to a vertex, as a figure eight does at its crossing. The parity of the degrees decides which trails can exist, and this is the base of [Euler's theorem](/eulers-theorem-eulerian-graphs/).

## Definition

Let $G = (V, E)$ be a graph, directed or undirected, possibly a [multigraph](/multigraph/) with [self-loops](/self-loop/).

**Trail.** A *trail* is a walk $W = (v_0, e_1, v_1, \ldots, e_k, v_k)$ whose edges $e_1, \ldots, e_k$ are pairwise distinct: $e_i \ne e_j$ for $1 \le i < j \le k$. Its length is $k$. In a directed graph, each $e_i$ is an arc from $v_{i-1}$ to $v_i$.

**Closed trail.** A trail with $k \ge 1$ and $v_0 = v_k$. Many books call it a *circuit*, but CLRS and others use "circuit" for a cycle, so this page avoids the word.

Since edges are compared, and not vertex pairs, two parallel edges $a \ne b$ between $u$ and $v$ may both be used: $(u, a, v, b, u)$ is a closed trail of length 2. A self-loop at $v$ can be used once, and it adds 2 to the count of trail edges at $v$.

**Degree parity.** For a trail $T$, let $d_T(x)$ be the number of edge ends at $x$ among the edges of $T$, with a loop counted twice.

- If $T$ is closed, $d_T(x)$ is even for every vertex $x$.
- If $T$ is open with $v_0 \ne v_k$, then $d_T(v_0)$ and $d_T(v_k)$ are odd and $d_T(x)$ is even for every other $x$.

*Proof.* Walk along $T$. Each position $i$ with $0 < i < k$ is entered by $e_i$ and left by $e_{i+1}$, and these are two different edges of $T$. So each interior position adds 2 to $d_T(v_i)$. The position $0$ adds 1 to $d_T(v_0)$ (the edge $e_1$) and the position $k$ adds 1 to $d_T(v_k)$ (the edge $e_k$). Each edge end of $T$ is counted at exactly one position, because the edges are distinct. If $v_0 = v_k$, the two single counts go to the same vertex and its total is even. If $v_0 \ne v_k$, each of them gets one odd contribution. $\square$

For a directed trail, the same count gives: each interior position adds one arc in and one arc out, so in a closed directed trail each vertex has as many trail arcs in as out, and in an open one $v_0$ has one more out than in and $v_k$ one more in than out.

These are the necessary conditions of [Euler's theorem](/eulers-theorem-eulerian-graphs/): a trail that uses all edges forces the parities on the whole graph.

**Closed trails split into cycles.** The edge set of each closed trail is the union of edge-disjoint [simple cycles](/simple-cycle/). *Proof* by induction on the length $k$. If no vertex repeats except $v_0 = v_k$, the trail is a cycle. Otherwise some $v_i = v_j$ with $0 \le i < j \le k$ and $(i, j) \ne (0, k)$. The trail splits at this vertex into two closed trails with disjoint edge sets, both shorter, and the induction hypothesis applies to each. $\square$

**Every trail contains a path.** By the result on the [walk](/walk/) page, each $u$-$v$ trail contains a $u$-$v$ [simple path](/simple-path/) made of some of its edges.

## Examples and non-examples

**The bowtie.** Take two triangles $0, 1, 2$ and $2, 3, 4$ that share the vertex 2, so the edges are $01, 12, 20, 23, 34, 42$.

- $(0, 1, 2, 3, 4, 2, 0)$ is a closed trail of length 6. It passes through 2 twice, so it is not a cycle, and it uses all six edges, so it is an Eulerian circuit. Every vertex has $d_T(x)$ even: $d_T(2) = 4$, the others 2.
- $(1, 2, 3, 4, 2)$ is an open trail of length 4 from 1 to 2. Here $d_T(1) = 1$ and $d_T(2) = 3$, both odd, and $d_T(3) = d_T(4) = 2$.
- $(0, 1, 2, 0, 1)$ is a walk but not a trail: it uses the edge $01$ twice.

**A path is a trail.** $(0, 1, 2, 3)$ repeats nothing, so it is a trail and a path.

**Directed.** In the directed graph with arcs $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $3 \to 2$, the sequence $(0, 1, 2, 3, 2, 0)$ is a closed directed trail that uses all five arcs. The vertex 2 has 2 trail arcs in and 2 out.

**Multigraph.** With two parallel edges $a, b$ between $u$ and $v$ and a loop $c$ at $v$, the sequence $(u, a, v, c, v, b, u)$ is a closed trail of length 3 that uses every edge. Its counts are $d_T(u) = 2$ and $d_T(v) = 4$.

**Non-example from parity.** The star with centre 0 and leaves 1, 2, 3 has three vertices of degree 1. A trail has at most two vertices of odd count, so no trail uses all three edges. The longest trails, such as $(1, 0, 2)$, have length 2.

## Related definitions

- **Walk.** A trail is a walk with no repeated edge. See [walk](/walk/).
- **Path.** A trail with no repeated vertex. See [simple path](/simple-path/). Every path is a trail; the bowtie trail above is a trail that is not a path.
- **Cycle.** A closed trail with no repeated vertex except its ends. See [simple cycle](/simple-cycle/).
- **Eulerian path and circuit.** A trail, or closed trail, that uses every edge of the graph. See [Eulerian path](/eulerian-path/), [Eulerian circuit](/eulerian-circuit/) and [Hierholzer's algorithm](/hierholzer-algorithm/), which builds one in linear time by joining closed trails.
- **Chinese postman.** When no Eulerian circuit exists, the [Chinese postman problem](/chinese-postman-problem/) asks for a shortest closed walk that uses every edge at least once; it is a closed trail in the graph with some edges doubled.

## References
