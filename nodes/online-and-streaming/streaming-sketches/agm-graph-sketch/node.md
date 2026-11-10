---
tag: 25M25W
kind: algorithm
slug: agm-graph-sketch
name: AGM graph sketch
aliases:
- Ahn-Guha-McGregor sketch
- linear graph sketching
area: online-and-streaming/streaming-sketches
level: advanced
summary: Linear sketch of a graph under edge insertions and deletions. L0 samplers of signed incidence vectors drive Borůvka rounds that find a spanning forest, in O(n log³ n) bits.
solves: [stream-connectivity-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {update: O(log² n), query: O(n log² n)}
  space: {extra: O(n log² n)}
properties: {online: true, deterministic: false, linear: true, dynamic: true, one_pass: true}
history:
  year: 2012
  people: [Kook Jin Ahn, Sudipto Guha, Andrew McGregor]
  note: Ahn, Guha and McGregor introduced linear sketches of graphs at SODA 2012, with spanning forests, k-connectivity, bipartiteness and minimum spanning tree weight in dynamic streams. Nelson and Yu (SODA 2019) proved that the O(n log³ n) bits for spanning forests are optimal.
prereqs: [l0-sampler, boruvka, spanning-forest, linear-sketch, turnstile-model]
see_also: [stream-connectivity-problem, l0-sampling-problem, connected-components, dynamic-connectivity, disjoint-set, edge-connectivity, bipartiteness-testing, greedy-streaming-matching]
sources:
  - paper: doi:10.1137/1.9781611973099.40
    title: Kook Jin Ahn, Sudipto Guha and Andrew McGregor, Analyzing graph structure via linear measurements, SODA 2012
    locator: pp. 459 to 467; the section on connectivity (signed incidence vectors, the spanning forest algorithm and its space), and the sections on k-connectivity, bipartiteness and minimum spanning trees
  - url: https://arxiv.org/abs/1807.05135
    title: Jelani Nelson and Huacheng Yu, Optimal lower bounds for distributed and streaming spanning forest computation, SODA 2019
    locator: the main theorems (Ω(n log³ n) bits for dynamic spanning forest with constant success probability, and Ω(log³ n) bits per vertex for distributed sketching)
  - url: https://arxiv.org/abs/1012.4889
    title: Hossein Jowhari, Mert Sağlam and Gábor Tardos, Tight bounds for Lp samplers, finding duplicates in streams, and related problems, PODS 2011
    locator: the L0 sampler with O(log² n) bits that the sketch uses
  - paper: doi:10.1145/2627692.2627694
    title: Andrew McGregor, Graph stream algorithms, a survey, SIGMOD Record 43(1), 2014
    locator: the section on graph sketching (connectivity in dynamic streams)
---

The AGM graph sketch stores a graph on $n$ vertices whose edges are inserted and deleted in a stream, in $O(n \log^3 n)$ bits, and at the end returns a spanning forest of the final graph with high probability. Each vertex keeps [L0 samplers](/l0-sampler/) of a signed incidence vector, chosen so that the sum of the vectors over a set of vertices is nonzero exactly on the edges that leave the set. A sampler of that sum, which is the sum of the samplers, returns such an edge, and [Borůvka](/boruvka/) rounds merge components along these edges. The sketch is linear, so it handles deletions, and it can be built in parts on many machines and added up. On this page $n$ is the number of vertices and the vertices are $1, \ldots, n$.

## In plain words

Each person in a town keeps a small notebook about their own friendships. A new friendship adds an entry to two notebooks, and an ended friendship removes it from both. The entries are made so that when a group of people adds up their notebooks, every friendship inside the group cancels out. What is left describes only the friendships with people outside the group, and a small trick reads one of them. So each group can find a friend outside itself and join with that friend's group. After a few such rounds, every group is a whole circle of friends that has no friend outside. The notebooks are tiny compared with a full list of friendships.

## The problem

The input is a stream of updates $(u, v, \pm 1)$, each inserting or deleting the edge $\{u, v\}$ of a simple graph on the vertex set $[n]$. The stream may delete only edges that are present. After the stream, output a spanning forest of the final graph $G = (V, E)$, that is, a forest $F \subseteq E$ with the same connected components as $G$. This is the dynamic version of the [connectivity in streams problem](/stream-connectivity-problem/). The algorithm may fail with probability at most a given $\delta_{\text{all}}$, over its own random choices, for each fixed stream.

## The algorithm

**Signed incidence vectors.** Index the possible edges by the pairs $u < v$, so the vectors have $\binom{n}{2}$ coordinates (the code uses the index $(u - 1)n + v$). For a vertex $w$, the vector $a_w$ has, at the coordinate of an edge $\{u, v\} \in E$ with $u < v$,
$$a_w[u, v] = \begin{cases} +1 & \text{if } w = u, \\ -1 & \text{if } w = v, \\ 0 & \text{otherwise,} \end{cases}$$
and 0 at the coordinates of pairs that are not edges. An update of the edge $\{u, v\}$ changes one coordinate of $a_u$ and one coordinate of $a_v$, so the vectors follow the stream as [turnstile](/turnstile-model/) updates.

**Cut lemma.** For every $S \subseteq V$, the vector $\sum_{w \in S} a_w$ has the value $[u \in S] - [v \in S]$ at the edge $\{u, v\}$. So it is nonzero exactly on the edges with one end in $S$.

**Sketches.** Use $R = O(\log n)$ rounds. For each round $r$, draw the seeds of one L0 sampler, and give every vertex $w$ its own counters $\mathcal{S}_r(a_w)$ with these seeds. Because the samplers are linear and share seeds, $\sum_{w \in S}\mathcal{S}_r(a_w) = \mathcal{S}_r(\sum_{w \in S} a_w)$.

```pseudo id=main
UPDATE(u, v, d)            ▷ d = +1 inserts the edge, d = −1 deletes it; u < v
L1  e ← the index of the pair (u, v)
L2  for r ← 1 to R do add d at coordinate e to S_r(a_u), and −d at coordinate e to S_r(a_v)

SPANNING-FOREST()
L3  F ← ∅; every vertex is its own component; no component is closed
L4  for r ← 1 to R, while some component is not closed do
L5      for each component C that is not closed do
L6          s ← the query of the sum of S_r(a_w) over w ∈ C
L7          if s = EMPTY then mark C closed; if s is an edge, keep it as the pick of C
L8      for each pick {a, b}: if a and b are in different components, merge them and add {a, b} to F
L9  return F
```

A query of line L6 returns an edge that leaves $C$, EMPTY if no edge leaves $C$, or FAIL. Line L8 uses a [disjoint-set](/disjoint-set/) structure, so it never adds an edge inside a component, and $F$ stays a forest.

## Example

Take $n = 6$ and the stream: insert $\{1,2\}$, $\{2,3\}$, $\{1,3\}$, $\{4,5\}$, $\{3,4\}$, delete $\{3,4\}$, insert $\{5,6\}$. The final graph has the triangle on 1, 2, 3 and the path 4, 5, 6. With the code's index $e = 6(u - 1) + v$ the edges are $\{1,2\} \to 2$, $\{1,3\} \to 3$, $\{2,3\} \to 9$, $\{4,5\} \to 23$, $\{5,6\} \to 30$, and the deleted edge $\{3,4\} \to 16$. The signed vectors are

| vertex | nonzero entries of $a_w$ |
|---|---|
| 1 | $+1$ at 2, $+1$ at 3 |
| 2 | $-1$ at 2, $+1$ at 9 |
| 3 | $-1$ at 3, $-1$ at 9 |
| 4 | $+1$ at 23 |
| 5 | $-1$ at 23, $+1$ at 30 |
| 6 | $-1$ at 30 |

The edge $\{3, 4\}$ left no trace: its insert and its delete cancel in $a_3$ and in $a_4$. For $S = \{1, 2\}$, $a_1 + a_2$ is $+1$ at 3 and at 9, which are the edges $\{1,3\}$ and $\{2,3\}$ that leave $S$; the inner edge $\{1,2\}$ cancels. For $S = \{1, 2, 3\}$ the sum is 0.

The code of this page with seed 0 uses $R = 14$ rounds of 3 copies with 9 levels each. In round 1 the six single-vertex queries return $\{1,2\}$, $\{1,2\}$, $\{1,3\}$, $\{4,5\}$, $\{5,6\}$, $\{5,6\}$. Line L8 adds $\{1,2\}$, skips the second $\{1,2\}$, adds $\{1,3\}$, $\{4,5\}$ and $\{5,6\}$, and skips the second $\{5,6\}$. In round 2 the components $\{1,2,3\}$ and $\{4,5,6\}$ both return EMPTY and are closed, and the algorithm stops after 2 of its 14 rounds with $F = \{\{1,2\}, \{1,3\}, \{4,5\}, \{5,6\}\}$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts.

1. **Cut lemma.** Coordinate $\{u, v\}$ of $\sum_{w \in S} a_w$ receives $+1$ from $u$ if $u \in S$ and $-1$ from $v$ if $v \in S$, so it is $[u \in S] - [v \in S]$, which is nonzero exactly when one end is in $S$.
2. **Safety.** Assume that every sampler answers correctly when it does not FAIL (the 1-sparse test errs with probability at most $n^2/q$ per level, which a union bound makes negligible). Then every edge in $F$ is an edge of $G$ that joins two different components, so $F$ is a forest in $G$. A component is closed only if no edge of $G$ leaves it, so a closed component is a whole connected component of $G$. Hence, if every component is closed at the end, $F$ is a spanning forest.
3. **Progress.** Let $k_r$ be the number of components at the start of round $r$ that have an edge leaving them. Round $r$ uses fresh seeds, and the components depend only on earlier rounds, so each of these components gets an edge with probability at least $1 - \delta$, where $\delta$ is the failure probability of one sampler. If $s$ of them get an edge, merging removes at least $s/2$ components, since a group of $t \ge 2$ components joined by picked edges becomes one. So $\mathbb{E}[k_{r+1}] \le \frac{1 + \delta}{2}k_r$, and $\Pr[k_{R+1} \ge 1] \le n\left(\frac{1 + \delta}{2}\right)^R$. With $R = \lceil \log(n/\delta_{\text{all}})/\log(2/(1 + \delta)) \rceil$ this is at most $\delta_{\text{all}}$.

## Complexity

**Space.** Each vertex keeps $R$ samplers of dimension $\binom{n}{2}$. With a constant failure probability $\delta$, a sampler has $O(\log n)$ levels of three counters of $O(\log n)$ bits, so $O(\log^2 n)$ bits. With $R = O(\log n)$ rounds and $\delta_{\text{all}} = 1/\mathrm{poly}(n)$, the total is $n \cdot O(\log n) \cdot O(\log^2 n) = O(n \log^3 n)$ bits, or $O(n \log^2 n)$ words. The seeds take $O(\log^2 n)$ bits more. A graph can have $\Theta(n^2)$ edges, so this is much less than storing the edges.

**Lower bound.** Nelson and Yu (2019) proved that every structure that keeps a spanning forest under edge insertions and deletions, and answers correctly with a constant probability, needs $\Omega(n \log^3 n)$ bits. So the AGM sketch is optimal. They also proved $\Omega(\log^3 n)$ bits per vertex in the distributed model where each vertex sends one message.

**Time.** An update touches $R$ rounds and, in each, a constant number of copies with $O(\log n)$ levels in the worst case and $O(1)$ levels in expectation, plus a power $z^e \bmod q$ in $O(\log n)$ multiplications. So an update costs $O(\log^2 n)$ word operations. A round of SPANNING-FOREST adds up all $n$ vertex sketches once, $O(n\log n)$ operations, and there are $O(\log n)$ rounds, so the query costs $O(n \log^2 n)$, plus near-linear time for the disjoint-set operations.

## Properties

- **Linear.** The sketch of the graph is a fixed random matrix times the vector of all $a_w$, so the order of updates does not matter, sketches of edge-disjoint parts add up, and an edge deletion is the update with $-1$.
- **Vertex-based.** Each vertex's sketch depends only on its own edges. This gives a distributed protocol: each vertex sends its $O(\log^3 n)$ bits to a referee, who computes a spanning forest.
- **Randomized, oblivious adversary.** The guarantee holds for a stream fixed before the seeds are drawn.
- **One pass, any order.** The stream can interleave inserts and deletes freely; only the final graph matters.

## Variants and improvements

- **k-edge-connectivity.** Keep $k$ independent sketches. Find a spanning forest $F_1$ with the first, subtract the edges of $F_1$ from the second by linearity, find $F_2$, and so on. The union $F_1 \cup \cdots \cup F_k$ is a certificate of $k$-edge-connectivity, in $O(kn \log^3 n)$ bits.
- **Bipartiteness.** A graph is bipartite exactly when its double cover, with vertices $(v, 0)$ and $(v, 1)$ and edges $(u, i)(v, 1 - i)$, has twice as many components. Sketching the double cover answers bipartiteness.
- **Minimum spanning tree weight.** Sketch the subgraphs of edges with weight at most $(1 + \varepsilon)^i$ for each $i$ and count their components, which gives the weight of a minimum spanning tree within a factor $1 + \varepsilon$.
- **Cut sparsifiers and spanners.** Later work by the same authors (PODS 2012) builds cut sparsifiers and spanners from similar sketches, with more passes or more space.
- **XOR sketches.** For spanning forests one can replace the integer counters by the XOR of edge identifiers with random subsampling, as in the dynamic connectivity structure of Kapron, King and Mountjoy (SODA 2013).

## When to use it

Use the AGM sketch when a graph changes by both insertions and deletions and you want its connected components, a spanning forest, or its $k$-edge-connectivity, with memory near linear in the number of vertices rather than the number of edges. It also fits distributed settings where each machine or vertex sees only its own edges. If the stream has no deletions, a [disjoint-set](/disjoint-set/) structure with $O(n \log n)$ bits is simpler and smaller. If the whole graph fits in memory, ordinary [connected components](/connected-components/) by search is faster.

## Pitfalls

- **Fresh samplers per round.** The components of round $r$ depend on the samples of the earlier rounds. Reusing one sampler for all rounds breaks the independence that the progress argument needs, and an adaptive choice of the sets $C$ can then make it fail.
- **Shared seeds.** All vertices must use the same seeds within a round, or the sum of the sketches is not the sketch of the sum.
- **Sign convention.** The $+1$ must go to one fixed end of each edge and $-1$ to the other. With $+1$ at both ends, inner edges add up instead of cancelling.
- **Simple graphs.** The guarantee is for a final graph with multiplicities 0 or 1. Inserting the same edge twice gives a multiplicity 2, which the sketch handles, but deleting an edge that is absent gives $-1$, which the cut lemma still treats as an edge.
- **Too few rounds.** The bound $n((1 + \delta)/2)^R$ needs $R$ of order $\log n$; in practice most graphs finish in far fewer rounds, but a fixed small $R$ has no guarantee.

## Implementations

## History

Ahn, Guha and McGregor (SODA 2012) introduced linear sketches of graphs. Their paper gives the spanning forest sketch of this page, $k$-edge-connectivity, bipartiteness and the weight of a minimum spanning tree, all in one pass over a dynamic stream, and a second paper at PODS 2012 adds sparsifiers and spanners. The sketch relies on the L0 samplers of Jowhari, Sağlam and Tardos (2011). Kapron, King and Mountjoy (2013) used a related cut-set trick for a dynamic connectivity structure with polylogarithmic worst-case update time. Nelson and Yu (2019) proved that $\Omega(n \log^3 n)$ bits are needed, so the sketch is optimal. Implementations for very large graphs, such as GraphZeppelin (Tench et al., SIGMOD 2022), use variants of the sketch.

## References
