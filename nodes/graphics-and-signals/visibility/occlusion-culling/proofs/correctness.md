---
title: Occlusion culling never skips a visible object
proves: [correctness, termination]
status: full
---

We use the model and the pseudocode of the page. For an object $o$ and a pixel center $c$ that a triangle of $o$ covers, let $z_o(c)$ be the largest depth of a triangle of $o$ at $c$. Let $Z(c)$ be the largest depth at $c$ over all triangles of all objects, or $-\infty$ if none covers $c$. Then $o$ is visible when $z_o(c) = Z(c)$ for some $c$. We write $D_s$ for the depth buffer after step $s$ of the loop of line L3, with $-\infty$ below each real number.

**Termination.** The loop of line L3 runs $n$ times, and each step reads a finite set of pixels and draws a finite set of triangles. So OCCLUSION-CULL stops.

**Lemma 1.** For each pixel $c$, $D_s(c)$ does not decrease with $s$, and $D_s(c)$ is the largest depth at $c$ of the triangles of the objects drawn in the first $s$ steps.

*Proof.* Only line L8 writes $D$, and only with a larger value. By induction on the triangles drawn, after each write $D(c)$ is the maximum of the depths drawn at $c$. $\square$

**Lemma 2.** If line L5 skips $o$ at step $s$, then $z_o(c) < D_{s-1}(c)$ for each pixel center $c$ that $o$ covers.

*Proof.* Each point of $o$ lies in its box, so a pixel center $c$ covered by $o$ is in the $xy$ rectangle of the box and $c \in R$. Each point of $o$ has depth at most $z_{\max}$. Line L5 holds, so $D_{s-1}(c) > z_{\max} \ge z_o(c)$. $\square$

**Theorem 1.** Each visible object is in `drawn`.

*Proof.* Suppose $o$ is skipped at step $s$ and $c$ is a pixel center that $o$ covers. By Lemma 2 and Lemma 1, $z_o(c) < D_{s-1}(c) \le Z(c)$, because $D_{s-1}(c)$ is the depth of some triangle at $c$. So $z_o(c) \ne Z(c)$ at each $c$, and $o$ is not visible. $\square$

**Theorem 2.** Let FULL be the z-buffer that draws all objects in `order` with the test of line L8. Then OCCLUSION-CULL and FULL give the same depth buffer and the same image.

*Proof.* Let $F_s$ and $J_s$ be the depth buffer and the image of FULL after step $s$, and $I_s$ the image of OCCLUSION-CULL. We show by induction that $F_s = D_s$ and $J_s = I_s$. For $s = 0$ both are empty. At step $s$, if $o$ is drawn by both, both runs execute the same writes from equal buffers. If OCCLUSION-CULL skips $o$, then by Lemma 2, for each covered center $c$, $z_o(c) < D_{s-1}(c) = F_{s-1}(c)$. Each triangle of $o$ at $c$ has depth at most $z_o(c)$, and $F$ only increases during the step, so the test of line L8 fails for each write of FULL at step $s$. So FULL writes nothing, and $F_s = F_{s-1} = D_{s-1} = D_s$ and $J_s = I_s$. $\square$

By Lemma 1 applied to FULL, the final depth at each $c$ is $Z(c)$, so the image shows at each covered pixel an object $o$ with $z_o(c) = Z(c)$, as the exact per-pixel test does. Neither proof uses the order of line L2, so the result holds for each order; the order changes only how many objects are skipped. $\blacksquare$
