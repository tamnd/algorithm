---
title: The Even-Tarjan algorithm returns the vertex connectivity
proves: [correctness]
status: full
---

Let $G = (V, E)$ be an undirected graph with vertices $v_1, \ldots, v_n$, $n \ge 1$. Parallel edges and loops are allowed. A loop joins a vertex to itself and parallel edges join the same two vertices, so neither changes which pairs of distinct vertices are adjacent, which $s$-$t$ paths exist, or which sets $X$ make $G - X$ disconnected. So we may assume $G$ is simple. Define $\kappa(G)$ and $\kappa(s, t)$ as on the main page.

**Lemma 1 (pairs).** If $G$ is not complete, then $\kappa(G) = \min \{ \kappa(s, t) : s \neq t \text{ not adjacent} \}$.

*Proof.* If $X$ separates the non-adjacent $s$ and $t$, then $G - X$ contains $s$ and $t$ and has no $s$-$t$ path, so it is disconnected; hence $\kappa(G) \le \kappa(s, t)$. Conversely, let $G - X$ be disconnected with $|X| = \kappa(G)$, and pick $s$ and $t$ in two different components of $G - X$. They are not adjacent, and $X$ separates them, so $\kappa(s, t) \le |X| = \kappa(G)$. A non-complete graph has a non-adjacent pair $s, t$, and $V \setminus \{s, t\}$ separates them, so the sets in the definition are not empty. $\square$

**Lemma 2 (LOCAL).** For non-adjacent $s \neq t$ and an integer $c \ge 0$, LOCAL$(s, t, c)$ returns $\min(c, \kappa(s, t))$.

*Proof.* In the split digraph $D$, a set of $f$ paths from $s$ to $t$ in $G$ that share no inner vertex gives $f$ arc-disjoint paths from $s_{\mathrm{out}}$ to $t_{\mathrm{in}}$: the path $s, w_1, \ldots, w_r, t$ becomes $s_{\mathrm{out}}, w_{1,\mathrm{in}}, w_{1,\mathrm{out}}, \ldots, w_{r,\mathrm{out}}, t_{\mathrm{in}}$, and two such paths share no arc since they share no $w$. Conversely, an integral flow of value $f$ with unit capacities splits into $f$ arc-disjoint paths from $s_{\mathrm{out}}$ to $t_{\mathrm{in}}$, and since the only arc that leaves $w_{\mathrm{in}}$ is $w_{\mathrm{in}} \to w_{\mathrm{out}}$, two of them never pass the same $w \notin \{s, t\}$. We may drop cycles from these paths, so a path ends at its first visit to $t_{\mathrm{in}}$ and never passes $s_{\mathrm{in}}$, whose only leaving arc goes back to $s_{\mathrm{out}}$. So the maximum flow value equals the most $s$-$t$ paths in $G$ that share no inner vertex, which is $\kappa(s, t)$ by Menger's theorem (Diestel, Section 3.3). Each round of lines L11 and L12 adds 1 to an integral flow, and by the augmenting path theorem the loop stops without the cap exactly when the flow is maximum. So LOCAL returns $c$ if $\kappa(s, t) \ge c$, and $\kappa(s, t)$ otherwise. $\square$

**Lemma 3 (upper invariant).** At every moment, $k \ge \kappa(G)$.

*Proof.* At line L1, $k = n - 1 \ge \kappa(G)$, because $\kappa(G) \le n - 1$ in both cases of the definition: a disconnecting set leaves at least two vertices. Line L6 only replaces $k$ by $\min(k, x)$ with $x = \min(k, \kappa(v_i, v_j))$, and both $k$ and $\kappa(v_i, v_j)$ are at least $\kappa(G)$ by induction and Lemma 1. $\square$

**Theorem.** VERTEX-CONNECTIVITY$(G)$ returns $\kappa(G)$.

*Proof.* It terminates, since $i$ grows by one at each round of line L3, and $k \le n - 1$.

If $G$ is complete, line L5 never holds, $k$ stays $n - 1 = \kappa(G)$, and that is returned.

Otherwise let $\kappa = \kappa(G)$, and let $X$ be a set with $|X| = \kappa$ such that $G - X$ is disconnected. Then $|X| \le n - 2$, so the vertices $v_1, \ldots, v_{\kappa + 1}$ exist and are $\kappa + 1$ in number, and at least one of them is not in $X$. Let $i^*$ be the least index with $v_{i^*} \notin X$, so $i^* \le \kappa + 1$. Pick a vertex $v_j$ in a component of $G - X$ that does not contain $v_{i^*}$. Then $v_j \notin X$, and $v_j$ is not adjacent to $v_{i^*}$. Every $v_\ell$ with $\ell < i^*$ is in $X$, so $j > i^*$.

Suppose the algorithm returns a value other than $\kappa$. By Lemma 3 the value is larger, so $k > \kappa$ at every moment, since $k$ never increases. In particular, at the test of line L3 with $i = i^*$, $k \ge \kappa + 1 \ge i^*$, so the loop body runs for $i = i^*$. Line L4 reaches $j$, line L5 holds, and line L6 sets $k$ to at most $\min(k, \kappa(v_{i^*}, v_j))$ by Lemma 2. Since $X$ separates $v_{i^*}$ from $v_j$, $\kappa(v_{i^*}, v_j) \le \kappa$, so $k \le \kappa$ after this step, a contradiction. $\blacksquare$
