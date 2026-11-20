---
title: The adaptive loop with Dorfler marking and newest vertex bisection contracts the error
proves: [correctness]
status: full
---

**Setting.** $\Omega \subset \mathbb{R}^2$ is a polygon, and $u \in H^1_0(\Omega)$ solves $(\nabla u, \nabla v) = (f, v)$ for all $v \in H^1_0(\Omega)$. The energy norm is $|||v||| = \|\nabla v\|_{L^2(\Omega)}$. AFEM starts from a conforming triangulation $\mathcal{T}_0$ and builds $\mathcal{T}_1, \mathcal{T}_2, \ldots$ by the loop of the main page, lines L1 to L8. $V_k$ is the space of continuous piecewise linear functions on $\mathcal{T}_k$ that vanish on $\partial\Omega$, and $U_k \in V_k$ is the Galerkin solution. For $V \in V_k$ and $K \in \mathcal{T}_k$, with $h_K = |K|^{1/2}$ and $J(V)$ the jump of $\partial V / \partial n$ across interior edges,

$$\eta_k(V, K)^2 = h_K^2\|f\|_K^2 + h_K\|J(V)\|_{\partial K \setminus \partial\Omega}^2, \qquad \eta_k(V, \mathcal{A})^2 = \sum_{K \in \mathcal{A}}\eta_k(V, K)^2, \qquad \eta_k = \eta_k(U_k, \mathcal{T}_k).$$

For P1 functions $\Delta V = 0$ inside each triangle, so the element residual is $f$. We assume:

1. *(Exact solve.)* $U_k$ is the exact Galerkin solution on $V_k$.
2. *(Marking.)* $\mathcal{M}_k$ satisfies $\eta_k(U_k, \mathcal{M}_k)^2 \ge \theta\,\eta_k^2$ for a fixed $\theta \in (0, 1]$.
3. *(Refinement.)* $\mathcal{T}_{k+1}$ is the output of newest vertex bisection for $\mathcal{M}_k$. So it is conforming, every $K \in \mathcal{M}_k$ is bisected at least once, and all triangles stay in finitely many similarity classes (see [newest vertex bisection](/newest-vertex-bisection/)).
4. *(Data.)* The integrals of $f$ in the load vector and in $\|f\|_K^2$ are exact. The code uses the centroid rule, which is exact when $f$ is constant on each triangle of $\mathcal{T}_0$, as in the tests ($f = 0$ and $f = 1$).

We prove three claims.

1. *(Well defined.)* Each step has a unique $U_k$, and the loop stops.
2. *(Reliability is used, not proved.)* There is $C_{\mathrm{rel}}$ that depends only on the similarity classes of $\mathcal{T}_0$ with $|||u - U_k||| \le C_{\mathrm{rel}}\,\eta_k$. This is the standard upper bound of the [residual error estimator](/residual-error-estimator/) (Verfurth 2013, Chapter 1), and we use it as a lemma.
3. *(Contraction.)* There are $\gamma > 0$ and $\alpha \in (0, 1)$, which depend only on $\theta$ and on the similarity classes of $\mathcal{T}_0$, such that for every $k$

$$|||u - U_{k+1}|||^2 + \gamma\,\eta_{k+1}^2 \le \alpha^2\bigl(|||u - U_k|||^2 + \gamma\,\eta_k^2\bigr).$$

So $|||u - U_k||| \to 0$ and $\eta_k \to 0$ at least as fast as $\alpha^k$ in the step count. This is the contraction theorem of Cascon, Kreuzer, Nochetto and Siebert (2008), in the special case of the Laplacian and P1 elements.

**Proof of 1.** The Galerkin matrix of $V_k$ is symmetric. For $V \ne 0$ in $V_k$ the form $|||V|||^2$ is positive, because a function in $H^1_0$ with zero gradient is zero (Poincare inequality). So the matrix is positive definite, and $U_k$ exists and is unique. Conjugate gradients solve such a system, in exact arithmetic, in at most $\dim V_k$ steps. The loop at line L1 has at most max_steps passes. Line L6 marks a nonempty set when $\eta_k > 0$, and each bisection adds one vertex, so the node count grows in each pass, and line L4 stops the loop when it passes max_nodes.

**Lemma A (Pythagoras).** $|||u - U_{k+1}|||^2 = |||u - U_k|||^2 - |||U_{k+1} - U_k|||^2$.

*Proof.* NVB gives a conforming refinement, so $V_k \subset V_{k+1}$ and $U_{k+1} - U_k \in V_{k+1}$. Galerkin orthogonality gives $(\nabla(u - U_{k+1}), \nabla(U_{k+1} - U_k)) = 0$. Write $u - U_k = (u - U_{k+1}) + (U_{k+1} - U_k)$ and expand the square. $\square$

**Lemma B (estimator reduction).** Let $\lambda = 1 - 2^{-1/2}$. There is $C_E$ that depends only on the similarity classes, such that for every $\delta > 0$

$$\eta_{k+1}^2 \le (1 + \delta)\bigl(\eta_k^2 - \lambda\,\eta_k(U_k, \mathcal{M}_k)^2\bigr) + (1 + \delta^{-1})\,C_E\,|||U_{k+1} - U_k|||^2.$$

*Proof.* Write $\eta_{k+1}(V)$ for the fine estimator of any $V \in V_{k+1}$. The element part $h_K\|f\|_K$ does not depend on $V$, and $J$ is linear in $V$. So $\eta_{k+1}(V)$ is the Euclidean norm of a vector whose entries are $h_K\|f\|_K$ and $h_K^{1/2}\|J(V)\|_{\partial K}$, and the triangle inequality gives

$$\eta_{k+1}(U_{k+1}) \le \eta_{k+1}(U_k) + \Bigl(\sum_{K \in \mathcal{T}_{k+1}} h_K\|J(W)\|_{\partial K}^2\Bigr)^{1/2}, \qquad W = U_{k+1} - U_k,$$

where in the second term the element part is left out. For a P1 function $W$ the gradient is constant on each triangle, and on an edge $E = K \cap K'$ the jump satisfies $|J(W)|^2 \le 2|\nabla W|_K|^2 + 2|\nabla W|_{K'}|^2$. Also $h_K|E| \le c\,|K|$ and $|K'| \ge c'|K|$ with constants from the similarity classes. Summing over edges gives $\sum_K h_K\|J(W)\|_{\partial K}^2 \le C_E|||W|||^2$. Young's inequality $(a + b)^2 \le (1 + \delta)a^2 + (1 + \delta^{-1})b^2$ then gives

$$\eta_{k+1}^2 \le (1 + \delta)\,\eta_{k+1}(U_k)^2 + (1 + \delta^{-1})\,C_E\,|||U_{k+1} - U_k|||^2.$$

It remains to bound $\eta_{k+1}(U_k)$, the fine estimator of the coarse solution. Take $K \in \mathcal{T}_k$. If $K$ is not refined, its term is the same on both meshes. If $K$ is refined, let $K'$ be a child. Then $|K'| \le |K|/2$, so $h_{K'} \le 2^{-1/2}h_K$ and $h_{K'}^2 \le \tfrac12 h_K^2 \le 2^{-1/2}h_K^2$. $U_k$ is linear on $K$, so its jump on every new edge inside $K$ is zero. Every edge part of $\partial K'$ where the jump is not zero lies on $\partial K$, and these parts cover each edge of $K$ once. With exact integrals (assumption 4), $\sum_{K'}\|f\|_{K'}^2 = \|f\|_K^2$. So

$$\sum_{K' \subset K}\eta_{k+1}(U_k, K')^2 \le 2^{-1/2}\eta_k(U_k, K)^2.$$

Every marked triangle is refined, so $\eta_{k+1}(U_k)^2 \le \eta_k^2 - (1 - 2^{-1/2})\,\eta_k(U_k, \mathcal{M}_k)^2$. $\square$

**Proof of 3.** Write $e_k = |||u - U_k|||$ and $E_k = |||U_{k+1} - U_k|||$. Lemma B and the marking rule give

$$\eta_{k+1}^2 \le (1 + \delta)(1 - \lambda\theta)\,\eta_k^2 + (1 + \delta^{-1})\,C_E\,E_k^2.$$

Choose $\gamma = 1 / ((1 + \delta^{-1})C_E)$. Add Lemma A:

$$e_{k+1}^2 + \gamma\,\eta_{k+1}^2 \le e_k^2 - E_k^2 + \gamma(1 + \delta)(1 - \lambda\theta)\,\eta_k^2 + E_k^2 = e_k^2 + \gamma(1 + \delta)(1 - \lambda\theta)\,\eta_k^2.$$

The term $E_k^2$ cancels, which is the reason for this choice of $\gamma$. Fix $\delta > 0$ so small that $q = (1 + \delta)(1 - \lambda\theta) < 1$, which is possible because $\lambda\theta > 0$. For $\beta \in (0, 1)$, reliability gives $e_k^2 \le (1 - \beta)e_k^2 + \beta C_{\mathrm{rel}}^2\eta_k^2$. So

$$e_{k+1}^2 + \gamma\,\eta_{k+1}^2 \le (1 - \beta)\,e_k^2 + \gamma\Bigl(q + \frac{\beta C_{\mathrm{rel}}^2}{\gamma}\Bigr)\eta_k^2.$$

Choose $\beta$ so small that $q + \beta C_{\mathrm{rel}}^2 / \gamma < 1$. Then $\alpha^2 = \max(1 - \beta,\ q + \beta C_{\mathrm{rel}}^2/\gamma) < 1$ works. All constants depend only on $\theta$, $C_{\mathrm{rel}}$ and $C_E$, and so only on $\theta$ and the similarity classes of $\mathcal{T}_0$. $\square$

**What the proof does not give.** Contraction gives linear convergence in the number of steps, not a rate in the number of unknowns. The rate $(\#\mathcal{T}_k)^{-s}$ needs two more facts, the optimal marking lemma and the closure estimate of NVB. They are on the [AFEM optimality theorem](/afem-optimality-theorem/) page. The proof also does not cover an inexact solve, which breaks Lemma A, or a quadrature rule that is not exact for $f$, which breaks Galerkin orthogonality and the sum over children in Lemma B. With conjugate gradients stopped at a tolerance, as in the code, the claims hold up to the solver error.
