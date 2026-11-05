---
title: Leaf peeling returns the centre of an unweighted tree
proves: [correctness, termination]
status: full
---

Let $T$ be a free tree with $n$ vertices and unit edge lengths. Write $d_T$ for the distance, $\mathrm{ecc}_T$ for the eccentricity and $Z(T)$ for the centre. A *leaf* is a vertex of degree 1.

**Lemma 1.** Let $n \ge 3$, and let $T'$ be $T$ with all leaves removed. Then $T'$ is a tree with at least one vertex, $d_{T'}(u, v) = d_T(u, v)$ for all $u, v$ in $T'$, and $\mathrm{ecc}_{T'}(v) = \mathrm{ecc}_T(v) - 1$ for each $v$ in $T'$.

*Proof.* *Not empty.* Since $T$ is connected with $n \ge 3$ vertices, it has a path with 2 edges, and its middle vertex has degree at least 2, so it is not a leaf.

*Distances.* Let $u, v$ be in $T'$, and let $Q$ be the path from $u$ to $v$ in $T$. Each inner vertex of $Q$ has two neighbours on $Q$, so it has degree at least 2 and is not a leaf. The ends $u$, $v$ are in $T'$. So $Q$ lies in $T'$. Hence $T'$ is connected and $d_{T'} = d_T$ on $T'$. It is acyclic as a subgraph of $T$, so it is a tree.

*Eccentricities.* Let $v$ be in $T'$ and $e = \mathrm{ecc}_T(v)$. Since $n \ge 2$, $e \ge 1$. Let $z$ be a vertex with $d_T(v, z) = e$. If $z$ had a neighbour $y$ that is not on the path from $v$ to $z$, then the path from $v$ to $z$ followed by $y$ would be a path of length $e + 1$, which is impossible. So the only neighbour of $z$ is its neighbour $z'$ on the path to $v$, and $z$ is a leaf. If $z' = v$, then $e = 1$, and $v$ is adjacent to every other vertex (each vertex is at distance at most 1); then $T'$ is the single vertex $v$, and $\mathrm{ecc}_{T'}(v) = 0 = e - 1$. Otherwise $z'$ is an inner vertex of a path, so $z' \in T'$, and $d_{T'}(v, z') = e - 1$. So $\mathrm{ecc}_{T'}(v) \ge e - 1$. Conversely, let $u \ne v$ be in $T'$. Then $u$ is not a leaf, so it has a neighbour $y$ other than its neighbour on the path to $v$, and $d_T(v, y) = d_T(v, u) + 1 \le e$. So $d_{T'}(v, u) \le e - 1$, and $\mathrm{ecc}_{T'}(v) \le e - 1$. $\square$

**Lemma 2.** If $n \ge 3$, then $Z(T') = Z(T)$, where $T'$ is as in Lemma 1.

*Proof.* A leaf $z$ of $T$ is not in $Z(T)$: its neighbour $z'$ has $d(z', u) \le d(z, u) - 1$ for each $u \ne z$ (the path from $z$ to $u$ goes through $z'$), and $d(z', z) = 1 \le \mathrm{ecc}(z) - 1$ because $\mathrm{ecc}(z) \ge 2$ when $n \ge 3$. So $\mathrm{ecc}(z') \le \mathrm{ecc}(z) - 1$. So $Z(T)$ lies in $T'$. By Lemma 1, $\mathrm{ecc}_{T'} = \mathrm{ecc}_T - 1$ on $T'$, so the vertices of $T'$ with the smallest eccentricity are the same in both trees. $\square$

**Invariant of the loop.** At the test of line L4, let $R$ be the set of vertices not yet removed. Then (a) the subgraph $T[R]$ is a tree with $|R| = \mathit{left}$, (b) $\mathrm{deg}[v]$ is the degree of $v$ in $T[R]$ for $v \in R$, and $\mathrm{deg}[v] = 0$ for $v \notin R$, (c) $L$ lists each leaf of $T[R]$ exactly once, and (d) $Z(T[R]) = Z(T)$.

*Initialization.* Line L1 handled $n \le 2$, so $n \ge 3$. After lines L2 and L3, $R = V$, the counters are the degrees, $L$ lists the leaves, and (d) is trivial.

*Maintenance.* Suppose the invariant holds and $\mathit{left} > 2$. In a tree with at least 3 vertices, no two leaves are adjacent (two adjacent leaves would form a component of 2 vertices). So when line L8 removes a leaf $u$ of $L$, its only neighbour in $R$ is not in $L$, and line L9 finds it as the only neighbour with $\mathrm{deg} > 0$; removed vertices have counter 0, and the other leaves of $L$ are not neighbours of $u$. Line L10 lowers its counter by 1. After the loop of line L7, the set $R'$ of vertices left is $R$ minus the leaves of $T[R]$, so $T[R'] = (T[R])'$, which by Lemma 1 is a tree; line L5 set $\mathit{left} = |R'|$. Each counter of a vertex of $R'$ went down by its number of leaf neighbours, so (b) holds for $R'$. A vertex $v \in R'$ is a leaf of $T[R']$ exactly when its counter is now 1. It had a counter of at least 2 before the round, since a vertex with counter 1 was a leaf of $T[R]$ and is removed. So its counter passed through 1 during this round, and line L11 appended it to $L'$ exactly once, at the moment it reached 1. A vertex of $R'$ whose counter went from 2 or more down to 1 and further down to 0 is the single vertex of $T[R']$, since a tree in which a vertex has degree 0 has one vertex; it is in $L'$ too, and it is the only element of $L'$, which is then the vertex set of $T[R']$. So after line L12, (c) holds in the form "L lists the leaves of $T[R']$, or its single vertex". By Lemma 2, $Z(T[R']) = Z(T[R]) = Z(T)$.

*Termination.* Each round removes all leaves of a tree with at least 3 vertices, at least 2 of them, so $\mathit{left}$ drops by at least 2 per round and the loop ends after at most $n/2$ rounds.

**Theorem.** LEAF-PEEL returns $Z(T)$.

*Proof.* For $n \le 2$, every vertex has the same eccentricity ($0$ or $1$), so line L1 is correct. Otherwise, at the end of the loop, $\mathit{left} \in \{1, 2\}$. If $|R| = 2$, $T[R]$ is one edge, both ends are leaves, $L = R$, and both have eccentricity 1 in $T[R]$, so $Z(T[R]) = R$. If $|R| = 1$, then $L = R$ as shown in the maintenance step, and $Z(T[R]) = R$. By (d), $Z(T) = Z(T[R]) = L$, which line L13 returns. $\blacksquare$

**Rounds.** By Lemma 1, each round lowers the eccentricity of the remaining vertices by 1. If the loop ran $k$ rounds and $c = |R|$ vertices are left, the centre has eccentricity $c - 1$ in $T[R]$, so $\mathrm{rad}(T) = k + c - 1$. A diametral path of $T$ has its two ends removed in round 1 (they are leaves), and its rest is a diametral path of $T'$, so the diameter drops by 2 per round and $D(T) = 2k + (c - 1)$.
