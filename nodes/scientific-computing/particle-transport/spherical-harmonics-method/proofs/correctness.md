---
title: The slab P_N equations are hyperbolic with the Gauss nodes as speeds, their diamond difference form with Mark conditions is the S_(N+1) scheme, they conserve particles, P1 is diffusion, and their decay constants are those of S_(N+1)
proves: [correctness]
status: full
---

We assume exact arithmetic. The slab, the cross sections and the lines L1 to L6 are those of the page, $N$ is odd, $P_l$ is the Legendre polynomial of degree $l$, and $\phi_l = \int_{-1}^1 P_l\psi\,d\mu$. Scattering and the source are isotropic, and $\Sigma_{a,j} = \Sigma_{t,j} - \Sigma_{s,j}$. The vector $u = (\phi_0, \ldots, \phi_N)$ has the streaming matrix $A$ with $A_{l,l+1} = (l + 1)/(2l + 1)$ and $A_{l,l-1} = l/(2l + 1)$, and the collision matrix $S = \Sigma_tI - \Sigma_se_0e_0^{\mathsf T}$. Let $\mu_1, \ldots, \mu_{N+1}$ be the roots of $P_{N+1}$ and $w_k$ the Gauss-Legendre weights.

## The moment equations

**Lemma 1 (the moment equations).** If $\psi$ solves $\mu\,\partial_x\psi + \Sigma_t\psi = (\Sigma_s\phi_0 + q)/2$, then for every $l \ge 0$
$$\frac{l + 1}{2l + 1}\phi_{l+1}' + \frac{l}{2l + 1}\phi_{l-1}' + \Sigma_t\phi_l = (\Sigma_s\phi_0 + q)\,\delta_{l0}.$$
The $P_N$ equations $Au' + Su = qe_0$ are these equations for $l \le N$ with $\phi_{N+1}$ set to 0.

*Proof.* Multiply by $P_l$ and integrate over $\mu$. The recurrence $(2l + 1)\mu P_l = (l + 1)P_{l+1} + lP_{l-1}$ turns $\int \mu P_l\,\partial_x\psi\,d\mu$ into the first two terms. On the right, $\int_{-1}^1 P_l\,d\mu/2 = \delta_{l0}$. $\square$

The only approximation is $\phi_{N+1} = 0$: the flux is assumed to be a polynomial of degree $N$ in $\mu$.

**Theorem 2 (the speeds are the Gauss nodes).** $Ap(\mu_k) = \mu_kp(\mu_k)$ for $p(\mu) = (P_0(\mu), \ldots, P_N(\mu))$. So $A$ has the $N + 1$ distinct real eigenvalues $\mu_k$, it is diagonalizable, and the $P_N$ equations are a hyperbolic system. Half of the speeds are positive and half are negative.

*Proof.* Row $l$ of $Ap(\mu)$ is $((l + 1)P_{l+1}(\mu) + lP_{l-1}(\mu))/(2l + 1) = \mu P_l(\mu)$ for $l < N$. For $l = N$ the term with $P_{N+1}$ is missing from $A$, so the row is $\mu P_N(\mu) - \frac{N + 1}{2N + 1}P_{N+1}(\mu)$, which is $\mu P_N(\mu)$ at a root of $P_{N+1}$. The vectors $p(\mu_k)$ are not zero ($P_0 = 1$). The roots of $P_{N+1}$ are real, distinct and symmetric about 0, and 0 is not a root because $N + 1$ is even. $\square$

So each face has $(N + 1)/2$ incoming characteristics, and it needs $(N + 1)/2$ conditions, as lines L2 and L4 give.

## The link to discrete ordinates

Let $W$ be the matrix with the entries $W_{lk} = w_kP_l(\mu_k)$ and $V$ the matrix with $V_{kl} = \frac{2l + 1}{2}P_l(\mu_k)$. So $u = W\psi$ takes the values $\psi_k$ at the nodes to the moments, by the Gauss rule, and $\psi = Vu$ evaluates the $P_N$ expansion at the nodes.

**Lemma 3.** $WV = I$, $AW = WM$ with $M = \mathrm{diag}(\mu_k)$, and $Ve_0 = \tfrac12\mathbf 1$.

*Proof.* $(WV)_{lm} = \frac{2m + 1}{2}\sum_k w_kP_l(\mu_k)P_m(\mu_k)$. The degree of $P_lP_m$ is at most $2N \le 2(N + 1) - 1$, so the Gauss rule is exact, and the orthogonality $\int P_lP_m = \frac{2}{2l + 1}\delta_{lm}$ gives $\delta_{lm}$. The columns of $W$ are $w_kp(\mu_k)$, so Theorem 2 gives $AW = WM$. Finally $P_0 = 1$. $\square$

**Theorem 4 (P_N with Mark conditions is S_(N+1)).** Let the cell rows of line L3 be the diamond difference form
$$A\,\frac{u_{j+1} - u_j}{h_j} + S_j\,\frac{u_j + u_{j+1}}{2} = q_je_0$$
on the edge vectors $u_j$, and let each face be reflecting ($\phi_l = 0$ for odd $l$) or vacuum with the Mark conditions ($\psi(\mu_k) = 0$ at the face for the incoming nodes). Then $u_j$ solves these equations if and only if $\psi_j = Vu_j$ solves the diamond difference $S_{N+1}$ equations with the Gauss rule, zero incoming flux at vacuum faces and reflection, and then $\phi_0$ and the current $\phi_1$ are the scalar flux and the current of $S_{N+1}$. With $\Sigma_{s,j} < \Sigma_{t,j}$ in every cell, the system of line L5 has exactly one solution.

*Proof.* By Lemma 3, $V = W^{-1}$, $VA = MV$, and $VSu = \Sigma_tVu - \Sigma_s(Ve_0)u_0 = \Sigma_t\psi - \tfrac12\Sigma_s\phi_0\mathbf 1$. Multiply the cell rows by $V$:
$$\mu_k\,\frac{\psi_{k,j+1} - \psi_{k,j}}{h_j} + \Sigma_{t,j}\,\frac{\psi_{k,j} + \psi_{k,j+1}}{2} = \frac{\Sigma_{s,j}\bar\phi_{0,j} + q_j}{2},$$
where $\bar\phi_{0,j}$ is the mean of the edge values of $\phi_0 = \sum_kw_k\psi_k$. This is the diamond difference $S_{N+1}$ scheme, with the cell value equal to the mean of the edge values. The Mark rows are $(Vu)_k = 0$ for the incoming nodes, which is zero incoming flux. At a reflecting face, since $P_l(-\mu) = (-1)^lP_l(\mu)$, $\psi(\mu_k) - \psi(-\mu_k) = 2\sum_{l\ \mathrm{odd}}\frac{2l + 1}{2}\phi_lP_l(\mu_k)$. If all odd $\phi_l$ vanish, the face reflects. Conversely, if this is 0 for all $\mu_k > 0$, the odd polynomial $\sum_{l\ \mathrm{odd}}\frac{2l + 1}{2}\phi_lP_l$ of degree at most $N$ has the $N + 2$ roots $0$ and $\pm\mu_k$, so it is zero, and every odd $\phi_l$ is 0. Since $V$ is invertible, the two systems have the same solutions, and $\phi_1 = \sum_kw_k\mu_k\psi_k$ is the current. The source iteration proof shows that the diamond difference $S_{N+1}$ equations with vacuum or reflecting faces have exactly one solution when $\Sigma_{s,j} < \Sigma_{t,j}$ in every cell. $\square$

So in a slab, $P_N$ adds nothing that $S_{N+1}$ does not have. The difference is in the solver: line L5 solves the coupled system directly, with no source iteration, so its cost does not depend on $c$.

## Conservation and the low orders

**Theorem 5 (balance).** For any face conditions, the solution of lines L1 to L5 satisfies
$$\text{leak}_{\text{left}} + \text{leak}_{\text{right}} + \sum_j \Sigma_{a,j}\bar\phi_{0,j}h_j = \sum_j q_jh_j,$$
with $\text{leak}_{\text{right}} = \phi_1$ at $x = L$ and $\text{leak}_{\text{left}} = -\phi_1$ at $x = 0$.

*Proof.* Row $l = 0$ of cell $j$ is $(\phi_{1,j+1} - \phi_{1,j})/h_j + \Sigma_{a,j}\bar\phi_{0,j} = q_j$, since $A_{0,1} = 1$ and $S_{00} = \Sigma_a$. Multiply by $h_j$ and sum over the cells; the sum of the differences telescopes to $\phi_1(L) - \phi_1(0)$. $\square$

**Theorem 6 (P1 is diffusion).** For $N = 1$ the equations are $\phi_1' + \Sigma_a\phi_0 = q$ and $\tfrac13\phi_0' + \Sigma_t\phi_1 = 0$, which is the balance with Fick's law $\phi_1 = -D\phi_0'$, $D = 1/(3\Sigma_t)$. The Marshak condition at $x = 0$ is $\phi_1 = -\phi_0/2$, and the Mark condition is $\phi_1 = -\phi_0/\sqrt3$. The diamond difference P1 system with Marshak faces is the edge system of consistent [diffusion synthetic acceleration](/diffusion-synthetic-acceleration/).

*Proof.* The equations are rows 0 and 1 of Lemma 1. With $\psi = \phi_0/2 + 3\phi_1\mu/2$, the Marshak condition $\int_0^1 P_1\psi\,d\mu = \phi_0/4 + \phi_1/2 = 0$ gives $\phi_1 = -\phi_0/2$, and the Mark condition $\psi(1/\sqrt3) = \phi_0/2 + \sqrt3\phi_1/2 = 0$ gives $\phi_1 = -\phi_0/\sqrt3$. The cell rows are the equations (2) of the proof of diffusion synthetic acceleration with the source $q$, and Theorem 2 of that proof eliminates the current. $\square$

So the two conditions place the zero of the linear extrapolation of $\phi_0$ at the distances $2D = 0.6667/\Sigma_t$ (Marshak) and $\sqrt3D = 0.5774/\Sigma_t$ (Mark) outside the face; the exact Milne value is $0.7104/\Sigma_t$.

## Decay constants

**Theorem 7 (the infinite medium modes).** Let $\Sigma_t = 1$ and $0 \le c < 1$. The $P_N$ equations have a solution $u = ve^{-\kappa x}$ with $v \ne 0$ if and only if $\det(S - \kappa A) = 0$, and
$$\det(S - \kappa A) = \prod_{k=1}^{N+1}(1 - \kappa\mu_k)\left[1 - \frac c2\sum_{k=1}^{N+1}\frac{w_k}{1 - \kappa^2\mu_k^2}\right],$$
which is, up to the factor in front, the dispersion function of $S_{N+1}$. On $0 \le \kappa < 1/\mu_{\max}$ it has exactly one root, the decay constant of the slowest mode, and bisection on the determinant finds it. For $N = 1$ the root is $\kappa = \sqrt{3(1 - c)}$.

*Proof.* Substituting $u = ve^{-\kappa x}$ gives $(S - \kappa A)v = 0$. By Lemma 3, $V(S - \kappa A)W = I - \kappa M - \tfrac c2\mathbf 1w^{\mathsf T}$, where $w$ is the vector of weights (row 0 of $W$). The matrix determinant lemma gives $\det(I - \kappa M)\,(1 - \tfrac c2w^{\mathsf T}(I - \kappa M)^{-1}\mathbf 1)$, and $\det V\det W = 1$. Pair the nodes $\pm\mu$: $\frac{w}{1 - \kappa\mu} + \frac{w}{1 + \kappa\mu} = \frac{2w}{1 - \kappa^2\mu^2}$, so the bracket is the one shown. For $0 \le \kappa < 1/\mu_{\max}$ the product is positive, and the bracket decreases strictly from $1 - c > 0$ to $-\infty$, so it has exactly one zero, where the determinant changes sign. For $N = 1$, $\mu = \pm1/\sqrt3$ and $w = 1$, so the bracket is $1 - c/(1 - \kappa^2/3)$, which is 0 at $\kappa^2 = 3(1 - c)$. $\square$

The implementation evaluates $\det(S - \kappa A)$ by the three-term recurrence of a tridiagonal determinant, $D_l = S_{ll}D_{l-1} - \kappa^2\frac{l^2}{(2l + 1)(2l - 1)}D_{l-2}$. As $N \to \infty$, the Gauss sum tends to $\frac c2\int_{-1}^1\frac{d\mu}{1 - \kappa^2\mu^2} = \frac{c}{2\kappa}\ln\frac{1 + \kappa}{1 - \kappa}$, whose zero of $1 - (\cdot)$ is the decay constant of exact transport, because the integrand is analytic on $[-1, 1]$ for $\kappa < 1$.
