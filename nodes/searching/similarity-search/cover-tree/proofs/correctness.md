---
title: Correctness of cover tree insertion and nearest neighbor search
proves: [correctness]
status: full
---

Let $(M, \delta)$ be a metric space and $S$ the stored points, with the levels $C_i$ as on the page. A tree is **valid** if it satisfies nesting, covering and separation for every $i$, and $C_{\text{top}} = \{\text{root}\}$ with $C_i = \{\text{root}\}$ for $i \ge \text{top}$.

**Lemma 1 (descendants).** In a valid tree, every descendant $r$ of a node $(q, j)$ satisfies $\delta(q, r) \le 2^{j+1}$, and if $r \in C_l$ with $l < j$ then $\delta(q, r) \le 2^{j+1} - 2^{l+1}$.

*Proof.* The path from $(q, j)$ down to $(r, l)$ passes through nodes $(q_m, m)$ for $m = j, j-1, \dots, l$, with $q_j = q$, $q_l = r$, and $\delta(q_{m}, q_{m-1}) \le 2^m$ by covering. By the triangle inequality $\delta(q, r) \le \sum_{m = l+1}^{j} 2^m = 2^{j+1} - 2^{l+1} < 2^{j+1}$. $\square$

**Lemma 2 (the sets $Q_j$).** In every call INSERT$(p, Q_j, j)$ made from the top call, $Q_j \subseteq C_j$ and $Q_j \supseteq \{r \in C_j : \delta(p, r) \le 2^{j+1}\}$. The same holds for the sets $Q_j$ of NEAREST with $2^{j+1}$ replaced by $\delta(p, Q) + 2^{j+1}$, where $Q$ is the set computed at the level above.

*Proof.* At the top, $Q_{\text{top}} = \{\text{root}\} = C_{\text{top}}$. Suppose the claim holds for $Q_i$, and let $r \in C_{i-1}$ with $\delta(p, r) \le 2^i$. Its parent $s \in C_i$ satisfies $\delta(r, s) \le 2^i$ by covering, so $\delta(p, s) \le 2^{i+1}$ and $s \in Q_i$. Then $r \in \text{Children}(Q_i, i)$, and line L3 keeps it. Every element of Children$(Q_i, i)$ is in $C_{i-1}$ by nesting and the definition of children. $\square$

**Lemma 3 (termination).** If $\delta(p, r) > 0$ for every $r \in S$, the recursion of INSERT has finite depth.

*Proof.* Let $m = \min_{r \in S} \delta(p, r) > 0$. A call at level $j$ with $2^j < m$ finds $\delta(p, Q) \ge m > 2^j$ at line L2 and returns without recursion. $\square$

**Lemma 4 (failure means far).** If INSERT$(p, Q_j, j)$ returns "no parent found", then $\delta(p, r) > 2^l$ for every $l \le j$ and every $r \in C_l$.

*Proof.* By induction on the recursion, from the deepest call up, which is possible by Lemma 3.

*Return at line L2.* Then $\delta(p, q) > 2^j$ for every $q \in \text{Children}(Q_j, j)$, which by Lemma 2 contains every $r \in C_{j-1}$ with $\delta(p, r) \le 2^j$. So $\delta(p, r) > 2^j$ for all $r \in C_{j-1}$, and since $C_j \subseteq C_{j-1}$ this covers $l = j$ and $l = j - 1$. For $l < j - 1$ and $r \in C_l$, let $a$ be the ancestor of $r$ in $C_{j-1}$. By Lemma 1, $\delta(a, r) \le 2^j - 2^{l+1}$, so $\delta(p, r) \ge \delta(p, a) - \delta(a, r) > 2^j - (2^j - 2^{l+1}) = 2^{l+1} > 2^l$.

*Return at line L5.* The call at level $j - 1$ returned "no parent found", so by induction the claim holds for all $l \le j - 1$. Also $\delta(p, q) > 2^j$ for all $q \in Q_j$, and by Lemma 2 every $r \in C_j$ with $\delta(p, r) \le 2^{j+1}$ is in $Q_j$; so every $r \in C_j$ has $\delta(p, r) > 2^j$, which is the case $l = j$. $\square$

**Theorem 1 (insertion keeps the tree valid).** Let the tree be valid, and let $p$ be at positive distance from every point of $S$. After raising top until $\delta(p, \text{root}) \le 2^{\text{top}}$, INSERT$(p, \{\text{root}\}, \text{top})$ returns "parent found", and the new tree is valid.

*Proof.* Raising top adds levels that hold only the root; they are valid. In the top call, the root is in Children$(\{\text{root}\}, \text{top})$ at distance at most $2^{\text{top}}$, so line L2 does not fail; if the recursive call fails, the root is within $2^{\text{top}}$ at line L5, so the top call returns "parent found". Exactly one call executes line L6, at some level $i$, after the call at level $i - 1$ failed. The new tree adds $p$ to $C_l$ for every $l \le i - 1$.

*Nesting* holds since $p$ is added to all levels below $i - 1$ as its own child. *Covering:* at level $i - 1$ the parent of $p$ is $q \in Q_i \subseteq C_i$ with $\delta(p, q) \le 2^i$; below it, $p$ is its own parent. Other points keep their parents. *Separation:* for $l \le i - 1$ and $r \in C_l$, Lemma 4 applied to the failed call at level $i - 1$ gives $\delta(p, r) > 2^l$. Pairs not involving $p$ are unchanged. $\square$

**Theorem 2 (search).** In a valid tree, NEAREST$(p)$ returns a point $r \in S$ with $\delta(p, r) = \min_{s \in S} \delta(p, s)$.

*Proof.* Let $p^*$ be a nearest point. For each level $j$ from top down to bottom, let $a_j$ be the ancestor of $p^*$ in $C_j$ (with $a_j = p^*$ when $p^* \in C_j$). We show $a_j \in Q_j$ by induction. $a_{\text{top}}$ is the root. Suppose $a_i \in Q_i$. Then $a_{i-1}$ is a child of $a_i$ at level $i - 1$, so $a_{i-1} \in Q = \text{Children}(Q_i, i)$. By Lemma 1 applied to the node $(a_{i-1}, i - 1)$, $\delta(a_{i-1}, p^*) \le 2^i$, so
$$\delta(p, a_{i-1}) \le \delta(p, p^*) + 2^i \le \delta(p, Q) + 2^i,$$
since $p^*$ is nearest overall. Line L9 keeps $a_{i-1}$.

At the end the loop has produced $Q_{\text{bottom}}$. Every point appears in some explicit list at a level at least bottom, or is the root, so $p^* \in C_{\text{bottom}}$ and $a_{\text{bottom}} = p^*$. Hence $p^* \in Q_{\text{bottom}}$, and line L10 returns a point at distance at most $\delta(p, p^*)$, which is the minimum. $\blacksquare$

**Space.** Each insertion executes line L6 once and adds one entry to one child list; a duplicate adds one entry to a duplicate list. So the explicit tree has exactly $n - 1$ entries for $n$ points, and the space is $O(n)$ for every metric.
