---
title: RAAR for two convex sets that meet, its fixed points and its convergence
proves: [correctness]
status: full
---

The space is $\mathbb{C}^N$ with the real inner product $\langle u, v \rangle = \operatorname{Re} \sum_r \overline{u_r} v_r$ and its norm. $A$ and $B$ are closed convex sets with nearest point maps $P_A$ and $P_B$ (in the algorithm, $A$ is the object set of $P_S$ and $B$ is the magnitude set of $P_M$). The reflections are $R_A = 2P_A - I$ and $R_B = 2P_B - I$. For $0 < \beta \le 1$ the RAAR map of lines L3 to L6 is

$$V(x) = \tfrac{\beta}{2}\bigl(R_A R_B x + x\bigr) + (1 - \beta) P_B x .$$

Line L6 writes this as $\tfrac{\beta}{2}(2q - r + x) + (1 - \beta)p$ with $p = P_B x$, $r = 2p - x = R_B x$ and $q = P_A r$; then $2q - r = R_A R_B x$, so the two forms agree.

A map $F$ is *nonexpansive* if $\|Fx - Fy\| \le \|x - y\|$ for all $x, y$, and *firmly nonexpansive* if $\|Fx - Fy\|^2 \le \langle Fx - Fy, x - y \rangle$ for all $x, y$.

**Lemma 1.** $F$ is firmly nonexpansive if and only if $2F - I$ is nonexpansive.

*Proof.* Put $a = Fx - Fy$ and $d = x - y$. Then $\|(2F - I)x - (2F - I)y\|^2 = \|2a - d\|^2 = 4\|a\|^2 - 4\langle a, d \rangle + \|d\|^2$. This is at most $\|d\|^2$ if and only if $\|a\|^2 \le \langle a, d \rangle$. $\square$

**Lemma 2.** For a closed convex set $C$, the nearest point $p = P_C x$ is the point of $C$ with $\langle x - p, w - p \rangle \le 0$ for all $w \in C$, and $P_C$ is firmly nonexpansive.

*Proof.* The first claim is the standard variational form of the nearest point: for $w \in C$ and $t \in (0, 1]$, the point $p + t(w - p)$ is in $C$, so $\|x - p\|^2 \le \|x - p - t(w - p)\|^2 = \|x - p\|^2 - 2t\langle x - p, w - p \rangle + t^2\|w - p\|^2$. Divide by $t$ and let $t \to 0$. For the second claim, put $p = P_C x$ and $p' = P_C y$. The inequality for $x$ with $w = p'$ and the one for $y$ with $w = p$ add to $\langle (x - y) - (p - p'), p' - p \rangle \le 0$, which is $\|p - p'\|^2 \le \langle p - p', x - y \rangle$. $\square$

**Lemma 3.** $V$ is firmly nonexpansive.

*Proof.* By Lemmas 1 and 2, $R_A$ and $R_B$ are nonexpansive, so $R_A R_B$ is nonexpansive. $T = \tfrac12(R_A R_B + I)$ has $2T - I = R_A R_B$, so $T$ is firmly nonexpansive by Lemma 1. Now $V = \beta T + (1 - \beta) P_B$, and

$$2V - I = \beta(2T - I) + (1 - \beta)(2P_B - I),$$

a convex combination of two nonexpansive maps, which is nonexpansive by the triangle inequality. By Lemma 1, $V$ is firmly nonexpansive. $\square$

**Theorem 1 (fixed points).** Let $0 < \beta < 1$ and let $A \cap B$ be nonempty. Then $V(x) = x$ if and only if $x \in A \cap B$.

*Proof.* If $x \in A \cap B$, then $P_B x = x$, $R_B x = x$, $R_A x = x$, so $V(x) = \tfrac{\beta}{2}(2x) + (1 - \beta)x = x$.

Conversely, let $V(x) = x$ and take any $z \in A \cap B$. With $p$, $r$, $q$ as above, $\tfrac{\beta}{2}(2q - r + x) = \beta(q - p + x)$, so the fixed point equation is $x = \beta x + \beta(q - p) + (1 - \beta)p$, that is, $(1 - \beta)(x - p) = \beta(q - p)$. Put $u = x - p$ and $c = (1 - \beta)/\beta > 0$. Then $q = p + c u$ and $r = p - u$.

Lemma 2 for $p = P_B x$ with $w = z \in B$ gives $\langle u, z - p \rangle \le 0$.

Lemma 2 for $q = P_A r$ with $w = z \in A$ gives $\langle r - q, z - q \rangle \le 0$. Here $r - q = -(1 + c)u$, so $\langle u, z - q \rangle \ge 0$, that is, $\langle u, z - p \rangle \ge c\|u\|^2$.

So $c\|u\|^2 \le \langle u, z - p \rangle \le 0$, and $u = 0$. Then $x = p \in B$ and $q = p = x$, so $x = P_A r \in A$. $\square$

For $\beta = 1$ (Douglas-Rachford) the argument gives only $c = 0$, and the fixed points are the points $x$ with $P_B x \in A \cap B$; the iterate itself need not be a solution. This is why the implementation returns $P_B x = P_M x$ (line L7) for all $\beta$.

**Theorem 2 (convergence).** Let $0 < \beta \le 1$, let $V$ have a fixed point, and let $x_{k+1} = V(x_k)$. Then for every fixed point $z$ the distance $\|x_k - z\|$ never grows, and $x_k$ converges to a fixed point $x^\ast$. For $\beta < 1$ and $A \cap B$ nonempty, $x^\ast \in A \cap B$, and the read-out $P_B x_k$ converges to $x^\ast$.

*Proof.* For firmly nonexpansive $V$ and $Vz = z$, with $a = Vx - z$ and $d = x - z$, we have $\|a\|^2 \le \langle a, d \rangle$, and so

$$\|x - Vx\|^2 = \|d - a\|^2 = \|d\|^2 - 2\langle a, d\rangle + \|a\|^2 \le \|d\|^2 - \|a\|^2 .$$

So $\|x_{k+1} - z\|^2 + \|x_k - x_{k+1}\|^2 \le \|x_k - z\|^2$. The distance to $z$ never grows, the sequence is bounded, and summing over $k$ gives $\sum_k \|x_k - x_{k+1}\|^2 \le \|x_0 - z\|^2$, so $\|x_k - V x_k\| \to 0$. In $\mathbb{C}^N$ a bounded sequence has a convergent subsequence $x_{k_j} \to x^\ast$. $V$ is continuous (it is nonexpansive), so $x^\ast - V x^\ast = \lim (x_{k_j} - V x_{k_j}) = 0$, and $x^\ast$ is a fixed point. Take $z = x^\ast$: the distance $\|x_k - x^\ast\|$ never grows and has a subsequence that tends to $0$, so it tends to $0$. The last claim follows from Theorem 1 and the continuity of $P_B$, since $P_B x^\ast = x^\ast$. $\square$

**The support form.** If $A$ is the subspace of images that are zero off a support $S$ (no sign constraint), then $P_A$ keeps the values on $S$ and sets the rest to zero, and for any $P_B$, convex or not,

$$V(x)(t) = p(t) \text{ for } t \in S, \qquad V(x)(t) = \beta x(t) + (1 - 2\beta) p(t) \text{ for } t \notin S .$$

*Proof.* On $S$, $q = r = 2p - x$ and $\tfrac{\beta}{2}(2q - r + x) = \tfrac{\beta}{2}(2p) = \beta p$, so $V(x) = \beta p + (1 - \beta)p = p$. Off $S$, $q = 0$ and $\tfrac{\beta}{2}(-r + x) = \beta(x - p)$, so $V(x) = \beta x - \beta p + (1 - \beta)p = \beta x + (1 - 2\beta)p$. $\square$

Compare HIO, which gives $x - \beta p$ off $S$: at $\beta = 1$ the two agree.

**What is not claimed.** The magnitude set $M$ of phase retrieval is not convex, $P_M$ is not firmly nonexpansive, and none of the theorems above applies to it. For phase retrieval RAAR is a heuristic with the fixed point property of the support form: if $x = V(x)$ and $\beta < 1$, then off $S$ we get $(1 - \beta)x = (1 - 2\beta)p$, which does not force $p = 0$ there, so a fixed point need not give a solution. The tests check Lemma 3 and Theorem 2 on two convex sets, the support form, the case $\beta = 1$, and that the true object is a fixed point; the reconstruction test on the page example is a measurement.
