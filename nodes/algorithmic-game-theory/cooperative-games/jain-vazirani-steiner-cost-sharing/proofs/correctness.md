---
title: The Jain-Vazirani shares are cross-monotonic, recover between the optimal Steiner cost and twice it, and match the primal-dual algorithm
proves: [correctness]
status: full
---

**Setting.** $G$ is a connected undirected graph with $N$ vertices and edge costs $c_e \ge 0$. The vertex $r$ is the root and $S$ is a set of $k$ terminals, the players, with $r \notin S$. Let $d$ be the shortest path metric of $G$, and let $P = S \cup \{r\}$. For $t \ge 0$, let $G_t$ be the graph on $P$ with an edge $\{u, v\}$ whenever $d(u, v) \le t$. For $i \in S$, let $K_t(i)$ be the component of $G_t$ that contains $i$. Let $\mathrm{OPT}(S)$ be the cost of a cheapest connected subgraph of $G$ that contains $P$, and let $\mathrm{MST}(S)$ be the cost of a minimum spanning tree of the complete graph on $P$ with costs $d$.

The algorithm (lines L1 to L7) computes $d$ on $P$, sorts the pairs of $P$ by $d$, and scans them in this order. When a pair $\{u, v\}$ joins two components, line L5 adds $(d(u, v) - t)/|K|$ to the share of each member of each component $K$ that does not contain $r$, and line L6 sets $t \leftarrow d(u, v)$ and merges the two components.

**Lemma 1 (the shares as an integral).** For every $i \in S$, the algorithm returns

$$\xi(i, S) = \int_0^\infty \frac{[\, r \notin K_t(i) \,]}{|K_t(i)|}\, dt,$$

where $[\cdot]$ is 1 if the condition holds and 0 otherwise.

*Proof.* The scan is Kruskal's algorithm on the complete graph on $P$. Let $w_1 \le w_2 \le \cdots \le w_{k}$ be the costs of the $k$ pairs that merge two components, in scan order ($|P| = k + 1$ points need $k$ merges). Set $w_0 = 0$. After the scan has processed every pair of cost at most $t$, the union-find components are the components of $G_t$. A pair that is scanned between two merges does not merge anything. So for $w_j \le t < w_{j+1}$, the components of $G_t$ are the components after the first $j$ merges. The step of line L5 for merge $j + 1$ adds, to each $i$ in a component $K$ without $r$, exactly the integral of $1/|K|$ over $[w_j, w_{j+1})$, since $t = w_j$ at that moment. Equal costs give intervals of length 0, which add nothing. After the last merge all points are in the component of $r$, and the integrand is 0. $\square$

**Lemma 2 (the sum).** $\sum_{i \in S} \xi(i, S) = \mathrm{MST}(S)$.

*Proof.* Each component $K$ of $G_t$ without $r$ contributes $|K| \cdot 1/|K| = 1$ to the integrand of the sum. So the sum is $\int_0^\infty (\kappa(t) - 1)\, dt$, where $\kappa(t)$ is the number of components of $G_t$. With the merge costs $w_1, \ldots, w_k$ of Lemma 1, $\kappa(t) - 1 = k - |\{ j : w_j \le t \}| = |\{ j : w_j > t \}|$. So the sum is $\sum_j \int_0^\infty [\, w_j > t \,]\, dt = \sum_j w_j$, the cost of the tree that Kruskal's algorithm builds, which is $\mathrm{MST}(S)$. $\square$

**Lemma 3 (budget).** $\mathrm{OPT}(S) \le \mathrm{MST}(S) \le 2\, \mathrm{OPT}(S)$.

*Proof.* Lower bound: replace each edge $\{u, v\}$ of a minimum spanning tree on $P$ by a shortest path from $u$ to $v$ in $G$. The union of these paths is a connected subgraph of $G$ that contains $P$, and its cost is at most the sum of the path costs, $\mathrm{MST}(S)$. So $\mathrm{OPT}(S) \le \mathrm{MST}(S)$.

Upper bound: let $T^*$ be an optimal Steiner tree. Double each edge of $T^*$. Every vertex then has even degree, so there is a closed walk that uses each doubled edge once, with cost $2\, \mathrm{OPT}(S)$. The walk visits every point of $P$. List the points of $P$ in the order of their first visit, $p_0, p_1, \ldots, p_k$. The part of the walk from $p_{j-1}$ to $p_j$ costs at least $d(p_{j-1}, p_j)$, so the path $p_0, p_1, \ldots, p_k$ in the complete graph on $P$ costs at most $2\, \mathrm{OPT}(S)$. It is a spanning tree of $P$, so $\mathrm{MST}(S) \le 2\, \mathrm{OPT}(S)$. $\square$

By Lemmas 2 and 3, the shares satisfy $\mathrm{OPT}(S) \le \sum_{i \in S} \xi(i, S) \le 2\, \mathrm{OPT}(S)$. The method is 2-budget balanced in the form $C(S) \le \sum_i \xi(i, S) \le \beta\, C(S)$ with $C = \mathrm{OPT}$ and $\beta = 2$. It is exactly budget balanced for the cost of the tree it builds, when the tree is taken as the minimum spanning tree on $P$ with the costs $d$.

**Lemma 4 (cross-monotonicity).** If $i \in S \subseteq S'$ and $r \notin S'$, then $\xi(i, S') \le \xi(i, S)$.

*Proof.* The metric $d$ does not depend on the terminal set. So $G_t$ for $S$ is the subgraph of $G_t$ for $S'$ induced by $S \cup \{r\}$. A path in the smaller graph is a path in the larger one, so $K_t(i) \subseteq K'_t(i)$, where $K'_t(i)$ is the component of $i$ for $S'$. Hence $|K'_t(i)| \ge |K_t(i)|$, and if $r \in K_t(i)$ then $r \in K'_t(i)$. So the integrand of Lemma 1 for $S'$ is at most the integrand for $S$ at every $t$, and the integral is at most the integral for $S$. $\square$

**Lemma 5 (agreement with the primal-dual algorithm).** Consider the complete directed graph on $P$ with arc costs $d(u, v)$. The primal-dual algorithm keeps a dual value $y_X \ge 0$ for each set $X \subseteq P \setminus \{r\}$. The load of an arc $(u, v)$ is the sum of $y_X$ over the sets $X$ with $v \in X$ and $u \notin X$, and the arc is tight when its load equals $d(u, v)$. A set is active if it is a strongly connected component of the tight arcs, does not contain $r$, and has no tight arc that enters it. Each active set raises its dual at rate 1 and splits the increase equally among its members. Then at every time $t$ the active sets are the components of $G_t$ without $r$, so each terminal is charged at rate $[\, r \notin K_t(i) \,]/|K_t(i)|$, and the shares equal those of Lemma 1.

*Proof.* For $v \in P \setminus \{r\}$, let $\tau(v)$ be the first time at which $v$ is in the component of $r$ in $G_t$. We show by induction over time the following claim: for every $t$, the active sets are the components of $G_t$ without $r$, and an arc $(u, v)$ with $u \notin K_t(v)$ has load $\min(t, \tau(v))$. At $t = 0$ no dual is positive, every load is 0, and an arc is tight only if $d(u, v) = 0$, in which case $u$ and $v$ are in one component of $G_0$.

Assume the claim up to time $t$. An arc $(u, v)$ between two components of $G_t$ has load $\min(t, \tau(v))$. If it were tight, then $d(u, v) \le t$, and $u$ and $v$ would be in one component of $G_t$. So no arc between components is tight. Inside a component $K$ without $r$, each merge that built $K$ was caused by a pair $\{u, v\}$ with $d(u, v)$ equal to the merge time $s$, and at time $s$ both sides were components without $r$. By the claim, both arcs $(u, v)$ and $(v, u)$ had load $s = d(u, v)$ and became tight. These pairs form a spanning tree of $K$, so the tight arcs inside $K$ are strongly connected. So $K$ is a strongly connected component of the tight arcs, it has no tight arc that enters it, and it does not contain $r$: $K$ is active. Inside the component of $r$, the same argument shows that each merge made the arc from the side of $r$ into the other side tight. So every point of this component is reached from $r$ by tight arcs, and every strongly connected component in it other than the one of $r$ has a tight arc that enters it. So no set inside the component of $r$ is active.

So the active sets are exactly the components of $G_t$ without $r$. They are disjoint, so the load of an arc $(u, v)$ with $u \notin K_t(v)$ grows at rate 1 while $K_t(v)$ does not contain $r$ and at rate 0 after that. This keeps the load equal to $\min(t, \tau(v))$. The components of $G_t$ change only at the costs $d(u, v)$, and at each such time the argument above applies again. $\square$

**Cost.** Line L1 runs Floyd-Warshall in $O(N^3)$ time, or Dijkstra's algorithm from each of the $k + 1$ points of $P$. Line L2 sorts $O(k^2)$ pairs in $O(k^2 \log k)$ time. There are $k$ merges. Each merge runs line L5 over all $k + 1$ points and relabels the smaller component, so lines L4 to L6 take $O(k^2)$ time in total, plus $O(k^2)$ for the pairs that do not merge. The total time is $O(N^3 + k^2 \log k)$, and the extra space is $O(N^2)$ for the metric.

**Remark.** The tests in `impl/python/test_jain_vazirani_steiner_cost_sharing.py` compare the shares on 250 random graphs with at most 7 vertices against an event-by-event simulation of the primal-dual algorithm of Lemma 5, check Lemma 2 against Prim's algorithm on the metric closure, check Lemma 3 against an optimal Steiner tree found by brute force over the sets of Steiner vertices, and check Lemma 4 for every pair of nested terminal sets on 60 random graphs. $\blacksquare$
