---
title: Branch and reduce returns a maximum independent set
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. For a graph $H$, $\alpha(H)$ is the largest size of an independent set of $H$. A pair $(H, I)$ is *valid* if $H$ is an induced subgraph of $G$, $I$ is independent in $G$, and no vertex of $I$ is in $H$ or adjacent to a vertex of $H$. Then $I \cup J$ is independent in $G$ for every independent set $J$ of $H$. Define the value of a valid pair as $\mathrm{val}(H, I) = |I| + \alpha(H)$.

**Lemma 1 (reductions).** Each of lines L5, L6 and L7 turns a valid pair into a valid pair with the same value.

*Proof.* Line L5: $v$ has no neighbor in $H$. The new pair is valid, and $\alpha(H) = \alpha(H - v) + 1$, since a maximum independent set of $H - v$ plus $v$ is independent, and an independent set of $H$ minus $v$ is one of $H - v$.

Line L6: $v$ has one neighbor $u$. The new pair $(H - N[v], I \cup \{v\})$ is valid, as the only neighbor of $v$ in $H$ is deleted. Let $J$ be a maximum independent set of $H$. If $u \in J$, then $J - u + v$ is independent, since $v$ has no other neighbor, and has the same size. If $J$ has neither, $J + v$ is independent, a contradiction with maximality. So some maximum $J$ contains $v$ and not $u$, and $J - v$ is independent in $H - N[v]$. Hence $\alpha(H - N[v]) \ge \alpha(H) - 1$, and the other inequality holds as any independent set of $H - N[v]$ plus $v$ is independent in $H$.

Line L7: $uv$ is an edge and $N[v] \subseteq N[u]$. Clearly $\alpha(H - u) \le \alpha(H)$. Let $J$ be a maximum independent set of $H$ with $u \in J$. Then $J \cap N[u] = \{u\}$, so $J$ has no vertex of $N[v] - \{u\} \subseteq N[u] - \{u\}$, and $J - u + v$ is independent in $H - u$ with the same size. So $\alpha(H - u) = \alpha(H)$. Validity is kept as only $u$ is deleted. $\square$

**Lemma 2 (leaves).** At line L9, every vertex of $H$ has degree exactly 2, $H$ is a disjoint union of cycles, and the set added at line L9 is an independent set of $H$ of size $\alpha(H)$.

*Proof.* The loop of line L4 ends only when lines L5 and L6 do not apply, so no vertex has degree 0 or 1, and line L8 gives degree at most 2. A graph with all degrees 2 is a disjoint union of cycles. In a cycle $c_0, \ldots, c_{k-1}$, the vertices $c_0, c_2, \ldots, c_{2(\lfloor k/2 \rfloor - 1)}$ are pairwise non-adjacent, since the largest index is at most $k - 2$ and, when $k$ is odd, at most $k - 3$, so it is not adjacent to $c_0$. Each vertex of a cycle lies on two of its $k$ edges, and each edge has at most one end in an independent set $J$, so $2 |J| \le k$ and $|J| \le \lfloor k/2 \rfloor$. $\square$

**Lemma 3 (branching).** At lines L11 and L12, both children are valid, and $\mathrm{val}(H, I) = \max(\mathrm{val}(H - v, I), \mathrm{val}(H - N[v], I \cup \{v\}))$.

*Proof.* Both children are valid, as in Lemma 1. A maximum independent set $J$ of $H$ either does not contain $v$, so it is one of $H - v$, or contains $v$ and none of $N(v)$, so $J - v$ is one of $H - N[v]$. Conversely, an independent set of $H - v$, or one of $H - N[v]$ plus $v$, is independent in $H$. $\square$

**Claim 4 (invariant).** At the start of each iteration of line L2, $\max(|best|, \max_{(H, I) \in Q} \mathrm{val}(H, I)) = \alpha(G)$, every pair on the stack is valid, and $best$ is independent in $G$.

*Proof.* At the start, $Q$ holds $(G, \emptyset)$ with value $\alpha(G)$, and $best = \emptyset$. In an iteration, the popped pair keeps its value through line L4 by Lemma 1. If it is a leaf, Lemma 2 makes $I$ an independent set of $G$ of size $\mathrm{val}(H, I)$, and line L9 keeps the larger of it and $best$. Otherwise, by Lemma 3, the value of the popped pair is the larger of the values of the two pushed pairs. In both cases the maximum is unchanged. It is never above $\alpha(G)$ since every value is the size of an independent set of $G$. $\square$

**Claim 5 (termination).** Each pushed child has fewer vertices than its parent, as line L11 deletes $v$ and line L12 deletes $N[v] \ni v$, and each reduction deletes at least one vertex. So the stack holds at most $n + 1$ pairs at any time, every path of the tree has at most $n$ branches, and the loop ends. $\square$

**Theorem.** BRANCH-AND-REDUCE-MIS$(G)$ returns a maximum independent set of $G$.

*Proof.* By Claim 5 the loop ends with $Q$ empty. Claim 4 then gives $|best| = \alpha(G)$, and $best$ is independent in $G$. $\blacksquare$
