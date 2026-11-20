---
title: The Gerchberg-Saxton error never increases
proves: [correctness]
status: full
---

The setting is that of the algorithm. Signals have length $n$ and live in $\mathbb{C}^n$ with $\langle u, v\rangle = \sum_j \overline{u_j}\, v_j$ and $\|u\|^2 = \langle u, u\rangle$. The DFT is unnormalized forward, with $1/n$ on the inverse. The data are object magnitudes $a_j \ge 0$ and Fourier magnitudes $A_u \ge 0$. Let $O = \{g : |g_j| = a_j \text{ for all } j\}$ and $M = \{g : |G_u| = A_u \text{ for all } u\}$, where $G$ is the DFT of $g$. Arithmetic is exact.

Let $P_M g$ be the signal of lines L3 to L5 and $P_O g'$ the signal of line L6. Define $E_F(g) = \|g - P_M g\|$ and $E_0(g') = \|g' - P_O g'\|$.

**Lemma 1 (one entry).** Let $z \in \mathbb{C}$ and $a \ge 0$. Let $w^\ast = a z / |z|$ if $z \ne 0$ and $w^\ast = a$ if $z = 0$. Then $|z - w^\ast| = \bigl||z| - a\bigr| \le |z - w|$ for every $w$ with $|w| = a$.

*Proof.* The triangle inequality gives $|z - w| \ge \bigl||z| - |w|\bigr| = \bigl||z| - a\bigr|$. If $z \ne 0$, $w^\ast$ lies on the ray from $0$ through $z$ at distance $a$, so $|z - w^\ast| = \bigl||z| - a\bigr|$. If $z = 0$, $|z - w^\ast| = a = \bigl||z| - a\bigr|$. $\square$

**Lemma 2 (the two steps are nearest points).** $P_O g' \in O$ and $\|g' - P_O g'\| \le \|g' - h\|$ for all $h \in O$. $P_M g \in M$ and $\|g - P_M g\| \le \|g - h\|$ for all $h \in M$, and $E_F(g)^2 = \frac{1}{n}\sum_u (|G_u| - A_u)^2$.

*Proof.* The first claim is Lemma 1 applied to each entry, because $\|g' - h\|^2 = \sum_j |g'_j - h_j|^2$. For the second, the unitary DFT $n^{-1/2} F$ preserves norms, so $\|g - h\|^2 = \frac{1}{n}\sum_u |G_u - H_u|^2$ (Parseval). Line L4 applies the map of Lemma 1 to each $G_u$ with $a = A_u$, so it minimizes each term, and line L5 returns to the signal domain. The minimum value is $\frac{1}{n}\sum_u (|G_u| - A_u)^2$. $\square$

**Theorem.** Let $g_0$ be the signal of line L1, $g_k$ the signal after $k$ passes of the loop of line L2, and $g'_k = P_M g_k$. Then for every $k \ge 0$,

$$E_F(g_{k+1}) \le E_0(g'_k) \le E_F(g_k),$$

so $E_F(g_0) \ge E_F(g_1) \ge E_F(g_2) \ge \cdots$.

*Proof.* Line L1 gives $|g_0| = a$, so $g_0 \in O$, and line L6 with Lemma 2 gives $g_{k+1} = P_O g'_k \in O$. Lemma 2 gives $g'_k \in M$.

Since $g'_k \in M$, Lemma 2 for $g_{k+1}$ gives $E_F(g_{k+1}) = \|g_{k+1} - P_M g_{k+1}\| \le \|g_{k+1} - g'_k\| = E_0(g'_k)$.

Since $g_k \in O$, Lemma 2 for $g'_k$ gives $E_0(g'_k) = \|g'_k - P_O g'_k\| \le \|g'_k - g_k\| = E_F(g_k)$. $\square$

**Corollary (fixed points).** If $f \in O \cap M$, the start $g_0 = f$ gives $g_k = f$ for all $k$. If the run reaches $E_F(g_k) = 0$, then $g_k \in O \cap M$, so $g_k$ is consistent with both magnitudes.

*Proof.* For $f \in O \cap M$, Lemma 1 maps each entry and each Fourier coefficient to itself, so $P_M f = f$ and $P_O f = f$. If $E_F(g_k) = 0$ then $g_k = P_M g_k \in M$, and $g_k \in O$ by the theorem. $\square$

**What is not claimed.** $O$ and $M$ are not convex. The error is monotone, so it converges, but the limit can be positive: the iteration can stagnate at a point that is in neither set. Even at error zero, the result is fixed only up to the ambiguities that the two magnitudes leave, at least a global phase factor.
