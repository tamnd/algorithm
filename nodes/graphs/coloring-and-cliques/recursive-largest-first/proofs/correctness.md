---
title: RLF builds maximal independent classes and a proper coloring
proves: [correctness, termination]
status: full
---

Number the passes of the outer loop (line L2) by $k = 1, 2, \ldots$. Let $U_k$ be the set $U$ at line L3 of pass $k$, and let $C_k$ be the set of vertices that receive color $k$.

**Invariant of the inner loop.** At line L8 of pass $k$:

1. $C_k$ (the vertices colored $k$ so far), $P$ and $W$ are disjoint and their union is $U_k$;
2. $C_k$ is independent;
3. no vertex of $P$ has a neighbor in $C_k$;
4. every vertex of $W$ has a neighbor in $C_k$.

*Initialization.* At line L3, $P = U_k$, $W = \emptyset$ and $C_k = \emptyset$. Line L4 picks $v \in P$, which exists because $U_k \ne \emptyset$ by line L2.

*Maintenance.* Each turn of the loop starts with a vertex $v \in P$ (from line L4 or line L9, both choose from $P$, which is nonempty). Before line L6, the invariant holds with $v \in P$, so by part 3, $v$ has no neighbor in $C_k$, and $C_k \cup \{v\}$ is independent. Line L6 moves $v$ from $P$ to $C_k$, which keeps part 1. After line L6, a vertex of $P$ may be a neighbor of $v$; line L7 moves exactly these to $W$, which restores part 3 and keeps part 4, since each moved vertex has the neighbor $v \in C_k$. Vertices already in $W$ keep their neighbor in $C_k$. So the invariant holds at line L8.

*Termination of the inner loop.* Each turn removes $v$ from $P$, so $|P|$ falls by at least one, and line L8 exits when $P = \emptyset$.

**Maximality.** At exit, $P = \emptyset$, so by part 1 every vertex of $U_k \setminus C_k$ is in $W$, and by part 4 it has a neighbor in $C_k$. So $C_k$ is an independent set of $G[U_k]$ to which no vertex of $U_k$ can be added: a maximal independent set of $G[U_k]$. Line L6 removed exactly $C_k$ from $U$, so $U_{k+1} = U_k \setminus C_k$.

**Termination of the outer loop.** $C_k$ contains the vertex chosen at line L4, so $|U|$ falls by at least one in each pass, and after at most $n$ passes $U = \emptyset$. Every vertex is colored, because it leaves $U$ only at line L6.

**Properness.** Let $uw$ be an edge. If $c(u) = c(w) = k$, both are in $C_k$, which is independent by part 2, a contradiction. So $c(u) \ne c(w)$.

**The degree bound.** Let $c(v) = j$. For each $i < j$, the vertex $v$ was in $U_i \setminus C_i$, so by maximality it has a neighbor in $C_i$. These $j - 1$ neighbors are distinct, as they have distinct colors, so $j - 1 \le \deg(v)$. ∎
