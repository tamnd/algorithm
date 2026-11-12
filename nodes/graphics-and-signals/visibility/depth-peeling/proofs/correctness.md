---
title: Pass m of depth peeling keeps the m-th nearest fragment at each pixel
proves: [correctness]
status: full
---

We use the pseudocode and the definitions of the page. Fix a pixel $p$. Let its fragments have the keys $\kappa_1 < \kappa_2 < \dots < \kappa_r$, where a key is the pair (plane depth at the center, triangle index). The keys are distinct, because the indices are, and $r \le d$. Write $\mathit{prev}_m$ for the value of $\mathit{prev}[p]$ after pass $m$, with $\mathit{prev}_0 = -\infty$, and $\kappa_m = +\infty$ for $m > r$.

**Lemma 1.** For each $m \ge 1$, after pass $m$ we have $\mathit{best}[p] = \kappa_m$, and $\mathit{layer}[p]$ is the triangle of $\kappa_m$, or nothing if $m > r$. So $\mathit{prev}_m = \kappa_m$.

*Proof.* By induction on $m$. Assume $\mathit{prev}_{m - 1} = \kappa_{m - 1}$, with $\kappa_0 = -\infty$; this holds for $m = 1$ by line L1. Line L3 sets $\mathit{best}[p] = +\infty$. In the loop of line L4, the fragments at $p$ that pass line L5 are those with a key greater than $\kappa_{m - 1}$, that is $\kappa_m, \dots, \kappa_r$ (none if $m > r$). Lines L6 and L7 are the z-buffer update on these keys, which leaves the least of them in $\mathit{best}[p]$ and its triangle in $\mathit{layer}[p]$, in any order of the fragments, by the [z-buffer](/z-buffer/) proof. The least is $\kappa_m$ if $m \le r$. If $m > r$ no fragment passes, so $\mathit{best}[p]$ stays $+\infty = \kappa_m$ and $\mathit{layer}[p]$ is nothing. Line L10 sets $\mathit{prev}_m = \kappa_m$. $\square$

**Lemma 2 (termination).** Pass $m$ writes some pixel if and only if $m \le d$. So the loop outputs exactly $d$ layers and stops in pass $d + 1$.

*Proof.* By Lemma 1, pass $m$ writes pixel $p$ if and only if $p$ has at least $m$ fragments. Some pixel has $d$ fragments and none has more. $\square$

**Theorem.** Layer $m$ holds, at each pixel, the triangle of its $m$-th fragment in key order, or nothing if the pixel has fewer than $m$ fragments. COMPOSITE returns the over composite of the fragments of the pixel, front to back in key order, over the background.

*Proof.* The first claim is Lemmas 1 and 2. For the second, let the triangles of the fragments at $p$ be $k_1, \dots, k_r$ in key order; by the first claim, lines L12 and L13 visit them in this order. By induction, before $k_q$ we have $\tau = \prod_{s < q} (1 - \alpha_{k_s})$ and $c = \sum_{s < q} \big(\prod_{u < s} (1 - \alpha_{k_u})\big) \alpha_{k_s} \mathrm{col}_{k_s}$. Line L13 keeps this. After the loop, line L14 adds $\prod_{s \le r} (1 - \alpha_{k_s}) \cdot \mathrm{bg}$. The result is the front-to-back expansion of
$$\mathrm{col}_{k_1} \text{ over } (\mathrm{col}_{k_2} \text{ over } (\cdots (\mathrm{col}_{k_r} \text{ over } \mathrm{bg}))),$$
which one shows by expanding the over operator $a \text{ over } b = \alpha_a \mathrm{col}_a + (1 - \alpha_a) b$ from the inside out. $\blacksquare$

**Remark (depth-only keys).** If the key is the depth alone, two fragments with the same depth at $p$ have the same key. Line L5 with a strict test then lets neither pass in the pass after the one that kept one of them, so one of them never appears in a layer. This is why the page uses the pair as the key.
