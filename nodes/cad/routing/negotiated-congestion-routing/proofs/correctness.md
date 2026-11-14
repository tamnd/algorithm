---
title: Negotiated congestion routing builds valid trees, keeps exact usage counts, returns a legal routing when it stops early, and ends after at most max_iters iterations
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be the grid graph, connected, with capacities $c_e \ge 0$. Every cost in the algorithm has the form $(b_e + h_e) p_e$ with $b_e > 0$, $h_e \ge 0$ and $p_e \ge 1$, so every cost is at least $b_e > 0$. Write $\beta = \min_e b_e > 0$.

**Lemma 1 (one search step).** Let $S$ be the node set of the current tree and $L$ the set of terminals not in $S$, with $L \ne \emptyset$. The search of $\textsc{Route-Tree}$, Dijkstra's algorithm with every node of $S$ as a source at distance 0, stops at a terminal $t \in L$ with the least distance from $S$, and the path it traces back from $t$ is a cheapest path from $S$ to $t$. Its nodes other than its first node are not in $S$.

*Proof.* Join a new node $z$ to every node of $S$ by an edge of cost 0. Dijkstra's algorithm from $z$ on this graph is the multi-source search, and all other costs are positive, so it removes nodes from the heap in order of their distance from $z$, which is their distance from $S$, and the predecessor links give shortest paths ([Dijkstra's algorithm](/dijkstra/)). The search stops at the first removed node of $L$, which has the least distance among the nodes of $L$. Every node of $S$ has distance 0, and no relaxation can lower a distance below 0, so no node of $S$ gets a predecessor link. The trace back from $t$ follows predecessor links and stops at the first node of $S$ that it meets. So only the first node of the path is in $S$. $G$ is connected, so some node of $L$ is reachable and the search does not run out of nodes before it stops. $\square$

**Lemma 2 (valid trees).** $\textsc{Route-Tree}(T_i, \mathrm{cost})$ returns an edge set $R_i$ that is a tree, holds every node of $T_i$, and has only terminals as leaves. It makes at most $|T_i| - 1$ searches.

*Proof.* The invariant is: the current edge set is a tree on the node set $S$, every leaf of it is a terminal, and $S$ holds the first terminal. At the start, $S$ is the first terminal and there are no edges. A step adds a path whose first node is in $S$ and whose other nodes are new (Lemma 1). Adding a path that meets a tree in exactly one node gives a tree. The only new leaf is the last node $t$, a terminal. The first node gets one more edge, so if it was a leaf it no longer is, and the inner nodes of the path have degree 2. So the invariant holds. Each step puts at least the terminal $t$ into $S$, so after at most $|T_i| - 1$ steps every terminal is in $S$ and the loop ends. $\square$

**Lemma 3 (exact usage).** At the start of line L4 for net $i$, and after line L7, $u_e = |\{ j : e \in R_j \}|$ for every edge $e$, where $R_j$ is the current route of net $j$ (empty before net $j$ is first routed).

*Proof.* At the start all routes are empty and all $u_e = 0$. Line L4 subtracts 1 for each edge of the old $R_i$, so $u_e$ then counts the nets other than $i$. Line L7 adds 1 for each edge of the new $R_i$, and $R_i$ is a set, so each edge gets at most 1 from net $i$. So the count is exact after line L7, and it stays exact until the next line L4, because nothing else changes $u$. $\square$

By Lemma 3, $u_e$ at line L5 counts the other nets on $e$, so $p_e = 1$ exactly when one more net fits, $u_e + 1 \le c_e$, and $p_e - 1$ is $\mathrm{pres\_fac}$ times the overflow that net $i$ would cause on $e$.

**Lemma 4 (growing penalties).** $h_e$ never decreases. If edge $e$ is overflowed at line L9 of an iteration, then $h_e$ grows by at least $\mathrm{hist\_fac}$ in that iteration. If $\mathrm{pres\_init} > 0$ and $\mathrm{pres\_mult} \ge 1$, then $\mathrm{pres\_fac}$ never decreases.

*Proof.* Line L9 adds $\mathrm{hist\_fac} \cdot \max(0, u_e - c_e) \ge 0$, and the max is at least 1 when $u_e > c_e$, since the values are integers. Line L10 replaces 0 by $\mathrm{pres\_init} > 0$, or multiplies a positive value by $\mathrm{pres\_mult} \ge 1$. No other line changes $h$ or $\mathrm{pres\_fac}$. $\square$

**Theorem (correctness and termination).**

1. Every returned route $R_i$ is a tree that holds $T_i$, and its leaves are terminals.
2. If the loop stops at line L8, the returned routing has $u_e \le c_e$ for every edge.
3. In every case the returned routing is, among the routings at the ends of the iterations that ran, one with the least total overflow and, among those, the least wirelength.
4. The algorithm stops after at most $\mathrm{max\_iters}$ iterations, and each iteration makes at most $P - m$ searches.

*Proof.* (1) is Lemma 2 for each call of line L6, and line L11 returns routes recorded at line L8, which are outputs of line L6. (2) At line L8 the usage is exact by Lemma 3. The stop happens only when no edge has $u_e > c_e$. That routing has total overflow 0, the least possible, so it is recorded as the best, and it is returned. (3) Line L8 records the routing at the end of each iteration when its pair (total overflow, wirelength) is smaller in lexicographic order than the best pair so far. So the recorded routing is a lexicographic minimum over all iterations that ran. (4) The loop of line L2 runs at most $\mathrm{max\_iters}$ times. Each net makes at most $|T_i| - 1$ searches by Lemma 2, and $\sum_i (|T_i| - 1) = P - m$. Each search ends, since Dijkstra's algorithm removes each node at most once. $\square$

**What the theorem does not say.** It does not say that the loop reaches total overflow 0 when a legal routing exists, and it gives no bound on the number of iterations needed. No such general result is known. The $2 \times 2$ grid with capacity 1 and two nets between opposite corners shows that overflow 0 can be impossible: each route of one net meets each route of the other net in an edge, so the loop runs all $\mathrm{max\_iters}$ iterations and returns overflow 1.
