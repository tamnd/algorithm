---
tag: NAYARS
kind: problem
slug: uniform-spanning-tree-sampling
name: Uniform spanning tree sampling
aliases:
- random spanning tree generation
area: graphs/spanning-trees
level: advanced
summary: Generate a spanning tree of a graph uniformly at random among all spanning trees.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {expected: O(m n)}
prereqs: [spanning-tree, markov-chain, matrix-tree-theorem, randomized-algorithm]
see_also: [wilson-algorithm, aldous-broder, counting-spanning-trees, spanning-tree-enumeration, laplacian-matrix, stationary-distribution, coupling-from-the-past, mixing-time]
sources:
  - paper: doi:10.1145/237814.237880
    title: David Bruce Wilson, Generating random spanning trees more quickly than the cover time, Proceedings of the 28th Annual ACM Symposium on Theory of Computing (1996), 296-303
    locator: the whole paper (the loop-erased random walk algorithm, its run time as the mean hitting time, and the comparison with earlier methods)
  - paper: doi:10.1109/SFCS.1989.63516
    title: Andrei Z. Broder, Generating random spanning trees, Proceedings of the 30th Annual Symposium on Foundations of Computer Science (1989), 442-447
    locator: the whole paper (the random walk algorithm)
  - paper: doi:10.1137/0403039
    title: David J. Aldous, The random walk construction of uniform spanning trees and uniform labelled trees, SIAM Journal on Discrete Mathematics 3(4) (1990), 450-465
    locator: the whole paper (the same construction, found independently)
  - book: isbn:9781107160156
    title: Russell Lyons and Yuval Peres, Probability on Trees and Networks, Cambridge University Press (2016)
    locator: Chapter 4, Uniform Spanning Trees (Wilson's method, the Aldous-Broder method, and the transfer current theorem)
---

The uniform spanning tree sampling problem asks for a random [spanning tree](/spanning-tree/) of a connected graph, where each of the $\tau(G)$ spanning trees has probability exactly $1/\tau(G)$. Listing all trees is far too slow, since $\tau(G)$ can be exponential. Classical exact methods either use determinants, deciding one edge at a time with the probabilities from the [matrix-tree theorem](/matrix-tree-theorem/), or use random walks: the [Aldous-Broder algorithm](/aldous-broder/) runs in the cover time of the walk and [Wilson's algorithm](/wilson-algorithm/) in time proportional to its mean hitting time, both $O(mn)$ in expectation. A weighted form samples each tree with probability proportional to the product of its edge weights.

## In plain words

A network can have a huge number of trees that connect all its points. You want to pick one of them so that every tree has the same chance. Writing them all down and drawing one by lot works only for tiny networks.

There are two better ideas. The first goes edge by edge: a formula tells the exact chance that a given link is in a random tree, so you decide that link with a coin of that bias, and then go on with the next one. The second walks through the network at random and keeps some of the links that the walk uses. A clever choice of which links to keep makes every tree equally likely, without ever counting the trees.

## Definition

**Input.** A finite undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, and a source of random bits. Parallel edges are allowed and count as different edges, so a pair joined by two edges gives two different trees. Self-loops are never in a tree and play no role.

**Output.** A random spanning tree $T$ with

$$\Pr[T = t] = \frac{1}{\tau(G)} \quad \text{for each spanning tree } t \text{ of } G,$$

where $\tau(G)$ is the number of spanning trees.

**Connectivity.** The graph must be [connected](/connected-graph/), or it has no spanning tree. For a disconnected graph the natural output is a *uniform spanning forest*: a uniform spanning tree of each component, chosen independently. It is uniform among the spanning forests with one tree for each component, since their number is the product of the numbers for the components.

**Weighted form.** Given weights $w(e) > 0$, sample $t$ with probability $\prod_{e \in t} w(e) / Z$, where $Z$ is the sum of these products over all spanning trees. Weights may tie; equal weights simply give equal factors. With all weights equal, this is the uniform form. Weights 0 are the same as deleting the edge.

**Exact and approximate.** An *exact* sampler has the stated distribution. An *approximate* sampler is within a given total variation distance $\varepsilon$ of it.

## Variants

- **Uniform spanning arborescences.** In a directed graph, sample an arborescence with a given root uniformly. Wilson's algorithm does this directly.
- **Approximate sampling.** Run the [Markov chain](/markov-chain/) that swaps one edge of the current tree for another, until it is close to its [stationary distribution](/stationary-distribution/). Its [mixing time](/mixing-time/) bounds the cost.
- **Exact sampling by coupling.** Wilson's algorithm can be read as a form of [coupling from the past](/coupling-from-the-past/), the "cycle popping" view in Wilson's paper.
- **Random spanning forests.** Rooted forests in which each vertex is a root with a given probability, sampled by Wilson's method with an extra absorbing vertex.
- **Infinite graphs.** Uniform spanning forests of infinite graphs, such as the grid $\mathbb{Z}^d$, are limits of the finite ones and a topic of probability theory.

## Examples

**A triangle.** It has three trees, each with probability $1/3$. Each edge is in the tree with probability $2/3$.

**The complete graph $K_4$.** It has 16 trees, each with probability $1/16$. By symmetry, each of the six edges is in the tree with probability $3/6 = 1/2$, since each tree has three edges.

**A graph with six vertices.** The graph on $a$ to $f$ with the nine edges below has 55 spanning trees, so each has probability $1/55$. The number of trees that contain each edge:

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| trees with the edge | 34 | 34 | 26 | 31 | 25 | 31 | 26 | 34 | 34 |

The counts add up to $275 = 5 \times 55$, since each tree has five edges. The edge $cd$ is in a random tree with probability $25/55$ and $ab$ with probability $34/55$. These probabilities are the effective resistances between the ends of the edges when each edge is a unit resistor.

**Weights.** In the triangle with weights $1, 2, 3$, the trees have the products $1 \cdot 2 = 2$, $1 \cdot 3 = 3$ and $2 \cdot 3 = 6$, so they are sampled with probabilities $2/11$, $3/11$ and $6/11$.

**A disconnected graph.** Two disjoint triangles give $3 \times 3 = 9$ spanning forests, each with probability $1/9$.

## Known algorithms

| algorithm | year | expected time | notes |
|---|---|---|---|
| List all trees and draw one | | $O(n \tau(G))$ | only for tiny graphs |
| Edge by edge with determinants | 1980s | $O(m n^3)$ simple form | exact; faster versions use fast matrix products |
| [Aldous-Broder](/aldous-broder/) | 1989, 1990 | cover time, $O(m n)$ | first-entrance edges of a random walk |
| [Wilson](/wilson-algorithm/) | 1996 | about the mean hitting time, $O(m n)$ | loop-erased random walks |
| Kelner and Mądry | 2009 | $\tilde O(m \sqrt{n})$ | random walks with shortcuts by electrical flows |
| Schild | 2018 | $m^{1 + o(1)}$ | almost-linear time |

**Edge by edge.** Order the edges $e_1, \ldots, e_m$. For $e_1 = uv$, the probability that a uniform tree contains it is $\tau(G / e_1) / \tau(G)$, which equals the effective resistance between $u$ and $v$. With this probability, contract $e_1$ and keep it; otherwise delete it. Go on with $e_2$ in the new graph. Each probability is a ratio of two determinants of [Laplacian](/laplacian-matrix/) minors, so the simple form computes $O(m)$ determinants.

**Random walks.** Aldous-Broder needs a walk that visits every vertex. Wilson's algorithm needs, for each vertex, only a walk until it hits the tree built so far, and erases the loops of that walk. Its expected number of steps is proportional to the mean hitting time of the walk, which is always less than the cover time and on many graphs much smaller. On the complete graph $K_n$ the cover time is $\Theta(n \log n)$ steps while Wilson's algorithm takes $O(n)$ steps.

## Bounds

**Lower bound.** An exact sampler for general graphs must read the whole graph, so it takes $\Omega(n + m)$ time.

**Upper bounds.** Wilson's and the Aldous-Broder algorithms run in $O(mn)$ expected time, since both the cover time and the mean hitting time of a simple random walk on a connected graph are $O(mn)$. The fastest known exact algorithm, by Schild, runs in $m^{1 + o(1)}$ time.

**Random bits.** The random walk methods use a number of random choices that is not bounded in advance. They give probability exactly $1/\tau(G)$ when each choice among $d$ neighbours is exactly uniform, for example with [uniform random integers](/uniform-random-integer-generation/) drawn by rejection.

## Reductions

- **Sampling to counting.** The edge-by-edge method needs the counts $\tau(G / e)$ and $\tau(G)$, from the matrix-tree theorem ([counting spanning trees](/counting-spanning-trees/)). The general theory of self-reducible problems turns exact counting into exact sampling in the same way.
- **Counting to sampling, approximately.** Many samples estimate $\Pr[e \in T]$ for one edge, and $\tau(G) = \tau(G - e) / (1 - \Pr[e \in T])$ for an edge that is not a bridge. Repeating this on a shrinking graph estimates $\tau(G)$.
- **Disconnected graphs to connected graphs.** Sample each component on its own.

## Applications

- **Maze generation.** A uniform spanning tree of a grid is a maze with no bias towards any shape, and Wilson's algorithm is a common way to build one.
- **Graph sparsification and cuts.** Random spanning trees give sparse subgraphs that keep cut sizes in expectation and are used in fast algorithms for flows and Laplacian systems.
- **Travelling salesman approximation.** Random spanning trees, sampled from a distribution with given marginals, are a step of the best approximation algorithms for asymmetric and symmetric TSP.
- **Statistical physics and probability.** Uniform spanning trees are linked to loop-erased random walks, electrical networks and the Potts model.
- **Testing.** Random trees give test inputs for tree algorithms.

## References
