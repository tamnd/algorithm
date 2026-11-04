---
title: Bentley's sweep returns the area of the union of the rectangles
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The rectangles are $R_i = [a_i, b_i] \times [c_i, d_i]$ with $a_i \le b_i$ and $c_i \le d_i$, for $i = 1, \ldots, n$. We write $|A|$ for the length (one-dimensional Lebesgue measure) of a set $A \subseteq \mathbb{R}$ and $\mu$ for the area. For a node $u$ with index range $[l_u, r_u)$, let $Y_u = [Y[l_u], Y[r_u]]$ be its $y$-range. The leaves are the elementary intervals, and the two children of a node split its index range in two non-empty parts. If $n = 0$, the loop does not run and line L10 returns 0, which is correct. Assume $n \ge 1$.

**Termination.** The loop runs $2n$ times. Each UPDATE call either returns at line L11 or L12, or calls UPDATE on the two children of a node that is not a leaf. (A leaf $u$ has $r_u = l_u + 1$, so it is either disjoint from $[lo, hi)$ or inside it, and it never reaches line L13.) The depth grows by one at each call, so the recursion stops at the leaves.

**Canonical nodes.** For $0 \le lo \le hi \le m - 1$, let $C(lo, hi)$ be the set of nodes $u$ with $[l_u, r_u) \subseteq [lo, hi)$ whose parent range is not inside $[lo, hi)$ (or $u$ is the root). The ranges of the nodes of $C(lo, hi)$ are pairwise disjoint, and their union is $[lo, hi)$: each index $j \in [lo, hi)$ is in the leaf $[j, j+1)$, which is inside $[lo, hi)$, and the highest ancestor of that leaf whose range is inside $[lo, hi)$ is the unique node of $C(lo, hi)$ that contains $j$. So $\bigcup_{u \in C(lo, hi)} Y_u = [Y[lo], Y[hi]]$ when $lo < hi$.

**Lemma 1.** UPDATE$(root, lo, hi, v)$ changes $cnt[u]$ by $v$ for each $u \in C(lo, hi)$ and for no other node. It changes $len$ only at the nodes on the paths from the root to the nodes of $C(lo, hi)$.

*Proof.* By induction on the depth, a call UPDATE$(u, lo, hi, v)$ is made exactly for the nodes $u$ whose parent range meets $[lo, hi)$ but is not inside it (and for the root). For such a $u$, line L11 returns if its range is disjoint from $[lo, hi)$; line L12 applies if its range is inside $[lo, hi)$, and then $u \in C(lo, hi)$ by definition; otherwise line L13 calls both children, which again have a parent that meets but is not inside $[lo, hi)$. Each node of $C(lo, hi)$ has such a parent (or is the root), so it is reached, and line L12 runs there. Lines L14 to L16 run only at nodes that are called and do not return at line L11. A called node that returns at line L11 changes nothing. A called node that does not return meets $[lo, hi)$, so it is on a path from the root to a node of $C(lo, hi)$. $\square$

**Lemma 2 (counts).** Let $t$ be the moment just before the first event with coordinate $x$ is processed. Call rectangle $i$ *active at $t$* if $a_i < x \le b_i$. Then at $t$, for each node $u$, $cnt[u]$ is the number of rectangles $i$ active at $t$ with $c_i < d_i$ and $u \in C(\operatorname{idx}(c_i), \operatorname{idx}(d_i))$.

*Proof.* By Lemma 1 and induction over the events, $cnt[u]$ is the sum, over the events processed so far, of $v$ if $u$ is in the set $C$ of the event's rectangle, and 0 otherwise. If $c_i = d_i$, the set $C$ is empty and rectangle $i$ adds nothing. At $t$, the events processed so far are exactly those with coordinate less than $x$, since line L3 sorts by $x$. So rectangle $i$ with $u \in C$ adds $+1$ if $a_i < x$ and $-1$ if $b_i < x$. Since $a_i \le b_i$, it adds 1 if $a_i < x \le b_i$ and 0 otherwise. $\square$

Between these moments, inside a group of events with the same $x$, a count can be off (for example $-1$ when a rectangle with $a_i = b_i$ has its $-1$ event sorted first). The proof uses the counts only at the moments of Lemma 2.

**Lemma 3 (node invariant).** After each event, for each node $u$,
$$len[u] = \Big|\bigcup \{\, Y_w : w \text{ in the subtree of } u,\ cnt[w] > 0 \,\}\Big|.$$

*Proof.* Call the right side $L(u)$. At the start all counts and lengths are 0, so both sides are 0. Assume the claim before an event. By Lemma 1 the event changes counts only at nodes of $C$, and lines L14 to L16 run at each node on the paths from the root to those nodes, after the calls on its children. The value $L(u)$ can change only if a count in the subtree of $u$ changes, and then $u$ is on one of those paths. So it is enough to show that lines L14 to L16 compute $L(u)$ when the values of the children are already right. We check the three cases.

- If $cnt[u] > 0$: $Y_u$ is in the union, and each $Y_w$ for $w$ below $u$ is inside $Y_u$. So $L(u) = |Y_u| = Y[r_u] - Y[l_u]$, as line L14 sets.
- If $cnt[u] = 0$ and $u$ is a leaf: the union is empty, so $L(u) = 0$, as line L15 sets.
- If $cnt[u] = 0$ and $u$ has children $u_1, u_2$: the union is the union of the two unions for $u_1$ and $u_2$. These lie in $Y_{u_1}$ and $Y_{u_2}$, which share at most one point. So $L(u) = L(u_1) + L(u_2) = len[u_1] + len[u_2]$, as line L16 sets.

Nodes not on the paths keep both $len[u]$ and $L(u)$. $\square$

**Lemma 4 (covered length).** At a moment $t$ of Lemma 2, $len[root] = \big|\bigcup_{i \text{ active at } t} [c_i, d_i]\big|$.

*Proof.* By Lemma 3, $len[root]$ is the length of the union of $Y_w$ over the nodes with $cnt[w] > 0$. By Lemma 2, these are the nodes of $C(\operatorname{idx}(c_i), \operatorname{idx}(d_i))$ for the active $i$ with $c_i < d_i$. For such $i$, the union of these $Y_w$ is $[c_i, d_i]$. An active $i$ with $c_i = d_i$ adds a single point, of length 0. So both sides are the length of the same set, up to a finite set of points. $\square$

**Theorem.** UNION-AREA returns $\mu\big(\bigcup_{i=1}^{n} R_i\big)$.

*Proof.* Let $x_1 < x_2 < \cdots < x_s$ be the distinct values among all $a_i$ and $b_i$.

*Step 1: the area is a sum over strips.* Let $U = \bigcup_i R_i$. Every point of $U$ has $x_1 \le x \le x_s$. The vertical lines $x = x_k$ have area 0. So $\mu(U) = \sum_{k=1}^{s-1} \mu(U \cap S_k)$, with the open strip $S_k = (x_k, x_{k+1}) \times \mathbb{R}$. For $x \in (x_k, x_{k+1})$, rectangle $R_i$ meets the vertical line at $x$ if and only if $a_i \le x \le b_i$, which holds if and only if $a_i \le x_k$ and $b_i \ge x_{k+1}$, because no $a_i$ or $b_i$ lies strictly between $x_k$ and $x_{k+1}$. Call this set of rectangles $A_k$; it does not depend on $x$. The section of $U$ at $x$ is $\bigcup_{i \in A_k} [c_i, d_i]$, of length $\ell_k$ that does not depend on $x$. By Fubini's theorem, $\mu(U \cap S_k) = \ell_k (x_{k+1} - x_k)$.

*Step 2: the loop adds these terms.* Consider the events in sorted order. Within a group of events with the same $x$, line L7 adds $len[root] \cdot 0 = 0$ for each event after the first, because $prev = x$ already. At the first event of the group with $x = x_{k+1}$, $prev = x_k$ (the $x$ of the previous group), and line L7 adds $len[root] \cdot (x_{k+1} - x_k)$, with $len[root]$ read before this group changes anything. This is the moment $t$ of Lemma 2 for $x = x_{k+1}$. The rectangles active at $t$ have $a_i < x_{k+1} \le b_i$, that is $a_i \le x_k$ and $b_i \ge x_{k+1}$. This is $A_k$. By Lemma 4, $len[root] = \ell_k$. At the first event, line L5 set $prev$ to its $x$, so line L7 adds 0.

So at the end, $area = \sum_{k=1}^{s-1} \ell_k (x_{k+1} - x_k) = \mu(U)$ by Step 1. $\blacksquare$
