---
title: The full reducer removes all dangling tuples, and the join phase computes the projected join
proves: [correctness, complexity]
status: full
---

Notation. The join tree has nodes $u$ with attribute sets $A_u$ and relations $R_u$. It satisfies the *running intersection property*: for each attribute, the nodes that hold it form a connected subtree. Let $\mathrm{sub}(u)$ be the subtree rooted at $u$, $A_{\mathrm{sub}(u)}$ its attributes, and $J_{\mathrm{sub}(u)} = \bowtie_{w \in \mathrm{sub}(u)} R_w$. Let $J$ be the join of all relations. For a set of tuples $S$ over attributes $X$ and $Y \subseteq X$, $\pi_Y S$ is the projection.

**Lemma 0 (separation).** Let $c$ be a child of $u$. Then $A_{\mathrm{sub}(c)} \cap A_w \subseteq A_c \cap A_u$ for each node $w \notin \mathrm{sub}(c)$, and two different children $c, c'$ of $u$ have $A_{\mathrm{sub}(c)} \cap A_{\mathrm{sub}(c')} \subseteq A_u$.

*Proof.* The path in the tree from a node of $\mathrm{sub}(c)$ to a node outside it goes through $c$ and $u$. If an attribute is held by both ends, by the running intersection property it is held by every node on the path, so by $c$ and $u$. The second claim is the same with a path through $u$. $\square$

**Lemma 1 (bottom-up pass).** After the pass of line L1 has handled all children of $u$, $R_u = \pi_{A_u} J_{\mathrm{sub}(u)}$, where the join is of the original relations.

*Proof.* By induction over the post-order. A leaf is not changed, and $J_{\mathrm{sub}(u)} = R_u$. For an inner node $u$ with children $c_1, \ldots, c_j$, the pass sets $R_u \leftarrow R_u \ltimes R_{c_1} \ltimes \cdots \ltimes R_{c_j}$, and by induction $R_{c_i} = \pi_{A_{c_i}} J_{\mathrm{sub}(c_i)}$. A tuple $t \in R_u$ is in $\pi_{A_u} J_{\mathrm{sub}(u)}$ if and only if for each $i$ some $s_i \in J_{\mathrm{sub}(c_i)}$ agrees with $t$ on $A_u \cap A_{\mathrm{sub}(c_i)}$; the tuples $t, s_1, \ldots, s_j$ then combine into one tuple, because by Lemma 0 two of them share only attributes of $A_u$, where all agree with $t$. By Lemma 0, $A_u \cap A_{\mathrm{sub}(c_i)} = A_u \cap A_{c_i}$, so the condition says that $t$ agrees with some tuple of $\pi_{A_{c_i}} J_{\mathrm{sub}(c_i)} = R_{c_i}$ on the shared attributes, which is the semijoin test. $\square$

**Lemma 2 (top-down pass).** After the pass of line L2, $R_u = \pi_{A_u} J$ for each node $u$.

*Proof.* By induction over the pre-order. For the root, Lemma 1 gives $R_{\mathrm{root}} = \pi J$, and line L2 does not change it. Let $c$ be a child of $u$ with $R_u = \pi_{A_u} J$, and let $R'_c = \pi_{A_c} J_{\mathrm{sub}(c)}$ be the value from Lemma 1. Line L2 sets $R_c \leftarrow R'_c \ltimes R_u$.

If $y \in J$, then $y[A_c] \in R'_c$ and it agrees with $y[A_u] \in R_u$, so $y[A_c]$ stays. Conversely, let $s \in R'_c$ agree with $t \in R_u$ on $A_c \cap A_u$. Then $s = x[A_c]$ for some $x \in J_{\mathrm{sub}(c)}$, and $t = y[A_u]$ for some $y \in J$. By Lemma 0, $x$ and the restriction of $y$ to the attributes outside $\mathrm{sub}(c)$ share only attributes of $A_c \cap A_u$, on which $x$ agrees with $s$, $s$ with $t$, and $t$ with $y$. So they combine into a tuple of $J$ whose restriction to $A_c$ is $s$. $\square$

**Theorem 1 (full reducer).** After lines L1 and L2, each $R_u$ equals $\pi_{A_u} J$. In particular, no tuple is dangling: each remaining tuple is part of some output tuple, and if $J$ is empty, all relations are empty.

*Proof.* This is Lemma 2. Since semijoins only remove tuples, the join of the reduced relations is still $J$. $\blacksquare$

**Theorem 2 (join phase).** Let $O$ be the output attributes, and let $X_u = (A_u \cap A_{\mathrm{parent}(u)}) \cup (O \cap A_{\mathrm{sub}(u)})$, with $A_{\mathrm{parent}(u)} = \emptyset$ for the root. Line L6 gives $J_u = \pi_{X_u} J_{\mathrm{sub}(u)}$, computed from the reduced relations, and line L7 returns $\pi_O J$.

*Proof.* By induction over the post-order. Line L5 joins $R_u$ with the $J_c$ of the children. An attribute of $J_{\mathrm{sub}(c)}$ that is not in $X_c$ is not in $A_u$ and not in $O$. By Lemma 0 it appears nowhere outside $\mathrm{sub}(c)$, so it takes no part in any later join, and dropping it before the join gives the same projection as dropping it after. Hence $R_u \bowtie J_{c_1} \bowtie \cdots \bowtie J_{c_j}$ equals the projection of $J_{\mathrm{sub}(u)}$ on $A_u \cup \bigcup_i X_{c_i}$, and line L6 projects it on $X_u$. At the root, $X_{\mathrm{root}} = O$, and $J_{\mathrm{sub}(\mathrm{root})}$ is the join of the reduced relations, which is $J$ by Theorem 1. $\blacksquare$

**Theorem 3 (cost).** Let $n = \sum_u |R_u|$, $N_{\mathrm{out}} = |\pi_O J|$, and let $r$ be the number of nodes. With hash tables, lines L1 and L2 take $O(r \cdot n)$ expected time in the worst case and $O(n)$ for a fixed query. For a full join ($O$ is all attributes), the join phase takes $O(n + r \cdot N_{\mathrm{out}})$ expected time, and each intermediate result has at most $N_{\mathrm{out}}$ tuples. With projections, each $J_u$ has at most $|R_u| \cdot N_{\mathrm{out}}$ tuples, and the time is $O(r \cdot n \cdot N_{\mathrm{out}})$ for $N_{\mathrm{out}} \ge 1$.

*Proof.* Each semijoin builds a hash set of one relation and probes it with the other, so each tree edge costs $O(|R_u| + |R_{\mathrm{parent}(u)}|)$ in each pass. For a full join, after the full reducer the reduced relations are globally consistent, so the join of $R_u$ with any set of children's results is a projection of $J$ by the argument of Theorem 2, and has at most $|J| = N_{\mathrm{out}}$ tuples. A hash join takes time linear in its two inputs and its output, so each of the $r - 1$ joins costs $O(|R_u| + N_{\mathrm{out}})$. With projections, the partial results at line L5 have attributes in $A_u \cup O$, and each of their tuples is a tuple of $\pi_{A_u} J \subseteq R_u$ joined with a tuple of $\pi_{O'} J$ for some $O' \subseteq O$. The second set has at most $N_{\mathrm{out}}$ elements, so each partial result and each $J_u$ has at most $|R_u| \cdot N_{\mathrm{out}}$ tuples, and each hash join costs $O(n \cdot N_{\mathrm{out}})$. $\blacksquare$
