---
tag: CXSCDF
kind: algorithm
slug: nagamochi-ibaraki-certificate
name: Nagamochi-Ibaraki sparse certificate
aliases:
- Sparse k-connectivity certificate
area: graphs/connectivity
level: research
summary: Extracts a sparse subgraph with O(kn) edges that preserves k-connectivity.
solves: [edge-connectivity, vertex-connectivity]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the connectivity to preserve}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true}
history:
  year: 1992
  people: [Hiroshi Nagamochi, Toshihide Ibaraki]
  note: One scan in maximum-label order splits the edges into forests; the first k forests form a certificate for k-edge and k-vertex connectivity.
prereqs: [k-edge-connected-graph, k-vertex-connected-graph, spanning-forest, bucket-queue]
see_also: [nagamochi-ibaraki, edge-connectivity, vertex-connectivity, even-tarjan-vertex-connectivity, menger-theorem, sparsification, stoer-wagner, global-min-cut-problem]
sources:
  - paper: doi:10.1007/BF01758778
    title: Hiroshi Nagamochi and Toshihide Ibaraki, A linear-time algorithm for finding a sparse k-connected spanning subgraph of a k-connected graph, Algorithmica 7, 583 to 596 (1992)
    locator: the whole paper (the scanning procedure, the forest decomposition, and the certificates for k-edge and k-vertex connectivity with at most k(n - 1) edges)
  - paper: doi:10.1137/0405004
    title: Hiroshi Nagamochi and Toshihide Ibaraki, Computing edge-connectivity in multigraphs and capacitated graphs, SIAM Journal on Discrete Mathematics 5(1), 54 to 66 (1992)
    locator: the whole paper (the same scan used to compute edge connectivity without flows)
  - paper: doi:10.1137/0222013
    title: Joseph Cheriyan, Ming-Yang Kao and Ramakrishna Thurimella, Scan-first search and sparse certificates, an improved parallel algorithm for k-vertex connectivity, SIAM Journal on Computing 22(1), 157 to 174 (1993)
    locator: the sections on scan-first search and certificates (the forests of any scan-first search give a k-vertex-connectivity certificate)
  - book: doi:10.1017/cbo9780511721649
    title: Hiroshi Nagamochi and Toshihide Ibaraki, Algorithmic Aspects of Graph Connectivity, Cambridge University Press (2008)
    locator: the chapter on maximum adjacency orderings and forest decompositions
---

The Nagamochi-Ibaraki certificate is a subgraph $H_k$ of an undirected graph $G$ with at most $k(n - 1)$ edges such that $H_k$ is $k$-edge-connected exactly when $G$ is, and, for simple graphs, $k$-vertex-connected exactly when $G$ is. One scan over the graph, always taking the vertex with the most edges to the scanned part, splits the edges into forests $F_1, F_2, \ldots$, and $H_k$ is the union of the first $k$. The scan takes $\Theta(n + m)$ time. Algorithms that test $k$-connectivity on a dense graph run it first, which replaces $m$ by $O(kn)$ in their running time.

## In plain words

A dense network has far more links than it needs to stay connected after a few failures. The question is which links can be thrown away without making it any more fragile, as long as at most $k$ failures matter.

The method visits the nodes one by one. It always visits next the node that has the most links back to the nodes already visited. When it visits a node, it hands each link to a not yet visited neighbor a number: the first such link a neighbor receives gets number 1, the second gets number 2, and so on.

The links with number 1 form a spanning forest, the links with number 2 another forest, and so on. Keeping only the links numbered 1 to $k$ keeps every cut of size below $k$ exactly as it was, and cuts at least $k$ in size.

## The problem

The input is an undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and $m$ edges, and an integer $k \ge 1$. [Parallel edges](/multigraph/) and [self-loops](/self-loop/) are allowed. Write $\lambda_G(u, v)$ for the least number of edges whose removal separates $u$ from $v$. The output is a set $H_k \subseteq E$ such that:

- $|H_k| \le k(n - 1)$;
- for every pair $u \ne v$, $\min(k, \lambda_{H_k}(u, v)) = \min(k, \lambda_G(u, v))$, so $H_k$ is [k-edge-connected](/k-edge-connected-graph/) exactly when $G$ is.

For a simple graph the same $H_k$ is also [k-vertex-connected](/k-vertex-connected-graph/) exactly when $G$ is. This second property fails with parallel edges, see the Pitfalls; for vertex connectivity, delete parallel copies and loops first, which does not change it.

## The algorithm

```pseudo id=main
NI-CERTIFICATE(G, k)
L1  for each vertex v do r[v] ← 0; mark v unscanned; put v in bucket 0
L2  for each edge e do label[e] ← 0
L3  repeat n times
L4      x ← an unscanned vertex with the largest r[x]      ▷ ties broken arbitrarily
L5      mark x scanned
L6      for each edge e = {x, y} with y unscanned and y ≠ x do
L7          r[y] ← r[y] + 1
L8          label[e] ← r[y]
L9          move y to bucket r[y]
L10 return the edges e with 1 ≤ label[e] ≤ k
```

$r[y]$ counts the edges between $y$ and the scanned vertices, so line L4 picks the unscanned vertex most strongly tied to the scanned part, a *maximum adjacency* order. Each non-loop edge gets its label once, when the first of its ends is scanned; a loop keeps label 0. The forest $F_i$ is the set of edges with label $i$.

The buckets form a [bucket queue](/bucket-queue/) indexed by $r$, with a pointer to the highest non-empty bucket. The pointer rises by at most one at each step of line L7 and never falls below 0, so its total movement is $O(n + m)$.

## Example

Take $K_4$ on $\{0, 1, 2, 3\}$, with edges numbered $e_0 = \{0,1\}$, $e_1 = \{0,2\}$, $e_2 = \{0,3\}$, $e_3 = \{1,2\}$, $e_4 = \{1,3\}$, $e_5 = \{2,3\}$, and add two parallel edges $e_6, e_7$ between $3$ and $4$ and a loop $e_8$ at $4$. Ties go to the vertex moved most recently, and at the start to vertex 0.

| step | scanned $x$ | $r[x]$ | labels given |
|---|---|---|---|
| 1 | 0 | 0 | $e_0 \to 1$, $e_1 \to 1$, $e_2 \to 1$; now $r = 1$ at 1, 2, 3 |
| 2 | 3 | 1 | $e_4 \to 2$, $e_5 \to 2$, $e_6 \to 1$, $e_7 \to 2$; now $r[1] = r[2] = r[4] = 2$ |
| 3 | 4 | 2 | none; the loop is skipped |
| 4 | 2 | 2 | $e_3 \to 3$; now $r[1] = 3$ |
| 5 | 1 | 3 | none |

So $F_1 = \{e_0, e_1, e_2, e_6\}$ is a spanning tree, $F_2 = \{e_4, e_5, e_7\}$ is a forest, and $F_3 = \{e_3\}$. The certificate $H_2 = F_1 \cup F_2$ drops only $e_3 = \{1, 2\}$. It still has $\lambda = 2$, like $G$: vertex 4 has its two parallel edges, and $1$ and $2$ are still joined by the two edge-disjoint paths $1, 0, 2$ and $1, 3, 2$, although in $G$ they had three. Its only cut vertex is $3$, as in $G$, so both have vertex connectivity $1$.

## Correctness

Three facts carry the proof, written out in full on [the proof page](proofs/correctness.md).

- **Each $F_i$ is a forest.** Direct each edge of label $i$ from the end scanned first to the other end. A vertex $y$ gets exactly one such edge into it, the one that raised $r[y]$ to $i$, and edges point from earlier to later scanned vertices. A directed graph with in-degree at most 1 and no directed cycle is a forest.
- **Later edges are spanned.** If an edge $\{x, y\}$ has label $j > i$, then $x$ and $y$ are joined by a path in $F_i$. Here the maximum adjacency rule matters: between two moments when the chosen vertex has $r < i$, every scanned vertex and every unscanned vertex with $r \ge i$ hangs in one tree of $F_i$.
- **Cut lemma.** Let $F_1, \ldots, F_k$ be edge-disjoint forests in $G$ such that the ends of every other edge of $G$ are joined in each $F_i$. Then every cut $X$ of $G$ with fewer than $k$ edges keeps all its edges in $H = F_1 \cup \cdots \cup F_k$, and every cut of $G$ with at least $k$ edges keeps at least $k$. Indeed, if a cut loses an edge, the ends of that edge are joined in each $F_i$ by a path, which must cross the cut, so $H$ has $k$ edges across it, one from each forest.

The cut lemma gives $\min(k, \lambda_H(u, v)) = \min(k, \lambda_G(u, v))$. The proof page does not prove the vertex version; it is due to Nagamochi and Ibaraki, and Cheriyan, Kao and Thurimella showed that the forests of any scan-first search give it as well.

## Complexity

- **Time.** Lines L1 and L2 take $\Theta(n + m)$. Each vertex is scanned once, and each edge is looked at twice in line L6, once from each end, so lines L6 to L9 take $\Theta(n + m)$ in total, with each bucket move $O(1)$ in doubly linked lists. Line L4 moves the bucket pointer down past empty buckets; the pointer rises at most $m$ times in total, so it falls at most $m$ times. Line L10 takes $\Theta(m)$. The total is $\Theta(n + m)$ for every input and every $k$.
- **Space.** The labels take $\Theta(m)$, the counters, marks and bucket links $\Theta(n)$, and the buckets need up to $m + 1$ heads, since with parallel edges $r[v]$ can exceed $n - 1$. The implementation also builds incidence lists. The extra space is $\Theta(n + m)$.
- **Output size.** Each $F_i$ is a forest, so $|H_k| \le k(n - 1)$.

## Properties

- **One pass for all $k$.** The labels do not depend on $k$; one scan gives the certificates for every $k$ at once, nested as $H_1 \subseteq H_2 \subseteq \cdots$.
- **$F_1$ is a spanning forest of $G$.** It has one tree per [connected component](/connected-components/), so $H_1$ is a certificate for connectivity.
- **Deterministic once ties are fixed.** Different tie rules give different certificates; all of them satisfy the guarantees.
- **Not minimal.** $H_k$ need not be a smallest $k$-connected spanning subgraph, a problem that is NP-hard for $k \ge 2$ since $k = 2$ includes the Hamiltonian cycle question. It is within a factor 2 of the trivial lower bound $kn/2$ edges, given by the degrees.
- **Not stable under edits.** A single new edge can change many labels. Dynamic algorithms use the [sparsification](/sparsification/) technique to maintain certificates under updates.

## Variants and improvements

- **Any forest decomposition, for edges only.** Choosing $F_1$ as any spanning forest of $G$, $F_2$ as any spanning forest of $G - F_1$, and so on, also satisfies the cut lemma, so it gives an edge certificate in $O(k(n + m))$ time. The single scan does it in linear time for all $k$.
- **Scan-first search, for vertices.** Cheriyan, Kao and Thurimella defined scan-first search, which includes breadth-first search, and showed that $k$ rounds of it, each on the edges left by the previous rounds, give a certificate for $k$-vertex connectivity. Their version parallelizes well.
- **Minimum cuts.** The same maximum adjacency order lets Nagamochi and Ibaraki compute the edge connectivity of a multigraph, or a minimum cut of a graph with capacities, without flows: the last two scanned vertices $s, t$ satisfy $\lambda(s, t) = r[t]$. That is the [Nagamochi-Ibaraki min cut algorithm](/nagamochi-ibaraki/), later simplified by [Stoer and Wagner](/stoer-wagner/).

## When to use it

Run it before any algorithm whose cost grows with $m$ when only connectivity up to $k$ matters and $m$ is much larger than $kn$. Typical uses are testing $k$-vertex connectivity by [Even's method](/even-tarjan-vertex-connectivity/), which needs about $kn$ flows, and testing $k$-edge connectivity with flows or by [Menger's theorem](/menger-theorem/). For $k = 1$ it reduces to computing one spanning forest, and for $k$ near the maximum degree it removes few edges and is not worth running.

## Pitfalls

- **Parallel edges and the vertex version.** The vertex guarantee needs a simple graph. Take a triangle on $\{0, 1, 2\}$ with the edges $\{0, 1\}$ and $\{0, 2\}$ doubled, listed as $\{1, 2\}, \{2, 0\}, \{0, 2\}, \{0, 1\}, \{1, 0\}$. It is 2-vertex-connected. The scan starts at 0, puts one copy of each doubled edge in $F_1$ and the other in $F_2$, and $\{1, 2\}$ in $F_3$, so $H_2$ consists of the four parallel copies and has the cut vertex 0. The edge guarantee still holds: $\lambda = 3$ between 0 and 1 in $G$, and 2 in $H_2$. Removing copies first fixes it.
- **Ties do not matter, the order does.** Scanning in plain breadth-first order while still labeling by $r[y]$ breaks the certificate. Take the edges $\{0,2\}, \{0,3\}, \{0,4\}, \{1,3\}, \{2,4\}, \{3,4\}$ and a breadth-first scan from 0 that visits 2 before 3. Vertex 4 gets label 2 from 2 and then label 3 on $\{3, 4\}$ from 3, so $H_2$ drops $\{3, 4\}$, and the cut around $\{1, 3\}$ falls from 2 edges in $G$ to 1 in $H_2$. The maximum adjacency rule would scan 4 right after 2, since $r[4] = 2$ then.
- **Self-loops.** A loop never helps any connectivity and must not take a forest slot; the scan skips it.
- **Bucket count.** With parallel edges, $r[v]$ can reach the degree of $v$, which may exceed $n - 1$. Allocate $m + 1$ buckets, or cap $r$ at $k$ when only $H_k$ is needed.

## Implementations

## History

Hiroshi Nagamochi and Toshihide Ibaraki gave the scan and the certificate in 1992 in Algorithmica, and in the same year used the same order to compute edge connectivity in multigraphs and minimum cuts in capacitated graphs. Joseph Cheriyan, Ming-Yang Kao and Ramakrishna Thurimella in 1993 introduced scan-first search, which explains why such forests certify vertex connectivity, and used it for a parallel algorithm.

## References
