---
tag: 9CK9Y1
kind: problem
slug: maximum-acyclic-subgraph
name: Maximum acyclic subgraph
aliases:
- Acyclic subgraph
- maximum acyclic subgraph problem
area: graphs/paths-and-cycles
level: core
summary: Find a largest set of arcs of a directed graph that contains no directed cycle; the complement of a minimum feedback arc set, and NP-hard.
prereqs: [directed-graph, directed-acyclic-graph, topological-ordering, np-hard]
see_also: [feedback-arc-set-problem, feedback-vertex-set-problem, topological-ordering-theorem, topological-sort, karps-21-np-complete-problems, bitmask-dp, unique-games-conjecture, cycle-detection]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, the problems FEEDBACK NODE SET and FEEDBACK ARC SET and their reductions from VERTEX COVER
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.1, problem GT8 (feedback arc set), with its comments on special cases
  - paper: Venkatesan Guruswami, Rajsekar Manokaran and Prasad Raghavendra, Beating the random ordering is hard, Inapproximability of maximum acyclic subgraph, Proceedings of the 49th IEEE Symposium on Foundations of Computer Science (FOCS), 2008
    title: Guruswami, Manokaran and Raghavendra, the hardness of approximating maximum acyclic subgraph under the Unique Games Conjecture
    locator: the main theorem (no ratio 1/2 + ε in polynomial time under the Unique Games Conjecture)
  - paper: doi:10.1016/0020-0190(93)90079-O
    title: Peter Eades, Xuemin Lin and W. F. Smyth, A fast and effective heuristic for the feedback arc set problem, Information Processing Letters 47(6), 319 to 323 (1993)
    locator: the whole paper (the greedy heuristic and its bound for graphs without 2-cycles)
  - paper: Bonnie Berger and Peter W. Shor, Approximation algorithms for the maximum acyclic subgraph problem, Proceedings of the First Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1990
    title: Berger and Shor, approximation algorithms for maximum acyclic subgraph
    locator: the main theorem (a ratio above 1/2 that depends on the maximum degree)
  - paper: Noga Alon, Ranking tournaments, SIAM Journal on Discrete Mathematics 20(1), 2006
    title: Noga Alon, Ranking tournaments, SIAM Journal on Discrete Mathematics 20(1), 137 to 142 (2006)
    locator: the main theorem (minimum feedback arc set in tournaments is NP-hard)
---

The maximum acyclic subgraph problem asks, for a [directed graph](/directed-graph/) $G = (V, A)$, for a largest set of arcs $B \subseteq A$ such that $(V, B)$ has no directed cycle. Its complement $A \setminus B$ is a minimum [feedback arc set](/feedback-arc-set-problem/), so the two problems have the same optimal solutions and differ only in what they count. An arc set is acyclic exactly when some order of the vertices puts every arc of it forward, so the problem is also "order the vertices to make as many arcs as possible point forward". The problem is [NP-hard](/np-hard/), half of the arcs is always easy to get, and under the [Unique Games Conjecture](/unique-games-conjecture/) no polynomial-time algorithm guarantees more than that fraction.

## In plain words

You have a set of rules of the form "this item comes before that item", and the rules contradict each other: some of them form loops. You want to keep as many rules as you can and drop the rest, so that the kept rules have no loop. Then some order of the items obeys every kept rule.

Another view: put the items in a row. Each rule now points forward or backward. Count the rules that point forward. The best row gives the answer.

Getting half of the rules is easy. Take any row. If fewer than half of the rules point forward, reverse the row. Getting the exact best is hard: no fast method is known for large inputs.

## Definition

**Input.** A finite directed graph $G = (V, A)$ with $n = |V|$ and $m = |A|$. Parallel arcs are allowed and count separately; self-loops are allowed. In the weighted version, each arc $a$ has a weight $w(a) \ge 0$.

**Output.** A set $B \subseteq A$ such that the graph $(V, B)$ is a [directed acyclic graph](/directed-acyclic-graph/), of maximum size $|B|$ (or of maximum weight $w(B) = \sum_{a \in B} w(a)$).

**Ordering form.** For a bijection $\pi : V \to \{1, \ldots, n\}$, call an arc $(u, v)$ *forward* if $\pi(u) < \pi(v)$. Let $F(\pi)$ be the set of forward arcs. Then

$$\mathrm{MAS}(G) = \max_{B \subseteq A,\ (V, B) \text{ acyclic}} |B| = \max_{\pi} |F(\pi)|.$$

*Proof.* $F(\pi)$ is acyclic: along a directed cycle of forward arcs, $\pi$ would increase at each step and return to its start value, which is impossible. So the right side is at most the left side. Conversely, if $(V, B)$ is acyclic, it has a [topological ordering](/topological-ordering/) $\pi$ by the [topological ordering theorem](/topological-ordering-theorem/), and every arc of $B$ is forward in $\pi$, so $|B| \le |F(\pi)|$. $\square$

The same proof works with weights. A self-loop $(v, v)$ is a cycle by itself, so it is never in $B$ and never forward. Two antiparallel arcs $(u, v)$ and $(v, u)$ form a cycle of length 2, and exactly one of them is forward in each order.

**Decision version.** Given $G$ and an integer $k$, is there an acyclic $B \subseteq A$ with $|B| \ge k$? It is the same as asking whether a feedback arc set of size at most $m - k$ exists.

## Variants

- **Minimum feedback arc set.** Minimize $|A \setminus B|$ instead. The exact problems are equivalent, but approximation ratios do not carry over: a ratio near 1 for one can be a poor ratio for the other. See [feedback arc set problem](/feedback-arc-set-problem/).
- **Weighted version.** Maximize $w(B)$. On the complete directed graph with a weight on each ordered pair, this is the *linear ordering problem* of operations research.
- **Tournaments.** The input has exactly one arc between each pair of distinct vertices. This is the problem of ranking players from the results of a round-robin, with the fewest upsets. It is still NP-hard (see Bounds).
- **Undirected graphs.** The analogue for an undirected graph asks for a largest forest. It is solved by any [spanning forest](/spanning-forest/): every spanning forest of a graph with $c$ connected components has $n - c$ edges. So the problem is only interesting for directed graphs.
- **Acyclic induced subgraph.** Keep vertices instead of arcs: find a largest $S \subseteq V$ such that $G[S]$ is acyclic. Its complement is a minimum [feedback vertex set](/feedback-vertex-set-problem/).

## Examples

**A small graph.** Take $V = \{0, 1, 2, 3, 4\}$ and the 8 arcs

$$0 \to 1,\ 1 \to 2,\ 2 \to 0,\ 2 \to 3,\ 3 \to 4,\ 4 \to 2,\ 1 \to 3,\ 4 \to 1.$$

The cycles $0 \to 1 \to 2 \to 0$ and $2 \to 3 \to 4 \to 2$ share no arc, and each must lose at least one arc. So $\mathrm{MAS}(G) \le 6$. The order $0, 4, 1, 2, 3$ makes 6 arcs forward and only $2 \to 0$ and $3 \to 4$ backward. So $\mathrm{MAS}(G) = 6$, and $\{2 \to 0, 3 \to 4\}$ is a minimum feedback arc set. Of the $5! = 120$ orders, exactly 5 reach 6 forward arcs. The order $0, 1, 2, 3, 4$ gives only 5 forward arcs; its reverse gives 3.

**The bound one half is tight.** In the complete symmetric directed graph on $n$ vertices, each pair $u \ne v$ has both arcs $(u, v)$ and $(v, u)$, so $m = n(n-1)$. Each order makes exactly one arc of each pair forward, so every order gives $n(n-1)/2 = m/2$. For $n = 4$, $m = 12$ and $\mathrm{MAS} = 6$.

**Acyclic input.** If $G$ is already a directed acyclic graph, $\mathrm{MAS}(G) = m$, and a [topological sort](/topological-sort/) finds an order with all arcs forward in $O(n + m)$ time.

**Self-loops and isolated vertices.** A graph with one vertex and one self-loop has $\mathrm{MAS} = 0$. Isolated vertices change nothing: they can go anywhere in the order.

## Known algorithms

- **Linear time for acyclic graphs.** Check acyclicity with a [topological sort](/topological-sort/) or [cycle detection](/cycle-detection/); if no cycle exists, keep all arcs.
- **Strongly connected components first.** Each arc between two different [strongly connected components](/strongly-connected-components/) lies on no cycle, so it is kept in every optimal solution. The problem splits into one independent instance for each component.
- **Exact dynamic program over subsets.** Let $f(S)$ be the most forward arcs among the vertices of $S$ when $S$ is placed first, in the best order. Then $f(\emptyset) = 0$ and
  $$f(S) = \max_{v \in S} \big( f(S \setminus \{v\}) + |\{(u, v) \in A : u \in S \setminus \{v\}\}| \big),$$
  where $v$ is the last vertex of $S$. The answer is $f(V)$. This takes $O(2^n n^2)$ time with arc counts by adjacency matrix, or $O(2^n n)$ with bit masks and a population count, and $\Theta(2^n)$ space. It is a [bitmask dynamic program](/bitmask-dp/) of the same shape as the [Held-Karp algorithm](/held-karp-algorithm/).
- **The trivial one-half approximation.** Take any order $\pi$ and its reverse. Each non-loop arc is forward in exactly one of them, so the better of the two keeps at least $(m - \ell)/2$ arcs, where $\ell$ is the number of self-loops. Since $\mathrm{MAS}(G) \le m - \ell$, this is a $\tfrac{1}{2}$-approximation in $O(n + m)$ time.
- **Greedy heuristic of Eades, Lin and Smyth (1993).** Repeatedly remove sinks to the back of the order and sources to the front; when neither exists, move the vertex with the largest out-degree minus in-degree to the front. It runs in $O(m)$ time. For a simple connected directed graph without 2-cycles it keeps at least $m/2 + n/6$ arcs.
- **Berger and Shor (1990).** A randomized method keeps at least $(\tfrac{1}{2} + \Omega(1/\sqrt{\Delta}))\,m$ arcs on graphs without 2-cycles, where $\Delta$ is the maximum degree.
- **Branch and bound and integer programming.** In practice, exact solvers use the linear ordering polytope or cycle inequalities, which separate on violated cycles.

## Bounds

- **NP-hardness.** The decision version of feedback arc set is one of Karp's 21 NP-complete problems (1972), by a reduction from vertex cover. So the decision version of maximum acyclic subgraph is NP-complete: it is in NP because an order $\pi$ with at least $k$ forward arcs is a certificate checkable in $O(n + m)$ time.
- **Tournaments.** The problem stays NP-hard on tournaments. Alon proved this in 2006.
- **Approximation.** The ratio $\tfrac{1}{2}$ is reached by the trivial method above. Guruswami, Manokaran and Raghavendra (2008) proved that, if the [Unique Games Conjecture](/unique-games-conjecture/) holds, no polynomial-time algorithm reaches a ratio $\tfrac{1}{2} + \varepsilon$ for any fixed $\varepsilon > 0$. So under that conjecture the trivial bound is best possible. The complementary feedback arc set problem behaves differently: its best known ratio grows with $n$, and it is not known to be constant.
- **Exact exponential time.** The dynamic program above runs in $O^*(2^n)$ time.

## Reductions

- **To and from feedback arc set.** $B$ is acyclic if and only if $A \setminus B$ meets every directed cycle. So $\mathrm{MAS}(G) = m - \mathrm{FAS}(G)$, with the same optimal solutions, in $O(1)$ extra time.
- **From vertex cover.** Karp's reduction builds, from an undirected graph $H$, a directed graph with two vertices $v_{\text{in}}, v_{\text{out}}$ and an arc $v_{\text{in}} \to v_{\text{out}}$ for each vertex $v$ of $H$, and arcs $u_{\text{out}} \to v_{\text{in}}$ and $v_{\text{out}} \to u_{\text{in}}$ for each edge $\{u, v\}$. Each cycle uses an arc $v_{\text{in}} \to v_{\text{out}}$, and $H$ has a vertex cover of size $k$ if and only if the directed graph has a feedback arc set of size $k$.
- **To the linear ordering problem.** Set the weight of the ordered pair $(u, v)$ to the number of arcs from $u$ to $v$. A best linear order is a best order for maximum acyclic subgraph.

## Applications

- **Ranking.** From pairwise results (games, votes, user preferences), find the order of the items that disagrees with the fewest results. On a tournament this is the minimum number of upsets.
- **Layered graph drawing.** The first step of the Sugiyama method for drawing a directed graph in layers reverses the arcs of a small feedback arc set, so that all arcs can point down.
- **Breaking cycles before scheduling.** A dependency graph with conflicting constraints becomes schedulable after the dropped arcs are removed; then a [topological sort](/topological-sort/) gives the schedule.
- **Economics.** Triangulation of input-output tables, which orders the sectors of an economy to put the most weight above the diagonal, is the weighted linear ordering problem.

## References
