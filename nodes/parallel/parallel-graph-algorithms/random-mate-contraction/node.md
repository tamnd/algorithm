---
tag: BNJSDN
kind: technique
slug: random-mate-contraction
name: Random-mate contraction
aliases:
- Reif's random-mate
- random mating
area: parallel/parallel-graph-algorithms
level: advanced
summary: Each vertex flips a coin and contracts its edges to tails neighbours, shrinking the graph by a constant factor per round in expectation.
prereqs: [graph-contraction, linearity-of-expectation, markov-inequality, work-span-model]
see_also: [list-contraction, tree-contraction, shiloach-vishkin, parallel-minimum-spanning-tree, luby-mis, cole-vishkin, crcw-pram, connected-components]
sources:
  - paper: "John H. Reif, Optimal parallel algorithms for integer sorting and graph connectivity, Technical Report TR-08-85, Aiken Computation Laboratory, Harvard University, 1985"
    title: Optimal parallel algorithms for integer sorting and graph connectivity
    locator: the random-mate connectivity algorithm; report number and sections to be checked
  - paper: doi:10.1109/SFCS.1985.43
    title: Gary L. Miller and John H. Reif, Parallel tree contraction and its application, 26th Annual Symposium on Foundations of Computer Science (FOCS), 1985
    locator: the randomized COMPRESS step, in which coin flips choose the nodes to splice out
  - url: https://sites.google.com/site/alphalambdabook/
    title: Umut A. Acar and Guy E. Blelloch, Algorithms, Parallel and Sequential, draft book for Carnegie Mellon course 15-210
    locator: part Graph Contraction, the chapter on star contraction (coin flips, the 1/4 bound, and connectivity in O(m log n) work and O(log^2 n) span); chapter numbers differ between drafts
---

Random-mate contraction is a technique that shrinks a graph in parallel by coin flips: in each round every vertex flips a fair coin, and each vertex that flips tails and has a neighbour that flips heads merges into one such neighbour. The merged groups are stars, so one round of [graph contraction](/graph-contraction/) needs no long chains of pointers, and each non-isolated vertex disappears with probability at least $1/4$. So $O(\log n)$ rounds suffice with high probability on any graph. Reif (1985) used it for connectivity and Miller and Reif (1985) for [tree contraction](/tree-contraction/); [list contraction](/list-contraction/) is the same idea on a path.

## In plain words

In a crowd, everybody wants to pair up with a neighbour, but if everybody chooses at once, the choices form long chains. A coin breaks the clash. Everybody flips. People who flip heads stand still and act as hosts. People who flip tails look around for a host next to them, and if they find one, they join that host and leave the crowd.

No host moves, so nobody can join somebody who is also leaving. Each group is one host with some guests around it.

A person with at least one neighbour leaves with a chance of at least one in four: one half to flip tails, times at least one half that some neighbour flips heads. So each round removes about a quarter of the crowd, and the crowd shrinks to nothing after a number of rounds that grows with the logarithm of its size.

## When it applies

Use it when a problem can be solved by [contraction](/graph-contraction/): the answer for the graph follows from the answer for the graph with some connected groups merged, as in connectivity, spanning forests, list ranking and tree evaluation. It needs random coins and a step in which one vertex picks one of several candidates, which is an arbitrary concurrent write on the [CRCW PRAM](/crcw-pram/) or a random or minimum choice in the [work-span model](/work-span-model/). It fits the case where a deterministic choice would need symmetry breaking: in a cycle all vertices look the same, and a coin is the cheapest way to tell them apart.

## The template

Notation: $G = (V, E)$ has $n$ vertices and $m$ edges, $W$ is the work and $S$ the span. The model is the work-span model with independent fair coins. "With high probability" (w.h.p.) means with probability at least $1 - n^{-c}$ for any fixed constant $c > 0$, with the constant in the bound depending on $c$.

```pseudo id=template
RANDOM-MATE-CONTRACT(G)
T1  while G has an edge do
T2      for all v in parallel do coin[v] ← heads or tails, each with probability 1/2, fresh in each round
T3      for all v in parallel do r[v] ← v
T4      for all edges {u, v} in parallel do
T5          if coin[u] = tails and coin[v] = heads then r[u] ← v    ▷ several writers: one wins
T6      G ← the graph on {r[v]} with edges {r[u], r[v]} for each edge with r[u] ≠ r[v]
T7      (record r, to map the answer back after the recursion)
```

A heads vertex never changes $r$, and a tails vertex points to a heads vertex, so each block is a star of depth at most 1. One round costs $O(n + m)$ work and $O(\log n)$ span (the relabeling and a [pack](/parallel-pack/) of the edges).

**Theorem.** Let $N_t$ be the number of non-isolated vertices at the start of round $t$, with $N_0 \le n$, and let $R$ be the number of rounds. Then $E[N_t] \le (3/4)^t n$, $E[R] \le \log_{4/3} n + 5$, and $\Pr[R > (c + 1) \log_{4/3} n + 1] \le n^{-c}$ for every $c > 0$.

*Proof.* Fix the state at the start of round $t$ and a non-isolated vertex $v$ of degree $d \ge 1$. The coins of the round are fresh and independent, so $v$ flips tails and some neighbour flips heads with probability $\frac{1}{2}(1 - 2^{-d}) \ge \frac{1}{4}$. Such a $v$ joins a heads vertex and is not a vertex of the next graph. A vertex that is isolated now has no edges in any later graph, since an edge of the next graph comes from an edge of this one. So the non-isolated vertices of the next graph are among the survivors of the $N_t$ non-isolated vertices, and by [linearity of expectation](/linearity-of-expectation/), $E[N_{t+1} \mid \text{state}] \le N_t - N_t / 4 = \frac{3}{4} N_t$. Taking expectations and iterating gives $E[N_t] \le (3/4)^t n$.

The loop runs past round $t$ only if $N_t \ge 1$, so by [Markov's inequality](/markov-inequality/), $\Pr[R > t] \le \Pr[N_t \ge 1] \le E[N_t] \le (3/4)^t n$. For $t \ge (c + 1) \log_{4/3} n$ this is at most $n^{-c}$. For the mean, let $t_0 = \lceil \log_{4/3} n \rceil$, so that $(3/4)^{t_0} n \le 1$. Then

$$E[R] = \sum_{t \ge 0} \Pr[R > t] \le t_0 + \sum_{j \ge 0} (3/4)^{j} = t_0 + 4 \le \log_{4/3} n + 5. \qquad \square$$

Since $\log_{4/3} n = \log_2 n / \log_2(4/3) \approx 2.41 \log_2 n$, the mean number of rounds is at most about $2.41 \log_2 n + 5$. For connectivity, each round costs $O(m)$ work, because the number of edges need not fall, so $W = O(m \log n)$ in expectation and $S = O(\log^2 n)$ w.h.p.

## Classic examples

- **Connectivity.** Contract until no edges remain, then each vertex follows its recorded $r$ pointers back up to get the label of its component. This is the star-contraction connectivity algorithm of Acar and Blelloch, with $W = O(m \log n)$ in expectation and $S = O(\log^2 n)$ w.h.p. On a star with $n - 1 \ge 1$ leaves, a round removes the tails leaves when the center flips heads, and only the center when it flips tails and some leaf flips heads. The expected number removed is $\frac{n-1}{4} + \frac{1}{2}(1 - 2^{-(n-1)})$, about a quarter of the vertices, so the factor $3/4$ of the theorem is close to tight on stars.
- **List contraction.** On a linked list, a node that flips heads and whose successor flips tails is spliced out. This is [list contraction](/list-contraction/), the work-efficient core of [list ranking](/parallel-list-ranking/): there the number of edges is the number of nodes minus 1, so it does fall, and the work is $O(n)$ in expectation.
- **Tree contraction.** Miller and Reif (1985) choose the nodes to COMPRESS on chains of a tree by coin flips, together with the RAKE of leaves. See [tree contraction](/tree-contraction/).
- **Spanning forests.** Record, for each tails vertex that joins a host, the edge that it used. The recorded edges form a spanning forest of $G$.

## Variations

- **Biased coins.** With heads probability $p$, a vertex of degree 1 is removed with probability $p(1 - p)$, which is largest at $p = 1/2$.
- **Deterministic coin tossing.** On lists and rooted trees, the [Cole-Vishkin](/cole-vishkin/) technique replaces the coins by colors computed from the vertex names, in $O(\log^\ast n)$ steps. On general graphs there is no such direct replacement; [Shiloach-Vishkin](/shiloach-vishkin/) is a deterministic connectivity algorithm that hooks trees by vertex names instead.
- **Hooking to the smallest neighbour.** [Parallel Borůvka](/parallel-minimum-spanning-tree/) contracts along the lightest edge of each vertex. The blocks are trees, not stars, so they need [pointer jumping](/pointer-jumping/), but each round halves the number of vertices.
- **Independent sets.** [Luby's algorithm](/luby-mis/) uses random values in the same way, to pick vertices that no neighbour beats, but it removes them with their neighbours instead of merging them.

## Pitfalls

- **Letting heads vertices hook too.** If every vertex may hook to any neighbour, the pointers form long paths and cycles. The blocks are then not stars, and the round needs pointer jumping and a rule to break cycles.
- **Reusing the coins.** The bound needs fresh coins in each round. With coins fixed once, a graph whose vertices all flipped heads never changes.
- **Counting isolated vertices.** An isolated vertex is never removed. The bound $E[N_t] \le (3/4)^t n$ is for the non-isolated vertices; the isolated ones are finished components and leave the computation.
- **Claiming linear work for graphs.** The vertices fall geometrically, but the edges do not have to, because the edges between blocks stay. Connectivity by random mate is $O(m \log n)$ work, not $O(m)$. On lists and trees the edges do fall with the vertices.
- **Two winners for one tails vertex.** A tails vertex with several heads neighbours must take exactly one of them. If the code lets every edge write and then reads $r[u]$ in the same step, $u$ can end up in two blocks.

## Exercises

1. Show that on a cycle of $n$ vertices, a round removes exactly the tails vertices with at least one heads neighbour, and compute the expected number removed. (Answer: each vertex is removed with probability $\frac{1}{2} \cdot \frac{3}{4} = \frac{3}{8}$, so $3n/8$.)
2. Give a graph on which one round removes a vertex with probability exactly $1/4$ for every vertex. (A perfect matching: every vertex has degree 1.)
3. Prove that the recorded edges of the spanning forest example form a forest that spans each component.
4. Show that on the complete graph with $n \ge 2$ vertices one round removes $\frac{n}{2}(1 - 2^{-(n-1)})$ vertices in expectation. (A vertex is removed when it flips tails and one of the other $n - 1$ vertices flips heads.)

## References
