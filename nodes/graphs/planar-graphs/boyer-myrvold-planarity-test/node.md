---
tag: 1RE4H8
kind: algorithm
slug: boyer-myrvold-planarity-test
name: Boyer-Myrvold planarity test
aliases:
- Boyer-Myrvold algorithm
- edge addition planarity test
area: graphs/planar-graphs
level: advanced
summary: Simplified linear-time planarity test that also produces an embedding or a Kuratowski subgraph.
solves: [planarity-testing]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, needs_embedding: false, recursive: false, certifying: true}
history:
  year: 2004
  people: [John Boyer, Wendy Myrvold]
  note: Boyer and Myrvold gave the edge addition method in its final form in the Journal of Graph Algorithms and Applications in 2004; it adds the back edges of a depth-first search tree to a growing planar embedding, one vertex at a time in reverse order.
prereqs: [planar-graph, depth-first-search, biconnected-components, low-link, rotation-system, planar-edge-bound]
see_also: [planarity-testing, hopcroft-tarjan-planarity-test, lempel-even-cederbaum-st-numbering, kuratowski-theorem, planar-embedding, wagner-theorem, pq-tree, bucket-sort]
sources:
  - paper: doi:10.7155/jgaa.00091
    title: John M. Boyer and Wendy J. Myrvold, On the cutting edge, simplified O(n) planarity by edge addition, Journal of Graph Algorithms and Applications 8(3), 241 to 273 (2004)
    locator: the edge addition method, Walkup, Walkdown with its rule for choosing a direction, flips by a sign on the root edge, short-circuit edges, and the non-planarity minors A to E
  - paper: doi:10.1137/0201010
    title: Robert Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: depth-first search, low points and biconnected components
---

The Boyer-Myrvold test decides in linear time whether a graph is [planar](/planar-graph/), and it always returns a certificate: a planar embedding when the answer is yes, and a [Kuratowski subgraph](/kuratowski-theorem/) when the answer is no. It runs a [depth-first search](/depth-first-search/), starts from the search tree, which is trivially planar, and then adds the back edges one vertex at a time, in reverse search order. All the time it keeps a planar embedding of the edges added so far, split into [biconnected components](/biconnected-components/). Each new back edge goes into the *external face* of a component, and components are merged and flipped as needed. If a back edge cannot be added, the graph is not planar. **How the embedding is given:** the input has no embedding. It is the abstract graph by adjacency lists. The output is a [rotation system](/rotation-system/): for each vertex, the list of its neighbours in counterclockwise order around it. This is the combinatorial form of a [planar embedding](/planar-embedding/); coordinates are not computed.

## In plain words

Do a depth-first walk of the graph. It leaves a tree, which can always be drawn flat; every other edge goes up the tree. Now handle the vertices from the last one visited back to the first. At each vertex, try to draw all the edges that come up to it from below.

The drawing is kept in pieces. A new edge is always drawn on the outer rim of a piece, so it cannot cross anything. Pieces on its way are glued together and, if needed, turned over. The rule for choosing a way around a piece is careful: a vertex that still has an edge to a vertex higher up must stay on the outer rim, because that edge comes later. If an edge cannot be drawn on the rim, the graph is not planar, and the blocking vertices show a $K_5$ or $K_{3,3}$ inside it.

## The problem

Input: a simple undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, by adjacency lists. Output: a rotation system of a planar embedding of $G$ if $G$ is planar, and *nil* otherwise. A second function returns, for a non-planar graph, the edges of a subdivision of $K_5$ or $K_{3,3}$ in $G$.

**Search tree terms.** After the search, a vertex is its preorder number. A *back edge* $(v, w)$ joins a vertex $v$ and a descendant $w$ that is not its child. $\mathrm{least}(w)$ is the smallest ancestor of $w$ joined to $w$ by a back edge (or $w$ itself), and $\mathrm{low}(w)$ is the smallest value of $\mathrm{least}$ in the subtree of $w$; this is the [low point](/low-link/).

**Embedding terms.** During the run, the embedded graph $\tilde G$ is a set of biconnected components. A component is born as one tree edge $(p, c)$, where the end at $p$ is a *root copy* $r_c$ of $p$, a separate node that stands for $p$ inside this component only. Root copies are what make the components separate: a vertex $p$ with several children has one root copy per child. The *external face* of a component is its outer boundary. When vertex $v$ is processed:

- $w$ is *pertinent* if $w$ has a back edge to $v$ that is not embedded yet, or if a component whose root copy is a copy of $w$ contains a pertinent vertex.
- $w$ is *externally active* if $\mathrm{least}(w) < v$, or if $w$ has a child $c$ whose component is still separate and $\mathrm{low}(c) < v$. Such a $w$ has a path to an ancestor of $v$ that is still to be embedded.
- $w$ is *internally active* if it is pertinent and not externally active, and *inactive* if it is neither pertinent nor externally active.

## The algorithm

```pseudo id=main
BM-PLANAR(G)                               ▷ G simple, by adjacency lists; no embedding is given
L1  if n ≥ 3 and m > 3n − 6 then return nil
L2  DFS of G: preorder numbers, parent, least, low; bucket sort the children of each vertex by low
L3  for each tree edge (parent(c), c) do make the component with the edge between c and a new root copy r_c of parent(c)
L4  for v ← n − 1 down to 0 do
L5      for each back edge (v, w) with w a descendant do WALKUP(v, w)
L6      for each child c of v do WALKDOWN(v, r_c)
L7      if some back edge (v, w) is still not embedded then return nil
L8  for each root copy r_c that is left, join the component of r_c to parent(c)
L9  reverse the list of each vertex whose tree path has an odd number of flipped components
L10 return the lists as the rotation system

WALKUP(v, w)                                ▷ marks the components on the way from w up to v
L11 flag(w) ← v
L12 walk from w around the external face in both directions at once until a root copy r_c is found, or a node marked in this step
L13     if parent(c) ≠ v then add r_c to pertinentRoots(parent(c)): at the end if low(c) < v, else at the front; repeat from parent(c)

WALKDOWN(v, R)                              ▷ R = r_c for a child c of v
L14 for d ∈ {0, 1} do
L15     w ← the neighbour of R on side d of the external face; S ← an empty stack
L16     while w ≠ R and w is not a root copy do
L17         if flag(w) = v then pop and MERGE every entry of S; embed the edge (R, w) on side d; clear flag(w)
L18         if pertinentRoots(w) is not empty then
L19             r ← the first of pertinentRoots(w); x ← first active node from r on one side; y ← on the other side
L20             choose x if it is internally active, else y if it is, else x if it is pertinent, else y; push (w, r, side) on S; w ← the choice
L21         else if w is not externally active then w ← the next node on the external face
L22         else leave the loop                                               ▷ w is a stopping vertex
L23     if S is not empty then return

MERGE(w, r, side)                           ▷ joins the component of the root copy r to w
L24 if the walk enters the component of r against the orientation of w then flip it: reverse the list of r, sign(child of r) ← −1
L25 move the edges of r to w and splice the list of r into the list of w on the side of the walk; remove r from pertinentRoots(w)
```

A node is *active* in line L19 if it is pertinent or externally active; "first active node from $r$" walks along the external face from $r$ and passes over inactive nodes. Lines L17 to L22 look at the same $w$ in this order, so a vertex with a back edge to $v$ and also pertinent children first gets its edge and then sends the walk down. After the walk has gone down into a child component and embedded an edge there, the stack is empty again, and the walk goes on along the external face of the merged component. The walk returns to $w$ along the other side of that component if nothing on that side stops it.

**Why the order of the roots.** Line L13 puts the root copies of internally active components first and those of externally active components last. The walk handles all internally active components of $w$ first and comes back to $w$ each time. The one externally active component is handled last, because after it the walk does not come back: the stopping vertex inside it stays on the external face, and the vertices that the walk went past are closed in.

**Why the choice rule.** In line L20 the walk prefers a side whose first active node is internally active. Such a node can be closed in after its edges are added, so taking that side keeps every externally active node on the external face. If both sides start with an externally active node, the walk takes the side whose node is pertinent, and stops right after it.

**Lazy flips.** Line L24 reverses only the list of the root copy and puts a sign of $-1$ on the root edge of the component; the lists of the other vertices of the component are not touched. The true orientation of a vertex is the product of the signs on its tree path, and line L9 fixes all lists in one pass at the end. The walk itself reads lists in both directions, so it does not need to know the orientation, and lines L15, L19 and L21 track the side by which the walk entered each node.

## Example

**$K_{3,3}$.** Take $K_{3,3}$ with the search tree the path $0 - 1 - 2 - 3 - 4 - 5$ and the back edges $(0, 3)$, $(1, 4)$, $(0, 5)$ and $(2, 5)$. Then $\mathrm{least}(3) = \mathrm{least}(5) = 0$, $\mathrm{least}(4) = 1$, and $\mathrm{low}(c) = 0$ for every $c \ge 1$. At first there are five components, one per tree edge, $r_c - c$ for $c = 1, \ldots, 5$, where $r_c$ is a copy of $c - 1$.

| step | line | action |
|---|---|---|
| $v = 5, 4, 3$ | L6 | no back edges to these vertices; each walk stops at once, at the child, which is externally active |
| $v = 2$ | L11 | back edge $(2, 5)$: flag(5) = 2 |
| | L13 | from 5 the walk reaches $r_5$, a copy of 4: put $r_5$ at the end of pertinentRoots(4), since low(5) = 0 < 2; from 4 it reaches $r_4$: pertinentRoots(3) = ($r_4$); from 3 it reaches $r_3$, a copy of 2 = $v$: stop |
| | L18 to L20 | WALKDOWN(2, $r_3$), side 0: at 3, go down into $r_4$; the only active node is 4, pertinent: go to 4; at 4, go down into $r_5$ and go to 5 |
| | L17 | flag(5) = 2: merge $r_5$ into 4 and $r_4$ into 3, embed $(r_3, 5)$; the component is now the cycle $r_3 - 3 - 4 - 5 - r_3$ |
| | L22 | 5 is externally active (least 0): stop; side 1 stops at 3 |
| $v = 1$ | L13 | back edge $(1, 4)$: flag(4) = 1; from 4 the walk reaches $r_3$, a copy of 2: pertinentRoots(2) = ($r_3$) |
| | L19 | WALKDOWN(1, $r_2$), side 0: at 2, go down into $r_3$; the first active nodes are 3 on one side and 5 on the other |
| | L20 | 3 and 5 are both externally active and not pertinent: push and go to 5 |
| | L22, L23 | 5 is a stopping vertex and the stack is not empty: return |
| | L7 | the back edge $(1, 4)$ is not embedded: return nil |

The pertinent vertex 4 lies between the stopping vertices 3 and 5 on the external face of the component of $r_3$, and the root of that component is a copy of 2, not of $v = 1$. This is Minor A of the proof. It gives the $K_{3,3}$ with parts $\{2, 4, 0\}$ and $\{3, 5, 1\}$: 2 reaches 3 and 5 along the external face and 1 by the tree edge, 4 reaches 3 and 5 along the external face and 1 by its back edge, and 0 reaches 3 and 5 by back edges and 1 by the tree edge. Here this is all of $K_{3,3}$.

**$K_4$.** With the tree $0 - 1 - 2 - 3$ and back edges $(0, 2)$, $(1, 3)$ and $(0, 3)$: at $v = 1$ the walk goes down from 2 into $r_3$, merges it and embeds $(1, 3)$, then stops at 3 and at 2, which are both externally active. At $v = 0$ the edge $(0, 2)$ makes the component of $r_2$ internally active (low(2) = 0 is not below 0); the walk goes down from 1 into it, merges it, embeds $(0, 3)$ and then $(0, 2)$, and goes around back to $r_1$. The output with the vertices in this order is the rotation system $0: (2, 3, 1)$, $1: (0, 3, 2)$, $2: (1, 3, 0)$, $3: (2, 1, 0)$. Its face tracing gives 4 faces, and $4 - 6 + 4 = 2$, as the [Euler formula](/euler-formula/) requires.

**Small cases.** The empty graph returns an empty list and a single vertex returns one empty list. A tree has no back edges, so lines L4 to L7 do nothing and line L8 joins the tree edges into one rotation per vertex. $K_5$ has $10 > 9$ edges and is rejected by line L1; its Kuratowski subgraph is all 10 edges. $K_{3,3}$ is rejected as in the trace, and its Kuratowski subgraph is all 9 edges.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Soundness is proved in full: every operation keeps a planar embedding of each component, because a new edge joins two nodes on the external face and is drawn in that face, a merge glues two embeddings at one vertex, and a flip replaces an embedding by its mirror image. The key invariant is that after vertex $v$ is processed, every vertex with a path to an ancestor of $v$ that is not yet embedded is on the external face of its component. Completeness says that if line L7 fails, $G$ contains a subdivision of $K_5$ or $K_{3,3}$. The proof file builds this subgraph for the case where the walk is blocked inside a child component (Minor A), the case where the blocked pertinent vertex has a pertinent child component that is also externally active (Minor B), and one case of the x-y path (Minor C). For the other cases it follows the case analysis of Boyer and Myrvold and does not repeat it, so the completeness part is a sketch. The tests check the answer against a separate quadratic test on 1500 random graphs, check every returned rotation system by face tracing, and check every returned Kuratowski subgraph.

## Complexity

In the paper, every part is linear. The search, the low points and the bucket sort take $O(n)$ after line L1. WALKUP walks in both directions at once and stops at a node marked in the same step, so its cost is bounded by the number of nodes that become pertinent. Each merge and each embedded edge costs $O(1)$, and flips are $O(1)$ because only the root copy is changed. The remaining cost is the inactive vertices that the walk passes over in line L21. Boyer and Myrvold add a *short-circuit edge* from the root copy to each stopping vertex after the walk, so that the inactive vertices between them are never walked again; with this, the total is $O(n)$ time and $\Theta(n)$ extra space.

The implementation leaves out the short-circuit edges, because they are not needed for the answer and they must be removed from the final embedding. Without them, an inactive vertex can be passed over at each of up to $n$ steps, so the proved bound for the code is $O(n^2)$. On the test inputs, a triangulation with 30000 vertices, a cycle with 200000 vertices and a $150 \times 150$ grid, the running time grows linearly. The function that finds a Kuratowski subgraph removes edges one at a time while the graph stays non-planar, which takes $m$ runs of the test; the paper's isolator does it in linear time.

## Properties

- **Certifying.** The answer always comes with a certificate that can be checked in linear time: a rotation system whose face count satisfies the Euler formula, or a Kuratowski subgraph.
- **Iterative.** The search, WALKUP and WALKDOWN use loops and explicit stacks only, so a path or a cycle with $10^5$ vertices does not overflow the call stack.
- **Deterministic.** The search tree, and so the embedding that is returned, depends on the order of the adjacency lists. The answer does not.
- **No special structures.** The method needs only adjacency lists with two ends, a sign per tree edge and a few arrays. It needs no [PQ-tree](/pq-tree/), no [st-numbering](/st-numbering/) and no split into blocks before the run.

## Variants and improvements

- **Kuratowski subgraph isolator.** When line L7 fails, the paper finds the blocking configuration from the state of the walk, decides which of five minors A to E it is, and reads off a subdivision of $K_5$ or $K_{3,3}$ in linear time.
- **Short-circuit edges.** As above, these make the walk skip runs of inactive vertices, which is needed for the linear bound.
- **Outerplanarity.** With small changes, the same method tests whether a graph is [outerplanar](/outerplanar-graph/) and finds a $K_4$ or $K_{2,3}$ subdivision when it is not.
- **Other linear-time tests.** The [Hopcroft-Tarjan test](/hopcroft-tarjan-planarity-test/) uses path addition; the [Lempel-Even-Cederbaum](/lempel-even-cederbaum-st-numbering/) test with PQ-trees uses vertex addition; the left-right test of de Fraysseix and Rosenstiehl uses a 2-colouring of the back edges.

## When to use it

Use it when a planar embedding is needed after the test, for example to find the faces, to build the [dual graph](/planar-dual-graph/), or to draw the graph, and when a non-planar answer should be explained by a $K_5$ or $K_{3,3}$. It is the method used in the Boost Graph Library and in many other libraries. For only a yes or no answer on small graphs, a slower but simpler test is easier to write. When the graph comes from geometry and coordinates are already known, check for crossings with a sweep instead.

## Pitfalls

- **Root order.** If an externally active child component is handled before an internally active one, the walk leaves the parent and does not come back, and planar graphs are rejected.
- **The choice rule.** Going down on the wrong side of a child component can close in an externally active vertex. The edges from it come later, and they can no longer be embedded.
- **Orientation.** After lazy flips, the stored list of a vertex can be reversed relative to its true orientation. Code that reads the lists before line L9, or forgets a sign, returns a rotation system that is not planar. Check the output by face tracing.
- **Sides of degree-1 nodes.** A node with one edge in its component has both list ends on the same edge, so the side by which the walk leaves it must be kept from the side it came in on.
- **Removing merged roots.** A root copy that has been merged must leave the list of pertinent roots, and its child must count as no longer separate when external activity is computed; otherwise vertices stay active for ever.
- **Recursion and input.** The search must be iterative for long paths. Loops and parallel edges break the edge bound of line L1 and the list operations; reject them or remove them first.

## Implementations

## History

Boyer and Myrvold first described a planar embedding method without PQ-trees at the ACM-SIAM Symposium on Discrete Algorithms in 1999. Their journal paper of 2004 gave the edge addition form on this page, with the minors A to E for Kuratowski subgraphs. Their aim was a linear-time test that is simple enough to be written correctly from the description, after three decades in which the linear-time methods of Hopcroft and Tarjan (1974) and of Booth and Lueker (1976), with PQ-trees, were known to be hard to implement in full. The method was put into the Boost Graph Library, and Boyer published a reference implementation in C as the Edge Addition Planarity Suite.

## References
