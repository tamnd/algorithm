---
title: The hierarchical z-buffer gives the z-buffer image, and its query is exact on rectangles
proves: [correctness]
status: full
---

We use the pseudocode and the definitions of the page. For an entry $e = (x, y)$ of level $l$, its block $\beta(e)$ is the set of pixels $(i, j)$ with $2^l x \le i < 2^l (x + 1)$ and $2^l y \le j < 2^l (y + 1)$, including padding pixels outside the screen, which hold $+\infty$. The *invariant* is $Z_l[e] = \max_{p \in \beta(e)} Z_0[p]$ for every entry $e$ of every level $l \ge 1$.

**Lemma 1 (writes keep the invariant).** If the invariant holds before WRITE$(p, z)$, it holds after it.

*Proof.* Line L12 changes only $Z_0[p]$. The blocks that contain $p$ are those of the entries $e_1, \dots, e_L$ on the path above $p$, one per level; the max over any other block does not change. The blocks of level $l$ split the block of the parent into four, so $\max_{\beta(e_l)} Z_0$ is the max of the four children of $e_l$, each correct by induction on $l$ (for $l = 1$ the children are level-0 entries). Line L13 sets $e_l$ to this max. If the new value of $e_l$ equals the old one, the four children of $e_{l + 1}$ are unchanged, so its max is unchanged, and the same holds for all higher entries; stopping there keeps the invariant. $\square$

**Lemma 2 (the query).** If the invariant holds, HIDDEN$(R, z_{\min})$ returns true if and only if $z_{\min} \ge Z_0[p]$ for every pixel $p \in R$.

*Proof.* Call an entry *bad* if its block contains a pixel $p \in R$ with $Z_0[p] > z_{\min}$. By the invariant, an entry whose block meets $R$ and with $z_{\min} \ge Z_l[e]$ is not bad, since every pixel of its block has $Z_0 \le Z_l[e] \le z_{\min}$.

If some pixel $p \in R$ has $Z_0[p] > z_{\min}$, the entries on the path from the root to $p$ are all bad. The root is pushed by line L1. When a bad entry of level $l \ge 1$ is popped, line L3 does not skip it, because its block contains $p \in R$; line L4 does not skip it, because $Z_l[e] \ge Z_0[p] > z_{\min}$; so line L6 pushes its children, one of which is the next entry on the path. The bad entry of level 0 is $p$ itself, and when it is popped line L5 returns false. The query may return false earlier at another pixel, which is also bad. Either way it returns false.

If no pixel of $R$ has $Z_0 > z_{\min}$, line L5 can only be reached by a level-0 entry $p$ with $p \in R$ (line L3) and $z_{\min} < Z_0[p]$ (line L4), which does not exist. Each entry is pushed at most once, by its parent, so the stack empties and line L7 returns true. $\square$

**Lemma 3 (safe culling).** Suppose HIDDEN returns true for a triangle $t$ at line L10, or for an object that contains $t$ at line L9, before $t$ would be drawn. Then, in a z-buffer that draws $t$ at that time, no fragment of $t$ would pass the test $z < Z_0[p]$, then or later.

*Proof.* Let $(p, z)$ be a fragment of $t$. The pixel center of $p$ is in $t$, so $p$ is in the rectangle of $t$ and in that of its object, since each rectangle holds every pixel center its triangles can cover. The depth $z$ is a convex combination of the vertex depths of $t$, so $z \ge z_{\min}$, for the least depth of $t$ and also for the least depth of the object. By Lemma 2, $z_{\min} \ge Z_0[p]$ at the time of the query. The stored depths never increase, since line L11 writes only a smaller value. So at any later time $z \ge z_{\min} \ge Z_0[p]$, and $z < Z_0[p]$ is false. $\square$

**Theorem.** HZB-RENDER gives the same depth and color at each pixel as a z-buffer that draws all triangles in the same order.

*Proof.* Compare the run with a z-buffer that draws the same triangles in the same order but culls nothing. By induction over the triangles, both have the same level-0 depths and colors after each triangle: a triangle that is drawn makes the same updates in both, by line L11, and the invariant holds by Lemma 1, so the next query is answered correctly; a triangle that is culled would make no update in the plain z-buffer, by Lemma 3. $\blacksquare$

The order of the objects only changes which ties are won (the first drawn) and how much is culled. The depth at each pixel is the least covering depth in every order. The color is the color of the nearest triangle when it is unique.
