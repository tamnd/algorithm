---
tag: PKWE4D
kind: concept
slug: blocking-flow
name: Blocking flow
aliases:
- blocking flow in a level graph
area: graphs/flows-and-cuts
level: core
summary: A flow in the level graph that saturates at least one edge on every s-t path.
prereqs: [level-graph, s-t-flow, residual-graph]
see_also: [dinic, mpm-algorithm, edmonds-karp, link-cut-tree, hopcroft-karp, push-relabel, augmenting-path-flow]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (Dinitz's blocking flows)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 7, Maximum Flows, Polynomial Algorithms (layered networks, blocking flows and Dinic's algorithm)
  - book: isbn:9780898711875
    title: Robert Endre Tarjan, Data Structures and Network Algorithms
    locator: Chapter 8, Network Flows (blocking flows, Dinic's algorithm and the dynamic tree method)
  - paper: doi:10.1007/11685654_10
    title: Yefim Dinitz, Dinitz' algorithm, the original version and Even's version, in Theoretical Computer Science, Essays in Memory of Shimon Even, LNCS 3895, 218 to 240 (2006)
    locator: the whole chapter (the layered network and the blocking flow phase)
---

A blocking flow in a network is a flow such that every path from $s$ to $t$ has at least one edge that the flow fills to capacity, so no path can take more flow without first cancelling some. It is usually computed in the [level graph](/level-graph/) of a [residual graph](/residual-graph/), where it is the work of one phase of [Dinic's algorithm](/dinic/). A blocking flow need not be a maximum flow, but adding it to the current flow makes the distance from $s$ to $t$ in the residual graph strictly larger, which bounds the number of phases by $n - 1$.

## In plain words

Push water along routes from the source to the drain, using only forward moves, until every route has some full pipe. You may not undo anything. The result is a blocking flow: it blocks every route, but a cleverer plan that sends water differently might still carry more.

Dinic's algorithm uses this idea on the shortest routes only. It finds a blocking flow among all the routes of the current shortest length, adds it, and then the shortest route left is strictly longer. Since a route cannot be longer than the number of places, there are few such rounds.

## The idea

Let $H = (V, A)$ be a directed graph with capacities $u(x) > 0$ on its arcs, and $s \ne t$. A flow $g$ in $H$ (capacity and conservation constraints as for an [s-t flow](/s-t-flow/)) is **blocking** if every directed path from $s$ to $t$ in $H$ contains an arc $x$ with $g(x) = u(x)$. Equivalently: after deleting the saturated arcs, $t$ is not reachable from $s$ in $H$.

Every maximum flow of $H$ is blocking, since a path of $H$ with no full arc could take more flow. The converse fails: the definition looks only at paths of $H$, not at residual paths that use backward arcs, so a blocking flow need not be maximum.

**The level graph.** Let $f$ be a flow in a [flow network](/flow-network/) $N$, and let $d(v)$ be the BFS distance from $s$ to $v$ in the residual graph $G_f$. The [level graph](/level-graph/) $L_f$ keeps the arcs $(v, w)$ of $G_f$ with $d(w) = d(v) + 1$, with capacities $c_f$. It is acyclic, and its s-t paths are exactly the shortest s-t paths of $G_f$.

**Lemma (distance grows).** Let $g$ be a blocking flow in $L_f$, and let $f'$ be $f$ augmented by $g$ (on each arc of $L_f$, add $g$ to the forward arc and subtract it from its reverse). Then $d_{f'}(t) > d_f(t)$.

*Proof.* The arcs of $G_{f'}$ are arcs of $G_f$, or reverses of arcs of $L_f$ that carry flow in $g$. A reverse arc $(w, v)$ of an arc $(v, w)$ of $L_f$ has $d(v) = d(w) - 1$; it goes down one level. An arc of $G_f$ goes up at most one level. So every arc of $G_{f'}$ goes up at most one level in the labels $d = d_f$, and an s-t path in $G_{f'}$ has at least $d(t)$ arcs. Suppose one has exactly $d(t)$ arcs. Then each of its arcs goes up exactly one level, so each is an arc of $G_f$ with $d(w) = d(v) + 1$, which is an arc of $L_f$, and it is still in $G_{f'}$, so it is not saturated by $g$. That is an s-t path in $L_f$ with no saturated arc, which contradicts that $g$ is blocking. So every s-t path in $G_{f'}$ has more than $d(t)$ arcs. $\square$

Since $1 \le d(t) \le n - 1$ while $t$ is reachable, at most $n - 1$ blocking flow phases occur before $t$ becomes unreachable and the flow is maximum.

**Computing a blocking flow.**

- **Augment and retreat (Dinic).** Walk from $s$ along arcs of $L_f$ with a current-arc pointer per vertex. When the walk reaches $t$, push the bottleneck and restart from $s$; at least one arc becomes full. When a vertex has no usable arc left, delete it (retreat). Each augmentation costs $O(n)$ and deletes an arc, and each retreat deletes an arc, so the time is $O(nm)$ per blocking flow.
- **MPM.** The [MPM algorithm](/mpm-algorithm/) pushes from the vertex of least throughput, in $O(n^2)$ per blocking flow.
- **Dynamic trees.** Sleator and Tarjan keep the current paths in [link-cut trees](/link-cut-tree/), so a blocking flow costs $O(m \log n)$; the whole maximum flow then costs $O(nm \log n)$.
- **Unit capacities.** With all capacities 1, each arc is used once and then deleted, so a blocking flow costs $O(m)$. This is the phase of [Hopcroft-Karp](/hopcroft-karp/).

## Examples

**Blocking but not maximum.** Take the acyclic network with arcs $s x_1$, $s x_2$, $x_1 y_1$, $x_1 y_2$, $x_2 y_1$, $y_1 t$, $y_2 t$, each of capacity 1. Its s-t paths are $s\,x_1\,y_1\,t$, $s\,x_1\,y_2\,t$ and $s\,x_2\,y_1\,t$. The flow of 1 along $s\,x_1\,y_1\,t$ fills $s x_1$ and $y_1 t$, and each of the three paths uses one of them, so this flow is blocking. Its value is 1, but the maximum flow is 2, along $s\,x_1\,y_2\,t$ and $s\,x_2\,y_1\,t$. To get there one needs the backward arc $(y_1, x_1)$, which the next phase of Dinic finds: the residual path $s\,x_2\,y_1\,x_1\,y_2\,t$ of length 5.

**The running network.** In the network $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10 with $f = 0$, the levels are $s$: 0, $a, c$: 1, $b, d$: 2, $t$: 3. The level graph keeps $s a$, $s c$, $a b$, $a d$, $c d$, $b t$, $d t$, and drops $a c$ (both ends at level 1) and $d b$ (both at level 2). A blocking flow is $s\,a\,b\,t$ with 4, $s\,a\,d\,t$ with 6 and $s\,c\,d\,t$ with 4: after it, $s a$ and $a b$ are full and $d t$ is full, and every s-t path of the level graph uses $s a$ or $d t$. Its value is 14. In the new residual graph $d(t) = 4$, by the path $s\,c\,d\,b\,t$, which takes 5 more in the next phase and gives the maximum value 19.

**A zero-capacity arc and an unreachable sink.** Arcs of capacity 0 are not in the residual graph, so they are not in the level graph. If $t$ is not reachable, the level graph has no s-t path, and the zero flow is blocking (vacuously); Dinic stops at once.

**Antiparallel edges.** If $N$ has edges $(a, b)$ and $(b, a)$, the residual graph can have two arcs from $a$ to $b$: the forward arc of the first edge and the backward arc of the second. When $d(b) = d(a) + 1$, both are in the level graph as separate arcs. A path that uses one of them is blocked only if one of its own arcs is full, so a blocking flow treats them as two parallel arcs. Keeping one arc pair per edge handles this case with no special code.

**Real capacities.** Nothing in the definition or the lemma needs integers; with real capacities each Dinic phase still ends, because each augmentation fills at least one arc.

## Where it is used

- [Dinic's algorithm](/dinic/): one blocking flow per phase, at most $n - 1$ phases, $O(n^2 m)$ total.
- [MPM algorithm](/mpm-algorithm/): a faster blocking flow, $O(n^3)$ total.
- [Hopcroft-Karp](/hopcroft-karp/) for bipartite matching: blocking flows in unit networks, $O(\sqrt{n})$ phases.
- Dinic with [link-cut trees](/link-cut-tree/): $O(nm \log n)$ maximum flow.
- Goldberg and Rao's binary blocking flow algorithm: $O(\min(n^{2/3}, m^{1/2})\, m \log(n^2/m) \log U)$ for integer capacities up to $U$.
- The phase argument also shows that [Edmonds-Karp](/edmonds-karp/) does at most $m$ augmentations of each length.

## References
