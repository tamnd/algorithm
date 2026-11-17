---
tag: 561KFN
kind: algorithm
slug: winnower-algorithm
name: WINNOWER
aliases:
- Pevzner-Sze clique motif finding
area: biology/gene-finding-and-motifs
level: advanced
summary: Build a graph of l-mers joined when close in Hamming distance and find the planted motif as a large clique after pruning weak edges.
solves: [planted-motif-problem]
model: word-ram
complexity:
  vars: {n: the number of sequences, G: the length of each sequence, L: the motif length, d: the number of mismatches, W: "the number of windows per sequence, G - L + 1", E: the number of edges of the graph}
  time: {worst: O(n^2 W^2 L + E^2 n W + W^n), build: O(n^2 W^2 L), per_pass: O(E n W)}
  space: {extra: O(n W + E)}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 2000
  people: [Pavel A. Pevzner, Sing-Hoi Sze]
  note: Pevzner and Sze proposed WINNOWER and SP-STAR for the planted (15, 4) motif challenge, on which the methods of the time failed. WINNOWER recasts motif finding as the search for large cliques in a graph of windows.
prereqs: [planted-motif-problem, hamming-distance, clique-problem]
see_also: [random-projection-motif-finding, motif-finding-problem, maximal-clique-enumeration, median-string-problem, gibbs-motif-sampler, meme-algorithm, kmer, np-complete]
sources:
  - paper: "Pavel A. Pevzner and Sing-Hoi Sze, Combinatorial approaches to finding subtle signals in DNA sequences, Proceedings of the Eighth International Conference on Intelligent Systems for Molecular Biology (ISMB 2000), AAAI Press, 2000, pp. 269-278"
    title: Combinatorial approaches to finding subtle signals in DNA sequences
    locator: the graph of windows, extendable cliques and the WINNOWER pruning, and Table 1 with the performance on the (15, 4) problem
  - paper: doi:10.1089/10665270252935430
    title: Jeremy Buhler and Martin Tompa, Finding motifs using random projections, Journal of Computational Biology 9(2), 2002
    locator: pp. 225 to 242, the comparison of PROJECTION with WINNOWER and other methods on planted motif problems
---

WINNOWER, of Pevzner and Sze (2000), solves the [planted motif problem](/planted-motif-problem/) through graphs. Each window of length $L$ of each sequence is a vertex, and two windows of different sequences are joined when their [Hamming distance](/hamming-distance/) is at most $2d$. The planted copies of the motif are within $d$ of the motif, so they are within $2d$ of each other and form a clique with one vertex in each sequence. Random windows give many more edges, but few of them lie in large cliques. WINNOWER removes, again and again, every edge that cannot be part of a clique that reaches all sequences, and then looks for the cliques in the small graph that is left.

## In plain words

Draw a dot for every short piece of every sequence. Join two dots of different sequences when the two pieces differ in at most $2d$ places. The hidden copies of the motif are all close to one word, so each pair of them is joined: they form a group in which every dot is joined to every other, with one dot from each sequence.

Most lines in the drawing join two random pieces that just happen to be similar. Such a line is weak: for some other sequence, no piece there is close to both ends. A line between two real copies is never weak, because every other sequence has a copy close to both. So erase the weak lines, and repeat, since erasing lines can make other lines weak. Only a few lines are left, and among them the real group is easy to find.

## The problem

**Input.** DNA sequences $s_1, \ldots, s_n$ with $n \ge 2$, each of length $G$, a motif length $L$ and a number of mismatches $d$. Each sequence has $W = G - L + 1$ windows. Positions are 1-based on this page and 0-based in the code.

**The graph.** The vertices are the pairs $(i, q)$, the window of $s_i$ at $q$. An edge joins $(i, q)$ and $(k, r)$ for $i \ne k$ when $d_H(s_i[q .. q + L - 1], s_k[r .. r + L - 1]) \le 2d$. The graph is $n$-partite: there are no edges inside a sequence.

**Output.** The pruned graph and its $n$-cliques, each a choice of one window per sequence with every pair within $2d$. Every $(L, d)$ motif of the input gives such a clique, by the triangle inequality, but not every clique comes from a motif: the condition is necessary, not sufficient.

## The algorithm

Call an edge $(u, v)$ *extendable* if every sequence other than those of $u$ and $v$ has a window joined to both $u$ and $v$.

```pseudo id=main
WINNOWER(s[1 .. n], L, d)
L1  build the graph: a vertex per window, an edge between windows of different sequences with d_H ≤ 2d
L2  repeat
L3      for each edge (u, v) do
L4          if some sequence p other than those of u and v has no window joined to both u and v then
L5              remove the edge (u, v)
L6  until a pass removes no edge
L7  C ← the n-cliques of the graph that is left, by backtracking over the sequences in order
L8  return the graph and C
```

Lines L2 to L6 are the winnowing: a pass removes the edges that are not extendable, and the passes go on until every edge is extendable. Line L7 picks a window of $s_1$, then a window of $s_2$ joined to it, then a window of $s_3$ joined to both, and so on; the code keeps, for each sequence, the set of neighbours of each vertex in that sequence, so the candidates are an intersection of sets.

**The general form.** Pevzner and Sze call a clique extendable when every other sequence has a window joined to all of its vertices. An edge of a planted $n$-clique lies in $\binom{n-2}{k-2}$ cliques of size $k$ inside the planted clique, and all of them are extendable. So an edge that lies in fewer extendable $k$-cliques cannot be in the planted clique and can go. The case $k = 2$, where an edge must itself be extendable, is the rule on this page. Larger $k$ removes more edges, at a higher cost per pass.

## Example

Take the small instance of the [planted motif problem](/planted-motif-problem/) page: $L = 5$, $d = 1$ and the four sequences TCGAATCACAAC, CTAGTTACTCTT, GCTAGATTACGT and AACTAGTGGGAC, with the motif AATTA planted at the 1-based starts 4, 3, 5 and 1. Each sequence has $W = 8$ windows, so the graph has 32 vertices. With the bound $2d = 2$, it has 42 edges:

| pair of sequences | 1, 2 | 1, 3 | 1, 4 | 2, 3 | 2, 4 | 3, 4 |
|---|---|---|---|---|---|---|
| edges | 6 | 7 | 5 | 9 | 10 | 5 |

The first pass removes 36 edges, and the second removes none. The 6 edges left join the four windows AATCA (sequence 1, position 4), AGTTA (2, 3), GATTA (3, 5) and AACTA (4, 1): they form one clique, the planted sites, and their consensus is AATTA.

**Measured pruning.** The test generator plants a motif with exactly $d$ changes in each sequence:

| $(n, G, L, d)$ | seed | edges before | edges after | passes | cliques | planted clique found |
|---|---|---|---|---|---|---|
| (8, 100, 11, 2) | 0 | 1872 | 28 | 2 | 1 | yes |
| (10, 100, 12, 3) | 1 | 19,962 | 64 | 3 | 4 | yes |
| (10, 200, 15, 4) | 0 | 90,140 | 126 | 4 | 6 | yes |
| (10, 200, 15, 4) | 1 | 88,543 | 54 | 3 | 2 | yes |

A planted clique with $n = 8$ has $\binom{8}{2} = 28$ edges, so in the first row WINNOWER leaves exactly the planted clique. In the rows with several cliques, most of the other cliques share 8 or 9 of their 10 windows with the planted one, but in the third row three of the six cliques share no window with it: they are random cliques that survive the pruning. These are measurements on these seeds.

**The (15, 4) challenge.** For $n = 20$ and $G = 600$ there are $\binom{20}{2} \cdot 586^2 = 65{,}245{,}240$ pairs of windows, and two random 15-letter windows are within distance 8 with probability about 0.0566, so the graph has about $3.7 \times 10^6$ random edges against the 190 edges of the planted clique, about 20,000 random edges for each true one. Pevzner and Sze report, in Table 1 of their paper, the mean performance coefficient on 8 such samples, a measure of the overlap of the predicted sites with the planted ones that is 1 for a perfect answer: CONSENSUS 0.07, GibbsDNA 0.12, MEME 0.10, WINNOWER 0.92 and SP-STAR 0.84.

## Correctness

WINNOWER is exact in one sense: it never removes an edge of an $n$-clique, so line L7 finds every $n$-clique of the original graph.

**Theorem (no clique edge is removed).** Every edge of an $n$-clique of the graph built at line L1 is in the graph at the end.

*Proof.* Let $K$ be an $n$-clique with one vertex in each sequence. As long as all edges of $K$ are present, each edge $(u, v)$ of $K$ is extendable: for each other sequence $p$, the vertex of $K$ in $p$ is joined to $u$ and to $v$. So line L4 does not remove the first edge of $K$ that would be removed, a contradiction. $\square$

**Theorem (the result is unique).** The graph at the end is the largest subgraph of the original graph in which every edge is extendable, and it does not depend on the order of the removals.

*Proof.* If two subgraphs have only extendable edges, so does their union, since an edge keeps its common neighbours when edges are added. So there is a largest such subgraph $H$. An edge of $H$ is extendable in any graph that contains $H$, so by the argument of the first theorem no edge of $H$ is ever removed. At the end, every edge is extendable, so the graph at the end is a subgraph with only extendable edges and contains $H$; by the choice of $H$, it is $H$. $\square$

So the set $C$ of line L7 is exactly the set of $n$-cliques of the original graph. What WINNOWER does not promise is that $C$ contains only the planted motif: random cliques survive too, and the planted clique, if the input has several near motifs, is only one of them. The tests compare $C$ with brute force over all choices of windows, check that every remaining edge is extendable and that one more pass removes nothing, and check that a removal in a random order gives the same graph. The proofs are in proofs/correctness.md.

## Complexity

- **Building the graph.** There are $\binom{n}{2} W^2$ pairs of windows and each distance takes $O(L)$, so $O(n^2 W^2 L)$ time. This is the main cost in practice.
- **Winnowing.** A pass checks each edge against $n - 2$ other sequences, and each check is an intersection of two sets of at most $W$ vertices, so a pass takes $O(E n W)$ time. Each pass but the last removes an edge, so there are at most $E + 1$ passes; in the measured runs there were 2 to 4.
- **Listing cliques.** Backtracking over the $n$ sequences can take $O(W^n)$ time in the worst case, but after the winnowing the graph is small and the search is fast.
- **Space.** The graph takes $O(nW + E)$. For the $(15, 4)$ challenge, $E$ is in the millions, so the memory of the graph limits the size of the input that WINNOWER can handle.

## Properties

- **Deterministic and complete for cliques.** It finds every $n$-clique of the graph, with no randomness.
- **Not a full solution of the planted motif problem.** A clique is a necessary condition for a motif, not a sufficient one. The consensus of a clique need not be a valid motif, and a clique can come from random windows.
- **Parameter driven.** The bound $2d$ must match the planted motif. A larger bound gives many more edges, a smaller one can lose the planted clique.
- **Order independent.** By the uniqueness theorem, the pruned graph does not depend on the order of the removals.

## Variants and improvements

- **Larger cliques for the rule.** Use extendable cliques of size $k \ge 3$, as in the general form above. Pevzner and Sze used this to prune more of the random edges.
- **SP-STAR.** In the same paper, Pevzner and Sze give SP-STAR, a local search for the sites with a sum of pairs score.
- **Missing sites.** Allow cliques that miss a few sequences, for inputs in which not every sequence has a site.
- **Hashing first.** [PROJECTION](/random-projection-motif-finding/) avoids the full graph: it hashes windows into buckets and refines the large buckets, with much less memory.
- **Exact pattern enumeration.** For small $L$, test all $4^L$ candidate strings, as in the [median string](/median-string-problem/) search; later exact methods for the planted motif problem use this idea with pruning.

## When to use it

Use WINNOWER when the motif is subtle, the planted model with a known $(L, d)$ fits the data, and the graph fits in memory. It found the $(15, 4)$ motif where the profile based methods of its time failed. For long sequences or many sequences, the $W^2$ graph becomes too large, and [PROJECTION](/random-projection-motif-finding/) is the better choice. When the motif model is a profile and not a string with mismatches, use [MEME](/meme-algorithm/) or the [Gibbs motif sampler](/gibbs-motif-sampler/).

## Pitfalls

- **Reading a clique as the motif.** A clique is a set of windows with small pairwise distances. Check that some string is within $d$ of all of them, for example the consensus, before you report it.
- **The wrong bound.** Use $2d$, not $d$, for the edges: two copies of the motif can differ in up to $2d$ places.
- **Memory.** The graph has about $\binom{n}{2} W^2$ times the probability of a close pair edges; work it out before you build it.
- **Edges inside a sequence.** Do not join two windows of the same sequence; the clique must take one window from each sequence.
- **Stopping after one pass.** A removal can make other edges not extendable, so repeat the passes until nothing changes.

## Implementations

## History

Pevzner and Sze (2000) posed the planted $(15, 4)$ motif problem as a challenge: 20 sequences of length 600, each with a copy of a 15-letter motif with 4 mismatches. They showed that CONSENSUS, the Gibbs sampler and MEME failed on it, and they gave two new methods, WINNOWER, based on cliques in a graph of windows, and SP-STAR, based on a sum of pairs score. Both did much better on the challenge. Buhler and Tompa (2001, 2002) then gave PROJECTION, which solves the same problems with much less memory.

## References
