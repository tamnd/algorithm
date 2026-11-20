---
title: HDG local problems are uniquely solvable, the trace system is symmetric positive definite, and for k at least 1 the traces are exact at the nodes
proves: [correctness]
status: full
---

**Setting.** The problem is $-u'' = f$ on $(0, 1)$ with $u(0) = g_0$ and $u(1) = g_1$, written as $q + u' = 0$ and $q' = f$. The mesh has the nodes $x_e = eh$, $e = 0, \ldots, m$, $h = 1/m$, and the cells $K_j = (x_j, x_{j+1})$. On each cell $q$ and $u$ are polynomials of degree at most $k \ge 0$, and there is one trace value $\hat u_e$ at each node. On the boundary of a cell the outward normal is $n = -1$ at the left end and $n = +1$ at the right end, and $\sum_{\partial K} z$ means $z(x_j) + z(x_{j+1})$, with $n$ taken at the end where $z$ is evaluated. The numerical flux is $\hat q n = qn + \tau(u - \hat u)$ with a constant $\tau > 0$. The local problem on $K$ is: given $\hat u$ at the two ends of $K$, find $(q, u) \in \mathcal{P}_k(K)^2$ with

$$(q, r)_K - (u, r')_K + \textstyle\sum_{\partial K} \hat u\, r\, n = 0 \quad \text{for all } r \in \mathcal{P}_k(K), \tag{1}$$

$$-(q, w')_K + \textstyle\sum_{\partial K} \hat q n\, w = (f, w)_K \quad \text{for all } w \in \mathcal{P}_k(K). \tag{2}$$

The global equation at an interior node $x_e$ is that the two values of $\hat q n$ at $x_e$, one from $K_{e-1}$ and one from $K_e$, add up to $0$. The code writes it as the row $G_e(\hat u) = -(\hat q n|_{K_{e-1}} + \hat q n|_{K_e}) = 0$, and it fixes $\hat u_0 = g_0$ and $\hat u_m = g_1$.

**Claim 1 (local well-posedness).** For every $k \ge 0$ and $\tau > 0$ the local problem has exactly one solution for any data $\hat u$ and $f$.

*Proof.* The problem is a square linear system, so it is enough to show that $\hat u = 0$ and $f = 0$ give only $q = u = 0$. Take $r = q$ in (1) and $w = u$ in (2):

$$\|q\|_K^2 - (u, q')_K = 0, \qquad -(q, u')_K + \textstyle\sum_{\partial K}(qn + \tau u)u = 0.$$

Integration by parts gives $-(q, u')_K = (q', u)_K - \sum_{\partial K} q u n$, so the second equation is $(q', u)_K + \tau\sum_{\partial K} u^2 = 0$. The sum of the two equations is $\|q\|_K^2 + \tau\sum_{\partial K} u^2 = 0$. So $q = 0$ and $u = 0$ at both ends. Then (1) reads $(u, r')_K = 0$ for all $r \in \mathcal{P}_k$, that is, $u$ is orthogonal to $\mathcal{P}_{k-1}$. If $k = 0$, $u$ is a constant that is $0$ at an end, so $u = 0$. If $k \ge 1$, $u = cL_k$ where $L_k$ is the Legendre polynomial of degree $k$ moved to $K$, and $L_k = \pm 1$ at the ends, so $c = 0$. $\square$

**Claim 2 (what the code computes).** Lines L1 to L4 build the rows $G_e$ exactly, line L5 moves the boundary values to the right side, and lines L6 and L7 return the traces and the local solutions of the HDG equations.

*Proof.* In the basis $\xi^s$, $\xi = (x - x_j)/h$, the entries of the local matrix are $(\xi^s, \xi^i)_K = h/(i + s + 1)$ and $(\xi^s, (\xi^i)')_K = i/(i + s)$ for $i \ge 1$, and $\xi^i = 1$ at the right end and $[i = 0]$ at the left end. These are the entries that `local_matrix` writes, with the $qn$ and $\tau u$ parts of $\hat q n$ on the left side and the $\hat u$ parts on the right side, as `local_rhs` writes them. By Claim 1 the matrix is nonsingular, and since the problem is linear in $(\hat u_L, \hat u_R, f)$, the local solution is $\hat u_L s_L + \hat u_R s_R + s_f$ with the three columns that line L2 computes. So at each end $\hat q n$ is affine in $(\hat u_L, \hat u_R)$ with the coefficients of line L3, in which $-\tau$ is the $-\tau\hat u$ part of the flux. Line L4 adds $-\hat q n$ of the right end of $K_j$ to row $j + 1$ and $-\hat q n$ of its left end to row $j$, so row $e$ is $G_e$, in the tridiagonal arrays because $\hat q n$ on $K_j$ depends only on $\hat u_j$ and $\hat u_{j+1}$. Line L5 is the usual elimination of known values, line L6 solves the interior rows, and line L7 forms the local solutions from the stored columns. $\square$

**Claim 3 (the trace system is symmetric positive definite).** Let $f = 0$ and let $\hat u$, $\hat v$ be trace vectors that are $0$ at $x_0$ and $x_m$. Write $(q_{\hat u}, u_{\hat u})$ for the local solutions with traces $\hat u$. Then

$$\sum_{e=1}^{m-1}\hat v_e G_e(\hat u) = \sum_j\Bigl((q_{\hat u}, q_{\hat v})_{K_j} + \tau\textstyle\sum_{\partial K_j}(u_{\hat u} - \hat u)(u_{\hat v} - \hat v)\Bigr).$$

So the matrix $S$ of the rows $G_1, \ldots, G_{m-1}$ is symmetric, and it is positive definite for all $k \ge 0$ and $\tau > 0$.

*Proof.* Since $\hat v = 0$ at the boundary nodes, the left side is $-\sum_j\sum_{\partial K_j}\hat q n(\hat u)\,\hat v$. Fix a cell $K$. Test (1) for $\hat v$ with $r = q_{\hat u}$: $(q_{\hat v}, q_{\hat u})_K - (u_{\hat v}, q_{\hat u}')_K + \sum_{\partial K}\hat v q_{\hat u} n = 0$. Test (2) for $\hat u$ with $w = u_{\hat v}$ and integrate by parts as in Claim 1: $(q_{\hat u}', u_{\hat v})_K + \tau\sum_{\partial K}(u_{\hat u} - \hat u)u_{\hat v} = 0$. Eliminating $(q_{\hat u}', u_{\hat v})_K$ gives

$$-\textstyle\sum_{\partial K} q_{\hat u} n\,\hat v = (q_{\hat u}, q_{\hat v})_K + \tau\sum_{\partial K}(u_{\hat u} - \hat u)u_{\hat v}.$$

Now $-\hat q n(\hat u)\hat v = -q_{\hat u}n\hat v - \tau(u_{\hat u} - \hat u)\hat v$, and the sum over the two ends gives the cell term of the identity. The right side is symmetric in $\hat u$ and $\hat v$, so $S$ is symmetric. With $\hat v = \hat u$ it is $\sum_j\bigl(\|q_{\hat u}\|_{K_j}^2 + \tau\sum_{\partial K_j}(u_{\hat u} - \hat u)^2\bigr) \ge 0$. If it is $0$, then $q_{\hat u} = 0$ on every cell, and (1) with $r = 1$ gives $(q_{\hat u}, 1)_K + \hat u_R - \hat u_L = 0$, so $\hat u_R = \hat u_L$ on every cell. Then $\hat u$ is constant, and $\hat u_0 = 0$ makes it $0$. $\square$

**Claim 4 (end fluxes for $k \ge 1$).** If $k \ge 1$, the end fluxes of the local solution on $K_j$ are

$$\hat q n\big|_{x_j} = (f, \psi_L)_{K_j} - \frac{\hat u_j - \hat u_{j+1}}{h}, \qquad \hat q n\big|_{x_{j+1}} = (f, \psi_R)_{K_j} - \frac{\hat u_{j+1} - \hat u_j}{h},$$

with $\psi_L = 1 - \xi$ and $\psi_R = \xi$, for every $\tau > 0$.

*Proof.* Equation (1) with $r = 1$ gives $(q, 1)_K = \hat u_L - \hat u_R$. Since $k \ge 1$, $\psi_R \in \mathcal{P}_k$ is allowed in (2). It is $0$ at the left end, $1$ at the right end, and $\psi_R' = 1/h$, so (2) gives $-(q, 1)_K/h + \hat q n|_R = (f, \psi_R)_K$, which is the second formula. In the same way $\psi_L$ is $1$ at the left end, $0$ at the right end, and $\psi_L' = -1/h$, which gives $(q, 1)_K/h + \hat q n|_L = (f, \psi_L)_K$, the first formula. $\square$

**Claim 5 (the trace system is the linear finite element system).** If $k \ge 1$, the row at an interior node is

$$G_e(\hat u) = \frac{2\hat u_e - \hat u_{e-1} - \hat u_{e+1}}{h} - (f, \phi_e),$$

where $\phi_e$ is the piecewise linear hat function of node $x_e$. So $S = \frac1h\operatorname{tridiag}(-1, 2, -1)$, independent of $k$ and $\tau$.

*Proof.* Add the right-end flux of $K_{e-1}$ and the left-end flux of $K_e$ from Claim 4 and change the sign. The functions $\psi_R$ on $K_{e-1}$ and $\psi_L$ on $K_e$ are the two halves of $\phi_e$. $\square$

**Claim 6 (exact traces for $k \ge 1$).** If $k \ge 1$ and $u \in H^2(0, 1)$ is the exact solution, then $\hat u_e = u(x_e)$ for every $e$, when the loads $(f, \xi^i)_K$ are integrated exactly.

*Proof.* For an interior node, $\phi_e \in H^1_0(0, 1)$, so the weak form gives $(u', \phi_e') = (f, \phi_e)$. On $K_{e-1}$, $\phi_e' = 1/h$, and on $K_e$, $\phi_e' = -1/h$, so $(u', \phi_e') = \frac1h\bigl(u(x_e) - u(x_{e-1})\bigr) - \frac1h\bigl(u(x_{e+1}) - u(x_e)\bigr)$. By Claim 5 the nodal values of $u$ satisfy every row $G_e = 0$, and they take the boundary values $g_0$ and $g_1$. By Claim 3 the system has only one solution. $\square$

The code integrates the loads with the five-point Boole rule, which is exact for polynomials of degree at most $5$. The traces depend on $f$ only through $(f, \phi_e)$, so they are exact when $f$ is a polynomial of degree at most $4$. For other $f$ the traces are the nodal values of the piecewise linear solution with the quadrature load.

**Claim 7 (polynomial reproduction).** If the exact solution $u$ is a polynomial of degree at most $k$ and the loads are exact, then the method returns $q = -u'$, $u$ on every cell and $\hat u_e = u(x_e)$.

*Proof.* Take $q = -u'$ and $\hat u = u$ at the nodes. Integration by parts gives (1), because $(q, r)_K = (u, r')_K - \sum_{\partial K} u r n$ and $\hat u = u$ at the ends, and it gives (2), because $u = \hat u$ at the ends makes $\hat q n = qn$ and $-(q, w')_K + \sum_{\partial K} q n w = (q', w)_K = (f, w)_K$. The global equations hold because $q$ is continuous at every node, so the two values of $\hat q n = qn$ have opposite signs. By Claim 3 the traces are unique, and by Claim 1 so are the local solutions. $\square$

**Conclusion.** By Claim 2 the code assembles the HDG trace equations, and by Claim 3 their matrix is symmetric positive definite for every $k \ge 0$ and $\tau > 0$. It is tridiagonal, and the Thomas algorithm in line L6 needs no pivoting for a symmetric positive definite tridiagonal matrix, so it finds the unique traces. By Claim 1 line L7 then gives the unique local solutions, and line L8 returns them. For $k \ge 1$ the traces are the exact nodal values (Claim 6), and polynomials of degree at most $k$ are reproduced exactly (Claim 7). $\blacksquare$
