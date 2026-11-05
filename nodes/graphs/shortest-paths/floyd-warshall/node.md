---
tag: HSBPN7
kind: algorithm
slug: floyd-warshall
name: Floyd-Warshall algorithm
aliases:
- Roy-Floyd-Warshall algorithm
area: graphs/shortest-paths
level: intro
summary: Dynamic program over intermediate vertices computing all-pairs distances in O(n^3) time.
solves: [all-pairs-shortest-paths, negative-cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [all-pairs-shortest-paths, edge-relaxation, adjacency-matrix]
see_also: [warshall-algorithm, transitive-closure, johnson, bellman-ford, dijkstra, apsp-repeated-squaring, min-plus-matrix-multiplication, kleene-algebra]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.2, The Floyd-Warshall algorithm (the recurrence on intermediate vertices, the predecessor matrix, and transitive closure)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 9, All-Pairs Shortest Paths (the section on the Kleene-Roy-Floyd-Warshall algorithm)
  - paper: doi:10.1145/367766.368168
    title: Robert W. Floyd, Algorithm 97, Shortest path, Communications of the ACM 5(6), 345 (1962)
    locator: the whole one-page algorithm
  - paper: doi:10.1145/321105.321107
    title: Stephen Warshall, A theorem on Boolean matrices, Journal of the ACM 9(1), 11 to 12 (1962)
    locator: the whole paper (transitive closure of a Boolean matrix)
  - paper: doi:10.1016/j.ipl.2010.02.001
    title: Stefan Hougardy, The Floyd-Warshall algorithm on graphs with negative cycles, Information Processing Letters 110(8-9), 279 to 281 (2010)
    locator: the whole paper (the size of the numbers when a negative cycle exists)
  - url: https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    title: Wikipedia, Floyd-Warshall algorithm
    locator: section History and naming (Roy 1959, Warshall 1962, Floyd 1962, Ingerman 1962)
---

The Floyd-Warshall algorithm solves the [all-pairs shortest-path problem](/all-pairs-shortest-paths/) with a dynamic program over the set of vertices that a path may pass through. For $k = 1, 2, \ldots, n$ it lets the paths use vertex $k$ as a stop, and updates each pair $(i, j)$ with $D[i][j] \leftarrow \min(D[i][j], D[i][k] + D[k][j])$. It runs in $\Theta(n^3)$ time with $\Theta(n^2)$ space, allows **negative** weights, and detects a **negative cycle** by a negative entry on the diagonal. Its three short loops make it the usual choice for dense graphs with up to a few thousand vertices.

## In plain words

You want a table of the cheapest trip between every two towns. Start with the direct roads only.

Now pick one town, say town 1, and allow trips to change there. For every pair of towns, ask: is going from the first town to town 1, then from town 1 to the second town, cheaper than what the table says? If yes, write the cheaper cost. Then allow town 2 as well, and ask the same question for every pair. Go on until every town is allowed as a stop.

When town number k is added, the table already holds the best trips that stop only at the earlier towns. A best trip that also stops at town k is a best trip to town k followed by a best trip from town k, and both of those use only earlier stops. So one check per pair is enough.

## The problem

The input is a directed graph with vertices $1, \ldots, n$ and real weights $w(i, j)$ on its edges. The output is the matrix $D$ with $D[i][j] = \delta(i, j)$ for every ordered pair, and a matrix $\text{nxt}$ that gives, for each pair, the vertex after $i$ on a shortest path.

**Weight assumptions.** Weights are any real numbers; negative weights are allowed and they need not be integers. If the graph has a cycle of negative weight, the algorithm detects it: then some $D[i][i] < 0$ at the end, and the matrix holds no distances. If there is no negative cycle, all entries are correct, with $D[i][j] = \infty$ when $j$ is unreachable from $i$. Parallel edges keep the lightest one, and a self-loop of nonnegative weight has no effect.

## The algorithm

```pseudo id=main
FLOYD-WARSHALL(n, E)
L1  D ← the n × n matrix with D[i][i] = 0 and ∞ elsewhere, nxt[i][j] ← nil
L2  for each edge (u, v) with weight w in E do if w < D[u][v] then D[u][v] ← w, nxt[u][v] ← v
L3  for k ← 1 to n do
L4      for i ← 1 to n do
L5          for j ← 1 to n do
L6              if D[i][k] + D[k][j] < D[i][j] then
L7                  D[i][j] ← D[i][k] + D[k][j], nxt[i][j] ← nxt[i][k]
L8  return D, nxt
```

Let $D^{(k)}[i][j]$ be the least weight of a path from $i$ to $j$ whose inner vertices all lie in $\{1, \ldots, k\}$. Then $D^{(0)}$ is the matrix of lines L1 and L2, and

$$D^{(k)}[i][j] = \min\left(D^{(k-1)}[i][j],\; D^{(k-1)}[i][k] + D^{(k-1)}[k][j]\right),$$

because a best path either avoids $k$ or passes $k$ once and splits there into two paths with inner vertices below $k$. Pass $k$ of line L3 computes this layer. It updates one matrix in place instead of keeping $n + 1$ matrices: in pass $k$ the entries of row $k$ and column $k$ do not get smaller unless $D[k][k] < 0$, so reading a new value instead of an old one does no harm. Line L7 updates the next hop: a path through $k$ starts like the path from $i$ to $k$.

To read a path from $i$ to $j$, start at $i$ and follow $\text{nxt}[\cdot][j]$ until $j$. A row $i$ with $D[i][k] = \infty$ cannot change in pass $k$, so a program can skip it, which is fast on sparse graphs.

## Example

The vertices are $1, 2, 3, 4$ and the edges are $1 \to 2$ (3), $1 \to 3$ (8), $2 \to 4$ (1), $2 \to 3$ (4), $3 \to 2$ ($-2$), $4 \to 1$ (2), $4 \to 3$ (2). Row $i$ lists $D[i][1], \ldots, D[i][4]$.

| after | row 1 | row 2 | row 3 | row 4 |
|---|---|---|---|---|
| lines L1, L2 | 0 3 8 ∞ | ∞ 0 4 1 | ∞ −2 0 ∞ | 2 ∞ 2 0 |
| $k = 1$ | 0 3 8 ∞ | ∞ 0 4 1 | ∞ −2 0 ∞ | 2 **5** 2 0 |
| $k = 2$ | 0 3 **7** **4** | ∞ 0 4 1 | ∞ −2 0 **−1** | 2 5 2 0 |
| $k = 3$ | 0 3 7 4 | ∞ 0 4 1 | ∞ −2 0 −1 | 2 **0** 2 0 |
| $k = 4$ | 0 3 **6** 4 | **3** 0 **3** 1 | **1** −2 0 −1 | 2 0 2 0 |

The bold entries changed in that pass. For example, in pass $k = 4$, $D[1][3]$ falls from 7 to $D[1][4] + D[4][3] = 4 + 2 = 6$: the path $1 \to 2 \to 4 \to 3$. The diagonal stays 0, so there is no negative cycle. The cycle $2 \to 4 \to 3 \to 2$ has weight $1 + 2 - 2 = 1$. Following nxt from 3 to 1 gives $3 \to 2 \to 4 \to 1$, with weight $-2 + 1 + 2 = 1 = D[3][1]$.

**With a negative cycle.** Change the weight of $4 \to 3$ to $-5$. The cycle $2 \to 4 \to 3 \to 2$ now has weight $1 - 5 - 2 = -6$. At the end the diagonal has $D[2][2] = -6$, $D[3][3] = -6$ and $D[4][4] = -12$, so the algorithm reports a negative cycle. The value $-12$ is the weight of a closed walk that goes around the cycle twice. Vertex 1 is not on the cycle, and its entry $D[1][1]$ stays 0 in this run even though a negative closed walk passes through it.

## Correctness

**Theorem.** At the end of FLOYD-WARSHALL: (1) each finite $D[i][j]$ is the weight of a walk from $i$ to $j$; (2) $D[i][j] \le w(p)$ for each path $p$ from $i$ to $j$, and $D[i][i] \le w(C)$ for each cycle $C$ through $i$ that repeats no vertex. Hence, if no negative cycle exists, $D[i][j] = \delta(i, j)$ for all pairs and every $D[i][i] = 0$; and if a negative cycle exists, $D[i][i] < 0$ for each vertex $i$ of a negative cycle with no repeated vertex.

The key invariant is: after pass $k$, $D[i][j]$ is at most the weight of every path from $i$ to $j$ with inner vertices in $\{1, \ldots, k\}$, and it is the weight of some walk. Both parts survive the in-place update because entries only decrease. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/), with weights added and compared in $O(1)$ time.

- **Time.** Lines L1 and L2 take $\Theta(n^2 + m)$. The three loops of lines L3 to L5 run $n^3$ times, and each run of lines L6 and L7 is $O(1)$. The total is $\Theta(n^3)$ in every case, since $m \le n^2$ after keeping the lightest of parallel edges and the triple loop always runs in full. The skip of rows with $D[i][k] = \infty$ makes the best case faster in practice, but not in the worst case.
- **Space.** $D$ and nxt take $\Theta(n^2)$. Without paths, the in-place update needs only $D$.
- **Comparison with other methods.** [Dijkstra's algorithm](/dijkstra/) from each source takes $O(nm + n^2 \log n)$ with a Fibonacci heap, which is better when $m = o(n^2)$; with negative weights, [Johnson's algorithm](/johnson/) reweights first. [Repeated squaring](/apsp-repeated-squaring/) takes $\Theta(n^3 \log n)$. The best known bound for dense real weights is $n^3 / 2^{\Omega(\sqrt{\log n})}$, by Williams; see [all-pairs shortest paths](/all-pairs-shortest-paths/).

## Properties

- **Negative weights.** Allowed, and negative cycles are detected.
- **Dense input.** It reads an [adjacency matrix](/adjacency-matrix/) and does the same work for every graph with $n$ vertices.
- **Simple memory pattern.** For a fixed $k$, the inner loop scans row $i$ and row $k$ in order, which suits caches and vector units. Blocked versions do better still.
- **Semiring form.** The same loops compute the [transitive closure](/transitive-closure/) with (or, and) in place of (min, +); this is [Warshall's algorithm](/warshall-algorithm/). With other closed semirings they compute widest paths or a regular expression of all paths (the method of [Kleene's algebra](/kleene-algebra/)).

## Variants and improvements

- **Predecessor matrix.** CLRS keeps $\pi[i][j]$, the vertex before $j$, and updates it with $\pi[i][j] \leftarrow \pi[k][j]$. It is the mirror of the next-hop matrix.
- **[Transitive closure](/transitive-closure/).** Boolean version, $\Theta(n^3)$ bit operations, or $\Theta(n^3 / w)$ word operations with bit vectors.
- **[Widest path](/widest-path/).** Replace (min, +) by (max, min).
- **Finding a negative cycle.** When $D[i][i] < 0$, follow nxt from $i$ until a vertex repeats; the walk contains a negative cycle. The numbers can become very large: Hougardy shows that with negative cycles the entries can grow exponentially in $n$, so a program should stop as soon as some $D[i][i] < 0$.
- **Blocked Floyd-Warshall.** Process the matrix in tiles that fit in cache, for the same $\Theta(n^3)$ work.

## When to use it

Use Floyd-Warshall for all pairs on a dense graph, or on any graph of up to a few thousand vertices where the simplicity matters more than speed. It also fits when weights are negative and a negative cycle must be detected for all pairs at once. For a sparse graph with many vertices, run [Dijkstra](/dijkstra/) from each source, after a [Johnson](/johnson/) reweighting when some weight is negative. For a single source, it is far too slow.

## Pitfalls

- **The loop order.** The loop on $k$ must be the outermost one, as in line L3. With $k$ in the inner loop, as in `for i, for j, for k`, one pass does not compute $D^{(n)}$, and the result can be wrong.
- **Overflow with infinity.** With $\infty$ stored as a large integer, $D[i][k] + D[k][j]$ can overflow or look finite. Test both terms for $\infty$ first, or use a constant at most half the largest value; with negative weights, test explicitly.
- **Forgetting the diagonal.** Line L1 must set $D[i][i] = 0$. Without it, $D[i][i]$ ends as the lightest cycle through $i$, which is a different quantity (useful for the [shortest cycle](/shortest-cycle-problem/), but not the distance).
- **Trusting $D$ after a negative cycle.** If some $D[i][i] < 0$, the other entries are not distances, and which diagonal entries are negative can depend on details of the code, as the example shows for vertex 1.
- **The next-hop update.** Line L7 sets nxt$[i][j] \leftarrow$ nxt$[i][k]$, not $k$; setting it to $k$ records an inner vertex of the path, not the next one, and the simple path reader then jumps over edges. That matrix needs a recursive reader that splits the path at $k$.

## Implementations

The Python version skips row $i$ when $D[i][k] = \infty$, keeps the next-hop matrix, and has helpers to test for a negative cycle and to read a path.

## History

Bernard Roy published the algorithm in 1959. Stephen Warshall published the Boolean version for transitive closure in 1962, and Robert Floyd published the shortest-path version in the same year, as Algorithm 97 of the Communications of the ACM. Peter Ingerman wrote it in 1962 in the form of three nested loops. The idea of eliminating one vertex at a time also appears in Kleene's construction of a regular expression from an automaton in 1956.

## References
