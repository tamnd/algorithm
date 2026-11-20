---
title: Convergence of POCS partial Fourier reconstruction
proves: [correctness]
status: full
---

The setting is that of the algorithm. Images are vectors in $\mathbb{C}^n$, viewed as the real vector space $\mathbb{R}^{2n}$ with the inner product $\langle u, v \rangle = \operatorname{Re} \sum_j \overline{u_j} v_j$ and the norm $\|u\|^2 = \sum_j |u_j|^2$. $F_u$ is the unitary DFT, so $\|F_u u\| = \|u\|$. The acquired set is $S = \{-n/2, \ldots, k_0\}$ (frequencies modulo $n$), the reference phase $p$ has $|p_j| = 1$, and

$$C_1 = \{\rho \cdot p : \rho \in \mathbb{R}^n\}, \qquad C_2 = \{x \in \mathbb{C}^n : (F_u x)(f) = y_f \text{ for all } f \in S\}.$$

The iterates are $x_0 = F_u^H(y \text{ on } S, 0 \text{ elsewhere})$ (line L2) and $x_{t+1} = P_2 P_1 x_t$ (lines L4 to L7).

**Lemma 1 (the two steps are projections).** Line L4 maps $x$ to the point of $C_1$ nearest to $x$, and lines L5 to L7 map $x$ to the point of $C_2$ nearest to $x$. $C_1$ is a real linear subspace, and $C_2$ is a nonempty affine subspace.

*Proof.* $C_1$ is closed under real linear combinations. For $\rho \in \mathbb{R}^n$, $\|x - \rho p\|^2 = \sum_j |x_j - \rho_j p_j|^2 = \sum_j |\overline{p_j} x_j - \rho_j|^2$ because $|p_j| = 1$. Each term is smallest for $\rho_j = \operatorname{Re}(\overline{p_j} x_j)$, which is line L4. $C_2$ is the solution set of linear equations and contains $x_0$. For $v \in C_2$, $\|x - v\| = \|F_u x - F_u v\|$, and $F_u v$ is free on the frequencies outside $S$ and fixed to $y$ on $S$. The distance is smallest when $F_u v$ equals $F_u x$ outside $S$, which is lines L5 to L7. $\square$

For a closed subspace $U$ write $P_U$ for the orthogonal projection. If $C = a + U$ is an affine subspace, the nearest point map is $P_C(x) = a + P_U(x - a)$.

**Lemma 2.** Let $U$ and $V$ be subspaces of a finite dimensional real inner product space, $W = U \cap V$ and $T = P_V P_U$. Then $T w = w$ for $w \in W$, $T$ maps $W^\perp$ into $W^\perp$, and there is $c < 1$ with $\|T e\| \le c \|e\|$ for all $e \in W^\perp$. Hence $T^t u \to P_W u$ for every $u$, with $\|T^t u - P_W u\| \le c^t \|u - P_W u\|$.

*Proof.* For $w \in W$, $P_U w = w$ and $P_V w = w$. For $e \in W^\perp$ and $w \in W$, using that projections are self-adjoint, $\langle T e, w \rangle = \langle P_U e, P_V w \rangle = \langle P_U e, w \rangle = \langle e, P_U w \rangle = \langle e, w \rangle = 0$, so $T e \in W^\perp$. Projections do not increase norms, so $\|T e\| \le \|e\|$. If $\|T e\| = \|e\|$ for some $e \ne 0$, then $\|P_U e\| = \|e\|$, so $e \in U$ by Pythagoras, and then $\|P_V e\| = \|e\|$, so $e \in V$. Then $e \in W \cap W^\perp = \{0\}$, a contradiction. So $\|T e\| < \|e\|$ on the unit sphere of $W^\perp$, which is compact, and the maximum $c$ of the continuous function $\|T e\|$ there is below 1. Write $u = P_W u + e$ with $e \in W^\perp$; then $T^t u = P_W u + T^t e$ and $\|T^t e\| \le c^t \|e\|$. $\square$

**Theorem 1 (consistent case).** If $C_1 \cap C_2 \ne \emptyset$, then $x_t$ converges to the point of $C_1 \cap C_2$ nearest to $x_0$, and the error falls at least geometrically: $\|x_t - x_\ast\| \le c^t \|x_0 - x_\ast\|$ with $c < 1$ from Lemma 2. Moreover $\|x_{t+1} - z\| \le \|x_t - z\|$ for every $z \in C_1 \cap C_2$ and every $t$.

*Proof.* Take $z \in C_1 \cap C_2$. Then $C_1 = z + U$ with $U = C_1$ (a subspace that contains $z$), and $C_2 = z + V$ with $V = \{v : (F_u v)(f) = 0 \text{ for } f \in S\}$. By Lemma 1 and the formula for $P_C$, $x_{t+1} - z = P_V P_U (x_t - z) = T (x_t - z)$. Lemma 2 gives $x_t - z \to P_W(x_0 - z)$ with $W = U \cap V$, at the stated rate. The limit $x_\ast = z + P_W(x_0 - z)$ lies in $z + W = C_1 \cap C_2$, and it is the point of $z + W$ nearest to $x_0$. The monotone distance follows from $\|T e\| \le \|e\|$ with $e = x_t - z$. $\square$

**Theorem 2 (inconsistent case).** If $C_1 \cap C_2 = \emptyset$, for example with noisy data, then $x_t$ still converges, to a point $b \in C_2$ such that $P_1 b \in C_1$ and $\|b - P_1 b\|$ is the distance between $C_1$ and $C_2$.

*Proof.* Write $C_1 = U$ and $C_2 = a + V$ with $a = x_0$. The sum $U + V$ is a subspace of a finite dimensional space, so $a = u - v + g$ with $u \in U$, $v \in V$ and $g \perp U + V$. Put $a' = u \in C_1$; then $a + v = a' + g$, so $C_2 = a' + g + V$. For any $x$, $P_1 x = a' + P_U(x - a')$ and $P_2 x = a' + g + P_V(x - a' - g) = a' + g + P_V(x - a')$, because $P_V g = 0$. With $e_t = x_t - a' - g$ and $P_U g = 0$,

$$e_{t+1} = P_V P_U (x_t - a') = P_V P_U (e_t + g) = T e_t.$$

By Lemma 2, $e_t \to P_W e_0$, so $x_t \to b = a' + g + P_W e_0 \in C_2$. Then $P_1 b = a' + P_U(g + P_W e_0) = a' + P_W e_0 = b - g \in C_1$. For any $c_1 = a' + u_1 \in C_1$ and $c_2 = a' + g + v_2 \in C_2$, $\|c_2 - c_1\|^2 = \|g\|^2 + \|v_2 - u_1\|^2 \ge \|g\|^2$ because $g \perp U + V$. So $\|b - P_1 b\| = \|g\|$ is the distance between the sets. $\square$

**Theorem 3 (constant phase).** Let $x = e^{i\varphi_0}\rho$ with $\rho$ real, $y = F_u x$ on $S$, and $p_j \in \{e^{i\varphi_0}, -e^{i\varphi_0}\}$ for all $j$. Then $C_1 \cap C_2 = \{x\}$, and $\|x_t - x\| = 2^{-t} \|x_0 - x\|$ for every $t$.

*Proof.* The set $C_1$ is $e^{i\varphi_0}\mathbb{R}^n$, because a sign on $p_j$ does not change the real multiples. It contains $x$, and $C_2$ contains $x$. Let $x' \in C_1 \cap C_2$ and $d = x - x' = e^{i\varphi_0}\delta$ with $\delta$ real. Then $D = F_u \delta$ is Hermitian, $D(-f) = \overline{D(f)}$, and $D(f) = 0$ for $f \in S$. Every frequency $f$ has $f \in S$ or $-f \in S$: if $f > k_0 \ge 0$ then $-n/2 < -f < 0$. So $D = 0$ and $x' = x$.

For the rate, let $M = \{k_0 + 1, \ldots, n/2 - 1\}$ be the missing set; then $-M \subset S$ and $M \cap (-M) = \emptyset$. The error $e_t = x_t - x$ lies in $V$, so $E_t = F_u e_t$ is zero on $S$ and lives on $M$. Line L4 fixes $x$ and is real linear, so $P_1 x_t - x = P_1 e_t = e^{i\varphi_0} \operatorname{Re}(e^{-i\varphi_0} e_t) = \frac{1}{2}\bigl(e_t + e^{2i\varphi_0}\overline{e_t}\bigr)$. The DFT of $\overline{e_t}$ at $f$ is $\overline{E_t(-f)}$, which lives on $-M \subset S$. Lines L5 to L7 set the spectrum on $S$ back to that of $x$, so they remove that part, and $E_{t+1} = \frac{1}{2} E_t$. By Parseval, $\|e_{t+1}\| = \frac{1}{2}\|e_t\|$. $\blacksquare$

**Remarks.**

- The reference phase of line L1 is $p_j = l_j/|l_j|$ for the triangle-windowed image $l$. For $x = e^{i\varphi_0}\rho$ with real $\rho$, $l = e^{i\varphi_0} r$ with $r$ real (the argument of the homodyne proof), so $p_j = \pm e^{i\varphi_0}$ wherever $l_j \ne 0$, and Theorem 3 applies when no $l_j$ is zero.
- The variant that replaces $x_j$ by $|x_j| p_j$ (keep the magnitude, impose the phase) does not map onto a convex set. The theorems above do not cover it.
- For a phase that varies, the theorems still hold for the sets $C_1$ and $C_2$, but $C_1$ is built from an estimated phase. The limit is then the nearest point of the model, not the true image.
