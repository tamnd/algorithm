---
title: The Reingold-Tilford layout is a tidy drawing and takes linear time
proves: [correctness, termination]
status: full
---

Let $T$ be an ordered rooted tree with $n$ vertices and $\delta > 0$. For a vertex $v$, the subtree $T_v$ is drawn *relative to* $v$ when $v$ is at $x = 0$ and each vertex $u$ of $T_v$ is at $x_v(u) = \sum \mathrm{rel}(w)$ over the vertices $w \ne v$ on the path from $v$ down to $u$. Write $L_v(i)$ for the set of vertices of $T_v$ at depth $i$ below $v$, and $h(v)$ for the largest $i$ with $L_v(i) \ne \emptyset$.

Call a drawing of a forest *tidy* if, on each level, the vertices in preorder have increasing $x$ with gaps of at least $\delta$.

**Lemma 1 (contours).** When the loop of line L1 has handled $v$, the values $\mathrm{rel}(c)$ are set for all vertices $c \ne v$ of $T_v$, the drawing of $T_v$ relative to $v$ is tidy, and $\mathrm{lc}_v(i) = \min x_v(L_v(i))$, $\mathrm{rc}_v(i) = \max x_v(L_v(i))$ for $0 \le i \le h(v)$.

*Proof.* By induction in the order of line L1, which handles each child before its parent. A leaf has one level with the single vertex at $0$, so line L2 is right.

Let $v$ have the children $c_1, \ldots, c_k$, each already handled. Consider the forest $F_j$ made of $T_{c_1}, \ldots, T_{c_j}$, where $T_{c_t}$ is drawn relative to $c_t$ and shifted by $\mathrm{off}[c_t]$. We show by induction on $j$ that $F_j$ is tidy, in the preorder of the forest, and that after step $j$ the contours $F$ of the algorithm are the true smallest and largest $x$ on each level of $F_j$. For $j = 1$, this is the induction hypothesis on $c_1$ with $\mathrm{off}[c_1] = 0$ (line L3).

Step $j \ge 2$, with $c = c_j$. On a level $i$ that only one of $F_{j-1}$ and $T_c$ has, the vertices of $F_j$ on that level are those of one tidy part, so the level stays tidy. On a common level $i$, the preorder of $F_j$ lists the level of $F_{j-1}$ and then the level of $T_c$. Both parts are tidy, so the level of $F_j$ is tidy exactly when the last vertex of the first part and the first vertex of the second part are at least $\delta$ apart, which is
$$\mathrm{rc}_F(i) + \delta \le \mathrm{lc}_c(i) + \mathrm{off}[c].$$
Line L5 and line L6 choose $\mathrm{off}[c] = \max_i(\mathrm{rc}_F(i) - \mathrm{lc}_c(i)) + \delta$, the least value for which this holds on all common levels (the level $0$ is common, so the maximum exists). So $F_j$ is tidy, and $\mathrm{off}[c]$ is the leftmost tidy position, which is rule 4. On a common level, the smallest $x$ of $F_j$ is that of $F_{j-1}$ and the largest is that of $T_c$ plus $\mathrm{off}[c]$; on other levels both come from the part that has the level. This is the merge of line L7.

After the last child, line L8 sets $m = \mathrm{off}[c_k]/2$, the midpoint of $\mathrm{off}[c_1] = 0$ and $\mathrm{off}[c_k]$, and line L9 sets $\mathrm{rel}(c_j) = \mathrm{off}[c_j] - m$. So relative to $v$, each vertex $u$ of $T_{c_j}$ has $x_v(u) = \mathrm{rel}(c_j) + x_{c_j}(u)$, which is its position in $F_k$ minus $m$. Shifting keeps $F_k$ tidy, and adding $v$ alone on level $0$ keeps the drawing tidy. The levels of $T_v$ are level $0$, holding $v$ at $0$, and the levels of $F_k$ one deeper, shifted by $-m$, which is line L10. $\square$

**Theorem.** REINGOLD-TILFORD terminates and returns a drawing in which $y(v)$ is the depth of $v$, each level is tidy in preorder, each parent is at the midpoint of its first and last child, and each child subtree is at the leftmost tidy offset against the subtrees of its left siblings. No two edges cross.

*Proof.* Each loop runs over a finite list, so the algorithm stops. Lines L11 and L12 give $y(v)$ equal to the depth and $x(u) = x_r(u)$, the drawing of $T = T_r$ relative to the root $r$, since the preorder sets each parent before its children. By Lemma 1 for $v = r$, every level is tidy. By lines L8 and L9, $\mathrm{rel}(c_1) = -m$ and $\mathrm{rel}(c_k) = m$, so the parent is at the midpoint of its first and last child. The offsets are leftmost by the proof of Lemma 1.

For the edges, take two edges $(p, c)$ and $(p', c')$ from level $i$ to level $i + 1$ with $c$ before $c'$ in preorder. Then $p$ is $p'$ or comes before $p'$ in preorder, because the preorder of the children follows the preorder of the parents. By tidiness, $x(p) \le x(p')$ and $x(c) < x(c')$. Two segments between the same two horizontal lines whose ends are in the same weak order on both lines can only meet at a shared end, which happens only when $p = p'$. So no two edges cross. $\square$

**Running time.** Lines L2 to L4 and L8 to L12 do $O(1)$ work per vertex or child, so $O(n)$ in all. A merge of $F$ and $T_c$ with the contour lists of the implementation (deepest level first, with a shift) costs $O(1 + \min(h_F, h_c))$, where $h_F$, $h_c$ count levels. On each common level $i$, the vertex $w$ of $F$ with the largest $x$ is, after the merge, to the left of a vertex of $T_c$ on that level. In every larger subtree that contains $F_j$, that vertex of $T_c$ stays to the right of $w$ on the same level, since later steps only shift whole subtrees and the relative order is the preorder. So $w$ is never again the rightmost vertex of its level, and each vertex is charged for at most one common level of one merge. There are at most $n - 1$ merges, so all merges cost $O(n)$, and the total time is $\Theta(n)$ arithmetic operations. $\blacksquare$
