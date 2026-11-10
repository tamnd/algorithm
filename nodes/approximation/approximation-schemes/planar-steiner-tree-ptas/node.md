---
tag: H3DF34
kind: algorithm
slug: planar-steiner-tree-ptas
name: PTAS for Steiner tree in planar graphs
aliases:
- Borradaile-Klein-Mathieu scheme
- brick decomposition PTAS
- planar Steiner tree approximation scheme
area: approximation/approximation-schemes
level: research
summary: Approximation scheme for Steiner tree on planar graphs using a planar decomposition into bounded-treewidth pieces.
solves: [steiner-tree-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, ε: the accuracy parameter, f: a function of ε alone}
  time: {worst: "O(n log n + f(ε) n)"}
  space: {extra: "O(f(ε) n)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2007
  people: [Glencora Borradaile, Philip Klein, Claire Mathieu]
  note: Borradaile, Kenyon-Mathieu and Klein gave the first PTAS for Steiner tree in planar graphs in 2007, and the journal paper of Borradaile, Klein and Mathieu in 2009 gave the O(n log n) form with the brick decomposition.
prereqs: [steiner-tree-problem, planar-graph, ptas, treewidth]
see_also: [baker-technique, baker-planar-ptas, planar-separator-theorem, tree-decomposition, steiner-tree-inapproximability, parameterized-steiner-tree, portal-based-dissection, planar-dual-graph]
sources:
  - paper: "G. Borradaile, P. Klein and C. Mathieu, An O(n log n) approximation scheme for Steiner tree in planar graphs, ACM Transactions on Algorithms 5(3), 2009, Article 31"
    title: Borradaile, Klein and Mathieu 2009
    locator: cutting open along an approximate tree, the mortar graph and bricks, the structure theorem, portals, and the dynamic program
  - paper: "G. Borradaile, C. Kenyon-Mathieu and P. Klein, A polynomial-time approximation scheme for Steiner tree in planar graphs, Proceedings of the 18th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2007"
    title: Borradaile, Kenyon-Mathieu and Klein 2007
    locator: the first PTAS for planar Steiner tree
  - paper: "M. Bateni, M. Hajiaghayi and D. Marx, Approximation schemes for Steiner forest on planar graphs and graphs of bounded treewidth, Journal of the ACM 58(5), 2011"
    title: Bateni, Hajiaghayi and Marx 2011
    locator: the extension of the brick decomposition to Steiner forest
  - paper: "S. E. Dreyfus and R. A. Wagner, The Steiner problem in graphs, Networks 1(3), 1971, pp. 195-207"
    title: Dreyfus and Wagner 1971
    locator: the exact dynamic program over subsets of terminals that the code uses on the portal graph
---

The scheme of Borradaile, Klein and Mathieu finds, for each fixed $\varepsilon > 0$, a [Steiner tree](/steiner-tree-problem/) of weight at most $(1 + \varepsilon)\,\mathrm{OPT}$ in a [planar graph](/planar-graph/) with nonnegative edge weights, in $O(n \log n)$ time. In general graphs the problem has no PTAS unless P = NP ([Steiner tree inapproximability](/steiner-tree-inapproximability/)), so planarity is what makes it possible. [Baker's technique](/baker-technique/) does not apply directly: its pieces have bounded diameter in edges, but the cost of a Steiner tree is a sum of weights. The key idea is the *brick decomposition*. A light planar subgraph, the *mortar graph*, splits the graph into faces called *bricks*; a structure theorem says that a near-optimal tree crosses each brick boundary only $\alpha(\varepsilon)$ times, so a few *portals* per brick are enough. Contracting the bricks then leaves a graph that becomes of bounded [treewidth](/treewidth/) after a cheap deletion, and a dynamic program solves it. This page gives an outline; the structure theorem and the dynamic program are sketched, not proved.

## In plain words

We want the cheapest set of roads in a flat road map that joins some given towns.

First we find a road network that is at most twice too expensive; this is easy. From it we build a frame of roads whose total cost is a fixed multiple of the best answer. The frame splits the map into regions, the bricks.

A good answer only needs to enter each brick at a few fixed gates on its border. Then each brick can be solved for every way of joining its gates, and the bricks can be put together by a table, since the frame has a simple shape once a few cheap roads are removed.

## The problem

The input is a connected planar graph $G$ with $n$ vertices and nonnegative edge weights $w$, a set $Q$ of $k$ terminals, and $\varepsilon > 0$. A *Steiner tree* is a tree in $G$ that contains every terminal; other vertices may be used. The goal is a Steiner tree of weight at most $(1 + \varepsilon)\,\mathrm{OPT}$. The problem is NP-hard on planar graphs, and an exact algorithm takes time exponential in $k$, such as the dynamic program of Dreyfus and Wagner over subsets of terminals, which takes $O(3^k n + 2^k n \log n)$ time when its shortest-path steps use Dijkstra's algorithm.

## The algorithm

```pseudo id=main
PLANAR-STEINER-PTAS(G, Q, ε)
L1  find a 2-approximate Steiner tree T, and cut G open along T so that every terminal lies on the outer face
L2  build the mortar graph MG from the outer face and short paths, of weight at most f(ε)·OPT; its faces are the bricks
L3  put θ(ε) portals on the boundary of each brick, spaced evenly by length
L4  build B+: a copy of each brick, joined to MG only at its portals by edges of weight 0
L5  solve B+: contract the bricks, delete a light class of breadth-first levels to get bounded treewidth, and run a dynamic program whose brick states are non-crossing partitions of the portals
L6  map the tree back to G, and return a spanning tree of it
```

A *brick* is the part of the graph inside one face of $MG$, together with the face boundary. In the paper, each brick boundary consists of four paths, and two of them are *short*: the distance along the path between two of its vertices is at most $1 + \varepsilon$ times their distance in the graph. The bricks share only their boundaries, so a solution decomposes into pieces inside bricks that meet only on $MG$.

**What the code covers.** The code works on weighted grid graphs. Line L1 is the shortest-path 2-approximation, without cutting open. Line L2 uses the lines of a coarse grid as the mortar graph, in place of the construction from short paths, so the bound $w(MG) \le f(\varepsilon)\,\mathrm{OPT}$ does not hold for it. Lines L3, L4 and L6 are as above. Line L5 solves $B^+$ exactly with the Dreyfus-Wagner algorithm in place of the dynamic program. The code also lists the connection states of a brick and checks that they are non-crossing.

## Example

Take the $9 \times 9$ grid with unit weights, with the mortar graph on the rows and columns $0$, $4$ and $8$. It has 45 vertices and splits the grid into 4 bricks of $5 \times 5$ vertices, so $B^+$ has $45 + 4 \cdot 25 = 145$ vertices. Let the terminals be $(2, 3)$ and $(2, 5)$, inside two different bricks. The optimum is the path of weight 2 through $(2, 4)$, on the mortar column 4.

| portals on each side | portals per brick | $\mathrm{OPT}(B^+)$ | tree returned |
|---|---|---|---|
| the corners | 4 | 6 | 6 |
| corners and midpoints | 8 | 2 | 2 |
| every boundary vertex | 16 | 2 | 2 |

With corner portals only, each terminal must reach a corner such as $(0, 4)$ or $(4, 4)$, at distance 3 from each, so the best tree in $B^+$ weighs 6. With the midpoint $(2, 4)$ as a portal, the optimum is kept.

On a $9 \times 9$ grid with weights from 1 to 9, drawn with seed 13, and the terminals $(0, 4)$, $(2, 8)$, $(4, 8)$ and $(6, 0)$, the optimum is 61 and the 2-approximation gives 70. The scheme gives 66, 63 and 61 with 4, 8 and 16 portals per brick.

## Correctness

**Theorem (Borradaile, Klein and Mathieu 2009, sketch).** For each fixed $\varepsilon$, the algorithm returns a Steiner tree of weight at most $(1 + c\varepsilon)\,\mathrm{OPT}$ for an absolute constant $c$, so running it with $\varepsilon / c$ gives the ratio $1 + \varepsilon$.

The proof file has these steps.

1. **The approximate tree.** Line L1 gives weight at most $2(1 - 1/k)\,\mathrm{OPT}$. Proved in full.
2. **Mapping back.** A tree in $B^+$ maps to a connected subgraph of $G$ of no larger weight, so the output is feasible and $\mathrm{OPT} \le \mathrm{ALG} \le \mathrm{OPT}(B^+)$. Proved in full.
3. **The cost of portals.** Without the structure theorem, $\mathrm{OPT}(B^+) \le \mathrm{OPT} + 2 \sum_B w(\partial B)$, more portals never hurt, and portals at every boundary vertex lose nothing. Proved in full.
4. **Brick states.** By planarity, the ways a brick can join its portals are non-crossing partitions, at most the Catalan number $C_\theta$ of them. Proved in full.
5. **The structure theorem.** Some tree of weight at most $(1 + c\varepsilon)\,\mathrm{OPT}$ crosses each brick boundary at most $\alpha(\varepsilon)$ times, and moving the crossings to $\theta(\varepsilon)$ portals costs at most $\varepsilon\,\mathrm{OPT}$. Sketch.
6. **The dynamic program.** Deleting a light class of levels costs at most $\varepsilon\,\mathrm{OPT}$ and leaves bounded treewidth. Sketch.

## Complexity

- **Time.** $O(n \log n)$ for each fixed $\varepsilon$, with a factor that depends on $\varepsilon$ only; the WADS 2007 title of the work speaks of a singly exponential dependence on $\varepsilon$.
- **States.** At most $C_\theta \le 4^\theta$ connection states per brick, with $\theta$ a function of $\varepsilon$.
- **The code.** $O(3^k n + 2^k n \log n)$ for the exact solve of $B^+$, which has $O(n)$ vertices.

## Properties

- **Deterministic.**
- **An EPTAS.** The exponent of $n$ does not grow with $1/\varepsilon$, so the scheme is an [EPTAS](/eptas/).
- **Planar only.** The structure theorem uses the plane embedding. The method extends to graphs of bounded genus.

## Variants and improvements

- **Steiner forest.** Bateni, Hajiaghayi and Marx (2011) extended the method to Steiner forest in planar graphs, with a separate scheme for graphs of bounded treewidth.
- **TSP and other problems.** The same framework of a light spanner-like subgraph, contraction and bounded treewidth gives schemes for the TSP in planar graphs (Klein 2008) and related problems.
- **Exact algorithms.** For small $k$, exact algorithms such as Dreyfus-Wagner, or [parameterized algorithms](/parameterized-steiner-tree/), are simpler.

## When to use it

Use the scheme as a proof that planar Steiner tree has an EPTAS, or as the template for a scheme for a related planar problem. In practice, a 2-approximation followed by local search, or an exact solver for few terminals, is much faster.

## Pitfalls

- **Weights, not hops.** Baker's layers bound the number of edges, not the weight, so they do not give a scheme for Steiner tree by themselves. The mortar graph is what ties the deletions to $\mathrm{OPT}$.
- **Portals by length.** The portals must be spaced by weight along the brick boundary, not by the number of vertices, or a heavy gap can make moving a crossing expensive.
- **Cutting open.** After cutting along $T$, a vertex of $T$ has several copies, and a solution must be mapped back by joining them.
- **The bound $f(\varepsilon)$.** A mortar graph that is not light, like the coarse grid in the code, makes the cost of portals grow with the grid, not with $\mathrm{OPT}$.

## Implementations

## History

Borradaile, Kenyon-Mathieu and Klein gave the first PTAS for Steiner tree in planar graphs at SODA 2007. A WADS 2007 paper of Borradaile, Klein and Mathieu gave the $O(n \log n)$ form with a singly exponential dependence on $\varepsilon$, and the journal paper appeared in ACM Transactions on Algorithms in 2009. Bateni, Hajiaghayi and Marx extended the brick decomposition to Steiner forest.

## References
