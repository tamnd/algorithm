---
tag: T77RVB
kind: algorithm
slug: chazelle-mst
name: Chazelle's minimum spanning tree algorithm
aliases:
- soft heap MST
area: graphs/spanning-trees
level: research
summary: Deterministic O(m α(m,n)) MST algorithm built on soft heaps.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, "α(m, n)": the inverse Ackermann function}
  time: {worst: "O(m α(m, n))"}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: true}
prereqs: [minimum-spanning-tree, soft-heap, prim, boruvka, cut-property, cycle-property, inverse-ackermann-function, kruskal]
see_also: [pettie-ramachandran-mst, karger-klein-tarjan-mst, fredman-tarjan-mst, generic-mst-method, mst-verification, cycle-contraction, ackermann-function, decision-tree-complexity]
sources:
  - paper: doi:10.1145/355541.355562
    title: "Bernard Chazelle, A minimum spanning tree algorithm with inverse-Ackermann type complexity, Journal of the ACM 47(6) (2000), 1028-1047"
    locator: the whole paper (contractible subgraphs, the bad edges, the recursion msf(G, t), and the O(m α(m, n)) analysis)
  - paper: doi:10.1145/355541.355554
    title: "Bernard Chazelle, The soft heap: an approximate priority queue with optimal error rate, Journal of the ACM 47(6) (2000), 1012-1027"
    locator: the whole paper (the soft heap and its error bound)
  - paper: doi:10.1137/120880185
    title: "Haim Kaplan, Robert E. Tarjan and Uri Zwick, Soft heaps simplified, SIAM Journal on Computing 42(4) (2013), 1660-1673"
    locator: the whole paper (the binary-tree soft heap that the implementation follows)
  - paper: doi:10.1145/505241.505243
    title: "Seth Pettie and Vijaya Ramachandran, An optimal minimum spanning tree algorithm, Journal of the ACM 49(1) (2002), 16-34"
    locator: the sections on DJP-contractible subgraphs and the lemma that reduces the MSF of G to the MSFs of the pieces, the contracted graph and the corrupted edges
---

Chazelle's algorithm computes a [minimum spanning tree](/minimum-spanning-tree/) deterministically in $O(m \, \alpha(m, n))$ time, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). Published in 2000, it is the fastest known deterministic algorithm with a proven explicit bound. It grows pieces of the graph by [Prim's rule](/prim/), but it keeps the candidate edges in a [soft heap](/soft-heap/), a priority queue that may raise (*corrupt*) some keys in exchange for speed. The pieces are then correct for the corrupted weights, not the true ones. Chazelle's key lemma repairs this. The true minimum spanning tree uses only edges of three kinds: edges in the trees of the pieces, edges in the tree of the graph in which each piece is contracted to a vertex and the corrupted edges are removed, and the corrupted edges themselves. Recursion on these smaller problems, with piece sizes taken from the Ackermann function, gives the bound. The implementation on this page keeps the soft heaps, the pieces and the lemma, but not the tuned hierarchy, so it is correct but not fast.

## In plain words

Prim's way of building a cheapest network grows one region at a time and always adds the cheapest road that leaves the region. Keeping the leaving roads in order is the slow part, so Chazelle uses a sloppy sorter. The sloppy sorter is fast, but now and then it pretends that a road costs more than it does. A road it has lied about is called corrupted.

The regions grown with the sloppy sorter are still correct for the made-up prices. The trick: remember every corrupted road. Then the cheapest network is found among three short lists: the roads chosen inside each region, the roads chosen between regions once each region is shrunk to a point and the corrupted roads are put aside, and the corrupted roads themselves. Each list is much smaller than the whole map, because the sorter lies about only a small share of the roads.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and a real weight $w(e)$ on each edge. Weights may tie. The algorithm compares the keys $(w(e), i)$, where $i$ is the index of the edge, so all keys are distinct and the answer is the unique forest that [Kruskal's algorithm](/kruskal/) gives under that order. The graph need not be connected, and then the output is a minimum spanning forest. Parallel edges are allowed, and self-loops are dropped at the start.

## The algorithm

**Chazelle's algorithm, in outline.** The procedure msf$(G, t)$ has a parameter $t$ that controls the target sizes of the pieces.

1. If $t = 1$ or the graph is small, solve directly. Otherwise run a constant number $c$ of [Borůvka](/boruvka/) phases, which shrink $n$ by a factor of $2^c$, and contract.
2. Build a hierarchy of pieces with a soft heap of error rate about $1/c$. A piece at height $z$ of the hierarchy has a target size given by an Ackermann-type function of $t$ and $z$. The pieces are grown in depth-first order along an *active path*, each by Prim's rule on current keys.
3. Every edge whose key was corrupted when it left a piece is *bad*. Bad edges are set aside.
4. For each piece $C$, recursively compute msf$(C \setminus \text{bad}, t - 1)$.
5. Recursively compute the MSF of the union of those forests and the bad edges, and add the Borůvka edges.

With $t$ chosen as the least value for which $n$ is below a cube of the Ackermann-type size function at density $m/n$, the total time is $O(m \, \alpha(m, n))$ (Chazelle, 2000). The details of the hierarchy, the order of growth and the accounting fill most of the paper.

**The simplified version on this page.** It uses the same two tools in one flat level per recursion. The parameters are a piece size $s \ge 2$, a soft heap threshold $t$, and a base size.

```pseudo id=main
SOFT-HEAP-MSF(G)
L1  if G has at most base edges then return KRUSKAL(G)
L2  mark every vertex free; B ← ∅                        ▷ B collects the bad (corrupted) edges
L3  for each free vertex r: make r a new piece C, and a new soft heap H holding the edges at r
L4      while H is not empty and |C| < s do
L5          (e, ckey) ← DELETE-MIN(H); if ckey > key(e) then B ← B ∪ {e}
L6          let y be the far end of e; if y ∈ C then continue; if y is in an earlier piece C' then merge C into C' unless e ∈ B, and leave the loop
L7          add y to C; insert into H each edge (y, z) with z ∉ C
L8      add to B each edge left in H whose current key is larger than its key
L9  F ← the union over the pieces P of KRUSKAL(G[P])
L10 F' ← SOFT-HEAP-MSF((G − B) / pieces)                  ▷ each piece contracted to one vertex
L11 K ← F ∪ F' ∪ B
L12 return KRUSKAL(K)
```

Lines L3 to L7 are Prim's algorithm on the current keys of the soft heap. A piece stops at $s$ vertices, or when its heap is empty, or when it reaches an earlier piece. In the last case it joins that piece, unless the joining edge is bad. Lines L9 to L12 are Chazelle's filter.

## Example

The graph has the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$. Its minimum spanning tree is $\{bc, bd, ef, ac, ce\}$, of weight 13. Run the algorithm with $s = 3$, base 0, and threshold $t = 0$, which corrupts many keys.

| step | piece | event | bad edges so far |
|---|---|---|---|
| 1 | from $a$ | the heap holds $ab = 4$, $ac = 3$; it returns $ab$ with current key 4, because $ac$ was moved into a node with key 4 | none |
| 2 | $\{a, b\}$ | insert $bc$, $bd$; the heap returns $ac$ with current key $4 > 3$ | $ac$ |
| 3 | $\{a, b, c\}$ | full; the edges left are $bc$ (1, current 4), $bd$ (2, current 4), $cd$ (4, current 5), $ce$ (5, current 5) | $ac, bc, bd, cd$ |
| 4 | from $d$ | the heap returns $de = 7$, so $e$ joins; then $ce = 5$ reaches the earlier piece, $ce$ is not bad, so $\{d, e\}$ joins $\{a, b, c\}$ | $ac, bc, bd, cd$ |
| 5 | | the edges left are $ef$ (2, current 5), $bd$, $cd$, $df$ (6, current 7) | $ac, bc, bd, cd, ef, df$ |
| 6 | from $f$ | the heap returns $df$, which reaches an earlier piece, but $df$ is bad, so $\{f\}$ stays alone | the same six |

The two pieces are $\{a, b, c, d, e\}$ and $\{f\}$. The tree grown by Prim's rule in the first piece is $\{ab, ac, de, ce\}$. It is not part of the true minimum spanning tree: the corrupted key of $ac$ made the heap pick $ab$. The filter does not use that tree.

- Line L9: Kruskal's algorithm inside the first piece gives $F = \{bc, bd, ac, ce\}$.
- Line L10: the only edges between the two pieces are $df$ and $ef$, and both are bad, so the contracted graph has no edges and $F' = \emptyset$.
- Line L11: $K = F \cup B = \{ac, bc, bd, cd, ce, ef, df\}$, which has seven of the nine edges.
- Line L12: Kruskal's algorithm on $K$ returns $\{bc, bd, ef, ac, ce\}$, the minimum spanning tree.

With $t = 2$ the heaps here are too small to corrupt anything. Then all six vertices end in one piece, and line L9 alone finds the tree.

## Correctness

**Theorem.** For every finite undirected graph with real weights, SOFT-HEAP-MSF terminates and returns the minimum spanning forest under the keys $(w(e), i)$.

The proof has three steps. Let $w'(e)$ be the largest current key that $e$ has when it leaves a heap (or when the heap is discarded), and $w'(e) = \mathrm{key}(e)$ if $e$ was never in a heap.

1. **The soft heap contract.** A current key is never below the item's key and never decreases, and DELETE-MIN returns an item with the smallest current key.
2. **The pieces are contractible for $w'$.** Each edge added at line L7, and each joining edge at line L6, is a light edge, for $w'$, of the cut around the piece being grown. By the [cut property](/cut-property/), as in the [generic method](/generic-mst-method/), some minimum spanning forest $T'$ for $w'$ contains all these edges. So $T'$ contains a spanning tree of each final piece. Every edge with $w'(e) \ne \mathrm{key}(e)$ is in $B$.
3. **The filter lemma.** Let $e$ be an edge of the true minimum spanning forest that is not in $B$.
   - If $e$ lies inside a piece, the [cycle property](/cycle-property/) puts it in that piece's forest.
   - If $e$ lies between pieces and is not in the forest of the contracted graph, then it closes a cycle of lighter edges there. Each piece on that cycle can be crossed by a path of $T'$. Every edge on such a path is lighter than $e$, because the cycle must cross that edge's fundamental cut of $T'$ again, at an edge whose $w'$ equals its key. This gives a cycle in $G$ on which $e$ is the heaviest edge, a contradiction.

   So the true forest lies inside $K$, and Kruskal's algorithm on $K$ returns it.

The recursion terminates because the first edge taken from the first non-empty heap never reaches the contracted graph, so line L10 recurses on fewer edges. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM, and the algorithm only compares keys.

**Chazelle's algorithm.** $O(m \, \alpha(m, n))$ time in the worst case and $O(m)$ space. The bound comes from three parts. The soft heaps have error rate $1/c$ and cost $O(\log c)$ amortized per operation. The number of bad edges is at most a $1/c$ fraction of the insertions. The target sizes, which grow like the Ackermann function, make the recursion depth $t = O(\alpha(m, n))$, while the total size of the subproblems at each depth stays $O(m)$. Pettie and Ramachandran later gave an algorithm whose time is, up to a constant factor, the [decision-tree complexity](/decision-tree-complexity/) of the problem. That complexity lies between $\Omega(m)$ and $O(m \, \alpha(m, n))$, and its exact value is unknown.

**The implementation on this page.** One level costs $O(m \log m)$. The soft heap operations cost $O(\log m)$ each, because the minimum root is found by a scan over the ranks. Kruskal's algorithm runs at line L9 and at line L12. Each level removes at least one edge, so there are at most $m$ levels, and the honest worst-case bound is $O(m^2 \log m)$. In practice the number of levels is small. On a random graph with 2000 vertices and 9991 edges (no loops), with $s = 8$ and base 8, the runs took 2, 6, 7 and 4 levels for the thresholds $t = 0, 2, 4, 8$. The bad edges at the top level were 8442, 4728, 519 and 0. A small threshold makes many edges bad, so the filter keeps most of the graph. A large threshold makes the heaps exact.

| claim | bound | case |
|---|---|---|
| time, Chazelle | $O(m \, \alpha(m, n))$ | worst |
| space, Chazelle | $O(m)$ | worst |
| time, one level of the implementation | $O(m \log m)$ | worst |
| time, the implementation | $O(m^2 \log m)$ | worst |

## Properties

- **Deterministic.** There are no random choices, unlike the [Karger-Klein-Tarjan algorithm](/karger-klein-tarjan-mst/).
- **Comparison-based.** Only comparisons of keys are used. The bound holds in the pointer machine model, without bit tricks.
- **Recursive.** The recursion goes both into the pieces and into a smaller graph made of their forests and the bad edges.
- **Errors by design.** The heaps make mistakes on purpose, and the algorithm tolerates them by remembering every mistake.

## Variants and improvements

- **Chazelle 1997.** An earlier version ran in $O(m \, \alpha(m, n) \log \alpha(m, n))$ time.
- **Pettie and Ramachandran (2002).** The [optimal algorithm](/pettie-ramachandran-mst/) uses the same contractible pieces and the same filter lemma, with very small pieces whose MSF is found by precomputed optimal decision trees. Its time is optimal, but no explicit bound better than $O(m \, \alpha(m, n))$ is known for it.
- **Randomized linear time.** The [Karger-Klein-Tarjan algorithm](/karger-klein-tarjan-mst/) reaches expected $O(m)$ time by random sampling and [MST verification](/mst-verification/).
- **Simpler bounds.** The [Fredman-Tarjan algorithm](/fredman-tarjan-mst/), with $O(m \beta(m, n))$ time, and the algorithm of Gabow, Galil, Spencer and Tarjan, with $O(m \log \beta(m, n))$, came before and use Fibonacci heaps instead of soft heaps.

## When to use it

Chazelle's algorithm is a theoretical result. Its constants and its complexity make it slower in practice than [Kruskal](/kruskal/), [Prim](/prim/) with a binary heap, or [Borůvka](/boruvka/) on every graph of realistic size. Study it to see how soft heaps and contractible pieces give a near-linear deterministic bound. Use the simple algorithms for real work.

## Pitfalls

- **Forgetting a bad edge.** Every edge whose current key ever exceeded its key must go to $B$, both the edges returned by DELETE-MIN (line L5) and the edges still in the heap when it is discarded (line L8). Dropping the second group loses tree edges. Corrupted edges inside a piece may also go to $B$; that is harmless.
- **Joining along a bad edge.** If a piece joins an earlier piece along a corrupted edge, the joining edge may not be light for $w'$, because its key in the earlier heap can be higher. Line L6 refuses to join along a bad edge.
- **Using the Prim tree of a piece.** The tree grown inside a piece is optimal only for the corrupted keys. Line L9 recomputes each piece's forest from the true keys. The example shows the two can differ.
- **Ties.** The keys must be compared as $(w, i)$, both in the heaps and in Kruskal's algorithm. Otherwise the uniqueness used in the proof fails, and with ties the result could differ from the reference forest. The tests with equal weights catch this.
- **Disconnected graphs.** A piece never crosses components, so the result is a spanning forest. Never wait for $n - 1$ edges.

## Implementations

## History

Chazelle announced an $O(m \, \alpha(m, n) \log \alpha(m, n))$ algorithm in 1997, and the soft heap and the $O(m \, \alpha(m, n))$ algorithm in the same issue of the Journal of the ACM in 2000. Pettie and Ramachandran (2002) built on his structure to get a provably optimal algorithm with an unknown running time. Kaplan, Tarjan and Zwick (2013) simplified the soft heap. Whether the minimum spanning tree can be found deterministically in $O(m)$ time is still open.

## References
