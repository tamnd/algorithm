---
tag: VS4KBS
kind: model
slug: pregel-model
name: Pregel vertex-centric model
aliases:
- Pregel
- vertex-centric programming
- think like a vertex
area: parallel/mapreduce-and-bsp
level: advanced
summary: A BSP model for graph computation. In each superstep every active vertex runs one function on the messages it received, changes its value, sends messages for the next superstep and may vote to halt.
history:
  year: 2010
  people: [Grzegorz Malewicz, Matthew H. Austern, Aart J. C. Bik, James C. Dehnert, Ilan Horn, Naty Leiser, Grzegorz Czajkowski]
  note: Malewicz et al. described Pregel, the graph system of Google, at SIGMOD 2010.
prereqs: [bsp-model, superstep, bellman-ford]
see_also: [gas-model, pagerank, single-source-shortest-paths, distributed-pagerank, distributed-connected-components, iterative-mapreduce, combiner, round-complexity]
sources:
  - paper: doi:10.1145/1807167.1807184
    title: "Grzegorz Malewicz, Matthew H. Austern, Aart J. C. Bik, James C. Dehnert, Ilan Horn, Naty Leiser and Grzegorz Czajkowski, Pregel: a system for large-scale graph processing, SIGMOD 2010"
    locator: pp. 135-146; Section 2 (the model, voting to halt, the maximum value example), Section 3 (combiners and aggregators), Section 4.2 (checkpoints), Section 5.1 (PageRank) and Section 5.2 (shortest paths)
  - paper: doi:10.1145/79173.79181
    title: "Leslie G. Valiant, A bridging model for parallel computation, Communications of the ACM 33(8), 1990"
    locator: pp. 103-111, the BSP model that Pregel follows
  - book: isbn:9781108476348
    title: "Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020"
    locator: Chapter 2, extensions of MapReduce, including Pregel
---

Pregel is a model and a system for computing on large graphs, described by Malewicz and others at Google in 2010. A computation is a sequence of [supersteps](/superstep/), as in the [BSP model](/bsp-model/). In each superstep, every active vertex runs the same user function on the messages sent to it in the previous superstep; the function may change the value of the vertex, send messages to other vertices and vote to halt. The programmer writes code for one vertex, which is why the style is called "think like a vertex".

## The machine

The notation follows the parallel pages of this site. The input is a directed graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, stored on $p$ workers.

| Symbol | Meaning |
|---|---|
| $n$, $m$ | the number of vertices and of edges |
| $p$ | the number of workers (processors) |
| $S$ | the number of supersteps |
| $W$, $H$ | the sums over supersteps of the largest work and of the h-relation of a worker |
| $g$, $L$ | the BSP cost of one word and of one barrier |

Each vertex has a unique identifier, a value that the program can change, and a list of out-edges, each with a target identifier and a value. A vertex is active or inactive. In superstep $0$ all vertices are active.

In superstep $s$, the system calls the user function `compute` once for each vertex that is active or has received a message; a message makes an inactive vertex active again. The call may:

- read the messages sent to the vertex in superstep $s - 1$;
- read and change the value of the vertex and of its out-edges;
- send messages to any vertex whose identifier it knows, usually its out-neighbours; they arrive in superstep $s + 1$;
- add a value to an aggregator, a global reduction (such as a sum or a minimum) whose result all vertices can read in superstep $s + 1$;
- ask for changes of the graph (adding or removing vertices or edges), which take effect in superstep $s + 1$;
- vote to halt, which makes the vertex inactive.

The computation ends when every vertex is inactive and no message is in transit. The output is the set of vertex values.

A combiner is an optional user function that merges several messages to the same vertex into one, for example by taking their minimum or their sum. The system may apply it on the sending worker, so it must be commutative and associative, and the program must give the same result with or without it.

The system splits the vertices among the workers, by default by a hash of the identifier mod the number of partitions. A master coordinates the barrier. For fault tolerance, the workers save their state at the start of some supersteps (a checkpoint); after a failure, the lost partitions restart from the last checkpoint.

## What it counts

A Pregel program is a BSP program on the $p$ workers, so it costs

$$
T = W + g\,H + S\,L.
$$

In superstep $s$, the work $w_s$ of a worker is the number of `compute` calls on its vertices plus the number of messages they read, and $h_s$ is the largest number of messages that one worker sends to or receives from other workers, after the combiner. The usual measures of a Pregel algorithm are therefore:

- the number of supersteps $S$, since each costs a barrier and, on a real cluster, a round of network latency;
- the number of messages per superstep, which sets $H$;
- the balance of the work, since a vertex of high degree makes its worker the slowest one.

The simulator of this page places vertex $v$ on worker $v \bmod p$ and records $w_s$, $h_s$ and the number of messages and active vertices in each superstep. It counts aggregator traffic separately: an aggregator adds about $p$ words and no extra superstep.

## Relation to other models

- [BSP](/bsp-model/). Pregel is BSP with the processors replaced by vertices. Several vertices share a worker, and the cost is BSP cost on the workers.
- [MapReduce](/mapreduce-model/). A graph algorithm in [iterative MapReduce](/iterative-mapreduce/) must read and write the whole graph in every round, because a reduce function keeps no state between jobs. Pregel keeps each vertex and its edges on one worker for the whole computation, and sends only the messages.
- [Gather-apply-scatter](/gas-model/). The GAS model of PowerGraph splits the vertex function into three phases and splits high-degree vertices over several machines (a vertex cut). It can express Pregel-style programs and balances work better on graphs with a few very high-degree vertices.
- Distributed graph algorithms. If each vertex sends only to its neighbours, a superstep is a round of a synchronous message-passing network on the graph itself, so [round complexity](/round-complexity/) bounds from distributed computing carry over to the number of supersteps. Pregel does not limit message size, which makes it closer to the LOCAL model than to CONGEST.

## Known results in the model

### Single-source shortest paths

The program of Section 5.2 of the paper: the value of each vertex starts at $\infty$. In each superstep a vertex takes the minimum $d$ of its messages (and $0$ for the source $s$ in superstep $0$); if $d$ is less than its value, it sets its value to $d$ and sends $d + w(v, u)$ to each out-neighbour $u$. Then it votes to halt. A min combiner is safe.

For $k \ge 0$, let $d_k(v)$ be the least weight of a walk from $s$ to $v$ with at most $k$ edges ($\infty$ if there is none).

**Claim.** After superstep $k$, the value of every vertex $v$ is $d_k(v)$, and in superstep $k$ exactly the vertices with $d_k(v) < d_{k-1}(v)$ send messages (with $d_{-1} = \infty$).

*Proof.* By induction on $k$. In superstep $0$ only $s$ changes, to $0 = d_0(s)$, and every other value stays $\infty = d_0(v)$. Assume the claim for $k$. In superstep $k + 1$, vertex $v$ receives $d_k(u) + w(u, v)$ from each in-neighbour $u$ with $d_k(u) < d_{k-1}(u)$, so its new value is the minimum of $d_k(v)$ and these sums. By definition, $d_{k+1}(v) = \min\left(d_k(v), \min_u \left(d_k(u) + w(u, v)\right)\right)$ over all in-neighbours $u$. For an in-neighbour $u$ that did not change in superstep $k$, $d_k(u) = d_{k-1}(u)$, and $d_{k-1}(u) + w(u, v) \ge d_k(v)$ because a walk to $u$ with at most $k - 1$ edges plus the edge $(u, v)$ is a walk to $v$ with at most $k$ edges. So the missing messages do not change the minimum, the new value is $d_{k+1}(v)$, and $v$ sends exactly when its value drops. $\square$

So the program is a synchronous [Bellman-Ford](/bellman-ford/). If no negative cycle is reachable from $s$, then $d_k = \delta(s, \cdot)$ for $k \ge n - 1$, and the run ends. Let $h(v)$ be the last superstep in which $v$ changes; it is the least number of edges of a shortest path from $s$ to $v$. If $s$ has an out-edge, the run takes exactly $S = H + 2$ supersteps, where $H$ is the largest $h(v)$ over reachable vertices $v$ that have an out-edge: the last messages are sent in superstep $H$, read in superstep $H + 1$, and cause no change. Each vertex sends in at most $h(v) + 1$ supersteps, so at most $(H + 1)m \le nm$ messages are sent in all. Against [Dijkstra's algorithm](/dijkstra/), which takes $O(m + n \log n)$ time on one processor, Pregel does more work but needs only about as many supersteps as there are edges on a shortest path.

Example: the edges $0 \to 1$ (weight 4), $0 \to 2$ (1), $2 \to 1$ (2), $1 \to 3$ (1) and $2 \to 3$ (5), with source $0$.

| Superstep | Messages read | Values after the superstep |
|---|---|---|
| 0 | none | $0, \infty, \infty, \infty$ |
| 1 | $1 \leftarrow 4$, $2 \leftarrow 1$ | $0, 4, 1, \infty$ |
| 2 | $1 \leftarrow 3$, $3 \leftarrow 5$, $3 \leftarrow 6$ | $0, 3, 1, 5$ |
| 3 | $3 \leftarrow 4$ | $0, 3, 1, 4$ |

Vertex $1$ last changes in superstep $2$ and has an out-edge, so $H = 2$ and the run has $4$ supersteps. The answer equals the distances found by Dijkstra's algorithm.

The paper reports that a min combiner cuts the number of messages of this program by more than a factor of four on its test graphs (Section 3.2).

### PageRank

The program of Section 5.1 of the paper: in superstep $0$ each vertex holds $1/n$. In each later superstep a vertex sets its value to $(1 - \alpha)/n + \alpha \sum$ (its messages), with follow probability $\alpha = 0.85$, and then, while the number of iterations is not reached, sends its value divided by its out-degree along each out-edge. The paper stops after 30 supersteps.

With $k$ iterations the run has exactly $k + 1$ supersteps, and after superstep $t$ the values equal $t$ steps of the [power iteration](/power-iteration/) for [PageRank](/pagerank/), by induction on $t$: a vertex's messages in superstep $t$ are the shares $x_{t-1}(u)/\deg^+(u)$ of its in-neighbours. Vertices with no out-edges lose their rank in the paper's program. A sum aggregator fixes this: such a vertex adds its value to the aggregator, and in the next superstep every vertex adds $\alpha D/n$, where $D$ is the aggregated sum. With this change the values sum to $1$ and match the power iteration exactly. Each superstep sends at most $m$ messages, one per edge, or one per pair of worker and target with a sum combiner.

### Other algorithms

The paper also gives a randomized bipartite matching that runs in cycles of four phases, one superstep each, and semi-clustering for social graphs. In the maximum-value example of Section 2, every vertex sends its value in superstep $0$, and later a vertex sends only when its value grows. On an undirected graph with at least one edge, every vertex ends with the largest value of its connected component after exactly $D + 2$ supersteps, where $D$ is the largest, over all vertices $v$, of the distance from $v$ to the nearest vertex that holds the largest value of the component of $v$: after superstep $t$ a vertex holds the largest value within distance $t$.

## References
