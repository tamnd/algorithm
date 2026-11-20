---
title: The error of error reduction never increases
proves: [correctness]
status: full
---

The setting is that of the algorithm. Images have $N$ pixels and live in $\mathbb{C}^N$ with $\langle u, v\rangle = \sum_r \overline{u(r)}\, v(r)$ and $\|u\|^2 = \langle u, u\rangle$. The data are magnitudes $A_u \ge 0$ for each frequency $u$. Let $M = \{g : |G_u| = A_u \text{ for all } u\}$, where $G$ is the DFT of $g$ (unnormalized forward, $1/N$ on the inverse). Let $C$ be the object constraint set: the images that are zero off the support $S$, and, with nonnegativity, real and nonnegative on $S$. Arithmetic is exact.

Let $P_M g$ be the image of lines L3 to L5, and let $P_C g'$ be the image of line L6. Define $E_F(g) = \|g - P_M g\|$ and $E_0(g') = \|g' - P_C g'\|$.

**Lemma 1 (Parseval).** For all images $g, h$, $\|g - h\|^2 = \frac{1}{N} \sum_u |G_u - H_u|^2$.

*Proof.* The unitary DFT $F_u = N^{-1/2} F$ preserves inner products, and $F_u(g - h) = N^{-1/2}(G - H)$. $\square$

**Lemma 2 (the magnitude step).** $P_M g \in M$, and $\|g - P_M g\| \le \|g - h\|$ for every $h \in M$. Also $E_F(g)^2 = \frac{1}{N}\sum_u (|G_u| - A_u)^2$.

*Proof.* By line L4, the DFT of $P_M g$ has magnitude $A_u$ at each $u$, so $P_M g \in M$. By Lemma 1, $\|g - h\|^2 = \frac{1}{N}\sum_u |G_u - H_u|^2$, and each term depends on one frequency. For complex numbers $z$ and $w$ with $|w| = a$, the triangle inequality gives $|z - w| \ge \bigl||z| - a\bigr|$. If $z \ne 0$, the number $a z / |z|$ of line L4 lies on the ray of $z$ and gives equality. If $z = 0$, each $w$ with $|w| = a$ gives $|z - w| = a = \bigl||z| - a\bigr|$, so the choice $w = a$ also gives equality. So line L4 minimizes each term, and the minimum is $\frac{1}{N}\sum_u (|G_u| - A_u)^2$. $\square$

**Lemma 3 (the object step).** $P_C g' \in C$, and $\|g' - P_C g'\| \le \|g' - h\|$ for every $h \in C$.

*Proof.* The squared distance is a sum over pixels, and the constraints act on each pixel alone. Off $S$, every $h \in C$ has $h(r) = 0$, and line L6 sets $0$. On $S$ without nonnegativity, $h(r)$ is free, and line L6 keeps $g'(r)$, with distance $0$. On $S$ with nonnegativity, $h(r) = t \ge 0$ is real, and $|g'(r) - t|^2 = (\operatorname{Re} g'(r) - t)^2 + (\operatorname{Im} g'(r))^2$. The minimum over $t \ge 0$ is at $t = \max(\operatorname{Re} g'(r), 0)$, which is what line L6 sets. $\square$

**Theorem.** Let $g_0 = P_C(\text{input})$ be the image of line L1, let $g_k$ be the image after $k$ passes of the loop of line L2, and let $g'_k = P_M g_k$. Then for every $k \ge 0$,

$$E_F(g_{k+1}) \le E_0(g'_k) \le E_F(g_k).$$

In particular, $E_F(g_0) \ge E_F(g_1) \ge E_F(g_2) \ge \cdots$.

*Proof.* Each $g_k$ is in $C$: $g_0$ by line L1 and Lemma 3, and $g_{k+1} = P_C g'_k$ by line L6 and Lemma 3. Each $g'_k$ is in $M$ by Lemma 2.

First inequality. $g'_k \in M$, so Lemma 2 applied to $g_{k+1}$ gives $E_F(g_{k+1}) = \|g_{k+1} - P_M g_{k+1}\| \le \|g_{k+1} - g'_k\| = \|P_C g'_k - g'_k\| = E_0(g'_k)$.

Second inequality. $g_k \in C$, so Lemma 3 applied to $g'_k$ gives $E_0(g'_k) = \|g'_k - P_C g'_k\| \le \|g'_k - g_k\| = \|P_M g_k - g_k\| = E_F(g_k)$. $\square$

**Corollary (steepest descent).** Let $B(g) = \frac{1}{2} E_F(g)^2$, seen as a function of the $2N$ real numbers $\operatorname{Re} g(r)$ and $\operatorname{Im} g(r)$. At each $g$ whose DFT has no zero entry, $B$ is differentiable and its gradient is $g - P_M g$, in the sense that $\frac{d}{dt} B(g + t d)\big|_{t=0} = \operatorname{Re}\langle g - P_M g, d\rangle$ for every direction $d$. So line L5 is a steepest descent step $g - 1 \cdot \nabla B(g)$ with unit step, and line L6 projects it onto $C$.

*Proof.* By Lemma 2 and Lemma 1, $B(g) = \frac{1}{2N}\sum_u (|G_u| - A_u)^2$. For $G_u \ne 0$, $\frac{d}{dt}|G_u + t D_u| = \operatorname{Re}(\overline{G_u} D_u)/|G_u|$ at $t = 0$. So

$$\frac{d}{dt} B(g + t d)\Big|_{t=0} = \frac{1}{N}\sum_u (|G_u| - A_u)\frac{\operatorname{Re}(\overline{G_u} D_u)}{|G_u|} = \frac{1}{N}\sum_u \operatorname{Re}\Bigl(\overline{G_u - A_u G_u/|G_u|}\; D_u\Bigr).$$

The term $G_u - A_u G_u / |G_u|$ is the DFT of $g - P_M g$ at $u$, so by Lemma 1 (in its inner product form) the sum is $\operatorname{Re}\langle g - P_M g, d\rangle$. $\square$

**What is not claimed.** The theorem does not say that $E_F(g_k) \to 0$. $M$ is not convex, so the iterates can stop at a point with $E_F > 0$ that is not a solution. This stagnation is common in practice. The error is monotone, so it converges to some value $E^\ast \ge 0$, but $E^\ast$ can be positive.
