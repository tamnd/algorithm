---
title: Thorup's VISIT settles every vertex reachable from s at its distance
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be undirected with weights $w : E \to \{1, 2, \ldots\}$ and source $s$, and let $\delta(v) = \delta(s, v)$. For a vertex $v$ and a level $j$, write $C_j(v)$ for the level-$j$ component that holds $v$; for a component $x$ on level $i$ and $j \ge i$, write $C_j(x)$ for the level-$j$ component that holds $x$. Let $R = C_r(s)$; every edge has weight below $2^r$, so $R$ is the connected component of $s$, and no edge joins $R$ to $V \setminus R$.

**Fact 1 (crossing).** If $z \notin C_j(x)$, every path from $z$ to a vertex of $C_j(x)$ has an edge of weight at least $2^j$.

*Proof.* If all its edges had weight below $2^j$, all its vertices would be in one level-$j$ component, which would hold $z$ and meet $C_j(x)$, so it would be $C_j(x)$. $\square$

**Invariants.** At every time, (I1) every settled vertex $u$ has $D(u) = \delta(u)$ and the edges at $u$ have been relaxed in line L7; (I2) every $D(u)$ is $\infty$ or the weight of a path from $s$ to $u$, so $D(u) \ge \delta(u)$. (I2) is clear: $D(s) = 0$, and line L7 extends a path to $v$ by one edge. (I1) is shown below, in Lemma 4.

**Lemma 2 (first unsettled vertex).** Assume (I1). If $u$ is unsettled and $\delta(u) < \infty$, then on every shortest path $P$ from $s$ to $u$ the first unsettled vertex $z$ has $D(z) = \delta(z)$.

*Proof.* If $z = s$, $D(s) = 0 = \delta(s)$, as weights are positive. Otherwise the vertex $p$ before $z$ on $P$ is settled, so by (I1) $D(p) = \delta(p)$ and the edge $\{p, z\}$ was relaxed, giving $D(z) \le \delta(p) + w(p, z) = \delta(z)$, since a prefix of a shortest path is shortest. With (I2), $D(z) = \delta(z)$. $\square$

**The precondition.** For a component $x$ on level $i$ and a vertex $z \notin x$, let $\ell(z, x)$ be the largest $j \in \{i, \ldots, r\}$ with $z \notin C_j(x)$; if $z \notin R$, let $\ell(z, x) = r$. A call VISIT($x$, $i$, hi) *has the precondition* at a given time if

- (P1) when $x \ne R$: every unsettled $u \in x$ has $D(u) \ge \mathrm{hi} - 2^i$, and
- (P2) every unsettled $z \notin x$ has $D(z) + 2^{\ell(z, x)} \ge \mathrm{hi}$.

The root call VISIT($R$, $r$, $\infty$) has it trivially: (P1) does not apply, and a vertex $z \notin R$ has no path from $s$, so $D(z) = \infty$ by (I2). For other calls, hi is a multiple of $2^i$, by line L10.

**Lemma 3 (the precondition holds for the whole call).** If VISIT($x$, $i$, hi) has the precondition when it starts, it has it at every time until it returns, provided (I1) holds.

*Proof.* While the call is active, every vertex settled is in $x$, as every nested call is on a component inside $x$. $D$ values only decrease, by line L7 at a settled vertex $u \in x$. By (P1), when $x \ne R$, $D(u) \ge \mathrm{hi} - 2^i$ at the time $u$ is settled (it was unsettled just before). Consider a relaxation of $\{u, z\}$.

If $z \in x$, the new value is $D(u) + w(u, z) \ge D(u) \ge \mathrm{hi} - 2^i$, so (P1) stays true.

If $z \notin x$, let $\ell = \ell(z, x) \ge i$. Since $u \in x \subseteq C_\ell(x)$ and $z \notin C_\ell(x)$, Fact 1 gives $w(u, z) \ge 2^\ell$. The new value satisfies

$$D(z) + 2^\ell \ge \mathrm{hi} - 2^i + 2^\ell + 2^\ell \ge \mathrm{hi},$$

since $2^\ell \ge 2^i$. So (P2) stays true. For the root, (P2) concerns only vertices outside $R$, which no edge reaches. $\square$

**Lemma 4 (children get the precondition).** Suppose VISIT($x$, $i$, hi) with $i \ge 1$ has the precondition, and line L10 calls VISIT($y$, $i - 1$, $\mathrm{hi}_y$) with $y = C_{i-1}(v)$, $b = \lfloor D(v) / 2^{i-1} \rfloor$ and $\mathrm{hi}_y = (b + 1) 2^{i-1}$, where $v$ has the least $D$ among the unsettled vertices of $x$ and $D(v) < \mathrm{hi}$. Then the child call has the precondition.

*Proof.* (P1) for $y$: every unsettled $u \in y \subseteq x$ has $D(u) \ge D(v) \ge b \cdot 2^{i-1} = \mathrm{hi}_y - 2^{i-1}$.

(P2) for $y$, case $z \in x \setminus y$: then $z \in C_i(y) = x$ and $z \notin C_{i-1}(y) = y$, so $\ell(z, y) = i - 1$. As above, $D(z) \ge D(v) \ge b \cdot 2^{i-1}$, so $D(z) + 2^{i-1} \ge \mathrm{hi}_y$.

(P2) for $y$, case $z \notin x$: $C_j(y) = C_j(x)$ for $j \ge i$, so $\ell(z, y) = \ell(z, x)$, and by (P2) for $x$, $D(z) + 2^{\ell(z, y)} \ge \mathrm{hi}$. Finally $\mathrm{hi}_y \le \mathrm{hi}$: if $\mathrm{hi} = \infty$ this is clear, and otherwise hi is a multiple of $2^i$, hence of $2^{i-1}$, and $b \cdot 2^{i-1} \le D(v) < \mathrm{hi}$ gives $(b + 1) 2^{i-1} \le \mathrm{hi}$. $\square$

**Lemma 5 (settling is correct).** Assume (I1) before line L6 runs in VISIT($\{v\}$, 0, hi), and that this call has the precondition. Then $D(v) = \delta(v)$, so (I1) still holds after lines L6 and L7.

*Proof.* The call comes from line L10 with $i = 1$, so $b = D(v)$ and $\mathrm{hi} = D(v) + 1$; in particular $D(v) < \infty$ and $\delta(v) \le D(v) < \infty$. Suppose $\delta(v) < D(v)$. Take a shortest path $P$ from $s$ to $v$ and its first unsettled vertex $z$; by Lemma 2, $D(z) = \delta(z)$, so $z \ne v$. The part of $P$ from $z$ to $v$ goes from $z \notin \{v\}$ into $C_{\ell}(\{v\})$ with $\ell = \ell(z, \{v\})$, so by Fact 1 it has an edge of weight at least $2^\ell$, and all its weights are positive. Hence, using (P2),

$$\delta(v) \ge \delta(z) + 2^\ell = D(z) + 2^\ell \ge \mathrm{hi} = D(v) + 1 > D(v),$$

which contradicts $\delta(v) < D(v)$. So $D(v) = \delta(v)$. Line L7 then relaxes all edges at $v$, so (I1) holds for $v$. $\square$

By induction over the sequence of calls, Lemmas 3, 4 and 5 show that every call has the precondition when it starts and that (I1) holds throughout.

**Lemma 6 (each child call makes progress).** Every call VISIT($y$, $j$, $\mathrm{hi}_y$) made in line L10 settles at least one vertex.

*Proof.* By induction on $j$. When it is called, $y$ holds an unsettled $v$ with $D(v) < \mathrm{hi}_y$. If $j = 0$, line L6 settles $v$. If $j \ge 1$, the condition of line L8 holds, so the loop runs at least once and makes a call that settles a vertex by induction. $\square$

**Theorem.** THORUP-SSSP terminates and returns $D(v) = \delta(v)$ for every $v$.

*Proof.* Termination: a vertex is settled only while unsettled, so at most $n$ vertices are ever settled. By Lemma 6 every iteration of a loop in line L8 settles a vertex, so each call runs at most $n$ iterations, and the depth of the calls is at most $r + 1$. Hence the algorithm stops.

When the root call returns, the condition of line L8 fails for $R$ with $\mathrm{hi} = \infty$, so every unsettled vertex of $R$ has $D = \infty$. If some $u$ with $\delta(u) < \infty$ were unsettled, Lemma 2 would give an unsettled $z$ on a shortest path to $u$ with $D(z) = \delta(z) < \infty$, and $z \in R$; a contradiction. So every vertex reachable from $s$ is settled, and by (I1) has $D(u) = \delta(u)$. A vertex not reachable from $s$ keeps $D = \infty = \delta(u)$ by (I2). $\blacksquare$
