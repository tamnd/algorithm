---
tag: ZDC65T
kind: algorithm
slug: blossom-quad
name: Blossom-Quad
aliases:
- blossom quad meshing
area: cad/mesh-generation-for-analysis
level: research
summary: Remacle and coauthors' indirect quad mesher that pairs triangles into quads by a minimum cost perfect matching found with Edmonds' blossom algorithm.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of triangles}
  time: {worst: O(n^3)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 2012
  people: [Jean-François Remacle, Jonathan Lambrechts, Bruno Seny, Emilie Marchandise, Amaury Johnen, Christophe Geuzaine]
  note: Remacle and coauthors published Blossom-Quad in 2012; it merges the triangles of a mesh into quads all at once by a minimum cost perfect matching, and it is part of the Gmsh mesh generator.
prereqs: [minimum-weight-perfect-matching, edmonds-blossom, perfect-matching]
see_also: [q-morph, paving, maximum-weight-matching, petersens-theorem, matching-polytope, mesh-quality-measures, delaunay-triangulation, finite-element-method]
sources:
  - paper: doi:10.1002/nme.3279
    title: Jean-François Remacle, Jonathan Lambrechts, Bruno Seny, Emilie Marchandise, Amaury Johnen and Christophe Geuzaine, Blossom-Quad, a non-uniform quadrilateral mesh generator using a minimum-cost perfect-matching algorithm, International Journal for Numerical Methods in Engineering 89(9), 2012, 1102 to 1119
    locator: the dual graph of the triangles, the quality cost of a quad, the perfect matching, and the results (general locator)
  - paper: doi:10.6028/jres.069B.013
    title: Jack Edmonds, Maximum matching and a polyhedron with 0,1-vertices, Journal of Research of the National Bureau of Standards 69B, 1965, 125 to 130
    locator: the weighted matching algorithm and the matching polytope (general locator)
  - paper: doi:10.1145/6462.6502
    title: Zvi Galil, Efficient algorithms for finding maximum matching in graphs, ACM Computing Surveys 18(1), 1986, 23 to 38
    locator: the O(n^3) weighted matching algorithm for general graphs (general locator)
---

Blossom-Quad is a method that turns a triangle mesh into a quad mesh by pairing every triangle with a neighbour. Two triangles that share an edge make a quad when the shared edge is removed. A good pairing uses each triangle exactly once and makes quads that are close to rectangles. Blossom-Quad states this as a graph problem: the triangles are the nodes of the dual graph, each pair that makes a convex quad is an edge with a cost that measures how bad the quad is, and the best pairing is a minimum cost perfect matching. Edmonds' blossom algorithm finds that matching exactly in polynomial time. Jean-François Remacle and his coauthors published the method in 2012. It finds the best pairing for the given triangles, but a perfect matching need not exist, and the method gives no bound on the worst quad.

## In plain words

You have a floor covered with triangular tiles and you want four sided tiles. Two triangles that touch along a side can be glued into one four sided tile. You must glue every triangle to exactly one neighbour, and you want the glued tiles to look as much like rectangles as possible.

If you glue the best looking pair first, then the next best, and so on, you can end up with lonely triangles that have no free neighbour left. So instead, give every possible pair a score and ask a classic method from graph theory for the set of pairs that uses every triangle once and has the best total score. That method, the blossom method, never gets stuck where the greedy choice does.

## The problem

The input is a conforming triangle mesh with an even number of triangles. The output is a conforming quad mesh of the same region with the same vertices, in which every quad is the union of two triangles that share an edge and is strictly convex, and the sum of the costs of the quads is as small as possible; or a report that no such quad mesh exists.

## The algorithm

The cost of a quad here is $1 - \eta$, with the angle quality $\eta = \max(0, 1 - \tfrac{2}{\pi} \max_k |\tfrac{\pi}{2} - \alpha_k|)$ over the four corner angles $\alpha_k$, so a rectangle has cost 0. The cost is scaled by $10^6$ and rounded to an integer, so the matching is exact for the rounded costs. This measure and the scale are parameters of this code; the paper defines its own quality of a quad.

```pseudo id=main
BLOSSOM-QUAD(T)
L1  if the number of triangles is odd then fail
L2  build the dual graph: one node per triangle
L3  for each pair of triangles that share an edge and form a strictly convex quad, add a dual edge with the cost of that quad
L4  M ← a minimum cost perfect matching of the dual graph, by Edmonds' weighted blossom algorithm
L5  if the dual graph has no perfect matching then fail
L6  for each pair in M, remove the shared edge and make the quad
L7  return the quads
```

L4 runs the weighted blossom algorithm in Galil's $O(n^3)$ primal-dual form as a [maximum weight matching](/maximum-weight-matching/), with the weight $K + C - c$ for the cost $c$, where $C$ is larger than every cost and $K = nC$. With this $K$, a larger matching always weighs more, so the maximum weight matching is perfect when a perfect matching exists, and among the perfect matchings it has the least cost. The weights are integers, so all dual values stay integers and every test is exact. The convexity test in L3 uses exact [orientation tests](/orientation-test/).

## Example

Take the centre $o = (0, 0)$ and the six points $p_1 = (2, 0)$, $p_2 = (1, 2)$, $p_3 = (-1, 2)$, $p_4 = (-2, 0)$, $p_5 = (-1, -2)$ and $p_6 = (1, -2)$, with the six triangles $o p_s p_{s+1}$ around $o$. Neighbouring triangles share an edge $o p_s$, so the dual graph is a cycle of six nodes. Removing the edge $o p_1$ or $o p_4$ gives a quad with an angle of $126.9°$ at $o$ and quality $0.590$; removing $o p_2$, $o p_3$, $o p_5$ or $o p_6$ gives a quad whose worst angle is $116.6°$, with quality $0.705$.

A cycle of six nodes has two perfect matchings: remove the edges at $p_1, p_3, p_5$, or the edges at $p_2, p_4, p_6$. Each has qualities $0.590$, $0.705$ and $0.705$, a total cost of $1.000$. The greedy choice fails here: it takes a pair of quality $0.705$ first, say the one across $o p_2$, then the next free pair of quality $0.705$, the one across $o p_5$, and the two triangles left over, $o p_3 p_4$ and $o p_6 p_1$, are not neighbours. The blossom algorithm returns a perfect matching.

Move $p_1$ to $(3, 0)$. The pairs across $o p_2$ and $o p_6$ now have quality $0.5$. The matching at $p_1, p_3, p_5$ costs $1.000$ and the one at $p_2, p_4, p_6$ costs $1.410$, and the blossom algorithm returns the first.

## Correctness

The proof file shows that the merges of a triangle mesh into strictly convex quads are exactly the perfect matchings of the convex dual graph. A matched pair loses only its shared edge, every other directed edge stays and is used once, and no vertex moves, so the quads form a conforming mesh of the same region with the same boundary. The parity rule follows from counting edge sides: $4Q = 2E_\text{int} + E_\text{bnd}$, so a quad mesh has an even number of boundary edges, and a triangle mesh with an odd number of boundary edges has an odd number of triangles.

The reduction from the minimum cost perfect matching to the maximum weight matching is proved. The optimality of Edmonds' algorithm is the classical primal-dual theorem; the proof file outlines it, and the tests compare the code with a brute force over all matchings, on random graphs and on triangle meshes of at most 12 triangles.

Not proved, because it is false: that a perfect matching always exists. A triangle with one ear on each of its sides has four triangles, but its dual graph is a star, and two ears can never be paired. Also not proved: any bound on the worst quad, since the matching minimises the sum of the costs.

## Complexity

The dual graph has $n$ nodes and at most $3n/2$ edges. The weighted blossom algorithm in this code runs in $O(n^3)$ time. Faster forms run in $O(n m + n^2 \log n)$, or $O(n^2 \log n)$ for the sparse dual graph, and practical codes for minimum cost perfect matching are fast on large meshes. The dual graph and the merge cost $O(n)$.

## Properties

- **Global.** The pairing is optimal for the whole mesh, not built pair by pair, so it never strands a triangle when a perfect pairing exists.
- **Exact.** With integer costs, the matching is exactly optimal.
- **Indirect.** The quality of the quads depends on the triangle mesh; triangles close to right isosceles triangles give near squares.
- **No vertices added.** The quads use the vertices of the triangle mesh.
- **Parity.** The number of triangles must be even, which is the same as an even number of boundary edges.
- **No guarantee.** A perfect matching may not exist, and no bound on the worst quad is known.

## Variants and improvements

- **Q-Morph.** An advancing front of quads over the triangle mesh, which aligns the quads with the boundary better; see [Q-Morph](/q-morph/).
- **Paving.** A direct method that places rows of quads from the boundary; see [Paving](/paving/).
- **All-quad by splitting.** Splitting each quad of a quad-dominant mesh into four quads, and each leftover triangle into three, always gives an all-quad mesh at the cost of more elements and worse angles.
- **Existence.** For a closed surface, the dual graph is cubic, and when it has no bridge, [Petersen's theorem](/petersens-theorem/) gives a perfect matching, if all pairs are allowed; for planar meshes with a boundary there is no such result, and a mesher must fix the mesh near the boundary.
- **Other costs.** Any cost that adds over the quads works, for example one that measures alignment with a direction field.

## When to use it

Use Blossom-Quad when you need a quad mesh from a triangle mesh and you want the best global pairing, for example for finite element analysis with quads, or to make a quad-dominant mesh with few triangles left. It is fast and simple when a good triangle mesh is given. If quads must follow the boundary in rows, Q-Morph or paving is better. If an all-quad mesh is required for every input, add a fallback for the case without a perfect matching.

## Pitfalls

- **Odd counts.** An odd number of triangles cannot be paired. Fix the count, for example by changing the number of boundary edges.
- **Greedy pairing.** Pairing the best quads first can strand triangles. Use a matching algorithm.
- **Non-convex pairs.** Two triangles can form a non-convex or flat quad. Leave such pairs out of the dual graph, or give them a very high cost.
- **Float costs.** Ties and rounding in float costs can make the matching depend on the order of the edges. Use integer costs, or accept that ties are broken arbitrarily.
- **No perfect matching.** The dual graph can lack a perfect matching even with an even count. Detect it and change the mesh.

## Implementations

## History

Jean-François Remacle, Jonathan Lambrechts, Bruno Seny, Emilie Marchandise, Amaury Johnen and Christophe Geuzaine published Blossom-Quad in the International Journal for Numerical Methods in Engineering in 2012. Earlier indirect methods merged triangles into quads by local or greedy rules, which can leave unpaired triangles. Blossom-Quad replaced those rules with an exact optimisation, using Jack Edmonds' 1965 algorithm for weighted matching in general graphs, whose odd cycles, the blossoms, give the method its name. The method is part of the open source mesh generator Gmsh.

## References
