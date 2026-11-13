---
title: The Felzenszwalb-Huttenlocher algorithm keeps Int exactly and returns a segmentation that is neither too fine nor too coarse, for any non-decreasing order of the edges
proves: [correctness]
status: full
---

Fix a graph $G = (V, E)$ with weights $w(e) \ge 0$ and a threshold function $\tau \ge 0$ on sets of nodes; the algorithm uses $\tau(C) = k/|C|$, but the proof only needs $\tau \ge 0$. Let $o_1, \ldots, o_m$ be the edges in the order used at line L3, with $w(o_1) \le \cdots \le w(o_m)$, and let $S^q$ be the partition of $V$ given by the forest after the first $q$ edges. Write $t(C) = \mathrm{Int}(C) + \tau(C)$, so $\mathrm{MInt}(C_1, C_2) = \min(t(C_1), t(C_2))$. Merges only join sets, so every component of $S^q$ is contained in a component of $S^r$ for $q \le r$, and in a component of the final segmentation $S = S^m$.

**Lemma 0 (Int as a bottleneck).** For a connected set $C$, let $b(C)$ be the least $x$ such that the edges of $E$ inside $C$ with weight at most $x$ connect $C$, and $b(C) = 0$ if $|C| = 1$. Then $\mathrm{Int}(C) = b(C)$ for every minimum spanning tree of $C$.

*Proof.* Let $T$ be a minimum spanning tree of $C$ with heaviest edge $e$ of weight $W$. The edges of $T$ have weight at most $W$ and connect $C$, so $b(C) \le W$. Suppose the edges of weight less than $W$ connect $C$. Removing $e$ splits $T$ into two parts, and some edge $f$ with $w(f) < W$ joins them. Then $T - e + f$ is a spanning tree of $C$ lighter than $T$, a contradiction. So $b(C) = W$. $\square$

**Lemma 1 (a rejected edge leaves a final component).** Let $o_q$ join two different components $A$ and $B$ of $S^{q-1}$ and be rejected at line L6, so $w(o_q) > t(A)$ or $w(o_q) > t(B)$; say $w(o_q) > t(A)$. Then $A$ is a component of $S$.

*Proof.* We show by induction on $r \ge q$ that $A$ is a component of $S^r$. It is one of $S^q$, because $o_q$ caused no merge. If $A$ is a component of $S^{r-1}$ and $o_r$ joins $A$ to another component $Z$, then $w(o_r) \ge w(o_q) > t(A) \ge \min(t(A), t(Z))$, so $o_r$ is rejected and $A$ is still a component of $S^r$. Edges that do not touch $A$ do not change $A$. $\square$

This uses the true $\mathrm{Int}(A)$, and Lemma 2 shows that line L6 reads the true value.

**Lemma 2 (merging edges and Int).** If $o_q$ merges the components $A$ and $B$ of $S^{q-1}$, then $o_q$ is a lightest edge between $A$ and $B$, and $\mathrm{Int}(A \cup B) = w(o_q)$. Hence the value stored at line L8 is the true internal difference of each component, at every step, and every component is connected.

*Proof.* By induction on $q$; singletons have $\mathrm{Int} = 0$, which line L2 stores. Suppose some edge $o_p$ with $p < q$ joins $A$ and $B$. At step $p$ its ends were in components $A' \subseteq A$ and $B' \subseteq B$, which are different because $A$ and $B$ are still different at step $q - 1$. The edge was not merged, for the same reason, so it was rejected, and by Lemma 1 one of $A'$ and $B'$ is a component of the final $S$. But $A' \subseteq A$ and $B' \subseteq B$ are proper subsets of $A \cup B$, which lies in one component of $S$, so neither of them is a component of $S$, which is a contradiction. So every edge between $A$ and $B$ comes at or after $o_q$ in the order and has weight at least $w(o_q)$. Now apply Lemma 0 to $C = A \cup B$. The edges inside $A$ with weight at most $\mathrm{Int}(A) \le w(o_q)$ connect $A$, the same holds for $B$, and $o_q$ joins them, so $b(C) \le w(o_q)$. Every path inside $C$ from $A$ to $B$ uses an edge between $A$ and $B$, of weight at least $w(o_q)$, so the edges lighter than $w(o_q)$ do not connect $C$ and $b(C) \ge w(o_q)$. Here $\mathrm{Int}(A) \le w(o_q)$ holds because $\mathrm{Int}(A)$ is the weight of an earlier merging edge (or 0). Connectivity follows from the merging edges. $\square$

Lemma 2 says that the merging edges are those that Kruskal's algorithm picks for each final component, and that one assignment at line L8 keeps Int exact.

**Theorem 1 (not too fine).** For every two components $C_i \ne C_j$ of $S$, $D(C_i, C_j)$ is true.

*Proof.* If no edge joins them, $\mathrm{Dif} = \infty$ and $D$ is true. Otherwise let $o_q$ be the first edge in the order between $C_i$ and $C_j$, so $w(o_q) = \mathrm{Dif}(C_i, C_j)$. At step $q$ its ends are in components $A \subseteq C_i$ and $B \subseteq C_j$, which are different, and the edge is rejected, since otherwise $A \cup B$ would lie in one final component. By Lemma 1, one of them is final and has its threshold below $w(o_q)$; say $A = C_i$ and $w(o_q) > t(A) = t(C_i)$. Then $\mathrm{Dif}(C_i, C_j) > t(C_i) \ge \mathrm{MInt}(C_i, C_j)$. $\square$

**Theorem 2 (not too coarse).** No proper refinement of $S$ into connected parts is not too fine.

*Proof.* Let $T$ be a proper refinement. Some component $C$ of $S$ is split into two or more parts of $T$, and since $C$ is connected, some edge inside $C$ joins two different parts. Among all edges inside a component of $S$ that join two different parts of $T$, let $e$ be the first in the order, and let it join the parts $A$ and $B$, both inside the component $C$ of $S$. Every edge between $A$ and $B$ is such an edge, so it is not before $e$, and $\mathrm{Dif}(A, B) = w(e)$. Suppose, for a contradiction, that $D(A, B)$ holds. Then $w(e) > \mathrm{MInt}(A, B)$, and say $w(e) > t(A)$, so $w(e) > \mathrm{Int}(A)$.

Every edge from $A$ to $C \setminus A$ is inside $C$ and joins two parts of $T$, so it is not before $e$, and its weight is at least $w(e)$. Let $f$ be the first such edge in the order, and look at the moment just before $f$ is processed.

First, the component $X$ of a node of $A$ at that moment lies in $A$. $X$ lies in $C$, and it is connected by merging edges processed before $f$. If $X$ had a node outside $A$, one of these merging edges would join $A$ to $C \setminus A$ before $f$, which is impossible.

Second, $A$ is one component at that moment. Take an edge $g$ of a minimum spanning tree of $A$. Then $w(g) \le \mathrm{Int}(A) < w(e) \le w(f)$, so $g$ was processed before $f$. When $g$ was processed, it was inside one component, or it was merged, or it was rejected. If it was rejected, Lemma 1 makes one of its two components final, so that component equals $C$. But that component lies in $A$ by the first point, and $A \ne C$ because $C$ also contains $B$. So $g$ was never rejected, its two ends are in one component, and since the tree connects $A$, all of $A$ is in one component, which by the first point is exactly $A$.

Since $A \ne C$ and $A \subseteq C$, the component $A$ is merged later. Let $g'$ be the edge of the first merge of $A$, which joins $A$ to a component $Z$. $Z$ lies in $C$ and is disjoint from $A$, so $g'$ is an edge from $A$ to $C \setminus A$, and $w(g') \ge w(e)$. Line L6 accepted it, so $w(g') \le \min(t(A), t(Z)) \le t(A) < w(e) \le w(g')$, a contradiction. Hence $D(A, B)$ is false, and $T$ is too fine. $\square$

**Theorem 3 (order independence).** All non-decreasing orders of the edges give the same segmentation.

*Proof.* Two non-decreasing orders list the same edges in the same blocks of equal weight, so one can be turned into the other by swaps of adjacent edges of equal weight. It is enough to show that one such swap gives the same partition after both edges, because by Lemma 2 the partition fixes Int and the sizes, which are all that later steps read. Let $e_1$ and $e_2$ have the same weight $w$, and let $S'$ be the partition before them.

If an edge has both ends in one component of $S'$, it does nothing in either order, since sets only grow. If $e_1$ and $e_2$ touch four different components, neither changes what the other sees. If both join the same two components $A$ and $B$, the first one in either order applies the test $w \le \mathrm{MInt}(A, B)$, and the second one is then inside one set, or faces the same test and fails again.

The remaining case is that $e_1$ joins $A$ and $B$, and $e_2$ joins $B$ and $Z$, with $A$, $B$ and $Z$ different. Let $\alpha$, $\beta$ and $\zeta$ be the truth values of $w \le t(A)$, $w \le t(B)$ and $w \le t(Z)$. A merged set made at this weight has $\mathrm{Int} = w$ and so $t \ge w$, which means a later test against it passes on its side. With $e_1$ first: $A$ and $B$ merge if $\alpha \wedge \beta$; then $Z$ joins if $\zeta$. Otherwise $B$ and $Z$ merge if $\beta \wedge \zeta$. With $e_2$ first: $B$ and $Z$ merge if $\beta \wedge \zeta$; then $A$ joins if $\alpha$. Otherwise $A$ and $B$ merge if $\alpha \wedge \beta$. Checking the five cases: if $\beta$ is false, nothing merges in either order. If $\alpha$, $\beta$ and $\zeta$ hold, both orders give $A \cup B \cup Z$. If only $\alpha \wedge \beta$ holds, both give $A \cup B$ and $Z$. If only $\beta \wedge \zeta$ holds, both give $A$ and $B \cup Z$. If only $\beta$ holds, nothing merges. $\square$

The postprocessing pass for a minimum size, which merges small components without the test of line L6, is outside these theorems.
