---
tag: WVPFW7
kind: algorithm
slug: breaking-sorting-barrier-sssp
name: Breaking the sorting barrier for directed SSSP
aliases:
- Duan et al. SSSP
- beyond-sorting-barrier SSSP
area: graphs/shortest-paths
level: research
summary: Deterministic directed SSSP in O(m log^(2/3) n) time on sparse graphs with nonnegative weights, beating Dijkstra's sorting bound.
solves: [single-source-shortest-paths]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m log^(2/3) n)}
  space: {extra: O(m + n)}
properties: {deterministic: true, recursive: true}
prereqs: [dijkstra, bellman-ford, single-source-shortest-paths, sorting-barrier, edge-relaxation]
see_also: [sorting-barrier, dijkstra, bellman-ford, fibonacci-heap, thorup-undirected-sssp, comparison-model, near-linear-negative-sssp, single-source-shortest-paths]
sources:
  - url: https://arxiv.org/abs/2504.17033
    title: Ran Duan, Jiayi Mao, Xiao Mao, Xinkai Shu and Longhui Yin, Breaking the sorting barrier for directed single-source shortest paths (STOC 2025)
    locator: Theorem 1.1 (the bound), Section 2 (constant-degree graph, comparison-addition model, Assumption 2.1 and the total order of paths), Section 3.1 (Algorithms 1 to 3, FindPivots, BaseCase and BMSSP, and Lemma 3.3 for the data structure), Sections 3.3 and 3.4 (correctness and time analysis)
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 596 to 615 (1987)
    locator: the O(m + n log n) bound for Dijkstra's algorithm, which is the bound this algorithm improves on sparse graphs
  - paper: "Seth Pettie and Vijaya Ramachandran, A shortest path algorithm for real-weighted undirected graphs, SIAM Journal on Computing 34(6), 1398 to 1431 (2005)"
    locator: the comparison-addition model, in which the new algorithm is stated
---

The algorithm of Duan, Mao, Mao, Shu and Yin computes [single-source shortest paths](/single-source-shortest-paths/) in a directed graph with nonnegative real weights in $O(m \log^{2/3} n)$ time, deterministically, in the comparison-addition model. [Dijkstra's algorithm](/dijkstra/) with a [Fibonacci heap](/fibonacci-heap/) takes $O(m + n \log n)$, and it settles the vertices in sorted order of distance, so on its own it cannot beat sorting; this is the [sorting barrier](/sorting-barrier/). The new algorithm is faster on sparse graphs, when $m = o(n \log^{1/3} n)$. It does not sort the vertices. It mixes Dijkstra's algorithm with a few rounds of [Bellman-Ford](/bellman-ford/) inside a divide-and-conquer recursion, so that a priority queue only has to order a small set of "pivot" vertices instead of all of them. The result appeared at STOC 2025.

## In plain words

Dijkstra's algorithm keeps every frontier vertex in a priority queue and takes them out one by one in order of distance. That ordering is where the $\log n$ per vertex goes.

This algorithm splits the distance range into bands and solves each band by recursion. Before it uses a queue, it runs $k$ rounds of Bellman-Ford from the current frontier. A vertex whose shortest path needs few more steps is finished by those rounds alone. Only the roots of large shortest-path subtrees, at most one in $k$ of the vertices, go into the queue. The recursion has about $\log^{1/3} n$ levels, and each level splits its band into chunks of size $2^t$. So no queue ever has to order many vertices finely.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a source $s$, and a weight $w(u, v)$ on each edge. The output is the distance $\delta(s, v)$ for every $v$ and a [shortest-path tree](/shortest-path-tree/).

**Weight assumptions.** Every weight must be a real number with $w(u, v) \ge 0$; the input is rejected otherwise, and so is NaN. Zero weights, zero-weight cycles, parallel edges and self-loops are allowed. Since no edge is negative, there is no negative cycle, and a negative cycle in the input is rejected with its negative edge. Vertices that $s$ does not reach get $\delta = +\infty$ and no parent. The algorithm uses weights only by adding and comparing them, which is the comparison-addition model.

## The algorithm

The labels $\hat d(v)$ are compared as path keys: length first, then the number of edges, then the vertex sequence from the end. This is the paper's Assumption 2.1, which makes all path lengths different. Two parameters are fixed, $k = \lfloor \log^{1/3} n \rfloor$ and $t = \lfloor \log^{2/3} n \rfloor$.

The core is BMSSP$(l, B, S)$, a bounded multi-source shortest-path call. It gets a level $l$, a bound $B$, and a frontier $S$ of at most $2^{lt}$ vertices whose paths cover everything below $B$ that is still unfinished. It returns a new bound $B' \le B$ and the set $U$ of vertices below $B'$ whose shortest path passes through $S$, all finished.

```pseudo id=main
BMSSP-SSSP(G, w, s)
L1  d̂(s) ← 0; d̂(v) ← ∞ for v ≠ s
    BMSSP(l, B, S):
L2      if l = 0 then return BASECASE(B, S)        ▷ Dijkstra from the single x ∈ S, for k + 1 vertices
L3      (P, W) ← FINDPIVOTS(B, S)                  ▷ k Bellman-Ford rounds; P = roots of big trees
L4      D ← block structure with pull size 2^((l−1)t) and bound B; insert x with d̂(x) for x ∈ P
L5      U ← ∅; while |U| < k·2^(lt) and D is not empty do
L6          (B_i, S_i) ← PULL(D); remove from S_i the vertices already in U
L7          (B'_i, U_i) ← BMSSP(l − 1, B_i, S_i); U ← U ∪ U_i
L8          for each edge (u, v) with u ∈ U_i and d̂(u) + w(u, v) ≤ d̂(v) do d̂(v) ← d̂(u) + w(u, v)
L9              if B_i ≤ d̂(v) < B then INSERT(D, v, d̂(v)), else if B'_i ≤ d̂(v) < B_i then add v to K
L10         BATCHPREPEND(D, K ∪ {x ∈ S_i : B'_i ≤ d̂(x) < B_i})
L11     B' ← min(B'_i of the last call, B); return (B', U ∪ {x ∈ W : d̂(x) < B'})
L12 BMSSP(⌈log n / t⌉, ∞, {s}); return d̂
```

**FindPivots** (line L3) relaxes the edges out of the frontier $k$ times, each time from the vertices whose labels just changed to something below $B$; $W$ collects them. If $W$ grows beyond $k|S|$, it returns $P = S$. Otherwise it builds the forest of tight predecessor edges inside $W$ and returns the roots in $S$ whose trees have at least $k$ vertices, so $|P| \le |W| / k$. Every vertex below $B$ is then either finished and in $W$, or has a finished pivot on its shortest path.

**BaseCase** (line L2) runs Dijkstra's algorithm from the single vertex $x$, ignoring labels of $B$ or more, until $k + 1$ vertices are popped. If fewer are popped, it returns $B$ and all of them; otherwise it returns the key $B'$ of the last one and the $k$ before it.

**The structure $D$** (line L4) holds key-value pairs below $B$. INSERT keeps the smaller value for a key. BATCHPREPEND adds pairs whose values are below everything in $D$. PULL removes up to $M = 2^{(l-1)t}$ pairs of smallest value and returns them with a bound $B_i$ that separates them from the rest, or $B$ if $D$ is now empty. Lemma 3.3 of the paper builds it from blocks of size $M$, so that it never sorts more than it must.

**Partial execution.** A call stops early when $U$ has $k \cdot 2^{lt}$ vertices, and then returns $B' < B$. Its caller handles this in line L10: the frontier vertices between $B'_i$ and $B_i$, and the neighbours that landed there, go back into $D$ in front of everything else.

## Example

The vertices are $s, a, b, c, d, e$ and the edges $s \to a$ (1), $s \to b$ (4), $a \to b$ (2), $a \to c$ (6), $b \to c$ (1), $b \to d$ (5), $c \to d$ (1), $c \to e$ (3), $d \to e$ (1). The distances are $0, 1, 3, 4, 5, 6$, and the tree is the path $s, a, b, c, d, e$. With $n = 6$ the default parameters are $k = t = 1$; to show a partial execution we use $k = 2$, $t = 1$, so the top level is $\lceil \log_2 7 \rceil = 3$.

- **Level 3, $B = \infty$, $S = \{s\}$.** One Bellman-Ford round labels $a = 1$ and $b = 4$, and $|W| = 3 > k|S| = 2$, so $P = \{s\}$. $D$ has only $s$, the pull gives $S_1 = \{s\}$ with $B_1 = \infty$, and the call goes down to level 2, which does the same and calls level 1.
- **Level 1, $S = \{s\}$.** Again $P = \{s\}$, and the pull size is 1. BaseCase from $s$ pops $s$ (0), $a$ (1) and $b$ (3, through $a$), which is $k + 1 = 3$ vertices. On the way it also labels $c = 4$ and $d = 8$. It returns $B' = 3$ and $U = \{s, a\}$: a partial execution.
- Back at level 1, relaxing from $a$ gives $b = 3$ again, which lies in $[B'_1, B_1) = [3, \infty)$, so $b$ is batch-prepended. The next pull gives $\{b\}$, and BaseCase from $b$ pops $b$ (3), $c$ (4) and $d$ (5, through $c$), returning $B' = 5$ and $U = \{b, c\}$. Now $|U| = 4 = k \cdot 2^{1}$, so level 1 stops with $B' = 5$ and $U = \{s, a, b, c\}$.
- **Level 2.** Relaxing from $c$ gives $d = 5 \in [5, \infty)$, which is prepended. The next level-1 call starts from $\{d\}$. FindPivots finds $W = \{d, e\}$ with the tree $d \to e$ of size $2 \ge k$, so $P = \{d\}$. BaseCase pops only $d$ and $e$, which is not more than $k$, and returns $B' = \infty$. $D$ is now empty, so levels 2 and 3 return $B' = \infty$ with all six vertices.

The trace below is what the implementation records, one line per call as it returns.

| level | frontier | pivots | returned $B'$ | returned $U$ |
|---|---|---|---|---|
| 0 | $s$ | | 3 | $s, a$ |
| 0 | $b$ | | 5 | $b, c$ |
| 1 | $s$ | $s$ | 5 | $s, a, b, c$ |
| 0 | $d$ | | $\infty$ | $d, e$ |
| 1 | $d$ | $d$ | $\infty$ | $d, e$ |
| 2 | $s$ | $s$ | $\infty$ | all |
| 3 | $s$ | $s$ | $\infty$ | all |

**Unreachable vertices.** With extra vertices $x, y$ and edges $x \to y$, $y \to s$, no relaxation ever starts at $x$ or $y$, so both keep $\hat d = \infty$ and no parent.

**Negative weights.** With $b \to c$ ($-1$) the input is rejected before any work. So is the negative cycle $a \to b$ ($-3$), $b \to a$ (1). Negative weights need other methods, such as [Bellman-Ford](/bellman-ford/) or the [near-linear negative-weight algorithm](/near-linear-negative-sssp/).

## Correctness

**Theorem.** For nonnegative real weights, the top call terminates with $\hat d(v) = \delta(s, v)$ for every $v$, and $\hat d(v) = \infty$ exactly when $s$ does not reach $v$. This holds for any $k, t \ge 1$.

The proof is an induction on the level. A call is *proper* when its frontier is below $B$ and every unfinished vertex below $B$ has a finished frontier vertex on its shortest path. For a proper call, the claim is that the returned $U$ contains every vertex below $B'$ whose shortest path passes through the frontier, and that all of $U$ is finished.

- **BaseCase** is Dijkstra's algorithm from one finished vertex, so this is the usual argument for Dijkstra.
- **FindPivots.** If a vertex is fewer than $k$ steps past the last finished frontier vertex on its path, $k$ rounds of Bellman-Ford finish it. If not, the first $k$ steps form a chain of tight edges, which lies in a tree of at least $k + 1$ vertices. The root of that tree is finished, lies on the path, and is in $S$, so it is a pivot.
- **The loop** keeps an invariant: every unfinished vertex below $B$ has a finished vertex on its path that sits in $D$ with its exact distance as its value. The prepends in line L10 restore this for the vertices that a partial subcall left out, and this is what makes each subcall proper.
- **The top call.** It can never stop on the size limit, because $k \cdot 2^{lt} > n$, so it runs until $D$ is empty, and the invariant then says every reachable vertex is finished.

Termination follows because each subcall finishes at least one new vertex. The full proof is in the proof file below.

## Complexity

The model is the comparison-addition model: weights are real numbers that can only be added and compared, at unit cost (Pettie and Ramachandran). The page lists it under the [real RAM](/real-ram/).

- **Time.** The paper first makes every vertex have in-degree and out-degree at most 2, by replacing each vertex with a cycle of zero-weight edges; this keeps $m' = O(m)$ and $n' = O(m)$. On that graph the recursion has $\lceil \log n / t \rceil = O(\log^{1/3} n)$ levels. FindPivots costs $O(k)$ per vertex per level, which totals $O(\log^{2/3} n)$ per vertex. The block structure pays $O(\log(N/M))$, about $t$, for each INSERT, and less for prepended pairs. The paper's analysis (Section 3.4) shows that the total is $O(m \log^{2/3} n)$.
- **Against Dijkstra.** $O(m \log^{2/3} n)$ is below $O(m + n \log n)$ when $m = o(n \log^{1/3} n)$, for example on graphs of constant average degree. On dense graphs Dijkstra with a Fibonacci heap is still better.
- **Space.** Labels, predecessors, the sets of one recursion path and the structures $D$ take $O(m + n)$.
- **This implementation.** The Python version uses a binary heap with lazy deletion as $D$ and skips the degree reduction. So it has the algorithm's structure and correctness, but not its time bound; on small inputs it is slower than plain Dijkstra.

## Properties

- **Deterministic.** There is no randomness; the earlier sub-$n \log n$ results for real weights were for undirected graphs.
- **Does not sort.** The vertices are finished in bands, not one by one in distance order. This is what lets it go below the sorting bound for this problem, since sorting the distances is not required by the output.
- **Comparison-addition only.** It never uses integer tricks such as bucketing or word operations, unlike [Thorup's algorithm](/thorup-undirected-sssp/).
- **Directed graphs.** The bound holds for directed graphs, where earlier comparison-addition improvements did not apply.
- **Correct for any parameters.** The choice of $k$ and $t$ affects only time; any $k, t \ge 1$ gives correct distances.

## Variants and improvements

- **Parameters.** The analysis balances $k$, the Bellman-Ford depth, against $t$, the chunk size of the recursion. The values $\log^{1/3} n$ and $\log^{2/3} n$ give the bound; other values give correct but slower runs.
- **Constant degree.** The degree reduction is only for the analysis. An implementation can work on the original graph and keep correctness, as this one does.
- **The data structure.** The block list of Lemma 3.3 can be replaced by any structure with the same operations; a heap keeps correctness and loses the bound.

## When to use it

It is mainly of theoretical interest: it shows that directed SSSP with real weights does not need sorting time. In practice, Dijkstra's algorithm with a binary or pairing heap is simpler and has smaller constants for the graph sizes in use. With integer weights, bucket-based methods such as [Dial's algorithm](/dial-algorithm/) or a [radix heap](/radix-heap/) are often faster. Consider this algorithm when studying lower bounds and the structure of shortest-path computations, or for very large sparse graphs where the asymptotic gain might matter.

## Pitfalls

- **Ties.** The correctness argument assumes all path keys are different. With plain lengths, zero-weight edges create ties, and the tight-edge forest of FindPivots can contain cycles. Compare (length, edge count, vertex, predecessor) instead.
- **Strict versus non-strict relaxation.** Relaxations must use $\le$, not $<$. A vertex that is already finished must still be re-inserted when it is reached again with its exact distance, or a later call loses its cover vertex.
- **Forgetting the prepends.** After a partial subcall, the frontier vertices in $[B'_i, B_i)$ were pulled but not finished. If line L10 does not put them back, their subtrees are lost.
- **Pivots outside $S$.** Only roots that lie in $S$ may become pivots. A root outside $S$ is a vertex whose predecessor improved in the last round, and its label is not final.
- **Top level too low.** The top level must satisfy $k \cdot 2^{lt} > n$, or the top call can stop on its size limit before all vertices are finished.
- **Negative weights.** One negative edge breaks the cover argument; such input must be rejected, not passed through.

## Implementations

The Python version stores labels as tuples (length, edges, vertex, predecessor) and implements FindPivots, BaseCase and the recursive BMSSP as in the paper. $D$ is a binary heap with lazy deletion. Pulled vertices that the current call has already finished are dropped before the subcall; this changes nothing for correctness and keeps termination easy to prove. It returns distances and parents, and can record one line per call as in the example.

## History

Dijkstra's algorithm (1959) with Fibonacci heaps (Fredman and Tarjan 1987) gives $O(m + n \log n)$, and for a long time this was seen as the limit for real weights, because the algorithm outputs the vertices in sorted order. Thorup (1999) beat it for undirected graphs with integer weights on the word RAM, and Pettie and Ramachandran (2005) improved it for undirected real-weighted graphs in the comparison-addition model. Duan, Mao, Mao, Shu and Yin (STOC 2025) gave the first deterministic algorithm that beats sorting time for directed graphs with real weights, in $O(m \log^{2/3} n)$.

## References
