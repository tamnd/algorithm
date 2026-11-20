---
title: The boundary integral equation, the exact element integrals and the discrete Gauss law
proves: [correctness]
status: partial
---

**Setting.** $\Omega \subset \mathbb R^2$ is a bounded domain whose boundary $\Gamma$ is a simple closed polygon, traversed counterclockwise, with outward unit normal $n$. $G(x, y) = -\frac{1}{2\pi}\ln|x - y|$, so $-\Delta_y G(x, \cdot) = \delta_x$. The function $u$ is harmonic in $\Omega$ and continuously differentiable up to $\Gamma$, and $q = \partial u/\partial n$. The status is partial because the convergence of midpoint collocation is cited, not proved (Remark 2).

**Lemma 1 (representation formula).** For $x \in \Omega$, $u(x) = \int_\Gamma G(x, y)\,q(y)\,ds_y - \int_\Gamma \partial_{n_y} G(x, y)\,u(y)\,ds_y$.

*Proof.* Let $D_\epsilon$ be the disc of radius $\epsilon$ around $x$, inside $\Omega$, and $\Omega_\epsilon = \Omega \setminus \overline{D_\epsilon}$. On $\Omega_\epsilon$ both $u$ and $G(x, \cdot)$ are harmonic, so Green's second identity gives $\int_{\partial\Omega_\epsilon}(G\,\partial_n u - u\,\partial_n G)\,ds = 0$. The boundary of $\Omega_\epsilon$ is $\Gamma$ and the circle $|y - x| = \epsilon$, with the normal pointing toward $x$ on the circle. On the circle $G = -\frac{1}{2\pi}\ln\epsilon$ and $\partial_n G = \frac{1}{2\pi\epsilon}$ (the normal points toward $x$, where $G$ grows). So the circle contributes $-\frac{\ln\epsilon}{2\pi}\int \partial_n u\,ds - \frac{1}{2\pi\epsilon}\int u\,ds$. The first term is $O(\epsilon\ln\epsilon)$ because $\partial_n u$ is bounded, and the second tends to $-u(x)$ by continuity. Letting $\epsilon \to 0$ gives $\int_\Gamma (G q - u\,\partial_n G)\,ds - u(x) = 0$. $\square$

**Lemma 2 (the boundary equation).** For $x$ on $\Gamma$ in the interior of a straight side, $\tfrac12 u(x) + \int_\Gamma \partial_{n_y} G(x, y)\,u(y)\,ds_y = \int_\Gamma G(x, y)\,q(y)\,ds_y$, where both integrals exist as ordinary integrals.

*Proof.* Near $x$ the side is a line through $x$, and for $y$ on it, $(y - x)\cdot n_y = 0$, so $\partial_{n_y} G(x, y) = -\frac{(y - x)\cdot n_y}{2\pi|y - x|^2}$ vanishes there. Away from $x$ the kernel is bounded. So the double layer integral is an ordinary integral, and the single layer integral exists because $\ln|x - y|$ is integrable on a line. Repeat the proof of Lemma 1 with $\Omega_\epsilon = \Omega \setminus \overline{D_\epsilon}$ for this boundary point. For small $\epsilon$ the part of the circle inside $\Omega$ is a half circle, so the term $\frac{1}{2\pi\epsilon}\int u\,ds$ over it tends to $\tfrac12 u(x)$, and the logarithmic term tends to 0. The part of $\Gamma$ cut out by the disc has length $2\epsilon$, and its contribution tends to 0 because the double layer kernel is zero there and $\int_{-\epsilon}^{\epsilon}|\ln|s||\,ds \to 0$. $\square$

**Lemma 3 (closed forms).** Let a straight element run from $a$ to $b$ with length $L$, unit tangent $t$, normal $n = (t_2, -t_1)$, and let $s_0 = (x - a)\cdot t$ and $d = (x - a)\cdot n$. Then $\int_0^L \ln\sqrt{(s - s_0)^2 + d^2}\,ds = F(L - s_0) - F(-s_0)$ with $F$ as on the page, and $\int (y - x)\cdot n / |y - x|^2\,ds_y = -\theta$, where $\theta$ is the angle at $x$ between $a - x$ and $b - x$, taken with the sign of $d$.

*Proof.* With $y = a + s\,t$ we have $y - x = (s - s_0)\,t - d\,n$, so $|y - x|^2 = (s - s_0)^2 + d^2$. Put $w = s - s_0$. For $d \ne 0$, $F'(w) = \tfrac12\ln(w^2 + d^2) + \frac{w^2}{w^2 + d^2} - 1 + \frac{d^2}{w^2 + d^2} = \ln\sqrt{w^2 + d^2}$. For $d = 0$, $\frac{d}{dw}(w\ln|w| - w) = \ln|w|$, and the integral is improper but finite at $w = 0$. For the second integral, $(y - x)\cdot n = -d$, so it equals $-\int_{-s_0}^{L - s_0}\frac{d\,dw}{w^2 + d^2} = -\big[\arctan(w/d)\big]$. The bracket is the angle swept by the direction of $y - x$ as $y$ moves from $a$ to $b$. Its absolute value is the angle between $a - x$ and $b - x$, which is less than $\pi$, and its sign is that of $d$. For $d = 0$ both sides are zero. $\square$

The reference code uses exactly these formulas, with $h = -\frac{1}{2\pi}\int (y - x)\cdot n/|y - x|^2\,ds$, so lines L3 and L4 are exact up to rounding. At $x$ the midpoint of its own element, $s_0 = L/2$, $d = 0$, and $F(L/2) - F(-L/2) = L\ln(L/2) - L$.

**Theorem 1 (discrete Gauss law).** Let $x_i$ be the midpoint of element $i$. Then $\sum_j H_{ij} = 0$. So $H$ applied to a constant vector is zero, and if $G$ is nonsingular, the computed $q$ for constant Dirichlet data is zero.

*Proof.* Apply Lemma 2 to $u = 1$, which is harmonic with $q = 0$: $\tfrac12 + \int_\Gamma \partial_{n_y} G(x_i, y)\,ds_y = 0$. The integral over $\Gamma$ is the sum of the integrals over the elements, which are the off diagonal $H_{ij}$ by Lemma 3 (and zero for $j = i$). So $\tfrac12 + \sum_{j \ne i} H_{ij} = 0$, which is $\sum_j H_{ij} = 0$ since $H_{ii} = \tfrac12$. Note that this is an identity of exact integrals, not an approximation: the double layer of a constant is computed exactly. With constant data $u_j = c$, the system of line L5 is $G q = H u = 0$, so $q = 0$ if $G$ is nonsingular. $\square$

**Corollary 1.** At an interior point $x$, the same argument with Lemma 1 gives $\sum_j h_j(x) = -1$, so line L7 returns exactly $c$ for constant data. The reference tests check both identities to $10^{-14}$.

**Remark 1 (the kernel of the single layer).** On the circle of radius $R$, $\frac{1}{2\pi R}\int_{|y| = R}\ln|x - y|\,ds_y = \ln R$ for $|x| = R$ (the mean value of $\ln|x - y|$ over a circle through $x$). So the constant density lies in the kernel of the single layer for $R = 1$. Scaling the domain so that its diameter is less than 1 makes the single layer operator elliptic on $H^{-1/2}(\Gamma)$ (Steinbach 2008).

**Remark 2 (convergence, cited).** For the Galerkin method with the single layer operator and piecewise constants, ellipticity and Cea's lemma give quasi optimal convergence in $H^{-1/2}(\Gamma)$ (Steinbach 2008). The midpoint collocation of the code is the classical method of Symm. Its error at interior points, second order in the element length on the square, is measured by the reference tests and is not proved here.
