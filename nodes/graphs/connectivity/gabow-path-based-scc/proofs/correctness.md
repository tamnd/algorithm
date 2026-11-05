---
title: The path-based method pops exactly the strong components
proves: [correctness]
status: full
---

Let $G = (V, E)$ be a directed graph; loops and parallel edges are allowed. Write $x \leadsto y$ when $G$ has a directed path from $x$ to $y$, with $x \leadsto x$ always. At any moment of PATH-BASED-SCC, a vertex is *new* if $\mathrm{pre} = 0$, *active* if it is on $S$, and *done* if it has a component. The *call stack* is the list of vertices whose VISIT has started and not ended; it is a path $p_1, \ldots, p_h$ of the [depth-first forest](/dfs-forest/), and $\mathrm{pre}$ increases along it. Let $B = (b_1 < \cdots < b_r)$ and let $\rho_q$ be the vertex with $\mathrm{pre}[\rho_q] = b_q$. The *block* $T_q$ is the set of active $x$ with $b_q \le \mathrm{pre}[x] < b_{q+1}$ (with $b_{r+1} = \infty$).

We show that the following hold at each moment between lines.

- **(I1)** $S$ holds the active vertices in increasing preorder. Each $\rho_q$ is on the call stack, and every vertex on the call stack is active. If $S$ is not empty, $b_1 \le \mathrm{pre}$ of every active vertex, so the blocks partition the active vertices.
- **(I2)** Any two vertices of one block reach each other.
- **(I3)** If the edge $(x, w)$ has been scanned at line L5 and $x$ is active, then $w$ is done or $w$ is in the block of $x$.
- **(I4)** Every edge out of a done vertex ends at a done vertex.

Also, **(I5)** when VISIT$(v)$ reaches line L9, $\mathrm{top}(B) \le \mathrm{pre}[v]$, and $\mathrm{pre}[v]$ is the only entry of $B$ that can be $\ge \mathrm{pre}[v]$.

*At the start* every vertex is new, and all claims hold trivially.

*Lines L3 and L4.* The new vertex $v$ gets the largest preorder number so far, so pushing it keeps $S$ in preorder, and pushing $\mathrm{pre}[v]$ keeps $B$ increasing. The new block is $\{v\}$, and $v$ is on the call stack. Since $\mathrm{pre}[v]$ is larger than every older number, no older vertex changes block. (I2) to (I4) are untouched.

*Proof of (I5).* At line L4 the top of $B$ is $\mathrm{pre}[v]$. Each child call VISIT$(w)$ from line L6 ends, by (I5) for $w$ and lines L9 to L11, with every entry of $B$ at most $\mathrm{pre}[w]$ and with the entry $\mathrm{pre}[w]$ itself removed if it was there; so its pushes are gone and all entries are again at most the entries present before the call. Line L8 only pops. So at line L9 every entry is at most $\mathrm{pre}[v]$, and the entries pushed before $v$ are smaller. This also shows the first part of (I1) for $B$: after VISIT$(v)$ ends, no entry equals $\mathrm{pre}[v]$, so every entry belongs to a vertex still on the call stack.

*Line L8.* Here $v$ is the current vertex, the last on the call stack, and $w$ is active, say $w \in T_q$. By (I1) $v$ is in the top block $T_r$, since $\mathrm{pre}[v] \ge b_r$ (the entry $b_r$ belongs to a vertex on the call stack, which is an ancestor of $v$ or $v$). We show that all vertices of $T_q \cup \cdots \cup T_r$ reach each other. For each $j$ with $q \le j < r$, the vertex $\rho_{j+1}$ is a descendant of $\rho_j$ in the forest, since both are on the call stack, so $\rho_j \leadsto \rho_{j+1}$, and also $\rho_r \leadsto v$. By (I2) each vertex of $T_j$ reaches $\rho_j$ and back. So every vertex of these blocks reaches $v$ through $\rho_j \leadsto \cdots \leadsto \rho_r \leadsto v$. Conversely, $v \to w$ is an edge, $w \leadsto \rho_q$ by (I2), and $\rho_q$ reaches every $\rho_j$ with $j \ge q$ and hence every vertex of $T_j$. So the union is mutually reachable. Line L8 pops exactly $b_r, \ldots, b_{q+1}$, the entries greater than $\mathrm{pre}[w]$, because $b_q \le \mathrm{pre}[w] < b_{q+1}$. This merges $T_q, \ldots, T_r$ into one block and keeps (I2). Merging only unites blocks, so (I3) stays true. After this step $w$ is in the block of $v$, which gives (I3) for the edge $(v, w)$.

*The other cases of an edge $(v, w)$.* If $w$ is done, (I3) holds for this edge. If $w$ was new, VISIT$(w)$ runs and returns; then $w$ is done, or $w$ is active with $\mathrm{pre}[w] > \mathrm{pre}[v] \ge \mathrm{top}(B)$ by (I5) for the call of $w$ and since all entries now belong to the call stack, which ends at $v$. Then $v$ and $w$ are both in the top block, and (I3) holds.

*Lines L9 to L11.* Suppose $\mathrm{top}(B) = \mathrm{pre}[v]$. The top block is $T = \{x \text{ active} : \mathrm{pre}[x] \ge \mathrm{pre}[v]\}$, and by (I1) these are exactly the entries of $S$ from $v$ to the top, which line L11 pops. Each $x \in T$ was reached after $v$ and before the end of VISIT$(v)$, so $x = v$ or $x$ is a descendant of $v$ whose VISIT has ended; in both cases all edges out of $x$ have been scanned. By (I3), each edge out of $T$ ends in $T$ or at a done vertex, and by (I4) a done vertex reaches only done vertices. So every vertex reachable from $v$ is in $T$ or done, and no done vertex reaches $v$. Hence the strong component of $v$ lies in $T$, and by (I2) it contains $T$. So line L11 gives one strong component the label $c$. Afterwards (I4) holds: the edges out of the new done vertices end in $T$ or at done vertices. (I1) holds because the popped vertices are exactly the vertices with $\mathrm{pre} \ge \mathrm{pre}[v]$, and $v$ leaves the call stack. If $\mathrm{top}(B) < \mathrm{pre}[v]$, nothing changes, and $v$ stays active in a block whose first vertex is a proper ancestor of $v$, so (I1) still holds after $v$ leaves the call stack.

**Theorem.** PATH-BASED-SCC labels each vertex with its strong component, and the labels are in reverse topological order of the condensation.

*Proof.* Line L2 starts VISIT at every vertex that is still new, so every vertex is reached. When the outer call VISIT$(r)$ reaches line L9, the call stack is $r$ alone, so by (I1) and (I5) $B = (\mathrm{pre}[r])$ and the test holds; every active vertex is popped. So when line L2 ends, every vertex is done, and by the case of lines L9 to L11 each label class is one strong component. Each component gets one label, because its vertices leave $S$ together. If an edge leads from a component $C$ to a different component $C'$, then at the moment $C$ closes, every edge out of $C$ ends at a done vertex, so $C'$ closed earlier and has a smaller label. Each line runs a bounded number of times per vertex or per edge, so the method also ends. $\blacksquare$
