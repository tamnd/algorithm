---
tag: 5JW6R2
kind: problem
slug: flow-decomposition
name: Flow decomposition
aliases:
- path and cycle decomposition of a flow
area: graphs/flows-and-cuts
level: intro
summary: Write a flow as a sum of s-t paths and cycles carrying the flow values.
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m)}
prereqs: [s-t-flow, flow-conservation]
see_also: [edge-disjoint-paths, vertex-disjoint-paths, flow-integrality-theorem, ford-fulkerson, multi-commodity-flow-problem, min-cost-flow-problem, circulation-problem]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 3, Section 3.5, Flow decomposition algorithms (the flow decomposition theorem, the bound of n + m paths and cycles, and the O(nm) algorithm)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (flow decompositions) and Chapter 11, Applications of Flows and Cuts (edge-disjoint paths from an integer flow)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.6, Disjoint Paths in Directed and Undirected Graphs (an integer flow of value k gives k edge-disjoint paths)
---

Flow decomposition is the problem of writing a given [s-t flow](/s-t-flow/) as a sum of flows along paths from $s$ to $t$ and around cycles, each with a positive weight. Every flow has such a decomposition with at most $m$ parts, where $m$ is the number of edges with positive flow, and a simple greedy method finds one in $O(nm)$ time. Asking for the fewest parts is NP-hard. The decomposition turns an abstract flow into the routes that carry it, which is how a maximum flow becomes a set of [edge-disjoint paths](/edge-disjoint-paths/).

## In plain words

A flow says only how much goes along each edge. Often you want routes instead: "send 4 units along this route, 6 along that one". Flow decomposition turns the edge amounts back into routes.

The method is greedy. Start at the source and follow edges that still carry flow until you reach the sink. Take the smallest amount on the route, record the route with that amount, and subtract it from each edge on the route. At least one edge drops to nothing. If the walk comes back to a place it has already visited, you found a loop instead of a route; record and subtract it in the same way. Repeat until no flow is left. Each round empties an edge, so the number of rounds is at most the number of edges.

## Definition

**Input.** A [flow network](/flow-network/) $N = (G, c, s, t)$ with $G = (V, E)$ directed, and an s-t flow $f$ on it with $|f| \ge 0$. Capacities and flow values are nonnegative reals; when they are integers, the output weights are integers too. Antiparallel edges are separate edges, each with its own value $f(e)$; the decomposition may put a cycle of two edges on an antiparallel pair.

**Output.** A list of s-t paths $P_1, \ldots, P_p$ (each a simple path from $s$ to $t$ in $G$), a list of directed cycles $C_1, \ldots, C_q$ in $G$, and weights $\alpha_i > 0$, $\beta_j > 0$, such that for each edge $e$

$$f(e) = \sum_{i : e \in P_i} \alpha_i + \sum_{j : e \in C_j} \beta_j,$$

and then $|f| = \sum_i \alpha_i$, because each path adds its weight to the net flow out of $s$ and each cycle adds 0.

**Theorem (flow decomposition).** Every s-t flow $f$ with $|f| \ge 0$ has such a decomposition with $p + q \le |E^{+}|$, where $E^{+} = \{e : f(e) > 0\}$. If $f$ is integral, the weights can be chosen to be integers.

*Proof.* By induction on $|E^+|$. If $E^+ = \emptyset$, the empty lists work. Otherwise:

1. *Find a path or a cycle.* Walk along edges of $E^+$. If $|f| > 0$, start at $s$: then $f^{\text{out}}(s) = f^{\text{in}}(s) + |f| > 0$, and at each other vertex $v \ne t$ that the walk enters, $f^{\text{in}}(v) > 0$, so $f^{\text{out}}(v) > 0$ by conservation. So the walk can always go on until it reaches $t$ or repeats a vertex. If it reaches $t$ first, it is a simple s-t path; if it repeats a vertex, the part between the two visits is a cycle. If $|f| = 0$, conservation holds at every vertex, $s$ and $t$ included, so a walk from the tail of any edge of $E^+$ never gets stuck and must repeat a vertex: it gives a cycle.
2. *Subtract.* Let $X$ be the path or cycle found and $\gamma = \min_{e \in X} f(e) > 0$. Set $f'(e) = f(e) - \gamma$ on $X$ and $f' = f$ elsewhere. Then $0 \le f' \le c$. Conservation still holds at each $v \ne s, t$, since $X$ enters and leaves $v$ equally often. If $X$ is a path, $|f'| = |f| - \gamma \ge 0$; if a cycle, $|f'| = |f|$.
3. *Recurse.* At least one edge of $X$ has $f'(e) = 0$, so $|E^{+}(f')| < |E^+(f)|$. By induction $f'$ has a decomposition with at most $|E^+(f')| \le |E^+(f)| - 1$ parts; add $X$ with weight $\gamma$.

If $f$ is integral, each $\gamma$ is an integer and $f'$ stays integral, so all weights are integers. $\square$

## Variants

- **Paths only.** If $f$ has no cycle in its support (an acyclic flow), the decomposition has only paths. Every flow can be made acyclic without changing its value, by subtracting the cycles that the decomposition finds; a maximum flow found by an augmenting path method may still contain cycles.
- **Circulations.** For a circulation (conservation at every vertex, including $s$ and $t$), the decomposition has only cycles.
- **Supplies and demands.** For a flow with given excesses, the parts are paths from supply vertices to demand vertices, plus cycles. The proof is the same.
- **Unit capacities.** If $c \equiv 1$ and $f$ is integral, each edge carries 0 or 1, so the paths are edge-disjoint with weight 1 each, and there are exactly $|f|$ of them. This is the link to [edge-disjoint paths](/edge-disjoint-paths/) and Menger's theorem.
- **Minimum decomposition.** Find a decomposition with the least number $p + q$ of parts, or the least number of paths. This is NP-hard in the strong sense (Vatinlen, Chauvet, Chretienne and Mahey, 2008).
- **Multi-commodity flows.** Each commodity of a [multi-commodity flow](/multi-commodity-flow-problem/) is decomposed on its own. The path formulation of multi-commodity flow uses this.

## Examples

**The running network.** The [flow network](/flow-network/) has $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10. A maximum flow of value 19 is $f(s, a) = 10$, $f(s, c) = 9$, $f(a, b) = 4$, $f(a, c) = 0$, $f(a, d) = 6$, $f(c, d) = 9$, $f(d, b) = 5$, $f(b, t) = 9$, $f(d, t) = 10$. The greedy method, taking the first edge with flow in the order of the edge list, finds:

| round | part | weight | edges that become empty |
|---|---|---|---|
| 1 | $s\,a\,b\,t$ | 4 | $a b$ |
| 2 | $s\,a\,d\,b\,t$ | 5 | $d b$, $b t$ |
| 3 | $s\,a\,d\,t$ | 1 | $s a$, $a d$ |
| 4 | $s\,c\,d\,t$ | 9 | $s c$, $c d$, $d t$ |

The weights sum to $4 + 5 + 1 + 9 = 19 = |f|$. A different order gives a different decomposition: $s\,a\,b\,t$ 4, $s\,a\,d\,t$ 6, $s\,c\,d\,t$ 4, $s\,c\,d\,b\,t$ 5 is also valid. Both have 4 parts, below the bound $|E^+| = 8$.

**A flow with a cycle.** In $s \to a$ (3), $a \to b$ (2), $b \to a$ (1), $b \to t$ (2), $s \to b$ (1), the flow $f(s, a) = 1$, $f(a, b) = 2$, $f(b, a) = 1$, $f(s, b) = 1$, $f(b, t) = 2$ has value 2 and decomposes into $s\,a\,b\,t$ (1), $s\,b\,t$ (1) and the cycle $a\,b\,a$ (1) on the antiparallel pair. Removing the cycle gives a flow of the same value with $f(a, b) = 1$, $f(b, a) = 0$.

**A circulation.** The flow $f = 3$ on each edge of the cycle $s \to a \to t \to s$ has value $3 - 3 = 0$. It decomposes into one cycle of weight 3 and no path.

**No flow.** In a network with no path from $s$ to $t$, or with $f = 0$, the decomposition is empty. A zero-capacity edge always has $f(e) = 0$ and never appears in a part.

**Real values.** The flow $f(s, a) = f(a, t) = \sqrt 2$ is one path of weight $\sqrt 2$.

## Known algorithms

- **Greedy path and cycle removal.** The proof above, run as an algorithm. A walk of step 1 visits at most $n$ vertices before it reaches $t$ or repeats a vertex, so it costs $O(n)$ steps if each vertex keeps a pointer to its current edge with positive flow (edges that become empty are skipped once and never looked at again). There are at most $m$ rounds, so the time is $O(nm)$, plus $O(m)$ for the skipped edges.
- **Integer paths from a maximum flow.** For unit capacities, decomposing an integral maximum flow from [Ford-Fulkerson](/ford-fulkerson/) gives a maximum set of edge-disjoint paths. Each path is found in $O(n)$ amortized time per edge it uses, so the whole set costs $O(m)$ after the flow.
- **Heuristics for few paths.** Since the minimum version is NP-hard, practice uses greedy rules such as "take the path with the largest bottleneck first" (a [widest path](/widest-path/) in the support). They give no exact optimum.

## Bounds

- **Upper bound on the size.** At most $|E^+| \le m$ parts, by the theorem. Each part has at most $n$ edges, so the output has $O(nm)$ size.
- **The size bound is tight.** Take a path $s = v_0 \to v_1 \to \cdots \to v_k$ of $k$ edges, each of capacity $k$, and $k$ parallel edges from $v_k$ to $t$, each of capacity 1. Then $f = k$ on the path and 1 on each parallel edge is a flow, $m = 2k$, and each decomposition needs $k$ paths (one per parallel edge), each with $k + 1$ edges. So the output has $\Theta(k^2) = \Theta(nm)$ edges in total, and the $O(nm)$ time is optimal for an algorithm that writes the paths out.
- **Fewest parts.** NP-hard in the strong sense; no polynomial exact algorithm is known.

## Reductions

- **Edge-disjoint paths to flow decomposition.** A maximum set of [edge-disjoint paths](/edge-disjoint-paths/) from $s$ to $t$ is the path part of a decomposition of an integral maximum flow in the network with unit capacities. [Vertex-disjoint paths](/vertex-disjoint-paths/) use the same idea after splitting each vertex.
- **Path flows and linear programs.** The decomposition theorem shows that the edge formulation of the [maximum flow](/max-flow-problem/) linear program and the path formulation (one variable per s-t path) have the same optimum. The path form is the base of column generation for multi-commodity flow.

## Applications

- Turning a maximum flow or a [min-cost flow](/min-cost-flow-problem/) into routes for shipments, packets or vehicles.
- Proving facts about flows: the [integrality theorem](/flow-integrality-theorem/) combined with decomposition gives Menger's theorem and the matching results of [bipartite matching](/bipartite-matching/).
- Cancelling cycles: a decomposition shows which cycles a flow carries, and removing them gives an acyclic flow with the same value and no higher cost when costs are nonnegative.
- Bioinformatics, where a flow on a splice graph is decomposed into few paths to guess transcripts; this is one practical source of the minimum decomposition problem.

## References
