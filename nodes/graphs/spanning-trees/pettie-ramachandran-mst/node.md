---
tag: BJQNXT
kind: algorithm
slug: pettie-ramachandran-mst
name: Pettie-Ramachandran optimal MST algorithm
aliases:
- optimal minimum spanning tree algorithm
area: graphs/spanning-trees
level: research
summary: Algorithm whose comparison count is optimal among decision-tree algorithms; running time is unknown.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: "O(m α(m, n))", best: "Ω(n + m)"}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: true}
history:
  year: 2002
  people: [Seth Pettie, Vijaya Ramachandran]
  note: Pettie and Ramachandran presented the algorithm at ICALP 2000 and published the journal version in 2002.
prereqs: [chazelle-mst, soft-heap, decision-tree, boruvka, graph-contraction]
see_also: [chazelle-mst, karger-klein-tarjan-mst, fredman-tarjan-mst, yao-mst, mst-verification, mst-lower-bound, inverse-ackermann-function, comparison-model]
sources:
  - paper: doi:10.1145/505241.505243
    title: Seth Pettie and Vijaya Ramachandran, An optimal minimum spanning tree algorithm, Journal of the ACM 49(1) (2002), 16-34
    locator: the whole paper (the partition with a soft heap, the decision trees for small graphs, the recursion, and the proof that the time is O(T*(m, n)))
  - paper: doi:10.1145/355541.355562
    title: Bernard Chazelle, A minimum spanning tree algorithm with inverse-Ackermann type complexity, Journal of the ACM 47(6) (2000), 1028-1047
    locator: the whole paper (contractible subgraphs, corrupted edges, and the O(m α(m, n)) bound that also bounds T*)
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert Endre Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3) (1987), 596-615
    locator: the section on minimum spanning trees (the method that is linear on dense graphs)
---

The Pettie-Ramachandran algorithm finds a [minimum spanning tree](/minimum-spanning-tree/) using, up to a constant factor, the least possible number of edge-weight comparisons. Its running time is $O(T^\ast(m, n))$, where $T^\ast(m, n)$ is the depth of an optimal comparison decision tree for the MST problem on graphs with $n$ vertices and $m$ edges. Nobody knows what $T^\ast$ is: it lies between $\Omega(m)$ and the $O(m \alpha(m, n))$ of [Chazelle's algorithm](/chazelle-mst/), so the algorithm is provably optimal, but its running time is unknown. It works by cutting the graph into tiny pieces with a [soft heap](/soft-heap/), solving each piece with a precomputed optimal [decision tree](/decision-tree/), and recursing on a smaller graph.

## In plain words

Most algorithms come with a running time that you can write down. This one is different. Its authors proved that no method that works by comparing edge weights can do better than it by more than a constant factor, yet no one can say how fast it is in a formula.

The trick is to cut the network into very small parts, each with only a handful of points. For such tiny networks, a computer can search, before the real work starts, for the best possible way to find the cheapest tree. Each part is then solved in the best possible way. Joining the parts and repeating on a much smaller network costs little. So the whole run is as fast as the best way to solve the tiny parts, which is as fast as anything can be.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and real weights. Weights may be negative and may tie. Parallel edges and self-loops are allowed, and the graph does not have to be [connected](/connected-graph/). The output is a minimum spanning forest. Edges are compared by the key $(w(e), \text{index of } e)$, so all keys are distinct and the output is the unique minimum forest for this order; with ties in $w$ it is the forest that [Kruskal's algorithm](/kruskal/) returns when it breaks ties by index.

The model is the comparison model of the word RAM: the algorithm may do any bookkeeping, but it looks at weights only by comparing two of them. $T^\ast(m, n)$ is the least worst-case number of comparisons that any decision tree needs to find the MSF of every graph with $n$ vertices and $m$ edges.

## The algorithm

```pseudo id=main
OPTIMAL-MSF(G)
L1  if G has no edge other than self-loops then return ∅
L2  r ← ⌈log₂ log₂ log₂ n⌉  ▷ the largest piece size
L3  (M_1, …, M_s, C, L) ← PARTITION(G, r)  ▷ pieces of at most r vertices, corrupted edges C, link edges L
L4  F ← L ∪ DECISION-TREE(M_1 \ C) ∪ … ∪ DECISION-TREE(M_s \ C)  ▷ MSF of each piece
L5  G_A ← (G \ C) / F without self-loops  ▷ contract each component of F
L6  F_A ← DENSE-MSF(G_A)
L7  G_B ← F ∪ F_A ∪ C, as a subgraph of G
L8  (G_C, F_B) ← two Borůvka steps on G_B: F_B is the set of chosen edges and G_C is G_B / F_B
L9  F_C ← OPTIMAL-MSF(G_C)
L10 return F_B ∪ F_C
```

**PARTITION.** Mark all vertices live. For each live vertex $v$, grow a piece $S$ from $v$ as in [Prim's algorithm](/prim/): keep the edges that leave $S$ in a soft heap, and repeatedly extract the edge with the least current key. A soft heap may *corrupt* keys, that is, raise them, so that it can run faster. An extracted edge with a corrupted key goes into $C$ and is skipped. An edge with both ends in $S$ is skipped. An edge to a vertex of an earlier piece goes into $L$, and the growth stops. Otherwise its other end joins $S$, and its edges enter the heap. The growth also stops when $|S| = r$ or the heap is empty. Then all corrupted edges left in the heap go into $C$, and the vertices of $S$ become dead. $M_i$ is the subgraph induced by the $i$-th piece.

**DECISION-TREE.** Before the main work, the algorithm builds an optimal decision tree for every graph with at most $r$ vertices by brute-force search. Since $r = \lceil \log_2 \log_2 \log_2 n \rceil$ is tiny, there are few such graphs and the search takes $o(n)$ time. Line L4 runs the decision tree of each piece on its weights.

**DENSE-MSF.** $G_A$ has few vertices compared with its edges, and on such dense graphs the [Fredman-Tarjan](/fredman-tarjan-mst/) algorithm runs in linear time.

**Borůvka steps.** Line L8 runs two [Borůvka](/boruvka/) steps, each of which adds the least edge at each vertex and contracts, so $G_C$ has at most a quarter of the vertices of $G_B$ that have edges.

This page follows the structure of the paper. The details of PARTITION are given in the form that makes the proof short: a corrupted edge never makes a piece grow, and the link edge at which a piece stops is kept in $F$. The Python code on this site follows the recursion, the partition with corrupted keys, the contraction and the Borůvka steps, but it replaces the decision trees and the dense step by Kruskal's algorithm, which compute the same forests, and the soft heap by a binary heap whose keys a test can corrupt. So it checks the correctness argument, not the optimal running time.

## Example

The graph has the vertices $a$ to $f$ and nine edges, with two ties in weight that the index breaks. Take $r = 3$.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

Suppose the soft heap corrupts the key of $bc$ from 1 to 6 when it enters the heap of the first piece.

| step | line | action | result |
|---|---|---|---|
| 1 | L3 | grow from $a$: heap $ab$ 4, $ac$ 3; extract $ac$, add $c$; insert $bc$ (key 6, corrupted), $cd$ 4, $ce$ 5 | $S = \{a, c\}$ |
| 2 | L3 | extract $ab$ 4, add $b$; $|S| = 3$, stop; the corrupted $bc$ is still in the heap | piece $\{a, b, c\}$, $C = \{bc\}$ |
| 3 | L3 | grow from $d$: extract $bd$ 2, and $b$ is dead | piece $\{d\}$, link $bd$ |
| 4 | L3 | grow from $e$: extract $ef$ 2, add $f$; extract $ce$ 5, and $c$ is dead | piece $\{e, f\}$, link $ce$ |
| 5 | L4 | MSF of $\{a, b, c\}$ without $bc$ is $\{ab, ac\}$; of $\{e, f\}$ it is $\{ef\}$ | $F = \{ab, ac, ef, bd, ce\}$ |
| 6 | L5, L6 | $F$ is a spanning tree, so $G_A$ has one vertex and no edges | $F_A = \emptyset$ |
| 7 | L7 | $G_B = F \cup C$ | $\{ab, ac, bc, bd, ce, ef\}$ |
| 8 | L8 | step 1 picks $ac$ at $a$, $bc$ at $b$ and $c$, $bd$ at $d$, $ef$ at $e$ and $f$; step 2 picks $ce$ | $F_B = \{ac, bc, bd, ce, ef\}$ |
| 9 | L9 | $G_C$ has one vertex | $F_C = \emptyset$ |

The result is $\{ac, bc, bd, ce, ef\}$ with weight 13. The corruption made $F$ wrong, since it holds $ab$ instead of $bc$, but $bc$ was kept in $C$, and the Borůvka steps on $G_B$ restored the minimum tree. Without corruption, the first piece is grown by $ac$ and $bc$, and $F$ is already the minimum tree.

## Correctness

**Theorem.** OPTIMAL-MSF returns the unique minimum spanning forest $F^\ast$ for the key order, for every graph and every behaviour of the soft heap.

The proof has three steps. (1) Every edge of $F$ is in $\operatorname{MSF}(G \setminus C)$: when PARTITION extracts an uncorrupted edge from the heap of $S$, every edge of $G \setminus C$ that leaves $S$ is in the heap with its true key, so the extracted edge is the least edge of $G \setminus C$ across the cut, and the [cut property](/cut-property/) applies. The MSF of $M_i \setminus C$ is the tree that grew the piece. (2) Since $F \subseteq \operatorname{MSF}(G \setminus C)$, contracting $F$ gives $\operatorname{MSF}(G \setminus C) = F \cup \operatorname{MSF}((G \setminus C)/F)$, and every edge of $F^\ast$ outside $C$ lies in $\operatorname{MSF}(G \setminus C)$. So $F^\ast \subseteq F \cup F_A \cup C = G_B$, and then $\operatorname{MSF}(G_B) = F^\ast$. (3) The Borůvka edges are in $\operatorname{MSF}(G_B)$, and the recursion on the contracted graph finds the rest, by induction on the number of vertices. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Comparisons and time.** Pettie and Ramachandran prove that all steps except line L4 take $O(m + n)$ time at each level, that the sizes shrink by a constant factor from one level to the next, and that the decision trees of line L4 take $O(T^\ast(m, n))$ comparisons and time in total. The corrupted set $C$ is a small fraction of the edges, set by the error rate of the soft heap, which keeps $G_B$ small. Since $T^\ast(m, n) = \Omega(m)$ for connected graphs, the total is $O(T^\ast(m, n))$.

**What is known about $T^\ast$.** Every algorithm must look at each edge, so $T^\ast(m, n) = \Omega(m)$. Chazelle's algorithm uses $O(m \alpha(m, n))$ comparisons, so $T^\ast(m, n) = O(m \alpha(m, n))$, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). Whether $T^\ast$ is linear is open, and so the running time of the algorithm is known only to lie between these bounds.

| claim | bound | case |
|---|---|---|
| time | $O(T^\ast(m, n))$, which is $O(m \alpha(m, n))$ | worst |
| time | $\Omega(n + m)$ | best |
| extra space | $O(n + m)$ | worst |

The precomputation of the decision trees takes $o(n)$ time because the pieces have at most $\log_2 \log_2 \log_2 n$ vertices.

## Properties

- **Optimal, with an unknown bound.** It is the only known MST algorithm proved optimal in the comparison model. If $T^\ast(m, n) = O(m)$, it runs in linear time.
- **Deterministic.** It uses no random bits; the soft heap is deterministic.
- **Robust to corruption.** Correctness holds for any pattern of corrupted keys; corruption affects only the speed, through the size of $C$.
- **Recursive.** Each level shrinks the graph by a constant factor and recurses once.
- **Impractical.** The constants and the precomputation make it a theoretical result; no one uses it for real graphs.

## Variants and improvements

- **Randomized linear time.** The [Karger-Klein-Tarjan](/karger-klein-tarjan-mst/) algorithm runs in expected $O(m)$ time, so with random bits the question of the time is settled.
- **Chazelle's algorithm.** Chazelle's $O(m \alpha(m, n))$ algorithm uses the same tools, the soft heap and contractible pieces, with an explicit bound.
- **Verification.** [MST verification](/mst-verification/) has a known linear-time algorithm, unlike construction; see also the [lower bound](/mst-lower-bound/) page.

## When to use it

Do not use it to compute trees. Use [Kruskal's](/kruskal/) or [Prim's](/prim/) algorithm, or Borůvka for parallel work. The algorithm matters as a theorem: it settles the comparison complexity of the MST problem up to the value of $T^\ast$, and it shows that any future proof of a linear bound on $T^\ast$ immediately gives a linear-time algorithm.

## Pitfalls

- **Dropping the corrupted edges.** If $C$ is not put back in line L7, an edge of the MSF can be lost. The example shows this: $bc$ is in $C$ and in the result. The tests with random corruption catch it.
- **Growing a piece by a corrupted edge.** In this form of PARTITION a corrupted edge goes to $C$ instead of growing the piece; growing by it breaks step (1) of the proof.
- **Forgetting the link edges.** A piece that stops at an earlier piece is joined to it by its link edge; dropping $L$ is still correct but leaves more vertices in $G_A$, which spoils the size bound.
- **Ties.** Without the index in the key, the Borůvka steps can close a cycle with equal weights. The test with all weights equal catches it.
- **Claiming a running time.** The bound is $O(T^\ast(m, n))$; writing $O(m)$ or $O(m \alpha(m, n))$ as its exact time is wrong in one direction or the other.

## Implementations

## History

Chazelle introduced the soft heap and the $O(m \alpha(m, n))$ algorithm in 2000. Pettie and Ramachandran presented their optimal algorithm at ICALP 2000, and the journal version appeared in the Journal of the ACM in 2002. The question whether $T^\ast(m, n)$ is linear, and so whether there is a deterministic linear-time MST algorithm, remains open.

## References
