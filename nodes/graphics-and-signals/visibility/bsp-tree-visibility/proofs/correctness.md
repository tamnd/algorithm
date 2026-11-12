---
title: The BSP traversal gives a valid back-to-front order for each viewpoint
proves: [correctness, termination]
status: full
---

We use the model and the pseudocode of the page. The tree satisfies the build property of the [BSP tree](/bsp-tree/) page, in space: for each node $t$, the fragments of $t.on$ lie in the plane $\sigma_t = 0$, each fragment of the subtree $t.front$ lies in the closed half-space $\sigma_t \ge 0$, and each fragment of $t.back$ lies in $\sigma_t \le 0$. The fragments of an input polygon have the union of that polygon, and they lie in its plane.

For a pixel sample $S$, the ray is $R(\tau) = E + \tau (S - E)$, $\tau > 0$. A fragment $f$ *meets the ray at* $\tau$ when $R(\tau) \in f$, and $f$ is *in front of* $g$ on the ray when $f$ meets it at $\tau_f$, $g$ meets it at $\tau_g$, and $\tau_f < \tau_g$. An order of fragments is valid when no fragment is in front of a later fragment on any pixel ray.

**Lemma 1 (one node).** Let $t$ be a node, let $N$ be the fragments on the side of $E$ ($t.front$ if $\sigma_t(E) \ge 0$, else $t.back$), and let $F$ be the fragments on the other side. Then no fragment of $F$ is in front of a fragment of $t.on \cup N$, and no fragment of $t.on$ is in front of a fragment of $N$ or of $t.on$.

*Proof.* Let $s(\tau) = \sigma_t(R(\tau))$, an affine function of $\tau$ with $s(0) = \sigma_t(E)$.

Case $\sigma_t(E) > 0$. Let $g \in t.on \cup N$ meet the ray at $\tau_g$, so $s(\tau_g) \ge 0$. Since $s(0) > 0$ and $s(\tau_g) \ge 0$, $s(\tau) > 0$ for each $\tau \in (0, \tau_g)$. A fragment of $F$ lies in $\sigma_t \le 0$, so it does not meet the ray at any $\tau < \tau_g$. So no fragment of $F$ is in front of $g$. Next let $f \in t.on$ meet the ray at $\tau_f$, so $s(\tau_f) = 0$. Then $s(\tau) > 0$ on $(0, \tau_f)$ and $s$ is affine with $s(0) > 0 = s(\tau_f)$, so $s < 0$ for $\tau > \tau_f$. A fragment of $N$ lies in $\sigma_t \ge 0$, so it meets the ray only at $\tau \le \tau_f$, and $f$ is not in front of it. Two fragments of $t.on$ both meet the ray at the single zero $\tau_f$ of $s$, so neither is in front of the other.

Case $\sigma_t(E) < 0$. This is the first case with the sign of $\sigma_t$ changed.

Case $\sigma_t(E) = 0$. If $s$ is identically 0, the ray lies in the plane, and no fragment of $t.on$ meets it, by the convention of the model that a polygon whose plane holds the ray covers no pixel. Fragments of $N$ and $F$ in the plane are also edge on. A fragment of $F$ off the plane meets the ray nowhere. So the claim holds. Otherwise $s(\tau) = c \tau$ with $c \ne 0$, and $s(\tau) \ne 0$ for $\tau > 0$. So no fragment of $t.on$ meets the ray. If $c > 0$, only fragments in $\sigma_t \ge 0$ can meet the ray, that is, those of $t.front = N$; fragments of $F = t.back$ meet it only where $s = 0$, which does not occur. If $c < 0$, only fragments of $t.back = F$ meet the ray, and fragments of $N$ do not meet it, so no fragment of $F$ is in front of a fragment of $N$. $\square$

**Lemma 2 (the output order).** BSP-PAINT outputs the fragments of the subtree of a node $t$ as: the output for the far child, then $t.on$, then the output for the near child. It outputs each fragment of the tree exactly once.

*Proof.* Line L7 pushes $(near, visit)$, $(t, draw)$ and $(far, visit)$, so the stack pops $(far, visit)$ first. By induction on the height of the subtree, all pairs that the visit of $far$ pushes are popped before $(t, draw)$, because they lie above it on the stack. Then line L5 outputs $t.on$, and then the visit of $near$ runs in the same way. Each node is visited once, from its parent, so each fragment is output once. $\square$

**Theorem 1.** For each viewpoint $E$, the order of BSP-PAINT is valid, and the image at each pixel holds the input polygon of a fragment that the pixel ray meets first, or the background.

*Proof.* By induction on the height of the subtree of $t$, the output for the subtree is valid. Leaves and empty subtrees are clear. For a node, by Lemma 2 the output is (far part, $t.on$, near part). The far and near parts are valid by induction. A fragment of the far part is not in front of a later fragment of $t.on$ or the near part, and a fragment of $t.on$ is not in front of a later fragment of $t.on$ or the near part, by Lemma 1. So the output is valid.

At a pixel, line L5 writes each fragment that meets the ray, in order, so the image holds the last such fragment $f$. Each fragment $g$ that meets the ray comes before $f$, and by validity $g$ is not in front of $f$, so $\tau_f \le \tau_g$. Each input polygon that the ray meets has a fragment that meets the ray at the same $\tau$, because the fragments cover the polygon. So $f$ belongs to a polygon that the ray meets first. $\square$

**Theorem 2.** BSP-FRONT-TO-BACK writes, at each pixel, the input polygon of a fragment that the ray meets first, or the background.

*Proof.* Line L12 is line L7 with $near$ and $far$ exchanged, so by Lemma 2 its order is the reverse of the order of BSP-PAINT, as long as the loop runs. At a pixel, the first fragment $f$ in the reverse order that meets the ray is the last such fragment in the order of BSP-PAINT. Line L11 writes $f$ and never changes a written pixel, so the pixel holds $f$, which is correct by Theorem 1. If the loop stops early at line L9, each pixel is already written, and each written value is final. If no fragment meets the ray, the pixel keeps the background. $\square$

**Termination.** Each node is pushed once for a visit and once for a draw, and each pop removes one pair, so each loop runs at most $2m + 1$ times for $m$ nodes, besides the pairs with nil, of which there are at most $m + 1$. $\blacksquare$
