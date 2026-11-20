---
title: The ideal localized orthogonal decomposition has an energy error of order H for any rough coefficient
proves: [correctness]
status: full
---

We prove the properties of the 1D method of the page, in exact arithmetic. The problem is $-(a u')' = f$ on $(0, 1)$, $u(0) = u(1) = 0$, with $\alpha \le a \le \beta$ piecewise constant on the fine mesh and no other assumption on $a$. Let $V_h$ be the fine P1 space with zero boundary values, $V_H \subset V_h$ the coarse P1 space, $a(v, w) = \int a v' w'$, $\|v\|_a = a(v, v)^{1/2}$, and $f_h$ the P1 interpolant of $f$. The reference is the fine solution $u_h \in V_h$ with $a(u_h, v) = (f_h, v)$ for all $v \in V_h$.

**Lemma 1 ($I_H$ is a projection onto $V_H$).** $I_H v_H = v_H$ for every $v_H \in V_H$.

*Proof.* On each coarse element $v_H$ is linear, so the elementwise $L^2$ projection $\Pi_H$ returns it unchanged. Its two one-sided values at an interior coarse node agree, so their mean $E_H$ is the nodal value, and $E_H$ is 0 at the boundary nodes, where $v_H$ is 0. $\square$

Let $W = \{ w \in V_h : I_H w = 0 \}$. By Lemma 1, every $v \in V_h$ splits as $v = I_H v + (v - I_H v)$ with $v - I_H v \in W$, so $V_h = V_H \oplus W$.

**Lemma 2 (the interpolation estimate).** For every $v \in V_h$, $\|v - I_H v\|_{L^2} \le C_I H \|v'\|_{L^2}$ with $C_I = (1 + 4\sqrt 3)/\pi < 2.53$.

*Proof.* Fix a coarse element $K$. Since $\Pi_H$ is the best $L^2$ approximation in the linear functions, which contain the constants, the Poincare-Wirtinger inequality gives $\|v - \Pi_H v\|_K \le (H/\pi) \|v'\|_K$. For the second part, two facts on an interval of length $H$: a linear $p$ has $\|p\|_K^2 \le (H/2)(p_l^2 + p_r^2)$ and $p_l^2 + p_r^2 \le (6/H) \|p\|_K^2$, because the element mass matrix $(H/6)\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ has eigenvalues $H/6$ and $H/2$. Let $x_i$ be an end of $K$ and $g = v - \Pi_H v$ on $K$. With $w = v - v(x_i)$, $g = w - \Pi_H w$, so $g(x_i) = -(\Pi_H w)(x_i)$ and

$$|g(x_i)| \le \sqrt{6/H}\, \|\Pi_H w\|_K \le \sqrt{6/H}\, \|w\|_K \le \sqrt{6/H}\, \frac{2H}{\pi} \|v'\|_K,$$

by the bound on $p_l^2 + p_r^2$, the stability of the projection and the Poincare inequality for a function that vanishes at one end, with constant $2H/\pi$. On $K$, $\Pi_H v - E_H \Pi_H v$ is linear with end values $\delta$. At an interior node, $\delta$ is half the jump of $\Pi_H v$, which is $\tfrac12 (g_{K'}(x_i) - g_K(x_i))$ for the neighbor $K'$ because $v$ is continuous. At a boundary node, $\delta = (\Pi_H v)(x_i) = -g(x_i)$, since $v(x_i) = 0$. In both cases $\delta^2 \le (24 H/\pi^2)(\|v'\|_K^2 + \|v'\|_{K'}^2)$, with $K' = K$ at the boundary. So $\|\Pi_H v - I_H v\|_K^2 \le (H/2)(\delta_l^2 + \delta_r^2)$, and the sum over all $K$ counts each $\|v'\|_K^2$ at most four times:

$$\|\Pi_H v - I_H v\|_{L^2}^2 \le \frac{H}{2} \cdot \frac{24 H}{\pi^2} \cdot 4 \|v'\|^2 = \frac{48 H^2}{\pi^2} \|v'\|^2.$$

The triangle inequality gives $\|v - I_H v\| \le (H/\pi)(1 + \sqrt{48}) \|v'\|$. $\square$

**Lemma 3 (the ideal correctors).** Let $Q = \sum_K Q_K$ with $Q_K v \in W$ and $a(Q_K v, w) = a_K(v, w)$ for all $w \in W$, which is line L3 with the whole domain as the patch. Then $a(v - Q v, w) = 0$ for all $v \in V_H$ and $w \in W$, and the space $V_{ms} = (1 - Q) V_H$ satisfies $V_h = V_{ms} \oplus W$ with the two parts $a$-orthogonal.

*Proof.* Each $Q_K v$ exists and is unique, because $a$ is an inner product on the subspace $W$ (Riesz, or the positive definite Gram matrix). Summing over $K$, $a(Q v, w) = \sum_K a_K(v, w) = a(v, w)$, which is the orthogonality. In the code, line L3 imposes $I_H w = 0$ with Lagrange multipliers; when the saddle point matrix is nonsingular (the elimination in `solve` stops with an error otherwise), its solution is this $Q_K v$, because the first block row says $a(Q_K v, w) = a_K(v, w)$ for $w$ in the kernel of the constraints and the second says $Q_K v \in W$. For the splitting: $I_H (1 - Q) v = v$ for $v \in V_H$ by Lemma 1 and $Q v \in W$, so $1 - Q$ is one to one on $V_H$. For $v \in V_h$, write $v = (1 - Q) I_H v + r$; then $I_H r = I_H v - I_H v = 0$, so $r \in W$. A function in both $V_{ms}$ and $W$ is $a$-orthogonal to itself, hence zero. $\square$

**Theorem (the ideal method).** Let $u_{ms}$ be the Galerkin solution of lines L4 to L6 with global patches. Then

$$\|u_h - u_{ms}\|_a \le \frac{C_I H}{\sqrt \alpha} \|f_h\|_{L^2}.$$

*Proof.* By Lemma 3, $u_h = v + e$ with $v \in V_{ms}$ and $e \in W$. For $\phi \in V_{ms}$, $a(v, \phi) = a(u_h, \phi) - a(e, \phi) = (f_h, \phi)$, so $v$ solves the Galerkin problem, whose matrix is the Gram matrix of a basis and is nonsingular, and $v = u_{ms}$. Then $e = u_h - u_{ms} \in W$, and $a(u_{ms}, e) = 0$ gives

$$\|e\|_a^2 = a(u_h, e) = (f_h, e) = (f_h, e - I_H e) \le \|f_h\|\, C_I H\, \|e'\| \le \|f_h\|\, \frac{C_I H}{\sqrt \alpha} \|e\|_a,$$

by $I_H e = 0$, Lemma 2 and $a \ge \alpha$. Divide by $\|e\|_a$. $\square$

The constant depends only on $\alpha$ and not on $\beta$, on how $a$ oscillates, or on any period. This is the difference from the [multiscale finite element method](/multiscale-finite-element-method/) in several dimensions, whose error has a resonance term.

**The localized method.** With patches of $k$ layers, lines L1 to L3 give correctors $Q_k$ and the space $V_{ms, k} = (1 - Q_k) V_H$, and lines L4 to L6 are the Galerkin method in it. By the Cea lemma, for any choice of $v \in V_{ms, k}$,

$$\|u_h - u_{ms, k}\|_a \le \|u_h - v\|_a \le \|u_h - u_{ms}\|_a + \|(Q - Q_k) I_H u_{ms}\|_a,$$

taking $v = (1 - Q_k) I_H u_{ms}$ and using $u_{ms} = (1 - Q) I_H u_{ms}$. The first term is the error of the theorem. The second is the localization error. Malqvist and Peterseim proved that it decays like $\exp(-c k)$ times $H^{-1}$ factors of polynomial size, with $c$ depending on the contrast $\beta/\alpha$; we use that result and do not prove it here. If the patch of every element is the whole domain, which happens for $k \ge M - 1$, then $Q_k = Q$ and the localized method equals the ideal one, as the tests check.
