---
title: The GLL rule is exact to degree 2N-1, so the stiffness is exact and the mass is diagonal, and the assembled system has a unique solution
proves: [correctness]
status: full
---

**Setting.** The problem is $-u'' + cu = f$ on $(a, b)$ with $u(a) = u(b) = 0$ and a constant $c \ge 0$. The interval is cut into elements $K_e$ of length $h_e$. On $[-1, 1]$, the GLL nodes of degree $N \ge 1$ are $\xi_0 = -1 < \xi_1 < \cdots < \xi_N = 1$, where $\xi_1, \ldots, \xi_{N-1}$ are the roots of $P_N'$, and $\ell_0, \ldots, \ell_N$ are the Lagrange polynomials of degree $N$ on these nodes. The weights are $w_j = \int_{-1}^{1}\ell_j$. The discrete space $V_N$ is the set of continuous functions that are 0 at $a$ and $b$ and are polynomials of degree at most $N$ on each element, stored by their values at the mapped nodes. SEM-1D is lines L1 to L6 of the main page.

We prove four claims.

1. *(Exactness of the rule.)* $\sum_j w_j q(\xi_j) = \int_{-1}^1 q$ for every polynomial $q$ of degree at most $2N - 1$.
2. *(Stiffness and mass.)* The matrix $(2/h)D^{\mathsf T}\operatorname{diag}(w)D$ at line L3 equals the exact element stiffness $\int_{K}\phi_i'\phi_j'\,dx$, and the GLL mass $(h/2)\operatorname{diag}(w)$ is the exact mass matrix with each row summed onto the diagonal.
3. *(The derivative matrix.)* $D_{ij} = \ell_j'(\xi_i)$, so $Dv$ is the exact derivative at the nodes of the polynomial with node values $v$.
4. *(Unique solution.)* The assembled system at line L5 is symmetric positive definite, so it has exactly one solution, and this solution is the $u_N \in V_N$ with $\int u_N'v' + c(u_N, v)_N = (f, v)_N$ for all $v \in V_N$, where $(\cdot, \cdot)_N$ is the GLL rule applied element by element.

**Proof of 1.** First, the rule is exact for degree at most $N$: such a $q$ equals its interpolant $\sum_j q(\xi_j)\ell_j$, and integrating gives $\sum_j q(\xi_j)w_j$. Now let $q$ have degree at most $2N - 1$, and let $\omega(x) = (1 - x^2)P_N'(x)$, of degree $N + 1$, which is 0 at all $N + 1$ nodes. Divide: $q = \omega s + r$ with $\deg s \le N - 2$ and $\deg r \le N$. The rule gives $\sum_j w_j r(\xi_j) = \int r$. For the other part, integrate by parts; the boundary term is 0 because $1 - x^2$ is 0 at $\pm 1$:
$$\int_{-1}^{1}(1 - x^2)P_N'\,s = -\int_{-1}^{1}P_N\,\big((1 - x^2)s\big)'.$$
The polynomial $((1 - x^2)s)'$ has degree at most $N - 1$, and $P_N$ is orthogonal to all such polynomials, so the integral is 0. The rule also gives 0 for $\omega s$. So the rule is exact for $q$. (If $N = 1$ there is no $s$ and the claim is the trapezoid rule for linear $q$.) $\square$

The code computes $w_j$ by the classical formula $w_j = 2/(N(N+1)P_N(\xi_j)^2)$, which equals $\int\ell_j$. The test file checks this for $N = 2, 4$ against the known values and checks the exactness of claim 1 for $N = 3, 6, 9$.

**Proof of 3.** For $i \ne j$, write $\ell_j(x) = \lambda_j\prod_{k \ne j}(x - \xi_k)$ with the barycentric weight $\lambda_j = 1/\prod_{k \ne j}(\xi_j - \xi_k)$. The product rule at $x = \xi_i$ leaves only the term in which the factor $(x - \xi_i)$ is differentiated: $\ell_j'(\xi_i) = \lambda_j\prod_{k \ne i, j}(\xi_i - \xi_k) = (\lambda_j/\lambda_i)/(\xi_i - \xi_j)$, which is the formula in the code. For $i = j$, the polynomials $\ell_j$ sum to 1, so their derivatives sum to 0 and $\ell_i'(\xi_i) = -\sum_{j \ne i}\ell_j'(\xi_i)$, which is the diagonal in the code. $\square$

**Proof of 2.** On $K$ with $x = x_K + h(\xi + 1)/2$, the basis is $\phi_i(x) = \ell_i(\xi)$, and $\phi_i' = (2/h)\ell_i'$. So the exact stiffness is $(2/h)\int_{-1}^{1}\ell_i'\ell_j'\,d\xi$. The integrand has degree $2N - 2 \le 2N - 1$, so by claim 1 it equals $(2/h)\sum_q w_q\ell_i'(\xi_q)\ell_j'(\xi_q) = (2/h)\sum_q w_qD_{qi}D_{qj}$ by claim 3, which is line L3. For the mass, the GLL rule gives $(h/2)\sum_q w_q\ell_i(\xi_q)\ell_j(\xi_q) = (h/2)w_i\delta_{ij}$, because $\ell_i(\xi_q) = \delta_{iq}$. The exact mass has row sums $(h/2)\sum_j\int\ell_i\ell_j = (h/2)\int\ell_i = (h/2)w_i$, because $\sum_j\ell_j = 1$. So the GLL mass is the row sum lumping of the exact mass. The exact mass itself is not diagonal, because $\ell_i\ell_j$ has degree $2N$, one more than claim 1 covers. $\square$

**Proof of 4.** Line L4 adds the element matrices into the rows and columns of the global node numbers, and neighbor elements share their end node, so the assembled matrix $A$ satisfies $v^{\mathsf T}Av = \int v'^2 + c\,(v, v)_N$ for the function $v \in V_N$ with node values $v$, by claim 2. Both terms are at least 0, because the weights $w_j = 2/(N(N+1)P_N(\xi_j)^2)$ are positive. If $v^{\mathsf T}Av = 0$ then $v' = 0$, so $v$ is constant, and $v(a) = 0$ gives $v = 0$. So $A$ restricted to the interior nodes at line L5 is symmetric positive definite, the solve has a unique solution, and the equations are the stated discrete weak form, with the load $(f, \phi_i)_N = (h/2)w_if(x_i)$ on each element. $\square$

**Remark on the rate.** The method is a Galerkin method with the integrals of the mass and the load replaced by the GLL rule. Strang's first lemma bounds the error by the best approximation error in $V_N$ plus the quadrature errors in the load and the mass, and for analytic $u$ and $f$ both decay like $\rho^{-N}$ for some $\rho > 1$ on a fixed mesh. Maday and Patera gave this analysis; the reference run shows maximum errors from $1.6 \times 10^{-2}$ at $N = 4$ to $2 \times 10^{-13}$ at $N = 14$ on one element.
