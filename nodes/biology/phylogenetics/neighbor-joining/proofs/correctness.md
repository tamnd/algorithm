---
title: Neighbor-joining returns the tree of an additive distance matrix
proves: [correctness]
status: full
---

**Setting.** $T$ is an unrooted tree with leaf set $X$, $|X| = r \ge 2$. For $r \ge 3$ every internal vertex has degree 3 (a binary tree); for $r = 2$, $T$ is one edge. Every edge $e$ has a length $w(e) > 0$. For vertices $x, y$, $d(x, y)$ is the length of the unique path $P_{xy}$ between them. $D$ is the restriction of $d$ to $X \times X$. We prove: NEIGHBOR-JOINING on $D$ returns $T$, with the leaf labels and all edge lengths.

For leaves $i \ne j$ write $R_i = \sum_{k \in X} D_{ik}$ and $Q(i, j) = (r-2) D_{ij} - R_i - R_j$, as in lines L3 and L4. For a vertex $v$ of $T$, the *leaf status* is $\ell(v) = \sum_{k \in X} d(v, k)$.

**Fact 1 (attachment point).** Let $i \ne j$ be leaves and $k$ a vertex. Let $m$ be the vertex of $P_{ij}$ closest to $k$, and write $d(k, P_{ij}) = d(k, m)$. Then for every vertex $v$ of $P_{ij}$, $d(k, v) = d(k, m) + d(m, v)$, and if $k$ is a leaf, $d(k, P_{ij}) = \frac{1}{2}\big(D_{ki} + D_{kj} - D_{ij}\big)$.

*Proof.* The path from $k$ to $m$ meets $P_{ij}$ only in $m$, because a second common vertex would be closer to $k$. So the path from $k$ to $m$ followed by the part of $P_{ij}$ from $m$ to $v$ has no repeated vertex. In a tree the path between two vertices is unique, so this is $P_{kv}$, and $d(k, v) = d(k, m) + d(m, v)$. With $v = i$ and $v = j$, and $d(m, i) + d(m, j) = D_{ij}$ because $m$ is on $P_{ij}$, we get $D_{ki} + D_{kj} = 2 d(k, m) + D_{ij}$. $\square$

**Lemma 1 (Q as a path score).** For leaves $i \ne j$ let $z(i, j) = D_{ij} + \sum_{k \in X} d(k, P_{ij})$. Then $Q(i, j) = -2\, z(i, j)$.

*Proof.* For $k \in \{i, j\}$, $d(k, P_{ij}) = 0$. By Fact 1,
$$\sum_{k \in X} d(k, P_{ij}) = \frac{1}{2} \sum_{k \ne i, j} \big(D_{ki} + D_{kj} - D_{ij}\big) = \frac{1}{2}\big((R_i - D_{ij}) + (R_j - D_{ij}) - (r - 2) D_{ij}\big) = \frac{1}{2}\big(R_i + R_j - r D_{ij}\big).$$
Add $D_{ij}$: $z(i, j) = \frac{1}{2}\big(R_i + R_j - (r - 2) D_{ij}\big) = -\frac{1}{2} Q(i, j)$. $\square$

So a pair minimizes $Q$ exactly when it maximizes $z$. A *cherry* is a pair of leaves with a common neighbor, that is, $P_{ij}$ has two edges.

**Lemma 2 (internal vertex bound).** Let $r \ge 3$, let $i \ne j$ be leaves and let $v$ be an internal vertex of $P_{ij}$. Then $z(i, j) \le \ell(v)$, with equality if and only if $i$ and $j$ are both neighbors of $v$.

*Proof.* For each leaf $k$ let $m_k$ be the vertex of $P_{ij}$ closest to $k$. By Fact 1 with $v$ on $P_{ij}$, $d(v, k) = d(k, P_{ij}) + d(v, m_k)$. Sum over $k$:
$$\ell(v) = \sum_{k} d(k, P_{ij}) + \sum_{k} d(v, m_k).$$
Since $m_i = i$, $m_j = j$ and $v$ lies on $P_{ij}$, the terms for $k = i$ and $k = j$ add up to $d(v, i) + d(v, j) = D_{ij}$. The other terms are at least 0. So $\ell(v) \ge z(i, j)$, with equality if and only if $m_k = v$ for every leaf $k \ne i, j$.

If $i$ and $j$ are both neighbors of $v$, then $P_{ij} = (i, v, j)$. A leaf $k \ne i, j$ is not $i$ or $j$, and the path from $k$ to $i$ enters $i$ through its only neighbor $v$, so $v$ is closer to $k$ than $i$ is, and likewise for $j$. Hence $m_k = v$ for all such $k$, and equality holds.

If not, $P_{ij}$ has at least three edges, so it has an internal vertex $y \ne v$. The vertex $y$ has degree 3 and two of its neighbors are on $P_{ij}$, so it has a neighbor $y'$ off the path. Start at $y'$ and walk away from $y$, always to a neighbor not yet visited. Each internal vertex has a neighbor other than the one we came from, and the tree is finite, so the walk stops at a leaf $k$. The path from $k$ to $P_{ij}$ reaches it at $y$, so $m_k = y \ne v$, and $d(v, m_k) > 0$ because all edge lengths are positive. So the inequality is strict. $\square$

**Lemma 3 (status across an edge).** Let $(a, b)$ be an edge of length $\omega$. Removing it splits the leaves into $X_a$ (on the side of $a$) and $X_b$, of sizes $n_a$ and $n_b$. Then $\ell(b) - \ell(a) = \omega (n_a - n_b)$.

*Proof.* For $k \in X_a$ the path from $b$ to $k$ passes through $a$, so $d(b, k) = d(a, k) + \omega$. For $k \in X_b$, $d(a, k) = d(b, k) + \omega$. Sum over all leaves. $\square$

**Lemma 4 (every minimizer of Q is a cherry).** Let $r \ge 3$. If $u, v$ are leaves that are not a cherry, there is a cherry $(a, b)$ with $Q(a, b) < Q(u, v)$.

*Proof.* Let $c$ be a vertex with the smallest leaf status. A leaf $x$ has one neighbor $y$, which is internal because $r \ge 3$, and Lemma 3 with $n_x = 1$ and $n_y = r - 1 \ge 2$ gives $\ell(x) - \ell(y) = w(x, y)(r - 2) > 0$. So $c$ is internal. Root $T$ at $c$. For a vertex $b \ne c$ let $n_b$ be the number of leaves below $b$ and $a$ its parent. The side of $a$ has $r - n_b$ leaves, so by Lemma 3
$$\ell(b) - \ell(a) = w(a, b)\,(r - 2 n_b).$$
For a child $b$ of $c$, $\ell(b) \ge \ell(c)$ by the choice of $c$, so $n_b \le r/2$. If $a \ne c$, then $a$ is an internal non-root vertex with two children, so $n_b \le n_a - 1$, and by induction down the tree $n_b < r/2$, so $\ell(b) > \ell(a)$. Hence $\ell$ never decreases from $c$ to a child, and strictly increases along every other edge directed away from $c$.

Now let $u, v$ be leaves that are not a cherry. Let $x$ be the parent of $u$. Then $x$ is internal and lies on $P_{uv}$, and $u, v$ are not both neighbors of $x$, so $z(u, v) < \ell(x)$ by Lemma 2. Since $x$ is internal, it has a child $s \ne u$.

- If $s$ is a leaf, $(u, s)$ is a cherry at $x$, and $z(u, s) = \ell(x)$ by Lemma 2.
- If $s$ is internal, walk down from $s$: while the current vertex has an internal child, move to one. The tree is finite, so this stops at an internal vertex $m \ne c$ whose two children $a, b$ are leaves. The path from $x$ down to $m$ starts at $x$, so by the monotonicity above $\ell(m) \ge \ell(s) \ge \ell(x)$. The pair $(a, b)$ is a cherry at $m$, and $z(a, b) = \ell(m)$ by Lemma 2.

In both cases there is a cherry with $z \ge \ell(x) > z(u, v)$, and Lemma 1 turns this into $Q < Q(u, v)$. $\square$

**Lemma 5 (branch lengths and reduction).** Let $r \ge 3$ and let $(i, j)$ be a cherry with common neighbor $p$. Then $\delta_{iu}$ and $\delta_{ju}$ of line L6 equal $w(i, p)$ and $w(j, p)$, and for every leaf $k \ne i, j$ the value $D_{uk}$ of line L8 equals $d(p, k)$.

*Proof.* For $k \ne i, j$, $D_{ik} = w(i, p) + d(p, k)$ and $D_{jk} = w(j, p) + d(p, k)$. The term $D_{ij}$ is in both $R_i$ and $R_j$, so
$$R_i - R_j = \sum_{k \ne i, j} (D_{ik} - D_{jk}) = (r - 2)\big(w(i, p) - w(j, p)\big).$$
With $D_{ij} = w(i, p) + w(j, p)$, line L6 gives $\delta_{iu} = \frac{1}{2}\big(w(i,p) + w(j,p)\big) + \frac{1}{2}\big(w(i,p) - w(j,p)\big) = w(i, p)$, and then $\delta_{ju} = D_{ij} - \delta_{iu} = w(j, p)$. Line L8 gives $\frac{1}{2}\big(2 d(p, k) + w(i,p) + w(j,p) - D_{ij}\big) = d(p, k)$. $\square$

**Theorem.** NEIGHBOR-JOINING on $D$ returns $T$ with its edge lengths.

*Proof.* Each pass of the loop only reads the active set and the matrix on it, so the passes from any point on behave as NEIGHBOR-JOINING called on that smaller matrix. We use induction on $r$.

For $r = 2$, $T$ is one edge of length $D_{ab}$, and line L10 returns it.

For $r \ge 3$, line L4 picks a pair $(i, j)$ that minimizes $Q$. By Lemma 4 it is a cherry, with common neighbor $p$. By Lemma 5, line L7 adds the edges $(i, p)$ and $(j, p)$ with their true lengths, where the new node $u$ plays the role of $p$. Let $T'$ be $T$ with $i$ and $j$ removed. The vertex $p$ had degree 3, so in $T'$ it has degree 1 and is a leaf, named $u$; all other degrees are unchanged, and all edge lengths stay positive. So $T'$ is a tree of the same kind with $r - 1$ leaves (for $r = 3$, it is one edge). By Lemma 5 the new matrix after line L9 is exactly the leaf distance matrix of $T'$. By the induction hypothesis the remaining passes return $T'$ with its edge lengths. Adding the two edges of line L7 at $u = p$ gives $T$. $\blacksquare$

**Remarks.** The proof never uses which minimizer line L4 picks, so the result holds for every tie rule. Positive edge lengths matter in Lemma 2: with a zero-length internal edge, a non-cherry can tie with a cherry, and NJ may join it. Lemma 2 and the use of leaf status follow the argument of the note *Neighbor joining and leaf status* (arXiv:2305.18866); Lemma 5 is the standard computation in Studier and Keppler (1988).
