---
tag: RHWBG9
kind: data-structure
slug: liaison-graph
name: Liaison graph
aliases:
- contact graph of an assembly
- assembly connection graph
area: cad/mechanism-and-assembly-design
level: core
summary: An undirected graph with a node per part and an edge per contact or fastening, the input of most assembly sequence generators.
model: word-ram
complexity:
  vars:
    n: the number of parts
    m: the number of liaisons
    K: the number of pairs of parts whose closed x intervals meet
  time:
    worst: O(n log n + K)
  space:
    extra: Θ(n + m)
prereqs: [undirected-graph, induced-subgraph, connected-components]
see_also: [assembly-sequence-planning, and-or-graph-of-assembly-plans, de-fazio-whitney-precedence-method, non-directional-blocking-graph, assembly-constraint-solving, rectangle-intersection-sweep, adjacency-list, bitmask]
sources:
  - paper: "Alain Bourjault, Contribution à une approche méthodologique de l'assemblage automatisé: élaboration automatique des séquences opératoires, Thèse d'État, Université de Franche-Comté, Besançon, 1984"
    locator: the graph of liaisons of a product and the questions asked on its liaisons
  - paper: doi:10.1109/JRA.1987.1087132
    title: Thomas L. De Fazio and Daniel E. Whitney, Simplified generation of all mechanical assembly sequences, IEEE Journal of Robotics and Automation 3(6), 640 to 658 (1987)
    locator: the liaison diagram of a product and the numbering of its liaisons
  - paper: doi:10.1109/70.54734
    title: Luiz S. Homem de Mello and Arthur C. Sanderson, AND/OR graph representation of assembly plans, IEEE Transactions on Robotics and Automation 6(2), 188 to 199 (1990)
    locator: the relational model of an assembly and its graph of connections
  - book: "Daniel E. Whitney, Mechanical Assemblies: Their Design, Manufacture, and Role in Product Development, Oxford University Press, 2004"
    locator: the chapter on assembly sequence analysis (the liaison diagram)
---

The liaison graph of an assembly has one node for each part and one edge, called a liaison, for each pair of parts that touch or that a fastener joins. Each liaison can carry data: the kind of joint, the contact normal, the contact area. Assembly sequence methods use it in three ways: a liaison is the unit of work that a sequence orders, a set of parts counts as a subassembly only if it is connected in the graph, and the liaisons that cross a split are the joints that the split must make or break. This page builds the graph from a model of axis-aligned boxes and gives the operations that the [assembly planners](/assembly-sequence-planning/) call.

## In plain words

Draw a dot for each part of a product. When two parts touch, or a screw or a weld holds them together, draw a line between their dots. That picture is the liaison graph.

The picture answers simple questions fast. Which parts touch this part? Do these four parts hold together as one piece, or do they fall into two piles? If I lift these parts off the rest, which joints do I break? A planner asks these questions thousands of times, so it is worth building the picture once.

To build it from a CAD model, do not test every pair of parts. Sort the parts from left to right, and compare each part only with the earlier parts that reach far enough to the right to touch it. Parts far apart are never compared.

## The abstract type

An assembly is a set of parts $P = \{1, \ldots, n\}$. The liaison graph is an [undirected graph](/undirected-graph/) $L = (P, E)$ with a label on each edge. On this page a part is a closed axis-aligned box $b_i$, and the interiors of the boxes are pairwise disjoint. A *contact liaison* joins $i$ and $j$ when $b_i \cap b_j$ has positive area in a plane, that is, the two parts share a patch of a face. Its label is $(k, s, A)$: the contact normal from $i$ to $j$ is $s\,e_k$ with $s = \pm 1$ and $e_k$ a unit vector along the axis $k$, and $A$ is the area of the patch. Boxes that touch only along an edge or at a corner do not give a liaison. A *fastener liaison* is added by hand, because a bolt or a weld is not in the geometry of the two parts.

The graph has no motion model and no hand model of its own. It is the same for every planner. The planners add them: the [blocking graphs](/non-directional-blocking-graph/) add the motions, and the [AND/OR graph](/and-or-graph-of-assembly-plans/) adds the two-handed hand model.

The operations are:

- $\mathrm{BUILD}(b_1, \ldots, b_n)$: the graph of all contact liaisons.
- $\mathrm{ADD}(i, j, label)$: add a fastener liaison.
- $\mathrm{NEIGHBOURS}(i)$: the parts that share a liaison with $i$.
- $\mathrm{IS\text{-}CONNECTED}(S)$: true if the [induced subgraph](/induced-subgraph/) $L[S]$ is connected. Most planners accept a set $S$ as a subassembly only if this holds.
- $\mathrm{CUT}(S)$: the liaisons with one end in $S$ and one end outside, the joints made when $S$ is joined to the rest.
- $\mathrm{CONNECTED\text{-}SUBSETS}()$: every connected nonempty set of parts, each once. Their number $N$ bounds the size of the AND/OR graph of all plans.

## Representation

The code keeps, for each part $i$, a [bit mask](/bitmask/) $adj[i]$ of its neighbours, and a dictionary from the pair $(i, j)$ with $i < j$ to the label. A set of parts is a bit mask too, so the neighbourhood $N(S)$ of a set (the parts outside $S$ with a neighbour in $S$) is the union of $adj[i]$ over $i \in S$, without $S$. For a product of a few dozen parts, a mask fits in one or two machine words. For large products, [adjacency lists](/adjacency-list/) with a hash set of edges give the same operations, with a breadth first search for IS-CONNECTED.

## Operations

```pseudo id=main
BUILD(b[1..n])                          ▷ closed boxes with disjoint interiors
L1  order ← the parts sorted by lo_x; active ← empty list
L2  for each part i in order do
L3      remove from active every j with hi_x(b_j) < lo_x(b_i)
L4      for each j in active do c ← CONTACT(b_i, b_j)
L5          if c ≠ nil then add the liaison {i, j} with label c
L6      append i to active

CONTACT(a, b)                           ▷ w_m: overlap width of a and b on axis m
L7  for each axis k do
L8      if hi_k(a) = lo_k(b) then s ← +1 else if hi_k(b) = lo_k(a) then s ← -1 else skip k
L9      if w_m > 0 for both other axes m then return (k, s, the product of the two w_m)
L10 return nil

IS-CONNECTED(S)                         ▷ S: a bit mask of parts
L11 R ← {the lowest part of S}; repeat R' ← R; R ← R ∪ (N(R) ∩ S) until R = R'
L12 return R = S

CUT(S)
L13 return the liaisons {i, j} with i in S and j not in S

GROW(S, B)                              ▷ S connected, B: banned parts
L14 output S
L15 C ← N(S) \ B
L16 for each w in C, in increasing order do
L17     GROW(S ∪ {w}, B); B ← B ∪ {w}

CONNECTED-SUBSETS()
L18 B ← ∅
L19 for each part v in increasing order do
L20     GROW({v}, B); B ← B ∪ {v}
```

**Build.** This is the sort step of a [sweep](/sweep-line-technique/) along $x$, as in the [rectangle intersection sweep](/rectangle-intersection-sweep/). Two parts in contact have closed $x$ intervals that meet. So when part $i$ comes, the only earlier parts that can touch it are the ones whose interval has not ended before $lo_x(b_i)$. Line L3 drops the others, and they can never come back, because later parts start even further right. Each pair that survives gets the exact test CONTACT. With integer or rational coordinates, the test is exact.

**Contact.** Disjoint interiors force at least one axis with overlap width at most 0. The patch has positive area exactly when one axis has width 0, where one box ends and the other starts, and the two other widths are positive.

**Connected subsets.** GROW never lists a set twice: the first branch that takes candidate $w$ covers every larger set that contains $w$, so the later branches ban $w$. A set is listed by the call for its lowest part.

## Example

Take a frame of five boxes, with corners $(x_0, y_0, z_0)$ and $(x_1, y_1, z_1)$:

| part | name | corners |
|---|---|---|
| 0 | base plate | $(0, 0, 0)$, $(4, 2, 1)$ |
| 1 | left post | $(0, 0, 1)$, $(1, 2, 3)$ |
| 2 | right post | $(3, 0, 1)$, $(4, 2, 3)$ |
| 3 | block | $(1, 0, 1)$, $(3, 2, 2)$ |
| 4 | top plate | $(0, 0, 3)$, $(4, 2, 4)$ |

The posts and the block stand on the base plate. The block sits between the posts, and the top plate rests on the posts, with an empty gap of height 1 above the block.

BUILD sorts by $lo_x$ and gets the order $0, 1, 4, 3, 2$. Part 0 finds an empty list. Part 1 is compared with 0. Part 4 is compared with 0 and 1. Part 3 is compared with 0, 1 and 4. When part 2 comes, with $lo_x = 3$, line L3 drops part 1, whose interval ends at $x = 1$, and part 2 is compared with 0, 4 and 3. That is 9 calls of CONTACT, out of the 10 pairs. The pair $\{1, 2\}$ is never tested. Seven calls find a contact:

| liaison | axis | sign | area |
|---|---|---|---|
| $\{0, 1\}$ | $z$ | $+1$ | 2 |
| $\{0, 2\}$ | $z$ | $+1$ | 2 |
| $\{0, 3\}$ | $z$ | $+1$ | 4 |
| $\{1, 3\}$ | $x$ | $+1$ | 2 |
| $\{2, 3\}$ | $x$ | $-1$ | 2 |
| $\{1, 4\}$ | $z$ | $+1$ | 2 |
| $\{2, 4\}$ | $z$ | $+1$ | 2 |

For $\{2, 3\}$ the normal from part 2 to part 3 points along $-x$, because the block lies to the left of the right post. The pairs $\{0, 4\}$ and $\{3, 4\}$ do not touch: the top plate is 2 above the base and 1 above the block.

CUT($\{3\}$) gives $\{0, 3\}$, $\{1, 3\}$ and $\{2, 3\}$: inserting the block makes three joints at once. IS-CONNECTED is false for the three pairs without a liaison, $\{1, 2\}$, $\{0, 4\}$ and $\{3, 4\}$, and true for every set of four parts, because no single part holds the frame together. CONNECTED-SUBSETS lists $N = 27$ sets: 5 single parts, 7 pairs, 9 triples, 5 sets of four and the whole frame. Of the $2^5 - 1 = 31$ nonempty sets, only the three pairs above and the triple $\{0, 3, 4\}$ are not connected.

## Correctness

CONTACT is correct because the intersection of two boxes is a box whose sides are the three overlap widths, so it is a planar patch of positive area exactly when one width is 0 and the two others are positive. The sweep tests every pair in contact: such a pair has meeting $x$ intervals, and since the parts come in order of $lo_x$, the earlier part is still in the active list when the later one comes. IS-CONNECTED grows the component of one part inside $S$. GROW outputs each connected set that contains its first argument and avoids the banned set exactly once, by induction on the number of free parts: a larger set is produced only in the branch of the first candidate it contains. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst-case time |
|---|---|
| BUILD | $O(n \log n + K)$, $K$ the pairs of parts whose closed $x$ intervals meet |
| ADD | $O(1)$ expected (dictionary) |
| NEIGHBOURS($i$) | $O(n / w)$ word operations to scan the mask, $O(\deg i)$ with lists |
| IS-CONNECTED($S$) | $O(|S|^2)$ word operations with masks, $O(n + m)$ with lists |
| CUT($S$) | $O(m)$ |
| CONNECTED-SUBSETS | $O(N n)$ word operations, $N$ the number of connected sets |

Here $w$ is the word length, and the mask bounds assume $n \le w$. Space is $\Theta(n + m)$. The sweep does $K$ calls of CONTACT, and $K \ge m$. Both can be $\Theta(n^2)$: lay $n/2$ long bars along $x$ side by side, and $n/2$ long bars along $y$ on top of them, and every bar of the lower layer touches every bar of the upper layer, so $m = n^2/4$. With an [interval tree](/interval-tree/) on the $y$ intervals of the active parts, the sweep can skip pairs whose $y$ intervals do not meet, but it still pays for each liaison it reports.

$N$ can be small or large. A chain of $n$ parts has $n(n+1)/2$ connected sets, a star with one central part has $2^{n-1} + n - 1$, and a product where every part touches every other has $2^n - 1$. The frame above has 27 of 31.

## Variants

- **Contact types.** Real liaison graphs label each liaison with its kind: plane contact, cylindrical fit, thread, snap fit, weld, glue. A cylindrical fit allows motion only along its axis, and the planners turn this into motion constraints.
- **Contact normals for planning.** The normals on the labels are the raw data of the infinitesimal [blocking graph](/non-directional-blocking-graph/): a part with a plane contact of normal $n$ against another part cannot move along any direction $d$ with $d \cdot n > 0$.
- **Liaison diagram with numbered liaisons.** The question methods of [Bourjault and of De Fazio and Whitney](/de-fazio-whitney-precedence-method/) number the liaisons $1, \ldots, m$ and describe a state of the assembly by the set of liaisons made. A state is then a set of edges, not a set of parts.
- **Graph of connections.** Homem de Mello and Sanderson describe an assembly by a relational model and its graph of connections, which is the same graph with contacts and attachments as two kinds of edge.
- **Polyhedral parts.** For general solids the contact test is a face to face test on the boundary representations, with a tolerance. The sweep stays the same, with bounding boxes in place of the parts.

## When to use it

Use the liaison graph as the first structure of any assembly planner. It decides which subsets are physical subassemblies, it is the vocabulary of the question methods, and its connected sets index the nodes of the AND/OR graph. It is also the base of design reviews that count joints, such as [design for assembly](/design-for-assembly/). It is not a model of motion: two parts can be free of contact and still block each other, as the top plate blocks the block in the example. For motion, build the blocking graphs.

## Pitfalls

- **Contact is not blocking.** The top plate and the block do not touch, yet the plate stops the block from moving up. A planner that uses only liaisons to test motions accepts wrong sequences.
- **Edge contacts.** Two boxes that share only an edge have no liaison here, but under an infinitesimal motion along a diagonal they still collide. The blocking tests must use the geometry, not the liaison list.
- **Tolerances.** Real CAD faces that should touch often have a gap or an overlap of $10^{-6}$. With floating point coordinates, a contact test needs a tolerance and a rule for what it means. The code here uses exact coordinates, so the question does not come up.
- **Fasteners are not in the geometry.** When the CAD model leaves out a bolt, a rivet or a weld, nothing in the geometry joins the parts it holds. Add such liaisons by hand.
- **Parts versus liaisons.** A state can be a set of parts or a set of liaisons. When all liaisons inside a set of parts must be made together (the usual monotone model), the two are the same thing for a connected set of two or more parts. When a part can be placed with one liaison made and another left open, they differ.
- **Exponential lists.** CONNECTED-SUBSETS is output sensitive, not polynomial. A product with one central part, such as a base plate that holds all others, has more than $2^{n-1}$ connected sets.

## Implementations

The Python module builds the graph of a list of boxes with integer or Fraction corners by the sweep, keeps neighbours as bit masks, and gives NEIGHBOURS, CUT, IS-CONNECTED and CONNECTED-SUBSETS by the GROW scheme. A shared helper holds the box predicates and a generator of random assemblies. The tests compare the sweep with the pairwise test on every pair for random assemblies of up to 30 boxes, compare each contact area and normal with a count of unit faces on a voxel grid, compare the connected sets and IS-CONNECTED with a check of all $2^n$ subsets for up to 9 parts, and check the counts for chains, stars and complete graphs.

## History

Bourjault introduced the graph of liaisons in his 1984 thesis at Besançon as the base of an automatic method for generating assembly sequences: the method asks the engineer questions about the liaisons. De Fazio and Whitney (1987) kept the liaison diagram and cut down the number of questions. Homem de Mello and Sanderson (1986 and 1990) built their AND/OR graph of plans on a relational model whose graph of connections is the same object. Whitney's book (2004) uses the liaison diagram as the start of assembly sequence analysis.

## References
