---
title: The greedy streaming matching is a maximal matching, so it has at least half the edges of a maximum matching, and the factor 1/2 is tight
proves: [correctness]
status: full
---

Let the stream be the edges $e_1, \ldots, e_m$ of a graph $G = (V, E)$, in this order, with no self-loops (repeats are allowed). Let $M_t$ be the set $M$ after reading $e_1, \ldots, e_t$, and let $V(M_t)$ be the set of vertices marked as matched at that time. Let $\nu(G)$ be the size of a maximum matching.

**Lemma 1 (invariant).** For every $t$, $M_t$ is a matching, and $V(M_t)$ is exactly the set of endpoints of the edges of $M_t$.

*Proof.* By induction on $t$. For $t = 0$, $M_0 = \emptyset$ and no vertex is marked (line L1). Let the claim hold for $t - 1$ and let $e_t = \{u, v\}$. If line L3 finds $u$ or $v$ marked, nothing changes. Otherwise $u, v \notin V(M_{t-1})$, so by the induction hypothesis no edge of $M_{t-1}$ has $u$ or $v$ as an endpoint, and $u \ne v$. Line L4 adds $\{u, v\}$ and marks exactly $u$ and $v$. So $M_t = M_{t-1} \cup \{\{u, v\}\}$ is a matching, and its endpoint set is $V(M_{t-1}) \cup \{u, v\} = V(M_t)$. $\square$

**Lemma 2 (monotone).** $V(M_1) \subseteq V(M_2) \subseteq \cdots \subseteq V(M_m)$.

*Proof.* The algorithm only marks vertices; it never removes a mark or an edge. $\square$

**Lemma 3 (maximal).** $M = M_m$ is a maximal matching of $G$: every edge of $G$ has at least one endpoint in $V(M)$.

*Proof.* Let $\{u, v\} \in E$, and let $t$ be a time at which it is read. If $u$ or $v$ is in $V(M_{t-1})$, it stays in $V(M)$ by Lemma 2. Otherwise line L4 adds the edge, so $u, v \in V(M_t) \subseteq V(M)$. So no edge of $G$ can be added to $M$ while keeping a matching, which is the definition of maximal. $\square$

**Theorem 1.** $\nu(G)/2 \le |M| \le \nu(G)$.

*Proof.* $M$ is a matching by Lemma 1, so $|M| \le \nu(G)$. Let $M^*$ be a maximum matching. By Lemma 3, each edge $f \in M^*$ has an endpoint in $V(M)$; choose one and call it $\phi(f)$. If $f \ne f'$ are in $M^*$, they share no endpoint, so $\phi(f) \ne \phi(f')$. So $\phi$ is an injective map from $M^*$ into $V(M)$, and $|M^*| \le |V(M)| = 2|M|$, using Lemma 1 for the last equality. $\square$

**Theorem 2 (tightness).** For every $k \ge 1$ there is a graph with $\nu = 2k$ and a stream order on which $|M| = k$.

*Proof.* Take $k$ disjoint paths $a_i, b_i, c_i, d_i$, and stream, for each $i$, first $\{b_i, c_i\}$, then $\{a_i, b_i\}$ and $\{c_i, d_i\}$. The first edge of each path is added, and the other two each have a matched end, so they are skipped. So $|M| = k$, while the edges $\{a_i, b_i\}$ and $\{c_i, d_i\}$ form a matching of size $2k$, and no path on 4 vertices has a larger matching than 2. $\square$

**Corollary (vertex cover).** $V(M)$ is a vertex cover of $G$ of size $2|M| \le 2\tau(G)$, where $\tau(G)$ is the size of a minimum vertex cover.

*Proof.* $V(M)$ covers every edge by Lemma 3. Every vertex cover contains an endpoint of each edge of $M$, and these endpoints are distinct because $M$ is a matching, so $\tau(G) \ge |M|$. $\blacksquare$
