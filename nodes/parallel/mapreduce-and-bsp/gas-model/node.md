---
tag: Z8G7PR
kind: model
slug: gas-model
name: Gather-apply-scatter model
aliases:
- GAS model
- PowerGraph model
area: parallel/mapreduce-and-bsp
level: research
summary: A graph model in which each vertex gathers a sum over its edges, applies an update and scatters along its edges. PowerGraph runs it on a vertex cut, so one vertex can span several machines.
history:
  year: 2012
  people: [Joseph E. Gonzalez, Yucheng Low, Haijie Gu, Danny Bickson, Carlos Guestrin]
  note: Gonzalez et al. introduced the GAS decomposition and vertex cuts in PowerGraph at OSDI 2012.
prereqs: [pregel-model]
see_also: [bsp-model, superstep, pagerank, connected-components, data-skew, hash-partitioning, vertex-cut]
sources:
  - paper: "Joseph E. Gonzalez, Yucheng Low, Haijie Gu, Danny Bickson and Carlos Guestrin, PowerGraph: distributed graph-parallel computation on natural graphs, OSDI 2012"
    locator: pp. 17-30; Section 4 and Figure 2 (the GAS vertex program), Algorithm 1 (execution and delta caching), Section 5 (vertex cuts, Theorem 5.1 on random edge cuts, Theorem 5.2 on random vertex cuts, Theorem 5.3, and the greedy placements)
  - paper: doi:10.1145/1807167.1807184
    title: "Grzegorz Malewicz, Matthew H. Austern, Aart J. C. Bik, James C. Dehnert, Ilan Horn, Naty Leiser and Grzegorz Czajkowski, Pregel: a system for large-scale graph processing, SIGMOD 2010"
    locator: pp. 135-146, Section 2, the vertex-centric model that GAS refines
---

The gather-apply-scatter (GAS) model describes a graph computation as a vertex program in three phases: gather a sum over the edges of a vertex, apply the sum to update the vertex value, and scatter along the edges to update them and to activate neighbours. Gonzalez and others introduced it in PowerGraph (2012) for graphs with very skewed degrees, such as social and web graphs. Because the gather is a commutative and associative sum, the system can split one vertex over several machines, each summing over its own edges. The graph is then stored by a vertex cut: edges go to machines, and a vertex is copied to every machine that holds one of its edges.

## The machine

The notation follows the parallel pages of this site. The input is a graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, and data $D_v$ on each vertex and $D_{(u,v)}$ on each edge.

| Symbol | Meaning |
|---|---|
| $n$, $m$ | the number of vertices and of edges |
| $p$ | the number of machines |
| $A(v)$ | the set of machines that hold a copy of vertex $v$ |
| $D[v]$ | the degree of $v$ (in-edges plus out-edges) |
| $\mathrm{RF}$ | the replication factor $\frac{1}{n}\sum_v \lvert A(v) \rvert$ |

**The vertex program.** The user writes four functions (Figure 2 of the paper):

- $\mathrm{gather}(D_u, D_{(u,v)}, D_v) \to a$, run on each edge of the gather direction (in-edges, out-edges, all or none);
- $\mathrm{sum}(a, b) \to a$, which must be commutative and associative;
- $\mathrm{apply}(D_u, a) \to D_u^{new}$, run once per vertex on the total sum;
- $\mathrm{scatter}(D_u^{new}, D_{(u,v)}, D_v) \to D_{(u,v)}^{new}$, run on each edge of the scatter direction; it may also activate the neighbour $v$.

For [PageRank](/pagerank/) with follow probability $\alpha$: gather returns $x_u/\deg^+(u)$ over the in-edges $(u, v)$, sum is $+$, apply sets $x_v = (1 - \alpha)/n + \alpha a$, and scatter activates the out-neighbours if $x_v$ changed by more than a tolerance. For shortest paths: gather returns $d_u + w(u, v)$, sum is $\min$, apply keeps the smaller of the old value and $a$, and scatter activates the out-neighbours when the value dropped.

**The vertex cut.** Each edge $e$ is stored on one machine $A(e)$. A vertex $v$ is stored on every machine of $A(v) = \{A(e) : e \text{ touches } v\}$. One copy is the master; the others are mirrors. A balanced $p$-way vertex cut minimizes the replication factor subject to each machine holding about $m/p$ edges. This is a partition of the edges, not the [vertex cut](/vertex-cut/) of graph connectivity, which is a set of vertices whose removal disconnects the graph. The alternative, an edge cut, stores each vertex on one machine with all its edges; an edge between two machines then needs a ghost copy of a vertex.

**One synchronous iteration.** For each active vertex $v$:

1. Gather: each machine in $A(v)$ sums gather over the local edges of $v$, using its local copies of the neighbours; each mirror sends its partial sum to the master.
2. Apply: the master adds the partial sums, runs apply, and sends the new value $D_v$ to each mirror.
3. Scatter: each machine runs scatter on its local edges of $v$, and the activations go to the masters of the neighbours.

In the synchronous engine these three phases are separated by barriers, so an iteration is a short sequence of [supersteps](/superstep/). PowerGraph also has an asynchronous engine, which runs vertex programs as soon as they are active. Algorithm 1 of the paper adds delta caching: scatter may send a change of the accumulator to a neighbour, so that its next gather can be skipped.

## What it counts

Per iteration, with every vertex active, the communication of the vertex cut is

$$
\text{gather} \le \sum_v \left(\lvert A(v) \rvert - 1\right), \qquad \text{apply} = \sum_v \left(\lvert A(v) \rvert - 1\right) = n(\mathrm{RF} - 1),
$$

so at most $2n(\mathrm{RF} - 1)$ words, plus the activations. Memory is also proportional to $n \cdot \mathrm{RF}$ copies of vertex data. The work of a machine is the number of edges it holds, so balance means about $m/p$ edges per machine, and a vertex of degree $d$ adds at most about $d/p$ work to each machine instead of $d$ to one. The paper measures that run time grows linearly with the replication factor.

**Random edge cut (Theorem 5.1).** If each vertex is put on a machine chosen uniformly and independently, the expected fraction of cut edges is $1 - 1/p$. *Proof.* The two ends of an edge land on the same machine with probability $\sum_{j} (1/p)^2 = 1/p$, and [linearity of expectation](/linearity-of-expectation/) gives the fraction. $\square$ So with $p = 8$, a random edge cut cuts $87.5\%$ of the edges.

**Random vertex cut (Theorem 5.2).** If each edge is put on a machine chosen uniformly and independently, then

$$
\mathbb{E}[\mathrm{RF}] = \frac{p}{n} \sum_{v \in V} \left(1 - \left(1 - \frac{1}{p}\right)^{D[v]}\right).
$$

*Proof.* Machine $j$ holds no edge of $v$ with probability $(1 - 1/p)^{D[v]}$, since the $D[v]$ edges are placed independently. So $\mathbb{E}\lvert A(v) \rvert = \sum_{j=1}^{p} \Pr[j \in A(v)] = p\left(1 - (1 - 1/p)^{D[v]}\right)$, and linearity of expectation gives the sum. $\square$ The formula counts $0$ copies for a vertex with no edges; a real system stores such a vertex once. Each term is at most $\min(D[v], p)$, so a vertex never has more copies than edges or machines. For $p = 8$, a vertex of degree $10$ is expected on $5.90$ machines and a vertex of degree $100$ on almost all $8$.

The paper also proves (Theorem 5.3) that from an edge cut one can build a vertex cut along the same boundary with fewer mirrors than the edge cut has ghosts, and it gives two greedy placements, coordinated and oblivious, that place each edge on a machine that already holds its endpoints when possible. They give a lower replication factor than random placement.

**Example.** Take the edges $\{0,1\}, \{0,2\}, \{1,2\}$ on machine $0$ and $\{0,3\}, \{2,3\}$ on machine $1$. Then $A(0) = \{0,1\}$, $A(1) = \{0\}$, $A(2) = \{0,1\}$ and $A(3) = \{1\}$, so $\mathrm{RF} = 6/4 = 1.5$ and one iteration with all vertices active sends at most $2 \cdot 2 = 4$ words.

The simulator of this page places edges at random, checks the formula of Theorem 5.2 against the average of 300 placements (for a graph with 60 vertices and $p = 8$ the two agree to within $0.01$), checks that PageRank equals the exact power iteration and shortest paths equal [Dijkstra's algorithm](/dijkstra/), and checks the word counts above.

## Relation to other models

- [Pregel](/pregel-model/). A Pregel vertex receives messages and may send any message. A GAS vertex reads its neighbourhood only through gather, a commutative and associative sum, which plays the part of a Pregel [combiner](/combiner/) but is built in. That restriction is what lets the system split a vertex over machines. Pregel stores the graph by an edge cut, with each vertex and its out-edges on one worker.
- [BSP](/bsp-model/). The synchronous engine is BSP: each iteration has three phases with barriers, and the gather and apply traffic are h-relations among the $p$ machines. A good vertex cut makes these h-relations small and balanced.
- [Data skew](/data-skew/). In a graph whose degrees follow a power law, an edge cut puts all edges of a very high-degree vertex on one machine, which then dominates each superstep. The vertex cut spreads them.

## Known results in the model

- The two theorems above on random edge and vertex cuts, proved on this page, and Theorem 5.3 of the paper.
- Synchronous GAS computes the same values as the corresponding Pregel program or power iteration when the sum is exact: PageRank after $k$ iterations equals $k$ steps of the power iteration, and shortest paths with $\min$ as sum is a synchronous [Bellman-Ford](/bellman-ford/), ending after about as many iterations as there are edges on a shortest path.
- [Connected components](/connected-components/) by minimum labels uses gather $= \min$ of neighbour labels over all edges and stops when no label changes; the number of iterations is at most the largest distance from a vertex to the smallest vertex of its component, plus one.

## References
