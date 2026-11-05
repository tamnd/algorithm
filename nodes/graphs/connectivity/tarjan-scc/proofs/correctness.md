---
title: Tarjan's algorithm outputs each strongly connected component exactly when its root finishes
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph, where parallel arcs and loops are allowed. Write $u \leadsto v$ when $G$ has a directed path from $u$ to $v$, and let the components be the classes of the relation "$u \leadsto v$ and $v \leadsto u$". Write $C(x)$ for the component of $x$. The calls of STRONGCONNECT form a [depth-first search](/depth-first-search/), and $index$ is its preorder: $index[x] < index[y]$ exactly when $x$ is discovered before $y$. A call is *active* between its start and its end. We use these facts about depth-first search.

- (D1) The active calls at any moment form a path of the DFS forest from a root, so of two active vertices one is an ancestor of the other.
- (D2) A vertex discovered while the call of $x$ is active is a descendant of $x$, and every descendant of $x$ is discovered and finished while the call of $x$ is active (the [parenthesis theorem](/parenthesis-theorem/)).
- (D3) If, when $x$ is discovered, a path from $x$ to $y$ has only undiscovered vertices, then $y$ becomes a descendant of $x$ (the [white-path theorem](/white-path-theorem/)).

The *root* $r(C)$ of a component $C$ is its vertex with the least index. Write $T(x)$ for the set of descendants of $x$, $x$ included.

**Lemma 1.** Let $C$ be a component with root $r$. Then $C \subseteq T(r)$, and every vertex on the tree path from $r$ to a vertex $c \in C$ is in $C$.

*Proof.* When $r$ is discovered, no vertex of $C$ is discovered yet. Each $c \in C$ has a path from $r$ inside $C$, as a path between two vertices of a component stays in the component (each vertex $y$ on it has $r \leadsto y \leadsto c \leadsto r$). By (D3), $c \in T(r)$. A vertex $y$ on the tree path from $r$ to $c$ has $r \leadsto y \leadsto c \leadsto r$, so $y \in C$. $\square$

**Lemma 2.** Let $x$ be a vertex, and let $c$ be a child of $x$ with $C(c) \ne C(x)$. Then $c = r(C(c))$.

*Proof.* Let $r' = r(C(c))$. By Lemma 1, $r'$ is an ancestor of $c$. If $r' \ne c$, then $r'$ is an ancestor of $x$, the parent of $c$, and $x$ lies on the tree path from $r'$ to $c$. By Lemma 1, $x \in C(c)$, which is false. So $r' = c$. $\square$

**Lemma 3 (stack order).** At any moment the vertices of $S$, from bottom to top, have increasing index. If $v$ is active, the vertices above $v$ on $S$ are descendants of $v$.

*Proof.* Line L6 pushes each vertex at its discovery, so pushes happen in increasing index, and line L13 pops from the top, which keeps the order. A vertex above an active $v$ was pushed after $v$, so it was discovered while $v$ was active, and it is a descendant of $v$ by (D2). $\square$

We now prove, by induction on the order in which the calls end, the statement

> **(H)** When the call STRONGCONNECT$(v)$ ends: line L11 fires exactly when $v = r(C(v))$, and when it fires, lines L12 and L13 pop exactly the vertices of $C(v)$.

Fix a call STRONGCONNECT$(v)$ and assume (H) for all calls that end before it. Vertices leave $S$ only in line L13. By (H) for these calls, during the call of $v$ the following holds.

> **(S)** A discovered vertex $y$ is on $S$ exactly when the call of $r(C(y))$ has not ended.

Indeed, $y$ is pushed when discovered. It is popped only by an earlier call of a root that pops exactly its own component, so only by the call of $r(C(y))$, and that call does pop it.

**Claim A.** At every moment of the call of $v$ and of the calls inside it, $\mathrm{low}[x] \ge index[r(C(x))]$ for each discovered $x$.

*Proof.* We check each assignment to $\mathrm{low}[x]$. Line L5 sets $\mathrm{low}[x] = index[x] \ge index[r(C(x))]$. Line L10 runs while $x$ is active and sets $\mathrm{low}[x]$ to at least $\min(\mathrm{low}[x], index[w])$ for an arc $(x, w)$ with $w$ on $S$. By (S), the call of $r_w = r(C(w))$ has not ended, and it has started, as $r_w$ was discovered before $w$. So $r_w$ and $x$ are both active, and by (D1) one is an ancestor of the other. If $r_w$ is an ancestor of $x$, then $r_w \leadsto x \to w \leadsto r_w$, so $C(x) = C(w)$ and $index[w] \ge index[r_w] = index[r(C(x))]$. If $x$ is a proper ancestor of $r_w$, then $index[w] \ge index[r_w] > index[x] \ge index[r(C(x))]$. Line L9 sets $\mathrm{low}[x]$ to $\min(\mathrm{low}[x], \mathrm{low}[c])$ for a child $c$, and $\mathrm{low}[c] \ge index[r(C(c))]$ by the claim at an earlier moment. If $C(c) = C(x)$ this is the bound we need. If not, $c = r(C(c))$ by Lemma 2, so $\mathrm{low}[c] \ge index[c] > index[x] \ge index[r(C(x))]$. $\square$

**Claim B.** If $v \ne r(C(v))$, then $\mathrm{low}[v] < index[v]$ when the call of $v$ ends.

*Proof.* Let $r = r(C(v))$. By Lemma 1, $r$ is a proper ancestor of $v$, so $r \notin T(v)$. Take a path from $v$ to $r$ inside $C(v)$, and let $(y, z)$ be its first arc with $y \in T(v)$ and $z \notin T(v)$. Consider the moment line L7 of the call of $y$ scans this arc; it is inside the call of $v$ by (D2). If $z$ were undiscovered, line L9 would make $z$ a child of $y$, so $z \in T(v)$. So $z$ is discovered. It is not a descendant of $v$, so by (D2) it was discovered before $v$, and $index[z] < index[v]$. As $z \in C(v)$, its root is $r$, an ancestor of $v$ whose call has not ended, so $z$ is on $S$ by (S). Line L10 then sets $\mathrm{low}[y] \le index[z]$. Values of $\mathrm{low}$ only decrease, and line L9 passes the final value of each child to its parent, so along the tree path from $v$ to $y$ we get $\mathrm{low}[v] \le \mathrm{low}[y] \le index[z] < index[v]$. $\square$

*Proof of (H) for $v$.* Values of $\mathrm{low}[v]$ start at $index[v]$ and only decrease, so $\mathrm{low}[v] \le index[v]$. If $v = r(C(v))$, Claim A gives $\mathrm{low}[v] \ge index[v]$, so line L11 fires. If not, Claim B gives $\mathrm{low}[v] < index[v]$, so it does not fire.

Let $v = r(C(v))$ and let $A$ be the set of vertices at or above $v$ on $S$ when the call ends. By Lemma 3 and (D2), $A \subseteq T(v)$, and $v \in A$ by (S). We show $A = C(v)$.

- $C(v) \subseteq A$. Each $c \in C(v)$ is in $T(v)$ by Lemma 1, so it is discovered by now, and after $v$ unless $c = v$, so it lies above $v$ on $S$ if it is on $S$ at all. It is on $S$ by (S), since its root is $v$ and the call of $v$ has not ended.
- $A \subseteq C(v)$. Let $y \in A$ and $r_y = r(C(y))$. By (S), the call of $r_y$ has not ended. By Lemma 1, $r_y$ is an ancestor of $y$, so it is an ancestor or a descendant of $v$. If $r_y$ were a proper ancestor of $v$, then $r_y \leadsto v \leadsto y \leadsto r_y$, so $v \in C(y)$ and $r_y = r(C(v)) = v$, which is false. If $r_y$ were a proper descendant of $v$, its call would have ended before the call of $v$, which is false. So $r_y = v$ and $y \in C(v)$.

By Lemma 3, $v$ is the lowest vertex of $A$ on $S$, so the loop of lines L12 and L13 pops the vertices of $A$ from the top down and stops after it pops $v$. It pops exactly $C(v)$. This proves (H). $\square$

**Theorem.** TARJAN-SCC stops, and when it returns, $comp[u] = comp[v]$ if and only if $u$ and $v$ are in the same component. For each arc $(u, v)$ of $G$, $comp[u] \ge comp[v]$.

*Proof.* Line L5 runs once for each vertex, because STRONGCONNECT is called only on vertices with $index = $ NIL, and each call scans a finite list, so the algorithm stops. Lines L2 and L3 start a call at every vertex that is not yet discovered, so every vertex is discovered, and every call ends. Every component $C$ has a root, and by (H) the end of the call of its root pops exactly $C$ and gives all of it the current value of $k$, after which line L14 increases $k$. No vertex is popped twice, because each is pushed once. So each component gets its own label, and only its vertices get it. This proves the first claim.

The labels are given in the order in which the roots finish. Let $(u, v)$ be an arc with $C(u) \ne C(v)$, and let $r_u$ and $r_v$ be the roots. By Lemma 1, the latest finish time in $C(u)$ is that of $r_u$, and likewise for $C(v)$. By Lemma 1 of the [Kosaraju-Sharir proof](/kosaraju-sharir/), the component with an arc into the other finishes later: $r_u$ finishes after $r_v$. So $comp[u] > comp[v]$. If $C(u) = C(v)$, the labels are equal. $\blacksquare$

**Remark on the iterative version.** The Python implementation keeps a stack of frames $(v, i)$ in place of the recursion. A frame is pushed when line L9 would call STRONGCONNECT, and when it is popped the implementation runs lines L11 to L14 for $v$ and then the update $\mathrm{low}[p] \leftarrow \min(\mathrm{low}[p], \mathrm{low}[v])$ of line L9 in the parent $p$. This is the same sequence of steps as the recursion, so the proof applies to it.
