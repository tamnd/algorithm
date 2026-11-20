---
title: Proof of the Bramble-Hilbert lemma and the interpolation estimate
proves: [statement]
status: full
---

Throughout, $\Omega \subset \mathbb{R}^d$ is bounded, connected and Lipschitz, $k \ge 0$, $A_k = \{\alpha : |\alpha| \le k\}$ is the set of multi-indices of order at most $k$, and $\mathcal{P}_k$ is the space of polynomials of total degree at most $k$. The monomials $x^\alpha$ with $\alpha \in A_k$ are a basis of $\mathcal{P}_k$, so $\dim\mathcal{P}_k = |A_k|$.

**Lemma 1 (zero seminorm).** If $u \in H^{k+1}(\Omega)$ and $|u|_{k+1} = 0$, then $u \in \mathcal{P}_k$.

*Proof.* By induction on $k$. For $k = 0$, $u$ has weak gradient zero. Its mollification $u_\varepsilon = u * \eta_\varepsilon$ has gradient $(\nabla u) * \eta_\varepsilon = 0$ on $\{x : \operatorname{dist}(x, \partial\Omega) > \varepsilon\}$, so it is constant on every ball in that set. Since $u_\varepsilon \to u$ in $L^1_{\mathrm{loc}}(\Omega)$, $u$ is constant almost everywhere on every ball in $\Omega$, and a function that is locally constant on a connected open set is constant. For $k \ge 1$, every $D^\alpha u$ with $|\alpha| = k$ has weak gradient zero, so it equals a constant $c_\alpha$. Let $p = \sum_{|\alpha| = k} c_\alpha x^\alpha/\alpha!$. For $|\alpha| = |\beta| = k$ we have $D^\alpha(x^\beta/\beta!) = 1$ if $\alpha = \beta$ and $0$ otherwise, so $D^\alpha(u - p) = 0$ for all $|\alpha| = k$. Then $|u - p|_k = 0$, the induction hypothesis gives $u - p \in \mathcal{P}_{k-1}$, and so $u \in \mathcal{P}_k$. $\square$

**Lemma 2 (moments).** The linear map $\Phi : \mathcal{P}_k \to \mathbb{R}^{A_k}$, $\Phi(q) = \bigl(\int_\Omega D^\alpha q\,dx\bigr)_{\alpha \in A_k}$, is a bijection.

*Proof.* Both spaces have dimension $|A_k|$, so it is enough to show that $\Phi$ is one to one. Let $\Phi(q) = 0$ and suppose that $q \ne 0$ has degree $j \le k$, $q = \sum_{|\beta| \le j} a_\beta x^\beta$. For $|\alpha| = j$ the derivative $D^\alpha q = \alpha!\,a_\alpha$ is constant, so $0 = \int_\Omega D^\alpha q = \alpha!\,a_\alpha|\Omega|$ and $a_\alpha = 0$. All coefficients of degree $j$ vanish, which contradicts the choice of $j$. $\square$

**Lemma 3 (norm equivalence).** Let $|||u||| = |u|_{k+1} + \sum_{\alpha \in A_k}\bigl|\int_\Omega D^\alpha u\,dx\bigr|$. There is $C$ with $\|u\|_{k+1} \le C\,|||u|||$ for all $u \in H^{k+1}(\Omega)$.

*Proof.* Suppose not. Then there are $u_n$ with $\|u_n\|_{k+1} = 1$ and $|||u_n||| < 1/n$. Because $\Omega$ is bounded and Lipschitz, the Rellich-Kondrachov theorem says that $H^1(\Omega) \to L^2(\Omega)$ is compact. Applied to each $D^\alpha u_n$ with $|\alpha| \le k$, it gives a subsequence, still called $u_n$, that converges in $H^k(\Omega)$. Also $D^\alpha u_n \to 0$ in $L^2$ for $|\alpha| = k+1$, because $|u_n|_{k+1} \to 0$. Since $\|v\|_{k+1}^2 = \|v\|_k^2 + |v|_{k+1}^2$, the sequence is Cauchy in $H^{k+1}(\Omega)$, and it has a limit $u$ with $\|u\|_{k+1} = 1$ and $|u|_{k+1} = 0$. Convergence in $L^2$ on a bounded set implies convergence of integrals, so $\int_\Omega D^\alpha u = \lim_n \int_\Omega D^\alpha u_n = 0$ for every $\alpha \in A_k$. By Lemma 1, $u \in \mathcal{P}_k$. By Lemma 2, $u = 0$. This contradicts $\|u\|_{k+1} = 1$. $\square$

**Part 1.** Let $u \in H^{k+1}(\Omega)$. By Lemma 2 there is $q \in \mathcal{P}_k$ with $\int_\Omega D^\alpha q = \int_\Omega D^\alpha u$ for all $\alpha \in A_k$. All derivatives of order $k+1$ of $q$ vanish, so $|||u - q||| = |u - q|_{k+1} = |u|_{k+1}$, and Lemma 3 gives $\|u - q\|_{k+1} \le C|u|_{k+1}$. $\square$

**Part 2.** With $q$ from Part 1, $\ell(u) = \ell(u - q)$ because $\ell(q) = 0$, so $|\ell(u)| \le C_\ell\|u - q\|_{k+1} \le C\,C_\ell\,|u|_{k+1}$. $\square$

**Part 3.** Let $F(\hat x) = x_0 + \delta\hat x$ map $\Omega$ onto $\Omega_\delta$, and for $v$ on $\Omega_\delta$ let $\hat v = v \circ F$. The chain rule gives $\hat D^\alpha\hat v = \delta^{|\alpha|}(D^\alpha v)\circ F$, and $dx = \delta^d\,d\hat x$. Hence

$$|\hat v|_{m, \Omega}^2 = \sum_{|\alpha| = m}\int_\Omega \delta^{2m}\,|D^\alpha v(F(\hat x))|^2\,d\hat x = \delta^{2m - d}\,|v|_{m, \Omega_\delta}^2 .$$

Given $u$ on $\Omega_\delta$, apply Part 1 to $\hat u$ and get $\hat q$. Then $q = \hat q \circ F^{-1} \in \mathcal{P}_k$, and for $0 \le m \le k+1$

$$|u - q|_{m, \Omega_\delta} = \delta^{d/2 - m}|\hat u - \hat q|_{m, \Omega} \le \delta^{d/2 - m}\,C\,|\hat u|_{k+1, \Omega} = C\,\delta^{k+1-m}|u|_{k+1, \Omega_\delta}. \qquad \square$$

**The corollary.** Let $\hat K$ be the reference simplex, with diameter $\hat h$, and let $\hat\rho$ be the diameter of the largest ball in $\hat K$. For a cell $K$ of the mesh let $h_K$ and $\rho_K$ be the same quantities, and let $F_K(\hat x) = B\hat x + b$ be an affine map of $\hat K$ onto $K$.

*Step 1 (the map).* Let $|\hat y| = \hat\rho$. The ball of diameter $\hat\rho$ in $\hat K$ contains two points $\hat x$ and $\hat z$ with $\hat x - \hat z = \hat y$, and $B\hat y = F_K(\hat x) - F_K(\hat z)$ is a difference of two points of $K$. So $|B\hat y| \le h_K$ and $\|B\| \le h_K/\hat\rho$. The same argument for $F_K^{-1}$ gives $\|B^{-1}\| \le \hat h/\rho_K$. Also $|\det B| = |K|/|\hat K|$.

*Step 2 (seminorms under the map).* Let $\hat v = v \circ F_K$. For $|\alpha| = m$ the chain rule writes $\hat D^\alpha\hat v(\hat x)$ as a sum of $d^m$ terms, each a product of $m$ entries of $B$ and one derivative $D^\beta v(F_K(\hat x))$ with $|\beta| = m$. Every entry of $B$ is at most $\|B\|$ in size. Squaring, summing over $\alpha$ and changing variables with $d\hat x = dx/|\det B|$ gives, with a constant $c$ that depends only on $d$ and $m$,

$$|\hat v|_{m, \hat K} \le c\,\|B\|^m|\det B|^{-1/2}|v|_{m, K}, \qquad |v|_{m, K} \le c\,\|B^{-1}\|^m|\det B|^{1/2}|\hat v|_{m, \hat K} .$$

*Step 3 (the reference interpolant).* Let $\hat a_i$ be the nodes and $\hat\phi_i$ the nodal basis of the Lagrange element of degree $k$ on $\hat K$, and let $\hat I\hat v = \sum_i \hat v(\hat a_i)\hat\phi_i$. Because $k + 1 > d/2$, the Sobolev embedding gives $\max_{\hat K}|\hat v| \le C_S\|\hat v\|_{k+1, \hat K}$, so $\|\hat I\hat v\|_{k+1, \hat K} \le C_S\sum_i\|\hat\phi_i\|_{k+1, \hat K}\,\|\hat v\|_{k+1, \hat K} = C_I\|\hat v\|_{k+1, \hat K}$. The interpolant reproduces $\mathcal{P}_k$, so for every $\hat q \in \mathcal{P}_k$

$$\hat v - \hat I\hat v = (\hat v - \hat q) - \hat I(\hat v - \hat q), \qquad \|\hat v - \hat I\hat v\|_{k+1, \hat K} \le (1 + C_I)\|\hat v - \hat q\|_{k+1, \hat K}.$$

$\hat K$ is convex, so it is connected and Lipschitz, and Part 1 on $\hat K$ gives $\hat q$ with $\|\hat v - \hat I\hat v\|_{k+1, \hat K} \le (1 + C_I)\hat C|\hat v|_{k+1, \hat K}$.

*Step 4 (back to $K$).* An affine map takes $\mathcal{P}_k$ to $\mathcal{P}_k$ and the nodes $\hat a_i$ to the nodes $a_i = F_K(\hat a_i)$ of $K$, so $(I_K u)\circ F_K = \hat I\hat u$. By Step 2, Step 3 and Step 2 again, for $0 \le m \le k+1$,

$$|u - I_K u|_{m, K} \le c\|B^{-1}\|^m|\det B|^{1/2}|\hat u - \hat I\hat u|_{m, \hat K} \le c'\,\|B^{-1}\|^m\|B\|^{k+1}|u|_{k+1, K} \le c'\,\frac{\hat h^m}{\hat\rho^{k+1}}\Bigl(\frac{h_K}{\rho_K}\Bigr)^m h_K^{k+1-m}|u|_{k+1, K}.$$

With $h_K/\rho_K \le \sigma$ this is the local estimate, with a constant that depends only on $d$, $k$ and $\sigma$.

*Step 5 (global).* For $m = 0$, square and sum over the cells. For $m = 1$, note that $I_h u$ is continuous, because neighboring cells share the nodes on their common face and a polynomial of degree $k$ on a face is fixed by those nodes. A function that is continuous and in $H^1$ on each cell is in $H^1(\Omega)$, and its weak gradient is the gradient on each cell. So $|u - I_h u|_1^2 = \sum_K|u - I_K u|_{1, K}^2 \le C^2\sum_K h_K^{2k}|u|_{k+1, K}^2 \le C^2h^{2k}|u|_{k+1}^2$. $\square$
