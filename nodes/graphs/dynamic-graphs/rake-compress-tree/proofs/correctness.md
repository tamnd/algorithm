---
title: The RC-tree represents the forest, and its queries are correct
proves: [correctness]
status: full
---

Let $F$ be the forest with positive or arbitrary integer weights, and fix the coins. For a cluster $K$, let $E(K)$ be its set of edges and $V(K)$ the set of the ends of those edges, together with the vertex $v$ if $K = C(v)$. Write $d(x, y)$ for the weight of the tree path from $x$ to $y$.

**Lemma 1 (no conflicts).** In one round, no two adjacent live vertices are both removed, and no vertex is both chosen and the target of a rake.

*Proof.* A finalized vertex has no live neighbor. If a leaf $v$ rakes into $u$ and $u$ is also removed, then $u$ is not compressed, since a compressing vertex has no leaf neighbor, and $u$ is not finalized, so $u$ rakes, which means $u$ is a leaf whose only neighbor is $v$. Then both are leaves and only the smaller one rakes, a contradiction. Two adjacent compressing vertices would both have heads while each needs the other to have tails. $\square$

So each round is a set of independent local changes, and their order inside the round does not matter.

**Invariant (I).** After every round, with $L$ the live vertices and $\mathcal{T}$ the top clusters (clusters with no parent yet):

1. the sets $E(K)$ for $K \in \mathcal{T}$ partition $E(F)$;
2. each binary $K \in \mathcal{T}$ is a live edge between its two boundary vertices $a, b \in L$, $E(K)$ is the edge set of a subtree of $F$ that contains the path from $a$ to $b$, and its stored weight is $d(a, b)$;
3. each unary $K \in \mathcal{T}$ hangs on one live vertex $u$, its boundary, and $E(K)$ is the edge set of a subtree of $F$ that contains $u$;
4. two distinct clusters of $\mathcal{T}$ share no vertex except a common boundary vertex, and every vertex of $V(K) \setminus \mathrm{bound}(K)$ is removed;
5. two live vertices are in one tree of the live forest if and only if they are in one tree of $F$.

*Proof.* Before round 1, the top clusters are the base clusters, all vertices are live, and the live forest is $F$; all items hold. Assume (I) before a round. By Lemma 1 we may apply the removals one at a time.

A finalize of $v$ joins the unary clusters hanging on $v$, and no binary cluster since $v$ has no live edge, into $C(v)$ with no boundary. By item 4 these clusters meet only at $v$, so $E(C(v))$ is connected and is a subtree; nothing else changes.

A rake of $v$ into $u$ joins the live edge $K_{uv}$ and the unary clusters on $v$ into $C(v)$ with boundary $\{u\}$. Each part is a subtree containing $v$ (items 2 and 3), so the union is a subtree containing $u$. The vertex $v$ leaves $L$; any other vertex of $V(C(v))$ was already interior to a part, hence removed. Removing a leaf does not change connectivity among the other live vertices.

A compress of $v$ with live edges $K_{av}$ and $K_{vb}$ joins them and the unary clusters on $v$ into $C(v)$ with boundary $\{a, b\}$. The union is a subtree that contains the path from $a$ to $v$ and the path from $v$ to $b$. These two paths share only $v$, because $K_{av}$ and $K_{vb}$ share only $v$ (item 4), so their union is the path from $a$ to $b$, and $d(a, b) = d(a, v) + d(v, b)$, the stored sum. The live forest replaces the path $a, v, b$ by the edge $ab$, which keeps connectivity among the live vertices.

In all three cases the new cluster takes the place of its parts in $\mathcal{T}$, so item 1 holds, and it shares with other top clusters only its boundary vertices, which gives item 4. $\square$

**Termination.** In each round with a live vertex, the live forest has a vertex $v$ of degree at most one. If $v$ is isolated it is finalized; if it is a leaf with neighbor $u$, then $v$ rakes, or $u$ is a leaf with $u < v$ and $u$ rakes. So some vertex is removed in every round, so the number of live vertices strictly drops, and the loop ends. When it ends, $L$ is empty, every top cluster has no boundary, and every vertex $v$ owns the cluster $C(v)$ made when it was removed.

**Lemma 2 (connectivity).** $u$ and $v$ are in one tree of $F$ if and only if $C(u)$ and $C(v)$ have the same root.

*Proof.* By item 5 and induction over the rounds, the vertices of one tree of $F$ stay in one live tree until the last of them is finalized, and the clusters on them are joined into the cluster of that last vertex; clusters of different trees never meet, because a new cluster only joins clusters at a common live vertex or a live edge, which lie in one tree. The cluster of a finalized vertex has no parent. So each tree of $F$ gives exactly one root, and $C(x)$ lies below the root of the tree of $x$ because $x \in V(C(x))$ and clusters only grow upward. $\square$

**Lemma 3 (containment).** Let $u$ be a vertex and $K = C(z)$ a cluster on the path from $C(u)$ to its root. Then $u \in V(K)$, and for every $x \in \{z\} \cup \mathrm{bound}(K)$ the tree path from $u$ to $x$ uses only edges of $E(K)$.

*Proof.* $E(K)$ is the edge set of a subtree that contains $u$, $z$ and the boundary vertices (items 2 and 3 at the time $K$ is made, and $u \in V(C(u)) \subseteq V(K)$). In a tree, the path between two vertices of a subtree stays in the subtree. $\square$

**Lemma 4 (the climb).** In the walk up from $C(u)$, after reaching $K = C(z)$, the value stored for each $x \in \{z\} \cup \mathrm{bound}(K)$ is $d(u, x)$.

*Proof.* At $K = C(u)$: $d(u, u) = 0$, and each boundary vertex $x$ of $C(u)$ is the other end of a binary child $B$ of $C(u)$ with boundary $\{u, x\}$, since $\mathrm{bound}(C(u))$ is the set of boundary vertices of its children other than $u$; by item 2, $d(u, x)$ is the weight of $B$.

Step from a child $K'$ to its parent $K = C(z)$, assuming the claim for $K'$. The vertex $z$ is a boundary vertex of $K'$, so $d(u, z)$ is known. Let $x \in \mathrm{bound}(K)$. If $x \in \mathrm{bound}(K')$, its value is already $d(u, x)$. Otherwise $x$ is the other end of a binary child $B \neq K'$ of $K$ with boundary $\{z, x\}$. By Lemma 3 the path from $u$ to $x$ lies in $E(K)$. It starts in $E(K')$ and ends at a vertex not in $V(K')$, since by item 4 the only vertices $K'$ shares with $B$ are common boundary vertices, and $x \notin \mathrm{bound}(K')$. The children of $K$ meet only at $z$, so the path leaves $K'$ through $z$ and then follows the path from $z$ to $x$, which lies in $B$. Hence $d(u, x) = d(u, z) + w(B)$, which is the value set. $\square$

**Lemma 5 (meeting point).** Let $u \neq v$ be connected, and let $K = C(z)$ be the first cluster on the walk up from $C(v)$ that is also on the walk up from $C(u)$. Then $d(u, v) = d(u, z) + d(z, v)$.

*Proof.* By Lemma 2 such a $K$ exists. If $u = z$ or $v = z$ the claim is trivial. Otherwise $u$ lies in a child $A$ of $K$ and $v$ in a child $B$ of $K$, with $A \neq B$ by the choice of $K$. By Lemma 3 the path from $u$ to $v$ lies in $E(K)$. All children of $K$ have $z$ in their boundary, and by item 4 at the time $K$ was made, two of them share only the vertex $z$. Inside the subtree $E(K)$, which is the union of the children's subtrees, the path from a vertex of $A$ to a vertex of $B$ must therefore pass through $z$. $\square$

**Theorem.** After any sequence of links and cuts, connected$(u, v)$ is true exactly when $u$ and $v$ are in one tree, and path weight$(u, v)$ returns $d(u, v)$ for connected $u$ and $v$.

*Proof.* Each update rebuilds the contraction for the current forest, so (I) and the lemmas apply to it. Connectivity is Lemma 2. For path weight, the walk from $C(v)$ stops at the cluster $C(z)$ of Lemma 5, and by Lemma 4 applied to both walks the returned value is $d(u, z) + d(z, v) = d(u, v)$; for $u = v$ the walk stops at $C(u)$ and returns $0 + 0$. $\blacksquare$
