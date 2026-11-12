---
title: The painter's algorithm is correct for a valid visibility order
proves: [correctness, termination]
status: full
---

We use the model and the pseudocode of the page. For a polygon $p$ we write $\min_p$ and $\max_p$ for the least and the largest $z$ of its vertices. Because $p$ is a convex polygon, $z_p(c) \in [\min_p, \max_p]$ for each point $c$ of its projection.

**Termination.** Line L1 does $n$ steps, line L2 is a sort of $n$ keys, and the loops of lines L4 and L5 are over finite sets. So PAINTER stops.

**Lemma 1.** After line L7, the image at a pixel $c$ is the last polygon of `order` that covers $c$, or the background if no polygon covers $c$.

*Proof.* Line L3 writes the background at $c$. Later, only line L6 writes at $c$, and it writes $p$ exactly when $p$ covers $c$. The polygons are taken in the order of `order`, so the last write at $c$ is by the last polygon of `order` that covers $c$. $\square$

**Theorem 1.** If `order` is a valid visibility order, then at each pixel $c$ the image holds a polygon of largest depth at $c$ among those that cover $c$, or the background if none covers $c$.

*Proof.* Let $q$ be the last polygon of `order` that covers $c$; by Lemma 1 the image holds $q$. Let $p$ be another polygon that covers $c$. Then $p$ comes before $q$, and validity gives $z_p(c) \le z_q(c)$. So $q$ has the largest depth at $c$. If no polygon covers $c$, Lemma 1 gives the background. $\square$

**Theorem 2.** Assume that for each two polygons $p \ne q$ that cover a common pixel, $\max_p < \min_q$ or $\max_q < \min_p$. Then line L2 gives a valid visibility order, so the output is correct.

*Proof.* Let $p$ come before $q$ in `order`, and let both cover $c$. The sort gives $\min_p \le \min_q$. By the assumption, either $\max_p < \min_q$ or $\max_q < \min_p$. The second case gives $\min_q \le \max_q < \min_p \le \min_q$, which is false. So $\max_p < \min_q$, and $z_p(c) \le \max_p < \min_q \le z_q(c)$. By Theorem 1 the output is correct. $\square$

**Theorem 3.** Assume that at a pixel $c$ the image holds $p$, while $q$ covers $c$ with $z_q(c) > z_p(c)$. Then $\min_p < \max_q$ and $\min_q \le \max_p$. So the depth ranges $[\min_p, \max_p]$ and $[\min_q, \max_q]$ intersect.

*Proof.* By Lemma 1, $p$ is the last polygon that covers $c$, so $q$ comes before $p$ and the sort gives $\min_q \le \min_p$. Then $\min_p \le z_p(c) < z_q(c) \le \max_q$, and $\min_q \le \min_p \le \max_p$. $\square$

**No sort key can be correct for each scene.** Let the scene have polygons $s_1, s_2, s_3$ and pixels $c_{12}, c_{23}, c_{31}$ such that $c_{ab}$ is covered by $s_a$ and $s_b$ only, with $z_{s_a}(c_{ab}) > z_{s_b}(c_{ab})$. A correct image needs, by Lemma 1, $s_a$ after $s_b$ at each $c_{ab}$. So in `order`, $s_1$ comes after $s_2$, $s_2$ after $s_3$ and $s_3$ after $s_1$. This is a cycle, and no total order has it. Hence each order gives a wrong pixel, whatever the keys of line L1 are. The test file checks all six orders of a scene with cyclic overlap, with exact coordinates, against a per-pixel depth test. $\blacksquare$
