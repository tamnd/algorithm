---
tag: GGH2BB
kind: algorithm
slug: newest-vertex-bisection
name: Newest vertex bisection
area: scientific-computing/finite-element-practice
level: core
summary: Refines a triangle by cutting from its newest vertex to the opposite edge, with a closure step to avoid hanging nodes, keeping angles bounded.
model: real-ram
complexity:
  vars: {M: the number of triangles of the mesh before the call}
  time: {average: "Θ(M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, conforming_output: true, nested_meshes: true, bounded_similarity_classes: true}
history:
  year: 1972
  people: [E. G. Sewell, William F. Mitchell, Peter Binev, Wolfgang Dahmen, Ronald DeVore]
  note: Sewell introduced the newest vertex rule in his 1972 Purdue thesis. Mitchell gave the recursive form in 1989, and Binev, Dahmen and DeVore proved the closure estimate in 2004.
prereqs: [finite-element-method, mesh-generation]
see_also: [adaptive-finite-element-method, dorfler-marking, afem-optimality-theorem, residual-error-estimator, adaptive-mesh-refinement, anisotropic-mesh-adaptation, delaunay-triangulation, lagrange-finite-element]
sources:
  - paper: doi:10.1145/76909.76912
    title: William F. Mitchell, A comparison of adaptive refinement techniques for elliptic problems, ACM Transactions on Mathematical Software 15(4) (1989) 326-347
    locator: newest node bisection, its recursive form and the bound on the similarity classes
  - paper: doi:10.1007/s00211-003-0492-7
    title: Peter Binev, Wolfgang Dahmen and Ronald DeVore, Adaptive finite element methods with convergence rates, Numerische Mathematik 97(2) (2004) 219-268
    locator: Section 2 (newest vertex bisection, compatible initial labeling and the closure estimate)
  - paper: doi:10.1007/s00365-013-9192-4
    title: Michael Karkulik, David Pavlicek and Dirk Praetorius, On 2D newest vertex bisection, optimality of mesh-closure and H1-stability of L2-projection, Constructive Approximation 38(2) (2013) 213-234
    locator: the closure estimate in 2D for an arbitrary initial labeling
  - paper: doi:10.2478/cmam-2011-0026
    title: Stefan Funken, Dirk Praetorius and Philipp Wissgott, Efficient implementation of adaptive P1-FEM in Matlab, Computational Methods in Applied Mathematics 11(4) (2011) 460-490
    locator: the refinement by marked edges, the closure loop and the vectorized bisection
---

Newest vertex bisection (NVB) refines a triangle mesh locally for the [adaptive finite element method](/adaptive-finite-element-method/). Each triangle stores one of its vertices as the newest vertex, and the opposite edge is its refinement edge. A bisection cuts the triangle from the newest vertex to the midpoint of the refinement edge, and the midpoint becomes the newest vertex of both children. A closure step bisects more triangles until no vertex lies in the middle of an edge of another triangle, so the mesh stays conforming and a continuous [Lagrange element](/lagrange-finite-element/) space can live on it. The rule never makes thin triangles: all descendants of one initial triangle fall into at most four similarity classes, so the angles stay bounded below by a constant that depends only on the initial mesh.

## In plain words

Cut a triangle in two, from one corner to the middle of the opposite side. The new point becomes the special corner of both halves, and the next cut of each half starts from there. Because the cut always starts at the newest corner, the halves never get very thin. After a few cuts, the triangles repeat the same few shapes at smaller and smaller sizes. A cut puts a new point in the middle of a side. The triangle on the other side of that side does not have this point as a corner, so it must also be cut. That cut may force another one, and so on. The closure step follows this chain until every point is a corner of all the triangles around it.

## The problem

**Input.** A conforming triangulation $\mathcal{T}$ of a polygon $\Omega \subset \mathbb{R}^2$, where every triangle is an ordered triple $[z_1, z_2, z_3]$ of vertex numbers. The edge $z_1z_2$ is the refinement edge, and $z_3$ is the newest vertex. A set $\mathcal{M} \subset \mathcal{T}$ of marked triangles, usually from [Dorfler marking](/dorfler-marking/). A list of boundary edges.

**Output.** The coarsest conforming triangulation $\mathcal{T}'$ that we get from $\mathcal{T}$ by newest vertex bisections and in which every marked triangle is bisected at least once, with the refinement edges of the new triangles and the split boundary edges.

## The algorithm

The code uses the form with marked edges of Funken, Praetorius and Wissgott. First it finds the set $S$ of edges that must be split. Then it bisects each triangle one, two or three times, according to which of its edges are in $S$. This works in one pass because a bisection makes the two old edges $z_3z_1$ and $z_2z_3$ the refinement edges of the two children. So one triangle can split each of its three edges with at most three bisections, and the refinement edge always goes first.

```pseudo id=main
REFINE(T, M)                    ▷ each triangle is [z1, z2, z3]; z1z2 is its refinement edge
L1  S <- the refinement edges of the triangles in M; push each of them on a stack
L2  while the stack is not empty do pop an edge e
L3      for each triangle T of the mesh that contains e do
L4          if the refinement edge r of T is not in S then add r to S and push r
L5  for each edge in S do create its midpoint
L6  for each triangle [z1, z2, z3] with z1z2 in S do bisect it at the midpoint m of z1z2 into [z3, z1, m] and [z2, z3, m]
L7      look up the midpoints l of z3z1 and r of z2z3, if these edges are in S
L8      if z3z1 is in S then bisect [z3, z1, m] into [m, z3, l] and [z1, m, l]
L9      if z2z3 is in S then bisect [z2, z3, m] into [m, z2, r] and [z3, m, r]
L10 return the new triangles, and split every boundary edge in S into two
```

Triangles with no edge in $S$ are kept as they are. Line L4 is the closure rule. If some edge of $T$ will be split, then $T$ must be bisected, and its first bisection always cuts its refinement edge.

**Initial labels.** The labels of the initial mesh fix all later bisections. A labeling is compatible if every interior refinement edge is the refinement edge of both triangles that share it. Then the closure of a single triangle stops after the neighbor across the edge. On a mesh made of squares cut along one diagonal, the diagonals are a compatible choice. Every conforming triangulation in 2D has a compatible labeling (Mitchell 1989; Binev, Dahmen and DeVore 2004, Section 2). Labeling by the longest edge does not always give one.

## Example

Take the unit square with corners $v_0 = (0,0)$, $v_1 = (1,0)$, $v_2 = (1,1)$, $v_3 = (0,1)$ and the two triangles $[v_0, v_2, v_1]$ and $[v_2, v_0, v_3]$. Both have the diagonal $v_0v_2$ as refinement edge, so the labeling is compatible. The reference code gives the following steps.

| Step | Marked triangle | Edges put in $S$ | New vertices | Triangles |
|---|---|---|---|---|
| 0 | none | none | none | 2 |
| 1 | $[v_0, v_2, v_1]$ | $v_0v_2$ | $v_4 = (0.5, 0.5)$ | 4 |
| 2 | all 4 | the 4 sides of the square | $v_5 = (0.5, 0)$, $v_6 = (1, 0.5)$, $v_7 = (0.5, 1)$, $v_8 = (0, 0.5)$ | 8 |
| 3 | $[v_0, v_4, v_5]$ | $v_0v_4$ | $v_9 = (0.25, 0.25)$ | 10 |
| 4 | $[v_4, v_5, v_9]$ | $v_4v_5$, then $v_4v_1$ | $(0.5, 0.25)$, $(0.75, 0.25)$ | 14 |

In step 1, line L1 puts the diagonal in $S$. Line L3 visits the other triangle $[v_2, v_0, v_3]$, but its refinement edge is the same diagonal, so line L4 adds nothing. Both triangles are bisected once, and the result is $[v_1, v_0, v_4]$, $[v_2, v_1, v_4]$, $[v_3, v_2, v_4]$, $[v_0, v_3, v_4]$. All four have the new vertex $v_4$ as newest vertex and a side of the square as refinement edge.

Step 4 shows the closure. The marked triangle has the refinement edge $v_4v_5$, which is the vertical segment from $(0.5, 0.5)$ to $(0.5, 0)$. Its neighbor across that edge is $[v_4, v_1, v_5]$, and the refinement edge of the neighbor is $v_4v_1$, not $v_4v_5$. So line L4 adds $v_4v_1$ to $S$. The triangle on the other side of $v_4v_1$ is $[v_1, v_4, v_6]$, and its refinement edge is $v_1v_4$ itself, so the chain stops. Lines L6 to L9 then bisect $[v_4, v_5, v_9]$ once, $[v_1, v_4, v_6]$ once and $[v_4, v_1, v_5]$ twice (first at $v_4v_1$ and then the child that contains $v_4v_5$). The count is $10 - 3 + 2 + 2 + 3 = 14$ triangles, and no vertex hangs.

**Shapes.** The test file refines the scalene triangle $(0,0)$, $(1,0)$, $(0.3, 0.7)$ twelve times with random marks. After 12 steps the mesh is conforming and has at most four distinct triangle shapes up to similarity, for each of the three choices of the first refinement edge. Marking all triangles of this single triangle mesh eight times gives $2^8 = 256$ triangles with total area $0.35$.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). Every edge enters the stack at most once, so the closure loop stops. When the loop ends, every triangle that has some edge in $S$ also has its refinement edge in $S$. So each triangle falls into one of four cases (no split, one, two or three bisections), and in each case the parent edges in $S$ appear as two halves on both sides and the other parent edges stay whole. So the output is conforming. Minimality follows by induction over the order in which edges enter $S$: a conforming refinement that bisects the marked triangles must split every edge in $S$, because a split edge leaves a hanging node on the neighbor until the neighbor is bisected, and a bisection always starts at the refinement edge. The test file checks the output against a second method that bisects triangles with hanging nodes until none is left, on nine random steps on the L-shaped domain.

## Complexity

With a hash map from edges to triangles, one call costs $\Theta(M)$ expected time in the real-RAM model for a mesh of $M$ triangles: building the map, the closure (each edge is pushed at most once and has at most two triangles) and the bisection are all linear. The memory is $\Theta(M)$. The output has at most $4M$ triangles.

One call can bisect triangles far from the marked ones, because a closure chain can be long. So the size of one step is not bounded by a constant times $\#\mathcal{M}$. The bound holds on average over the whole adaptive loop. Binev, Dahmen and DeVore proved that, for a compatible initial labeling, $\#\mathcal{T}_k - \#\mathcal{T}_0 \le C\sum_{j=0}^{k-1}\#\mathcal{M}_j$ with $C$ that depends only on $\mathcal{T}_0$. Karkulik, Pavlicek and Praetorius proved the same estimate in 2D with no condition on the initial labeling. This closure estimate is one of the three parts of the [AFEM optimality theorem](/afem-optimality-theorem/).

## Properties

- **Conformity.** The output has no hanging nodes, so P1 functions on it are continuous, and the P1 space of $\mathcal{T}$ is a subspace of the P1 space of $\mathcal{T}'$.
- **Shape regularity.** All descendants of one initial triangle are similar to at most four triangles (Sewell 1972; Mitchell 1989). The minimum angle and the ratio of diameter to inradius stay bounded by constants that depend only on $\mathcal{T}_0$.
- **Area halving.** Each bisection halves the area. A triangle of generation $g$ has area $2^{-g}$ times the area of its initial ancestor.
- **Uniform refinement.** With a compatible labeling, two rounds of marking every triangle cut each triangle into four triangles of area one quarter. All three edges of the parent are split at their midpoints.
- **Binary tree.** The refinements of one initial triangle form a binary tree of bisections, so the set of all NVB meshes is a lattice: two NVB refinements of $\mathcal{T}_0$ have a coarsest common refinement. The optimality proofs use this overlay.
- **Orientation.** The children keep the orientation of the parent, as the test file checks with signed areas.

## Variants and improvements

- **Recursive form.** Mitchell refines a marked triangle by first refining its neighbor across the refinement edge if the two edges do not agree, recursively, and then bisecting both together. The result is the same mesh as the form with marked edges.
- **More bisections per marked triangle.** Some codes split all three edges of each marked triangle, which gives four children in one step. The convergence proof of Morin, Nochetto and Siebert (2000) needed several bisections, so that each marked triangle gets a new vertex inside it. Cascon, Kreuzer, Nochetto and Siebert (2008) showed that one bisection is enough.
- **Longest edge bisection.** Rivara cuts each triangle at its longest edge. The angles also stay bounded, but the closure is longer and the theory of optimal rates is less complete.
- **Red-green refinement.** Bank, Sherman and Weiser cut a marked triangle into four similar children (red) and remove hanging nodes with temporary bisections (green). The green triangles must be removed before the next step.
- **Higher dimensions.** Bansch, Kossaczky, Maubach and Traxler gave bisection rules for tetrahedra. Stevenson extended the closure estimate to any dimension under a condition on the initial mesh.
- **Coarsening.** The binary tree makes coarsening simple: two children with the same parent can be merged back if no neighbor needs them. The 2004 algorithm of Binev, Dahmen and DeVore used coarsening, and later proofs removed it.

## When to use it

Use NVB for adaptive finite elements on triangles, especially when the code must follow the theory of convergence rates: the closure estimate, the bounded shapes and the nested spaces are exactly what the proofs need. It is simple to store, because each triangle only needs the order of its vertices. For meshes that must stretch in one direction, for example along boundary layers, NVB is the wrong tool, because it keeps the shapes of the initial mesh; use [anisotropic mesh adaptation](/anisotropic-mesh-adaptation/). For structured grids with block refinement in time dependent problems, use [block-structured AMR](/berger-colella-amr/).

## Pitfalls

- **Vertex order.** The refinement edge must be stored as $z_1z_2$ in every triangle. A mesh generator that outputs counterclockwise triples with no thought about labels gives a valid labeling, but it can be far from compatible, and then the closure chains get long.
- **Missed boundary split.** If the list of boundary edges is not split with the triangles, the midpoints of Dirichlet edges become free nodes, and the solve imposes a wrong boundary condition with no error message.
- **Hash keys.** The edge $z_1z_2$ and the edge $z_2z_1$ must give the same key. Store each edge as the pair (smaller number, larger number).
- **Mixed refinement rules.** Mixing NVB with other cuts, such as red refinement on some triangles, breaks the bound on similarity classes and the closure estimate.
- **Cost of one step.** Do not expect one call to bisect only a few triangles beyond the marked ones. The bound on the number of extra triangles holds only summed over all steps.
- **Floating point midpoints.** Computing midpoints again from coordinates for each triangle can give two different nodes for one edge after many levels. Create each midpoint once per edge, as line L5 does.

## Implementations

## History

E. G. Sewell introduced the newest vertex rule in his 1972 PhD thesis at Purdue University, and showed that the descendants of a triangle fall into a few similarity classes. William Mitchell gave the recursive refinement and compared it with other adaptive refinement methods in 1989. Eberhard Bansch, Igor Kossaczky, Joseph Maubach and Christoph Traxler extended bisection to tetrahedra in the 1990s. Peter Binev, Wolfgang Dahmen and Ronald DeVore proved in 2004 that the closure does not spoil the complexity of the adaptive loop, which made optimal rates for adaptive finite elements possible. Rob Stevenson extended this to higher dimensions, and Michael Karkulik, David Pavlicek and Dirk Praetorius removed the condition on the initial labeling in 2D in 2013.

## References
