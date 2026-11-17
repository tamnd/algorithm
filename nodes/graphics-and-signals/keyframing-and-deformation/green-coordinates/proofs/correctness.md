---
title: Green coordinates reproduce the point and the constants, reproduce similarities, and give a holomorphic map in 2D
proves: [correctness]
status: full
---

We use the notation of the page.
$\Omega$ is the inside of the cage, $\eta \in \Omega$, and $G(\xi, \eta) = \frac{1}{2\pi}\ln|\xi - \eta|$, which satisfies $\Delta_\xi G = \delta_\eta$.
On edge $j$ we write $\xi = a + td$ with $d = b - a$ and $t \in [0, 1]$, so $ds = |d|\,dt$.

## The closed forms of lines L4 to L7

**Lemma 1.** On edge $j$, $(\xi - \eta) \cdot n_j = h$ for every $\xi$ on the edge, $\frac{\partial G}{\partial n}(\xi, \eta) = \frac{h}{2\pi q(t)}$, and $G(\xi, \eta) = \frac{1}{4\pi}\ln q(t)$.

*Proof.*
$(\xi - \eta) \cdot n_j = (a - \eta) \cdot n_j + t\,d \cdot n_j$, and $d \cdot n_j = 0$.
$\nabla_\xi G = \frac{\xi - \eta}{2\pi|\xi - \eta|^2}$, so $\partial G/\partial n = \nabla_\xi G \cdot n_j = h/(2\pi q)$.
The last claim is $\ln|\xi - \eta| = \frac12\ln q$. $\square$

So $\phi_j$ gets $\int_0^1 (1 - t)\frac{h}{2\pi q}|d|\,dt = \frac{h|d|}{2\pi}(I_0 - I_1)$ from edge $j$, and $\phi_{j+1}$ gets $\frac{h|d|}{2\pi}I_1$, which is line L6. And $\psi_j = -\int_0^1 \frac{1}{4\pi}\ln q\,|d|\,dt = -\frac{|d|}{4\pi}\Lambda$, which is line L7.
The antiderivatives of $1/q$, $t/q$ and $\ln q$ for a quadratic $q$ with no real zero are standard; the tests compare the closed forms with Gauss-Legendre quadrature on 384 points per edge.

## Reproduction

**Theorem 1.** For every $\eta \in \Omega$: $\sum_i \phi_i(\eta) = 1$ and $\sum_i \phi_i(\eta)v_i + \sum_j \psi_j(\eta)n_j = \eta$.

*Proof.*
Green's second identity on $\Omega$ for a function $u$ that is harmonic on a neighbourhood of the closure of $\Omega$, and for $G(\cdot, \eta)$, gives Green's third identity:

$$u(\eta) = \int_{\partial\Omega}\Big(u(\xi)\frac{\partial G}{\partial n}(\xi, \eta) - G(\xi, \eta)\frac{\partial u}{\partial n}(\xi)\Big)ds(\xi).$$

For $u = 1$ the second term is 0, and $1 = \sum_i\Gamma_i$ on the boundary, so $1 = \sum_i\int\Gamma_i\,\partial G/\partial n\,ds = \sum_i\phi_i$.
For $u(\xi) = \xi$, applied to each coordinate, $\partial u/\partial n = n_j$ on edge $j$, and $\xi = \sum_i\Gamma_i(\xi)v_i$ on the boundary, because $\Gamma_j = 1 - t$ and $\Gamma_{j+1} = t$ on edge $j$.
So $\eta = \sum_i v_i\int\Gamma_i\,\partial G/\partial n\,ds - \sum_j n_j\int_{e_j}G\,ds = \sum_i\phi_iv_i + \sum_j\psi_jn_j$. $\square$

**Corollary.** With $v' = v$, line L9 returns $\eta$, because then $s_j = 1$ and $n'_j = n_j$.

## Similarities

**Theorem 2.** Let $v'_i = Mv_i + c$ for every $i$, where $M = \lambda Q$ with a rotation $Q$ and $\lambda > 0$. Then line L9 returns $M\eta + c$.

*Proof.*
Every edge vector becomes $Md$, so $s_j = |Md|/|d| = \lambda$, and the outward normal becomes $n'_j = Qn_j$, because $Q$ is a rotation and keeps the orientation.
So $s_jn'_j = \lambda Qn_j = Mn_j$, and line L9 gives $\sum_i\phi_i(Mv_i + c) + \sum_j\psi_jMn_j = M(\sum_i\phi_iv_i + \sum_j\psi_jn_j) + c\sum_i\phi_i = M\eta + c$, by Theorem 1. $\square$

## The map is a Cauchy integral

We identify $\mathbb{R}^2$ with $\mathbb{C}$.
Let $g$ be the piecewise linear map of the cage boundary onto the moved cage: on edge $j$, $g(a + td) = a' + td'$, with $a' = v'_j$ and $d' = v'_{j+1} - v'_j$.
So $g(\xi) = a' + \beta_j(\xi - a)$ on edge $j$ with $\beta_j = d'/d$.
For a counterclockwise cage, the outward normal of edge $j$ is $n_j = -i\,d/|d|$, and then $s_jn'_j = \frac{|d'|}{|d|}\cdot(-i)\frac{d'}{|d'|} = \beta_jn_j$.

**Lemma 2.** On edge $j$, with $r = |\xi - \eta|$: $\frac{\partial G}{\partial n}ds = \frac{1}{2\pi}\operatorname{Im}\frac{d\xi}{\xi - \eta}$ and $\operatorname{Re}\frac{d\xi}{\xi - \eta} = d(\ln r)$, the derivative of $\ln r$ along the edge.

*Proof.*
$\frac{d\xi}{\xi - \eta} = \frac{d\,\overline{(\xi - \eta)}}{r^2}dt$.
Its imaginary part is $\frac{\operatorname{Im}(d\,\overline{(\xi - \eta)})}{r^2}dt$, and $\operatorname{Im}(d\,\overline{w}) = -\operatorname{Im}(w\,\overline{d}) = \operatorname{Re}(w\cdot i\overline{d}) = |d|\,w \cdot n_j$ for $w = \xi - \eta$, because $\overline{n_j} = i\overline{d}/|d|$ and $w \cdot n = \operatorname{Re}(w\overline{n})$. So the imaginary part is $\frac{|d|h}{r^2}dt = 2\pi\frac{\partial G}{\partial n}ds$ by Lemma 1.
Its real part is $\frac{\operatorname{Re}(d\,\overline{w})}{r^2}dt = \frac{d \cdot w}{r^2}dt = \frac{1}{2}\frac{dq}{q} = d(\ln r)$. $\square$

**Theorem 3.** Line L9 returns $f(\eta) = \frac{1}{2\pi i}\oint_{\partial\Omega}\frac{g(\xi)}{\xi - \eta}d\xi$.

*Proof.*
$\frac{1}{2\pi i}w = \frac{1}{2\pi}(\operatorname{Im}w - i\operatorname{Re}w)$ for every complex $w$. So, by Lemma 2,

$$\frac{1}{2\pi i}\int_{e_j}\frac{g\,d\xi}{\xi - \eta} = \int_{e_j}g\frac{\partial G}{\partial n}ds - \frac{i}{2\pi}\int_{e_j}g\,d(\ln r).$$

Integrate the last term by parts: $\int_{e_j}g\,d(\ln r) = [g\ln r]_{v_j}^{v_{j+1}} - \int_{e_j}\ln r\,dg$, and $dg = \beta_j\,d\xi = \beta_j\frac{d}{|d|}ds = i\beta_jn_j\,ds$.
So $-\frac{i}{2\pi}\int_{e_j}g\,d(\ln r) = -\frac{i}{2\pi}[g\ln r]_{v_j}^{v_{j+1}} - \beta_jn_j\int_{e_j}G\,ds = -\frac{i}{2\pi}[g\ln r]_{v_j}^{v_{j+1}} + \psi_js_jn'_j$.
Sum over all edges. The bracket terms cancel, because $g$ and $\ln r$ are continuous at every vertex and the boundary is closed.
The first terms add up to $\int_{\partial\Omega}g\,\partial G/\partial n\,ds = \sum_iv'_i\int\Gamma_i\,\partial G/\partial n\,ds = \sum_i\phi_iv'_i$, since $g = \sum_i\Gamma_iv'_i$ on the boundary.
So the sum is $\sum_i\phi_iv'_i + \sum_j\psi_js_jn'_j$, which is line L9. $\square$

**Corollary (conformal in 2D).** $f$ is holomorphic in $\Omega$, so it satisfies the Cauchy-Riemann equations, and it keeps angles at every point where $f'(\eta) \ne 0$.

*Proof.*
$g$ is bounded on the boundary, and $\frac{1}{\xi - \eta}$ is holomorphic in $\eta$ with derivatives bounded uniformly for $\eta$ in a compact subset of $\Omega$, so differentiation under the integral sign shows that $f$ is complex differentiable in $\Omega$. A holomorphic map with $f' \ne 0$ is conformal. $\square$

Theorem 3 also explains Theorem 2 and the shear of the example: if $g$ extends to a holomorphic map $\hat g$ on $\Omega$, Cauchy's formula gives $f = \hat g$; a similarity $\xi \mapsto M\xi + c$ is holomorphic, while a shear $\xi \mapsto \xi + \frac12\operatorname{Im}\xi$ is not, and it is not reproduced.
