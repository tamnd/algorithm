---
tag: 5037C3
kind: algorithm
slug: attributed-adjacency-graph
name: Attributed adjacency graph recognition
aliases:
- AAG feature recognition
- Joshi-Chang feature recognition
area: cad/solid-modeling
level: advanced
summary: Joshi and Chang's method that labels the face adjacency graph of a B-rep with edge convexity and finds features as subgraphs that match templates.
solves: [feature-recognition]
model: word-ram
complexity:
  vars: {E: the number of polygon edges of the input, n: the number of faces, t: the number of templates, k: the largest number of faces in a template}
  time: {worst: O(E log E + n t k! k^2)}
  space: {extra: O(E)}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1988
  people: [S. Joshi, T. C. Chang]
  note: Joshi and Chang defined the attributed adjacency graph of a polyhedral solid, with each arc marked convex or concave, and recognized machined features as the components left after the faces with only convex edges are deleted.
prereqs: [feature-recognition, subgraph-isomorphism]
see_also: [feature-based-modeling, boundary-representation, ullmann-algorithm, vf2-algorithm, orientation-test, catastrophic-cancellation, pocket-machining, mesh-segmentation]
sources:
  - paper: doi:10.1016/0010-4485(88)90050-4
    title: S. Joshi and T. C. Chang, Graph-based heuristics for recognition of machined features from a 3D solid model, Computer-Aided Design 20(2), 58 to 66, 1988
    locator: the whole paper (the definition of the attributed adjacency graph, with 0 for a concave and 1 for a convex arc, the deletion of faces with only convex arcs, and the matching of the remaining components with feature graphs)
  - paper: doi:10.1109/70.897789
    title: JungHyun Han, Mike Pratt and William C. Regli, Manufacturing feature recognition from solid models, a status report, IEEE Transactions on Robotics and Automation 16(6), 782 to 796, 2000
    locator: the section on graph-based recognition and its trouble with interacting features
  - book: isbn:9780471002147
    title: Jami J. Shah and Martti Mäntylä, Parametric and Feature-Based CAD/CAM, Concepts, Techniques, and Applications, Wiley, 1995
    locator: the part on feature recognition, graph-based methods (chapter number not checked)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.4, Subgraph isomorphism (the matching step is NP-complete when the templates are part of the input)
---

Attributed adjacency graph recognition finds machining features in a polyhedral solid by looking at a graph instead of at the geometry. Each face of the [B-rep](/boundary-representation/) is a node, each edge between two faces is an arc, and each arc carries one attribute: 1 if the edge is convex and 0 if it is concave. A depression feature such as a slot or a pocket is a group of faces joined by concave edges, so Joshi and Chang (1988) delete every face whose edges are all convex, and match each connected group that is left with a library of feature graphs. The matching is a labeled [subgraph isomorphism](/subgraph-isomorphism/) test; it is NP-complete in general and fast for the small templates of real libraries.

## In plain words

Look at the edges of a part with a slot cut into its top. Most edges stick out, like the edges of a box. The edges at the bottom of the slot go in, like the inside corner of a room.

The method draws a map: one dot for each face of the part, a line between two dots when the faces touch, and a mark on each line that says whether the edge sticks out or goes in. Then it rubs out every dot whose lines all stick out, because a face like that is part of the outside of the box, not of a hole or a slot.

What is left falls apart into small groups. Each group is compared with a picture book of known features: two walls and a floor make a slot, four walls and a floor make a pocket.

## The problem

The input is a polyhedral solid, given as planar polygons with integer vertices, and an ordered list $T$ of templates. Each polygon is listed counterclockwise when seen from outside the solid, so that its normal $n_P$, computed by the right-hand rule, points out of the material. The polygons form a closed conforming mesh: every directed edge $(p, q)$ of a polygon is matched by exactly one edge $(q, p)$ of another polygon. A face of the solid may be split into several polygons. A template is a small graph whose arcs are labeled with 0 or 1, together with a feature name.

The output is the attributed adjacency graph $G$ of the solid, and for each connected component $C$ of $G$ minus the faces with only convex arcs, the first template that is isomorphic to $C$ as a labeled graph, with the map of the faces, or the report that $C$ matches no template. This is the surface-based version of [feature recognition](/feature-recognition/), with the extra choice of Joshi and Chang that a feature is a whole component.

## The algorithm

```pseudo id=main
AAG-RECOGNIZE(B, T)
L1  for each directed edge (p, q) of a polygon P of B, find the polygon P' that holds (q, p)
L2      s ← sign((n_P × n_P') · (q − p))                  ▷ exact, integer coordinates
L3      if s = 0 and n_P · n_P' > 0 then merge the faces of P and P'
L4      else if s = 0 then reject B                     ▷ a knife edge
L5  G ← a node per merged face, an arc {F, F'} labeled 1 for each edge with s > 0 and 0 for s < 0
L6  H ← G without the nodes whose arcs are all labeled 1
L7  for each connected component C of H do
L8      for each template t in T, in order, do
L9          if MATCH(t, C) then report (t, C) and continue with the next component
L10     report C as unrecognized

MATCH(t, C)
L11 if t and C have different numbers of nodes then return false
L12 map the nodes of t to distinct nodes of C one at a time, by backtracking
L13     keep a partial map only if each pair of mapped nodes has the same label, or no arc, in t and in C
L14 return true if some map covers all nodes of t
```

The normal of a polygon is its Newell vector, $\sum_i (y_i - y_{i+1})(z_i + z_{i+1})$ and its two cyclic shifts, which is twice the area times the unit outward normal. For an edge running from $p$ to $q$ in the loop of $P$, the face of $P$ lies on the left of the edge when seen from outside, and the sign at line L2 is positive exactly when the material angle along the edge is less than $\pi$, a convex edge. Line L3 merges two coplanar polygons that meet along an edge, so the nodes are the true faces even when the input splits them. Two faces with opposite normals along an edge bound a fin of zero thickness or a crack of zero width, and line L4 rejects them. Two faces may share several edges; the arc then carries the set of their labels, and line L6 keeps a node if any of its arcs has a 0.

The templates used here are depression features of a block milled from the top:

| template | faces | concave arcs |
|---|---|---|
| step | wall, floor | wall to floor |
| through slot | two walls, floor | each wall to floor |
| blind step | two walls, floor | all three pairs |
| through hole | four walls | each wall to the next, in a cycle |
| blind slot | three walls, floor | each wall to floor, and the end wall to each side wall |
| pocket | four walls, floor | each wall to floor, and each wall to the next, in a cycle |

## Example

Take the block $[0, 10] \times [0, 4] \times [0, 3]$ and cut from it a through slot $[3, 5] \times [0, 4] \times [2, 3]$, a step $[9, 10] \times [0, 4] \times [2, 3]$ and a pocket $[6, 8] \times [1, 3] \times [1, 3]$. The implementation builds the input from unit cubes, so every face comes as unit squares.

| step | lines | result |
|---|---|---|
| pair the edges | L1 | $182$ unit squares with $728$ directed edges, each matched with its reverse |
| merge | L2 to L4 | the flat edges merge the squares into $17$ faces; no knife edge |
| build $G$ | L5 | $42$ arcs: $31$ convex and $11$ concave |
| delete | L6 | the bottom, the left, right, front and back faces, and the two pieces of the top face, $x \in [0, 3]$ and $x \in [5, 9]$ with the pocket as a hole, have only convex arcs; $7$ nodes go, $10$ stay |
| components | L7 | $\{$slot wall $x = 3$, slot wall $x = 5$, slot floor$\}$, $\{$step wall $x = 9$, step floor$\}$, $\{$pocket floor, four pocket walls$\}$ |
| match | L8 to L10 | three faces with two concave arcs at the floor: through slot; two faces with one concave arc: step; five faces with a concave wheel: pocket |

Two checks of the signs. The top face $z = 3$ and the front face $y = 0$ meet along an edge from $(0, 0, 3)$ to $(3, 0, 3)$, as it runs in the top face, with $n_{top} = (0, 0, 1)$ and $n_{front} = (0, -1, 0)$ up to positive factors. Then $n_{top} \times n_{front} = (1, 0, 0)$, and its dot product with $q - p = (3, 0, 0)$ is $3 > 0$, convex. The slot floor $z = 2$ and the slot wall $x = 3$, whose normal $(1, 0, 0)$ points into the slot, meet along an edge that runs from $(3, 4, 2)$ to $(3, 0, 2)$ in the floor, so that the floor is on its left. Then $(0, 0, 1) \times (1, 0, 0) = (0, 1, 0)$, and the dot product with $(0, -4, 0)$ is $-4 < 0$, concave.

Now cut two crossing slots, $[2, 4] \times [0, 4] \times [2, 3]$ and $[0, 6] \times [1, 3] \times [2, 3]$, from the block $[0, 6] \times [0, 4] \times [0, 3]$. The common floor is one cross-shaped face, and each slot splits the walls of the other into two, so line L7 finds one component of nine faces: the floor with eight concave arcs to eight wall pieces, and four convex arcs between wall pieces that meet at the outer corners of the block. No template matches, and line L10 reports it. This is the weakness of the method that every later graph-based method tries to fix.

## Correctness

Newell's formula gives a positive multiple of the outward normal of each polygon, because the polygons run counterclockwise seen from outside. Along an edge from $p$ to $q$ in polygon $P$, the vector $n_P \times n_{P'}$ is parallel to $q - p$, since both normals are orthogonal to the edge, so the sign at line L2 is zero only when the faces are parallel; then they are coplanar or form a knife edge, and lines L3 and L4 sort the two cases. In a frame with the edge direction $u$, the direction $d = n_P \times u$ into face $P$, and $n_P$, write $n_{P'} = \alpha d + \beta n_P$. Then $(n_P \times n_{P'}) \cdot u = -\alpha$, and the edge is convex exactly when $\alpha < 0$, which is when face $P'$ bends down from face $P$ around the material. So $G$ is the attributed adjacency graph of the solid, line L6 and line L7 compute the components of Joshi and Chang, and MATCH, which tries every injective map that keeps all labels, finds an isomorphism exactly when one exists. The [full proof](proofs/correctness.md) gives the details.

What is proved is that the algorithm computes the graph, the components and the matches exactly as defined. That a component is the feature a machinist would name is not provable; it is a modeling choice, and the example of the crossing slots shows where it fails.

## Complexity

The costs are in the word RAM, with integer coordinates of bounded size. Pairing the $E$ directed edges by sorting takes $O(E \log E)$ time, or $O(E)$ expected time with a hash table, as in the implementation. The signs are $O(1)$ each, and the merges are $E$ operations of a union-find structure with path halving, $O(E \log E)$ in the worst case. Lines L5 to L7 take $O(E)$ time. MATCH only runs on a component with exactly as many faces as the template, and then tries at most $k!$ maps with $O(k^2)$ label checks each, so the matching takes $O(n t k! k^2)$ in the worst case. The template sizes are fixed and small, at most $5$ here, so in practice the cost is linear in the size of the B-rep. The extra space is $O(E)$ for the edge table and the graph.

## Properties

- **Exact.** With integer vertices every decision is the sign of an integer, and the graph is the true graph of the solid. No tolerance is used.
- **Independent of size and position.** The graph does not change when a feature is moved or scaled, as long as its faces keep their adjacency. A slot $1$ wide and a slot $100$ wide have the same graph.
- **Depressions only.** The deletion rule keeps faces with a concave edge. A boss on a face drags that face into its component, with convex arcs between the walls of the boss, and no depression template matches.
- **Components, not subgraphs.** A feature must be a whole component of $H$. Two features that touch along a concave edge form one component and are not recognized.

## Variants and improvements

- **Richer attributes.** Labeling arcs only convex or concave makes a V-groove and a step look the same, and a square through hole and a through hole with a rhombic cross section look the same. Later systems add the face type, the angle between the faces, the direction of the normal relative to the tool axis, and loops on a face.
- **Subgraph matching.** Instead of whole components, search for each template as a labeled induced subgraph of $H$, with [Ullmann's algorithm](/ullmann-algorithm/) or [VF2](/vf2-algorithm/), so that features inside a larger component are found.
- **Virtual links and hints.** For interacting features, add arcs for edges that the interaction removed, or start from traces of features and grow them, as in hint-based recognition.
- **Curved faces.** For cylinders and other curved faces, the convexity of an edge varies along it and needs the normals at a point of the edge, and a face may be tangent to its neighbor, where the sign is zero; these are labeled smooth and treated separately.
- **Meshes.** For scanned data, a [mesh segmentation](/mesh-segmentation/) gives the faces first, and the graph is built on the segments.

## When to use it

Use the attributed adjacency graph for prismatic parts with isolated 2.5D features, when the part has no feature history, for example after a neutral B-rep file was read. It is simple, exact and fast. When features interact heavily, or for freeform parts, use it as a first stage and pass the unrecognized components to a volumetric or hint-based method, as surveyed on the [feature recognition](/feature-recognition/) page. When the part was built with [feature-based modeling](/feature-based-modeling/), read the features from the history instead.

## Pitfalls

- **Signs near zero.** Line L2 is an [orientation test](/orientation-test/) of the two normals and the edge. With floating-point vertices, two almost coplanar faces give a tiny value with [catastrophic cancellation](/catastrophic-cancellation/), and the label can be wrong or an edge that should be merged can be kept. The fix is exact arithmetic on integer or rational vertices, as here, or a floating-point filter with an exact fall back.
- **Orientation.** If the polygons run clockwise seen from outside, every label flips, all faces have a concave arc, and the whole solid is one component. Check the orientation first, for example with the sign of the volume.
- **Split faces.** A B-rep from a mesher or a translator often splits a planar face into several pieces. Without the merge at line L3, a floor split in two gives a graph that matches no template.
- **Same graph, different shape.** The labels do not see angles, so a V-groove is reported as a step. A test of the implementation checks exactly this case.
- **Interactions.** Cut a slot $[1, 5] \times [0, 4] \times [2, 3]$ into the block $[0, 6] \times [0, 4] \times [0, 3]$ and drill a square hole $[2, 4] \times [1, 3] \times [0, 2]$ down from its floor. The hole walls meet the floor at convex edges, but both are kept, because each has a concave arc elsewhere, so the slot and the hole form one component of seven faces, which matches neither template. If the hole is flush with a slot wall, the two coplanar walls even merge into one face.

## Implementations

## History

Joshi and Chang published the attributed adjacency graph in 1988, as heuristics for the recognition of machined features from a 3D solid model. It was one of the first graph-based recognizers and the start of a large literature that added richer attributes, subgraph matching and ways to handle interacting features. The survey of Han, Pratt and Regli in 2000 counts graph-based methods as one of the three main families of feature recognition, with volumetric decomposition and hint-based methods, and names feature interactions as their main limit.

## References
