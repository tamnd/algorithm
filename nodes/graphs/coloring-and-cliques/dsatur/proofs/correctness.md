---
title: DSATUR returns a proper coloring and two-colors every bipartite graph
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph with $n$ vertices. Call round $t$ the $t$-th run of the loop of line L2, and let $U_t$ be the set of uncolored vertices at its start, so $U_1 = V$.

**Claim.** DSATUR$(G)$ stops after $n$ rounds and returns $c$ with $c(v) \ge 1$ for all $v$ and $c(u) \ne c(v)$ for each edge $\{u, v\}$. The color of $v$ is at most $|S[v]| + 1 \le \deg(v) + 1$ at the moment it is colored. If $G$ is bipartite, $c(v) \in \{1, 2\}$ for all $v$.

**Invariant.** At the start of round $t$:

> **(D)** $c(v) = 0$ exactly for $v \in U_t$, and $|U_t| = n - t + 1$. For each $v \in U_t$, $S[v] = \{ c(w) : w \in N(v) \setminus U_t \}$ and $\mathrm{dunc}[v] = |N(v) \cap U_t|$. No edge joins two colored vertices of the same color.

*Initialization.* Line L1 sets every color to 0, every $S[v]$ to $\emptyset$ and $\mathrm{dunc}[v]$ to $\deg(v)$, which is (D) for $U_1 = V$.

*Maintenance.* In round $t \le n$, $U_t$ is not empty, so line L3 finds a vertex $v \in U_t$. The set $S[v]$ has at most $|S[v]|$ elements, so one of $1, \ldots, |S[v]| + 1$ is not in it, and line L4 stops with $1 \le k \le |S[v]| + 1$ and $k \notin S[v]$. By (D), $k$ differs from the color of every colored neighbor of $v$, so after line L5 no edge joins two colored vertices of the same color. Now $U_{t+1} = U_t \setminus \{v\}$. For $w \in U_{t+1}$, the set $N(w) \setminus U_{t+1}$ gains $v$ exactly when $w$ is a neighbor of $v$; lines L6 to L8 add $c(v) = k$ to $S[w]$ and lower $\mathrm{dunc}[w]$ by one for exactly these $w$, once each since $G$ is simple. So (D) holds at the start of round $t + 1$. Also $|S[v]| \le |N(v)| = \deg(v)$.

*Termination.* Each round colors one vertex of $U_t$, and line L4 stops after at most $\deg(v) + 1$ tests. After $n$ rounds, (D) with $U_{n+1} = \emptyset$ says that all vertices are colored with colors at least 1 and the coloring is proper.

**Bipartite graphs.** Let $G$ be bipartite with a bipartition fixed in each connected component. We show by induction on $t$ that at the start of round $t$:

> **(B)** at most one connected component $C$ is partly colored (it has colored and uncolored vertices); in that component the colored vertices induce a connected subgraph; and every colored vertex has color 1 or 2, with the colors given by the sides of its component (in each component, all colored vertices of one side share one color, and the other side has the other color).

For $t = 1$ nothing is colored. Assume (B) at round $t$ and let $v$ be the vertex chosen at line L3.

*Case 1: some component $C$ is partly colored.* Since $C$ is connected and has colored and uncolored vertices, some uncolored $u \in C$ has a colored neighbor, so $|S[u]| \ge 1$. A vertex in any other component has no colored neighbor, because the other components are fully colored or fully uncolored; so its saturation is 0. Line L3 compares saturation first, so $v \in C$ and $|S[v]| \ge 1$. All colored neighbors of $v$ lie on the side of $C$ opposite to $v$, so by (B) they all have one color $x \in \{1, 2\}$, and $S[v] = \{x\}$. Line L4 gives $v$ the color $3 - x$. If other colored vertices of $C$ lie on the side of $v$, then by (B) they have the color other than $x$, which is $3 - x$; so the colors in $C$ still follow the sides. The colored part of $C$ stays connected, because $v$ has a colored neighbor. So (B) holds after round $t$, with $C$ partly colored or now fully colored.

*Case 2: no component is partly colored.* Then every uncolored vertex has saturation 0, and $v$ starts a new component $C'$ with $S[v] = \emptyset$, so $c(v) = 1$. The colored part of $C'$ is $\{v\}$, which is connected and uses the color 1 on the side of $v$. If $C' = \{v\}$, then $C'$ is fully colored. So (B) holds after round $t$.

In both cases each new color is 1 or 2. So DSATUR colors every bipartite graph with at most 2 colors. $\blacksquare$
