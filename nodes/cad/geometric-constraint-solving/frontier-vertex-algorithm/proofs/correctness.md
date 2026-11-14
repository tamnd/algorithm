---
title: The Frontier algorithm builds a DR-plan whose clusters are rigid in the plane and whose roots are the rigid components
proves: [correctness, invariant, termination, rigid components, running time]
status: full
---

Line numbers refer to the pseudocode on the main page. $G = (V, E)$ has $n$ entities and $m$ distinct constraints; a repeated constraint is skipped in line L1, so we assume there is none. During the run, $S$ is the simplified graph. Its *points* are the entities still in $S$, and its *cores* are the cores of the *live* clusters, those that are not yet a child. For a core $c$, $U(c)$ is the vertex set of its cluster and $F(c)$ is the set of points joined to $c$. For a point $x$, $U(x) = \{x\}$. A set $X$ of nodes of $S$ is *closed* if $F(c) \subseteq X$ for every core $c \in X$, and $U(X) = \bigcup_{x \in X} U(x)$.

Lemmas 1 to 3 and Theorem 5 hold for any positive weights. Lemma 4 and Theorems 6 and 7 are for points and distances in the plane: $w(v) = 2$, $w(e) = 1$, $D = 3$. There, a set $X \subseteq V$ with $|X| \ge 2$ is *rigid* when $E(X)$ has rank $2|X| - 3$ in the generic rigidity matroid of the plane, that is, when the framework $(X, E(X))$ is infinitesimally rigid at a generic placement, and a *rigid component* is a maximal rigid set.

**Lemma 1 (invariants).** After each call of SIMPLIFY, for all live cores $c \ne c'$:

1. a point $x$ is joined to $c$ if and only if $x \in U(c)$, and every edge of $S$ that is not between two points joins a core to a point;
2. if $x \in U(c) \cap U(c')$, then $x$ is a point of $S$, so $x \in F(c) \cap F(c')$;
3. $U(c) \not\subseteq U(c')$.

Moreover, no core is ever in a frontier, and after lines L1 and L2 no edge joins two points.

*Proof.* At the start there are no cores. Consider a call SIMPLIFY($X$), where $X$ is closed: in line L2, $X = \{u, v\}$ has no core, and in line L10, $X$ is closed by Lemma 2 and Lemma 3 below. Assume the claims before the call.

First, every point $x \in U = U(X)$ lies in $X$. Either $x \in X$, or $x \in U(c)$ for a core $c \in X$; then $x$ is joined to $c$ by claim 1, and $x \in F(c) \subseteq X$ since $X$ is closed. Let $X'$ be $X$ with the cores added in line L11. For such an added core $c''$, $F(c'')$ consists of points of $U(c'') \subseteq U$, so $F(c'') \subseteq X$. Hence no core of $X'$ has a neighbor outside $X'$, and no core is in the frontier $F$ of line L12.

Claim 2. Let $c'$ be a live core that stays live, so $U(c') \not\subseteq U$ and $c' \notin X'$. Let $x \in U \cap U(c')$. Then $x \in U(y)$ for some $y \in X$. If $y = x$ is a point, $x$ is joined to $c'$ by claim 1. If $y$ is a core, $x$ is a point joined to $c'$ by claim 2. In both cases $x$ is a point in $X$ with the neighbor $c' \notin X'$, so $x \in F$: it stays a point and is joined to the new core and to $c'$.

Claim 1. The new core is joined exactly to $F \subseteq U$. A point of $U$ in $S$ lies in $X$, as shown, so after line L13 it is in $F$ or deleted; hence the points of $U$ left in $S$ are exactly $F$. For an old core $c'$ that stays live, a point deleted in line L13 had no neighbor outside $X'$, so it was not joined to $c'$, and by claim 1 it was not in $U(c')$. So the equivalence still holds for $c'$.

Claim 3. Before the call the live sets form an antichain. If $U \subseteq U(c')$ for a live $c'$ that stays live, then $U(y) \subseteq U(c')$ for each core $y \in X$, which is false; and if $X$ has no core, $X = \{u, v\}$ and $c'$ would contain the constraint $uv$, which line L1 excludes. All live clusters inside $U$ are absorbed in line L11. So the antichain is kept.

Line L13 deletes the edges inside $X$, so after line L2 for $uv$ the edge $uv$ is gone, and after lines L1 and L2 no edge joins two points. $\square$

After lines L1 and L2, every edge of $S$ joins a core $c$ to a point $f \in F(c)$ and has weight $w(f)$. For a closed set $X$ with cores $C$ and points $P$, let $d_X(f)$ be the number of cores of $X$ joined to $f$. Then
$$ \rho_S(X) = \sum_{f \in P} w(f) \, (d_X(f) - 1) - D \, |C|. \qquad (1) $$
For points and distances in the plane this reads $\rho_S(X) = \sum_f 2(d_X(f) - 1) - 3|C|$. A *target* is a closed set $X$ with $\rho_S(X) \ge -D$ and $|C| \ge 2$.

**Lemma 2 (the search finds targets).** Let $Y$ be a closed set of nodes, after lines L1 and L2. The search of lines L4 and L5 on $Y$ returns only targets inside $Y$, each point of which is joined to a core of it. If $Y$ contains a target, the search returns one.

*Proof.* MAX-CLOSURE($Y$, $\{a, b\}$) is a maximum-weight closure in the network with a node for each edge of $S$ inside $Y$, of profit $w(e)$, that needs both its ends, and a node for each $x \in Y$ of cost $w(x)$, with $a$ and $b$ forced. By Picard's reduction, see [maximum-weight closure](/maximum-weight-closure/), the source side of a minimum cut gives a set $Z$ with $\{a, b\} \subseteq Z \subseteq Y$ and the largest $\rho_S(Z)$. A point is on the source side only if an edge node $e$ that reaches it is, and then the other end of $e$, a core, is too, since the arcs from $e$ have infinite capacity. So every point of $Z$ is joined to a core of $Z$. Line L5 then adds $F(c)$ for each core $c \in Z$; these points lie in $Y$ since $Y$ is closed, and each of them costs $w(f)$ and brings $d \cdot w(f)$ with $d \ge 1$, so the density does not drop. The result is closed, holds the two cores $a$ and $b$, and is a target if line L5 accepts it.

Let $W \subseteq Y$ be a target with cores $C_W$. If no point of $W$ were joined to two cores of $W$, then by (1) $\rho_S(W) \le -D|C_W| \le -2D < -D$. So two cores $a, b \in W$ share a point, and $\{a, b\}$ is a candidate pair of $Y$. Since $W$ is a feasible set for MAX-CLOSURE($Y$, $\{a, b\}$), that call returns a set of density at least $\rho_S(W) \ge -D$, and line L5 accepts it. The search tries every candidate pair, so it returns a target. $\square$

**Lemma 3 (minimal targets).** Lines L7 to L9 end with a target $X$ such that no closed set $W \subsetneq X$ is a target.

*Proof.* $X$ is a target when line L7 is reached, by Lemma 2, and line L9 replaces it by a target. For a core $c \in X$, let $Y_c$ be $X \setminus \{c\}$ without the points that are joined to no other core of $X$. $Y_c$ is closed, since every other core of $X$ keeps its frontier. A target found in $Y_c$ lacks $c$, so each change makes $X$ smaller, and the loop ends. At the end, by Lemma 2, no $Y_c$ contains a target. Now let $W \subsetneq X$ be a closed target. Every point of $X$ is joined to a core of $X$ (Lemma 2, and line L5 adds only frontier points), so if $W$ held every core of $X$, it would hold every point too, and $W = X$. So $W$ misses a core $c$. Drop from $W$ the points joined to no core of $W$: by (1) this raises the density by their weights and keeps $W$ closed, so the result is still a target. It lies in $Y_c$, which is a contradiction. $\square$

**Lemma 4 (every core has two frontier points).** For points and distances in the plane, let $X$ be the target of Lemma 3, with cores $C$, $|C| = k \ge 2$. Then $|F(c)| \ge 2$ for every $c \in C$.

*Proof.* Suppose $|F(c)| \le 1$. If $k = 2$, at most one point lies on both cores, so by (1) $\rho_S(X) \le 2 - 6 = -4$, and $X$ is not a target. If $k \ge 3$, let $W$ be $X$ without $c$ and without the points joined only to $c$. $W$ is closed and has $k - 1 \ge 2$ cores. In (1), dropping $c$ adds 3, the point of $F(c)$, if there is one, loses at most 2, and the dropped points had the term 0. So $\rho_S(W) \ge \rho_S(X) + 1 \ge -2$, and $W \subsetneq X$ is a target, against Lemma 3. $\square$

**Theorem 5 (the plan).** For any positive weights:

1. each cluster is the union of its children and its leaves;
2. each child is a proper subset of its parent and was made earlier;
3. each cluster is a child of at most one cluster;
4. the main loop stops after at most $m - 1$ steps, so there are at most $2m - 1$ clusters;
5. every constraint lies in a root, and the roots cover $V$.

*Proof.* (1) The leaves are defined in line L15 as the entities of $U$ in no child. (2) A child is a live cluster inside $U$ before the call. A cluster of line L2 has no child, since a live cluster inside $\{u, v\}$ would be an earlier copy of $uv$, and its leaves are single entities. In line L10, $X$ holds at least two cores whose sets form an antichain (Lemma 1), so no child equals $U$, and every point of $X$ lies in the set of a core of $X$, so there are no leaves. (3) Line L13 deletes every core of $X'$, so a cluster stops being live when it becomes a child. (4) After lines L1 and L2 there are at most $m$ live clusters, and each step absorbs at least two and adds one. (5) Each constraint is in the cluster of line L2 for it or for its first copy. Follow the parent of that cluster, which is unique by (3); the sets grow along the way, and at the end the chain stops at a live cluster, which is a root. Line L16 lists as roots the live clusters and the entities in no constraint, so the roots cover $V$. $\square$

For the rest, the weights are those of points and distances in the plane, and all frameworks are at one generic placement of $V$. We use three facts about rigidity in the plane.

- **(R1)** If $A$ and $B$ are rigid and share at least two vertices, then $A \cup B$ is rigid with the edges $E(A) \cup E(B)$. An infinitesimal motion is trivial on $A$ and on $B$, and a trivial motion of the plane is fixed by its values at two distinct points, so the two agree.
- **(R2)** Every edge lies in exactly one rigid component, and two rigid components share at most one vertex. An edge is rigid, so it lies in a maximal rigid set; by (R1) two rigid components that share two vertices would have a rigid union.
- **(R3)** For a multigraph $H$ with rigid components $R_1, \ldots, R_t$, the rank of $H$ is $\sum_i (2|R_i| - 3)$. Take a basis $B_i$ of the edges inside each $R_i$, so $|B_i| = 2|R_i| - 3$. The $B_i$ are disjoint by (R2), and their union spans $H$, since each edge of $H$ lies in some $R_i$ and so in the closure of $B_i$. So it is enough that the union is independent. If $\bigcup_i B_i$ held a circuit $Q$, then $Q$ minus any edge would be independent with $2|V(Q)| - 3$ edges, so $V(Q)$ is rigid by [Laman's theorem](/laman-theorem/) and lies in one component $R_j$; then $Q \subseteq B_j$, which is impossible.

**Theorem 6 (clusters are rigid).** For points and distances in the plane, the vertex set of every cluster is rigid. Hence the recorded density $\rho(U) = |E(U)| - 2|U|$ is at least $-3$.

*Proof.* By induction on the order of the clusters. A cluster of line L2 is one constraint, which is rigid. Let the cluster $U$ come from the target $X$ of Lemma 3, with cores $C$, $k \ge 2$, and points $P$. Each $U(c)$ with $c \in C$ is rigid by induction, $U = \bigcup_{c \in C} U(c)$, and $|F(c)| \ge 2$ by Lemma 4. A vertex that lies in two of the sets $U(c)$ is a point of $P$ in both frontiers, by Lemma 1. For each $c \in C$, let $L_c$ be a minimally rigid graph on $F(c)$, with $2|F(c)| - 3$ edges, and let $H$ be the multigraph on $P$ that is the union of the $L_c$.

*If $H$ is rigid, $U$ is rigid.* Let $u$ be an infinitesimal motion of the framework on $U$ with the edges $\bigcup_c E(U(c)) \subseteq E(U)$. On each $U(c)$ it is trivial, since $U(c)$ is rigid. So on $P$ it keeps the length of each edge of each $L_c$ to first order, and as $H$ is rigid, $u$ agrees on $P$ with one trivial motion $T$. On each $U(c)$, $u$ is a trivial motion that agrees with $T$ on the two or more points of $F(c)$, so it is $T$. Every vertex of $U$ lies in some $U(c)$, so $u = T$ on $U$. Thus the rank of $E(U)$ is $2|U| - 3$.

*$H$ is rigid.* Let $R_1, \ldots, R_t$ be the rigid components of $H$. Each $F(c)$ spans the rigid graph $L_c$, so by (R2) it lies in exactly one component; let $C_i$ be the cores with $F(c) \subseteq R_i$. An edge of $L_c$ lies in the component of $F(c)$, so the edges of $H$ inside $R_i$ are the edges of the $L_c$ with $c \in C_i$, and as every vertex of a rigid set with two or more vertices has an edge in it, $R_i = \bigcup_{c \in C_i} F(c)$. So $W_i = C_i \cup R_i$ is closed, and by (1),
$$ \rho_S(W_i) = \sum_{c \in C_i} 2|F(c)| - 3|C_i| - 2|R_i| = \sum_{c \in C_i} (2|F(c)| - 3) - 2|R_i| \ge (2|R_i| - 3) - 2|R_i| = -3, $$
since the number of edges of $H$ inside $R_i$ is at least their rank, $2|R_i| - 3$. If some $C_i$ has two or more cores, $W_i$ is a target inside $X$, so $W_i = X$ by Lemma 3, $R_i = P$, and $H$ is rigid. Otherwise every $C_i$ has one core, and by (R3)
$$ \operatorname{rank} H = \sum_{c \in C} (2|F(c)| - 3) = \sum_{f \in P} 2 d_X(f) - 3k = \rho_S(X) + 2|P| \ge 2|P| - 3, $$
so $H$ is rigid. Finally, rigid $U$ means $|E(U)| \ge 2|U| - 3$. $\square$

**Theorem 7 (roots are the rigid components).** For points and distances in the plane, when the algorithm stops, the live clusters are exactly the rigid components of $G$. So the roots with two or more entities are the rigid components.

*Proof.* The algorithm stops when the search of lines L4 and L5 on all of $S$, a closed set, finds nothing, so by Lemma 2 $S$ holds no target. Let $R$ be a rigid component, and let $C_R$ be the live cores $c$ with $|U(c) \cap R| \ge 2$. For such $c$, $U(c)$ is rigid (Theorem 6), so $U(c) \cup R$ is rigid by (R1), and $U(c) \subseteq R$ as $R$ is maximal. Each edge of $G[R]$ lies in a live cluster (Theorem 5), which then meets $R$ in two vertices, so the edges of $G[R]$ are exactly $\bigcup_{c \in C_R} E(U(c))$.

Suppose $k = |C_R| \ge 2$. Consider the tuples $(T_c)_{c \in C_R}$ of trivial motions that agree on every vertex lying in two or more of the sets $U(c)$. Each tuple gives an infinitesimal motion of $(R, E(R))$, since every edge lies in some $U(c)$, and different tuples give different motions. $R$ is rigid, so these tuples form a space of dimension at most 3. A vertex in $d \ge 2$ of the sets is a point in their frontiers (Lemma 1), and the agreement there is $2(d - 1)$ linear equations, so the dimension is at least $3k - \sum_f 2(d(f) - 1)$. Let $W$ be $C_R$ with all their frontiers. $W$ is closed, and by Lemma 1, $d_W(f)$ is the number of sets $U(c)$, $c \in C_R$, that contain $f$. By (1),
$$ \rho_S(W) = \sum_f 2(d_W(f) - 1) - 3k \ge -3, $$
so $W$ is a target in $S$, a contradiction. Hence $k = 1$; as every vertex of $R$ has an edge in $G[R]$, $R \subseteq U(c) \subseteq R$ for the one core $c$. So every rigid component is a live cluster. Conversely, a live cluster is rigid, so it lies in a rigid component, which is a live cluster; by the antichain of Lemma 1 the two are the same. $\square$

**Running time.** The number of edges between cores and points never grows: the new core gets one edge for each point of $F \subseteq X$, and each point of $X$ had an edge to a core of $X$, which line L13 deletes. So after lines L1 and L2, $S$ has at most $n + m$ nodes and $2m$ edges. One MAX-CLOSURE runs a maximum flow on a network with $O(n + m)$ nodes and arcs, and the flow value is at most the total weight $2n + 3m$; each augmenting path carries at least one unit and is found by breadth-first search in $O(n + m)$, so one call costs $O((n + m)^2)$. Two cores share a point in at most $\sum_f d(f)^2 \le (2m)^2$ ways, so one search makes $O(m^2)$ calls. Lines L7 to L9 make at most $m$ rounds, since each round removes a core, of at most $m$ searches each, and the main loop runs at most $m - 1$ times (Theorem 5). The total is $O(m^5 (n + m)^2)$. $\square$
