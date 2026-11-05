---
tag: ER8HZE
kind: theorem
slug: dijkstra-correctness
name: Correctness of Dijkstra's algorithm
aliases:
- Dijkstra's greedy invariant
area: graphs/shortest-paths
level: core
summary: With nonnegative weights, a vertex extracted with minimum tentative distance has its final shortest-path distance.
prereqs: [dijkstra, edge-relaxation, upper-bound-property]
see_also: [dijkstra, shortest-path-optimal-substructure, greedy-algorithm, sorting-barrier, dial-algorithm, bidirectional-dijkstra, a-star-search, johnson]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.3, Dijkstra's algorithm (the correctness theorem with the loop invariant on the set S, and its corollary on the predecessor subgraph)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths, the section on Dijkstra's algorithm (the proof that each vertex is scanned once, with nonnegative weights)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 4.4, Dijkstra's algorithm (the alternative derivation by growing a known region)
  - paper: doi:10.1007/BF01386390
    title: Edsger W. Dijkstra, A note on two problems in connexion with graphs, Numerische Mathematik 1, 269 to 271 (1959)
    locator: Problem 2, the shortest path between two given nodes
---

## Statement

Let $G = (V, E)$ be a directed graph with a weight $w(u, v) \ge 0$ on each edge, and let $s \in V$. Run the following label-setting procedure: start with $d[s] = 0$, $d[v] = \infty$ for $v \ne s$, and $S = \emptyset$; while some vertex outside $S$ has a finite label, choose such a vertex $u$ with the least $d[u]$, add it to $S$, and [relax](/edge-relaxation/) every edge $(u, v)$.

**Theorem (Dijkstra's invariant).** Whenever a vertex $u$ is chosen, $d[u] = \delta(s, u)$. Consequently, when the procedure ends, $d[v] = \delta(s, v)$ for every vertex $v$, with $\delta(s, v) = +\infty$ exactly for the vertices that $s$ does not reach, and the vertices enter $S$ in nondecreasing order of distance.

**Weight assumptions.** Weights are real and nonnegative; zero weights are allowed and integers are not needed. With nonnegative weights there is no negative cycle. The theorem is false for graphs with a negative edge (see Tightness), even when they have no negative cycle.

## In plain words

Grow a set of places whose cheapest cost from the start is known. Every round, among the places not in the set, pick the one with the lowest cost found so far and add it.

The claim is that this cost is already the true cheapest one. Any cheaper route to it would have to leave the known set at some point. The first place outside the set on that route already has a cost at least as high as the place picked, since the picked one was the lowest. The rest of the route cannot make the total smaller, because no road has a negative length.

So each pick is final, and the places come out in order of their true distance.

## Proof

Write $S$ for the set at the moment $u$ is chosen. Two facts about relaxation are used.

- **Upper bound.** Every finite $d[v]$ is the weight of some walk from $s$ to $v$, so $d[v] \ge \delta(s, v)$ at all times; see the [upper-bound property](/upper-bound-property/). With nonnegative weights, $\delta(s, v)$ is a number $\ge 0$ or $+\infty$.
- **Labels of the frontier.** For $v \notin S$, $d[v] \le d[x] + w(x, v)$ for every edge $(x, v)$ with $x \in S$, because that edge was relaxed when $x$ entered $S$, and labels only decrease.

Use induction on the order in which vertices are chosen; assume $d[x] = \delta(s, x)$ for every $x \in S$, and that labels in $S$ no longer change (relaxing an edge into $x \in S$ cannot lower $d[x]$ below $\delta(s, x)$, and $d[x]$ already equals it).

Let $u$ be chosen. Its label is finite, so $u$ is reachable; take a shortest path $P = (s = p_0, p_1, \ldots, p_r = u)$, which exists since there is no negative cycle. Let $p_j$ be the first vertex of $P$ not in $S$.

- If $j = 0$, then $p_j = s \notin S$, so $S = \emptyset$, $u$ is the only vertex with a finite label, $u = s$, and $d[s] = 0 = \delta(s, s)$.
- If $j \ge 1$, then $p_{j-1} \in S$, and by the frontier fact and the induction hypothesis, $d[p_j] \le \delta(s, p_{j-1}) + w(p_{j-1}, p_j) = \delta(s, p_j)$, the last step because a prefix of a shortest path is a shortest path ([optimal substructure](/shortest-path-optimal-substructure/)).

The part of $P$ from $p_j$ to $u$ has nonnegative weight, **because every weight is nonnegative**, so $\delta(s, p_j) \le \delta(s, u)$. Since $u$ has the least label outside $S$,

$$d[u] \le d[p_j] \le \delta(s, p_j) \le \delta(s, u).$$

With the upper bound, $d[u] = \delta(s, u)$.

*Order.* If $u$ is chosen before $u'$, then at the time $u$ is chosen, $d[u] \le d[u']$ when $d[u']$ is finite, and later relaxations from vertices $x$ with $d[x] \ge d[u]$ can only give $u'$ a label $\ge d[u]$. By induction, every label outside $S$ stays $\ge d[u]$, so $\delta(s, u') = d[u'] \ge d[u] = \delta(s, u)$.

*End.* The procedure ends because each round adds a new vertex to $S$. At the end, no vertex outside $S$ has a finite label. If some $v \notin S$ were reachable, a path from $s$ to $v$ has a first vertex $y \notin S$; $y \ne s$ because $s$ always has a finite label until it is chosen, and the predecessor of $y$ on the path is in $S$, so $d[y] < \infty$ by the frontier fact. That is a contradiction. So the vertices outside $S$ are exactly the unreachable ones, with $d = \infty = \delta$. $\blacksquare$

The proof does not depend on how the minimum is found or how ties are broken, so it covers Dijkstra's algorithm with any [priority queue](/priority-queue/): a [binary heap](/binary-heap/) with lazy deletion, a [Fibonacci heap](/fibonacci-heap/), or the buckets of [Dial's algorithm](/dial-algorithm/). A proof for the heap version with line numbers is on the [Dijkstra](/dijkstra/) page.

## Consequences

- **Each vertex is scanned once.** A chosen vertex is final, so its edges need to be relaxed only once. This gives the $O(m + n \log n)$ bound with a Fibonacci heap.
- **Early exit for one target.** A search for a single target $t$ can stop as soon as $t$ is chosen. [Bidirectional Dijkstra](/bidirectional-dijkstra/) uses the invariant on both sides.
- **Monotone queues suffice.** The chosen labels never decrease, so priority queues that only support a nondecreasing minimum, such as buckets and [radix heaps](/radix-heap/), are enough.
- **Order of distances.** The vertices come out sorted by distance. For algorithms that compare labels, this links shortest paths to sorting; see the [sorting barrier](/sorting-barrier/).
- **A\* search.** With a consistent heuristic $h$, the reduced weights $w(u, v) - h(u) + h(v)$ are nonnegative, and [A\* search](/a-star-search/) is Dijkstra on them, so the theorem applies.
- **Negative weights after reweighting.** [Johnson's algorithm](/johnson/) uses Bellman-Ford to find potentials that make all reduced weights nonnegative, and then applies Dijkstra; correctness follows from this theorem.

## Tightness

The hypothesis $w \ge 0$ cannot be dropped, even when there is no negative cycle. Take the edges $s \to a$ (2), $a \to c$ (1), $s \to b$ (4), $b \to a$ ($-3$). The procedure chooses $s$ (0), then $a$ (2), then $c$ (3), then $b$ (4); relaxing $b \to a$ lowers $d[a]$ to 1 only after $a$ was chosen, so $c$ keeps $d[c] = 3$, while $\delta(s, c) = 4 - 3 + 1 = 2$. The failing step is $\delta(s, p_j) \le \delta(s, u)$: for $u = c$, the first vertex of the shortest path $s, b, a, c$ outside $S$ is $b$, with $\delta(s, b) = 4 > 2$.

With a negative cycle reachable from $s$, distances are $-\infty$ and no label-setting rule can be correct.

The hypothesis can be weakened a little. If every negative edge leaves $s$, the theorem still holds: a shortest path is simple, so its part after $p_j$ with $j \ge 1$ contains no edge out of $s$, and the step $\delta(s, p_j) \le \delta(s, u)$ remains true. Zero weights are fine, as the proof uses only $w \ge 0$. If chosen vertices may be put back when their label drops, the procedure becomes label-correcting and handles negative edges without negative cycles, but then a vertex can be chosen many times and the running time can be exponential.

## History

Dijkstra (1959) gave the algorithm with the argument that the node with the least tentative distance has its final distance. Textbooks state it as a loop invariant on the set $S$: CLRS proves it in Section 22.3 together with the predecessor tree, and Erickson presents it as the observation that with nonnegative weights each vertex is scanned once.

## References
