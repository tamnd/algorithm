---
title: IKKBZ finds the cheapest left-deep order without cross products for a tree query
proves: [correctness]
status: full
---

**Setting.** The relations are $R_0, \ldots, R_{n-1}$ with sizes $|R_i| > 0$, and the query graph is a tree whose edge $\{i, j\}$ has a selectivity $f_{ij} > 0$. The size of the join of a set $S$ is $|R_S| = \prod_{i \in S} |R_i| \prod_{\{i,j\} \subseteq S} f_{ij}$. A left-deep order $R_{v_1}, \ldots, R_{v_n}$ has no cross product when each $R_{v_k}$, $k \ge 2$, has an edge to some earlier relation. Its cost is $C_{out} = \sum_{k=2}^{n} |R_{\{v_1, \ldots, v_k\}}|$.

Fix a root $r$ and hang the tree from it; $p(v)$ is the parent of $v$. Put $T(v) = f_{v p(v)} |R_v|$ for $v \ne r$. For a sequence $s$ of non-root relations put $T(s) = \prod_{v \in s} T(v)$ and define $C$ by $C(\varepsilon) = 0$, $C(v) = T(v)$ and $C(s_1 s_2) = C(s_1) + T(s_1) C(s_2)$. This is well defined, because both sides of the rule for $C((s_1 s_2) s_3)$ and $C(s_1 (s_2 s_3))$ equal $C(s_1) + T(s_1) C(s_2) + T(s_1) T(s_2) C(s_3)$. Unfolding gives $C(u_1 \cdots u_m) = \sum_{k=1}^{m} T(u_1 \cdots u_k)$. For a nonempty $s$ put $\mathrm{rank}(s) = (T(s) - 1) / C(s)$. All $T$ and $C$ of nonempty sequences are positive. A sequence of the non-root relations is *valid* if every $v$ comes after $p(v)$ (the root counts as placed first).

**Lemma 1 (orders and costs).** The orders without cross products that start with $r$ are exactly $r s$ for the valid sequences $s$, and $C_{out}(r s) = |R_r| \cdot C(s)$.

*Proof.* If $s$ is valid, each $v$ joins its parent, which is earlier. Conversely, take an order $r s$ without cross products and suppose some $v$ comes before $p(v)$; take the first such $v$ in $s$. It has an earlier neighbor, which is not $p(v)$, so it is a child $w$ of $v$. Then $w$ is earlier than $v$ and comes before its parent $v$, which contradicts the choice of $v$. For the cost, a prefix $r u_1 \cdots u_k$ of a valid order is closed under parents, so the tree edges inside it are exactly the edges $\{u_i, p(u_i)\}$, and $|R_{\{r, u_1, \ldots, u_k\}}| = |R_r| T(u_1 \cdots u_k)$. Summing over $k$ gives $|R_r| C(s)$. $\square$

**Lemma 2 (adjacent sequence interchange).** For sequences $U, A, B, V$ with $A$ and $B$ nonempty,
$$C(UABV) - C(UBAV) = T(U)\, C(A)\, C(B)\, (\mathrm{rank}(A) - \mathrm{rank}(B)).$$

*Proof.* $C(UXV) = C(U) + T(U) C(X) + T(U) T(X) C(V)$, and $T(AB) = T(BA)$, so the difference is $T(U)(C(AB) - C(BA))$. Then $C(AB) - C(BA) = C(A) + T(A) C(B) - C(B) - T(B) C(A) = C(B)(T(A) - 1) - C(A)(T(B) - 1) = C(A) C(B) (\mathrm{rank}(A) - \mathrm{rank}(B))$. $\square$

So, in any sequence, exchanging two adjacent blocks $A B$ into $B A$ does not raise the cost when $\mathrm{rank}(A) \ge \mathrm{rank}(B)$, and lowers it when the inequality is strict.

**Lemma 3 (rank of a concatenation).** $\mathrm{rank}(AB)$ is a weighted mean of $\mathrm{rank}(A)$ and $\mathrm{rank}(B)$ with positive weights $C(A)$ and $T(A) C(B)$.

*Proof.* $T(A)T(B) - 1 = (T(A) - 1) + T(A)(T(B) - 1) = C(A)\,\mathrm{rank}(A) + T(A) C(B)\,\mathrm{rank}(B)$, and $C(AB) = C(A) + T(A) C(B)$. $\square$

Lemma 3 is not needed for the proof below, but it explains why the merged head of line L13 has a rank between the ranks of its parts.

**The invariant.** For $v \ne r$ let $L(v) = M_1, \ldots, M_k$ be the list that LINEARIZE returns. Call a valid sequence $s$ *$v$-normal* if the relations of the subtree of $v$ appear in $s$ as the blocks $M_1, \ldots, M_k$, each contiguous, in this order (other relations may lie between the blocks). We show, for the nodes $v$ in post-order:

- (a) the concatenation $M_1 \cdots M_k$ is a valid order of the subtree of $v$ that starts with $v$, and $\mathrm{rank}(M_1) \le \cdots \le \mathrm{rank}(M_k)$;
- (b) every valid $s$ can be changed into a valid $s'$ with $C(s') \le C(s)$ that is $v$-normal and also $w$-normal for every node $w$, outside the subtree of $v$, for which $s$ was $w$-normal.

All changes below move a contiguous block of relations of the subtree of $v$ past a block $X$ that is the whole gap between two such blocks. So $X$ stays contiguous and in order, and a contiguous block of another subtree, which cannot contain a relation of the subtree of $v$, lies entirely inside $X$ or entirely outside the moved span. This gives the second half of (b).

*Proof of (a) and (b).* Let $c_1, \ldots, c_m$ be the children of $v$. By induction (a) and (b) hold for each $c_i$; applying (b) to $c_1, \ldots, c_m$ in turn, we may assume $s$ is $c_i$-normal for all $i$.

*Merge (line L9).* Line L9 sorts all modules of the lists $L(c_i)$ by the key (rank, $i$, position in $L(c_i)$). This order keeps each $L(c_i)$ in its own order, because ranks inside $L(c_i)$ are nondecreasing by (a), so the merged order is a valid order of the subtree of $v$ minus $v$, given $v$ first. In $s$, list the child modules in their order of appearance. If this list is not the merged order, it has two neighbors $P$ before $Q$ with $\mathrm{key}(P) > \mathrm{key}(Q)$. They come from different lists $L(c_i)$ and $L(c_j)$, since the list keeps the order inside each $L(c_i)$ and that order agrees with the keys. Let $X$ be the gap between $P$ and $Q$ in $s$. It holds no relation of the subtree of $v$: $v$ comes before every child module, and the child modules between $P$ and $Q$ are none. No relation of $X$ is an ancestor or a descendant of a relation of $P$ or $Q$, and $P$ and $Q$ are not related either, so every reordering of $P X Q$ that keeps $X$ in order is valid. Note $\mathrm{rank}(P) \ge \mathrm{rank}(Q)$. If $X$ is empty, swap $P$ and $Q$; by Lemma 2 the cost does not rise. Otherwise, if $\mathrm{rank}(X) \le \mathrm{rank}(P)$, change $P X$ into $X P$; else $\mathrm{rank}(X) > \mathrm{rank}(P) \ge \mathrm{rank}(Q)$ and change $X Q$ into $Q X$. By Lemma 2 neither step raises the cost, and now $P$ and $Q$ are adjacent, so swap them. The number of inverted pairs in the list drops by one. Repeat until the child modules appear in the merged order $N_1, N_2, \ldots$.

*Contraction (lines L11 to L13).* Keep the invariant that the current head $H$ (at first the single relation $v$) is contiguous in $s$ and the remaining merged modules follow it in order. Let $N$ be the first remaining module, with $\mathrm{rank}(H) > \mathrm{rank}(N)$, as line L12 requires. Let $X$ be the gap between $H$ and $N$; it holds no relation of the subtree of $v$. The parent of the first relation of $N$ is $v$ or lies in an earlier module of the same $L(c_i)$; that module comes earlier in the merged order, so it is already in $H$. Hence every ancestor of a relation of $N$ is in $H$, in $N$ or before $v$, and no relation of $X$ is related to $H$ or $N$. If $X$ is not empty: when $\mathrm{rank}(X) \le \mathrm{rank}(H)$ change $H X$ into $X H$; otherwise $\mathrm{rank}(X) > \mathrm{rank}(H) > \mathrm{rank}(N)$ and change $X N$ into $N X$. By Lemma 2 the cost does not rise. Now $H N$ is contiguous, which is the new head of line L13.

When the loop stops, the list of line L14 is $H$ followed by the remaining merged modules. Its ranks are nondecreasing: the remaining merged modules are sorted, and $\mathrm{rank}(H) \le \mathrm{rank}(N)$ for the first of them if any is left. $H$ starts with $v$, and the concatenation is valid because the merged order is valid after $v$. This proves (a), and $s$ is now $v$-normal, which proves (b). $\square$

**Theorem.** For each root $r$, the order of lines L3 to L6 is a cheapest order without cross products among those that start with $r$, and its cost is computed correctly. Line L7 keeps the cheapest over all roots, so line L8 returns a cheapest left-deep order without cross products.

*Proof.* Take any order $r s$ without cross products. By Lemma 1, $s$ is valid. Apply (b) to every child $c$ of $r$ and then the merge step above with $v = r$. Every non-root relation lies in the subtree of a child of $r$, so all gaps $X$ are empty and $s$ becomes exactly the merged list that line L10 returns, with cost at most $C(s)$. By Lemma 1 the cost of the result is $|R_r| C(\cdot)$, which is what line L6 computes, since the code folds the modules with the rule $C(s_1 s_2) = C(s_1) + T(s_1) C(s_2)$. Every order starts with some root, and line L2 tries all of them. $\blacksquare$

**Where the hypotheses are used.** Positive sizes and selectivities make every $C$ positive, so the ranks exist and Lemma 2 gives the sign of each exchange. The tree shape gives the parent of each relation, which Lemma 1 needs; on a graph with a cycle, the prefix of a valid order can contain an edge that is not a parent edge, and the cost is no longer $|R_r| C(s)$.
