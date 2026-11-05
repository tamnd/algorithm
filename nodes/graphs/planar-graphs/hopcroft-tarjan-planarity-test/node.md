---
tag: QDYX9D
kind: algorithm
slug: hopcroft-tarjan-planarity-test
name: Hopcroft-Tarjan planarity test
aliases:
- Hopcroft-Tarjan algorithm
- path addition planarity test
area: graphs/planar-graphs
level: advanced
summary: First linear-time planarity test; it splits a depth-first search tree into paths and checks with a stack of blocks that the pieces hanging off each path can be put on two sides.
solves: [planarity-testing]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, needs_embedding: false, recursive: true}
history:
  year: 1974
  people: [John Hopcroft, Robert Tarjan]
  note: Hopcroft and Tarjan gave the first linear-time planarity test in 1974, building on the path addition method of Auslander, Parter and Goldstein; Mehlhorn later gave the form with a stack of blocks used here.
prereqs: [planar-graph, depth-first-search, biconnected-components, low-link, planar-edge-bound]
see_also: [planarity-testing, boyer-myrvold-planarity-test, lempel-even-cederbaum-st-numbering, kuratowski-theorem, planar-embedding, jordan-curve-theorem, bucket-sort, bipartite-testing]
sources:
  - paper: doi:10.1145/321850.321852
    title: John Hopcroft and Robert Tarjan, Efficient planarity testing, Journal of the ACM 21(4), 549 to 568 (1974)
    locator: the palm tree, the arc ordering by low points, the path decomposition and the linear-time test
  - paper: doi:10.1137/0201010
    title: Robert Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: depth-first search, palm trees, low points and biconnected components
  - book: "Kurt Mehlhorn, Data Structures and Algorithms 2, Graph Algorithms and NP-Completeness, EATCS Monographs on Theoretical Computer Science, Springer, 1984"
    locator: the chapter on planar graphs, the planarity test by segments, strong planarity and the stack of blocks of attachments
  - paper: "Kurt Mehlhorn and Petra Mutzel, On the embedding phase of the Hopcroft and Tarjan planarity testing algorithm, Algorithmica 16(2), 233 to 242 (1996)"
    locator: the construction of an embedding from a successful run of the test
---

The Hopcroft-Tarjan test decides in linear time whether a graph is [planar](/planar-graph/). It was the first linear-time planarity test. It runs a [depth-first search](/depth-first-search/), splits each [biconnected component](/biconnected-components/) into paths of the search tree, and then checks, path by path, that the pieces that hang off a path can be split into two groups, one drawn on each side of the cycle that the path closes, so that no two pieces in a group get in each other's way. This page gives the decision version in the form of Mehlhorn: a recursive check of *segments* with a stack of *blocks* of attachment lists. **How the embedding is given:** it is not. The input is the abstract graph by adjacency lists, and the output is only yes or no; no rotation system and no coordinates are given or returned.

## In plain words

Walk through the graph depth first. The walk leaves a tree, and every other edge leads back up the tree. Follow one long path down the tree and back up by a returning edge: that closes a loop. Everything else hangs off this loop, like laundry on a line, and each hanging piece must go either inside or outside the loop.

Two pieces block each other if they would cross on the same side. So the question becomes: can the pieces be split into an inside group and an outside group with no blocking pair in either group? Each piece is checked in the same way first, from the deepest ones up. A stack keeps the groups of pieces that depend on each other, so that each new piece is compared with only a few earlier ones. If some piece blocks pieces on both sides, the graph is not planar.

## The problem

Input: a simple undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, by adjacency lists. Output: true if $G$ has a planar embedding, false otherwise. The test does not build an embedding; see the Variants section. A graph is planar exactly when all its [biconnected components](/biconnected-components/) are, so the algorithm tests each one.

**Palm tree.** Inside one biconnected component $B$, a depth-first search numbers the vertices $0, 1, \ldots$ in preorder; from now on a vertex is its number. Each edge becomes an *arc*: a tree arc $v \to c$ to a child, or a back arc $v \to w$ with $w < v$ to an ancestor. $\mathrm{lowpt}_1(v)$ is the smallest vertex reachable from $v$ by tree arcs and then at most one back arc ($v$ itself if nothing smaller), and $\mathrm{lowpt}_2(v)$ is the second smallest, or $v$. These are the [low points](/low-link/) of Tarjan's search.

**Segments.** For a tree arc $e = x \to y$, the *segment* $S(e)$ is the subtree of $y$ with $e$ and all back arcs out of the subtree. For a back arc $e = v \to w$, $S(e)$ is the arc itself. The *attachments* of $S(e)$ are the ends $w < y$ of its back arcs; they lie on the tree path above $y$. Following first arcs from $y$ (after the sort below) gives the *spine* $y = w_1 \to w_2 \to \cdots \to w_k$ and a back arc $w_k \to w_0$ with $w_0 = \mathrm{lowpt}_1(y)$. The *stem* of $e$ is the tree path from $w_0$ to $x$. $S(e)$ is *strongly planar* if $S(e)$ with its stem has a planar embedding with the whole stem on the boundary of the outer face. The component $B$ is planar exactly when the segment of the first tree arc $0 \to 1$ is strongly planar.

## The algorithm

```pseudo id=main
HT-PLANAR(G)                               ▷ G simple, by adjacency lists; no embedding is given or returned
L1  if n ≥ 3 and m > 3n − 6 then return false
L2  for each biconnected component B of G with at least 5 vertices do
L3      DFS of B from one vertex; rename the vertices 0, 1, ... in preorder; split edges into tree arcs and back arcs
L4      compute lowpt1(v) and lowpt2(v) for every vertex v
L5      bucket sort the arcs out of each v by cost: 2·lowpt1(c) + [lowpt2(c) < v] for a tree arc v → c, 2w for a back arc v → w
L6      if SEGMENT(0, 1) fails then return false
L7  return true

SEGMENT(x, y)                              ▷ tree arc x → y; returns the attachments below x, largest first, or fails
L8  follow first arcs y = w1 → w2 → ... → wk until the first arc wk → w0 is a back arc     ▷ the spine
L9  S ← an empty stack of blocks; a block is a pair (left list, right list) of attachments
L10 for w ← wk, wk−1, ..., w1 do
L11     for each arc w → t other than the first one, in sorted order do
L12         if t > w then A ← SEGMENT(w, t) else A ← (t)         ▷ a failure inside is a failure here
L13         ADD-BLOCK(S, A)
L14     delete the attachment parent(w) from the heads of all lists on S; pop blocks that become empty
L15 if a block on S has both list heads > w0 then fail
L16 return, for each block from the top of S down, its list with head > w0 (or its left list), all concatenated, then (w0) if w0 ≠ x

ADD-BLOCK(S, A)                            ▷ A is sorted, largest first
L17 B ← (A, empty list)
L18 while S is not empty do
L19     if head(left(top S)) > min(left B) then swap the two lists of top S              ▷ flip
L20     if head(left(top S)) > min(left B) then fail                                      ▷ conflicts on both sides
L21     if head(right(top S)) > min(left B) then T ← pop S; left B ← left B · left T; right B ← right B · right T
L22     else leave the loop
L23 push B on S
```

Lists are sorted with the largest vertex first, so the head of a list is its maximum and its last element its minimum; $\cdot$ is concatenation, which is $O(1)$ on linked lists with a tail pointer. Line L14 runs when the loop moves from $w$ to its parent on the spine (from $w_1$ the parent is $x$), so attachments that are not below the current vertex leave the lists. The first arc of $w_k$ is the back arc to $w_0$, and the first arc of every other spine vertex is the spine arc, so line L11 skips exactly the arcs of the spine cycle.

**What the stack means.** The pieces that hang off the spine cycle $C$ (the stem, the spine and the arc $w_k \to w_0$) are the segments $S(w \to t)$ of line L11. Two of them *conflict* if they cannot be drawn on the same side of $C$. ADD-BLOCK keeps the connected components of the conflict graph of the pieces seen so far as blocks, with the two colour classes of each component as its left and right lists. A new piece with lowest attachment $a$ conflicts with an earlier one exactly when the earlier one still has an attachment above $a$, which is what lines L19 to L21 compare. Line L20 finds an odd cycle in the conflict graph. Line L15 checks that the pieces with an attachment strictly inside the stem can all go on one side, so that the stem stays on the outer face.

**Why the sort.** The cost puts the arcs with the lowest attachment first. Among tree arcs with the same $\mathrm{lowpt}_1$, a segment whose attachments are only $\mathrm{lowpt}_1$ (cost even) comes before one that also attaches between $\mathrm{lowpt}_1$ and $v$ (cost odd). This order makes the comparison with the minimum of the new piece exact, and it keeps all attachments in lower blocks below all attachments in higher blocks.

## Example

**$K_{3,3}$.** Take $K_{3,3}$ with the depth-first numbering in which the tree is the path $0 - 1 - 2 - 3 - 4 - 5$ and the back arcs are $3 \to 0$, $4 \to 1$, $5 \to 0$ and $5 \to 2$ (the classes are $\{0, 2, 4\}$ and $\{1, 3, 5\}$). All $\mathrm{lowpt}_1$ values are 0, and $\mathrm{lowpt}_2(5) = 2$, $\mathrm{lowpt}_2(4) = \mathrm{lowpt}_2(3) = 1$. The sorted arc lists are $3: (0, 4)$, $4: (5, 1)$ and $5: (0, 2)$, since the tree arc $4 \to 5$ has cost $2 \cdot 0 + 1 = 1$ and the back arc $4 \to 1$ has cost 2.

| step | line | action | stack $S$ (left, right) |
|---|---|---|---|
| SEGMENT(0, 1) | L8 | spine $1 \to 2 \to 3$, first arc of 3 is $3 \to 0$: $w_0 = 0$ | empty |
| at $w = 3$ | L12 | tree arc $3 \to 4$: call SEGMENT(3, 4) | |
| SEGMENT(3, 4) | L8 | spine $4 \to 5$, first arc of 5 is $5 \to 0$: $w_0 = 0$ | empty |
| at $w = 5$ | L13 | back arc $5 \to 2$, $A = (2)$, push | $((2), ())$ |
| move to 4 | L14 | no head equals 4 | $((2), ())$ |
| at $w = 4$ | L19 | back arc $4 \to 1$, $A = (1)$: head 2 > 1, flip | $((), (2))$ |
| | L21 | right head 2 > 1: combine | $((1), (2))$ |
| move to 3 | L14 | no head equals 3; the spine is done | $((1), (2))$ |
| | L15 | both heads 1 and 2 are above $w_0 = 0$: fail | |

The segment of $3 \to 4$ has two pieces, the arcs $5 \to 2$ and $4 \to 1$, which cross if they are on the same side of the cycle $0 - 1 - 2 - 3 - 4 - 5 - 0$, and both attach strictly inside the stem $0 - 1 - 2 - 3$. One of them would have to be on the outer side, and then the stem is not on the outer face. So $K_{3,3}$ is not planar.

**Small cases.** The empty graph, a single vertex and a tree have no biconnected component with 5 or more vertices, so the answer is true. $K_4$ has one block of 4 vertices, which is planar, so the answer is true without a search. $K_5$ has $10 > 3 \cdot 5 - 6 = 9$ edges and is rejected by line L1. $K_{3,3}$ has $9 \le 12$ edges and fails as in the trace. The Petersen graph has $15 \le 24$ edges and fails inside the segment test. The wheel with 5 spokes passes: every segment there has the single attachment 0 below its stem, so no block ever has a head above $w_0$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Its main lemma is a decomposition: $S(x \to y)$ is strongly planar if and only if every piece hanging off its spine cycle is strongly planar, the conflict graph of the pieces is bipartite, and some 2-colouring puts all pieces with an attachment strictly between $w_0$ and $x$ on one side. The *only if* part uses the [Jordan curve theorem](/jordan-curve-theorem/): a piece lies on one side of the cycle, and two pieces on the same side that conflict would cross. The *if* part draws the pieces of each colour on one side, nested by their attachment intervals. A second lemma shows that the stack holds exactly the components of the conflict graph, with the invariant that every attachment in a block is at most every attachment in the blocks above it. Line L1 is safe by the [edge bound for planar graphs](/planar-edge-bound/), and line L2 because a graph is planar exactly when its blocks are.

## Complexity

Line L1 and the split into blocks take $O(n + m)$ time. After line L1, $m \le 3n - 6$, so every later bound in $m$ is also $O(n)$. The search, the low points and the bucket sort with $2n + 2$ buckets are linear in the size of each block. SEGMENT is called once per tree arc, and each arc is handled once on line L12. Each attachment enters a list once and leaves it once (on line L14, or as part of a returned list that is used once by the caller). Each loop round of ADD-BLOCK either pops a block, which was pushed once, or ends the loop. Concatenation is $O(1)$. The total is $O(n)$ time, after the $O(n + m)$ check of line L1, and $\Theta(n)$ extra space. The implementation replaces the recursion by an explicit stack of frames, so long paths do not overflow the call stack.

## Properties

- **Decision only.** The test answers yes or no. It does not return an embedding or a [Kuratowski subgraph](/kuratowski-theorem/) as a certificate.
- **Deterministic.** The DFS tree depends on the order of the adjacency lists, but the answer does not.
- **Arbitrary input order.** Any order of the adjacency lists works, because line L5 sorts the arcs again.

## Variants and improvements

- **Embedding phase.** Hopcroft and Tarjan also described how to build an embedding from a successful run. Mehlhorn and Mutzel (1996) pointed out gaps in this phase and gave a complete version: the side of each piece is fixed by the final flips of its block, and the pieces are put into the rotation system in the order of the sort.
- **Left-right planarity test.** De Fraysseix and Rosenstiehl described planarity by a 2-colouring of the edges of a DFS tree, with constraints between pairs of back edges. Brandes gave a short linear-time version that also builds an embedding. It is related to this test, with edges in place of segments.
- **Vertex addition.** The [Lempel-Even-Cederbaum](/lempel-even-cederbaum-st-numbering/) test adds vertices in an [st-numbering](/st-numbering/) order and keeps all possible embeddings in a [PQ-tree](/pq-tree/); Booth and Lueker made it linear in 1976.
- **Edge addition.** The [Boyer-Myrvold test](/boyer-myrvold-planarity-test/) adds back edges to a growing embedding in reverse DFS order. It returns an embedding or a Kuratowski subgraph and is the method used in most libraries today.

## When to use it

Use it when only the answer is needed and a short, self-contained linear-time test is welcome; the decision version fits in about 200 lines of Python. When an embedding or a certificate is needed, use the [Boyer-Myrvold test](/boyer-myrvold-planarity-test/) or the left-right test instead, since the embedding phase of this method is known to be hard to get right. For graphs with a few hundred vertices, the quadratic method of Demoucron, Malgrange and Pertuiset is simpler still.

## Pitfalls

- **The arc order.** Sorting by $\mathrm{lowpt}_1$ alone is not enough. Without the $+1$ for tree arcs whose $\mathrm{lowpt}_2$ is below $v$, the test rejects planar graphs, because a piece that touches only $\mathrm{lowpt}_1$ must come before one that touches more.
- **Removing attachments.** Attachments equal to the parent must be removed when the walk moves up, before the arcs of the parent are handled; otherwise a piece that touches only the current vertex looks like a conflict.
- **Biconnectivity.** The segment argument needs a biconnected graph, where every $\mathrm{lowpt}_1$ is below the parent. Running it on a graph with cut vertices gives wrong answers; split into blocks first.
- **Edge bound.** Line L1 is what makes the running time linear in $n$; without it the search alone costs $\Theta(m)$, which may be $\Theta(n^2)$.
- **Recursion depth.** Both the search and SEGMENT go as deep as the longest path, which is $n$ for a cycle. Use explicit stacks.
- **Multigraphs and loops.** Loops and parallel edges do not change planarity, but the edge bound and the segment test assume a simple graph. Remove them first, or reject them as the implementation does.

## Implementations

## History

The path addition method goes back to Auslander and Parter (1961) and Goldstein (1963): find a cycle, split the rest into pieces, and place the pieces recursively. Hopcroft and Tarjan made it run in $O(n \log n)$ time in 1971 and in linear time in their 1974 paper, using Tarjan's depth-first search and low points (1972) to choose the paths and to order the pieces. It was the first linear-time planarity test. Booth and Lueker gave a second linear-time test in 1976 with PQ-trees. Mehlhorn restated the Hopcroft-Tarjan test with segments and a stack of blocks in his 1984 textbook, which is the form on this page, and the algorithm became part of the LEDA library; Mehlhorn and Mutzel completed the embedding phase in 1996.

## References
