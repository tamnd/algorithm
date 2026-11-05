---
tag: H0EB9M
kind: model
slug: random-geometric-graph
name: Random geometric graph
aliases:
- unit disk random graph
area: graphs/network-analysis
level: advanced
summary: Nodes placed at random points; edges join points within a fixed distance.
prereqs: [erdos-renyi-model, percolation, connected-components]
see_also: [erdos-renyi-model, percolation, giant-component, clustering-coefficient, small-world-network, euclidean-minimum-spanning-tree, spatial-hashing, kd-tree]
sources:
  - paper: doi:10.1137/0109045
    title: E. N. Gilbert, Random plane networks, Journal of the Society for Industrial and Applied Mathematics 9(4), 533 to 543 (1961)
    locator: the whole paper (points of a Poisson process in the plane joined when within distance r, and bounds on the critical density for an infinite component)
  - book: isbn:9780198506263
    title: Mathew Penrose, Random Geometric Graphs, Oxford University Press, 2003
    locator: Chapter 13 (connectivity and the largest nearest-neighbour link) and Chapters 9 and 10 (the giant component and continuum percolation)
  - paper: doi:10.1214/aoap/1034625335
    title: Mathew D. Penrose, The longest edge of the random minimal spanning tree, Annals of Applied Probability 7(2), 340 to 361 (1997)
    locator: the limit law of the longest edge of the minimum spanning tree of uniform points, which gives the connectivity threshold
  - paper: doi:10.1103/PhysRevE.66.016121
    title: Jesper Dall and Michael Christensen, Random geometric graphs, Physical Review E 66(1), 016121 (2002)
    locator: the clustering coefficient in d dimensions, equal to 1 minus 3 times the square root of 3 over 4 pi in two dimensions, and the percolation threshold as a function of dimension
---

A random geometric graph places $n$ vertices at random points of a space, usually the unit square, and joins two vertices by an edge when their points are within distance $r$ of each other. Gilbert (1961) introduced it to model radio stations that can talk only to stations within range, and it remains the basic model of wireless and sensor networks. It shares with the [Erdős-Rényi model](/erdos-renyi-model/) a threshold for a [giant component](/giant-component/) and a threshold for connectivity, but its edges are far from independent: two neighbours of a vertex are close to each other, so the graph has a high [clustering coefficient](/clustering-coefficient/) and a large diameter, the opposite of a [small-world network](/small-world-network/).

## The machine

**Input.** A number of vertices $n$, a dimension $d$ (usually 2), a radius $r > 0$, a region (the unit cube $[0, 1]^d$, or the unit torus, in which opposite sides are glued so that no point is near a boundary), and a norm, usually the Euclidean one.

**Generation.** Draw points $X_1, \dots, X_n$ independently and uniformly from the region. Join $i$ and $j$ by an undirected edge when $\|X_i - X_j\| \le r$. The result $G(n, r)$ is undirected and simple. Edges carry no weights, though the distance $\|X_i - X_j\|$ is often kept as a weight. Gilbert's original version places the points by a Poisson process of intensity $\lambda$ in the plane, so the number of points in a region is random.

**Building it.** Comparing all pairs takes $\Theta(n^2)$ time. A grid of cells of side $r$ ([spatial hashing](/spatial-hashing/)) puts each point in its cell, and the neighbours of a point lie in its cell and the adjacent ones, $3^d$ cells in all, so the graph is built in $O(n + m)$ expected time for fixed $d$, where $m$ is the number of edges. A [k-d tree](/kd-tree/) with range queries is the other common choice.

**Example.** Take six points in the unit square, $0 = (0.1, 0.1)$, $1 = (0.3, 0.2)$, $2 = (0.5, 0.1)$, $3 = (0.4, 0.4)$, $4 = (0.8, 0.5)$ and $5 = (0.9, 0.8)$, and $r = 0.35$. The pairs within distance $0.35$ are 0-1, 1-2 and 1-3 (each $\sqrt{0.05} \approx 0.224$), and 2-3 and 4-5 (each $\sqrt{0.1} \approx 0.316$). The graph has a triangle $\{1, 2, 3\}$ and two components, $\{0, 1, 2, 3\}$ and $\{4, 5\}$. With $r = 0.45$, the edges 0-2 ($0.4$), 3-4 ($\sqrt{0.17} \approx 0.412$) and 0-3 ($\sqrt{0.18} \approx 0.424$) appear, and the graph becomes connected.

## What it counts

- **Degree.** On the torus in two dimensions, a vertex has $\mathrm{Binomial}(n - 1, \pi r^2)$ neighbours, with mean $(n - 1)\pi r^2$, which is close to Poisson when $r$ is small. Near the boundary of the square, the disk is cut off and the degree is lower.
- **Clustering.** The probability that two neighbours of a vertex are neighbours of each other, a property of the geometry alone.
- **Components.** The size of the largest component, as the mean degree grows, and the radius at which the graph becomes connected.
- **Distances.** The diameter and the number of hops between two points, which grow like the Euclidean distance divided by $r$ once the graph is well connected.

## Relation to other models

- **[Erdős-Rényi model](/erdos-renyi-model/).** With mean degree $c$ fixed, both models have Poisson degrees, but in the Erdős-Rényi graph edges are independent, while here they are correlated through the positions. As a result the clustering coefficient tends to 0 there and to a positive constant here, and distances grow like $\log n$ there and like $n^{1/2}$ (in hops, for constant mean degree in the plane) here.
- **[Percolation](/percolation/).** The giant component of a random geometric graph is *continuum percolation*: Gilbert's disk model is percolation of overlapping disks of radius $r/2$ around Poisson points.
- **Unit disk graphs.** A graph is a unit disk graph if some placement of points makes it the graph of pairs within distance 1. A random geometric graph is a random unit disk graph, and algorithms for unit disk graphs (colouring, independent sets, routing) are often studied on it.
- **Spatial network models.** The [small-world network](/small-world-network/) of Kleinberg adds long-range links to a lattice with probability falling with distance, and soft random geometric graphs join points with a probability that decreases with distance instead of a hard cutoff. Hyperbolic random graphs place the points in the hyperbolic plane and obtain power-law degrees.
- **The [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/).** The graph $G(n, r)$ is connected exactly when $r$ is at least the longest edge of the Euclidean minimum spanning tree of the points, so the connectivity threshold is a statement about that edge.

## Known results in the model

All statements are for uniform points in the unit square or torus, with $n \to \infty$.

**Clustering.** In two dimensions, the clustering coefficient tends to $1 - \frac{3\sqrt{3}}{4\pi} \approx 0.5865$, independent of $r$ for small $r$ on the torus (Dall and Christensen). It decreases with the dimension. A sample with $n = 5000$ points on the torus and mean degree about 10 gave $0.592$.

**The giant component.** There is a critical mean degree $c^* \approx 4.51$ in the plane: when $n \pi r^2 \to c < c^*$, all components have $o(n)$ vertices, and when $c > c^*$, one component holds a positive fraction of the vertices. The value is known only numerically, from simulation of continuum percolation. Simulations with $n = 20000$ on the torus (mean of 5 graphs):

| mean degree | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|
| largest component | 0.009 | 0.09 | 0.926 | 0.986 | 0.999 |

The jump between degree 4 and 5 is far sharper than the jump at mean degree 1 in the Erdős-Rényi model.

**Connectivity.** If $n \pi r^2 = \ln n + c$, the probability that $G(n, r)$ on the torus is connected tends to $e^{-e^{-c}}$, the same limit as for the Erdős-Rényi graph with $np = \ln n + c$ (Penrose 1997). The proof shows that, at this scale, the last obstacle to connectivity is an isolated vertex: the graph is connected almost exactly when it has minimum degree at least 1, and the number of isolated vertices is close to Poisson with mean $e^{-c}$. The convergence is slow. In 200 samples with $n = 2000$:

| $c$ | 0 | 1 | 2 |
|---|---|---|---|
| $e^{-e^{-c}}$ | 0.368 | 0.692 | 0.873 |
| no isolated vertex | 0.38 | 0.72 | 0.88 |
| connected | 0.185 | 0.565 | 0.835 |

The probability of no isolated vertex is already close to the limit, while small groups of two or three vertices cut off from the rest still occur at this $n$.

**Distances and diameter.** When the graph is connected and $r \to 0$, the number of hops on the shortest path between two vertices is close to their distance divided by $r$, so the diameter is about $\sqrt{2}/r$ in the unit square: there is no small-world effect.

**Other properties.** Penrose's book gives thresholds for $k$-connectivity (matching minimum degree $k$) and limit laws for the chromatic number and clique number, which grow like $n r^2$ rather than like $\log n$.

**Disconnected graphs and ties.** The model is defined for every $r$, and below the connectivity threshold it is disconnected with high probability; measures such as distances are then taken within components. Points at distance exactly $r$ are joined, but this has probability 0 for continuous positions.

## References
