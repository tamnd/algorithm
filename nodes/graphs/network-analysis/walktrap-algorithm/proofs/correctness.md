---
title: Walktrap merges by the least increase of sigma and ends with one community per component
proves: [correctness, termination]
status: full
---

We use the notation of the page. After line L1, $A$ is symmetric with positive diagonal, $d(k) > 0$ for every $k$, and $P = D^{-1} A$. Let $v_i = D^{-1/2} P^t_{i\cdot} \in \mathbb{R}^n$, and for a set $C$ let $\bar v_C = \frac{1}{|C|} \sum_{i \in C} v_i$. Then $D^{-1/2} P^t_{C\cdot} = \bar v_C$ by linearity, so $r_{C_1 C_2} = \|\bar v_{C_1} - \bar v_{C_2}\|$ and $r_{iC} = \|v_i - \bar v_C\|$. For a set $C$ write $W(C) = \sum_{i \in C} \|v_i - \bar v_C\|^2$, so that $\sigma(\mathcal{P}) = \frac{1}{n} \sum_{C \in \mathcal{P}} W(C)$.

**Lemma 1 (Ward's identity).** For disjoint non-empty sets $C_1, C_2$, $W(C_1 \cup C_2) - W(C_1) - W(C_2) = \frac{|C_1|\,|C_2|}{|C_1| + |C_2|} \|\bar v_{C_1} - \bar v_{C_2}\|^2$.

*Proof.* For any set $C$ and any point $x$, $\sum_{i \in C} \|v_i - x\|^2 = W(C) + |C|\, \|\bar v_C - x\|^2$, because the cross term $2 \sum_{i \in C} (v_i - \bar v_C) \cdot (\bar v_C - x)$ is 0. Let $C = C_1 \cup C_2$, $s_1 = |C_1|$, $s_2 = |C_2|$, and $\mu = \bar v_C = (s_1 \bar v_{C_1} + s_2 \bar v_{C_2}) / (s_1 + s_2)$. Splitting the sum over $C$ and applying the identity to $C_1$ and to $C_2$ with $x = \mu$ gives $W(C) = W(C_1) + s_1 \|\bar v_{C_1} - \mu\|^2 + W(C_2) + s_2 \|\bar v_{C_2} - \mu\|^2$. Now $\bar v_{C_1} - \mu = \frac{s_2}{s_1 + s_2} (\bar v_{C_1} - \bar v_{C_2})$ and $\bar v_{C_2} - \mu = -\frac{s_1}{s_1 + s_2} (\bar v_{C_1} - \bar v_{C_2})$, so the two extra terms add to $\frac{s_1 s_2^2 + s_2 s_1^2}{(s_1 + s_2)^2} \|\bar v_{C_1} - \bar v_{C_2}\|^2 = \frac{s_1 s_2}{s_1 + s_2} \|\bar v_{C_1} - \bar v_{C_2}\|^2$. $\square$

So merging $C_1$ and $C_2$ changes $\sigma$ by exactly $\Delta\sigma(C_1, C_2) = \frac{1}{n} \frac{|C_1||C_2|}{|C_1| + |C_2|} r_{C_1 C_2}^2$, since the other communities are unchanged.

Call two disjoint sets *adjacent* if some edge of $G$ (not a loop) joins them.

**Lemma 2 (invariants).** Before each test of line L5: (a) the current communities partition $V$; (b) each community $C$ has stored vector $\bar v_C$; (c) the table holds an entry for a pair of current communities exactly when they are adjacent, and the entry equals $\Delta\sigma$ of the pair; (d) each community induces a connected subgraph of $G$.

*Proof.* Initially (lines L2 and L3) the communities are the singletons, with $\bar v_{\{i\}} = v_i$; the pairs in the table are the edges, with value $\frac{1}{n} \cdot \frac{1 \cdot 1}{2} \|v_i - v_j\|^2$, which is $\Delta\sigma$; and singletons are connected. Suppose the invariants hold and lines L6 to L8 merge $C_1$ and $C_2$, which are adjacent by (c). (a) The new set of communities is again a partition. (b) Line L7 sets the vector of $C_3$ to $\frac{|C_1| \bar v_{C_1} + |C_2| \bar v_{C_2}}{|C_1| + |C_2|} = \bar v_{C_3}$, and the other vectors are unchanged. (c) The entries with $C_1$ or $C_2$ are removed. A community $C \ne C_3$ is adjacent to $C_3$ exactly when it is adjacent to $C_1$ or to $C_2$, and line L8 adds an entry for each such $C$, with value $\Delta\sigma(C, C_3)$ by (b). Entries between two other communities are unchanged and still correct, as their communities and vectors did not change. (d) $C_1$ and $C_2$ are connected and joined by an edge, so their union is connected. $\square$

**Lemma 3 (termination).** The loop of lines L5 to L9 runs at most $n - 1$ times, and when it stops, the communities are exactly the connected components of $G$.

*Proof.* Each round reduces the number of communities by one, and there is at least one community while $n \ge 1$, so there are at most $n - 1$ rounds. When the loop stops, no two communities are adjacent. By Lemma 2(d) each community lies inside one component. If a component contained two communities, then, the component being connected, some edge would join two different communities inside it, and they would be adjacent, a contradiction. $\square$

**Theorem.** WALKTRAP$(G, t)$ stops. Each merge it performs joins the pair of adjacent communities whose union increases $\sigma$ the least (the smallest pair of ids among equal increases), and the dendrogram ends with one community per connected component. The returned partition is the one of largest modularity among the partitions of the dendrogram, the earliest among equal ones.

*Proof.* Termination and the final partition are Lemma 3. By Lemma 2(c) the table at line L6 holds the value $\Delta\sigma$ for exactly the adjacent pairs, and by Lemma 1 this value is the increase of $\sigma$ caused by the merge, so line L6 picks the pair with the least increase, with the stated tie rule. Line L9 records every partition of the dendrogram, and line L10 scans them in order and keeps the first maximum of modularity. $\blacksquare$
