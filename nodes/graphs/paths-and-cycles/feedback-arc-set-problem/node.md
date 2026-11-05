---
tag: VKCSD3
kind: problem
slug: feedback-arc-set-problem
name: Feedback arc set problem
aliases:
- minimum feedback arc set
area: graphs/paths-and-cycles
level: advanced
summary: Find a smallest set of arcs whose removal makes a directed graph acyclic. NP-hard, also on tournaments; exact in O(2^n n^2) time by a subset DP.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: O(2^n n^2)}
prereqs: [directed-graph, directed-acyclic-graph, topological-sort, np-hard]
see_also: [feedback-vertex-set-problem, directed-feedback-vertex-set, vertex-cover, cycle-detection, dfs-cycle-detection, bitmask-dp, unique-games-conjecture, ptas]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 85 to 103 (1972)
    locator: the list of 21 problems (feedback arc set, reduced from vertex cover)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman (1979)
    locator: Appendix A1.1, problem GT8 (feedback arc set) and its comments
  - paper: "Guy Even, Joseph Naor, Baruch Schieber and Madhu Sudan, Approximating minimum feedback sets and multicuts in directed graphs, Algorithmica 20(2), 151 to 174 (1998)"
    locator: the whole paper (an O(log n log log n) approximation for weighted feedback arc and vertex sets)
  - paper: "Venkatesan Guruswami, Rajsekar Manokaran and Prasad Raghavendra, Beating the random ordering is hard, inapproximability of maximum acyclic subgraph, Proceedings of the 49th IEEE Symposium on Foundations of Computer Science (FOCS), 573 to 582 (2008)"
    locator: the main theorem and its corollary for feedback arc set under the Unique Games Conjecture
  - paper: "Noga Alon, Ranking tournaments, SIAM Journal on Discrete Mathematics 20(1), 137 to 142 (2006)"
    locator: the whole paper (feedback arc set is NP-hard on tournaments)
  - paper: "Claire Kenyon-Mathieu and Warren Schudy, How to rank with few errors, Proceedings of the 39th ACM Symposium on Theory of Computing (STOC), 95 to 103 (2007)"
    locator: the whole paper (a PTAS for feedback arc set in tournaments)
  - paper: "C. L. Lucchesi and D. H. Younger, A minimax theorem for directed graphs, Journal of the London Mathematical Society (2) 17, 369 to 374 (1978)"
    locator: the main theorem (with planar duality it makes the planar case polynomial)
---

The feedback arc set problem asks for a smallest set of arcs whose removal leaves a [directed graph](/directed-graph/) with no directed cycle. An equivalent form asks for an order of the vertices with the fewest arcs that point backwards. The problem is [NP-hard](/np-hard/), one of [Karp's 21 problems](/karps-21-np-complete-problems/), and it stays NP-hard on tournaments. It can be solved exactly in $O(2^n n^2)$ time by [dynamic programming over subsets](/bitmask-dp/), and the best known polynomial approximation ratio is $O(\log n \log \log n)$.

## In plain words

Some tasks must be done before others, and the rules are given as arrows from one task to another. If the arrows go round in a circle, no order of the tasks can follow all the rules. The question is: what is the smallest number of rules to drop so that an order exists?

The same question in other words: put the tasks in a line so that as few arrows as possible point backwards. The arrows that point backwards are the rules to drop. Trying every line works only for a few tasks, and no fast method is known that always finds the best answer.

## Definition

**Input.** A finite directed graph $G = (V, A)$ with $n$ vertices and $m$ arcs. Parallel arcs and [self-loops](/self-loop/) are allowed, so $G$ may be a [multigraph](/multigraph/). In the weighted form each arc $a$ has a weight $w(a) \ge 0$.

**Output.** A set $F \subseteq A$ such that $G - F$ is a [directed acyclic graph](/directed-acyclic-graph/), with $|F|$ (or $w(F)$) as small as possible. The minimum is written $\tau'(G)$ here.

**Decision form.** Given $G$ and $k$, is there a feedback arc set with at most $k$ arcs? This is NP-complete.

**Conventions.** A self-loop is a cycle of length 1, so every self-loop is in every feedback arc set. Parallel arcs count separately: if $p$ arcs go from $u$ to $v$ and the order puts $v$ before $u$, all $p$ are removed. A pair of opposite arcs $u \to v$, $v \to u$ is a cycle of length 2. Isolated vertices change nothing.

**The ordering form.** For an order $\pi$ of $V$, call an arc $u \to v$ backward if $v$ comes before $u$ or $u = v$. Then

$$\tau'(G) = \min_{\pi} \bigl|\{\text{backward arcs of } \pi\}\bigr|.$$

*Proof.* The backward arcs of any order form a feedback arc set, because the other arcs all go forward and a cycle of forward arcs cannot return to its start. Conversely, if $G - F$ is acyclic, a [topological order](/topological-sort/) of $G - F$ has all arcs of $G - F$ forward, so its backward arcs lie in $F$. $\square$

Thus a minimum feedback arc set is the complement of a maximum acyclic subgraph, and both problems have the same exact solutions but different approximation behaviour.

## Variants

- **Weighted.** Minimise $w(F)$; a weight $p$ is the same as $p$ parallel arcs.
- **Maximum acyclic subgraph.** Maximise the number of arcs kept. Either a random order or the better of an order and its reverse keeps at least half of the non-loop arcs, so this is a 1/2 approximation.
- **Tournaments.** Every pair of vertices has exactly one arc between them. This is the ranking problem: order players to disagree with as few game results as possible.
- **Undirected graphs.** The smallest set of edges whose removal leaves a forest has exactly $m - n + c$ edges, where $c$ is the number of components, the dimension of the [cycle space](/cycle-basis/). Deleting the edges outside a spanning forest achieves it, so the undirected case is easy.
- **Vertex version.** Remove vertices instead of arcs: the [feedback vertex set problem](/feedback-vertex-set-problem/), and for directed graphs the [directed feedback vertex set](/directed-feedback-vertex-set/).

## Examples

**Three cycles through one vertex.** Take vertices $0, \ldots, 4$ and the arcs $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $3 \to 1$, $3 \to 4$, $4 \to 2$. The directed cycles $0, 1, 2$ and $2, 3, 4$ share no arc, so $\tau' \ge 2$. Removing $1 \to 2$ and $2 \to 3$ breaks all three cycles, the third being $1, 2, 3$, so $\tau' = 2$. The order $2, 0, 1, 3, 4$ has exactly these two arcs backward. A single vertex, $2$, meets every cycle, so the vertex version has answer 1.

**Acyclic input.** If $G$ is a DAG, $\tau'(G) = 0$, and [cycle detection](/cycle-detection/) confirms it in $O(n + m)$ time.

**Self-loops and 2-cycles.** The graph with arcs $0 \to 0$, $0 \to 1$, $1 \to 0$, $1 \to 0$ has $\tau' = 2$: the loop, and the single arc $0 \to 1$, which is cheaper than the two parallel arcs $1 \to 0$.

**Tournaments.** The cyclic triangle needs one arc. Exhaustive search over all tournaments shows that the largest minimum feedback arc set has 1, 1, 3, 4 arcs for $n = 3, 4, 5, 6$.

## Known algorithms

| algorithm | input | guarantee | time |
|---|---|---|---|
| subset dynamic programming | general | exact | $O(2^n n^2)$ |
| better of an order and its reverse | general | at most $(m - \ell)/2 + \ell$ arcs, $\ell$ the number of loops | $O(n + m)$ |
| Even, Naor, Schieber and Sudan (1998) | weighted | ratio $O(\log n \log \log n)$ | polynomial |
| via directed feedback vertex set | general | FPT in the answer $k$ | $f(k) \cdot n^{O(1)}$ |
| Lucchesi and Younger with planar duality | planar | exact | polynomial |
| Kenyon-Mathieu and Schudy (2007) | tournaments | PTAS | polynomial for fixed $\varepsilon$ |

**Subset dynamic programming.** Let $f(S)$ be the fewest backward arcs in an order of the vertex set $S$, counting only arcs inside $S$. In the best order of $S$, some vertex $v$ comes last, and its backward arcs are those from $v$ into $S \setminus \{v\}$. So

$$f(\emptyset) = 0, \qquad f(S) = \min_{v \in S} \Bigl( f(S \setminus \{v\}) + \bigl|\{\, v \to u : u \in S \setminus \{v\} \,\}\bigr| \Bigr),$$

and $\tau'(G) = f(V) + \ell$. There are $2^n$ sets and $n$ choices of $v$, and the count takes $O(n)$ with an $n \times n$ table of arc multiplicities, which gives $O(2^n n^2)$ time and $O(2^n)$ space after $O(n^2 + m)$ preprocessing. This is the same scheme as the [Held-Karp algorithm](/held-karp-algorithm/). Tested against brute force over all arc subsets on 600 random multigraphs with up to 5 vertices and 7 arcs, with loops and parallel arcs, it gave the same value every time.

**Splitting into components.** Every cycle lies inside one [strongly connected component](/strongly-connected-components/), so the problem splits into one instance per component, and arcs between components are never needed in $F$.

## Bounds

**NP-hardness.** Karp (1972) showed that the decision problem is NP-complete, by a reduction from [vertex cover](/vertex-cover/); see Reductions. Garey and Johnson list it as GT8.

**Tournaments.** Alon (2006) proved that the problem stays NP-hard on tournaments; Charbit, Thomassé and Yeo found a proof at about the same time.

**Approximation hardness.** The reduction below preserves the size of the solution, so any lower bound on the [approximation ratio](/approximation-ratio/) of vertex cover holds for feedback arc set; for example, there is no ratio better than 1.36 unless P = NP. Guruswami, Manokaran and Raghavendra (2008) proved that, under the [Unique Games Conjecture](/unique-games-conjecture/), no polynomial algorithm beats the 1/2 ratio for maximum acyclic subgraph, and that feedback arc set has no constant ratio at all.

**Upper bounds.** Every graph has $\tau'(G) \le (m - \ell)/2 + \ell$, since an order or its reverse has at most half of the non-loop arcs backward. The gap between the $O(\log n \log \log n)$ ratio and the constant lower bounds is open.

## Reductions

**From vertex cover.** Let $H$ be an undirected graph. Build a directed graph $D$: each vertex $v$ of $H$ becomes two vertices $v_{\text{in}}$ and $v_{\text{out}}$ with one arc $v_{\text{in}} \to v_{\text{out}}$, and each edge $uv$ of $H$ becomes arcs $u_{\text{out}} \to v_{\text{in}}$ and $v_{\text{out}} \to u_{\text{in}}$, each repeated $n + 1$ times (or given weight $n + 1$). Then $\tau'(D)$ equals the size of a minimum vertex cover of $H$.

*Proof.* A vertex cover $C$ gives $F = \{ v_{\text{in}} \to v_{\text{out}} : v \in C \}$. Every cycle of $D$ follows a closed walk of $H$ with at least one edge $uv$, so it passes through both $u_{\text{in}} \to u_{\text{out}}$ and $v_{\text{in}} \to v_{\text{out}}$, and one of $u, v$ is in $C$. Conversely, a feedback arc set of size at most $n$ uses no heavy arc, since one copy of a group of $n + 1$ does not help; so it consists of arcs $v_{\text{in}} \to v_{\text{out}}$, and for each edge $uv$ it must break the cycle $u_{\text{in}}, u_{\text{out}}, v_{\text{in}}, v_{\text{out}}$, so the corresponding vertices cover $H$. $\square$

The reduction was checked by brute force on 500 random graphs with up to 5 vertices.

**To directed feedback vertex set.** Replace each arc $u \to v$ by $u \to x_{uv} \to v$ with a new vertex $x_{uv}$, and make each original vertex expensive, for example by $m + 1$ copies with the same arcs. Then a feedback vertex set of size at most $m$ uses only new vertices, and these correspond to arcs. So the two problems are equivalent under such reductions.

**Ordering problems.** In the ordering form, the problem is the linear ordering problem with a 0/1 weight matrix, and Kemeny rank aggregation is a weighted feedback arc set problem on a complete directed graph.

## Applications

- **Layered drawing of directed graphs.** The Sugiyama method first reverses a small set of arcs so that the graph becomes acyclic and can be drawn with all arcs pointing down.
- **Ranking.** Order teams or items from pairwise comparisons with as few upsets as possible.
- **Circuits and scheduling.** Break feedback loops in sequential circuits for testing, or break cyclic dependencies in a schedule or a build.
- **[Deadlock](/deadlock/) resolution.** Choose a few wait relations to cancel so that the wait-for graph becomes acyclic.

## References
