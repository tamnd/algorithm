---
tag: MAJJEY
kind: algorithm
slug: force-directed-layout
name: Force-directed layout
area: graphs/network-analysis
level: core
summary: Draws a graph by treating edges as springs and vertices as repelling charges, then moving vertices until forces balance.
solves: [graph-drawing]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, T: the number of rounds}
  time: {worst: Θ(T (n^2 + m)), best: Θ(T (n^2 + m))}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1984
  people: [Peter Eades, Thomas M. J. Fruchterman, Edward M. Reingold, Tomihisa Kamada, Satoru Kawai]
  note: Eades proposed the spring embedder in 1984; Kamada and Kawai (1989) and Fruchterman and Reingold (1991) gave the two forms used most today. Tutte's barycentric drawing of 1963 is an early ancestor.
prereqs: [graph, graph-drawing, shortest-path]
see_also: [tutte-spring-theorem, planar-straight-line-drawing, multidimensional-scaling, spectral-clustering, node-embedding, community-detection]
sources:
  - paper: doi:10.1002/spe.4380211102
    title: Thomas M. J. Fruchterman and Edward M. Reingold, Graph drawing by force-directed placement, Software, Practice and Experience 21(11), 1129 to 1164 (1991)
    locator: the forces f_a(d) = d^2/k and f_r(d) = k^2/d, the optimal distance k from the area and the number of vertices, the temperature and cooling, the frame, and the grid variant
  - paper: doi:10.1016/0020-0190(89)90102-6
    title: Tomihisa Kamada and Satoru Kawai, An algorithm for drawing general undirected graphs, Information Processing Letters 31(1), 7 to 15 (1989)
    locator: the spring energy with natural lengths proportional to graph distances, and its minimization by moving one vertex at a time with Newton-Raphson steps
  - paper: doi:10.1112/plms/s3-13.1.743
    title: W. T. Tutte, How to draw a graph, Proceedings of the London Mathematical Society s3-13(1), 743 to 767 (1963)
    locator: the barycentric drawing, in which each free vertex lies at the mean of its neighbours, and its planarity for 3-connected planar graphs
  - paper: doi:10.1007/978-3-540-31843-9_25
    title: Emden R. Gansner, Yehuda Koren and Stephen North, Graph drawing by stress majorization, Graph Drawing 2004, Lecture Notes in Computer Science 3383, 239 to 250 (2005)
    locator: the stress energy and its minimization by majorization, as a replacement for the Kamada-Kawai method
  - book: isbn:9780133016154
    title: Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999
    locator: the chapter on force-directed methods (spring embedders, Eades' forces, energy functions and their minimization)
---

A force-directed layout places the [vertices](/vertex/) of a graph in the plane by simulating a physical system. Every edge acts as a spring that pulls its two ends together, and every pair of vertices pushes apart like two equal charges. Starting from some positions, the vertices move step by step in the direction of the total force on them, with a step size that shrinks over time, until the forces nearly balance. The result tends to show the structure of the graph: dense groups form clusters, edges have similar lengths, and symmetric graphs look symmetric. The best-known form, by Fruchterman and Reingold, costs $\Theta(n^2 + m)$ time per round.

## In plain words

Think of the vertices as small magnets that all push each other away, and the edges as rubber bands that tie some of them together. Drop them on a table and let go. The magnets spread out so that nothing overlaps, while the rubber bands keep linked vertices close.

The algorithm imitates this. In each round, it adds up the pushes and pulls on each vertex and moves the vertex a little in that direction. The allowed move gets smaller each round, like a liquid that cools and sets. When the moves are tiny, the picture is done. Vertices with many links in common end up near each other, so groups in the network become visible.

## The problem

The input is a [graph](/graph/) $G = (V, E)$ with $n$ vertices and $m$ edges, start positions $p_v \in \mathbb{R}^2$, a natural edge length $k > 0$, a start temperature $t_0 > 0$ and a number of rounds $T$. The graph is undirected and unweighted; directions are ignored. The output is a position for every vertex. There is no single correct answer: the aim is a drawing that a person can read, with few crossings, even edge lengths and visible clusters. The method treats it as finding a low point of an energy.

**The forces.** Fruchterman and Reingold use, for two vertices at distance $d$,

- a repulsion $f_r(d) = k^2/d$ between every pair of vertices, pushing them apart, and
- an attraction $f_a(d) = d^2/k$ between the two ends of every edge, pulling them together.

The two forces balance at $d = k$, so $k$ is the length an isolated edge takes. They suggest $k = C\sqrt{\text{area}/n}$ for a frame of the given area and a constant $C$. These forces are the negative gradient of the energy

$$E(p) = \sum_{\{u,v\} \in E} \frac{\lVert p_u - p_v \rVert^3}{3k} \;-\; \sum_{\{u, v\} \subseteq V} k^2 \ln \lVert p_u - p_v \rVert,$$

so a balanced drawing is a critical point of $E$.

## The algorithm

```pseudo id=main
FORCE-DIRECTED-LAYOUT(G, p, k, t0, T)
L1  t ← t0
L2  for r ← 1 to T do
L3      for each vertex v do disp[v] ← (0, 0)
L4      for each pair {u, v} of vertices do δ ← p[v] − p[u]; disp[v] ← disp[v] + (δ/|δ|) k²/|δ|; disp[u] ← disp[u] − (δ/|δ|) k²/|δ|
L5      for each edge {u, v} do δ ← p[v] − p[u]; disp[v] ← disp[v] − (δ/|δ|) |δ|²/k; disp[u] ← disp[u] + (δ/|δ|) |δ|²/k
L6      for each vertex v with disp[v] ≠ 0 do p[v] ← p[v] + (disp[v]/|disp[v]|) · min(|disp[v]|, t)
L7      t ← t0 (1 − r/T)                       ▷ linear cooling
L8  return p
```

Line L4 adds the repulsion, line L5 the attraction, and line L6 moves each vertex along its total force by at most the temperature $t$. Lines L4 to L6 read the positions of the previous round, so the order of the vertices does not matter. Fruchterman and Reingold also keep the vertices inside a rectangular frame by clipping the positions after line L6.

**Ties and special cases.** The method has no ties to break, but two vertices at the same point have no direction between them; this page then pushes them apart along the $x$ axis, the lower index to the left, with a very large force that line L6 caps at $t$. The start positions are an input: with random starts, use a seeded generator so that the result can be repeated.

**Disconnected graphs.** Different [components](/connected-components/) only repel each other, so without a frame they drift apart for ever and the drawing shrinks the components to dots when it is scaled to fit. Common fixes are a weak pull of every vertex towards the centre, or a layout of each component on its own, followed by packing the drawings side by side.

**Weighted and directed graphs.** A weight can set the natural length of an edge or scale its attraction. Directed graphs are drawn as undirected, with the arrows added at the end; layered methods are better when the direction matters.

## Example

Take the path $0 - 1 - 2$ with the start positions $(0, 0)$, $(0.5, 0.3)$ and $(1, 0)$, $k = 1$ and $t_0 = 0.2$. In the first round, the pairs $\{0,1\}$ and $\{1,2\}$ are at distance $0.5831$ and repel with force $1.7150$; the pair $\{0,2\}$ is at distance 1 and repels with force 1; each edge attracts with force $0.5831^2 = 0.3400$.

| vertex | repulsion | attraction | total force | length | new position |
|---|---|---|---|---|---|
| 0 | $(-2.4706, -0.8824)$ | $(0.2915, 0.1749)$ | $(-2.1790, -0.7074)$ | 2.2910 | $(-0.1902, -0.0618)$ |
| 1 | $(0, 1.7647)$ | $(0, -0.3499)$ | $(0, 1.4148)$ | 1.4148 | $(0.5, 0.5)$ |
| 2 | $(2.4706, -0.8824)$ | $(-0.2915, 0.1749)$ | $(2.1790, -0.7074)$ | 2.2910 | $(1.1902, -0.0618)$ |

Every force is longer than $t = 0.2$, so each vertex moves by exactly 0.2. The vertices start too close together, so repulsion wins and the drawing grows. After 300 rounds the three vertices lie on a line with the middle one between the others, and each edge has length $1.1443$, close to the balance value $1.5^{1/3} \approx 1.1447$: an end vertex feels the attraction $d^2$ against the repulsions $1/d$ and $1/(2d)$, and $d^3 = 3/2$.

## Correctness

The method is a heuristic and has no guarantee about the quality of the drawing. What holds exactly is the following. The vector $\mathrm{disp}[v]$ computed in lines L3 to L5 is $-\nabla_v E(p)$, so each round moves every vertex in the direction of steepest descent of $E$ for that vertex, by a step capped at $t$. A drawing is left unchanged by a round with $t > 0$ if and only if it is a critical point of $E$, a drawing where all forces balance. The loop ends after $T$ rounds, and in round $r$ no vertex moves farther than $t_0(1 - (r-1)/T)$. The full proof, with the balance distances of an edge and of a path of three vertices, is in [the proof page](proofs/correctness.md).

## Complexity

- **One round.** Line L4 visits all $\binom{n}{2}$ pairs and line L5 all $m$ edges, each in $O(1)$, so a round costs $\Theta(n^2 + m)$ time on the [real RAM](/real-ram/).
- **The whole run.** $\Theta(T(n^2 + m))$ for $T$ rounds. The number of rounds needed for a good drawing depends on the graph and the start; a few hundred is common for small graphs.
- **Faster repulsion.** Fruchterman and Reingold's grid variant counts repulsion only from vertices in nearby cells of a grid, so only from vertices within a fixed distance, which takes $O(n + m)$ per round when the vertices are spread evenly. Barnes-Hut quadtrees approximate all the repulsions in $O(n \log n)$ per round.
- **Space.** The positions and displacements take $\Theta(n)$ numbers besides the graph.
- **Kamada-Kawai.** Its energy needs the graph distance of every pair, so it first solves [all-pairs shortest paths](/all-pairs-shortest-paths/), $O(nm)$ by [breadth-first search](/breadth-first-search/), and stores $\Theta(n^2)$ numbers.

## Properties

- **Deterministic for fixed starts.** Random starts make the result random. Different starts can give different drawings, since $E$ has many local minima.
- **Arbitrary orientation.** A rotation or reflection of a drawing has the same energy, so the orientation of the output depends on the start.
- **Translation invariant.** Shifting all start positions shifts the result by the same vector, since every force depends only on differences.
- **Shows clusters.** Dense groups pull together and repel the rest, which is why these layouts are a standard way to look at [communities](/community-detection/).
- **No planarity guarantee.** Even for [planar graphs](/planar-graph/) the result can have crossings, unlike Tutte's barycentric drawing of 3-connected planar graphs with a fixed outer face.

## Variants and improvements

- **Eades' spring embedder (1984).** Logarithmic springs on edges and inverse-square repulsion between non-adjacent vertices; the model all later methods build on.
- **Kamada-Kawai (1989).** Springs between all pairs, with natural length proportional to the graph distance and stiffness falling with the square of it; the energy is minimized one vertex at a time by Newton-Raphson steps.
- **Stress majorization.** Gansner, Koren and North minimize the same kind of energy, called stress, by solving a sequence of linear systems, which converges more reliably than Kamada-Kawai. This links force-directed layout to [multidimensional scaling](/multidimensional-scaling/).
- **Multilevel methods.** Coarsen the graph by matching or clustering, lay out the small graph, and refine back up, which avoids poor local minima and handles large graphs.
- **Tutte's barycentric method.** Fix the outer face of a 3-connected [planar graph](/planar-graph/) on a convex polygon and put each other vertex at the mean of its neighbours: a linear system whose solution is a planar drawing, by the [Tutte spring theorem](/tutte-spring-theorem/).

## When to use it

Use it to look at a network of up to a few thousand vertices, when its clusters and overall shape matter more than exact positions: social networks, biological networks, small software graphs. For large graphs use a multilevel method with Barnes-Hut repulsion. When the drawing must be planar or must show a hierarchy, use a [planar straight-line drawing](/planar-straight-line-drawing/) or a layered method instead. For graphs where distances should be faithful, use stress majorization.

## Pitfalls

- **Too few rounds or too fast cooling.** The drawing freezes in a poor local minimum with folded parts. Start hot enough to let the drawing unfold, and cool slowly.
- **Hairballs.** Dense graphs with thousands of edges give a ball with no visible structure; no layout fixes that, and filtering or aggregating the graph helps more.
- **Disconnected input.** Components fly apart without a frame or a pull to the centre.
- **Coincident start positions.** The direction between two vertices at one point is undefined; a rule such as the one above, or a random start, is needed.
- **Reading distances as data.** Positions depend on the start and the run, so the distance between two vertices in the picture is not a measure of their relation.

## Implementations

## History

Tutte showed in 1963 that the barycentric drawing of a 3-connected planar graph is planar, the first drawing method defined by balanced forces. Peter Eades proposed the spring embedder in 1984. Kamada and Kawai in 1989 based the energy on graph distances, and Fruchterman and Reingold in 1991 gave the simple forces, the temperature and the grid, which most graph tools still use. Stress majorization (2004) and multilevel schemes in the following years made the methods reliable on large graphs.

## References
