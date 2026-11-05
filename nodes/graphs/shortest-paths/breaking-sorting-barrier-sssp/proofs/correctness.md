---
title: The bounded multi-source recursion computes all distances
proves: [correctness, termination]
status: full
---

**Claim.** Let every edge weight be a real number $w(u, v) \ge 0$. The top call BMSSP$(\lceil \log_2 (n+1) / t \rceil, \infty, \{s\})$ of line L12 terminates, and afterwards $\hat d(v) = \delta(s, v)$ for every vertex $v$, with $\hat d(v) = \infty$ exactly when $s$ does not reach $v$. This holds for every choice of the parameters $k \ge 1$ and $t \ge 1$; the values $k = \lfloor \log^{1/3} n \rfloor$ and $t = \lfloor \log^{2/3} n \rfloor$ matter only for the running time.

**Keys.** Following the total order of paths in Duan et al. (their Assumption 2.1), compare walks by their *key*: the length, then the number of edges, then the vertex sequence read from the end, lexicographically. We use three facts.

- (K1) The keys form a total order, and two different walks have different keys.
- (K2) For walks $Q, Q'$ that end at the same vertex $u$, and an edge $(u, v)$: $\mathrm{key}(Q) < \mathrm{key}(Q')$ if and only if $\mathrm{key}(Q + v) < \mathrm{key}(Q' + v)$.
- (K3) $\mathrm{key}(Q + v) > \mathrm{key}(Q)$, because the edge count grows by one and $w \ge 0$.

Every label $\hat d(v)$ is the key of a walk from $s$ to $v$, or $\infty$. Write $d(v)$ for the smallest key of a walk from $s$ to $v$. It exists: deleting a cycle from a walk does not increase the length and decreases the edge count, so the minimum is over the finitely many simple paths. The walk $P_v$ with key $d(v)$ is unique by (K1), and by (K2) its prefix that ends at the previous vertex $u$ is $P_u$. So the paths $P_v$ form a tree, and $d(v)$ starts with $\delta(s, v)$. A vertex is *complete* when $\hat d(v) = d(v)$.

Relaxing $(u, v)$ forms the candidate $c = \hat d(u) + w(u, v)$, the key of the walk of $u$ extended by $v$, and sets $\hat d(v) \leftarrow c$ when $c \le \hat d(v)$. Labels never increase and never go below $d$. If $u$ is complete and $(u, v)$ is the last edge of $P_v$, the relaxation makes $v$ complete, because then $c = d(v) \le \hat d(v)$. Conversely, if a relaxation from $u$ leaves $\hat d(v) = c = d(v)$, then by (K2) $u$ is complete and is the vertex before $v$ on $P_v$.

**Notation.** For a call with bound $B$ and frontier $S$, and a key $b$, let $\tilde U(b)$ be the set of vertices $v$ with $d(v) < b$ whose path $P_v$ visits a vertex of $S$. A call is *proper* if, when it starts,

- (P1) $\hat d(x) < B$ for every $x \in S$, and
- (P2) every incomplete vertex $v$ with $d(v) < B$ has a complete vertex of $S$ on $P_v$.

We prove that a proper call terminates and returns $(B', U)$ with

- (R1) $B' \le B$;
- (R2) every vertex of $\tilde U(B')$ is in $U$, and every vertex of $U$ is complete and in $\tilde U(B)$;
- (R3) $B' > \min_{x \in S} \hat d(x)$, where the labels are taken at the start of the call.

The proof is by induction on the level $l$. First, two facts about any proper call.

**Fact A (cover).** In a proper call, every $v \in \tilde U(B)$ has a complete vertex of $S$ on $P_v$. If $v$ is incomplete this is (P2). If $v$ is complete, let $x \in S$ be on $P_v$. If $x$ is complete we are done; otherwise $d(x) \le d(v) < B$ and (P2) gives a complete vertex of $S$ on $P_x$, which is a prefix of $P_v$.

**Fact B (where the relaxations go).** Suppose that during a proper call a relaxation from a vertex $u \in \tilde U(B)$ gives $c \le \hat d(v)$ and $c < B$. Then $v \in \tilde U(B)$. Indeed $d(v) \le c < B$. If $v$ was incomplete at the start of the call, (P2) puts a vertex of $S$ on $P_v$. If $v$ was complete, then $c \le \hat d(v) = d(v) \le c$, so $u$ is the vertex before $v$ on $P_v$ and $P_v = P_u + v$ visits $S$.

**Lemma 1 (base case, level 0).** A proper call with $S = \{x\}$ runs Dijkstra's algorithm from $x$, pushing only candidates below $B$, and stops after $k + 1$ vertices are popped. By (P2), $x$ is complete: otherwise $d(x) \le \hat d(x) < B$ and (P2) would need a complete vertex of $S = \{x\}$ on $P_x$.

*Every popped vertex is complete when it is popped.* Suppose $u$ is the first popped vertex that is not. Then $d(u) < \hat d(u) < B$, and by (P2) $P_u$ visits $x$. Let $y$ be the last vertex of $P_u$ that was popped before $u$ (there is one, $x$), and $z$ its successor on $P_u$. When $y$ was popped it was complete, and relaxing $(y, z)$ set $\hat d(z) = d(z) < B$ and pushed $z$ with key $d(z)$, since $z$ was not yet popped. That entry stays valid, and $d(z) \le d(u) < \hat d(u)$, so $z$ is popped before $u$ unless $z = u$; in both cases we get a contradiction. The keys popped are increasing by (K3), and $x$ is popped first.

*The result.* If at most $k$ vertices are popped, the heap ran empty, $B' = B$, and $U$ is the set of popped vertices. Otherwise $B'$ is the key of the last popped vertex, and $U$ is the popped vertices with smaller keys. In both cases every $v \in \tilde U(B')$ is popped: if not, take the last popped vertex $y$ on $P_v$ and its successor $z$; as above $z$ was pushed with key $d(z) \le d(v) < B'$, so it would have been popped before the last pop. Every popped vertex is complete and lies in $\tilde U(B)$ by Fact B. So (R1) and (R2) hold. For (R3), $B' = B > \hat d(x)$ by (P1), or $B'$ is the key of a vertex popped after $x$, so $B' > \hat d(x)$ by (K3).

**Lemma 2 (FindPivots).** In a proper call, after line L3, every $v \in \tilde U(B)$ is in $W$ and complete, or has a complete vertex of $P$ on $P_v$. Also $P \subseteq S$ and $W \subseteq \tilde U(B)$.

*Proof.* $W \subseteq \tilde U(B)$: $S \subseteq \tilde U(B)$ by (P1), and every other vertex enters $W$ through a relaxation from a vertex of $W$ with a candidate below $B$, so Fact B applies.

Let $v \in \tilde U(B)$. By Fact A, $P_v$ has a vertex of $S$ that is complete at the start; let $y_0$ be the last one, and $y_0, z_1, \ldots, z_j = v$ the rest of $P_v$. By induction on $i$, after round $i \le \min(j, k)$ the vertex $z_i$ is complete and in the next layer: round $i$ relaxes from $z_{i-1}$ ($y_0$ is in the first layer, all of $S$), the candidate is $d(z_i) \le \hat d(z_i)$, and it is below $B$.

If FindPivots returns early with $P = S$, then $y_0 \in P$ is complete and on $P_v$. If $j \le k$, then $v$ is complete and in $W$. Otherwise $z_1, \ldots, z_k$ are complete and in $W$.

In the last case, consider the forest $F$ on $W$: $(p, q)$ is an edge when $p$ is the stored predecessor of $q$, $p \in W$, and $\hat d(q) = \hat d(p) + w(p, q)$. Each vertex has at most one parent, and keys increase along edges by (K3), so $F$ is a forest. The edges $(y_0, z_1), (z_1, z_2), \ldots, (z_{k-1}, z_k)$ are in $F$, since these vertices are complete and $P_{z_i} = P_{z_{i-1}} + z_i$.

If $q$ is complete and $(p, q) \in F$, then $\hat d(p) + w = d(q) \le d(p) + w$, so $\hat d(p) = d(p)$ by (K2), and $P_q = P_p + q$. So every ancestor in $F$ of a complete vertex is complete and lies on its path. Let $r$ be the root of the tree of $y_0$. Then $r$ is complete and on $P_{y_0}$, a prefix of $P_v$.

We claim $r \in S$. If not, $r$ entered $W$ when a relaxation during FindPivots set its label. At the last such time, its label became $\hat d(p) + w$ with $p \in W$ the new predecessor. If $\hat d(p)$ later dropped, then $\hat d(p) + w < \hat d(r) = d(r)$, which is impossible. So $(p, r) \in F$ and $r$ is not a root.

So $r$ is a root in $S$ whose tree has at least $k + 1$ vertices, hence $r \in P$. $\square$

**Lemma 3 (the loop).** Consider a proper call at level $l \ge 1$, and let done be the union of the sets $U_i$ returned so far. Call $v \in \tilde U(B) \setminus$ done *pending*. Before every iteration, and when the loop stops:

- (J0) every vertex in done is complete and in $\tilde U(B)$; every value in $D$ is below $B$, and it is at least $B'_i$ of the last subcall, if there was one;
- (J) every pending $v$ satisfies one of the following:
  - (a) $v \in W$ and $v$ is complete;
  - (b) $P_v$ contains a vertex of done; for the last such vertex, its successor $z$ on $P_v$ is complete and is a key of $D$ with value $d(z)$;
  - (c) $P_v$ contains no vertex of done, and some complete vertex $x$ on $P_v$ is a key of $D$ with value $d(x)$.

Also, every key of $D$ lies in $\tilde U(B)$.

*Start.* done is empty, and $D$ holds the pivots with their labels. By Lemma 2 each pending $v$ satisfies (a) or (c). Pivots are in $S \subseteq \tilde U(B)$.

*Values.* $D$ keeps the smaller value when a key is inserted again. A key $z$ with value $d(z)$ keeps that value until it is pulled, since no candidate is below $d(z)$.

*The subcall is proper.* Line L6 pulls the keys with values below $B_i$; values are keys of different vertices, so they are distinct. If $D$ is left empty, $B_i = B$. The vertices of done are then removed from $S_i$.

- (P1) holds because $\hat d(x)$ is at most the value of $x$ in $D$, which is below $B_i$.
- For (P2), let $v$ be incomplete with $d(v) < B_i \le B$. By (P2) of this call and Fact A, $v \in \tilde U(B)$. It is not in done, because those vertices are complete, and it is not in case (a). In case (b) or (c), the vertex $z$ or $x$ has value at most $d(v) < B_i$, so it was pulled. It is not in done, so it is in $S_i$, and it is complete and on $P_v$.

If $S_i$ ends up empty, no subcall happens, and the iteration only removes keys of done vertices; such keys are never the $z$ or $x$ of (J). So (J0) and (J) still hold.

*After the subcall.* By induction, the subcall returns with (R1) to (R3) for $(B_i, S_i)$. Every vertex of $S_i$ is a key of $D$, so it lies in $\tilde U(B)$. Hence every vertex of $U_i$ is complete, and its path visits $S_i$ and so $S$, which keeps done inside $\tilde U(B)$. Relaxations from $U_i$ in line L8 insert or prepend only candidates $c$ with $B'_i \le c < B$; by Fact B these vertices lie in $\tilde U(B)$. All other keys have values at least $B_i \ge B'_i$. So (J0) holds.

*(J) after the iteration.* Let $v$ be pending afterwards. Case (a) persists, so assume $v$ is not in case (a).

- If $P_v$ meets done, let $y$ be the last vertex of $P_v$ in done and $z$ its successor; $z$ is complete, because $P_z = P_y + z$ and the edge was relaxed after $y$ became complete.
  - If $y \in U_i$, line L8 relaxed $(y, z)$ and the candidate is $d(z) < B$. If $d(z) < B'_i$, then $z \in \tilde U_i(B'_i) \subseteq U_i$ (as $P_z$ visits $S_i$), which contradicts the choice of $y$. So $d(z) \ge B'_i$, and line L9 or line L10 put $z$ into $D$ with value $d(z)$.
  - If $y$ was in done before, then (J) before the iteration gave $z$ as a key with value $d(z)$. If $z$ was pulled now, it is in $S_i$ and not in $U_i$. Then $d(z) \ge B'_i$, because otherwise $z \in \tilde U_i(B'_i) \subseteq U_i$. So line L10 prepends it again with value $\hat d(z) = d(z) < B_i$.
- If $P_v$ does not meet done, then before the iteration it was in case (c) with some $x$. If $x$ was pulled, $x \notin U_i$, so as above $d(x) \ge B'_i$, and line L10 puts it back with value $d(x)$.

*Termination of the loop.* Take a subcall. Let $y \in S_i$ have the smallest label at the start of the subcall. By (R3), $B'_i > \hat d(y) \ge d(y)$, so $y \in \tilde U_i(B'_i) \subseteq U_i$. Since $y$ is not in done, done grows by at least one vertex. So there are at most $n$ subcalls, and between two of them each iteration removes keys without adding any. Every iteration pulls at least one key, so the loop stops. $\square$

**Lemma 4 (the result of the call).** A proper call at level $l \ge 1$ satisfies (R1) to (R3).

(R1) holds by line L11. For (R2), let $v \in \tilde U(B')$, and suppose $v$ is pending. Cases (b) and (c) give a key with value at most $d(v) < B'$. But when the loop stops, either $D$ is empty, or every value is at least $B'_i$ of the last subcall, which is at least $B'$, by (J0). So $v$ is in case (a): $v \in W$, complete, with $\hat d(v) < B'$, and line L11 adds it to $U$. Every vertex added to $U$ is in done, which is complete and in $\tilde U(B)$ by (J0), or is a vertex of $W$ with $\hat d < B'$. Such a vertex lies in $\tilde U(B')$ by Lemma 2, so it is in done or in case (a), and in both cases it is complete.

For (R3): if there was no subcall, $B' = B > \hat d(x)$ for every $x \in S$ by (P1). Otherwise $B' = \min(B'_i, B)$ for the last subcall. $B$ is larger than every label in $S$. By (R3) of the subcall, $B'_i > \hat d(y) \ge d(y)$ for some $y \in S_i$. By Fact A, $P_y$ has a vertex $x \in S$ that is complete at the start, and $d(y) \ge d(x) = \hat d(x)$, because $d$ does not decrease along $P_y$. $\blacksquare$ (lemma)

**The top call.** With $S = \{s\}$, $B = \infty$ and $\hat d(s) = 0$ the call is proper: $s$ is complete, and every reachable $v$ has $s$ on $P_v$. Its level $L = \lceil \log_2(n+1)/t \rceil$ gives $k \cdot 2^{Lt} \ge n + 1 > |\text{done}|$, so the loop stops only when $D$ is empty. Then (J) leaves only case (a): every reachable vertex is in done or in $W$, and complete. So $\hat d(v) = d(v)$, whose first entry is $\delta(s, v)$. A vertex that $s$ does not reach is never the target of a relaxation from a finite label, so it keeps $\hat d = \infty$. The recursion depth is $L$, every FindPivots is $k$ rounds, every base case pops each vertex at most once, and every loop stops by Lemma 3, so the algorithm terminates.

**The stored keys.** The implementation stores only the first four entries of a key: (length, edge count, $v$, predecessor). Labels of different vertices differ in the third entry. Two candidates for the same vertex with the same four entries come from the same predecessor $u$, with the same length and edge count for $u$. For these, the code compares with $\le$ and keeps the newer one. Its full key is never larger, because the label of $u$ only decreases. So every comparison of stored labels agrees with the comparison of full keys, except between two such candidates; they have equal lengths, so the distances are not affected. $\blacksquare$
