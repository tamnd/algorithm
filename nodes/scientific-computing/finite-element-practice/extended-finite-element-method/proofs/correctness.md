---
title: The one dimensional XFEM space contains the kinked and cracked solutions, and the Galerkin error is of order h
proves: [correctness]
status: full
---

**Setting.** Nodes $0 = x_0 < x_1 < \cdots < x_n = L$ with spacing at most $h$, hat functions $N_I$, and a point $c$ with $x_e < c < x_{e+1}$. Put $a = x_e$, $b = x_{e+1}$, $\varphi(x) = x - c$, and let $E = E_1 > 0$ on $(0, c)$ and $E = E_2 > 0$ on $(c, L)$, with $E_{\max} = \max(E_1, E_2)$. The crack enrichments are $\psi_e = H(\varphi) - H(\varphi(a)) = H(\varphi)$ and $\psi_{e+1} = H(\varphi) - H(\varphi(b)) = H(\varphi) - 1$. The interface enrichment is the ridge $\psi = N_e\,|\varphi(a)| + N_{e+1}\,|\varphi(b)| - |\varphi|$ on $[a, b]$, extended by zero outside $[a, b]$ (as in the code, which uses it on the cut element only), for both nodes. The discrete space $V_h$ is spanned by all $N_I$ and by $N_e\psi_e, N_{e+1}\psi_{e+1}$ (crack) or $N_e\psi, N_{e+1}\psi$ (interface).

For the crack, $V$ is the set of functions in $H^1(0, c)$ and $H^1(c, L)$ (separately), and $A(u, v) = \int_0^L E u'v'\,dx + k\,[u][v]$ with $k > 0$. For the interface, $V = H^1(0, L)$ and $A(u, v) = \int_0^L E u'v'\,dx$. In both cases $V_0$ is the subspace with $v(0) = v(L) = 0$, the energy norm is $\|v\|_A = A(v, v)^{1/2}$, and the exact and discrete solutions satisfy $A(u, v) = \int f v$ for all $v$ in $V_0$ and in $V_h \cap V_0$, with $u(0) = u_h(0) = u_0$ and $u(L) = u_h(L) = u_L$.

**Lemma 1 (the enrichments are local and vanish at the nodes).** Every enriched function is zero outside $[a, b]$ and at every node.

*Proof.* $N_e$ is zero outside $[x_{e-1}, b]$. On $[x_{e-1}, a]$ we have $\varphi < 0$, so $\psi_e = H(\varphi) = 0$ there. In the same way $N_{e+1}$ is zero outside $[a, x_{e+2}]$, and $\psi_{e+1} = H(\varphi) - 1 = 0$ on $[b, x_{e+2}]$. The ridge is zero outside $[a, b]$ by definition, and zero at $a$ and $b$ because $N_e(a)\,|\varphi(a)| = |\varphi(a)|$ and $N_{e+1}(a) = 0$ there, and symmetrically at $b$. So it is continuous on $[0, L]$. At the nodes $a$ and $b$ the crack functions are $N_e(a)\,\psi_e(a) = 1 \cdot 0$, $N_e(b) = 0$, $N_{e+1}(a) = 0$ and $N_{e+1}(b)\,\psi_{e+1}(b) = 1 \cdot 0$. $\square$

So $u_h(x_I) = u_I$ for every node, the Dirichlet values of line L6 are the boundary values of $u_h$, and $V_h \subset V$: the crack functions are linear on each side of $c$, and the ridge functions are continuous (they vanish at $a$ and $b$).

**Lemma 2 (span on the cut element).** On $[a, b]$:

1. The crack functions $N_e, N_{e+1}, N_e\psi_e, N_{e+1}\psi_{e+1}$ span exactly the functions that are linear on $[a, c)$ and linear on $(c, b]$, a space of dimension 4, so they are linearly independent.
2. The ridge functions $N_e, N_{e+1}, N_e\psi, N_{e+1}\psi$ are linearly independent, and their span contains every continuous function that is linear on $[a, c]$ and on $[c, b]$.

*Proof.* (1) The four functions are linear on each side, so the span is inside that space, which has dimension $2 + 2 = 4$. On $[a, c)$, $H = 0$, so a combination $\alpha N_e + \beta N_{e+1} + \gamma N_e H + \delta N_{e+1}(H - 1)$ is $\alpha N_e + (\beta - \delta)N_{e+1}$. On $(c, b]$ it is $(\alpha + \gamma)N_e + \beta N_{e+1}$. Any pair of linear functions $(p N_e + q N_{e+1}, r N_e + s N_{e+1})$ comes from $\alpha = p$, $\gamma = r - p$, $\beta = s$, $\delta = s - q$. So the span has dimension 4 and the four functions are independent.

(2) Since $N_e + N_{e+1} = 1$ on $[a, b]$, the span contains $\psi = N_e\psi + N_{e+1}\psi$. The function $\psi$ is continuous, linear on each side of $c$, zero at $a$ and $b$, and $\psi(c) = N_e(c)\,(c - a) + N_{e+1}(c)\,(b - c) = 2(c - a)(b - c)/(b - a) > 0$. A continuous function $g$ that is linear on each side is fixed by $g(a)$, $g(c)$ and $g(b)$, and $g = g(a)\,N_e + g(b)\,N_{e+1} + \frac{g(c) - g(a)N_e(c) - g(b)N_{e+1}(c)}{\psi(c)}\,\psi$, because both sides are linear on each side and agree at $a$, $c$ and $b$. For independence, let $\alpha N_e + \beta N_{e+1} + \gamma N_e\psi + \delta N_{e+1}\psi = 0$. At $a$ and $b$ the ridge is zero, so $\alpha = \beta = 0$. The function $|\varphi|$ is convex and not affine on $[a, b]$, so its chord $N_e|\varphi(a)| + N_{e+1}|\varphi(b)|$ is strictly above it on $(a, b)$ and $\psi > 0$ there. Then $\gamma N_e + \delta N_{e+1} = 0$ on $(a, b)$, so $\gamma = \delta = 0$. $\square$

With Lemma 1, the global functions are linearly independent too: outside $[a, b]$ only the standard hats are nonzero, and they are independent of each other and of the local functions.

**Lemma 3 (coercivity).** $A$ is symmetric and $A(v, v) > 0$ for every nonzero $v \in V_0$. On the finite dimensional $V_h \cap V_0$ the stiffness matrix is therefore symmetric positive definite and line L6 has a unique solution.

*Proof.* Symmetry is clear. If $A(v, v) = 0$, then $v' = 0$ on $(0, c)$ and on $(c, L)$, and (crack) $[v] = 0$ because $k > 0$. So $v$ is constant on each side. $v(0) = 0$ makes the left constant zero and $v(L) = 0$ the right one. In the interface case $v$ is continuous and constant, so $v = 0$ as well. A symmetric matrix $M$ with $z^\top M z = A(v_z, v_z) > 0$ for every nonzero coefficient vector $z$ (nonzero by the linear independence above) is positive definite. $\square$

**Theorem 1 (best approximation).** $\|u - u_h\|_A = \min \{\|u - w\|_A : w \in V_h,\ w(0) = u_0,\ w(L) = u_L\}$.

*Proof.* For such $w$, $u_h - w \in V_h \cap V_0$, and subtracting the two weak forms gives the orthogonality $A(u - u_h, v) = 0$ for $v \in V_h \cap V_0$. Then $\|u - w\|_A^2 = \|u - u_h\|_A^2 + 2A(u - u_h, u_h - w) + \|u_h - w\|_A^2 = \|u - u_h\|_A^2 + \|u_h - w\|_A^2 \ge \|u - u_h\|_A^2$. $\square$

**Theorem 2 (exactness for piecewise linear solutions).** If $f = 0$, then $u_h = u$ for every position of $c$.

*Proof.* With $f = 0$, $(E u')' = 0$ on each side, so $\sigma = E u'$ is constant on each side. The interface condition (continuity of $E u'$, or of the force through the spring) makes it one constant $\sigma$, and $u$ is linear on $(0, c)$ and on $(c, L)$, continuous for the interface and with jump $\sigma/k$ for the crack. Integrating, $u_L - u_0 = \sigma\,(c/E_1 + (L - c)/E_2 + 1/k)$ (no last term for the interface), which is the formula of the reference code. Such a $u$ is linear on each uncut element, so it is a combination of hats there, and on $[a, b]$ it lies in the span of Lemma 2. So $u \in V_h$ with the right boundary values, and Theorem 1 gives $\|u - u_h\|_A = 0$. By Lemma 3 applied to $u - u_h \in V_0$, $u_h = u$. $\square$

**Theorem 3 (order h with a load).** Let $u$ restricted to $(0, c)$ and to $(c, L)$ be in $H^2$. Then

$$\|u - u_h\|_A \le \sqrt{E_{\max}}\,\frac{h}{\pi}\,\Big(\int_0^c (u'')^2\,dx + \int_c^L (u'')^2\,dx\Big)^{1/2}.$$

*Proof.* Let $w$ be the function that is linear on each uncut element and on $[a, c]$ and $[c, b]$, with $w = u$ at all nodes and $w(c^\pm) = u(c^\pm)$. For the interface $u(c^-) = u(c^+)$, so $w$ is continuous. By Lemma 2, $w$ is in $V_h$, and $w$ has the boundary values of $u$. On every piece $[p, q]$ (an uncut element, $[a, c]$ or $[c, b]$), the error $\eta = u - w$ vanishes at $p$ and $q$, so $\eta'$ has mean zero on $[p, q]$. The Poincaré inequality for functions with mean zero on an interval of length $\ell$, $\int_p^q g^2 \le (\ell/\pi)^2 \int_p^q (g')^2$ (Wirtinger's inequality, from the cosine series of $g$), applied to $g = \eta'$ with $g' = u''$, gives $\int_p^q (\eta')^2 \le (h/\pi)^2 \int_p^q (u'')^2$. For the crack $[w] = u(c^+) - u(c^-) = [u]$, so $[\eta] = 0$ and the spring term of $\|\eta\|_A^2$ is zero. Summing over the pieces with $E \le E_{\max}$, $\|u - w\|_A^2 \le E_{\max}(h/\pi)^2 \int (u'')^2$, and Theorem 1 finishes the proof. $\square$

**Remark (standard elements).** Without enrichment, the best linear approximation on the cut element of a function whose derivative jumps by $\delta = |u'(c^+) - u'(c^-)|$ has a derivative error of order $\delta$ on a set of length of order $h$, so the energy error is of order $\delta\sqrt h$. The reference tests measure the order $0.50$ for $f = 0$ and $0.55$ at the finest mesh for $f = 1$. Theorems 2 and 3 show that XFEM removes this loss and keeps the order of linear elements.
